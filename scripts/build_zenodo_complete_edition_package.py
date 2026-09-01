#!/usr/bin/env python3
"""Assemble the deterministic complete-edition preservation package.

The builder advances only the existing Zenodo concept lineage.  It consumes a
passing complete source/backend manifest plus the final deterministic PDF and
finalized offline HTML receipts.  It packages the reader-first PDF, HTML tree,
compact editable source/backend, component-rights documents, a release
manifest, and SHA-256 checksums.  No historical partial package is read.

``--preflight`` validates and privacy-scans the static complete-edition source
selection without requiring final build artifacts and writes nothing.
``--check-only`` performs the full admission and byte checks without assembling
ZIPs or other release files.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
from typing import Any, Iterable
import zipfile

try:
    from PyPDF2 import PdfReader
except ModuleNotFoundError:
    from pypdf import PdfReader

import build_complete_edition_source_manifest as source_builder


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
BOUNDARY = source_builder.BOUNDARY
CONCEPT_DOI = "10.5281/zenodo.22059894"
# The latest published record currently in the existing concept lineage is
# 22164668.  Keep this pinned so a complete-edition release cannot accidentally
# fork from an older checkpoint or create a parallel lineage.
PREDECESSOR_RECORD_ID = 22164668
FIXED_ZIP_TIME = (2023, 8, 15, 0, 0, 0)

BASE = "topologi-pendekatan-berbasis-inkuiri-edisi-lengkap"
PDF_NAME = f"{BASE}-id.pdf"
HTML_NAME = f"{BASE}-html.zip"
SOURCE_NAME = f"{BASE}-sumber-backend.zip"
LICENSES_NAME = f"{BASE}-licenses.md"
COMPANION_RIGHTS_NAME = f"{BASE}-rights-companion.md"
MANIFEST_NAME = f"{BASE}-manifest.json"
CHECKSUMS_NAME = f"{BASE}-checksums.sha256"

PDF = source_builder.FINAL_PDF
HTML_ROOT = ROOT / "output/chapters01-20-complete-html"
SOURCE_MANIFEST = source_builder.DEFAULT_OUTPUT
HTML_MANIFEST = source_builder.HTML_MANIFEST
HTML_QA = source_builder.HTML_QA
HTML_VENDOR_MANIFEST = source_builder.HTML_VENDOR_MANIFEST
PDF_QA = source_builder.PDF_QA
AUTHORITY_ARCHIVE = source_builder.AUTHORITY_ARCHIVE

TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".csv", ".ptx", ".py", ".xsl",
    ".xml", ".css", ".html", ".js", ".mjs", ".svg", ".tex",
    ".toml", ".yaml", ".yml", ".sha256",
}
ABSOLUTE_PATH_PATTERNS = (
    re.compile(r"(?i)(?<![A-Za-z0-9])[A-Za-z]:[\\/](?:Users|Documents and Settings|ProgramData|Windows|home|tmp|temp)[\\/]"),
    # A UNC path must have a host component that cannot contain a slash.  The
    # narrower host class avoids mistaking escaped regular-expression literals
    # in minified JavaScript for paths.
    re.compile(r"(?i)(?<![A-Za-z0-9_])\\\\[^\\/\s]+[\\/](?:Users|home|[A-Za-z]\$)[\\/]"),
    re.compile(r"/(?:home|Users)/[^/\s]+/"),
    re.compile(r"(?i)file://(?:localhost)?/"),
)
CREDENTIAL_PATTERNS = (
    re.compile(r"(?i)Authorization:\s*Bearer\s+[A-Za-z0-9._~+/=-]{20,}"),
    re.compile(r"(?i)(?:access_token|api_token)\s*=\s*['\"]?[A-Za-z0-9._~+/=-]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"(?i)ZENODO_TOKEN\s*[:=]\s*['\"]?[A-Za-z0-9._~-]{20,}"),
)
BINARY_CREDENTIAL_PATTERNS = (
    re.compile(rb"(?i)Authorization:\s*Bearer\s+[A-Za-z0-9._~+/=-]{20,}"),
    re.compile(rb"(?i)(?:access_token|api_token)\s*=\s*['\"]?[A-Za-z0-9._~+/=-]{20,}"),
    re.compile(rb"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(rb"ghp_[A-Za-z0-9]{20,}"),
    re.compile(rb"(?i)ZENODO_TOKEN\s*[:=]\s*['\"]?[A-Za-z0-9._~-]{20,}"),
)
PRIVATE_NAME_MARKER = bytes((70, 108, 111, 114, 105, 115))
SENSITIVE_PATH_LABELS = ("new " "zenodo token", "github " "tokens")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def identity(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {"bytes": len(payload), "sha256": sha256_bytes(payload)}


def json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def safe_archive_name(raw: str) -> str:
    path = PurePosixPath(raw)
    require(not path.is_absolute() and bool(path.parts) and ".." not in path.parts, f"unsafe archive path: {raw!r}")
    return path.as_posix()


def assert_public_text(name: str, text: str) -> None:
    require(PRIVATE_NAME_MARKER.decode("ascii").casefold() not in text.casefold(), f"private-name marker in {name}")
    for pattern in ABSOLUTE_PATH_PATTERNS:
        require(pattern.search(text) is None, f"absolute/local path marker in {name}")
    lowered = text.casefold()
    require(not any(label in lowered for label in SENSITIVE_PATH_LABELS), f"sensitive credential-file label in {name}")
    for pattern in CREDENTIAL_PATTERNS:
        require(pattern.search(text) is None, f"credential-like value in {name}")


def assert_sanitized(name: str, data: bytes) -> None:
    folded = name.casefold()
    require(not folded.endswith((".log", ".tmp", ".pyc", ".part", ".partial")), f"disallowed archive entry: {name}")
    require("__pycache__" not in folded and ".partial." not in folded, f"historical/transient archive entry: {name}")
    require(PRIVATE_NAME_MARKER.lower() not in data.lower(), f"private-name marker in {name}")
    for pattern in BINARY_CREDENTIAL_PATTERNS:
        require(pattern.search(data) is None, f"credential-like byte sequence in {name}")
    if Path(name).suffix.casefold() in TEXT_EXTENSIONS:
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise RuntimeError(f"selected textual entry is not UTF-8: {name}") from exc
        assert_public_text(name, text)


def assert_pdf_payload_privacy(name: str, data: bytes) -> int:
    assert_sanitized(name, data)
    reader = PdfReader(BytesIO(data))
    metadata = reader.metadata
    if metadata is not None:
        assert_public_text(f"{name} metadata", "\n".join(str(value) for value in metadata.values()))
    root = reader.trailer.get("/Root")
    if root is not None:
        try:
            stream = root.get_object().get("/Metadata")
            if stream is not None:
                payload = stream.get_object().get_data()
                if payload.startswith((b"\xff\xfe", b"\xfe\xff")):
                    text = payload.decode("utf-16")
                elif b"\0" in payload[:128]:
                    encoding = "utf-16-be" if payload[:1] == b"\0" else "utf-16-le"
                    text = payload.decode(encoding)
                else:
                    text = payload.decode("utf-8-sig")
                assert_public_text(f"{name} XMP", text)
        except (AttributeError, KeyError, TypeError, UnicodeDecodeError, ValueError) as exc:
            raise RuntimeError(f"unable to inspect PDF XMP privacy metadata: {name}") from exc
    return len(reader.pages)


@dataclass(frozen=True)
class ArchiveEntry:
    name: str
    path: Path | None = None
    data: bytes | None = None
    expected_bytes: int | None = None
    expected_sha256: str | None = None

    def payload(self) -> bytes:
        require((self.path is None) != (self.data is None), f"archive entry has ambiguous payload: {self.name}")
        payload = self.path.read_bytes() if self.path is not None else bytes(self.data or b"")
        if self.expected_bytes is not None:
            require(len(payload) == self.expected_bytes, f"archive entry byte count changed: {self.name}")
        if self.expected_sha256 is not None:
            require(sha256_bytes(payload) == self.expected_sha256, f"archive entry SHA-256 changed: {self.name}")
        assert_sanitized(self.name, payload)
        if PurePosixPath(self.name).suffix.casefold() == ".pdf":
            assert_pdf_payload_privacy(self.name, payload)
        return payload


def file_entry(name: str, path: Path, expected: dict[str, Any] | None = None) -> ArchiveEntry:
    require(path.is_file(), f"missing archive input: {path}")
    safe = safe_archive_name(name)
    return ArchiveEntry(
        safe,
        path=path,
        expected_bytes=None if expected is None else int(expected["bytes"]),
        expected_sha256=None if expected is None else str(expected["sha256"]),
    )


def data_entry(name: str, payload: bytes) -> ArchiveEntry:
    return ArchiveEntry(safe_archive_name(name), data=payload, expected_bytes=len(payload), expected_sha256=sha256_bytes(payload))


def validate_entry_set(entries: Iterable[ArchiveEntry]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    total = 0
    canonical = hashlib.sha256()
    for entry in sorted(entries, key=lambda value: value.name.casefold()):
        require(entry.name not in seen, f"duplicate archive member: {entry.name}")
        seen.add(entry.name)
        payload = entry.payload()
        total += len(payload)
        digest = sha256_bytes(payload)
        rows.append({"path": entry.name, "bytes": len(payload), "sha256": digest})
        canonical.update(entry.name.encode("utf-8"))
        canonical.update(b"\0")
        canonical.update(str(len(payload)).encode("ascii"))
        canonical.update(b"\0")
        canonical.update(payload)
        canonical.update(b"\0")
    return {
        "entry_count": len(rows),
        "uncompressed_bytes": total,
        "canonical_entry_sha256": canonical.hexdigest(),
        "entries": rows,
    }


def write_zip(path: Path, entries: list[ArchiveEntry]) -> dict[str, Any]:
    ordered = sorted(entries, key=lambda value: value.name.casefold())
    seen: set[str] = set()
    total = 0
    canonical = hashlib.sha256()
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", allowZip64=True) as archive:
        for entry in ordered:
            require(entry.name not in seen, f"duplicate archive member: {entry.name}")
            seen.add(entry.name)
            payload = entry.payload()
            total += len(payload)
            canonical.update(entry.name.encode("utf-8"))
            canonical.update(b"\0")
            canonical.update(str(len(payload)).encode("ascii"))
            canonical.update(b"\0")
            canonical.update(payload)
            canonical.update(b"\0")
            info = zipfile.ZipInfo(filename=entry.name, date_time=FIXED_ZIP_TIME)
            info.create_system = 3
            info.external_attr = (0o100644 & 0xFFFF) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            info.flag_bits |= 0x800
            archive.writestr(info, payload, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(path, "r") as archive:
        require(archive.testzip() is None, f"ZIP CRC verification failed: {path}")
        names = archive.namelist()
        require(names == [entry.name for entry in ordered], f"ZIP inventory/order differs: {path}")
        require(len(names) == len(set(names)), f"duplicate ZIP member: {path}")
        require(sum(row.file_size for row in archive.infolist()) == total, f"ZIP uncompressed-byte census differs: {path}")
    return {
        "path": path.name,
        **identity(path),
        "entry_count": len(ordered),
        "uncompressed_bytes": total,
        "canonical_entry_sha256": canonical.hexdigest(),
    }


def deterministic_zip(path: Path, entries: list[ArchiveEntry]) -> dict[str, Any]:
    first = write_zip(path, entries)
    with tempfile.TemporaryDirectory(prefix="o003-complete-release-verify-") as temporary:
        second = write_zip(Path(temporary) / path.name, entries)
        for key in ("bytes", "sha256", "entry_count", "uncompressed_bytes", "canonical_entry_sha256"):
            require(first[key] == second[key], f"non-deterministic ZIP {path.name}: {key}")
    first["deterministic_double_build"] = True
    return first


def load_source_manifest() -> dict[str, Any]:
    expected = source_builder.build_manifest(require_final=True)
    expected_payload = source_builder.json_bytes(expected)
    require(SOURCE_MANIFEST.is_file(), "complete source/backend manifest has not been frozen")
    require(SOURCE_MANIFEST.read_bytes() == expected_payload, "complete source/backend manifest is stale or non-deterministic")
    require(expected.get("status") == "pass" and expected.get("complete_edition") is True, "source/backend manifest is not a complete edition")
    return expected


def source_entries(manifest: dict[str, Any]) -> list[ArchiveEntry]:
    raw = manifest.get("package_source_inventory")
    require(isinstance(raw, list) and raw, "source/backend manifest has no inventory")
    entries: list[ArchiveEntry] = []
    for row in raw:
        require(isinstance(row, dict) and isinstance(row.get("path"), str), "malformed source/backend inventory row")
        value = str(row["path"])
        path = source_builder.inventory_disk_path(value)
        entries.append(file_entry(f"point-set-topology-id/{value}", path, row))
    entries.append(
        file_entry(
            "point-set-topology-id/repo/backend/complete_edition_source_backend_manifest.json",
            SOURCE_MANIFEST,
            identity(SOURCE_MANIFEST),
        )
    )
    return entries


def validate_html() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = source_builder.read_json(HTML_MANIFEST)
    qa = source_builder.read_json(HTML_QA)
    require(manifest.get("stage") == "finalized" and manifest.get("target") == "chapters01-20-complete-html", "HTML manifest is not final")
    require(qa.get("status") == "pass" and qa.get("failures") == [], "HTML QA did not pass")
    checks = qa.get("checks")
    require(isinstance(checks, dict) and checks and all(value is True for value in checks.values()), "HTML QA checks are not all true")
    return manifest, qa


def html_entries(manifest: dict[str, Any], qa: dict[str, Any]) -> list[ArchiveEntry]:
    raw = manifest.get("files")
    require(isinstance(raw, list) and len(raw) == manifest.get("file_count"), "HTML manifest inventory is malformed")
    entries: list[ArchiveEntry] = []
    total = 0
    for row in raw:
        require(isinstance(row, dict) and isinstance(row.get("path"), str), "malformed HTML manifest row")
        relative = source_builder.safe_relative(str(row["path"]))
        path = HTML_ROOT.joinpath(*relative.parts).resolve()
        path.relative_to(HTML_ROOT.resolve())
        entries.append(file_entry(f"reader/{relative.as_posix()}", path, row))
        total += int(row["bytes"])
    require(total == manifest.get("total_bytes"), "HTML manifest byte total changed")
    for name, path in (
        ("README.md", ROOT / "README.md"),
        ("LICENSES.md", ROOT / "LICENSES.md"),
        ("COMPANION_RIGHTS.md", ROOT / "companion/RIGHTS.md"),
        ("CHAPTER20_COMPLETE_HTML_MANIFEST.json", HTML_MANIFEST),
        ("CHAPTER20_COMPLETE_HTML_QA.json", HTML_QA),
        ("CHAPTER20_COMPLETE_HTML_VENDOR_MANIFEST.json", HTML_VENDOR_MANIFEST),
    ):
        entries.append(file_entry(name, path))
    return entries


def validate_pdf() -> tuple[dict[str, Any], int]:
    qa = source_builder.read_json(PDF_QA)
    require(qa.get("status") == "pass" and qa.get("failures") == [], "complete PDF QA did not pass")
    artifact = qa.get("artifact")
    require(isinstance(artifact, dict), "complete PDF QA artifact is missing")
    require(artifact.get("path") == "output/chapters01-20-complete-pdf/chapters_01_20_complete_reader.pdf", "complete PDF path changed")
    expected = {"bytes": artifact.get("bytes"), "sha256": artifact.get("sha256")}
    source_builder.require_identity(PDF, expected, "complete PDF")
    pages = assert_pdf_payload_privacy(PDF.name, PDF.read_bytes())
    require(pages == artifact.get("pages") and pages > 0, "complete PDF page count differs from QA")
    return qa, pages


def validate_static_preflight() -> dict[str, Any]:
    manifest = source_builder.build_manifest(require_final=False)
    entries: list[ArchiveEntry] = []
    for row in manifest["package_source_inventory"]:
        entries.append(file_entry(f"point-set-topology-id/{row['path']}", source_builder.inventory_disk_path(row["path"]), row))
    inventory = validate_entry_set(entries)
    return {
        "status": "pass",
        "preflight": True,
        "complete_edition": True,
        "concept_doi": CONCEPT_DOI,
        "predecessor_record_id": PREDECESSOR_RECORD_ID,
        "chapters": "20/20",
        "completion_modules": "8/8",
        "static_source_entries": inventory["entry_count"],
        "static_source_bytes": inventory["uncompressed_bytes"],
        "pending_final_inputs": [
            path.relative_to(ROOT).as_posix()
            for path in (SOURCE_MANIFEST, HTML_MANIFEST, HTML_QA, PDF_QA, PDF)
            if not path.is_file()
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--preflight", action="store_true", help="validate static source selection without final build artifacts or writes")
    mode.add_argument("--check-only", action="store_true", help="validate all final admitted inputs without assembling release files")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "output/zenodo-complete-edition", help="complete-edition release package directory")
    parser.add_argument("--version", help="release version label; required for assembly")
    parser.add_argument("--concept-doi", default=CONCEPT_DOI, help="existing Zenodo concept DOI")
    parser.add_argument("--predecessor-record-id", type=int, default=PREDECESSOR_RECORD_ID, help="latest published record in the existing concept lineage")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        require(args.concept_doi == CONCEPT_DOI, f"--concept-doi must remain {CONCEPT_DOI}")
        require(args.predecessor_record_id == PREDECESSOR_RECORD_ID, f"--predecessor-record-id must remain {PREDECESSOR_RECORD_ID}")
        if args.preflight:
            print(json.dumps(validate_static_preflight(), sort_keys=True))
            return 0

        source_manifest = load_source_manifest()
        html_manifest, html_qa = validate_html()
        pdf_qa, pages = validate_pdf()
        source_payload = source_entries(source_manifest)
        html_payload = html_entries(html_manifest, html_qa)

        if args.check_only:
            source_inventory = validate_entry_set(source_payload)
            html_inventory = validate_entry_set(html_payload)
            print(
                json.dumps(
                    {
                        "status": "pass",
                        "check_only": True,
                        "complete_edition": True,
                        "chapters": "20/20",
                        "completion_modules": "8/8",
                        "pdf_pages": pages,
                        "html_entries": html_inventory["entry_count"],
                        "source_entries": source_inventory["entry_count"],
                    },
                    sort_keys=True,
                )
            )
            return 0

        require(isinstance(args.version, str) and args.version.strip(), "--version is required for package assembly")
        assert_public_text("release version", args.version)
        output = args.output_dir.resolve()
        output.relative_to(ROOT.resolve())
        output.mkdir(parents=True, exist_ok=True)
        expected_names = {
            PDF_NAME, HTML_NAME, SOURCE_NAME, LICENSES_NAME,
            COMPANION_RIGHTS_NAME, MANIFEST_NAME, CHECKSUMS_NAME,
        }
        unexpected = sorted(path.name for path in output.iterdir() if path.name not in expected_names)
        require(not unexpected, f"unexpected existing package output(s): {unexpected}")

        pdf_target = output / PDF_NAME
        licenses_target = output / LICENSES_NAME
        rights_target = output / COMPANION_RIGHTS_NAME
        shutil.copyfile(PDF, pdf_target)
        shutil.copyfile(ROOT / "LICENSES.md", licenses_target)
        shutil.copyfile(ROOT / "companion/RIGHTS.md", rights_target)
        assert_pdf_payload_privacy(pdf_target.name, pdf_target.read_bytes())
        assert_sanitized(licenses_target.name, licenses_target.read_bytes())
        assert_sanitized(rights_target.name, rights_target.read_bytes())

        html_zip = deterministic_zip(output / HTML_NAME, html_payload)
        source_zip = deterministic_zip(output / SOURCE_NAME, source_payload)
        file_rows = [
            {"path": PDF_NAME, **identity(pdf_target), "role": f"complete {pages}-page Indonesian reader PDF"},
            {**html_zip, "role": "finalized offline complete HTML reader plus component-rights notes"},
            {**source_zip, "role": "compact editable complete reader source, modular backend, essential build/QA code, rights, and public controls"},
            {"path": LICENSES_NAME, **identity(licenses_target), "role": "collection component-rights map"},
            {"path": COMPANION_RIGHTS_NAME, **identity(rights_target), "role": "original companion/completion rights and attribution"},
        ]
        package_manifest = {
            "schema_version": 1,
            "status": "pass",
            "partial": False,
            "boundary_complete": True,
            "boundary": BOUNDARY,
            "record": {
                "concept_doi": args.concept_doi,
                "predecessor_record_id": args.predecessor_record_id,
                "publication_target": "new version of the existing concept lineage",
                "title": "Topologi: Pendekatan Berbasis Inkuiri",
                "version": args.version,
                "language": "ind",
                "completion": {
                    "chapters_verified": 20,
                    "chapters_total": 20,
                    "completion_modules_verified": 8,
                    "completion_modules_total": 8,
                    "complete_edition": True,
                },
            },
            "authority": source_manifest["authority"],
            "reader": {
                "pdf": {"path": PDF.relative_to(ROOT).as_posix(), **identity(PDF), "pages": pages},
                "pdf_qa": {"path": PDF_QA.relative_to(ROOT).as_posix(), **identity(PDF_QA)},
                "html": {
                    "path": HTML_ROOT.relative_to(ROOT).as_posix(),
                    "files": html_manifest["file_count"],
                    "html_files": html_manifest["html_files"],
                    "bytes": html_manifest["total_bytes"],
                    "canonical_manifest_sha256": html_manifest["canonical_manifest_sha256"],
                },
                "html_qa": {"path": HTML_QA.relative_to(ROOT).as_posix(), **identity(HTML_QA)},
                "html_vendor_manifest": {"path": HTML_VENDOR_MANIFEST.relative_to(ROOT).as_posix(), **identity(HTML_VENDOR_MANIFEST)},
                "source_backend_manifest": {"path": SOURCE_MANIFEST.relative_to(ROOT).as_posix(), **identity(SOURCE_MANIFEST)},
            },
            "pedagogical_closure": {
                "chapter_companions": 20,
                "chapter20_source_supports": 56,
                "chapter20_mastery_entries": 8,
                "chapter20_staged_surfaces": 256,
                "completion_modules": 8,
                "completion_mastery_exercises": 56,
                "completion_staged_surfaces": 224,
            },
            "rights": [
                {"component": "translated GVSU instructional spine", "license": "CC BY-NC-SA 3.0", "url": "https://creativecommons.org/licenses/by-nc-sa/3.0/", "basis": "conservative determination because upstream metadata conflicts"},
                {"component": "original self-study companions and O003 completion Modules 1--8", "license": "CC BY 4.0", "url": "https://creativecommons.org/licenses/by/4.0/"},
                {"component": "software, XSLT, fonts, figures, and separately noticed assets", "license": "component notices retained"},
            ],
            "collection_policy": "per-component rights; no flattened license",
            "non_endorsement": True,
            "production_provenance": {
                "tool": MODEL,
                "direction": "the user",
                "scope": "translation drafting, original companion/completion, modular backend, and edition QA",
                "credit_note": "This provenance does not replace source-author, institutional, or human-contributor credits.",
            },
            "accessibility": {
                "primary_surface": "localized finalized HTML",
                "pdf_tagged": bool(pdf_qa.get("structure", {}).get("tagged")),
                "pdf_caveat": "The PDF may remain untagged; the localized HTML reader is the primary accessible surface.",
            },
            "files": file_rows,
            "checksums": {
                "path": CHECKSUMS_NAME,
                "scope": "all five payload files plus this package manifest; checksum file excludes itself",
                "algorithm": "SHA-256",
            },
            "package_validation": {
                "complete_edition": True,
                "chapters": "20/20",
                "completion_modules": "8/8",
                "source_inventory_identity_validation": "pass",
                "html_final_manifest_identity_validation": "pass",
                "pdf_deterministic_visual_structure_qa": "pass",
                "zip_crc_test": "pass",
                "zip_inventory": "pass",
                "zip_deterministic_double_build": "pass",
                "textual_privacy_scan": "pass",
                "binary_credential_marker_scan": "pass",
                "pdf_metadata_and_xmp_privacy_scan": "pass",
                "raw_build_logs_included": False,
                "historical_partial_package_used": False,
                "authority_archive_publicly_included": False,
            },
        }
        manifest_target = output / MANIFEST_NAME
        manifest_payload = json_bytes(package_manifest)
        assert_sanitized(MANIFEST_NAME, manifest_payload)
        manifest_target.write_bytes(manifest_payload)
        require(manifest_target.read_bytes() == manifest_payload, "package manifest readback failed")

        checksum_paths = sorted(
            (pdf_target, output / HTML_NAME, output / SOURCE_NAME, licenses_target, rights_target, manifest_target),
            key=lambda path: path.name.casefold(),
        )
        checksum_payload = "".join(
            f"{identity(path)['sha256']}  {path.name}\n" for path in checksum_paths
        ).encode("utf-8")
        assert_sanitized(CHECKSUMS_NAME, checksum_payload)
        checksums_target = output / CHECKSUMS_NAME
        checksums_target.write_bytes(checksum_payload)
        require(checksums_target.read_bytes() == checksum_payload, "checksum readback failed")

        actual_names = {path.name for path in output.iterdir() if path.is_file()}
        require(actual_names == expected_names, f"final package output set differs: {sorted(actual_names)}")
        print(
            json.dumps(
                {
                    "status": "pass",
                    "complete_edition": True,
                    "output_directory": output.relative_to(ROOT).as_posix(),
                    "files": [
                        *file_rows,
                        {"path": MANIFEST_NAME, **identity(manifest_target), "role": "complete-edition package manifest"},
                        {"path": CHECKSUMS_NAME, **identity(checksums_target), "role": "SHA-256 checksums for payloads and package manifest"},
                    ],
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    except (FileNotFoundError, RuntimeError, json.JSONDecodeError, ValueError) as exc:
        raise SystemExit(f"complete-edition package admission gate failed: {exc}") from exc


if __name__ == "__main__":
    raise SystemExit(main())
