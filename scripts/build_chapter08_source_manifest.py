#!/usr/bin/env python3
"""Build the fail-closed cumulative Chapters 1-8 source and artifact manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

from qa_chapter08_companion import (
    EXPECTED_AUTHORITY_ORDERED_SHA256,
    EXPECTED_CORRECTION_IDS,
    EXPECTED_EXTERNAL_XREFS,
    EXPECTED_INSERTIONS,
    EXPECTED_TERM_IDS,
    FRAGMENTS,
    SOURCE_FILES,
)


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
OUTPUT = ROOT / "qa" / "CHAPTER08_SOURCE_MANIFEST.json"
AUTHORITY_SOURCE = (
    LANE
    / "authority/gvsu-pinned/topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9/source"
)
PRIOR_MANIFEST = "qa/CHAPTER07_SOURCE_MANIFEST.json"
PRIOR_MANIFEST_IDENTITY = {
    "bytes": 36_095,
    "sha256": "4771f640ee8d1c2ed57e8a528dcfead233fab05e5067b7853c3dceb59feffe71",
}
PRIOR_CHAPTERS = tuple(f"chapter_{number:02d}" for number in range(1, 8))
CHAPTER_ORDER = (*PRIOR_CHAPTERS, "chapter_08")
COMPANION_WRAPPER = "companion/chapter_08_open_sets_self_study.ptx"
COMPANION_FRAGMENTS = tuple(f"companion/{name}" for name in FRAGMENTS)
ALIAS_MAP = "backend/chapter_08_entry_aliases.csv"
BACKEND_MANIFEST = "backend/chapter_08_companion_manifest.json"
NEW_ADDITIVE = (
    COMPANION_WRAPPER,
    *COMPANION_FRAGMENTS,
    ALIAS_MAP,
    BACKEND_MANIFEST,
)
CHAPTER_08_IMPLEMENTATION = (
    "README.md",
    "LICENSES.md",
    "assets/o003-readable-layout.css",
    "companion/RIGHTS.md",
    "project.ptx",
    "publication/publication.ptx",
    "publication/zenodo_chapters01_08_metadata.json",
    "requirements.txt",
    "scripts/build_directory_manifest.py",
    "scripts/build_zenodo_boundary_package.py",
    "scripts/qa_source_translation.py",
    "scripts/qa_chapter08_companion.py",
    "scripts/build_chapter08_backend.py",
    "scripts/build_chapter08_source_manifest.py",
    "scripts/build_pretext_pdf_strict.py",
    "scripts/finalize_chapter01_html.py",
    "scripts/inspect_pdf_structure.py",
    "source/chapters_01_08_reader.ptx",
    "xsl/custom-latex.xsl",
    "xsl/topology-style.xsl",
)
EVOLVING_PRIOR_IMPLEMENTATION = {
    "README.md": "advance the truthful cumulative reader boundary to Chapters 1-8",
    "LICENSES.md": "cumulative Chapter 8 collection-rights preservation",
    "assets/o003-readable-layout.css": "cumulative reader layout evolution",
    "companion/RIGHTS.md": "cumulative Chapter 8 companion rights preservation",
    "project.ptx": "addition of cumulative Chapters 1-8 build targets",
    "scripts/qa_source_translation.py": "Chapter 8 source topology and approved-change validation",
    "scripts/build_pretext_pdf_strict.py": "cumulative deterministic PDF builder evolution",
    "xsl/custom-latex.xsl": "cumulative PDF reader implementation evolution",
}
EVOLVING_PRIOR_ADDITIVE = {
    "companion/RIGHTS.md": "cumulative Chapter 8 companion rights preservation",
}
CONTROL_INPUTS = (
    "00_control/TERMINOLOGY.csv",
    "00_control/SOURCE_CORRECTIONS.csv",
)
EXPECTED_PRIOR_SOURCE_FILES = 43
EXPECTED_TOTAL_SOURCE_FILES = 51


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
    path = ROOT / relative
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object in {relative}")
    return value


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
    if posix.is_absolute() or ".." in posix.parts or "\\" in relative:
        raise RuntimeError(f"{label} has unsafe or nonportable path: {value!r}")
    return relative


def assert_identity(label: str, expected: object, current: dict[str, object]) -> None:
    row = require_dict(expected, label)
    if row.get("bytes") != current["bytes"] or row.get("sha256") != current["sha256"]:
        raise RuntimeError(
            f"{label} identity mismatch: expected "
            f"{row.get('bytes')}/{row.get('sha256')}, current "
            f"{current['bytes']}/{current['sha256']}"
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


def current_row_from_public_path(public_path: str) -> dict[str, object]:
    relative = safe_relative_path(public_path, "manifest row")
    return file_row(relative)


def validate_html_tree(
    html_root: Path, manifest: dict[str, Any]
) -> tuple[int, int, int]:
    expected_rows = require_list(manifest.get("files"), "HTML manifest files")
    expected: dict[str, tuple[int, str]] = {}
    for raw in expected_rows:
        row = require_dict(raw, "HTML manifest row")
        relative = safe_relative_path(row.get("path"), "HTML manifest row")
        if relative in expected:
            raise RuntimeError(f"duplicate HTML manifest path: {relative}")
        expected[relative] = (int(row.get("bytes", -1)), str(row.get("sha256", "")))
    # Windows sorts Path objects case-insensitively, while the portable
    # manifest is ordered by exact POSIX path strings.  Use the manifest's
    # ordering rule explicitly so mixed-case upstream asset names compare
    # deterministically on every platform.
    actual_paths = sorted(
        (path for path in html_root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(html_root).as_posix(),
    )
    actual_names = [path.relative_to(html_root).as_posix() for path in actual_paths]
    if actual_names != sorted(expected):
        raise RuntimeError("canonical Chapter 8 HTML tree differs from its manifest")
    total_bytes = 0
    html_files = 0
    for path, relative in zip(actual_paths, actual_names, strict=True):
        current = identity(path)
        expected_bytes, expected_sha = expected[relative]
        if current["bytes"] != expected_bytes or current["sha256"] != expected_sha:
            raise RuntimeError(f"HTML identity mismatch: {relative}")
        total_bytes += int(current["bytes"])
        html_files += relative.lower().endswith(".html")
    if len(actual_paths) != manifest.get("file_count"):
        raise RuntimeError("HTML file count differs from manifest")
    if html_files != manifest.get("html_files"):
        raise RuntimeError("HTML page count differs from manifest")
    if total_bytes != manifest.get("total_bytes"):
        raise RuntimeError("HTML byte total differs from manifest")
    return len(actual_paths), html_files, total_bytes


def assert_no_absolute_paths(value: object, location: str = "manifest") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            assert_no_absolute_paths(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            assert_no_absolute_paths(child, f"{location}[{index}]")
    elif isinstance(value, str):
        if re_absolute(value):
            raise RuntimeError(f"absolute/local path leaked at {location}: {value!r}")


def re_absolute(value: str) -> bool:
    return (
        value.startswith("/")
        or value.startswith("\\\\")
        or (len(value) >= 3 and value[1] == ":" and value[2] in {"\\", "/"})
    )


def main() -> int:
    prior_path = ROOT / PRIOR_MANIFEST
    assert_identity("pinned Chapter 7 source manifest", PRIOR_MANIFEST_IDENTITY, identity(prior_path))
    prior = read_json(PRIOR_MANIFEST)
    require_pass(prior, "Chapter 7 cumulative source manifest")
    if prior.get("boundary") != "chapters_01_07_with_separately_licensed_self_study_companions":
        raise RuntimeError("unexpected Chapter 7 admission boundary")

    prior_source_names: list[str] = []
    translated_source = require_dict(prior.get("translated_source"), "prior translated source")
    inherited_chapters: dict[str, dict[str, Any]] = {}
    for chapter in PRIOR_CHAPTERS:
        chapter_row = require_dict(translated_source.get(chapter), f"prior {chapter}")
        files = require_list(chapter_row.get("files"), f"prior {chapter} files")
        current_files: list[dict[str, object]] = []
        for raw in files:
            row = require_dict(raw, f"prior {chapter} source row")
            relative = safe_relative_path(row.get("path"), f"prior {chapter} source row")
            if not relative.startswith("source/"):
                raise RuntimeError(f"non-source path in prior {chapter}: {relative}")
            name = relative.removeprefix("source/")
            if name in prior_source_names:
                raise RuntimeError(f"duplicate previously admitted source file: {name}")
            current = file_row(relative)
            assert_identity(f"previously admitted source {name}", row, current)
            prior_source_names.append(name)
            current_files.append(current)
        inherited = dict(chapter_row)
        inherited["files"] = current_files
        inherited["admission"] = f"identity preserved from repo/{PRIOR_MANIFEST}"
        inherited_chapters[chapter] = inherited
    if len(prior_source_names) != EXPECTED_PRIOR_SOURCE_FILES:
        raise RuntimeError(
            f"prior source closure changed: {len(prior_source_names)} != {EXPECTED_PRIOR_SOURCE_FILES}"
        )
    if set(prior_source_names).intersection(SOURCE_FILES):
        raise RuntimeError("Chapter 8 source closure overlaps prior chapters")

    source_qa = read_json("qa/CHAPTER08_SOURCE_QA.json")
    companion_qa = read_json("qa/CHAPTER08_COMPANION_QA.json")
    backend = read_json(BACKEND_MANIFEST)
    require_pass(source_qa, "Chapter 8 source QA")
    require_pass(companion_qa, "Chapter 8 companion QA")
    if source_qa.get("failures") != [] or companion_qa.get("failures") != []:
        raise RuntimeError("Chapter 8 source or companion QA records failures")

    source_qa_rows = {
        str(row.get("file")): require_dict(row, "Chapter 8 source-QA file")
        for row in require_list(source_qa.get("files"), "Chapter 8 source-QA files")
    }
    if set(source_qa_rows) != set(SOURCE_FILES):
        raise RuntimeError("Chapter 8 source-QA file closure changed")
    authority_files: list[dict[str, object]] = []
    chapter_files: list[dict[str, object]] = []
    for name in SOURCE_FILES:
        authority = authority_row(name)
        translated = file_row(f"source/{name}")
        row = source_qa_rows[name]
        assert_identity(f"Chapter 8 authority {name}", row.get("authority"), authority)
        assert_identity(f"Chapter 8 translated source {name}", row.get("translated"), translated)
        authority_files.append(authority)
        chapter_files.append(translated)
    authority_combined = combined_named_files(AUTHORITY_SOURCE, SOURCE_FILES)
    if authority_combined != EXPECTED_AUTHORITY_ORDERED_SHA256:
        raise RuntimeError("frozen Chapter 8 authority closure identity changed")
    chapter_combined = combined_named_files(ROOT / "source", SOURCE_FILES)
    if source_qa.get("combined_translated_sha256") != chapter_combined:
        raise RuntimeError("Chapter 8 source-QA combined translated identity is stale")

    insertion_rows = {
        row.get("key"): row
        for row in require_list(
            source_qa.get("approved_element_insertions"),
            "Chapter 8 approved insertions",
        )
    }
    if set(insertion_rows) != set(EXPECTED_INSERTIONS):
        raise RuntimeError("Chapter 8 approved insertion closure changed")
    if source_qa.get("approved_math_changes") != [
        {
            "authority": "<m>\\R^2 \\setminus A</m>",
            "key": "sec_open_sets_exer.ptx:28",
            "translated": "<m>\\R^2 \\setminus S</m>",
        }
    ]:
        raise RuntimeError("Chapter 8 protected-math change is not exactly A to S")
    if set(source_qa.get("approved_external_xref_targets", [])) != EXPECTED_EXTERNAL_XREFS:
        raise RuntimeError("Chapter 8 external-xref admission changed")

    companion_row = file_row(COMPANION_WRAPPER)
    companion_qa_row = file_row("qa/CHAPTER08_COMPANION_QA.json")
    source_qa_row = file_row("qa/CHAPTER08_SOURCE_QA.json")
    backend_row = file_row(BACKEND_MANIFEST)
    alias_row = file_row(ALIAS_MAP)
    assert_identity("Chapter 8 companion", companion_qa.get("companion"), companion_row)
    assert_identity("Chapter 8 source-QA receipt", companion_qa.get("source_qa"), source_qa_row)
    fragment_rows = rows_by_path(companion_qa.get("fragments"), "Chapter 8 fragments")
    expected_fragment_names = {f"companion/{name}" for name in FRAGMENTS}
    if set(fragment_rows) != expected_fragment_names:
        raise RuntimeError("Chapter 8 companion fragment closure changed")
    for relative, row in fragment_rows.items():
        assert_identity(f"Chapter 8 fragment {relative}", row, file_row(relative))

    if backend.get("schema_version") != "2.0.0" or backend.get("locale") != "id-ID":
        raise RuntimeError("Chapter 8 backend schema or locale changed")
    component = require_dict(backend.get("component"), "Chapter 8 backend component")
    assert_path("Chapter 8 backend component", component.get("path"), f"repo/{COMPANION_WRAPPER}")
    assert_identity("Chapter 8 backend component", component.get("identity"), companion_row)
    backend_alias = require_dict(component.get("entry_alias_map"), "Chapter 8 backend aliases")
    assert_path("Chapter 8 backend aliases", backend_alias.get("path"), f"repo/{ALIAS_MAP}")
    assert_identity("Chapter 8 backend aliases", backend_alias, alias_row)
    backend_source_qa = require_dict(backend.get("translated_unit_source_qa"), "backend source QA")
    assert_path("backend source QA", backend_source_qa.get("path"), "repo/qa/CHAPTER08_SOURCE_QA.json")
    assert_identity("backend source QA", backend_source_qa, source_qa_row)
    if backend_source_qa.get("combined_translated_sha256") != chapter_combined:
        raise RuntimeError("backend Chapter 8 translated-source identity is stale")
    backend_companion_qa = require_dict(backend.get("companion_qa"), "backend companion QA")
    assert_path("backend companion QA", backend_companion_qa.get("path"), "repo/qa/CHAPTER08_COMPANION_QA.json")
    assert_identity("backend companion QA", backend_companion_qa, companion_qa_row)

    entry_counts = require_dict(companion_qa.get("entry_counts"), "companion entry counts")
    if entry_counts != {
        "source_prompt_guide": 55,
        "activity_or_task_guide": 30,
        "exercise_prompt_guide": 25,
        "mastery_check": 6,
        "total": 61,
    }:
        raise RuntimeError("Chapter 8 companion entry-count contract changed")
    reveal_counts = require_dict(companion_qa.get("reveal_counts"), "companion reveals")
    surface_counts = require_dict(companion_qa.get("surface_counts"), "companion surfaces")
    for kind in ("statement", "hint", "answer", "solution"):
        if surface_counts.get(kind) != 61:
            raise RuntimeError(f"Chapter 8 companion lacks complete {kind} surfaces")
    for kind in ("hint", "answer", "solution"):
        if reveal_counts.get(kind) != 61:
            raise RuntimeError(f"Chapter 8 companion lacks complete {kind} reveals")
    coverage = require_dict(backend.get("coverage_contract"), "backend coverage")
    expected_coverage = {
        "source_prompt_guides": 55,
        "activity_or_task_guides": 30,
        "exercise_prompt_guides": 25,
        "mastery_checks": 6,
        "total_entries": 61,
        "statements": 61,
        "hints": 61,
        "answers": 61,
        "solutions": 61,
        "active_images_with_id_ID_descriptions": 0,
        "remote_or_interactive_surfaces": 0,
        "source_correction_records": 9,
    }
    for key, expected in expected_coverage.items():
        if coverage.get(key) != expected:
            raise RuntimeError(f"Chapter 8 backend coverage is stale for {key}")
    if coverage.get("all_entries_have_statement_hint_answer_solution") is not True:
        raise RuntimeError("Chapter 8 backend complete-surface contract is false")

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
                }
            )
        inherited_additive_paths.add(relative)
        inherited_additive.append(current)
    if inherited_additive_paths.intersection(NEW_ADDITIVE):
        raise RuntimeError("Chapter 8 additive component duplicates a prior component")

    prior_controls = rows_by_path(prior.get("control_inputs"), "prior control inputs")
    if set(prior_controls) != set(CONTROL_INPUTS):
        raise RuntimeError("prior control-input closure changed")
    inherited_control_updates = [
        {
            "path": relative,
            "previous_bytes": prior_controls[relative].get("bytes"),
            "previous_sha256": prior_controls[relative].get("sha256"),
            "current": current_controls[relative],
            "reason": "append-only cumulative terminology/correction ledger update",
        }
        for relative in CONTROL_INPUTS
    ]

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
    for relative in CHAPTER_08_IMPLEMENTATION:
        implementation_by_path[relative] = file_row(relative)

    html_manifest = read_json("qa/CHAPTER08_HTML_MANIFEST.json")
    html_run_1 = read_json("qa/CHAPTER08_HTML_MANIFEST_RUN1.json")
    html_run_2 = read_json("qa/CHAPTER08_HTML_MANIFEST_RUN2.json")
    html_qa = read_json("qa/CHAPTER08_HTML_QA.json")
    browser_qa = read_json("qa/CHAPTER08_BROWSER_QA.json")
    require_pass(html_qa, "Chapter 8 HTML QA")
    require_pass(browser_qa, "Chapter 8 browser QA")
    if browser_qa.get("failures") != []:
        raise RuntimeError("Chapter 8 browser QA records failures")
    assert_path(
        "Chapter 8 browser surface",
        browser_qa.get("surface"),
        "output/chapters01-08-html",
    )
    if (
        browser_qa.get("canonical_html_manifest_sha256")
        != html_manifest.get("canonical_manifest_sha256")
    ):
        raise RuntimeError("Chapter 8 browser QA targets a different HTML tree")

    browser_evidence_rows: list[dict[str, object]] = []
    for section, relative in (
        ("desktop", "qa/browser-evidence/CHAPTER08_DESKTOP_1280x900.jpg"),
        (
            "staged_disclosure",
            "qa/browser-evidence/CHAPTER08_DISCLOSURE_1280x900.jpg",
        ),
        (
            "interior_macro_repair",
            "qa/browser-evidence/CHAPTER08_INTERIOR_MACRO_1280x900.jpg",
        ),
        ("mobile", "qa/browser-evidence/CHAPTER08_MOBILE_390x844_DRAWER.jpg"),
    ):
        section_row = require_dict(browser_qa.get(section), f"browser QA {section}")
        if section_row.get("visual_result") != "pass":
            raise RuntimeError(f"browser QA {section} did not pass")
        evidence = require_dict(
            section_row.get("evidence"), f"browser QA {section} evidence"
        )
        assert_path(f"browser QA {section} evidence", evidence.get("path"), relative)
        current = file_row(relative)
        assert_identity(f"browser QA {section} evidence", evidence, current)
        browser_evidence_rows.append(current)
    canonical_files = require_list(html_manifest.get("files"), "canonical HTML files")
    identity_keys = ("file_count", "html_files", "total_bytes", "canonical_manifest_sha256")
    for label, report in (("HTML run 1", html_run_1), ("HTML run 2", html_run_2)):
        if report.get("files") != canonical_files:
            raise RuntimeError(f"{label} file identities differ from canonical HTML")
        for key in identity_keys:
            if report.get(key) != html_manifest.get(key):
                raise RuntimeError(f"{label} differs from canonical HTML for {key}")
    for key in identity_keys:
        if html_qa.get(key) != html_manifest.get(key):
            raise RuntimeError(f"HTML QA differs from canonical HTML for {key}")
    html_root = ROOT / "output" / "chapters01-08-html"
    html_file_count, html_files, html_bytes = validate_html_tree(html_root, html_manifest)

    pdf_run_1 = read_json("qa/CHAPTER08_PDF_RUN1_HASH.json")
    pdf_run_2 = read_json("qa/CHAPTER08_PDF_RUN2_HASH.json")
    pdf_structure = read_json("qa/CHAPTER08_PDF_STRUCTURE.json")
    pdf_qa = read_json("qa/CHAPTER08_PDF_VISUAL_QA.json")
    require_pass(pdf_run_1, "Chapter 8 PDF run 1")
    require_pass(pdf_run_2, "Chapter 8 PDF run 2")
    require_pass(pdf_structure, "Chapter 8 PDF structure")
    require_pass(pdf_qa, "Chapter 8 PDF visual QA")
    pdf_relative = "output/chapters01-08-pdf/chapters_01_08_reader.pdf"
    pdf_row = file_row(pdf_relative)
    assert_identity("Chapter 8 PDF run 1", pdf_run_1, pdf_row)
    assert_identity("Chapter 8 PDF run 2", pdf_run_2, pdf_row)
    pdf_structure_artifact = require_dict(
        pdf_structure.get("artifact"), "Chapter 8 PDF structure identity"
    )
    assert_path(
        "Chapter 8 PDF structure identity",
        pdf_structure_artifact.get("path"),
        pdf_relative,
    )
    assert_identity("Chapter 8 PDF structure identity", pdf_structure_artifact, pdf_row)
    pdf_visual = require_dict(pdf_qa.get("pdf"), "Chapter 8 PDF visual identity")
    assert_path("Chapter 8 PDF visual identity", pdf_visual.get("path"), pdf_relative)
    assert_identity("Chapter 8 PDF visual identity", pdf_visual, pdf_row)
    if pdf_qa.get("sha256") != pdf_row["sha256"]:
        raise RuntimeError("Chapter 8 PDF visual-QA top-level hash is stale")
    if not isinstance(pdf_qa.get("pages"), int) or int(pdf_qa["pages"]) <= 0:
        raise RuntimeError("Chapter 8 PDF visual QA has no valid page count")

    all_source_names = [*prior_source_names, *SOURCE_FILES]
    if len(all_source_names) != EXPECTED_TOTAL_SOURCE_FILES or len(set(all_source_names)) != EXPECTED_TOTAL_SOURCE_FILES:
        raise RuntimeError("cumulative Chapters 1-8 source closure is not exactly 51 unique files")
    cumulative_combined = combined_named_files(ROOT / "source", all_source_names)
    chapter_08 = {
        "authority_combined_sha256": authority_combined,
        "authority_files": authority_files,
        "combined_sha256": chapter_combined,
        "files": chapter_files,
        "source_qa": "repo/qa/CHAPTER08_SOURCE_QA.json",
        "activities_and_explorations": 8,
        "exercises": 12,
        "tasks": 53,
        "assessable_prompts": 55,
        "xml_ids": source_qa.get("xml_ids"),
        "xrefs": source_qa.get("xrefs"),
        "approved_external_xrefs": sorted(EXPECTED_EXTERNAL_XREFS),
    }
    translated = {
        **inherited_chapters,
        "chapter_08": chapter_08,
        "combined_algorithm": "SHA-256 over each ordered source filename, one NUL byte, then exact file bytes",
        "cumulative_combined_sha256": cumulative_combined,
    }

    qa_receipts = {
        "prior_source_manifest": file_row(PRIOR_MANIFEST),
        "source": source_qa_row,
        "companion": companion_qa_row,
        "backend": backend_row,
        "html_manifest": file_row("qa/CHAPTER08_HTML_MANIFEST.json"),
        "html_run_1": file_row("qa/CHAPTER08_HTML_MANIFEST_RUN1.json"),
        "html_run_2": file_row("qa/CHAPTER08_HTML_MANIFEST_RUN2.json"),
        "html": file_row("qa/CHAPTER08_HTML_QA.json"),
        "browser": file_row("qa/CHAPTER08_BROWSER_QA.json"),
        "pdf_run_1": file_row("qa/CHAPTER08_PDF_RUN1_HASH.json"),
        "pdf_run_2": file_row("qa/CHAPTER08_PDF_RUN2_HASH.json"),
        "pdf_structure": file_row("qa/CHAPTER08_PDF_STRUCTURE.json"),
        "pdf": file_row("qa/CHAPTER08_PDF_VISUAL_QA.json"),
    }
    offline_closed = not bool(html_qa.get("external_hosts"))
    caveats: list[str] = []
    if not offline_closed:
        caveats.append(
            "The cumulative HTML reader still has recorded remote dependencies; whole-edition offline closure remains a release gate."
        )
    if pdf_qa.get("tagged") is not True:
        caveats.append("PDF is not tagged; HTML remains the primary accessible surface.")
    caveats.append(
        "Whole-book figure provenance remains a final-release gate; Chapter 8 introduces no active figures or remote interactive surfaces."
    )

    rights_boundary = require_dict(companion_qa.get("rights_boundary"), "companion rights boundary")
    rights_row = file_row("companion/RIGHTS.md")
    licenses_row = file_row("LICENSES.md")
    assert_identity("companion rights note", rights_boundary.get("companion_rights"), rights_row)
    assert_identity("collection licenses", rights_boundary.get("collection_licenses"), licenses_row)
    if rights_boundary.get("translated_spine_license") != "CC-BY-NC-SA-3.0":
        raise RuntimeError("translated-spine license boundary changed")
    if rights_boundary.get("companion_license") != "CC-BY-4.0":
        raise RuntimeError("companion license boundary changed")

    manifest = {
        "schema_version": 1,
        "lane": "O003/C90",
        "locale": "id-ID",
        "boundary": "chapters_01_08_with_separately_licensed_self_study_companions",
        "status": "pass",
        "prior_admission": {
            **file_row(PRIOR_MANIFEST),
            "admission_basis": "locally validated Chapter 7 source manifest",
            "locally_admitted": True,
            "published_identity_pinned": False,
            "publication_status": "not_publicly_pushed",
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
            "chapter_08_ordered_sha256": authority_combined,
        },
        "translated_source": translated,
        "additive_components": inherited_additive + [file_row(path) for path in NEW_ADDITIVE],
        "inherited_additive_updates": inherited_additive_updates,
        "control_inputs": [current_controls[path] for path in CONTROL_INPUTS],
        "inherited_control_updates": inherited_control_updates,
        "production_implementation": [
            implementation_by_path[path] for path in sorted(implementation_by_path)
        ],
        "inherited_implementation_updates": inherited_implementation_updates,
        "chapter_08_identity_bundle": {
            "source_qa": source_qa_row,
            "companion_qa": companion_qa_row,
            "backend": backend_row,
            "companion_wrapper": companion_row,
            "companion_fragments": [file_row(path) for path in COMPANION_FRAGMENTS],
            "entry_alias_map": alias_row,
            "cumulative_reader_wrapper": file_row("source/chapters_01_08_reader.ptx"),
            "project": file_row("project.ptx"),
            "rights_note": rights_row,
            "collection_licenses": licenses_row,
        },
        "companion_coverage": {
            "contract": coverage,
            "entry_counts": entry_counts,
            "source_prompt_counts": companion_qa.get("source_prompt_counts"),
            "reveal_counts": reveal_counts,
            "described_images": require_dict(companion_qa.get("assets"), "companion assets").get("described_images"),
            "remote_or_interactive_surfaces": 0,
        },
        "rights": {
            "translated_gvsu_spine": "CC-BY-NC-SA-3.0 (conservative determination)",
            "original_self_study_companions": "CC-BY-4.0",
            "collection_policy": "per-component rights; no flattened license",
            "rights_note": rights_row,
            "collection_licenses": licenses_row,
            "non_endorsement": True,
        },
        "reader_artifacts": {
            "html": {
                "path": "repo/output/chapters01-08-html",
                "file_count": html_file_count,
                "html_files": html_files,
                "bytes": html_bytes,
                "canonical_manifest_sha256": html_manifest.get("canonical_manifest_sha256"),
                "manifest": qa_receipts["html_manifest"],
                "deterministic_run_1": qa_receipts["html_run_1"],
                "deterministic_run_2": qa_receipts["html_run_2"],
                "qa": qa_receipts["html"],
                "browser_qa": qa_receipts["browser"],
                "browser_evidence": browser_evidence_rows,
                "offline_closed": offline_closed,
            },
            "pdf": {
                **pdf_row,
                "pages": pdf_qa["pages"],
                "tagged": pdf_qa.get("tagged"),
                "deterministic_run_1": qa_receipts["pdf_run_1"],
                "deterministic_run_2": qa_receipts["pdf_run_2"],
                "structure_qa": qa_receipts["pdf_structure"],
                "visual_qa": qa_receipts["pdf"],
            },
        },
        "qa_receipts": qa_receipts,
        "known_caveats": caveats,
    }
    assert_no_absolute_paths(manifest)
    OUTPUT.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "output": str(OUTPUT),
                "bytes": OUTPUT.stat().st_size,
                "sha256": sha256(OUTPUT),
                "chapter_08_combined_sha256": chapter_combined,
                "cumulative_combined_sha256": cumulative_combined,
                "source_files": len(all_source_names),
                "html_files": html_file_count,
                "pdf_pages": pdf_qa["pages"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
