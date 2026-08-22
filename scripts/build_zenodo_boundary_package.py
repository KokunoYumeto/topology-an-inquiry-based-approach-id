#!/usr/bin/env python3
"""Build the deterministic, sanitized Chapters 1–8 Zenodo preservation set."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
FIXED_ZIP_TIME = (2023, 8, 15, 0, 0, 0)
BASE = "topologi-pendekatan-berbasis-inkuiri-bab-01-08"
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
PDF = ROOT / "output" / "chapters01-08-pdf" / "chapters_01_08_reader.pdf"
HTML_ROOT = ROOT / "output" / "chapters01-08-html"
SOURCE_MANIFEST = ROOT / "qa" / "CHAPTER08_SOURCE_MANIFEST.json"
HTML_MANIFEST = ROOT / "qa" / "CHAPTER08_HTML_MANIFEST.json"

EXPECTED = {
    "authority_archive": {
        "bytes": 2_200_204,
        "sha256": "d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3",
    },
    "pdf": {
        "bytes": 1_653_047,
        "sha256": "78c076c58839dfd1a18cca663e58accdee2a391e429d5f38e6c71ac3c3e7937d",
        "pages": 187,
    },
    "html": {
        "files": 6_172,
        "bytes": 15_657_116,
        "canonical_manifest_sha256": "5877bcaf7c08baf2d56e58a36fe9097af3b902f2315f86e667f82dd3118dbdab",
    },
    "source_manifest_sha256": "TO_BE_VALIDATED_AT_BUILD_TIME",
}

SANITIZED_QA = (
    *(f"qa/CHAPTER{number:02d}_SOURCE_MANIFEST.json" for number in range(1, 9)),
    "qa/CHAPTER08_SOURCE_QA.json",
    "qa/CHAPTER08_COMPANION_QA.json",
    "qa/CHAPTER08_HTML_MANIFEST.json",
    "qa/CHAPTER08_HTML_MANIFEST_RUN1.json",
    "qa/CHAPTER08_HTML_MANIFEST_RUN2.json",
    "qa/CHAPTER08_HTML_QA.json",
    "qa/CHAPTER08_BROWSER_QA.json",
    "qa/CHAPTER08_PDF_RUN1_HASH.json",
    "qa/CHAPTER08_PDF_RUN2_HASH.json",
    "qa/CHAPTER08_PDF_STRUCTURE.json",
    "qa/CHAPTER08_PDF_VISUAL_QA.json",
    "qa/CHAPTER08_PDF_RENDER_MANIFEST.json",
    "qa/CHAPTER08_PDF_CONTACT_SHEET_MANIFEST.json",
    "qa/CHAPTER08_BUILD_QA.md",
)

BROWSER_EVIDENCE = (
    "qa/browser-evidence/CHAPTER08_DESKTOP_1280x900.jpg",
    "qa/browser-evidence/CHAPTER08_DISCLOSURE_1280x900.jpg",
    "qa/browser-evidence/CHAPTER08_INTERIOR_MACRO_1280x900.jpg",
    "qa/browser-evidence/CHAPTER08_MOBILE_390x844_DRAWER.jpg",
)

SENSITIVE_TEXT_MARKERS = (
    b"C:\\Users\\Floris",
    b"New " b"zenodo token",
    b"Github " b"Tokens",
    b"Authorization:" b" Bearer",
    b"access_" b"token=",
)


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


def safe_archive_name(raw: str) -> str:
    name = PurePosixPath(raw)
    if name.is_absolute() or ".." in name.parts or not name.parts:
        raise RuntimeError(f"unsafe archive path: {raw!r}")
    return name.as_posix()


def assert_sanitized(name: str, data: bytes) -> None:
    lowered = name.casefold()
    if lowered.endswith((".log", ".tmp", ".pyc")) or "__pycache__" in lowered:
        raise RuntimeError(f"disallowed archive entry: {name}")
    if Path(name).suffix.casefold() in {
        ".md",
        ".txt",
        ".json",
        ".csv",
        ".ptx",
        ".py",
        ".xsl",
        ".xml",
        ".css",
        ".html",
    }:
        for marker in SENSITIVE_TEXT_MARKERS:
            if marker.lower() in data.lower():
                raise RuntimeError(f"sensitive/local marker in {name}: {marker!r}")


def file_entry(archive_name: str, path: Path) -> tuple[str, bytes]:
    if not path.is_file():
        raise FileNotFoundError(path)
    name = safe_archive_name(archive_name)
    data = path.read_bytes()
    assert_sanitized(name, data)
    return name, data


def add_tree(
    entries: dict[str, bytes], archive_prefix: str, root: Path, *, suffixes: set[str] | None = None
) -> None:
    if not root.is_dir():
        raise FileNotFoundError(root)
    for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.as_posix().casefold()):
        if "__pycache__" in path.parts or path.suffix.casefold() == ".pyc":
            continue
        if suffixes is not None and path.suffix.casefold() not in suffixes:
            continue
        relative = path.relative_to(root).as_posix()
        name, data = file_entry(f"{archive_prefix}/{relative}", path)
        if name in entries:
            raise RuntimeError(f"duplicate archive entry: {name}")
        entries[name] = data


def collect_paths(value: object) -> set[str]:
    paths: set[str] = set()
    if isinstance(value, dict):
        candidate = value.get("path")
        if isinstance(candidate, str):
            paths.add(candidate)
        for item in value.values():
            paths.update(collect_paths(item))
    elif isinstance(value, list):
        for item in value:
            paths.update(collect_paths(item))
    return paths


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


def html_entries(html_manifest: dict[str, object]) -> dict[str, bytes]:
    files = html_manifest.get("files")
    if not isinstance(files, list):
        raise RuntimeError("HTML manifest has no file list")
    if len(files) != EXPECTED["html"]["files"]:
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
    if total != EXPECTED["html"]["bytes"]:
        raise RuntimeError(f"HTML byte count changed: {total}")
    for name, path in (
        ("README.md", ROOT / "README.md"),
        ("LICENSES.md", ROOT / "LICENSES.md"),
        ("COMPANION_RIGHTS.md", ROOT / "companion" / "RIGHTS.md"),
        ("CHAPTER08_HTML_MANIFEST.json", HTML_MANIFEST),
    ):
        archive_name, data = file_entry(name, path)
        entries[archive_name] = data
    return entries


def source_entries(source_manifest: dict[str, object]) -> dict[str, bytes]:
    entries: dict[str, bytes] = {}

    def add(name: str, path: Path) -> None:
        archive_name, data = file_entry(name, path)
        if archive_name in entries:
            if entries[archive_name] != data:
                raise RuntimeError(f"conflicting duplicate entry: {archive_name}")
            return
        entries[archive_name] = data

    prefix = "point-set-topology-id"
    for relative in (
        "README.md",
        "LICENSES.md",
        "project.ptx",
        "requirements.txt",
        "publication/publication.ptx",
        "00_control/TERMINOLOGY.csv",
        "00_control/SOURCE_CORRECTIONS.csv",
    ):
        if relative.startswith("00_control/"):
            path = LANE / relative
            archive_name = f"{prefix}/{relative}"
        else:
            path = ROOT / relative
            archive_name = f"{prefix}/repo/{relative}"
        add(archive_name, path)

    add(
        f"{prefix}/authority/archives/{AUTHORITY_ARCHIVE.name}",
        AUTHORITY_ARCHIVE,
    )

    for manifest_path in sorted(collect_paths(source_manifest), key=str.casefold):
        if not manifest_path.startswith("repo/source/"):
            continue
        relative = manifest_path.removeprefix("repo/")
        add(f"{prefix}/repo/{relative}", ROOT / relative)

    for directory in ("companion", "backend", "assets", "xsl"):
        tree_entries: dict[str, bytes] = {}
        add_tree(tree_entries, f"{prefix}/repo/{directory}", ROOT / directory)
        for name, data in tree_entries.items():
            add_name = safe_archive_name(name)
            if add_name in entries and entries[add_name] != data:
                raise RuntimeError(f"conflicting tree entry: {add_name}")
            entries[add_name] = data

    scripts: dict[str, bytes] = {}
    add_tree(
        scripts,
        f"{prefix}/repo/scripts",
        ROOT / "scripts",
        suffixes={".py"},
    )
    entries.update(scripts)

    for relative in (*SANITIZED_QA, *BROWSER_EVIDENCE):
        add(f"{prefix}/repo/{relative}", ROOT / relative)

    return entries


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "output" / "zenodo-chapters01-08",
    )
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)

    require_identity(AUTHORITY_ARCHIVE, EXPECTED["authority_archive"], "authority archive")
    require_identity(PDF, EXPECTED["pdf"], "PDF")
    source_manifest = read_json(SOURCE_MANIFEST)
    html_manifest = read_json(HTML_MANIFEST)
    if source_manifest.get("status") != "pass":
        raise RuntimeError("source manifest is not passing")
    if html_manifest.get("canonical_manifest_sha256") != EXPECTED["html"]["canonical_manifest_sha256"]:
        raise RuntimeError("HTML canonical identity changed")

    pdf_target = output / PDF_NAME
    shutil.copyfile(PDF, pdf_target)
    licenses_target = output / LICENSES_NAME
    companion_target = output / COMPANION_RIGHTS_NAME
    shutil.copyfile(ROOT / "LICENSES.md", licenses_target)
    shutil.copyfile(ROOT / "companion" / "RIGHTS.md", companion_target)

    html_zip = deterministic_zip(output / HTML_NAME, html_entries(html_manifest))
    source_zip = deterministic_zip(output / SOURCE_NAME, source_entries(source_manifest))

    file_rows = [
        {"path": PDF_NAME, **identity(pdf_target), "role": "187-page Indonesian reader PDF"},
        {**html_zip, "role": "cumulative HTML reader and rights notes"},
        {**source_zip, "role": "editable PreTeXt, companions, backend, build code, authority archive, and sanitized QA"},
        {"path": LICENSES_NAME, **identity(licenses_target), "role": "collection component-rights map"},
        {"path": COMPANION_RIGHTS_NAME, **identity(companion_target), "role": "original companion rights and attribution"},
    ]
    package_manifest = {
        "schema_version": 1,
        "status": "pass",
        "record": {
            "id": 22059895,
            "doi": "10.5281/zenodo.22059895",
            "title": "Topologi: Pendekatan Berbasis Inkuiri",
            "version": "2026.08.22-bab01-08",
            "language": "ind",
            "completion": {"chapters_verified": 8, "chapters_total": 20, "complete": False},
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
            "pdf": {"pages": 187, **identity(PDF)},
            "html": {
                "files": EXPECTED["html"]["files"],
                "bytes": EXPECTED["html"]["bytes"],
                "canonical_manifest_sha256": EXPECTED["html"]["canonical_manifest_sha256"],
            },
            "source_files_translated": 51,
            "source_manifest": {"path": "qa/CHAPTER08_SOURCE_MANIFEST.json", **identity(SOURCE_MANIFEST)},
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
            "This is a verified 8-of-20 maintenance boundary, not the complete edition.",
            "HTML is the primary accessible surface; the PDF is untagged and some mathematical fonts have incomplete Unicode maps.",
            "The cumulative HTML reader retains nine remote runtime host families; full offline closure remains a complete-edition gate.",
            "Whole-book figure-provenance closure remains unfinished beyond this bounded release.",
            "The dedicated GitHub mirror remains at Chapters 1–5 while account suspension prevents the Chapters 1–8 push.",
        ],
        "files": file_rows,
        "package_validation": {
            "zip_crc_test": "pass",
            "zip_inventory": "pass",
            "zip_deterministic_double_build": "pass",
            "absolute_or_credential_markers": "none in selected textual entries",
            "raw_build_logs_included": False,
        },
    }
    manifest_target = output / MANIFEST_NAME
    manifest_target.write_text(
        json.dumps(package_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    result = {
        "status": "pass",
        "output": output.as_posix(),
        "files": [*file_rows, {"path": MANIFEST_NAME, **identity(manifest_target), "role": "package manifest"}],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
