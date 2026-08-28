#!/usr/bin/env python3
"""Build the fail-closed cumulative Chapters 1-17 release-source manifest.

Run only after Chapter 17 source, companion/backend, cumulative HTML/PDF,
browser, schema, and PDF evidence have frozen. The --check-only mode performs
all validation without writing the final manifest. No Chapter 16 byte identity
or content census is embedded: inherited identities come from the current
admitted Chapter 16 manifest, and Chapter 17 facts are derived from current
bounded artifacts and then compared across their receipts.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
AUTHORITY_COMMIT = "0c2d8f614ef87aa00de373f3418146c2f1d13bb9"
AUTHORITY_SOURCE = (
    LANE / "authority" / "gvsu-pinned" / f"topology-{AUTHORITY_COMMIT}" / "source"
)
OUTPUT = ROOT / "qa/CHAPTER17_SOURCE_MANIFEST.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
PRIOR_MANIFEST = "qa/CHAPTER16_SOURCE_MANIFEST.json"
PRIOR_BOUNDARY = "chapters_01_16_with_separately_licensed_self_study_companions"
BOUNDARY = "chapters_01_17_with_separately_licensed_self_study_companions"
XI_INCLUDE = "{http://www.w3.org/2001/XInclude}include"

CHAPTER_SOURCE_FILES = (
    "chap_Compact_topology.ptx",
    "sec_compact_top_intro.ptx",
    "sec_compact_cont.ptx",
    "sec_compact_rn.ptx",
    "sec_compact_app.ptx",
    "sec_compact_top_summ.ptx",
    "sec_fractals.ptx",
    "sec_compact_top_exer.ptx",
)
COMPANION_WRAPPER = "companion/chapter_17_compact_spaces_self_study.ptx"
COMPANION_FILES = (
    "companion/chapter_17_source_guides_a.ptx",
    "companion/chapter_17_source_guides_b.ptx",
    "companion/chapter_17_source_guides_c.ptx",
    "companion/chapter_17_exercise_guides_b.ptx",
    "companion/chapter_17_exercise_guides_d.ptx",
    "companion/chapter_17_exercise_guides_e.ptx",
    "companion/chapter_17_mastery.ptx",
)
READER_WRAPPER = "source/chapters_01_17_reader.ptx"
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
    "./chap_Compact_topology.ptx",
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
        (17, "compact_spaces_self_study"),
    )
)

FINAL_BACKEND = "backend/chapter_17_companion_manifest.json"
FINAL_ALIASES = "backend/chapter_17_entry_aliases.csv"
PROMPT_MAP = "backend/chapter_17_source_prompt_map.csv"
GROUPING_BACKEND = "backend/chapter_17_grouping_nodes.json"
PROMPT_INVENTORY = "backend/chapter_17_prompt_inventory.json"
OCCURRENCE_ALIASES = "backend/chapter_17_occurrence_entry_aliases.csv"
BACKEND_FILES = (
    FINAL_BACKEND,
    FINAL_ALIASES,
    PROMPT_MAP,
    GROUPING_BACKEND,
    PROMPT_INVENTORY,
    OCCURRENCE_ALIASES,
)

SOURCE_QA = "qa/CHAPTER17_SOURCE_COMPLETE_QA.json"
COMPANION_QA = "qa/CHAPTER17_COMPANION_QA.json"
WRAPPER_SCHEMA_QA = "qa/CHAPTER17_COMPANION_WRAPPER_SCHEMA_QA.json"
MASTERY_SCHEMA_QA = "qa/CHAPTER17_MASTERY_SCHEMA_QA.json"
SCHEMA_QA = "qa/CHAPTER17_CUMULATIVE_SCHEMA_QA.json"
HTML_MANIFEST = "qa/CHAPTER17_HTML_MANIFEST.json"
HTML_RUN_1 = "qa/CHAPTER17_HTML_MANIFEST_RUN1.json"
HTML_RUN_2 = "qa/CHAPTER17_HTML_MANIFEST_RUN2.json"
HTML_QA = "qa/CHAPTER17_HTML_QA.json"
BROWSER_QA = "qa/CHAPTER17_BROWSER_QA.json"
ASSET_PDF_QA = "qa/CHAPTER17_ASSET_PDF_METADATA_QA.json"
PDF_RECEIPTS = {
    "deterministic_run_1": "qa/CHAPTER17_PDF_RUN1_HASH.json",
    "deterministic_run_2": "qa/CHAPTER17_PDF_RUN2_HASH.json",
    "structure_qa": "qa/CHAPTER17_PDF_STRUCTURE.json",
    "visual_qa": "qa/CHAPTER17_PDF_VISUAL_QA.json",
}
PDF_LOGS = (
    "qa/CHAPTER17_PDF_BUILD_RUN1.log",
    "qa/CHAPTER17_PDF_BUILD_RUN2.log",
)
QA_FILES = (
    "qa/CHAPTER17_COMPANION_BACKEND_RECEIPT.md",
    SOURCE_QA,
    "qa/CHAPTER17_SOURCE_COMPLETE_RECEIPT.md",
    "qa/CHAPTER17_SOURCE_PREFIX_QA.json",
    "qa/CHAPTER17_SCHEMA_VALIDATION.json",
    "qa/CHAPTER17_RN_QA.json",
    "qa/CHAPTER17_FRACTALS_QA.json",
    "qa/CHAPTER17_EXERCISES_QA.json",
    "qa/CHAPTER17_SOURCE_GUIDES_A_SCHEMA_QA.json",
    "qa/CHAPTER17_SOURCE_GUIDES_B_SCHEMA_QA.json",
    "qa/CHAPTER17_SOURCE_GUIDES_C_SCHEMA_QA.json",
    "qa/CHAPTER17_EXERCISE_GUIDES_B_SCHEMA_QA.json",
    "qa/CHAPTER17_EXERCISE_GUIDES_D_SCHEMA_QA.json",
    "qa/CHAPTER17_EXERCISE_GUIDES_E_SCHEMA_QA.json",
    MASTERY_SCHEMA_QA,
    WRAPPER_SCHEMA_QA,
    COMPANION_QA,
    SCHEMA_QA,
    HTML_MANIFEST,
    HTML_RUN_1,
    HTML_RUN_2,
    HTML_QA,
    BROWSER_QA,
    ASSET_PDF_QA,
    *PDF_RECEIPTS.values(),
    *PDF_LOGS,
)
HTML_ROOT = "output/chapters01-17-html"
PDF_PATH = "output/chapters01-17-pdf/chapters_01_17_reader.pdf"
PDF_RUN_1_SNAPSHOT = "tmp/pdfs/chapter17-run1.pdf"
PACKAGE_ROOT_FILES = (
    ".gitattributes",
    "README.md",
    "LICENSES.md",
    "project.ptx",
    "requirements.txt",
    "publication/publication.ptx",
    "companion/RIGHTS.md",
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


def safe_relative(raw: object) -> str:
    if not isinstance(raw, str) or not raw:
        raise RuntimeError("missing portable path")
    value = raw.removeprefix("repo/")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "\\" in value:
        raise RuntimeError(f"unsafe path: {raw!r}")
    return value


def assert_identity(label: str, reported: object, current: dict[str, object]) -> None:
    row = require_dict(reported, label)
    if row.get("bytes") != current["bytes"] or row.get("sha256") != current["sha256"]:
        raise RuntimeError(f"{label} identity mismatch")


def assert_path_identity(label: str, reported: object, current: dict[str, object]) -> None:
    row = require_dict(reported, label)
    if safe_relative(row.get("path")) != safe_relative(current.get("path")):
        raise RuntimeError(f"{label} path mismatch")
    assert_identity(label, row, current)


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


def resolve_xinclude_closure(start_relative: str) -> set[str]:
    closure: set[str] = set()
    visiting: set[str] = set()

    def visit(relative: str) -> None:
        relative = safe_relative(relative)
        if relative in closure:
            return
        if relative in visiting:
            raise RuntimeError(f"cyclic XInclude closure at {relative}")
        path = (ROOT / relative).resolve()
        try:
            path.relative_to(ROOT.resolve())
        except ValueError as exc:
            raise RuntimeError(f"XInclude escapes repository: {relative}") from exc
        if not path.is_file():
            raise FileNotFoundError(path)
        visiting.add(relative)
        root = ET.parse(path).getroot()
        for element in root.iter(XI_INCLUDE):
            href = element.get("href")
            if not href:
                raise RuntimeError(f"XInclude without href in {relative}")
            included = (path.parent / href).resolve()
            try:
                child = included.relative_to(ROOT.resolve()).as_posix()
            except ValueError as exc:
                raise RuntimeError(
                    f"non-local XInclude {href!r} in {relative}"
                ) from exc
            visit(child)
        visiting.remove(relative)
        closure.add(relative)

    visit(start_relative)
    return closure


def validate_schema_receipt(receipt_relative: str, source_relative: str) -> None:
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
        raise RuntimeError(f"{receipt_relative} has non-local XInclude")
    raw = require_list(xinclude.get("closure"), f"{receipt_relative} closure")
    reported = {safe_relative(value) for value in raw}
    if len(reported) != len(raw):
        raise RuntimeError(f"{receipt_relative} repeats a closure path")
    actual = resolve_xinclude_closure(source_relative)
    if reported != actual or xinclude.get("closure_file_count") != len(actual):
        raise RuntimeError(f"{receipt_relative} XInclude closure is stale")


def unique_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for row in rows:
        path = str(row["path"])
        if path in result and result[path] != row:
            raise RuntimeError(f"conflicting identity for {path}")
        result[path] = row
    return [result[path] for path in sorted(result, key=str.casefold)]


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


def validate_final_companion() -> tuple[
    dict[str, Any], list[dict[str, object]], dict[str, int]
]:
    backend = read_json(FINAL_BACKEND)
    companion_qa = read_json(COMPANION_QA)
    if backend.get("status") != "complete":
        raise RuntimeError("Chapter 17 companion backend is not complete")
    require_pass(companion_qa, "Chapter 17 companion QA")
    if companion_qa.get("failures") != []:
        raise RuntimeError("Chapter 17 companion QA records failures")
    raw_counts = require_dict(backend.get("counts"), "backend counts")
    counts: dict[str, int] = {}
    for key, value in raw_counts.items():
        if not isinstance(value, int) or value < 0:
            raise RuntimeError(f"invalid backend count {key}: {value!r}")
        counts[key] = value
    if require_dict(companion_qa.get("counts"), "QA counts") != raw_counts:
        raise RuntimeError("companion QA and backend counts differ")
    if counts["total_entries"] != (
        counts["canonical_source_entries"] + counts["mastery_entries"]
    ):
        raise RuntimeError("backend total-entry arithmetic differs")
    if counts["staged_surfaces"] != counts["total_entries"] * 4:
        raise RuntimeError("backend staged-surface arithmetic differs")
    if counts["physical_prompt_occurrences"] != (
        counts["canonical_source_entries"] + counts["occurrence_aliases"]
    ):
        raise RuntimeError("backend occurrence arithmetic differs")

    expected_hrefs = [f"./{Path(path).name}" for path in COMPANION_FILES]
    if include_hrefs(COMPANION_WRAPPER) != expected_hrefs:
        raise RuntimeError("Chapter 17 companion include order changed")
    companion_rows = [
        repo_row(COMPANION_WRAPPER),
        *[repo_row(path) for path in COMPANION_FILES],
    ]
    reported = rows_by_path(backend.get("companion_files"), "companion files")
    if set(reported) != {safe_relative(row["path"]) for row in companion_rows}:
        raise RuntimeError("backend companion closure changed")
    for row in companion_rows:
        relative = safe_relative(row["path"])
        assert_identity(f"companion {relative}", reported[relative], row)

    source_backend = require_dict(backend.get("source_backend"), "source backend")
    for key, relative in (
        ("inventory", PROMPT_INVENTORY),
        ("prompt_map_covered", PROMPT_MAP),
        ("grouping_nodes", GROUPING_BACKEND),
        ("occurrence_aliases", OCCURRENCE_ALIASES),
    ):
        assert_path_identity(key, source_backend.get(key), repo_row(relative))
    assert_path_identity(
        "entry aliases", backend.get("entry_aliases"), repo_row(FINAL_ALIASES)
    )
    outputs = require_dict(companion_qa.get("outputs"), "companion QA outputs")
    for key, relative in (
        ("manifest", FINAL_BACKEND),
        ("entry_aliases", FINAL_ALIASES),
        ("prompt_map", PROMPT_MAP),
    ):
        assert_path_identity(key, outputs.get(key), repo_row(relative))
    for raw in require_dict(companion_qa.get("inputs"), "QA inputs").values():
        row = require_dict(raw, "QA input")
        current = repo_row(safe_relative(row.get("path")))
        assert_path_identity("QA input", row, current)
    checks = require_dict(companion_qa.get("checks"), "companion QA checks")
    if any(value not in {"pass", "covered"} for value in checks.values()):
        raise RuntimeError("companion QA contains an incomplete check")

    with (ROOT / PROMPT_MAP).open(encoding="utf-8", newline="") as handle:
        prompt_rows = list(csv.DictReader(handle))
    if not prompt_rows or any(
        row.get("support_status") != "covered" for row in prompt_rows
    ):
        raise RuntimeError("source prompt map is not fully covered")
    if [int(row["sequence"]) for row in prompt_rows] != list(
        range(1, len(prompt_rows) + 1)
    ):
        raise RuntimeError("source prompt map sequence is not contiguous")
    if len({row["entry_id"] for row in prompt_rows}) != counts[
        "canonical_source_entries"
    ]:
        raise RuntimeError("source prompt map canonical census differs")
    if len(prompt_rows) != counts["physical_prompt_occurrences"]:
        raise RuntimeError("source prompt map physical census differs")

    inventory = read_json(PROMPT_INVENTORY)
    census = require_dict(inventory.get("census"), "prompt inventory census")
    expected_census = {
        "physical_prompt_occurrence_total": counts["physical_prompt_occurrences"],
        "canonical_source_support_entry_total": counts["canonical_source_entries"],
        "grouping_node_total": counts["grouping_nodes"],
    }
    for key, expected in expected_census.items():
        if census.get(key) != expected:
            raise RuntimeError(f"prompt inventory census differs for {key}")
    entries = require_list(backend.get("entries"), "backend entries")
    ids = [require_dict(entry, "backend entry").get("id") for entry in entries]
    if len(entries) != counts["total_entries"] or len(ids) != len(set(ids)):
        raise RuntimeError("backend entry census or uniqueness differs")
    return backend, companion_rows, counts


def validate_project_targets() -> None:
    root = ET.parse(ROOT / "project.ptx").getroot()
    names = {"chapters01-17-html", "chapters01-17-pdf"}
    targets = {
        node.get("name"): node
        for node in root.findall("./targets/target")
        if node.get("name") in names
    }
    if set(targets) != names:
        raise RuntimeError("project.ptx lacks exact Chapter 17 targets")
    expected = {
        "chapters01-17-html": {
            "format": "html",
            "source": READER_WRAPPER,
            "publication": "publication/publication.ptx",
            "output-dir": HTML_ROOT,
        },
        "chapters01-17-pdf": {
            "format": "pdf",
            "source": READER_WRAPPER,
            "publication": "publication/publication.ptx",
            "output-dir": "output/chapters01-17-pdf",
            "xsl": "xsl/custom-latex.xsl",
        },
    }
    for name, fields in expected.items():
        for child_name, value in fields.items():
            children = targets[name].findall(child_name)
            if len(children) != 1 or (children[0].text or "").strip() != value:
                raise RuntimeError(f"project target {name} has wrong {child_name}")
    if targets["chapters01-17-pdf"].get("pdf-method") != "xelatex":
        raise RuntimeError("Chapter 17 PDF target lost xelatex")
    params = [
        (node.get("key"), node.get("value"))
        for node in targets["chapters01-17-html"].findall("stringparam")
    ]
    if params != [("html.css.extra", "external/o003-readable-layout.css")]:
        raise RuntimeError("Chapter 17 HTML target lost readable-layout CSS")


def validate_html(manifest: dict[str, Any]) -> tuple[int, int, int]:
    expected = rows_by_path(manifest.get("files"), "HTML manifest files")
    root = ROOT / HTML_ROOT
    if not root.is_dir():
        raise FileNotFoundError(root)
    actual = {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file()
    }
    if set(actual) != set(expected):
        raise RuntimeError("Chapter 17 HTML tree differs from manifest")
    total = 0
    html_files = 0
    for relative, path in actual.items():
        current = identity(path)
        assert_identity(f"HTML {relative}", expected[relative], current)
        total += int(current["bytes"])
        html_files += relative.casefold().endswith(".html")
    facts = (len(actual), html_files, total)
    if facts != (
        manifest.get("file_count"),
        manifest.get("html_files"),
        manifest.get("total_bytes"),
    ):
        raise RuntimeError("Chapter 17 HTML census differs")
    return facts


def validate_pdf(pdf_row: dict[str, object]) -> tuple[int, dict[str, object]]:
    run_1 = read_json(PDF_RECEIPTS["deterministic_run_1"])
    run_2 = read_json(PDF_RECEIPTS["deterministic_run_2"])
    require_pass(run_1, "Chapter 17 PDF run 1")
    require_pass(run_2, "Chapter 17 PDF run 2")
    if safe_relative(run_1.get("path")) != PDF_RUN_1_SNAPSHOT:
        raise RuntimeError("Chapter 17 PDF run-1 snapshot path changed")
    snapshot = repo_row(PDF_RUN_1_SNAPSHOT)
    assert_path_identity("PDF run-1 snapshot", run_1, snapshot)
    assert_path_identity("PDF run-2 artifact", run_2, pdf_row)
    for key in ("bytes", "sha256", "pages", "source_date_epoch"):
        if run_1.get(key) != run_2.get(key):
            raise RuntimeError(f"Chapter 17 PDF double-build differs for {key}")
    if run_2.get("byte_identical_to_run_1") is not True:
        raise RuntimeError("Chapter 17 PDF run 2 lacks byte-identity attestation")
    assert_path_identity("nested run-1 identity", run_2.get("run_1"), snapshot)
    for report, transcript_path in ((run_1, PDF_LOGS[0]), (run_2, PDF_LOGS[1])):
        assert_path_identity(
            "PDF transcript",
            require_dict(report.get("transcript"), "PDF transcript"),
            repo_row(transcript_path),
        )
    visual = read_json(PDF_RECEIPTS["visual_qa"])
    structure = read_json(PDF_RECEIPTS["structure_qa"])
    require_pass(visual, "Chapter 17 PDF visual QA")
    require_pass(structure, "Chapter 17 PDF structure QA")
    assert_path_identity("PDF visual artifact", visual.get("pdf"), pdf_row)
    assert_path_identity("PDF structure artifact", structure.get("artifact"), pdf_row)
    assert_path_identity("PDF visual log", visual.get("build_log"), repo_row(PDF_LOGS[1]))
    pages = visual.get("pages")
    if (
        not isinstance(pages, int)
        or pages <= 0
        or pages != run_2.get("pages")
        or pages != structure.get("pages")
    ):
        raise RuntimeError("Chapter 17 PDF page census differs")
    return pages, snapshot


def inherited_source_names(prior: dict[str, Any]) -> list[str]:
    translated = require_dict(prior.get("translated_source"), "prior translated source")
    names: list[str] = []
    for number in range(1, 17):
        chapter = require_dict(translated.get(f"chapter_{number:02d}"), "prior chapter")
        for raw in require_list(chapter.get("files"), "prior source files"):
            row = require_dict(raw, "prior source row")
            relative = safe_relative(row.get("path"))
            if not relative.startswith("source/"):
                raise RuntimeError(f"prior source path escaped source tree: {relative}")
            assert_identity(relative, row, identity(ROOT / relative))
            names.append(relative.removeprefix("source/"))
    if len(names) != len(set(names)):
        raise RuntimeError("prior source closure repeats a file")
    return names


def inherited_inventory_rows(prior: dict[str, Any]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for raw in require_list(prior.get("package_source_inventory"), "prior inventory"):
        row = require_dict(raw, "prior inventory row")
        raw_path = row.get("path")
        if not isinstance(raw_path, str):
            raise RuntimeError("prior inventory row has no path")
        if raw_path.startswith("repo/"):
            rows.append(repo_row(safe_relative(raw_path)))
        elif raw_path.startswith("00_control/"):
            rows.append({"path": raw_path, **identity(LANE / raw_path)})
        else:
            raise RuntimeError(f"unsupported inherited package path: {raw_path}")
    return rows


def build_manifest() -> dict[str, Any]:
    prior = read_json(PRIOR_MANIFEST)
    require_pass(prior, "Chapter 16 source manifest")
    if prior.get("boundary") != PRIOR_BOUNDARY or prior.get("pending_evidence") != []:
        raise RuntimeError("unexpected Chapter 16 admission boundary")
    prior_names = inherited_source_names(prior)

    source_qa = read_json(SOURCE_QA)
    require_pass(source_qa, "Chapter 17 source QA")
    if source_qa.get("failures") != []:
        raise RuntimeError("Chapter 17 source QA records failures")
    qa_sources: dict[str, dict[str, Any]] = {}
    for raw in require_list(source_qa.get("files"), "Chapter 17 source QA files"):
        row = require_dict(raw, "Chapter 17 source QA row")
        name = row.get("file")
        if not isinstance(name, str) or not name or "/" in name or "\\" in name:
            raise RuntimeError(f"invalid Chapter 17 source filename: {name!r}")
        if name in qa_sources:
            raise RuntimeError(f"duplicate Chapter 17 source filename: {name}")
        qa_sources[name] = row
    if set(qa_sources) != set(CHAPTER_SOURCE_FILES):
        raise RuntimeError("Chapter 17 source-QA closure differs from target")

    translated_rows: list[dict[str, object]] = []
    authority_rows: list[dict[str, object]] = []
    for name in CHAPTER_SOURCE_FILES:
        qa_row = qa_sources[name]
        translated_row = repo_row(f"source/{name}")
        upstream_row = authority_row(name)
        assert_identity(f"translated source {name}", qa_row.get("translated"), translated_row)
        assert_identity(f"authority source {name}", qa_row.get("authority"), upstream_row)
        translated_rows.append(translated_row)
        authority_rows.append(upstream_row)
    chapter_combined = combined_named_files(ROOT / "source", CHAPTER_SOURCE_FILES)
    if source_qa.get("combined_translated_sha256") != chapter_combined:
        raise RuntimeError("Chapter 17 translated combined identity is stale")

    backend, companion_rows, counts = validate_final_companion()
    reader_text = (ROOT / READER_WRAPPER).read_text(encoding="utf-8")
    if MODEL not in reader_text:
        raise RuntimeError("Chapter 17 reader lacks exact model provenance")
    expected_reader_hrefs = [*READER_CHAPTER_INCLUDES, *READER_COMPANION_INCLUDES]
    if include_hrefs(READER_WRAPPER) != expected_reader_hrefs:
        raise RuntimeError("Chapter 17 reader include order changed")
    validate_project_targets()
    validate_schema_receipt(WRAPPER_SCHEMA_QA, COMPANION_WRAPPER)
    validate_schema_receipt(MASTERY_SCHEMA_QA, "companion/chapter_17_mastery.ptx")
    validate_schema_receipt(SCHEMA_QA, READER_WRAPPER)

    html_manifest = read_json(HTML_MANIFEST)
    html_qa = read_json(HTML_QA)
    browser_qa = read_json(BROWSER_QA)
    require_pass(html_qa, "Chapter 17 HTML QA")
    require_pass(browser_qa, "Chapter 17 browser QA")
    html_facts = validate_html(html_manifest)
    run_1 = read_json(HTML_RUN_1)
    run_2 = read_json(HTML_RUN_2)
    for key in ("file_count", "html_files", "total_bytes", "canonical_manifest_sha256"):
        values = (run_1.get(key), run_2.get(key), html_manifest.get(key))
        if values[0] != values[1] or values[1] != values[2]:
            raise RuntimeError(f"Chapter 17 HTML double-build differs for {key}")
    for key, value in zip(("file_count", "html_files", "total_bytes"), html_facts):
        if html_qa.get(key) != value:
            raise RuntimeError(f"Chapter 17 HTML QA differs for {key}")
    if html_qa.get("canonical_manifest_sha256") != html_manifest.get(
        "canonical_manifest_sha256"
    ):
        raise RuntimeError("Chapter 17 HTML canonical identity differs")

    pdf_row = repo_row(PDF_PATH)
    pdf_pages, snapshot_row = validate_pdf(pdf_row)

    qa_rows: dict[str, dict[str, object]] = {}
    json_without_status = {HTML_MANIFEST, HTML_RUN_1, HTML_RUN_2}
    for relative in QA_FILES:
        if relative.endswith(".json") and relative not in json_without_status:
            require_pass(read_json(relative), relative)
        qa_rows[relative] = repo_row(relative)
    evidence_rows = collect_evidence_rows(browser_qa)

    translated = dict(require_dict(prior.get("translated_source"), "prior source"))
    translated["chapter_17"] = {
        "admission": "complete cumulative reader admission",
        "source_qa": qa_rows[SOURCE_QA],
        "combined_sha256": chapter_combined,
        "files": translated_rows,
        "authority_files": authority_rows,
        "approved_external_xrefs": source_qa.get("approved_external_xref_targets"),
    }
    all_names = [*prior_names, *CHAPTER_SOURCE_FILES]
    translated["cumulative_combined_sha256"] = combined_named_files(
        ROOT / "source", all_names
    )
    translated["combined_algorithm"] = (
        "SHA-256 over each ordered source filename, one NUL byte, then exact file bytes"
    )

    inventory_rows = inherited_inventory_rows(prior)
    inventory_rows.extend(repo_row(path) for path in PACKAGE_ROOT_FILES)
    inventory_rows.extend(repo_row(f"source/{name}") for name in all_names)
    inventory_rows.append(repo_row(READER_WRAPPER))
    inventory_rows.extend(companion_rows)
    inventory_rows.extend(repo_row(path) for path in BACKEND_FILES)
    inventory_rows.extend(qa_rows.values())
    inventory_rows.extend(evidence_rows)
    inventory_rows.append(repo_row("scripts/build_chapter17_source_manifest.py"))
    inventory_rows.append(repo_row(PRIOR_MANIFEST))
    inventory = unique_rows(inventory_rows)

    prior_archive = require_dict(
        prior.get("package_authority_archive"), "prior authority archive"
    )
    archive_relative = prior_archive.get("path")
    if not isinstance(archive_relative, str) or not archive_relative.startswith(
        "authority/archives/"
    ):
        raise RuntimeError("prior authority archive path changed")
    current_archive_identity = identity(LANE / archive_relative)
    assert_identity("authority archive", prior_archive, current_archive_identity)
    authority_archive = {**prior_archive, **current_archive_identity}

    cumulative_companions = [
        row for row in inventory if str(row["path"]).startswith("repo/companion/")
    ]
    cumulative_backends = [
        row for row in inventory if str(row["path"]).startswith("repo/backend/")
    ]
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
        "prior_admission": {
            "path": f"repo/{PRIOR_MANIFEST}",
            **identity(ROOT / PRIOR_MANIFEST),
        },
        "authority": prior.get("authority"),
        "translated_source": translated,
        "chapter_17_identity_bundle": {
            "cumulative_reader_wrapper": repo_row(READER_WRAPPER),
            "source_qa": qa_rows[SOURCE_QA],
            "companion_qa": qa_rows[COMPANION_QA],
            "companion_wrapper": repo_row(COMPANION_WRAPPER),
            "companion_files": companion_rows[1:],
            "backend_files": [repo_row(path) for path in BACKEND_FILES],
            "companion_wrapper_schema_qa": qa_rows[WRAPPER_SCHEMA_QA],
            "mastery_schema_qa": qa_rows[MASTERY_SCHEMA_QA],
            "schema_qa": qa_rows[SCHEMA_QA],
            "project": repo_row("project.ptx"),
        },
        "cumulative_component_identities": {
            "translated_source_chapters_01_17": {
                "file_count": len(all_names),
                "chapters": [f"chapter_{number:02d}" for number in range(1, 18)],
                "cumulative_combined_sha256": translated[
                    "cumulative_combined_sha256"
                ],
            },
            "companions_chapters_01_17": cumulative_companions,
            "backends_chapters_01_17": cumulative_backends,
        },
        "companion_coverage": {
            **counts,
            "surfaces_per_entry": ["statement", "hint", "answer", "solution"],
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
                "canonical_manifest_sha256": html_manifest.get(
                    "canonical_manifest_sha256"
                ),
                "manifest": qa_rows[HTML_MANIFEST],
                "deterministic_run_1": qa_rows[HTML_RUN_1],
                "deterministic_run_2": qa_rows[HTML_RUN_2],
                "qa": qa_rows[HTML_QA],
                "browser_qa": {
                    **qa_rows[BROWSER_QA],
                    "status": "pass",
                    "evidence": evidence_rows,
                },
            },
            "standalone_pdf_asset_metadata_qa": qa_rows[ASSET_PDF_QA],
            "pdf": {
                **pdf_row,
                "status": "pass",
                "pages": pdf_pages,
                "run_1_snapshot": snapshot_row,
                "evidence": {
                    key: qa_rows[path] for key, path in PDF_RECEIPTS.items()
                },
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
            "scope": (
                "translation drafting, original companion, modular backend, "
                "and edition QA"
            ),
            "credit_note": (
                "Model provenance does not replace source-author, institutional, "
                "or human-contributor credits."
            ),
        },
        "package_source_inventory": inventory,
        "package_authority_archive": authority_archive,
        "known_caveats": [
            "This is a complete admitted 17-of-20 cumulative reader boundary, not the complete edition.",
            "HTML remains the primary accessible surface unless the admitted PDF receipt reports tagging.",
            "Whole-book figure-provenance and complete-edition closure remain later gates.",
        ],
    }
    if (
        manifest["partial"] is not True
        or manifest["boundary_complete"] is not True
        or manifest["pending_evidence"] != []
        or manifest["admission_status"] != "partial_checkpoint_admitted"
    ):
        raise RuntimeError("Chapter 17 checkpoint scope is represented incorrectly")
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate the frozen admission closure without writing the manifest.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = build_manifest()
    except (FileNotFoundError, RuntimeError, json.JSONDecodeError, ET.ParseError) as exc:
        raise SystemExit(f"Chapter 17 admission manifest gate failed: {exc}") from exc
    summary = {
        "status": manifest["status"],
        "partial": manifest["partial"],
        "boundary": manifest["boundary"],
        "source_files": manifest["cumulative_component_identities"][
            "translated_source_chapters_01_17"
        ]["file_count"],
        "package_inventory_files": len(manifest["package_source_inventory"]),
        "check_only": args.check_only,
    }
    if not args.check_only:
        payload = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        temporary = OUTPUT.with_name(f".{OUTPUT.name}.tmp")
        temporary.write_text(payload, encoding="utf-8", newline="\n")
        temporary.replace(OUTPUT)
        summary.update(
            {
                "output": "repo/qa/CHAPTER17_SOURCE_MANIFEST.json",
                **identity(OUTPUT),
            }
        )
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
