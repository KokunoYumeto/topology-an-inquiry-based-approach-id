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
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
from typing import Any
from urllib.parse import unquote, urlsplit


SCRIPT_PATH = Path(os.path.abspath(__file__))
ROOT = SCRIPT_PATH.parents[1]
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


class RollbackError(ContractError):
    """A transaction failed and at least one backup could not be restored."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def lexists(path: Path) -> bool:
    return os.path.lexists(os.fspath(path))


def lexical_absolute(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def reject_reparse_components(path: Path, label: str) -> None:
    """Reject symlinks, junctions, and other reparse points without following them."""
    absolute = lexical_absolute(path)
    components = [absolute, *absolute.parents]
    for component in reversed(components):
        if not lexists(component):
            continue
        try:
            metadata = os.lstat(component)
        except OSError as exc:
            raise ContractError(f"cannot inspect {label} path component {component}: {exc}") from exc
        attributes = int(getattr(metadata, "st_file_attributes", 0))
        reparse_mask = int(getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))
        require(
            not stat.S_ISLNK(metadata.st_mode) and not (attributes & reparse_mask),
            f"{label} contains a symlink, junction, or reparse point: {component}",
        )


def require_plain_directory(path: Path, label: str) -> None:
    reject_reparse_components(path, label)
    require(lexists(path), f"{label} directory is missing: {path}")
    try:
        metadata = os.lstat(path)
    except OSError as exc:
        raise ContractError(f"cannot inspect {label} directory {path}: {exc}") from exc
    require(stat.S_ISDIR(metadata.st_mode), f"{label} is not a plain directory: {path}")


def require_plain_file(path: Path, label: str) -> None:
    reject_reparse_components(path, label)
    require(lexists(path), f"{label} is missing: {path}")
    try:
        metadata = os.lstat(path)
    except OSError as exc:
        raise ContractError(f"cannot inspect {label} file {path}: {exc}") from exc
    require(stat.S_ISREG(metadata.st_mode), f"{label} is not a plain regular file: {path}")


def identity(path: Path) -> dict[str, Any]:
    require_plain_file(path, "required input")
    payload = path.read_bytes()
    return {"bytes": len(payload), "sha256": digest(payload)}


def repo_path(path: Path, label: str) -> str:
    reject_reparse_components(path, label)
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError as exc:
        raise ContractError(f"{label} must stay inside the repository: {path}") from exc


def resolve_input(path: Path) -> Path:
    candidate = path if path.is_absolute() else ROOT / path
    return lexical_absolute(candidate)


def json_payload(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def read_json(path: Path, label: str) -> dict[str, Any]:
    require_plain_file(path, label)
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
    require(value != ".", f"{label} must identify a file: {value!r}")
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
    folded_paths = {str(row["path"]).casefold() for row in rows}
    for row in rows:
        parts = PurePosixPath(str(row["path"])).parts
        for length in range(1, len(parts)):
            ancestor = PurePosixPath(*parts[:length]).as_posix().casefold()
            require(
                ancestor not in folded_paths,
                f"{label} has a file/descendant conflict at {row['path']}",
            )
    return rows


def assert_manifest_summary(manifest: dict[str, Any], rows: list[dict[str, Any]], label: str) -> None:
    computed = summary(rows)
    for key, value in computed.items():
        require(manifest.get(key) == value, f"{label} {key} differs from its rows")


def actual_rows(root: Path, label: str) -> list[dict[str, Any]]:
    require_plain_directory(root, label)
    files: list[Path] = []
    try:
        for current_text, directory_names, file_names in os.walk(
            root, topdown=True, followlinks=False
        ):
            current = Path(current_text)
            require_plain_directory(current, label)
            directory_names.sort(key=str.casefold)
            file_names.sort(key=str.casefold)
            for name in directory_names:
                child = current / name
                reject_reparse_components(child, label)
                metadata = os.lstat(child)
                require(
                    stat.S_ISDIR(metadata.st_mode),
                    f"{label} contains a non-directory tree node: {child}",
                )
            for name in file_names:
                child = current / name
                require_plain_file(child, label)
                files.append(child)
    except OSError as exc:
        raise ContractError(f"cannot inventory {label}: {exc}") from exc
    files.sort(key=lambda path: path.relative_to(root).as_posix().casefold())
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


def folded_row_map(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(row["path"]).casefold(): row for row in rows}


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
    require(isinstance(detail, dict), "prior docs admission omits its detailed manifest binding")
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


def replacement_paths(rows: list[dict[str, Any]]) -> set[str]:
    return {
        str(row["path"])
        for row in rows
        if str(row["path"]).casefold().startswith((READER_PREFIX + "/").casefold())
        or str(row["path"]).casefold()
        in {
            ROOT_INDEX.casefold(),
            PRIMARY_DOWNLOAD.casefold(),
            PUBLIC_EDITION_MANIFEST.casefold(),
        }
    }


def prove_replacement_scope_disjoint(
    prior_rows: list[dict[str, Any]],
    edition_rows: list[dict[str, Any]],
) -> None:
    preserved = {
        str(row["path"]).casefold()
        for row in prior_rows
        if str(row["path"]).casefold() != ROOT_INDEX.casefold()
    }
    owned = {path.casefold() for path in replacement_paths(edition_rows)}
    require(
        owned.isdisjoint(preserved),
        "complete-edition replacement scope intersects preserved historical rows",
    )
    for historical in preserved:
        historical_parts = PurePosixPath(historical).parts
        for replacement in owned:
            replacement_parts = PurePosixPath(replacement).parts
            shorter = min(len(historical_parts), len(replacement_parts))
            require(
                historical_parts[:shorter] != replacement_parts[:shorter]
                or len(historical_parts) == len(replacement_parts),
                "complete-edition replacement scope has a file/descendant conflict "
                f"with historical path {historical}",
            )


def bound_maintenance_predecessor(
    admission: dict[str, Any],
    *,
    expected_path: Path | None = None,
    docs_root: Path | None = None,
) -> dict[str, Any] | None:
    reference = admission.get("maintenance_predecessor")
    if reference is None:
        return None
    require(isinstance(reference, dict), "maintenance predecessor binding is not an object")
    require(
        set(reference) == {"path", "bytes", "sha256"},
        "maintenance predecessor binding fields differ",
    )
    relative = clean_relative_path(reference.get("path"), "maintenance predecessor path")
    receipt_path = lexical_absolute(ROOT / PurePosixPath(relative))
    try:
        receipt_path.relative_to(ROOT)
    except ValueError as exc:
        raise ContractError("maintenance predecessor path escapes the repository") from exc
    if docs_root is not None:
        try:
            receipt_path.relative_to(lexical_absolute(docs_root))
        except ValueError:
            pass
        else:
            raise ContractError("maintenance predecessor receipt must stay outside docs")
    if expected_path is not None:
        require(
            receipt_path == lexical_absolute(expected_path),
            "maintenance predecessor path differs from the requested receipt",
        )
    observed = identity(receipt_path)
    require(
        reference.get("bytes") == observed["bytes"]
        and reference.get("sha256") == observed["sha256"],
        "maintenance predecessor binding differs from its receipt bytes",
    )
    receipt = read_json(receipt_path, "maintenance predecessor receipt")
    require(
        receipt.get("schema_version") == 1 and receipt.get("status") == "pass",
        "maintenance predecessor receipt did not pass",
    )
    return {"path": relative, **observed}


def prepare_maintenance_overlay(
    docs_root: Path,
    current_file_manifest_path: Path,
    current_qa_path: Path,
    current_admission_path: Path,
    prior_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate the complete predecessor without changing any live path."""
    manifest = read_json(current_file_manifest_path, "current complete docs file manifest")
    require(manifest.get("schema_version") == 1, "current complete docs file-manifest schema differs")
    current_rows = validate_rows(manifest.get("files"), "current complete docs file manifest")
    assert_manifest_summary(manifest, current_rows, "current complete docs file manifest")
    observed_rows = actual_rows(docs_root, "current complete docs tree")
    assert_rows_equal(current_rows, observed_rows, "current complete docs tree before maintenance")

    admission = read_json(current_admission_path, "current complete docs admission")
    require(admission.get("schema_version") == 1 and admission.get("status") == "pass", "current complete docs admission did not pass")
    require(admission.get("failures") == [], "current complete docs admission records failures")
    for key, value in summary(current_rows).items():
        require(admission.get(key) == value, f"current complete docs admission {key} differs")
    require(
        admission.get("stable_reader_route") == f"{READER_PREFIX}/",
        "current complete docs admission stable reader route differs",
    )
    detail = admission.get("detailed_manifest")
    require(isinstance(detail, dict), "current complete docs admission omits detailed manifest identity")
    current_manifest_identity = identity(current_file_manifest_path)
    require(
        detail.get("path") == repo_path(current_file_manifest_path, "current docs file manifest")
        and
        detail.get("bytes") == current_manifest_identity["bytes"]
        and detail.get("sha256") == current_manifest_identity["sha256"],
        "current complete docs admission does not bind its detailed manifest",
    )
    qa_identity = identity(current_qa_path)
    qa_reference = admission.get("docs_qa")
    require(isinstance(qa_reference, dict), "current complete docs admission omits docs QA identity")
    require(
        qa_reference.get("path") == repo_path(current_qa_path, "current docs QA")
        and qa_reference.get("bytes") == qa_identity["bytes"]
        and qa_reference.get("sha256") == qa_identity["sha256"],
        "current complete docs admission does not bind its docs QA receipt",
    )
    current_qa = read_json(current_qa_path, "current complete docs QA")
    require(
        current_qa.get("schema_version") == 1
        and current_qa.get("status") == "pass"
        and current_qa.get("failures") == [],
        "current complete docs QA did not pass",
    )
    for key, value in summary(current_rows).items():
        require(current_qa.get(key) == value, f"current complete docs QA {key} differs")

    replaceable = sorted(replacement_paths(current_rows), key=str.casefold)
    require(f"{READER_PREFIX}/index.html" in replaceable, "current complete reader route is absent")
    require(PRIMARY_DOWNLOAD in replaceable, "current complete PDF route is absent")
    require(PUBLIC_EDITION_MANIFEST in replaceable, "current complete manifest route is absent")
    require(ROOT_INDEX in replaceable, "current complete landing page is absent")
    prove_replacement_scope_disjoint(prior_rows, current_rows)

    current = row_map(current_rows)
    preserved_rows = [row for row in prior_rows if row["path"] != ROOT_INDEX]
    preserved = row_map(preserved_rows)
    for path, row in preserved.items():
        require(current.get(path) == row, f"historical public byte differs before maintenance: {path}")
    require(
        set(current) == set(preserved) | set(replaceable),
        "current docs rows do not decompose into preserved history and owned replacement scope",
    )
    bound_predecessor = bound_maintenance_predecessor(admission, docs_root=docs_root)
    predecessor = {
        "schema_version": 1,
        "status": "pass",
        "scope": "validated complete-edition predecessor for transactional maintenance",
        "docs_tree": summary(current_rows),
        "file_manifest": {"path": repo_path(current_file_manifest_path, "current docs file manifest"), **current_manifest_identity},
        "admission": {"path": repo_path(current_admission_path, "current docs admission"), **identity(current_admission_path)},
        "docs_qa": {"path": repo_path(current_qa_path, "current docs QA"), **qa_identity},
        "previous_maintenance_predecessor": bound_predecessor,
        "replacement_scope": {
            "path_count": len(replaceable),
            "reader_prefix": f"{READER_PREFIX}/",
            "singletons": [ROOT_INDEX, PRIMARY_DOWNLOAD, PUBLIC_EDITION_MANIFEST],
            "canonical_manifest_sha256": canonical([current[path] for path in replaceable]),
            "disjoint_from_preserved_historical_rows": True,
        },
        "preserved_historical_rows": summary(preserved_rows),
    }
    return {
        "current_rows": current_rows,
        "current_file_manifest": current_manifest_identity,
        "current_qa": qa_identity,
        "current_admission": identity(current_admission_path),
        "bound_predecessor": bound_predecessor,
        "predecessor_payload": json_payload(predecessor),
        "replaceable_paths": replaceable,
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


def resolve_docs_target(source: str, url: str) -> str | None:
    parsed = urlsplit(url)
    if parsed.scheme.lower() in {"mailto", "tel", "javascript", "data"}:
        return None
    require(
        not parsed.scheme and not parsed.netloc,
        f"new public surface has an external URL: {source}: {url}",
    )
    raw = unquote(parsed.path)
    if not raw:
        return source
    require("\\" not in raw and "\x00" not in raw, f"new public URL is unsafe: {source}: {url}")
    base = PurePosixPath() if raw.startswith("/") else PurePosixPath(source).parent
    combined = base / PurePosixPath(raw.lstrip("/"))
    normalized_parts: list[str] = []
    for part in combined.parts:
        if part in {"", "."}:
            continue
        if part == "..":
            require(normalized_parts, f"new public URL escapes docs: {source}: {url}")
            normalized_parts.pop()
        else:
            normalized_parts.append(part)
    require(normalized_parts, f"new public URL has no target: {source}: {url}")
    target = PurePosixPath(*normalized_parts)
    if raw.endswith("/"):
        target /= "index.html"
    return clean_relative_path(target.as_posix(), f"new public URL target from {source}")


def build_docs_qa(
    rows: list[dict[str, Any]],
    prior_rows: list[dict[str, Any]],
    html_rows: list[dict[str, Any]],
    html_qa_identity: dict[str, Any],
    landing: bytes,
    public_manifest_payload: bytes,
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

    for relative, payload in ((ROOT_INDEX, landing),):
        try:
            text = payload.decode("utf-8")
            require(not TRACKER_RE.search(text), f"tracker reference in {relative}")
            parser = LinkCollector()
            parser.feed(text)
            parser.close()
            for _, _, url in parser.urls:
                links_checked += 1
                target = resolve_docs_target(relative, url)
                if target is not None and target not in current:
                    failures.append(f"{relative}: missing local target: {url}")
        except (UnicodeDecodeError, ContractError) as exc:
            failures.append(str(exc))

    try:
        manifest = json.loads(public_manifest_payload.decode("utf-8"))
        require(manifest.get("status") == "complete", "public edition manifest status differs")
        require(manifest.get("locale") == "id-ID", "public edition manifest locale differs")
    except (UnicodeDecodeError, json.JSONDecodeError, ContractError) as exc:
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


def require_inside_repository(path: Path, label: str) -> None:
    reject_reparse_components(path, label)
    try:
        lexical_absolute(path).relative_to(lexical_absolute(ROOT))
    except ValueError as exc:
        raise ContractError(f"{label} must stay inside the repository: {path}") from exc


def validate_transaction_layout(
    docs_root: Path,
    receipt_targets: list[Path],
    immutable_inputs: list[Path],
) -> None:
    require_plain_directory(docs_root, "docs root")
    require_inside_repository(docs_root, "docs root")
    docs_targets = [
        docs_root / PurePosixPath(READER_PREFIX),
        docs_root / PurePosixPath(PRIMARY_DOWNLOAD),
        docs_root / PurePosixPath(PUBLIC_EDITION_MANIFEST),
        docs_root / ROOT_INDEX,
    ]
    targets = [lexical_absolute(path) for path in docs_targets + receipt_targets]
    folded = [os.fspath(path).casefold() for path in targets]
    require(len(folded) == len(set(folded)), "transaction targets repeat or case-collide")
    for index, path in enumerate(targets):
        require_inside_repository(path, f"transaction target {index}")
        require_plain_directory(path.parent, f"transaction target {index} parent")
        try:
            path.relative_to(docs_root)
            is_docs_target = True
        except ValueError:
            is_docs_target = False
        require(
            is_docs_target == (index < len(docs_targets)),
            "receipt targets must remain outside docs and public targets must remain inside docs",
        )
    for left_index, left in enumerate(targets):
        for right in targets[left_index + 1 :]:
            require(
                left not in right.parents and right not in left.parents,
                f"transaction targets have an ancestor/descendant conflict: {left} and {right}",
            )
    target_keys = set(folded)
    for source in immutable_inputs:
        require_inside_repository(source, "immutable transaction input")
        absolute_source = lexical_absolute(source)
        require(
            os.fspath(absolute_source).casefold() not in target_keys,
            f"transaction target collides with immutable input: {source}",
        )
        for target in targets:
            require(
                absolute_source not in target.parents
                and target not in absolute_source.parents,
                f"transaction target and immutable input overlap: {target} and {source}",
            )


def validate_owned_receipt_target(path: Path, kind: str) -> None:
    reject_reparse_components(path, f"{kind} receipt target")
    if not lexists(path):
        return
    value = read_json(path, f"existing {kind} receipt target")
    require(value.get("schema_version") == 1, f"existing {kind} receipt is not owned schema 1")
    if kind == "docs file manifest":
        require(
            value.get("label") == "O003/C90 complete-edition GitHub Pages tree",
            "existing docs file manifest target is not an owned complete-edition receipt",
        )
        rows = validate_rows(value.get("files"), "existing docs file manifest target")
        assert_manifest_summary(value, rows, "existing docs file manifest target")
    elif kind == "docs QA":
        require(
            value.get("stable_reader_route") == f"{READER_PREFIX}/"
            and value.get("status") == "pass",
            "existing docs QA target is not an owned passing complete-edition receipt",
        )
    elif kind == "admission":
        require(
            value.get("scope")
            == "complete O003/C90 Bahasa Indonesia GitHub Pages edition"
            and value.get("status") == "pass",
            "existing admission target is not an owned passing complete-edition receipt",
        )
    elif kind == "maintenance predecessor":
        require(
            value.get("status") == "pass"
            and value.get("scope")
            in {
                "validated complete-edition routes replaced by terminology maintenance",
                "validated complete-edition predecessor for transactional maintenance",
            },
            "existing maintenance predecessor target is not an owned receipt",
        )
    else:
        raise ContractError(f"unknown receipt target kind: {kind}")


def create_owned_stage(docs_root: Path) -> tuple[Path, bytes]:
    parent = docs_root.parent
    require_plain_directory(parent, "transaction staging parent")
    require_inside_repository(parent, "transaction staging parent")
    stage = Path(
        tempfile.mkdtemp(
            prefix=f".{docs_root.name}.seal-chapter20-complete-docs.",
            dir=os.fspath(parent),
        )
    )
    require(stage.parent == parent, "transaction stage is not a sibling of docs root")
    marker = json_payload(
        {
            "schema_version": 1,
            "owner": "seal_chapter20_complete_docs.py",
            "pid": os.getpid(),
            "stage_name": stage.name,
        }
    )
    marker_path = stage / ".transaction-owner.json"
    with os.fdopen(
        os.open(marker_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600), "wb"
    ) as handle:
        handle.write(marker)
        handle.flush()
        os.fsync(handle.fileno())
    require(marker_path.read_bytes() == marker, "transaction ownership marker readback failed")
    return stage, marker


def require_plain_tree(root: Path, label: str) -> None:
    require_plain_directory(root, label)
    try:
        for current_text, directory_names, file_names in os.walk(
            root, topdown=True, followlinks=False
        ):
            current = Path(current_text)
            require_plain_directory(current, label)
            for name in directory_names:
                child = current / name
                reject_reparse_components(child, label)
                require(
                    stat.S_ISDIR(os.lstat(child).st_mode),
                    f"{label} contains a non-directory node: {child}",
                )
            for name in file_names:
                require_plain_file(current / name, label)
    except OSError as exc:
        raise ContractError(f"cannot inspect {label}: {exc}") from exc


def remove_owned_stage(stage: Path, marker: bytes) -> None:
    require(
        stage.name.startswith(f".{DOCS_ROOT.name}.seal-chapter20-complete-docs.")
        or ".seal-chapter20-complete-docs." in stage.name,
        f"refusing to clean an unrecognized transaction directory: {stage}",
    )
    marker_path = stage / ".transaction-owner.json"
    require_plain_file(marker_path, "transaction ownership marker")
    require(marker_path.read_bytes() == marker, "transaction ownership marker changed")
    require_plain_tree(stage, "owned transaction stage")
    shutil.rmtree(stage)
    require(not lexists(stage), f"owned transaction stage cleanup failed: {stage}")


def stage_bytes(path: Path, payload: bytes, label: str) -> None:
    require(not lexists(path), f"staged {label} already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    reject_reparse_components(path.parent, f"staged {label} parent")
    path.write_bytes(payload)
    require(identity(path) == {"bytes": len(payload), "sha256": digest(payload)}, f"staged {label} readback failed")


def stage_bundle(
    stage: Path,
    html_root: Path,
    html_rows: list[dict[str, Any]],
    pdf_path: Path,
    pdf_identity: dict[str, Any],
    landing: bytes,
    public_manifest: bytes,
    detailed_payload: bytes,
    qa_payload: bytes,
    output_payload: bytes,
    predecessor_payload: bytes | None,
) -> dict[str, Path]:
    payload_root = stage / "candidate"
    payload_root.mkdir()
    reader_root = payload_root / "complete-reader"
    reader_root.mkdir()
    for row in html_rows:
        relative = PurePosixPath(str(row["path"]))
        source = html_root / relative
        target = reader_root / relative
        expected = {"bytes": row["bytes"], "sha256": row["sha256"]}
        require(not lexists(target), f"duplicate staged complete-reader byte: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        reject_reparse_components(target.parent, "staged complete-reader parent")
        shutil.copyfile(source, target)
        require(identity(target) == expected, f"staged reader copy readback failed: {target}")
    assert_rows_equal(html_rows, actual_rows(reader_root, "staged complete reader"), "staged complete reader")

    pdf_target = payload_root / "complete.pdf"
    expected_pdf = pdf_identity
    require(identity(pdf_path) == expected_pdf, "complete PDF changed before staging")
    shutil.copyfile(pdf_path, pdf_target)
    require(identity(pdf_target) == expected_pdf, "staged complete PDF readback failed")

    paths = {
        "complete_reader": reader_root,
        "complete_pdf": pdf_target,
        "public_manifest": payload_root / "public-manifest.json",
        "root_landing": payload_root / "index.html",
        "docs_file_manifest": payload_root / "docs-file-manifest.json",
        "docs_qa": payload_root / "docs-qa.json",
        "admission": payload_root / "admission.json",
    }
    stage_bytes(paths["public_manifest"], public_manifest, "public manifest")
    stage_bytes(paths["root_landing"], landing, "root landing")
    stage_bytes(paths["docs_file_manifest"], detailed_payload, "docs file manifest")
    stage_bytes(paths["docs_qa"], qa_payload, "docs QA")
    stage_bytes(paths["admission"], output_payload, "docs admission")
    if predecessor_payload is not None:
        paths["maintenance_predecessor"] = payload_root / "maintenance-predecessor.json"
        stage_bytes(
            paths["maintenance_predecessor"],
            predecessor_payload,
            "maintenance predecessor",
        )
    require_plain_tree(stage, "complete staged transaction")
    return paths


def target_snapshot(path: Path, kind: str, label: str) -> dict[str, Any] | None:
    reject_reparse_components(path, label)
    if not lexists(path):
        return None
    if kind == "directory":
        return {"kind": "directory", "rows": actual_rows(path, label)}
    require(kind == "file", f"unknown transaction target kind: {kind}")
    return {"kind": "file", **identity(path)}


def make_swap_spec(label: str, target: Path, staged: Path, kind: str) -> dict[str, Any]:
    return {
        "label": label,
        "target": target,
        "staged": staged,
        "kind": kind,
        "before": target_snapshot(target, kind, f"pre-transaction {label}"),
        "after": target_snapshot(staged, kind, f"staged {label}"),
    }


def transactional_swap(
    specs: list[dict[str, Any]],
    stage: Path,
    pre_commit: Any,
    post_commit: Any,
) -> None:
    """Promote staged targets and restore every prior target on any failure."""
    backup_root = stage / "backups"
    backup_root.mkdir()
    require_plain_directory(backup_root, "transaction backup root")
    target_keys: set[str] = set()
    for spec in specs:
        target = lexical_absolute(spec["target"])
        staged = lexical_absolute(spec["staged"])
        key = os.fspath(target).casefold()
        require(key not in target_keys, f"transaction repeats target: {target}")
        target_keys.add(key)
        require_plain_directory(target.parent, f"{spec['label']} target parent")
        require(
            os.stat(target.parent).st_dev == os.stat(stage).st_dev,
            f"{spec['label']} target is not on the transaction staging volume",
        )
        require(
            target_snapshot(target, spec["kind"], f"pre-swap {spec['label']}") == spec["before"],
            f"{spec['label']} changed after validation",
        )
        require(
            target_snapshot(staged, spec["kind"], f"staged {spec['label']}") == spec["after"],
            f"staged {spec['label']} changed after validation",
        )
    pre_commit()

    journal: list[dict[str, Any]] = []
    try:
        for index, spec in enumerate(specs):
            if spec["before"] == spec["after"]:
                continue
            require(
                target_snapshot(
                    spec["target"], spec["kind"], f"immediate pre-swap {spec['label']}"
                )
                == spec["before"],
                f"{spec['label']} changed while the transaction was committing",
            )
            require(
                target_snapshot(
                    spec["staged"], spec["kind"], f"immediate staged {spec['label']}"
                )
                == spec["after"],
                f"staged {spec['label']} changed while the transaction was committing",
            )
            backup = backup_root / f"{index:02d}-{spec['label']}"
            require(not lexists(backup), f"transaction backup already exists: {backup}")
            entry = {**spec, "backup": backup, "backup_moved": False, "new_installed": False}
            journal.append(entry)
            if spec["before"] is not None:
                os.replace(spec["target"], backup)
                entry["backup_moved"] = True
                require(not lexists(spec["target"]), f"{spec['label']} target remained after backup rename")
            os.replace(spec["staged"], spec["target"])
            entry["new_installed"] = True
            require(
                target_snapshot(spec["target"], spec["kind"], f"installed {spec['label']}")
                == spec["after"],
                f"installed {spec['label']} differs from its staged bytes",
            )
        post_commit()
    except BaseException as original:
        rollback_failures: list[str] = []
        for entry in reversed(journal):
            try:
                if entry["new_installed"]:
                    require(
                        target_snapshot(entry["target"], entry["kind"], f"rollback {entry['label']}")
                        == entry["after"],
                        f"installed {entry['label']} changed before rollback",
                    )
                    os.replace(entry["target"], entry["staged"])
                if entry["backup_moved"]:
                    require(
                        target_snapshot(entry["backup"], entry["kind"], f"backup {entry['label']}")
                        == entry["before"],
                        f"backup {entry['label']} changed before rollback",
                    )
                    os.replace(entry["backup"], entry["target"])
                require(
                    target_snapshot(entry["target"], entry["kind"], f"restored {entry['label']}")
                    == entry["before"],
                    f"restored {entry['label']} differs from its validated predecessor",
                )
            except BaseException as rollback_exc:
                rollback_failures.append(f"{entry['label']}: {rollback_exc}")
        if rollback_failures:
            raise RollbackError(
                f"transaction failed ({original}); rollback incomplete; backups retained at {stage}: "
                + "; ".join(rollback_failures)
            ) from original
        raise


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


def derive_maintenance_predecessor(output_path: Path) -> Path:
    suffix = output_path.suffix or ".json"
    stem = output_path.stem if output_path.suffix else output_path.name
    if stem.endswith("_MANIFEST"):
        stem = stem[: -len("_MANIFEST")] + "_MAINTENANCE_PREDECESSOR"
    else:
        stem += "_MAINTENANCE_PREDECESSOR"
    return output_path.with_name(stem + suffix)


def build_final_rows(
    prior_rows: list[dict[str, Any]],
    html_rows: list[dict[str, Any]],
    pdf_identity: dict[str, Any],
    landing: bytes,
    public_manifest: bytes,
) -> list[dict[str, Any]]:
    final_by_fold = folded_row_map(prior_rows)
    final_by_fold[ROOT_INDEX.casefold()] = {
        "path": ROOT_INDEX,
        "bytes": len(landing),
        "sha256": digest(landing),
    }
    for row in html_rows:
        path = f"{READER_PREFIX}/{row['path']}"
        folded = path.casefold()
        require(folded not in final_by_fold, f"complete reader collides with prior docs path: {path}")
        final_by_fold[folded] = {
            "path": path,
            "bytes": row["bytes"],
            "sha256": row["sha256"],
        }
    for path, file_identity in (
        (PRIMARY_DOWNLOAD, pdf_identity),
        (
            PUBLIC_EDITION_MANIFEST,
            {"bytes": len(public_manifest), "sha256": digest(public_manifest)},
        ),
    ):
        folded = path.casefold()
        require(folded not in final_by_fold, f"complete edition collides with prior docs path: {path}")
        final_by_fold[folded] = {"path": path, **file_identity}
    rows = sorted(final_by_fold.values(), key=lambda row: str(row["path"]).casefold())
    rows = validate_rows(rows, "planned complete docs manifest")
    prove_replacement_scope_disjoint(prior_rows, rows)
    return rows


def build_output_value(
    final_rows: list[dict[str, Any]],
    pdf_pages: int,
    html_evidence: dict[str, Any],
    pdf_qa_identity: dict[str, Any],
    prior_evidence: dict[str, Any],
    prior_row_count: int,
    docs_file_manifest_path: Path,
    detailed_payload: bytes,
    docs_qa_path: Path,
    qa_payload: bytes,
    maintenance_predecessor: dict[str, Any] | None,
) -> dict[str, Any]:
    final = row_map(final_rows)
    return {
        "schema_version": 1,
        "status": "pass",
        "scope": "complete O003/C90 Bahasa Indonesia GitHub Pages edition",
        **summary(final_rows),
        "stable_reader_route": f"{READER_PREFIX}/",
        "primary_reader": final[PRIMARY_READER],
        "primary_download": {**final[PRIMARY_DOWNLOAD], "pages": pdf_pages},
        "public_edition_manifest": final[PUBLIC_EDITION_MANIFEST],
        "root_landing_page": final[ROOT_INDEX],
        "input_html": html_evidence,
        "input_pdf_qa": pdf_qa_identity,
        "historical_retention": {
            "status": "pass",
            **prior_evidence,
            "preserved_file_count": prior_row_count - 1,
            "only_replaced_path": ROOT_INDEX,
        },
        "maintenance_predecessor": maintenance_predecessor,
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


def payload_matches(path: Path, payload: bytes, label: str) -> bool:
    reject_reparse_components(path, label)
    if not lexists(path):
        return False
    require_plain_file(path, label)
    return path.read_bytes() == payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--maintenance", action="store_true", help="replace only validated existing complete-edition routes")
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
    parser.add_argument(
        "--maintenance-predecessor",
        type=Path,
        default=None,
        help="receipt target; defaults beside --output and is discovered from the admission in check-only mode",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require_plain_file(SCRIPT_PATH, "maintenance script")
    require_plain_directory(ROOT, "repository root")
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
    explicit_predecessor_path = (
        resolve_input(args.maintenance_predecessor)
        if args.maintenance_predecessor is not None
        else None
    )
    predecessor_base_path = explicit_predecessor_path or derive_maintenance_predecessor(
        output_path
    )
    next_predecessor_path = predecessor_base_path

    html_rows, html_evidence = validate_html_inputs(
        html_manifest_path, html_qa_path, html_root
    )
    pdf_identity, pdf_pages, pdf_qa_identity = validate_pdf_input(pdf_path, pdf_qa_path)
    prior_rows, prior_evidence = validate_prior_docs(
        prior_file_manifest_path, prior_admission_path, docs_root
    )

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
    final_rows = build_final_rows(
        prior_rows, html_rows, pdf_identity, landing, public_manifest
    )
    docs_qa_value = build_docs_qa(
        final_rows,
        prior_rows,
        html_rows,
        html_evidence["qa"],
        landing,
        public_manifest,
    )
    require(docs_qa_value["status"] == "pass", f"complete docs QA failed: {docs_qa_value['failures'][:10]}")
    detailed_payload = manifest_payload(final_rows)
    qa_payload = json_payload(docs_qa_value)

    if args.check_only:
        assert_rows_equal(
            final_rows,
            actual_rows(docs_root, "complete docs tree"),
            "complete docs tree",
        )
        existing_admission = read_json(output_path, "complete docs admission receipt")
        maintenance_evidence = bound_maintenance_predecessor(
            existing_admission,
            expected_path=explicit_predecessor_path,
            docs_root=docs_root,
        )
        if explicit_predecessor_path is not None:
            require(
                maintenance_evidence is not None,
                "requested maintenance predecessor is not bound by the admission",
            )
        output_value = build_output_value(
            final_rows,
            pdf_pages,
            html_evidence,
            pdf_qa_identity,
            prior_evidence,
            len(prior_rows),
            docs_file_manifest_path,
            detailed_payload,
            docs_qa_path,
            qa_payload,
            maintenance_evidence,
        )
        output_payload = json_payload(output_value)
        require(
            payload_matches(
                docs_file_manifest_path, detailed_payload, "complete docs file manifest"
            ),
            "complete docs file manifest differs",
        )
        require(
            payload_matches(docs_qa_path, qa_payload, "complete docs QA receipt"),
            "complete docs QA receipt differs",
        )
        require(
            payload_matches(output_path, output_payload, "complete docs admission receipt"),
            "complete docs admission receipt differs",
        )
        mode = "check-only"
    else:
        maintenance_plan: dict[str, Any] | None = None
        maintenance_evidence: dict[str, Any] | None = None

        if args.maintenance:
            observed_rows = actual_rows(docs_root, "current complete docs tree")
            if observed_rows == final_rows and lexists(output_path):
                existing_admission = read_json(
                    output_path, "current complete docs admission receipt"
                )
                existing_evidence = bound_maintenance_predecessor(
                    existing_admission, docs_root=docs_root
                )
                requested_matches = (
                    explicit_predecessor_path is None
                    or (
                        existing_evidence is not None
                        and existing_evidence["path"]
                        == repo_path(
                            explicit_predecessor_path,
                            "requested maintenance predecessor",
                        )
                    )
                )
                candidate_value = build_output_value(
                    final_rows,
                    pdf_pages,
                    html_evidence,
                    pdf_qa_identity,
                    prior_evidence,
                    len(prior_rows),
                    docs_file_manifest_path,
                    detailed_payload,
                    docs_qa_path,
                    qa_payload,
                    existing_evidence,
                )
                candidate_payload = json_payload(candidate_value)
                if (
                    requested_matches
                    and payload_matches(
                        docs_file_manifest_path,
                        detailed_payload,
                        "current complete docs file manifest",
                    )
                    and payload_matches(
                        docs_qa_path, qa_payload, "current complete docs QA"
                    )
                    and payload_matches(
                        output_path,
                        candidate_payload,
                        "current complete docs admission",
                    )
                ):
                    output_payload = candidate_payload
                    mode = "maintenance-check-only"
                    print(
                        json.dumps(
                            {
                                "status": "pass",
                                "mode": mode,
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
            maintenance_plan = prepare_maintenance_overlay(
                docs_root,
                docs_file_manifest_path,
                docs_qa_path,
                output_path,
                prior_rows,
            )
            predecessor_payload = maintenance_plan["predecessor_payload"]
            if explicit_predecessor_path is None:
                predecessor_digest = digest(predecessor_payload)
                next_predecessor_path = predecessor_base_path.with_name(
                    f"{predecessor_base_path.stem}.{predecessor_digest}"
                    f"{predecessor_base_path.suffix}"
                )
            elif lexists(next_predecessor_path):
                require(
                    payload_matches(
                        next_predecessor_path,
                        predecessor_payload,
                        "explicit maintenance predecessor target",
                    ),
                    "refusing to overwrite a prior receipt at the explicit maintenance predecessor path",
                )
            maintenance_evidence = {
                "path": repo_path(
                    next_predecessor_path, "maintenance predecessor receipt"
                ),
                "bytes": len(predecessor_payload),
                "sha256": digest(predecessor_payload),
            }
            mode = "maintenance-write"
        else:
            preflight_overlay(docs_root, prior_rows, final_rows)
            predecessor_payload = None
            mode = "write"

        output_value = build_output_value(
            final_rows,
            pdf_pages,
            html_evidence,
            pdf_qa_identity,
            prior_evidence,
            len(prior_rows),
            docs_file_manifest_path,
            detailed_payload,
            docs_qa_path,
            qa_payload,
            maintenance_evidence,
        )
        output_payload = json_payload(output_value)
        receipt_targets = [docs_file_manifest_path, docs_qa_path, output_path]
        if predecessor_payload is not None:
            receipt_targets.append(next_predecessor_path)
        validate_transaction_layout(
            docs_root,
            receipt_targets,
            [
                html_root,
                html_manifest_path,
                html_qa_path,
                pdf_path,
                pdf_qa_path,
                prior_file_manifest_path,
                prior_admission_path,
            ],
        )
        validate_owned_receipt_target(
            docs_file_manifest_path, "docs file manifest"
        )
        validate_owned_receipt_target(docs_qa_path, "docs QA")
        validate_owned_receipt_target(output_path, "admission")
        if predecessor_payload is not None:
            validate_owned_receipt_target(
                next_predecessor_path, "maintenance predecessor"
            )

        stage: Path | None = None
        stage_marker = b""
        stage_disposable = True
        try:
            stage, stage_marker = create_owned_stage(docs_root)
            staged = stage_bundle(
                stage,
                html_root,
                html_rows,
                pdf_path,
                pdf_identity,
                landing,
                public_manifest,
                detailed_payload,
                qa_payload,
                output_payload,
                predecessor_payload,
            )

            def verify_precommit_inputs() -> None:
                assert_rows_equal(
                    html_rows,
                    actual_rows(html_root, "pre-commit complete HTML input"),
                    "complete HTML input changed during staging",
                )
                require(
                    identity(html_manifest_path)
                    == {
                        "bytes": html_evidence["manifest"]["bytes"],
                        "sha256": html_evidence["manifest"]["sha256"],
                    },
                    "complete HTML manifest changed during staging",
                )
                require(
                    identity(html_qa_path)
                    == {
                        "bytes": html_evidence["qa"]["bytes"],
                        "sha256": html_evidence["qa"]["sha256"],
                    },
                    "complete HTML QA changed during staging",
                )
                require(identity(pdf_path) == pdf_identity, "complete PDF changed during staging")
                require(
                    identity(pdf_qa_path)
                    == {
                        "bytes": pdf_qa_identity["bytes"],
                        "sha256": pdf_qa_identity["sha256"],
                    },
                    "complete PDF QA changed during staging",
                )
                require(
                    identity(prior_file_manifest_path)
                    == {
                        "bytes": prior_evidence["file_manifest"]["bytes"],
                        "sha256": prior_evidence["file_manifest"]["sha256"],
                    },
                    "prior docs file manifest changed during staging",
                )
                require(
                    identity(prior_admission_path)
                    == {
                        "bytes": prior_evidence["admission"]["bytes"],
                        "sha256": prior_evidence["admission"]["sha256"],
                    },
                    "prior docs admission changed during staging",
                )
                if maintenance_plan is not None:
                    assert_rows_equal(
                        maintenance_plan["current_rows"],
                        actual_rows(docs_root, "maintenance predecessor docs tree"),
                        "maintenance predecessor docs tree changed during staging",
                    )
                    require(
                        identity(docs_file_manifest_path)
                        == maintenance_plan["current_file_manifest"],
                        "maintenance predecessor file manifest changed during staging",
                    )
                    require(
                        identity(docs_qa_path) == maintenance_plan["current_qa"],
                        "maintenance predecessor docs QA changed during staging",
                    )
                    require(
                        identity(output_path) == maintenance_plan["current_admission"],
                        "maintenance predecessor admission changed during staging",
                    )
                else:
                    preflight_overlay(docs_root, prior_rows, final_rows)

            specs = [
                make_swap_spec(
                    "complete-reader",
                    docs_root / PurePosixPath(READER_PREFIX),
                    staged["complete_reader"],
                    "directory",
                ),
                make_swap_spec(
                    "complete-pdf",
                    docs_root / PurePosixPath(PRIMARY_DOWNLOAD),
                    staged["complete_pdf"],
                    "file",
                ),
                make_swap_spec(
                    "public-manifest",
                    docs_root / PurePosixPath(PUBLIC_EDITION_MANIFEST),
                    staged["public_manifest"],
                    "file",
                ),
                make_swap_spec(
                    "root-landing",
                    docs_root / ROOT_INDEX,
                    staged["root_landing"],
                    "file",
                ),
                make_swap_spec(
                    "docs-file-manifest",
                    docs_file_manifest_path,
                    staged["docs_file_manifest"],
                    "file",
                ),
                make_swap_spec(
                    "docs-qa", docs_qa_path, staged["docs_qa"], "file"
                ),
            ]
            if predecessor_payload is not None:
                specs.append(
                    make_swap_spec(
                        "maintenance-predecessor",
                        next_predecessor_path,
                        staged["maintenance_predecessor"],
                        "file",
                    )
                )
            specs.append(
                make_swap_spec("admission", output_path, staged["admission"], "file")
            )

            def verify_committed_bundle() -> None:
                assert_rows_equal(
                    final_rows,
                    actual_rows(docs_root, "committed complete docs tree"),
                    "committed complete docs tree",
                )
                require(
                    payload_matches(
                        docs_file_manifest_path,
                        detailed_payload,
                        "committed docs file manifest",
                    ),
                    "committed docs file manifest differs",
                )
                require(
                    payload_matches(docs_qa_path, qa_payload, "committed docs QA"),
                    "committed docs QA differs",
                )
                if predecessor_payload is not None:
                    require(
                        payload_matches(
                            next_predecessor_path,
                            predecessor_payload,
                            "committed maintenance predecessor",
                        ),
                        "committed maintenance predecessor differs",
                    )
                require(
                    payload_matches(output_path, output_payload, "committed admission"),
                    "committed admission differs",
                )
                committed_admission = read_json(
                    output_path, "committed complete docs admission"
                )
                committed_evidence = bound_maintenance_predecessor(
                    committed_admission,
                    expected_path=(
                        next_predecessor_path
                        if predecessor_payload is not None
                        else None
                    ),
                    docs_root=docs_root,
                )
                require(
                    committed_evidence == maintenance_evidence,
                    "committed admission has the wrong maintenance predecessor binding",
                )

            transactional_swap(
                specs, stage, verify_precommit_inputs, verify_committed_bundle
            )
        except RollbackError:
            stage_disposable = False
            raise
        finally:
            if stage is not None and stage_disposable and lexists(stage):
                remove_owned_stage(stage, stage_marker)

    print(
        json.dumps(
            {
                "status": "pass",
                "mode": mode,
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
