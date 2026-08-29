#!/usr/bin/env python3
"""Build deterministic backend and content-QA receipts for completion Module 7."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from typing import Any

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "completion" / "module_07_function_spaces.ptx"
READER = ROOT / "source" / "o003_completion_module_07_reader.ptx"
SCHEMA_QA = ROOT / "qa" / "O003_COMPLETION_MODULE07_SCHEMA_QA.json"
MANIFEST = ROOT / "backend" / "o003_completion_module_07_manifest.json"
CONTENT_QA = ROOT / "qa" / "O003_COMPLETION_MODULE07_CONTENT_QA.json"
RECEIPT = ROOT / "qa" / "O003_COMPLETION_MODULE07_BACKEND_RECEIPT.md"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
EXACT_MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
MODULE_ID = "o003-c90-completion-function-spaces"
EXPECTED_EXERCISES = 6


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
        raise SystemExit("Module 7 pinned-schema gate has not passed")

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
    expected_ids = [f"o003-c90-completion-function-ex-{number:02d}" for number in range(1, EXPECTED_EXERCISES + 1)]
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
        "pointwise_product_topology": "topologi hasil kali pada" in module_text and "Topologi titik demi titik" in module_text,
        "uniform_topology": "topologi seragam" in module_text and "d_\\infty" in module_text,
        "uniform_structure_scope": "struktur seragam" in module_text,
        "compact_open_topology": "Topologi kompak-terbuka" in module_text and "C_k(X,Y)" in module_text,
        "topology_comparisons": "benar-benar lebih kasar" in module_text and "tidak konvergen seragam" in module_text,
        "evaluation": "o003-c90-thm-compact-open-evaluation" in ids and "pemetaan evaluasi" in module_text,
        "composition": "o003-c90-thm-compact-open-composition" in ids and "komposisi" in module_text,
        "exponential_law": "o003-c90-thm-exponential-law-bridge" in ids and "hukum eksponensial" in module_text,
        "compact_generated_scope": "ruang kompak-terbangkitkan" in module_text,
        "arzela_ascoli": "Arzelà–Ascoli" in module_text and "ekukontinu" in module_text,
        "analysis_bridge_bounded": "bentuk bernilai real" in module_text,
    }
    required_ids = {
        "o003-c90-def-function-space-pointwise",
        "o003-c90-def-uniform-function-topology",
        "o003-c90-def-compact-open-topology",
        "o003-c90-thm-compact-open-evaluation",
        "o003-c90-thm-compact-open-composition",
        "o003-c90-thm-exponential-law-bridge",
        "o003-c90-thm-arzela-ascoli-bounded",
    }
    rights = {
        "module_cc_by_4": "CC BY 4.0" in module_text,
        "reader_cc_by_4": "CC BY 4.0" in reader_text,
        "module_source_rights_context": "CC BY-NC-SA 3.0" in module_text,
        "reader_source_rights_context": "CC BY-NC-SA 3.0" in reader_text,
        "module_nonendorsement": "tidak menyatakan atau menyiratkan" in module_text,
        "reader_nonendorsement": "tidak menyatakan ataupun menyiratkan" in reader_text,
        "module_exact_provenance": EXACT_MODEL in module_text,
        "reader_exact_provenance": EXACT_MODEL in reader_text,
    }

    failures: list[str] = []
    if duplicates:
        failures.append(f"duplicate IDs: {duplicates}")
    if unresolved:
        failures.append(f"unresolved xrefs: {unresolved}")
    if observed_ids != expected_ids:
        failures.append(f"mastery sequence differs: {observed_ids}")
    failures.extend(stage_failures)
    failures.extend(f"missing concept: {key}" for key, present in concepts.items() if not present)
    failures.extend(f"failed rights check: {key}" for key, passed in rights.items() if not passed)
    if not required_ids.issubset(set(ids)):
        failures.append(f"missing required IDs: {sorted(required_ids - set(ids))}")
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
        "component_title": "Pelengkap C90 Modul 7: Ruang Fungsi",
        "component_license": "CC BY 4.0",
        "source_spine_license_context": "CC BY-NC-SA 3.0 (conservative treatment)",
        "nonendorsement": True,
        "model_provenance": EXACT_MODEL,
        "module": identity(MODULE),
        "standalone_reader_source": identity(READER),
        "schema_receipt": identity(SCHEMA_QA),
        "stable_content_ids": sorted(ids),
        "concepts": sorted(concepts),
        "required_theory_ids": sorted(required_ids),
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
            "six_mastery_exercises": len(exercises) == EXPECTED_EXERCISES,
            "mastery_sequence_exact": observed_ids == expected_ids,
            "all_mastery_surfaces_complete_and_substantive": not stage_failures,
            "concept_closure": concepts,
            "required_theory_ids_complete": required_ids.issubset(set(ids)),
            "rights_and_provenance": rights,
            "no_placeholders": "placeholder marker found" not in failures,
        },
        "counts": counts,
        "manifest_expected": {"path": MANIFEST.relative_to(ROOT).as_posix(), "bytes": len(manifest_payload), "sha256": sha256(manifest_payload)},
    }
    qa_payload = json_bytes(qa)
    receipt = f"""# O003 C90 completion Module 7 backend receipt

Status: **{'pass' if not failures else 'fail'}**

- Module: `completion/module_07_function_spaces.ptx`.
- Standalone reader: `source/o003_completion_module_07_reader.ptx`.
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
concept, rights, provenance, and staged-content gates. It does not yet modify
the shared completion wrapper or cumulative readers.
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
