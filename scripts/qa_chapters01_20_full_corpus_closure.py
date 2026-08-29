#!/usr/bin/env python3
"""Fail-closed backend/companion closure gate for the complete 20-chapter reader.

The gate is deliberately bounded to the complete reader, its twenty companion
wrappers and their local XInclude closures, the eight completion modules, and
the already validated component manifests/receipts.  It does not build or
modify reader sources.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from typing import Any, Iterator

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "source" / "chapters_01_20_complete_reader.ptx"
OUTPUT_MANIFEST = ROOT / "backend" / "chapters_01_20_full_corpus_closure_manifest.json"
OUTPUT_QA = ROOT / "qa" / "CHAPTERS01_20_FULL_CORPUS_CLOSURE_QA.json"
COMPLETE_SCHEMA_QA = ROOT / "qa" / "CHAPTERS01_20_COMPLETE_SCHEMA_QA.json"
XI = {"xi": "http://www.w3.org/2001/XInclude"}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"

MAIN_CHAPTER_HREFS = (
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
    "./chap_Connected_topology.ptx",
    "./chap_Path_connected_topology.ptx",
    "./chap_Product_topology.ptx",
)

COMPANION_HREFS = (
    "../companion/chapter_01_sets_self_study.ptx",
    "../companion/chapter_02_functions_self_study.ptx",
    "../companion/chapter_03_metric_spaces_self_study.ptx",
    "../companion/chapter_04_metric_space_applications_self_study.ptx",
    "../companion/chapter_05_greatest_lower_bound_self_study.ptx",
    "../companion/chapter_06_continuous_functions_self_study.ptx",
    "../companion/chapter_07_open_balls_self_study.ptx",
    "../companion/chapter_08_open_sets_self_study.ptx",
    "../companion/chapter_09_sequences_self_study.ptx",
    "../companion/chapter_10_closed_sets_self_study.ptx",
    "../companion/chapter_11_metric_subspaces_self_study.ptx",
    "../companion/chapter_12_topological_spaces_self_study.ptx",
    "../companion/chapter_13_closed_sets_topological_spaces_self_study.ptx",
    "../companion/chapter_14_continuity_homeomorphisms_self_study.ptx",
    "../companion/chapter_15_subspaces_self_study.ptx",
    "../companion/chapter_16_quotient_spaces_self_study.ptx",
    "../companion/chapter_17_compact_spaces_self_study.ptx",
    "../companion/chapter_18_connected_spaces_self_study.ptx",
    "../companion/chapter_19_path_connected_spaces_self_study.ptx",
    "../companion/chapter_20_product_topology_self_study_appendix.ptx",
)

COMPLETION_HREF = "../completion/o003_c90_completion_self_study.ptx"
COMPLETION_MODULE_HREFS = (
    "./module_01_separation_completion.ptx",
    "./module_02_countability_size.ptx",
    "./module_03_nets_general_convergence.ptx",
    "./module_04_arbitrary_products.ptx",
    "./module_05_local_compactness.ptx",
    "./module_06_metrization.ptx",
    "./module_07_function_spaces.ptx",
    "./module_08_integrated_mastery.ptx",
)


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def identity(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {"path": rel(path), "bytes": len(payload), "sha256": sha256(payload)}


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def parse(path: Path) -> etree._ElementTree:
    return etree.parse(
        str(path),
        etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False, huge_tree=True),
    )


def normalize_manifest_path(value: str) -> str:
    value = value.replace("\\", "/")
    if value.startswith("repo/"):
        value = value[5:]
    while value.startswith("./"):
        value = value[2:]
    return value


def asserted_identities(value: Any) -> Iterator[dict[str, Any]]:
    """Yield every manifest-provided path/bytes/SHA identity recursively."""
    if isinstance(value, dict):
        path = value.get("path")
        if isinstance(path, str) and isinstance(value.get("bytes"), int) and isinstance(value.get("sha256"), str):
            yield {"path": normalize_manifest_path(path), "bytes": value["bytes"], "sha256": value["sha256"].lower()}
        for key, child in value.items():
            if (
                isinstance(key, str)
                and isinstance(child, dict)
                and isinstance(child.get("bytes"), int)
                and isinstance(child.get("sha256"), str)
                and ("/" in key or "\\" in key)
            ):
                yield {"path": normalize_manifest_path(key), "bytes": child["bytes"], "sha256": child["sha256"].lower()}
            yield from asserted_identities(child)
    elif isinstance(value, list):
        for child in value:
            yield from asserted_identities(child)


def safe_local_include(owner: Path, href: str) -> Path:
    if "://" in href or href.startswith(("/", "\\")):
        raise SystemExit(f"nonlocal XInclude in {rel(owner)}: {href}")
    target = (owner.parent / href).resolve()
    try:
        target.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise SystemExit(f"XInclude escapes repository in {rel(owner)}: {href}") from exc
    if not target.is_file():
        raise SystemExit(f"missing XInclude target in {rel(owner)}: {href}")
    return target


def xinclude_closure(wrapper: Path) -> list[Path]:
    seen: set[Path] = set()
    ordered: list[Path] = []

    def visit(path: Path) -> None:
        resolved = path.resolve()
        if resolved in seen:
            return
        seen.add(resolved)
        ordered.append(resolved)
        tree = parse(resolved)
        for href in tree.xpath("//xi:include/@href", namespaces=XI):
            visit(safe_local_include(resolved, str(href)))

    visit(wrapper)
    return ordered


def require_marker(text: str, marker: str, owner: str) -> None:
    if " ".join(marker.split()) not in " ".join(text.split()):
        raise SystemExit(f"required marker missing from {owner}: {marker}")


def require_staged_exercises(root: etree._Element, expected_ids: set[str], label: str) -> dict[str, int]:
    exercises = {node.get(XML_ID): node for node in root.xpath(".//exercise") if node.get(XML_ID)}
    if set(exercises) != expected_ids:
        missing = sorted(expected_ids - set(exercises))
        extra = sorted(set(exercises) - expected_ids)
        raise SystemExit(f"{label} exercise IDs changed: missing={missing}, extra={extra}")
    for entry_id, exercise in exercises.items():
        for stage in ("statement", "hint", "answer", "solution"):
            nodes = exercise.findall(stage)
            if len(nodes) != 1:
                raise SystemExit(f"{label} {entry_id} has {len(nodes)} {stage} nodes")
    return {
        "exercises": len(exercises),
        "statements": sum(len(node.findall("statement")) for node in exercises.values()),
        "hints": sum(len(node.findall("hint")) for node in exercises.values()),
        "answers": sum(len(node.findall("answer")) for node in exercises.values()),
        "solutions": sum(len(node.findall("solution")) for node in exercises.values()),
        "staged_surfaces": len(exercises) * 4,
    }


def build_manifest() -> dict[str, Any]:
    if not READER.is_file():
        raise SystemExit("complete reader is missing")
    reader_tree = parse(READER)
    main_hrefs = tuple(reader_tree.xpath("/pretext/book/part/xi:include/@href", namespaces=XI))
    backmatter_hrefs = tuple(reader_tree.xpath("/pretext/book/backmatter/xi:include/@href", namespaces=XI))
    if main_hrefs != MAIN_CHAPTER_HREFS:
        raise SystemExit(f"complete reader main-chapter include contract changed: {main_hrefs}")
    if backmatter_hrefs != COMPANION_HREFS + (COMPLETION_HREF,):
        raise SystemExit(f"complete reader companion/completion include contract changed: {backmatter_hrefs}")
    for href in main_hrefs + backmatter_hrefs:
        safe_local_include(READER, href)

    if not COMPLETE_SCHEMA_QA.is_file():
        raise SystemExit("complete-reader schema receipt is missing")
    complete_schema = json.loads(COMPLETE_SCHEMA_QA.read_text(encoding="utf-8"))
    required_schema_checks = {
        "all_xrefs_resolve",
        "chapter_20_appendix_adapter_is_exact_root_transform",
        "exact_ordered_20_chapter_includes",
        "exact_ordered_20_companion_plus_completion_includes",
        "exact_ordered_8_completion_modules",
        "pinned_schema_identity",
        "prerequisite_receipts_bound_and_passing",
        "reader_well_formed",
        "relaxng_valid",
        "xinclude_closure_complete_local_and_bounded",
        "xml_ids_unique",
    }
    if complete_schema.get("status") != "pass" or complete_schema.get("failures") != [] or complete_schema.get("diagnostics") != []:
        raise SystemExit("complete-reader schema receipt is not a clean pass")
    checks = complete_schema.get("checks", {})
    if set(checks) != required_schema_checks or not all(checks.values()):
        raise SystemExit(f"complete-reader schema check contract changed: {checks}")
    reader_live_identity = identity(READER)
    if complete_schema.get("source") != reader_live_identity:
        raise SystemExit("complete-reader bytes differ from the passing schema receipt")
    direct = complete_schema.get("direct_structure", {})
    if tuple(direct.get("ordered_source_chapter_hrefs", ())) != MAIN_CHAPTER_HREFS:
        raise SystemExit("schema receipt source-chapter include order changed")
    if tuple(direct.get("ordered_backmatter_hrefs", ())) != COMPANION_HREFS + (COMPLETION_HREF,):
        raise SystemExit("schema receipt companion/completion include order changed")
    if tuple(direct.get("ordered_completion_module_hrefs", ())) != COMPLETION_MODULE_HREFS:
        raise SystemExit("schema receipt completion-module include order changed")
    if direct.get("source_chapters") != 20 or direct.get("self_study_companions") != 20 or direct.get("completion_modules") != 8:
        raise SystemExit("schema receipt direct include census changed")
    expanded = complete_schema.get("expanded_document", {})
    closure_receipt = complete_schema.get("xinclude_closure", {})
    if expanded.get("duplicate_xml_ids") != [] or expanded.get("unresolved_xrefs") != [] or closure_receipt.get("all_local_and_repo_bounded") is not True:
        raise SystemExit("complete-reader expanded closure no longer passes")

    reader_text = READER.read_text(encoding="utf-8")
    reader_markers = (
        "CC BY-NC-SA 3.0",
        "CC BY 4.0",
        "komponen CC BY 4.0 yang terpisah",
        "tidak diratakan menjadi satu lisensi",
        "tidak ada dukungan resmi",
        "OpenAI Codex gpt-5.6-sol, Ultra",
    )
    for marker in reader_markers:
        require_marker(reader_text, marker, rel(READER))

    companion_records: list[dict[str, Any]] = []
    manifest_inputs: list[dict[str, Any]] = []
    total_companion_closure_files = 0
    for chapter, href in enumerate(COMPANION_HREFS, 1):
        wrapper = safe_local_include(READER, href)
        expected_wrapper_rel = f"companion/{Path(href).name}"
        manifest_wrapper_rel = (
            "companion/chapter_20_product_topology_self_study.ptx"
            if chapter == 20
            else expected_wrapper_rel
        )
        if rel(wrapper) != expected_wrapper_rel:
            raise SystemExit(f"Chapter {chapter} wrapper resolved unexpectedly: {rel(wrapper)}")
        manifest_path = ROOT / "backend" / f"chapter_{chapter:02d}_companion_manifest.json"
        if not manifest_path.is_file():
            raise SystemExit(f"Chapter {chapter} companion manifest is missing")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest_input = identity(manifest_path)
        manifest_inputs.append(manifest_input)
        status = manifest.get("status")
        if isinstance(status, str) and "complete" not in status:
            raise SystemExit(f"Chapter {chapter} manifest status is not complete: {status}")
        if manifest.get("partial") is True:
            raise SystemExit(f"Chapter {chapter} manifest is marked partial")
        serialized = json.dumps(manifest, ensure_ascii=False)
        if manifest_wrapper_rel not in normalize_manifest_path(serialized):
            # Normalizing a whole JSON string is intentionally only a reference-presence gate.
            if f"repo/{manifest_wrapper_rel}" not in serialized and manifest_wrapper_rel not in serialized:
                raise SystemExit(f"Chapter {chapter} manifest does not reference its wrapper")

        closure = xinclude_closure(wrapper)
        total_companion_closure_files += len(closure)
        closure_identities = [identity(path) for path in closure]
        closure_map = {item["path"]: item for item in closure_identities}
        asserted = list(asserted_identities(manifest))
        asserted_companion: dict[str, dict[str, Any]] = {}
        for item in asserted:
            path = item["path"]
            if not path.startswith("companion/"):
                continue
            prior = asserted_companion.get(path)
            if prior is not None and prior != item:
                raise SystemExit(f"Chapter {chapter} manifest contains conflicting identities for {path}")
            asserted_companion[path] = item

        wrapper_assertion = asserted_companion.get(manifest_wrapper_rel)
        if wrapper_assertion is not None:
            manifest_wrapper_path = ROOT / manifest_wrapper_rel
            if not manifest_wrapper_path.is_file():
                raise SystemExit(f"Chapter {chapter} manifest wrapper is missing: {manifest_wrapper_rel}")
            manifest_wrapper_live = identity(manifest_wrapper_path)
            if (
                manifest_wrapper_live["bytes"] != wrapper_assertion["bytes"]
                or manifest_wrapper_live["sha256"] != wrapper_assertion["sha256"]
            ):
                raise SystemExit(f"Chapter {chapter} manifest wrapper identity changed: {manifest_wrapper_rel}")
        wrapper_live = closure_map[expected_wrapper_rel]
        chapter20_coverage: dict[str, Any] | None = None
        if chapter == 20:
            expected_coverage = {
                "canonical_source_prompt_covered": 56,
                "canonical_source_prompt_total": 56,
                "exercise_covered": 25,
                "mastery_checks": 8,
                "mastery_staged_surfaces": 32,
                "nonexercise_covered": 31,
                "pending": 0,
                "source_support_staged_surfaces": 224,
                "total_staged_surfaces": 256,
            }
            if manifest.get("coverage") != expected_coverage:
                raise SystemExit(f"Chapter 20 manifest coverage changed: {manifest.get('coverage')}")
            component = manifest.get("component", {})
            if component.get("license") != "CC BY 4.0" or component.get("model_provenance") != "OpenAI Codex gpt-5.6-sol, Ultra" or component.get("nonendorsement") is not True:
                raise SystemExit("Chapter 20 component rights/provenance markers changed")
            chapter20_coverage = expected_coverage

        companion_records.append(
            {
                "chapter": chapter,
                "reader_include": href,
                "wrapper": wrapper_live,
                "manifest_wrapper": manifest_wrapper_rel,
                "manifest_wrapper_identity_asserted_and_matching": wrapper_assertion is not None,
                "component_manifest": manifest_input,
                "component_manifest_status": status if status is not None else "legacy-complete-manifest-without-status-field",
                "closure_file_count": len(closure_identities),
                "closure_files": closure_identities,
                "manifest_asserted_companion_identity_count": len(asserted_companion),
                **({"coverage": chapter20_coverage} if chapter20_coverage is not None else {}),
            }
        )

    # Re-prove the Chapter 20 live staged surface while treating its manifest as
    # the authoritative expected-count contract.
    chapter20_wrapper = safe_local_include(READER, COMPANION_HREFS[19])
    chapter20_tree = parse(chapter20_wrapper)
    chapter20_tree.xinclude()
    chapter20_support_ids = {
        *{f"o003-c90-ch20-guide-{i:02d}" for i in range(1, 32)},
        *{f"o003-c90-ch20-exer-a-{i:02d}" for i in range(1, 11)},
        *{f"o003-c90-ch20-exer-b-{i:02d}" for i in range(1, 11)},
        *{f"o003-c90-ch20-exer-c-{i:02d}" for i in range(1, 6)},
    }
    chapter20_mastery_ids = {f"o003-c90-ch20-mastery-{i:02d}" for i in range(1, 9)}
    chapter20_live = require_staged_exercises(
        chapter20_tree.getroot(), chapter20_support_ids | chapter20_mastery_ids, "Chapter 20 companion"
    )
    if chapter20_live != {
        "exercises": 64,
        "statements": 64,
        "hints": 64,
        "answers": 64,
        "solutions": 64,
        "staged_surfaces": 256,
    }:
        raise SystemExit(f"Chapter 20 live staged counts changed: {chapter20_live}")
    chapter20_manifest_path = ROOT / "backend" / "chapter_20_companion_manifest.json"
    chapter20_manifest = json.loads(chapter20_manifest_path.read_text(encoding="utf-8"))
    chapter20_schema_path = ROOT / str(chapter20_manifest["qa"]["schema"])
    chapter20_content_path = ROOT / str(chapter20_manifest["qa"]["content"])
    for receipt in (chapter20_schema_path, chapter20_content_path):
        if json.loads(receipt.read_text(encoding="utf-8")).get("status") != "pass":
            raise SystemExit(f"Chapter 20 validated receipt no longer passes: {rel(receipt)}")

    # Re-prove the completion wrapper and compare exact identities/counts to its
    # current validated manifest and schema receipt.
    completion_wrapper = safe_local_include(READER, COMPLETION_HREF)
    completion_text = completion_wrapper.read_text(encoding="utf-8")
    completion_markers = (
        "CC BY 4.0 yang terpisah",
        "CC BY-NC-SA 3.0",
        "tidak diratakan menjadi satu lisensi",
        "bukan teks maupun solusi resmi",
        "tidak menyatakan ataupun menyiratkan dukungan mereka",
        "OpenAI Codex gpt-5.6-sol, Ultra",
    )
    for marker in completion_markers:
        require_marker(completion_text, marker, rel(completion_wrapper))
    completion_raw_tree = parse(completion_wrapper)
    completion_hrefs = tuple(completion_raw_tree.xpath("//xi:include/@href", namespaces=XI))
    if completion_hrefs != COMPLETION_MODULE_HREFS:
        raise SystemExit(f"completion wrapper module include contract changed: {completion_hrefs}")

    current_manifest_path = ROOT / "backend" / "o003_completion_current_manifest.json"
    current_qa_path = ROOT / "qa" / "O003_COMPLETION_CURRENT_QA.json"
    schema_qa_path = ROOT / "qa" / "O003_COMPLETION_MODULES01_08_SCHEMA_QA.json"
    current_manifest = json.loads(current_manifest_path.read_text(encoding="utf-8"))
    current_qa = json.loads(current_qa_path.read_text(encoding="utf-8"))
    schema_qa = json.loads(schema_qa_path.read_text(encoding="utf-8"))
    manifest_inputs.extend([identity(current_manifest_path), identity(current_qa_path), identity(schema_qa_path)])
    expected_completion_counts = {
        "answers": 56,
        "hints": 56,
        "mastery_exercises": 56,
        "module_elements": 3430,
        "modules": 8,
        "reader_xml_ids": 381,
        "reader_xrefs": 1,
        "solutions": 56,
        "stable_module_ids": 378,
        "staged_surfaces": 224,
    }
    if current_manifest.get("status") != "modules_01_08_complete_schema_and_backend_qa_pass":
        raise SystemExit("completion current manifest status changed")
    if current_manifest.get("remaining_modules") != [] or current_manifest.get("cumulative_counts") != expected_completion_counts:
        raise SystemExit("completion current manifest count/remaining-module contract changed")
    if current_manifest.get("component_license") != "CC BY 4.0" or current_manifest.get("source_spine_license_context") != "CC BY-NC-SA 3.0 (conservative treatment)" or current_manifest.get("model_provenance") != "OpenAI Codex gpt-5.6-sol, Ultra" or current_manifest.get("nonendorsement") is not True:
        raise SystemExit("completion current manifest rights/provenance contract changed")
    if current_qa.get("status") != "pass" or current_qa.get("counts") != expected_completion_counts or current_qa.get("failures") != []:
        raise SystemExit("completion current QA contract changed")
    if schema_qa.get("status") != "pass" or schema_qa.get("counts", {}).get("modules") != 8 or schema_qa.get("diagnostics") != [] or schema_qa.get("failures") != []:
        raise SystemExit("completion schema QA contract changed")

    wrapper_manifest_identity = current_manifest.get("wrapper")
    wrapper_live_identity = identity(completion_wrapper)
    if wrapper_manifest_identity != wrapper_live_identity:
        raise SystemExit("completion wrapper identity differs from current manifest")
    module_manifest_identities = [module["file"] for module in current_manifest.get("modules", [])]
    if len(module_manifest_identities) != 8 or module_manifest_identities != schema_qa.get("modules"):
        raise SystemExit("completion module identities differ between validated manifests")
    for href, expected in zip(COMPLETION_MODULE_HREFS, module_manifest_identities):
        module_path = safe_local_include(completion_wrapper, href)
        live = identity(module_path)
        if live != expected:
            raise SystemExit(f"completion module identity changed: {rel(module_path)}")

    completion_tree = parse(completion_wrapper)
    completion_tree.xinclude()
    completion_ids = {
        item["id"]
        for module in current_manifest["modules"]
        for item in module["mastery_exercises"]
    }
    if len(completion_ids) != 56:
        raise SystemExit("completion manifest no longer provides 56 unique mastery exercise IDs")
    completion_live = require_staged_exercises(completion_tree.getroot(), completion_ids, "completion Modules 1--8")
    if completion_live != {
        "exercises": 56,
        "statements": 56,
        "hints": 56,
        "answers": 56,
        "solutions": 56,
        "staged_surfaces": 224,
    }:
        raise SystemExit(f"completion live staged counts changed: {completion_live}")

    # Bind every prerequisite receipt identity named by the passing whole-reader
    # schema receipt.  These are the validated sources for Chapter 20 and the
    # eight completion modules; no semantic counts are inferred from XML alone.
    for item in complete_schema.get("prerequisite_receipts", []):
        target = ROOT / item["path"]
        if not target.is_file() or identity(target) != item:
            raise SystemExit(f"whole-reader prerequisite receipt identity changed: {item['path']}")
    manifest_inputs.append(identity(COMPLETE_SCHEMA_QA))
    manifest_inputs = sorted(manifest_inputs, key=lambda item: item["path"])
    return {
        "schema_version": 1,
        "status": "pass",
        "partial": False,
        "lane_id": "O003/C90",
        "locale": "id-ID",
        "reader": reader_live_identity,
        "complete_schema_receipt": identity(COMPLETE_SCHEMA_QA),
        "direct_include_contract": {
            "main_chapter_count": 20,
            "main_chapters": list(MAIN_CHAPTER_HREFS),
            "companion_count": 20,
            "companions": list(COMPANION_HREFS),
            "completion": COMPLETION_HREF,
            "exact_order_match": True,
            "all_targets_local_and_present": True,
        },
        "chapter_companions": companion_records,
        "chapter20": {
            "manifest": identity(chapter20_manifest_path),
            "schema_receipt": identity(chapter20_schema_path),
            "content_receipt": identity(chapter20_content_path),
            "source_support_entries": 56,
            "mastery_entries": 8,
            "live_staged_counts": chapter20_live,
            "manifest_coverage": chapter20_manifest["coverage"],
        },
        "completion": {
            "wrapper": wrapper_live_identity,
            "module_include_count": 8,
            "module_includes": list(COMPLETION_MODULE_HREFS),
            "module_identities": module_manifest_identities,
            "current_manifest": identity(current_manifest_path),
            "current_qa": identity(current_qa_path),
            "schema_qa": identity(schema_qa_path),
            "manifest_counts": expected_completion_counts,
            "live_staged_counts": completion_live,
        },
        "rights_and_provenance": {
            "source_derivative": "CC BY-NC-SA 3.0 (conservative treatment)",
            "original_companions_and_completion": "CC BY 4.0 separate components",
            "licenses_not_flattened": True,
            "nonendorsement": True,
            "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
            "reader_markers": list(reader_markers),
            "completion_markers": list(completion_markers),
        },
        "counts": {
            "main_chapter_includes": 20,
            "chapter_companion_includes": 20,
            "chapter_companion_manifests": 20,
            "chapter_companion_closure_files": total_companion_closure_files,
            "completion_modules": 8,
            "chapter20_source_support_entries": 56,
            "chapter20_mastery_entries": 8,
            "chapter20_staged_surfaces": 256,
            "completion_mastery_exercises": 56,
            "completion_staged_surfaces": 224,
        },
        "manifest_inputs": manifest_inputs,
        "qa_receipt": "qa/CHAPTERS01_20_FULL_CORPUS_CLOSURE_QA.json",
    }


def build_outputs() -> dict[Path, bytes]:
    manifest = build_manifest()
    manifest_payload = json_bytes(manifest)
    qa = {
        "schema_version": 1,
        "status": "pass",
        "failures": [],
        "checks": {
            "reader_exactly_20_main_chapter_includes": True,
            "reader_exactly_20_companion_includes": True,
            "all_reader_include_targets_local_and_present": True,
            "all_20_companion_manifests_present": True,
            "component_manifests_bound_and_manifest_wrapper_identities_checked_when_asserted": True,
            "all_companion_xinclude_closures_local_and_present": True,
            "chapter20_56_source_supports": True,
            "chapter20_8_mastery_entries": True,
            "chapter20_256_staged_surfaces": True,
            "completion_exactly_modules_01_08": True,
            "completion_56_exercises": True,
            "completion_224_staged_surfaces": True,
            "completion_module_identities_match_validated_manifests": True,
            "separate_rights_markers_present": True,
            "exact_model_provenance_present": True,
            "nonendorsement_markers_present": True,
        },
        "counts": manifest["counts"],
        "reader": manifest["reader"],
        "backend_manifest": {
            "path": OUTPUT_MANIFEST.relative_to(ROOT).as_posix(),
            "bytes": len(manifest_payload),
            "sha256": sha256(manifest_payload),
        },
        "authoritative_component_inputs": manifest["manifest_inputs"],
    }
    return {OUTPUT_MANIFEST: manifest_payload, OUTPUT_QA: json_bytes(qa)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = build_outputs()
    if args.check:
        stale = [str(path.relative_to(ROOT)) for path, payload in outputs.items() if not path.exists() or path.read_bytes() != payload]
        if stale:
            raise SystemExit("stale full-corpus closure outputs: " + ", ".join(stale))
        print("PASS: 20 companions + Chapter 20 support + Modules 1--8 closure are deterministic")
        return
    for path, payload in outputs.items():
        path.write_bytes(payload)
        print(f"WROTE {path.relative_to(ROOT)} {len(payload)} bytes sha256={sha256(payload)}")


if __name__ == "__main__":
    main()
