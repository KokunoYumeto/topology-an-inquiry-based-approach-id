#!/usr/bin/env python3
"""Build the deterministic occurrence-aware Chapter 18 prompt backend.

This is a hash-pinned adaptation of the proven Chapter 17 builder. The
translated nine-file Chapter 18 closure is the locator and source-order
denominator, while the unchanged pinned English closure verifies prompt
carrier order and every real ``xml:id``. All 128 physical prompt carriers are
canonical; an explicit zero-row occurrence-alias artifact records that no
duplicate source carrier was collapsed.
"""

from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
PREVIOUS_PATH = ROOT / "scripts" / "build_chapter17_prompt_inventory.py"
PREVIOUS_SHA256 = "12a946177c20b52c073fdcbaa88ecfec28ce41fa7bf6f2ed9f0762289b0a9f43"
TEMPLATE_PATH = ROOT / "scripts" / "build_chapter16_prompt_inventory.py"
TEMPLATE_SHA256 = "2bdf2424a7f47926b394508cf11c68233b1ffa55b52bad45edb3a72349906ca2"

FROZEN_AUTHORITY_COMMIT = "0c2d8f614ef87aa00de373f3418146c2f1d13bb9"
CHAPTER_FILE = "chap_Connected_topology.ptx"
EXPECTED_CHAPTER_INCLUDES = (
    "sec_connect_top_intro.ptx",
    "sec_connect_sets.ptx",
    "sec_connect_subset_rn.ptx",
    "sec_components.ptx",
    "sec_cut_sets.ptx",
    "sec_ivt_fpt.ptx",
    "sec_connect_top_summ.ptx",
    "sec_connect_top_exer.ptx",
)
EXPECTED_AUTHORITY_FILE_COUNT = 9
TRANSLATED_ORDERED_SHA256 = (
    "d0b9502b73e3b858b88a5aa914aef7ddf81b9d5dbb22c4d3786229b9f8259873"
)
UPSTREAM_ORDERED_SHA256 = (
    "85b18fac052f015c59c7451cdd9c76fe847ba4a668af392103cff709b55bbf7b"
)
TRANSLATED_ORDERED_HASH_CONTRACT = (
    "sha256 over each declared translated source path as UTF-8, NUL, decimal "
    "byte length, NUL, raw file bytes, NUL, in translated chapter-closure order"
)

EXPECTED_PROMPT_OCCURRENCE_TOTAL = 128
EXPECTED_CANONICAL_ENTRY_TOTAL = 128
EXPECTED_NONEXERCISE_OCCURRENCE_TOTAL = 43
EXPECTED_EXERCISE_OCCURRENCE_TOTAL = 85
EXPECTED_NONEXERCISE_ENTRY_TOTAL = 43
EXPECTED_EXERCISE_ENTRY_TOTAL = 85
EXPECTED_ATOMIC_OCCURRENCE_TOTAL = 117
EXPECTED_DIRECT_STATEMENT_OCCURRENCE_TOTAL = 9
EXPECTED_DIRECT_BODY_OCCURRENCE_TOTAL = 2
EXPECTED_GROUPING_TOTAL = 6
EXPECTED_ALIAS_TOTAL = 0

EXACT_OCCURRENCE_ALIAS_PAIRS: tuple[
    tuple[tuple[str, str], tuple[str, str]], ...
] = ()
EXPECTED_DIRECT_BODY_KEYS = (
    ("source/sec_connect_sets.ptx", "/section/activity[3]"),
    ("source/sec_cut_sets.ptx", "/section/activity[2]"),
)


def digest_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def replace_once(source: str, old: str, new: str) -> str:
    count = source.count(old)
    if count != 1:
        raise SystemExit(
            f"Chapter 16 template adaptation expected one occurrence, found {count}: {old!r}"
        )
    return source.replace(old, new)


def normalized_element_bytes(element: etree._Element) -> bytes:
    """Return deterministic subtree bytes with XML formatting whitespace folded."""
    clone = copy.deepcopy(element)
    clone.tail = None
    for node in clone.iter():
        if node.text is not None:
            node.text = " ".join(node.text.split())
        if node.tail is not None:
            node.tail = " ".join(node.tail.split())
    return etree.tostring(clone, method="c14n", with_comments=True)


def load_adapted_template() -> dict[str, Any]:
    previous_hash = digest_bytes(PREVIOUS_PATH.read_bytes())
    if previous_hash != PREVIOUS_SHA256:
        raise SystemExit(
            "Chapter 17 prompt-inventory adaptation authority changed: "
            f"expected {PREVIOUS_SHA256}, found {previous_hash}"
        )
    payload = TEMPLATE_PATH.read_bytes()
    actual_hash = digest_bytes(payload)
    if actual_hash != TEMPLATE_SHA256:
        raise SystemExit(
            "Chapter 16 prompt-inventory template changed: "
            f"expected {TEMPLATE_SHA256}, found {actual_hash}"
        )
    source = payload.decode("utf-8")

    old_direct_body = '''    direct_body_occurrences = [
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
'''
    new_direct_body = '''    direct_body_occurrences = [
        occurrence
        for occurrence in occurrences
        if occurrence["prompt_carrier"] == "direct_body"
    ]
    direct_body_keys = tuple(
        (
            occurrence["authority_source_file"],
            occurrence["authority_locator"]["xpath"],
        )
        for occurrence in direct_body_occurrences
    )
    if direct_body_keys != EXPECTED_DIRECT_BODY_KEYS:
        raise SystemExit(
            "Chapter 18 direct-body locator sequence changed: "
            f"expected {EXPECTED_DIRECT_BODY_KEYS}, found {direct_body_keys}"
        )
'''
    source = replace_once(source, old_direct_body, new_direct_body)
    source = source.replace("Chapter 16", "Chapter 18")
    source = source.replace("chapter_16", "chapter_18")
    source = source.replace("ch16", "ch18")
    source = source.replace("quotient-spaces", "connected-spaces")
    source = source.replace("{1: 50, 2: 2}", "{1: 128}")
    source = source.replace(
        "two hard-coded exact frozen file/XPath pairs",
        "no source occurrences as aliases",
    )
    source = source.replace("two exact declared pairs", "the empty declared alias set")
    source = source.replace(
        "two declared canonical entries", "no canonical entry"
    )
    source = source.replace("exactly seven unique files", "exactly nine unique files")
    source = source.replace('"exact_subtree_sha256"', '"alias_subtree_sha256"')
    source = source.replace(
        "hard_coded_exact_subtree_pair",
        "hard_coded_exact_locator_pair_whitespace_normalized_content",
    )
    source = replace_once(source, '"sequence": 16,', '"sequence": 18,')
    source = replace_once(
        source,
        '"source_chapter_xml_id": "chap_quotients",',
        '"source_chapter_xml_id": "chap_Connected_topology",',
    )
    source = replace_once(
        source,
        'if locator["subtree_sha256"] != canonical_locator["subtree_sha256"]:',
        "if base.digest_bytes(element_bytes(element)) != "
        "base.digest_bytes(element_bytes(canonical_element[0])):",
    )

    namespace: dict[str, Any] = {
        "__name__": "_chapter18_prompt_inventory_template",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(source, str(TEMPLATE_PATH), "exec"), namespace)
    overrides = {
        "FROZEN_AUTHORITY_COMMIT": FROZEN_AUTHORITY_COMMIT,
        "CHAPTER_FILE": CHAPTER_FILE,
        "EXPECTED_CHAPTER_INCLUDES": EXPECTED_CHAPTER_INCLUDES,
        "EXPECTED_AUTHORITY_FILE_COUNT": EXPECTED_AUTHORITY_FILE_COUNT,
        "FROZEN_ORDERED_SHA256": TRANSLATED_ORDERED_SHA256,
        "AUTHORITY_ORDERED_HASH_CONTRACT": TRANSLATED_ORDERED_HASH_CONTRACT,
        "EXPECTED_PROMPT_OCCURRENCE_TOTAL": EXPECTED_PROMPT_OCCURRENCE_TOTAL,
        "EXPECTED_CANONICAL_ENTRY_TOTAL": EXPECTED_CANONICAL_ENTRY_TOTAL,
        "EXPECTED_NONEXERCISE_OCCURRENCE_TOTAL": EXPECTED_NONEXERCISE_OCCURRENCE_TOTAL,
        "EXPECTED_EXERCISE_OCCURRENCE_TOTAL": EXPECTED_EXERCISE_OCCURRENCE_TOTAL,
        "EXPECTED_NONEXERCISE_ENTRY_TOTAL": EXPECTED_NONEXERCISE_ENTRY_TOTAL,
        "EXPECTED_EXERCISE_ENTRY_TOTAL": EXPECTED_EXERCISE_ENTRY_TOTAL,
        "EXPECTED_ATOMIC_OCCURRENCE_TOTAL": EXPECTED_ATOMIC_OCCURRENCE_TOTAL,
        "EXPECTED_DIRECT_STATEMENT_OCCURRENCE_TOTAL": EXPECTED_DIRECT_STATEMENT_OCCURRENCE_TOTAL,
        "EXPECTED_DIRECT_BODY_OCCURRENCE_TOTAL": EXPECTED_DIRECT_BODY_OCCURRENCE_TOTAL,
        "EXPECTED_GROUPING_TOTAL": EXPECTED_GROUPING_TOTAL,
        "EXPECTED_ALIAS_TOTAL": EXPECTED_ALIAS_TOTAL,
        "EXACT_OCCURRENCE_ALIAS_PAIRS": EXACT_OCCURRENCE_ALIAS_PAIRS,
        "EXACT_OCCURRENCE_ALIAS_MAP": dict(EXACT_OCCURRENCE_ALIAS_PAIRS),
        "EXPECTED_DIRECT_BODY_KEYS": EXPECTED_DIRECT_BODY_KEYS,
        "element_bytes": normalized_element_bytes,
        "SOURCE_DIR": ROOT / "source",
    }
    namespace.update(overrides)
    return namespace


def xml_id_sequence(document: etree._ElementTree, xml_id: str) -> list[tuple[str, str]]:
    return [
        (element.tag, value)
        for element in document.iter()
        if (value := element.get(xml_id)) is not None
    ]


def event_signature(events: list[dict[str, Any]], base: Any) -> list[dict[str, Any]]:
    return [
        {
            "sequence": sequence,
            "event_kind": event["event_kind"],
            "partition": event.get("partition"),
            "prompt_carrier": event.get("prompt_carrier"),
            "source_file": event["source_file"],
            "nearest_real_xml_id": base.nearest_real_xml_id(event["element"]),
            "element_tag": event["element"].tag,
        }
        for sequence, event in enumerate(events, start=1)
    ]


def validate_translated_closure(template: dict[str, Any]) -> dict[str, Any]:
    base = template["base"]
    translated_root = ROOT / "source"
    chapter_path = translated_root / CHAPTER_FILE
    chapter_document = base.parse_xml(chapter_path)
    hrefs = tuple(
        chapter_document.xpath("//xi:include/@href", namespaces={"xi": base.XI_NS})
    )
    if hrefs != EXPECTED_CHAPTER_INCLUDES:
        raise SystemExit(
            "translated Chapter 18 XInclude order changed: "
            f"expected {EXPECTED_CHAPTER_INCLUDES}, found {hrefs}"
        )

    records: list[dict[str, Any]] = []
    documents: dict[str, etree._ElementTree] = {}
    for sequence, name in enumerate((CHAPTER_FILE, *hrefs), start=1):
        path = translated_root / name
        if not path.is_file():
            raise SystemExit(f"missing translated Chapter 18 closure file: {path}")
        document = chapter_document if name == CHAPTER_FILE else base.parse_xml(path)
        if name != CHAPTER_FILE and document.xpath(
            "//xi:include/@href", namespaces={"xi": base.XI_NS}
        ):
            raise SystemExit(f"unexpected nested XInclude in translated file: {name}")
        payload = path.read_bytes()
        relative = base.authority_relative(name)
        records.append(
            {
                "sequence": sequence,
                "path": relative,
                "bytes": len(payload),
                "sha256": base.digest_bytes(payload),
                "payload": payload,
            }
        )
        documents[relative] = document

    translated_ordered_hash = base.ordered_authority_hash(records)
    if translated_ordered_hash != TRANSLATED_ORDERED_SHA256:
        raise SystemExit(
            "translated Chapter 18 ordered source hash changed: "
            f"expected {TRANSLATED_ORDERED_SHA256}, found {translated_ordered_hash}"
        )

    upstream_root = (
        LANE
        / "authority"
        / "gvsu-pinned"
        / f"topology-{FROZEN_AUTHORITY_COMMIT}"
        / "source"
    )
    upstream_records: list[dict[str, Any]] = []
    upstream_documents: dict[str, etree._ElementTree] = {}
    for record in records:
        name = Path(record["path"]).name
        path = upstream_root / name
        document = base.parse_xml(path)
        payload = path.read_bytes()
        upstream_records.append(
            {
                "sequence": record["sequence"],
                "path": record["path"],
                "bytes": len(payload),
                "sha256": base.digest_bytes(payload),
                "payload": payload,
            }
        )
        upstream_documents[record["path"]] = document
    upstream_ordered_hash = base.ordered_authority_hash(upstream_records)
    if upstream_ordered_hash != UPSTREAM_ORDERED_SHA256:
        raise SystemExit(
            "pinned Chapter 18 authority hash changed: "
            f"expected {UPSTREAM_ORDERED_SHA256}, found {upstream_ordered_hash}"
        )

    authority_events = base.discover_events(upstream_records, upstream_documents)
    translated_events = base.discover_events(records, documents)
    authority_signature = event_signature(authority_events, base)
    translated_signature = event_signature(translated_events, base)
    if translated_signature != authority_signature:
        raise SystemExit(
            "translated Chapter 18 prompt order/carrier/xml:id signature differs from authority"
        )
    for source_file, authority_document in upstream_documents.items():
        if xml_id_sequence(authority_document, base.XML_ID) != xml_id_sequence(
            documents[source_file], base.XML_ID
        ):
            raise SystemExit(f"translated Chapter 18 xml:id sequence changed: {source_file}")

    prompt_events = [
        event for event in translated_events if event["event_kind"] == "prompt"
    ]
    grouping_events = [
        event for event in translated_events if event["event_kind"] == "grouping"
    ]
    carriers = Counter(event["prompt_carrier"] for event in prompt_events)
    partitions = Counter(event["partition"] for event in prompt_events)
    if carriers != Counter(
        atomic_task=EXPECTED_ATOMIC_OCCURRENCE_TOTAL,
        direct_statement=EXPECTED_DIRECT_STATEMENT_OCCURRENCE_TOTAL,
        direct_body=EXPECTED_DIRECT_BODY_OCCURRENCE_TOTAL,
    ):
        raise SystemExit(f"translated Chapter 18 carrier census changed: {carriers}")
    if partitions != Counter(
        nonexercise=EXPECTED_NONEXERCISE_OCCURRENCE_TOTAL,
        exercise=EXPECTED_EXERCISE_OCCURRENCE_TOTAL,
    ):
        raise SystemExit(f"translated Chapter 18 partition census changed: {partitions}")
    if len(grouping_events) != EXPECTED_GROUPING_TOTAL:
        raise SystemExit("translated Chapter 18 grouping census changed")

    normalized_hashes = Counter(
        base.digest_bytes(normalized_element_bytes(event["element"]))
        for event in prompt_events
    )
    duplicates = sorted(value for value, count in normalized_hashes.items() if count > 1)
    if duplicates:
        raise SystemExit(
            "Chapter 18 gained duplicate prompt subtrees without declared aliases: "
            f"{duplicates}"
        )

    signature_payload = base.json_bytes(translated_signature)
    return {
        "root": "source",
        "source_file_count": len(records),
        "ordered_hash_contract": TRANSLATED_ORDERED_HASH_CONTRACT,
        "ordered_sha256": translated_ordered_hash,
        "ordered_files": [
            {key: record[key] for key in ("sequence", "path", "bytes", "sha256")}
            for record in records
        ],
        "lineage_upstream_commit": FROZEN_AUTHORITY_COMMIT,
        "lineage_upstream_ordered_sha256": upstream_ordered_hash,
        "lineage_upstream_ordered_files": [
            {key: record[key] for key in ("sequence", "path", "bytes", "sha256")}
            for record in upstream_records
        ],
        "upstream_per_file_event_signature_match": True,
        "xml_id_sequence_match": True,
        "event_signature_sha256": base.digest_bytes(signature_payload),
        "physical_prompt_occurrence_total": len(prompt_events),
        "canonical_source_support_entry_total": len(prompt_events),
        "grouping_node_total": len(grouping_events),
        "occurrence_alias_total": 0,
        "duplicate_normalized_prompt_subtree_total": 0,
    }


def build_payloads(template: dict[str, Any]) -> tuple[dict[Path, bytes], dict[str, Any]]:
    translated_source = validate_translated_closure(template)
    (
        inventory_payload,
        prompt_payload,
        grouping_payload,
        alias_payload,
        summary,
    ) = template["build_inventory"]()
    grouping = json.loads(grouping_payload.decode("utf-8"))
    grouping["locator_contract"]["locator_basis"] = "translated_chapter_closure"
    grouping["locator_contract"]["lineage_upstream_commit"] = grouping[
        "locator_contract"
    ].pop("authority_commit")
    grouping_payload = template["base"].json_bytes(grouping)
    inventory = json.loads(inventory_payload.decode("utf-8"))
    inventory["authority"]["locator_basis"] = "translated_chapter_closure"
    inventory["authority"]["root"] = "source"
    inventory["authority"]["lineage_upstream_commit"] = inventory["authority"].pop(
        "commit"
    )
    inventory["authority"]["line_locator_contract"]["meaning"] = (
        "one-based exact carrier-start line in the translated Chapter 18 source"
    )
    inventory["authority"]["line_locator_contract"]["legacy_field_names"] = [
        "authority_source_file",
        "authority_line",
    ]
    inventory["occurrence_entry_contract"]["alias_method"] = (
        "no occurrence aliases; every physical Chapter 18 prompt carrier is canonical"
    )
    inventory["grouping_backend"].update(
        template["base"].identity_bytes(grouping_payload)
    )
    inventory["translated_source"] = translated_source
    inventory_payload = template["base"].json_bytes(inventory)
    exercise_batches = template["derive_exercise_batches"](
        EXPECTED_EXERCISE_ENTRY_TOTAL
    )
    _, documents = template["load_authority_closure"]()
    template["verify_payloads"](
        inventory_payload,
        prompt_payload,
        grouping_payload,
        alias_payload,
        documents,
        exercise_batches,
    )
    payloads = {
        template["INVENTORY_PATH"]: inventory_payload,
        template["PROMPT_MAP_PATH"]: prompt_payload,
        template["GROUPING_PATH"]: grouping_payload,
        template["OCCURRENCE_ALIAS_PATH"]: alias_payload,
    }
    summary["translated_source_ordered_sha256"] = translated_source["ordered_sha256"]
    summary["lineage_upstream_ordered_sha256"] = translated_source[
        "lineage_upstream_ordered_sha256"
    ]
    return payloads, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify all generated Chapter 18 inventory artifacts byte for byte",
    )
    arguments = parser.parse_args()
    template = load_adapted_template()
    payloads, summary = build_payloads(template)
    prompt_map_phase = template["PROMPT_MAP_PHASE_BOOTSTRAP"]
    prompt_path = template["PROMPT_MAP_PATH"]
    covered_prompt_payload = template["prompt_payload_with_support_status"](
        payloads[prompt_path], "covered"
    )

    if arguments.check:
        for path, expected in payloads.items():
            if not path.is_file():
                raise SystemExit(f"generated output is missing: {path}")
            actual = path.read_bytes()
            if path == prompt_path and actual == covered_prompt_payload:
                prompt_map_phase = template["PROMPT_MAP_PHASE_COVERED"]
            elif actual != expected:
                raise SystemExit(
                    f"generated output differs from deterministic regeneration: {path}"
                )
    else:
        for path, payload in payloads.items():
            path.write_bytes(payload)
        for path, payload in payloads.items():
            if path.read_bytes() != payload:
                raise SystemExit(f"written output failed byte-for-byte readback: {path}")

    summary["mode"] = "check" if arguments.check else "write"
    summary["prompt_map_phase"] = prompt_map_phase
    summary["authority_ordered_sha256"] = UPSTREAM_ORDERED_SHA256
    summary["outputs"] = {
        path.relative_to(ROOT).as_posix(): template["base"].identity_bytes(
            path.read_bytes() if arguments.check else payload
        )
        for path, payload in payloads.items()
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
