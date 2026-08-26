#!/usr/bin/env python3
"""Build the deterministic Chapter 15 prompt inventory and bootstrap backend.

The carrier census and exercise batches are derived from the immutable pinned
PreTeXt structure.  Prompts are never inferred from prose or translated titles.
The only outputs are the Chapter 15 inventory, prompt map, and grouping backend.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import io
import json
from pathlib import Path
import string
from typing import Any

from lxml import etree

import build_chapter14_prompt_inventory as base


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
BACKEND = ROOT / "backend"

FROZEN_AUTHORITY_COMMIT = "0c2d8f614ef87aa00de373f3418146c2f1d13bb9"
PINNED_AUTHORITY_ROOT = (
    LANE / "authority" / "gvsu-pinned" / f"topology-{FROZEN_AUTHORITY_COMMIT}"
)
SOURCE_DIR = PINNED_AUTHORITY_ROOT / "source"
CHAPTER_FILE = "chap_subspaces.ptx"
EXPECTED_CHAPTER_INCLUDES = (
    "sec_sub.ptx",
    "sec_subspace_top.ptx",
    "sec_base_sub.ptx",
    "sec_open_int_rn.ptx",
    "sec_sub_summ.ptx",
    "sec_sub_exer.ptx",
)
EXPECTED_AUTHORITY_FILE_COUNT = 7

AUTHORITY_ORDERED_HASH_CONTRACT = (
    "sha256 over each declared authority path as UTF-8, NUL, decimal byte "
    "length, NUL, raw file bytes, NUL, in chapter-closure order"
)
FROZEN_ORDERED_SHA256 = (
    "0586ff4d5a22ad9d220dfa4c8555ad775ffd99c8f1b3ed30030b48f6e4f6d3be"
)
AUTHORITY_SUBTREE_HASH_CONTRACT = "sha256-c14n-1.0-with-comments"
SOURCE_ANCHOR_KIND = "synthetic_locale_neutral_alias"

EXPECTED_PROMPT_TOTAL = 30
EXPECTED_NONEXERCISE_TOTAL = 16
EXPECTED_EXERCISE_TOTAL = 14
EXPECTED_GROUPING_TOTAL = 2
EXERCISE_BATCH_SIZE = 10

PROMPT_MAP_FIELDS = base.PROMPT_MAP_FIELDS
CANONICAL_PROMPT_FIELDS = base.CANONICAL_PROMPT_FIELDS

INVENTORY_PATH = BACKEND / "chapter_15_prompt_inventory.json"
PROMPT_MAP_PATH = BACKEND / "chapter_15_source_prompt_map.csv"
GROUPING_PATH = BACKEND / "chapter_15_grouping_nodes.json"
OUTPUT_PATHS = (INVENTORY_PATH, PROMPT_MAP_PATH, GROUPING_PATH)

XML_ID = base.XML_ID
XI_NS = base.XI_NS


def load_authority_closure() -> tuple[
    list[dict[str, Any]], dict[str, etree._ElementTree]
]:
    chapter_path = SOURCE_DIR / CHAPTER_FILE
    if not chapter_path.is_file():
        raise SystemExit(f"missing frozen Chapter 15 wrapper: {chapter_path}")
    chapter_doc = base.parse_xml(chapter_path)
    hrefs = tuple(
        chapter_doc.xpath("//xi:include/@href", namespaces={"xi": XI_NS})
    )
    if hrefs != EXPECTED_CHAPTER_INCLUDES:
        raise SystemExit(
            "frozen Chapter 15 XInclude order changed: "
            f"expected {EXPECTED_CHAPTER_INCLUDES}, found {hrefs}"
        )

    names = (CHAPTER_FILE, *hrefs)
    if len(names) != EXPECTED_AUTHORITY_FILE_COUNT or len(set(names)) != len(names):
        raise SystemExit("Chapter 15 authority closure is not exactly seven unique files")

    records: list[dict[str, Any]] = []
    documents: dict[str, etree._ElementTree] = {}
    for file_sequence, name in enumerate(names, start=1):
        if Path(name).name != name:
            raise SystemExit(f"nonlocal Chapter 15 include is forbidden: {name}")
        path = SOURCE_DIR / name
        if not path.is_file():
            raise SystemExit(f"missing frozen Chapter 15 authority file: {path}")
        document = chapter_doc if name == CHAPTER_FILE else base.parse_xml(path)
        if name != CHAPTER_FILE:
            nested_hrefs = document.xpath(
                "//xi:include/@href", namespaces={"xi": XI_NS}
            )
            if nested_hrefs:
                raise SystemExit(f"unexpected nested XInclude in {name}: {nested_hrefs}")
        payload = path.read_bytes()
        relative = base.authority_relative(name)
        records.append(
            {
                "sequence": file_sequence,
                "path": relative,
                "bytes": len(payload),
                "sha256": base.digest_bytes(payload),
                "payload": payload,
            }
        )
        documents[relative] = document

    actual_ordered_hash = base.ordered_authority_hash(records)
    if actual_ordered_hash != FROZEN_ORDERED_SHA256:
        raise SystemExit(
            "frozen Chapter 15 ordered authority hash changed: "
            f"expected {FROZEN_ORDERED_SHA256}, found {actual_ordered_hash}"
        )
    return records, documents


def derive_exercise_batches(exercise_total: int) -> tuple[tuple[str, int], ...]:
    """Partition the exact authority-order exercise census into bounded batches."""
    if exercise_total <= 0:
        raise SystemExit("Chapter 15 authority has no exercise prompt carriers")
    counts: list[int] = []
    remaining = exercise_total
    while remaining:
        count = min(EXERCISE_BATCH_SIZE, remaining)
        counts.append(count)
        remaining -= count
    if len(counts) > len(string.ascii_lowercase):
        raise SystemExit("exercise census exceeds the one-letter batch namespace")
    batches = tuple(zip(string.ascii_lowercase, counts, strict=False))
    if sum(count for _, count in batches) != exercise_total:
        raise SystemExit("derived exercise batches do not cover the authority census")
    if any(count < 1 or count > EXERCISE_BATCH_SIZE for _, count in batches):
        raise SystemExit("derived exercise batch violates the bounded batch contract")
    if len(batches) > 1 and any(
        count != EXERCISE_BATCH_SIZE for _, count in batches[:-1]
    ):
        raise SystemExit("a nonfinal derived exercise batch is not full")
    return batches


def exercise_entry_id(
    ordinal: int, batches: tuple[tuple[str, int], ...]
) -> tuple[str, str, int]:
    cursor = ordinal
    for letter, count in batches:
        if cursor <= count:
            return f"o003-c90-ch15-exer-{letter}-{cursor:02d}", letter, cursor
        cursor -= count
    raise SystemExit(f"exercise prompt ordinal exceeds derived batches: {ordinal}")


def build_inventory() -> tuple[bytes, bytes, bytes, dict[str, Any]]:
    if base.FROZEN_AUTHORITY_COMMIT != FROZEN_AUTHORITY_COMMIT:
        raise SystemExit("shared locator implementation has a different authority commit")
    if base.AUTHORITY_SUBTREE_HASH_CONTRACT != AUTHORITY_SUBTREE_HASH_CONTRACT:
        raise SystemExit("shared locator implementation has a different subtree contract")

    authority_records, documents = load_authority_closure()
    events = base.discover_events(authority_records, documents)
    group_events = [event for event in events if event["event_kind"] == "grouping"]
    prompt_events = [event for event in events if event["event_kind"] == "prompt"]

    if len(group_events) != EXPECTED_GROUPING_TOTAL:
        raise SystemExit(
            f"expected {EXPECTED_GROUPING_TOTAL} grouping-only tasks, "
            f"found {len(group_events)}"
        )
    if len(prompt_events) != EXPECTED_PROMPT_TOTAL:
        raise SystemExit(
            f"expected {EXPECTED_PROMPT_TOTAL} prompt units, found {len(prompt_events)}"
        )

    partition_counts = Counter(event["partition"] for event in prompt_events)
    nonexercise_total = partition_counts["nonexercise"]
    exercise_total = partition_counts["exercise"]
    if nonexercise_total != EXPECTED_NONEXERCISE_TOTAL:
        raise SystemExit(
            f"expected {EXPECTED_NONEXERCISE_TOTAL} nonexercise prompts, "
            f"found {nonexercise_total}"
        )
    if exercise_total != EXPECTED_EXERCISE_TOTAL:
        raise SystemExit(
            f"expected {EXPECTED_EXERCISE_TOTAL} exercise prompts, "
            f"found {exercise_total}"
        )
    if set(partition_counts) != {"nonexercise", "exercise"}:
        raise SystemExit(f"unexpected authority prompt partition: {partition_counts}")
    exercise_batches = derive_exercise_batches(exercise_total)

    source_xml_ids: dict[str, str] = {}
    for source_file, document in documents.items():
        for element in document.iter():
            xml_id = element.get(XML_ID)
            if not xml_id:
                continue
            if xml_id in source_xml_ids:
                raise SystemExit(
                    f"duplicate real authority xml:id {xml_id!r} in "
                    f"{source_xml_ids[xml_id]} and {source_file}"
                )
            source_xml_ids[xml_id] = source_file

    alias_counters: Counter[tuple[str, str]] = Counter()
    group_records_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    grouping_nodes: list[dict[str, Any]] = []
    for event in group_events:
        element = event["element"]
        context = base.alias_context(base.nearest_real_xml_id(element))
        counter_key = (context, "group")
        alias_counters[counter_key] += 1
        source_anchor = (
            f"o003-gvsu-ch15-{context}-group-{alias_counters[counter_key]:02d}"
        )
        locator = base.make_locator(event["source_file"], event["document"], element)
        key = (event["source_file"], locator["xpath"])
        record = {
            "id": source_anchor,
            "authority_source_file": event["source_file"],
            "authority_line": locator["authority_line"],
            "child_entry_ids": [],
            "anchor_kind": SOURCE_ANCHOR_KIND,
            "authority_locator": locator,
        }
        if key in group_records_by_key:
            raise SystemExit(f"duplicate grouping locator: {key}")
        group_records_by_key[key] = record
        grouping_nodes.append(record)

    entries: list[dict[str, Any]] = []
    nonexercise_ordinal = 0
    exercise_ordinal = 0
    prompt_alias_counters: Counter[tuple[str, str]] = Counter()
    group_keys = set(group_records_by_key)

    for sequence, event in enumerate(prompt_events, start=1):
        element = event["element"]
        partition = event["partition"]
        if partition == "exercise":
            exercise_ordinal += 1
            entry_id, batch, batch_sequence = exercise_entry_id(
                exercise_ordinal, exercise_batches
            )
            partition_sequence = exercise_ordinal
        else:
            nonexercise_ordinal += 1
            entry_id = f"o003-c90-ch15-guide-{nonexercise_ordinal:02d}"
            batch = None
            batch_sequence = None
            partition_sequence = nonexercise_ordinal

        context = base.alias_context(base.nearest_real_xml_id(element))
        label = base.alias_label(event["prompt_carrier"])
        counter_key = (context, label)
        prompt_alias_counters[counter_key] += 1
        source_anchor = (
            f"o003-gvsu-ch15-{context}-{label}-"
            f"{prompt_alias_counters[counter_key]:02d}"
        )
        locator = base.make_locator(event["source_file"], event["document"], element)
        parent_key = base.nearest_group_key(
            event["source_file"], event["document"], element, group_keys
        )
        parent_group_anchor = (
            group_records_by_key[parent_key]["id"] if parent_key is not None else None
        )
        entry = {
            "sequence": sequence,
            "id": entry_id,
            "entry_type": "source_prompt_guide",
            "source_anchor": source_anchor,
            "source_anchor_kind": SOURCE_ANCHOR_KIND,
            "authority_source_file": event["source_file"],
            "authority_line": locator["authority_line"],
            "prompt_carrier": event["prompt_carrier"],
            "authority_locator": locator,
            "parent_group_anchor": parent_group_anchor,
            "support_status": "pending",
            "partition": partition,
            "partition_sequence": partition_sequence,
            "exercise_batch": batch,
            "exercise_batch_sequence": batch_sequence,
        }
        entries.append(entry)
        if parent_key is not None:
            group_records_by_key[parent_key]["child_entry_ids"].append(entry_id)

    if nonexercise_ordinal != nonexercise_total or exercise_ordinal != exercise_total:
        raise SystemExit("generated entry partition counts differ from authority discovery")

    entry_ids = [entry["id"] for entry in entries]
    source_anchors = [entry["source_anchor"] for entry in entries]
    if len(set(entry_ids)) != len(entry_ids):
        raise SystemExit("generated Chapter 15 entry IDs are not unique")
    if len(set(source_anchors)) != len(source_anchors):
        raise SystemExit("generated Chapter 15 source aliases are not unique")
    if [entry["sequence"] for entry in entries] != list(
        range(1, EXPECTED_PROMPT_TOTAL + 1)
    ):
        raise SystemExit(
            "generated Chapter 15 entries are not in exact order "
            f"1..{EXPECTED_PROMPT_TOTAL}"
        )
    if any(entry["support_status"] != "pending" for entry in entries):
        raise SystemExit("bootstrap support status must be pending for every entry")

    grouped_children = [
        child for group in grouping_nodes for child in group["child_entry_ids"]
    ]
    prompts_with_parent = [
        entry["id"] for entry in entries if entry["parent_group_anchor"] is not None
    ]
    if not all(group["child_entry_ids"] for group in grouping_nodes):
        raise SystemExit("a grouping-only task has no mapped child prompts")
    if len(grouped_children) != len(set(grouped_children)):
        raise SystemExit("a prompt child is assigned to more than one grouping node")
    if grouped_children != prompts_with_parent:
        raise SystemExit("grouping children and prompt parent links are not one-to-one")
    if not set(grouped_children).issubset(set(entry_ids)):
        raise SystemExit("one or more grouping children do not resolve")

    prompt_rows: list[dict[str, Any]] = []
    for entry in entries:
        prompt_rows.append(
            {
                "sequence": entry["sequence"],
                "entry_id": entry["id"],
                "source_anchor": entry["source_anchor"],
                "source_anchor_kind": entry["source_anchor_kind"],
                "authority_source_file": entry["authority_source_file"],
                "authority_line": entry["authority_line"],
                "prompt_carrier": entry["prompt_carrier"],
                "authority_locator": json.dumps(
                    entry["authority_locator"],
                    ensure_ascii=False,
                    separators=(",", ":"),
                ),
                "parent_group_anchor": entry["parent_group_anchor"] or "",
                "support_status": entry["support_status"],
            }
        )

    prompt_payload = base.csv_bytes(prompt_rows)
    grouping_payload = {
        "schema_version": 1,
        "unit": "o003-c90-ch15-subspaces",
        "locator_contract": {
            "authority_commit": FROZEN_AUTHORITY_COMMIT,
            "file_field": "authority_source_file",
            "line_field": "authority_line",
            "anchor_kind": SOURCE_ANCHOR_KIND,
            "xpath_field": "authority_locator.xpath",
            "subtree_hash_contract": AUTHORITY_SUBTREE_HASH_CONTRACT,
        },
        "grouping_node_count": len(grouping_nodes),
        "all_children_resolve": True,
        "nodes": grouping_nodes,
    }
    grouping_bytes_payload = base.json_bytes(grouping_payload)

    file_census: list[dict[str, Any]] = []
    for file_record in authority_records:
        source_file = file_record["path"]
        file_entries = [
            entry for entry in entries if entry["authority_source_file"] == source_file
        ]
        file_groups = [
            group
            for group in grouping_nodes
            if group["authority_source_file"] == source_file
        ]
        carriers = Counter(entry["prompt_carrier"] for entry in file_entries)
        file_census.append(
            {
                "authority_source_file": source_file,
                "prompt_total": len(file_entries),
                "nonexercise_prompt_total": sum(
                    entry["partition"] == "nonexercise" for entry in file_entries
                ),
                "exercise_prompt_total": sum(
                    entry["partition"] == "exercise" for entry in file_entries
                ),
                "atomic_task_total": carriers["atomic_task"],
                "direct_statement_total": carriers["direct_statement"],
                "direct_body_total": carriers["direct_body"],
                "grouping_node_total": len(file_groups),
            }
        )

    carrier_counts = Counter(entry["prompt_carrier"] for entry in entries)
    canonical_mapping_sha256 = base.canonical_prompt_hash(entries)
    inventory_payload = {
        "schema_version": 1,
        "status": "prompt_inventory_complete_companion_pending",
        "partial": False,
        "lane_id": "O003/C90",
        "locale": "id-ID",
        "unit": {
            "id": "o003-c90-ch15-subspaces",
            "sequence": 15,
            "source_chapter_xml_id": "chap_subspaces",
        },
        "authority": {
            "commit": FROZEN_AUTHORITY_COMMIT,
            "root": f"authority/gvsu-pinned/topology-{FROZEN_AUTHORITY_COMMIT}",
            "source_file_count": len(authority_records),
            "ordered_hash_contract": AUTHORITY_ORDERED_HASH_CONTRACT,
            "ordered_sha256": FROZEN_ORDERED_SHA256,
            "canonical_prompt_mapping_sha256": canonical_mapping_sha256,
            "ordered_files": [
                {key: record[key] for key in ("sequence", "path", "bytes", "sha256")}
                for record in authority_records
            ],
            "line_locator_contract": {
                "file_field": "authority_source_file",
                "line_field": "authority_line",
                "source_anchor_kind": SOURCE_ANCHOR_KIND,
                "structured_locator_field": "authority_locator",
                "subtree_hash_contract": AUTHORITY_SUBTREE_HASH_CONTRACT,
                "meaning": (
                    "one-based exact carrier-start line in the pinned authority "
                    "source at the stated commit"
                ),
            },
        },
        "carrier_contract": {
            "atomic_task": "task element with no descendant task element",
            "grouping_task": (
                "task element with one or more descendant task elements; backend-only, "
                "not a prompt unit"
            ),
            "direct_statement": (
                "direct statement child of a taskless exercise, activity, or exploration"
            ),
            "direct_body": (
                "taskless activity or exploration with a direct p child and no direct statement"
            ),
        },
        "source_anchor_contract": {
            "kind": SOURCE_ANCHOR_KIND,
            "format": (
                "o003-gvsu-ch15-{nearest-real-xml-id}-{task|statement|body|group}-NN"
            ),
            "sequence_scope": "nearest real xml:id plus carrier label, in authority order",
            "translated_titles_used": False,
        },
        "entry_id_contract": {
            "nonexercise": {
                "format": "o003-c90-ch15-guide-NN",
                "count": nonexercise_ordinal,
                "first": entries[0]["id"],
                "last": next(
                    entry["id"]
                    for entry in reversed(entries)
                    if entry["partition"] == "nonexercise"
                ),
            },
            "exercise": {
                "format": "o003-c90-ch15-exer-{batch}-{NN}",
                "count": exercise_ordinal,
                "batch_derivation": (
                    "exact authority-order exercise-prompt census partitioned into "
                    f"sequential batches of at most {EXERCISE_BATCH_SIZE}"
                ),
                "batches": [
                    {"letter": letter, "count": count}
                    for letter, count in exercise_batches
                ],
                "first": next(
                    entry["id"] for entry in entries if entry["partition"] == "exercise"
                ),
                "last": entries[-1]["id"],
            },
        },
        "census": {
            "source_prompt_total": len(entries),
            "nonexercise_prompt_total": nonexercise_ordinal,
            "exercise_prompt_total": exercise_ordinal,
            "atomic_prompt_total": carrier_counts["atomic_task"],
            "direct_statement_prompt_total": carrier_counts["direct_statement"],
            "direct_body_prompt_total": carrier_counts["direct_body"],
            "direct_prompt_total": (
                carrier_counts["direct_statement"] + carrier_counts["direct_body"]
            ),
            "grouping_node_total": len(grouping_nodes),
            "grouped_child_prompt_total": len(grouped_children),
            "pending_support_total": len(entries),
            "covered_support_total": 0,
            "by_source_file": file_census,
        },
        "prompt_map": {
            "path": "backend/chapter_15_source_prompt_map.csv",
            **base.identity_bytes(prompt_payload),
            "fields": list(PROMPT_MAP_FIELDS),
            "row_count": len(prompt_rows),
        },
        "grouping_backend": {
            "path": "backend/chapter_15_grouping_nodes.json",
            **base.identity_bytes(grouping_bytes_payload),
            "node_count": len(grouping_nodes),
            "all_children_resolve": True,
        },
        "entries": entries,
    }
    inventory_bytes_payload = base.json_bytes(inventory_payload)

    verify_payloads(
        inventory_bytes_payload,
        prompt_payload,
        grouping_bytes_payload,
        documents,
        exercise_batches,
    )
    summary = {
        "status": inventory_payload["status"],
        "source_prompts": len(entries),
        "nonexercise_prompts": nonexercise_ordinal,
        "exercise_prompts": exercise_ordinal,
        "exercise_batches": [
            {"letter": letter, "count": count} for letter, count in exercise_batches
        ],
        "grouping_nodes": len(grouping_nodes),
        "carrier_counts": dict(sorted(carrier_counts.items())),
        "canonical_prompt_mapping_sha256": canonical_mapping_sha256,
    }
    return inventory_bytes_payload, prompt_payload, grouping_bytes_payload, summary


def verify_payloads(
    inventory_payload: bytes,
    prompt_payload: bytes,
    grouping_payload: bytes,
    documents: dict[str, etree._ElementTree],
    exercise_batches: tuple[tuple[str, int], ...],
) -> None:
    inventory = json.loads(inventory_payload.decode("utf-8"))
    grouping = json.loads(grouping_payload.decode("utf-8"))
    reader = csv.DictReader(io.StringIO(prompt_payload.decode("utf-8"), newline=""))
    rows = list(reader)

    if reader.fieldnames != list(PROMPT_MAP_FIELDS):
        raise SystemExit(f"prompt-map fields changed: {reader.fieldnames}")
    entries = inventory.get("entries", [])
    if len(entries) != EXPECTED_PROMPT_TOTAL or len(rows) != EXPECTED_PROMPT_TOTAL:
        raise SystemExit("serialized inventory/map prompt total changed")
    if grouping.get("grouping_node_count") != EXPECTED_GROUPING_TOTAL:
        raise SystemExit("serialized grouping-node total changed")
    if grouping.get("all_children_resolve") is not True:
        raise SystemExit("serialized grouping backend has unresolved children")

    if Counter(entry["partition"] for entry in entries) != Counter(
        {"nonexercise": EXPECTED_NONEXERCISE_TOTAL, "exercise": EXPECTED_EXERCISE_TOTAL}
    ):
        raise SystemExit("serialized prompt partitions differ from the authority census")
    exercise_entries = [entry for entry in entries if entry["partition"] == "exercise"]
    for ordinal, entry in enumerate(exercise_entries, start=1):
        expected_id, expected_batch, expected_batch_sequence = exercise_entry_id(
            ordinal, exercise_batches
        )
        if (
            entry["id"],
            entry["exercise_batch"],
            entry["exercise_batch_sequence"],
        ) != (expected_id, expected_batch, expected_batch_sequence):
            raise SystemExit(f"serialized exercise batching differs at ordinal {ordinal}")

    entry_ids = {entry["id"] for entry in entries}
    parent_by_child: dict[str, str] = {}
    for group in grouping.get("nodes", []):
        base.verify_locator(group["authority_locator"], documents, None, grouping=True)
        for child in group["child_entry_ids"]:
            if child not in entry_ids or child in parent_by_child:
                raise SystemExit(
                    f"serialized grouping child is missing or duplicated: {child}"
                )
            parent_by_child[child] = group["id"]

    for entry, row in zip(entries, rows, strict=True):
        locator = json.loads(row["authority_locator"])
        if locator != entry["authority_locator"]:
            raise SystemExit(f"CSV locator differs from inventory for {entry['id']}")
        base.verify_locator(locator, documents, entry["prompt_carrier"])
        expected_parent = entry["parent_group_anchor"] or ""
        if row["parent_group_anchor"] != expected_parent:
            raise SystemExit(f"CSV parent group differs for {entry['id']}")
        if parent_by_child.get(entry["id"], "") != expected_parent:
            raise SystemExit(f"grouping backend parent differs for {entry['id']}")
        expected_row = {
            "sequence": str(entry["sequence"]),
            "entry_id": entry["id"],
            "source_anchor": entry["source_anchor"],
            "source_anchor_kind": entry["source_anchor_kind"],
            "authority_source_file": entry["authority_source_file"],
            "authority_line": str(entry["authority_line"]),
            "prompt_carrier": entry["prompt_carrier"],
            "authority_locator": row["authority_locator"],
            "parent_group_anchor": expected_parent,
            "support_status": "pending",
        }
        if row != expected_row:
            raise SystemExit(f"serialized CSV row differs for {entry['id']}")

    if inventory["prompt_map"] != {
        "path": "backend/chapter_15_source_prompt_map.csv",
        **base.identity_bytes(prompt_payload),
        "fields": list(PROMPT_MAP_FIELDS),
        "row_count": EXPECTED_PROMPT_TOTAL,
    }:
        raise SystemExit("inventory prompt-map identity is inconsistent")
    if inventory["grouping_backend"] != {
        "path": "backend/chapter_15_grouping_nodes.json",
        **base.identity_bytes(grouping_payload),
        "node_count": EXPECTED_GROUPING_TOTAL,
        "all_children_resolve": True,
    }:
        raise SystemExit("inventory grouping-backend identity is inconsistent")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify that all three existing outputs exactly match regeneration",
    )
    arguments = parser.parse_args()

    inventory_payload, prompt_payload, grouping_payload, summary = build_inventory()
    payloads = {
        INVENTORY_PATH: inventory_payload,
        PROMPT_MAP_PATH: prompt_payload,
        GROUPING_PATH: grouping_payload,
    }
    if arguments.check:
        for path, expected in payloads.items():
            if not path.is_file():
                raise SystemExit(f"generated output is missing: {path}")
            actual = path.read_bytes()
            if actual != expected:
                raise SystemExit(
                    f"generated output differs from deterministic regeneration: {path}"
                )
    else:
        for path in OUTPUT_PATHS:
            path.write_bytes(payloads[path])
        for path in OUTPUT_PATHS:
            if path.read_bytes() != payloads[path]:
                raise SystemExit(f"written output failed byte-for-byte readback: {path}")

    summary["mode"] = "check" if arguments.check else "write"
    summary["authority_ordered_sha256"] = FROZEN_ORDERED_SHA256
    summary["outputs"] = {
        path.relative_to(ROOT).as_posix(): base.identity_bytes(payloads[path])
        for path in OUTPUT_PATHS
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
