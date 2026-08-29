#!/usr/bin/env python3
"""Build the deterministic occurrence-aware Chapter 19 prompt backend.

This bounded, hash-pinned adaptation of the admitted Chapter 18 builder uses
the translated nine-file Chapter 19 closure as the locator denominator and the
unchanged pinned English closure as lineage evidence.  Every one of the 39
physical prompt carriers is canonical; no occurrence alias is inferred.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_PATH = ROOT / "scripts" / "build_chapter18_prompt_inventory.py"
PREVIOUS_SHA256 = "2b583f08e5bb863c4013d53b4c8eb81a0c09feec97351eae758da3f412b926e7"

FROZEN_AUTHORITY_COMMIT = "0c2d8f614ef87aa00de373f3418146c2f1d13bb9"
CHAPTER_FILE = "chap_Path_connected_topology.ptx"
EXPECTED_CHAPTER_INCLUDES = (
    "sec_path_intro.ptx",
    "sec_path_connect.ptx",
    "sec_path_connect_equiv.ptx",
    "sec_connectedness.ptx",
    "sec_connect_finite.ptx",
    "sec_connect_infinite.ptx",
    "sec_path_summ.ptx",
    "sec_path_exer.ptx",
)
EXPECTED_AUTHORITY_FILE_COUNT = 9
TRANSLATED_ORDERED_SHA256 = (
    "ba26d5c4a1cb27cc9c5d6bea845e8406340a54d421905d11f8d562aacb118b0f"
)
UPSTREAM_ORDERED_SHA256 = (
    "7c9c1aeb231d101bc2efaf0fd071edee2ae9a244b4095e00875e2ee19054a58b"
)

EXPECTED_PROMPT_OCCURRENCE_TOTAL = 39
EXPECTED_CANONICAL_ENTRY_TOTAL = 39
EXPECTED_NONEXERCISE_OCCURRENCE_TOTAL = 21
EXPECTED_EXERCISE_OCCURRENCE_TOTAL = 18
EXPECTED_NONEXERCISE_ENTRY_TOTAL = 21
EXPECTED_EXERCISE_ENTRY_TOTAL = 18
EXPECTED_ATOMIC_OCCURRENCE_TOTAL = 33
EXPECTED_DIRECT_STATEMENT_OCCURRENCE_TOTAL = 5
EXPECTED_DIRECT_BODY_OCCURRENCE_TOTAL = 1
EXPECTED_GROUPING_TOTAL = 2
EXPECTED_ALIAS_TOTAL = 0
EXPECTED_DIRECT_BODY_KEYS = (
    ("source/sec_path_connect_equiv.ptx", "/section/activity[1]"),
)


def digest_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def replace_once(source: str, old: str, new: str) -> str:
    count = source.count(old)
    if count != 1:
        raise SystemExit(
            f"Chapter 18 adaptation expected one occurrence, found {count}: {old!r}"
        )
    return source.replace(old, new)


def load_adapted_previous() -> dict[str, Any]:
    payload = PREVIOUS_PATH.read_bytes()
    actual_hash = digest_bytes(payload)
    if actual_hash != PREVIOUS_SHA256:
        raise SystemExit(
            "Chapter 18 prompt-inventory builder changed: "
            f"expected {PREVIOUS_SHA256}, found {actual_hash}"
        )
    source = payload.decode("utf-8")
    source = source.replace("Chapter 18", "Chapter 19")
    source = source.replace("chapter_18", "chapter_19")
    source = source.replace("ch18", "ch19")
    source = source.replace("connected-spaces", "path-connected-spaces")
    source = replace_once(source, '"{1: 128}"', '"{1: 39}"')
    source = replace_once(source, "All 128 physical", "All 39 physical")
    source = replace_once(source, '"sequence": 18,', '"sequence": 19,')
    source = replace_once(
        source,
        '"source_chapter_xml_id": "chap_Connected_topology",',
        '"source_chapter_xml_id": "chap_Path_connected_topology",',
    )
    source = replace_once(
        source,
        '''def xml_id_sequence(document: etree._ElementTree, xml_id: str) -> list[tuple[str, str]]:
    return [
        (element.tag, value)
        for element in document.iter()
        if (value := element.get(xml_id)) is not None
    ]
''',
        '''def xml_id_sequence(document: etree._ElementTree, xml_id: str) -> list[str]:
    return [
        value
        for element in document.iter()
        if (value := element.get(xml_id)) is not None
    ]
''',
    )

    namespace: dict[str, Any] = {
        "__name__": "_chapter19_prompt_inventory_adaptation",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(source, str(PREVIOUS_PATH), "exec"), namespace)
    namespace.update(
        {
            "FROZEN_AUTHORITY_COMMIT": FROZEN_AUTHORITY_COMMIT,
            "CHAPTER_FILE": CHAPTER_FILE,
            "EXPECTED_CHAPTER_INCLUDES": EXPECTED_CHAPTER_INCLUDES,
            "EXPECTED_AUTHORITY_FILE_COUNT": EXPECTED_AUTHORITY_FILE_COUNT,
            "TRANSLATED_ORDERED_SHA256": TRANSLATED_ORDERED_SHA256,
            "UPSTREAM_ORDERED_SHA256": UPSTREAM_ORDERED_SHA256,
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
            "EXACT_OCCURRENCE_ALIAS_PAIRS": (),
            "EXACT_OCCURRENCE_ALIAS_MAP": {},
            "EXPECTED_DIRECT_BODY_KEYS": EXPECTED_DIRECT_BODY_KEYS,
            "SOURCE_DIR": ROOT / "source",
        }
    )
    return namespace


def main() -> int:
    namespace = load_adapted_previous()
    return int(namespace["main"]())


if __name__ == "__main__":
    raise SystemExit(main())
