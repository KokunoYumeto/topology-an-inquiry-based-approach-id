#!/usr/bin/env python3
"""Build deterministic cumulative backend/QA receipts for O003 completion Modules 1–3."""

from __future__ import annotations

import argparse
import json

from qa_o003_completion_modules01_02 import (
    ROOT,
    XML_ID,
    identity,
    module_record,
    parse,
    payload,
)


MODULES = [
    ROOT / "completion" / "module_01_separation_completion.ptx",
    ROOT / "completion" / "module_02_countability_size.ptx",
    ROOT / "completion" / "module_03_nets_general_convergence.ptx",
]
WRAPPER = ROOT / "completion" / "o003_c90_completion_self_study.ptx"
READER = ROOT / "source" / "o003_completion_modules_01_03_reader.ptx"
SCHEMA_QA = ROOT / "qa" / "O003_COMPLETION_MODULES01_03_SCHEMA_QA.json"
MANIFEST = ROOT / "backend" / "o003_completion_modules_01_03_manifest.json"
CONTENT_QA = ROOT / "qa" / "O003_COMPLETION_MODULES01_03_CONTENT_QA.json"


def build() -> tuple[bytes, bytes]:
    schema = json.loads(SCHEMA_QA.read_text(encoding="utf-8"))
    if schema.get("status") != "pass" or schema.get("diagnostics"):
        raise RuntimeError("cumulative pinned schema gate has not passed")
    reader = parse(READER, expand=True).getroot()
    wrapper = parse(WRAPPER, expand=True).getroot()
    ids = [node.get(XML_ID) for node in reader.iter() if node.get(XML_ID)]
    id_set = set(ids)
    duplicate_ids = sorted({value for value in ids if ids.count(value) > 1})
    refs = [node.get("ref") for node in reader.iter() if node.get("ref")]
    missing_refs = sorted({ref for ref in refs if ref not in id_set})

    records: list[dict[str, object]] = []
    failures: list[str] = []
    for path in MODULES:
        record, local_failures = module_record(path)
        records.append(record)
        failures.extend(local_failures)

    text = " ".join("".join(parse(MODULES[2]).getroot().itertext()).split())
    concepts = {
        "directed_set": "Himpunan terarah",
        "net": "Jaring",
        "eventually": "akhirnya",
        "frequently": "sering",
        "subnet": "subjaring",
        "cluster_point": "titik gugus",
        "closure_characterization": "karakterisasi penutup",
        "continuity_characterization": "pelestarian jaring",
        "compactness_characterization": "setiap jaring",
        "sequences_fail": "ordinal pertama yang tak terhitung",
        "filter_bridge": "Filter pada",
    }
    concept_presence = {key: phrase in text for key, phrase in concepts.items()}
    failures.extend(f"missing Module 3 concept: {key}" for key, present in concept_presence.items() if not present)
    if duplicate_ids:
        failures.append(f"duplicate IDs: {duplicate_ids}")
    if missing_refs:
        failures.append(f"unresolved xrefs: {missing_refs}")

    model = "OpenAI Codex gpt-5.6-sol, Ultra"
    reader_text = " ".join("".join(reader.itertext()).split())
    wrapper_text = " ".join("".join(wrapper.itertext()).split())
    rights = {
        "cc_by_4": "CC BY 4.0" in reader_text and "CC BY 4.0" in wrapper_text,
        "core_cc_by_nc_sa_3": "CC BY-NC-SA 3.0" in reader_text and "CC BY-NC-SA 3.0" in wrapper_text,
        "nonendorsement": "tidak menyatakan" in reader_text and "dukungan" in reader_text,
        "exact_model_provenance": model in reader_text and model in wrapper_text,
    }
    failures.extend(f"failed rights check: {key}" for key, passed in rights.items() if not passed)

    counts = {
        "modules": len(records),
        "module_elements": sum(record["counts"]["elements"] for record in records),
        "stable_module_ids": sum(record["counts"]["xml_ids"] for record in records),
        "mastery_exercises": sum(record["counts"]["mastery_exercises"] for record in records),
        "hints": sum(record["counts"]["hints"] for record in records),
        "answers": sum(record["counts"]["answers"] for record in records),
        "solutions": sum(record["counts"]["solutions"] for record in records),
        "staged_surfaces": sum(record["counts"]["staged_surfaces"] for record in records),
        "reader_xml_ids": len(ids),
        "reader_xrefs": len(refs),
    }
    manifest = {
        "schema_version": 1,
        "locale": "id-ID",
        "component_id": "o003-c90-completion-companion",
        "status": "modules_01_03_complete_schema_and_backend_qa_pass" if not failures else "qa_failed",
        "component_license": "CC BY 4.0",
        "source_spine_license_context": "CC BY-NC-SA 3.0 (conservative treatment)",
        "nonendorsement": True,
        "model_provenance": model,
        "wrapper": identity(WRAPPER),
        "reader_source": identity(READER),
        "schema_receipt": identity(SCHEMA_QA),
        "modules": records,
        "cumulative_counts": counts,
        "remaining_modules": [
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
        "inputs": [identity(path) for path in MODULES] + [identity(WRAPPER), identity(READER), identity(SCHEMA_QA)],
        "checks": {
            "schema_gate": schema.get("status") == "pass" and not schema.get("diagnostics"),
            "ids_unique": not duplicate_ids,
            "xrefs_closed": not missing_refs,
            "all_mastery_surfaces_complete": not any("missing" in item or "staged" in item for item in failures),
            "module3_concept_closure": concept_presence,
            "rights_and_provenance": rights,
        },
        "counts": counts,
        "failures": failures,
    }
    return payload(manifest), payload(qa)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    manifest, qa = build()
    outputs = [(MANIFEST, manifest), (CONTENT_QA, qa)]
    if args.check:
        for path, data in outputs:
            if not path.is_file() or path.read_bytes() != data:
                raise SystemExit(f"deterministic output differs: {path.relative_to(ROOT)}")
    else:
        for path, data in outputs:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            if path.read_bytes() != data:
                raise RuntimeError(f"readback failed: {path}")
    report = json.loads(qa)
    print(json.dumps({"status": report["status"], "failures": report["failures"]}, ensure_ascii=False))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
