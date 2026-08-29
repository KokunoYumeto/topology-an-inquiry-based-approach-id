#!/usr/bin/env python3
"""Assemble and seal the complete O003 GitHub Pages tree.

This is an additive, resumable overlay.  It preserves every previously
admitted public byte except the former redirect at ``docs/index.html``, copies
the exact finalized complete HTML reader to ``docs/reader/complete/``, places
the verified complete PDF at a stable download route, and writes one
edition-specific public machine manifest plus deterministic QA receipts.

Normal mode performs the overlay.  ``--check-only`` is read-only and proves
the docs tree and every generated receipt byte for byte.  The script never
runs Git or publishes anything.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
import shutil
from typing import Any
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
HTML_ROOT = ROOT / "output/chapters01-20-complete-html"
HTML_MANIFEST = ROOT / "qa/CHAPTER20_COMPLETE_HTML_MANIFEST.json"
HTML_QA = ROOT / "qa/CHAPTER20_COMPLETE_HTML_QA.json"
PDF = ROOT / "output/chapters01-20-complete-pdf/chapters_01_20_complete_reader.pdf"
PDF_QA = ROOT / "qa/CHAPTERS01_20_COMPLETE_PDF_QA.json"
DOCS_ROOT = ROOT / "docs"
PRIOR_DOCS_FILE_MANIFEST = ROOT / "qa/CHAPTER17_DOCS_FILE_MANIFEST.json"
PRIOR_DOCS_ADMISSION = ROOT / "qa/CHAPTER17_DOCS_MANIFEST.json"
DOCS_FILE_MANIFEST = ROOT / "qa/CHAPTER20_COMPLETE_DOCS_FILE_MANIFEST.json"
DOCS_QA = ROOT / "qa/CHAPTER20_COMPLETE_DOCS_QA.json"
OUTPUT = ROOT / "qa/CHAPTER20_COMPLETE_DOCS_MANIFEST.json"

READER_PREFIX = "reader/complete"
PRIMARY_READER = f"{READER_PREFIX}/frontmatter-1.html"
PRIMARY_DOWNLOAD = "downloads/topologi-pendekatan-berbasis-inkuiri-edisi-lengkap-id.pdf"
PUBLIC_EDITION_MANIFEST = "reader/complete-edition-manifest.json"
ROOT_INDEX = "index.html"
PRIOR_PRIMARY_READER = "o003-c90-chapters-01-17-reader.html"
PRIOR_PRIMARY_DOWNLOAD = "downloads/topologi-pendekatan-berbasis-inkuiri-bab-01-17-id.pdf"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
UPSTREAM_COMMIT = "0c2d8f614ef87aa00de373f3418146c2f1d13bb9"
ALGORITHM = (
    "SHA-256 over UTF-8 lines: relative path, TAB, byte count, TAB, "
    "file SHA-256, LF; paths ordered case-insensitively"
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
TRACKER_RE = re.compile(
    r"(?:google-analytics|googletagmanager|doubleclick|matomo|plausible|"
    r"mixpanel|segment\.io|hotjar|facebook\.net/.+fbevents|sentry\.io)",
    flags=re.IGNORECASE,
)


class ContractError(RuntimeError):
    """A fail-closed deployment contract was not satisfied."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def identity(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"required file is missing: {path}")
    payload = path.read_bytes()
    return {"bytes": len(payload), "sha256": digest(payload)}


def repo_path(path: Path, label: str) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError as exc:
        raise ContractError(f"{label} must stay inside the repository: {path}") from exc


def resolve_input(path: Path) -> Path:
    return path.resolve() if path.is_absolute() else (ROOT / path).resolve()


def json_payload(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def read_json(path: Path, label: str) -> dict[str, Any]:
    require(path.is_file(), f"{label} is missing: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"{label} is not valid UTF-8 JSON: {exc}") from exc
    require(isinstance(value, dict), f"{label} must be a JSON object")
    return value


def clean_relative_path(value: object, label: str) -> str:
    require(isinstance(value, str) and value, f"{label} must be non-empty text")
    require("\\" not in value, f"{label} must use POSIX separators: {value!r}")
    pure = PurePosixPath(value)
    require(not pure.is_absolute(), f"{label} must be relative: {value!r}")
    require(".." not in pure.parts, f"{label} escapes its tree: {value!r}")
    require(pure.as_posix() == value, f"{label} is not normalized: {value!r}")
    return value


def sha256_value(value: object, label: str) -> str:
    require(
        isinstance(value, str) and SHA256_RE.fullmatch(value) is not None,
        f"{label} must be a lowercase SHA-256 digest",
    )
    return value


def nonnegative_int(value: object, label: str, *, positive: bool = False) -> int:
    minimum = 1 if positive else 0
    require(
        isinstance(value, int) and not isinstance(value, bool) and value >= minimum,
        f"{label} must be an integer >= {minimum}",
    )
    return int(value)


def canonical(rows: list[dict[str, Any]]) -> str:
    payload = "".join(
        f"{row['path']}\t{row['bytes']}\t{row['sha256']}\n" for row in rows
    ).encode("utf-8")
    return digest(payload)


def summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "canonical_manifest_sha256": canonical(rows),
        "file_count": len(rows),
        "html_files": sum(
            1 for row in rows if str(row["path"]).lower().endswith((".html", ".htm"))
        ),
        "total_bytes": sum(int(row["bytes"]) for row in rows),
    }


def validate_rows(raw_rows: object, label: str) -> list[dict[str, Any]]:
    require(isinstance(raw_rows, list) and raw_rows, f"{label} has no file rows")
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_rows):
        require(isinstance(raw, dict), f"{label} row {index} is not an object")
        require(set(raw) == {"path", "bytes", "sha256"}, f"{label} row {index} fields differ")
        path = clean_relative_path(raw.get("path"), f"{label} row {index} path")
        size = nonnegative_int(raw.get("bytes"), f"{label} row {index} bytes")
        checksum = sha256_value(raw.get("sha256"), f"{label} row {index} sha256")
        folded = path.casefold()
        require(folded not in seen, f"{label} repeats or case-collides at {path}")
        seen.add(folded)
        rows.append({"path": path, "bytes": size, "sha256": checksum})
    require(
        rows == sorted(rows, key=lambda row: str(row["path"]).casefold()),
        f"{label} rows are not canonically ordered",
    )
    return rows


def assert_manifest_summary(manifest: dict[str, Any], rows: list[dict[str, Any]], label: str) -> None:
    computed = summary(rows)
    for key, value in computed.items():
        require(manifest.get(key) == value, f"{label} {key} differs from its rows")


def actual_rows(root: Path, label: str) -> list[dict[str, Any]]:
    require(root.is_dir(), f"{label} directory is missing: {root}")
    files = sorted(
        (path for path in root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(root).as_posix().casefold(),
    )
    require(files, f"{label} directory is empty")
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in files:
        relative = path.relative_to(root).as_posix()
        folded = relative.casefold()
        require(folded not in seen, f"{label} has a case collision: {relative}")
        seen.add(folded)
        rows.append({"path": relative, **identity(path)})
    return rows


def row_map(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(row["path"]): row for row in rows}


def assert_rows_equal(expected: list[dict[str, Any]], observed: list[dict[str, Any]], label: str) -> None:
    if expected == observed:
        return
    expected_map = row_map(expected)
    observed_map = row_map(observed)
    missing = sorted(set(expected_map) - set(observed_map), key=str.casefold)
    unexpected = sorted(set(observed_map) - set(expected_map), key=str.casefold)
    changed = sorted(
        (
            path
            for path in set(expected_map) & set(observed_map)
            if expected_map[path] != observed_map[path]
        ),
        key=str.casefold,
    )
    raise ContractError(
        f"{label} differs: missing={missing[:8]!r}, unexpected={unexpected[:8]!r}, changed={changed[:8]!r}"
    )


def validate_html_inputs(manifest_path: Path, qa_path: Path, html_root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest = read_json(manifest_path, "complete HTML manifest")
    require(manifest.get("schema_version") == 1, "complete HTML manifest schema differs")
    require(manifest.get("stage") == "finalized", "HTML manifest is not finalized")
    require(manifest.get("target") == "chapters01-20-complete-html", "HTML target differs")
    rows = validate_rows(manifest.get("files"), "complete HTML manifest")
    assert_manifest_summary(manifest, rows, "complete HTML manifest")
    observed = actual_rows(html_root, "complete finalized HTML tree")
    assert_rows_equal(rows, observed, "complete finalized HTML tree")
    paths = {row["path"] for row in rows}
    for required in (
        "index.html",
        "frontmatter-1.html",
        "chap_Product_topology.html",
        "o003-c90-ch20-self-study.html",
        "external/o003-readable-layout.css",
    ):
        require(required in paths, f"complete HTML tree omits {required}")

    qa = read_json(qa_path, "complete HTML QA")
    require(qa.get("schema_version") == 1 and qa.get("status") == "pass", "complete HTML QA did not pass")
    require(qa.get("target") == "chapters01-20-complete-html", "complete HTML QA target differs")
    require(qa.get("failures") == [], "complete HTML QA records failures")
    checks = qa.get("checks")
    require(isinstance(checks, dict) and checks, "complete HTML QA checks are absent")
    failed_checks = [key for key, value in checks.items() if value is not True]
    require(not failed_checks, f"complete HTML QA checks failed: {failed_checks}")
    final = qa.get("final_manifest")
    require(isinstance(final, dict), "complete HTML QA lacks final-manifest identity")
    require(
        final.get("canonical_manifest_sha256") == manifest.get("canonical_manifest_sha256"),
        "HTML manifest and QA canonical identities differ",
    )
    return rows, {
        "manifest": {"path": repo_path(manifest_path, "HTML manifest"), **identity(manifest_path)},
        "qa": {"path": repo_path(qa_path, "HTML QA"), **identity(qa_path)},
        "tree": summary(rows),
    }


def find_pdf_record(value: dict[str, Any], pdf_identity: dict[str, Any]) -> dict[str, Any] | None:
    candidates = [value]
    for key in ("pdf", "artifact", "reader", "output", "run_2"):
        nested = value.get(key)
        if isinstance(nested, dict):
            candidates.append(nested)
    for candidate in candidates:
        if (
            candidate.get("bytes") == pdf_identity["bytes"]
            and candidate.get("sha256") == pdf_identity["sha256"]
            and isinstance(candidate.get("pages"), int)
            and candidate.get("pages") > 0
        ):
            return candidate
    return None


def validate_pdf_input(pdf_path: Path, qa_path: Path) -> tuple[dict[str, Any], int, dict[str, Any]]:
    pdf_identity = identity(pdf_path)
    require(pdf_path.read_bytes().startswith(b"%PDF-"), "complete PDF has no PDF header")
    qa = read_json(qa_path, "complete PDF QA")
    require(qa.get("schema_version") == 1, "complete PDF QA schema differs")
    require(qa.get("status") == "pass", "complete PDF QA did not pass")
    require(qa.get("failures", []) == [], "complete PDF QA records failures")
    record = find_pdf_record(qa, pdf_identity)
    require(record is not None, "complete PDF QA does not bind the final PDF identity/pages")
    checks = qa.get("checks") if isinstance(qa.get("checks"), dict) else {}
    deterministic_builds = (
        qa.get("deterministic_builds")
        if isinstance(qa.get("deterministic_builds"), dict)
        else {}
    )
    deterministic = (
        deterministic_builds.get("normalized_byte_identical") is True
        and checks.get("two_clean_strict_builds") is True
        and checks.get("identical_normalized_pdf_bytes") is True
        and isinstance(deterministic_builds.get("run_1"), dict)
        and isinstance(deterministic_builds.get("run_2"), dict)
        and isinstance(deterministic_builds.get("run_1_log"), dict)
        and isinstance(deterministic_builds.get("run_2_log"), dict)
    )
    require(deterministic, "complete PDF QA does not prove a byte-identical double build")
    pages = int(record["pages"])
    return pdf_identity, pages, {"path": repo_path(qa_path, "PDF QA"), **identity(qa_path)}


def validate_prior_docs(file_manifest_path: Path, admission_path: Path, docs_root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest = read_json(file_manifest_path, "prior docs file manifest")
    require(manifest.get("schema_version") == 1, "prior docs file-manifest schema differs")
    rows = validate_rows(manifest.get("files"), "prior docs file manifest")
    assert_manifest_summary(manifest, rows, "prior docs file manifest")
    paths = {row["path"] for row in rows}
    for path in (ROOT_INDEX, PRIOR_PRIMARY_READER, PRIOR_PRIMARY_DOWNLOAD, ".nojekyll"):
        require(path in paths, f"prior public docs manifest omits {path}")
    admission = read_json(admission_path, "prior docs admission receipt")
    require(admission.get("schema_version") == 1 and admission.get("status") == "pass", "prior docs admission did not pass")
    require(admission.get("failures") == [], "prior docs admission records failures")
    detail = admission.get("detailed_manifest")
    if isinstance(detail, dict):
        observed = identity(file_manifest_path)
        require(
            detail.get("bytes") == observed["bytes"] and detail.get("sha256") == observed["sha256"],
            "prior docs admission does not bind its detailed manifest",
        )
    return rows, {
        "file_manifest": {"path": repo_path(file_manifest_path, "prior docs file manifest"), **identity(file_manifest_path)},
        "admission": {"path": repo_path(admission_path, "prior docs admission"), **identity(admission_path)},
        "primary_reader": row_map(rows)[PRIOR_PRIMARY_READER],
        "primary_download": row_map(rows)[PRIOR_PRIMARY_DOWNLOAD],
    }


def landing_payload() -> bytes:
    value = """<!DOCTYPE html>
<html lang="id-ID" xml:lang="id-ID">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Topologi: Pendekatan Berbasis Inkuiri — Edisi Bahasa Indonesia Lengkap</title>
  <style>
    :root { color-scheme: light dark; font-family: system-ui, sans-serif; }
    body { max-width: 58rem; margin: 0 auto; padding: clamp(1rem, 4vw, 3rem); line-height: 1.6; }
    h1 { line-height: 1.15; }
    nav { display: flex; flex-wrap: wrap; gap: .75rem; margin: 1.5rem 0; }
    a.button { display: inline-block; padding: .7rem 1rem; border: 1px solid currentColor; border-radius: .4rem; }
    code { overflow-wrap: anywhere; }
  </style>
</head>
<body>
  <main>
    <h1>Topologi: Pendekatan Berbasis Inkuiri</h1>
    <p>Edisi Bahasa Indonesia lengkap dengan pembaca HTML yang dapat direflow, PDF, pendamping belajar mandiri, dan materi penyelesaian kurikulum O003/C90.</p>
    <nav aria-label="Akses edisi lengkap">
      <a class="button" href="reader/complete/">Baca edisi lengkap</a>
      <a class="button" href="downloads/topologi-pendekatan-berbasis-inkuiri-edisi-lengkap-id.pdf">Unduh PDF lengkap</a>
      <a class="button" href="reader/complete-edition-manifest.json">Manifest mesin</a>
    </nav>
    <p>Karya sumber Steven Schlicker/GVSU diperlakukan secara konservatif sebagai CC BY-NC-SA 3.0. Materi pendamping orisinal memiliki identitas CC BY 4.0 tersendiri. Lisensi komponen tidak diratakan, dan tidak ada dukungan resmi penulis atau institusi yang dinyatakan ataupun tersirat.</p>
    <p>Rilis historis tetap tersedia, termasuk <a href="o003-c90-chapters-01-17-reader.html">pembaca Bab 1–17</a>.</p>
  </main>
</body>
</html>
"""
    return value.encode("utf-8")


def public_manifest_payload(
    html_evidence: dict[str, Any],
    pdf_identity: dict[str, Any],
    pdf_pages: int,
    pdf_qa_identity: dict[str, Any],
    reader_entry_name: str,
) -> bytes:
    value = {
        "schema_version": 1,
        "status": "complete",
        "work": "Topology: An Inquiry-Based Approach",
        "author": "Steven Schlicker",
        "edition": "Bahasa Indonesia — complete O003/C90 reader",
        "locale": "id-ID",
        "reader": {
            "route": f"{READER_PREFIX}/",
            "landing_page": PRIMARY_READER,
            "book_entry": f"{READER_PREFIX}/{reader_entry_name}",
            **html_evidence["tree"],
        },
        "pdf": {"path": PRIMARY_DOWNLOAD, "pages": pdf_pages, **pdf_identity},
        "source_authority": {
            "upstream_commit": UPSTREAM_COMMIT,
            "translated_spine_license": "CC BY-NC-SA 3.0 (conservative treatment)",
            "original_companion_license": "CC BY 4.0",
            "license_policy": "per-component rights; no flattened license",
            "non_endorsement": True,
        },
        "evidence": {
            "html_manifest": html_evidence["manifest"],
            "html_qa": html_evidence["qa"],
            "pdf_qa": pdf_qa_identity,
        },
        "production_provenance": MODEL,
    }
    return json_payload(value)


def detailed_manifest_payload(rows: list[dict[str, Any]]) -> bytes:
    return json_payload(
        {
            "schema_version": 1,
            "label": "O003/C90 complete-edition GitHub Pages tree",
            "source_directory": ".",
            "glob": "**/*",
            "combined_algorithm": ALGORITHM,
            **summary(rows),
            "files": rows,
        }
    )


class LinkCollector(HTMLParser):
    ATTRIBUTES = frozenset({"href", "src", "poster", "data", "action"})

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.urls: list[tuple[str, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name.lower() in self.ATTRIBUTES and value:
                self.urls.append((tag.lower(), name.lower(), value.strip()))


def resolve_docs_target(root: Path, source: Path, url: str) -> Path | None:
    parsed = urlsplit(url)
    if parsed.scheme.lower() in {"mailto", "tel", "javascript", "data"}:
        return None
    require(not parsed.scheme and not parsed.netloc, f"new public surface has an external URL: {source}: {url}")
    raw = unquote(parsed.path)
    if not raw:
        return source
    target = (root / raw.lstrip("/")).resolve() if raw.startswith("/") else (source.parent / raw).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError as exc:
        raise ContractError(f"new public URL escapes docs: {source}: {url}") from exc
    if raw.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target


def build_docs_qa(
    docs_root: Path,
    rows: list[dict[str, Any]],
    prior_rows: list[dict[str, Any]],
    html_rows: list[dict[str, Any]],
    html_qa_identity: dict[str, Any],
) -> dict[str, Any]:
    failures: list[str] = []
    links_checked = 0
    external_hosts: Counter[str] = Counter()
    prior = row_map(prior_rows)
    current = row_map(rows)
    preserved_paths = sorted(set(prior) - {ROOT_INDEX}, key=str.casefold)
    changed_historical = [path for path in preserved_paths if current.get(path) != prior[path]]
    if changed_historical:
        failures.append(f"historical public bytes changed: {changed_historical[:20]}")

    expected_reader = [
        {"path": f"{READER_PREFIX}/{row['path']}", "bytes": row["bytes"], "sha256": row["sha256"]}
        for row in html_rows
    ]
    observed_reader = [row for row in rows if str(row["path"]).startswith(READER_PREFIX + "/")]
    if expected_reader != observed_reader:
        failures.append("stable complete-reader subtree differs from finalized HTML input")

    for relative in (ROOT_INDEX,):
        source = docs_root / relative
        try:
            text = source.read_text(encoding="utf-8")
            require(not TRACKER_RE.search(text), f"tracker reference in {relative}")
            parser = LinkCollector()
            parser.feed(text)
            parser.close()
            for _, _, url in parser.urls:
                links_checked += 1
                target = resolve_docs_target(docs_root, source, url)
                if target is not None and not target.is_file():
                    failures.append(f"{relative}: missing local target: {url}")
        except (OSError, UnicodeDecodeError, ContractError) as exc:
            failures.append(str(exc))

    public_manifest_path = docs_root / PUBLIC_EDITION_MANIFEST
    try:
        manifest = json.loads(public_manifest_path.read_text(encoding="utf-8"))
        require(manifest.get("status") == "complete", "public edition manifest status differs")
        require(manifest.get("locale") == "id-ID", "public edition manifest locale differs")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ContractError) as exc:
        failures.append(f"public edition manifest is invalid: {exc}")

    required = (
        ROOT_INDEX,
        f"{READER_PREFIX}/index.html",
        PRIMARY_READER,
        PRIMARY_DOWNLOAD,
        PUBLIC_EDITION_MANIFEST,
        PRIOR_PRIMARY_READER,
        PRIOR_PRIMARY_DOWNLOAD,
        ".nojekyll",
    )
    missing = [path for path in required if path not in current]
    if missing:
        failures.append(f"required docs surfaces are missing: {missing}")

    return {
        "schema_version": 1,
        "status": "pass" if not failures else "fail",
        **summary(rows),
        "stable_reader_route": f"{READER_PREFIX}/",
        "primary_reader": PRIMARY_READER,
        "primary_download": PRIMARY_DOWNLOAD,
        "historical_preservation": {
            "status": "pass" if not changed_historical else "fail",
            "preserved_files": len(preserved_paths),
            "replaced_prior_root_index": prior[ROOT_INDEX],
            "changed_historical_paths": changed_historical,
        },
        "current_edition": {
            "reader_files": len(html_rows),
            "reader_canonical_manifest_sha256": canonical(html_rows),
            "input_html_qa": html_qa_identity,
            "offline_privacy_gate": "inherited exact pass from complete HTML QA and byte-identical reader subtree",
        },
        "root_links_checked": links_checked,
        "external_hosts_on_new_root": dict(sorted(external_hosts.items())),
        "required_surfaces": list(required),
        "failures": failures,
    }


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    require(not temporary.exists(), f"stale temporary file blocks atomic write: {temporary}")
    temporary.write_bytes(payload)
    require(temporary.read_bytes() == payload, f"temporary readback failed: {temporary}")
    temporary.replace(path)
    require(path.read_bytes() == payload, f"atomic write readback failed: {path}")


def preflight_overlay(
    docs_root: Path,
    prior_rows: list[dict[str, Any]],
    final_rows: list[dict[str, Any]],
) -> None:
    observed = row_map(actual_rows(docs_root, "existing docs tree"))
    prior = row_map(prior_rows)
    final = row_map(final_rows)
    for path in set(prior) - {ROOT_INDEX}:
        require(observed.get(path) == prior[path], f"historical public byte differs before overlay: {path}")
    require(set(observed) <= set(final), "existing docs tree contains paths outside the complete overlay contract")
    for path, row in observed.items():
        require(
            row == final[path] or (path == ROOT_INDEX and row == prior[path]),
            f"existing docs byte is neither prior nor final: {path}",
        )


def apply_overlay(
    html_root: Path,
    html_rows: list[dict[str, Any]],
    pdf_path: Path,
    docs_root: Path,
    landing: bytes,
    public_manifest: bytes,
) -> None:
    reader_root = docs_root / PurePosixPath(READER_PREFIX)
    for row in html_rows:
        relative = PurePosixPath(str(row["path"]))
        source = html_root / relative
        target = reader_root / relative
        expected = {"bytes": row["bytes"], "sha256": row["sha256"]}
        if target.is_file() and identity(target) == expected:
            continue
        require(not target.exists(), f"refusing to overwrite a differing complete-reader byte: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        require(identity(target) == expected, f"reader copy readback failed: {target}")

    pdf_target = docs_root / PurePosixPath(PRIMARY_DOWNLOAD)
    expected_pdf = identity(pdf_path)
    if not pdf_target.is_file():
        pdf_target.parent.mkdir(parents=True, exist_ok=True)
        temporary = pdf_target.with_name(f".{pdf_target.name}.tmp")
        require(not temporary.exists(), f"stale PDF temporary file blocks overlay: {temporary}")
        shutil.copyfile(pdf_path, temporary)
        require(identity(temporary) == expected_pdf, "complete PDF temporary readback failed")
        temporary.replace(pdf_target)
    require(identity(pdf_target) == expected_pdf, "public complete PDF identity differs")

    atomic_write(docs_root / PUBLIC_EDITION_MANIFEST, public_manifest)
    atomic_write(docs_root / ROOT_INDEX, landing)


def manifest_payload(rows: list[dict[str, Any]]) -> bytes:
    return json_payload(
        {
            "schema_version": 1,
            "label": "O003/C90 complete-edition GitHub Pages tree",
            "source_directory": ".",
            "glob": "**/*",
            "combined_algorithm": ALGORITHM,
            **summary(rows),
            "files": rows,
        }
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--html-root", type=Path, default=HTML_ROOT)
    parser.add_argument("--html-manifest", type=Path, default=HTML_MANIFEST)
    parser.add_argument("--html-qa", type=Path, default=HTML_QA)
    parser.add_argument("--pdf", type=Path, default=PDF)
    parser.add_argument("--pdf-qa", type=Path, default=PDF_QA)
    parser.add_argument("--docs-root", type=Path, default=DOCS_ROOT)
    parser.add_argument("--prior-docs-file-manifest", type=Path, default=PRIOR_DOCS_FILE_MANIFEST)
    parser.add_argument("--prior-docs-admission", type=Path, default=PRIOR_DOCS_ADMISSION)
    parser.add_argument("--docs-file-manifest", type=Path, default=DOCS_FILE_MANIFEST)
    parser.add_argument("--docs-qa", type=Path, default=DOCS_QA)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    html_root = resolve_input(args.html_root)
    html_manifest_path = resolve_input(args.html_manifest)
    html_qa_path = resolve_input(args.html_qa)
    pdf_path = resolve_input(args.pdf)
    pdf_qa_path = resolve_input(args.pdf_qa)
    docs_root = resolve_input(args.docs_root)
    prior_file_manifest_path = resolve_input(args.prior_docs_file_manifest)
    prior_admission_path = resolve_input(args.prior_docs_admission)
    docs_file_manifest_path = resolve_input(args.docs_file_manifest)
    docs_qa_path = resolve_input(args.docs_qa)
    output_path = resolve_input(args.output)

    html_rows, html_evidence = validate_html_inputs(
        html_manifest_path, html_qa_path, html_root
    )
    pdf_identity, pdf_pages, pdf_qa_identity = validate_pdf_input(pdf_path, pdf_qa_path)
    prior_rows, prior_evidence = validate_prior_docs(
        prior_file_manifest_path, prior_admission_path, docs_root
    )
    prior = row_map(prior_rows)
    require(READER_PREFIX + "/index.html" not in prior, "stable complete-reader route already belongs to prior admission")
    require(PRIMARY_DOWNLOAD not in prior, "complete PDF route already belongs to prior admission")
    require(PUBLIC_EDITION_MANIFEST not in prior, "complete public manifest route already belongs to prior admission")

    book_entries = sorted(
        str(row["path"])
        for row in html_rows
        if str(row["path"]) == "o003-c90-complete-reader.html"
    )
    require(len(book_entries) == 1, f"complete HTML book entry is ambiguous: {book_entries}")
    landing = landing_payload()
    public_manifest = public_manifest_payload(
        html_evidence, pdf_identity, pdf_pages, pdf_qa_identity, book_entries[0]
    )

    final_map = dict(prior)
    final_map[ROOT_INDEX] = {"path": ROOT_INDEX, "bytes": len(landing), "sha256": digest(landing)}
    for row in html_rows:
        path = f"{READER_PREFIX}/{row['path']}"
        require(path not in final_map, f"complete reader collides with prior docs path: {path}")
        final_map[path] = {"path": path, "bytes": row["bytes"], "sha256": row["sha256"]}
    final_map[PRIMARY_DOWNLOAD] = {"path": PRIMARY_DOWNLOAD, **pdf_identity}
    final_map[PUBLIC_EDITION_MANIFEST] = {
        "path": PUBLIC_EDITION_MANIFEST,
        "bytes": len(public_manifest),
        "sha256": digest(public_manifest),
    }
    final_rows = [final_map[path] for path in sorted(final_map, key=str.casefold)]

    if args.check_only:
        assert_rows_equal(final_rows, actual_rows(docs_root, "complete docs tree"), "complete docs tree")
    else:
        preflight_overlay(docs_root, prior_rows, final_rows)
        apply_overlay(html_root, html_rows, pdf_path, docs_root, landing, public_manifest)
        assert_rows_equal(final_rows, actual_rows(docs_root, "complete docs tree"), "complete docs tree after overlay")

    docs_qa_value = build_docs_qa(
        docs_root, final_rows, prior_rows, html_rows, html_evidence["qa"]
    )
    require(docs_qa_value["status"] == "pass", f"complete docs QA failed: {docs_qa_value['failures'][:10]}")
    detailed_payload = manifest_payload(final_rows)
    qa_payload = json_payload(docs_qa_value)
    output_value = {
        "schema_version": 1,
        "status": "pass",
        "scope": "complete O003/C90 Bahasa Indonesia GitHub Pages edition",
        **summary(final_rows),
        "stable_reader_route": f"{READER_PREFIX}/",
        "primary_reader": row_map(final_rows)[PRIMARY_READER],
        "primary_download": {**row_map(final_rows)[PRIMARY_DOWNLOAD], "pages": pdf_pages},
        "public_edition_manifest": row_map(final_rows)[PUBLIC_EDITION_MANIFEST],
        "root_landing_page": row_map(final_rows)[ROOT_INDEX],
        "input_html": html_evidence,
        "input_pdf_qa": pdf_qa_identity,
        "historical_retention": {
            "status": "pass",
            **prior_evidence,
            "preserved_file_count": len(prior_rows) - 1,
            "only_replaced_path": ROOT_INDEX,
        },
        "detailed_manifest": {
            "path": repo_path(docs_file_manifest_path, "docs file manifest"),
            "bytes": len(detailed_payload),
            "sha256": digest(detailed_payload),
        },
        "docs_qa": {
            "path": repo_path(docs_qa_path, "docs QA"),
            "bytes": len(qa_payload),
            "sha256": digest(qa_payload),
        },
        "rights": {
            "translated_gvsu_spine": "CC BY-NC-SA 3.0 (conservative treatment)",
            "original_companions_and_completion": "CC BY 4.0",
            "collection_policy": "per-component rights; no flattened license",
            "non_endorsement": True,
        },
        "production_provenance": MODEL,
        "failures": [],
    }
    output_payload = json_payload(output_value)

    if args.check_only:
        require(docs_file_manifest_path.read_bytes() == detailed_payload, "complete docs file manifest differs")
        require(docs_qa_path.read_bytes() == qa_payload, "complete docs QA receipt differs")
        require(output_path.read_bytes() == output_payload, "complete docs admission receipt differs")
    else:
        atomic_write(docs_file_manifest_path, detailed_payload)
        atomic_write(docs_qa_path, qa_payload)
        atomic_write(output_path, output_payload)

    print(
        json.dumps(
            {
                "status": "pass",
                "mode": "check-only" if args.check_only else "write",
                "stable_reader_route": f"{READER_PREFIX}/",
                "output": repo_path(output_path, "output receipt"),
                "bytes": len(output_payload),
                "sha256": digest(output_payload),
                "file_count": len(final_rows),
                "canonical_manifest_sha256": canonical(final_rows),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContractError as exc:
        raise SystemExit(f"FAIL: {exc}") from exc
