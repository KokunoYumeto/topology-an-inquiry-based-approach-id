#!/usr/bin/env python3
"""Generate and fail-closed validate the Chapter 3 modular backend."""

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
    ("chap_metric_spaces.ptx", "chapter_container"),
    ("sec_metric_space_intro.ptx", "taxicab_motivation_and_exploration"),
    ("sec_metric_space.ptx", "metric_axioms_examples_and_max_metric"),
    ("sec_euclid_rn.ptx", "euclidean_metric_and_cauchy_schwarz"),
    ("sec_metric_space_summ.ptx", "chapter_summary"),
    ("sec_metric_space_exer.ptx", "fourteen_exercises"),
)
ENTRY_COUNTS = {"activity_checkpoint": 6, "exercise_guide": 14, "mastery_check": 8}
STRUCTURAL_TAGS = {
    "definition",
    "lemma",
    "corollary",
    "example",
    "exploration",
    "activity",
    "exercise",
}


def local_name(node: etree._Element) -> str:
    return etree.QName(node).localname


def file_identity(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def stable_node_id(file_stem: str, tag: str, ordinal: int, xml_id: str | None) -> str:
    return xml_id or f"o003-gvsu-ch03-{file_stem}-{tag}-{ordinal:02d}"


def main() -> int:
    repo = Path(__file__).resolve().parent.parent
    lane = repo.parent
    authority_root = lane / "authority/gvsu-pinned/topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9/source"
    authority_assets = authority_root.parent / "assets"
    companion_path = repo / "companion/chapter_03_metric_spaces_self_study.ptx"
    aliases_path = repo / "backend/chapter_03_entry_aliases.csv"
    terminology_path = lane / "00_control/TERMINOLOGY.csv"
    corrections_path = lane / "00_control/SOURCE_CORRECTIONS.csv"
    source_qa_path = repo / "qa/CHAPTER03_SOURCE_QA.json"
    output_path = repo / "backend/chapter_03_companion_manifest.json"

    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    companion_root = etree.parse(str(companion_path), parser).getroot()
    companion_elements = [node for node in companion_root.iter() if isinstance(node.tag, str)]
    companion_ids = [node.get(XML_ID) for node in companion_elements if node.get(XML_ID)]
    if len(companion_ids) != len(set(companion_ids)):
        raise SystemExit("duplicate companion xml:id")
    companion_by_id = {node.get(XML_ID): node for node in companion_elements if node.get(XML_ID)}

    with aliases_path.open(encoding="utf-8", newline="") as handle:
        alias_rows = list(csv.DictReader(handle))
    if len(alias_rows) != sum(ENTRY_COUNTS.values()):
        raise SystemExit(f"expected {sum(ENTRY_COUNTS.values())} alias rows, found {len(alias_rows)}")
    if len({row["companion_entry_id"] for row in alias_rows}) != len(alias_rows):
        raise SystemExit("duplicate companion entry in alias map")

    translated_documents: dict[str, etree._Element] = {}
    authority_documents: dict[str, etree._ElementTree] = {}
    dependencies: list[dict[str, object]] = []
    structural_nodes: list[dict[str, object]] = []
    assets: list[dict[str, object]] = []
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

    entries: list[dict[str, object]] = []
    counts: Counter[str] = Counter()
    for row in alias_rows:
        entry_id = row["companion_entry_id"]
        entry = companion_by_id.get(entry_id)
        if entry is None or local_name(entry) != "exercise":
            raise SystemExit(f"alias entry does not resolve to an exercise: {entry_id}")
        reveals: dict[str, str] = {}
        for kind in ("hint", "answer", "solution"):
            children = entry.findall(kind)
            if len(children) != 1 or not children[0].get(XML_ID):
                raise SystemExit(f"{entry_id} must have exactly one ID-bearing {kind}")
            reveals[kind] = children[0].get(XML_ID)
        kind = row["entry_kind"]
        if kind not in ENTRY_COUNTS:
            raise SystemExit(f"unknown entry kind: {kind}")
        counts[kind] += 1

        origin = row["anchor_origin"]
        if origin in {"upstream", "assigned_locale_neutral"}:
            relative = row["authority_file"].removeprefix("source/")
            tree = authority_documents.get(relative)
            if tree is None:
                raise SystemExit(f"alias points outside Chapter 3 source closure: {relative}")
            selected = tree.xpath(row["authority_selector"], namespaces={"xml": "http://www.w3.org/XML/1998/namespace"})
            if len(selected) != 1:
                raise SystemExit(f"authority selector does not resolve uniquely: {entry_id}")
            if int(row["authority_line"]) != selected[0].sourceline:
                raise SystemExit(f"stale authority line for {entry_id}")
            if origin == "upstream" and selected[0].get(XML_ID) != row["source_anchor_id"]:
                raise SystemExit(f"upstream anchor mismatch for {entry_id}")

        entries.append({
            "id": entry_id,
            "kind": kind,
            "sequence": int(row["sequence"]),
            "source_anchor": row["source_anchor_id"],
            "anchor_origin": origin,
            "authority_file": row["authority_file"],
            "authority_line": int(row["authority_line"]) if row["authority_line"] else None,
            "authority_selector": row["authority_selector"],
            "relationship": row["relationship"],
            **reveals,
        })
    if dict(counts) != ENTRY_COUNTS:
        raise SystemExit(f"entry coverage mismatch: {dict(counts)}")

    with terminology_path.open(encoding="utf-8-sig", newline="") as handle:
        terms = list(csv.DictReader(handle))
    with corrections_path.open(encoding="utf-8-sig", newline="") as handle:
        corrections = [row for row in csv.DictReader(handle) if row["unit"] == "chapter_03_metric_spaces"]
    source_qa = json.loads(source_qa_path.read_text(encoding="utf-8"))
    if source_qa.get("status") != "pass":
        raise SystemExit("Chapter 3 source QA is not passing")

    manifest = {
        "schema_version": "1.0.0",
        "lane_id": "O003-C90",
        "locale": "id-ID",
        "unit": {
            "id": "o003-c90-ch03-metric-spaces",
            "sequence": 3,
            "title": "Ruang Metrik",
            "prerequisites": ["o003-c90-ch01-sets", "o003-c90-ch02-functions"],
            "concepts": [
                "metric_axioms",
                "euclidean_metric",
                "taxicab_metric",
                "max_metric",
                "discrete_metric",
                "open_balls",
                "cauchy_schwarz_inequality",
                "triangle_inequality",
                "finite_graph_metrics",
                "metric_transforms",
            ],
        },
        "component": {
            "id": "o003-c90-ch03-companion",
            "type": "self_study_companion",
            "title": "Pendamping Mandiri Bab 3: Ruang Metrik",
            "path": "repo/companion/chapter_03_metric_spaces_self_study.ptx",
            "entry_alias_map": "repo/backend/chapter_03_entry_aliases.csv",
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
        "translated_unit_source_qa": {"path": "repo/qa/CHAPTER03_SOURCE_QA.json", **file_identity(source_qa_path)},
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
            "source_exploration_and_activity_checkpoints": ENTRY_COUNTS["activity_checkpoint"],
            "source_exercise_guides": ENTRY_COUNTS["exercise_guide"],
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
    print(json.dumps({"status": "pass", "output": str(output_path), **file_identity(output_path)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
