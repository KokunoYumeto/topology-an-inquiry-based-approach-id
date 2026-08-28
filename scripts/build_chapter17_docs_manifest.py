#!/usr/bin/env python3
"""Assemble and admit the cumulative Chapters 1-17 GitHub Pages tree.

The operation is a non-destructive overlay.  It verifies the admitted Chapter
16 Pages tree, retains its frozen historical reader entry points and PDFs,
overlays the exact finalized Chapters 1-17 HTML tree, and adds the deterministic
Chapters 1-17 PDF.  It then writes a detailed byte manifest, a deterministic
link/asset QA receipt, and the compact admission receipt.  ``--check-only``
performs the same final validation without changing any file.
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
ALGORITHM = (
    "SHA-256 over UTF-8 lines: relative path, TAB, byte count, TAB, "
    "file SHA-256, LF; paths ordered case-insensitively"
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

HTML_ROOT = ROOT / "output/chapters01-17-html"
HTML_MANIFEST = ROOT / "qa/CHAPTER17_HTML_MANIFEST.json"
PDF = ROOT / "output/chapters01-17-pdf/chapters_01_17_reader.pdf"
PDF_RUN_1 = ROOT / "qa/CHAPTER17_PDF_RUN1_HASH.json"
PDF_RUN_2 = ROOT / "qa/CHAPTER17_PDF_RUN2_HASH.json"
PDF_RUN_1_CANDIDATE = ROOT / "tmp/pdfs/chapter17-run1.pdf"
SOURCE_MANIFEST = ROOT / "qa/CHAPTER17_SOURCE_MANIFEST.json"
DOCS_ROOT = ROOT / "docs"
DOCS_FILE_MANIFEST = ROOT / "qa/CHAPTER17_DOCS_FILE_MANIFEST.json"
DOCS_QA = ROOT / "qa/CHAPTER17_DOCS_QA.json"
PRIOR_DOCS_FILE_MANIFEST = ROOT / "qa/CHAPTER16_DOCS_FILE_MANIFEST.json"
PRIOR_DOCS_MANIFEST = ROOT / "qa/CHAPTER16_DOCS_MANIFEST.json"
OUTPUT = ROOT / "qa/CHAPTER17_DOCS_MANIFEST.json"

HTML_LABEL = "O003/C90 Chapters 1-17 HTML"
DOCS_LABEL = "O003/C90 Chapters 1-17 GitHub Pages tree"
PRIOR_DOCS_LABEL = "O003/C90 Chapters 1-16 GitHub Pages tree"
SOURCE_BOUNDARY = "chapters_01_17_with_separately_licensed_self_study_companions"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
PRIMARY_ENTRY = "o003-c90-chapters-01-17-reader.html"
PRIMARY_DOWNLOAD = (
    "downloads/topologi-pendekatan-berbasis-inkuiri-bab-01-17-id.pdf"
)
PRIOR_PRIMARY_ENTRY = "o003-c90-chapters-01-16-reader.html"
PRIOR_PRIMARY_DOWNLOAD = (
    "downloads/topologi-pendekatan-berbasis-inkuiri-bab-01-16-id.pdf"
)
PDF_REPO_PATH = "output/chapters01-17-pdf/chapters_01_17_reader.pdf"
PDF_RUN_1_REPO_PATH = "tmp/pdfs/chapter17-run1.pdf"

REQUIRED_DOCS_SURFACES = (
    "index.html",
    PRIMARY_ENTRY,
    "chap_Compact_topology.html",
    "sec_compact_top_exer.html",
    "o003-c90-ch17-companion.html",
    "o003-c90-ch17-mastery.html",
    "external/o003-readable-layout.css",
    PRIMARY_DOWNLOAD,
    PRIOR_PRIMARY_ENTRY,
    PRIOR_PRIMARY_DOWNLOAD,
)

EXPECTED_HISTORICAL_PATHS = frozenset(
    {
        ".nojekyll",
        *(
            "downloads/topologi-pendekatan-berbasis-inkuiri-"
            f"bab-01-{chapter:02d}-id.pdf"
            for chapter in range(2, 17)
        ),
        *(f"o003-c90-ch{chapter:02d}-edition-note.html" for chapter in range(8, 17)),
        *(
            f"o003-c90-chapters-01-{chapter:02d}-reader.html"
            for chapter in range(8, 17)
        ),
        # These Chapter 16 knowls were admitted with the previous reader but
        # are no longer emitted by the cumulative Chapter 17 build.  Retain
        # their exact prior bytes with the historical entry surfaces.
        "knowl/mrow-77.html",
        "knowl/p-6330.html",
        "knowl/p-6336.html",
        "knowl/p-6342.html",
        "knowl/p-6348.html",
        "knowl/p-6355.html",
        "knowl/p-6362.html",
        "knowl/p-6368.html",
        "knowl/p-6375.html",
    }
)
EXPECTED_EXTRA_FILES = len(EXPECTED_HISTORICAL_PATHS) + 1

EXPECTED_RIGHTS = {
    "translated_gvsu_spine": "CC-BY-NC-SA-3.0 (conservative determination)",
    "original_self_study_companions": "CC-BY-4.0",
    "software_figures_fonts_and_assets": "per-component notices retained",
    "collection_policy": "per-component rights; no flattened license",
    "non_endorsement": True,
}


class ContractError(RuntimeError):
    """One fail-closed admission contract was not satisfied."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def identity(path: Path) -> dict[str, object]:
    require(path.is_file(), f"required file is missing: {path}")
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": digest(data)}


def resolve_input(path: Path) -> Path:
    return path.resolve() if path.is_absolute() else (ROOT / path).resolve()


def repo_path(path: Path, label: str) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError as exc:
        raise ContractError(f"{label} must remain inside the repository: {path}") from exc


def read_json(path: Path, label: str) -> dict[str, Any]:
    require(path.is_file(), f"{label} is missing: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"{label} is not valid UTF-8 JSON: {exc}") from exc
    require(isinstance(value, dict), f"{label} must be a JSON object")
    return value


def clean_relative_path(value: object, label: str) -> str:
    require(isinstance(value, str) and value, f"{label} path must be non-empty text")
    require("\\" not in value, f"{label} path must use POSIX separators: {value!r}")
    pure = PurePosixPath(value)
    require(not pure.is_absolute(), f"{label} path must be relative: {value!r}")
    require(".." not in pure.parts, f"{label} path escapes its tree: {value!r}")
    require(pure.as_posix() == value, f"{label} path is not normalized: {value!r}")
    return value


def positive_int(value: object, label: str, *, allow_zero: bool = False) -> int:
    lower = 0 if allow_zero else 1
    require(
        isinstance(value, int) and not isinstance(value, bool) and value >= lower,
        f"{label} must be an integer >= {lower}",
    )
    return int(value)


def sha256_value(value: object, label: str) -> str:
    require(
        isinstance(value, str) and SHA256_RE.fullmatch(value) is not None,
        f"{label} must be a lowercase SHA-256 digest",
    )
    return value


def canonical(rows: list[dict[str, object]]) -> str:
    return digest(
        "".join(
            f"{row['path']}\t{row['bytes']}\t{row['sha256']}\n" for row in rows
        ).encode("utf-8")
    )


def summary(rows: list[dict[str, object]]) -> dict[str, int | str]:
    return {
        "canonical_manifest_sha256": canonical(rows),
        "file_count": len(rows),
        "html_files": sum(
            1 for row in rows if str(row["path"]).lower().endswith((".html", ".htm"))
        ),
        "total_bytes": sum(int(row["bytes"]) for row in rows),
    }


def manifest_rows(
    manifest: dict[str, Any], *, label: str, expected_label: str | None
) -> tuple[list[dict[str, object]], dict[str, int | str]]:
    require(manifest.get("schema_version") == 1, f"{label} schema version differs")
    if expected_label is None:
        require(
            set(manifest)
            == {
                "schema_version",
                "canonical_manifest_sha256",
                "file_count",
                "html_files",
                "total_bytes",
                "localized_nodes_and_attributes",
                "files",
            },
            f"{label} compact field set differs",
        )
        positive_int(
            manifest.get("localized_nodes_and_attributes"),
            f"{label} localized-node count",
            allow_zero=True,
        )
    else:
        require(manifest.get("label") == expected_label, f"{label} label differs")
        require(manifest.get("source_directory") == ".", f"{label} source directory differs")
        require(manifest.get("glob") == "**/*", f"{label} glob differs")
        require(manifest.get("combined_algorithm") == ALGORITHM, f"{label} algorithm differs")
    raw_rows = manifest.get("files")
    require(isinstance(raw_rows, list) and raw_rows, f"{label} has no file rows")
    rows: list[dict[str, object]] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_rows):
        require(isinstance(raw, dict), f"{label} row {index} is not an object")
        require(set(raw) == {"path", "bytes", "sha256"}, f"{label} row {index} has unexpected fields")
        path = clean_relative_path(raw.get("path"), f"{label} row {index}")
        size = positive_int(raw.get("bytes"), f"{label} row {index} bytes", allow_zero=True)
        checksum = sha256_value(raw.get("sha256"), f"{label} row {index} sha256")
        folded = path.casefold()
        require(folded not in seen, f"{label} repeats or case-collides at path: {path}")
        seen.add(folded)
        rows.append({"path": path, "bytes": size, "sha256": checksum})
    require(rows == sorted(rows, key=lambda row: str(row["path"]).casefold()), f"{label} rows are not canonically ordered")
    computed = summary(rows)
    for key, expected in computed.items():
        require(manifest.get(key) == expected, f"{label} {key} differs from its rows")
    return rows, computed


def actual_rows(root: Path, label: str) -> list[dict[str, object]]:
    require(root.is_dir(), f"{label} directory is missing: {root}")
    files = sorted(
        (path for path in root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(root).as_posix().casefold(),
    )
    require(files, f"{label} directory contains no files")
    rows: list[dict[str, object]] = []
    seen: set[str] = set()
    for path in files:
        relative = path.relative_to(root).as_posix()
        folded = relative.casefold()
        require(folded not in seen, f"{label} has a case-insensitive collision: {relative}")
        seen.add(folded)
        rows.append({"path": relative, **identity(path)})
    return rows


def row_map(rows: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    return {str(row["path"]): row for row in rows}


def assert_rows_equal(expected: list[dict[str, object]], observed: list[dict[str, object]], label: str) -> None:
    if expected == observed:
        return
    expected_map = row_map(expected)
    observed_map = row_map(observed)
    missing = sorted(set(expected_map) - set(observed_map), key=str.casefold)
    unexpected = sorted(set(observed_map) - set(expected_map), key=str.casefold)
    changed = sorted(
        (path for path in set(expected_map) & set(observed_map) if expected_map[path] != observed_map[path]),
        key=str.casefold,
    )
    raise ContractError(
        f"{label} differs: missing={missing[:5]!r}, unexpected={unexpected[:5]!r}, changed={changed[:5]!r}"
    )


def validate_pdf_receipts(run_one_path: Path, run_two_path: Path, run_one_pdf: Path, pdf: Path) -> tuple[dict[str, object], int]:
    run_two = read_json(run_two_path, "Chapter 17 PDF run-two receipt")
    require(run_two.get("schema_version") == 1, "PDF run-two schema version differs")
    require(run_two.get("status") == "pass" and run_two.get("run") == 2, "PDF run two did not pass")
    require(run_two.get("path") == PDF_REPO_PATH, "PDF run-two path differs")
    require(run_two.get("clean_build") is True, "PDF run two was not clean")
    require(run_two.get("strict_transcript_gate") is True, "PDF run two failed its transcript gate")
    require(run_two.get("byte_identical_to_run_1") is True, "PDF runs are not recorded as identical")
    final_identity = identity(pdf)
    require(run_two.get("bytes") == final_identity["bytes"] and run_two.get("sha256") == final_identity["sha256"], "PDF run-two identity differs")
    pages = positive_int(run_two.get("pages"), "PDF run-two page count")
    epoch = positive_int(run_two.get("source_date_epoch"), "PDF run-two source epoch", allow_zero=True)
    nested = run_two.get("run_1")
    require(isinstance(nested, dict) and nested.get("path") == PDF_RUN_1_REPO_PATH, "PDF run-two nested run-one path differs")

    run_one = read_json(run_one_path, "Chapter 17 PDF run-one receipt")
    require(run_one.get("schema_version") == 1, "PDF run-one schema version differs")
    require(run_one.get("status") == "pass" and run_one.get("run") == 1, "PDF run one did not pass")
    require(run_one.get("path") == PDF_RUN_1_REPO_PATH, "PDF run-one path differs")
    require(run_one.get("clean_build") is True and run_one.get("strict_transcript_gate") is True, "PDF run one failed a build gate")
    run_one_identity = identity(run_one_pdf)
    require(run_one.get("bytes") == run_one_identity["bytes"] and run_one.get("sha256") == run_one_identity["sha256"], "PDF run-one identity differs")
    require(positive_int(run_one.get("pages"), "PDF run-one page count") == pages, "PDF page counts differ")
    require(positive_int(run_one.get("source_date_epoch"), "PDF run-one source epoch", allow_zero=True) == epoch, "PDF source epochs differ")
    require(nested.get("bytes") == run_one_identity["bytes"] and nested.get("sha256") == run_one_identity["sha256"], "nested run-one identity differs")
    require(run_one_identity == final_identity, "the independently verified PDF runs differ")
    return final_identity, pages


def validate_source_manifest(path: Path) -> tuple[dict[str, Any], dict[str, object]]:
    source = read_json(path, "Chapter 17 source manifest")
    require(source.get("schema_version") == 1 and source.get("status") == "pass", "source manifest did not pass")
    require(source.get("boundary") == SOURCE_BOUNDARY, "source manifest boundary differs")
    require(source.get("admission_status") == "partial_checkpoint_admitted", "source checkpoint is not admitted")
    require(source.get("partial") is True and source.get("boundary_complete") is True, "source checkpoint scope differs")
    require(source.get("pending_evidence") == [], "source manifest has pending evidence")
    rights = source.get("rights")
    require(isinstance(rights, dict), "source manifest rights are missing")
    for key, expected in EXPECTED_RIGHTS.items():
        require(rights.get(key) == expected, f"source manifest right differs: {key}")
    for key in ("collection_licenses", "companion_rights"):
        row = rights.get(key)
        require(isinstance(row, dict), f"source manifest {key} identity is missing")
        clean_relative_path(row.get("path"), f"source manifest {key}")
        positive_int(row.get("bytes"), f"source manifest {key} bytes")
        sha256_value(row.get("sha256"), f"source manifest {key} sha256")
    provenance = source.get("production_provenance")
    require(isinstance(provenance, dict) and provenance.get("tool") == MODEL, "source manifest model provenance differs")
    return source, {"path": repo_path(path, "source manifest"), **identity(path)}


def validate_prior_admission(path: Path, detailed_path: Path, prior_rows: list[dict[str, object]], prior_summary: dict[str, int | str]) -> dict[str, Any]:
    admission = read_json(path, "Chapter 16 docs admission receipt")
    require(admission.get("schema_version") == 1 and admission.get("status") == "pass", "prior docs receipt did not pass")
    require(admission.get("failures") == [], "prior docs receipt records failures")
    for key, expected in prior_summary.items():
        require(admission.get(key) == expected, f"prior docs receipt {key} differs")
    detail = admission.get("detailed_manifest")
    require(isinstance(detail, dict), "prior docs receipt lacks its detailed-manifest identity")
    require(detail.get("path") == repo_path(detailed_path, "prior detailed manifest"), "prior detailed-manifest path differs")
    observed = identity(detailed_path)
    require(detail.get("bytes") == observed["bytes"] and detail.get("sha256") == observed["sha256"], "prior detailed-manifest identity differs")
    prior_map = row_map(prior_rows)
    for field, expected_path in (("primary_reader", PRIOR_PRIMARY_ENTRY), ("primary_download", PRIOR_PRIMARY_DOWNLOAD)):
        value = admission.get(field)
        require(isinstance(value, dict) and value.get("path") == expected_path, f"prior {field} path differs")
        require(expected_path in prior_map, f"prior detailed manifest omits {expected_path}")
        require(value.get("bytes") == prior_map[expected_path]["bytes"] and value.get("sha256") == prior_map[expected_path]["sha256"], f"prior {field} identity differs")
    return admission


def manifest_payload(rows: list[dict[str, object]]) -> bytes:
    value = {
        "schema_version": 1,
        "label": DOCS_LABEL,
        "source_directory": ".",
        "glob": "**/*",
        "combined_algorithm": ALGORITHM,
        **summary(rows),
        "files": rows,
    }
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


class LinkCollector(HTMLParser):
    URL_ATTRIBUTES = frozenset({"href", "src", "poster", "data-knowl", "data-knowl-url"})

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.urls: list[tuple[str, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name.lower() in self.URL_ATTRIBUTES and value:
                self.urls.append((tag.lower(), name.lower(), value.strip()))


def local_target(root: Path, source: Path, url: str) -> Path | None:
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc:
        return None
    raw_path = unquote(parsed.path)
    if not raw_path:
        return source
    if raw_path.startswith("/"):
        target = root / raw_path.lstrip("/")
    else:
        target = source.parent / raw_path
    target = target.resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError as exc:
        raise ContractError(f"local URL escapes docs tree in {source}: {url!r}") from exc
    if raw_path.endswith("/") or target.is_dir():
        target = target / "index.html"
    # PreTeXt knowl fragments are fetched into a parent page and therefore
    # emit some references relative to the reader root rather than to the
    # physical ``knowl/`` file.  Accept that second, still tree-bounded,
    # interpretation only when the ordinary file-relative target is absent.
    if not target.is_file() and not raw_path.startswith("/"):
        root_target = (root / raw_path).resolve()
        try:
            root_target.relative_to(root.resolve())
        except ValueError as exc:
            raise ContractError(
                f"root-relative knowl URL escapes docs tree in {source}: {url!r}"
            ) from exc
        if raw_path.endswith("/") or root_target.is_dir():
            root_target = root_target / "index.html"
        if root_target.is_file():
            return root_target
    return target


def build_docs_qa(root: Path, rows: list[dict[str, object]]) -> dict[str, Any]:
    paths = {str(row["path"]) for row in rows}
    missing_surfaces = [path for path in REQUIRED_DOCS_SURFACES if path not in paths]
    require(not missing_surfaces, f"docs tree omits required surfaces: {missing_surfaces!r}")
    failures: list[str] = []
    external_hosts: Counter[str] = Counter()
    checked = 0
    images_checked = 0
    for row in rows:
        relative = str(row["path"])
        if not relative.lower().endswith((".html", ".htm")):
            continue
        source = root / PurePosixPath(relative)
        try:
            parser = LinkCollector()
            parser.feed(source.read_text(encoding="utf-8"))
            parser.close()
        except (UnicodeDecodeError, OSError) as exc:
            failures.append(f"{relative}: unreadable HTML: {exc}")
            continue
        for tag, attribute, url in parser.urls:
            if not url:
                continue
            checked += 1
            parsed = urlsplit(url)
            host = parsed.hostname
            if host:
                external_hosts[host.lower()] += 1
                continue
            if parsed.scheme in {"mailto", "tel", "javascript", "data"}:
                continue
            if parsed.scheme:
                failures.append(f"{relative}: unsupported URL scheme in {attribute}: {url}")
                continue
            try:
                target = local_target(root, source, url)
            except ContractError as exc:
                failures.append(str(exc))
                continue
            if target is None:
                continue
            if not target.is_file():
                failures.append(f"{relative}: missing local target for {attribute}: {url}")
            elif tag == "img" and attribute == "src":
                images_checked += 1
    require(not failures, f"docs link/asset QA failed: {failures[:10]!r}")
    return {
        "schema_version": 1,
        "status": "pass",
        **summary(rows),
        "links_and_assets_checked": checked,
        "images_checked": images_checked,
        "external_hosts": dict(sorted(external_hosts.items())),
        "required_surfaces": list(REQUIRED_DOCS_SURFACES),
        "failures": [],
    }


def json_payload(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(payload)
    temporary.replace(path)


def assert_payload(path: Path, payload: bytes, label: str) -> None:
    require(path.is_file(), f"{label} is missing: {path}")
    require(path.read_bytes() == payload, f"{label} differs from deterministic reconstruction")


def preflight_overlay(docs_root: Path, prior_rows: list[dict[str, object]], final_rows: list[dict[str, object]]) -> None:
    observed = row_map(actual_rows(docs_root, "existing docs tree"))
    prior = row_map(prior_rows)
    final = row_map(final_rows)
    require(set(prior) <= set(observed), "existing docs tree omits bytes admitted at Chapter 16")
    require(set(observed) <= set(final), "existing docs tree contains paths outside the Chapter 17 overlay contract")
    for path, row in observed.items():
        if row == final[path]:
            continue
        require(path in prior and row == prior[path] and path not in EXPECTED_HISTORICAL_PATHS, f"existing docs byte is neither admitted prior nor final: {path}")
    for path in EXPECTED_HISTORICAL_PATHS:
        require(observed.get(path) == prior[path] == final[path], f"historical byte differs before overlay: {path}")


def apply_overlay(html_root: Path, html_rows: list[dict[str, object]], pdf: Path, docs_root: Path) -> None:
    for row in html_rows:
        relative = PurePosixPath(str(row["path"]))
        source = html_root / relative
        target = docs_root / relative
        if target.is_file() and identity(target) == {"bytes": row["bytes"], "sha256": row["sha256"]}:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    target_pdf = docs_root / PurePosixPath(PRIMARY_DOWNLOAD)
    target_pdf.parent.mkdir(parents=True, exist_ok=True)
    if not target_pdf.is_file() or identity(target_pdf) != identity(pdf):
        shutil.copyfile(pdf, target_pdf)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--html-root", type=Path, default=HTML_ROOT)
    parser.add_argument("--html-manifest", type=Path, default=HTML_MANIFEST)
    parser.add_argument("--pdf", type=Path, default=PDF)
    parser.add_argument("--pdf-run-1", type=Path, default=PDF_RUN_1)
    parser.add_argument("--pdf-run-2", type=Path, default=PDF_RUN_2)
    parser.add_argument("--pdf-run-1-candidate", type=Path, default=PDF_RUN_1_CANDIDATE)
    parser.add_argument("--source-manifest", type=Path, default=SOURCE_MANIFEST)
    parser.add_argument("--docs-root", type=Path, default=DOCS_ROOT)
    parser.add_argument("--docs-file-manifest", type=Path, default=DOCS_FILE_MANIFEST)
    parser.add_argument("--docs-qa", type=Path, default=DOCS_QA)
    parser.add_argument("--prior-docs-file-manifest", type=Path, default=PRIOR_DOCS_FILE_MANIFEST)
    parser.add_argument("--prior-docs-manifest", type=Path, default=PRIOR_DOCS_MANIFEST)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    html_root = resolve_input(args.html_root)
    html_manifest_path = resolve_input(args.html_manifest)
    pdf_path = resolve_input(args.pdf)
    run_one_path = resolve_input(args.pdf_run_1)
    run_two_path = resolve_input(args.pdf_run_2)
    run_one_pdf = resolve_input(args.pdf_run_1_candidate)
    source_manifest_path = resolve_input(args.source_manifest)
    docs_root = resolve_input(args.docs_root)
    docs_manifest_path = resolve_input(args.docs_file_manifest)
    docs_qa_path = resolve_input(args.docs_qa)
    prior_detailed_path = resolve_input(args.prior_docs_file_manifest)
    prior_admission_path = resolve_input(args.prior_docs_manifest)
    output_path = resolve_input(args.output)

    html_manifest = read_json(html_manifest_path, "Chapter 17 HTML manifest")
    html_rows, html_summary = manifest_rows(html_manifest, label="Chapter 17 HTML manifest", expected_label=None)
    assert_rows_equal(html_rows, actual_rows(html_root, "Chapter 17 HTML tree"), "Chapter 17 HTML tree")
    html_map = row_map(html_rows)
    require(PRIMARY_ENTRY in html_map, "Chapters 1-17 reader entry is absent from HTML")
    require(PRIMARY_DOWNLOAD not in html_map, "HTML tree unexpectedly contains the PDF")

    pdf_identity, pdf_pages = validate_pdf_receipts(run_one_path, run_two_path, run_one_pdf, pdf_path)
    source_manifest, source_manifest_identity = validate_source_manifest(source_manifest_path)

    prior_manifest = read_json(prior_detailed_path, "Chapter 16 detailed docs manifest")
    prior_rows, prior_summary = manifest_rows(prior_manifest, label="Chapter 16 detailed docs manifest", expected_label=PRIOR_DOCS_LABEL)
    prior_admission = validate_prior_admission(prior_admission_path, prior_detailed_path, prior_rows, prior_summary)
    prior_map = row_map(prior_rows)

    historical_paths = set(prior_map) - set(html_map)
    require(historical_paths == set(EXPECTED_HISTORICAL_PATHS), "the exact Chapter 16 historical-retention set differs")
    historical_rows = [prior_map[path] for path in sorted(historical_paths, key=str.casefold)]

    final_map = dict(html_map)
    final_map.update({path: prior_map[path] for path in historical_paths})
    final_map[PRIMARY_DOWNLOAD] = {"path": PRIMARY_DOWNLOAD, **pdf_identity}
    final_rows = [final_map[path] for path in sorted(final_map, key=str.casefold)]
    final_summary = summary(final_rows)
    require(len(final_rows) == int(html_summary["file_count"]) + EXPECTED_EXTRA_FILES, "docs count formula differs")

    if args.check_only:
        assert_rows_equal(final_rows, actual_rows(docs_root, "Chapter 17 docs tree"), "Chapter 17 docs tree")
    else:
        preflight_overlay(docs_root, prior_rows, final_rows)
        apply_overlay(html_root, html_rows, pdf_path, docs_root)
        assert_rows_equal(final_rows, actual_rows(docs_root, "Chapter 17 docs tree"), "Chapter 17 docs tree after overlay")

    detailed_payload = manifest_payload(final_rows)
    qa_value = build_docs_qa(docs_root, final_rows)
    qa_payload = json_payload(qa_value)
    detailed_identity = {"bytes": len(detailed_payload), "sha256": digest(detailed_payload)}
    qa_identity = {"bytes": len(qa_payload), "sha256": digest(qa_payload)}

    output = {
        "schema_version": 1,
        "status": "pass",
        "scope": (
            "GitHub Pages tree for the admitted partial Chapters 1-17 boundary "
            "(17 of 20), retaining deliberate historical entry surfaces and earlier PDFs"
        ),
        **final_summary,
        "source_manifest": {**source_manifest_identity, "boundary": SOURCE_BOUNDARY},
        "generated_html_tree": {"status": "pass", "checked_files": html_summary["file_count"], **html_summary},
        "detailed_manifest": {"path": repo_path(docs_manifest_path, "docs detailed manifest"), **detailed_identity},
        "docs_qa": {"path": repo_path(docs_qa_path, "docs QA"), **qa_identity},
        "historical_retention": {
            "status": "pass",
            "authority_admission": {"path": repo_path(prior_admission_path, "prior admission"), **identity(prior_admission_path)},
            "authority_manifest": {"path": repo_path(prior_detailed_path, "prior detailed manifest"), **identity(prior_detailed_path)},
            "file_count": len(historical_rows),
            "html_files": sum(1 for row in historical_rows if str(row["path"]).lower().endswith((".html", ".htm"))),
            "total_bytes": sum(int(row["bytes"]) for row in historical_rows),
            "canonical_manifest_sha256": canonical(historical_rows),
            "prior_primary_reader": prior_admission["primary_reader"],
            "prior_primary_download": prior_admission["primary_download"],
        },
        "count_contract": {
            "formula": f"docs file count = final HTML file count + {EXPECTED_EXTRA_FILES}",
            "expected_extra_files": EXPECTED_EXTRA_FILES,
            "actual_extra_files": len(set(final_map) - set(html_map)),
            "status": "pass",
        },
        "primary_reader": {"path": PRIMARY_ENTRY, "bytes": html_map[PRIMARY_ENTRY]["bytes"], "sha256": html_map[PRIMARY_ENTRY]["sha256"]},
        "primary_download": {"path": PRIMARY_DOWNLOAD, "pages": pdf_pages, **pdf_identity},
        "rights": source_manifest["rights"],
        "production_provenance": source_manifest["production_provenance"],
        "failures": [],
    }
    output_payload = json_payload(output)

    if args.check_only:
        assert_payload(docs_manifest_path, detailed_payload, "Chapter 17 detailed docs manifest")
        assert_payload(docs_qa_path, qa_payload, "Chapter 17 docs QA receipt")
        assert_payload(output_path, output_payload, "Chapter 17 docs admission receipt")
    else:
        atomic_write(docs_manifest_path, detailed_payload)
        atomic_write(docs_qa_path, qa_payload)
        atomic_write(output_path, output_payload)

    print(json.dumps({
        "status": "pass",
        "mode": "check-only" if args.check_only else "write",
        "output": repo_path(output_path, "output"),
        "bytes": len(output_payload),
        "sha256": digest(output_payload),
        "file_count": final_summary["file_count"],
        "canonical_manifest_sha256": final_summary["canonical_manifest_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContractError as exc:
        raise SystemExit(f"FAIL: {exc}") from exc
