#!/usr/bin/env python3
"""Run deterministic responsive-browser QA for the cumulative Chapter 14 reader.

The script serves the already-built HTML tree from localhost, launches a
system Chromium browser through Playwright, checks the five established reader
viewports, and exercises one complete Chapter 14 staged disclosure.  It does
not build or modify the reader.  Its only output is the JSON QA receipt.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import threading
import urllib.request
from datetime import date
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SURFACE = ROOT / "output/chapters01-14-html"
DEFAULT_OUTPUT = ROOT / "qa/CHAPTER14_BROWSER_QA.json"
VIEWPORTS = ((1440, 900), (1280, 900), (1024, 900), (768, 900), (390, 900))

ROOT_PAGE = "frontmatter-1.html"
BOOK_PAGE = "o003-c90-chapters-01-14-reader.html"
CHAPTER_PAGE = "chap_continuity_topology.html"
COMPANION_PAGE = "o003-c90-ch14-companion.html"
GUIDES_PAGE = "o003-c90-ch14-source-guides-a.html"
EDITION_NOTE_PAGE = "o003-c90-ch14-edition-note.html"
GUIDE_ID = "o003-c90-ch14-guide-01"

EVIDENCE_PATHS = (
    ROOT / "qa/CHAPTER14_HTML_MANIFEST.json",
    ROOT / "qa/CHAPTER14_HTML_QA.json",
    ROOT / "qa/CHAPTER14_COMPANION_QA.json",
)

SYSTEM_BROWSERS = (
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
)


class QuietHandler(SimpleHTTPRequestHandler):
    """Serve exact local bytes without writing an HTTP access log."""

    def log_message(self, _format: str, *args: object) -> None:
        del args


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--surface",
        type=Path,
        default=DEFAULT_SURFACE,
        help="Already-built cumulative Chapter 14 HTML directory.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="JSON receipt to write after the bounded browser run.",
    )
    parser.add_argument(
        "--browser-executable",
        type=Path,
        help="Chromium-family executable; defaults to installed Edge, then Chrome.",
    )
    parser.add_argument(
        "--checked-at",
        default=date.today().isoformat(),
        help="Receipt date (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=45_000,
        help="Navigation and interaction timeout in milliseconds.",
    )
    return parser.parse_args()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative_to_root(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def load_json(path: Path, failures: list[str]) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"cannot read {relative_to_root(path)}: {exc}")
        return {}
    if not isinstance(payload, dict):
        failures.append(f"{relative_to_root(path)} does not contain a JSON object")
        return {}
    return payload


def select_browser(requested: Path | None) -> Path:
    if requested is not None:
        candidate = requested.expanduser().resolve()
        if not candidate.is_file():
            raise FileNotFoundError(f"browser executable does not exist: {candidate}")
        return candidate
    for candidate in SYSTEM_BROWSERS:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        "no installed Edge/Chrome executable found; pass --browser-executable"
    )


def start_server(surface: Path) -> tuple[ThreadingHTTPServer, threading.Thread, str]:
    handler = partial(QuietHandler, directory=str(surface))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address[:2]
    return server, thread, f"http://{host}:{port}"


def rounded(value: float) -> int | float:
    nearest = round(value)
    return int(nearest) if abs(value - nearest) < 0.001 else round(value, 3)


def collect_geometry(page: Any) -> dict[str, Any]:
    raw = page.evaluate(
        """
        () => {
          const doc = document.documentElement;
          const main = document.querySelector('.ptx-page > .ptx-main');
          const content = main && (
            main.querySelector(':scope > .ptx-content') ||
            main.querySelector('#ptx-content')
          );
          if (!main || !content) {
            throw new Error('missing .ptx-main or .ptx-content');
          }
          const mr = main.getBoundingClientRect();
          const cr = content.getBoundingClientRect();
          return {
            htmlLang: doc.lang,
            xmlLang: doc.getAttribute('xml:lang'),
            clientWidth: doc.clientWidth,
            scrollWidth: doc.scrollWidth,
            mainLeft: mr.left,
            mainWidth: mr.width,
            mainRight: mr.right,
            contentLeft: cr.left,
            contentWidth: cr.width,
            contentRight: cr.right
          };
        }
        """
    )
    return {
        "html_language": raw["htmlLang"],
        "xml_language": raw["xmlLang"],
        "document_client_width": rounded(raw["clientWidth"]),
        "document_scroll_width": rounded(raw["scrollWidth"]),
        "main_left": rounded(raw["mainLeft"]),
        "main_width": rounded(raw["mainWidth"]),
        "main_right": rounded(raw["mainRight"]),
        "content_left": rounded(raw["contentLeft"]),
        "content_width": rounded(raw["contentWidth"]),
        "content_right": rounded(raw["contentRight"]),
    }


def geometry_checks(
    metrics: dict[str, Any], viewport_width: int
) -> tuple[dict[str, bool], dict[str, float]]:
    client = float(metrics["document_client_width"])
    scroll = float(metrics["document_scroll_width"])
    main_left = float(metrics["main_left"])
    main_width = float(metrics["main_width"])
    main_right = float(metrics["main_right"])
    content_left = float(metrics["content_left"])
    content_width = float(metrics["content_width"])
    content_right = float(metrics["content_right"])

    left_gap = content_left - main_left
    right_gap = main_right - content_right
    centering_delta = abs(left_gap - right_gap)
    expected_main_min = client - (242 if viewport_width >= 800 else 2)
    readable_min = min(960.0, main_width * 0.75)
    readable_max = min(962.0, main_width + 2)

    checks = {
        "language_id_ID": metrics["html_language"] == "id-ID",
        "no_horizontal_overflow": scroll <= client + 1,
        "main_inside_document": main_left >= -1 and main_right <= client + 1,
        "main_fills_available_width": main_width >= expected_main_min,
        "readable_measure_fills_main": content_width + 1 >= readable_min,
        "readable_measure_not_overwide": content_width <= readable_max,
        "readable_measure_centered": centering_delta <= 4,
    }
    derived = {
        "content_left_gap": rounded(left_gap),
        "content_right_gap": rounded(right_gap),
        "centering_delta": rounded(centering_delta),
        "content_to_main_ratio": round(content_width / main_width, 4),
    }
    return checks, derived


def new_page(
    browser: Any,
    width: int,
    height: int,
    timeout_ms: int,
    console_events: list[dict[str, str]],
    page_errors: list[dict[str, str]],
) -> tuple[Any, Any]:
    context = browser.new_context(viewport={"width": width, "height": height})
    page = context.new_page()
    page.set_default_timeout(timeout_ms)
    page.set_default_navigation_timeout(timeout_ms)
    page.on(
        "console",
        lambda message: console_events.append(
            {"type": message.type, "text": message.text, "url": page.url}
        ),
    )
    page.on(
        "pageerror",
        lambda error: page_errors.append({"text": str(error), "url": page.url}),
    )
    return context, page


def open_surface(page: Any, url: str) -> None:
    page.goto(url, wait_until="load")
    page.locator("#ptx-content").wait_for(state="visible")
    page.wait_for_timeout(250)


def inspect_identity(page: Any) -> dict[str, Any]:
    return page.evaluate(
        """
        () => {
          const text = (selector) => {
            const node = document.querySelector(selector);
            return node ? node.innerText.trim().replace(/\\s+/g, ' ') : null;
          };
          const countHref = (href) =>
            document.querySelectorAll(`a[href="${href}"]`).length;
          const allHrefs = Array.from(document.querySelectorAll('a[href]'))
            .map((node) => node.getAttribute('href') || '');
          return {
            language: document.documentElement.lang,
            bookHeading: text('.ptx-masthead h1.heading'),
            contentHeading: text('#ptx-content h1, #ptx-content h2'),
            bookLink: document.querySelector('.ptx-masthead h1.heading a')
              ?.getAttribute('href') || null,
            rootLinkCount: countHref('o003-c90-chapters-01-14-reader.html'),
            chapterLinkCount: countHref('chap_continuity_topology.html'),
            companionLinkCount: countHref('o003-c90-ch14-companion.html'),
            editionNoteLinkCount: countHref('o003-c90-ch14-edition-note.html'),
            legacyChapter13Links: allHrefs.filter((href) =>
              href.includes('chapters-01-13-reader') ||
              href.includes('ch13-edition-note')
            ).length
          };
        }
        """
    )


def add_failed_checks(
    failures: list[str], label: str, checks: dict[str, bool]
) -> None:
    for name, passed in checks.items():
        if not passed:
            failures.append(f"{label}: {name} failed")


def check_page_geometry(
    browser: Any,
    base_url: str,
    path: str,
    width: int,
    height: int,
    timeout_ms: int,
    console_events: list[dict[str, str]],
    page_errors: list[dict[str, str]],
    failures: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    context, page = new_page(
        browser, width, height, timeout_ms, console_events, page_errors
    )
    try:
        open_surface(page, f"{base_url}/{path}")
        metrics = collect_geometry(page)
        checks, derived = geometry_checks(metrics, width)
        add_failed_checks(failures, f"{path}@{width}x{height}", checks)
        return {
            "width": width,
            "height": height,
            **metrics,
            **derived,
            "checks": checks,
            "status": "pass" if all(checks.values()) else "fail",
        }, inspect_identity(page)
    except Exception as exc:  # Playwright supplies operation-specific detail.
        failures.append(f"{path}@{width}x{height}: {exc}")
        return {
            "width": width,
            "height": height,
            "checks": {},
            "status": "fail",
            "error": str(exc),
        }, {}
    finally:
        context.close()


def exercise_staged_disclosure(
    browser: Any,
    base_url: str,
    timeout_ms: int,
    console_events: list[dict[str, str]],
    page_errors: list[dict[str, str]],
    failures: list[str],
) -> dict[str, Any]:
    width, height = 390, 900
    context, page = new_page(
        browser, width, height, timeout_ms, console_events, page_errors
    )
    checked: list[str] = []
    active_controls: list[str] = []
    output: dict[str, Any] = {
        "exercise": GUIDE_ID,
        "page": GUIDES_PAGE,
        "viewport": {"width": width, "height": height},
    }
    try:
        open_surface(page, f"{base_url}/{GUIDES_PAGE}")
        if page.locator(f"article#{GUIDE_ID}").count() != 1:
            raise AssertionError(f"expected exactly one collapsed article #{GUIDE_ID}")
        checked.append("collapsed exercise")
        page.locator(f"article#{GUIDE_ID} > a[data-knowl]").click()
        page.locator(f"#{GUIDE_ID}-hint:visible").wait_for(state="visible")
        checked.append("statement expansion")

        expected_controls = (
            (f"{GUIDE_ID}-hint", "Petunjuk."),
            (f"{GUIDE_ID}-answer", "Jawaban."),
            (f"{GUIDE_ID}-solution", "Solusi."),
        )
        for control_id, expected_label in expected_controls:
            locator = page.locator(f"#{control_id}:visible")
            locator.wait_for(state="visible")
            label = " ".join(locator.inner_text().split())
            active_controls.append(label)
            if label != expected_label:
                failures.append(
                    f"{GUIDES_PAGE}: #{control_id} label {label!r}, "
                    f"expected {expected_label!r}"
                )
            visible_before = page.locator("div.knowl-output:visible").count()
            locator.click()
            page.wait_for_function(
                "expected => Array.from(document.querySelectorAll('div.knowl-output'))"
                ".filter(node => node.getClientRects().length > 0).length >= expected",
                arg=visible_before + 1,
            )
            checked.append(expected_label.rstrip(".").lower() + " expansion")

        metrics = collect_geometry(page)
        checks, derived = geometry_checks(metrics, width)
        add_failed_checks(failures, f"{GUIDES_PAGE} expanded@390x900", checks)
        visible_outputs = page.locator("div.knowl-output:visible").count()
        if visible_outputs < 4:
            failures.append(
                f"{GUIDES_PAGE}: only {visible_outputs} visible knowl outputs; expected 4"
            )
        output.update(
            {
                "checked": checked,
                "active_controls": active_controls,
                "visible_outputs_after_expansion": visible_outputs,
                **metrics,
                **derived,
                "checks": checks,
                "status": "pass"
                if all(checks.values()) and visible_outputs >= 4
                else "fail",
            }
        )
    except Exception as exc:
        failures.append(f"{GUIDES_PAGE} staged disclosure: {exc}")
        output.update({"checked": checked, "active_controls": active_controls})
        output.update({"status": "fail", "error": str(exc)})
    finally:
        context.close()
    return output


def validate_identity(
    root: dict[str, Any],
    chapter: dict[str, Any],
    companion: dict[str, Any],
    failures: list[str],
) -> dict[str, Any]:
    root_heading = root.get("bookHeading") or ""
    chapter_heading = chapter.get("contentHeading") or ""
    companion_heading = companion.get("contentHeading") or ""
    checks = {
        "root_language_id_ID": root.get("language") == "id-ID",
        "root_book_link_exact": root.get("bookLink") == BOOK_PAGE,
        "root_heading_names_chapters_01_14": "Bab 1-14" in root_heading,
        "root_exposes_chapter_14": int(root.get("chapterLinkCount") or 0) > 0,
        "root_exposes_companion": int(root.get("companionLinkCount") or 0) > 0,
        "root_exposes_edition_note": int(root.get("editionNoteLinkCount") or 0) > 0,
        "no_chapter_13_only_links": int(root.get("legacyChapter13Links") or 0) == 0,
        "chapter_language_id_ID": chapter.get("language") == "id-ID",
        "chapter_book_link_exact": chapter.get("bookLink") == BOOK_PAGE,
        "chapter_heading_is_chapter_14": "Bab 14" in chapter_heading,
        "chapter_heading_names_continuity": "kekontinuan" in chapter_heading.lower(),
        "chapter_navigates_to_companion": int(chapter.get("companionLinkCount") or 0) > 0,
        "companion_language_id_ID": companion.get("language") == "id-ID",
        "companion_book_link_exact": companion.get("bookLink") == BOOK_PAGE,
        "companion_heading_is_indonesian": (
            "panduan belajar mandiri" in companion_heading.lower()
        ),
    }
    add_failed_checks(failures, "Chapter 14 identity/navigation", checks)
    return {
        "book_heading": root_heading,
        "book_link": root.get("bookLink"),
        "edition_note_link": EDITION_NOTE_PAGE,
        "chapter_heading": chapter_heading,
        "chapter_page": CHAPTER_PAGE,
        "companion_heading": companion_heading,
        "companion_page": COMPANION_PAGE,
        "checks": checks,
        "status": "pass" if all(checks.values()) else "fail",
    }


def evidence_records(failures: list[str]) -> tuple[list[dict[str, Any]], str | None]:
    records: list[dict[str, Any]] = []
    canonical_manifest_sha: str | None = None
    for path in EVIDENCE_PATHS:
        if not path.is_file():
            failures.append(f"missing evidence file: {relative_to_root(path)}")
            continue
        records.append(
            {
                "path": relative_to_root(path),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
        payload = load_json(path, failures)
        if path.name == "CHAPTER14_HTML_MANIFEST.json":
            canonical_manifest_sha = payload.get("canonical_manifest_sha256")
            if not canonical_manifest_sha:
                failures.append(
                    "CHAPTER14_HTML_MANIFEST.json lacks canonical_manifest_sha256"
                )
        elif payload.get("status") != "pass":
            failures.append(f"{relative_to_root(path)} status is not pass")
    return records, canonical_manifest_sha


def static_closure(failures: list[str]) -> dict[str, Any]:
    path = ROOT / "qa/CHAPTER14_COMPANION_QA.json"
    payload = load_json(path, failures)
    observed = {
        "source_prompt_entries": payload.get("source_prompt_total"),
        "mastery_entries": payload.get("mastery_total"),
        "staged_surfaces": payload.get("staged_surface_total"),
        "grouping_nodes": payload.get("grouping_node_total"),
    }
    expected = {
        "source_prompt_entries": 81,
        "mastery_entries": 8,
        "staged_surfaces": 356,
        "grouping_nodes": 3,
    }
    passed = payload.get("status") == "pass" and observed == expected
    if not passed:
        failures.append(
            f"Chapter 14 static companion closure mismatch: observed {observed}, "
            f"expected {expected}"
        )
    return {
        **observed,
        "source": "qa/CHAPTER14_COMPANION_QA.json and generated companion HTML controls",
        "status": "pass" if passed else "fail",
    }


def main() -> int:
    args = parse_args()
    surface = args.surface.resolve()
    output_path = args.output.resolve()
    failures: list[str] = []

    required_pages = (ROOT_PAGE, BOOK_PAGE, CHAPTER_PAGE, COMPANION_PAGE, GUIDES_PAGE)
    if not surface.is_dir():
        failures.append(f"HTML surface does not exist: {surface}")
    else:
        for relative in required_pages:
            if not (surface / relative).is_file():
                failures.append(f"missing generated HTML surface: {relative}")

    evidence, canonical_manifest_sha = evidence_records(failures)
    closure = static_closure(failures)

    receipt: dict[str, Any] = {
        "schema_version": 3,
        "checked_at": args.checked_at,
        "status": "fail",
        "surface": relative_to_root(surface),
        "canonical_html_manifest_sha256": canonical_manifest_sha,
        "language": "id-ID",
    }

    if failures:
        receipt.update(
            {
                "staged_disclosures": {"static_closure": closure},
                "evidence": evidence,
                "failures": failures,
            }
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        return 1

    try:
        browser_executable = select_browser(args.browser_executable)
    except FileNotFoundError as exc:
        failures.append(str(exc))
        receipt.update(
            {
                "staged_disclosures": {"static_closure": closure},
                "evidence": evidence,
                "failures": failures,
            }
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        return 1

    local_root = (surface / ROOT_PAGE).read_bytes()
    server, thread, base_url = start_server(surface)
    console_events: list[dict[str, str]] = []
    page_errors: list[dict[str, str]] = []
    viewport_results: list[dict[str, Any]] = []
    root_identity: dict[str, Any] = {}
    chapter_identity: dict[str, Any] = {}
    companion_identity: dict[str, Any] = {}
    browser_version: str | None = None

    try:
        with urllib.request.urlopen(f"{base_url}/{ROOT_PAGE}", timeout=10) as response:
            served_root = response.read()
        served_identity = {
            "path": ROOT_PAGE,
            "local_bytes": len(local_root),
            "served_bytes": len(served_root),
            "local_sha256": sha256_bytes(local_root),
            "served_sha256": sha256_bytes(served_root),
        }
        if local_root != served_root:
            failures.append("localhost-served root bytes differ from the built root bytes")

        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise RuntimeError(
                "Python Playwright is unavailable in the selected interpreter"
            ) from exc

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True,
                executable_path=str(browser_executable),
                args=["--disable-gpu", "--no-first-run"],
            )
            try:
                browser_version = browser.version
                for width, height in VIEWPORTS:
                    row, identity = check_page_geometry(
                        browser,
                        base_url,
                        ROOT_PAGE,
                        width,
                        height,
                        args.timeout_ms,
                        console_events,
                        page_errors,
                        failures,
                    )
                    viewport_results.append(row)
                    if width == 1440:
                        root_identity = identity

                chapter_row, chapter_identity = check_page_geometry(
                    browser,
                    base_url,
                    CHAPTER_PAGE,
                    1440,
                    900,
                    args.timeout_ms,
                    console_events,
                    page_errors,
                    failures,
                )
                companion_row, companion_identity = check_page_geometry(
                    browser,
                    base_url,
                    COMPANION_PAGE,
                    390,
                    900,
                    args.timeout_ms,
                    console_events,
                    page_errors,
                    failures,
                )
                disclosure = exercise_staged_disclosure(
                    browser,
                    base_url,
                    args.timeout_ms,
                    console_events,
                    page_errors,
                    failures,
                )
            finally:
                browser.close()

        semantics = validate_identity(
            root_identity, chapter_identity, companion_identity, failures
        )
        console_errors = [event for event in console_events if event["type"] == "error"]
        console_warnings = [
            event for event in console_events if event["type"] == "warning"
        ]
        if console_errors:
            failures.append(f"browser emitted {len(console_errors)} console error(s)")
        if page_errors:
            failures.append(f"browser emitted {len(page_errors)} uncaught page error(s)")

        receipt.update(
            {
                "served_root_byte_identity": served_identity,
                "browser": {
                    "engine": "Playwright Chromium",
                    "executable": str(browser_executable),
                    "version": browser_version,
                },
                "viewports": viewport_results,
                "surfaces_checked": [
                    f"{ROOT_PAGE} at 1440, 1280, 1024, 768, and 390 pixels",
                    f"{CHAPTER_PAGE} at 1440 pixels",
                    f"{COMPANION_PAGE} at 390 pixels",
                    f"{GUIDES_PAGE} live disclosure at 390 pixels",
                ],
                "surface_regression": {
                    "page_width_checks": 7,
                    "chapter_14_desktop": chapter_row,
                    "chapter_14_companion_mobile": companion_row,
                    "all_geometry_checks_pass": all(
                        row.get("status") == "pass"
                        for row in [*viewport_results, chapter_row, companion_row]
                    ),
                },
                "chapter_14_semantics": semantics,
                "staged_disclosures": {
                    "chapter_14_live_interaction": disclosure,
                    "static_closure": closure,
                },
                "checks": {
                    "reader_centering_and_fill": "pass"
                    if all(row.get("status") == "pass" for row in viewport_results)
                    else "fail",
                    "responsive_reflow": "pass"
                    if all(row.get("status") == "pass" for row in viewport_results)
                    else "fail",
                    "chapter_14_navigation_and_identity": semantics["status"],
                    "staged_hint_answer_solution": disclosure.get("status", "fail"),
                    "html_language": "id-ID",
                    "browser_console_errors": len(console_errors),
                    "browser_page_errors": len(page_errors),
                    "browser_console_warnings": len(console_warnings),
                },
                "browser_console": {
                    "errors": console_errors,
                    "warnings": console_warnings,
                    "page_errors": page_errors,
                },
                "evidence": evidence,
            }
        )
    except Exception as exc:
        failures.append(f"browser QA execution failed: {exc}")
        receipt.update(
            {
                "browser": {
                    "engine": "Playwright Chromium",
                    "executable": str(browser_executable),
                    "version": browser_version,
                },
                "viewports": viewport_results,
                "staged_disclosures": {"static_closure": closure},
                "evidence": evidence,
            }
        )
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    receipt["status"] = "pass" if not failures else "fail"
    receipt["failures"] = failures
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "output": relative_to_root(output_path),
                "viewports": len(viewport_results),
                "failures": len(failures),
            },
            ensure_ascii=False,
        )
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
