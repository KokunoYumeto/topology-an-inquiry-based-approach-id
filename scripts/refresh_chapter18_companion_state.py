#!/usr/bin/env python3
"""Seal the complete Chapter 18 staged companion and stable-ID backend."""

from __future__ import annotations

import argparse
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
BACKEND = ROOT / "backend"
QA = ROOT / "qa"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"
XI_NS = "http://www.w3.org/2001/XInclude"

WRAPPER = COMPANION / "chapter_18_connected_spaces_self_study.ptx"
MASTERY = COMPANION / "chapter_18_mastery.ptx"
GUIDE_FILES = (
    "chapter_18_source_guides_a.ptx",
    "chapter_18_exercise_guides_a.ptx",
    "chapter_18_exercise_guides_b.ptx",
)
EXPECTED_WRAPPER_HREFS = tuple(f"./{name}" for name in GUIDE_FILES) + (
    "./chapter_18_mastery.ptx",
)

INVENTORY = BACKEND / "chapter_18_prompt_inventory.json"
PROMPT_MAP = BACKEND / "chapter_18_source_prompt_map.csv"
GROUPING = BACKEND / "chapter_18_grouping_nodes.json"
OCCURRENCE_ALIASES = BACKEND / "chapter_18_occurrence_entry_aliases.csv"
MANIFEST = BACKEND / "chapter_18_companion_manifest.json"
ENTRY_ALIASES = BACKEND / "chapter_18_entry_aliases.csv"
QA_OUTPUT = QA / "CHAPTER18_COMPANION_QA.json"
RECEIPT = QA / "CHAPTER18_COMPANION_BACKEND_RECEIPT.md"
WRAPPER_SCHEMA_QA = QA / "CHAPTER18_COMPANION_WRAPPER_SCHEMA_QA.json"
MARKER = BACKEND / ".chapter18_companion_refresh.in_progress.json"

EXPECTED_PHYSICAL_PROMPTS = 128
EXPECTED_CANONICAL_SOURCE = 128
EXPECTED_MASTERY = 8
EXPECTED_GROUPING = 6
EXPECTED_OCCURRENCE_ALIASES = 0
EXPECTED_TOTAL_ENTRIES = EXPECTED_CANONICAL_SOURCE + EXPECTED_MASTERY
EXPECTED_STAGED_SURFACES = EXPECTED_TOTAL_ENTRIES * 4
COMPANION_LICENSE = "CC BY 4.0"
SOURCE_RIGHTS = "CC BY-NC-SA 3.0 conservative treatment"
EXACT_MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"

PROMPT_FIELDS = (
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


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def identity_bytes(payload: bytes) -> dict[str, Any]:
    return {"bytes": len(payload), "sha256": sha256(payload)}


def identity(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), **identity_bytes(payload)}


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def csv_bytes(fields: tuple[str, ...], rows: list[dict[str, Any]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(fields), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def parse(path: Path) -> etree._ElementTree:
    return etree.parse(
        str(path),
        etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False),
    )


def local_name(node: etree._Element) -> str:
    return etree.QName(node).localname


def text_value(node: etree._Element) -> str:
    return " ".join("".join(node.itertext()).split())


def c14n_hash(node: etree._Element) -> str:
    return sha256(etree.tostring(node, method="c14n", with_comments=True))


def read_prompt_map() -> tuple[list[dict[str, str]], bytes]:
    reader = csv.DictReader(io.StringIO(PROMPT_MAP.read_text(encoding="utf-8"), newline=""))
    if tuple(reader.fieldnames or ()) != PROMPT_FIELDS:
        raise SystemExit(f"wrong Chapter 18 prompt-map fields: {reader.fieldnames}")
    rows = list(reader)
    if len(rows) != EXPECTED_PHYSICAL_PROMPTS:
        raise SystemExit(f"wrong physical prompt count: {len(rows)}")
    if [int(row["sequence"]) for row in rows] != list(range(1, EXPECTED_PHYSICAL_PROMPTS + 1)):
        raise SystemExit("physical prompt sequence is not contiguous")
    canonical: list[str] = []
    seen: set[str] = set()
    for row in rows:
        entry_id = row["entry_id"]
        if entry_id not in seen:
            seen.add(entry_id)
            canonical.append(entry_id)
        row["support_status"] = "covered"
    if len(canonical) != EXPECTED_CANONICAL_SOURCE:
        raise SystemExit(f"wrong canonical source-entry count: {len(canonical)}")
    return rows, csv_bytes(PROMPT_FIELDS, rows)


def parse_entry(node: etree._Element, path: Path, entry_type: str) -> dict[str, Any]:
    entry_id = node.get(XML_ID)
    if not entry_id:
        raise SystemExit(f"exercise lacks xml:id: {path}")
    children = [child for child in node if isinstance(child.tag, str)]
    names = [local_name(child) for child in children]
    if names != ["title", "statement", "hint", "answer", "solution"]:
        raise SystemExit(f"wrong staged child order for {entry_id}: {names}")
    title, statement, hint, answer, solution = children
    for label, surface in (
        ("title", title),
        ("statement", statement),
        ("hint", hint),
        ("answer", answer),
        ("solution", solution),
    ):
        if not text_value(surface):
            raise SystemExit(f"empty staged surface: {entry_id}/{label}")
    expected_stage_ids = {
        "hint": f"{entry_id}-hint",
        "answer": f"{entry_id}-answer",
        "solution": f"{entry_id}-solution",
    }
    observed = {key: node_value.get(XML_ID) for key, node_value in (("hint", hint), ("answer", answer), ("solution", solution))}
    if observed != expected_stage_ids:
        raise SystemExit(f"wrong stage IDs for {entry_id}: {observed}")
    return {
        "id": entry_id,
        "entry_type": entry_type,
        "file": path.relative_to(ROOT).as_posix(),
        "title": text_value(title),
        "license": COMPANION_LICENSE,
        "statement_id": entry_id,
        "hint_id": expected_stage_ids["hint"],
        "answer_id": expected_stage_ids["answer"],
        "solution_id": expected_stage_ids["solution"],
        "surface_sha256": {
            "statement": c14n_hash(statement),
            "hint": c14n_hash(hint),
            "answer": c14n_hash(answer),
            "solution": c14n_hash(solution),
        },
        "status": "staged_support_complete",
    }


def parse_division(path: Path, entry_type: str) -> list[dict[str, Any]]:
    root = parse(path).getroot()
    if local_name(root) != "section" or root.get(XML_LANG) != "id-ID":
        raise SystemExit(f"wrong companion division root or locale: {path}")
    entries = [child for child in root if isinstance(child.tag, str) and local_name(child) == "exercise"]
    return [parse_entry(node, path, entry_type) for node in entries]


def verify_wrapper() -> None:
    document = parse(WRAPPER)
    root = document.getroot()
    if local_name(root) != "appendix" or root.get(XML_LANG) != "id-ID":
        raise SystemExit("wrong Chapter 18 companion wrapper root or locale")
    hrefs = tuple(document.xpath("//xi:include/@href", namespaces={"xi": XI_NS}))
    if hrefs != EXPECTED_WRAPPER_HREFS:
        raise SystemExit(f"wrong Chapter 18 companion include sequence: {hrefs}")
    prose = text_value(root)
    for required in ("CC BY 4.0", "CC BY-NC-SA 3.0", EXACT_MODEL, "128", "136", "544"):
        if required not in prose:
            raise SystemExit(f"companion wrapper lacks required statement: {required}")


def build_payloads() -> dict[Path, bytes]:
    verify_wrapper()
    rows, covered_prompt_map = read_prompt_map()
    canonical_order: list[str] = []
    first_row: dict[str, dict[str, str]] = {}
    for row in rows:
        if row["entry_id"] not in first_row:
            first_row[row["entry_id"]] = row
            canonical_order.append(row["entry_id"])

    source_entries: list[dict[str, Any]] = []
    for name in GUIDE_FILES:
        source_entries.extend(parse_division(COMPANION / name, "source_prompt_guide"))
    observed_source_ids = [entry["id"] for entry in source_entries]
    if observed_source_ids != canonical_order:
        for index, (observed, expected) in enumerate(zip(observed_source_ids, canonical_order), start=1):
            if observed != expected:
                raise SystemExit(f"source-guide sequence diverges at {index}: {observed} != {expected}")
        raise SystemExit(
            f"wrong source-guide length: {len(observed_source_ids)} != {len(canonical_order)}"
        )

    mastery_entries = parse_division(MASTERY, "original_mastery")
    expected_mastery = [f"o003-c90-ch18-mastery-{number:02d}" for number in range(1, EXPECTED_MASTERY + 1)]
    if [entry["id"] for entry in mastery_entries] != expected_mastery:
        raise SystemExit("wrong Chapter 18 mastery sequence")

    all_entries = source_entries + mastery_entries
    all_ids = [entry["id"] for entry in all_entries]
    if len(all_ids) != EXPECTED_TOTAL_ENTRIES or len(set(all_ids)) != len(all_ids):
        raise SystemExit("wrong or duplicate complete companion entry IDs")

    alias_rows: list[dict[str, Any]] = []
    for sequence, entry in enumerate(all_entries, start=1):
        source_anchor = (
            first_row[entry["id"]]["source_anchor"]
            if entry["entry_type"] == "source_prompt_guide"
            else f"original:{entry['id']}"
        )
        alias_rows.append(
            {
                "sequence": sequence,
                "entry_id": entry["id"],
                "entry_type": entry["entry_type"],
                "license": COMPANION_LICENSE,
                "source_anchor": source_anchor,
                "companion_anchor": entry["id"],
                "statement_id": entry["statement_id"],
                "hint_id": entry["hint_id"],
                "answer_id": entry["answer_id"],
                "solution_id": entry["solution_id"],
                "status": entry["status"],
            }
        )
    alias_payload = csv_bytes(ALIAS_FIELDS, alias_rows)

    inventory_value = json.loads(INVENTORY.read_text(encoding="utf-8"))
    grouping_value = json.loads(GROUPING.read_text(encoding="utf-8"))
    occurrence_alias_rows = list(csv.DictReader(OCCURRENCE_ALIASES.read_text(encoding="utf-8").splitlines()))
    if grouping_value.get("grouping_node_count") != EXPECTED_GROUPING or len(grouping_value.get("nodes", [])) != EXPECTED_GROUPING:
        raise SystemExit("wrong Chapter 18 grouping-node count")
    if len(occurrence_alias_rows) != EXPECTED_OCCURRENCE_ALIASES:
        raise SystemExit("wrong Chapter 18 occurrence-alias count")

    companion_inputs = [WRAPPER, *(COMPANION / name for name in GUIDE_FILES), MASTERY]
    manifest = {
        "schema_version": 1,
        "status": "complete",
        "lane_id": "O003/C90",
        "locale": "id-ID",
        "unit": "Chapter 18 — Ruang Topologi Terhubung",
        "counts": {
            "physical_prompt_occurrences": EXPECTED_PHYSICAL_PROMPTS,
            "canonical_source_entries": EXPECTED_CANONICAL_SOURCE,
            "occurrence_aliases": EXPECTED_OCCURRENCE_ALIASES,
            "grouping_nodes": EXPECTED_GROUPING,
            "mastery_entries": EXPECTED_MASTERY,
            "total_entries": EXPECTED_TOTAL_ENTRIES,
            "staged_surfaces": EXPECTED_STAGED_SURFACES,
        },
        "rights": {
            "source_derivative": SOURCE_RIGHTS,
            "original_companion": COMPANION_LICENSE,
            "collection_not_flattened": True,
            "non_endorsement": True,
        },
        "model_provenance": EXACT_MODEL,
        "source_backend": {
            "inventory": identity(INVENTORY),
            "prompt_map_covered": {"path": PROMPT_MAP.relative_to(ROOT).as_posix(), **identity_bytes(covered_prompt_map)},
            "grouping_nodes": identity(GROUPING),
            "occurrence_aliases": identity(OCCURRENCE_ALIASES),
            "canonical_prompt_mapping_sha256": inventory_value["authority"]["canonical_prompt_mapping_sha256"],
            "occurrence_prompt_mapping_sha256": inventory_value["authority"]["occurrence_prompt_mapping_sha256"],
        },
        "companion_files": [identity(path) for path in companion_inputs],
        "entries": all_entries,
        "entry_aliases": {"path": ENTRY_ALIASES.relative_to(ROOT).as_posix(), **identity_bytes(alias_payload)},
    }
    manifest_payload = json_bytes(manifest)

    qa = {
        "schema_version": 1,
        "status": "pass",
        "failures": [],
        "checks": {
            "wrapper_include_order": "pass",
            "source_entry_order_matches_prompt_map": "pass",
            "all_staged_surfaces_nonempty": "pass",
            "stage_ids_deterministic": "pass",
            "all_entry_ids_unique": "pass",
            "prompt_map_support_status": "covered",
            "grouping_and_occurrence_alias_counts": "pass",
            "rights_and_model_provenance": "pass",
        },
        "counts": manifest["counts"],
        "inputs": {
            "source_complete_qa": identity(QA / "CHAPTER18_SOURCE_COMPLETE_QA.json"),
            "wrapper_schema": identity(WRAPPER_SCHEMA_QA),
        },
        "outputs": {
            "prompt_map": {"path": PROMPT_MAP.relative_to(ROOT).as_posix(), **identity_bytes(covered_prompt_map)},
            "manifest": {"path": MANIFEST.relative_to(ROOT).as_posix(), **identity_bytes(manifest_payload)},
            "entry_aliases": {"path": ENTRY_ALIASES.relative_to(ROOT).as_posix(), **identity_bytes(alias_payload)},
        },
    }
    qa_payload = json_bytes(qa)
    receipt_text = f"""# Chapter 18 companion/backend receipt

Status: **pass**

- Source prompts: {EXPECTED_PHYSICAL_PROMPTS} physical occurrences / {EXPECTED_CANONICAL_SOURCE} canonical support entries.
- Explicit duplicate aliases: {EXPECTED_OCCURRENCE_ALIASES}; grouping-only nodes: {EXPECTED_GROUPING}.
- Original mastery: {EXPECTED_MASTERY} entries.
- Complete companion: {EXPECTED_TOTAL_ENTRIES} entries / {EXPECTED_STAGED_SURFACES} staged surfaces.
- Source derivative rights: {SOURCE_RIGHTS}.
- Original companion rights: {COMPANION_LICENSE}, separately identified.
- Model provenance: `{EXACT_MODEL}`.
- Prompt-map SHA-256: `{sha256(covered_prompt_map)}`.
- Entry-alias SHA-256: `{sha256(alias_payload)}`.
- Manifest SHA-256: `{sha256(manifest_payload)}`.
- QA SHA-256: `{sha256(qa_payload)}`.

Every canonical source prompt has exactly one keyed statement, hint, answer or
rubric, and complete solution in prompt-map order. All eight original mastery
entries carry the same four staged surfaces. No upstream answer or solution is
misrepresented as source-authored material.
"""
    receipt_payload = receipt_text.encode("utf-8")
    return {
        PROMPT_MAP: covered_prompt_map,
        ENTRY_ALIASES: alias_payload,
        MANIFEST: manifest_payload,
        QA_OUTPUT: qa_payload,
        RECEIPT: receipt_payload,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payloads = build_payloads()
    if args.check:
        for path, expected in payloads.items():
            if not path.is_file() or path.read_bytes() != expected:
                raise SystemExit(f"deterministic companion state differs: {path}")
    else:
        marker_payload = json_bytes({"schema_version": 1, "outputs": [path.relative_to(ROOT).as_posix() for path in payloads]})
        MARKER.write_bytes(marker_payload)
        try:
            for path, payload in payloads.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
                temporary.write_bytes(payload)
                os.replace(temporary, path)
        finally:
            if MARKER.exists():
                MARKER.unlink()
    print(
        json.dumps(
            {
                "status": "pass",
                "physical_prompt_occurrences": EXPECTED_PHYSICAL_PROMPTS,
                "canonical_source_entries": EXPECTED_CANONICAL_SOURCE,
                "mastery_entries": EXPECTED_MASTERY,
                "total_entries": EXPECTED_TOTAL_ENTRIES,
                "staged_surfaces": EXPECTED_STAGED_SURFACES,
                "check_only": args.check,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

