#!/usr/bin/env python3
"""Regenerate deterministic staged-content QA for the Chapter 19 companion."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
from typing import Any

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
COMPANION = ROOT / "companion"
BACKEND = ROOT / "backend"
QA = ROOT / "qa"
WRAPPER = COMPANION / "chapter_19_path_connected_spaces_self_study.ptx"
PROMPT_MAP = BACKEND / "chapter_19_source_prompt_map.csv"
OUTPUT = QA / "CHAPTER19_COMPANION_CONTENT_QA.json"
FILES = (
    "chapter_19_source_guides_a.ptx",
    "chapter_19_exercise_guides_a.ptx",
    "chapter_19_exercise_guides_b.ptx",
    "chapter_19_mastery.ptx",
)
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
EXACT_MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
FORBIDDEN = ("TODO", "TBD", "lorem ipsum", "solusi menyusul", "jawaban menyusul")


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def identity(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(payload), "sha256": sha256(payload)}


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def text(node: etree._Element) -> str:
    return " ".join("".join(node.itertext()).split())


def build_payload() -> bytes:
    prompt_rows = list(csv.DictReader(io.StringIO(PROMPT_MAP.read_text(encoding="utf-8"), newline="")))
    if len(prompt_rows) != 39 or {row["support_status"] for row in prompt_rows} != {"covered"}:
        raise SystemExit("Chapter 19 prompt map is not sealed at 39 covered rows")
    canonical_ids: list[str] = []
    for row in prompt_rows:
        if row["entry_id"] not in canonical_ids:
            canonical_ids.append(row["entry_id"])
    expected_ids = canonical_ids + [f"o003-c90-ch19-mastery-{number:02d}" for number in range(1, 9)]

    document = etree.parse(str(WRAPPER), etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False))
    document.xinclude()
    exercises = document.xpath("//exercise")
    observed_ids = [exercise.get(XML_ID) for exercise in exercises]
    if observed_ids != expected_ids:
        raise SystemExit("companion entry order differs from the covered prompt map plus mastery sequence")

    minimum_lengths = {"statement": 40, "hint": 20, "answer": 5, "solution": 100}
    length_failures: list[dict[str, Any]] = []
    stage_hashes: dict[str, dict[str, str]] = {}
    for exercise in exercises:
        entry_id = exercise.get(XML_ID)
        stage_hashes[entry_id] = {}
        for tag, minimum in minimum_lengths.items():
            nodes = exercise.xpath(f"./{tag}")
            if len(nodes) != 1:
                raise SystemExit(f"wrong {tag} cardinality for {entry_id}")
            value = text(nodes[0])
            if len(value) < minimum:
                length_failures.append({"entry_id": entry_id, "stage": tag, "characters": len(value), "minimum": minimum})
            if any(marker.casefold() in value.casefold() for marker in FORBIDDEN):
                raise SystemExit(f"placeholder marker in {entry_id}/{tag}")
            stage_hashes[entry_id][tag] = sha256(etree.tostring(nodes[0], method="c14n", with_comments=True))
    if length_failures:
        raise SystemExit(f"underspecified staged surfaces: {length_failures}")

    by_id = {exercise.get(XML_ID): exercise for exercise in exercises}
    truth_expectations = {
        "o003-c90-ch19-exer-b-04": "Salah",
        "o003-c90-ch19-exer-b-05": "Salah",
        "o003-c90-ch19-exer-b-06": "salah",
        "o003-c90-ch19-exer-b-07": "Benar",
        "o003-c90-ch19-exer-b-08": "Benar",
    }
    for entry_id, expected in truth_expectations.items():
        answer = text(by_id[entry_id].xpath("./answer")[0])
        if expected.casefold() not in answer.casefold():
            raise SystemExit(f"true/false answer is not explicit for {entry_id}")
    harmonic_text = " ".join(
        text(by_id[entry_id])
        for entry_id in ("o003-c90-ch19-exer-a-07", "o003-c90-ch19-exer-a-08")
    )
    for required in ("definisi literal", "lokal terhubung lintasan", "ruas vertikal"):
        if required.casefold() not in harmonic_text.casefold():
            raise SystemExit(f"harmonic-broom source mismatch is not transparent: {required}")

    wrapper_text = text(document.getroot())
    for required in ("CC BY 4.0", "CC BY-NC-SA 3.0", EXACT_MODEL, "tidak menyatakan dukungan", "39", "47", "188"):
        if required not in wrapper_text:
            raise SystemExit(f"rights/provenance/count statement absent: {required}")

    report = {
        "schema_version": 1,
        "status": "pass",
        "failures": [],
        "checks": {
            "covered_prompt_map_exact": True,
            "source_entry_order_exact": True,
            "mastery_sequence_exact": True,
            "all_four_staged_surfaces_present": True,
            "all_staged_surfaces_substantive": True,
            "no_placeholder_markers": True,
            "true_false_answers_explicit": True,
            "literal_harmonic_broom_mismatch_transparent": True,
            "rights_non_endorsement_and_model_exact": True,
        },
        "counts": {"source_entries": 39, "mastery_entries": 8, "total_entries": 47, "staged_surfaces": 188, "true_false_entries": 5},
        "inputs": {"wrapper": identity(WRAPPER), "prompt_map": identity(PROMPT_MAP), "companion_files": [identity(COMPANION / name) for name in FILES]},
        "stage_c14n_sha256": stage_hashes,
        "model_provenance": EXACT_MODEL,
    }
    return json_bytes(report)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = build_payload()
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_bytes() != payload:
            raise SystemExit(f"deterministic Chapter 19 content QA differs: {OUTPUT}")
    else:
        OUTPUT.write_bytes(payload)
        if OUTPUT.read_bytes() != payload:
            raise SystemExit("content QA readback failed")
    print(json.dumps({"status": "pass", "check_only": args.check, "output": {"path": OUTPUT.relative_to(ROOT).as_posix(), "bytes": len(payload), "sha256": sha256(payload)}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
