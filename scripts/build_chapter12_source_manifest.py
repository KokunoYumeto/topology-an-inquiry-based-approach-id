#!/usr/bin/env python3
"""Build the fail-closed cumulative Chapters 1-12 admission manifest.

Run only after the Chapter 12 source, final companion/backend, cumulative
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


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
AUTHORITY_SOURCE = LANE / "authority/gvsu-pinned/topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9/source"
AUTHORITY_ARCHIVE = LANE / "authority/archives/gvsuoer-topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9.zip"
OUTPUT = ROOT / "qa/CHAPTER12_SOURCE_MANIFEST.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"

PRIOR_MANIFEST = "qa/CHAPTER11_SOURCE_MANIFEST.json"
PRIOR_MANIFEST_IDENTITY = {
    "bytes": 127_524,
    "sha256": "72760069b015de0db2b4a7d0df921203c37404f039c930cf1d80ceab6c41d0ba",
}
BOUNDARY = "chapters_01_12_with_separately_licensed_self_study_companions"
PRIOR_BOUNDARY = "chapters_01_11_with_separately_licensed_self_study_companions"

CHAPTER_SOURCE_FILES = (
    "chap_top_spaces.ptx",
    "sec_top_space_intro.ptx",
    "sec_exam_top.ptx",
    "sec_base_top.ptx",
    "sec_metric_top_space.ptx",
    "sec_neighborhood_top_space.ptx",
    "sec_interior_set_top.ptx",
    "sec_top_space_summ.ptx",
    "sec_top_space_exer.ptx",
)
COMPANION_FILES = (
    "companion/chapter_12_source_guides_a.ptx",
    "companion/chapter_12_source_guides_b.ptx",
    "companion/chapter_12_source_guides_c.ptx",
    "companion/chapter_12_source_guides_d.ptx",
    "companion/chapter_12_source_guides_e.ptx",
    "companion/chapter_12_source_guides_f.ptx",
    "companion/chapter_12_exercise_guides_a.ptx",
    "companion/chapter_12_exercise_guides_b.ptx",
    "companion/chapter_12_exercise_guides_c.ptx",
    "companion/chapter_12_exercise_guides_d.ptx",
    "companion/chapter_12_exercise_guides_e.ptx",
    "companion/chapter_12_exercise_guides_f.ptx",
    "companion/chapter_12_exercise_guides_g.ptx",
    "companion/chapter_12_mastery.ptx",
)
COMPANION_WRAPPER = "companion/chapter_12_topological_spaces_self_study.ptx"
READER_WRAPPER = "source/chapters_01_12_reader.ptx"
FINAL_BACKEND = "backend/chapter_12_companion_manifest.json"
FINAL_ALIASES = "backend/chapter_12_entry_aliases.csv"
PROMPT_MAP = "backend/chapter_12_source_prompt_map.csv"
GROUPING_BACKEND = "backend/chapter_12_grouping_nodes.json"

SOURCE_QA = "qa/CHAPTER12_SOURCE_QA.json"
COMPANION_QA = "qa/CHAPTER12_COMPANION_QA.json"
SCHEMA_QA = "qa/CHAPTER12_CUMULATIVE_SCHEMA_QA.json"
HTML_MANIFEST = "qa/CHAPTER12_HTML_MANIFEST.json"
HTML_RUN_1 = "qa/CHAPTER12_HTML_MANIFEST_RUN1.json"
HTML_RUN_2 = "qa/CHAPTER12_HTML_MANIFEST_RUN2.json"
HTML_QA = "qa/CHAPTER12_HTML_QA.json"
BROWSER_QA = "qa/CHAPTER12_BROWSER_QA.json"
ASSET_PDF_QA = "qa/CHAPTER12_ASSET_PDF_METADATA_QA.json"
PDF_RECEIPTS = {
    "deterministic_run_1": "qa/CHAPTER12_PDF_RUN1_HASH.json",
    "deterministic_run_2": "qa/CHAPTER12_PDF_RUN2_HASH.json",
    "structure_qa": "qa/CHAPTER12_PDF_STRUCTURE.json",
    "visual_qa": "qa/CHAPTER12_PDF_VISUAL_QA.json",
}
DOCS_RECEIPTS = (
    "qa/CHAPTER12_DOCS_MANIFEST.json",
    "qa/CHAPTER12_DOCS_QA.json",
    "qa/CHAPTER12_BUILD_QA.md",
)
HTML_ROOT = "output/chapters01-12-html"
PDF_PATH = "output/chapters01-12-pdf/chapters_01_12_reader.pdf"

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
    "00_control/CHAPTER12_TERMINOLOGY_AUDIT.md",
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


def is_historical_partial_path(relative: str) -> bool:
    name = PurePosixPath(relative).name.casefold()
    return (
        ".partial." in name
        or "chapter12_companion_partial" in name
        or name == "build_zenodo_chapter12_partial_package.py"
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
        raise RuntimeError("cumulative Chapter 12 HTML closure differs from its manifest")
    total = 0
    html_files = 0
    for relative, path in actual.items():
        current = identity(path)
        assert_identity(f"HTML {relative}", expected[relative], current)
        total += int(current["bytes"])
        html_files += relative.casefold().endswith(".html")
    facts = (len(actual), html_files, total)
    if facts != (manifest.get("file_count"), manifest.get("html_files"), manifest.get("total_bytes")):
        raise RuntimeError("cumulative Chapter 12 HTML census differs")
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
    expected_status = "companion_complete_reader_admission_pending"
    if backend.get("partial") is not False or backend.get("status") != expected_status:
        raise RuntimeError("Chapter 12 backend is partial or has not reached final companion status")
    if companion_qa.get("status") != expected_status:
        raise RuntimeError("Chapter 12 companion QA has not reached final companion status")
    coverage = require_dict(backend.get("coverage_contract"), "backend coverage")
    expected_coverage = {
        "covered_source_prompt_guides": 79,
        "pending_source_prompt_guides": 0,
        "covered_mastery_checks": 8,
        "total_companion_entries": 87,
        "total_staged_surfaces": 348,
        "companion_complete": True,
    }
    for key, expected in expected_coverage.items():
        if coverage.get(key) != expected:
            raise RuntimeError(f"Chapter 12 backend coverage changed: {key}")
    wrapper_text = (ROOT / COMPANION_WRAPPER).read_text(encoding="utf-8")
    missing_includes = [Path(path).name for path in COMPANION_FILES if f'href="./{Path(path).name}"' not in wrapper_text]
    if missing_includes:
        raise RuntimeError(f"Chapter 12 wrapper omits final companion files: {missing_includes}")
    companion_rows = [repo_row(COMPANION_WRAPPER), *[repo_row(path) for path in COMPANION_FILES]]
    qa_files = rows_by_path(companion_qa.get("companion_files"), "companion QA files")
    for row in companion_rows:
        relative = safe_relative(row["path"])
        if relative not in qa_files:
            raise RuntimeError(f"companion QA omits {relative}")
        assert_identity(f"companion QA {relative}", qa_files[relative], row)
    for key, relative in (
        ("prompt_map", PROMPT_MAP),
        ("grouping_nodes", GROUPING_BACKEND),
        ("aliases", FINAL_ALIASES),
    ):
        current = repo_row(relative)
        qa_backend = require_dict(companion_qa.get("backend"), "companion QA backend")
        assert_identity(key, qa_backend.get(key), current)
    return backend, companion_qa, companion_rows


def build_manifest() -> dict[str, Any]:
    assert_identity("pinned Chapter 11 manifest", PRIOR_MANIFEST_IDENTITY, identity(ROOT / PRIOR_MANIFEST))
    prior = read_json(PRIOR_MANIFEST)
    require_pass(prior, "Chapter 11 source manifest")
    if prior.get("boundary") != PRIOR_BOUNDARY or prior.get("pending_evidence") != []:
        raise RuntimeError("unexpected Chapter 11 admission boundary")

    translated = require_dict(prior.get("translated_source"), "prior translated source")
    prior_names: list[str] = []
    for chapter_number in range(1, 12):
        chapter = require_dict(translated.get(f"chapter_{chapter_number:02d}"), "prior chapter")
        for row in require_list(chapter.get("files"), "prior source files"):
            relative = safe_relative(require_dict(row, "prior source row").get("path"))
            if not relative.startswith("source/"):
                raise RuntimeError(f"prior source path escaped source tree: {relative}")
            assert_identity(relative, row, identity(ROOT / relative))
            prior_names.append(relative.removeprefix("source/"))
    if len(prior_names) != 72 or len(set(prior_names)) != 72:
        raise RuntimeError("prior translated source closure is not exactly 72 files")

    source_qa = read_json(SOURCE_QA)
    require_pass(source_qa, "Chapter 12 source QA")
    if source_qa.get("failures") != []:
        raise RuntimeError("Chapter 12 source QA records failures")
    qa_sources: dict[str, dict[str, Any]] = {}
    for raw in require_list(source_qa.get("files"), "Chapter 12 source QA files"):
        row = require_dict(raw, "Chapter 12 source QA row")
        name = row.get("file")
        if not isinstance(name, str) or not name or "/" in name or "\\" in name:
            raise RuntimeError(f"invalid Chapter 12 source-QA filename: {name!r}")
        if name in qa_sources:
            raise RuntimeError(f"duplicate Chapter 12 source-QA filename: {name}")
        qa_sources[name] = row
    if set(qa_sources) != set(CHAPTER_SOURCE_FILES):
        raise RuntimeError("Chapter 12 source QA closure is not the exact nine-file target")
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
        raise RuntimeError("Chapter 12 translated combined identity is stale")

    backend, companion_qa, companion_rows = validate_final_companion()
    reader_text = (ROOT / READER_WRAPPER).read_text(encoding="utf-8")
    if MODEL not in reader_text or "chapter_12_topological_spaces_self_study.ptx" not in reader_text:
        raise RuntimeError("Chapter 12 reader wrapper lacks exact provenance or companion include")
    project_text = (ROOT / "project.ptx").read_text(encoding="utf-8")
    required_target_fragments = (
        '<target name="chapters01-12-html">',
        '<target name="chapters01-12-pdf" pdf-method="xelatex">',
        '<source>source/chapters_01_12_reader.ptx</source>',
        '<output-dir>output/chapters01-12-html</output-dir>',
        '<output-dir>output/chapters01-12-pdf</output-dir>',
    )
    if any(fragment not in project_text for fragment in required_target_fragments):
        raise RuntimeError("project.ptx lacks the exact cumulative Chapter 12 wrapper/targets")

    schema_qa = read_json(SCHEMA_QA)
    require_pass(schema_qa, "Chapter 12 cumulative schema QA")
    html_manifest = read_json(HTML_MANIFEST)
    html_qa = read_json(HTML_QA)
    browser_qa = read_json(BROWSER_QA)
    require_pass(html_qa, "Chapter 12 HTML QA")
    require_pass(browser_qa, "Chapter 12 browser QA")
    html_facts = validate_html(html_manifest)
    for key, value in zip(("file_count", "html_files", "total_bytes"), html_facts):
        if html_qa.get(key) != value:
            raise RuntimeError(f"Chapter 12 HTML QA differs for {key}")
    if html_qa.get("canonical_manifest_sha256") != html_manifest.get("canonical_manifest_sha256"):
        raise RuntimeError("Chapter 12 HTML canonical identity differs")

    pdf_visual = read_json(PDF_RECEIPTS["visual_qa"])
    require_pass(pdf_visual, "Chapter 12 PDF visual QA")
    pdf_row = repo_row(PDF_PATH)
    assert_identity("Chapter 12 PDF", pdf_visual.get("pdf"), pdf_row)
    pdf_pages = pdf_visual.get("pages")
    if not isinstance(pdf_pages, int) or pdf_pages <= 0:
        raise RuntimeError("Chapter 12 PDF visual QA has no positive page count")
    qa_paths = [
        SOURCE_QA, COMPANION_QA, SCHEMA_QA, HTML_MANIFEST, HTML_RUN_1,
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

    chapter_12 = {
        "admission": "complete cumulative reader admission",
        "source_qa": qa_rows[SOURCE_QA],
        "combined_sha256": chapter_combined,
        "files": translated_rows,
        "authority_files": authority_rows,
        "approved_external_xrefs": source_qa.get("approved_external_xref_targets"),
    }
    translated = dict(translated)
    translated["chapter_12"] = chapter_12
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

    authority_archive = {"path": f"authority/archives/{AUTHORITY_ARCHIVE.name}", **identity(AUTHORITY_ARCHIVE)}
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
        "chapter_12_identity_bundle": {
            "cumulative_reader_wrapper": repo_row(READER_WRAPPER),
            "source_qa": qa_rows[SOURCE_QA],
            "companion_qa": qa_rows[COMPANION_QA],
            "companion_wrapper": repo_row(COMPANION_WRAPPER),
            "companion_files": companion_rows[1:],
            "backend": repo_row(FINAL_BACKEND),
            "entry_alias_map": repo_row(FINAL_ALIASES),
            "source_prompt_map": repo_row(PROMPT_MAP),
            "grouping_backend": repo_row(GROUPING_BACKEND),
            "schema_qa": qa_rows[SCHEMA_QA],
            "project": repo_row("project.ptx"),
        },
        "cumulative_component_identities": {
            "translated_source_chapters_01_12": {
                "file_count": 81,
                "chapters": [f"chapter_{number:02d}" for number in range(1, 13)],
                "cumulative_combined_sha256": translated["cumulative_combined_sha256"],
            },
            "companions_chapters_01_12": cumulative_companions,
            "backends_chapters_01_12": cumulative_backends,
        },
        "companion_coverage": {
            "source_prompt_guides": 79,
            "mastery_checks": 8,
            "total_entries": 87,
            "surfaces_per_entry": ["statement", "hint", "answer", "solution"],
            "total_surfaces": 348,
            "grouping_nodes_mapped": 5,
            "backend_status_before_reader_admission": backend.get("status"),
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
            "This is a complete admitted 12-of-20 cumulative reader boundary, not the complete edition.",
            "HTML remains the primary accessible surface unless the admitted PDF receipt reports tagging.",
            "Whole-book figure-provenance and complete-edition closure remain later gates.",
        ],
    }
    if (
        manifest.get("partial") is not True
        or manifest.get("boundary_complete") is not True
        or manifest.get("admission_status") != "partial_checkpoint_admitted"
    ):
        raise RuntimeError("Chapter 12 checkpoint scope is not represented truthfully")
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
        raise SystemExit(f"Chapter 12 admission manifest gate failed: {exc}") from exc
    summary = {
        "status": manifest["status"],
        "partial": manifest["partial"],
        "boundary": manifest["boundary"],
        "source_files": 81,
        "package_inventory_files": len(manifest["package_source_inventory"]),
        "check_only": args.check_only,
    }
    if not args.check_only:
        payload = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        temporary = OUTPUT.with_name(f".{OUTPUT.name}.tmp")
        temporary.write_text(payload, encoding="utf-8", newline="\n")
        temporary.replace(OUTPUT)
        summary.update({"output": "repo/qa/CHAPTER12_SOURCE_MANIFEST.json", **identity(OUTPUT)})
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
