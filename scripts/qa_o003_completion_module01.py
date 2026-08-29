#!/usr/bin/env python3
"""Build deterministic backend and content-QA receipts for O003 completion Module 1."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from lxml import etree


ROOT = Path(__file__).resolve().parent.parent
COMPLETION = ROOT / "completion"
SOURCE = ROOT / "source"
BACKEND = ROOT / "backend"
QA = ROOT / "qa"
MODULE = COMPLETION / "module_01_separation_completion.ptx"
WRAPPER = COMPLETION / "o003_c90_completion_self_study.ptx"
READER = SOURCE / "o003_completion_module_01_reader.ptx"
SCHEMA_QA = QA / "O003_COMPLETION_MODULE01_SCHEMA_QA.json"
MANIFEST = BACKEND / "o003_completion_module_01_manifest.json"
CONTENT_QA = QA / "O003_COMPLETION_MODULE01_CONTENT_QA.json"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def identity(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(data),
        "sha256": sha256(data),
    }


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def local_name(node: etree._Element) -> str:
    return etree.QName(node).localname


def parse(path: Path) -> etree._ElementTree:
    parser = etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False)
    return etree.parse(str(path), parser)


def expanded(path: Path) -> etree._ElementTree:
    tree = parse(path)
    tree.xinclude()
    return tree


def build() -> tuple[bytes, bytes]:
    module_tree = parse(MODULE)
    wrapper_tree = expanded(WRAPPER)
    reader_tree = expanded(READER)
    module_root = module_tree.getroot()
    reader_root = reader_tree.getroot()

    schema_receipt = json.loads(SCHEMA_QA.read_text(encoding="utf-8"))
    if schema_receipt.get("status") != "pass" or schema_receipt.get("diagnostics"):
        raise RuntimeError("pinned PreTeXt schema gate has not passed")

    ids = [node.get(XML_ID) for node in reader_root.iter() if node.get(XML_ID)]
    duplicate_ids = sorted({value for value in ids if ids.count(value) > 1})
    refs = [node.get("ref") for node in reader_root.iter() if node.get("ref")]
    missing_refs = sorted({ref for ref in refs if ref not in set(ids)})

    tag_counts: dict[str, int] = {}
    for node in module_root.iter():
        if not isinstance(node.tag, str):
            continue
        name = local_name(node)
        tag_counts[name] = tag_counts.get(name, 0) + 1

    exercises = [node for node in module_root.iter() if local_name(node) == "exercise"]
    staged: list[dict[str, object]] = []
    stage_failures: list[str] = []
    for exercise in exercises:
        exercise_id = exercise.get(XML_ID)
        children = [local_name(child) for child in exercise]
        required = ["statement", "hint", "answer", "solution"]
        missing = [name for name in required if name not in children]
        if missing:
            stage_failures.append(f"{exercise_id}: missing {', '.join(missing)}")
        staged.append(
            {
                "id": exercise_id,
                "title": "".join(exercise.findtext("title", default="")),
                "surfaces": required,
                "status": "complete" if not missing else "incomplete",
            }
        )

    text = " ".join("".join(module_root.itertext()).split())
    required_concepts = {
        "t0_kolmogorov": "ruang Kolmogorov",
        "topological_indistinguishability": "tak terbedakan secara topologis",
        "specialization_preorder": "praurutan spesialisasi",
        "kolmogorov_quotient": "kuosien Kolmogorov",
        "complete_regularity": "reguler lengkap",
        "tychonoff": "ruang Tychonoff",
        "urysohn_lemma": "Lema Urysohn",
        "non_t0_witness": "topologi indiskret",
        "t0_not_t1_witness": "ruang Sierpiński",
        "t1_not_t2_witness": "topologi komplemen berhingga",
        "t2_not_t3_witness": "R_K",
        "t3_not_t4_witness": "Bidang Niemytzki",
    }
    concept_presence = {key: phrase in text for key, phrase in required_concepts.items()}

    exact_provenance = "OpenAI Codex gpt-5.6-sol, Ultra"
    wrapper_text = " ".join("".join(wrapper_tree.getroot().itertext()).split())
    reader_text = " ".join("".join(reader_root.itertext()).split())
    rights_checks = {
        "wrapper_cc_by_4": "CC BY 4.0" in wrapper_text,
        "wrapper_core_cc_by_nc_sa_3": "CC BY-NC-SA 3.0" in wrapper_text,
        "wrapper_nonendorsement": "tidak menyatakan ataupun menyiratkan dukungan" in wrapper_text,
        "wrapper_exact_provenance": exact_provenance in wrapper_text,
        "reader_exact_provenance": exact_provenance in reader_text,
    }

    failures: list[str] = []
    if duplicate_ids:
        failures.append(f"duplicate IDs: {duplicate_ids}")
    if missing_refs:
        failures.append(f"unresolved xrefs: {missing_refs}")
    failures.extend(stage_failures)
    failures.extend(f"missing concept: {key}" for key, present in concept_presence.items() if not present)
    failures.extend(f"failed rights check: {key}" for key, passed in rights_checks.items() if not passed)
    if len(exercises) != 6:
        failures.append(f"expected 6 mastery exercises, found {len(exercises)}")
    if tag_counts.get("hint") != 6 or tag_counts.get("answer") != 6 or tag_counts.get("solution") != 6:
        failures.append("staged surface counts are not 6/6/6")

    manifest = {
        "schema_version": 1,
        "locale": "id-ID",
        "component_id": "o003-c90-completion-companion",
        "component_title": "Pelengkap C90: Topologi Himpunan-Titik untuk Belajar Mandiri",
        "component_license": "CC BY 4.0",
        "source_spine_license_context": "CC BY-NC-SA 3.0 (conservative treatment)",
        "nonendorsement": True,
        "model_provenance": exact_provenance,
        "current_module": {
            "module_id": "o003-c90-completion-separation",
            "title": "Penyempurnaan Aksioma Separasi",
            "status": "content_complete_schema_and_backend_qa_pass" if not failures else "qa_failed",
            "file": identity(MODULE),
            "wrapper": identity(WRAPPER),
            "standalone_reader_source": identity(READER),
            "prerequisite_source_ids": [
                "chap_Closed_sets_topology",
                "sec_separation_ax",
                "ex_T_1_2_3",
                "ex_not_T_1_2_3",
            ],
            "concepts": sorted(required_concepts),
            "stable_content_ids": sorted(node_id for node_id in ids if node_id.startswith("o003-c90-completion")),
            "mastery_exercises": staged,
            "counts": {
                "elements": sum(tag_counts.values()),
                "xml_ids_in_standalone_reader": len(ids),
                "xrefs_in_standalone_reader": len(refs),
                "definitions": tag_counts.get("definition", 0),
                "theorems": tag_counts.get("theorem", 0),
                "propositions": tag_counts.get("proposition", 0),
                "examples": tag_counts.get("example", 0),
                "mastery_exercises": len(exercises),
                "hints": tag_counts.get("hint", 0),
                "answers": tag_counts.get("answer", 0),
                "solutions": tag_counts.get("solution", 0),
                "staged_surfaces": len(exercises) * 4,
            },
            "schema_receipt": identity(SCHEMA_QA),
        },
        "remaining_modules": [
            {"module_id": "o003-c90-completion-countability", "status": "not_started"},
            {"module_id": "o003-c90-completion-general-convergence", "status": "not_started"},
            {"module_id": "o003-c90-completion-arbitrary-products", "status": "not_started"},
            {"module_id": "o003-c90-completion-local-compactness", "status": "not_started"},
            {"module_id": "o003-c90-completion-metrization", "status": "not_started"},
            {"module_id": "o003-c90-completion-function-spaces", "status": "not_started"},
            {"module_id": "o003-c90-completion-integrated-mastery", "status": "not_started"},
        ],
    }

    qa = {
        "schema_version": 1,
        "status": "pass" if not failures else "fail",
        "inputs": [identity(MODULE), identity(WRAPPER), identity(READER), identity(SCHEMA_QA)],
        "checks": {
            "xml_ids_unique": not duplicate_ids,
            "xrefs_resolve_in_standalone_reader": not missing_refs,
            "six_mastery_exercises": len(exercises) == 6,
            "all_mastery_surfaces_complete": not stage_failures,
            "concept_closure": concept_presence,
            "rights_and_provenance": rights_checks,
            "schema_gate": schema_receipt.get("status") == "pass" and not schema_receipt.get("diagnostics"),
        },
        "counts": manifest["current_module"]["counts"],
        "failures": failures,
    }
    return json_bytes(manifest), json_bytes(qa)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    manifest_payload, qa_payload = build()
    outputs = [(MANIFEST, manifest_payload), (CONTENT_QA, qa_payload)]
    if args.check:
        for path, payload in outputs:
            if not path.is_file() or path.read_bytes() != payload:
                raise SystemExit(f"deterministic output differs: {path.relative_to(ROOT)}")
    else:
        for path, payload in outputs:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
            if path.read_bytes() != payload:
                raise RuntimeError(f"write readback failed: {path}")
    report = json.loads(qa_payload)
    print(json.dumps({"status": report["status"], "failures": report["failures"]}, ensure_ascii=False))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
