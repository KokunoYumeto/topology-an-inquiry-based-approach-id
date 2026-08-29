#!/usr/bin/env python3
"""Regenerate bounded Chapter 19 source and companion schema/ID/xref receipts."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from typing import Any

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
COMPANION = ROOT / "companion"
QA = ROOT / "qa"
SOURCE_WRAPPER = SOURCE / "chap_Path_connected_topology.ptx"
COMPANION_WRAPPER = COMPANION / "chapter_19_path_connected_spaces_self_study.ptx"
SOURCE_QA = QA / "CHAPTER19_SOURCE_COMPLETE_QA.json"
COMPANION_QA = QA / "CHAPTER19_COMPANION_WRAPPER_SCHEMA_QA.json"
SCHEMA = Path.home() / ".ptx" / "schema" / "pretext.rng"
SCHEMA_SHA256 = "fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0"
SCHEMA_BYTES = 101829
PRETEXT_RESOURCE_COMMIT = "9bce7e55911fb14e3e6e362bfa78bd6431c38597"
EXACT_MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XI_NS = "http://www.w3.org/2001/XInclude"
SOURCE_FILES = (
    "chap_Path_connected_topology.ptx",
    "sec_path_intro.ptx",
    "sec_path_connect.ptx",
    "sec_path_connect_equiv.ptx",
    "sec_connectedness.ptx",
    "sec_connect_finite.ptx",
    "sec_connect_infinite.ptx",
    "sec_path_summ.ptx",
    "sec_path_exer.ptx",
)
SOURCE_HREFS = SOURCE_FILES[1:]
COMPANION_FILES = (
    "chapter_19_path_connected_spaces_self_study.ptx",
    "chapter_19_source_guides_a.ptx",
    "chapter_19_exercise_guides_a.ptx",
    "chapter_19_exercise_guides_b.ptx",
    "chapter_19_mastery.ptx",
)
COMPANION_HREFS = tuple(f"./{name}" for name in COMPANION_FILES[1:])
SOURCE_ORDERED_SHA256 = "ba26d5c4a1cb27cc9c5d6bea845e8406340a54d421905d11f8d562aacb118b0f"


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def identity(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(payload), "sha256": sha256(payload)}


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def parse(path: Path) -> etree._ElementTree:
    return etree.parse(str(path), etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False))


def ordered_source_hash() -> str:
    digest = hashlib.sha256()
    for name in SOURCE_FILES:
        path = SOURCE / name
        payload = path.read_bytes()
        relative = f"source/{name}".encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(str(len(payload)).encode("ascii"))
        digest.update(b"\0")
        digest.update(payload)
        digest.update(b"\0")
    return digest.hexdigest()


def validate_expanded(path: Path, relaxng: etree.RelaxNG) -> tuple[etree._ElementTree, list[str]]:
    document = parse(path)
    document.xinclude()
    valid = relaxng.validate(document)
    diagnostics = [str(entry) for entry in relaxng.error_log]
    if not valid or diagnostics:
        raise SystemExit(f"schema validation failed for {path}: {diagnostics}")
    return document, diagnostics


def id_xref_census(document: etree._ElementTree) -> dict[str, Any]:
    nodes = [node for node in document.getroot().iter() if isinstance(node.tag, str)]
    ids = [node.get(XML_ID) for node in nodes if node.get(XML_ID)]
    refs = [node.get("ref") for node in nodes if etree.QName(node).localname == "xref" and node.get("ref")]
    duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
    unresolved = sorted(set(refs) - set(ids))
    return {
        "expanded_elements": len(nodes),
        "xml_ids": len(ids),
        "unique_xml_ids": len(set(ids)),
        "xrefs": len(refs),
        "unique_xref_targets": len(set(refs)),
        "duplicate_xml_ids": duplicates,
        "unresolved_xrefs": unresolved,
    }


def build_payloads() -> dict[Path, bytes]:
    schema_payload = SCHEMA.read_bytes()
    if len(schema_payload) != SCHEMA_BYTES or sha256(schema_payload) != SCHEMA_SHA256:
        raise SystemExit("pinned PreTeXt schema identity changed")
    relaxng = etree.RelaxNG(parse(SCHEMA))

    source_hrefs = tuple(parse(SOURCE_WRAPPER).xpath("//xi:include/@href", namespaces={"xi": XI_NS}))
    if source_hrefs != SOURCE_HREFS:
        raise SystemExit(f"Chapter 19 source include order changed: {source_hrefs}")
    if ordered_source_hash() != SOURCE_ORDERED_SHA256:
        raise SystemExit("Chapter 19 ordered translated-source hash changed")
    for name in SOURCE_FILES:
        parse(SOURCE / name)
    source_document, source_diagnostics = validate_expanded(SOURCE_WRAPPER, relaxng)
    source_census = id_xref_census(source_document)
    approved_external = {
        "act_connected_compenent",
        "chap_Connected_topology",
        "ex_excluded_point_topology",
        "ex_particular_point_topology",
        "exp_K_topology",
        "thm_connected_limitpoints",
    }
    if source_census["duplicate_xml_ids"] or set(source_census["unresolved_xrefs"]) != approved_external:
        raise SystemExit(f"source ID/xref boundary changed: {source_census}")
    source_report = {
        "schema_version": 1,
        "status": "pass",
        "failures": [],
        "source": identity(SOURCE_WRAPPER),
        "source_files": [identity(SOURCE / name) for name in SOURCE_FILES],
        "ordered_source_sha256": SOURCE_ORDERED_SHA256,
        "schema": {"path": "pretext-user-cache/schema/pretext.rng", "bytes": SCHEMA_BYTES, "sha256": SCHEMA_SHA256},
        "pretext_resource_commit": PRETEXT_RESOURCE_COMMIT,
        "diagnostics": source_diagnostics,
        "checks": {
            "all_nine_files_well_formed": True,
            "include_order_exact": True,
            "schema_valid": True,
            "xml_ids_unique": True,
            "xref_boundary_exact": True,
            "five_image_descriptions_present": len(source_document.xpath("//image/description")) == 5,
        },
        "counts": {**source_census, "tasks": len(source_document.xpath("//task")), "exercises": len(source_document.xpath("//exercise")), "images": len(source_document.xpath("//image")), "image_descriptions": len(source_document.xpath("//image/description"))},
    }

    companion_hrefs = tuple(parse(COMPANION_WRAPPER).xpath("//xi:include/@href", namespaces={"xi": XI_NS}))
    if companion_hrefs != COMPANION_HREFS:
        raise SystemExit(f"Chapter 19 companion include order changed: {companion_hrefs}")
    for name in COMPANION_FILES:
        parse(COMPANION / name)
    companion_document, companion_diagnostics = validate_expanded(COMPANION_WRAPPER, relaxng)
    companion_census = id_xref_census(companion_document)
    if companion_census["duplicate_xml_ids"] or companion_census["unresolved_xrefs"]:
        raise SystemExit(f"companion ID/xref gate failed: {companion_census}")
    entries = companion_document.xpath("//exercise")
    stage_counts = {tag: len(companion_document.xpath(f"//exercise/{tag}")) for tag in ("statement", "hint", "answer", "solution")}
    text = " ".join("".join(companion_document.getroot().itertext()).split())
    if len(entries) != 47 or set(stage_counts.values()) != {47}:
        raise SystemExit(f"companion staged count changed: entries={len(entries)}, stages={stage_counts}")
    for required in ("CC BY 4.0", "CC BY-NC-SA 3.0", EXACT_MODEL, "tidak menyatakan dukungan"):
        if required not in text:
            raise SystemExit(f"companion lacks required rights/provenance text: {required}")
    companion_report = {
        "schema_version": 1,
        "status": "pass",
        "failures": [],
        "source": identity(COMPANION_WRAPPER),
        "closure": [identity(COMPANION / name) for name in COMPANION_FILES],
        "schema": {"path": "pretext-user-cache/schema/pretext.rng", "bytes": SCHEMA_BYTES, "sha256": SCHEMA_SHA256},
        "pretext_resource_commit": PRETEXT_RESOURCE_COMMIT,
        "diagnostics": companion_diagnostics,
        "checks": {
            "all_five_files_well_formed": True,
            "include_order_exact": True,
            "schema_valid": True,
            "all_xml_ids_unique": True,
            "all_xrefs_resolve": True,
            "staged_counts_exact": True,
            "rights_non_endorsement_and_model_exact": True,
        },
        "counts": {**companion_census, "entries": len(entries), "staged_surfaces": sum(stage_counts.values()), **stage_counts},
        "model_provenance": EXACT_MODEL,
    }
    return {SOURCE_QA: json_bytes(source_report), COMPANION_QA: json_bytes(companion_report)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payloads = build_payloads()
    if args.check:
        for path, expected in payloads.items():
            if not path.is_file() or path.read_bytes() != expected:
                raise SystemExit(f"deterministic Chapter 19 schema receipt differs: {path}")
    else:
        for path, payload in payloads.items():
            path.write_bytes(payload)
        for path, payload in payloads.items():
            if path.read_bytes() != payload:
                raise SystemExit(f"schema receipt readback failed: {path}")
    print(json.dumps({"status": "pass", "check_only": args.check, "outputs": {path.relative_to(ROOT).as_posix(): {"bytes": len(payload), "sha256": sha256(payload)} for path, payload in payloads.items()}}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
