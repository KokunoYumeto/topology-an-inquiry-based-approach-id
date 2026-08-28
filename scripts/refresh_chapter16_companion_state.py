#!/usr/bin/env python3
"""Validate and deterministically seal the complete Chapter 16 companion backend.

The prompt census and pinned-authority locators come from
``build_chapter16_prompt_inventory.py``. This transaction proves that every
source prompt has exactly one staged companion entry, keeps grouping tasks out
of the denominator, adds eight separately authored mastery checks, and writes
the five coupled machine-readable state artifacts atomically.
"""

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

from build_chapter16_prompt_inventory import (
    EXPECTED_ALIAS_TOTAL,
    EXPECTED_CANONICAL_ENTRY_TOTAL,
    EXPECTED_PROMPT_OCCURRENCE_TOTAL,
    FROZEN_AUTHORITY_COMMIT,
    PROMPT_MAP_FIELDS,
    build_inventory,
    prompt_payload_with_support_status,
)


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
COMPANION = ROOT / "companion"
BACKEND = ROOT / "backend"
QA = ROOT / "qa"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"
XI = "{http://www.w3.org/2001/XInclude}include"

WRAPPER = COMPANION / "chapter_16_quotient_spaces_self_study.ptx"
MASTERY = COMPANION / "chapter_16_mastery.ptx"
INVENTORY = BACKEND / "chapter_16_prompt_inventory.json"
PROMPT_MAP = BACKEND / "chapter_16_source_prompt_map.csv"
GROUPING = BACKEND / "chapter_16_grouping_nodes.json"
OCCURRENCE_ALIASES = BACKEND / "chapter_16_occurrence_entry_aliases.csv"
MANIFEST = BACKEND / "chapter_16_companion_manifest.json"
ALIASES = BACKEND / "chapter_16_entry_aliases.csv"
QA_OUTPUT = QA / "CHAPTER16_COMPANION_QA.json"
WRAPPER_SCHEMA = QA / "CHAPTER16_COMPANION_WRAPPER_SCHEMA_QA.json"
MASTERY_SCHEMA = QA / "CHAPTER16_MASTERY_SCHEMA_QA.json"
CUMULATIVE_SCHEMA = QA / "CHAPTER16_CUMULATIVE_SCHEMA_QA.json"
SOURCE_QA = QA / "CHAPTER16_SOURCE_COMPLETE_QA.json"
AUTHORITY_AUDIT = LANE / "00_control" / "CHAPTER16_AUTHORITY_AUDIT.md"
CORRECTIONS = LANE / "00_control" / "SOURCE_CORRECTIONS.csv"
TERMINOLOGY = LANE / "00_control" / "TERMINOLOGY.csv"
CUMULATIVE_WRAPPER = ROOT / "source" / "chapters_01_16_reader.ptx"
TRANSACTION_MARKER = BACKEND / ".chapter16_companion_refresh.in_progress.json"

COMPANION_LICENSE = "CC BY 4.0"
SOURCE_RIGHTS = "CC BY-NC-SA 3.0 conservative treatment"
EXACT_MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
EXPECTED_PRETEXT = "1.7.5"
EXPECTED_PYTHON = "3.12.13"
EXPECTED_RESOURCE_COMMIT = "9bce7e55911fb14e3e6e362bfa78bd6431c38597"
EXPECTED_SCHEMA_BYTES = 101829
EXPECTED_SCHEMA_SHA256 = "fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0"
EXPECTED_SOURCE_PROMPTS = 52
EXPECTED_PROMPT_OCCURRENCES = 54
EXPECTED_MASTERY = 8
EXPECTED_GROUPS = 3
EXPECTED_OCCURRENCE_ALIASES = 2

GUIDE_LAYOUT: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("chapter_16_source_guides_a.ptx", tuple(f"o003-c90-ch16-guide-{n:02d}" for n in range(1, 11))),
    ("chapter_16_source_guides_b.ptx", tuple(f"o003-c90-ch16-guide-{n:02d}" for n in range(11, 19))),
    ("chapter_16_exercise_guides_a.ptx", tuple(f"o003-c90-ch16-exer-a-{n:02d}" for n in range(1, 11))),
    ("chapter_16_exercise_guides_b.ptx", tuple(f"o003-c90-ch16-exer-b-{n:02d}" for n in range(1, 11))),
    ("chapter_16_exercise_guides_c.ptx", tuple(f"o003-c90-ch16-exer-c-{n:02d}" for n in range(1, 11))),
    ("chapter_16_exercise_guides_d.ptx", tuple(f"o003-c90-ch16-exer-d-{n:02d}" for n in range(1, 5))),
)
GUIDE_FILES = tuple(name for name, _ in GUIDE_LAYOUT)
EXPECTED_GUIDE_IDS = tuple(entry for _, entries in GUIDE_LAYOUT for entry in entries)
EXPECTED_MASTERY_IDS = tuple(f"o003-c90-ch16-mastery-{n:02d}" for n in range(1, 9))
EXPECTED_WRAPPER_HREFS = tuple(f"./{name}" for name in GUIDE_FILES) + ("./chapter_16_mastery.ptx",)

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


def digest_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def identity(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {"bytes": len(payload), "sha256": digest_bytes(payload)}


def identity_bytes(payload: bytes) -> dict[str, Any]:
    return {"bytes": len(payload), "sha256": digest_bytes(payload)}


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def lane_relative(path: Path) -> str:
    return path.relative_to(LANE).as_posix()


def json_bytes(payload: Any) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def csv_bytes(fieldnames: tuple[str, ...], rows: list[dict[str, Any]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(fieldnames), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def parse_xml(path: Path) -> etree._ElementTree:
    parser = etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False)
    return etree.parse(str(path), parser)


def local_name(element: etree._Element) -> str:
    return etree.QName(element).localname


def c14n_hash(element: etree._Element) -> str:
    payload = etree.tostring(element, method="c14n", exclusive=True, with_comments=True)
    return digest_bytes(payload)


def require_nonempty(element: etree._Element, label: str) -> None:
    if not " ".join("".join(element.itertext()).split()):
        raise SystemExit(f"empty staged surface: {label}")


def parse_entry(element: etree._Element, path: Path, entry_type: str) -> dict[str, Any]:
    entry_id = element.get(XML_ID)
    if not entry_id:
        raise SystemExit(f"exercise without xml:id in {path}")
    children = [child for child in element if isinstance(child.tag, str)]
    names = [local_name(child) for child in children]
    if names != ["title", "statement", "hint", "answer", "solution"]:
        raise SystemExit(f"wrong direct staged-child order for {entry_id}: {names}")
    title, statement, hint, answer, solution = children
    for label, node in (("title", title), ("statement", statement), ("hint", hint), ("answer", answer), ("solution", solution)):
        require_nonempty(node, f"{entry_id}/{label}")
    expected_stage_ids = {
        "hint": f"{entry_id}-hint",
        "answer": f"{entry_id}-answer",
        "solution": f"{entry_id}-solution",
    }
    observed_stage_ids = {
        "hint": hint.get(XML_ID),
        "answer": answer.get(XML_ID),
        "solution": solution.get(XML_ID),
    }
    if observed_stage_ids != expected_stage_ids:
        raise SystemExit(
            f"wrong staged IDs for {entry_id}: {observed_stage_ids} != {expected_stage_ids}"
        )
    return {
        "id": entry_id,
        "entry_type": entry_type,
        "file": repo_relative(path),
        "title": " ".join("".join(title.itertext()).split()),
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


def parse_guide_file(name: str, expected_ids: tuple[str, ...]) -> list[dict[str, Any]]:
    path = COMPANION / name
    if not path.is_file():
        raise SystemExit(f"missing guide file: {path}")
    root = parse_xml(path).getroot()
    if local_name(root) != "section" or root.get(XML_LANG) != "id-ID":
        raise SystemExit(f"wrong guide root or locale: {path}")
    exercises = [child for child in root if isinstance(child.tag, str) and local_name(child) == "exercise"]
    observed_ids = tuple(item.get(XML_ID) or "" for item in exercises)
    if observed_ids != expected_ids:
        raise SystemExit(f"wrong guide entry sequence in {path}: {observed_ids}")
    return [parse_entry(item, path, "source_prompt_guide") for item in exercises]


def parse_mastery() -> list[dict[str, Any]]:
    if not MASTERY.is_file():
        raise SystemExit(f"missing mastery file: {MASTERY}")
    root = parse_xml(MASTERY).getroot()
    if local_name(root) != "section" or root.get(XML_LANG) != "id-ID":
        raise SystemExit("wrong Chapter 16 mastery root or locale")
    exercises = [child for child in root if isinstance(child.tag, str) and local_name(child) == "exercise"]
    observed = tuple(item.get(XML_ID) or "" for item in exercises)
    if observed != EXPECTED_MASTERY_IDS:
        raise SystemExit(f"wrong mastery entry sequence: {observed}")
    return [parse_entry(item, MASTERY, "original_mastery") for item in exercises]


def verify_wrapper() -> list[str]:
    if not WRAPPER.is_file():
        raise SystemExit(f"missing companion wrapper: {WRAPPER}")
    document = parse_xml(WRAPPER)
    root = document.getroot()
    if local_name(root) != "appendix" or root.get(XML_LANG) != "id-ID":
        raise SystemExit("wrong Chapter 16 companion wrapper root or locale")
    hrefs = tuple(document.xpath("//xi:include/@href", namespaces={"xi": XI[1:].split("}")[0]}))
    if hrefs != EXPECTED_WRAPPER_HREFS:
        raise SystemExit(f"wrong Chapter 16 wrapper includes: {hrefs}")
    visible = " ".join("".join(root.itertext()).split())
    for required in (
        "54",
        "52",
        "60",
        "240",
        "Tiga",
        "CC BY 4.0",
        "CC BY-NC-SA 3.0",
        "bukan teks",
        "solusi resmi",
        EXACT_MODEL,
    ):
        if required not in visible:
            raise SystemExit(f"wrapper rights/coverage statement is missing {required!r}")
    return [f"companion/{Path(href).name}" for href in hrefs]


def read_schema_receipt(path: Path, expected_source: str) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"missing pinned-schema receipt: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("status") != "pass" or value.get("diagnostics") != []:
        raise SystemExit(f"schema receipt is not an exact pass: {path}")
    if value.get("pretext_resource_commit") != EXPECTED_RESOURCE_COMMIT:
        raise SystemExit(f"schema receipt uses the wrong resource commit: {path}")
    if value.get("schema", {}).get("bytes") != EXPECTED_SCHEMA_BYTES or value.get("schema", {}).get("sha256") != EXPECTED_SCHEMA_SHA256:
        raise SystemExit(f"schema receipt uses the wrong pinned schema bytes: {path}")
    runtime = value.get("runtime", {})
    if runtime.get("python") != EXPECTED_PYTHON or runtime.get("pretext") != EXPECTED_PRETEXT:
        raise SystemExit(f"schema receipt uses the wrong pinned runtime: {path}")
    if value.get("source", {}).get("path") != expected_source:
        raise SystemExit(f"schema receipt binds the wrong source: {path}")
    source_path = ROOT / expected_source
    if value["source"].get("bytes") != source_path.stat().st_size or value["source"].get("sha256") != digest(source_path):
        raise SystemExit(f"schema receipt source identity is stale: {path}")
    current_closure = [repo_relative(member) for member in include_closure(source_path)]
    receipt_xinclude = value.get("xinclude")
    if not isinstance(receipt_xinclude, dict) or receipt_xinclude.get("all_local") is not True:
        raise SystemExit(f"schema receipt lacks a local XInclude closure: {path}")
    receipt_closure = receipt_xinclude.get("closure")
    if (
        not isinstance(receipt_closure, list)
        or len(receipt_closure) != len(set(receipt_closure))
        or set(receipt_closure) != set(current_closure)
    ):
        raise SystemExit(f"schema receipt XInclude closure is stale: {path}")
    if receipt_xinclude.get("closure_file_count") != len(current_closure):
        raise SystemExit(f"schema receipt XInclude count is stale: {path}")
    return {
        "path": repo_relative(path),
        **identity(path),
        "status": "pass",
        "source": {"path": expected_source, **identity(source_path)},
        "closure_file_count": len(current_closure),
    }


def include_closure(entry: Path) -> list[Path]:
    pending = [entry.resolve()]
    seen: set[Path] = set()
    root = ROOT.resolve()
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        if not current.is_file() or root not in (current, *current.parents):
            raise SystemExit(f"invalid local XInclude closure member: {current}")
        seen.add(current)
        document = parse_xml(current)
        for include in document.iter(XI):
            href = include.get("href")
            if not href or "://" in href or href.startswith(("/", "\\")):
                raise SystemExit(f"nonlocal or empty XInclude in {current}: {href}")
            pending.append((current.parent / href).resolve())
    return sorted(seen, key=lambda path: path.relative_to(ROOT).as_posix().casefold())


def cumulative_id_xref_closure() -> dict[str, Any]:
    paths = include_closure(CUMULATIVE_WRAPPER)
    ordered_digest = hashlib.sha256()
    total_bytes = 0
    ids: dict[str, str] = {}
    xrefs: list[dict[str, str]] = []
    for path in paths:
        document = parse_xml(path)
        relative = repo_relative(path)
        payload = path.read_bytes()
        total_bytes += len(payload)
        ordered_digest.update(relative.encode("utf-8"))
        ordered_digest.update(b"\0")
        ordered_digest.update(str(len(payload)).encode("ascii"))
        ordered_digest.update(b"\0")
        ordered_digest.update(payload)
        ordered_digest.update(b"\0")
        for element in document.iter():
            if not isinstance(element.tag, str):
                continue
            xml_id = element.get(XML_ID)
            if xml_id:
                if xml_id in ids:
                    raise SystemExit(f"duplicate cumulative xml:id {xml_id!r}: {ids[xml_id]} and {relative}")
                ids[xml_id] = relative
            if local_name(element) == "xref" and element.get("ref"):
                xrefs.append({"source": relative, "ref": element.get("ref") or ""})
    missing = [xref for xref in xrefs if xref["ref"] not in ids]
    if missing:
        raise SystemExit(f"unresolved cumulative xrefs: {missing[:10]}")
    return {
        "xinclude_files": len(paths),
        "ordered_identity_contract": (
            "sha256 over each repo-relative closure path as UTF-8, NUL, decimal "
            "byte length, NUL, raw file bytes, NUL, in casefolded path order"
        ),
        "ordered_sha256": ordered_digest.hexdigest(),
        "total_bytes": total_bytes,
        "unique_ids": len(ids),
        "xref_occurrences": len(xrefs),
        "all_xrefs_resolve": True,
        "missing_targets": [],
    }


def cumulative_reader_admission() -> dict[str, Any]:
    """Derive Chapter 16 reader admission from the live cumulative wrapper."""
    document = parse_xml(CUMULATIVE_WRAPPER)
    root = document.getroot()
    books = [node for node in root if isinstance(node.tag, str) and local_name(node) == "book"]
    if local_name(root) != "pretext" or len(books) != 1 or books[0].get(XML_ID) != "o003-c90-chapters-01-16-reader":
        raise SystemExit("wrong cumulative Chapter 16 reader root or book ID")
    visible = " ".join("".join(root.itertext()).split())
    for required in ("enam belas", "CC BY-NC-SA 3.0", "CC BY 4.0", EXACT_MODEL, "tidak ada dukungan resmi"):
        if required not in visible:
            raise SystemExit(f"cumulative reader rights/provenance statement is missing {required!r}")
    namespace = {"xi": XI[1:].split("}")[0]}
    chapter_hrefs = list(
        document.xpath("/pretext/book/part/xi:include/@href", namespaces=namespace)
    )
    companion_hrefs = list(
        document.xpath(
            "/pretext/book/backmatter/xi:include/@href",
            namespaces=namespace,
        )
    )
    main_href = "./chap_quotients.ptx"
    companion_href = "../companion/chapter_16_quotient_spaces_self_study.ptx"
    main_positions = [
        index for index, href in enumerate(chapter_hrefs, start=1) if href == main_href
    ]
    companion_positions = [
        index
        for index, href in enumerate(companion_hrefs, start=1)
        if href == companion_href
    ]
    exact_main_tail = chapter_hrefs[-2:] == ["./chap_subspaces.ptx", main_href]
    exact_companion_tail = companion_hrefs[-2:] == [
        "../companion/chapter_15_subspaces_self_study.ptx",
        companion_href,
    ]
    admitted = (
        len(main_positions) == 1
        and len(companion_positions) == 1
        and exact_main_tail
        and exact_companion_tail
    )
    return {
        "admitted": admitted,
        "cumulative_wrapper": repo_relative(CUMULATIVE_WRAPPER),
        "main_include": main_href,
        "main_include_positions": main_positions,
        "main_include_total": len(chapter_hrefs),
        "companion_include": companion_href,
        "companion_include_positions": companion_positions,
        "companion_include_total": len(companion_hrefs),
        "main_include_order_exact": exact_main_tail,
        "companion_include_order_exact": exact_companion_tail,
    }


def selected_ledger_ids(path: Path, prefix: str, first: int, last: int) -> list[str]:
    text = path.read_text(encoding="utf-8-sig")
    found: list[str] = []
    for number in range(first, last + 1):
        candidate = f"{prefix}{number:03d}"
        if candidate in text:
            found.append(candidate)
    expected = [f"{prefix}{number:03d}" for number in range(first, last + 1)]
    if found != expected:
        raise SystemExit(f"ledger range incomplete in {path}: {found} != {expected}")
    return found


def load_prompt_rows(prompt_payload: bytes) -> list[dict[str, str]]:
    reader = csv.DictReader(io.StringIO(prompt_payload.decode("utf-8"), newline=""))
    if tuple(reader.fieldnames or ()) != tuple(PROMPT_MAP_FIELDS):
        raise SystemExit("bootstrap prompt map fields changed")
    rows = list(reader)
    if len(rows) != EXPECTED_PROMPT_OCCURRENCES:
        raise SystemExit(f"wrong bootstrap prompt row count: {len(rows)}")
    if len({row["entry_id"] for row in rows}) != EXPECTED_SOURCE_PROMPTS:
        raise SystemExit("wrong canonical entry count in occurrence-aware prompt map")
    return rows


def build_payloads() -> tuple[dict[Path, bytes], dict[str, Any]]:
    (
        inventory_payload,
        bootstrap_prompt_payload,
        grouping_payload,
        occurrence_alias_payload,
        inventory_summary,
    ) = build_inventory()
    if EXPECTED_CANONICAL_ENTRY_TOTAL != EXPECTED_SOURCE_PROMPTS:
        raise SystemExit("inventory module and companion canonical totals diverged")
    if EXPECTED_PROMPT_OCCURRENCE_TOTAL != EXPECTED_PROMPT_OCCURRENCES:
        raise SystemExit("inventory module and companion occurrence totals diverged")
    if EXPECTED_ALIAS_TOTAL != EXPECTED_OCCURRENCE_ALIASES:
        raise SystemExit("inventory module and companion alias totals diverged")
    if not INVENTORY.is_file() or INVENTORY.read_bytes() != inventory_payload:
        raise SystemExit("prompt inventory file differs from deterministic regeneration")
    if not OCCURRENCE_ALIASES.is_file() or OCCURRENCE_ALIASES.read_bytes() != occurrence_alias_payload:
        raise SystemExit("occurrence-alias artifact differs from deterministic regeneration")
    source_rows = load_prompt_rows(bootstrap_prompt_payload)
    source_entries: list[dict[str, Any]] = []
    for name, expected_ids in GUIDE_LAYOUT:
        source_entries.extend(parse_guide_file(name, expected_ids))
    if tuple(entry["id"] for entry in source_entries) != EXPECTED_GUIDE_IDS:
        raise SystemExit("companion guide entries do not match the 52-entry prompt plan")
    mastery_entries = parse_mastery()
    wrapper_includes = verify_wrapper()
    wrapper_schema = read_schema_receipt(
        WRAPPER_SCHEMA,
        "companion/chapter_16_quotient_spaces_self_study.ptx",
    )
    mastery_schema = read_schema_receipt(MASTERY_SCHEMA, "companion/chapter_16_mastery.ptx")
    cumulative_schema = read_schema_receipt(
        CUMULATIVE_SCHEMA,
        "source/chapters_01_16_reader.ptx",
    )
    source_qa = json.loads(SOURCE_QA.read_text(encoding="utf-8"))
    if source_qa.get("status") != "pass" or source_qa.get("failures") != []:
        raise SystemExit("Chapter 16 source QA is not a pass")
    source_qa_rows = source_qa.get("files")
    if not isinstance(source_qa_rows, list) or len(source_qa_rows) != 7:
        raise SystemExit("Chapter 16 source QA has the wrong file closure")
    for row in source_qa_rows:
        if not isinstance(row, dict) or not isinstance(row.get("file"), str):
            raise SystemExit("Chapter 16 source QA has a malformed file row")
        translated = row.get("translated")
        if not isinstance(translated, dict):
            raise SystemExit(f"Chapter 16 source QA lacks translated identity: {row}")
        current = ROOT / "source" / row["file"]
        if translated.get("bytes") != current.stat().st_size or translated.get("sha256") != digest(current):
            raise SystemExit(f"Chapter 16 source QA identity is stale: {row['file']}")

    final_prompt_rows: list[dict[str, Any]] = []
    manifest_source_entries: list[dict[str, Any]] = []
    alias_rows: list[dict[str, Any]] = []
    source_support_by_id = {entry["id"]: entry for entry in source_entries}
    seen_source_entries: set[str] = set()
    for occurrence_sequence, row in enumerate(source_rows, start=1):
        if int(row["sequence"]) != occurrence_sequence:
            raise SystemExit(f"prompt occurrence order mismatch at sequence {occurrence_sequence}")
        final_row = dict(row)
        final_row["support_status"] = "covered"
        final_prompt_rows.append(final_row)
        if row["entry_id"] in seen_source_entries:
            continue
        seen_source_entries.add(row["entry_id"])
        sequence = len(manifest_source_entries) + 1
        support = source_support_by_id.get(row["entry_id"])
        if support is None or EXPECTED_GUIDE_IDS[sequence - 1] != row["entry_id"]:
            raise SystemExit(f"prompt/support canonical order mismatch at entry {sequence}")
        locator = json.loads(row["authority_locator"])
        manifest_source_entries.append(
            {
                "sequence": sequence,
                **support,
                "source_anchor": row["source_anchor"],
                "source_anchor_kind": row["source_anchor_kind"],
                "authority_source_file": row["authority_source_file"],
                "authority_line": int(row["authority_line"]),
                "prompt_carrier": row["prompt_carrier"],
                "authority_locator": locator,
                "parent_group_anchor": row["parent_group_anchor"] or None,
                "canonical_occurrence_sequence": occurrence_sequence,
            }
        )
        alias_rows.append(
            {
                "sequence": sequence,
                "entry_id": support["id"],
                "entry_type": support["entry_type"],
                "license": COMPANION_LICENSE,
                "source_anchor": row["source_anchor"],
                "companion_anchor": support["id"],
                "statement_id": support["statement_id"],
                "hint_id": support["hint_id"],
                "answer_id": support["answer_id"],
                "solution_id": support["solution_id"],
                "status": support["status"],
            }
        )
    if len(seen_source_entries) != EXPECTED_SOURCE_PROMPTS:
        raise SystemExit("not all canonical source entries were mapped")

    manifest_mastery_entries: list[dict[str, Any]] = []
    for offset, support in enumerate(mastery_entries, start=1):
        sequence = EXPECTED_SOURCE_PROMPTS + offset
        manifest_mastery_entries.append(
            {
                "sequence": sequence,
                **support,
                "source_anchor": None,
                "source_anchor_kind": None,
                "authority_source_file": None,
                "authority_line": None,
                "prompt_carrier": "original_mastery",
                "authority_locator": None,
                "parent_group_anchor": None,
            }
        )
        alias_rows.append(
            {
                "sequence": sequence,
                "entry_id": support["id"],
                "entry_type": support["entry_type"],
                "license": COMPANION_LICENSE,
                "source_anchor": "",
                "companion_anchor": support["id"],
                "statement_id": support["statement_id"],
                "hint_id": support["hint_id"],
                "answer_id": support["answer_id"],
                "solution_id": support["solution_id"],
                "status": support["status"],
            }
        )

    all_companion_paths = [COMPANION / name for name in GUIDE_FILES] + [MASTERY, WRAPPER]
    all_ids: dict[str, str] = {}
    for path in all_companion_paths:
        for element in parse_xml(path).iter():
            if not isinstance(element.tag, str):
                continue
            xml_id = element.get(XML_ID)
            if xml_id:
                if xml_id in all_ids:
                    raise SystemExit(f"duplicate companion xml:id {xml_id!r}")
                all_ids[xml_id] = repo_relative(path)

    final_prompt_payload = prompt_payload_with_support_status(bootstrap_prompt_payload, "covered")
    if final_prompt_payload != csv_bytes(tuple(PROMPT_MAP_FIELDS), final_prompt_rows):
        raise SystemExit("covered prompt-map helper and local serialization diverged")
    aliases_payload = csv_bytes(ALIAS_FIELDS, alias_rows)
    prompt_inventory = json.loads(inventory_payload.decode("utf-8"))
    covered_phase = (
        prompt_inventory.get("prompt_map", {})
        .get("phase_contract", {})
        .get("companion_support_covered")
    )
    expected_covered_phase = {
        "support_status": "covered",
        **identity_bytes(final_prompt_payload),
    }
    if covered_phase != expected_covered_phase:
        raise SystemExit(
            "prompt inventory covered-phase identity differs from the final prompt map"
        )
    grouping_value = json.loads(grouping_payload.decode("utf-8"))
    if grouping_value.get("grouping_node_count") != EXPECTED_GROUPS:
        raise SystemExit("grouping backend count changed")
    occurrence_alias_rows = list(
        csv.DictReader(io.StringIO(occurrence_alias_payload.decode("utf-8"), newline=""))
    )
    if len(occurrence_alias_rows) != EXPECTED_OCCURRENCE_ALIASES:
        raise SystemExit("occurrence-alias row count changed")
    if [(row["alias_occurrence_sequence"], row["canonical_occurrence_sequence"]) for row in occurrence_alias_rows] != [("51", "49"), ("52", "50")]:
        raise SystemExit("hard-coded occurrence-alias pairs changed")

    file_identities = {
        repo_relative(path): identity(path)
        for path in all_companion_paths
    }
    cumulative = cumulative_id_xref_closure()
    reader_admission = cumulative_reader_admission()
    reader_admission_pending = not reader_admission["admitted"]
    manifest_status = (
        "companion_complete_reader_admission_pending"
        if reader_admission_pending
        else "companion_complete_reader_admitted"
    )
    qa_boundary = (
        "chapter_16_complete_companion_backend_reader_admission_pending"
        if reader_admission_pending
        else "chapter_16_complete_companion_backend_reader_admitted"
    )
    manifest_value = {
        "schema_version": 1,
        "status": manifest_status,
        "partial": False,
        "lane_id": "O003/C90",
        "locale": "id-ID",
        "component": "original_o003_completion_and_self_study_companion",
        "license": COMPANION_LICENSE,
        "unit": {
            "id": "o003-c90-ch16-quotient-spaces",
            "title": "Ruang Kuosien",
            "sequence": 16,
        },
        "authority": {
            "audit": "00_control/CHAPTER16_AUTHORITY_AUDIT.md",
            "audit_sha256": digest(AUTHORITY_AUDIT),
            "commit": FROZEN_AUTHORITY_COMMIT,
            "ordered_hash_contract": prompt_inventory["authority"]["ordered_hash_contract"],
            "ordered_sha256": prompt_inventory["authority"]["ordered_sha256"],
            "canonical_prompt_mapping_sha256": prompt_inventory["authority"]["canonical_prompt_mapping_sha256"],
            "occurrence_prompt_mapping_sha256": prompt_inventory["authority"]["occurrence_prompt_mapping_sha256"],
            "source_file_count": prompt_inventory["authority"]["source_file_count"],
            "source_prompt_total": EXPECTED_SOURCE_PROMPTS,
            "physical_prompt_occurrence_total": EXPECTED_PROMPT_OCCURRENCES,
            "explicit_occurrence_alias_total": EXPECTED_OCCURRENCE_ALIASES,
            "atomic_prompt_total": prompt_inventory["census"]["atomic_prompt_total"],
            "direct_prompt_total": prompt_inventory["census"]["direct_prompt_total"],
            "grouping_node_total": EXPECTED_GROUPS,
        },
        "companion": {
            "wrapper": repo_relative(WRAPPER),
            "guide_files": [f"companion/{name}" for name in GUIDE_FILES],
            "mastery": repo_relative(MASTERY),
            "file_identities": file_identities,
            "wrapper_includes": wrapper_includes,
            "source_entries": manifest_source_entries,
            "mastery_entries": manifest_mastery_entries,
        },
        "coverage": {
            "covered_source_prompt_guides": EXPECTED_SOURCE_PROMPTS,
            "pending_source_prompt_guides": 0,
            "covered_mastery_checks": EXPECTED_MASTERY,
            "entry_total": EXPECTED_SOURCE_PROMPTS + EXPECTED_MASTERY,
            "statements": EXPECTED_SOURCE_PROMPTS + EXPECTED_MASTERY,
            "hints": EXPECTED_SOURCE_PROMPTS + EXPECTED_MASTERY,
            "answers_or_rubrics": EXPECTED_SOURCE_PROMPTS + EXPECTED_MASTERY,
            "complete_solutions": EXPECTED_SOURCE_PROMPTS + EXPECTED_MASTERY,
            "staged_surface_total": 4 * (EXPECTED_SOURCE_PROMPTS + EXPECTED_MASTERY),
            "grouping_nodes": EXPECTED_GROUPS,
        },
        "rights": {
            "source_derivative": SOURCE_RIGHTS,
            "companion_component": "CC BY 4.0 separate original component",
            "non_endorsement": "The companion is not authored by Steven Schlicker or Grand Valley State University.",
        },
        "provenance": {
            "tool": EXACT_MODEL,
            "instruction": "Produced at the user's direction; source-author, institutional, and human-contributor credits remain unchanged.",
        },
        "backend": {
            "prompt_map": {
                "path": "backend/chapter_16_source_prompt_map.csv",
                "phase": "companion_support_covered",
                **identity_bytes(final_prompt_payload),
            },
            "grouping_nodes": {"path": "backend/chapter_16_grouping_nodes.json", **identity_bytes(grouping_payload)},
            "entry_aliases": {"path": "backend/chapter_16_entry_aliases.csv", **identity_bytes(aliases_payload)},
            "occurrence_entry_aliases": {
                "path": "backend/chapter_16_occurrence_entry_aliases.csv",
                **identity_bytes(occurrence_alias_payload),
                "role": "immutable two-row physical-occurrence alias evidence",
                "exact_pairs": [
                    {
                        "alias_occurrence_sequence": int(row["alias_occurrence_sequence"]),
                        "canonical_occurrence_sequence": int(row["canonical_occurrence_sequence"]),
                        "canonical_entry_id": row["canonical_entry_id"],
                        "exact_subtree_sha256": row["exact_subtree_sha256"],
                    }
                    for row in occurrence_alias_rows
                ],
            },
            "inventory": {
                "path": "backend/chapter_16_prompt_inventory.json",
                **identity(INVENTORY),
                "role": (
                    "immutable authority census with deterministic bootstrap-pending "
                    "and post-companion-covered prompt-map phase identities"
                ),
            },
        },
        "schema": {
            "wrapper": wrapper_schema,
            "mastery": mastery_schema,
            "cumulative": cumulative_schema,
        },
        "reader_admission": reader_admission,
        "reader_admission_pending": reader_admission_pending,
    }
    manifest_payload = json_bytes(manifest_value)
    correction_ids = selected_ledger_ids(CORRECTIONS, "O003-C", 188, 211)
    terminology_ids = selected_ledger_ids(TERMINOLOGY, "O003-T", 204, 240)
    qa_value = {
        "schema_version": 1,
        "status": "pass",
        "boundary": qa_boundary,
        "source_prompt_total": EXPECTED_SOURCE_PROMPTS,
        "physical_prompt_occurrence_total": EXPECTED_PROMPT_OCCURRENCES,
        "explicit_occurrence_alias_total": EXPECTED_OCCURRENCE_ALIASES,
        "mastery_total": EXPECTED_MASTERY,
        "entry_total": EXPECTED_SOURCE_PROMPTS + EXPECTED_MASTERY,
        "staged_surface_total": 4 * (EXPECTED_SOURCE_PROMPTS + EXPECTED_MASTERY),
        "grouping_node_total": EXPECTED_GROUPS,
        "source_prompt_support": {"covered": EXPECTED_SOURCE_PROMPTS, "pending": 0},
        "xml": {
            "companion_unique_ids": len(all_ids),
            "all_companion_ids_unique": True,
            "all_stage_ids_exact": True,
            "all_staged_surfaces_nonempty": True,
            "wrapper_include_order_exact": True,
            "cumulative": cumulative,
        },
        "source_qa": {"path": "repo/qa/CHAPTER16_SOURCE_COMPLETE_QA.json", **identity(SOURCE_QA), "status": "pass"},
        "schema": {
            "wrapper": wrapper_schema,
            "mastery": mastery_schema,
            "cumulative": cumulative_schema,
        },
        "reader_admission": reader_admission,
        "authority": {
            "commit": FROZEN_AUTHORITY_COMMIT,
            "canonical_prompt_mapping_sha256": inventory_summary["canonical_prompt_mapping_sha256"],
            "prompt_inventory": {"path": "repo/backend/chapter_16_prompt_inventory.json", **identity(INVENTORY)},
            "all_locators_regenerated": True,
        },
        "ledgers": {
            "source_corrections": {"path": "00_control/SOURCE_CORRECTIONS.csv", **identity(CORRECTIONS), "ids": correction_ids},
            "terminology": {"path": "00_control/TERMINOLOGY.csv", **identity(TERMINOLOGY), "ids": terminology_ids},
        },
        "rights": manifest_value["rights"],
        "provenance": manifest_value["provenance"],
        "generated_outputs": {
            "prompt_map": {
                "path": "repo/backend/chapter_16_source_prompt_map.csv",
                "phase": "companion_support_covered",
                **identity_bytes(final_prompt_payload),
            },
            "grouping_nodes": {"path": "repo/backend/chapter_16_grouping_nodes.json", **identity_bytes(grouping_payload)},
            "entry_aliases": {"path": "repo/backend/chapter_16_entry_aliases.csv", **identity_bytes(aliases_payload)},
            "occurrence_entry_aliases": {
                "path": "repo/backend/chapter_16_occurrence_entry_aliases.csv",
                **identity_bytes(occurrence_alias_payload),
                "preserved_unchanged": True,
                "all_hard_coded_exact_pairs_verified": True,
                "pairs": [
                    {
                        "alias_occurrence_sequence": int(row["alias_occurrence_sequence"]),
                        "canonical_occurrence_sequence": int(row["canonical_occurrence_sequence"]),
                        "canonical_entry_id": row["canonical_entry_id"],
                        "exact_subtree_sha256": row["exact_subtree_sha256"],
                    }
                    for row in occurrence_alias_rows
                ],
            },
            "companion_manifest": {"path": "repo/backend/chapter_16_companion_manifest.json", **identity_bytes(manifest_payload)},
        },
        "failures": [],
        "reader_admission_pending": reader_admission_pending,
    }
    qa_payload = json_bytes(qa_value)
    payloads = {
        PROMPT_MAP: final_prompt_payload,
        GROUPING: grouping_payload,
        ALIASES: aliases_payload,
        MANIFEST: manifest_payload,
        QA_OUTPUT: qa_payload,
    }
    summary = {
        "status": "pass",
        "source_prompts": EXPECTED_SOURCE_PROMPTS,
        "physical_prompt_occurrences": EXPECTED_PROMPT_OCCURRENCES,
        "occurrence_aliases": EXPECTED_OCCURRENCE_ALIASES,
        "mastery": EXPECTED_MASTERY,
        "entries": EXPECTED_SOURCE_PROMPTS + EXPECTED_MASTERY,
        "staged_surfaces": 4 * (EXPECTED_SOURCE_PROMPTS + EXPECTED_MASTERY),
        "grouping_nodes": EXPECTED_GROUPS,
        "reader_admitted": reader_admission["admitted"],
        "prompt_map_phase": "companion_support_covered",
        "outputs": {repo_relative(path): identity_bytes(payload) for path, payload in payloads.items()},
    }
    return payloads, summary


def write_transaction(payloads: dict[Path, bytes]) -> None:
    if TRANSACTION_MARKER.exists():
        raise SystemExit(f"stale Chapter 16 transaction marker requires inspection: {TRANSACTION_MARKER}")
    marker_payload = json_bytes({"schema_version": 1, "outputs": [repo_relative(path) for path in payloads]})
    TRANSACTION_MARKER.write_bytes(marker_payload)
    staged: list[tuple[Path, Path]] = []
    try:
        for target, payload in payloads.items():
            temporary = target.with_name(target.name + ".stage")
            if temporary.exists():
                raise SystemExit(f"stale staged output requires inspection: {temporary}")
            temporary.write_bytes(payload)
            if temporary.read_bytes() != payload:
                raise SystemExit(f"staged byte readback failed: {temporary}")
            staged.append((temporary, target))
        for temporary, target in staged:
            os.replace(temporary, target)
        for target, payload in payloads.items():
            if target.read_bytes() != payload:
                raise SystemExit(f"committed byte readback failed: {target}")
    finally:
        for temporary, _ in staged:
            if temporary.exists():
                temporary.unlink()
        if TRANSACTION_MARKER.exists():
            TRANSACTION_MARKER.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="regenerate in memory and require exact existing bytes")
    args = parser.parse_args()
    payloads, summary = build_payloads()
    if args.check:
        for path, expected in payloads.items():
            if not path.is_file() or path.read_bytes() != expected:
                raise SystemExit(f"generated output differs from deterministic regeneration: {path}")
        summary["mode"] = "check"
    else:
        write_transaction(payloads)
        summary["mode"] = "write"
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
