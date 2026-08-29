#!/usr/bin/env python3
"""Finalize and fail-closed QA the complete Chapters 1–20 HTML reader.

The first normal run must follow a successful ``chapters01-20-complete-html``
PreTeXt build.  It records the untouched build tree, applies the established
deterministic Indonesian finalizer, writes the finalized manifest and performs
the complete static reader audit.  ``--check`` is read-only and proves that the
finalized tree, manifests, and QA receipt reproduce byte for byte.

External citation links are inventory data, not offline dependencies.  Remote
runtime resources, forms, CSS imports/URLs, dynamic network endpoints, and
known tracking surfaces fail the privacy/offline gate.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import posixpath
import re
import shutil
from typing import Any
from urllib.parse import unquote, urlsplit

from lxml import etree, html

import finalize_chapter17_html as finalizer


ROOT = Path(__file__).resolve().parents[1]
HTML_ROOT = ROOT / "output" / "chapters01-20-complete-html"
RAW_MANIFEST = ROOT / "qa" / "CHAPTER20_COMPLETE_HTML_RAW_MANIFEST.json"
FINAL_MANIFEST = ROOT / "qa" / "CHAPTER20_COMPLETE_HTML_MANIFEST.json"
QA_RECEIPT = ROOT / "qa" / "CHAPTER20_COMPLETE_HTML_QA.json"

LAYOUT_RELATIVE = Path("external/o003-readable-layout.css")
EXPECTED_EXACT_SURFACES = (
    "frontmatter-1.html",
    "chap_Product_topology.html",
    "sec_prod_top_exer.html",
    "o003-c90-ch20-self-study.html",
    "o003-c90-ch20-mastery.html",
)
EXPECTED_UNIQUE_PATTERNS = {
    "complete_book": "o003-c90-complete-reader.html",
    "chapter_20_edition_note": "o003-c90-complete-edition-note.html",
}
EXPECTED_NONEMPTY_PATTERNS = {
    "chapter_20_source_guides": "o003-c90-ch20-source-guides-*.html",
}
MINIMUM_TREE_FILES = 20_000
MINIMUM_HTML_FILES = 19_800

LINK_ATTRIBUTES = {
    "a": ("href",),
    "audio": ("src",),
    "form": ("action",),
    "iframe": ("src",),
    "img": ("src", "srcset"),
    "link": ("href",),
    "object": ("data",),
    "script": ("src",),
    "source": ("src", "srcset"),
    "video": ("src", "poster"),
}
REMOTE_RUNTIME_TAGS = {"audio", "form", "iframe", "img", "object", "script", "source", "video"}
REMOTE_RUNTIME_LINK_RELS = {
    "dns-prefetch",
    "icon",
    "manifest",
    "modulepreload",
    "preconnect",
    "prefetch",
    "preload",
    "stylesheet",
}
IGNORED_SCHEMES = {"data", "javascript", "mailto", "tel"}
TRACKER_RE = re.compile(
    r"(?:google-analytics(?:\.com|/)|googletagmanager\.com|doubleclick\.net|"
    r"matomo(?:\.org|/)|plausible\.io|mixpanel\.com|segment\.io|hotjar\.com|"
    r"facebook\.net/.+fbevents|sentry\.io)",
    flags=re.IGNORECASE,
)
DYNAMIC_REMOTE_RE = re.compile(
    r"(?:fetch\s*\(|XMLHttpRequest|WebSocket\s*\(|sendBeacon\s*\(|"
    r"importScripts\s*\()[^\n;]{0,500}(?:https?:)?//",
    flags=re.IGNORECASE,
)
CSS_REMOTE_RE = re.compile(
    r"(?:@import\s+(?:url\()?\s*['\"]?(?:https?:)?//|"
    r"url\(\s*['\"]?(?:https?:)?//)",
    flags=re.IGNORECASE,
)
LOCALIZATION_PLACEHOLDER_RE = re.compile(
    r"\[(?:missing|unknown)[^\]]*\]", flags=re.IGNORECASE
)
LAYOUT_REQUIRED_SNIPPETS = (
    "@media (min-width: 1200px)",
    "width: min(960px, 100%)",
    "@media (min-width: 600px) and (max-width: 1199px)",
    "width: min(600px, 100%)",
    "margin-left: auto",
    "margin-right: auto",
)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def identity(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(payload),
        "sha256": sha256_bytes(payload),
    }


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_exact(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    if temporary.exists():
        raise RuntimeError(f"refusing to overwrite stale temporary receipt: {temporary}")
    temporary.write_bytes(payload)
    if temporary.read_bytes() != payload:
        raise RuntimeError(f"temporary receipt readback failed: {temporary}")
    temporary.replace(path)
    if path.read_bytes() != payload:
        raise RuntimeError(f"receipt readback failed: {path}")


def tree_manifest(root: Path, stage: str) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    html_files = 0
    total_bytes = 0
    for path in sorted(
        (item for item in root.rglob("*") if item.is_file()),
        key=lambda item: item.relative_to(root).as_posix().casefold(),
    ):
        payload = path.read_bytes()
        relative = path.relative_to(root).as_posix()
        if path.suffix.lower() in {".html", ".htm"}:
            html_files += 1
        total_bytes += len(payload)
        rows.append(
            {
                "path": relative,
                "bytes": len(payload),
                "sha256": sha256_bytes(payload),
            }
        )
    canonical = "".join(
        f"{row['path']}\t{row['bytes']}\t{row['sha256']}\n" for row in rows
    ).encode("utf-8")
    return {
        "schema_version": 1,
        "stage": stage,
        "target": "chapters01-20-complete-html",
        "root": "output/chapters01-20-complete-html",
        "file_count": len(rows),
        "html_files": html_files,
        "total_bytes": total_bytes,
        "canonical_manifest_sha256": sha256_bytes(canonical),
        "files": rows,
    }


def candidate_values(attribute: str, value: str) -> list[str]:
    if attribute != "srcset":
        return [value]
    return [part.strip().split()[0] for part in value.split(",") if part.strip()]


def local_target(root: Path, source: Path, raw: str) -> tuple[Path | None, str | None]:
    parsed = urlsplit(raw)
    if parsed.scheme.lower() in IGNORED_SCHEMES:
        return None, None
    if parsed.scheme.lower() in {"http", "https"} or parsed.netloc:
        return None, (parsed.hostname or parsed.netloc).lower()
    path = unquote(parsed.path)
    if not path:
        return source, None
    if path.startswith("/"):
        normalized = posixpath.normpath(path.lstrip("/"))
        target = root / Path(normalized)
    else:
        base = root if source.parent.name == "knowl" else source.parent
        normalized = posixpath.normpath(
            base.relative_to(root).as_posix() + "/" + path
        )
        target = root / Path(normalized)
    if path.endswith("/"):
        target = target / "index.html"
    return target, None


def class_tokens(node: etree._Element) -> set[str]:
    return set((node.get("class") or "").split())


def visible_accessible_name(node: etree._Element) -> str:
    values = [
        node.get("alt") or "",
        node.get("aria-label") or "",
        node.get("title") or "",
        " ".join(node.itertext()),
    ]
    return " ".join(" ".join(values).split())


def required_surfaces(root: Path, failures: list[str]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {"exact": [], "unique_patterns": [], "nonempty_patterns": []}
    for value in EXPECTED_EXACT_SURFACES:
        path = root / value
        result["exact"].append(value)
        if not path.is_file():
            failures.append(f"required reader surface is missing: {value}")
    for label, pattern in EXPECTED_UNIQUE_PATTERNS.items():
        matches = sorted(path.name for path in root.glob(pattern) if path.is_file())
        result["unique_patterns"].extend(matches)
        if len(matches) != 1:
            failures.append(
                f"required unique surface pattern {label}={pattern!r} matched {len(matches)} files: {matches}"
            )
    for label, pattern in EXPECTED_NONEMPTY_PATTERNS.items():
        matches = sorted(path.name for path in root.glob(pattern) if path.is_file())
        result["nonempty_patterns"].extend(matches)
        if not matches:
            failures.append(
                f"required surface pattern {label}={pattern!r} matched no files"
            )
    return result


def audit_reader(
    root: Path,
    raw_manifest_path: Path,
    current_manifest: dict[str, Any],
    expected_manifest: dict[str, Any],
) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    external_nonruntime_hosts: Counter[str] = Counter()
    remote_runtime_hosts: Counter[str] = Counter()
    remote_runtime_references: list[dict[str, str]] = []
    missing_alt: list[str] = []
    empty_nondecorative_alt: list[str] = []
    missing_iframe_title: list[str] = []
    links_checked = 0
    fragments_checked = 0
    images_checked = 0
    html_parsed = 0
    pretext_pages = 0
    layout_linked_pages = 0
    viewport_pages = 0
    id_cache: dict[Path, set[str]] = {}
    surfaces = required_surfaces(root, failures)

    if current_manifest != expected_manifest:
        failures.append("current finalized tree differs from the supplied final manifest")
    if current_manifest["file_count"] < MINIMUM_TREE_FILES:
        failures.append(
            f"tree is implausibly incomplete: {current_manifest['file_count']} files < {MINIMUM_TREE_FILES}"
        )
    if current_manifest["html_files"] < MINIMUM_HTML_FILES:
        failures.append(
            f"HTML tree is implausibly incomplete: {current_manifest['html_files']} pages < {MINIMUM_HTML_FILES}"
        )

    layout_path = root / LAYOUT_RELATIVE
    layout_checks: dict[str, bool] = {}
    if not layout_path.is_file():
        failures.append(f"readable-layout stylesheet is missing: {LAYOUT_RELATIVE.as_posix()}")
        layout_payload = ""
    else:
        layout_payload = layout_path.read_text(encoding="utf-8")
    for snippet in LAYOUT_REQUIRED_SNIPPETS:
        passed = snippet in layout_payload
        layout_checks[snippet] = passed
        if not passed:
            failures.append(f"readable-layout safeguard is missing: {snippet}")

    html_paths = sorted(
        (*root.rglob("*.html"), *root.rglob("*.htm")),
        key=lambda path: path.relative_to(root).as_posix().casefold(),
    )
    for source in html_paths:
        relative = source.relative_to(root).as_posix()
        payload = source.read_bytes()
        try:
            document = html.fromstring(payload)
        except Exception as exc:
            failures.append(f"HTML parse failed: {relative}: {exc}")
            continue
        html_parsed += 1
        document_root = document.getroottree().getroot()
        if (document_root.get("lang") or "").lower() != "id-id":
            failures.append(f"wrong or missing html lang: {relative}")
        visible = " ".join(document.itertext())
        if LOCALIZATION_PLACEHOLDER_RE.search(visible):
            failures.append(f"localization placeholder remains: {relative}")
        if TRACKER_RE.search(payload.decode("utf-8", errors="ignore")):
            failures.append(f"tracking surface found: {relative}")

        bodies = document.xpath("//body")
        is_pretext = bool(bodies and "pretext" in class_tokens(bodies[0]))
        if is_pretext:
            pretext_pages += 1
            viewport = document.xpath(
                "//meta[translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='viewport']/@content"
            )
            viewport_ok = any("width=device-width" in value.replace(" ", "").lower() for value in viewport)
            if viewport_ok:
                viewport_pages += 1
            else:
                failures.append(f"mobile viewport safeguard is missing: {relative}")
            layout_links = document.xpath("//link[@href]/@href")
            layout_ok = any(urlsplit(value).path.endswith(LAYOUT_RELATIVE.as_posix()) for value in layout_links)
            if layout_ok:
                layout_linked_pages += 1
            else:
                failures.append(f"readable-layout stylesheet is not linked: {relative}")

        for image in document.xpath("//img"):
            images_checked += 1
            if image.get("alt") is None:
                missing_alt.append(relative)
            elif not (image.get("alt") or "").strip():
                decorative = (
                    (image.get("role") or "").lower() == "presentation"
                    or (image.get("aria-hidden") or "").lower() == "true"
                    or bool(image.xpath("ancestor::*[@aria-hidden='true']"))
                )
                if not decorative:
                    empty_nondecorative_alt.append(relative)
        for frame in document.xpath("//iframe"):
            if not visible_accessible_name(frame):
                missing_iframe_title.append(relative)

        for element in document.iter():
            tag = element.tag.lower() if isinstance(element.tag, str) else ""
            for attribute in LINK_ATTRIBUTES.get(tag, ()):
                value = element.get(attribute)
                if not value:
                    continue
                for candidate in candidate_values(attribute, value):
                    links_checked += 1
                    target, host = local_target(root, source, candidate)
                    if host:
                        rels = set((element.get("rel") or "").lower().split())
                        runtime = tag in REMOTE_RUNTIME_TAGS or (
                            tag == "link" and bool(rels & REMOTE_RUNTIME_LINK_RELS)
                        )
                        if runtime:
                            remote_runtime_hosts[host] += 1
                            if len(remote_runtime_references) < 200:
                                remote_runtime_references.append(
                                    {
                                        "page": relative,
                                        "tag": tag,
                                        "attribute": attribute,
                                        "value": candidate,
                                    }
                                )
                        elif tag in {"a", "link"} and attribute == "href":
                            external_nonruntime_hosts[host] += 1
                        else:
                            remote_runtime_hosts[host] += 1
                            if len(remote_runtime_references) < 200:
                                remote_runtime_references.append(
                                    {
                                        "page": relative,
                                        "tag": tag,
                                        "attribute": attribute,
                                        "value": candidate,
                                    }
                                )
                        continue
                    if target is None:
                        continue
                    if not target.is_file():
                        failures.append(f"missing local target: {relative} -> {candidate}")
                        continue
                    fragment = unquote(urlsplit(candidate).fragment)
                    if fragment and target.suffix.lower() in {".html", ".htm"}:
                        fragments_checked += 1
                        if target not in id_cache:
                            try:
                                target_document = html.fromstring(target.read_bytes())
                                id_cache[target] = {
                                    value for value in target_document.xpath("//@id") if value
                                }
                            except Exception:
                                id_cache[target] = set()
                        if fragment not in id_cache[target]:
                            failures.append(f"missing fragment: {relative} -> {candidate}")

    if missing_alt:
        failures.append(f"{len(missing_alt)} image elements lack an alt attribute")
    if empty_nondecorative_alt:
        failures.append(
            f"{len(empty_nondecorative_alt)} nondecorative image elements have empty alt text"
        )
    if missing_iframe_title:
        failures.append(f"{len(missing_iframe_title)} iframe elements lack an accessible name")
    if pretext_pages == 0:
        failures.append("no PreTeXt reader pages were detected")
    if layout_linked_pages != pretext_pages:
        failures.append(
            f"readable-layout coverage mismatch: {layout_linked_pages}/{pretext_pages} PreTeXt pages"
        )
    if viewport_pages != pretext_pages:
        failures.append(
            f"mobile viewport coverage mismatch: {viewport_pages}/{pretext_pages} PreTeXt pages"
        )
    if remote_runtime_references:
        failures.append(
            f"offline closure failed: {sum(remote_runtime_hosts.values())} remote runtime references"
        )

    css_files = sorted(root.rglob("*.css"))
    css_remote: list[str] = []
    for path in css_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        if CSS_REMOTE_RE.search(text):
            css_remote.append(path.relative_to(root).as_posix())
        if TRACKER_RE.search(text):
            failures.append(f"tracking reference found in CSS: {path.relative_to(root).as_posix()}")
    if css_remote:
        failures.append(f"offline closure failed: remote URL/import in CSS files: {css_remote}")

    network_javascript: list[str] = []
    for path in sorted(root.rglob("*.js")):
        text = path.read_text(encoding="utf-8", errors="replace")
        if DYNAMIC_REMOTE_RE.search(text):
            network_javascript.append(path.relative_to(root).as_posix())
        if TRACKER_RE.search(text):
            failures.append(f"tracking reference found in JavaScript: {path.relative_to(root).as_posix()}")
    if network_javascript:
        failures.append(
            f"privacy gate failed: dynamic remote network endpoints in JavaScript: {network_javascript}"
        )

    raw_manifest_valid = False
    if not raw_manifest_path.is_file():
        failures.append("raw build-tree manifest is missing")
        raw_identity: dict[str, Any] | None = None
    else:
        raw_identity = identity(raw_manifest_path)
        try:
            raw_document = json.loads(raw_manifest_path.read_text(encoding="utf-8"))
            raw_manifest_valid = (
                raw_document.get("schema_version") == 1
                and raw_document.get("stage") == "raw-pretext-build"
                and raw_document.get("target") == "chapters01-20-complete-html"
                and raw_document.get("root") == "output/chapters01-20-complete-html"
                and int(raw_document.get("file_count", 0)) >= MINIMUM_TREE_FILES
                and int(raw_document.get("html_files", 0)) >= MINIMUM_HTML_FILES
                and isinstance(raw_document.get("canonical_manifest_sha256"), str)
                and len(raw_document["canonical_manifest_sha256"]) == 64
                and len(raw_document.get("files", [])) == raw_document.get("file_count")
            )
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            raw_manifest_valid = False
        if not raw_manifest_valid:
            failures.append("raw build-tree manifest is malformed or incomplete")

    return {
        "schema_version": 1,
        "status": "pass" if not failures else "fail",
        "target": "chapters01-20-complete-html",
        "surface": "output/chapters01-20-complete-html",
        "raw_manifest": raw_identity,
        "final_manifest": {
            "path": "qa/CHAPTER20_COMPLETE_HTML_MANIFEST.json",
            "canonical_manifest_sha256": current_manifest["canonical_manifest_sha256"],
            "file_count": current_manifest["file_count"],
            "html_files": current_manifest["html_files"],
            "total_bytes": current_manifest["total_bytes"],
        },
        "required_surfaces": surfaces,
        "checks": {
            "raw_tree_inventory_present": raw_identity is not None and raw_manifest_valid,
            "final_tree_matches_manifest": current_manifest == expected_manifest,
            "internal_links_assets_fragments_closed": not any(
                value.startswith(("missing local target:", "missing fragment:")) for value in failures
            ),
            "html_language_id_ID": not any(value.startswith("wrong or missing html lang:") for value in failures),
            "generated_chrome_indonesian": not any(
                "localization" in value or "generated chrome" in value for value in failures
            ),
            "image_accessibility_present": not missing_alt and not empty_nondecorative_alt and not missing_iframe_title,
            "readable_layout_complete": layout_linked_pages == pretext_pages and all(layout_checks.values()),
            "mobile_viewport_complete": viewport_pages == pretext_pages,
            "offline_runtime_closed": not remote_runtime_references and not css_remote and not network_javascript,
            "privacy_trackers_absent": not any("tracking" in value for value in failures),
        },
        "counts": {
            "html_parsed": html_parsed,
            "pretext_pages": pretext_pages,
            "layout_linked_pages": layout_linked_pages,
            "viewport_pages": viewport_pages,
            "links_and_assets_checked": links_checked,
            "fragments_checked": fragments_checked,
            "images_checked": images_checked,
            "css_files_checked": len(css_files),
        },
        "accessibility": {
            "missing_alt_count": len(missing_alt),
            "empty_nondecorative_alt_count": len(empty_nondecorative_alt),
            "missing_iframe_accessible_name_count": len(missing_iframe_title),
            "missing_alt_sample": sorted(set(missing_alt))[:100],
            "empty_nondecorative_alt_sample": sorted(set(empty_nondecorative_alt))[:100],
            "missing_iframe_title_sample": sorted(set(missing_iframe_title))[:100],
        },
        "layout": {
            "stylesheet": identity(layout_path) if layout_path.is_file() else None,
            "required_snippets": layout_checks,
        },
        "offline_privacy": {
            "external_nonruntime_hosts": dict(sorted(external_nonruntime_hosts.items())),
            "remote_runtime_hosts": dict(sorted(remote_runtime_hosts.items())),
            "remote_runtime_reference_sample": remote_runtime_references,
            "css_remote_files": css_remote,
            "dynamic_remote_javascript": network_javascript,
        },
        "warnings": warnings,
        "failures": failures,
    }


def ensure_tree_exists(root: Path) -> None:
    if not root.is_dir():
        raise SystemExit(
            "complete HTML output is absent; run `pretext build chapters01-20-complete-html` first"
        )
    if not any(root.glob("*.html")):
        raise SystemExit(
            "complete HTML output has no root-level HTML and is not a finished build"
        )


def preflight_complete_tree(root: Path) -> None:
    failures: list[str] = []
    required_surfaces(root, failures)
    transients = sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
        and (
            path.name.endswith(".o003-finalize.tmp")
            or path.suffix.lower() in {".tmp", ".partial", ".part"}
        )
    )
    if transients:
        failures.append(f"transient/incomplete build files remain: {transients[:100]}")
    files = [path for path in root.rglob("*") if path.is_file()]
    file_count = len(files)
    html_count = sum(
        1 for path in files if path.suffix.lower() in {".html", ".htm"}
    )
    if file_count < MINIMUM_TREE_FILES:
        failures.append(
            f"tree is implausibly incomplete: {file_count} files < {MINIMUM_TREE_FILES}"
        )
    if html_count < MINIMUM_HTML_FILES:
        failures.append(
            f"HTML tree is implausibly incomplete: {html_count} pages < {MINIMUM_HTML_FILES}"
        )
    if failures:
        raise SystemExit(
            "refusing to finalize an incomplete full-reader tree:\n- "
            + "\n- ".join(failures)
        )


def vendor_runtime(root: Path) -> int:
    """Copy the pinned repository vendor tree and rewrite runtime URLs locally."""
    source = ROOT / "external" / "vendor"
    if not source.is_dir():
        raise RuntimeError(f"required vendor tree is missing: {source}")
    destination = root / "external" / "vendor"
    destination.mkdir(parents=True, exist_ok=True)
    for item in source.rglob("*"):
        if item.is_file():
            target = destination / item.relative_to(source)
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists() or target.read_bytes() != item.read_bytes():
                shutil.copyfile(item, target)
    inventory = []
    for item in sorted(destination.rglob("*")):
        if item.is_file():
            inventory.append(identity(item))
    write_exact(ROOT / "qa" / "CHAPTER20_COMPLETE_HTML_VENDOR_MANIFEST.json", json_bytes({
        "schema_version": 1,
        "source": "repo/external/vendor",
        "versions": {"mathjax": "3/es5 tex-chtml", "lunr": "2.3.9", "pretext_js": "0.3", "pretext_css": "0.7"},
        "files": inventory,
    }))
    replacements = {
        "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js": "external/vendor/mathjax/es5/tex-chtml.js",
        "https://cdnjs.cloudflare.com/ajax/libs/lunr.js/2.3.9/lunr.min.js": "external/vendor/lunr/lunr.min.js",
        "https://pretextbook.org/js/0.3/": "external/vendor/pretext/js/0.3/",
        "https://pretextbook.org/js/lib/": "external/vendor/pretext/js/lib/",
        "https://pretextbook.org/css/0.7/": "external/vendor/pretext/css/0.7/",
        "https://runestone.academy/runestone/static/images/RAIcon_cropped.png": "external/vendor/badges/runestone.svg",
        "https://www.mathjax.org/badge/badge-square-2.png": "external/vendor/badges/mathjax.svg",
    }
    # Generated pages currently live at the output root, but compute every
    # replacement relative to its page so the same finalizer remains correct
    # if PreTeXt later emits nested reader pages.
    def page_relative(target: str, page: Path) -> str:
        page_dir = page.parent.relative_to(root).as_posix()
        return posixpath.relpath(target, start=page_dir or ".")

    changed = 0
    for path in root.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        updated = text
        for old, new in replacements.items():
            updated = updated.replace(old, page_relative(new, path))
        # Web-font stylesheets are network-only; the local layout stylesheet
        # supplies system fallbacks and remains the authoritative typography.
        updated = re.sub(
            r"<link[^>]+fonts\.(?:googleapis\.com|gstatic\.com|cdnfonts\.com)[^>]*>\s*",
            "",
            updated,
            flags=re.I,
        )
        if updated != text:
            path.write_text(updated, encoding="utf-8", newline="")
            changed += 1
    return changed


def finalize_tree(root: Path) -> tuple[int, dict[str, list[str]]]:
    changes = 0
    residue: dict[str, list[str]] = {}
    changes += vendor_runtime(root)
    html_paths = sorted(
        (*root.rglob("*.html"), *root.rglob("*.htm")),
        key=lambda path: path.relative_to(root).as_posix().casefold(),
    )
    for path in html_paths:
        count, findings = finalizer.transform(path, root, check_only=False)
        changes += count
        if findings:
            residue[path.relative_to(root).as_posix()] = findings
        # The upstream theme occasionally emits an empty alt on a real figure
        # (rather than a decorative image).  Preserve the figure's own
        # Indonesian title/caption as a faithful, stable accessible name.  Do
        # not invent generic filler and leave genuinely unresolved cases for
        # the fail-closed audit below.
        document = html.fromstring(path.read_bytes())
        dirty = False
        for image in document.xpath("//img[@alt='']"):
            decorative = (
                (image.get("role") or "").lower() == "presentation"
                or (image.get("aria-hidden") or "").lower() == "true"
                or bool(image.xpath("ancestor::*[@aria-hidden='true']"))
            )
            if decorative:
                continue
            candidates = image.xpath(
                "ancestor::*[self::figure or contains(concat(' ', normalize-space(@class), ' '), ' figure ')][1]"
                "//*[self::figcaption or @title or @aria-label]"
            )
            text = ""
            for node in candidates:
                candidate = " ".join(" ".join(node.itertext()).split())
                if candidate:
                    text = candidate
                    break
            if not text:
                text = (image.get("title") or image.get("aria-label") or "").strip()
            if text:
                image.set("alt", text)
                changes += 1
                dirty = True
        if dirty:
            payload = etree.tostring(document, encoding="utf-8", method="html", doctype="<!DOCTYPE html>")
            path.write_bytes(payload)
    if residue:
        raise RuntimeError(
            f"Indonesian generated-chrome finalization left forbidden residue: {residue}"
        )
    return changes, residue


def check_finalizer_idempotent(root: Path) -> tuple[int, dict[str, list[str]]]:
    changes = 0
    residue: dict[str, list[str]] = {}
    html_paths = sorted(
        (*root.rglob("*.html"), *root.rglob("*.htm")),
        key=lambda path: path.relative_to(root).as_posix().casefold(),
    )
    for path in html_paths:
        count, findings = finalizer.transform(path, root, check_only=True)
        changes += count
        if findings:
            residue[path.relative_to(root).as_posix()] = findings
    return changes, residue


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="read-only byte-for-byte verification of the finalized tree and receipts",
    )
    args = parser.parse_args()
    ensure_tree_exists(HTML_ROOT)
    preflight_complete_tree(HTML_ROOT)

    if args.check:
        for path in (RAW_MANIFEST, FINAL_MANIFEST, QA_RECEIPT):
            if not path.is_file():
                raise SystemExit(f"required finalized-reader receipt is missing: {path}")
        changes, residue = check_finalizer_idempotent(HTML_ROOT)
        if changes or residue:
            raise SystemExit(
                f"HTML finalizer is not idempotent: unapplied_changes={changes}, residue={residue}"
            )
        stored_final_payload = FINAL_MANIFEST.read_bytes()
        current_final = tree_manifest(HTML_ROOT, "finalized")
        if json_bytes(current_final) != stored_final_payload:
            raise SystemExit("finalized HTML manifest differs from current tree")
        stored_final = json.loads(stored_final_payload.decode("utf-8"))
        current_qa = audit_reader(
            HTML_ROOT, RAW_MANIFEST, current_final, stored_final
        )
        current_qa_payload = json_bytes(current_qa)
        if current_qa_payload != QA_RECEIPT.read_bytes():
            raise SystemExit("complete-reader QA receipt is not deterministic")
        print(
            json.dumps(
                {
                    "status": current_qa["status"],
                    "check_only": True,
                    "finalizer_unapplied_changes": changes,
                    "canonical_manifest_sha256": current_final["canonical_manifest_sha256"],
                    "qa_receipt_sha256": sha256_bytes(current_qa_payload),
                    "failures": len(current_qa["failures"]),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0 if current_qa["status"] == "pass" else 1

    if not RAW_MANIFEST.is_file():
        raw_manifest = tree_manifest(HTML_ROOT, "raw-pretext-build")
        if (
            raw_manifest["file_count"] < MINIMUM_TREE_FILES
            or raw_manifest["html_files"] < MINIMUM_HTML_FILES
        ):
            raise SystemExit(
                "refusing to inventory/finalize an implausibly incomplete full-reader tree: "
                f"files={raw_manifest['file_count']}, html={raw_manifest['html_files']}"
            )
        write_exact(RAW_MANIFEST, json_bytes(raw_manifest))

    changes, _ = finalize_tree(HTML_ROOT)
    idempotent_changes, idempotent_residue = check_finalizer_idempotent(HTML_ROOT)
    if idempotent_changes or idempotent_residue:
        raise SystemExit(
            f"post-finalization idempotence failed: changes={idempotent_changes}, residue={idempotent_residue}"
        )

    final_manifest = tree_manifest(HTML_ROOT, "finalized")
    final_manifest_payload = json_bytes(final_manifest)
    write_exact(FINAL_MANIFEST, final_manifest_payload)
    receipt = audit_reader(
        HTML_ROOT, RAW_MANIFEST, final_manifest, final_manifest
    )
    receipt_payload = json_bytes(receipt)
    write_exact(QA_RECEIPT, receipt_payload)
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "check_only": False,
                "localized_nodes_and_attributes": changes,
                "canonical_manifest_sha256": final_manifest["canonical_manifest_sha256"],
                "qa_receipt_sha256": sha256_bytes(receipt_payload),
                "failures": len(receipt["failures"]),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0 if receipt["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
