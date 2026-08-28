#!/usr/bin/env python3
"""Build the deterministic occurrence-aware Chapter 16 prompt backend.

Every physical carrier retains its own frozen-authority locator.  Two repeated
leaf tasks in the thirteenth authority exercise are mapped, by exact declared
locator pairs only, to the earlier canonical source-support entries.  No text
or subtree hash is used to discover aliases.
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
CHAPTER_FILE = "chap_quotients.ptx"
EXPECTED_CHAPTER_INCLUDES = (
    "sec_quotients.ptx",
    "sec_quotient_top.ptx",
    "sec_quotient_space.ptx",
    "sec_find_quotient_space.ptx",
    "sec_quotients_summ.ptx",
    "sec_quotients_exer.ptx",
)
EXPECTED_AUTHORITY_FILE_COUNT = 7

AUTHORITY_ORDERED_HASH_CONTRACT = (
    "sha256 over each declared authority path as UTF-8, NUL, decimal byte "
    "length, NUL, raw file bytes, NUL, in chapter-closure order"
)
FROZEN_ORDERED_SHA256 = (
    "c778bea11f8afb5c389e0f6d7b1b68f95b5cad2c61a9b41665bc00cdd0dbc285"
)
AUTHORITY_SUBTREE_HASH_CONTRACT = "sha256-c14n-1.0-with-comments"
SOURCE_ANCHOR_KIND = "synthetic_locale_neutral_alias"

EXPECTED_PROMPT_OCCURRENCE_TOTAL = 54
EXPECTED_CANONICAL_ENTRY_TOTAL = 52
EXPECTED_NONEXERCISE_OCCURRENCE_TOTAL = 18
EXPECTED_EXERCISE_OCCURRENCE_TOTAL = 36
EXPECTED_NONEXERCISE_ENTRY_TOTAL = 18
EXPECTED_EXERCISE_ENTRY_TOTAL = 34
EXPECTED_ATOMIC_OCCURRENCE_TOTAL = 50
EXPECTED_DIRECT_STATEMENT_OCCURRENCE_TOTAL = 3
EXPECTED_DIRECT_BODY_OCCURRENCE_TOTAL = 1
EXPECTED_GROUPING_TOTAL = 3
EXPECTED_ALIAS_TOTAL = 2
EXERCISE_BATCH_SIZE = 10

# These are the only permitted occurrence aliases.  The mapping is declared by
# frozen file/XPath identity and is never inferred from matching prompt text or
# subtree hashes.  Each tuple is (alias occurrence, canonical occurrence).
EXACT_OCCURRENCE_ALIAS_PAIRS = (
    (
        ("source/sec_quotients_exer.ptx", "/exercises/exercise[13]/task[3]"),
        ("source/sec_quotients_exer.ptx", "/exercises/exercise[13]/task[1]"),
    ),
    (
        ("source/sec_quotients_exer.ptx", "/exercises/exercise[13]/task[4]"),
        ("source/sec_quotients_exer.ptx", "/exercises/exercise[13]/task[2]"),
    ),
)
EXACT_OCCURRENCE_ALIAS_MAP = dict(EXACT_OCCURRENCE_ALIAS_PAIRS)
EXPECTED_DIRECT_BODY_KEY = (
    "source/sec_quotient_space.ptx",
    "/section/activity[3]",
)

PROMPT_MAP_FIELDS = base.PROMPT_MAP_FIELDS
CANONICAL_PROMPT_FIELDS = base.CANONICAL_PROMPT_FIELDS
OCCURRENCE_HASH_FIELDS = (
    "sequence",
    "entry_id",
    "source_anchor",
    "source_anchor_kind",
    "authority_source_file",
    "authority_line",
    "prompt_carrier",
    "occurrence_role",
    "canonical_occurrence_sequence",
)
OCCURRENCE_ALIAS_FIELDS = (
    "alias_occurrence_sequence",
    "canonical_occurrence_sequence",
    "canonical_entry_id",
    "alias_source_anchor",
    "canonical_source_anchor",
    "alias_authority_source_file",
    "alias_authority_line",
    "alias_authority_locator",
    "canonical_authority_source_file",
    "canonical_authority_line",
    "canonical_authority_locator",
    "alias_rule",
    "exact_subtree_sha256",
)

INVENTORY_PATH = BACKEND / "chapter_16_prompt_inventory.json"
PROMPT_MAP_PATH = BACKEND / "chapter_16_source_prompt_map.csv"
GROUPING_PATH = BACKEND / "chapter_16_grouping_nodes.json"
OCCURRENCE_ALIAS_PATH = BACKEND / "chapter_16_occurrence_entry_aliases.csv"
OUTPUT_PATHS = (
    INVENTORY_PATH,
    PROMPT_MAP_PATH,
    GROUPING_PATH,
    OCCURRENCE_ALIAS_PATH,
)

PROMPT_MAP_PHASE_BOOTSTRAP = "bootstrap_support_pending"
PROMPT_MAP_PHASE_COVERED = "companion_support_covered"

XML_ID = base.XML_ID
XI_NS = base.XI_NS


def csv_payload(
    rows: list[dict[str, Any]], fields: tuple[str, ...]
) -> bytes:
    """Serialize a fixed-schema CSV with platform-independent LF endings."""
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(
        buffer,
        fieldnames=list(fields),
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def prompt_payload_with_support_status(prompt_payload: bytes, status: str) -> bytes:
    """Return the same occurrence map with one explicit support phase."""
    if status not in {"pending", "covered"}:
        raise SystemExit(f"unsupported Chapter 16 prompt-map phase status: {status}")
    reader = csv.DictReader(io.StringIO(prompt_payload.decode("utf-8"), newline=""))
    if tuple(reader.fieldnames or ()) != tuple(PROMPT_MAP_FIELDS):
        raise SystemExit("prompt-map fields changed while deriving a support phase")
    rows = list(reader)
    if len(rows) != EXPECTED_PROMPT_OCCURRENCE_TOTAL:
        raise SystemExit("prompt-map row count changed while deriving a support phase")
    for row in rows:
        row["support_status"] = status
    return csv_payload(rows, PROMPT_MAP_FIELDS)


def load_authority_closure() -> tuple[
    list[dict[str, Any]], dict[str, etree._ElementTree]
]:
    chapter_path = SOURCE_DIR / CHAPTER_FILE
    if not chapter_path.is_file():
        raise SystemExit(f"missing frozen Chapter 16 wrapper: {chapter_path}")
    chapter_doc = base.parse_xml(chapter_path)
    hrefs = tuple(
        chapter_doc.xpath("//xi:include/@href", namespaces={"xi": XI_NS})
    )
    if hrefs != EXPECTED_CHAPTER_INCLUDES:
        raise SystemExit(
            "frozen Chapter 16 XInclude order changed: "
            f"expected {EXPECTED_CHAPTER_INCLUDES}, found {hrefs}"
        )

    names = (CHAPTER_FILE, *hrefs)
    if len(names) != EXPECTED_AUTHORITY_FILE_COUNT or len(set(names)) != len(names):
        raise SystemExit("Chapter 16 authority closure is not exactly seven unique files")

    records: list[dict[str, Any]] = []
    documents: dict[str, etree._ElementTree] = {}
    for file_sequence, name in enumerate(names, start=1):
        if Path(name).name != name:
            raise SystemExit(f"nonlocal Chapter 16 include is forbidden: {name}")
        path = SOURCE_DIR / name
        if not path.is_file():
            raise SystemExit(f"missing frozen Chapter 16 authority file: {path}")
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
            "frozen Chapter 16 ordered authority hash changed: "
            f"expected {FROZEN_ORDERED_SHA256}, found {actual_ordered_hash}"
        )
    return records, documents


def derive_exercise_batches(exercise_total: int) -> tuple[tuple[str, int], ...]:
    """Partition canonical exercise entries into bounded sequential batches."""
    if exercise_total <= 0:
        raise SystemExit("Chapter 16 authority has no canonical exercise entries")
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
        raise SystemExit("derived exercise batches do not cover the canonical census")
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
            return f"o003-c90-ch16-exer-{letter}-{cursor:02d}", letter, cursor
        cursor -= count
    raise SystemExit(f"exercise entry ordinal exceeds derived batches: {ordinal}")


def occurrence_mapping_hash(occurrences: list[dict[str, Any]]) -> str:
    projection = [
        {field: occurrence[field] for field in OCCURRENCE_HASH_FIELDS}
        for occurrence in occurrences
    ]
    payload = json.dumps(
        projection,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return base.digest_bytes(payload)


def element_bytes(element: etree._Element) -> bytes:
    """Serialize one parsed authority subtree without its following tail."""
    return etree.tostring(element, encoding="utf-8", with_tail=False)


def build_inventory() -> tuple[bytes, bytes, bytes, bytes, dict[str, Any]]:
    if base.FROZEN_AUTHORITY_COMMIT != FROZEN_AUTHORITY_COMMIT:
        raise SystemExit("shared locator implementation has a different authority commit")
    if base.AUTHORITY_SUBTREE_HASH_CONTRACT != AUTHORITY_SUBTREE_HASH_CONTRACT:
        raise SystemExit("shared locator implementation has a different subtree contract")
    if len(EXACT_OCCURRENCE_ALIAS_MAP) != EXPECTED_ALIAS_TOTAL:
        raise SystemExit("declared Chapter 16 alias keys are missing or duplicated")
    declared_alias_keys = {
        key for pair in EXACT_OCCURRENCE_ALIAS_PAIRS for key in pair
    }
    if len(declared_alias_keys) != EXPECTED_ALIAS_TOTAL * 2:
        raise SystemExit("declared Chapter 16 alias-pair locators are not disjoint")

    authority_records, documents = load_authority_closure()
    events = base.discover_events(authority_records, documents)
    group_events = [event for event in events if event["event_kind"] == "grouping"]
    prompt_events = [event for event in events if event["event_kind"] == "prompt"]

    if len(group_events) != EXPECTED_GROUPING_TOTAL:
        raise SystemExit(
            f"expected {EXPECTED_GROUPING_TOTAL} grouping-only tasks, "
            f"found {len(group_events)}"
        )
    if len(prompt_events) != EXPECTED_PROMPT_OCCURRENCE_TOTAL:
        raise SystemExit(
            f"expected {EXPECTED_PROMPT_OCCURRENCE_TOTAL} physical prompt occurrences, "
            f"found {len(prompt_events)}"
        )

    occurrence_partitions = Counter(event["partition"] for event in prompt_events)
    if occurrence_partitions != Counter(
        {
            "nonexercise": EXPECTED_NONEXERCISE_OCCURRENCE_TOTAL,
            "exercise": EXPECTED_EXERCISE_OCCURRENCE_TOTAL,
        }
    ):
        raise SystemExit(
            "physical prompt partition census changed: "
            f"{dict(sorted(occurrence_partitions.items()))}"
        )
    occurrence_carriers = Counter(
        event["prompt_carrier"] for event in prompt_events
    )
    if occurrence_carriers != Counter(
        {
            "atomic_task": EXPECTED_ATOMIC_OCCURRENCE_TOTAL,
            "direct_statement": EXPECTED_DIRECT_STATEMENT_OCCURRENCE_TOTAL,
            "direct_body": EXPECTED_DIRECT_BODY_OCCURRENCE_TOTAL,
        }
    ):
        raise SystemExit(
            "physical prompt carrier census changed: "
            f"{dict(sorted(occurrence_carriers.items()))}"
        )

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
            f"o003-gvsu-ch16-{context}-group-{alias_counters[counter_key]:02d}"
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

    exercise_batches = derive_exercise_batches(EXPECTED_EXERCISE_ENTRY_TOTAL)
    entries: list[dict[str, Any]] = []
    occurrences: list[dict[str, Any]] = []
    alias_rows: list[dict[str, Any]] = []
    canonical_entry_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    canonical_occurrence_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    occurrence_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    prompt_alias_counters: Counter[tuple[str, str]] = Counter()
    group_keys = set(group_records_by_key)
    nonexercise_occurrence_ordinal = 0
    exercise_occurrence_ordinal = 0
    nonexercise_entry_ordinal = 0
    exercise_entry_ordinal = 0

    for occurrence_sequence, event in enumerate(prompt_events, start=1):
        element = event["element"]
        partition = event["partition"]
        if partition == "exercise":
            exercise_occurrence_ordinal += 1
            partition_occurrence_sequence = exercise_occurrence_ordinal
        else:
            nonexercise_occurrence_ordinal += 1
            partition_occurrence_sequence = nonexercise_occurrence_ordinal

        context = base.alias_context(base.nearest_real_xml_id(element))
        label = base.alias_label(event["prompt_carrier"])
        counter_key = (context, label)
        prompt_alias_counters[counter_key] += 1
        source_anchor = (
            f"o003-gvsu-ch16-{context}-{label}-"
            f"{prompt_alias_counters[counter_key]:02d}"
        )
        locator = base.make_locator(event["source_file"], event["document"], element)
        key = (event["source_file"], locator["xpath"])
        if key in occurrence_by_key:
            raise SystemExit(f"duplicate physical prompt locator: {key}")
        parent_key = base.nearest_group_key(
            event["source_file"], event["document"], element, group_keys
        )
        parent_group_anchor = (
            group_records_by_key[parent_key]["id"] if parent_key is not None else None
        )

        canonical_key = EXACT_OCCURRENCE_ALIAS_MAP.get(key)
        if canonical_key is None:
            if partition == "exercise":
                exercise_entry_ordinal += 1
                entry_id, batch, batch_sequence = exercise_entry_id(
                    exercise_entry_ordinal, exercise_batches
                )
                partition_entry_sequence = exercise_entry_ordinal
            else:
                nonexercise_entry_ordinal += 1
                entry_id = f"o003-c90-ch16-guide-{nonexercise_entry_ordinal:02d}"
                batch = None
                batch_sequence = None
                partition_entry_sequence = nonexercise_entry_ordinal

            entry = {
                "sequence": len(entries) + 1,
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
                "partition_sequence": partition_entry_sequence,
                "exercise_batch": batch,
                "exercise_batch_sequence": batch_sequence,
                "canonical_occurrence_sequence": occurrence_sequence,
                "source_occurrence_count": 0,
                "source_occurrence_sequences": [],
                "source_occurrence_anchors": [],
            }
            entries.append(entry)
            canonical_entry_by_key[key] = entry
            occurrence_role = "canonical"
        else:
            if canonical_key not in canonical_entry_by_key:
                raise SystemExit(
                    "declared alias does not follow its canonical occurrence: "
                    f"{key} -> {canonical_key}"
                )
            entry = canonical_entry_by_key[canonical_key]
            canonical_occurrence = canonical_occurrence_by_key[canonical_key]
            if partition != entry["partition"]:
                raise SystemExit(f"declared alias changes partition: {key}")
            if event["prompt_carrier"] != entry["prompt_carrier"]:
                raise SystemExit(f"declared alias changes carrier kind: {key}")
            if parent_group_anchor != entry["parent_group_anchor"]:
                raise SystemExit(f"declared alias changes grouping parent: {key}")
            canonical_element = documents[canonical_key[0]].xpath(canonical_key[1])
            if len(canonical_element) != 1:
                raise SystemExit(
                    f"declared canonical alias locator is not unique: {canonical_key}"
                )
            canonical_locator = entry["authority_locator"]
            if element_bytes(element) != element_bytes(canonical_element[0]):
                raise SystemExit(
                    "declared Chapter 16 alias pair is not byte-identical after "
                    f"isolated subtree serialization: {key} -> {canonical_key}"
                )
            if locator["subtree_sha256"] != canonical_locator["subtree_sha256"]:
                raise SystemExit(
                    f"declared Chapter 16 alias pair has different C14N hashes: {key}"
                )
            alias_rows.append(
                {
                    "alias_occurrence_sequence": occurrence_sequence,
                    "canonical_occurrence_sequence": canonical_occurrence["sequence"],
                    "canonical_entry_id": entry["id"],
                    "alias_source_anchor": source_anchor,
                    "canonical_source_anchor": entry["source_anchor"],
                    "alias_authority_source_file": event["source_file"],
                    "alias_authority_line": locator["authority_line"],
                    "alias_authority_locator": json.dumps(
                        locator, ensure_ascii=False, separators=(",", ":")
                    ),
                    "canonical_authority_source_file": entry[
                        "authority_source_file"
                    ],
                    "canonical_authority_line": entry["authority_line"],
                    "canonical_authority_locator": json.dumps(
                        canonical_locator, ensure_ascii=False, separators=(",", ":")
                    ),
                    "alias_rule": "hard_coded_exact_subtree_pair",
                    "exact_subtree_sha256": locator["subtree_sha256"],
                }
            )
            occurrence_role = "explicit_alias"

        occurrence = {
            "sequence": occurrence_sequence,
            "entry_id": entry["id"],
            "entry_sequence": entry["sequence"],
            "occurrence_role": occurrence_role,
            "canonical_occurrence_sequence": entry["canonical_occurrence_sequence"],
            "canonical_source_anchor": entry["source_anchor"],
            "source_anchor": source_anchor,
            "source_anchor_kind": SOURCE_ANCHOR_KIND,
            "authority_source_file": event["source_file"],
            "authority_line": locator["authority_line"],
            "prompt_carrier": event["prompt_carrier"],
            "authority_locator": locator,
            "parent_group_anchor": parent_group_anchor,
            "support_status": "pending",
            "partition": partition,
            "partition_sequence": partition_occurrence_sequence,
        }
        occurrences.append(occurrence)
        occurrence_by_key[key] = occurrence
        if occurrence_role == "canonical":
            canonical_occurrence_by_key[key] = occurrence
            if parent_key is not None:
                group_records_by_key[parent_key]["child_entry_ids"].append(entry["id"])
        entry["source_occurrence_count"] += 1
        entry["source_occurrence_sequences"].append(occurrence_sequence)
        entry["source_occurrence_anchors"].append(source_anchor)

    if set(occurrence_by_key) != {
        (event["source_file"], event["document"].getpath(event["element"]))
        for event in prompt_events
    }:
        raise SystemExit("physical prompt locator inventory is incomplete")
    if not declared_alias_keys.issubset(set(occurrence_by_key)):
        raise SystemExit("one or more declared Chapter 16 alias locators were not found")
    if set(EXACT_OCCURRENCE_ALIAS_MAP) != {
        key
        for key, occurrence in occurrence_by_key.items()
        if occurrence["occurrence_role"] == "explicit_alias"
    }:
        raise SystemExit("generated aliases differ from the two exact declared pairs")

    direct_body_occurrences = [
        occurrence
        for occurrence in occurrences
        if occurrence["prompt_carrier"] == "direct_body"
    ]
    if len(direct_body_occurrences) != 1:
        raise SystemExit("Chapter 16 must have exactly one direct-body occurrence")
    direct_body = direct_body_occurrences[0]
    if (
        direct_body["authority_source_file"],
        direct_body["authority_locator"]["xpath"],
    ) != EXPECTED_DIRECT_BODY_KEY:
        raise SystemExit("the direct-body occurrence is not activity act_quotient_er")
    if direct_body["authority_locator"]["nearest_ancestor_or_self_xml_id"] != (
        "act_quotient_er"
    ):
        raise SystemExit("the direct-body occurrence lost xml:id act_quotient_er")

    if len(entries) != EXPECTED_CANONICAL_ENTRY_TOTAL:
        raise SystemExit(
            f"expected {EXPECTED_CANONICAL_ENTRY_TOTAL} canonical entries, "
            f"found {len(entries)}"
        )
    if nonexercise_entry_ordinal != EXPECTED_NONEXERCISE_ENTRY_TOTAL:
        raise SystemExit("canonical nonexercise entry census changed")
    if exercise_entry_ordinal != EXPECTED_EXERCISE_ENTRY_TOTAL:
        raise SystemExit("canonical exercise entry census changed")
    if nonexercise_occurrence_ordinal != EXPECTED_NONEXERCISE_OCCURRENCE_TOTAL:
        raise SystemExit("nonexercise occurrence census changed during generation")
    if exercise_occurrence_ordinal != EXPECTED_EXERCISE_OCCURRENCE_TOTAL:
        raise SystemExit("exercise occurrence census changed during generation")
    if len(alias_rows) != EXPECTED_ALIAS_TOTAL:
        raise SystemExit("generated alias-row count differs from the declared pairs")

    entry_ids = [entry["id"] for entry in entries]
    canonical_source_anchors = [entry["source_anchor"] for entry in entries]
    occurrence_source_anchors = [
        occurrence["source_anchor"] for occurrence in occurrences
    ]
    occurrence_locators = [
        (
            occurrence["authority_source_file"],
            occurrence["authority_locator"]["xpath"],
        )
        for occurrence in occurrences
    ]
    if len(set(entry_ids)) != EXPECTED_CANONICAL_ENTRY_TOTAL:
        raise SystemExit("generated Chapter 16 canonical entry IDs are not unique")
    if len(set(canonical_source_anchors)) != EXPECTED_CANONICAL_ENTRY_TOTAL:
        raise SystemExit("generated Chapter 16 canonical source aliases are not unique")
    if len(set(occurrence_source_anchors)) != EXPECTED_PROMPT_OCCURRENCE_TOTAL:
        raise SystemExit("generated Chapter 16 occurrence source aliases are not unique")
    if len(set(occurrence_locators)) != EXPECTED_PROMPT_OCCURRENCE_TOTAL:
        raise SystemExit("generated Chapter 16 occurrence locators are not unique")
    if [entry["sequence"] for entry in entries] != list(
        range(1, EXPECTED_CANONICAL_ENTRY_TOTAL + 1)
    ):
        raise SystemExit("canonical entries are not in exact order 1..52")
    if [occurrence["sequence"] for occurrence in occurrences] != list(
        range(1, EXPECTED_PROMPT_OCCURRENCE_TOTAL + 1)
    ):
        raise SystemExit("physical occurrences are not in exact order 1..54")
    if any(entry["support_status"] != "pending" for entry in entries):
        raise SystemExit("bootstrap support status must be pending for every entry")
    if any(occurrence["support_status"] != "pending" for occurrence in occurrences):
        raise SystemExit("bootstrap support status must be pending for every occurrence")
    if sum(entry["source_occurrence_count"] for entry in entries) != (
        EXPECTED_PROMPT_OCCURRENCE_TOTAL
    ):
        raise SystemExit("canonical entry occurrence counts do not cover all locators")
    if Counter(entry["source_occurrence_count"] for entry in entries) != Counter(
        {1: 50, 2: 2}
    ):
        raise SystemExit("canonical entry occurrence multiplicities changed")

    duplicate_entry_occurrences = {
        entry_id: count
        for entry_id, count in Counter(
            occurrence["entry_id"] for occurrence in occurrences
        ).items()
        if count > 1
    }
    expected_duplicate_entry_ids = {
        canonical_entry_by_key[canonical_key]["id"]: 2
        for _, canonical_key in EXACT_OCCURRENCE_ALIAS_PAIRS
    }
    if duplicate_entry_occurrences != expected_duplicate_entry_ids:
        raise SystemExit("only the two declared canonical entries may occur twice")

    grouped_children = [
        child for group in grouping_nodes for child in group["child_entry_ids"]
    ]
    entries_with_parent = [
        entry["id"] for entry in entries if entry["parent_group_anchor"] is not None
    ]
    if not all(group["child_entry_ids"] for group in grouping_nodes):
        raise SystemExit("a grouping-only task has no mapped child prompts")
    if len(grouped_children) != len(set(grouped_children)):
        raise SystemExit("a canonical child is assigned to more than one grouping node")
    if grouped_children != entries_with_parent:
        raise SystemExit("grouping children and canonical parent links are not one-to-one")
    if not set(grouped_children).issubset(set(entry_ids)):
        raise SystemExit("one or more grouping children do not resolve")

    prompt_rows: list[dict[str, Any]] = []
    for occurrence in occurrences:
        prompt_rows.append(
            {
                "sequence": occurrence["sequence"],
                "entry_id": occurrence["entry_id"],
                "source_anchor": occurrence["source_anchor"],
                "source_anchor_kind": occurrence["source_anchor_kind"],
                "authority_source_file": occurrence["authority_source_file"],
                "authority_line": occurrence["authority_line"],
                "prompt_carrier": occurrence["prompt_carrier"],
                "authority_locator": json.dumps(
                    occurrence["authority_locator"],
                    ensure_ascii=False,
                    separators=(",", ":"),
                ),
                "parent_group_anchor": occurrence["parent_group_anchor"] or "",
                "support_status": occurrence["support_status"],
            }
        )

    prompt_payload = csv_payload(prompt_rows, PROMPT_MAP_FIELDS)
    covered_prompt_payload = prompt_payload_with_support_status(prompt_payload, "covered")
    alias_payload = csv_payload(alias_rows, OCCURRENCE_ALIAS_FIELDS)
    grouping_payload = {
        "schema_version": 1,
        "unit": "o003-c90-ch16-quotient-spaces",
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
        file_occurrences = [
            occurrence
            for occurrence in occurrences
            if occurrence["authority_source_file"] == source_file
        ]
        file_entries = [
            entry
            for entry in entries
            if entry["authority_source_file"] == source_file
        ]
        file_groups = [
            group
            for group in grouping_nodes
            if group["authority_source_file"] == source_file
        ]
        occurrence_carrier_counts = Counter(
            occurrence["prompt_carrier"] for occurrence in file_occurrences
        )
        file_census.append(
            {
                "authority_source_file": source_file,
                "prompt_occurrence_total": len(file_occurrences),
                "canonical_entry_total": len(file_entries),
                "nonexercise_prompt_occurrence_total": sum(
                    occurrence["partition"] == "nonexercise"
                    for occurrence in file_occurrences
                ),
                "exercise_prompt_occurrence_total": sum(
                    occurrence["partition"] == "exercise"
                    for occurrence in file_occurrences
                ),
                "nonexercise_canonical_entry_total": sum(
                    entry["partition"] == "nonexercise" for entry in file_entries
                ),
                "exercise_canonical_entry_total": sum(
                    entry["partition"] == "exercise" for entry in file_entries
                ),
                "atomic_task_occurrence_total": occurrence_carrier_counts[
                    "atomic_task"
                ],
                "direct_statement_occurrence_total": occurrence_carrier_counts[
                    "direct_statement"
                ],
                "direct_body_occurrence_total": occurrence_carrier_counts[
                    "direct_body"
                ],
                "explicit_alias_occurrence_total": sum(
                    occurrence["occurrence_role"] == "explicit_alias"
                    for occurrence in file_occurrences
                ),
                "grouping_node_total": len(file_groups),
            }
        )

    canonical_carriers = Counter(entry["prompt_carrier"] for entry in entries)
    canonical_mapping_sha256 = base.canonical_prompt_hash(entries)
    occurrence_mapping_sha256 = occurrence_mapping_hash(occurrences)
    alias_contract_pairs = [
        {
            "alias": {
                "authority_source_file": alias_key[0],
                "xpath": alias_key[1],
            },
            "canonical": {
                "authority_source_file": canonical_key[0],
                "xpath": canonical_key[1],
            },
        }
        for alias_key, canonical_key in EXACT_OCCURRENCE_ALIAS_PAIRS
    ]
    inventory_payload = {
        "schema_version": 2,
        "status": "prompt_inventory_complete_companion_pending",
        "partial": False,
        "lane_id": "O003/C90",
        "locale": "id-ID",
        "unit": {
            "id": "o003-c90-ch16-quotient-spaces",
            "sequence": 16,
            "source_chapter_xml_id": "chap_quotients",
        },
        "authority": {
            "commit": FROZEN_AUTHORITY_COMMIT,
            "root": f"authority/gvsu-pinned/topology-{FROZEN_AUTHORITY_COMMIT}",
            "source_file_count": len(authority_records),
            "ordered_hash_contract": AUTHORITY_ORDERED_HASH_CONTRACT,
            "ordered_sha256": FROZEN_ORDERED_SHA256,
            "canonical_prompt_mapping_sha256": canonical_mapping_sha256,
            "occurrence_prompt_mapping_sha256": occurrence_mapping_sha256,
            "occurrence_prompt_mapping_fields": list(OCCURRENCE_HASH_FIELDS),
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
                "not a prompt occurrence"
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
                "o003-gvsu-ch16-{nearest-real-xml-id}-{task|statement|body|group}-NN"
            ),
            "sequence_scope": "nearest real xml:id plus carrier label, in authority order",
            "translated_titles_used": False,
        },
        "occurrence_entry_contract": {
            "physical_occurrence_count": len(occurrences),
            "canonical_source_support_entry_count": len(entries),
            "every_physical_locator_preserved": True,
            "generic_text_deduplication_used": False,
            "alias_method": "two hard-coded exact frozen file/XPath pairs",
            "exact_alias_pair_count": len(EXACT_OCCURRENCE_ALIAS_PAIRS),
            "exact_alias_pairs": alias_contract_pairs,
            "canonical_entry_selection": "first occurrence in authority order",
        },
        "entry_id_contract": {
            "nonexercise": {
                "format": "o003-c90-ch16-guide-NN",
                "canonical_entry_count": nonexercise_entry_ordinal,
                "physical_occurrence_count": nonexercise_occurrence_ordinal,
                "first": entries[0]["id"],
                "last": next(
                    entry["id"]
                    for entry in reversed(entries)
                    if entry["partition"] == "nonexercise"
                ),
            },
            "exercise": {
                "format": "o003-c90-ch16-exer-{batch}-{NN}",
                "canonical_entry_count": exercise_entry_ordinal,
                "physical_occurrence_count": exercise_occurrence_ordinal,
                "batch_derivation": (
                    "exact authority-order canonical exercise-entry census partitioned "
                    f"into sequential batches of at most {EXERCISE_BATCH_SIZE}"
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
            "physical_prompt_occurrence_total": len(occurrences),
            "unique_source_locator_total": len(set(occurrence_locators)),
            "source_prompt_total": len(entries),
            "canonical_source_support_entry_total": len(entries),
            "nonexercise_prompt_occurrence_total": nonexercise_occurrence_ordinal,
            "exercise_prompt_occurrence_total": exercise_occurrence_ordinal,
            "nonexercise_prompt_total": nonexercise_entry_ordinal,
            "exercise_prompt_total": exercise_entry_ordinal,
            "atomic_prompt_occurrence_total": occurrence_carriers["atomic_task"],
            "direct_statement_prompt_occurrence_total": occurrence_carriers[
                "direct_statement"
            ],
            "direct_body_prompt_occurrence_total": occurrence_carriers[
                "direct_body"
            ],
            "direct_prompt_occurrence_total": (
                occurrence_carriers["direct_statement"]
                + occurrence_carriers["direct_body"]
            ),
            "atomic_prompt_total": canonical_carriers["atomic_task"],
            "direct_statement_prompt_total": canonical_carriers["direct_statement"],
            "direct_body_prompt_total": canonical_carriers["direct_body"],
            "direct_prompt_total": (
                canonical_carriers["direct_statement"]
                + canonical_carriers["direct_body"]
            ),
            "explicit_alias_occurrence_total": len(alias_rows),
            "grouping_node_total": len(grouping_nodes),
            "grouped_child_prompt_total": len(grouped_children),
            "pending_support_total": len(entries),
            "covered_support_total": 0,
            "by_source_file": file_census,
        },
        "prompt_map": {
            "path": "backend/chapter_16_source_prompt_map.csv",
            "fields": list(PROMPT_MAP_FIELDS),
            "row_semantics": "one row per physical prompt occurrence",
            "row_count": len(prompt_rows),
            "unique_entry_id_count": len(set(row["entry_id"] for row in prompt_rows)),
            "phase_contract": {
                PROMPT_MAP_PHASE_BOOTSTRAP: {
                    "support_status": "pending",
                    **base.identity_bytes(prompt_payload),
                },
                PROMPT_MAP_PHASE_COVERED: {
                    "support_status": "covered",
                    **base.identity_bytes(covered_prompt_payload),
                },
            },
        },
        "occurrence_entry_aliases": {
            "path": "backend/chapter_16_occurrence_entry_aliases.csv",
            **base.identity_bytes(alias_payload),
            "fields": list(OCCURRENCE_ALIAS_FIELDS),
            "row_count": len(alias_rows),
            "generic_text_deduplication_used": False,
        },
        "grouping_backend": {
            "path": "backend/chapter_16_grouping_nodes.json",
            **base.identity_bytes(grouping_bytes_payload),
            "node_count": len(grouping_nodes),
            "all_children_resolve": True,
        },
        "entries": entries,
        "occurrences": occurrences,
    }
    inventory_bytes_payload = base.json_bytes(inventory_payload)

    verify_payloads(
        inventory_bytes_payload,
        prompt_payload,
        grouping_bytes_payload,
        alias_payload,
        documents,
        exercise_batches,
    )
    summary = {
        "status": inventory_payload["status"],
        "physical_prompt_occurrences": len(occurrences),
        "canonical_source_support_entries": len(entries),
        "nonexercise_occurrences": nonexercise_occurrence_ordinal,
        "exercise_occurrences": exercise_occurrence_ordinal,
        "nonexercise_entries": nonexercise_entry_ordinal,
        "exercise_entries": exercise_entry_ordinal,
        "exercise_batches": [
            {"letter": letter, "count": count} for letter, count in exercise_batches
        ],
        "explicit_alias_pairs": len(alias_rows),
        "grouping_nodes": len(grouping_nodes),
        "occurrence_carrier_counts": dict(sorted(occurrence_carriers.items())),
        "canonical_carrier_counts": dict(sorted(canonical_carriers.items())),
        "canonical_prompt_mapping_sha256": canonical_mapping_sha256,
        "occurrence_prompt_mapping_sha256": occurrence_mapping_sha256,
    }
    return (
        inventory_bytes_payload,
        prompt_payload,
        grouping_bytes_payload,
        alias_payload,
        summary,
    )


def verify_payloads(
    inventory_payload: bytes,
    prompt_payload: bytes,
    grouping_payload: bytes,
    alias_payload: bytes,
    documents: dict[str, etree._ElementTree],
    exercise_batches: tuple[tuple[str, int], ...],
) -> None:
    inventory = json.loads(inventory_payload.decode("utf-8"))
    grouping = json.loads(grouping_payload.decode("utf-8"))
    prompt_reader = csv.DictReader(
        io.StringIO(prompt_payload.decode("utf-8"), newline="")
    )
    prompt_rows = list(prompt_reader)
    alias_reader = csv.DictReader(
        io.StringIO(alias_payload.decode("utf-8"), newline="")
    )
    alias_rows = list(alias_reader)

    if prompt_reader.fieldnames != list(PROMPT_MAP_FIELDS):
        raise SystemExit(f"prompt-map fields changed: {prompt_reader.fieldnames}")
    if alias_reader.fieldnames != list(OCCURRENCE_ALIAS_FIELDS):
        raise SystemExit(f"occurrence-alias fields changed: {alias_reader.fieldnames}")
    entries = inventory.get("entries", [])
    occurrences = inventory.get("occurrences", [])
    if len(entries) != EXPECTED_CANONICAL_ENTRY_TOTAL:
        raise SystemExit("serialized canonical entry total changed")
    if (
        len(occurrences) != EXPECTED_PROMPT_OCCURRENCE_TOTAL
        or len(prompt_rows) != EXPECTED_PROMPT_OCCURRENCE_TOTAL
    ):
        raise SystemExit("serialized occurrence/map total changed")
    if len(alias_rows) != EXPECTED_ALIAS_TOTAL:
        raise SystemExit("serialized occurrence-alias total changed")
    if grouping.get("grouping_node_count") != EXPECTED_GROUPING_TOTAL:
        raise SystemExit("serialized grouping-node total changed")
    if grouping.get("all_children_resolve") is not True:
        raise SystemExit("serialized grouping backend has unresolved children")

    if Counter(entry["partition"] for entry in entries) != Counter(
        {
            "nonexercise": EXPECTED_NONEXERCISE_ENTRY_TOTAL,
            "exercise": EXPECTED_EXERCISE_ENTRY_TOTAL,
        }
    ):
        raise SystemExit("serialized canonical entry partitions changed")
    if Counter(occurrence["partition"] for occurrence in occurrences) != Counter(
        {
            "nonexercise": EXPECTED_NONEXERCISE_OCCURRENCE_TOTAL,
            "exercise": EXPECTED_EXERCISE_OCCURRENCE_TOTAL,
        }
    ):
        raise SystemExit("serialized physical occurrence partitions changed")

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

    entry_by_id = {entry["id"]: entry for entry in entries}
    if len(entry_by_id) != EXPECTED_CANONICAL_ENTRY_TOTAL:
        raise SystemExit("serialized canonical entry IDs are duplicated")
    occurrence_by_sequence = {
        occurrence["sequence"]: occurrence for occurrence in occurrences
    }
    if len(occurrence_by_sequence) != EXPECTED_PROMPT_OCCURRENCE_TOTAL:
        raise SystemExit("serialized occurrence sequences are duplicated")

    parent_by_child: dict[str, str] = {}
    for group in grouping.get("nodes", []):
        base.verify_locator(group["authority_locator"], documents, None, grouping=True)
        for child in group["child_entry_ids"]:
            if child not in entry_by_id or child in parent_by_child:
                raise SystemExit(
                    f"serialized grouping child is missing or duplicated: {child}"
                )
            parent_by_child[child] = group["id"]

    for entry in entries:
        base.verify_locator(
            entry["authority_locator"], documents, entry["prompt_carrier"]
        )
        expected_parent = entry["parent_group_anchor"] or ""
        if parent_by_child.get(entry["id"], "") != expected_parent:
            raise SystemExit(f"grouping backend parent differs for {entry['id']}")
        source_sequences = entry["source_occurrence_sequences"]
        source_anchors = entry["source_occurrence_anchors"]
        if entry["source_occurrence_count"] != len(source_sequences):
            raise SystemExit(f"entry occurrence count differs for {entry['id']}")
        if len(source_sequences) != len(source_anchors):
            raise SystemExit(f"entry occurrence anchors differ for {entry['id']}")
        for sequence, anchor in zip(source_sequences, source_anchors, strict=True):
            occurrence = occurrence_by_sequence.get(sequence)
            if occurrence is None or occurrence["entry_id"] != entry["id"]:
                raise SystemExit(f"entry occurrence does not resolve for {entry['id']}")
            if occurrence["source_anchor"] != anchor:
                raise SystemExit(f"entry occurrence anchor does not resolve for {entry['id']}")

    actual_alias_keys: set[tuple[str, str]] = set()
    for occurrence, row in zip(occurrences, prompt_rows, strict=True):
        if occurrence["entry_id"] not in entry_by_id:
            raise SystemExit("occurrence points to an unknown canonical entry")
        entry = entry_by_id[occurrence["entry_id"]]
        if occurrence["entry_sequence"] != entry["sequence"]:
            raise SystemExit("occurrence canonical entry sequence changed")
        if occurrence["canonical_occurrence_sequence"] != entry[
            "canonical_occurrence_sequence"
        ]:
            raise SystemExit("occurrence canonical-occurrence link changed")
        if occurrence["canonical_source_anchor"] != entry["source_anchor"]:
            raise SystemExit("occurrence canonical-source-anchor link changed")
        if occurrence["partition"] != entry["partition"]:
            raise SystemExit("occurrence and canonical entry partitions differ")
        if occurrence["prompt_carrier"] != entry["prompt_carrier"]:
            raise SystemExit("occurrence and canonical entry carrier kinds differ")

        locator = json.loads(row["authority_locator"])
        if locator != occurrence["authority_locator"]:
            raise SystemExit(
                f"CSV locator differs from occurrence {occurrence['sequence']}"
            )
        base.verify_locator(locator, documents, occurrence["prompt_carrier"])
        expected_parent = occurrence["parent_group_anchor"] or ""
        if row["parent_group_anchor"] != expected_parent:
            raise SystemExit("CSV occurrence parent group changed")
        if parent_by_child.get(occurrence["entry_id"], "") != expected_parent:
            raise SystemExit("grouping backend occurrence parent changed")
        expected_row = {
            "sequence": str(occurrence["sequence"]),
            "entry_id": occurrence["entry_id"],
            "source_anchor": occurrence["source_anchor"],
            "source_anchor_kind": occurrence["source_anchor_kind"],
            "authority_source_file": occurrence["authority_source_file"],
            "authority_line": str(occurrence["authority_line"]),
            "prompt_carrier": occurrence["prompt_carrier"],
            "authority_locator": row["authority_locator"],
            "parent_group_anchor": expected_parent,
            "support_status": "pending",
        }
        if row != expected_row:
            raise SystemExit(
                f"serialized CSV row differs for occurrence {occurrence['sequence']}"
            )
        key = (
            occurrence["authority_source_file"],
            occurrence["authority_locator"]["xpath"],
        )
        if occurrence["occurrence_role"] == "explicit_alias":
            actual_alias_keys.add(key)
        elif occurrence["occurrence_role"] != "canonical":
            raise SystemExit("serialized occurrence has an unknown role")

    if actual_alias_keys != set(EXACT_OCCURRENCE_ALIAS_MAP):
        raise SystemExit("serialized explicit aliases differ from the exact pair keys")

    for row, (alias_key, canonical_key) in zip(
        alias_rows, EXACT_OCCURRENCE_ALIAS_PAIRS, strict=True
    ):
        alias_sequence = int(row["alias_occurrence_sequence"])
        canonical_sequence = int(row["canonical_occurrence_sequence"])
        alias_occurrence = occurrence_by_sequence.get(alias_sequence)
        canonical_occurrence = occurrence_by_sequence.get(canonical_sequence)
        if alias_occurrence is None or canonical_occurrence is None:
            raise SystemExit("occurrence-alias CSV contains an unknown sequence")
        if (
            alias_occurrence["authority_source_file"],
            alias_occurrence["authority_locator"]["xpath"],
        ) != alias_key:
            raise SystemExit("occurrence-alias CSV alias locator changed")
        if (
            canonical_occurrence["authority_source_file"],
            canonical_occurrence["authority_locator"]["xpath"],
        ) != canonical_key:
            raise SystemExit("occurrence-alias CSV canonical locator changed")
        if alias_occurrence["entry_id"] != canonical_occurrence["entry_id"]:
            raise SystemExit("declared alias occurrences do not share an entry ID")
        expected_alias_row = {
            "alias_occurrence_sequence": str(alias_occurrence["sequence"]),
            "canonical_occurrence_sequence": str(canonical_occurrence["sequence"]),
            "canonical_entry_id": canonical_occurrence["entry_id"],
            "alias_source_anchor": alias_occurrence["source_anchor"],
            "canonical_source_anchor": canonical_occurrence["source_anchor"],
            "alias_authority_source_file": alias_occurrence[
                "authority_source_file"
            ],
            "alias_authority_line": str(alias_occurrence["authority_line"]),
            "alias_authority_locator": row["alias_authority_locator"],
            "canonical_authority_source_file": canonical_occurrence[
                "authority_source_file"
            ],
            "canonical_authority_line": str(canonical_occurrence["authority_line"]),
            "canonical_authority_locator": row["canonical_authority_locator"],
            "alias_rule": "hard_coded_exact_subtree_pair",
            "exact_subtree_sha256": alias_occurrence["authority_locator"][
                "subtree_sha256"
            ],
        }
        if row != expected_alias_row:
            raise SystemExit("serialized occurrence-alias row changed")
        if json.loads(row["alias_authority_locator"]) != alias_occurrence[
            "authority_locator"
        ]:
            raise SystemExit("alias CSV structured alias locator changed")
        if json.loads(row["canonical_authority_locator"]) != canonical_occurrence[
            "authority_locator"
        ]:
            raise SystemExit("alias CSV structured canonical locator changed")
        alias_elements = documents[alias_key[0]].xpath(alias_key[1])
        canonical_elements = documents[canonical_key[0]].xpath(canonical_key[1])
        if len(alias_elements) != 1 or len(canonical_elements) != 1:
            raise SystemExit("declared alias locator no longer resolves uniquely")
        if element_bytes(alias_elements[0]) != element_bytes(canonical_elements[0]):
            raise SystemExit("declared serialized alias subtrees are no longer identical")

    covered_prompt_payload = prompt_payload_with_support_status(prompt_payload, "covered")
    if inventory["prompt_map"] != {
        "path": "backend/chapter_16_source_prompt_map.csv",
        "fields": list(PROMPT_MAP_FIELDS),
        "row_semantics": "one row per physical prompt occurrence",
        "row_count": EXPECTED_PROMPT_OCCURRENCE_TOTAL,
        "unique_entry_id_count": EXPECTED_CANONICAL_ENTRY_TOTAL,
        "phase_contract": {
            PROMPT_MAP_PHASE_BOOTSTRAP: {
                "support_status": "pending",
                **base.identity_bytes(prompt_payload),
            },
            PROMPT_MAP_PHASE_COVERED: {
                "support_status": "covered",
                **base.identity_bytes(covered_prompt_payload),
            },
        },
    }:
        raise SystemExit("inventory prompt-map identity is inconsistent")
    if inventory["occurrence_entry_aliases"] != {
        "path": "backend/chapter_16_occurrence_entry_aliases.csv",
        **base.identity_bytes(alias_payload),
        "fields": list(OCCURRENCE_ALIAS_FIELDS),
        "row_count": EXPECTED_ALIAS_TOTAL,
        "generic_text_deduplication_used": False,
    }:
        raise SystemExit("inventory occurrence-alias identity is inconsistent")
    if inventory["grouping_backend"] != {
        "path": "backend/chapter_16_grouping_nodes.json",
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
        help=(
            "verify the inventory, grouping, and alias bytes plus either the "
            "bootstrap-pending or post-companion-covered deterministic prompt-map phase"
        ),
    )
    arguments = parser.parse_args()

    (
        inventory_payload,
        prompt_payload,
        grouping_payload,
        alias_payload,
        summary,
    ) = build_inventory()
    covered_prompt_payload = prompt_payload_with_support_status(prompt_payload, "covered")
    payloads = {
        INVENTORY_PATH: inventory_payload,
        PROMPT_MAP_PATH: prompt_payload,
        GROUPING_PATH: grouping_payload,
        OCCURRENCE_ALIAS_PATH: alias_payload,
    }
    prompt_map_phase = PROMPT_MAP_PHASE_BOOTSTRAP
    if arguments.check:
        for path, expected in (
            (INVENTORY_PATH, inventory_payload),
            (GROUPING_PATH, grouping_payload),
            (OCCURRENCE_ALIAS_PATH, alias_payload),
        ):
            if not path.is_file():
                raise SystemExit(f"generated output is missing: {path}")
            actual = path.read_bytes()
            if actual != expected:
                raise SystemExit(
                    f"generated output differs from deterministic regeneration: {path}"
                )
        if not PROMPT_MAP_PATH.is_file():
            raise SystemExit(f"generated output is missing: {PROMPT_MAP_PATH}")
        actual_prompt_payload = PROMPT_MAP_PATH.read_bytes()
        if actual_prompt_payload == prompt_payload:
            prompt_map_phase = PROMPT_MAP_PHASE_BOOTSTRAP
        elif actual_prompt_payload == covered_prompt_payload:
            prompt_map_phase = PROMPT_MAP_PHASE_COVERED
        else:
            raise SystemExit(
                "generated prompt map matches neither deterministic support phase: "
                f"{PROMPT_MAP_PATH}"
            )
    else:
        for path in OUTPUT_PATHS:
            path.write_bytes(payloads[path])
        for path in OUTPUT_PATHS:
            if path.read_bytes() != payloads[path]:
                raise SystemExit(f"written output failed byte-for-byte readback: {path}")

    summary["mode"] = "check" if arguments.check else "write"
    summary["prompt_map_phase"] = prompt_map_phase
    summary["authority_ordered_sha256"] = FROZEN_ORDERED_SHA256
    if arguments.check:
        summary["outputs"] = {
            path.relative_to(ROOT).as_posix(): base.identity_bytes(path.read_bytes())
            for path in OUTPUT_PATHS
        }
    else:
        summary["outputs"] = {
            path.relative_to(ROOT).as_posix(): base.identity_bytes(payloads[path])
            for path in OUTPUT_PATHS
        }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
