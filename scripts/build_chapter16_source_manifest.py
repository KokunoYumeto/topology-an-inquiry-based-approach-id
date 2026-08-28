#!/usr/bin/env python3
"""Build the fail-closed cumulative Chapters 1-16 admission manifest.

Run only after the Chapter 16 source, final companion/backend, cumulative
HTML/PDF, browser, schema, and documentation evidence have frozen.  The
``--check-only`` mode performs every validation but does not write the final
manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
AUTHORITY_SOURCE = LANE / "authority/gvsu-pinned/topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9/source"
AUTHORITY_ARCHIVE = LANE / "authority/archives/gvsuoer-topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9.zip"
OUTPUT = ROOT / "qa/CHAPTER16_SOURCE_MANIFEST.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"

PRIOR_MANIFEST = "qa/CHAPTER15_SOURCE_MANIFEST.json"
PRIOR_MANIFEST_IDENTITY = {
    "bytes": 175_497,
    "sha256": "a1c48757893f0830f75ec1ba29dc8fe00b605db42c62bf48f7a653265068a3aa",
}
BOUNDARY = "chapters_01_16_with_separately_licensed_self_study_companions"
PRIOR_BOUNDARY = "chapters_01_15_with_separately_licensed_self_study_companions"

CHAPTER_SOURCE_FILES = (
    "chap_quotients.ptx",
    "sec_quotients.ptx",
    "sec_quotient_top.ptx",
    "sec_quotient_space.ptx",
    "sec_find_quotient_space.ptx",
    "sec_quotients_summ.ptx",
    "sec_quotients_exer.ptx",
)
COMPANION_FILES = (
    "companion/chapter_16_source_guides_a.ptx",
    "companion/chapter_16_source_guides_b.ptx",
    "companion/chapter_16_exercise_guides_a.ptx",
    "companion/chapter_16_exercise_guides_b.ptx",
    "companion/chapter_16_exercise_guides_c.ptx",
    "companion/chapter_16_exercise_guides_d.ptx",
    "companion/chapter_16_mastery.ptx",
)
COMPANION_WRAPPER = "companion/chapter_16_quotient_spaces_self_study.ptx"
READER_WRAPPER = "source/chapters_01_16_reader.ptx"
XI_INCLUDE = "{http://www.w3.org/2001/XInclude}include"
READER_CHAPTER_INCLUDES = (
    "./chap_sets.ptx",
    "./chap_functions.ptx",
    "./chap_metric_spaces.ptx",
    "./chap_metric_spaces_apps.ptx",
    "./chap_glb.ptx",
    "./chap_continuous_functions.ptx",
    "./chap_open_balls.ptx",
    "./chap_open_sets.ptx",
    "./chap_sequences.ptx",
    "./chap_closed_sets.ptx",
    "./chap_metric_subspaces.ptx",
    "./chap_top_spaces.ptx",
    "./chap_Closed_sets_topology.ptx",
    "./chap_continuity_topology.ptx",
    "./chap_subspaces.ptx",
    "./chap_quotients.ptx",
)
READER_COMPANION_INCLUDES = tuple(
    f"../companion/chapter_{number:02d}_{stem}.ptx"
    for number, stem in (
        (1, "sets_self_study"),
        (2, "functions_self_study"),
        (3, "metric_spaces_self_study"),
        (4, "metric_space_applications_self_study"),
        (5, "greatest_lower_bound_self_study"),
        (6, "continuous_functions_self_study"),
        (7, "open_balls_self_study"),
        (8, "open_sets_self_study"),
        (9, "sequences_self_study"),
        (10, "closed_sets_self_study"),
        (11, "metric_subspaces_self_study"),
        (12, "topological_spaces_self_study"),
        (13, "closed_sets_topological_spaces_self_study"),
        (14, "continuity_homeomorphisms_self_study"),
        (15, "subspaces_self_study"),
        (16, "quotient_spaces_self_study"),
    )
)
FINAL_BACKEND = "backend/chapter_16_companion_manifest.json"
FINAL_ALIASES = "backend/chapter_16_entry_aliases.csv"
PROMPT_MAP = "backend/chapter_16_source_prompt_map.csv"
GROUPING_BACKEND = "backend/chapter_16_grouping_nodes.json"
PROMPT_INVENTORY = "backend/chapter_16_prompt_inventory.json"
OCCURRENCE_ALIASES = "backend/chapter_16_occurrence_entry_aliases.csv"

SOURCE_QA = "qa/CHAPTER16_SOURCE_COMPLETE_QA.json"
COMPANION_QA = "qa/CHAPTER16_COMPANION_QA.json"
COMPANION_WRAPPER_SCHEMA_QA = "qa/CHAPTER16_COMPANION_WRAPPER_SCHEMA_QA.json"
MASTERY_SCHEMA_QA = "qa/CHAPTER16_MASTERY_SCHEMA_QA.json"
SCHEMA_QA = "qa/CHAPTER16_CUMULATIVE_SCHEMA_QA.json"
HTML_MANIFEST = "qa/CHAPTER16_HTML_MANIFEST.json"
HTML_RUN_1 = "qa/CHAPTER16_HTML_MANIFEST_RUN1.json"
HTML_RUN_2 = "qa/CHAPTER16_HTML_MANIFEST_RUN2.json"
HTML_QA = "qa/CHAPTER16_HTML_QA.json"
BROWSER_QA = "qa/CHAPTER16_BROWSER_QA.json"
ASSET_PDF_QA = "qa/CHAPTER16_ASSET_PDF_METADATA_QA.json"
PDF_RECEIPTS = {
    "deterministic_run_1": "qa/CHAPTER16_PDF_RUN1_HASH.json",
    "deterministic_run_2": "qa/CHAPTER16_PDF_RUN2_HASH.json",
    "structure_qa": "qa/CHAPTER16_PDF_STRUCTURE.json",
    "visual_qa": "qa/CHAPTER16_PDF_VISUAL_QA.json",
}
DOCS_RECEIPTS = (
    "qa/CHAPTER16_DOCS_MANIFEST.json",
    "qa/CHAPTER16_DOCS_QA.json",
    "qa/CHAPTER16_BUILD_QA.md",
)
HTML_ROOT = "output/chapters01-16-html"
PDF_PATH = "output/chapters01-16-pdf/chapters_01_16_reader.pdf"

PACKAGE_ROOT_FILES = (
    ".gitattributes",
    "README.md",
    "LICENSES.md",
    "project.ptx",
    "requirements.txt",
    "publication/publication.ptx",
)
PACKAGE_TREES = ("companion", "backend", "assets", "xsl")
CONTROL_FILES = (
    "00_control/TERMINOLOGY.csv",
    "00_control/SOURCE_CORRECTIONS.csv",
    "00_control/CHAPTER16_AUTHORITY_AUDIT.md",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def identity(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise FileNotFoundError(path)
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": digest(data)}


def repo_row(relative: str) -> dict[str, object]:
    return {"path": f"repo/{relative}", **identity(ROOT / relative)}


def control_row(relative: str) -> dict[str, object]:
    return {"path": relative, **identity(LANE / relative)}


def authority_row(name: str) -> dict[str, object]:
    return {"path": f"authority/source/{name}", **identity(AUTHORITY_SOURCE / name)}


def read_json(relative: str) -> dict[str, Any]:
    value = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object: {relative}")
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


def assert_identity(label: str, reported: object, current: dict[str, object]) -> None:
    row = require_dict(reported, label)
    if row.get("bytes") != current["bytes"] or row.get("sha256") != current["sha256"]:
        raise RuntimeError(f"{label} identity mismatch")


def assert_path_identity(label: str, reported: object, current: dict[str, object]) -> None:
    row = require_dict(reported, label)
    if safe_relative(row.get("path")) != safe_relative(current.get("path")):
        raise RuntimeError(f"{label} path mismatch")
    assert_identity(label, row, current)


def safe_relative(raw: object) -> str:
    if not isinstance(raw, str) or not raw:
        raise RuntimeError("missing portable path")
    value = raw.removeprefix("repo/")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "\\" in value or (len(value) > 2 and value[1] == ":"):
        raise RuntimeError(f"unsafe path: {raw!r}")
    return value


def rows_by_path(rows: object, label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for raw in require_list(rows, label):
        row = require_dict(raw, label)
        path = safe_relative(row.get("path"))
        if path in result:
            raise RuntimeError(f"duplicate {label} path: {path}")
        result[path] = row
    return result


def combined_named_files(base: Path, names: list[str] | tuple[str, ...]) -> str:
    value = hashlib.sha256()
    for name in names:
        value.update(name.encode("utf-8"))
        value.update(b"\0")
        value.update((base / name).read_bytes())
    return value.hexdigest()


def include_hrefs(relative: str) -> list[str]:
    root = ET.parse(ROOT / relative).getroot()
    hrefs: list[str] = []
    for element in root.iter(XI_INCLUDE):
        href = element.get("href")
        if not href:
            raise RuntimeError(f"XInclude without href in {relative}")
        hrefs.append(href)
    return hrefs


def validate_schema_receipt(
    receipt_relative: str,
    source_relative: str,
    *,
    exact_closure: set[str] | None = None,
    required_closure: set[str] | None = None,
    closure_file_count: int,
) -> dict[str, Any]:
    receipt = read_json(receipt_relative)
    require_pass(receipt, receipt_relative)
    if receipt.get("diagnostics") != []:
        raise RuntimeError(f"{receipt_relative} records schema diagnostics")
    assert_path_identity(
        f"{receipt_relative} source",
        receipt.get("source"),
        repo_row(source_relative),
    )
    xinclude = require_dict(receipt.get("xinclude"), f"{receipt_relative} XInclude")
    if xinclude.get("all_local") is not True:
        raise RuntimeError(f"{receipt_relative} has a non-local XInclude")
    raw_closure = require_list(xinclude.get("closure"), f"{receipt_relative} closure")
    if not all(isinstance(value, str) and value for value in raw_closure):
        raise RuntimeError(f"{receipt_relative} has an invalid closure path")
    closure = set(raw_closure)
    if len(closure) != len(raw_closure):
        raise RuntimeError(f"{receipt_relative} repeats a closure path")
    if len(closure) != closure_file_count or xinclude.get("closure_file_count") != closure_file_count:
        raise RuntimeError(f"{receipt_relative} closure count changed")
    if exact_closure is not None and closure != exact_closure:
        raise RuntimeError(f"{receipt_relative} exact closure changed")
    if required_closure is not None and not required_closure.issubset(closure):
        missing = sorted(required_closure - closure)
        raise RuntimeError(f"{receipt_relative} omits required closure paths: {missing}")
    return receipt


def is_historical_partial_path(relative: str) -> bool:
    name = PurePosixPath(relative).name.casefold()
    return (
        ".partial." in name
        or "chapter12_companion_partial" in name
        or name == "build_zenodo_chapter12_partial_package.py"
        or "chapter14_partial" in name
        or "chapter15_partial" in name
        or "chapter16_partial" in name
    )


def package_tree_rows(relative: str, *, python_only: bool = False) -> list[dict[str, object]]:
    base = ROOT / relative
    rows: list[dict[str, object]] = []
    for path in sorted(base.rglob("*"), key=lambda item: item.as_posix().casefold()):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix.casefold() == ".pyc":
            continue
        if python_only and path.suffix.casefold() != ".py":
            continue
        repo_relative = path.relative_to(ROOT).as_posix()
        if is_historical_partial_path(repo_relative):
            continue
        rows.append(repo_row(repo_relative))
    return rows


def unique_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for row in rows:
        path = str(row["path"])
        if path in result and result[path] != row:
            raise RuntimeError(f"conflicting inventory identity: {path}")
        result[path] = row
    return [result[path] for path in sorted(result, key=str.casefold)]


def validate_html(manifest: dict[str, Any]) -> tuple[int, int, int]:
    expected = rows_by_path(manifest.get("files"), "HTML manifest files")
    root = ROOT / HTML_ROOT
    actual = {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file()
    }
    if set(actual) != set(expected):
        raise RuntimeError("cumulative Chapter 16 HTML closure differs from its manifest")
    total = 0
    html_files = 0
    for relative, path in actual.items():
        current = identity(path)
        assert_identity(f"HTML {relative}", expected[relative], current)
        total += int(current["bytes"])
        html_files += relative.casefold().endswith(".html")
    facts = (len(actual), html_files, total)
    if facts != (manifest.get("file_count"), manifest.get("html_files"), manifest.get("total_bytes")):
        raise RuntimeError("cumulative Chapter 16 HTML census differs")
    return facts


def collect_evidence_rows(value: object) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    if isinstance(value, dict):
        if all(key in value for key in ("path", "bytes", "sha256")):
            relative = safe_relative(value["path"])
            current = repo_row(relative)
            assert_identity(f"evidence {relative}", value, current)
            found.append(current)
        for child in value.values():
            found.extend(collect_evidence_rows(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(collect_evidence_rows(child))
    return unique_rows(found)


def validate_final_companion() -> tuple[dict[str, Any], dict[str, Any], list[dict[str, object]]]:
    backend = read_json(FINAL_BACKEND)
    companion_qa = read_json(COMPANION_QA)
    expected_status = "companion_complete_reader_admitted"
    if backend.get("partial") is not False or backend.get("status") != expected_status:
        raise RuntimeError("Chapter 16 backend is partial or has not reached final companion status")
    if companion_qa.get("status") != "pass" or companion_qa.get("failures") != []:
        raise RuntimeError("Chapter 16 companion QA is not passing")
    ledgers = require_dict(companion_qa.get("ledgers"), "companion QA ledgers")
    corrections = require_dict(
        ledgers.get("source_corrections"),
        "companion QA source-correction ledger",
    )
    expected_correction_ids = [f"O003-C{number:03d}" for number in range(188, 212)]
    if corrections.get("ids") != expected_correction_ids:
        raise RuntimeError("Chapter 16 correction-ID closure changed")
    coverage = require_dict(backend.get("coverage"), "backend coverage")
    expected_coverage = {
        "covered_source_prompt_guides": 52,
        "pending_source_prompt_guides": 0,
        "covered_mastery_checks": 8,
        "entry_total": 60,
        "staged_surface_total": 240,
        "grouping_nodes": 3,
    }
    for key, expected in expected_coverage.items():
        if coverage.get(key) != expected:
            raise RuntimeError(f"Chapter 16 backend coverage changed: {key}")
    expected_wrapper_includes = [f"./{Path(path).name}" for path in COMPANION_FILES]
    actual_wrapper_includes = include_hrefs(COMPANION_WRAPPER)
    if actual_wrapper_includes != expected_wrapper_includes:
        raise RuntimeError(
            "Chapter 16 wrapper XInclude order or exact closure changed: "
            f"{actual_wrapper_includes!r}"
        )
    companion_rows = [repo_row(COMPANION_WRAPPER), *[repo_row(path) for path in COMPANION_FILES]]
    component = require_dict(backend.get("companion"), "backend companion")
    qa_files = require_dict(component.get("file_identities"), "backend companion files")
    for row in companion_rows:
        relative = safe_relative(row["path"])
        if relative not in qa_files:
            raise RuntimeError(f"companion backend omits {relative}")
        assert_identity(f"companion backend {relative}", qa_files[relative], row)
    qa_backend = require_dict(companion_qa.get("generated_outputs"), "companion QA generated outputs")
    for key, relative in (
        ("prompt_map", PROMPT_MAP),
        ("grouping_nodes", GROUPING_BACKEND),
        ("entry_aliases", FINAL_ALIASES),
        ("companion_manifest", FINAL_BACKEND),
    ):
        current = repo_row(relative)
        assert_identity(key, qa_backend.get(key), current)
    source_ref = require_dict(companion_qa.get("source_qa"), "companion QA source QA")
    assert_identity("companion QA source QA", source_ref, repo_row(SOURCE_QA))
    authority = require_dict(companion_qa.get("authority"), "companion QA authority")
    prompt_inventory = require_dict(
        authority.get("prompt_inventory"),
        "companion QA prompt inventory",
    )
    assert_identity(
        "companion QA prompt inventory",
        prompt_inventory,
        repo_row(PROMPT_INVENTORY),
    )
    reader_admission = require_dict(
        companion_qa.get("reader_admission"),
        "companion QA reader admission",
    )
    expected_reader_admission = {
        "admitted": True,
        "cumulative_wrapper": READER_WRAPPER,
        "main_include": "./chap_quotients.ptx",
        "main_include_positions": [16],
        "main_include_total": 16,
        "companion_include": f"../{COMPANION_WRAPPER}",
        "companion_include_positions": [16],
        "companion_include_total": 16,
        "main_include_order_exact": True,
        "companion_include_order_exact": True,
    }
    if reader_admission != expected_reader_admission:
        raise RuntimeError("Chapter 16 companion reader-admission contract changed")
    return backend, companion_qa, companion_rows


def validate_project_targets() -> None:
    root = ET.parse(ROOT / "project.ptx").getroot()
    targets = {
        element.get("name"): element
        for element in root.findall("./targets/target")
        if element.get("name") in {"chapters01-16-html", "chapters01-16-pdf"}
    }
    if set(targets) != {"chapters01-16-html", "chapters01-16-pdf"}:
        raise RuntimeError("project.ptx lacks one exact cumulative Chapter 16 target")

    expected = {
        "chapters01-16-html": {
            "format": "html",
            "source": READER_WRAPPER,
            "publication": "publication/publication.ptx",
            "output-dir": HTML_ROOT,
        },
        "chapters01-16-pdf": {
            "format": "pdf",
            "source": READER_WRAPPER,
            "publication": "publication/publication.ptx",
            "output-dir": "output/chapters01-16-pdf",
            "xsl": "xsl/custom-latex.xsl",
        },
    }
    for name, fields in expected.items():
        target = targets[name]
        for child_name, value in fields.items():
            children = target.findall(child_name)
            if len(children) != 1 or (children[0].text or "").strip() != value:
                raise RuntimeError(f"project target {name} has the wrong {child_name}")
    if targets["chapters01-16-pdf"].get("pdf-method") != "xelatex":
        raise RuntimeError("Chapter 16 PDF target lost the pinned xelatex method")
    html_params = [
        (element.get("key"), element.get("value"))
        for element in targets["chapters01-16-html"].findall("stringparam")
    ]
    if html_params != [("html.css.extra", "external/o003-readable-layout.css")]:
        raise RuntimeError("Chapter 16 HTML target lost its exact readable-layout CSS")


def validate_html_determinism(final_manifest: dict[str, Any]) -> None:
    run_1 = read_json(HTML_RUN_1)
    run_2 = read_json(HTML_RUN_2)
    for key in ("file_count", "html_files", "total_bytes", "canonical_manifest_sha256"):
        values = (run_1.get(key), run_2.get(key), final_manifest.get(key))
        if values[0] != values[1] or values[1] != values[2]:
            raise RuntimeError(f"Chapter 16 HTML double-build differs for {key}: {values!r}")


def validate_pdf_determinism(pdf_row: dict[str, object]) -> tuple[dict[str, Any], dict[str, Any]]:
    run_1 = read_json(PDF_RECEIPTS["deterministic_run_1"])
    run_2 = read_json(PDF_RECEIPTS["deterministic_run_2"])
    require_pass(run_1, "Chapter 16 PDF run 1")
    require_pass(run_2, "Chapter 16 PDF run 2")

    run_1_path = safe_relative(run_1.get("path"))
    if run_1_path != "tmp/pdfs/chapter16-run1.pdf":
        raise RuntimeError("Chapter 16 PDF run-1 snapshot path changed")
    snapshot_row = repo_row(run_1_path)
    assert_path_identity("Chapter 16 PDF run-1 snapshot", run_1, snapshot_row)
    assert_path_identity("Chapter 16 PDF run-2 artifact", run_2, pdf_row)
    for key in ("bytes", "sha256", "pages", "source_date_epoch"):
        if run_1.get(key) != run_2.get(key):
            raise RuntimeError(f"Chapter 16 PDF double-build differs for {key}")
    if run_2.get("byte_identical_to_run_1") is not True:
        raise RuntimeError("Chapter 16 PDF run 2 does not attest byte identity")
    assert_path_identity(
        "Chapter 16 PDF run-2 nested run-1 identity",
        run_2.get("run_1"),
        snapshot_row,
    )
    for run, expected_path in (
        (run_1, "qa/CHAPTER16_PDF_BUILD_RUN1.log"),
        (run_2, "qa/CHAPTER16_PDF_BUILD_RUN2.log"),
    ):
        transcript = require_dict(run.get("transcript"), "PDF run transcript")
        assert_path_identity("Chapter 16 PDF transcript", transcript, repo_row(expected_path))
    return run_1, run_2


def build_manifest() -> dict[str, Any]:
    assert_identity("pinned Chapter 15 manifest", PRIOR_MANIFEST_IDENTITY, identity(ROOT / PRIOR_MANIFEST))
    prior = read_json(PRIOR_MANIFEST)
    require_pass(prior, "Chapter 15 source manifest")
    if prior.get("boundary") != PRIOR_BOUNDARY or prior.get("pending_evidence") != []:
        raise RuntimeError("unexpected Chapter 15 admission boundary")

    translated = require_dict(prior.get("translated_source"), "prior translated source")
    prior_names: list[str] = []
    for chapter_number in range(1, 16):
        chapter = require_dict(translated.get(f"chapter_{chapter_number:02d}"), "prior chapter")
        for row in require_list(chapter.get("files"), "prior source files"):
            relative = safe_relative(require_dict(row, "prior source row").get("path"))
            if not relative.startswith("source/"):
                raise RuntimeError(f"prior source path escaped source tree: {relative}")
            assert_identity(relative, row, identity(ROOT / relative))
            prior_names.append(relative.removeprefix("source/"))
    if len(prior_names) != len(set(prior_names)):
        raise RuntimeError("prior translated source closure repeats a file")

    source_qa = read_json(SOURCE_QA)
    require_pass(source_qa, "Chapter 16 source QA")
    if source_qa.get("failures") != []:
        raise RuntimeError("Chapter 16 source QA records failures")
    qa_sources: dict[str, dict[str, Any]] = {}
    for raw in require_list(source_qa.get("files"), "Chapter 16 source QA files"):
        row = require_dict(raw, "Chapter 16 source QA row")
        name = row.get("file")
        if not isinstance(name, str) or not name or "/" in name or "\\" in name:
            raise RuntimeError(f"invalid Chapter 16 source-QA filename: {name!r}")
        if name in qa_sources:
            raise RuntimeError(f"duplicate Chapter 16 source-QA filename: {name}")
        qa_sources[name] = row
    if set(qa_sources) != set(CHAPTER_SOURCE_FILES):
        raise RuntimeError("Chapter 16 source QA closure is not the exact seven-file target")
    translated_rows: list[dict[str, object]] = []
    authority_rows: list[dict[str, object]] = []
    for name in CHAPTER_SOURCE_FILES:
        qa_row = qa_sources[name]
        translated_row = repo_row(f"source/{name}")
        authority_file_row = authority_row(name)
        assert_identity(f"translated source {name}", qa_row.get("translated"), translated_row)
        assert_identity(f"authority source {name}", qa_row.get("authority"), authority_file_row)
        translated_rows.append(translated_row)
        authority_rows.append(authority_file_row)
    chapter_combined = combined_named_files(ROOT / "source", CHAPTER_SOURCE_FILES)
    if source_qa.get("combined_translated_sha256") != chapter_combined:
        raise RuntimeError("Chapter 16 translated combined identity is stale")

    backend, companion_qa, companion_rows = validate_final_companion()
    reader_text = (ROOT / READER_WRAPPER).read_text(encoding="utf-8")
    if MODEL not in reader_text:
        raise RuntimeError("Chapter 16 reader wrapper lacks exact model provenance")
    expected_reader_includes = [*READER_CHAPTER_INCLUDES, *READER_COMPANION_INCLUDES]
    actual_reader_includes = include_hrefs(READER_WRAPPER)
    if actual_reader_includes != expected_reader_includes:
        raise RuntimeError(
            "Chapter 16 reader XInclude order or exact closure changed: "
            f"{actual_reader_includes!r}"
        )
    validate_project_targets()

    chapter_16_companion_closure = {COMPANION_WRAPPER, *COMPANION_FILES}
    validate_schema_receipt(
        COMPANION_WRAPPER_SCHEMA_QA,
        COMPANION_WRAPPER,
        exact_closure=chapter_16_companion_closure,
        closure_file_count=8,
    )
    validate_schema_receipt(
        MASTERY_SCHEMA_QA,
        "companion/chapter_16_mastery.ptx",
        exact_closure={"companion/chapter_16_mastery.ptx"},
        closure_file_count=1,
    )
    cumulative_required_closure = {
        READER_WRAPPER,
        *[f"source/{name}" for name in (*prior_names, *CHAPTER_SOURCE_FILES)],
        *chapter_16_companion_closure,
    }
    schema_qa = validate_schema_receipt(
        SCHEMA_QA,
        READER_WRAPPER,
        required_closure=cumulative_required_closure,
        closure_file_count=209,
    )
    html_manifest = read_json(HTML_MANIFEST)
    html_qa = read_json(HTML_QA)
    browser_qa = read_json(BROWSER_QA)
    require_pass(html_qa, "Chapter 16 HTML QA")
    require_pass(browser_qa, "Chapter 16 browser QA")
    html_facts = validate_html(html_manifest)
    validate_html_determinism(html_manifest)
    for key, value in zip(("file_count", "html_files", "total_bytes"), html_facts):
        if html_qa.get(key) != value:
            raise RuntimeError(f"Chapter 16 HTML QA differs for {key}")
    if html_qa.get("canonical_manifest_sha256") != html_manifest.get("canonical_manifest_sha256"):
        raise RuntimeError("Chapter 16 HTML canonical identity differs")

    pdf_visual = read_json(PDF_RECEIPTS["visual_qa"])
    require_pass(pdf_visual, "Chapter 16 PDF visual QA")
    pdf_row = repo_row(PDF_PATH)
    assert_path_identity("Chapter 16 PDF", pdf_visual.get("pdf"), pdf_row)
    pdf_run_1, pdf_run_2 = validate_pdf_determinism(pdf_row)
    pdf_pages = pdf_visual.get("pages")
    if not isinstance(pdf_pages, int) or pdf_pages <= 0:
        raise RuntimeError("Chapter 16 PDF visual QA has no positive page count")
    if pdf_pages != pdf_run_2.get("pages"):
        raise RuntimeError("Chapter 16 PDF visual and deterministic page counts differ")
    assert_path_identity(
        "Chapter 16 PDF visual build log",
        pdf_visual.get("build_log"),
        repo_row("qa/CHAPTER16_PDF_BUILD_RUN2.log"),
    )
    structure_qa = read_json(PDF_RECEIPTS["structure_qa"])
    require_pass(structure_qa, "Chapter 16 PDF structure QA")
    assert_path_identity("Chapter 16 PDF structure artifact", structure_qa.get("artifact"), pdf_row)
    if structure_qa.get("pages") != pdf_pages:
        raise RuntimeError("Chapter 16 PDF structure page count differs")
    qa_paths = [
        SOURCE_QA, COMPANION_QA, COMPANION_WRAPPER_SCHEMA_QA,
        MASTERY_SCHEMA_QA, SCHEMA_QA, HTML_MANIFEST, HTML_RUN_1,
        HTML_RUN_2, HTML_QA, BROWSER_QA, ASSET_PDF_QA,
        *PDF_RECEIPTS.values(), *DOCS_RECEIPTS,
    ]
    qa_rows: dict[str, dict[str, object]] = {}
    for relative in qa_paths:
        if relative.endswith(".json") and relative not in {HTML_MANIFEST, HTML_RUN_1, HTML_RUN_2}:
            report = read_json(relative)
            if relative not in {SOURCE_QA, COMPANION_QA}:
                require_pass(report, relative)
        qa_rows[relative] = repo_row(relative)
    evidence_rows = collect_evidence_rows(browser_qa)

    chapter_16 = {
        "admission": "complete cumulative reader admission",
        "source_qa": qa_rows[SOURCE_QA],
        "combined_sha256": chapter_combined,
        "files": translated_rows,
        "authority_files": authority_rows,
        "approved_external_xrefs": source_qa.get("approved_external_xref_targets"),
    }
    translated = dict(translated)
    translated["chapter_16"] = chapter_16
    all_names = [*prior_names, *CHAPTER_SOURCE_FILES]
    translated["cumulative_combined_sha256"] = combined_named_files(ROOT / "source", all_names)
    translated["combined_algorithm"] = "SHA-256 over each ordered source filename, one NUL byte, then exact file bytes"

    prior_inventory = require_list(prior.get("package_source_inventory"), "prior package inventory")
    inventory_rows: list[dict[str, object]] = []
    for raw in prior_inventory:
        relative_with_prefix = require_dict(raw, "prior inventory row").get("path")
        if not isinstance(relative_with_prefix, str):
            raise RuntimeError("prior package inventory row has no path")
        if relative_with_prefix.startswith("repo/"):
            relative = safe_relative(relative_with_prefix)
            if not is_historical_partial_path(relative):
                inventory_rows.append(repo_row(relative))
        elif relative_with_prefix.startswith("00_control/"):
            inventory_rows.append(control_row(relative_with_prefix))
        else:
            raise RuntimeError(f"unsupported inherited package path: {relative_with_prefix}")
    inventory_rows.extend(repo_row(path) for path in PACKAGE_ROOT_FILES)
    inventory_rows.extend(repo_row(f"source/{name}") for name in all_names)
    inventory_rows.append(repo_row(READER_WRAPPER))
    inventory_rows.extend(row for tree in PACKAGE_TREES for row in package_tree_rows(tree))
    inventory_rows.extend(package_tree_rows("scripts", python_only=True))
    inventory_rows.extend(qa_rows.values())
    inventory_rows.extend(evidence_rows)
    inventory_rows.extend(control_row(path) for path in CONTROL_FILES)
    inventory_rows.append(repo_row(PRIOR_MANIFEST))
    inventory = unique_rows(inventory_rows)
    cumulative_companions = [
        row for row in inventory if str(row["path"]).startswith("repo/companion/")
    ]
    cumulative_backends = [
        row for row in inventory if str(row["path"]).startswith("repo/backend/")
    ]

    authority_archive = {
        "path": f"authority/archives/{AUTHORITY_ARCHIVE.name}",
        **identity(AUTHORITY_ARCHIVE),
        "public_source_package_included": False,
        "omission_reason": (
            "The byte-preserving upstream archive contains legacy absolute "
            "author-workstation paths in 20 PDF metadata dictionaries; its exact "
            "identity and official commit/tree remain bound here without publicly "
            "redistributing those metadata bytes."
        ),
    }
    prior_archive = require_dict(prior.get("package_authority_archive"), "prior authority archive")
    assert_identity("authority archive", prior_archive, authority_archive)
    manifest = {
        "schema_version": 1,
        "status": "pass",
        "partial": True,
        "boundary_complete": True,
        "pending_evidence": [],
        "boundary": BOUNDARY,
        "admission_status": "partial_checkpoint_admitted",
        "lane": "O003/C90",
        "locale": "id-ID",
        "prior_admission": {"path": f"repo/{PRIOR_MANIFEST}", **identity(ROOT / PRIOR_MANIFEST)},
        "authority": prior.get("authority"),
        "translated_source": translated,
        "chapter_16_identity_bundle": {
            "cumulative_reader_wrapper": repo_row(READER_WRAPPER),
            "source_qa": qa_rows[SOURCE_QA],
            "companion_qa": qa_rows[COMPANION_QA],
            "companion_wrapper": repo_row(COMPANION_WRAPPER),
            "companion_files": companion_rows[1:],
            "backend": repo_row(FINAL_BACKEND),
            "entry_alias_map": repo_row(FINAL_ALIASES),
            "occurrence_alias_map": repo_row(OCCURRENCE_ALIASES),
            "source_prompt_map": repo_row(PROMPT_MAP),
            "grouping_backend": repo_row(GROUPING_BACKEND),
            "prompt_inventory": repo_row(PROMPT_INVENTORY),
            "companion_wrapper_schema_qa": qa_rows[COMPANION_WRAPPER_SCHEMA_QA],
            "mastery_schema_qa": qa_rows[MASTERY_SCHEMA_QA],
            "schema_qa": qa_rows[SCHEMA_QA],
            "project": repo_row("project.ptx"),
        },
        "cumulative_component_identities": {
            "translated_source_chapters_01_16": {
                "file_count": len(all_names),
                "chapters": [f"chapter_{number:02d}" for number in range(1, 17)],
                "cumulative_combined_sha256": translated["cumulative_combined_sha256"],
            },
            "companions_chapters_01_16": cumulative_companions,
            "backends_chapters_01_16": cumulative_backends,
        },
        "companion_coverage": {
            "source_prompt_guides": 52,
            "mastery_checks": 8,
            "total_entries": 60,
            "surfaces_per_entry": ["statement", "hint", "answer", "solution"],
            "total_surfaces": 240,
            "grouping_nodes_mapped": 3,
            "backend_status": backend.get("status"),
            "reader_admission": "pass",
        },
        "reader_artifacts": {
            "html": {
                "path": f"repo/{HTML_ROOT}",
                "status": "deterministic_tree_pass",
                "file_count": html_facts[0],
                "html_files": html_facts[1],
                "bytes": html_facts[2],
                "canonical_manifest_sha256": html_manifest.get("canonical_manifest_sha256"),
                "manifest": qa_rows[HTML_MANIFEST],
                "deterministic_run_1": qa_rows[HTML_RUN_1],
                "deterministic_run_2": qa_rows[HTML_RUN_2],
                "qa": qa_rows[HTML_QA],
                "browser_qa": {**qa_rows[BROWSER_QA], "status": "pass", "evidence": evidence_rows},
            },
            "standalone_pdf_asset_metadata_qa": qa_rows[ASSET_PDF_QA],
            "pdf": {
                **pdf_row,
                "status": "pass",
                "pages": pdf_pages,
                "tagged": pdf_visual.get("tagged"),
                "evidence": {key: qa_rows[path] for key, path in PDF_RECEIPTS.items()},
            },
        },
        "qa_receipts": {path: row for path, row in sorted(qa_rows.items())},
        "rights": {
            "translated_gvsu_spine": "CC-BY-NC-SA-3.0 (conservative determination)",
            "original_self_study_companions": "CC-BY-4.0",
            "software_figures_fonts_and_assets": "per-component notices retained",
            "collection_policy": "per-component rights; no flattened license",
            "collection_licenses": repo_row("LICENSES.md"),
            "companion_rights": repo_row("companion/RIGHTS.md"),
            "non_endorsement": True,
        },
        "production_provenance": {
            "tool": MODEL,
            "scope": "translation drafting, original companion, modular backend, and edition QA",
            "credit_note": "Model provenance does not replace source-author, institutional, or human-contributor credits.",
        },
        "package_source_inventory": inventory,
        "package_authority_archive": authority_archive,
        "known_caveats": [
            "This is a complete admitted 16-of-20 cumulative reader boundary, not the complete edition.",
            "HTML remains the primary accessible surface unless the admitted PDF receipt reports tagging.",
            "Whole-book figure-provenance and complete-edition closure remain later gates.",
        ],
    }
    if (
        manifest.get("partial") is not True
        or manifest.get("boundary_complete") is not True
        or manifest.get("admission_status") != "partial_checkpoint_admitted"
    ):
        raise RuntimeError("Chapter 16 checkpoint scope is not represented truthfully")
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate the frozen admission closure and print a summary without writing the manifest.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = build_manifest()
    except (FileNotFoundError, RuntimeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Chapter 16 admission manifest gate failed: {exc}") from exc
    summary = {
        "status": manifest["status"],
        "partial": manifest["partial"],
        "boundary": manifest["boundary"],
        "source_files": manifest["cumulative_component_identities"]["translated_source_chapters_01_16"]["file_count"],
        "package_inventory_files": len(manifest["package_source_inventory"]),
        "check_only": args.check_only,
    }
    if not args.check_only:
        payload = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        temporary = OUTPUT.with_name(f".{OUTPUT.name}.tmp")
        temporary.write_text(payload, encoding="utf-8", newline="\n")
        temporary.replace(OUTPUT)
        summary.update({"output": "repo/qa/CHAPTER16_SOURCE_MANIFEST.json", **identity(OUTPUT)})
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
