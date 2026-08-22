#!/usr/bin/env python3
"""Generate and fail-closed validate the Chapter 5 modular backend."""

from __future__ import annotations

from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import sys

from lxml import etree


XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
SOURCE_FILES = (
    ("chap_glb.ptx", "chapter_container"),
    ("sec_glb_intro.ptx", "greatest_lower_bound_introduction"),
    ("sec_dist_point_set.ptx", "point_to_set_distance"),
    ("sec_glb_summ.ptx", "chapter_summary"),
    ("sec_glb_exer.ptx", "chapter_exercises"),
)
COMPANION_FRAGMENTS = (
    "chapter_05_intro_guides.ptx",
    "chapter_05_point_set_guides.ptx",
    "chapter_05_exercise_guides_a.ptx",
    "chapter_05_exercise_guides_b.ptx",
    "chapter_05_mastery.ptx",
)
ALIAS_FIELDS = (
    "companion_entry_id",
    "entry_kind",
    "sequence",
    "source_anchor_id",
    "anchor_origin",
    "authority_file",
    "authority_line",
    "authority_selector",
    "relationship",
)
STRUCTURAL_TAGS = {
    "definition",
    "theorem",
    "lemma",
    "corollary",
    "example",
    "exploration",
    "activity",
    "exercise",
    "task",
}


def local_name(node: etree._Element) -> str:
    return etree.QName(node).localname


def file_identity(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def entry_ids() -> tuple[list[str], list[str]]:
    source = (
        [f"o003-c90-ch05-intro-task-{number:02d}" for number in range(1, 6)]
        + [f"o003-c90-ch05-pointset-task-{number:02d}" for number in range(1, 7)]
        + [f"o003-c90-ch05-exercise-task-{number:02d}" for number in range(1, 38)]
    )
    mastery = [f"o003-c90-ch05-mastery-{number:02d}" for number in range(1, 7)]
    return source, mastery


def prompt_nodes(tree: etree._ElementTree, name: str) -> list[tuple[etree._Element, str]]:
    root = tree.getroot()
    if name in {"sec_glb_intro.ptx", "sec_dist_point_set.ptx"}:
        return [
            (node, "statement_bearing_task")
            for node in root.iter("task")
            if node.find("statement") is not None
        ]
    if name != "sec_glb_exer.ptx":
        return []
    prompts: list[tuple[etree._Element, str]] = []
    for exercise in root.findall("exercise"):
        tasks = [
            node
            for node in exercise.iter("task")
            if node.find("statement") is not None
        ]
        if tasks:
            prompts.extend((node, "statement_bearing_task") for node in tasks)
        elif exercise.find("statement") is not None:
            prompts.append((exercise, "standalone_exercise"))
    return prompts


def main() -> int:
    repo = Path(__file__).resolve().parent.parent
    lane = repo.parent
    authority_root = (
        lane
        / "authority/gvsu-pinned/topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9/source"
    )
    companion_path = repo / "companion/chapter_05_greatest_lower_bound_self_study.ptx"
    aliases_path = repo / "backend/chapter_05_entry_aliases.csv"
    output_path = repo / "backend/chapter_05_companion_manifest.json"
    terminology_path = lane / "00_control/TERMINOLOGY.csv"
    corrections_path = lane / "00_control/SOURCE_CORRECTIONS.csv"
    source_qa_path = repo / "qa/CHAPTER05_SOURCE_QA.json"
    companion_qa_path = repo / "qa/CHAPTER05_COMPANION_QA.json"
    parser = etree.XMLParser(resolve_entities=False, no_network=True)

    source_qa = json.loads(source_qa_path.read_text(encoding="utf-8"))
    companion_qa = json.loads(companion_qa_path.read_text(encoding="utf-8"))
    if source_qa.get("status") != "pass":
        raise SystemExit("Chapter 5 source QA is not passing")
    if companion_qa.get("status") != "pass":
        raise SystemExit("Chapter 5 companion QA is not passing")

    companion_tree = etree.parse(str(companion_path), parser)
    companion_tree.xinclude()
    companion_root = companion_tree.getroot()
    if companion_root.get(XML_ID) != "o003-c90-ch05-companion":
        raise SystemExit("unexpected Chapter 5 companion root ID")
    companion_elements = [
        node for node in companion_root.iter() if isinstance(node.tag, str)
    ]
    companion_by_id = {
        node.get(XML_ID): node for node in companion_elements if node.get(XML_ID)
    }

    dependencies: list[dict[str, object]] = []
    structural_nodes: list[dict[str, object]] = []
    authority_trees: dict[str, etree._ElementTree] = {}
    source_prompts: list[dict[str, object]] = []
    for order, (name, role) in enumerate(SOURCE_FILES):
        authority_path = authority_root / name
        translated_path = repo / "source" / name
        authority_tree = etree.parse(str(authority_path), parser)
        translated_tree = etree.parse(str(translated_path), parser)
        authority_trees[name] = authority_tree
        dependencies.append(
            {
                "order": order,
                "path": f"source/{name}",
                "xml_id": translated_tree.getroot().get(XML_ID),
                "role": role,
                "authority": file_identity(authority_path),
                "translated": file_identity(translated_path),
            }
        )

        authority_prompts = prompt_nodes(authority_tree, name)
        translated_prompts = prompt_nodes(translated_tree, name)
        if len(authority_prompts) != len(translated_prompts):
            raise SystemExit(f"source prompt topology changed in {name}")
        for ordinal, ((authority_node, kind), (translated_node, translated_kind)) in enumerate(
            zip(authority_prompts, translated_prompts, strict=True), start=1
        ):
            if kind != translated_kind:
                raise SystemExit(f"source prompt kind changed in {name}:{ordinal}")
            source_prompts.append(
                {
                    "source_anchor_id": f"o003-gvsu-ch05-{Path(name).stem}-prompt-{ordinal:02d}",
                    "prompt_kind": kind,
                    "authority_file": f"source/{name}",
                    "authority_line": authority_node.sourceline,
                    "authority_selector": authority_tree.getpath(authority_node),
                    "translated_line": translated_node.sourceline,
                }
            )

        ordinal_by_tag: Counter[str] = Counter()
        for node in translated_tree.getroot().iter():
            if not isinstance(node.tag, str):
                continue
            tag = local_name(node)
            if tag not in STRUCTURAL_TAGS:
                continue
            ordinal_by_tag[tag] += 1
            xml_id = node.get(XML_ID)
            structural_nodes.append(
                {
                    "id": xml_id
                    or f"o003-gvsu-ch05-{Path(name).stem}-{tag}-{ordinal_by_tag[tag]:02d}",
                    "source_xml_id": xml_id,
                    "kind": tag,
                    "file": f"source/{name}",
                    "ordinal_within_file_and_kind": ordinal_by_tag[tag],
                    "translated_line": node.sourceline,
                }
            )

    source_entry_ids, mastery_entry_ids = entry_ids()
    if len(source_prompts) != len(source_entry_ids) or len(source_prompts) != 48:
        raise SystemExit(f"expected 48 source prompts, found {len(source_prompts)}")

    alias_rows: list[dict[str, object]] = []
    for sequence, (entry_id, prompt) in enumerate(
        zip(source_entry_ids, source_prompts, strict=True), start=1
    ):
        alias_rows.append(
            {
                "companion_entry_id": entry_id,
                "entry_kind": "source_prompt_guide",
                "sequence": sequence,
                "source_anchor_id": prompt["source_anchor_id"],
                "anchor_origin": "assigned_locale_neutral",
                "authority_file": prompt["authority_file"],
                "authority_line": prompt["authority_line"],
                "authority_selector": prompt["authority_selector"],
                "relationship": "provides_staged_support_for_source_prompt",
            }
        )
    for offset, entry_id in enumerate(mastery_entry_ids, start=1):
        alias_rows.append(
            {
                "companion_entry_id": entry_id,
                "entry_kind": "mastery_check",
                "sequence": len(source_entry_ids) + offset,
                "source_anchor_id": f"o003-c90-ch05-original-mastery-{offset:02d}",
                "anchor_origin": "original",
                "authority_file": "",
                "authority_line": "",
                "authority_selector": "",
                "relationship": "original_transfer_and_mastery_check",
            }
        )
    aliases_path.parent.mkdir(parents=True, exist_ok=True)
    with aliases_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ALIAS_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(alias_rows)

    entries: list[dict[str, object]] = []
    counts: Counter[str] = Counter()
    for row in alias_rows:
        entry_id = str(row["companion_entry_id"])
        entry = companion_by_id.get(entry_id)
        if entry is None or local_name(entry) != "exercise":
            raise SystemExit(f"alias entry does not resolve: {entry_id}")
        reveals: dict[str, str] = {}
        for kind in ("hint", "answer", "solution"):
            children = entry.findall(kind)
            expected = f"{entry_id}-{kind}"
            if len(children) != 1 or children[0].get(XML_ID) != expected:
                raise SystemExit(f"{entry_id} has invalid {kind} reveal")
            reveals[kind] = expected
        entry_kind = str(row["entry_kind"])
        counts[entry_kind] += 1
        if row["anchor_origin"] == "assigned_locale_neutral":
            name = str(row["authority_file"]).removeprefix("source/")
            selected = authority_trees[name].xpath(str(row["authority_selector"]))
            if len(selected) != 1 or selected[0].sourceline != int(row["authority_line"]):
                raise SystemExit(f"stale authority locator for {entry_id}")
        entries.append(
            {
                "id": entry_id,
                "kind": entry_kind,
                "sequence": int(row["sequence"]),
                "source_anchor": row["source_anchor_id"],
                "anchor_origin": row["anchor_origin"],
                "authority_file": row["authority_file"] or None,
                "authority_line": int(row["authority_line"]) if row["authority_line"] else None,
                "authority_selector": row["authority_selector"] or None,
                "relationship": row["relationship"],
                **reveals,
            }
        )
    expected_counts = {"source_prompt_guide": 48, "mastery_check": 6}
    if dict(counts) != expected_counts:
        raise SystemExit(f"entry coverage mismatch: {dict(counts)}")

    with terminology_path.open(encoding="utf-8-sig", newline="") as handle:
        terms = list(csv.DictReader(handle))
    with corrections_path.open(encoding="utf-8-sig", newline="") as handle:
        corrections = [
            row
            for row in csv.DictReader(handle)
            if row["unit"] == "chapter_05_greatest_lower_bounds"
        ]

    manifest = {
        "schema_version": "1.0.0",
        "lane_id": "O003-C90",
        "locale": "id-ID",
        "unit": {
            "id": "o003-c90-ch05-greatest-lower-bound",
            "sequence": 5,
            "title": "Batas Bawah Terbesar",
            "prerequisites": ["o003-c90-ch03-metric-spaces"],
            "concepts": [
                "lower_and_upper_bounds",
                "infimum_and_supremum",
                "completeness_of_real_numbers",
                "point_to_set_distance",
                "supremum_metric",
                "archimedean_property",
                "density_of_rationals_and_irrationals",
            ],
        },
        "component": {
            "id": "o003-c90-ch05-companion",
            "type": "self_study_companion",
            "title": "Pendamping Mandiri Bab 5: Batas Bawah Terbesar",
            "path": "repo/companion/chapter_05_greatest_lower_bound_self_study.ptx",
            "fragments": [
                {"path": f"repo/companion/{name}", **file_identity(repo / "companion" / name)}
                for name in COMPANION_FRAGMENTS
            ],
            "entry_alias_map": "repo/backend/chapter_05_entry_aliases.csv",
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
            "chapter_ordered_sha256": "f61946b39ce441f8c2323ac9b03d398dc00ffdc6f730deb6f5f75afe61d115bf",
        },
        "translated_unit_source_qa": {
            "path": "repo/qa/CHAPTER05_SOURCE_QA.json",
            **file_identity(source_qa_path),
        },
        "companion_qa": {
            "path": "repo/qa/CHAPTER05_COMPANION_QA.json",
            **file_identity(companion_qa_path),
        },
        "control_inputs": {
            "terminology": {"path": "00_control/TERMINOLOGY.csv", **file_identity(terminology_path)},
            "source_corrections": {
                "path": "00_control/SOURCE_CORRECTIONS.csv",
                **file_identity(corrections_path),
            },
        },
        "unit_dependencies": dependencies,
        "structural_nodes": structural_nodes,
        "terms": terms,
        "entries": entries,
        "assets": [],
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
            "source_prompt_guides": 48,
            "mastery_checks": 6,
            "hints": 54,
            "answers": 54,
            "solutions": 54,
            "active_images_with_id_ID_descriptions": 0,
            "answer_reveal_policy": "delayed_or_collapsible_in_reader",
        },
    }
    output_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "aliases": {"path": str(aliases_path), **file_identity(aliases_path)},
                "output": {"path": str(output_path), **file_identity(output_path)},
                "entries": dict(counts),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
