#!/usr/bin/env python3
"""Deterministic inventory and reader-surface QA for the cumulative Modules 1--8 HTML tree.

The canonical tree digest uses exact file bytes.  The only representation
normalization is conversion of relative path separators to POSIX ``/`` before
UTF-8 bytewise sorting; file content is never decoded, timestamp-stripped, or
otherwise normalized for the digest.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import posixpath
import re
from typing import Any, Iterable
from urllib.parse import unquote, urlsplit

from lxml import html


ROOT = Path(__file__).resolve().parents[1]
TREE = ROOT / "output" / "o003-completion-modules01-08-html"
READER = ROOT / "source" / "o003_completion_modules_01_08_reader.ptx"
WRAPPER = ROOT / "completion" / "o003_c90_completion_self_study.ptx"
SCHEMA_QA = ROOT / "qa" / "O003_COMPLETION_MODULES01_08_SCHEMA_QA.json"
BACKEND = ROOT / "backend" / "o003_completion_current_manifest.json"
SOURCE_QA = ROOT / "qa" / "O003_COMPLETION_CURRENT_QA.json"
INVENTORY = ROOT / "backend" / "o003_completion_modules_01_08_html_inventory.json"
REPORT = ROOT / "qa" / "O003_COMPLETION_MODULES01_08_HTML_QA.json"
RECEIPT = ROOT / "qa" / "O003_COMPLETION_MODULES01_08_HTML_QA.md"
EXPECTED_LANG = "id-ID"
READABLE_CSS = "external/o003-readable-layout.css"

LINK_ATTRIBUTES: dict[str, tuple[str, ...]] = {
    "a": ("href", "data-knowl"),
    "audio": ("src",),
    "iframe": ("src",),
    "img": ("src", "srcset"),
    "link": ("href",),
    "object": ("data",),
    "script": ("src",),
    "source": ("src", "srcset"),
    "use": ("href", "xlink:href"),
    "video": ("src", "poster"),
}
ASSET_TAGS = {"audio", "iframe", "img", "link", "object", "script", "source", "use", "video"}
IGNORED_SCHEMES = {"about", "data", "javascript", "mailto", "tel"}
TEXT_SUFFIXES = {".css", ".htm", ".html", ".js", ".json", ".map", ".svg", ".txt", ".xml"}
LOCAL_PATH_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("file_uri", re.compile(r"file:(?://|\\\\)", re.IGNORECASE)),
    ("windows_user_path", re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+", re.IGNORECASE)),
    ("encoded_windows_user_path", re.compile(r"[A-Za-z](?:%3A|:)(?:%2F|%5C)+(?:Users)(?:%2F|%5C)+", re.IGNORECASE)),
    ("unix_home_path", re.compile(r"/(?:home|Users)/[^/\s<>'\"]+/", re.IGNORECASE)),
)
CREDENTIAL_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("openai_key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("github_classic_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("github_fine_grained_token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("bearer_token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}\b", re.IGNORECASE)),
    ("assigned_api_token", re.compile(r"(?:api[_-]?token|access[_-]?token|zenodo[_-]?token|figshare[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{20,}", re.IGNORECASE)),
)
UI_EXPECTATIONS: dict[str, set[str]] = {
    "toc": {"Daftar Isi", "Isi"},
    "previous": {"Sebelumnya"},
    "next": {"Berikutnya"},
    "up": {"Induk", "Naik"},
    "top": {"Atas"},
}
UI_CLASS_TO_KIND = {
    "toc-toggle": "toc",
    "previous-button": "previous",
    "next-button": "next",
    "up-button": "up",
    "top-button": "top",
}


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def identity(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(payload), "sha256": sha256(payload)}


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def classify(relative: str) -> str:
    suffix = Path(relative).suffix.casefold()
    if suffix in {".html", ".htm"}:
        return "html_document"
    if suffix == ".css":
        return "stylesheet"
    if suffix == ".js":
        return "javascript"
    if suffix == ".json":
        return "json"
    if suffix in {".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp"}:
        return "image"
    if suffix in {".woff", ".woff2", ".ttf", ".otf"}:
        return "font"
    return "other"


def inventory_rows() -> list[dict[str, Any]]:
    paths = [path for path in TREE.rglob("*") if path.is_file()]
    paths.sort(key=lambda path: path.relative_to(TREE).as_posix().encode("utf-8"))
    rows: list[dict[str, Any]] = []
    for path in paths:
        payload = path.read_bytes()
        relative = path.relative_to(TREE).as_posix()
        rows.append({
            "path": relative,
            "bytes": len(payload),
            "sha256": sha256(payload),
            "kind": classify(relative),
        })
    return rows


def canonical_tree_sha256(rows: Iterable[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    digest.update(b"O003-C90-MODULES01-08-HTML-TREE-V1\0")
    for row in rows:
        digest.update(str(row["path"]).encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(row["bytes"]).encode("ascii"))
        digest.update(b"\0")
        digest.update(str(row["sha256"]).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def candidate_values(attribute: str, value: str) -> list[str]:
    if attribute != "srcset":
        return [value]
    return [part.strip().split()[0] for part in value.split(",") if part.strip()]


def resolve_local(source: Path, raw: str) -> tuple[Path | None, str | None, str]:
    parsed = urlsplit(raw.strip())
    scheme = parsed.scheme.casefold()
    if scheme in IGNORED_SCHEMES:
        return None, None, parsed.fragment
    if scheme in {"http", "https"} or parsed.netloc:
        return None, (parsed.hostname or parsed.netloc or "").casefold(), parsed.fragment
    decoded = unquote(parsed.path)
    if not decoded:
        return source, None, unquote(parsed.fragment)
    if decoded.startswith("/"):
        relative = posixpath.normpath(decoded.lstrip("/"))
    else:
        # Knowl documents are injected into a top-level reader page.  Their
        # in-context URLs are therefore intentionally rooted at TREE rather
        # than at the physical knowl directory.
        base = "" if source.parent.name == "knowl" else source.parent.relative_to(TREE).as_posix()
        relative = posixpath.normpath(posixpath.join(base, decoded))
    target = TREE / Path(relative)
    if decoded.endswith("/"):
        target /= "index.html"
    return target, None, unquote(parsed.fragment)


def parse_html(path: Path) -> html.HtmlElement:
    return html.document_fromstring(path.read_bytes())


def ids_for(path: Path, cache: dict[Path, set[str]]) -> set[str]:
    if path not in cache:
        document = parse_html(path)
        cache[path] = {value for value in document.xpath("//@id") if value}
    return cache[path]


def extract_css_urls(payload: str) -> list[str]:
    values: list[str] = []
    for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", payload, flags=re.IGNORECASE):
        value = match.group(2).strip()
        if value:
            values.append(value)
    return values


def compact_samples(values: list[str], limit: int = 30) -> dict[str, Any]:
    return {"count": len(values), "samples": values[:limit], "samples_truncated": len(values) > limit}


def scan_tree(rows: list[dict[str, Any]]) -> dict[str, Any]:
    html_paths = [TREE / Path(row["path"]) for row in rows if row["kind"] == "html_document"]
    main_documents = [path for path in html_paths if path.parent == TREE and path.name != "index.html"]
    failures: list[str] = []
    broken_targets: list[str] = []
    broken_fragments: list[str] = []
    broken_embedded_knowls: list[str] = []
    parse_failures: list[str] = []
    absolute_local_hits: list[str] = []
    credential_hits: list[str] = []
    links_checked = 0
    local_targets_checked = 0
    local_assets_checked = 0
    local_fragments_checked = 0
    external_hosts: Counter[str] = Counter()
    external_asset_hosts: Counter[str] = Counter()
    language_counts: Counter[str] = Counter()
    language_samples: dict[str, list[str]] = {}
    ui_labels: dict[str, Counter[str]] = {kind: Counter() for kind in UI_EXPECTATIONS}
    css_linked_documents: list[str] = []
    id_cache: dict[Path, set[str]] = {}

    for path in html_paths:
        relative_source = path.relative_to(TREE).as_posix()
        try:
            document = parse_html(path)
        except Exception as exc:  # pragma: no cover - fail-closed diagnostic
            parse_failures.append(f"{relative_source}: {type(exc).__name__}")
            continue
        lang_values = document.xpath("/html/@lang")
        lang = lang_values[0] if lang_values else "(missing)"
        language_counts[lang] += 1
        language_samples.setdefault(lang, [])
        if len(language_samples[lang]) < 8:
            language_samples[lang].append(relative_source)

        if path in main_documents:
            css_hrefs = set(document.xpath("//link[contains(concat(' ', normalize-space(@rel), ' '), ' stylesheet ')]/@href"))
            if READABLE_CSS in css_hrefs:
                css_linked_documents.append(relative_source)
            for node in document.xpath("//*[contains(concat(' ', normalize-space(@class), ' '), ' name ')]"):
                label = " ".join(node.itertext()).strip()
                if not label:
                    continue
                ancestor_classes = " ".join(node.xpath("ancestor-or-self::*[@class]/@class")).split()
                for css_class, kind in UI_CLASS_TO_KIND.items():
                    if css_class in ancestor_classes:
                        ui_labels[kind][label] += 1

        for element in document.iter():
            tag = element.tag.casefold() if isinstance(element.tag, str) else ""
            for attribute in LINK_ATTRIBUTES.get(tag, ()):
                value = element.get(attribute)
                if not value:
                    continue
                for candidate in candidate_values(attribute, value):
                    links_checked += 1
                    target, host, fragment = resolve_local(path, candidate)
                    if host:
                        external_hosts[host] += 1
                        if tag in ASSET_TAGS:
                            external_asset_hosts[host] += 1
                        continue
                    if target is None:
                        continue
                    local_targets_checked += 1
                    if tag in ASSET_TAGS:
                        local_assets_checked += 1
                    try:
                        target_relative = target.relative_to(TREE).as_posix()
                    except ValueError:
                        broken_targets.append(f"{relative_source} -> {candidate} [escapes tree]")
                        continue
                    if not target.is_file():
                        broken_targets.append(f"{relative_source} -> {candidate} [{target_relative} missing]")
                        continue
                    if fragment and target.suffix.casefold() in {".html", ".htm"}:
                        local_fragments_checked += 1
                        try:
                            target_ids = ids_for(target, id_cache)
                        except Exception:
                            target_ids = set()
                        if fragment not in target_ids:
                            broken_fragments.append(f"{relative_source} -> {candidate}")

            data_refid = element.get("data-refid")
            data_knowl = element.get("data-knowl")
            if data_refid and not data_knowl:
                if data_refid not in ids_for(path, id_cache):
                    broken_embedded_knowls.append(f"{relative_source} -> #{data_refid}")

        for content in document.xpath("//meta[translate(@http-equiv, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='refresh']/@content"):
            match = re.search(r"url\s*=\s*['\"]?([^'\";]+)", content, flags=re.IGNORECASE)
            if match:
                candidate = match.group(1).strip()
                links_checked += 1
                target, host, _ = resolve_local(path, candidate)
                if host:
                    external_hosts[host] += 1
                elif target is not None:
                    local_targets_checked += 1
                    if not target.is_file():
                        broken_targets.append(f"{relative_source} -> meta-refresh {candidate}")

    for row in rows:
        relative = str(row["path"])
        path = TREE / Path(relative)
        suffix = path.suffix.casefold()
        if suffix in TEXT_SUFFIXES:
            decoded = path.read_bytes().decode("utf-8", errors="replace")
            for label, pattern in LOCAL_PATH_PATTERNS:
                if pattern.search(decoded):
                    absolute_local_hits.append(f"{relative}: {label}")
            for label, pattern in CREDENTIAL_PATTERNS:
                if pattern.search(decoded):
                    credential_hits.append(f"{relative}: {label}")
            if suffix == ".css":
                for candidate in extract_css_urls(decoded):
                    links_checked += 1
                    target, host, _ = resolve_local(path, candidate)
                    if host:
                        external_hosts[host] += 1
                        external_asset_hosts[host] += 1
                    elif target is not None:
                        local_targets_checked += 1
                        local_assets_checked += 1
                        if not target.is_file():
                            broken_targets.append(f"{relative} -> CSS url({candidate})")

    wrong_languages = {lang: count for lang, count in sorted(language_counts.items()) if lang.casefold() != EXPECTED_LANG.casefold()}
    ui_failures: list[str] = []
    for kind, expected in UI_EXPECTATIONS.items():
        observed = set(ui_labels[kind])
        disallowed = sorted(observed - expected)
        if disallowed:
            ui_failures.append(f"{kind}: generated labels not Indonesian: {disallowed}")
        if ui_labels[kind] and not (observed & expected):
            ui_failures.append(f"{kind}: no accepted Indonesian label present")

    css_path = TREE / READABLE_CSS
    css_payload = css_path.read_text(encoding="utf-8") if css_path.is_file() else ""
    css_checks = {
        "asset_exists": css_path.is_file(),
        "linked_from_all_main_documents": len(css_linked_documents) == len(main_documents),
        "desktop_full_width_shell": all(token in css_payload for token in ("@media (min-width: 1200px)", "max-width: 1440px", "width: calc(100% - 240px)")),
        "centered_reading_measure": all(token in css_payload for token in ("max-width: 960px", "margin-left: auto", "margin-right: auto")),
        "tablet_breakpoint": "@media (min-width: 600px) and (max-width: 1199px)" in css_payload,
        "localized_nav_widths": all(token in css_payload for token in (".previous-button", ".next-button", "width: 110px")),
    }

    if parse_failures:
        failures.append(f"HTML parse failures: {len(parse_failures)}")
    if broken_targets:
        failures.append(f"missing or escaping local targets: {len(broken_targets)}")
    if broken_fragments:
        failures.append(f"missing local fragments: {len(broken_fragments)}")
    if broken_embedded_knowls:
        failures.append(f"missing embedded knowl targets: {len(broken_embedded_knowls)}")
    if wrong_languages:
        failures.append(f"wrong or missing html lang; expected {EXPECTED_LANG}: {wrong_languages}")
    failures.extend(ui_failures)
    failures.extend(f"readable-layout CSS check failed: {key}" for key, passed in css_checks.items() if not passed)
    if absolute_local_hits:
        failures.append(f"absolute local path patterns found: {len(absolute_local_hits)}")
    if credential_hits:
        failures.append(f"credential patterns found: {len(credential_hits)}")

    return {
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "counts": {
            "html_documents": len(html_paths),
            "main_reader_documents": len(main_documents),
            "links_and_asset_references_checked": links_checked,
            "local_targets_checked": local_targets_checked,
            "local_assets_checked": local_assets_checked,
            "local_fragments_checked": local_fragments_checked,
        },
        "internal_closure": {
            "status": "pass" if not (parse_failures or broken_targets or broken_fragments or broken_embedded_knowls) else "fail",
            "parse_failures": compact_samples(parse_failures),
            "broken_targets": compact_samples(broken_targets),
            "broken_fragments": compact_samples(broken_fragments),
            "broken_embedded_knowls": compact_samples(broken_embedded_knowls),
        },
        "external_references": {
            "hosts": dict(sorted(external_hosts.items())),
            "asset_hosts": dict(sorted(external_asset_hosts.items())),
            "note": "External references are inventoried, not treated as failures by the bounded internal-closure gate.",
        },
        "language_and_generated_ui": {
            "expected_html_lang": EXPECTED_LANG,
            "html_lang_counts": dict(sorted(language_counts.items())),
            "html_lang_samples": dict(sorted(language_samples.items())),
            "generated_navigation_labels": {kind: dict(sorted(counter.items())) for kind, counter in ui_labels.items()},
            "failures": ui_failures,
        },
        "readable_layout_css": {
            "identity": identity(css_path) if css_path.is_file() else None,
            "linked_main_documents": len(css_linked_documents),
            "expected_main_documents": len(main_documents),
            "checks": css_checks,
        },
        "privacy": {
            "absolute_local_paths": compact_samples(absolute_local_hits),
            "credential_patterns": compact_samples(credential_hits),
            "status": "pass" if not absolute_local_hits and not credential_hits else "fail",
            "note": "Only pattern labels and file paths are recorded; matching secret-like values are never emitted.",
        },
    }


def build() -> tuple[bytes, bytes, bytes]:
    if not TREE.is_dir():
        raise SystemExit(f"HTML tree missing: {TREE.relative_to(ROOT)}")
    required_inputs = [READER, WRAPPER, SCHEMA_QA, BACKEND, SOURCE_QA]
    missing = [path.relative_to(ROOT).as_posix() for path in required_inputs if not path.is_file()]
    if missing:
        raise SystemExit(f"required current receipts missing: {missing}")
    schema = json.loads(SCHEMA_QA.read_text(encoding="utf-8"))
    source_qa = json.loads(SOURCE_QA.read_text(encoding="utf-8"))
    backend = json.loads(BACKEND.read_text(encoding="utf-8"))
    if schema.get("status") != "pass" or schema.get("failures") or schema.get("diagnostics"):
        raise SystemExit("cumulative Modules 1--8 pinned-schema receipt is not passing")
    if source_qa.get("status") != "pass" or source_qa.get("failures"):
        raise SystemExit("cumulative Modules 1--8 source/backend QA is not passing")
    accepted_backend_statuses = {
        "modules_01_08_complete_schema_and_backend_qa_pass",
        "content_complete_schema_and_backend_qa_pass",
    }
    if backend.get("status") not in accepted_backend_statuses:
        raise SystemExit(f"current completion backend status is not sealed: {backend.get('status')!r}")
    if schema.get("source", {}).get("sha256") != identity(READER)["sha256"]:
        raise SystemExit("reader bytes no longer match cumulative schema receipt")
    if schema.get("wrapper", {}).get("sha256") != identity(WRAPPER)["sha256"]:
        raise SystemExit("shared wrapper bytes no longer match cumulative schema receipt")

    rows = inventory_rows()
    tree_sha = canonical_tree_sha256(rows)
    kinds = Counter(str(row["kind"]) for row in rows)
    total_bytes = sum(int(row["bytes"]) for row in rows)
    inventory = {
        "schema_version": 1,
        "tree": TREE.relative_to(ROOT).as_posix(),
        "canonicalization": {
            "algorithm": "sha256",
            "domain_prefix": "O003-C90-MODULES01-08-HTML-TREE-V1\\0",
            "entry_encoding": "UTF-8 POSIX-relative-path NUL decimal-byte-count NUL lowercase-raw-file-sha256 LF",
            "ordering": "UTF-8 bytewise ascending POSIX-relative paths",
            "content_normalization": "none; every raw file byte contributes through its raw SHA-256",
            "path_normalization": "platform separators represented as POSIX / only",
        },
        "canonical_tree_sha256": tree_sha,
        "file_count": len(rows),
        "document_count": kinds.get("html_document", 0),
        "total_bytes": total_bytes,
        "kind_counts": dict(sorted(kinds.items())),
        "files": rows,
    }
    inventory_payload = json_bytes(inventory)
    scan = scan_tree(rows)
    report = {
        "schema_version": 1,
        "status": scan["status"],
        "failures": scan["failures"],
        "inputs": [identity(path) for path in required_inputs],
        "tree": {
            "path": TREE.relative_to(ROOT).as_posix(),
            "file_count": len(rows),
            "document_count": kinds.get("html_document", 0),
            "total_bytes": total_bytes,
            "canonical_tree_sha256": tree_sha,
            "raw_bytes_no_content_normalization": True,
        },
        "inventory_expected": {
            "path": INVENTORY.relative_to(ROOT).as_posix(),
            "bytes": len(inventory_payload),
            "sha256": sha256(inventory_payload),
        },
        "checks": scan,
    }
    report_payload = json_bytes(report)
    failure_lines = "\n".join(f"  - {failure}" for failure in scan["failures"]) or "  - none"
    receipt = f"""# O003/C90 completion Modules 1--8 cumulative HTML QA

Status: **{scan['status']}**

- Tree: `output/o003-completion-modules01-08-html`.
- Files: {len(rows)}; HTML documents: {kinds.get('html_document', 0)}; exact bytes: {total_bytes}.
- Canonical raw-byte tree SHA-256: `{tree_sha}`.
- Inventory SHA-256: `{sha256(inventory_payload)}`.
- QA report SHA-256: `{sha256(report_payload)}`.
- Reader source SHA-256: `{identity(READER)['sha256']}`.
- Shared wrapper SHA-256: `{identity(WRAPPER)['sha256']}`.
- Pinned cumulative schema receipt SHA-256: `{identity(SCHEMA_QA)['sha256']}`.
- Current completion backend manifest SHA-256: `{identity(BACKEND)['sha256']}`.
- Current completion source-QA SHA-256: `{identity(SOURCE_QA)['sha256']}`.

Canonicalization uses exact raw file bytes.  It normalizes no content and strips
no build metadata; only platform path separators are represented as POSIX `/`
before UTF-8 bytewise sorting.

Internal closure: **{scan['internal_closure']['status']}**; privacy: **{scan['privacy']['status']}**.
Readable-layout CSS checks: {scan['readable_layout_css']['checks']}.
HTML language counts: {scan['language_and_generated_ui']['html_lang_counts']}.
Generated navigation labels: {scan['language_and_generated_ui']['generated_navigation_labels']}.

Failures:
{failure_lines}

External hosts are inventoried in the JSON report but are outside this bounded
internal-link closure gate.  This receipt does not claim an offline-closed
reader and does not modify or rebuild the reader, modules, project, chapters,
Git, publication state, or global controls.
""".encode("utf-8")
    return inventory_payload, report_payload, receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="require byte-identical pre-existing outputs")
    args = parser.parse_args()
    inventory_payload, report_payload, receipt_payload = build()
    outputs = ((INVENTORY, inventory_payload), (REPORT, report_payload), (RECEIPT, receipt_payload))
    if args.check:
        for path, payload in outputs:
            if not path.is_file() or path.read_bytes() != payload:
                raise SystemExit(f"deterministic output differs: {path.relative_to(ROOT)}")
    else:
        for path, payload in outputs:
            path.write_bytes(payload)
            if path.read_bytes() != payload:
                raise SystemExit(f"write/readback failed: {path.relative_to(ROOT)}")
    status = json.loads(report_payload)["status"]
    summary = {
        "status": status,
        "check_only": args.check,
        "deterministic_outputs_match": True,
        "outputs": {
            path.relative_to(ROOT).as_posix(): {"bytes": len(payload), "sha256": sha256(payload)}
            for path, payload in outputs
        },
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    # During --check, exit status expresses deterministic identity only.  The
    # persisted JSON retains the independent content-QA status and failures.
    return 0 if args.check or status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
