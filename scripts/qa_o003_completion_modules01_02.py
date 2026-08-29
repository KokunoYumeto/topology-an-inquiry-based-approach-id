#!/usr/bin/env python3
"""Build deterministic cumulative backend/QA receipts for O003 completion Modules 1–2."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from lxml import etree


ROOT = Path(__file__).resolve().parent.parent
MODULES = [
    ROOT / "completion" / "module_01_separation_completion.ptx",
    ROOT / "completion" / "module_02_countability_size.ptx",
]
WRAPPER = ROOT / "completion" / "o003_c90_completion_self_study.ptx"
READER = ROOT / "source" / "o003_completion_modules_01_02_reader.ptx"
SCHEMA_QA = ROOT / "qa" / "O003_COMPLETION_MODULES01_02_SCHEMA_QA.json"
MANIFEST = ROOT / "backend" / "o003_completion_modules_01_02_manifest.json"
CONTENT_QA = ROOT / "qa" / "O003_COMPLETION_MODULES01_02_CONTENT_QA.json"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def identity(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": digest(data)}


def payload(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def parse(path: Path, expand: bool = False) -> etree._ElementTree:
    parser = etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False)
    tree = etree.parse(str(path), parser)
    if expand:
        tree.xinclude()
    return tree


def name(node: etree._Element) -> str:
    return etree.QName(node).localname


def module_record(path: Path) -> tuple[dict[str, object], list[str]]:
    root = parse(path).getroot()
    counts: dict[str, int] = {}
    ids: list[str] = []
    failures: list[str] = []
    for node in root.iter():
        if not isinstance(node.tag, str):
            continue
        tag = name(node)
        counts[tag] = counts.get(tag, 0) + 1
        if node.get(XML_ID):
            ids.append(node.get(XML_ID))
    exercises = [node for node in root.iter() if name(node) == "exercise"]
    entries: list[dict[str, object]] = []
    for exercise in exercises:
        child_names = {name(child) for child in exercise}
        missing = [tag for tag in ("statement", "hint", "answer", "solution") if tag not in child_names]
        if missing:
            failures.append(f"{exercise.get(XML_ID)} missing {', '.join(missing)}")
        entries.append(
            {
                "id": exercise.get(XML_ID),
                "title": exercise.findtext("title", default=""),
                "status": "complete" if not missing else "incomplete",
                "surfaces": ["statement", "hint", "answer", "solution"],
            }
        )
    if len(exercises) != 6:
        failures.append(f"{path.name}: expected 6 mastery exercises, found {len(exercises)}")
    if any(counts.get(tag, 0) != 6 for tag in ("hint", "answer", "solution")):
        failures.append(f"{path.name}: staged counts are not 6/6/6")
    return (
        {
            "module_id": root.get(XML_ID),
            "title": root.findtext("title", default=""),
            "status": "content_complete_schema_and_backend_qa_pass" if not failures else "qa_failed",
            "file": identity(path),
            "stable_content_ids": sorted(ids),
            "mastery_exercises": entries,
            "counts": {
                "elements": sum(counts.values()),
                "xml_ids": len(ids),
                "definitions": counts.get("definition", 0),
                "theorems": counts.get("theorem", 0),
                "propositions": counts.get("proposition", 0),
                "examples": counts.get("example", 0),
                "mastery_exercises": len(exercises),
                "hints": counts.get("hint", 0),
                "answers": counts.get("answer", 0),
                "solutions": counts.get("solution", 0),
                "staged_surfaces": len(exercises) * 4,
            },
        },
        failures,
    )


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

    module2_text = " ".join("".join(parse(MODULES[1]).getroot().itertext()).split())
    module2_concepts = {
        "local_base": "basis lokal",
        "first_countability": "terhitung pertama",
        "second_countability": "terhitung kedua",
        "dense_set": "padat",
        "separability": "separabel",
        "lindelof": "Lindelöf",
        "metric_equivalence": "ruang metrik",
        "separable_not_second_countable": "Garis Sorgenfrey",
        "separability_not_hereditary": "anti-diagonal",
        "lindelof_not_hereditary": "diskret tak terhitung",
    }
    concept_presence = {key: phrase in module2_text for key, phrase in module2_concepts.items()}
    failures.extend(f"missing Module 2 concept: {key}" for key, present in concept_presence.items() if not present)
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

    cumulative_counts = {
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
        "status": "modules_01_02_complete_schema_and_backend_qa_pass" if not failures else "qa_failed",
        "component_license": "CC BY 4.0",
        "source_spine_license_context": "CC BY-NC-SA 3.0 (conservative treatment)",
        "nonendorsement": True,
        "model_provenance": model,
        "wrapper": identity(WRAPPER),
        "reader_source": identity(READER),
        "schema_receipt": identity(SCHEMA_QA),
        "modules": records,
        "cumulative_counts": cumulative_counts,
        "remaining_modules": [
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
        "inputs": [identity(path) for path in MODULES] + [identity(WRAPPER), identity(READER), identity(SCHEMA_QA)],
        "checks": {
            "schema_gate": schema.get("status") == "pass" and not schema.get("diagnostics"),
            "ids_unique": not duplicate_ids,
            "xrefs_closed": not missing_refs,
            "all_mastery_surfaces_complete": not any("missing" in item or "staged" in item for item in failures),
            "module2_concept_closure": concept_presence,
            "rights_and_provenance": rights,
        },
        "counts": cumulative_counts,
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
