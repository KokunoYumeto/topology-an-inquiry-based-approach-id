#!/usr/bin/env python3
"""Build the fail-closed cumulative Chapters 1-11 source/artifact manifest.

The source, companion, backend, schema, deterministic reader artifacts,
browser/PDF evidence, documentation receipts, and build receipt are mandatory.
The manifest also freezes the exact portable source-package inventory used by
publication.  Run this only after every Chapter 11 evidence artifact exists.
"""

from __future__ import annotations

from collections import Counter
import csv
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

from qa_chapter11_companion import (
    EXPECTED_ACTIVITY_PROMPTS,
    EXPECTED_AUTHORITY_ORDERED_SHA256,
    EXPECTED_AUTHORITY_RAW_SHA256,
    EXPECTED_CORRECTION_IDS,
    EXPECTED_EXERCISE_PROMPTS,
    EXPECTED_GROUPING_TASKS,
    EXPECTED_MASTERY,
    EXPECTED_MATH_CHANGES,
    EXPECTED_SOURCE_PROMPTS,
    EXPECTED_TERM_IDS,
    FRAGMENTS,
    SOURCE_FILES,
)


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
OUTPUT = ROOT / "qa" / "CHAPTER11_SOURCE_MANIFEST.json"
AUTHORITY_SOURCE = (
    LANE
    / "authority/gvsu-pinned/topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9/source"
)
AUTHORITY_ARCHIVE = (
    LANE
    / "authority/archives/gvsuoer-topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9.zip"
)

PRIOR_MANIFEST = "qa/CHAPTER10_SOURCE_MANIFEST.json"
PRIOR_MANIFEST_IDENTITY = {
    "bytes": 112_906,
    "sha256": "a671ff075f5d8dc88770acfffa1ec8f4bc8fae134377121951210a824f866845",
}
PRIOR_CHAPTERS = tuple(f"chapter_{number:02d}" for number in range(1, 11))

COMPANION_WRAPPER = "companion/chapter_11_metric_subspaces_self_study.ptx"
COMPANION_FRAGMENTS = tuple(f"companion/{name}" for name in FRAGMENTS)
ALIAS_MAP = "backend/chapter_11_entry_aliases.csv"
BACKEND_MANIFEST = "backend/chapter_11_companion_manifest.json"
SOURCE_QA = "qa/CHAPTER11_SOURCE_QA.json"
COMPANION_QA = "qa/CHAPTER11_COMPANION_QA.json"
SCHEMA_QA = "qa/CHAPTER11_SCHEMA_QA.json"
READER_WRAPPER = "source/chapters_01_11_reader.ptx"
NEW_ADDITIVE = (
    COMPANION_WRAPPER,
    *COMPANION_FRAGMENTS,
    ALIAS_MAP,
    BACKEND_MANIFEST,
)

CHAPTER_11_IMPLEMENTATION = (
    "project.ptx",
    "scripts/qa_chapter11_companion.py",
    "scripts/build_chapter11_backend.py",
    "scripts/build_chapter11_source_manifest.py",
    "scripts/build_zenodo_chapter11_package.py",
    "scripts/qa_html_tree.py",
    READER_WRAPPER,
)
EVOLVING_PRIOR_IMPLEMENTATION = {
    "README.md": "advance the truthful cumulative reader boundary to Chapters 1-11",
    "LICENSES.md": "cumulative Chapter 11 collection-rights preservation",
    "assets/o003-readable-layout.css": "cumulative reader layout evolution",
    "companion/RIGHTS.md": "cumulative Chapter 11 companion rights preservation",
    "project.ptx": "addition of cumulative Chapters 1-11 build targets",
    "scripts/qa_source_translation.py": "Chapter 11 source topology and approved-change validation",
    "scripts/build_pretext_pdf_strict.py": "cumulative deterministic PDF builder evolution",
    "scripts/build_directory_manifest.py": "full-tree manifest and HTML-QA algorithm alignment",
    "scripts/build_zenodo_boundary_package.py": "generic public-byte privacy hardening",
    "scripts/finalize_chapter01_html.py": "cumulative finalized HTML reader evolution",
    "scripts/qa_chapter01_reader.py": "generic public-byte privacy hardening",
    "scripts/qa_chapter03_companion.py": "portable QA-path preservation",
    "scripts/qa_chapter04_companion.py": "portable QA-path preservation",
    "scripts/qa_chapter05_companion.py": "portable QA-path preservation",
    "xsl/custom-latex.xsl": "cumulative PDF reader implementation evolution",
    "xsl/topology-style.xsl": "cumulative HTML reader implementation evolution",
}
EVOLVING_PRIOR_ADDITIVE = {
    "companion/RIGHTS.md": "cumulative Chapter 11 companion rights preservation",
    "companion/chapter_09_mastery.ptx": (
        "inherited Chapter 9 companion schema repair required by the cumulative "
        "Chapters 1-11 RelaxNG pass"
    ),
}
REQUIRED_INHERITED_ADDITIVE_UPDATES = {"companion/chapter_09_mastery.ptx"}

# These are the only inherited translated-source identities allowed to differ
# from the admitted Chapter 10 manifest.  C095/C111 record the superseded,
# invalid derivative rewrites; C129/C130 record the two source-native schema
# repairs that replace them at the cumulative Chapter 11 boundary.
EVOLVING_PRIOR_SOURCE = {
    "source/sec_seq_summ.ptx": {
        "correction_id": "O003-C095",
        "correction_status": "superseded",
        "reason": "restore the source-valid list nested in its paragraph",
    },
    "source/sec_closed_set_summ.ptx": {
        "correction_id": "O003-C111",
        "correction_status": "superseded",
        "reason": "restore the source-valid list nested in its paragraph",
    },
    "source/sec_cont_open_sets.ptx": {
        "correction_id": "O003-C129",
        "correction_status": "verified",
        "reason": "move the unchanged corollary out of an inadmissible activity introduction",
    },
    "source/sec_seq_exer.ptx": {
        "correction_id": "O003-C130",
        "correction_status": "verified",
        "reason": "move the unchanged theorem out of an inadmissible task statement",
    },
}

CONTROL_INPUTS = (
    "00_control/TERMINOLOGY.csv",
    "00_control/SOURCE_CORRECTIONS.csv",
)
PRIOR_TERMINOLOGY_AUDIT = "00_control/CHAPTER09_TERMINOLOGY_AUDIT.md"
TERMINOLOGY_AUDIT = "00_control/CHAPTER11_TERMINOLOGY_AUDIT.md"
PRIOR_PUBLICATION_RECEIPTS = (
    "qa/CHAPTER10_GITHUB_PUBLICATION_RECEIPT.md",
    "qa/CHAPTER10_ZENODO_PUBLICATION_RECEIPT.md",
    "qa/CHAPTER10_FIGSHARE_PUBLICATION_RECEIPT.md",
)

EXPECTED_EXTERNAL_XREFS: set[str] = set()
EXPECTED_INSERTIONS = {"sec_sub_metric_intro.ptx:57:exploration"}
EXPECTED_PRIOR_SOURCE_FILES = 66
EXPECTED_CHAPTER_SOURCE_FILES = 6
EXPECTED_TOTAL_SOURCE_FILES = 72
EXPECTED_COMPANION_FRAGMENTS = 5
EXPECTED_SOURCE_GUIDES = 35
EXPECTED_ACTIVITY_GUIDES = 16
EXPECTED_EXERCISE_GUIDES = 19
EXPECTED_MASTERY_CHECKS = 8
EXPECTED_GROUPING_TASK_COUNT = 1
EXPECTED_TOTAL_ENTRIES = 43
EXPECTED_CORRECTION_RECORDS = 15
EXPECTED_TERM_ID_SET = {f"O003-T{number:03d}" for number in range(133, 142)}
EXPECTED_CORRECTION_ID_SET = {
    *(f"O003-C{number:03d}" for number in range(113, 122)),
    *(f"O003-C{number:03d}" for number in range(123, 129)),
}

HTML_RUN_1 = "qa/CHAPTER11_HTML_MANIFEST_RUN1.json"
HTML_RUN_2 = "qa/CHAPTER11_HTML_MANIFEST_RUN2.json"
HTML_CANONICAL = "qa/CHAPTER11_HTML_MANIFEST.json"
HTML_QA = "qa/CHAPTER11_HTML_QA.json"
HTML_ROOT = "output/chapters01-11-html"
PDF_RELATIVE = "output/chapters01-11-pdf/chapters_01_11_reader.pdf"
PDF_EVIDENCE = {
    "deterministic_run_1": "qa/CHAPTER11_PDF_RUN1_HASH.json",
    "deterministic_run_2": "qa/CHAPTER11_PDF_RUN2_HASH.json",
    "structure_qa": "qa/CHAPTER11_PDF_STRUCTURE.json",
    "visual_qa": "qa/CHAPTER11_PDF_VISUAL_QA.json",
}
BROWSER_QA = "qa/CHAPTER11_BROWSER_QA.json"
DOCS_EVIDENCE = (
    "qa/CHAPTER11_DOCS_MANIFEST.json",
    "qa/CHAPTER11_DOCS_QA.json",
    "qa/CHAPTER11_BUILD_QA.md",
)

PACKAGE_ROOT_FILES = (
    ".gitattributes",
    "README.md",
    "LICENSES.md",
    "project.ptx",
    "requirements.txt",
    "publication/publication.ptx",
)
PACKAGE_TREE_DIRECTORIES = ("companion", "backend", "assets", "xsl")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise FileNotFoundError(path)
    return {"bytes": path.stat().st_size, "sha256": sha256(path)}


def file_row(relative: str, prefix: str = "repo/") -> dict[str, object]:
    return {"path": f"{prefix}{relative}", **identity(ROOT / relative)}


def authority_row(name: str) -> dict[str, object]:
    return {"path": f"authority/source/{name}", **identity(AUTHORITY_SOURCE / name)}


def control_row(relative: str) -> dict[str, object]:
    return {"path": relative, **identity(LANE / relative)}


def read_json(relative: str) -> dict[str, Any]:
    value = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object in {relative}")
    return value


def read_csv_by_id(relative: str) -> dict[str, dict[str, str]]:
    path = LANE / relative
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        row_id = row.get("id", "")
        if not row_id:
            raise RuntimeError(f"row without id in {relative}")
        if row_id in result:
            raise RuntimeError(f"duplicate id in {relative}: {row_id}")
        result[row_id] = row
    return result


def require_dict(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} must be an object")
    return value


def require_list(value: object, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise RuntimeError(f"{label} must be an array")
    return value


def require_pass(report: dict[str, Any], label: str) -> None:
    if report.get("status") != "pass":
        raise RuntimeError(f"{label} is not passing")


def safe_relative_path(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise RuntimeError(f"{label} has no path")
    relative = value.removeprefix("repo/")
    posix = PurePosixPath(relative)
    if (
        posix.is_absolute()
        or ".." in posix.parts
        or "\\" in relative
        or re_absolute(relative)
    ):
        raise RuntimeError(f"{label} has unsafe or nonportable path: {value!r}")
    return relative


def assert_identity(label: str, expected: object, current: dict[str, object]) -> None:
    row = require_dict(expected, label)
    if row.get("bytes") != current["bytes"] or row.get("sha256") != current["sha256"]:
        raise RuntimeError(
            f"{label} identity mismatch: expected {row.get('bytes')}/{row.get('sha256')}, "
            f"current {current['bytes']}/{current['sha256']}"
        )


def assert_path(label: str, reported: object, expected: str) -> None:
    if reported != expected:
        raise RuntimeError(f"{label} path mismatch: {reported!r} != {expected!r}")


def rows_by_path(rows: object, label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for raw in require_list(rows, label):
        row = require_dict(raw, label)
        relative = safe_relative_path(row.get("path"), label)
        if relative in result:
            raise RuntimeError(f"duplicate {label} path: {relative}")
        result[relative] = row
    return result


def combined_named_files(base: Path, names: list[str] | tuple[str, ...]) -> str:
    digest = hashlib.sha256()
    for name in names:
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update((base / name).read_bytes())
    return digest.hexdigest()


def raw_concatenated_files(base: Path, names: tuple[str, ...]) -> str:
    digest = hashlib.sha256()
    for name in names:
        digest.update((base / name).read_bytes())
    return digest.hexdigest()


def re_absolute(value: str) -> bool:
    return (
        value.startswith("/")
        or value.startswith("\\\\")
        or (len(value) >= 3 and value[1] == ":" and value[2] in {"\\", "/"})
    )


def assert_no_absolute_paths(value: object, location: str = "manifest") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            assert_no_absolute_paths(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            assert_no_absolute_paths(child, f"{location}[{index}]")
    elif isinstance(value, str) and re_absolute(value):
        raise RuntimeError(f"absolute/local path leaked at {location}: {value!r}")


def validate_html_tree(html_root: Path, manifest: dict[str, Any]) -> tuple[int, int, int]:
    expected: dict[str, tuple[int, str]] = {}
    for raw in require_list(manifest.get("files"), "HTML manifest files"):
        row = require_dict(raw, "HTML manifest row")
        relative = safe_relative_path(row.get("path"), "HTML manifest row")
        if relative in expected:
            raise RuntimeError(f"duplicate HTML manifest path: {relative}")
        expected[relative] = (int(row.get("bytes", -1)), str(row.get("sha256", "")))
    actual_paths = [path for path in html_root.rglob("*") if path.is_file()]
    actual = {path.relative_to(html_root).as_posix(): path for path in actual_paths}
    if set(actual) != set(expected):
        missing = sorted(set(expected) - set(actual))[:5]
        extra = sorted(set(actual) - set(expected))[:5]
        raise RuntimeError(
            f"canonical Chapter 11 HTML closure differs: missing={missing}, extra={extra}"
        )
    total_bytes = 0
    html_files = 0
    for relative in sorted(actual, key=lambda value: (value.casefold(), value)):
        current = identity(actual[relative])
        expected_bytes, expected_sha = expected[relative]
        if current["bytes"] != expected_bytes or current["sha256"] != expected_sha:
            raise RuntimeError(f"HTML identity mismatch: {relative}")
        total_bytes += int(current["bytes"])
        html_files += relative.lower().endswith(".html")
    if len(actual) != manifest.get("file_count"):
        raise RuntimeError("HTML file count differs from manifest")
    if html_files != manifest.get("html_files"):
        raise RuntimeError("HTML page count differs from manifest")
    if total_bytes != manifest.get("total_bytes"):
        raise RuntimeError("HTML byte total differs from manifest")
    return len(actual), html_files, total_bytes


def validate_reported_evidence(value: object, label: str) -> list[dict[str, object]]:
    """Validate all nested evidence identity rows in a browser report."""
    found: list[dict[str, object]] = []
    if isinstance(value, dict):
        if "path" in value and "bytes" in value and "sha256" in value:
            relative = safe_relative_path(value["path"], label)
            current = file_row(relative)
            assert_identity(label, value, current)
            found.append(current)
        for child in value.values():
            found.extend(validate_reported_evidence(child, label))
    elif isinstance(value, list):
        for child in value:
            found.extend(validate_reported_evidence(child, label))
    unique = {str(row["path"]): row for row in found}
    return [unique[path] for path in sorted(unique)]


def package_tree_rows(relative: str, *, python_only: bool = False) -> list[dict[str, object]]:
    base = ROOT / relative
    rows: list[dict[str, object]] = []
    for path in sorted(
        (candidate for candidate in base.rglob("*") if candidate.is_file()),
        key=lambda candidate: candidate.relative_to(ROOT).as_posix().casefold(),
    ):
        if "__pycache__" in path.parts or path.suffix.casefold() == ".pyc":
            continue
        if python_only and path.suffix.casefold() != ".py":
            continue
        rows.append(file_row(path.relative_to(ROOT).as_posix()))
    return rows


def unique_identity_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    by_path: dict[str, dict[str, object]] = {}
    for row in rows:
        path = str(row["path"])
        previous = by_path.get(path)
        if previous is not None and previous != row:
            raise RuntimeError(f"conflicting package inventory identity: {path}")
        by_path[path] = row
    return [by_path[path] for path in sorted(by_path, key=str.casefold)]


def main() -> int:
    if EXPECTED_SOURCE_PROMPTS != EXPECTED_SOURCE_GUIDES:
        raise RuntimeError("Chapter 11 source-guide contract changed")
    if EXPECTED_ACTIVITY_PROMPTS != EXPECTED_ACTIVITY_GUIDES:
        raise RuntimeError("Chapter 11 activity-guide contract changed")
    if EXPECTED_EXERCISE_PROMPTS != EXPECTED_EXERCISE_GUIDES:
        raise RuntimeError("Chapter 11 exercise-guide contract changed")
    if EXPECTED_MASTERY != EXPECTED_MASTERY_CHECKS:
        raise RuntimeError("Chapter 11 mastery contract changed")
    if EXPECTED_GROUPING_TASKS != EXPECTED_GROUPING_TASK_COUNT:
        raise RuntimeError("Chapter 11 grouping-task contract changed")
    if len(SOURCE_FILES) != EXPECTED_CHAPTER_SOURCE_FILES:
        raise RuntimeError(
            f"Chapter 11 source closure is not exactly {EXPECTED_CHAPTER_SOURCE_FILES} files"
        )
    if len(FRAGMENTS) != EXPECTED_COMPANION_FRAGMENTS:
        raise RuntimeError(
            f"Chapter 11 companion closure is not exactly {EXPECTED_COMPANION_FRAGMENTS} fragments"
        )
    if set(EXPECTED_TERM_IDS) != EXPECTED_TERM_ID_SET:
        raise RuntimeError("Chapter 11 controlled-term ID closure changed")
    if set(EXPECTED_CORRECTION_IDS) != EXPECTED_CORRECTION_ID_SET:
        raise RuntimeError("Chapter 11 correction ID closure changed")

    prior_path = ROOT / PRIOR_MANIFEST
    assert_identity(
        "pinned Chapter 10 source manifest",
        PRIOR_MANIFEST_IDENTITY,
        identity(prior_path),
    )
    prior = read_json(PRIOR_MANIFEST)
    require_pass(prior, "Chapter 10 cumulative source manifest")
    if prior.get("boundary") != "chapters_01_10_with_separately_licensed_self_study_companions":
        raise RuntimeError("unexpected Chapter 10 admission boundary")

    terminology_rows = read_csv_by_id("00_control/TERMINOLOGY.csv")
    correction_rows = read_csv_by_id("00_control/SOURCE_CORRECTIONS.csv")
    for term_id in EXPECTED_TERM_ID_SET:
        row = terminology_rows.get(term_id)
        if row is None or row.get("status") != "approved" or not row.get("id_ID"):
            raise RuntimeError(f"Chapter 11 term is not approved and populated: {term_id}")
    for correction_id in EXPECTED_CORRECTION_ID_SET:
        row = correction_rows.get(correction_id)
        if row is None or row.get("status") != "verified" or not row.get("evidence"):
            raise RuntimeError(f"Chapter 11 correction is not verified and evidenced: {correction_id}")
    for relative, specification in EVOLVING_PRIOR_SOURCE.items():
        correction_id = str(specification["correction_id"])
        record = correction_rows.get(correction_id)
        if record is None:
            raise RuntimeError(f"missing inherited source-repair record: {correction_id}")
        if record.get("file") != f"repo/{relative}":
            raise RuntimeError(f"inherited source-repair path changed: {correction_id}")
        if record.get("status") != specification["correction_status"]:
            raise RuntimeError(f"inherited source-repair status changed: {correction_id}")
        if not record.get("evidence"):
            raise RuntimeError(f"inherited source-repair lacks evidence: {correction_id}")

    prior_source_names: list[str] = []
    inherited_source_updates: list[dict[str, object]] = []
    translated_source = require_dict(prior.get("translated_source"), "prior translated source")
    inherited_chapters: dict[str, dict[str, Any]] = {}
    for chapter in PRIOR_CHAPTERS:
        chapter_row = require_dict(translated_source.get(chapter), f"prior {chapter}")
        current_files: list[dict[str, object]] = []
        for raw in require_list(chapter_row.get("files"), f"prior {chapter} files"):
            row = require_dict(raw, f"prior {chapter} source row")
            relative = safe_relative_path(row.get("path"), f"prior {chapter} source row")
            if not relative.startswith("source/"):
                raise RuntimeError(f"non-source path in prior {chapter}: {relative}")
            name = relative.removeprefix("source/")
            if name in prior_source_names:
                raise RuntimeError(f"duplicate previously admitted source file: {name}")
            current = file_row(relative)
            changed = row.get("bytes") != current["bytes"] or row.get("sha256") != current["sha256"]
            specification = EVOLVING_PRIOR_SOURCE.get(relative)
            if changed and specification is None:
                raise RuntimeError(f"unapproved previously admitted source drift: {relative}")
            if changed and specification is not None:
                inherited_source_updates.append(
                    {
                        "path": current["path"],
                        "previous_bytes": row.get("bytes"),
                        "previous_sha256": row.get("sha256"),
                        "current": current,
                        "reason": specification["reason"],
                        "correction_id": specification["correction_id"],
                        "correction_status": specification["correction_status"],
                        "audit": f"repo/{SCHEMA_QA}",
                    }
                )
            prior_source_names.append(name)
            current_files.append(current)
        inherited = dict(chapter_row)
        inherited["files"] = current_files
        inherited["admission"] = (
            f"identity inherited from repo/{PRIOR_MANIFEST}, except the four explicit "
            f"schema repairs bound by repo/{SCHEMA_QA} and 00_control/SOURCE_CORRECTIONS.csv"
        )
        inherited_chapters[chapter] = inherited
    if len(prior_source_names) != EXPECTED_PRIOR_SOURCE_FILES:
        raise RuntimeError(
            f"prior source closure changed: {len(prior_source_names)} != {EXPECTED_PRIOR_SOURCE_FILES}"
        )
    changed_source_paths = {
        safe_relative_path(row["path"], "inherited source update")
        for row in inherited_source_updates
    }
    if changed_source_paths != set(EVOLVING_PRIOR_SOURCE):
        raise RuntimeError(
            "inherited source-repair closure differs: "
            f"{sorted(changed_source_paths)} != {sorted(EVOLVING_PRIOR_SOURCE)}"
        )
    if set(prior_source_names).intersection(SOURCE_FILES):
        raise RuntimeError("Chapter 11 source closure overlaps prior chapters")

    source_qa = read_json(SOURCE_QA)
    companion_qa = read_json(COMPANION_QA)
    backend = read_json(BACKEND_MANIFEST)
    require_pass(source_qa, "Chapter 11 source QA")
    require_pass(companion_qa, "Chapter 11 companion QA")
    if source_qa.get("failures") != [] or companion_qa.get("failures") != []:
        raise RuntimeError("Chapter 11 source or companion QA records failures")

    source_qa_rows = {
        str(row.get("file")): require_dict(row, "Chapter 11 source-QA file")
        for row in require_list(source_qa.get("files"), "Chapter 11 source-QA files")
    }
    if set(source_qa_rows) != set(SOURCE_FILES):
        raise RuntimeError("Chapter 11 source-QA file closure changed")
    authority_files: list[dict[str, object]] = []
    chapter_files: list[dict[str, object]] = []
    source_counts: Counter[str] = Counter()
    for name in SOURCE_FILES:
        authority = authority_row(name)
        translated = file_row(f"source/{name}")
        row = source_qa_rows[name]
        assert_identity(f"Chapter 11 authority {name}", row.get("authority"), authority)
        assert_identity(f"Chapter 11 translated source {name}", row.get("translated"), translated)
        authority_files.append(authority)
        chapter_files.append(translated)
        source_counts.update(
            {
                "activities_and_explorations": int(row.get("activities_and_explorations", 0)),
                "exercises": int(row.get("exercises", 0)),
                "tasks": int(row.get("tasks", 0)),
                "images": int(row.get("images", 0)),
            }
        )
    authority_combined = combined_named_files(AUTHORITY_SOURCE, SOURCE_FILES)
    authority_raw = raw_concatenated_files(AUTHORITY_SOURCE, SOURCE_FILES)
    if authority_combined != EXPECTED_AUTHORITY_ORDERED_SHA256:
        raise RuntimeError("frozen Chapter 11 ordered authority closure changed")
    if authority_raw != EXPECTED_AUTHORITY_RAW_SHA256:
        raise RuntimeError("frozen Chapter 11 raw authority closure changed")
    chapter_combined = combined_named_files(ROOT / "source", SOURCE_FILES)
    if source_qa.get("combined_translated_sha256") != chapter_combined:
        raise RuntimeError("Chapter 11 source-QA combined translated identity is stale")
    if set(source_qa.get("approved_external_xref_targets", [])) != EXPECTED_EXTERNAL_XREFS:
        raise RuntimeError("Chapter 11 external-xref admission changed")
    for key in (
        "approved_attribute_changes",
        "approved_element_block_moves",
        "approved_element_shell_moves",
    ):
        if source_qa.get(key) not in (None, []):
            raise RuntimeError(f"unexpected Chapter 11 source-QA closure: {key}")
    insertion_rows = {
        row.get("key"): row
        for row in require_list(source_qa.get("approved_element_insertions"), "Chapter 11 insertions")
    }
    if set(insertion_rows) != EXPECTED_INSERTIONS:
        raise RuntimeError("Chapter 11 approved insertion closure changed")
    math_rows = {
        row.get("key"): row
        for row in require_list(source_qa.get("approved_math_changes"), "Chapter 11 math changes")
    }
    expected_math_rows = {row["key"]: row for row in EXPECTED_MATH_CHANGES}
    if math_rows != expected_math_rows:
        raise RuntimeError("Chapter 11 approved protected-math repair closure changed")

    companion_row = file_row(COMPANION_WRAPPER)
    source_qa_row = file_row(SOURCE_QA)
    companion_qa_row = file_row(COMPANION_QA)
    backend_row = file_row(BACKEND_MANIFEST)
    alias_row = file_row(ALIAS_MAP)
    assert_identity("Chapter 11 companion", companion_qa.get("companion"), companion_row)
    assert_identity("Chapter 11 source-QA receipt", companion_qa.get("source_qa"), source_qa_row)
    fragment_rows = rows_by_path(companion_qa.get("fragments"), "Chapter 11 fragments")
    if set(fragment_rows) != set(COMPANION_FRAGMENTS):
        raise RuntimeError("Chapter 11 companion fragment closure changed")
    for relative, row in fragment_rows.items():
        assert_identity(f"Chapter 11 fragment {relative}", row, file_row(relative))

    if backend.get("schema_version") != "2.0.0" or backend.get("locale") != "id-ID":
        raise RuntimeError("Chapter 11 backend schema or locale changed")
    component = require_dict(backend.get("component"), "Chapter 11 backend component")
    assert_path("Chapter 11 backend component", component.get("path"), f"repo/{COMPANION_WRAPPER}")
    assert_identity("Chapter 11 backend component", component.get("identity"), companion_row)
    backend_alias = require_dict(component.get("entry_alias_map"), "Chapter 11 backend aliases")
    assert_path("Chapter 11 backend aliases", backend_alias.get("path"), f"repo/{ALIAS_MAP}")
    assert_identity("Chapter 11 backend aliases", backend_alias, alias_row)
    backend_fragments = rows_by_path(component.get("fragments"), "Chapter 11 backend fragments")
    if set(backend_fragments) != set(COMPANION_FRAGMENTS):
        raise RuntimeError("Chapter 11 backend fragment closure changed")
    for relative, row in backend_fragments.items():
        assert_identity(f"Chapter 11 backend fragment {relative}", row, file_row(relative))
    backend_source_qa = require_dict(backend.get("translated_unit_source_qa"), "backend source QA")
    assert_path("backend source QA", backend_source_qa.get("path"), f"repo/{SOURCE_QA}")
    assert_identity("backend source QA", backend_source_qa, source_qa_row)
    if backend_source_qa.get("combined_translated_sha256") != chapter_combined:
        raise RuntimeError("backend Chapter 11 translated-source identity is stale")
    backend_companion_qa = require_dict(backend.get("companion_qa"), "backend companion QA")
    assert_path("backend companion QA", backend_companion_qa.get("path"), f"repo/{COMPANION_QA}")
    assert_identity("backend companion QA", backend_companion_qa, companion_qa_row)

    entry_counts = require_dict(companion_qa.get("entry_counts"), "companion entry counts")
    expected_entry_counts = {
        "source_prompt_guide": EXPECTED_SOURCE_GUIDES,
        "activity_or_task_guide": EXPECTED_ACTIVITY_GUIDES,
        "exercise_prompt_guide": EXPECTED_EXERCISE_GUIDES,
        "mastery_check": EXPECTED_MASTERY_CHECKS,
        "total": EXPECTED_TOTAL_ENTRIES,
    }
    for key, expected in expected_entry_counts.items():
        if entry_counts.get(key) != expected:
            raise RuntimeError(f"Chapter 11 companion entry count changed for {key}")
    reveal_counts = require_dict(companion_qa.get("reveal_counts"), "companion reveals")
    surface_counts = require_dict(companion_qa.get("surface_counts"), "companion surfaces")
    for kind in ("statement", "hint", "answer", "solution"):
        if surface_counts.get(kind) != EXPECTED_TOTAL_ENTRIES:
            raise RuntimeError(f"Chapter 11 companion lacks complete {kind} surfaces")
    for kind in ("hint", "answer", "solution"):
        if reveal_counts.get(kind) != EXPECTED_TOTAL_ENTRIES:
            raise RuntimeError(f"Chapter 11 companion lacks complete {kind} reveals")
    coverage = require_dict(backend.get("coverage_contract"), "backend coverage")
    expected_coverage = {
        "source_prompt_guides": EXPECTED_SOURCE_GUIDES,
        "activity_or_task_guides": EXPECTED_ACTIVITY_GUIDES,
        "exercise_prompt_guides": EXPECTED_EXERCISE_GUIDES,
        "mastery_checks": EXPECTED_MASTERY_CHECKS,
        "excluded_grouping_tasks": EXPECTED_GROUPING_TASK_COUNT,
        "total_entries": EXPECTED_TOTAL_ENTRIES,
        "statements": EXPECTED_TOTAL_ENTRIES,
        "hints": EXPECTED_TOTAL_ENTRIES,
        "answers": EXPECTED_TOTAL_ENTRIES,
        "solutions": EXPECTED_TOTAL_ENTRIES,
        "active_images": 0,
        "remote_or_interactive_surfaces": 0,
        "source_correction_records": EXPECTED_CORRECTION_RECORDS,
    }
    for key, expected in expected_coverage.items():
        if coverage.get(key) != expected:
            raise RuntimeError(f"Chapter 11 backend coverage is stale for {key}")
    if coverage.get("all_entries_have_statement_hint_answer_solution") is not True:
        raise RuntimeError("Chapter 11 backend complete-surface contract is false")

    current_controls = {relative: control_row(relative) for relative in CONTROL_INPUTS}
    companion_controls = require_dict(companion_qa.get("control_inputs"), "companion controls")
    backend_controls = require_dict(backend.get("control_inputs"), "backend controls")
    for key, relative, ids in (
        ("terminology", "00_control/TERMINOLOGY.csv", EXPECTED_TERM_IDS),
        ("source_corrections", "00_control/SOURCE_CORRECTIONS.csv", EXPECTED_CORRECTION_IDS),
    ):
        companion_control = require_dict(companion_controls.get(key), f"companion control {key}")
        assert_path(f"companion control {key}", companion_control.get("path"), relative)
        assert_identity(f"companion control {key}", companion_control, current_controls[relative])
        if set(companion_control.get("required_ids", [])) != ids:
            raise RuntimeError(f"companion control ID closure changed: {key}")
        backend_control = require_dict(backend_controls.get(key), f"backend control {key}")
        assert_path(f"backend control {key}", backend_control.get("path"), relative)
        assert_identity(f"backend control {key}", backend_control, current_controls[relative])
        if set(backend_control.get("selected_ids", [])) != ids:
            raise RuntimeError(f"backend control ID closure changed: {key}")

    inherited_additive: list[dict[str, object]] = []
    inherited_additive_updates: list[dict[str, object]] = []
    inherited_additive_paths: set[str] = set()
    for raw in require_list(prior.get("additive_components"), "prior additive components"):
        row = require_dict(raw, "prior additive component")
        relative = safe_relative_path(row.get("path"), "prior additive component")
        if relative in inherited_additive_paths:
            raise RuntimeError(f"duplicate prior additive component: {relative}")
        current = file_row(relative)
        changed = row.get("bytes") != current["bytes"] or row.get("sha256") != current["sha256"]
        if changed and relative not in EVOLVING_PRIOR_ADDITIVE:
            raise RuntimeError(f"unapproved inherited additive drift: {relative}")
        if changed:
            inherited_additive_updates.append(
                {
                    "path": current["path"],
                    "previous_bytes": row.get("bytes"),
                    "previous_sha256": row.get("sha256"),
                    "current": current,
                    "reason": EVOLVING_PRIOR_ADDITIVE[relative],
                    "audit": f"repo/{SCHEMA_QA}",
                }
            )
        inherited_additive_paths.add(relative)
        inherited_additive.append(current)
    inherited_additive_update_paths = {
        safe_relative_path(row["path"], "inherited additive update")
        for row in inherited_additive_updates
    }
    if not REQUIRED_INHERITED_ADDITIVE_UPDATES.issubset(inherited_additive_update_paths):
        raise RuntimeError("required inherited Chapter 9 companion schema repair is not present")
    if inherited_additive_paths.intersection(NEW_ADDITIVE):
        raise RuntimeError("Chapter 11 additive component duplicates a prior component")

    prior_controls = rows_by_path(prior.get("control_inputs"), "prior control inputs")
    if set(prior_controls) != {*CONTROL_INPUTS, PRIOR_TERMINOLOGY_AUDIT}:
        raise RuntimeError("prior control-input closure changed")
    assert_identity(
        "inherited terminology audit",
        prior_controls[PRIOR_TERMINOLOGY_AUDIT],
        control_row(PRIOR_TERMINOLOGY_AUDIT),
    )
    inherited_control_updates: list[dict[str, object]] = []
    for relative in CONTROL_INPUTS:
        previous = prior_controls[relative]
        current = current_controls[relative]
        if previous.get("bytes") != current["bytes"] or previous.get("sha256") != current["sha256"]:
            inherited_control_updates.append(
                {
                    "path": relative,
                    "previous_bytes": previous.get("bytes"),
                    "previous_sha256": previous.get("sha256"),
                    "current": current,
                    "reason": "append-only cumulative terminology/correction ledger update",
                }
            )

    implementation_by_path: dict[str, dict[str, object]] = {}
    inherited_implementation_updates: list[dict[str, object]] = []
    for raw in require_list(prior.get("production_implementation"), "prior implementation"):
        row = require_dict(raw, "prior implementation row")
        relative = safe_relative_path(row.get("path"), "prior implementation row")
        if relative in implementation_by_path:
            raise RuntimeError(f"duplicate prior implementation path: {relative}")
        current = file_row(relative)
        changed = row.get("bytes") != current["bytes"] or row.get("sha256") != current["sha256"]
        if changed and relative not in EVOLVING_PRIOR_IMPLEMENTATION:
            raise RuntimeError(f"unapproved inherited implementation drift: {relative}")
        if changed:
            inherited_implementation_updates.append(
                {
                    "path": current["path"],
                    "previous_bytes": row.get("bytes"),
                    "previous_sha256": row.get("sha256"),
                    "current": current,
                    "reason": EVOLVING_PRIOR_IMPLEMENTATION[relative],
                }
            )
        implementation_by_path[relative] = current
    for relative in CHAPTER_11_IMPLEMENTATION:
        implementation_by_path[relative] = file_row(relative)

    all_source_names = [*prior_source_names, *SOURCE_FILES]
    if len(all_source_names) != EXPECTED_TOTAL_SOURCE_FILES or len(set(all_source_names)) != EXPECTED_TOTAL_SOURCE_FILES:
        raise RuntimeError(
            f"cumulative Chapters 1-11 source closure is not exactly "
            f"{EXPECTED_TOTAL_SOURCE_FILES} unique files"
        )
    cumulative_combined = combined_named_files(ROOT / "source", all_source_names)

    schema_qa = read_json(SCHEMA_QA)
    require_pass(schema_qa, "Chapter 11 schema QA")
    if schema_qa.get("diagnostics") != []:
        raise RuntimeError("Chapter 11 schema QA records diagnostics")
    schema_source = require_dict(schema_qa.get("source"), "Chapter 11 schema source")
    assert_path("Chapter 11 schema source", schema_source.get("path"), READER_WRAPPER)
    assert_identity("Chapter 11 schema source", schema_source, file_row(READER_WRAPPER))
    xinclude = require_dict(schema_qa.get("xinclude"), "Chapter 11 schema XInclude")
    if xinclude.get("all_local") is not True:
        raise RuntimeError("Chapter 11 schema XInclude closure is not local")
    closure = [
        safe_relative_path(value, "Chapter 11 schema XInclude path")
        for value in require_list(xinclude.get("closure"), "Chapter 11 schema XInclude closure")
    ]
    if len(closure) != len(set(closure)):
        raise RuntimeError("Chapter 11 schema XInclude closure has duplicate paths")
    expected_schema_closure = {
        READER_WRAPPER,
        *(f"source/{name}" for name in all_source_names),
        *(
            relative
            for relative in (*inherited_additive_paths, *NEW_ADDITIVE)
            if relative.startswith("companion/") and relative.endswith(".ptx")
        ),
    }
    if set(closure) != expected_schema_closure:
        missing = sorted(expected_schema_closure - set(closure))[:8]
        extra = sorted(set(closure) - expected_schema_closure)[:8]
        raise RuntimeError(f"Chapter 11 schema closure differs: missing={missing}, extra={extra}")
    if xinclude.get("closure_file_count") != len(closure):
        raise RuntimeError("Chapter 11 schema closure count is stale")
    assert_no_absolute_paths(schema_qa, "Chapter 11 schema QA")
    schema_qa_row = file_row(SCHEMA_QA)

    html_run_1 = read_json(HTML_RUN_1)
    html_run_2 = read_json(HTML_RUN_2)
    html_qa = read_json(HTML_QA)
    require_pass(html_qa, "Chapter 11 HTML QA")
    if html_qa.get("failures") != []:
        raise RuntimeError("Chapter 11 HTML QA records failures")
    identity_keys = ("file_count", "html_files", "total_bytes", "canonical_manifest_sha256")
    if html_run_1.get("files") != html_run_2.get("files"):
        raise RuntimeError("Chapter 11 deterministic HTML runs have different file identities")
    for key in identity_keys:
        if html_run_1.get(key) != html_run_2.get(key) or html_qa.get(key) != html_run_2.get(key):
            raise RuntimeError(f"Chapter 11 HTML evidence differs for {key}")
    canonical_relative = HTML_CANONICAL if (ROOT / HTML_CANONICAL).is_file() else HTML_RUN_2
    html_manifest = read_json(canonical_relative)
    if html_manifest.get("files") != html_run_2.get("files"):
        raise RuntimeError("canonical Chapter 11 HTML identities differ from deterministic run 2")
    for key in identity_keys:
        if html_manifest.get(key) != html_run_2.get(key):
            raise RuntimeError(f"canonical Chapter 11 HTML differs for {key}")
    html_file_count, html_files, html_bytes = validate_html_tree(ROOT / HTML_ROOT, html_manifest)

    browser_qa = read_json(BROWSER_QA)
    require_pass(browser_qa, "Chapter 11 browser QA")
    if browser_qa.get("failures") != []:
        raise RuntimeError("Chapter 11 browser QA records failures")
    assert_path("Chapter 11 browser surface", browser_qa.get("surface"), HTML_ROOT)
    if browser_qa.get("canonical_html_manifest_sha256") != html_manifest.get("canonical_manifest_sha256"):
        raise RuntimeError("Chapter 11 browser QA targets a different HTML tree")
    browser_evidence = validate_reported_evidence(browser_qa, "Chapter 11 browser evidence")
    browser = {
        "status": "pass",
        "receipt": file_row(BROWSER_QA),
        "evidence": browser_evidence,
    }

    docs_manifest = read_json(DOCS_EVIDENCE[0])
    docs_qa = read_json(DOCS_EVIDENCE[1])
    require_pass(docs_manifest, "Chapter 11 docs manifest")
    require_pass(docs_qa, "Chapter 11 docs QA")
    if docs_manifest.get("failures") not in (None, []) or docs_qa.get("failures") not in (None, []):
        raise RuntimeError("Chapter 11 docs evidence records failures")
    docs_receipts = {
        "manifest": file_row(DOCS_EVIDENCE[0]),
        "qa": file_row(DOCS_EVIDENCE[1]),
        "build_qa": file_row(DOCS_EVIDENCE[2]),
    }

    pdf_path = ROOT / PDF_RELATIVE
    if not pdf_path.is_file():
        raise FileNotFoundError(pdf_path)
    reports = {key: read_json(relative) for key, relative in PDF_EVIDENCE.items()}
    for key, report in reports.items():
        require_pass(report, f"Chapter 11 PDF {key}")
    pdf_row = file_row(PDF_RELATIVE)
    assert_identity("Chapter 11 PDF run 1", reports["deterministic_run_1"], pdf_row)
    assert_identity("Chapter 11 PDF run 2", reports["deterministic_run_2"], pdf_row)
    structure_artifact = require_dict(reports["structure_qa"].get("artifact"), "PDF structure artifact")
    assert_path("Chapter 11 PDF structure artifact", structure_artifact.get("path"), PDF_RELATIVE)
    assert_identity("Chapter 11 PDF structure artifact", structure_artifact, pdf_row)
    visual_pdf = require_dict(reports["visual_qa"].get("pdf"), "PDF visual artifact")
    assert_path("Chapter 11 PDF visual artifact", visual_pdf.get("path"), PDF_RELATIVE)
    assert_identity("Chapter 11 PDF visual artifact", visual_pdf, pdf_row)
    if reports["visual_qa"].get("sha256") != pdf_row["sha256"]:
        raise RuntimeError("Chapter 11 PDF visual-QA top-level hash is stale")
    pages = reports["visual_qa"].get("pages")
    if not isinstance(pages, int) or pages <= 0:
        raise RuntimeError("Chapter 11 PDF visual QA has no valid page count")
    pdf = {
        **pdf_row,
        "status": "pass",
        "pages": pages,
        "tagged": reports["visual_qa"].get("tagged"),
        **{key: file_row(relative) for key, relative in PDF_EVIDENCE.items()},
    }

    chapter_11 = {
        "authority_combined_sha256": authority_combined,
        "authority_raw_concatenated_sha256": authority_raw,
        "authority_files": authority_files,
        "combined_sha256": chapter_combined,
        "files": chapter_files,
        "source_qa": f"repo/{SOURCE_QA}",
        **dict(source_counts),
        "assessable_prompts": EXPECTED_SOURCE_GUIDES,
        "xml_ids": source_qa.get("xml_ids"),
        "xrefs": source_qa.get("xrefs"),
        "approved_external_xrefs": sorted(EXPECTED_EXTERNAL_XREFS),
    }
    translated = {
        **inherited_chapters,
        "chapter_11": chapter_11,
        "combined_algorithm": "SHA-256 over each ordered source filename, one NUL byte, then exact file bytes",
        "cumulative_combined_sha256": cumulative_combined,
    }

    rights_boundary = require_dict(companion_qa.get("rights_boundary"), "companion rights boundary")
    rights_row = file_row("companion/RIGHTS.md")
    licenses_row = file_row("LICENSES.md")
    assert_identity("companion rights note", rights_boundary.get("companion_rights"), rights_row)
    assert_identity("collection licenses", rights_boundary.get("collection_licenses"), licenses_row)
    if rights_boundary.get("translated_spine_license") != "CC-BY-NC-SA-3.0":
        raise RuntimeError("translated-spine license boundary changed")
    if rights_boundary.get("companion_license") != "CC-BY-4.0":
        raise RuntimeError("companion license boundary changed")

    prior_publication_receipts = {
        Path(relative).stem.removeprefix("CHAPTER10_").removesuffix("_PUBLICATION_RECEIPT").lower(): file_row(relative)
        for relative in PRIOR_PUBLICATION_RECEIPTS
    }

    asset_rows: list[dict[str, object]] = []
    companion_assets = require_dict(companion_qa.get("assets"), "companion assets")
    if companion_assets.get("images") != []:
        raise RuntimeError("Chapter 11 companion QA unexpectedly declares images")
    if companion_assets.get("interactive_or_remote_surfaces") != []:
        raise RuntimeError("Chapter 11 companion QA unexpectedly declares remote surfaces")
    backend_assets = require_list(backend.get("assets"), "backend assets")
    if backend_assets:
        raise RuntimeError("Chapter 11 backend unexpectedly declares active assets")
    for asset in backend_assets:
        asset_row = require_dict(asset, "backend asset")
        for raw_format in require_list(asset_row.get("formats"), "backend asset formats"):
            format_row = require_dict(raw_format, "backend asset format")
            relative = safe_relative_path(format_row.get("path"), "backend asset format")
            current = file_row(relative)
            assert_identity(f"Chapter 11 asset {relative}", format_row, current)
            asset_rows.append(current)

    backend_corrections = [
        require_dict(row, "source correction")
        for row in require_list(backend.get("source_corrections"), "source corrections")
    ]
    backend_correction_ids = {str(row.get("id")) for row in backend_corrections}
    if backend_correction_ids != EXPECTED_CORRECTION_ID_SET:
        raise RuntimeError("Chapter 11 backend correction-ID closure changed")
    correction_statuses = Counter(str(row.get("status")) for row in backend_corrections)
    if correction_statuses != Counter({"verified": EXPECTED_CORRECTION_RECORDS}):
        raise RuntimeError(
            f"Chapter 11 correction closure is not exactly {EXPECTED_CORRECTION_RECORDS} "
            f"verified records: {dict(sorted(correction_statuses.items()))}"
        )

    caveats = [
        "The cumulative HTML reader retains recorded remote dependencies; whole-edition offline closure remains a release gate.",
        "Whole-book figure provenance remains a final-release gate; Chapter 11 introduces no active assets.",
    ]
    if pdf.get("tagged") is not True:
        caveats.append("PDF is not tagged; HTML remains the primary accessible surface.")

    qa_receipts = {
        "prior_source_manifest": file_row(PRIOR_MANIFEST),
        "source": source_qa_row,
        "companion": companion_qa_row,
        "backend": backend_row,
        "schema": schema_qa_row,
        "html_manifest": file_row(canonical_relative),
        "html_run_1": file_row(HTML_RUN_1),
        "html_run_2": file_row(HTML_RUN_2),
        "html": file_row(HTML_QA),
        "browser": file_row(BROWSER_QA),
        "pdf": {key: file_row(relative) for key, relative in PDF_EVIDENCE.items()},
        "docs": docs_receipts,
        "prior_publication": prior_publication_receipts,
    }
    package_inventory_rows = [
        *[file_row(relative) for relative in PACKAGE_ROOT_FILES],
        *[
            control_row(relative)
            for relative in (*CONTROL_INPUTS, PRIOR_TERMINOLOGY_AUDIT, TERMINOLOGY_AUDIT)
        ],
        *[file_row(f"source/{name}") for name in all_source_names],
        *[row for directory in PACKAGE_TREE_DIRECTORIES for row in package_tree_rows(directory)],
        *package_tree_rows("scripts", python_only=True),
        *[file_row(f"qa/CHAPTER{number:02d}_SOURCE_MANIFEST.json") for number in range(1, 11)],
        source_qa_row,
        companion_qa_row,
        schema_qa_row,
        qa_receipts["html_manifest"],
        qa_receipts["html_run_1"],
        qa_receipts["html_run_2"],
        qa_receipts["html"],
        qa_receipts["browser"],
        *qa_receipts["pdf"].values(),
        *docs_receipts.values(),
        *prior_publication_receipts.values(),
        *browser_evidence,
    ]
    package_source_inventory = unique_identity_rows(package_inventory_rows)
    authority_archive_row = {
        "path": f"authority/archives/{AUTHORITY_ARCHIVE.name}",
        **identity(AUTHORITY_ARCHIVE),
    }

    manifest_status = "pass"
    manifest = {
        "schema_version": 1,
        "lane": "O003/C90",
        "locale": "id-ID",
        "boundary": "chapters_01_11_with_separately_licensed_self_study_companions",
        "status": manifest_status,
        "pending_evidence": [],
        "prior_admission": {
            **file_row(PRIOR_MANIFEST),
            "admission_basis": "locally validated and publicly read-back Chapter 10 source manifest",
            "locally_admitted": True,
            "publication_status": "published_github_zenodo_figshare",
            "publication_receipts": prior_publication_receipts,
        },
        "authority": {
            "work": "Topology: An Inquiry-Based Approach",
            "author": "Steven Schlicker",
            "official_record": "https://scholarworks.gvsu.edu/books/30/",
            "repository": "https://github.com/gvsuoer/topology",
            "commit": "0c2d8f614ef87aa00de373f3418146c2f1d13bb9",
            "tree": "7df245934eedb7174d5ff8af18afff5a7abdde78",
            "archive_sha256": "d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3",
            "controlling_core_license": "CC-BY-NC-SA-3.0",
            "chapter_11_ordered_sha256": authority_combined,
            "chapter_11_raw_concatenated_sha256": authority_raw,
        },
        "translated_source": translated,
        "inherited_source_updates": inherited_source_updates,
        "additive_components": inherited_additive + [file_row(path) for path in NEW_ADDITIVE],
        "inherited_additive_updates": inherited_additive_updates,
        "control_inputs": [
            *[current_controls[path] for path in CONTROL_INPUTS],
            control_row(PRIOR_TERMINOLOGY_AUDIT),
            control_row(TERMINOLOGY_AUDIT),
        ],
        "inherited_control_updates": inherited_control_updates,
        "production_implementation": [implementation_by_path[path] for path in sorted(implementation_by_path)],
        "inherited_implementation_updates": inherited_implementation_updates,
        "chapter_11_identity_bundle": {
            "source_qa": source_qa_row,
            "companion_qa": companion_qa_row,
            "backend": backend_row,
            "schema_qa": schema_qa_row,
            "terminology_audit": control_row(TERMINOLOGY_AUDIT),
            "companion_wrapper": companion_row,
            "companion_fragments": [file_row(path) for path in COMPANION_FRAGMENTS],
            "entry_alias_map": alias_row,
            "cumulative_reader_wrapper": file_row(READER_WRAPPER),
            "project": file_row("project.ptx"),
            "assets": asset_rows,
            "rights_note": rights_row,
            "collection_licenses": licenses_row,
        },
        "schema_validation": {
            "status": "pass",
            "receipt": schema_qa_row,
            "runtime": schema_qa.get("runtime"),
            "pretext_resource_commit": schema_qa.get("pretext_resource_commit"),
            "schema": schema_qa.get("schema"),
            "xinclude_all_local": True,
            "xinclude_closure_file_count": len(closure),
        },
        "companion_coverage": {
            "contract": coverage,
            "entry_counts": entry_counts,
            "source_prompt_counts": companion_qa.get("source_prompt_counts"),
            "reveal_counts": reveal_counts,
            "surface_counts": surface_counts,
            "excluded_grouping_tasks": EXPECTED_GROUPING_TASK_COUNT,
            "described_images": 0,
            "remote_or_interactive_surfaces": 0,
        },
        "source_correction_statuses": dict(sorted(correction_statuses.items())),
        "inherited_source_repair_records": [
            {
                "id": specification["correction_id"],
                "status": specification["correction_status"],
                "path": f"repo/{relative}",
                "reason": specification["reason"],
            }
            for relative, specification in EVOLVING_PRIOR_SOURCE.items()
        ],
        "rights": {
            "translated_gvsu_spine": "CC-BY-NC-SA-3.0 (conservative determination)",
            "original_self_study_companions": "CC-BY-4.0",
            "upstream_figures": "per-component provenance pending; not relicensed",
            "collection_policy": "per-component rights; no flattened license",
            "rights_note": rights_row,
            "collection_licenses": licenses_row,
            "non_endorsement": True,
        },
        "reader_artifacts": {
            "html": {
                "path": f"repo/{HTML_ROOT}",
                "status": "deterministic_tree_pass",
                "file_count": html_file_count,
                "html_files": html_files,
                "bytes": html_bytes,
                "canonical_manifest_sha256": html_manifest.get("canonical_manifest_sha256"),
                "manifest": qa_receipts["html_manifest"],
                "deterministic_run_1": qa_receipts["html_run_1"],
                "deterministic_run_2": qa_receipts["html_run_2"],
                "qa": qa_receipts["html"],
                "browser_qa": browser,
                "offline_closed": not bool(html_qa.get("external_hosts")),
                "external_hosts": html_qa.get("external_hosts"),
            },
            "pdf": pdf,
        },
        "qa_receipts": qa_receipts,
        "package_source_inventory": package_source_inventory,
        "package_authority_archive": authority_archive_row,
        "known_caveats": caveats,
    }
    assert_no_absolute_paths(manifest)
    payload = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    temporary = OUTPUT.with_name(f".{OUTPUT.name}.tmp")
    temporary.write_text(payload, encoding="utf-8", newline="\n")
    temporary.replace(OUTPUT)
    print(
        json.dumps(
            {
                "status": manifest_status,
                "output": "repo/qa/CHAPTER11_SOURCE_MANIFEST.json",
                "bytes": OUTPUT.stat().st_size,
                "sha256": sha256(OUTPUT),
                "chapter_11_combined_sha256": chapter_combined,
                "cumulative_combined_sha256": cumulative_combined,
                "source_files": len(all_source_names),
                "html_files": html_file_count,
                "pending_evidence": [],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
