#!/usr/bin/env python3
"""Run deterministic responsive-browser QA for the cumulative Chapter 15 reader.

The script serves the already-built HTML tree from localhost, launches a
system Chromium browser through Playwright, checks the five established reader
viewports and the Chapter 15 source/companion surfaces, and exercises one
complete Chapter 15 staged disclosure.  It does not build or modify the reader.
Its only output is the JSON QA receipt.
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any

import build_chapter14_browser_qa as engine


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SURFACE = ROOT / "output/chapters01-15-html"
DEFAULT_OUTPUT = ROOT / "qa/CHAPTER15_BROWSER_QA.json"
VIEWPORTS = ((1440, 900), (1280, 900), (1024, 900), (768, 900), (390, 900))

ROOT_PAGE = "frontmatter-1.html"
BOOK_PAGE = "o003-c90-chapters-01-15-reader.html"
CHAPTER_PAGE = "chap_subspaces.html"
EXERCISES_PAGE = "sec_sub_exer.html"
COMPANION_PAGE = "o003-c90-ch15-companion.html"
GUIDES_PAGE = "o003-c90-ch15-source-guides-a.html"
MASTERY_PAGE = "o003-c90-ch15-mastery.html"
EDITION_NOTE_PAGE = "o003-c90-ch15-edition-note.html"
GUIDE_ID = "o003-c90-ch15-guide-01"

EVIDENCE_PATHS = (
    ROOT / "qa/CHAPTER15_HTML_MANIFEST.json",
    ROOT / "qa/CHAPTER15_HTML_QA.json",
    ROOT / "qa/CHAPTER15_COMPANION_QA.json",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--surface",
        type=Path,
        default=DEFAULT_SURFACE,
        help="Already-built cumulative Chapter 15 HTML directory.",
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


def inspect_identity(page: Any) -> dict[str, Any]:
    """Collect Chapter 15 boundary identity and navigation facts."""
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
            rootLinkCount: countHref('o003-c90-chapters-01-15-reader.html'),
            chapterLinkCount: countHref('chap_subspaces.html'),
            exercisesLinkCount: countHref('sec_sub_exer.html'),
            companionLinkCount: countHref('o003-c90-ch15-companion.html'),
            masteryLinkCount: countHref('o003-c90-ch15-mastery.html'),
            editionNoteLinkCount: countHref('o003-c90-ch15-edition-note.html'),
            legacyBoundaryLinks: allHrefs.filter((href) =>
              href.includes('chapters-01-14-reader') ||
              href.includes('ch14-edition-note')
            ).length
          };
        }
        """
    )


def validate_identity(
    root: dict[str, Any],
    chapter: dict[str, Any],
    exercises: dict[str, Any],
    companion: dict[str, Any],
    mastery: dict[str, Any],
    failures: list[str],
) -> dict[str, Any]:
    root_heading = root.get("bookHeading") or ""
    chapter_heading = chapter.get("contentHeading") or ""
    exercises_heading = exercises.get("contentHeading") or ""
    companion_heading = companion.get("contentHeading") or ""
    mastery_heading = mastery.get("contentHeading") or ""
    checks = {
        "root_language_id_ID": root.get("language") == "id-ID",
        "root_book_link_exact": root.get("bookLink") == BOOK_PAGE,
        "root_heading_names_chapters_01_15": "Bab 1-15" in root_heading,
        "root_exposes_chapter_15": int(root.get("chapterLinkCount") or 0) > 0,
        "root_exposes_exercises": int(root.get("exercisesLinkCount") or 0) > 0,
        "root_exposes_companion": int(root.get("companionLinkCount") or 0) > 0,
        "root_exposes_mastery": int(root.get("masteryLinkCount") or 0) > 0,
        "root_exposes_edition_note": int(root.get("editionNoteLinkCount") or 0) > 0,
        "no_chapter_14_boundary_links": int(root.get("legacyBoundaryLinks") or 0) == 0,
        "chapter_language_id_ID": chapter.get("language") == "id-ID",
        "chapter_book_link_exact": chapter.get("bookLink") == BOOK_PAGE,
        "chapter_heading_is_chapter_15": "Bab 15" in chapter_heading,
        "chapter_heading_names_subspaces": "subruang" in chapter_heading.lower(),
        "chapter_navigates_to_exercises": int(chapter.get("exercisesLinkCount") or 0) > 0,
        "chapter_navigates_to_companion": int(chapter.get("companionLinkCount") or 0) > 0,
        "exercises_language_id_ID": exercises.get("language") == "id-ID",
        "exercises_book_link_exact": exercises.get("bookLink") == BOOK_PAGE,
        "exercises_heading_is_indonesian": "latihan" in exercises_heading.lower(),
        "companion_language_id_ID": companion.get("language") == "id-ID",
        "companion_book_link_exact": companion.get("bookLink") == BOOK_PAGE,
        "companion_heading_is_indonesian": (
            "panduan belajar mandiri" in companion_heading.lower()
        ),
        "mastery_language_id_ID": mastery.get("language") == "id-ID",
        "mastery_book_link_exact": mastery.get("bookLink") == BOOK_PAGE,
        "mastery_heading_is_indonesian": "penguasaan" in mastery_heading.lower(),
    }
    engine.add_failed_checks(failures, "Chapter 15 identity/navigation", checks)
    return {
        "book_heading": root_heading,
        "book_link": root.get("bookLink"),
        "edition_note_link": EDITION_NOTE_PAGE,
        "chapter_heading": chapter_heading,
        "chapter_page": CHAPTER_PAGE,
        "exercises_heading": exercises_heading,
        "exercises_page": EXERCISES_PAGE,
        "companion_heading": companion_heading,
        "companion_page": COMPANION_PAGE,
        "mastery_heading": mastery_heading,
        "mastery_page": MASTERY_PAGE,
        "checks": checks,
        "status": "pass" if all(checks.values()) else "fail",
    }


def static_closure(failures: list[str]) -> dict[str, Any]:
    path = ROOT / "qa/CHAPTER15_COMPANION_QA.json"
    payload = engine.load_json(path, failures)
    observed = {
        "source_prompt_entries": payload.get("source_prompt_total"),
        "mastery_entries": payload.get("mastery_total"),
        "staged_surfaces": payload.get("staged_surface_total"),
        "grouping_nodes": payload.get("grouping_node_total"),
    }
    expected = {
        "source_prompt_entries": 30,
        "mastery_entries": 8,
        "staged_surfaces": 152,
        "grouping_nodes": 2,
    }
    passed = payload.get("status") == "pass" and observed == expected
    if not passed:
        failures.append(
            f"Chapter 15 static companion closure mismatch: observed {observed}, "
            f"expected {expected}"
        )
    return {
        **observed,
        "source": "qa/CHAPTER15_COMPANION_QA.json and generated companion HTML controls",
        "status": "pass" if passed else "fail",
    }


def evidence_records(failures: list[str]) -> tuple[list[dict[str, Any]], str | None]:
    """Bind the exact Chapter 15 manifest and prerequisite QA receipts."""
    records: list[dict[str, Any]] = []
    canonical_manifest_sha: str | None = None
    for path in EVIDENCE_PATHS:
        if not path.is_file():
            failures.append(f"missing evidence file: {engine.relative_to_root(path)}")
            continue
        records.append(
            {
                "path": engine.relative_to_root(path),
                "bytes": path.stat().st_size,
                "sha256": engine.sha256_file(path),
            }
        )
        payload = engine.load_json(path, failures)
        if path.name == "CHAPTER15_HTML_MANIFEST.json":
            canonical_manifest_sha = payload.get("canonical_manifest_sha256")
            if not canonical_manifest_sha:
                failures.append(
                    "CHAPTER15_HTML_MANIFEST.json lacks canonical_manifest_sha256"
                )
        elif payload.get("status") != "pass":
            failures.append(f"{engine.relative_to_root(path)} status is not pass")
    return records, canonical_manifest_sha


def configure_engine() -> None:
    """Bind the maintained Chapter 14 browser engine helpers to Chapter 15."""
    engine.ROOT = ROOT
    engine.DEFAULT_SURFACE = DEFAULT_SURFACE
    engine.DEFAULT_OUTPUT = DEFAULT_OUTPUT
    engine.VIEWPORTS = VIEWPORTS
    engine.ROOT_PAGE = ROOT_PAGE
    engine.BOOK_PAGE = BOOK_PAGE
    engine.CHAPTER_PAGE = CHAPTER_PAGE
    engine.COMPANION_PAGE = COMPANION_PAGE
    engine.GUIDES_PAGE = GUIDES_PAGE
    engine.EDITION_NOTE_PAGE = EDITION_NOTE_PAGE
    engine.GUIDE_ID = GUIDE_ID
    engine.EVIDENCE_PATHS = EVIDENCE_PATHS
    engine.parse_args = parse_args
    engine.inspect_identity = inspect_identity
    engine.static_closure = static_closure


def main() -> int:
    configure_engine()
    args = parse_args()
    surface = args.surface.resolve()
    output_path = args.output.resolve()
    failures: list[str] = []

    required_pages = (
        ROOT_PAGE,
        BOOK_PAGE,
        EDITION_NOTE_PAGE,
        CHAPTER_PAGE,
        EXERCISES_PAGE,
        COMPANION_PAGE,
        GUIDES_PAGE,
        MASTERY_PAGE,
    )
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
        "surface": engine.relative_to_root(surface),
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
        browser_executable = engine.select_browser(args.browser_executable)
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
    server, thread, base_url = engine.start_server(surface)
    console_events: list[dict[str, str]] = []
    page_errors: list[dict[str, str]] = []
    viewport_results: list[dict[str, Any]] = []
    root_identity: dict[str, Any] = {}
    chapter_identity: dict[str, Any] = {}
    exercises_identity: dict[str, Any] = {}
    companion_identity: dict[str, Any] = {}
    mastery_identity: dict[str, Any] = {}
    browser_version: str | None = None

    try:
        with urllib.request.urlopen(f"{base_url}/{ROOT_PAGE}", timeout=10) as response:
            served_root = response.read()
        served_identity = {
            "path": ROOT_PAGE,
            "local_bytes": len(local_root),
            "served_bytes": len(served_root),
            "local_sha256": engine.sha256_bytes(local_root),
            "served_sha256": engine.sha256_bytes(served_root),
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
                    row, identity = engine.check_page_geometry(
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

                chapter_row, chapter_identity = engine.check_page_geometry(
                    browser, base_url, CHAPTER_PAGE, 1440, 900, args.timeout_ms,
                    console_events, page_errors, failures,
                )
                exercises_row, exercises_identity = engine.check_page_geometry(
                    browser, base_url, EXERCISES_PAGE, 1024, 900, args.timeout_ms,
                    console_events, page_errors, failures,
                )
                companion_row, companion_identity = engine.check_page_geometry(
                    browser, base_url, COMPANION_PAGE, 390, 900, args.timeout_ms,
                    console_events, page_errors, failures,
                )
                mastery_row, mastery_identity = engine.check_page_geometry(
                    browser, base_url, MASTERY_PAGE, 390, 900, args.timeout_ms,
                    console_events, page_errors, failures,
                )
                disclosure = engine.exercise_staged_disclosure(
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
            root_identity,
            chapter_identity,
            exercises_identity,
            companion_identity,
            mastery_identity,
            failures,
        )
        console_errors = [event for event in console_events if event["type"] == "error"]
        console_warnings = [
            event for event in console_events if event["type"] == "warning"
        ]
        if console_errors:
            failures.append(f"browser emitted {len(console_errors)} console error(s)")
        if page_errors:
            failures.append(f"browser emitted {len(page_errors)} uncaught page error(s)")

        geometry_rows = [
            *viewport_results,
            chapter_row,
            exercises_row,
            companion_row,
            mastery_row,
        ]
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
                    f"{EXERCISES_PAGE} at 1024 pixels",
                    f"{COMPANION_PAGE} at 390 pixels",
                    f"{MASTERY_PAGE} at 390 pixels",
                    f"{GUIDES_PAGE} live disclosure at 390 pixels",
                ],
                "surface_regression": {
                    "page_width_checks": len(geometry_rows),
                    "chapter_15_desktop": chapter_row,
                    "chapter_15_exercises_tablet": exercises_row,
                    "chapter_15_companion_mobile": companion_row,
                    "chapter_15_mastery_mobile": mastery_row,
                    "all_geometry_checks_pass": all(
                        row.get("status") == "pass" for row in geometry_rows
                    ),
                },
                "chapter_15_semantics": semantics,
                "staged_disclosures": {
                    "chapter_15_live_interaction": disclosure,
                    "static_closure": closure,
                },
                "checks": {
                    "reader_centering_and_fill": "pass"
                    if all(row.get("status") == "pass" for row in viewport_results)
                    else "fail",
                    "responsive_reflow": "pass"
                    if all(row.get("status") == "pass" for row in geometry_rows)
                    else "fail",
                    "chapter_15_navigation_and_identity": semantics["status"],
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
                "output": engine.relative_to_root(output_path),
                "viewports": len(viewport_results),
                "failures": len(failures),
            },
            ensure_ascii=False,
        )
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
