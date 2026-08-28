#!/usr/bin/env python3
"""Build the deterministic occurrence-aware Chapter 17 prompt backend.

The implementation is an exact, hash-pinned adaptation of the Chapter 16
builder pattern.  The translated Chapter 17 closure is the locator and source-
order denominator, while a preflight verifies that every file keeps the same
prompt order, carrier classifications, and real ``xml:id`` sequence as the
frozen upstream source.
The repeated opening exercise task is aliased only by its declared locator pair;
whitespace-normalized content equality is checked because the two source
subtrees differ only in indentation.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter
import hashlib
import json
from pathlib import Path
from typing import Any

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
TEMPLATE_PATH = ROOT / "scripts" / "build_chapter16_prompt_inventory.py"
TEMPLATE_SHA256 = "2bdf2424a7f47926b394508cf11c68233b1ffa55b52bad45edb3a72349906ca2"

FROZEN_AUTHORITY_COMMIT = "0c2d8f614ef87aa00de373f3418146c2f1d13bb9"
CHAPTER_FILE = "chap_Compact_topology.ptx"
EXPECTED_CHAPTER_INCLUDES = (
    "sec_compact_top_intro.ptx",
    "sec_compact_cont.ptx",
    "sec_compact_rn.ptx",
    "sec_compact_app.ptx",
    "sec_compact_top_summ.ptx",
    "sec_fractals.ptx",
    "sec_compact_top_exer.ptx",
)
EXPECTED_AUTHORITY_FILE_COUNT = 8
FROZEN_ORDERED_SHA256 = (
    "ad530c0e9362cd944b264c33aeb291d9c2e8ea2884ed8d5e76ddc9939a013c3e"
)
TRANSLATED_ORDERED_HASH_CONTRACT = (
    "sha256 over each declared translated source path as UTF-8, NUL, decimal "
    "byte length, NUL, raw file bytes, NUL, in translated chapter-closure order"
)

EXPECTED_PROMPT_OCCURRENCE_TOTAL = 76
EXPECTED_CANONICAL_ENTRY_TOTAL = 75
EXPECTED_NONEXERCISE_OCCURRENCE_TOTAL = 32
EXPECTED_EXERCISE_OCCURRENCE_TOTAL = 44
EXPECTED_NONEXERCISE_ENTRY_TOTAL = 32
EXPECTED_EXERCISE_ENTRY_TOTAL = 43
EXPECTED_ATOMIC_OCCURRENCE_TOTAL = 71
EXPECTED_DIRECT_STATEMENT_OCCURRENCE_TOTAL = 4
EXPECTED_DIRECT_BODY_OCCURRENCE_TOTAL = 1
EXPECTED_GROUPING_TOTAL = 2
EXPECTED_ALIAS_TOTAL = 1

EXACT_OCCURRENCE_ALIAS_PAIRS = (
    (
        ("source/sec_compact_top_exer.ptx", "/exercises/exercise[1]/task[2]"),
        ("source/sec_compact_top_exer.ptx", "/exercises/exercise[1]/task[1]"),
    ),
)
EXPECTED_DIRECT_BODY_KEY = (
    "source/sec_compact_rn.ptx",
    "/section/activity[3]",
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
    payload = TEMPLATE_PATH.read_bytes()
    actual_hash = digest_bytes(payload)
    if actual_hash != TEMPLATE_SHA256:
        raise SystemExit(
            "Chapter 16 prompt-inventory template changed: "
            f"expected {TEMPLATE_SHA256}, found {actual_hash}"
        )
    source = payload.decode("utf-8")
    source = source.replace("Chapter 16", "Chapter 17")
    source = source.replace("chapter_16", "chapter_17")
    source = source.replace("ch16", "ch17")
    source = source.replace("quotient-spaces", "compact-spaces")
    source = source.replace("act_quotient_er", "sec_compact_rn")
    source = source.replace("{1: 50, 2: 2}", "{1: 74, 2: 1}")
    source = source.replace(
        "two hard-coded exact frozen file/XPath pairs",
        "one hard-coded exact frozen file/XPath pair",
    )
    source = source.replace("two exact declared pairs", "one exact declared pair")
    source = source.replace("two declared canonical entries", "the declared canonical entry")
    source = source.replace("\"exact_subtree_sha256\"", "\"alias_subtree_sha256\"")
    source = source.replace(
        "hard_coded_exact_subtree_pair",
        "hard_coded_exact_locator_pair_whitespace_normalized_content",
    )
    source = replace_once(source, '"sequence": 16,', '"sequence": 17,')
    source = replace_once(
        source,
        '"source_chapter_xml_id": "chap_quotients",',
        '"source_chapter_xml_id": "chap_Compact_topology",',
    )
    source = replace_once(
        source,
        'if locator["subtree_sha256"] != canonical_locator["subtree_sha256"]:',
        "if base.digest_bytes(element_bytes(element)) != "
        "base.digest_bytes(element_bytes(canonical_element[0])):",
    )

    namespace: dict[str, Any] = {
        "__name__": "_chapter17_prompt_inventory_template",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(source, str(TEMPLATE_PATH), "exec"), namespace)

    overrides = {
        "FROZEN_AUTHORITY_COMMIT": FROZEN_AUTHORITY_COMMIT,
        "CHAPTER_FILE": CHAPTER_FILE,
        "EXPECTED_CHAPTER_INCLUDES": EXPECTED_CHAPTER_INCLUDES,
        "EXPECTED_AUTHORITY_FILE_COUNT": EXPECTED_AUTHORITY_FILE_COUNT,
        "FROZEN_ORDERED_SHA256": FROZEN_ORDERED_SHA256,
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
        "EXPECTED_DIRECT_BODY_KEY": EXPECTED_DIRECT_BODY_KEY,
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
            "translated Chapter 17 XInclude order changed: "
            f"expected {EXPECTED_CHAPTER_INCLUDES}, found {hrefs}"
        )

    records: list[dict[str, Any]] = []
    documents: dict[str, etree._ElementTree] = {}
    for sequence, name in enumerate((CHAPTER_FILE, *hrefs), start=1):
        path = translated_root / name
        if not path.is_file():
            raise SystemExit(f"missing translated Chapter 17 closure file: {path}")
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

    authority_events = base.discover_events(upstream_records, upstream_documents)
    translated_events = base.discover_events(records, documents)
    authority_signature = event_signature(authority_events, base)
    translated_signature = event_signature(translated_events, base)
    if translated_signature != authority_signature:
        raise SystemExit(
            "translated Chapter 17 prompt order/carrier/xml:id signature differs from authority"
        )
    for source_file, authority_document in upstream_documents.items():
        translated_document = documents[source_file]
        if xml_id_sequence(authority_document, base.XML_ID) != xml_id_sequence(
            translated_document, base.XML_ID
        ):
            raise SystemExit(f"translated Chapter 17 xml:id sequence changed: {source_file}")

    prompt_events = [event for event in translated_events if event["event_kind"] == "prompt"]
    grouping_events = [event for event in translated_events if event["event_kind"] == "grouping"]
    carriers = Counter(event["prompt_carrier"] for event in prompt_events)
    partitions = Counter(event["partition"] for event in prompt_events)
    if carriers != Counter(
        atomic_task=EXPECTED_ATOMIC_OCCURRENCE_TOTAL,
        direct_statement=EXPECTED_DIRECT_STATEMENT_OCCURRENCE_TOTAL,
        direct_body=EXPECTED_DIRECT_BODY_OCCURRENCE_TOTAL,
    ):
        raise SystemExit(f"translated Chapter 17 carrier census changed: {carriers}")
    if partitions != Counter(
        nonexercise=EXPECTED_NONEXERCISE_OCCURRENCE_TOTAL,
        exercise=EXPECTED_EXERCISE_OCCURRENCE_TOTAL,
    ):
        raise SystemExit(f"translated Chapter 17 partition census changed: {partitions}")
    if len(grouping_events) != EXPECTED_GROUPING_TOTAL:
        raise SystemExit("translated Chapter 17 grouping census changed")

    alias_key, canonical_key = EXACT_OCCURRENCE_ALIAS_PAIRS[0]
    alias_elements = documents[alias_key[0]].xpath(alias_key[1])
    canonical_elements = documents[canonical_key[0]].xpath(canonical_key[1])
    if len(alias_elements) != 1 or len(canonical_elements) != 1:
        raise SystemExit("translated Chapter 17 duplicate alias locator is not unique")
    alias_normalized = normalized_element_bytes(alias_elements[0])
    canonical_normalized = normalized_element_bytes(canonical_elements[0])
    if alias_normalized != canonical_normalized:
        raise SystemExit("translated Chapter 17 declared duplicate tasks differ in content")

    signature_payload = base.json_bytes(translated_signature)
    return {
        "root": "source",
        "source_file_count": len(records),
        "ordered_hash_contract": template["AUTHORITY_ORDERED_HASH_CONTRACT"],
        "ordered_sha256": base.ordered_authority_hash(records),
        "ordered_files": [
            {key: record[key] for key in ("sequence", "path", "bytes", "sha256")}
            for record in records
        ],
        "upstream_per_file_event_signature_match": True,
        "xml_id_sequence_match": True,
        "event_signature_sha256": base.digest_bytes(signature_payload),
        "physical_prompt_occurrence_total": len(prompt_events),
        "grouping_node_total": len(grouping_events),
        "duplicate_alias_normalized_subtree_sha256": base.digest_bytes(alias_normalized),
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
        "one-based exact carrier-start line in the translated Chapter 17 source"
    )
    inventory["authority"]["line_locator_contract"]["legacy_field_names"] = [
        "authority_source_file",
        "authority_line",
    ]
    inventory["occurrence_entry_contract"]["alias_method"] = (
        "one hard-coded translated file/XPath pair with whitespace-normalized "
        "content equality"
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
    return payloads, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify all generated Chapter 17 inventory artifacts byte for byte",
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
    summary["authority_ordered_sha256"] = FROZEN_ORDERED_SHA256
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
