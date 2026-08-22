#!/usr/bin/env python3
"""Fail-closed structural and coverage audit for the Chapter 3 companion."""

from __future__ import annotations

from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
import sys

from lxml import etree


XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
SOURCE_FILES = (
    "chap_metric_spaces.ptx",
    "sec_metric_space_intro.ptx",
    "sec_metric_space.ptx",
    "sec_euclid_rn.ptx",
    "sec_metric_space_summ.ptx",
    "sec_metric_space_exer.ptx",
)
EXPECTED = {"activity_checkpoint": 6, "exercise_guide": 14, "mastery_check": 8}


def local_name(node: etree._Element) -> str:
    return etree.QName(node).localname


def identity(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def text_length(node: etree._Element) -> int:
    return len(" ".join("".join(node.itertext()).split()))


def main() -> int:
    repo = Path(__file__).resolve().parent.parent
    companion = repo / "companion/chapter_03_metric_spaces_self_study.ptx"
    aliases = repo / "backend/chapter_03_entry_aliases.csv"
    report_path = repo / "qa/CHAPTER03_COMPANION_QA.json"
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    root = etree.parse(str(companion), parser).getroot()
    failures: list[str] = []

    if root.get(XML_ID) != "o003-c90-ch03-companion":
        failures.append("unexpected companion root ID")
    if root.get("{http://www.w3.org/XML/1998/namespace}lang") != "id-ID":
        failures.append("companion root is not explicitly id-ID")
    elements = [node for node in root.iter() if isinstance(node.tag, str)]
    ids = [node.get(XML_ID) for node in elements if node.get(XML_ID)]
    duplicate_ids = sorted(name for name, count in Counter(ids).items() if count > 1)
    if duplicate_ids:
        failures.append(f"duplicate companion IDs: {duplicate_ids}")
    by_id = {node.get(XML_ID): node for node in elements if node.get(XML_ID)}

    with aliases.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    counts = Counter(row["entry_kind"] for row in rows)
    if dict(counts) != EXPECTED:
        failures.append(f"alias coverage mismatch: {dict(counts)}")
    if len(rows) != len({row["companion_entry_id"] for row in rows}):
        failures.append("duplicate alias companion entry")

    reveal_counts = Counter()
    entry_rows: list[dict[str, object]] = []
    for row in rows:
        entry_id = row["companion_entry_id"]
        node = by_id.get(entry_id)
        if node is None or local_name(node) != "exercise":
            failures.append(f"missing exercise entry: {entry_id}")
            continue
        lengths: dict[str, int] = {}
        minima = {"statement": 40, "hint": 20, "answer": 20, "solution": 140}
        for kind, minimum in minima.items():
            children = node.findall(kind)
            if len(children) != 1:
                failures.append(f"{entry_id} has {len(children)} {kind} children")
                continue
            length = text_length(children[0])
            lengths[kind] = length
            if length < minimum:
                failures.append(f"{entry_id} {kind} is too short for a complete staged entry: {length}")
            if kind != "statement":
                reveal_counts[kind] += 1
                expected_id = f"{entry_id}-{kind}"
                if children[0].get(XML_ID) != expected_id:
                    failures.append(f"{entry_id} has noncanonical {kind} ID")
        entry_rows.append({"id": entry_id, "kind": row["entry_kind"], "text_lengths": lengths})

    source_ids: set[str] = set()
    source_activity_count = 0
    source_exercise_count = 0
    for name in SOURCE_FILES:
        source_root = etree.parse(str(repo / "source" / name), parser).getroot()
        for node in source_root.iter():
            if not isinstance(node.tag, str):
                continue
            if node.get(XML_ID):
                source_ids.add(node.get(XML_ID))
            tag = local_name(node)
            if tag in {"activity", "exploration"}:
                source_activity_count += 1
            elif tag == "exercise":
                source_exercise_count += 1
    if source_activity_count != EXPECTED["activity_checkpoint"]:
        failures.append(f"source activity count changed: {source_activity_count}")
    if source_exercise_count != EXPECTED["exercise_guide"]:
        failures.append(f"source exercise count changed: {source_exercise_count}")

    refs = [node.get("ref") for node in elements if local_name(node) == "xref" and node.get("ref")]
    missing_refs = sorted(set(refs) - source_ids - set(ids))
    if missing_refs:
        failures.append(f"unresolved companion xrefs: {missing_refs}")

    prose_parts: list[str] = []
    for node in elements:
        if local_name(node) in {"m", "me", "men", "mrow", "c", "code", "sage"}:
            continue
        if node.text:
            prose_parts.append(node.text)
        if node.tail:
            prose_parts.append(node.tail)
    prose = " ".join(prose_parts)
    english_markers = sorted(set(re.findall(
        r"\b(?:Let|Show|Prove|Determine|Describe|Every|Suppose|Recall|Hint|Answer|Solution|True|False)\b",
        prose,
        flags=re.IGNORECASE,
    )))
    if english_markers:
        failures.append(f"active English instruction markers: {english_markers}")
    placeholders = sorted(set(re.findall(r"\b(?:TODO|TBD|FIXME|LOREM)\b|\?\?\?", prose, flags=re.IGNORECASE)))
    if placeholders:
        failures.append(f"placeholder residue: {placeholders}")
    raw = companion.read_text(encoding="utf-8")
    if re.search(r"(?:C:\\Users\\|github_pat_|ghp_|ZENODO|api[_-]?token|access[_-]?token)", raw, flags=re.IGNORECASE):
        failures.append("local path or credential-like residue in companion")
    normalized_raw = " ".join(raw.split())
    required_rights_phrases = (
        "Creative Commons Attribution 4.0",
        "bukan teks Steven Schlicker atau GVSU",
        "tidak menyalin ungkapan dari karya Anton Petrunin",
    )
    for phrase in required_rights_phrases:
        if phrase not in normalized_raw:
            failures.append(f"missing component-boundary phrase: {phrase}")

    report = {
        "schema_version": 1,
        "status": "pass" if not failures else "fail",
        "companion": identity(companion),
        "aliases": identity(aliases),
        "entry_counts": dict(counts),
        "reveal_counts": dict(reveal_counts),
        "xml_ids": len(ids),
        "source_activity_containers": source_activity_count,
        "source_exercises": source_exercise_count,
        "xrefs": len(refs),
        "missing_xrefs": missing_refs,
        "entries": entry_rows,
        "failures": failures,
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"report": identity(report_path), **{key: report[key] for key in ("status", "entry_counts", "reveal_counts", "xml_ids", "xrefs", "failures")}}, ensure_ascii=False, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
