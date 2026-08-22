#!/usr/bin/env python3
"""Build the deterministic, sanitized Chapters 1–10 Zenodo preservation set."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
import zipfile

try:
    from PyPDF2 import PdfReader
except ModuleNotFoundError:  # Bundled runtime uses the maintained package name.
    from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
FIXED_ZIP_TIME = (2023, 8, 15, 0, 0, 0)
BASE = "topologi-pendekatan-berbasis-inkuiri-bab-01-10"
PDF_NAME = f"{BASE}-id.pdf"
HTML_NAME = f"{BASE}-html.zip"
SOURCE_NAME = f"{BASE}-sumber.zip"
LICENSES_NAME = f"{BASE}-licenses.md"
COMPANION_RIGHTS_NAME = f"{BASE}-rights-companion.md"
MANIFEST_NAME = f"{BASE}-manifest.json"

AUTHORITY_ARCHIVE = (
    LANE
    / "authority"
    / "archives"
    / "gvsuoer-topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9.zip"
)
PDF = ROOT / "output" / "chapters01-10-pdf" / "chapters_01_10_reader.pdf"
HTML_ROOT = ROOT / "output" / "chapters01-10-html"
SOURCE_MANIFEST = ROOT / "qa" / "CHAPTER10_SOURCE_MANIFEST.json"
HTML_MANIFEST = ROOT / "qa" / "CHAPTER10_HTML_MANIFEST.json"

EXPECTED_AUTHORITY_ARCHIVE = {
    "bytes": 2_200_204,
    "sha256": "d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3",
}
REQUIRED_CONTROL_AUDIT = "00_control/CHAPTER09_TERMINOLOGY_AUDIT.md"
FORBIDDEN_CONTROL_AUDIT = "00_control/CHAPTER10_TERMINOLOGY_AUDIT.md"
REQUIRED_EVIDENCE_PATHS = {
    "repo/qa/CHAPTER10_BROWSER_QA.json",
    "repo/qa/CHAPTER10_PDF_RUN1_HASH.json",
    "repo/qa/CHAPTER10_PDF_RUN2_HASH.json",
    "repo/qa/CHAPTER10_PDF_STRUCTURE.json",
    "repo/qa/CHAPTER10_PDF_VISUAL_QA.json",
    "repo/qa/CHAPTER10_DOCS_MANIFEST.json",
    "repo/qa/CHAPTER10_DOCS_QA.json",
    "repo/qa/CHAPTER10_BUILD_QA.md",
    "repo/qa/CHAPTER09_GITHUB_PUBLICATION_RECEIPT.md",
    "repo/qa/CHAPTER09_ZENODO_PUBLICATION_RECEIPT.md",
    "repo/qa/CHAPTER09_FIGSHARE_PUBLICATION_RECEIPT.md",
}

PRIVATE_NAME_MARKER = bytes((70, 108, 111, 114, 105, 115))
TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".csv", ".ptx", ".py", ".xsl",
    ".xml", ".css", ".html",
}
ABSOLUTE_PATH_PATTERNS = (
    re.compile(r"(?i)(?<![A-Za-z0-9])[A-Za-z]:[\\/](?:Users|Documents and Settings|ProgramData|Windows|home|tmp|temp)[\\/]"),
    re.compile(r"(?i)\\\\[^\\\s]+[\\/](?:Users|home|[A-Za-z]\$)[\\/]"),
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
SENSITIVE_PATH_LABELS = ("new " "zenodo token", "github " "tokens")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def identity(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": digest(data)}


def require_identity(path: Path, expected: dict[str, object], label: str) -> None:
    actual = identity(path)
    if actual != {"bytes": expected["bytes"], "sha256": expected["sha256"]}:
        raise RuntimeError(f"{label} identity changed: {actual}")


def read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return value


def require_dict(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} must be an object")
    return value


def require_positive_int(value: object, label: str) -> int:
    if not isinstance(value, int) or value <= 0:
        raise RuntimeError(f"{label} must be a positive integer")
    return value


def require_sha256(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise RuntimeError(f"{label} must be a lowercase SHA-256 digest")
    return value


def safe_archive_name(raw: str) -> str:
    name = PurePosixPath(raw)
    if name.is_absolute() or ".." in name.parts or not name.parts:
        raise RuntimeError(f"unsafe archive path: {raw!r}")
    return name.as_posix()


def assert_public_text(name: str, text: str) -> None:
    if PRIVATE_NAME_MARKER.decode("ascii").casefold() in text.casefold():
        raise RuntimeError(f"private-name marker in {name}")
    for pattern in ABSOLUTE_PATH_PATTERNS:
        if pattern.search(text):
            raise RuntimeError(f"absolute/local path marker in {name}")
    lowered = text.casefold()
    if any(label in lowered for label in SENSITIVE_PATH_LABELS):
        raise RuntimeError(f"sensitive credential-file label in {name}")
    for pattern in CREDENTIAL_PATTERNS:
        if pattern.search(text):
            raise RuntimeError(f"credential-like value in {name}")


def assert_sanitized(name: str, data: bytes) -> None:
    lowered = name.casefold()
    if lowered.endswith((".log", ".tmp", ".pyc")) or "__pycache__" in lowered:
        raise RuntimeError(f"disallowed archive entry: {name}")
    if PRIVATE_NAME_MARKER.lower() in data.lower():
        raise RuntimeError(f"private-name marker in {name}")
    for pattern in BINARY_CREDENTIAL_PATTERNS:
        if pattern.search(data):
            raise RuntimeError(f"credential-like byte sequence in {name}")
    if Path(name).suffix.casefold() in TEXT_EXTENSIONS:
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise RuntimeError(f"selected textual entry is not UTF-8: {name}") from exc
        assert_public_text(name, text)


def assert_pdf_privacy(path: Path) -> PdfReader:
    data = path.read_bytes()
    assert_sanitized(path.name, data)
    reader = PdfReader(str(path))
    metadata = reader.metadata
    if metadata is not None:
        assert_public_text(f"{path.name} metadata", "\n".join(str(value) for value in metadata.values()))
    root = reader.trailer.get("/Root")
    if root is not None:
        try:
            root_object = root.get_object()
            metadata_stream = root_object.get("/Metadata")
            if metadata_stream is not None:
                xmp_data = metadata_stream.get_object().get_data()
                if xmp_data.startswith((b"\xff\xfe", b"\xfe\xff")):
                    xmp = xmp_data.decode("utf-16")
                elif b"\x00" in xmp_data[:128]:
                    encoding = "utf-16-be" if xmp_data[:1] == b"\x00" else "utf-16-le"
                    xmp = xmp_data.decode(encoding)
                else:
                    xmp = xmp_data.decode("utf-8-sig")
                assert_public_text(f"{path.name} XMP", xmp)
        except (AttributeError, KeyError, TypeError, UnicodeDecodeError, ValueError) as exc:
            raise RuntimeError(f"unable to inspect PDF XMP privacy metadata: {path.name}") from exc
    return reader


def file_entry(archive_name: str, path: Path) -> tuple[str, bytes]:
    if not path.is_file():
        raise FileNotFoundError(path)
    name = safe_archive_name(archive_name)
    data = path.read_bytes()
    assert_sanitized(name, data)
    return name, data


def canonical_entries(entries: dict[str, bytes]) -> str:
    hasher = hashlib.sha256()
    for name in sorted(entries, key=str.casefold):
        hasher.update(name.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(entries[name])
    return hasher.hexdigest()


def write_zip(path: Path, entries: dict[str, bytes]) -> dict[str, object]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", allowZip64=True) as archive:
        for name in sorted(entries, key=str.casefold):
            info = zipfile.ZipInfo(filename=name, date_time=FIXED_ZIP_TIME)
            info.create_system = 3
            info.external_attr = (0o100644 & 0xFFFF) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            info.flag_bits |= 0x800
            archive.writestr(info, entries[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(path, "r") as archive:
        if archive.testzip() is not None:
            raise RuntimeError(f"ZIP CRC verification failed: {path}")
        names = archive.namelist()
        if names != sorted(entries, key=str.casefold):
            raise RuntimeError(f"ZIP inventory/order differs: {path}")
        if len(names) != len(set(names)):
            raise RuntimeError(f"duplicate ZIP member: {path}")
        if sum(row.file_size for row in archive.infolist()) != sum(map(len, entries.values())):
            raise RuntimeError(f"ZIP uncompressed-byte census differs: {path}")
    return {
        "path": path.name,
        **identity(path),
        "entry_count": len(entries),
        "uncompressed_bytes": sum(map(len, entries.values())),
        "canonical_entry_sha256": canonical_entries(entries),
    }


def deterministic_zip(path: Path, entries: dict[str, bytes]) -> dict[str, object]:
    first = write_zip(path, entries)
    with tempfile.TemporaryDirectory(prefix="o003-zenodo-verify-") as temp:
        second_path = Path(temp) / path.name
        second = write_zip(second_path, entries)
        for key in ("bytes", "sha256", "entry_count", "uncompressed_bytes", "canonical_entry_sha256"):
            if first[key] != second[key]:
                raise RuntimeError(f"non-deterministic ZIP {path.name}: {key}")
    first["deterministic_double_build"] = True
    return first


def html_entries(
    html_manifest: dict[str, object], expected_html: dict[str, object]
) -> dict[str, bytes]:
    files = html_manifest.get("files")
    if not isinstance(files, list):
        raise RuntimeError("HTML manifest has no file list")
    if len(files) != expected_html["files"]:
        raise RuntimeError("HTML manifest file count changed")
    entries: dict[str, bytes] = {}
    total = 0
    for row in files:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            raise RuntimeError("malformed HTML manifest row")
        leaf = PurePosixPath(row["path"])
        if leaf.is_absolute() or ".." in leaf.parts or not leaf.parts:
            raise RuntimeError(f"HTML manifest path escaped target: {leaf}")
        path = HTML_ROOT.joinpath(*leaf.parts)
        data = path.read_bytes()
        if len(data) != row.get("bytes") or digest(data) != row.get("sha256"):
            raise RuntimeError(f"HTML file differs from manifest: {leaf}")
        name = safe_archive_name(f"reader/{leaf.as_posix()}")
        assert_sanitized(name, data)
        entries[name] = data
        total += len(data)
    if total != expected_html["bytes"]:
        raise RuntimeError(f"HTML byte count changed: {total}")
    for name, path in (
        ("README.md", ROOT / "README.md"),
        ("LICENSES.md", ROOT / "LICENSES.md"),
        ("COMPANION_RIGHTS.md", ROOT / "companion" / "RIGHTS.md"),
        ("CHAPTER10_HTML_MANIFEST.json", HTML_MANIFEST),
    ):
        archive_name, data = file_entry(name, path)
        entries[archive_name] = data
    return entries


def source_entries(source_manifest: dict[str, object]) -> dict[str, bytes]:
    entries: dict[str, bytes] = {}
    prefix = "point-set-topology-id"
    raw_inventory = source_manifest.get("package_source_inventory")
    if not isinstance(raw_inventory, list) or not raw_inventory:
        raise RuntimeError("source manifest has no package-source inventory")
    inventory: dict[str, dict[str, object]] = {}
    for raw in raw_inventory:
        row = require_dict(raw, "package-source inventory row")
        path_value = row.get("path")
        if not isinstance(path_value, str):
            raise RuntimeError("package-source inventory row has no path")
        posix = PurePosixPath(path_value)
        if posix.is_absolute() or ".." in posix.parts or "\\" in path_value:
            raise RuntimeError(f"unsafe package-source inventory path: {path_value!r}")
        if path_value in inventory:
            raise RuntimeError(f"duplicate package-source inventory path: {path_value}")
        inventory[path_value] = row

    required_inventory = {REQUIRED_CONTROL_AUDIT, *REQUIRED_EVIDENCE_PATHS}
    if not required_inventory.issubset(inventory):
        raise RuntimeError(
            f"package-source inventory omits required evidence: "
            f"{sorted(required_inventory - set(inventory))}"
        )
    if FORBIDDEN_CONTROL_AUDIT in inventory:
        raise RuntimeError("package-source inventory uses the nonexistent Chapter 10 terminology audit")

    reader_artifacts = require_dict(source_manifest.get("reader_artifacts"), "reader artifacts")
    html_artifact = require_dict(reader_artifacts.get("html"), "HTML reader artifact")
    browser_qa = require_dict(html_artifact.get("browser_qa"), "browser QA admission")
    browser_evidence = browser_qa.get("evidence")
    if not isinstance(browser_evidence, list):
        raise RuntimeError("browser QA admission has no evidence array")
    for raw in browser_evidence:
        evidence = require_dict(raw, "browser evidence row")
        evidence_path = evidence.get("path")
        if not isinstance(evidence_path, str) or evidence_path not in inventory:
            raise RuntimeError(f"validated browser evidence is not packaged: {evidence_path!r}")
        inventory_row = inventory[evidence_path]
        if (
            inventory_row.get("bytes") != evidence.get("bytes")
            or inventory_row.get("sha256") != evidence.get("sha256")
        ):
            raise RuntimeError(f"browser evidence inventory identity differs: {evidence_path}")

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
            actual_scoped.add(f"repo/{path.relative_to(ROOT).as_posix()}")
    if actual_scoped != declared_scoped:
        missing = sorted(declared_scoped - actual_scoped)[:10]
        undeclared = sorted(actual_scoped - declared_scoped)[:10]
        raise RuntimeError(
            f"package source-tree drift: missing={missing}, undeclared={undeclared}"
        )

    for manifest_path in sorted(inventory, key=str.casefold):
        row = inventory[manifest_path]
        if manifest_path.startswith("repo/"):
            relative = manifest_path.removeprefix("repo/")
            disk_path = ROOT.joinpath(*PurePosixPath(relative).parts)
        elif manifest_path.startswith("00_control/"):
            disk_path = LANE.joinpath(*PurePosixPath(manifest_path).parts)
        else:
            raise RuntimeError(f"unsupported package-source inventory path: {manifest_path}")
        expected = {
            "bytes": require_positive_int(row.get("bytes"), f"{manifest_path} bytes"),
            "sha256": require_sha256(row.get("sha256"), f"{manifest_path} SHA-256"),
        }
        require_identity(disk_path, expected, manifest_path)
        archive_name, data = file_entry(f"{prefix}/{manifest_path}", disk_path)
        entries[archive_name] = data

    archive_row = require_dict(
        source_manifest.get("package_authority_archive"), "package authority archive"
    )
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
    archive_name, data = file_entry(f"{prefix}/{expected_archive_path}", AUTHORITY_ARCHIVE)
    entries[archive_name] = data

    current_manifest_name = f"{prefix}/repo/qa/CHAPTER10_SOURCE_MANIFEST.json"
    archive_name, data = file_entry(current_manifest_name, SOURCE_MANIFEST)
    if archive_name in entries:
        raise RuntimeError("source manifest must not self-declare an impossible identity")
    entries[archive_name] = data

    return entries


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "output" / "zenodo-chapters01-10",
    )
    parser.add_argument(
        "--version",
        default="2026.08.23-bab01-10",
        help="release version label recorded in the package manifest",
    )
    parser.add_argument(
        "--predecessor-record-id",
        type=int,
        default=22_062_508,
        help="published Chapters 1-9 Zenodo record in the existing concept lineage",
    )
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)

    expected_output_names = {
        PDF_NAME,
        HTML_NAME,
        SOURCE_NAME,
        LICENSES_NAME,
        COMPANION_RIGHTS_NAME,
        MANIFEST_NAME,
    }
    unexpected = sorted(
        path.name for path in output.iterdir() if path.name not in expected_output_names
    )
    if unexpected:
        raise RuntimeError(f"unexpected existing package output(s): {unexpected}")

    require_identity(AUTHORITY_ARCHIVE, EXPECTED_AUTHORITY_ARCHIVE, "authority archive")
    source_manifest = read_json(SOURCE_MANIFEST)
    if source_manifest.get("status") != "pass":
        raise RuntimeError("source manifest is not passing")
    if source_manifest.get("pending_evidence") != []:
        raise RuntimeError("source manifest still records pending evidence")
    if (
        source_manifest.get("boundary")
        != "chapters_01_10_with_separately_licensed_self_study_companions"
    ):
        raise RuntimeError("source manifest has the wrong cumulative boundary")
    reader_artifacts = require_dict(
        source_manifest.get("reader_artifacts"), "source-manifest reader artifacts"
    )
    expected_pdf = require_dict(reader_artifacts.get("pdf"), "admitted PDF")
    if expected_pdf.get("status") != "pass":
        raise RuntimeError("source manifest has not admitted the Chapter 10 PDF")
    if expected_pdf.get("path") != f"repo/{PDF.relative_to(ROOT).as_posix()}":
        raise RuntimeError("source manifest points to a different PDF")
    expected_pdf_identity = {
        "bytes": require_positive_int(expected_pdf.get("bytes"), "admitted PDF bytes"),
        "sha256": require_sha256(expected_pdf.get("sha256"), "admitted PDF SHA-256"),
    }
    expected_pdf_pages = require_positive_int(
        expected_pdf.get("pages"), "admitted PDF page count"
    )
    require_identity(PDF, expected_pdf_identity, "PDF")
    pdf_reader = assert_pdf_privacy(PDF)
    if len(pdf_reader.pages) != expected_pdf_pages:
        raise RuntimeError("PDF page count changed")

    expected_html_row = require_dict(reader_artifacts.get("html"), "admitted HTML")
    if expected_html_row.get("status") != "deterministic_tree_pass":
        raise RuntimeError("source manifest has not admitted the deterministic HTML tree")
    expected_html = {
        "files": require_positive_int(expected_html_row.get("file_count"), "admitted HTML file count"),
        "bytes": require_positive_int(expected_html_row.get("bytes"), "admitted HTML bytes"),
        "canonical_manifest_sha256": require_sha256(
            expected_html_row.get("canonical_manifest_sha256"),
            "admitted HTML canonical SHA-256",
        ),
    }
    html_manifest = read_json(HTML_MANIFEST)
    if html_manifest.get("file_count") != expected_html["files"]:
        raise RuntimeError("HTML manifest file count differs from source-manifest admission")
    if html_manifest.get("total_bytes") != expected_html["bytes"]:
        raise RuntimeError("HTML manifest byte count differs from source-manifest admission")
    if html_manifest.get("canonical_manifest_sha256") != expected_html["canonical_manifest_sha256"]:
        raise RuntimeError("HTML canonical identity changed")

    pdf_target = output / PDF_NAME
    shutil.copyfile(PDF, pdf_target)
    licenses_target = output / LICENSES_NAME
    companion_target = output / COMPANION_RIGHTS_NAME
    _, licenses_data = file_entry(LICENSES_NAME, ROOT / "LICENSES.md")
    _, companion_data = file_entry(COMPANION_RIGHTS_NAME, ROOT / "companion" / "RIGHTS.md")
    licenses_target.write_bytes(licenses_data)
    companion_target.write_bytes(companion_data)

    html_zip = deterministic_zip(output / HTML_NAME, html_entries(html_manifest, expected_html))
    source_zip = deterministic_zip(output / SOURCE_NAME, source_entries(source_manifest))

    file_rows = [
        {
            "path": PDF_NAME,
            **identity(pdf_target),
            "role": f"{expected_pdf_pages}-page Indonesian reader PDF",
        },
        {**html_zip, "role": "cumulative HTML reader and rights notes"},
        {**source_zip, "role": "editable PreTeXt, companions, backend, build code, authority archive, and sanitized QA"},
        {"path": LICENSES_NAME, **identity(licenses_target), "role": "collection component-rights map"},
        {"path": COMPANION_RIGHTS_NAME, **identity(companion_target), "role": "original companion rights and attribution"},
    ]
    package_manifest = {
        "schema_version": 1,
        "status": "pass",
        "record": {
            "concept_doi": "10.5281/zenodo.22059894",
            "predecessor_record_id": args.predecessor_record_id,
            "publication_target": "new version of the existing concept lineage",
            "title": "Topologi: Pendekatan Berbasis Inkuiri",
            "version": args.version,
            "language": "ind",
            "completion": {"chapters_verified": 10, "chapters_total": 20, "complete": False},
        },
        "authority": {
            "work": "Topology: An Inquiry-Based Approach",
            "author": "Steven Schlicker",
            "institution": "Grand Valley State University",
            "commit": "0c2d8f614ef87aa00de373f3418146c2f1d13bb9",
            "tree": "7df245934eedb7174d5ff8af18afff5a7abdde78",
            "archive": {"path": AUTHORITY_ARCHIVE.name, **identity(AUTHORITY_ARCHIVE)},
        },
        "reader": {
            "pdf": {"pages": expected_pdf_pages, **identity(PDF)},
            "html": {
                "files": expected_html["files"],
                "bytes": expected_html["bytes"],
                "canonical_manifest_sha256": expected_html["canonical_manifest_sha256"],
            },
            "source_files_translated": 66,
            "source_manifest": {"path": "qa/CHAPTER10_SOURCE_MANIFEST.json", **identity(SOURCE_MANIFEST)},
        },
        "rights": [
            {
                "component": "translated GVSU instructional text",
                "license": "CC BY-NC-SA 3.0",
                "url": "https://creativecommons.org/licenses/by-nc-sa/3.0/",
                "basis": "conservative determination because upstream metadata conflicts",
            },
            {
                "component": "original self-study companions and epsilon-delta lab",
                "license": "CC BY 4.0",
                "url": "https://creativecommons.org/licenses/by/4.0/",
            },
            {
                "component": "software, XSLT, fonts, figures, and separately noticed assets",
                "license": "component notices retained",
            },
        ],
        "caveats": [
            "This is a verified 10-of-20 maintenance boundary, not the complete edition.",
            "HTML is the primary accessible surface; the PDF is untagged and some mathematical fonts have incomplete Unicode maps.",
            "The cumulative HTML reader retains remote runtime dependencies; full offline closure remains a complete-edition gate.",
            "Whole-book figure-provenance closure remains unfinished beyond this bounded release.",
        ],
        "production_provenance": {
            "tool": "OpenAI Codex gpt-5.6-sol, Ultra",
            "direction": "the user",
            "scope": "translation drafting, original companion, modular backend, and edition QA",
            "credit_note": "This provenance does not replace source-author, institutional, or human-contributor credits.",
        },
        "files": file_rows,
        "package_validation": {
            "zip_crc_test": "pass",
            "zip_inventory": "pass",
            "zip_deterministic_double_build": "pass",
            "textual_privacy_scan": "private-name, common absolute/local-path, and credential markers absent",
            "binary_credential_marker_scan": "pass",
            "pdf_metadata_and_xmp_privacy_scan": "pass",
            "raw_build_logs_included": False,
            "source_inventory_identity_validation": "pass",
        },
    }
    manifest_target = output / MANIFEST_NAME
    manifest_target.write_text(
        json.dumps(package_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    assert_sanitized(manifest_target.name, manifest_target.read_bytes())
    actual_output_names = {path.name for path in output.iterdir() if path.is_file()}
    if actual_output_names != expected_output_names:
        raise RuntimeError(
            f"final package output set differs: {sorted(actual_output_names)}"
        )
    result = {
        "status": "pass",
        "output_directory": output.name,
        "files": [*file_rows, {"path": MANIFEST_NAME, **identity(manifest_target), "role": "package manifest"}],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
