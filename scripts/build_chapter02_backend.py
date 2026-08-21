#!/usr/bin/env python3
"""Generate and fail-closed validate the Chapter 2 modular backend."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import sys

from lxml import etree


XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
SOURCE_FILES = (
    ("chap_functions.ptx", "chapter_container"),
    ("sec_func_intro.ptx", "function_foundations_and_exploration"),
    ("sec_comp_func.ptx", "composition"),
    ("sec_inv_func.ptx", "inverse_functions"),
    ("sec_fun_set.ptx", "images_and_preimages"),
    ("sec_card_set.ptx", "cardinality"),
    ("sec_func_summ.ptx", "chapter_summary"),
    ("sec_func_exer.ptx", "seventeen_exercises"),
)


def file_identity(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def main() -> int:
    repo = Path(__file__).resolve().parent.parent
    lane = repo.parent
    authority_root = lane / "authority/gvsu-pinned/topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9/source"
    companion_path = repo / "companion/chapter_02_functions_self_study.ptx"
    aliases_path = repo / "backend/chapter_02_entry_aliases.csv"
    terminology_path = lane / "00_control/TERMINOLOGY.csv"
    corrections_path = lane / "00_control/SOURCE_CORRECTIONS.csv"
    output_path = repo / "backend/chapter_02_companion_manifest.json"

    root = etree.parse(str(companion_path)).getroot()
    elements = [node for node in root.iter() if isinstance(node.tag, str)]
    ids = [node.get(XML_ID) for node in elements if node.get(XML_ID)]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate companion xml:id")
    by_id = {node.get(XML_ID): node for node in elements if node.get(XML_ID)}

    with aliases_path.open(encoding="utf-8", newline="") as handle:
        alias_rows = list(csv.DictReader(handle))
    if len(alias_rows) != 33:
        raise SystemExit(f"expected 33 alias rows, found {len(alias_rows)}")
    entry_ids = [row["companion_entry_id"] for row in alias_rows]
    if len(entry_ids) != len(set(entry_ids)):
        raise SystemExit("duplicate companion entry in alias map")

    entries = []
    counts = {"activity_checkpoint": 0, "exercise_guide": 0, "mastery_check": 0}
    for row in alias_rows:
        entry_id = row["companion_entry_id"]
        entry = by_id.get(entry_id)
        if entry is None or etree.QName(entry).localname != "exercise":
            raise SystemExit(f"alias entry does not resolve to an exercise: {entry_id}")
        reveals: dict[str, str] = {}
        for kind in ("hint", "answer", "solution"):
            children = entry.findall(kind)
            if len(children) != 1 or not children[0].get(XML_ID):
                raise SystemExit(f"{entry_id} must have exactly one ID-bearing {kind}")
            reveals[kind] = children[0].get(XML_ID)
        kind = row["entry_kind"]
        if kind not in counts:
            raise SystemExit(f"unknown entry kind: {kind}")
        counts[kind] += 1
        entries.append({
            "id": entry_id,
            "kind": kind,
            "sequence": int(row["sequence"]),
            "source_anchor": row["source_anchor_id"],
            "anchor_origin": row["anchor_origin"],
            "authority_file": row["authority_file"],
            "authority_line": int(row["authority_line"]) if row["authority_line"] else None,
            "authority_selector": row["authority_selector"],
            "relationship": row["relationship"],
            **reveals,
        })
    expected_counts = {"activity_checkpoint": 8, "exercise_guide": 17, "mastery_check": 8}
    if counts != expected_counts:
        raise SystemExit(f"entry coverage mismatch: {counts}")

    dependencies = []
    for order, (name, role) in enumerate(SOURCE_FILES):
        authority_path = authority_root / name
        translated_path = repo / "source" / name
        translated_root = etree.parse(str(translated_path)).getroot()
        dependencies.append({
            "order": order,
            "path": f"source/{name}",
            "xml_id": translated_root.get(XML_ID),
            "role": role,
            "authority": file_identity(authority_path),
            "translated": file_identity(translated_path),
        })

    with terminology_path.open(encoding="utf-8-sig", newline="") as handle:
        terms = list(csv.DictReader(handle))
    with corrections_path.open(encoding="utf-8-sig", newline="") as handle:
        corrections = [row for row in csv.DictReader(handle) if row["unit"] == "chapter_02_functions"]

    manifest = {
        "schema_version": "1.0.0",
        "lane_id": "O003-C90",
        "locale": "id-ID",
        "component": {
            "id": "o003-c90-ch02-companion",
            "type": "self_study_companion",
            "title": "Pendamping Mandiri Bab 2: Fungsi",
            "path": "repo/companion/chapter_02_functions_self_study.ptx",
            "entry_alias_map": "repo/backend/chapter_02_entry_aliases.csv",
            "rights_note": "repo/companion/RIGHTS.md",
            "relationship_to_core": "supplements",
            "original_expression": True,
            "copies_petrunin_expression": False,
            "identity": file_identity(companion_path),
        },
        "authority": {
            "work": "Topology: An Inquiry-Based Approach",
            "author": "Steven Schlicker",
            "publisher_record": "Grand Valley State University ScholarWorks",
            "repository": "https://github.com/gvsuoer/topology",
            "commit": "0c2d8f614ef87aa00de373f3418146c2f1d13bb9",
            "tree": "7df245934eedb7174d5ff8af18afff5a7abdde78",
            "archive_sha256": "d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3",
            "official_record": "https://scholarworks.gvsu.edu/books/30/",
            "controlling_core_license": "CC-BY-NC-SA-3.0",
        },
        "unit_dependencies_role": "pinned_authority_and_translated_derivative",
        "translated_unit_source_qa": "repo/qa/CHAPTER02_SOURCE_QA.json",
        "unit_dependencies": dependencies,
        "terms": terms,
        "entries": entries,
        "source_corrections": corrections,
        "rights": [
            {
                "component": "upstream_text_and_id_ID_derivative",
                "license": "CC-BY-NC-SA-3.0",
                "attribution": "Steven Schlicker, Grand Valley State University",
                "noncommercial": True,
                "sharealike": True,
            },
            {
                "component": "original_id_ID_self_study_companion",
                "license": "CC-BY-4.0",
                "attribution": "Original companion for this Bahasa Indonesia edition",
                "noncommercial": False,
                "sharealike": False,
            },
            {
                "component": "software_xsl_fonts_images",
                "license": "per-component-notices",
                "attribution": "Not relicensed by this manifest",
            },
        ],
        "coverage_contract": {
            "source_exploration_and_activity_checkpoints": 8,
            "source_exercise_guides": 17,
            "mastery_checks": 8,
            "hints": 33,
            "answers": 33,
            "solutions": 33,
            "answer_reveal_policy": "delayed_or_collapsible_in_reader",
        },
    }
    payload = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    output_path.write_text(payload, encoding="utf-8", newline="\n")
    identity = file_identity(output_path)
    print(json.dumps({"status": "pass", "output": str(output_path), **identity}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
