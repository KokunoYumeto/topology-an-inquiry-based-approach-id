#!/usr/bin/env python3
"""Validate and freeze the complete Chapter 20 self-study companion."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = Path.home() / ".ptx" / "schema" / "pretext.rng"
SCHEMA_BYTES = 101829
SCHEMA_SHA256 = "fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"

READER = ROOT / "source" / "chapter_20_companion_reader.ptx"
PROMPT_INVENTORY = ROOT / "backend" / "chapter_20_prompt_inventory.json"
PROMPT_MAP = ROOT / "backend" / "chapter_20_source_prompt_map.csv"
FILES = (
    ROOT / "companion" / "chapter_20_product_topology_self_study.ptx",
    ROOT / "companion" / "chapter_20_source_guides_a.ptx",
    ROOT / "companion" / "chapter_20_source_guides_b.ptx",
    ROOT / "companion" / "chapter_20_exercise_guides_a.ptx",
    ROOT / "companion" / "chapter_20_exercise_guides_b.ptx",
    ROOT / "companion" / "chapter_20_exercise_guides_c.ptx",
    ROOT / "companion" / "chapter_20_mastery.ptx",
)

SCHEMA_QA = ROOT / "qa" / "CHAPTER20_COMPANION_SCHEMA_QA.json"
CONTENT_QA = ROOT / "qa" / "CHAPTER20_COMPANION_QA.json"
MANIFEST = ROOT / "backend" / "chapter_20_companion_manifest.json"


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def identity(path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(payload), "sha256": sha256(payload)}


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def parse(path: Path) -> etree._ElementTree:
    return etree.parse(
        str(path),
        etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False, huge_tree=True),
    )


def qname(node: etree._Element) -> str:
    return etree.QName(node).localname


def normalized_text(node: etree._Element) -> str:
    return " ".join("".join(node.itertext()).split())


def companion_support_ids() -> list[str]:
    return (
        [f"o003-c90-ch20-guide-{i:02d}" for i in range(1, 32)]
        + [f"o003-c90-ch20-exer-a-{i:02d}" for i in range(1, 11)]
        + [f"o003-c90-ch20-exer-b-{i:02d}" for i in range(1, 11)]
        + [f"o003-c90-ch20-exer-c-{i:02d}" for i in range(1, 6)]
    )


def inventory_support_ids() -> list[str]:
    """Authority order: applications follow the exercise section upstream."""
    return (
        [f"o003-c90-ch20-guide-{i:02d}" for i in range(1, 19)]
        + [f"o003-c90-ch20-exer-a-{i:02d}" for i in range(1, 11)]
        + [f"o003-c90-ch20-exer-b-{i:02d}" for i in range(1, 11)]
        + [f"o003-c90-ch20-exer-c-{i:02d}" for i in range(1, 6)]
        + [f"o003-c90-ch20-guide-{i:02d}" for i in range(19, 32)]
    )


def build() -> dict[Path, bytes]:
    schema_payload = SCHEMA.read_bytes()
    if len(schema_payload) != SCHEMA_BYTES or sha256(schema_payload) != SCHEMA_SHA256:
        raise SystemExit("pinned PreTeXt schema identity changed")
    missing = [path.relative_to(ROOT).as_posix() for path in (READER, PROMPT_INVENTORY, PROMPT_MAP, *FILES) if not path.exists()]
    if missing:
        raise SystemExit("missing Chapter 20 companion inputs: " + ", ".join(missing))

    tree = parse(READER)
    hrefs = tuple(tree.xpath("//xi:include/@href", namespaces={"xi": "http://www.w3.org/2001/XInclude"}))
    tree.xinclude()
    validator = etree.RelaxNG(parse(SCHEMA))
    schema_valid = validator.validate(tree)
    diagnostics = [str(entry) for entry in validator.error_log]
    if not schema_valid or diagnostics:
        raise SystemExit(f"Chapter 20 companion schema failed: {diagnostics}")

    root = tree.getroot()
    nodes = [node for node in root.iter() if isinstance(node.tag, str)]
    ids = [node.get(XML_ID) for node in nodes if node.get(XML_ID)]
    duplicate_ids = sorted(key for key, count in Counter(ids).items() if count > 1)
    refs = [node.get("ref") for node in root.xpath(".//xref") if node.get("ref")]
    unresolved = sorted(set(refs) - set(ids))
    if duplicate_ids or unresolved:
        raise SystemExit(f"companion ID/xref failure: duplicates={duplicate_ids}, unresolved={unresolved}")

    inventory = json.loads(PROMPT_INVENTORY.read_text(encoding="utf-8"))
    inventory_ids = [entry["id"] for entry in inventory["entries"]]
    authority_order_ids = inventory_support_ids()
    expected_ids = companion_support_ids()
    if inventory_ids != authority_order_ids:
        raise SystemExit("prompt-inventory entry order does not match the canonical Chapter 20 contract")
    with PROMPT_MAP.open("r", encoding="utf-8-sig", newline="") as handle:
        prompt_rows = list(csv.DictReader(handle))
    if [row["entry_id"] for row in prompt_rows] != authority_order_ids:
        raise SystemExit("source prompt map does not match the canonical Chapter 20 contract")

    exercises = {node.get(XML_ID): node for node in root.xpath(".//exercise") if node.get(XML_ID)}
    mastery_ids = [f"o003-c90-ch20-mastery-{i:02d}" for i in range(1, 9)]
    all_expected = expected_ids + mastery_ids
    unexpected = sorted(set(exercises) - set(all_expected))
    missing_entries = sorted(set(all_expected) - set(exercises))
    if unexpected or missing_entries or len(exercises) != 64:
        raise SystemExit(f"companion entry census failed: missing={missing_entries}, unexpected={unexpected}")

    entry_receipts: list[dict[str, object]] = []
    short_solutions: list[str] = []
    stage_failures: list[str] = []
    for sequence, entry_id in enumerate(all_expected, 1):
        exercise = exercises[entry_id]
        statement = exercise.find("statement")
        hint = exercise.find("hint")
        answer = exercise.find("answer")
        solution = exercise.find("solution")
        if any(node is None for node in (statement, hint, answer, solution)):
            stage_failures.append(entry_id)
            continue
        stage_ids = {
            "hint": hint.get(XML_ID),
            "answer": answer.get(XML_ID),
            "solution": solution.get(XML_ID),
        }
        expected_stage_ids = {kind: f"{entry_id}-{kind}" for kind in ("hint", "answer", "solution")}
        if stage_ids != expected_stage_ids:
            stage_failures.append(entry_id)
        solution_text = normalized_text(solution)
        if len(solution_text) < 145:
            short_solutions.append(entry_id)
        entry_receipts.append(
            {
                "sequence": sequence,
                "id": entry_id,
                "kind": "source_support" if entry_id in expected_ids else "mastery",
                "statement_chars": len(normalized_text(statement)),
                "hint_chars": len(normalized_text(hint)),
                "answer_chars": len(normalized_text(answer)),
                "solution_chars": len(solution_text),
                "stage_ids": stage_ids,
                "subtree_sha256": sha256(etree.tostring(exercise, method="c14n", with_comments=True)),
            }
        )
    if stage_failures or short_solutions:
        raise SystemExit(f"staged support incomplete: stage_failures={stage_failures}, short_solutions={short_solutions}")

    whole_text = normalized_text(root)
    required_phrases = (
        "CC BY 4.0",
        "CC BY-NC-SA 3.0",
        "OpenAI Codex gpt-5.6-sol, Ultra",
        "bukan solusi resmi GVSU",
        "tidak menyiratkan dukungan",
        "topologi hasil kali",
        "subbasis",
        "proyeksi",
        "Hausdorff",
        "kompak",
        "terhubung lintasan",
        "Khalimsky",
        "kurva Jordan digital",
    )
    missing_phrases = [phrase for phrase in required_phrases if phrase not in whole_text]
    if missing_phrases:
        raise SystemExit("missing companion content concepts: " + ", ".join(missing_phrases))

    forbidden_placeholder_pattern = re.compile(r"\b(TODO|TBD|PLACEHOLDER|FIXME|lorem ipsum)\b", re.IGNORECASE)
    placeholders = sorted(set(forbidden_placeholder_pattern.findall(whole_text)))
    if placeholders:
        raise SystemExit(f"placeholder residue in companion: {placeholders}")

    file_identities = [identity(path) for path in FILES]
    joined = b"".join(path.read_bytes() for path in FILES)
    combined_sha = sha256(joined)
    prompt_map_identity = identity(PROMPT_MAP)
    inventory_identity = identity(PROMPT_INVENTORY)

    schema_report = {
        "schema_version": 1,
        "status": "pass",
        "partial": False,
        "source": identity(READER),
        "schema": {"path": "pretext-user-cache/schema/pretext.rng", "bytes": SCHEMA_BYTES, "sha256": SCHEMA_SHA256},
        "xinclude": {
            "all_local": True,
            "reader_direct_hrefs": list(hrefs),
            "closure_file_count": 8,
            "closure": [READER.relative_to(ROOT).as_posix(), *[path.relative_to(ROOT).as_posix() for path in FILES]],
        },
        "diagnostics": diagnostics,
        "checks": {
            "xml_well_formed": True,
            "schema_valid": True,
            "xml_ids_unique": True,
            "all_xrefs_resolve": True,
        },
        "counts": {
            "expanded_elements": len(nodes),
            "xml_ids": len(ids),
            "unique_xml_ids": len(set(ids)),
            "xrefs": len(refs),
            "exercises": len(exercises),
            "hints": len(root.xpath(".//hint")),
            "answers": len(root.xpath(".//answer")),
            "solutions": len(root.xpath(".//solution")),
        },
    }

    content_report = {
        "schema_version": 1,
        "status": "pass",
        "partial": False,
        "lane_id": "O003/C90",
        "locale": "id-ID",
        "unit": "chapter_20_product_topology",
        "coverage": {
            "canonical_source_prompt_total": 56,
            "canonical_source_prompt_covered": 56,
            "nonexercise_covered": 31,
            "exercise_covered": 25,
            "mastery_checks": 8,
            "source_support_staged_surfaces": 224,
            "mastery_staged_surfaces": 32,
            "total_staged_surfaces": 256,
            "pending": 0,
        },
        "stage_contract": {
            "required_per_entry": ["statement", "hint", "answer", "solution"],
            "all_present": True,
            "all_stage_ids_canonical": True,
            "minimum_solution_chars": 145,
            "short_solutions": short_solutions,
        },
        "rights_and_provenance": {
            "companion_license": "CC BY 4.0",
            "spine_context": "CC BY-NC-SA 3.0 (conservative treatment)",
            "nonendorsement_present": True,
            "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
        },
        "content_concepts": {"required": list(required_phrases), "missing": missing_phrases},
        "placeholder_residue": placeholders,
        "entries": entry_receipts,
    }

    manifest_report = {
        "schema_version": 1,
        "status": "complete",
        "partial": False,
        "lane_id": "O003/C90",
        "locale": "id-ID",
        "unit": {"id": "chapter_20_product_topology", "sequence": 20},
        "component": {
            "title": "Pendamping Belajar Mandiri Bab 20: Hasil Kali Ruang Topologi",
            "license": "CC BY 4.0",
            "is_upstream_gvsu_expression": False,
            "nonendorsement": True,
            "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
        },
        "ordered_hash_contract": "sha256(concatenation of exact file bytes in companion_files order; no separators)",
        "ordered_sha256": combined_sha,
        "companion_files": file_identities,
        "standalone_reader": identity(READER),
        "prompt_inventory": inventory_identity,
        "source_prompt_map": prompt_map_identity,
        "coverage": content_report["coverage"],
        "entries": entry_receipts,
        "qa": {
            "schema": "qa/CHAPTER20_COMPANION_SCHEMA_QA.json",
            "content": "qa/CHAPTER20_COMPANION_QA.json",
        },
    }

    return {
        SCHEMA_QA: json_bytes(schema_report),
        CONTENT_QA: json_bytes(content_report),
        MANIFEST: json_bytes(manifest_report),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = build()
    if args.check:
        stale = [str(path.relative_to(ROOT)) for path, payload in outputs.items() if not path.exists() or path.read_bytes() != payload]
        if stale:
            raise SystemExit("stale Chapter 20 companion state: " + ", ".join(stale))
        print("PASS: Chapter 20 companion covers 56/56 source prompts plus 8 mastery checks")
        return
    for path, payload in outputs.items():
        path.write_bytes(payload)
        print(f"WROTE {path.relative_to(ROOT)} {len(payload)} bytes sha256={sha256(payload)}")


if __name__ == "__main__":
    main()
