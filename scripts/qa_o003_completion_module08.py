#!/usr/bin/env python3
"""Build deterministic backend and content-QA receipts for completion Module 8."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from typing import Any

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "completion" / "module_08_integrated_mastery.ptx"
READER = ROOT / "source" / "o003_completion_module_08_reader.ptx"
SCHEMA_QA = ROOT / "qa" / "O003_COMPLETION_MODULE08_SCHEMA_QA.json"
MANIFEST = ROOT / "backend" / "o003_completion_module_08_manifest.json"
CONTENT_QA = ROOT / "qa" / "O003_COMPLETION_MODULE08_CONTENT_QA.json"
RECEIPT = ROOT / "qa" / "O003_COMPLETION_MODULE08_BACKEND_RECEIPT.md"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
EXACT_MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
MODULE_ID = "o003-c90-completion-integrated-mastery"
EXPECTED_EXERCISES = 12

EXERCISE_DEPENDENCIES: dict[str, list[int]] = {
    "o003-c90-completion-integrated-ex-01": [1],
    "o003-c90-completion-integrated-ex-02": [2, 3],
    "o003-c90-completion-integrated-ex-03": [2, 6],
    "o003-c90-completion-integrated-ex-04": [2, 4, 6],
    "o003-c90-completion-integrated-ex-05": [4, 5],
    "o003-c90-completion-integrated-ex-06": [1, 2, 5, 6],
    "o003-c90-completion-integrated-ex-07": [3, 7],
    "o003-c90-completion-integrated-ex-08": [2, 7],
    "o003-c90-completion-integrated-ex-09": [4, 5, 7],
    "o003-c90-completion-integrated-ex-10": [1, 2],
    "o003-c90-completion-integrated-ex-11": [1, 2, 4, 6],
    "o003-c90-completion-integrated-ex-12": [1, 2, 3, 5, 6, 7],
}

DEPENDENCY_MAP_IDS = {
    "o003-c90-mastery-map-foundations",
    "o003-c90-mastery-map-convergence",
    "o003-c90-mastery-map-products",
    "o003-c90-mastery-map-compactification",
    "o003-c90-mastery-map-function-spaces",
    "o003-c90-mastery-map-synthesis",
}
RUBRIC_IDS = {"o003-c90-rubric-proof", "o003-c90-rubric-counterexample"}


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def identity(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(payload), "sha256": sha256(payload)}


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def parse(path: Path) -> etree._ElementTree:
    return etree.parse(str(path), etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False))


def local_name(node: etree._Element) -> str:
    return etree.QName(node).localname


def text(node: etree._Element) -> str:
    return " ".join("".join(node.itertext()).split())


def c14n_sha256(node: etree._Element) -> str:
    return sha256(etree.tostring(node, method="c14n", with_comments=True))


def build() -> tuple[bytes, bytes, bytes]:
    schema = json.loads(SCHEMA_QA.read_text(encoding="utf-8"))
    if schema.get("status") != "pass" or schema.get("diagnostics") or schema.get("failures"):
        raise SystemExit("Module 8 pinned-schema gate has not passed")

    module_tree = parse(MODULE)
    reader_tree = parse(READER)
    reader_tree.xinclude()
    module_root = module_tree.getroot()
    reader_root = reader_tree.getroot()
    nodes = [node for node in reader_root.iter() if isinstance(node.tag, str)]
    module_nodes = [node for node in module_root.iter() if isinstance(node.tag, str)]
    ids = [node.get(XML_ID) for node in nodes if node.get(XML_ID)]
    module_ids = [node.get(XML_ID) for node in module_nodes if node.get(XML_ID)]
    refs = [node.get("ref") for node in nodes if local_name(node) == "xref" and node.get("ref")]
    duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
    unresolved = sorted(set(refs) - set(ids))

    tag_counts = Counter(local_name(node) for node in module_nodes)
    exercises = [node for node in module_nodes if local_name(node) == "exercise"]
    expected_ids = [f"o003-c90-completion-integrated-ex-{number:02d}" for number in range(1, EXPECTED_EXERCISES + 1)]
    observed_ids = [node.get(XML_ID) for node in exercises]
    stage_failures: list[str] = []
    mastery: list[dict[str, Any]] = []
    for exercise in exercises:
        entry_id = exercise.get(XML_ID)
        children = [child for child in exercise if isinstance(child.tag, str)]
        names = [local_name(child) for child in children]
        if names != ["title", "statement", "hint", "answer", "solution"]:
            stage_failures.append(f"{entry_id}: wrong staged child order {names}")
            continue
        title, statement, hint, answer, solution = children
        expected_stage_ids = {
            "hint": f"{entry_id}-hint",
            "answer": f"{entry_id}-answer",
            "solution": f"{entry_id}-solution",
        }
        observed_stage_ids = {"hint": hint.get(XML_ID), "answer": answer.get(XML_ID), "solution": solution.get(XML_ID)}
        if observed_stage_ids != expected_stage_ids:
            stage_failures.append(f"{entry_id}: wrong stage IDs {observed_stage_ids}")
        lengths = {
            name: len(text(node))
            for name, node in (("statement", statement), ("hint", hint), ("answer", answer), ("solution", solution))
        }
        if lengths["statement"] < 100 or lengths["hint"] < 80 or lengths["answer"] < 80 or lengths["solution"] < 400:
            stage_failures.append(f"{entry_id}: underspecified staged content {lengths}")
        mastery.append({
            "id": entry_id,
            "title": text(title),
            "status": "complete",
            "depends_on_completion_modules": EXERCISE_DEPENDENCIES.get(entry_id, []),
            "stage_ids": {"statement": entry_id, **expected_stage_ids},
            "surface_characters": lengths,
            "surface_c14n_sha256": {
                "statement": c14n_sha256(statement),
                "hint": c14n_sha256(hint),
                "answer": c14n_sha256(answer),
                "solution": c14n_sha256(solution),
            },
        })

    module_text = text(module_root)
    reader_text = text(reader_root)
    id_set = set(ids)
    module_id_set = set(module_ids)
    concepts = {
        "separation_and_kolmogorov_quotient": "Kuosien Kolmogorov" in module_text and "praurutan spesialisasi" in module_text,
        "countability_and_nets": "jaring lingkungan" in module_text.casefold() and "terhitung pertama" in module_text,
        "separable_not_second_countable": "separabel tetapi tidak terhitung kedua" in module_text,
        "product_vs_box": "topologi hasil kali" in module_text and "topologi kotak" in module_text,
        "tychonoff_scope": "Teorema Tychonoff" in module_text and "aksioma pilihan" in module_text,
        "local_compactness": "Kekompakan lokal hasil kali" in module_text and "kompaktifikasi satu titik" in module_text,
        "urysohn_metrization": "teorema metrisasi Urysohn" in module_text,
        "compact_open_and_nets": "Kekonvergenan kompak-terbuka" in module_text and "Untuk jaring" in module_text,
        "arzela_ascoli": "Arzelà–Ascoli" in module_text and "ekukontinu" in module_text,
        "exponential_law": "hukum eksponensial" in module_text and "evaluasi bersama" in module_text,
        "integrated_counterexamples": "Empat contoh tandingan" in module_text,
        "integrated_final_audit": "Audit terpadu kompaktifikasi diskret takterhitung" in module_text,
    }
    rights = {
        "module_cc_by_4": "CC BY 4.0" in module_text,
        "reader_cc_by_4": "CC BY 4.0" in reader_text,
        "module_source_rights_context": "CC BY-NC-SA 3.0" in module_text,
        "reader_source_rights_context": "CC BY-NC-SA 3.0" in reader_text,
        "module_nonendorsement": "tidak menyatakan atau menyiratkan dukungan" in module_text,
        "reader_nonendorsement": "tidak menyatakan ataupun menyiratkan dukungan" in reader_text,
        "module_exact_provenance": EXACT_MODEL in module_text,
        "reader_exact_provenance": EXACT_MODEL in reader_text,
        "independent_expression": "Tidak ada ekspresi buku lain yang disalin" in module_text,
    }
    covered_modules = sorted({number for values in EXERCISE_DEPENDENCIES.values() for number in values})
    multi_concept_count = sum(len(values) >= 2 for values in EXERCISE_DEPENDENCIES.values())
    English_residue = sorted(set(re.findall(r"\b(?:Theorem|Proof|Exercise|Exercises|Hint|Answer|Solution|Solutions|Chapter|Section|TODO|TBD)\b", module_text, flags=re.IGNORECASE)))
    placeholder_markers = [marker for marker in ("TODO", "TBD", "lorem ipsum", "solusi menyusul", "akan dilengkapi") if marker.casefold() in module_text.casefold()]

    failures: list[str] = []
    if duplicates:
        failures.append(f"duplicate IDs: {duplicates}")
    if unresolved:
        failures.append(f"unresolved xrefs: {unresolved}")
    if observed_ids != expected_ids:
        failures.append(f"mastery sequence differs: {observed_ids}")
    if set(EXERCISE_DEPENDENCIES) != set(expected_ids):
        failures.append("backend dependency map does not exactly cover expected exercises")
    failures.extend(stage_failures)
    failures.extend(f"missing concept: {key}" for key, present in concepts.items() if not present)
    failures.extend(f"failed rights check: {key}" for key, passed in rights.items() if not passed)
    if not DEPENDENCY_MAP_IDS.issubset(module_id_set):
        failures.append(f"missing dependency-map IDs: {sorted(DEPENDENCY_MAP_IDS - module_id_set)}")
    if not RUBRIC_IDS.issubset(module_id_set):
        failures.append(f"missing rubric IDs: {sorted(RUBRIC_IDS - module_id_set)}")
    if covered_modules != list(range(1, 8)):
        failures.append(f"completion-module coverage differs: {covered_modules}")
    if multi_concept_count < 8:
        failures.append(f"only {multi_concept_count} multi-concept mastery exercises")
    if English_residue:
        failures.append(f"active English instructional residue: {English_residue}")
    if placeholder_markers:
        failures.append(f"placeholder markers found: {placeholder_markers}")

    counts = {
        "elements": sum(tag_counts.values()),
        "xml_ids_in_standalone_reader": len(ids),
        "xrefs_in_standalone_reader": len(refs),
        "subsections": tag_counts.get("subsection", 0),
        "dependency_map_entries": len(DEPENDENCY_MAP_IDS),
        "rubric_entries": len(RUBRIC_IDS),
        "mastery_exercises": len(exercises),
        "multi_concept_mastery_exercises": multi_concept_count,
        "hints": tag_counts.get("hint", 0),
        "answers": tag_counts.get("answer", 0),
        "solutions": tag_counts.get("solution", 0),
        "staged_surfaces": len(exercises) * 4,
        "completion_modules_covered": len(covered_modules),
    }
    manifest = {
        "schema_version": 1,
        "status": "content_complete_schema_and_backend_qa_pass" if not failures else "qa_failed",
        "locale": "id-ID",
        "component_id": MODULE_ID,
        "component_title": "Pelengkap C90 Modul 8: Puncak Penguasaan Terpadu",
        "component_license": "CC BY 4.0",
        "source_spine_license_context": "CC BY-NC-SA 3.0 (conservative treatment)",
        "nonendorsement": True,
        "independent_original_expression": True,
        "model_provenance": EXACT_MODEL,
        "module": identity(MODULE),
        "standalone_reader_source": identity(READER),
        "schema_receipt": identity(SCHEMA_QA),
        "stable_content_ids": sorted(module_ids),
        "dependency_map_ids": sorted(DEPENDENCY_MAP_IDS),
        "assessment_rubric_ids": sorted(RUBRIC_IDS),
        "completion_modules_covered": covered_modules,
        "concepts": sorted(concepts),
        "mastery_exercises": mastery,
        "counts": counts,
    }
    manifest_payload = json_bytes(manifest)
    qa = {
        "schema_version": 1,
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "inputs": [identity(MODULE), identity(READER), identity(SCHEMA_QA)],
        "checks": {
            "schema_gate": True,
            "xml_ids_unique": not duplicates,
            "xrefs_resolve_in_standalone_reader": not unresolved,
            "twelve_mastery_exercises": len(exercises) == EXPECTED_EXERCISES,
            "mastery_sequence_exact": observed_ids == expected_ids,
            "all_mastery_surfaces_complete_and_substantive": not stage_failures,
            "all_seven_theory_modules_synthesized": covered_modules == list(range(1, 8)),
            "at_least_eight_multi_concept_problems": multi_concept_count >= 8,
            "dependency_mastery_map_complete": DEPENDENCY_MAP_IDS.issubset(module_id_set),
            "proof_and_counterexample_rubric_complete": RUBRIC_IDS.issubset(module_id_set),
            "concept_closure": concepts,
            "rights_independence_and_provenance": rights,
            "active_English_instructional_residue": English_residue,
            "no_placeholders": not placeholder_markers,
        },
        "counts": counts,
        "manifest_expected": {"path": MANIFEST.relative_to(ROOT).as_posix(), "bytes": len(manifest_payload), "sha256": sha256(manifest_payload)},
    }
    qa_payload = json_bytes(qa)
    receipt = f"""# O003 C90 completion Module 8 backend receipt

Status: **{'pass' if not failures else 'fail'}**

- Module: `completion/module_08_integrated_mastery.ptx`.
- Standalone reader: `source/o003_completion_module_08_reader.ptx`.
- Original component rights: CC BY 4.0.
- Source-spine rights context: CC BY-NC-SA 3.0, conservative treatment.
- Non-endorsement and independent expression: explicit.
- Model provenance: `{EXACT_MODEL}`.
- Mastery exercises: {len(exercises)}; multi-concept: {multi_concept_count}; staged surfaces: {len(exercises) * 4}.
- Dependency-map entries: {len(DEPENDENCY_MAP_IDS)}; rubric entries: {len(RUBRIC_IDS)}.
- Completion theory modules synthesized: {covered_modules}.
- XML IDs: {len(ids)} unique; xrefs: {len(refs)}; unresolved: {len(unresolved)}.
- Manifest SHA-256: `{sha256(manifest_payload)}`.
- Content QA SHA-256: `{sha256(qa_payload)}`.
- Schema receipt SHA-256: `{identity(SCHEMA_QA)['sha256']}`.

The bounded standalone capstone passes the pinned schema, stable-ID, staged
mastery, dependency-map, assessment-rubric, synthesis, rights, provenance,
Indonesian residue, and content-closure gates. It does not modify or integrate
the shared completion wrapper, cumulative readers, project configuration,
spine chapters, global controls, Git, or publication state.
""".encode("utf-8")
    return manifest_payload, qa_payload, receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    manifest_payload, qa_payload, receipt_payload = build()
    outputs = ((MANIFEST, manifest_payload), (CONTENT_QA, qa_payload), (RECEIPT, receipt_payload))
    if args.check:
        for path, payload in outputs:
            if not path.is_file() or path.read_bytes() != payload:
                raise SystemExit(f"deterministic output differs: {path.relative_to(ROOT)}")
    else:
        for path, payload in outputs:
            path.write_bytes(payload)
            if path.read_bytes() != payload:
                raise SystemExit(f"write/readback failed: {path.relative_to(ROOT)}")
    report = json.loads(qa_payload)
    print(json.dumps({
        "status": report["status"],
        "check_only": args.check,
        "failures": report["failures"],
        "outputs": {
            path.relative_to(ROOT).as_posix(): {"bytes": len(payload), "sha256": sha256(payload)}
            for path, payload in outputs
        },
    }, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
