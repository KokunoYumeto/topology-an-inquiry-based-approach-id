#!/usr/bin/env python3
"""Generate and fail-closed validate the Chapter 4 modular backend."""

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
    ("chap_metric_spaces_apps.ptx", "chapter_container"),
    ("sec_met_space_app.ptx", "chapter_introduction"),
    ("sec_hamming.ptx", "hamming_metric_and_error_correction"),
    ("sec_levenshtein.ptx", "levenshtein_metric_and_edit_distance"),
)
ENTRY_COUNTS = {"source_task_guide": 8, "mastery_check": 4}
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


def stable_node_id(file_stem: str, tag: str, ordinal: int, xml_id: str | None) -> str:
    return xml_id or f"o003-gvsu-ch04-{file_stem}-{tag}-{ordinal:02d}"


def main() -> int:
    repo = Path(__file__).resolve().parent.parent
    lane = repo.parent
    authority_root = lane / "authority/gvsu-pinned/topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9/source"
    authority_assets = authority_root.parent / "assets"
    companion_path = repo / "companion/chapter_04_metric_space_applications_self_study.ptx"
    aliases_path = repo / "backend/chapter_04_entry_aliases.csv"
    terminology_path = lane / "00_control/TERMINOLOGY.csv"
    corrections_path = lane / "00_control/SOURCE_CORRECTIONS.csv"
    source_qa_path = repo / "qa/CHAPTER04_SOURCE_QA.json"
    output_path = repo / "backend/chapter_04_companion_manifest.json"

    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    companion_root = etree.parse(str(companion_path), parser).getroot()
    if companion_root.get(XML_ID) != "o003-c90-ch04-companion":
        raise SystemExit("unexpected Chapter 4 companion root ID")
    companion_elements = [node for node in companion_root.iter() if isinstance(node.tag, str)]
    companion_ids = [node.get(XML_ID) for node in companion_elements if node.get(XML_ID)]
    if len(companion_ids) != len(set(companion_ids)):
        raise SystemExit("duplicate companion xml:id")
    companion_by_id = {node.get(XML_ID): node for node in companion_elements if node.get(XML_ID)}
    companion_exercises = [node for node in companion_elements if local_name(node) == "exercise"]
    if len(companion_exercises) != sum(ENTRY_COUNTS.values()):
        raise SystemExit(
            f"expected {sum(ENTRY_COUNTS.values())} companion exercises, found {len(companion_exercises)}"
        )
    if any(not node.get(XML_ID) for node in companion_exercises):
        raise SystemExit("every companion exercise must have xml:id")

    translated_documents: dict[str, etree._Element] = {}
    authority_documents: dict[str, etree._ElementTree] = {}
    dependencies: list[dict[str, object]] = []
    structural_nodes: list[dict[str, object]] = []
    assets: list[dict[str, object]] = []
    source_tasks: list[dict[str, object]] = []
    for order, (name, role) in enumerate(SOURCE_FILES):
        authority_path = authority_root / name
        translated_path = repo / "source" / name
        authority_tree = etree.parse(str(authority_path), parser)
        translated_root = etree.parse(str(translated_path), parser).getroot()
        authority_documents[name] = authority_tree
        translated_documents[name] = translated_root
        dependencies.append({
            "order": order,
            "path": f"source/{name}",
            "xml_id": translated_root.get(XML_ID),
            "role": role,
            "authority": file_identity(authority_path),
            "translated": file_identity(translated_path),
        })

        authority_task_nodes = [
            node for node in authority_tree.getroot().iter()
            if isinstance(node.tag, str) and local_name(node) == "task"
        ]
        translated_task_nodes = [
            node for node in translated_root.iter()
            if isinstance(node.tag, str) and local_name(node) == "task"
        ]
        if len(authority_task_nodes) != len(translated_task_nodes):
            raise SystemExit(f"source task topology changed in {name}")
        for ordinal, (authority_task, translated_task) in enumerate(
            zip(authority_task_nodes, translated_task_nodes, strict=True), start=1
        ):
            source_tasks.append({
                "source_anchor_id": f"o003-gvsu-ch04-{Path(name).stem}-task-{ordinal:02d}",
                "authority_file": f"source/{name}",
                "authority_line": authority_task.sourceline,
                "authority_selector": f"(//task)[{ordinal}]",
                "translated_line": translated_task.sourceline,
            })

        ordinal_by_tag: Counter[str] = Counter()
        for node in translated_root.iter():
            if not isinstance(node.tag, str):
                continue
            tag = local_name(node)
            if tag in STRUCTURAL_TAGS:
                ordinal_by_tag[tag] += 1
                xml_id = node.get(XML_ID)
                structural_nodes.append({
                    "id": stable_node_id(Path(name).stem, tag, ordinal_by_tag[tag], xml_id),
                    "source_xml_id": xml_id,
                    "kind": tag,
                    "file": f"source/{name}",
                    "ordinal_within_file_and_kind": ordinal_by_tag[tag],
                    "translated_line": node.sourceline,
                })
            if tag == "image":
                stem = node.get("source")
                descriptions = node.findall("description")
                if not stem or len(descriptions) != 1 or not "".join(descriptions[0].itertext()).strip():
                    raise SystemExit(f"active image lacks one nonempty description: {name}:{node.sourceline}")
                asset_row: dict[str, object] = {
                    "source_stem": stem,
                    "file": f"source/{name}",
                    "line": node.sourceline,
                    "description_language": "id-ID",
                    "description_present": True,
                }
                for suffix in ("svg", "pdf"):
                    asset_path = authority_assets / f"{stem}.{suffix}"
                    if not asset_path.is_file():
                        raise SystemExit(f"missing active authority asset: {asset_path}")
                    asset_row[suffix] = {"path": f"assets/{stem}.{suffix}", **file_identity(asset_path)}
                assets.append(asset_row)

    if len(source_tasks) != ENTRY_COUNTS["source_task_guide"]:
        raise SystemExit(f"expected 8 source tasks, found {len(source_tasks)}")

    alias_rows: list[dict[str, object]] = []
    guide_exercises = companion_exercises[:ENTRY_COUNTS["source_task_guide"]]
    mastery_exercises = companion_exercises[ENTRY_COUNTS["source_task_guide"]:]
    for sequence, (entry, source_task) in enumerate(zip(guide_exercises, source_tasks, strict=True), start=1):
        alias_rows.append({
            "companion_entry_id": entry.get(XML_ID),
            "entry_kind": "source_task_guide",
            "sequence": sequence,
            "source_anchor_id": source_task["source_anchor_id"],
            "anchor_origin": "assigned_locale_neutral",
            "authority_file": source_task["authority_file"],
            "authority_line": source_task["authority_line"],
            "authority_selector": source_task["authority_selector"],
            "relationship": "provides_staged_support_for_source_task",
        })
    for offset, entry in enumerate(mastery_exercises, start=1):
        alias_rows.append({
            "companion_entry_id": entry.get(XML_ID),
            "entry_kind": "mastery_check",
            "sequence": ENTRY_COUNTS["source_task_guide"] + offset,
            "source_anchor_id": f"o003-c90-ch04-original-mastery-{offset:02d}",
            "anchor_origin": "original",
            "authority_file": "",
            "authority_line": "",
            "authority_selector": "",
            "relationship": "original_transfer_and_mastery_check",
        })
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
            raise SystemExit(f"alias entry does not resolve to an exercise: {entry_id}")
        reveals: dict[str, str] = {}
        for kind in ("hint", "answer", "solution"):
            children = entry.findall(kind)
            if len(children) != 1 or not children[0].get(XML_ID):
                raise SystemExit(f"{entry_id} must have exactly one ID-bearing {kind}")
            if children[0].get(XML_ID) != f"{entry_id}-{kind}":
                raise SystemExit(f"{entry_id} has noncanonical {kind} ID")
            reveals[kind] = children[0].get(XML_ID)
        kind = str(row["entry_kind"])
        counts[kind] += 1

        origin = str(row["anchor_origin"])
        if origin == "assigned_locale_neutral":
            relative = str(row["authority_file"]).removeprefix("source/")
            tree = authority_documents.get(relative)
            if tree is None:
                raise SystemExit(f"alias points outside Chapter 4 source closure: {relative}")
            selected = tree.xpath(str(row["authority_selector"]))
            if len(selected) != 1:
                raise SystemExit(f"authority selector does not resolve uniquely: {entry_id}")
            if int(row["authority_line"]) != selected[0].sourceline:
                raise SystemExit(f"stale authority line for {entry_id}")

        entries.append({
            "id": entry_id,
            "kind": kind,
            "sequence": int(row["sequence"]),
            "source_anchor": row["source_anchor_id"],
            "anchor_origin": origin,
            "authority_file": row["authority_file"] or None,
            "authority_line": int(row["authority_line"]) if row["authority_line"] else None,
            "authority_selector": row["authority_selector"] or None,
            "relationship": row["relationship"],
            **reveals,
        })
    if dict(counts) != ENTRY_COUNTS:
        raise SystemExit(f"entry coverage mismatch: {dict(counts)}")

    with terminology_path.open(encoding="utf-8-sig", newline="") as handle:
        terms = list(csv.DictReader(handle))
    with corrections_path.open(encoding="utf-8-sig", newline="") as handle:
        corrections = [
            row for row in csv.DictReader(handle)
            if row["unit"] == "chapter_04_metric_space_applications"
        ]
    source_qa = json.loads(source_qa_path.read_text(encoding="utf-8"))
    if source_qa.get("status") != "pass":
        raise SystemExit("Chapter 4 source QA is not passing")

    manifest = {
        "schema_version": "1.0.0",
        "lane_id": "O003-C90",
        "locale": "id-ID",
        "unit": {
            "id": "o003-c90-ch04-metric-space-applications",
            "sequence": 4,
            "title": "Penerapan Ruang Metrik",
            "prerequisites": ["o003-c90-ch03-metric-spaces"],
            "concepts": [
                "hamming_metric",
                "binary_codes",
                "error_detection",
                "nearest_codeword_decoding",
                "levenshtein_metric",
                "edit_distance",
                "finite_strings",
                "metric_verification",
            ],
        },
        "component": {
            "id": "o003-c90-ch04-companion",
            "type": "self_study_companion",
            "title": "Pendamping Mandiri Bab 4: Penerapan Ruang Metrik",
            "path": "repo/companion/chapter_04_metric_space_applications_self_study.ptx",
            "entry_alias_map": "repo/backend/chapter_04_entry_aliases.csv",
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
        "translated_unit_source_qa": {"path": "repo/qa/CHAPTER04_SOURCE_QA.json", **file_identity(source_qa_path)},
        "control_inputs": {
            "terminology": {"path": "00_control/TERMINOLOGY.csv", **file_identity(terminology_path)},
            "source_corrections": {"path": "00_control/SOURCE_CORRECTIONS.csv", **file_identity(corrections_path)},
        },
        "unit_dependencies": dependencies,
        "structural_nodes": structural_nodes,
        "terms": terms,
        "entries": entries,
        "assets": assets,
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
            "source_task_guides": ENTRY_COUNTS["source_task_guide"],
            "mastery_checks": ENTRY_COUNTS["mastery_check"],
            "hints": sum(ENTRY_COUNTS.values()),
            "answers": sum(ENTRY_COUNTS.values()),
            "solutions": sum(ENTRY_COUNTS.values()),
            "active_images_with_id_ID_descriptions": len(assets),
            "answer_reveal_policy": "delayed_or_collapsible_in_reader",
        },
    }
    payload = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    output_path.write_text(payload, encoding="utf-8", newline="\n")
    print(json.dumps({
        "status": "pass",
        "aliases": {"path": str(aliases_path), **file_identity(aliases_path)},
        "output": str(output_path),
        **file_identity(output_path),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
