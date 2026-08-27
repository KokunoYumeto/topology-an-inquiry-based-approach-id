#!/usr/bin/env python3
"""Validate and summarize the cumulative Chapters 1-15 Pages tree.

The Pages overlay is intentionally non-destructive: it contains the exact
final Chapters 1-15 HTML tree, the current PDF reader, and a small frozen set
of historical reader entry points and PDFs.  This script does not assemble or
modify ``docs/``.  It fails closed unless the detailed manifests, the actual
trees, the deterministic PDF receipt, the Pages QA report, and every retained
historical byte agree, then writes the compact admission receipt consumed by
the cumulative source manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ALGORITHM = (
    "SHA-256 over UTF-8 lines: relative path, TAB, byte count, TAB, "
    "file SHA-256, LF; paths ordered case-insensitively"
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

HTML_ROOT = ROOT / "output/chapters01-15-html"
HTML_MANIFEST = ROOT / "qa/CHAPTER15_HTML_MANIFEST.json"
PDF = ROOT / "output/chapters01-15-pdf/chapters_01_15_reader.pdf"
PDF_RUN_1 = ROOT / "qa/CHAPTER15_PDF_RUN1_HASH.json"
PDF_RUN_2 = ROOT / "qa/CHAPTER15_PDF_RUN2_HASH.json"
PDF_RUN_1_CANDIDATE = ROOT / "tmp/pdfs/chapter15-run1.pdf"
DOCS_ROOT = ROOT / "docs"
DOCS_FILE_MANIFEST = ROOT / "qa/CHAPTER15_DOCS_FILE_MANIFEST.json"
DOCS_QA = ROOT / "qa/CHAPTER15_DOCS_QA.json"
PRIOR_DOCS_FILE_MANIFEST = ROOT / "qa/CHAPTER14_DOCS_FILE_MANIFEST.json"
OUTPUT = ROOT / "qa/CHAPTER15_DOCS_MANIFEST.json"

HTML_LABEL = "O003/C90 Chapters 1-15 HTML"
DOCS_LABEL = "O003/C90 Chapters 1-15 GitHub Pages tree"
PRIMARY_ENTRY = "o003-c90-chapters-01-15-reader.html"
PRIMARY_DOWNLOAD = (
    "downloads/topologi-pendekatan-berbasis-inkuiri-bab-01-15-id.pdf"
)
PDF_REPO_PATH = "output/chapters01-15-pdf/chapters_01_15_reader.pdf"
PDF_RUN_1_REPO_PATH = "tmp/pdfs/chapter15-run1.pdf"

REQUIRED_DOCS_SURFACES = frozenset(
    {
        "index.html",
        PRIMARY_ENTRY,
        "chap_subspaces.html",
        "sec_sub_exer.html",
        "o003-c90-ch15-companion.html",
        "o003-c90-ch15-mastery.html",
        "external/o003-readable-layout.css",
        PRIMARY_DOWNLOAD,
        "o003-c90-chapters-01-14-reader.html",
        "downloads/topologi-pendekatan-berbasis-inkuiri-bab-01-14-id.pdf",
    }
)

# Chapter 14's detailed Pages manifest is the frozen authority for every byte
# that the Chapter 15 overlay must retain.  Pinning the manifest itself avoids
# accepting a mutually edited historical manifest and docs tree.
PRIOR_MANIFEST_IDENTITY = {
    "bytes": 2_281_783,
    "sha256": "0ecf12371b7087ed2b353bcdd429e68a166048c6bde9e44db69feebab97c501c",
}
PRIOR_MANIFEST_CENSUS = {
    "canonical_manifest_sha256": (
        "558084d5dcb049b3ba2c8d6a3c64db4537e03cab96ec72c55e86615380f977d2"
    ),
    "file_count": 13_919,
    "html_files": 13_794,
    "total_bytes": 57_919_130,
}

EXPECTED_HISTORICAL_PATHS = frozenset(
    {
        ".nojekyll",
        *(
            "downloads/topologi-pendekatan-berbasis-inkuiri-"
            f"bab-01-{chapter:02d}-id.pdf"
            for chapter in range(2, 15)
        ),
        *(f"o003-c90-ch{chapter:02d}-edition-note.html" for chapter in range(8, 15)),
        *(
            f"o003-c90-chapters-01-{chapter:02d}-reader.html"
            for chapter in range(8, 15)
        ),
    }
)
EXPECTED_EXTRA_FILES = 29


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


def manifest_rows(
    manifest: dict[str, Any],
    *,
    label: str,
    expected_label: str,
) -> tuple[list[dict[str, object]], dict[str, int | str]]:
    require(manifest.get("schema_version") == 1, f"{label} schema version differs")
    require(manifest.get("label") == expected_label, f"{label} label differs")
    require(manifest.get("source_directory") == ".", f"{label} source directory differs")
    require(manifest.get("glob") == "**/*", f"{label} glob differs")
    require(manifest.get("combined_algorithm") == ALGORITHM, f"{label} algorithm differs")

    raw_rows = manifest.get("files")
    require(isinstance(raw_rows, list) and raw_rows, f"{label} has no file rows")
    rows: list[dict[str, object]] = []
    seen: set[str] = set()
    seen_casefolded: set[str] = set()
    for index, raw in enumerate(raw_rows):
        require(isinstance(raw, dict), f"{label} row {index} is not an object")
        require(
            set(raw) == {"path", "bytes", "sha256"},
            f"{label} row {index} has unexpected fields",
        )
        path = clean_relative_path(raw.get("path"), f"{label} row {index}")
        size = positive_int(
            raw.get("bytes"), f"{label} row {index} bytes", allow_zero=True
        )
        checksum = sha256_value(raw.get("sha256"), f"{label} row {index} sha256")
        require(path not in seen, f"{label} repeats path: {path}")
        require(
            path.casefold() not in seen_casefolded,
            f"{label} has a case-insensitive path collision: {path}",
        )
        seen.add(path)
        seen_casefolded.add(path.casefold())
        rows.append({"path": path, "bytes": size, "sha256": checksum})

    require(
        rows == sorted(rows, key=lambda row: str(row["path"]).casefold()),
        f"{label} rows are not in canonical case-insensitive path order",
    )
    computed = {
        "canonical_manifest_sha256": canonical(rows),
        "file_count": len(rows),
        "html_files": sum(
            1 for row in rows if str(row["path"]).lower().endswith((".html", ".htm"))
        ),
        "total_bytes": sum(int(row["bytes"]) for row in rows),
    }
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
    seen_casefolded: set[str] = set()
    for path in files:
        relative = path.relative_to(root).as_posix()
        require(
            relative.casefold() not in seen_casefolded,
            f"{label} has a case-insensitive path collision: {relative}",
        )
        seen_casefolded.add(relative.casefold())
        rows.append({"path": relative, **identity(path)})
    return rows


def assert_manifest_matches_tree(
    manifest_rows_value: list[dict[str, object]],
    root: Path,
    label: str,
) -> None:
    observed = actual_rows(root, label)
    if manifest_rows_value == observed:
        return
    expected_map = {str(row["path"]): row for row in manifest_rows_value}
    observed_map = {str(row["path"]): row for row in observed}
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
        f"{label} differs from its detailed manifest: "
        f"missing={missing[:5]!r}, unexpected={unexpected[:5]!r}, "
        f"changed={changed[:5]!r}"
    )


def row_map(rows: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    return {str(row["path"]): row for row in rows}


def assert_same_row(
    expected: dict[str, object], observed: dict[str, object], label: str
) -> None:
    require(observed == expected, f"{label} byte identity differs")


def validate_pdf_receipts(
    run_one_path: Path,
    run_two_path: Path,
    run_one_pdf: Path,
    pdf: Path,
) -> tuple[dict[str, object], int]:
    run_two = read_json(run_two_path, "Chapter 15 PDF run-two receipt")
    require(run_two.get("schema_version") == 1, "PDF run-two schema version differs")
    require(run_two.get("status") == "pass", "PDF run two did not pass")
    require(run_two.get("run") == 2, "PDF receipt is not run two")
    require(run_two.get("path") == PDF_REPO_PATH, "PDF run-two path differs")
    require(run_two.get("clean_build") is True, "PDF run two was not clean")
    require(
        run_two.get("strict_transcript_gate") is True,
        "PDF run two did not pass the strict transcript gate",
    )
    require(
        run_two.get("byte_identical_to_run_1") is True,
        "PDF runs are not recorded as byte-identical",
    )
    expected = identity(pdf)
    require(run_two.get("bytes") == expected["bytes"], "PDF run-two byte count differs")
    require(run_two.get("sha256") == expected["sha256"], "PDF run-two SHA-256 differs")
    pages = positive_int(run_two.get("pages"), "PDF run-two page count")
    source_epoch = positive_int(
        run_two.get("source_date_epoch"),
        "PDF run-two source epoch",
        allow_zero=True,
    )

    nested_run_one = run_two.get("run_1")
    require(isinstance(nested_run_one, dict), "PDF run-two receipt has no run-one identity")
    require(
        nested_run_one.get("path") == PDF_RUN_1_REPO_PATH,
        "PDF run-two nested run-one path differs",
    )

    # Read and verify run one independently.  The run-two receipt is not an
    # authority for bytes that it merely repeats in its nested identity.
    run_one = read_json(run_one_path, "Chapter 15 PDF run-one receipt")
    require(run_one.get("schema_version") == 1, "PDF run-one schema version differs")
    require(run_one.get("status") == "pass", "PDF run one did not pass")
    require(run_one.get("run") == 1, "PDF receipt is not run one")
    require(run_one.get("path") == PDF_RUN_1_REPO_PATH, "PDF run-one path differs")
    require(run_one.get("clean_build") is True, "PDF run one was not clean")
    require(
        run_one.get("strict_transcript_gate") is True,
        "PDF run one did not pass the strict transcript gate",
    )
    observed_run_one = identity(run_one_pdf)
    require(
        run_one.get("bytes") == observed_run_one["bytes"],
        "PDF run-one receipt byte count differs from its candidate",
    )
    require(
        run_one.get("sha256") == observed_run_one["sha256"],
        "PDF run-one receipt SHA-256 differs from its candidate",
    )
    run_one_pages = positive_int(run_one.get("pages"), "PDF run-one page count")
    run_one_epoch = positive_int(
        run_one.get("source_date_epoch"),
        "PDF run-one source epoch",
        allow_zero=True,
    )
    require(run_one_pages == pages, "PDF run-one and run-two page counts differ")
    require(run_one_epoch == source_epoch, "PDF run-one and run-two source epochs differ")
    require(
        nested_run_one.get("bytes") == observed_run_one["bytes"],
        "PDF run-two nested run-one byte count differs from the run-one candidate",
    )
    require(
        nested_run_one.get("sha256") == observed_run_one["sha256"],
        "PDF run-two nested run-one SHA-256 differs from the run-one candidate",
    )
    require(
        observed_run_one == expected,
        "independently verified PDF run one and final run two are not byte-identical",
    )
    return expected, pages


def validate_docs_qa(
    path: Path,
    docs_summary: dict[str, int | str],
    docs_paths: set[str],
) -> dict[str, Any]:
    report = read_json(path, "Chapter 15 docs QA")
    require(report.get("schema_version") == 1, "docs QA schema version differs")
    require(report.get("status") == "pass", "docs QA did not pass")
    require(report.get("failures") == [], "docs QA records failures")
    for key in ("canonical_manifest_sha256", "file_count", "html_files", "total_bytes"):
        require(report.get(key) == docs_summary[key], f"docs QA {key} differs")
    required = report.get("required_surfaces")
    require(isinstance(required, list), "docs QA required surfaces are missing")
    normalized_required: list[str] = []
    seen_required: set[str] = set()
    for index, value in enumerate(required):
        surface = clean_relative_path(value, f"docs QA required surface {index}")
        require(
            surface.casefold() not in seen_required,
            f"docs QA repeats a required surface case-insensitively: {surface}",
        )
        seen_required.add(surface.casefold())
        normalized_required.append(surface)
    required_set = set(normalized_required)
    missing_required = sorted(REQUIRED_DOCS_SURFACES - required_set, key=str.casefold)
    require(
        not missing_required,
        f"docs QA omitted required reader surfaces: {missing_required!r}",
    )
    absent_required = sorted(required_set - docs_paths, key=str.casefold)
    require(
        not absent_required,
        f"docs QA names required surfaces absent from the docs tree: {absent_required!r}",
    )
    positive_int(report.get("links_and_assets_checked"), "docs QA checked links")
    positive_int(report.get("images_checked"), "docs QA checked images", allow_zero=True)
    require(isinstance(report.get("external_hosts"), dict), "docs QA host census is missing")
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html-root", type=Path, default=HTML_ROOT)
    parser.add_argument("--html-manifest", type=Path, default=HTML_MANIFEST)
    parser.add_argument("--pdf", type=Path, default=PDF)
    parser.add_argument("--pdf-run-1", type=Path, default=PDF_RUN_1)
    parser.add_argument("--pdf-run-2", type=Path, default=PDF_RUN_2)
    parser.add_argument(
        "--pdf-run-1-candidate", type=Path, default=PDF_RUN_1_CANDIDATE
    )
    parser.add_argument("--docs-root", type=Path, default=DOCS_ROOT)
    parser.add_argument("--docs-file-manifest", type=Path, default=DOCS_FILE_MANIFEST)
    parser.add_argument("--docs-qa", type=Path, default=DOCS_QA)
    parser.add_argument(
        "--prior-docs-file-manifest", type=Path, default=PRIOR_DOCS_FILE_MANIFEST
    )
    parser.add_argument("--output", type=Path, default=OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    html_root = resolve_input(args.html_root)
    html_manifest_path = resolve_input(args.html_manifest)
    pdf_path = resolve_input(args.pdf)
    pdf_run_1_path = resolve_input(args.pdf_run_1)
    pdf_run_2_path = resolve_input(args.pdf_run_2)
    pdf_run_1_candidate = resolve_input(args.pdf_run_1_candidate)
    docs_root = resolve_input(args.docs_root)
    docs_manifest_path = resolve_input(args.docs_file_manifest)
    docs_qa_path = resolve_input(args.docs_qa)
    prior_manifest_path = resolve_input(args.prior_docs_file_manifest)
    output_path = resolve_input(args.output)

    html_manifest = read_json(html_manifest_path, "Chapter 15 HTML manifest")
    html_rows, html_summary = manifest_rows(
        html_manifest,
        label="Chapter 15 HTML manifest",
        expected_label=HTML_LABEL,
    )
    assert_manifest_matches_tree(html_rows, html_root, "Chapter 15 HTML tree")
    html_by_path = row_map(html_rows)
    require(PRIMARY_ENTRY in html_by_path, "Chapters 1-15 reader entry is absent from HTML")
    require(PRIMARY_DOWNLOAD not in html_by_path, "HTML tree unexpectedly contains the PDF")

    pdf_identity, pdf_pages = validate_pdf_receipts(
        pdf_run_1_path,
        pdf_run_2_path,
        pdf_run_1_candidate,
        pdf_path,
    )

    prior_file_identity = identity(prior_manifest_path)
    require(
        prior_file_identity == PRIOR_MANIFEST_IDENTITY,
        "frozen Chapter 14 detailed docs manifest identity differs",
    )
    prior_manifest = read_json(prior_manifest_path, "frozen Chapter 14 docs manifest")
    prior_rows, prior_summary = manifest_rows(
        prior_manifest,
        label="frozen Chapter 14 docs manifest",
        expected_label="O003/C90 Chapters 1-14 GitHub Pages tree",
    )
    require(
        prior_summary == PRIOR_MANIFEST_CENSUS,
        "frozen Chapter 14 docs manifest census differs",
    )
    prior_by_path = row_map(prior_rows)

    historical_paths = set(prior_by_path) - set(html_by_path)
    require(
        historical_paths == set(EXPECTED_HISTORICAL_PATHS),
        "the exact Chapter 14 historical-retention set differs",
    )
    historical_rows = [
        prior_by_path[path] for path in sorted(historical_paths, key=str.casefold)
    ]

    docs_manifest = read_json(docs_manifest_path, "Chapter 15 detailed docs manifest")
    docs_rows, docs_summary = manifest_rows(
        docs_manifest,
        label="Chapter 15 detailed docs manifest",
        expected_label=DOCS_LABEL,
    )
    assert_manifest_matches_tree(docs_rows, docs_root, "Chapter 15 docs tree")
    docs_by_path = row_map(docs_rows)

    for path, expected in html_by_path.items():
        require(path in docs_by_path, f"docs overlay omitted current HTML file: {path}")
        assert_same_row(expected, docs_by_path[path], f"docs current HTML file {path}")
    for path in sorted(historical_paths, key=str.casefold):
        require(path in docs_by_path, f"docs overlay omitted historical file: {path}")
        assert_same_row(
            prior_by_path[path], docs_by_path[path], f"docs historical file {path}"
        )

    require(PRIMARY_DOWNLOAD in docs_by_path, "docs tree omits the Chapters 1-15 PDF")
    expected_pdf_row = {"path": PRIMARY_DOWNLOAD, **pdf_identity}
    assert_same_row(
        expected_pdf_row,
        docs_by_path[PRIMARY_DOWNLOAD],
        "docs Chapters 1-15 PDF",
    )
    assert_same_row(
        html_by_path[PRIMARY_ENTRY],
        docs_by_path[PRIMARY_ENTRY],
        "docs Chapters 1-15 reader entry",
    )
    require(
        identity(docs_root / PRIMARY_DOWNLOAD) == pdf_identity,
        "docs PDF bytes differ from the final deterministic PDF",
    )

    expected_extras = historical_paths | {PRIMARY_DOWNLOAD}
    actual_extras = set(docs_by_path) - set(html_by_path)
    require(actual_extras == expected_extras, "docs overlay has an incorrect extra-file set")
    require(
        docs_summary["file_count"] == html_summary["file_count"] + EXPECTED_EXTRA_FILES,
        "docs file count is not HTML file count + 29",
    )
    require(
        len(actual_extras) == EXPECTED_EXTRA_FILES,
        "docs overlay does not contain exactly 29 extra files",
    )
    historical_html = sum(
        1 for path in historical_paths if path.lower().endswith((".html", ".htm"))
    )
    require(
        docs_summary["html_files"] == html_summary["html_files"] + historical_html,
        "docs HTML census differs from current plus historical HTML",
    )
    expected_total = (
        int(html_summary["total_bytes"])
        + sum(int(row["bytes"]) for row in historical_rows)
        + int(pdf_identity["bytes"])
    )
    require(
        docs_summary["total_bytes"] == expected_total,
        "docs byte count differs from current HTML plus historical files plus PDF",
    )

    validate_docs_qa(docs_qa_path, docs_summary, set(docs_by_path))

    output = {
        "schema_version": 1,
        "status": "pass",
        "scope": (
            "GitHub Pages tree for the admitted partial Chapters 1-15 boundary "
            "(15 of 20), retaining deliberate historical entry surfaces and "
            "earlier PDFs"
        ),
        **docs_summary,
        "generated_html_tree": {
            "status": "pass",
            "checked_files": html_summary["file_count"],
            **html_summary,
        },
        "detailed_manifest": {
            "path": docs_manifest_path.relative_to(ROOT).as_posix(),
            **identity(docs_manifest_path),
        },
        "docs_qa": {
            "path": docs_qa_path.relative_to(ROOT).as_posix(),
            **identity(docs_qa_path),
        },
        "historical_retention": {
            "status": "pass",
            "authority_manifest": {
                "path": prior_manifest_path.relative_to(ROOT).as_posix(),
                **prior_file_identity,
            },
            "file_count": len(historical_rows),
            "html_files": historical_html,
            "total_bytes": sum(int(row["bytes"]) for row in historical_rows),
            "canonical_manifest_sha256": canonical(historical_rows),
        },
        "count_contract": {
            "formula": "docs file count = final HTML file count + 29",
            "expected_extra_files": EXPECTED_EXTRA_FILES,
            "actual_extra_files": len(actual_extras),
            "status": "pass",
        },
        "primary_reader": {
            "path": PRIMARY_ENTRY,
            "bytes": html_by_path[PRIMARY_ENTRY]["bytes"],
            "sha256": html_by_path[PRIMARY_ENTRY]["sha256"],
        },
        "primary_download": {
            "path": PRIMARY_DOWNLOAD,
            "pages": pdf_pages,
            **pdf_identity,
        },
        "failures": [],
    }
    payload = (
        json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_name(output_path.name + ".tmp")
    temporary.write_bytes(payload)
    temporary.replace(output_path)
    print(
        json.dumps(
            {
                "status": "pass",
                "output": output_path.relative_to(ROOT).as_posix(),
                "bytes": len(payload),
                "sha256": digest(payload),
                "file_count": docs_summary["file_count"],
                "canonical_manifest_sha256": docs_summary[
                    "canonical_manifest_sha256"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContractError as exc:
        raise SystemExit(f"FAIL: {exc}") from exc
