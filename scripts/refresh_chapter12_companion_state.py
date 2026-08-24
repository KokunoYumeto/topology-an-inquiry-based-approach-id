#!/usr/bin/env python3
"""Deterministically refresh the Chapter 12 prompt/support backend.

The script is deliberately bounded to the final Chapter 12 companion and its
five machine-readable state artifacts. Historical ``.partial`` artifacts are
read-only witnesses. The script does not build or admit a reader.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import os
from pathlib import Path
from typing import Any

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
COMPANION = ROOT / "companion"
PARTIAL_QA_PATH = ROOT / "qa" / "CHAPTER12_COMPANION_PARTIAL_QA.json"
PARTIAL_MANIFEST_PATH = ROOT / "backend" / "chapter_12_companion_manifest.partial.json"
PARTIAL_ALIASES_PATH = ROOT / "backend" / "chapter_12_entry_aliases.partial.csv"
QA_PATH = ROOT / "qa" / "CHAPTER12_COMPANION_QA.json"
MANIFEST_PATH = ROOT / "backend" / "chapter_12_companion_manifest.json"
ALIASES_PATH = ROOT / "backend" / "chapter_12_entry_aliases.csv"
HISTORICAL_PARTIAL_PATHS = (
    PARTIAL_MANIFEST_PATH,
    PARTIAL_QA_PATH,
    PARTIAL_ALIASES_PATH,
)
PROMPT_MAP_PATH = ROOT / "backend" / "chapter_12_source_prompt_map.csv"
GROUPING_PATH = ROOT / "backend" / "chapter_12_grouping_nodes.json"
WRAPPER = COMPANION / "chapter_12_topological_spaces_self_study.ptx"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XI_NS = "http://www.w3.org/2001/XInclude"
FROZEN_AUTHORITY_COMMIT = "0c2d8f614ef87aa00de373f3418146c2f1d13bb9"
PINNED_AUTHORITY_ROOT = LANE / "authority" / "gvsu-pinned" / f"topology-{FROZEN_AUTHORITY_COMMIT}"
FROZEN_CANONICAL_PROMPT_SHA256 = "ac30b9909de52371d5f0b44987246fd718bd90a100c3681f5b4db72290e95836"
FROZEN_LEGACY_51_SHA256 = "e662dc5309df34c96b46be0c8a852823e5384cd5e9dfffd6ec8a44b9a3b1e77b"
PRE_LOCATOR_CANONICAL_PROMPT_SHA256 = "a97eb97f9078219952329497b2b1d8deec10590f64663ce101fde682b2290d27"
PRE_LOCATOR_LEGACY_51_SHA256 = "b776a6fcb754b908315f820486c07d27151097b7e1a1bdf80d5ebd1b63160243"
PROMPT_CARRIERS = {"atomic_task", "direct_statement", "direct_body"}
SOURCE_ANCHOR_KIND = "synthetic_locale_neutral_alias"
AUTHORITY_SUBTREE_HASH_CONTRACT = "sha256-c14n-1.0-with-comments"
CANONICAL_PROMPT_FIELDS = (
    "sequence",
    "id",
    "source_anchor",
    "source_anchor_kind",
    "authority_source_file",
    "authority_line",
    "prompt_carrier",
)
PROMPT_MAP_FIELDS = (
    "sequence",
    "entry_id",
    "source_anchor",
    "source_anchor_kind",
    "authority_source_file",
    "authority_line",
    "prompt_carrier",
    "authority_locator",
    "parent_group_anchor",
    "support_status",
)
PRE_LOCATOR_PROMPT_MAP_FIELDS = (
    "sequence",
    "entry_id",
    "source_anchor",
    "authority_source_file",
    "authority_line",
    "prompt_carrier",
    "parent_group_anchor",
    "support_status",
)
LEGACY_PROMPT_MAP_FIELDS = (
    "sequence",
    "entry_id",
    "source_anchor",
    "source_file",
    "source_line",
    "prompt_carrier",
    "parent_group_anchor",
    "support_status",
)
ALIAS_FIELDS = (
    "sequence",
    "entry_id",
    "entry_type",
    "license",
    "source_anchor",
    "companion_anchor",
    "statement_id",
    "hint_id",
    "answer_id",
    "solution_id",
    "status",
)
TRANSACTION_MARKER = ROOT / "backend" / ".chapter12_companion_refresh.in_progress.json"

GUIDE_FILES = [
    "chapter_12_source_guides_a.ptx",
    "chapter_12_source_guides_b.ptx",
    "chapter_12_source_guides_c.ptx",
    "chapter_12_source_guides_d.ptx",
    "chapter_12_source_guides_e.ptx",
    "chapter_12_source_guides_f.ptx",
    "chapter_12_exercise_guides_a.ptx",
    "chapter_12_exercise_guides_b.ptx",
    "chapter_12_exercise_guides_c.ptx",
    "chapter_12_exercise_guides_d.ptx",
    "chapter_12_exercise_guides_e.ptx",
    "chapter_12_exercise_guides_f.ptx",
    "chapter_12_exercise_guides_g.ptx",
]
OPTIONAL_MASTERY_FILE = "chapter_12_mastery.ptx"
MASTERY_ENTRY_TYPE = "original_mastery"
SOURCE_GUIDE_ENTRY_TYPE = "source_prompt_guide"
COMPANION_LICENSE = "CC BY 4.0"
SOURCE_DERIVATIVE_RIGHTS = "CC BY-NC-SA 3.0 conservative treatment"
COMPANION_COMPONENT_RIGHTS = "CC BY 4.0 separate original component"
EXACT_MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra"
MANIFEST_PROVENANCE = {
    "tool": EXACT_MODEL_PROVENANCE,
    "non_endorsement": "This component is original companion content and is not GVSU or Schlicker prose.",
}
QA_RIGHTS_BOUNDARY = {
    "source_derivative": SOURCE_DERIVATIVE_RIGHTS,
    "companion_component": COMPANION_COMPONENT_RIGHTS,
    "non_endorsement": "The companion is not authored by Steven Schlicker or Grand Valley State University.",
}
QA_PROVENANCE = {
    "tool": EXACT_MODEL_PROVENANCE,
    "instruction": "Produced at the user's direction; source-author, institutional, and human-contributor credits remain unchanged.",
}
FROZEN_MASTERY_IDS = tuple(f"o003-c90-ch12-mastery-{number:02d}" for number in range(1, 9))
CHAPTER_SOURCE_FILES = [
    "chap_top_spaces.ptx",
    "sec_top_space_intro.ptx",
    "sec_exam_top.ptx",
    "sec_base_top.ptx",
    "sec_metric_top_space.ptx",
    "sec_neighborhood_top_space.ptx",
    "sec_interior_set_top.ptx",
    "sec_top_space_summ.ptx",
    "sec_top_space_exer.ptx",
]

# Exact carrier-start lines in the pinned authority.  These supersede only the
# earlier line semantics; historical partial artifacts remain immutable.
AUTHORITY_LINE_CORRECTIONS = {
    1: 64, 2: 73, 3: 84, 4: 98, 5: 112, 6: 123, 7: 132, 8: 141,
    9: 49, 10: 59, 11: 36, 12: 103, 13: 125, 14: 134, 15: 141,
    16: 304, 17: 317, 18: 332, 19: 343, 20: 16,
    27: 70, 28: 81, 29: 93, 30: 158, 31: 165,
    57: 372, 58: 382, 59: 394, 60: 409,
}

# Metadata for the 28 prompts after exercise batch B.  The first 51 rows are
# recovered from the already-public manifest on the first run and thereafter
# from the complete prompt-map CSV written by this script.
_NEW_PROMPTS_LEGACY: list[dict[str, Any]] = [
    {"sequence": 52, "id": "o003-c90-ch12-exer-c-01", "source_anchor": "o003-gvsu-ch12-sec_top_space_exer-finite_minimal_basis-task-04", "source_file": "source/sec_top_space_exer.ptx", "source_line": 262, "prompt_carrier": "atomic_task"},
    {"sequence": 53, "id": "o003-c90-ch12-exer-c-02", "source_anchor": "o003-gvsu-ch12-sec_top_space_exer-topology_chains-task-01", "source_file": "source/sec_top_space_exer.ptx", "source_line": 271, "prompt_carrier": "atomic_task"},
    {"sequence": 54, "id": "o003-c90-ch12-exer-c-03", "source_anchor": "o003-gvsu-ch12-sec_top_space_exer-finite_topologies-task-01", "source_file": "source/sec_top_space_exer.ptx", "source_line": 343, "prompt_carrier": "atomic_task"},
    {"sequence": 55, "id": "o003-c90-ch12-exer-c-04", "source_anchor": "o003-gvsu-ch12-sec_top_space_exer-finite_topologies-task-02", "source_file": "source/sec_top_space_exer.ptx", "source_line": 350, "prompt_carrier": "atomic_task"},
    {"sequence": 56, "id": "o003-c90-ch12-exer-c-05", "source_anchor": "o003-gvsu-ch12-sec_top_space_exer-finite_topologies-task-03", "source_file": "source/sec_top_space_exer.ptx", "source_line": 357, "prompt_carrier": "atomic_task"},
    {"sequence": 57, "id": "o003-c90-ch12-exer-d-01", "source_anchor": "o003-gvsu-ch12-sec_top_space_exer-tail_topology-direct-01", "source_file": "source/sec_top_space_exer.ptx", "source_line": 372, "prompt_carrier": "direct_statement"},
    {"sequence": 58, "id": "o003-c90-ch12-exer-d-02", "source_anchor": "o003-gvsu-ch12-sec_top_space_exer-interior_laws-direct-01", "source_file": "source/sec_top_space_exer.ptx", "source_line": 382, "prompt_carrier": "direct_statement"},
    {"sequence": 59, "id": "o003-c90-ch12-exer-d-03", "source_anchor": "o003-gvsu-ch12-ex_particular_point_topology-direct-01", "source_file": "source/sec_top_space_exer.ptx", "source_line": 394, "prompt_carrier": "direct_statement"},
    {"sequence": 60, "id": "o003-c90-ch12-exer-d-04", "source_anchor": "o003-gvsu-ch12-ex_excluded_point_topology-direct-01", "source_file": "source/sec_top_space_exer.ptx", "source_line": 409, "prompt_carrier": "direct_statement"},
    {"sequence": 61, "id": "o003-c90-ch12-exer-e-01", "source_anchor": "o003-gvsu-ch12-ex_digital_line_topology-task-01", "source_file": "source/sec_top_space_exer.ptx", "source_line": 442, "prompt_carrier": "atomic_task"},
    {"sequence": 62, "id": "o003-c90-ch12-exer-e-02", "source_anchor": "o003-gvsu-ch12-ex_digital_line_topology-open_sets-task-01", "source_file": "source/sec_top_space_exer.ptx", "source_line": 466, "prompt_carrier": "atomic_task"},
    {"sequence": 63, "id": "o003-c90-ch12-exer-e-03", "source_anchor": "o003-gvsu-ch12-ex_digital_line_topology-open_sets-task-02", "source_file": "source/sec_top_space_exer.ptx", "source_line": 473, "prompt_carrier": "atomic_task"},
    {"sequence": 64, "id": "o003-c90-ch12-exer-e-04", "source_anchor": "o003-gvsu-ch12-ex_digital_line_topology-open_sets-task-03", "source_file": "source/sec_top_space_exer.ptx", "source_line": 480, "prompt_carrier": "atomic_task"},
    {"sequence": 65, "id": "o003-c90-ch12-exer-e-05", "source_anchor": "o003-gvsu-ch12-ex_digital_line_topology-open_sets-task-04", "source_file": "source/sec_top_space_exer.ptx", "source_line": 487, "prompt_carrier": "atomic_task"},
    {"sequence": 66, "id": "o003-c90-ch12-exer-e-06", "source_anchor": "o003-gvsu-ch12-ex_digital_line_topology-open_sets-task-05", "source_file": "source/sec_top_space_exer.ptx", "source_line": 494, "prompt_carrier": "atomic_task"},
    {"sequence": 67, "id": "o003-c90-ch12-exer-e-07", "source_anchor": "o003-gvsu-ch12-ex_digital_line_topology-open_sets-task-06", "source_file": "source/sec_top_space_exer.ptx", "source_line": 501, "prompt_carrier": "atomic_task"},
    {"sequence": 68, "id": "o003-c90-ch12-exer-f-01", "source_anchor": "o003-gvsu-ch12-ex_TS_Zariski-task-01", "source_file": "source/sec_top_space_exer.ptx", "source_line": 536, "prompt_carrier": "atomic_task"},
    {"sequence": 69, "id": "o003-c90-ch12-exer-f-02", "source_anchor": "o003-gvsu-ch12-ex_TS_Zariski-task-02", "source_file": "source/sec_top_space_exer.ptx", "source_line": 543, "prompt_carrier": "atomic_task"},
    {"sequence": 70, "id": "o003-c90-ch12-exer-f-03", "source_anchor": "o003-gvsu-ch12-ex_TS_Zariski-task-03", "source_file": "source/sec_top_space_exer.ptx", "source_line": 552, "prompt_carrier": "atomic_task"},
    {"sequence": 71, "id": "o003-c90-ch12-exer-f-04", "source_anchor": "o003-gvsu-ch12-ex_TS_Zariski-task-04", "source_file": "source/sec_top_space_exer.ptx", "source_line": 564, "prompt_carrier": "atomic_task"},
    {"sequence": 72, "id": "o003-c90-ch12-exer-f-05", "source_anchor": "o003-gvsu-ch12-ex_TS_Zariski-task-05", "source_file": "source/sec_top_space_exer.ptx", "source_line": 572, "prompt_carrier": "atomic_task"},
    {"sequence": 73, "id": "o003-c90-ch12-exer-g-01", "source_anchor": "o003-gvsu-ch12-sec_top_space_exer-true_false-task-01", "source_file": "source/sec_top_space_exer.ptx", "source_line": 591, "prompt_carrier": "atomic_task"},
    {"sequence": 74, "id": "o003-c90-ch12-exer-g-02", "source_anchor": "o003-gvsu-ch12-sec_top_space_exer-true_false-task-02", "source_file": "source/sec_top_space_exer.ptx", "source_line": 598, "prompt_carrier": "atomic_task"},
    {"sequence": 75, "id": "o003-c90-ch12-exer-g-03", "source_anchor": "o003-gvsu-ch12-sec_top_space_exer-true_false-task-03", "source_file": "source/sec_top_space_exer.ptx", "source_line": 605, "prompt_carrier": "atomic_task"},
    {"sequence": 76, "id": "o003-c90-ch12-exer-g-04", "source_anchor": "o003-gvsu-ch12-sec_top_space_exer-true_false-task-04", "source_file": "source/sec_top_space_exer.ptx", "source_line": 615, "prompt_carrier": "atomic_task"},
    {"sequence": 77, "id": "o003-c90-ch12-exer-g-05", "source_anchor": "o003-gvsu-ch12-sec_top_space_exer-true_false-task-05", "source_file": "source/sec_top_space_exer.ptx", "source_line": 624, "prompt_carrier": "atomic_task"},
    {"sequence": 78, "id": "o003-c90-ch12-exer-g-06", "source_anchor": "o003-gvsu-ch12-sec_top_space_exer-true_false-task-06", "source_file": "source/sec_top_space_exer.ptx", "source_line": 636, "prompt_carrier": "atomic_task"},
    {"sequence": 79, "id": "o003-c90-ch12-exer-g-07", "source_anchor": "o003-gvsu-ch12-sec_top_space_exer-true_false-task-07", "source_file": "source/sec_top_space_exer.ptx", "source_line": 644, "prompt_carrier": "atomic_task"},
]

NEW_PROMPTS: list[dict[str, Any]] = [
    {
        "sequence": row["sequence"],
        "id": row["id"],
        "source_anchor": row["source_anchor"],
        "source_anchor_kind": SOURCE_ANCHOR_KIND,
        "authority_source_file": row["source_file"],
        "authority_line": row["source_line"],
        "prompt_carrier": row["prompt_carrier"],
    }
    for row in _NEW_PROMPTS_LEGACY
]

DIRECT_BODY_IDS = {"o003-c90-ch12-guide-11"}
DIRECT_STATEMENT_IDS = {"o003-c90-ch12-guide-20", *(row["id"] for row in NEW_PROMPTS if row["prompt_carrier"] == "direct_statement")}

_GROUPING_NODES_LEGACY = [
    {"id": "o003-gvsu-ch12-act_Basis-group-01", "source_file": "source/sec_base_top.ptx", "source_line": 111, "child_entry_ids": ["o003-c90-ch12-guide-13", "o003-c90-ch12-guide-14", "o003-c90-ch12-guide-15"]},
    {"id": "o003-gvsu-ch12-basis_final_activity-group-01", "source_file": "source/sec_base_top.ptx", "source_line": 298, "child_entry_ids": ["o003-c90-ch12-guide-16", "o003-c90-ch12-guide-17"]},
    {"id": "o003-gvsu-ch12-sec_top_space_exer-coset_f-group-01", "source_file": "source/sec_top_space_exer.ptx", "source_line": 87, "child_entry_ids": ["o003-c90-ch12-exer-a-08", "o003-c90-ch12-exer-a-09", "o003-c90-ch12-exer-a-10"]},
    {"id": "o003-gvsu-ch12-sec_top_space_exer-finite_minimal_basis-group-01", "source_file": "source/sec_top_space_exer.ptx", "source_line": 229, "child_entry_ids": ["o003-c90-ch12-exer-b-08", "o003-c90-ch12-exer-b-09", "o003-c90-ch12-exer-b-10", "o003-c90-ch12-exer-c-01"]},
    {"id": "o003-gvsu-ch12-ex_digital_line_topology-open_sets-group-01", "source_file": "source/sec_top_space_exer.ptx", "source_line": 460, "child_entry_ids": [f"o003-c90-ch12-exer-e-{number:02d}" for number in range(2, 8)]},
]

GROUPING_NODES = [
    {
        "id": row["id"],
        "authority_source_file": row["source_file"],
        "authority_line": row["source_line"],
        "child_entry_ids": row["child_entry_ids"],
    }
    for row in _GROUPING_NODES_LEGACY
]

SCHEMA_RECEIPTS = {
    letter: ROOT / "qa" / f"CHAPTER12_EXERCISE_GUIDES_{letter.upper()}_SCHEMA_QA.json"
    for letter in "abcdefg"
}
WRAPPER_SCHEMA_RECEIPT = ROOT / "qa" / "CHAPTER12_COMPANION_WRAPPER_SCHEMA_QA.json"
MASTERY_SCHEMA_RECEIPT = ROOT / "qa" / "CHAPTER12_MASTERY_SCHEMA_QA.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path: Path) -> dict[str, Any]:
    return {"bytes": path.stat().st_size, "sha256": digest(path)}


def json_bytes(payload: Any) -> bytes:
    """Serialize JSON with stable UTF-8 bytes and LF line endings."""
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def csv_bytes(fieldnames: tuple[str, ...] | list[str], rows: list[dict[str, Any]]) -> bytes:
    """Serialize CSV canonically, independent of the host newline convention."""
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(fieldnames), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def bytes_identity(payload: bytes) -> dict[str, Any]:
    return {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def xml_local_name(element: etree._Element) -> str:
    return etree.QName(element).localname


def resolve_authority_locator(
    record: dict[str, Any],
    *,
    grouping: bool = False,
) -> dict[str, Any]:
    """Resolve one exact carrier in the immutable pinned GVSU authority."""
    entry_id = record.get("id", record.get("entry_id", "<unknown>"))
    source_file = record.get("authority_source_file")
    try:
        line = int(record["authority_line"])
    except (KeyError, TypeError, ValueError) as exc:
        raise SystemExit(f"invalid pinned-authority line for {entry_id}") from exc
    allowed_sources = {f"source/{name}" for name in CHAPTER_SOURCE_FILES}
    if source_file not in allowed_sources:
        raise SystemExit(f"pinned-authority file is outside the Chapter 12 closure for {entry_id}: {source_file}")
    path = PINNED_AUTHORITY_ROOT / source_file
    if not path.is_file():
        raise SystemExit(f"pinned-authority file is missing for {entry_id}: {source_file}")

    parser = etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False)
    document = etree.parse(str(path), parser)
    candidates = [element for element in document.iter() if element.sourceline == line]
    carrier = "grouping_task" if grouping else record.get("prompt_carrier")

    if carrier == "atomic_task":
        matches = [
            element for element in candidates
            if xml_local_name(element) == "task" and not element.xpath(".//task")
        ]
    elif carrier == "direct_body":
        matches = [
            element for element in candidates
            if xml_local_name(element) == "activity" and element.find("p") is not None
        ]
    elif carrier == "direct_statement":
        matches = []
        for element in candidates:
            parent = element.getparent()
            if (
                xml_local_name(element) == "statement"
                and parent is not None
                and xml_local_name(parent) in {"activity", "exercise"}
                and not parent.xpath(".//task")
            ):
                matches.append(element)
    elif carrier == "grouping_task":
        matches = [element for element in candidates if xml_local_name(element) == "task"]
    else:
        raise SystemExit(f"unknown pinned-authority carrier for {entry_id}: {carrier}")

    if len(matches) != 1:
        found = [xml_local_name(element) for element in candidates]
        raise SystemExit(
            f"pinned-authority carrier mismatch for {entry_id}: file={source_file}, "
            f"line={line}, carrier={carrier}, start_tags={found}"
        )
    element = matches[0]
    nearest_xml_id = None
    cursor: etree._Element | None = element
    while cursor is not None:
        nearest_xml_id = cursor.get(XML_ID)
        if nearest_xml_id:
            break
        cursor = cursor.getparent()
    if nearest_xml_id is None:
        raise SystemExit(f"pinned-authority carrier has no ancestor-or-self xml:id for {entry_id}")

    subtree = etree.tostring(
        element,
        method="c14n",
        exclusive=True,
        with_comments=True,
    )
    xpath = document.getpath(element)
    resolved = document.xpath(xpath)
    if len(resolved) != 1 or resolved[0] is not element:
        raise SystemExit(f"pinned-authority XPath is not uniquely resolving for {entry_id}: {xpath}")
    return {
        "authority_commit": FROZEN_AUTHORITY_COMMIT,
        "authority_source_file": source_file,
        "authority_line": line,
        "element_tag": xml_local_name(element),
        "nearest_ancestor_or_self_xml_id": nearest_xml_id,
        "xpath": xpath,
        "subtree_hash_contract": AUTHORITY_SUBTREE_HASH_CONTRACT,
        "subtree_sha256": hashlib.sha256(subtree).hexdigest(),
    }


def validate_authority_locator(
    record: dict[str, Any],
    *,
    grouping: bool = False,
) -> None:
    actual = record.get("authority_locator")
    expected = resolve_authority_locator(record, grouping=grouping)
    if actual != expected:
        entry_id = record.get("id", record.get("entry_id", "<unknown>"))
        raise SystemExit(
            f"pinned-authority locator differs from the exact resolved carrier for {entry_id}: "
            f"expected {expected}, found {actual}"
        )


def canonical_prompt_projection(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{field: row[field] for field in CANONICAL_PROMPT_FIELDS} for row in rows]


def canonical_prompt_identity(rows: list[dict[str, Any]]) -> str:
    payload = json.dumps(
        canonical_prompt_projection(rows),
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def pre_locator_prompt_identity(rows: list[dict[str, Any]]) -> str:
    fields = (
        "sequence",
        "id",
        "source_anchor",
        "authority_source_file",
        "authority_line",
        "prompt_carrier",
    )
    payload = json.dumps(
        [{field: row[field] for field in fields} for row in rows],
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def apply_authority_line_corrections(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    corrected: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["authority_line"] = AUTHORITY_LINE_CORRECTIONS.get(item["sequence"], item["authority_line"])
        corrected.append(item)
    return corrected


def normalize_prompt_row(row: dict[str, Any]) -> dict[str, Any]:
    entry_id = row.get("id", row.get("entry_id"))
    authority_source_file = row.get("authority_source_file", row.get("source_file"))
    authority_line = row.get("authority_line", row.get("source_line"))
    if not entry_id or not authority_source_file or authority_line is None:
        raise SystemExit(f"incomplete canonical prompt row: {row}")
    carrier = row.get("prompt_carrier")
    if not carrier:
        carrier = "direct_body" if entry_id in DIRECT_BODY_IDS else (
            "direct_statement" if entry_id in DIRECT_STATEMENT_IDS else "atomic_task"
        )
    try:
        sequence = int(row["sequence"])
        line = int(authority_line)
    except (KeyError, TypeError, ValueError) as exc:
        raise SystemExit(f"invalid numeric canonical prompt field for {entry_id}") from exc
    locator = row.get("authority_locator")
    if isinstance(locator, str) and locator:
        try:
            locator = json.loads(locator)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"invalid authority_locator JSON for {entry_id}") from exc
    normalized = {
        "sequence": sequence,
        "id": entry_id,
        "source_anchor": row.get("source_anchor"),
        "source_anchor_kind": row.get("source_anchor_kind", SOURCE_ANCHOR_KIND),
        "authority_source_file": authority_source_file,
        "authority_line": line,
        "prompt_carrier": carrier,
    }
    if locator is not None and locator != "":
        if not isinstance(locator, dict):
            raise SystemExit(f"authority_locator is not a structured object for {entry_id}")
        normalized["authority_locator"] = locator
    return normalized


def validate_canonical_prompt_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = [normalize_prompt_row(row) for row in rows]
    if len(normalized) != 79:
        raise SystemExit(f"canonical prompt map must contain 79 rows, found {len(normalized)}")
    sequences = [row["sequence"] for row in normalized]
    if sequences != list(range(1, 80)):
        raise SystemExit("canonical prompt rows are not in exact sequence order 1..79")
    ids = [row["id"] for row in normalized]
    anchors = [row["source_anchor"] for row in normalized]
    if len(set(ids)) != 79 or any(not entry_id for entry_id in ids):
        raise SystemExit("canonical prompt IDs are missing or duplicated")
    if len(set(anchors)) != 79 or any(not anchor for anchor in anchors):
        raise SystemExit("canonical source anchors are missing or duplicated")
    if any(row["source_anchor_kind"] != SOURCE_ANCHOR_KIND for row in normalized):
        raise SystemExit("canonical source anchors are not explicitly synthetic locale-neutral aliases")
    if any(row["prompt_carrier"] not in PROMPT_CARRIERS for row in normalized):
        raise SystemExit("canonical prompt map contains an unknown carrier type")
    carrier_counts = {
        carrier: sum(row["prompt_carrier"] == carrier for row in normalized)
        for carrier in sorted(PROMPT_CARRIERS)
    }
    if carrier_counts != {"atomic_task": 73, "direct_body": 1, "direct_statement": 5}:
        raise SystemExit(f"canonical prompt carrier census changed: {carrier_counts}")
    allowed_sources = {f"source/{name}" for name in CHAPTER_SOURCE_FILES}
    if any(row["authority_source_file"] not in allowed_sources for row in normalized):
        raise SystemExit("canonical prompt map points outside the frozen Chapter 12 authority closure")
    if any(row["authority_line"] <= 0 for row in normalized):
        raise SystemExit("canonical prompt map contains a nonpositive frozen authority line")
    actual_identity = canonical_prompt_identity(normalized)
    if actual_identity != FROZEN_CANONICAL_PROMPT_SHA256:
        raise SystemExit(
            "canonical prompt mapping identity changed: "
            f"expected {FROZEN_CANONICAL_PROMPT_SHA256}, found {actual_identity}"
        )
    prefix_identity = canonical_prompt_identity(normalized[:51])
    if prefix_identity != FROZEN_LEGACY_51_SHA256:
        raise SystemExit(
            "the frozen original 51 prompt mappings changed: "
            f"expected {FROZEN_LEGACY_51_SHA256}, found {prefix_identity}"
        )
    return normalized


def validate_rights_and_provenance(
    manifest: dict[str, Any],
    qa: dict[str, Any],
) -> None:
    """Reject drift in the exact mixed-license, credit, and model boundary."""
    if manifest.get("license") != COMPANION_LICENSE:
        raise SystemExit("manifest companion license differs from the exact CC BY 4.0 contract")
    if manifest.get("provenance") != MANIFEST_PROVENANCE:
        raise SystemExit("manifest model provenance or non-endorsement differs from the exact contract")
    if qa.get("rights_boundary") != QA_RIGHTS_BOUNDARY:
        raise SystemExit("QA mixed-license or non-endorsement boundary differs from the exact contract")
    if qa.get("provenance") != QA_PROVENANCE:
        raise SystemExit("QA model provenance or source/human-credit instruction differs from the exact contract")


def validate_manifest_legacy_prefix(manifest: dict[str, Any]) -> None:
    entries = manifest.get("entries")
    if not isinstance(entries, list) or len(entries) < 51:
        raise SystemExit("manifest no longer contains the frozen original 51 entries")
    prefix = [normalize_prompt_row(entry) for entry in entries[:51]]
    if [row["sequence"] for row in prefix] != list(range(1, 52)):
        raise SystemExit("manifest original 51 entries are not in canonical order")
    if pre_locator_prompt_identity(prefix) == PRE_LOCATOR_LEGACY_51_SHA256:
        prefix = apply_authority_line_corrections(prefix)
    actual_identity = canonical_prompt_identity(prefix)
    if actual_identity != FROZEN_LEGACY_51_SHA256:
        raise SystemExit(
            "manifest original 51 mapping identity changed: "
            f"expected {FROZEN_LEGACY_51_SHA256}, found {actual_identity}"
        )


def load_source_metadata(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    validate_manifest_legacy_prefix(manifest)
    if PROMPT_MAP_PATH.exists():
        with PROMPT_MAP_PATH.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames not in (
                list(PROMPT_MAP_FIELDS),
                list(PRE_LOCATOR_PROMPT_MAP_FIELDS),
                list(LEGACY_PROMPT_MAP_FIELDS),
            ):
                raise SystemExit(
                    "prompt-map columns do not match the frozen authority-line contract: "
                    f"{reader.fieldnames}"
                )
            rows = list(reader)
        normalized = [normalize_prompt_row(row) for row in rows]
        if pre_locator_prompt_identity(normalized) == PRE_LOCATOR_CANONICAL_PROMPT_SHA256:
            normalized = apply_authority_line_corrections(normalized)
        return validate_canonical_prompt_rows(normalized)

    manifest_entries = manifest["entries"]
    if len(manifest_entries) == 51:
        rows = [normalize_prompt_row(entry) for entry in manifest_entries]
        if pre_locator_prompt_identity(rows) == PRE_LOCATOR_LEGACY_51_SHA256:
            rows = apply_authority_line_corrections(rows)
        rows.extend(NEW_PROMPTS)
    elif len(manifest_entries) in (79, 87):
        rows = [normalize_prompt_row(entry) for entry in manifest_entries[:79]]
        if pre_locator_prompt_identity(rows) == PRE_LOCATOR_CANONICAL_PROMPT_SHA256:
            rows = apply_authority_line_corrections(rows)
    else:
        raise SystemExit(
            "without a canonical prompt map, manifest entries must contain exactly "
            "the frozen 51-row prefix, the complete 79-row source mapping, or the "
            "final 87-entry companion mapping"
        )
    return validate_canonical_prompt_rows(rows)


def verify_wrapper() -> list[Path]:
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    doc = etree.parse(str(WRAPPER), parser)
    hrefs = doc.xpath("//xi:include/@href", namespaces={"xi": XI_NS})
    required_hrefs = [f"./{name}" for name in GUIDE_FILES]
    mastery_href = f"./{OPTIONAL_MASTERY_FILE}"
    if hrefs == required_hrefs:
        included_names = list(GUIDE_FILES)
    elif hrefs == required_hrefs + [mastery_href]:
        included_names = [*GUIDE_FILES, OPTIONAL_MASTERY_FILE]
    else:
        raise SystemExit(
            "wrapper XInclude order/closure differs from the required guide sequence; "
            f"found {hrefs}"
        )

    included_paths: list[Path] = []
    companion_root = COMPANION.resolve()
    for name in included_names:
        path = COMPANION / name
        if not path.exists() or path.resolve().parent != companion_root:
            raise SystemExit(f"wrapper include is missing or nonlocal: {name}")
        child = etree.parse(str(path), parser)
        nested = child.xpath("//xi:include/@href", namespaces={"xi": XI_NS})
        if nested:
            raise SystemExit(f"nested XInclude is outside the frozen wrapper closure in {name}: {nested}")
        included_paths.append(path)
    return included_paths


def validate_schema_receipt(
    receipt_path: Path,
    source_path: Path,
    expected_closure: list[Path],
) -> dict[str, Any]:
    if not receipt_path.exists():
        raise SystemExit(f"required schema receipt is missing: {receipt_path.name}")
    payload = json.loads(receipt_path.read_text(encoding="utf-8"))
    if payload.get("status") != "pass" or payload.get("diagnostics") != []:
        raise SystemExit(f"schema receipt is not a clean pass: {receipt_path.name}")
    expected_source = {"path": repo_relative(source_path), **identity(source_path)}
    if payload.get("source") != expected_source:
        raise SystemExit(
            f"schema receipt source identity is stale for {source_path.name}: "
            f"expected {expected_source}, found {payload.get('source')}"
        )
    xinclude = payload.get("xinclude", {})
    expected_paths = [repo_relative(path) for path in expected_closure]
    actual_paths = xinclude.get("closure")
    if (
        xinclude.get("all_local") is not True
        or xinclude.get("closure_file_count") != len(expected_paths)
        or not isinstance(actual_paths, list)
        or len(actual_paths) != len(set(actual_paths))
        or set(actual_paths) != set(expected_paths)
    ):
        raise SystemExit(
            f"schema receipt closure is stale or nonlocal for {receipt_path.name}"
        )
    return {
        "path": f"repo/qa/{receipt_path.name}",
        **identity(receipt_path),
        "status": "pass",
    }


def collect_xml_ids(paths: list[Path]) -> set[str]:
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    owners: dict[str, str] = {}
    for path in paths:
        doc = etree.parse(str(path), parser)
        for element in doc.iter():
            xml_id = element.get(XML_ID)
            if not xml_id:
                continue
            if xml_id in owners:
                raise SystemExit(
                    f"duplicate xml:id {xml_id!r} across {owners[xml_id]} and {path.name}"
                )
            owners[xml_id] = path.name
    return set(owners)


def parse_guides() -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    found: dict[str, dict[str, Any]] = {}
    files: list[dict[str, Any]] = []
    for name in GUIDE_FILES:
        path = COMPANION / name
        if not path.exists():
            raise SystemExit(f"required guide file is missing: {name}")
        doc = etree.parse(str(path), parser)
        document_ids = {element.get(XML_ID) for element in doc.iter() if element.get(XML_ID)}
        files.append({"path": f"repo/companion/{name}", **identity(path)})
        for exercise in doc.xpath("//exercise"):
            entry_id = exercise.get(XML_ID)
            if not entry_id or entry_id in found:
                raise SystemExit(f"missing or duplicate exercise xml:id in {name}: {entry_id}")
            title_node = exercise.find("title")
            title = " ".join("".join(title_node.itertext()).split()) if title_node is not None else entry_id
            statement = exercise.find("statement")
            hint = exercise.find("hint")
            answer = exercise.find("answer")
            solution = exercise.find("solution")
            if any(node is None for node in (statement, hint, answer, solution)):
                raise SystemExit(f"incomplete staged surfaces for {entry_id}")
            expected = {
                "hint": f"{entry_id}-hint",
                "answer": f"{entry_id}-answer",
                "solution": f"{entry_id}-solution",
            }
            actual = {key: node.get(XML_ID) for key, node in (("hint", hint), ("answer", answer), ("solution", solution))}
            if actual != expected:
                raise SystemExit(f"surface IDs do not match contract for {entry_id}: {actual}")
            statement_anchor = statement.get(XML_ID) or entry_id
            surfaces = {
                "statement": statement_anchor,
                "hint": expected["hint"],
                "answer": expected["answer"],
                "solution": expected["solution"],
            }
            if any(surface_id not in document_ids for surface_id in surfaces.values()):
                raise SystemExit(f"one or more surface anchors do not resolve for {entry_id}: {surfaces}")
            found[entry_id] = {
                "title": title,
                "guide_file": f"companion/{name}",
                "surfaces": surfaces,
            }
    return found, files


def parse_mastery(path: Path, companion_ids: set[str]) -> list[dict[str, Any]]:
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    doc = etree.parse(str(path), parser)
    records: list[dict[str, Any]] = []
    for exercise in doc.xpath("//exercise"):
        entry_id = exercise.get(XML_ID)
        if not entry_id:
            raise SystemExit("mastery exercise is missing xml:id")
        statement = exercise.find("statement")
        hint = exercise.find("hint")
        answer = exercise.find("answer")
        solution = exercise.find("solution")
        if any(node is None for node in (statement, hint, answer, solution)):
            raise SystemExit(f"mastery exercise lacks a staged surface: {entry_id}")
        surfaces = {
            "statement": statement.get(XML_ID) or entry_id,
            "hint": hint.get(XML_ID),
            "answer": answer.get(XML_ID),
            "solution": solution.get(XML_ID),
        }
        expected = {
            "statement": statement.get(XML_ID) or entry_id,
            "hint": f"{entry_id}-hint",
            "answer": f"{entry_id}-answer",
            "solution": f"{entry_id}-solution",
        }
        if surfaces != expected or any(surface not in companion_ids for surface in surfaces.values()):
            raise SystemExit(f"mastery surface anchors do not resolve for {entry_id}: {surfaces}")
        title_node = exercise.find("title")
        records.append({
            "id": entry_id,
            "title": " ".join("".join(title_node.itertext()).split()) if title_node is not None else entry_id,
            "surfaces": surfaces,
        })
    ids = tuple(record["id"] for record in records)
    if ids != FROZEN_MASTERY_IDS:
        raise SystemExit(
            "integrated mastery IDs/order differ from the frozen eight-entry contract: "
            f"{ids}"
        )
    for offset, record in enumerate(records, start=80):
        record.update({
            "sequence": offset,
            "entry_type": MASTERY_ENTRY_TYPE,
            "license": COMPANION_LICENSE,
            "origin": "original_companion_content",
            "companion_file": f"companion/{path.name}",
            "companion_anchor": record["id"],
        })
    return records


OUTPUT_TARGETS = (
    PROMPT_MAP_PATH,
    GROUPING_PATH,
    MANIFEST_PATH,
    QA_PATH,
    ALIASES_PATH,
)


def stage_path(target: Path) -> Path:
    return target.with_name(f".{target.name}.chapter12-refresh-stage")


def ensure_clean_transaction_state() -> None:
    stale = [path for path in (TRANSACTION_MARKER, *(stage_path(path) for path in OUTPUT_TARGETS)) if path.exists()]
    marker_replacement = TRANSACTION_MARKER.with_name(f".{TRANSACTION_MARKER.name}.replacement")
    if marker_replacement.exists():
        stale.append(marker_replacement)
    if stale:
        rendered = ", ".join(str(path) for path in stale)
        raise SystemExit(
            "an interrupted Chapter 12 refresh requires explicit inspection before retry: "
            f"{rendered}"
        )


def durable_write_new(path: Path, payload: bytes) -> None:
    with path.open("xb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())


def replace_marker(payload: dict[str, Any]) -> None:
    replacement = TRANSACTION_MARKER.with_name(f".{TRANSACTION_MARKER.name}.replacement")
    durable_write_new(replacement, json_bytes(payload))
    os.replace(replacement, TRANSACTION_MARKER)


def parse_csv_payload(payload: bytes) -> tuple[list[str] | None, list[dict[str, str]]]:
    reader = csv.DictReader(io.StringIO(payload.decode("utf-8"), newline=""))
    return reader.fieldnames, list(reader)


def verify_generated_payloads(
    payloads: dict[Path, bytes],
    *,
    source_rows: list[dict[str, Any]],
    prompt_rows: list[dict[str, Any]],
    grouping_payload: dict[str, Any],
    entries: list[dict[str, Any]],
    qa_entries: list[dict[str, Any]],
    alias_rows: list[dict[str, Any]],
    mastery_records: list[dict[str, Any]],
    companion_ids: set[str],
    ids_disjoint: bool,
    staged_surfaces_complete: bool,
    schema_validation: dict[str, dict[str, Any]],
    historical_partial_identities: dict[Path, dict[str, Any]],
) -> None:
    missing_payloads = [str(path) for path in OUTPUT_TARGETS if path not in payloads]
    if missing_payloads:
        raise SystemExit(f"cross-file verifier is missing payloads: {missing_payloads}")
    if any(path in OUTPUT_TARGETS for path in HISTORICAL_PARTIAL_PATHS):
        raise SystemExit("historical partial artifacts must never be refresh targets")
    if (
        MANIFEST_PATH.name != "chapter_12_companion_manifest.json"
        or QA_PATH.name != "CHAPTER12_COMPANION_QA.json"
        or ALIASES_PATH.name != "chapter_12_entry_aliases.csv"
    ):
        raise SystemExit("final companion output paths differ from the frozen naming contract")
    for path, expected_identity in historical_partial_identities.items():
        if not path.exists() or identity(path) != expected_identity:
            raise SystemExit(f"historical read-only artifact changed during refresh: {path.name}")

    prompt_fields, parsed_prompt_rows = parse_csv_payload(payloads[PROMPT_MAP_PATH])
    if prompt_fields != list(PROMPT_MAP_FIELDS) or payloads[PROMPT_MAP_PATH] != csv_bytes(PROMPT_MAP_FIELDS, prompt_rows):
        raise SystemExit("generated prompt map is not the canonical deterministic CSV")
    parsed_canonical = validate_canonical_prompt_rows(parsed_prompt_rows)
    if parsed_canonical != source_rows:
        raise SystemExit("generated prompt map differs from the frozen canonical source mapping")
    for row in parsed_canonical:
        validate_authority_locator(row)

    parsed_grouping = json.loads(payloads[GROUPING_PATH].decode("utf-8"))
    if parsed_grouping != grouping_payload:
        raise SystemExit("generated grouping JSON differs from the verified grouping payload")
    for group in parsed_grouping.get("nodes", []):
        if group.get("anchor_kind") != SOURCE_ANCHOR_KIND:
            raise SystemExit(f"grouping-node anchor is not explicitly synthetic: {group.get('id')}")
        validate_authority_locator(group, grouping=True)

    parsed_manifest = json.loads(payloads[MANIFEST_PATH].decode("utf-8"))
    parsed_qa = json.loads(payloads[QA_PATH].decode("utf-8"))
    validate_rights_and_provenance(parsed_manifest, parsed_qa)
    alias_fields, parsed_alias_rows = parse_csv_payload(payloads[ALIASES_PATH])
    alias_fieldnames = list(ALIAS_FIELDS)
    if alias_fields != alias_fieldnames or payloads[ALIASES_PATH] != csv_bytes(alias_fieldnames, alias_rows):
        raise SystemExit("generated alias map is not the canonical deterministic CSV")

    source_entries = entries[:79]
    mastery_entries = entries[79:]
    if len(mastery_entries) != 8:
        raise SystemExit("final companion boundary must contain exactly eight original mastery entries")
    covered = len(source_entries)
    pending = 79 - covered
    expected_status = "companion_complete_reader_admission_pending"
    if parsed_manifest.get("status") != expected_status or parsed_qa.get("status") != expected_status:
        raise SystemExit("manifest and QA status disagree with computed source-prompt coverage")
    if parsed_qa.get("companion_complete") is not True or parsed_qa.get("reader_admission_pending") is not True:
        raise SystemExit("final QA does not distinguish complete companion content from pending reader admission")
    if parsed_manifest.get("partial") is not False:
        raise SystemExit("final companion manifest must be explicitly non-partial")
    if (
        parsed_manifest.get("companion_complete") is not True
        or parsed_manifest.get("reader_admission_pending") is not True
    ):
        raise SystemExit(
            "final companion manifest must mark the companion complete while preserving "
            "the pending reader-admission gate"
        )
    if len(entries) != 87 or len(qa_entries) != 87 or len(alias_rows) != 87:
        raise SystemExit("final companion boundary must contain exactly 87 entries and aliases")
    if [entry["sequence"] for entry in entries] != list(range(1, 88)):
        raise SystemExit("final companion entries are not in exact stable sequence order 1..87")
    if any(
        entry.get("entry_type") != SOURCE_GUIDE_ENTRY_TYPE
        or entry.get("license") != COMPANION_LICENSE
        for entry in source_entries
    ):
        raise SystemExit("one or more source-guide entries lacks its explicit type or CC BY 4.0 identity")
    if [
        (
            entry.get("sequence"),
            entry.get("id"),
            entry.get("source_anchor"),
            entry.get("source_anchor_kind"),
            entry.get("authority_source_file"),
            entry.get("authority_line"),
            entry.get("prompt_carrier"),
            entry.get("authority_locator"),
        )
        for entry in source_entries
    ] != [
        (
            row["sequence"],
            row["id"],
            row["source_anchor"],
            row["source_anchor_kind"],
            row["authority_source_file"],
            row["authority_line"],
            row["prompt_carrier"],
            row["authority_locator"],
        )
        for row in source_rows
    ]:
        raise SystemExit("source-guide entries differ from the frozen 79-row authority mapping")
    if [entry["id"] for entry in mastery_entries] != list(FROZEN_MASTERY_IDS):
        raise SystemExit("final mastery entries differ from the frozen IDs/order 80..87")
    if any(
        entry.get("entry_type") != MASTERY_ENTRY_TYPE
        or entry.get("license") != COMPANION_LICENSE
        or "source_anchor" in entry
        or "source_anchor_kind" in entry
        or "authority_source_file" in entry
        or "authority_line" in entry
        or "authority_locator" in entry
        for entry in mastery_entries
    ):
        raise SystemExit("mastery entries have false upstream provenance or missing CC BY 4.0 identity")
    expected_mastery_entries = [
        {
            "sequence": record["sequence"],
            "id": record["id"],
            "entry_type": record["entry_type"],
            "license": record["license"],
            "origin": record["origin"],
            "companion_file": record["companion_file"],
            "companion_anchor": record["companion_anchor"],
            "surfaces": record["surfaces"],
        }
        for record in mastery_records
    ]
    if mastery_entries != expected_mastery_entries:
        raise SystemExit("mastery manifest entries differ from the actual integrated exercises and surfaces")
    if any(
        entry.get("entry_type") != MASTERY_ENTRY_TYPE
        or entry.get("license") != COMPANION_LICENSE
        or "source_anchor" in entry
        or "source_anchor_kind" in entry
        or "authority_source_file" in entry
        or "authority_line" in entry
        or "authority_locator" in entry
        for entry in qa_entries[79:]
    ):
        raise SystemExit("mastery QA entries have false upstream provenance or missing CC BY 4.0 identity")
    if any(
        row.get("entry_type") != MASTERY_ENTRY_TYPE
        or row.get("license") != COMPANION_LICENSE
        or row.get("source_anchor") != ""
        or row.get("companion_anchor") != row.get("entry_id")
        or row.get("statement_id") != row.get("entry_id")
        for row in alias_rows[79:]
    ):
        raise SystemExit("mastery alias rows have false source anchors or nonresolving statement anchors")
    if parsed_manifest.get("entries") != entries or parsed_qa.get("entries") != qa_entries:
        raise SystemExit("manifest or QA entries differ from the verified guide/source join")
    if parsed_alias_rows != [{key: str(value) for key, value in row.items()} for row in alias_rows]:
        raise SystemExit("alias rows differ from the verified staged surfaces")

    prompt_identity = bytes_identity(payloads[PROMPT_MAP_PATH])
    grouping_identity = bytes_identity(payloads[GROUPING_PATH])
    alias_identity = bytes_identity(payloads[ALIASES_PATH])
    if parsed_manifest.get("prompt_map") != {"path": "backend/chapter_12_source_prompt_map.csv", **prompt_identity}:
        raise SystemExit("manifest prompt-map identity is internally inconsistent")
    expected_grouping_backend = {
        "path": "backend/chapter_12_grouping_nodes.json",
        **grouping_identity,
        "node_count": len(GROUPING_NODES),
        "all_children_resolve": grouping_payload["all_children_resolve"],
    }
    if parsed_manifest.get("grouping_backend") != expected_grouping_backend:
        raise SystemExit("manifest grouping identity is internally inconsistent")
    if parsed_manifest.get("aliases") != {"path": "backend/chapter_12_entry_aliases.csv", **alias_identity}:
        raise SystemExit("manifest alias identity is internally inconsistent")
    expected_qa_backend = {
        "prompt_map": {"path": "repo/backend/chapter_12_source_prompt_map.csv", **prompt_identity},
        "grouping_nodes": {"path": "repo/backend/chapter_12_grouping_nodes.json", **grouping_identity},
        "aliases": {"path": "repo/backend/chapter_12_entry_aliases.csv", **alias_identity},
    }
    if parsed_qa.get("backend") != expected_qa_backend:
        raise SystemExit("QA backend identities are internally inconsistent")

    included_paths = verify_wrapper()
    current_companion_ids = collect_xml_ids([WRAPPER, *included_paths])
    current_source_ids = collect_xml_ids([ROOT / "source" / name for name in CHAPTER_SOURCE_FILES])
    if current_companion_ids != companion_ids:
        raise SystemExit("companion XML-ID closure changed during refresh verification")
    if current_source_ids.isdisjoint(current_companion_ids) is not ids_disjoint:
        raise SystemExit("source/companion ID-disjointness changed during refresh verification")
    expected_guide_hashes = {
        f"companion/{path.name}": digest(path)
        for path in [*included_paths, WRAPPER]
    }
    manifest_companion = parsed_manifest.get("companion", {})
    if manifest_companion.get("qa") != "repo/qa/CHAPTER12_COMPANION_QA.json":
        raise SystemExit("manifest points to a nonfinal companion QA artifact")
    if manifest_companion.get("guide_files") != [f"companion/{name}" for name in GUIDE_FILES]:
        raise SystemExit("manifest guide-file order differs from the verified required sequence")
    if manifest_companion.get("wrapper_includes") != [f"companion/{path.name}" for path in included_paths]:
        raise SystemExit("manifest wrapper closure differs from the verified XInclude closure")
    if manifest_companion.get("guide_file_sha256") != expected_guide_hashes:
        raise SystemExit("manifest companion hashes differ from the current verified files")
    mastery_paths = [path for path in included_paths if path.name == OPTIONAL_MASTERY_FILE]
    expected_mastery = (
        {
            "path": f"companion/{mastery_paths[0].name}",
            **identity(mastery_paths[0]),
            "entry_type": MASTERY_ENTRY_TYPE,
            "license": COMPANION_LICENSE,
            "check_count": len(mastery_records),
            "staged_surface_count": len(mastery_records) * 4,
        }
        if mastery_paths
        else None
    )
    if manifest_companion.get("mastery") != expected_mastery:
        raise SystemExit("manifest mastery identity or count is internally inconsistent")
    expected_companion_files = [
        {"path": f"repo/companion/{name}", **identity(COMPANION / name)}
        for name in GUIDE_FILES
    ]
    expected_companion_files.extend(
        {"path": f"repo/companion/{path.name}", **identity(path)} for path in mastery_paths
    )
    expected_companion_files.append({"path": f"repo/{repo_relative(WRAPPER)}", **identity(WRAPPER)})
    if parsed_qa.get("companion_files") != expected_companion_files:
        raise SystemExit("QA companion-file identities differ from the verified wrapper closure")

    current_schema_validation: dict[str, dict[str, Any]] = {}
    for letter, receipt in SCHEMA_RECEIPTS.items():
        guide_path = COMPANION / f"chapter_12_exercise_guides_{letter}.ptx"
        current_schema_validation[f"exercise_guides_{letter}"] = validate_schema_receipt(
            receipt,
            guide_path,
            [guide_path],
        )
    current_schema_validation["companion_wrapper"] = validate_schema_receipt(
        WRAPPER_SCHEMA_RECEIPT,
        WRAPPER,
        [WRAPPER, *included_paths],
    )
    if mastery_paths:
        current_schema_validation["mastery"] = validate_schema_receipt(
            MASTERY_SCHEMA_RECEIPT,
            mastery_paths[0],
            [mastery_paths[0]],
        )
    if current_schema_validation != schema_validation:
        raise SystemExit("schema-receipt evidence changed during refresh verification")

    coverage = parsed_manifest.get("coverage_contract", {})
    qa_coverage = parsed_qa.get("coverage", {})
    if coverage.get("covered_source_prompt_guides") != covered or coverage.get("pending_source_prompt_guides") != pending:
        raise SystemExit("manifest coverage counts are internally inconsistent")
    if coverage.get("covered_mastery_checks") != len(mastery_records):
        raise SystemExit("manifest mastery count is internally inconsistent")
    if (
        coverage.get("total_companion_entries") != 87
        or coverage.get("total_staged_surfaces") != 348
        or coverage.get("source_prompt_map_rows") != 79
        or coverage.get("companion_complete") is not True
        or coverage.get("reader_admission_pending") is not True
    ):
        raise SystemExit("manifest final-boundary totals/status are internally inconsistent")
    if qa_coverage.get("source_prompt_guides") != covered or qa_coverage.get("source_prompt_guides_pending") != pending:
        raise SystemExit("QA coverage counts are internally inconsistent")
    if qa_coverage.get("mastery_checks") != len(mastery_records):
        raise SystemExit("QA mastery count is internally inconsistent")
    if qa_coverage.get("covered_surfaces", {}).get("total") != covered * 4:
        raise SystemExit("QA staged-surface count is internally inconsistent")
    if (
        qa_coverage.get("mastery_surfaces", {}).get("total") != 32
        or qa_coverage.get("total_companion_entries") != 87
        or qa_coverage.get("total_staged_surfaces") != 348
    ):
        raise SystemExit("QA final companion totals are internally inconsistent")

    surface_ids = {surface for entry in entries for surface in entry["surfaces"].values()}
    if not surface_ids.issubset(companion_ids):
        raise SystemExit("one or more generated surface aliases do not resolve to actual companion XML IDs")
    mastery_surface_ids = {
        surface for record in mastery_records for surface in record["surfaces"].values()
    }
    if not mastery_surface_ids.issubset(companion_ids):
        raise SystemExit("one or more mastery surface anchors do not resolve")
    validation = parsed_qa.get("validation", {})
    if validation.get("all_covered_entries_have_statement_hint_answer_solution") is not staged_surfaces_complete:
        raise SystemExit("computed staged-surface validation boolean is inconsistent")
    if validation.get("source_and_companion_ids_are_disjoint") is not ids_disjoint:
        raise SystemExit("computed source/companion ID-disjointness boolean is inconsistent")
    if validation.get("schema_validation") != schema_validation:
        raise SystemExit("QA schema evidence differs from the verified receipt identities")
    if validation.get("complete_companion_boundary") is not True or validation.get("complete_reader_boundary") is not False:
        raise SystemExit("QA companion/readership boundary status is internally inconsistent")

    if parsed_manifest.get("authority", {}).get("canonical_prompt_mapping_sha256") != FROZEN_CANONICAL_PROMPT_SHA256:
        raise SystemExit("manifest does not identify the frozen canonical prompt mapping")
    if any("source_line" in entry or "source_file" in entry for entry in entries):
        raise SystemExit("legacy ambiguous source-line fields survived in generated entries")
    if grouping_payload.get("grouping_node_count") != len(GROUPING_NODES):
        raise SystemExit("grouping-node count is internally inconsistent")


def stage_and_commit(
    payloads: dict[Path, bytes],
    verifier: Any,
) -> dict[Path, bytes]:
    marker_payload = {
        "schema_version": 1,
        "transaction": "chapter12_companion_state_refresh",
        "phase": "staging",
        "canonical_prompt_mapping_sha256": FROZEN_CANONICAL_PROMPT_SHA256,
        "targets": [
            {
                "target": repo_relative(target),
                "stage": repo_relative(stage_path(target)),
                **bytes_identity(payloads[target]),
            }
            for target in OUTPUT_TARGETS
        ],
    }
    durable_write_new(TRANSACTION_MARKER, json_bytes(marker_payload))
    for target in OUTPUT_TARGETS:
        durable_write_new(stage_path(target), payloads[target])

    staged_payloads = {target: stage_path(target).read_bytes() for target in OUTPUT_TARGETS}
    verifier(staged_payloads)
    marker_payload["phase"] = "committing"
    replace_marker(marker_payload)
    for target in OUTPUT_TARGETS:
        os.replace(stage_path(target), target)

    final_payloads = {target: target.read_bytes() for target in OUTPUT_TARGETS}
    verifier(final_payloads)
    TRANSACTION_MARKER.unlink()
    return final_payloads


def main() -> int:
    ensure_clean_transaction_state()
    manifest_template = MANIFEST_PATH if MANIFEST_PATH.exists() else PARTIAL_MANIFEST_PATH
    qa_template = QA_PATH if QA_PATH.exists() else PARTIAL_QA_PATH
    if not manifest_template.exists() or not qa_template.exists():
        raise SystemExit("neither final nor historical read-only companion templates are available")
    # Historical partial witnesses are protected when present in a development
    # checkout, but the compact release source package intentionally omits
    # them. Final templates are sufficient to reproduce the current backend.
    historical_partial_identities = {
        path: identity(path) for path in HISTORICAL_PARTIAL_PATHS if path.exists()
    }
    manifest = json.loads(manifest_template.read_text(encoding="utf-8"))
    qa = json.loads(qa_template.read_text(encoding="utf-8"))
    source_rows = load_source_metadata(manifest)
    source_rows = [
        {**row, "authority_locator": resolve_authority_locator(row)}
        for row in source_rows
    ]
    included_paths = verify_wrapper()
    guides, companion_files = parse_guides()
    expected_ids = {row["id"] for row in source_rows}
    if set(guides) != expected_ids:
        missing = sorted(expected_ids - set(guides))
        unexpected = sorted(set(guides) - expected_ids)
        raise SystemExit(f"guide/source closure mismatch; missing={missing}, unexpected={unexpected}")

    companion_closure = [WRAPPER, *included_paths]
    companion_ids = collect_xml_ids(companion_closure)
    optional_files = [path for path in included_paths if path.name == OPTIONAL_MASTERY_FILE]
    if len(optional_files) != 1:
        raise SystemExit("final companion boundary requires the explicitly integrated chapter_12_mastery.ptx")
    mastery_records = parse_mastery(optional_files[0], companion_ids)
    source_paths = [ROOT / "source" / name for name in CHAPTER_SOURCE_FILES]
    missing_sources = [str(path) for path in source_paths if not path.exists()]
    if missing_sources:
        raise SystemExit(f"translated Chapter 12 source closure is incomplete: {missing_sources}")
    source_ids = collect_xml_ids(source_paths)
    ids_disjoint = source_ids.isdisjoint(companion_ids)
    if not ids_disjoint:
        raise SystemExit(f"source and companion XML IDs collide: {sorted(source_ids & companion_ids)}")

    surface_keys = ("statement", "hint", "answer", "solution")
    staged_surfaces_complete = all(
        tuple(guide["surfaces"]) == surface_keys
        and all(surface_id in companion_ids for surface_id in guide["surfaces"].values())
        for guide in guides.values()
    ) and len(mastery_records) == 8 and all(
        tuple(record["surfaces"]) == surface_keys
        and all(surface_id in companion_ids for surface_id in record["surfaces"].values())
        for record in mastery_records
    )
    if not staged_surfaces_complete:
        raise SystemExit("not every covered guide has four resolving staged-surface anchors")

    schema_validation: dict[str, dict[str, Any]] = {}
    for letter, receipt in SCHEMA_RECEIPTS.items():
        source_path = COMPANION / f"chapter_12_exercise_guides_{letter}.ptx"
        schema_validation[f"exercise_guides_{letter}"] = validate_schema_receipt(
            receipt,
            source_path,
            [source_path],
        )
    schema_validation["companion_wrapper"] = validate_schema_receipt(
        WRAPPER_SCHEMA_RECEIPT,
        WRAPPER,
        companion_closure,
    )
    mastery_path = optional_files[0]
    schema_validation["mastery"] = validate_schema_receipt(
        MASTERY_SCHEMA_RECEIPT,
        mastery_path,
        [mastery_path],
    )

    parent_by_child: dict[str, str] = {}
    grouping_ids: set[str] = set()
    for group in GROUPING_NODES:
        if group["id"] in grouping_ids:
            raise SystemExit(f"duplicate grouping-node ID: {group['id']}")
        grouping_ids.add(group["id"])
        for child in group["child_entry_ids"]:
            if child in parent_by_child:
                raise SystemExit(f"prompt {child} is assigned to more than one grouping node")
            parent_by_child[child] = group["id"]
    all_group_children_resolve = all(child in expected_ids and child in guides for child in parent_by_child)
    if not all_group_children_resolve:
        raise SystemExit("one or more grouping-node children do not resolve to canonical covered prompts")

    prompt_rows = [
        {
            "sequence": row["sequence"],
            "entry_id": row["id"],
            "source_anchor": row["source_anchor"],
            "source_anchor_kind": row["source_anchor_kind"],
            "authority_source_file": row["authority_source_file"],
            "authority_line": row["authority_line"],
            "prompt_carrier": row["prompt_carrier"],
            "authority_locator": json.dumps(
                row["authority_locator"],
                ensure_ascii=False,
                separators=(",", ":"),
            ),
            "parent_group_anchor": parent_by_child.get(row["id"], ""),
            "support_status": "covered" if row["id"] in guides else "pending",
        }
        for row in source_rows
    ]
    grouping_nodes = [
        {
            **group,
            "anchor_kind": SOURCE_ANCHOR_KIND,
            "authority_locator": resolve_authority_locator(group, grouping=True),
        }
        for group in GROUPING_NODES
    ]
    prompt_payload = csv_bytes(PROMPT_MAP_FIELDS, prompt_rows)
    grouping_payload = {
        "schema_version": 1,
        "unit": "o003-c90-ch12-topological-spaces",
        "locator_contract": {
            "authority_commit": FROZEN_AUTHORITY_COMMIT,
            "file_field": "authority_source_file",
            "line_field": "authority_line",
            "anchor_kind": SOURCE_ANCHOR_KIND,
            "xpath_field": "authority_locator.xpath",
            "subtree_hash_contract": AUTHORITY_SUBTREE_HASH_CONTRACT,
        },
        "grouping_node_count": len(GROUPING_NODES),
        "all_children_resolve": all_group_children_resolve,
        "nodes": grouping_nodes,
    }
    grouping_bytes_payload = json_bytes(grouping_payload)

    source_entries: list[dict[str, Any]] = []
    source_qa_entries: list[dict[str, Any]] = []
    for row in source_rows:
        guide = guides[row["id"]]
        source_entries.append({
            "sequence": row["sequence"],
            "id": row["id"],
            "entry_type": SOURCE_GUIDE_ENTRY_TYPE,
            "license": COMPANION_LICENSE,
            "source_anchor": row["source_anchor"],
            "source_anchor_kind": row["source_anchor_kind"],
            "authority_source_file": row["authority_source_file"],
            "authority_line": row["authority_line"],
            "prompt_carrier": row["prompt_carrier"],
            "authority_locator": row["authority_locator"],
            "parent_group_anchor": parent_by_child.get(row["id"]),
            "companion_file": guide["guide_file"],
            "companion_anchor": row["id"],
            "surfaces": guide["surfaces"],
        })
        source_qa_entries.append({
            "sequence": row["sequence"],
            "id": row["id"],
            "entry_type": SOURCE_GUIDE_ENTRY_TYPE,
            "license": COMPANION_LICENSE,
            "source_anchor": row["source_anchor"],
            "source_anchor_kind": row["source_anchor_kind"],
            "authority_source_file": row["authority_source_file"],
            "authority_line": row["authority_line"],
            "prompt_carrier": row["prompt_carrier"],
            "authority_locator": row["authority_locator"],
            "companion_file": guide["guide_file"],
            "companion_anchor": row["id"],
            "title": guide["title"],
            "surfaces": list(guide["surfaces"].values()),
        })

    mastery_entries = [
        {
            "sequence": record["sequence"],
            "id": record["id"],
            "entry_type": record["entry_type"],
            "license": record["license"],
            "origin": record["origin"],
            "companion_file": record["companion_file"],
            "companion_anchor": record["companion_anchor"],
            "surfaces": record["surfaces"],
        }
        for record in mastery_records
    ]
    mastery_qa_entries = [
        {
            "sequence": record["sequence"],
            "id": record["id"],
            "entry_type": record["entry_type"],
            "license": record["license"],
            "origin": record["origin"],
            "companion_file": record["companion_file"],
            "companion_anchor": record["companion_anchor"],
            "title": record["title"],
            "surfaces": list(record["surfaces"].values()),
        }
        for record in mastery_records
    ]
    entries = [*source_entries, *mastery_entries]
    qa_entries = [*source_qa_entries, *mastery_qa_entries]

    alias_fieldnames = list(ALIAS_FIELDS)
    alias_rows = [
        {
            "sequence": entry["sequence"],
            "entry_id": entry["id"],
            "entry_type": entry["entry_type"],
            "license": entry["license"],
            "source_anchor": entry.get("source_anchor", ""),
            "companion_anchor": entry["companion_anchor"],
            "statement_id": entry["surfaces"]["statement"],
            "hint_id": entry["surfaces"]["hint"],
            "answer_id": entry["surfaces"]["answer"],
            "solution_id": entry["surfaces"]["solution"],
            "status": "staged_support_complete",
        }
        for entry in entries
    ]
    aliases_payload = csv_bytes(alias_fieldnames, alias_rows)

    covered = len(source_entries)
    pending = 79 - covered
    source_qa = ROOT / "qa" / "CHAPTER12_SOURCE_QA.json"
    corrections = LANE / "00_control" / "SOURCE_CORRECTIONS.csv"
    audit = LANE / "00_control" / "CHAPTER12_AUTHORITY_AUDIT.md"
    correction_ids = []
    with corrections.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("unit") == "chapter_12_topological_spaces":
                correction_ids.append(row["id"])

    authority = {
        "audit": "00_control/CHAPTER12_AUTHORITY_AUDIT.md",
        "audit_sha256": digest(audit),
        "commit": FROZEN_AUTHORITY_COMMIT,
        "ordered_sha256": "dde360d7ec1d62d22d5a5afdbaad2055665d57b67e2b4aac6ae43636b84fda47",
        "canonical_prompt_mapping_sha256": FROZEN_CANONICAL_PROMPT_SHA256,
        "line_locator_contract": {
            "authority_root": f"authority/gvsu-pinned/topology-{FROZEN_AUTHORITY_COMMIT}",
            "file_field": "authority_source_file",
            "line_field": "authority_line",
            "source_anchor_kind": SOURCE_ANCHOR_KIND,
            "structured_locator_field": "authority_locator",
            "subtree_hash_contract": AUTHORITY_SUBTREE_HASH_CONTRACT,
            "meaning": "one-based exact carrier-start line in the pinned authority source at the stated commit",
        },
        "source_file_count": 9,
        "source_prompt_total": 79,
        "atomic_prompt_total": 73,
        "direct_prompt_total": 6,
        "grouping_node_total": 5,
    }
    source_corrections = {
        "path": "00_control/SOURCE_CORRECTIONS.csv",
        "sha256": digest(corrections),
        "chapter12_ids": correction_ids,
    }

    status = "companion_complete_reader_admission_pending"
    manifest["status"] = status
    manifest["partial"] = False
    manifest["license"] = COMPANION_LICENSE
    manifest["companion_complete"] = True
    manifest["reader_admission_pending"] = True
    manifest["provenance"] = dict(MANIFEST_PROVENANCE)
    manifest["authority"] = authority
    manifest["companion"]["guide_files"] = [f"companion/{name}" for name in GUIDE_FILES]
    manifest["companion"]["qa"] = "repo/qa/CHAPTER12_COMPANION_QA.json"
    manifest["companion"]["wrapper_includes"] = [f"companion/{path.name}" for path in included_paths]
    manifest["companion"]["guide_file_sha256"] = {
        f"companion/{path.name}": digest(path)
        for path in [*included_paths, WRAPPER]
    }
    manifest["companion"]["mastery"] = {
        "path": f"companion/{optional_files[0].name}",
        **identity(optional_files[0]),
        "entry_type": MASTERY_ENTRY_TYPE,
        "license": COMPANION_LICENSE,
        "check_count": len(mastery_records),
        "staged_surface_count": len(mastery_records) * 4,
    }
    manifest["source_corrections"] = {
        "path": source_corrections["path"],
        "sha256": source_corrections["sha256"],
        "ids": correction_ids,
    }
    manifest["coverage_contract"] = {
        "covered_source_prompt_guides": covered,
        "pending_source_prompt_guides": pending,
        "covered_mastery_checks": len(mastery_records),
        "total_companion_entries": len(entries),
        "total_staged_surfaces": len(entries) * 4,
        "source_prompt_map_rows": len(source_rows),
        "companion_complete": True,
        "reader_admission_pending": True,
        "required_surfaces_per_entry": list(surface_keys),
        "complete_boundary_required": True,
    }
    manifest["prompt_map"] = {"path": "backend/chapter_12_source_prompt_map.csv", **bytes_identity(prompt_payload)}
    manifest["grouping_backend"] = {
        "path": "backend/chapter_12_grouping_nodes.json",
        **bytes_identity(grouping_bytes_payload),
        "node_count": len(GROUPING_NODES),
        "all_children_resolve": all_group_children_resolve,
    }
    manifest["aliases"] = {"path": "backend/chapter_12_entry_aliases.csv", **bytes_identity(aliases_payload)}
    manifest["entries"] = entries

    source_qa_payload = json.loads(source_qa.read_text(encoding="utf-8"))
    if source_qa_payload.get("status") != "pass":
        raise SystemExit("Chapter 12 source QA is not a pass")
    qa["status"] = status
    qa["companion_complete"] = True
    qa["reader_admission_pending"] = True
    qa["rights_boundary"] = dict(QA_RIGHTS_BOUNDARY)
    qa["provenance"] = dict(QA_PROVENANCE)
    qa["authority"] = authority
    qa["source_qa"] = {"path": "repo/qa/CHAPTER12_SOURCE_QA.json", **identity(source_qa), "status": "pass"}
    qa["source_corrections"] = source_corrections
    qa["companion_files"] = companion_files + [
        {"path": f"repo/companion/{path.name}", **identity(path)} for path in optional_files
    ] + [{"path": "repo/companion/chapter_12_topological_spaces_self_study.ptx", **identity(WRAPPER)}]
    qa["coverage"] = {
        "source_prompt_guides": covered,
        "source_prompt_guides_pending": pending,
        "mastery_checks": len(mastery_records),
        "mastery_checks_pending": 0,
        "mastery_surfaces": {
            "statement": len(mastery_records),
            "hint": len(mastery_records),
            "answer": len(mastery_records),
            "solution": len(mastery_records),
            "total": len(mastery_records) * 4,
        },
        "covered_source_context": ["sec_top_space_intro", "act_TS_limits1", "act_top_basis", "act_Basis", "basis_final_activity", "sec_metric_top_space", "sec_neighborhood_top_space", "sec_interior_set_top", "sec_top_space_exer"],
        "covered_atomic_prompt_units": sum(row["prompt_carrier"] == "atomic_task" and row["id"] in guides for row in source_rows),
        "covered_direct_prompt_units": sum(row["prompt_carrier"] != "atomic_task" and row["id"] in guides for row in source_rows),
        "covered_grouping_prompt_units": 0,
        "grouping_nodes_mapped": len(GROUPING_NODES),
        "covered_surfaces": {"statement": covered, "hint": covered, "answer": covered, "solution": covered, "total": covered * 4},
        "total_companion_entries": len(entries),
        "total_staged_surfaces": len(entries) * 4,
    }
    qa["entries"] = qa_entries
    qa.setdefault("validation", {})["schema_validation"] = schema_validation
    qa["validation"].update({
        "all_covered_entries_have_statement_hint_answer_solution": staged_surfaces_complete,
        "source_and_companion_ids_are_disjoint": ids_disjoint,
        "complete_companion_boundary": True,
        "complete_reader_boundary": False,
        "cumulative_build": "not run; reader admission still requires a cumulative build",
        "blocking_gaps": ["complete cumulative HTML/PDF build and reader admission remain pending"],
    })
    qa["backend"] = {
        "prompt_map": {"path": "repo/backend/chapter_12_source_prompt_map.csv", **bytes_identity(prompt_payload)},
        "grouping_nodes": {"path": "repo/backend/chapter_12_grouping_nodes.json", **bytes_identity(grouping_bytes_payload)},
        "aliases": {"path": "repo/backend/chapter_12_entry_aliases.csv", **bytes_identity(aliases_payload)},
    }

    payloads = {
        PROMPT_MAP_PATH: prompt_payload,
        GROUPING_PATH: grouping_bytes_payload,
        MANIFEST_PATH: json_bytes(manifest),
        QA_PATH: json_bytes(qa),
        ALIASES_PATH: aliases_payload,
    }
    verifier_arguments = {
        "source_rows": source_rows,
        "prompt_rows": prompt_rows,
        "grouping_payload": grouping_payload,
        "entries": entries,
        "qa_entries": qa_entries,
        "alias_rows": alias_rows,
        "mastery_records": mastery_records,
        "companion_ids": companion_ids,
        "ids_disjoint": ids_disjoint,
        "staged_surfaces_complete": staged_surfaces_complete,
        "schema_validation": schema_validation,
        "historical_partial_identities": historical_partial_identities,
    }
    verify_generated_payloads(payloads, **verifier_arguments)
    final_payloads = stage_and_commit(
        payloads,
        lambda candidate: verify_generated_payloads(candidate, **verifier_arguments),
    )

    result = {
        "status": status,
        "covered_prompt_units": covered,
        "pending_prompt_units": pending,
        "total_companion_entries": len(entries),
        "staged_surfaces": len(entries) * 4,
        "mastery_checks": len(mastery_records),
        "canonical_prompt_mapping_sha256": FROZEN_CANONICAL_PROMPT_SHA256,
        "prompt_map": bytes_identity(final_payloads[PROMPT_MAP_PATH]),
        "grouping_nodes": bytes_identity(final_payloads[GROUPING_PATH]),
        "manifest": bytes_identity(final_payloads[MANIFEST_PATH]),
        "qa": bytes_identity(final_payloads[QA_PATH]),
        "aliases": bytes_identity(final_payloads[ALIASES_PATH]),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
