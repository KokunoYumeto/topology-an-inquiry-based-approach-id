#!/usr/bin/env python3
"""Build the deterministic current backend/QA state for the O003 completion companion."""

from __future__ import annotations

import argparse
import json

from qa_o003_completion_modules01_02 import ROOT, XML_ID, identity, module_record, parse, payload


MODULE_SPECS = [
    {
        "path": ROOT / "completion" / "module_01_separation_completion.ptx",
        "expected_exercises": 6,
        "concepts": {
            "t0": "ruang Kolmogorov",
            "specialization": "praurutan spesialisasi",
            "kolmogorov_quotient": "kuosien Kolmogorov",
            "complete_regularity": "reguler lengkap",
            "strictness": "Bidang Niemytzki",
        },
    },
    {
        "path": ROOT / "completion" / "module_02_countability_size.ptx",
        "expected_exercises": 6,
        "concepts": {
            "local_base": "basis lokal",
            "first_countability": "terhitung pertama",
            "second_countability": "terhitung kedua",
            "separability": "separabel",
            "lindelof": "Lindelöf",
            "separable_not_second": "Garis Sorgenfrey",
        },
    },
    {
        "path": ROOT / "completion" / "module_03_nets_general_convergence.ptx",
        "expected_exercises": 6,
        "concepts": {
            "directed_set": "Himpunan terarah",
            "net": "Jaring",
            "subnet": "subjaring",
            "cluster_point": "titik gugus",
            "sequences_fail": "ordinal pertama yang tak terhitung",
            "compactness": "setiap jaring",
            "filter_bridge": "Filter pada",
        },
    },
    {
        "path": ROOT / "completion" / "module_04_arbitrary_products.ptx",
        "expected_exercises": 6,
        "concepts": {
            "arbitrary_product": "Hasil Kali Sebarang",
            "product_topology": "topologi hasil kali",
            "box_topology": "topologi kotak",
            "universal_property": "sifat universal",
            "box_product_divergence": "terbuka dalam topologi kotak tetapi",
            "coordinatewise_convergence": "Kekonvergenan koordinat",
            "tychonoff": "Teorema Tychonoff",
            "choice_scope": "Aksioma Pilihan",
        },
    },
    {
        "path": ROOT / "completion" / "module_05_local_compactness.ptx",
        "expected_exercises": 6,
        "concepts": {
            "compact_neighborhood": "lingkungan kompak",
            "local_compactness": "kompak lokal",
            "shrinking": "penyusutan",
            "inheritance": "Subruang tertutup",
            "product_criterion": "semua kecuali berhingga banyak faktor",
            "one_point_compactification": "kompaktifikasi satu titik",
            "alexandroff": "kompaktifikasi Alexandroff",
            "proper_map": "Pemetaan proper",
        },
    },
    {
        "path": ROOT / "completion" / "module_06_metrization.ptx",
        "expected_exercises": 8,
        "concepts": {
            "pseudometric": "pseudometrik",
            "induced_topology": "Topologi yang diinduksi",
            "equivalent_metrics": "metrik ekuivalen",
            "urysohn_metrization": "Teorema Metrisasi Urysohn",
            "actual_hypotheses": "reguler dan terhitung kedua",
            "counterexamples": "Tanpa keterhitungan kedua",
        },
    },
    {
        "path": ROOT / "completion" / "module_07_function_spaces.ptx",
        "expected_exercises": 6,
        "concepts": {
            "pointwise": "topologi titik demi titik",
            "uniform": "topologi seragam",
            "compact_open": "topologi kompak-terbuka",
            "evaluation": "pemetaan evaluasi",
            "composition": "komposisi",
            "exponential_law": "hukum eksponensial",
            "arzela_ascoli": "Arzelà–Ascoli",
        },
    },
    {
        "path": ROOT / "completion" / "module_08_integrated_mastery.ptx",
        "expected_exercises": 12,
        "concepts": {
            "dependency_map": "Peta dependensi dan penguasaan",
            "assessment_rubric": "Rubrik pembuktian dan contoh tandingan",
            "separation": "separasi",
            "countability": "keterhitungan",
            "nets": "jaring",
            "products": "hasil kali",
            "local_compactness": "kompak lokal",
            "metrization": "metrisasi",
            "function_spaces": "ruang fungsi",
        },
    },
]
WRAPPER = ROOT / "completion" / "o003_c90_completion_self_study.ptx"
READER = ROOT / "source" / "o003_completion_modules_01_08_reader.ptx"
SCHEMA_QA = ROOT / "qa" / "O003_COMPLETION_MODULES01_08_SCHEMA_QA.json"
MANIFEST = ROOT / "backend" / "o003_completion_current_manifest.json"
CONTENT_QA = ROOT / "qa" / "O003_COMPLETION_CURRENT_QA.json"


def build() -> tuple[bytes, bytes]:
    schema = json.loads(SCHEMA_QA.read_text(encoding="utf-8"))
    if schema.get("status") != "pass" or schema.get("diagnostics"):
        raise RuntimeError("current cumulative pinned schema gate has not passed")
    reader = parse(READER, expand=True).getroot()
    wrapper = parse(WRAPPER, expand=True).getroot()
    ids = [node.get(XML_ID) for node in reader.iter() if node.get(XML_ID)]
    id_set = set(ids)
    duplicates = sorted({value for value in ids if ids.count(value) > 1})
    refs = [node.get("ref") for node in reader.iter() if node.get("ref")]
    missing_refs = sorted({ref for ref in refs if ref not in id_set})

    records: list[dict[str, object]] = []
    failures: list[str] = []
    concept_checks: dict[str, dict[str, bool]] = {}
    for number, spec in enumerate(MODULE_SPECS, start=1):
        path = spec["path"]
        record, local_failures = module_record(path)
        expected = spec["expected_exercises"]
        if expected != 6:
            local_failures = [
                failure for failure in local_failures
                if "expected 6 mastery exercises" not in failure and "staged counts are not 6/6/6" not in failure
            ]
            counts = record["counts"]
            if counts["mastery_exercises"] != expected:
                local_failures.append(f"{path.name}: expected {expected} mastery exercises, found {counts['mastery_exercises']}")
            if any(counts[tag] != expected for tag in ("hints", "answers", "solutions")):
                local_failures.append(f"{path.name}: staged counts are not {expected}/{expected}/{expected}")
            record["status"] = "content_complete_schema_and_backend_qa_pass" if not local_failures else "qa_failed"
        records.append(record)
        failures.extend(local_failures)
        text = " ".join("".join(parse(path).getroot().itertext()).split())
        current = {key: phrase in text for key, phrase in spec["concepts"].items()}
        concept_checks[f"module_{number:02d}"] = current
        failures.extend(
            f"Module {number} missing concept: {key}" for key, present in current.items() if not present
        )
    if duplicates:
        failures.append(f"duplicate IDs: {duplicates}")
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
        "status": "modules_01_08_complete_schema_and_backend_qa_pass" if not failures else "qa_failed",
        "component_license": "CC BY 4.0",
        "source_spine_license_context": "CC BY-NC-SA 3.0 (conservative treatment)",
        "nonendorsement": True,
        "model_provenance": model,
        "wrapper": identity(WRAPPER),
        "reader_source": identity(READER),
        "schema_receipt": identity(SCHEMA_QA),
        "modules": records,
        "cumulative_counts": counts,
        "remaining_modules": [],
    }
    qa = {
        "schema_version": 1,
        "status": "pass" if not failures else "fail",
        "inputs": [identity(spec["path"]) for spec in MODULE_SPECS]
        + [identity(WRAPPER), identity(READER), identity(SCHEMA_QA)],
        "checks": {
            "schema_gate": schema.get("status") == "pass" and not schema.get("diagnostics"),
            "ids_unique": not duplicates,
            "xrefs_closed": not missing_refs,
            "all_mastery_surfaces_complete": not any("missing" in item or "staged" in item for item in failures),
            "concept_closure": concept_checks,
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
