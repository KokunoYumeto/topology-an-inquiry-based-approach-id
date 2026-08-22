#!/usr/bin/env python3
"""Build the fail-closed cumulative Chapters 1-9 source/artifact manifest.

The source, companion, backend, and deterministic HTML tree are mandatory.
Browser and PDF admission evidence is incorporated and validated when present;
until then the manifest records exact current artifacts and explicit pending
gates instead of claiming a completely admitted reader boundary.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

from qa_chapter09_companion import (
    EXPECTED_AUTHORITY_ORDERED_SHA256,
    EXPECTED_AUTHORITY_RAW_SHA256,
    EXPECTED_CORRECTION_IDS,
    EXPECTED_EXTERNAL_XREFS,
    EXPECTED_INSERTIONS,
    EXPECTED_TERM_IDS,
    FRAGMENTS,
    SOURCE_FILES,
)


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
OUTPUT = ROOT / "qa" / "CHAPTER09_SOURCE_MANIFEST.json"
AUTHORITY_SOURCE = (
    LANE
    / "authority/gvsu-pinned/topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9/source"
)
PRIOR_MANIFEST = "qa/CHAPTER08_SOURCE_MANIFEST.json"
PRIOR_MANIFEST_IDENTITY = {
    "bytes": 44_745,
    "sha256": "5a324f70f61d6e52b69ce9b1245ded596c171b769155b1145330b311580e061d",
}
PRIOR_CHAPTERS = tuple(f"chapter_{number:02d}" for number in range(1, 9))
COMPANION_WRAPPER = "companion/chapter_09_sequences_self_study.ptx"
COMPANION_FRAGMENTS = tuple(f"companion/{name}" for name in FRAGMENTS)
ALIAS_MAP = "backend/chapter_09_entry_aliases.csv"
BACKEND_MANIFEST = "backend/chapter_09_companion_manifest.json"
NEW_ADDITIVE = (
    COMPANION_WRAPPER,
    *COMPANION_FRAGMENTS,
    ALIAS_MAP,
    BACKEND_MANIFEST,
)
CHAPTER_09_IMPLEMENTATION = (
    "project.ptx",
    "scripts/qa_chapter09_companion.py",
    "scripts/build_chapter09_backend.py",
    "scripts/build_chapter09_source_manifest.py",
    "scripts/qa_html_tree.py",
    "source/chapters_01_09_reader.ptx",
)
EVOLVING_PRIOR_IMPLEMENTATION = {
    "README.md": "advance the truthful cumulative reader boundary to Chapters 1-9",
    "LICENSES.md": "cumulative Chapter 9 collection-rights preservation",
    "assets/o003-readable-layout.css": "cumulative reader layout evolution",
    "companion/RIGHTS.md": "cumulative Chapter 9 companion rights preservation",
    "project.ptx": "addition of cumulative Chapters 1-9 build targets",
    "scripts/qa_source_translation.py": "Chapter 9 source topology and approved-change validation",
    "scripts/build_pretext_pdf_strict.py": "cumulative deterministic PDF builder evolution",
    "scripts/finalize_chapter01_html.py": "cumulative finalized HTML reader evolution",
    "xsl/custom-latex.xsl": "cumulative PDF reader implementation evolution",
    "xsl/topology-style.xsl": "cumulative HTML reader implementation evolution",
}
EVOLVING_PRIOR_ADDITIVE = {
    "companion/RIGHTS.md": "cumulative Chapter 9 companion rights preservation",
}
CONTROL_INPUTS = (
    "00_control/TERMINOLOGY.csv",
    "00_control/SOURCE_CORRECTIONS.csv",
)
EXPECTED_PRIOR_SOURCE_FILES = 51
EXPECTED_TOTAL_SOURCE_FILES = 56
HTML_RUN_1 = "qa/CHAPTER09_HTML_MANIFEST_RUN1.json"
HTML_RUN_2 = "qa/CHAPTER09_HTML_MANIFEST_RUN2.json"
HTML_CANONICAL = "qa/CHAPTER09_HTML_MANIFEST.json"
HTML_QA = "qa/CHAPTER09_HTML_QA.json"
HTML_ROOT = "output/chapters01-09-html"
PDF_RELATIVE = "output/chapters01-09-pdf/chapters_01_09_reader.pdf"
PDF_EVIDENCE = {
    "deterministic_run_1": "qa/CHAPTER09_PDF_RUN1_HASH.json",
    "deterministic_run_2": "qa/CHAPTER09_PDF_RUN2_HASH.json",
    "structure_qa": "qa/CHAPTER09_PDF_STRUCTURE.json",
    "visual_qa": "qa/CHAPTER09_PDF_VISUAL_QA.json",
}


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
        raise RuntimeError(f"canonical Chapter 9 HTML closure differs: missing={missing}, extra={extra}")
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


def validate_reported_evidence(value: object, label: str) -> list[dict[str, object]]:
    """Validate all nested evidence identity rows in a browser report."""
    found: list[dict[str, object]] = []
    if isinstance(value, dict):
        if "path" in value and "bytes" in value and "sha256" in value:
            relative = safe_relative_path(value["path"], label)
            current = file_row(relative)
            assert_identity(label, value, current)
            found.append(current)
        else:
            for child in value.values():
                found.extend(validate_reported_evidence(child, label))
    elif isinstance(value, list):
        for child in value:
            found.extend(validate_reported_evidence(child, label))
    unique: dict[str, dict[str, object]] = {}
    for row in found:
        unique[str(row["path"])] = row
    return [unique[path] for path in sorted(unique)]


def main() -> int:
    prior_path = ROOT / PRIOR_MANIFEST
    assert_identity("pinned Chapter 8 source manifest", PRIOR_MANIFEST_IDENTITY, identity(prior_path))
    prior = read_json(PRIOR_MANIFEST)
    require_pass(prior, "Chapter 8 cumulative source manifest")
    if prior.get("boundary") != "chapters_01_08_with_separately_licensed_self_study_companions":
        raise RuntimeError("unexpected Chapter 8 admission boundary")

    prior_source_names: list[str] = []
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
            assert_identity(f"previously admitted source {name}", row, current)
            prior_source_names.append(name)
            current_files.append(current)
        inherited = dict(chapter_row)
        inherited["files"] = current_files
        inherited["admission"] = f"identity preserved from repo/{PRIOR_MANIFEST}"
        inherited_chapters[chapter] = inherited
    if len(prior_source_names) != EXPECTED_PRIOR_SOURCE_FILES:
        raise RuntimeError(f"prior source closure changed: {len(prior_source_names)} != {EXPECTED_PRIOR_SOURCE_FILES}")
    if set(prior_source_names).intersection(SOURCE_FILES):
        raise RuntimeError("Chapter 9 source closure overlaps prior chapters")

    source_qa = read_json("qa/CHAPTER09_SOURCE_QA.json")
    companion_qa = read_json("qa/CHAPTER09_COMPANION_QA.json")
    backend = read_json(BACKEND_MANIFEST)
    require_pass(source_qa, "Chapter 9 source QA")
    require_pass(companion_qa, "Chapter 9 companion QA")
    if source_qa.get("failures") != [] or companion_qa.get("failures") != []:
        raise RuntimeError("Chapter 9 source or companion QA records failures")

    source_qa_rows = {
        str(row.get("file")): require_dict(row, "Chapter 9 source-QA file")
        for row in require_list(source_qa.get("files"), "Chapter 9 source-QA files")
    }
    if set(source_qa_rows) != set(SOURCE_FILES):
        raise RuntimeError("Chapter 9 source-QA file closure changed")
    authority_files: list[dict[str, object]] = []
    chapter_files: list[dict[str, object]] = []
    source_counts: Counter[str] = Counter()
    for name in SOURCE_FILES:
        authority = authority_row(name)
        translated = file_row(f"source/{name}")
        row = source_qa_rows[name]
        assert_identity(f"Chapter 9 authority {name}", row.get("authority"), authority)
        assert_identity(f"Chapter 9 translated source {name}", row.get("translated"), translated)
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
        raise RuntimeError("frozen Chapter 9 ordered authority closure changed")
    if authority_raw != EXPECTED_AUTHORITY_RAW_SHA256:
        raise RuntimeError("frozen Chapter 9 raw authority closure changed")
    chapter_combined = combined_named_files(ROOT / "source", SOURCE_FILES)
    if source_qa.get("combined_translated_sha256") != chapter_combined:
        raise RuntimeError("Chapter 9 source-QA combined translated identity is stale")
    if set(source_qa.get("approved_external_xref_targets", [])) != EXPECTED_EXTERNAL_XREFS:
        raise RuntimeError("Chapter 9 external-xref admission changed")
    insertion_rows = {
        row.get("key"): row
        for row in require_list(source_qa.get("approved_element_insertions"), "Chapter 9 insertions")
    }
    if set(insertion_rows) != set(EXPECTED_INSERTIONS):
        raise RuntimeError("Chapter 9 approved insertion closure changed")
    if len(require_list(source_qa.get("approved_math_changes"), "Chapter 9 math changes")) != 9:
        raise RuntimeError("Chapter 9 approved math-change closure is not exactly nine")

    companion_row = file_row(COMPANION_WRAPPER)
    source_qa_row = file_row("qa/CHAPTER09_SOURCE_QA.json")
    companion_qa_row = file_row("qa/CHAPTER09_COMPANION_QA.json")
    backend_row = file_row(BACKEND_MANIFEST)
    alias_row = file_row(ALIAS_MAP)
    assert_identity("Chapter 9 companion", companion_qa.get("companion"), companion_row)
    assert_identity("Chapter 9 source-QA receipt", companion_qa.get("source_qa"), source_qa_row)
    fragment_rows = rows_by_path(companion_qa.get("fragments"), "Chapter 9 fragments")
    if set(fragment_rows) != set(COMPANION_FRAGMENTS):
        raise RuntimeError("Chapter 9 companion fragment closure changed")
    for relative, row in fragment_rows.items():
        assert_identity(f"Chapter 9 fragment {relative}", row, file_row(relative))

    if backend.get("schema_version") != "2.0.0" or backend.get("locale") != "id-ID":
        raise RuntimeError("Chapter 9 backend schema or locale changed")
    component = require_dict(backend.get("component"), "Chapter 9 backend component")
    assert_path("Chapter 9 backend component", component.get("path"), f"repo/{COMPANION_WRAPPER}")
    assert_identity("Chapter 9 backend component", component.get("identity"), companion_row)
    backend_alias = require_dict(component.get("entry_alias_map"), "Chapter 9 backend aliases")
    assert_path("Chapter 9 backend aliases", backend_alias.get("path"), f"repo/{ALIAS_MAP}")
    assert_identity("Chapter 9 backend aliases", backend_alias, alias_row)
    backend_source_qa = require_dict(backend.get("translated_unit_source_qa"), "backend source QA")
    assert_path("backend source QA", backend_source_qa.get("path"), "repo/qa/CHAPTER09_SOURCE_QA.json")
    assert_identity("backend source QA", backend_source_qa, source_qa_row)
    if backend_source_qa.get("combined_translated_sha256") != chapter_combined:
        raise RuntimeError("backend Chapter 9 translated-source identity is stale")
    backend_companion_qa = require_dict(backend.get("companion_qa"), "backend companion QA")
    assert_path("backend companion QA", backend_companion_qa.get("path"), "repo/qa/CHAPTER09_COMPANION_QA.json")
    assert_identity("backend companion QA", backend_companion_qa, companion_qa_row)

    entry_counts = require_dict(companion_qa.get("entry_counts"), "companion entry counts")
    expected_entry_counts = {
        "source_prompt_guide": 44,
        "activity_or_task_guide": 16,
        "exercise_prompt_guide": 28,
        "mastery_check": 6,
        "total": 50,
    }
    if entry_counts != expected_entry_counts:
        raise RuntimeError("Chapter 9 companion entry-count contract changed")
    reveal_counts = require_dict(companion_qa.get("reveal_counts"), "companion reveals")
    surface_counts = require_dict(companion_qa.get("surface_counts"), "companion surfaces")
    for kind in ("statement", "hint", "answer", "solution"):
        if surface_counts.get(kind) != 50:
            raise RuntimeError(f"Chapter 9 companion lacks complete {kind} surfaces")
    for kind in ("hint", "answer", "solution"):
        if reveal_counts.get(kind) != 50:
            raise RuntimeError(f"Chapter 9 companion lacks complete {kind} reveals")
    coverage = require_dict(backend.get("coverage_contract"), "backend coverage")
    expected_coverage = {
        "source_prompt_guides": 44,
        "activity_or_task_guides": 16,
        "exercise_prompt_guides": 28,
        "mastery_checks": 6,
        "total_entries": 50,
        "statements": 50,
        "hints": 50,
        "answers": 50,
        "solutions": 50,
        "active_images_with_id_ID_descriptions": 1,
        "remote_or_interactive_surfaces": 0,
        "source_correction_records": 15,
    }
    for key, expected in expected_coverage.items():
        if coverage.get(key) != expected:
            raise RuntimeError(f"Chapter 9 backend coverage is stale for {key}")
    if coverage.get("all_entries_have_statement_hint_answer_solution") is not True:
        raise RuntimeError("Chapter 9 backend complete-surface contract is false")

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
        raise RuntimeError("Chapter 9 additive component duplicates a prior component")

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
    for relative in CHAPTER_09_IMPLEMENTATION:
        implementation_by_path[relative] = file_row(relative)

    html_run_1 = read_json(HTML_RUN_1)
    html_run_2 = read_json(HTML_RUN_2)
    html_qa = read_json(HTML_QA)
    require_pass(html_qa, "Chapter 9 HTML QA")
    if html_qa.get("failures") != []:
        raise RuntimeError("Chapter 9 HTML QA records failures")
    identity_keys = ("file_count", "html_files", "total_bytes", "canonical_manifest_sha256")
    if html_run_1.get("files") != html_run_2.get("files"):
        raise RuntimeError("Chapter 9 deterministic HTML runs have different file identities")
    for key in identity_keys:
        if html_run_1.get(key) != html_run_2.get(key) or html_qa.get(key) != html_run_2.get(key):
            raise RuntimeError(f"Chapter 9 HTML evidence differs for {key}")
    canonical_relative = HTML_CANONICAL if (ROOT / HTML_CANONICAL).is_file() else HTML_RUN_2
    html_manifest = read_json(canonical_relative)
    if html_manifest.get("files") != html_run_2.get("files"):
        raise RuntimeError("canonical Chapter 9 HTML identities differ from deterministic run 2")
    for key in identity_keys:
        if html_manifest.get(key) != html_run_2.get(key):
            raise RuntimeError(f"canonical Chapter 9 HTML differs for {key}")
    html_file_count, html_files, html_bytes = validate_html_tree(ROOT / HTML_ROOT, html_manifest)

    pending_evidence: list[str] = []
    browser_relative = "qa/CHAPTER09_BROWSER_QA.json"
    browser: dict[str, object] = {"status": "pending", "required_receipt": f"repo/{browser_relative}"}
    if (ROOT / browser_relative).is_file():
        browser_qa = read_json(browser_relative)
        require_pass(browser_qa, "Chapter 9 browser QA")
        if browser_qa.get("failures") != []:
            raise RuntimeError("Chapter 9 browser QA records failures")
        assert_path("Chapter 9 browser surface", browser_qa.get("surface"), HTML_ROOT)
        if browser_qa.get("canonical_html_manifest_sha256") != html_manifest.get("canonical_manifest_sha256"):
            raise RuntimeError("Chapter 9 browser QA targets a different HTML tree")
        browser = {
            "status": "pass",
            "receipt": file_row(browser_relative),
            "evidence": validate_reported_evidence(browser_qa, "Chapter 9 browser evidence"),
        }
    else:
        pending_evidence.append(browser_relative)

    pdf_path = ROOT / PDF_RELATIVE
    pdf: dict[str, object] = {
        "status": "pending",
        "path": f"repo/{PDF_RELATIVE}",
        "required_receipts": [f"repo/{path}" for path in PDF_EVIDENCE.values()],
    }
    if pdf_path.is_file():
        pdf["current_unadmitted_artifact"] = file_row(PDF_RELATIVE)
    build_log = "qa/CHAPTER09_PDF_BUILD_RUN1.log"
    if (ROOT / build_log).is_file():
        pdf["preliminary_build_log"] = file_row(build_log)
    missing_pdf = [relative for relative in PDF_EVIDENCE.values() if not (ROOT / relative).is_file()]
    if missing_pdf:
        pending_evidence.extend(missing_pdf)
    else:
        reports = {key: read_json(relative) for key, relative in PDF_EVIDENCE.items()}
        for key, report in reports.items():
            require_pass(report, f"Chapter 9 PDF {key}")
        pdf_row = file_row(PDF_RELATIVE)
        assert_identity("Chapter 9 PDF run 1", reports["deterministic_run_1"], pdf_row)
        assert_identity("Chapter 9 PDF run 2", reports["deterministic_run_2"], pdf_row)
        structure_artifact = require_dict(reports["structure_qa"].get("artifact"), "PDF structure artifact")
        assert_path("Chapter 9 PDF structure artifact", structure_artifact.get("path"), PDF_RELATIVE)
        assert_identity("Chapter 9 PDF structure artifact", structure_artifact, pdf_row)
        visual_pdf = require_dict(reports["visual_qa"].get("pdf"), "PDF visual artifact")
        assert_path("Chapter 9 PDF visual artifact", visual_pdf.get("path"), PDF_RELATIVE)
        assert_identity("Chapter 9 PDF visual artifact", visual_pdf, pdf_row)
        if reports["visual_qa"].get("sha256") != pdf_row["sha256"]:
            raise RuntimeError("Chapter 9 PDF visual-QA top-level hash is stale")
        pages = reports["visual_qa"].get("pages")
        if not isinstance(pages, int) or pages <= 0:
            raise RuntimeError("Chapter 9 PDF visual QA has no valid page count")
        pdf = {
            **pdf_row,
            "status": "pass",
            "pages": pages,
            "tagged": reports["visual_qa"].get("tagged"),
            **{key: file_row(relative) for key, relative in PDF_EVIDENCE.items()},
        }

    all_source_names = [*prior_source_names, *SOURCE_FILES]
    if len(all_source_names) != EXPECTED_TOTAL_SOURCE_FILES or len(set(all_source_names)) != EXPECTED_TOTAL_SOURCE_FILES:
        raise RuntimeError("cumulative Chapters 1-9 source closure is not exactly 56 unique files")
    cumulative_combined = combined_named_files(ROOT / "source", all_source_names)
    chapter_09 = {
        "authority_combined_sha256": authority_combined,
        "authority_raw_concatenated_sha256": authority_raw,
        "authority_files": authority_files,
        "combined_sha256": chapter_combined,
        "files": chapter_files,
        "source_qa": "repo/qa/CHAPTER09_SOURCE_QA.json",
        **dict(source_counts),
        "assessable_prompts": 44,
        "xml_ids": source_qa.get("xml_ids"),
        "xrefs": source_qa.get("xrefs"),
        "approved_external_xrefs": sorted(EXPECTED_EXTERNAL_XREFS),
    }
    translated = {
        **inherited_chapters,
        "chapter_09": chapter_09,
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

    asset_rows: list[dict[str, object]] = []
    for asset in require_list(backend.get("assets"), "backend assets"):
        asset_row = require_dict(asset, "backend asset")
        for raw_format in require_list(asset_row.get("formats"), "backend asset formats"):
            format_row = require_dict(raw_format, "backend asset format")
            relative = safe_relative_path(format_row.get("path"), "backend asset format")
            current = file_row(relative)
            assert_identity(f"Chapter 9 asset {relative}", format_row, current)
            asset_rows.append(current)

    correction_statuses = Counter(
        str(require_dict(row, "source correction").get("status"))
        for row in require_list(backend.get("source_corrections"), "source corrections")
    )
    if correction_statuses != Counter({"verified": 15}):
        raise RuntimeError(
            "Chapter 9 correction closure is not exactly 15 verified records: "
            f"{dict(sorted(correction_statuses.items()))}"
        )
    caveats = [
        "The cumulative HTML reader retains recorded remote dependencies; whole-edition offline closure remains a release gate.",
        "Whole-book figure provenance remains a final-release gate; the Chapter 9 figure is described in id-ID but is not relicensed.",
    ]
    if pdf.get("status") != "pass":
        caveats.append("The current Chapter 9 PDF is not admitted until both deterministic hashes, structure QA, and all-page visual QA pass.")
    elif pdf.get("tagged") is not True:
        caveats.append("PDF is not tagged; HTML remains the primary accessible surface.")
    if browser.get("status") != "pass":
        caveats.append("Responsive layout and staged-disclosure browser evidence remains pending.")

    qa_receipts = {
        "prior_source_manifest": file_row(PRIOR_MANIFEST),
        "source": source_qa_row,
        "companion": companion_qa_row,
        "backend": backend_row,
        "html_manifest": file_row(canonical_relative),
        "html_run_1": file_row(HTML_RUN_1),
        "html_run_2": file_row(HTML_RUN_2),
        "html": file_row(HTML_QA),
    }
    manifest_status = "pass" if not pending_evidence else "source_boundary_pass_reader_evidence_pending"
    manifest = {
        "schema_version": 1,
        "lane": "O003/C90",
        "locale": "id-ID",
        "boundary": "chapters_01_09_with_separately_licensed_self_study_companions",
        "status": manifest_status,
        "pending_evidence": sorted(pending_evidence),
        "prior_admission": {
            **file_row(PRIOR_MANIFEST),
            "admission_basis": "locally validated and publicly read-back Chapter 8 source manifest",
            "locally_admitted": True,
            "publication_status": "published_github_zenodo_figshare",
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
            "chapter_09_ordered_sha256": authority_combined,
            "chapter_09_raw_concatenated_sha256": authority_raw,
        },
        "translated_source": translated,
        "additive_components": inherited_additive + [file_row(path) for path in NEW_ADDITIVE],
        "inherited_additive_updates": inherited_additive_updates,
        "control_inputs": [current_controls[path] for path in CONTROL_INPUTS],
        "inherited_control_updates": inherited_control_updates,
        "production_implementation": [implementation_by_path[path] for path in sorted(implementation_by_path)],
        "inherited_implementation_updates": inherited_implementation_updates,
        "chapter_09_identity_bundle": {
            "source_qa": source_qa_row,
            "companion_qa": companion_qa_row,
            "backend": backend_row,
            "companion_wrapper": companion_row,
            "companion_fragments": [file_row(path) for path in COMPANION_FRAGMENTS],
            "entry_alias_map": alias_row,
            "cumulative_reader_wrapper": file_row("source/chapters_01_09_reader.ptx"),
            "project": file_row("project.ptx"),
            "assets": asset_rows,
            "rights_note": rights_row,
            "collection_licenses": licenses_row,
        },
        "companion_coverage": {
            "contract": coverage,
            "entry_counts": entry_counts,
            "source_prompt_counts": companion_qa.get("source_prompt_counts"),
            "reveal_counts": reveal_counts,
            "surface_counts": surface_counts,
            "described_images": require_dict(companion_qa.get("assets"), "companion assets").get("described_images"),
            "remote_or_interactive_surfaces": 0,
        },
        "source_correction_statuses": dict(sorted(correction_statuses.items())),
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
                "status": manifest_status,
                "output": str(OUTPUT),
                "bytes": OUTPUT.stat().st_size,
                "sha256": sha256(OUTPUT),
                "chapter_09_combined_sha256": chapter_combined,
                "cumulative_combined_sha256": cumulative_combined,
                "source_files": len(all_source_names),
                "html_files": html_file_count,
                "pending_evidence": sorted(pending_evidence),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
