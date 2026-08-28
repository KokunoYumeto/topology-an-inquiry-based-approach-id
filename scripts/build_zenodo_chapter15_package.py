#!/usr/bin/env python3
"""Assemble the full admitted Chapters 1-15 Zenodo package.

This builder consumes only the final cumulative Chapter 15 source manifest and
the admitted Chapter 15 HTML/PDF.  It never reads or advances a historical
partial-package directory.  ``--check-only`` validates the frozen inputs
without creating package artifacts.
"""

from __future__ import annotations

import argparse
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import shutil

from build_zenodo_chapter11_package import (
    PdfReader,
    assert_pdf_privacy,
    assert_public_text,
    assert_sanitized,
    deterministic_zip,
    digest,
    file_entry,
    identity,
    read_json,
    require_dict,
    require_identity,
    require_positive_int,
    require_sha256,
    safe_archive_name,
)


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
PREDECESSOR_RECORD_ID = 22105198
CONCEPT_DOI = "10.5281/zenodo.22059894"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
BOUNDARY = "chapters_01_15_with_separately_licensed_self_study_companions"
BASE = "topologi-pendekatan-berbasis-inkuiri-bab-01-15"
PDF_NAME = f"{BASE}-id.pdf"
HTML_NAME = f"{BASE}-html.zip"
SOURCE_NAME = f"{BASE}-sumber.zip"
LICENSES_NAME = f"{BASE}-licenses.md"
COMPANION_RIGHTS_NAME = f"{BASE}-rights-companion.md"
MANIFEST_NAME = f"{BASE}-manifest.json"

PDF = ROOT / "output/chapters01-15-pdf/chapters_01_15_reader.pdf"
HTML_ROOT = ROOT / "output/chapters01-15-html"
SOURCE_MANIFEST = ROOT / "qa/CHAPTER15_SOURCE_MANIFEST.json"
HTML_MANIFEST = ROOT / "qa/CHAPTER15_HTML_MANIFEST.json"
AUTHORITY_ARCHIVE = LANE / "authority/archives/gvsuoer-topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9.zip"

REQUIRED_INVENTORY = {
    "repo/source/chapters_01_15_reader.ptx",
    "repo/companion/chapter_15_subspaces_self_study.ptx",
    "repo/companion/chapter_15_mastery.ptx",
    "repo/backend/chapter_15_companion_manifest.json",
    "repo/backend/chapter_15_entry_aliases.csv",
    "repo/backend/chapter_15_source_prompt_map.csv",
    "repo/backend/chapter_15_grouping_nodes.json",
    "repo/backend/chapter_15_prompt_inventory.json",
    "repo/qa/CHAPTER15_SOURCE_COMPLETE_QA.json",
    "repo/qa/CHAPTER15_COMPANION_QA.json",
    "repo/qa/CHAPTER15_COMPANION_WRAPPER_SCHEMA_QA.json",
    "repo/qa/CHAPTER15_MASTERY_SCHEMA_QA.json",
    "repo/qa/CHAPTER15_CUMULATIVE_SCHEMA_QA.json",
    "repo/qa/CHAPTER15_HTML_MANIFEST.json",
    "repo/qa/CHAPTER15_HTML_QA.json",
    "repo/qa/CHAPTER15_BROWSER_QA.json",
    "repo/qa/CHAPTER15_ASSET_PDF_METADATA_QA.json",
    "repo/qa/CHAPTER15_PDF_VISUAL_QA.json",
    "repo/qa/CHAPTER15_BUILD_QA.md",
}


def is_historical_partial_path(value: str) -> bool:
    name = PurePosixPath(value).name.casefold()
    return (
        ".partial." in name
        or "chapter12_companion_partial" in name
        or name == "build_zenodo_chapter12_partial_package.py"
        or "chapter14_partial" in name
        or "chapter15_partial" in name
    )


def assert_pdf_payload_privacy(name: str, data: bytes) -> None:
    """Inspect metadata for every PDF carried inside either release ZIP."""
    reader = PdfReader(BytesIO(data))
    metadata = reader.metadata
    if metadata is not None:
        assert_public_text(
            f"{name} metadata",
            "\n".join(str(value) for value in metadata.values()),
        )
    root = reader.trailer.get("/Root")
    if root is None:
        return
    metadata_stream = root.get_object().get("/Metadata")
    if metadata_stream is None:
        return
    payload = metadata_stream.get_object().get_data()
    if payload.startswith((b"\xff\xfe", b"\xfe\xff")):
        text = payload.decode("utf-16")
    elif b"\x00" in payload[:128]:
        encoding = "utf-16-be" if payload[:1] == b"\x00" else "utf-16-le"
        text = payload.decode(encoding)
    else:
        text = payload.decode("utf-8-sig")
    assert_public_text(f"{name} XMP", text)


def html_entries(
    html_manifest: dict[str, object], expected_html: dict[str, object]
) -> dict[str, bytes]:
    files = html_manifest.get("files")
    if not isinstance(files, list) or len(files) != expected_html["files"]:
        raise RuntimeError("HTML manifest has the wrong file census")
    entries: dict[str, bytes] = {}
    total = 0
    for raw in files:
        row = require_dict(raw, "HTML manifest row")
        value = row.get("path")
        if not isinstance(value, str):
            raise RuntimeError("HTML manifest row has no path")
        relative = PurePosixPath(value)
        if relative.is_absolute() or ".." in relative.parts or "\\" in value:
            raise RuntimeError(f"HTML manifest path escaped target: {value!r}")
        path = HTML_ROOT.joinpath(*relative.parts)
        data = path.read_bytes()
        if len(data) != row.get("bytes") or digest(data) != row.get("sha256"):
            raise RuntimeError(f"HTML file differs from manifest: {relative}")
        archive_name = safe_archive_name(f"reader/{relative.as_posix()}")
        assert_sanitized(archive_name, data)
        if relative.suffix.casefold() == ".pdf":
            assert_pdf_payload_privacy(archive_name, data)
        entries[archive_name] = data
        total += len(data)
    if total != expected_html["bytes"]:
        raise RuntimeError("HTML byte total changed")
    for name, path in (
        ("README.md", ROOT / "README.md"),
        ("LICENSES.md", ROOT / "LICENSES.md"),
        ("COMPANION_RIGHTS.md", ROOT / "companion/RIGHTS.md"),
        ("CHAPTER15_HTML_MANIFEST.json", HTML_MANIFEST),
    ):
        archive_name, data = file_entry(name, path)
        entries[archive_name] = data
    return entries


def inventory_disk_path(manifest_path: str) -> Path:
    if manifest_path.startswith("repo/"):
        return ROOT.joinpath(*PurePosixPath(manifest_path.removeprefix("repo/")).parts)
    if manifest_path.startswith("00_control/"):
        return LANE.joinpath(*PurePosixPath(manifest_path).parts)
    raise RuntimeError(f"unsupported package-source inventory path: {manifest_path}")


def source_entries(source_manifest: dict[str, object]) -> dict[str, bytes]:
    raw_inventory = source_manifest.get("package_source_inventory")
    if not isinstance(raw_inventory, list) or not raw_inventory:
        raise RuntimeError("source manifest has no package-source inventory")
    inventory: dict[str, dict[str, object]] = {}
    for raw in raw_inventory:
        row = require_dict(raw, "package-source inventory row")
        value = row.get("path")
        if not isinstance(value, str):
            raise RuntimeError("package-source inventory row has no path")
        path = PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts or "\\" in value:
            raise RuntimeError(f"unsafe package-source inventory path: {value!r}")
        if is_historical_partial_path(value):
            raise RuntimeError(f"historical partial-package path leaked into final inventory: {value}")
        if value in inventory:
            raise RuntimeError(f"duplicate package-source inventory path: {value}")
        inventory[value] = row
    missing = REQUIRED_INVENTORY - set(inventory)
    if missing:
        raise RuntimeError(f"final source inventory omits required Chapter 15 files: {sorted(missing)}")

    declared_scoped = {
        path for path in inventory
        if path.startswith(("repo/companion/", "repo/backend/", "repo/assets/", "repo/xsl/", "repo/scripts/"))
    }
    actual_scoped: set[str] = set()
    for directory in ("companion", "backend", "assets", "xsl", "scripts"):
        base = ROOT / directory
        for path in base.rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix.casefold() == ".pyc":
                continue
            if directory == "scripts" and path.suffix.casefold() != ".py":
                continue
            value = f"repo/{path.relative_to(ROOT).as_posix()}"
            if is_historical_partial_path(value):
                continue
            actual_scoped.add(value)
    if actual_scoped != declared_scoped:
        missing_from_disk = sorted(declared_scoped - actual_scoped)[:10]
        undeclared = sorted(actual_scoped - declared_scoped)[:10]
        raise RuntimeError(f"package source-tree drift: missing={missing_from_disk}, undeclared={undeclared}")

    entries: dict[str, bytes] = {}
    prefix = "point-set-topology-id"
    for manifest_path in sorted(inventory, key=str.casefold):
        row = inventory[manifest_path]
        disk_path = inventory_disk_path(manifest_path)
        require_identity(
            disk_path,
            {
                "bytes": require_positive_int(row.get("bytes"), f"{manifest_path} bytes"),
                "sha256": require_sha256(row.get("sha256"), f"{manifest_path} SHA-256"),
            },
            manifest_path,
        )
        archive_name, data = file_entry(f"{prefix}/{manifest_path}", disk_path)
        if disk_path.suffix.casefold() == ".pdf":
            assert_pdf_payload_privacy(archive_name, data)
        entries[archive_name] = data

    archive_row = require_dict(source_manifest.get("package_authority_archive"), "authority archive")
    expected_archive_path = f"authority/archives/{AUTHORITY_ARCHIVE.name}"
    if archive_row.get("path") != expected_archive_path:
        raise RuntimeError("source manifest points to a different authority archive")
    require_identity(
        AUTHORITY_ARCHIVE,
        {
            "bytes": require_positive_int(archive_row.get("bytes"), "authority archive bytes"),
            "sha256": require_sha256(archive_row.get("sha256"), "authority archive SHA-256"),
        },
        "manifest-declared authority archive",
    )
    manifest_name = f"{prefix}/repo/qa/CHAPTER15_SOURCE_MANIFEST.json"
    archive_name, data = file_entry(manifest_name, SOURCE_MANIFEST)
    if archive_name in entries:
        raise RuntimeError("source manifest must not self-declare an impossible identity")
    entries[archive_name] = data
    return entries


def validate_inputs() -> tuple[dict[str, object], dict[str, object], dict[str, object], int]:
    source_manifest = read_json(SOURCE_MANIFEST)
    if (
        source_manifest.get("status") != "pass"
        or source_manifest.get("partial") is not True
        or source_manifest.get("boundary_complete") is not True
        or source_manifest.get("pending_evidence") != []
        or source_manifest.get("boundary") != BOUNDARY
        or source_manifest.get("admission_status") != "partial_checkpoint_admitted"
    ):
        raise RuntimeError("source manifest is not a truthful admitted Chapter 15 checkpoint")
    provenance = require_dict(source_manifest.get("production_provenance"), "production provenance")
    if provenance.get("tool") != MODEL:
        raise RuntimeError("source manifest model provenance changed")

    reader = require_dict(source_manifest.get("reader_artifacts"), "reader artifacts")
    pdf_row = require_dict(reader.get("pdf"), "admitted PDF")
    if pdf_row.get("status") != "pass" or pdf_row.get("path") != f"repo/{PDF.relative_to(ROOT).as_posix()}":
        raise RuntimeError("source manifest has not admitted the exact Chapter 15 PDF")
    expected_pdf = {
        "bytes": require_positive_int(pdf_row.get("bytes"), "PDF bytes"),
        "sha256": require_sha256(pdf_row.get("sha256"), "PDF SHA-256"),
    }
    pages = require_positive_int(pdf_row.get("pages"), "PDF pages")
    require_identity(PDF, expected_pdf, "Chapter 15 PDF")
    pdf_reader = assert_pdf_privacy(PDF)
    if len(pdf_reader.pages) != pages:
        raise RuntimeError("Chapter 15 PDF page count changed")

    html_row = require_dict(reader.get("html"), "admitted HTML")
    if html_row.get("status") != "deterministic_tree_pass":
        raise RuntimeError("source manifest has not admitted deterministic Chapter 15 HTML")
    expected_html = {
        "files": require_positive_int(html_row.get("file_count"), "HTML files"),
        "bytes": require_positive_int(html_row.get("bytes"), "HTML bytes"),
        "canonical_manifest_sha256": require_sha256(html_row.get("canonical_manifest_sha256"), "HTML canonical SHA-256"),
    }
    html_manifest = read_json(HTML_MANIFEST)
    if (
        html_manifest.get("file_count") != expected_html["files"]
        or html_manifest.get("total_bytes") != expected_html["bytes"]
        or html_manifest.get("canonical_manifest_sha256") != expected_html["canonical_manifest_sha256"]
    ):
        raise RuntimeError("HTML manifest differs from source-manifest admission")
    return source_manifest, html_manifest, expected_html, pages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "output/zenodo-chapters01-15",
        help="Empty or package-only output directory.",
    )
    parser.add_argument(
        "--version",
        help="Release version label; required for assembly, omitted for --check-only.",
    )
    parser.add_argument(
        "--predecessor-record-id",
        type=int,
        default=PREDECESSOR_RECORD_ID,
        help="Frozen latest published Zenodo record in the existing concept lineage.",
    )
    parser.add_argument(
        "--concept-doi",
        default=CONCEPT_DOI,
        help="Existing Zenodo concept DOI to advance.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate frozen admitted inputs without writing package artifacts.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.predecessor_record_id != PREDECESSOR_RECORD_ID:
        raise SystemExit(
            f"--predecessor-record-id must remain {PREDECESSOR_RECORD_ID} for this frozen checkpoint"
        )
    if args.concept_doi != CONCEPT_DOI:
        raise SystemExit(
            f"--concept-doi must remain {CONCEPT_DOI} for this existing lineage"
        )
    try:
        source_manifest, html_manifest, expected_html, pages = validate_inputs()
        # Validate the complete source inventory even in check-only mode; no
        # bytes are written and a historical partial package is never opened.
        source_payload = source_entries(source_manifest)
        html_payload = html_entries(html_manifest, expected_html)
    except (FileNotFoundError, RuntimeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Chapter 15 package admission gate failed: {exc}") from exc
    if args.check_only:
        print(json.dumps({
            "status": "pass",
            "partial": True,
            "boundary_complete": True,
            "boundary": BOUNDARY,
            "pdf_pages": pages,
            "html_entries": len(html_payload),
            "source_entries": len(source_payload),
            "check_only": True,
        }, sort_keys=True))
        return 0
    if not args.version:
        raise SystemExit("--version is required for package assembly")

    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    expected_names = {
        PDF_NAME, HTML_NAME, SOURCE_NAME, LICENSES_NAME, COMPANION_RIGHTS_NAME, MANIFEST_NAME,
    }
    unexpected = sorted(path.name for path in output.iterdir() if path.name not in expected_names)
    if unexpected:
        raise RuntimeError(f"unexpected existing package output(s): {unexpected}")

    pdf_target = output / PDF_NAME
    shutil.copyfile(PDF, pdf_target)
    licenses_target = output / LICENSES_NAME
    rights_target = output / COMPANION_RIGHTS_NAME
    _, licenses_data = file_entry(LICENSES_NAME, ROOT / "LICENSES.md")
    _, rights_data = file_entry(COMPANION_RIGHTS_NAME, ROOT / "companion/RIGHTS.md")
    licenses_target.write_bytes(licenses_data)
    rights_target.write_bytes(rights_data)
    html_zip = deterministic_zip(output / HTML_NAME, html_payload)
    source_zip = deterministic_zip(output / SOURCE_NAME, source_payload)

    file_rows = [
        {"path": PDF_NAME, **identity(pdf_target), "role": f"{pages}-page Indonesian cumulative Chapters 1-15 reader PDF"},
        {**html_zip, "role": "admitted cumulative Chapters 1-15 HTML reader and rights notes"},
        {**source_zip, "role": "editable Chapters 1-15 source, companions, final backend, build code, authority identity, and sanitized QA"},
        {"path": LICENSES_NAME, **identity(licenses_target), "role": "collection component-rights map"},
        {"path": COMPANION_RIGHTS_NAME, **identity(rights_target), "role": "original companion rights and attribution"},
    ]
    package_manifest = {
        "schema_version": 1,
        "status": "pass",
        "partial": True,
        "boundary_complete": True,
        "boundary": BOUNDARY,
        "admission_status": "partial_checkpoint_admitted",
        "record": {
            "concept_doi": args.concept_doi,
            "predecessor_record_id": args.predecessor_record_id,
            "publication_target": "new version of the existing concept lineage",
            "title": "Topologi: Pendekatan Berbasis Inkuiri",
            "version": args.version,
            "language": "ind",
            "completion": {"chapters_verified": 15, "chapters_total": 20, "complete_edition": False, "admitted_boundary_complete": True},
        },
        "authority": {
            "work": "Topology: An Inquiry-Based Approach",
            "author": "Steven Schlicker",
            "institution": "Grand Valley State University",
            "commit": "0c2d8f614ef87aa00de373f3418146c2f1d13bb9",
            "tree": "7df245934eedb7174d5ff8af18afff5a7abdde78",
            "archive": {
                "path": AUTHORITY_ARCHIVE.name,
                **identity(AUTHORITY_ARCHIVE),
                "public_source_package_included": False,
                "omission_reason": "legacy upstream PDF metadata contains absolute author-workstation paths",
            },
        },
        "reader": {
            "pdf": {"pages": pages, **identity(PDF)},
            "html": expected_html,
            "source_files_translated": 105,
            "source_manifest": {"path": "qa/CHAPTER15_SOURCE_MANIFEST.json", **identity(SOURCE_MANIFEST)},
        },
        "rights": [
            {"component": "translated GVSU instructional text", "license": "CC BY-NC-SA 3.0", "url": "https://creativecommons.org/licenses/by-nc-sa/3.0/", "basis": "conservative determination because upstream metadata conflicts"},
            {"component": "original self-study companions and epsilon-delta lab", "license": "CC BY 4.0", "url": "https://creativecommons.org/licenses/by/4.0/"},
            {"component": "software, XSLT, fonts, figures, and separately noticed assets", "license": "component notices retained"},
        ],
        "production_provenance": {
            "tool": MODEL,
            "direction": "the user",
            "scope": "translation drafting, original companion, modular backend, and edition QA",
            "credit_note": "This provenance does not replace source-author, institutional, or human-contributor credits.",
        },
        "caveats": [
            "This is a verified 15-of-20 admitted boundary, not the complete edition.",
            "HTML is the primary accessible surface unless the admitted PDF receipt reports tagging.",
            "Whole-book figure-provenance and complete-edition closure remain later gates.",
            "The unmodified upstream archive is hash-bound but omitted from the public source ZIP because 20 original PDF metadata dictionaries retain legacy absolute author-workstation paths.",
        ],
        "files": file_rows,
        "package_validation": {
            "zip_crc_test": "pass",
            "zip_inventory": "pass",
            "zip_deterministic_double_build": "pass",
            "textual_privacy_scan": "private-name, common absolute/local-path, and credential markers absent",
            "binary_credential_marker_scan": "pass",
            "pdf_metadata_and_xmp_privacy_scan": "all standalone and packaged PDFs pass",
            "raw_build_logs_included": False,
            "source_inventory_identity_validation": "pass",
            "authority_archive_identity_validation": "pass; exact local bytes retained and hash-bound",
            "raw_authority_archive_publicly_included": False,
            "historical_partial_package_used": False,
        },
    }
    manifest_target = output / MANIFEST_NAME
    manifest_target.write_text(
        json.dumps(package_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    assert_sanitized(manifest_target.name, manifest_target.read_bytes())
    actual_names = {path.name for path in output.iterdir() if path.is_file()}
    if actual_names != expected_names:
        raise RuntimeError(f"final package output set differs: {sorted(actual_names)}")
    print(json.dumps({
        "status": "pass",
        "partial": True,
        "boundary_complete": True,
        "output_directory": output.name,
        "files": [*file_rows, {"path": MANIFEST_NAME, **identity(manifest_target), "role": "package manifest"}],
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
