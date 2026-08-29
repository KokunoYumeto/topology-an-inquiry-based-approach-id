#!/usr/bin/env python3
"""Build deterministic backend and content-QA receipts for completion Module 6."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from typing import Any

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "completion" / "module_06_metrization.ptx"
READER = ROOT / "source" / "o003_completion_module_06_reader.ptx"
SCHEMA_QA = ROOT / "qa" / "O003_COMPLETION_MODULE06_SCHEMA_QA.json"
MANIFEST = ROOT / "backend" / "o003_completion_module_06_manifest.json"
CONTENT_QA = ROOT / "qa" / "O003_COMPLETION_MODULE06_CONTENT_QA.json"
RECEIPT = ROOT / "qa" / "O003_COMPLETION_MODULE06_BACKEND_RECEIPT.md"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
EXACT_MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
MODULE_ID = "o003-c90-completion-metrization"
EXPECTED_EXERCISES = 8


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
    schema_receipt = json.loads(SCHEMA_QA.read_text(encoding="utf-8"))
    if schema_receipt.get("status") != "pass" or schema_receipt.get("diagnostics") or schema_receipt.get("failures"):
        raise SystemExit("Module 6 pinned-schema gate has not passed")

    module_tree = parse(MODULE)
    reader_tree = parse(READER)
    reader_tree.xinclude()
    module_root = module_tree.getroot()
    reader_root = reader_tree.getroot()
    nodes = [node for node in reader_root.iter() if isinstance(node.tag, str)]
    ids = [node.get(XML_ID) for node in nodes if node.get(XML_ID)]
    refs = [node.get("ref") for node in nodes if node.get("ref")]
    duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
    unresolved = sorted(set(refs) - set(ids))

    tag_counts = Counter(local_name(node) for node in module_root.iter() if isinstance(node.tag, str))
    exercises = [node for node in module_root.iter() if isinstance(node.tag, str) and local_name(node) == "exercise"]
    expected_exercise_ids = [f"o003-c90-completion-metrization-ex-{number:02d}" for number in range(1, EXPECTED_EXERCISES + 1)]
    observed_exercise_ids = [node.get(XML_ID) for node in exercises]
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
        lengths = {name: len(text(node)) for name, node in (("statement", statement), ("hint", hint), ("answer", answer), ("solution", solution))}
        if lengths["statement"] < 40 or lengths["hint"] < 20 or lengths["answer"] < 20 or lengths["solution"] < 150:
            stage_failures.append(f"{entry_id}: underspecified staged content {lengths}")
        mastery.append({
            "id": entry_id,
            "title": text(title),
            "status": "complete",
            "stage_ids": {"statement": entry_id, **expected_stage_ids},
            "surface_c14n_sha256": {"statement": c14n_sha256(statement), "hint": c14n_sha256(hint), "answer": c14n_sha256(answer), "solution": c14n_sha256(solution)},
        })

    module_text = text(module_root)
    reader_text = text(reader_root)
    concepts = {
        "pseudometric_vs_metric": "pseudometrik mengizinkan dua titik berbeda berjarak nol" in module_text,
        "induced_topology": "Topologi yang diinduksi" in module_text,
        "zero_distance_quotient": "kuosien nol" in module_text,
        "metric_topological_properties": all(phrase in module_text for phrase in ("Hausdorff", "reguler", "terhitung pertama")),
        "bounded_equivalent_metrics": "d_2(x,y)=d(x,y)/(1+d(x,y))" in module_text,
        "topological_not_uniform_equivalence": "tidak ekuivalen secara seragam" in module_text,
        "countable_pseudometric_sum": "2^{-n}\\min\\{1,p_n(x,y)\\}" in module_text,
        "regular_second_countable_normal": "Setiap ruang reguler dan terhitung kedua adalah normal" in module_text,
        "urysohn_lemma": "Lema Urysohn" in module_text,
        "urysohn_actual_hypotheses": "Setiap ruang T_1 yang reguler dan terhitung kedua dapat dimetrisasi" in module_text,
        "urysohn_weighted_metric": "2^{-n}|f_n(x)-f_n(y)|" in module_text,
        "counterexample_without_t1": "Tanpa T1: ruang indisret" in module_text,
        "counterexample_without_regularity": "Tanpa regularitas: topologi K" in module_text,
        "counterexample_without_second_countability": "Tanpa keterhitungan kedua: kubus tak terhitung" in module_text,
        "sufficiency_not_necessity_nuance": "hipotesis cukup yang kuat, bukan syarat perlu" in module_text,
    }
    proof_route_ids = {
        "o003-c90-lem-second-countable-regular-normal",
        "o003-c90-lem-urysohn-functions",
        "o003-c90-thm-countable-pseudometric-sum",
        "o003-c90-thm-urysohn-metrization",
    }
    present_proof_route_ids = set(ids) & proof_route_ids
    counterexample_ids = {
        "o003-c90-example-without-t1",
        "o003-c90-example-without-regularity-k-topology",
        "o003-c90-example-without-second-countability",
    }

    rights = {
        "module_cc_by_4": "CC BY 4.0" in module_text,
        "reader_cc_by_4": "CC BY 4.0" in reader_text,
        "module_source_rights_context": "CC BY-NC-SA 3.0" in module_text,
        "reader_source_rights_context": "CC BY-NC-SA 3.0" in reader_text,
        "module_nonendorsement": "tidak menyatakan atau menyiratkan dukungan" in module_text,
        "reader_nonendorsement": "tidak menyatakan atau menyiratkan dukungan" in reader_text,
        "module_exact_provenance": EXACT_MODEL in module_text,
        "reader_exact_provenance": EXACT_MODEL in reader_text,
    }

    failures: list[str] = []
    if duplicates:
        failures.append(f"duplicate IDs: {duplicates}")
    if unresolved:
        failures.append(f"unresolved xrefs: {unresolved}")
    if observed_exercise_ids != expected_exercise_ids:
        failures.append(f"mastery sequence differs: {observed_exercise_ids}")
    failures.extend(stage_failures)
    failures.extend(f"missing concept: {key}" for key, present in concepts.items() if not present)
    failures.extend(f"failed rights check: {key}" for key, passed in rights.items() if not passed)
    if present_proof_route_ids != proof_route_ids:
        failures.append(f"incomplete Urysohn proof route IDs: {sorted(proof_route_ids - present_proof_route_ids)}")
    if not counterexample_ids.issubset(set(ids)):
        failures.append(f"missing counterexample IDs: {sorted(counterexample_ids - set(ids))}")
    if any(marker.casefold() in module_text.casefold() for marker in ("TODO", "TBD", "lorem ipsum", "solusi menyusul")):
        failures.append("placeholder marker found")

    counts = {
        "elements": sum(tag_counts.values()),
        "xml_ids_in_standalone_reader": len(ids),
        "xrefs_in_standalone_reader": len(refs),
        "subsections": tag_counts.get("subsection", 0),
        "definitions": tag_counts.get("definition", 0),
        "theorems": tag_counts.get("theorem", 0),
        "propositions": tag_counts.get("proposition", 0),
        "lemmas": tag_counts.get("lemma", 0),
        "examples": tag_counts.get("example", 0),
        "remarks": tag_counts.get("remark", 0),
        "mastery_exercises": len(exercises),
        "hints": tag_counts.get("hint", 0),
        "answers": tag_counts.get("answer", 0),
        "solutions": tag_counts.get("solution", 0),
        "staged_surfaces": len(exercises) * 4,
    }
    manifest = {
        "schema_version": 1,
        "status": "content_complete_schema_and_backend_qa_pass" if not failures else "qa_failed",
        "locale": "id-ID",
        "component_id": MODULE_ID,
        "component_title": "Pelengkap C90 Modul 6: Metrisasi",
        "component_license": "CC BY 4.0",
        "source_spine_license_context": "CC BY-NC-SA 3.0 (conservative treatment)",
        "nonendorsement": True,
        "model_provenance": EXACT_MODEL,
        "module": identity(MODULE),
        "standalone_reader_source": identity(READER),
        "schema_receipt": identity(SCHEMA_QA),
        "stable_content_ids": sorted(ids),
        "concepts": sorted(concepts),
        "proof_route_ids": sorted(proof_route_ids),
        "counterexample_ids": sorted(counterexample_ids),
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
            "eight_mastery_exercises": len(exercises) == EXPECTED_EXERCISES,
            "mastery_sequence_exact": observed_exercise_ids == expected_exercise_ids,
            "all_mastery_surfaces_complete_and_substantive": not stage_failures,
            "concept_closure": concepts,
            "urysohn_proof_route_complete": present_proof_route_ids == proof_route_ids,
            "hypothesis_counterexamples_complete": counterexample_ids.issubset(set(ids)),
            "rights_and_provenance": rights,
            "no_placeholders": "placeholder marker found" not in failures,
        },
        "counts": counts,
        "manifest_expected": {"path": MANIFEST.relative_to(ROOT).as_posix(), "bytes": len(manifest_payload), "sha256": sha256(manifest_payload)},
    }
    qa_payload = json_bytes(qa)
    receipt = f"""# O003 C90 completion Module 6 backend receipt

Status: **{'pass' if not failures else 'fail'}**

- Module: `completion/module_06_metrization.ptx`.
- Standalone reader: `source/o003_completion_module_06_reader.ptx`.
- Original component rights: CC BY 4.0.
- Source-spine rights context: CC BY-NC-SA 3.0, conservative treatment.
- Non-endorsement: explicit.
- Model provenance: `{EXACT_MODEL}`.
- Mastery exercises: {len(exercises)}; staged surfaces: {len(exercises) * 4}.
- XML IDs: {len(ids)} unique; xrefs: {len(refs)}; unresolved: {len(unresolved)}.
- Manifest SHA-256: `{sha256(manifest_payload)}`.
- Content QA SHA-256: `{sha256(qa_payload)}`.
- Schema receipt SHA-256: `{identity(SCHEMA_QA)['sha256']}`.

The bounded standalone module passes the pinned schema, stable-ID, xref,
concept, rights, provenance, and staged-content gates. It does not modify or
integrate the shared completion wrapper or cumulative readers.
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
    print(json.dumps({"status": report["status"], "check_only": args.check, "failures": report["failures"], "outputs": {path.relative_to(ROOT).as_posix(): {"bytes": len(payload), "sha256": sha256(payload)} for path, payload in outputs}}, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
