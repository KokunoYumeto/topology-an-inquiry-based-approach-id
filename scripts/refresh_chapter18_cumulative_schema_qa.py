#!/usr/bin/env python3
"""Regenerate isolated companion and cumulative Chapters 1–18 schema receipts."""

from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import platform
from typing import Any

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
COMPANION = ROOT / "companion"
QA = ROOT / "qa"
WRAPPER = SOURCE / "chapters_01_18_reader.ptx"
PRIOR = SOURCE / "chapters_01_17_reader.ptx"
COMPANION_WRAPPER = COMPANION / "chapter_18_connected_spaces_self_study.ptx"
COMPANION_QA = QA / "CHAPTER18_COMPANION_QA.json"
WRAPPER_SCHEMA_QA = QA / "CHAPTER18_COMPANION_WRAPPER_SCHEMA_QA.json"
CUMULATIVE_QA = QA / "CHAPTER18_CUMULATIVE_SCHEMA_QA.json"
SCHEMA = Path.home() / ".ptx" / "schema" / "pretext.rng"
SCHEMA_DISPLAY = "pretext-user-cache/schema/pretext.rng"
SCHEMA_SHA256 = "fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0"
PRETEXT_VERSION = "1.7.5"
PRETEXT_RESOURCE_COMMIT = "9bce7e55911fb14e3e6e362bfa78bd6431c38597"
EXACT_MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XI_NS = "http://www.w3.org/2001/XInclude"
EXPECTED_CH18_SOURCE = "./chap_Connected_topology.ptx"
EXPECTED_CH18_COMPANION = "../companion/chapter_18_connected_spaces_self_study.ptx"
EXPECTED_COMPANION_HREFS = (
    "./chapter_18_source_guides_a.ptx",
    "./chapter_18_exercise_guides_a.ptx",
    "./chapter_18_exercise_guides_b.ptx",
    "./chapter_18_mastery.ptx",
)


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def identity(path: Path, display: str) -> dict[str, Any]:
    payload = path.read_bytes()
    return {"path": display, "bytes": len(payload), "sha256": sha256(payload)}


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def parse(path: Path) -> etree._ElementTree:
    return etree.parse(str(path), etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False))


def replace_once(payload: bytes, old: bytes, new: bytes) -> bytes:
    count = payload.count(old)
    if count != 1:
        raise RuntimeError(f"authorized wrapper transform expected one occurrence, found {count}: {old!r}")
    return payload.replace(old, new)


def expected_wrapper_bytes() -> bytes:
    payload = PRIOR.read_bytes()
    replacements = (
        (b'o003-c90-chapters-01-17-reader', b'o003-c90-chapters-01-18-reader'),
        (
            'Bab 1-17 - Himpunan, Fungsi, Ruang Metrik, Ruang Topologi, Kekontinuan, Homeomorfisme, Subruang, Ruang Kuosien, Ruang Kompak, serta Pendamping Belajar Mandiri'.encode(),
            'Bab 1-18 - Himpunan, Fungsi, Ruang Metrik, Ruang Topologi, Kekontinuan, Homeomorfisme, Subruang, Ruang Kuosien, Ruang Kompak, Keterhubungan, serta Pendamping Belajar Mandiri'.encode(),
        ),
        (b'o003-c90-ch17-edition-note', b'o003-c90-ch18-edition-note'),
        ('tujuh belas bab pertama'.encode(), 'delapan belas bab pertama'.encode()),
        (
            'Ruang Topologi, Kekontinuan, Homeomorfisme, Subruang, Ruang Kuosien, dan Kekompakan'.encode(),
            'Ruang Topologi, Kekontinuan, Homeomorfisme, Subruang, Ruang Kuosien, Kekompakan, dan Keterhubungan'.encode(),
        ),
        (
            b'      <xi:include href="./chap_Compact_topology.ptx"/>',
            b'      <xi:include href="./chap_Compact_topology.ptx"/>\n      <xi:include href="./chap_Connected_topology.ptx"/>',
        ),
        (
            b'      <xi:include href="../companion/chapter_17_compact_spaces_self_study.ptx"/>',
            b'      <xi:include href="../companion/chapter_17_compact_spaces_self_study.ptx"/>\n      <xi:include href="../companion/chapter_18_connected_spaces_self_study.ptx"/>',
        ),
        (b'Bab 1-17 ini', b'Bab 1-18 ini'),
        (b'Bab 18; isi lengkap', b'Bab 19; isi lengkap'),
    )
    for old, new in replacements:
        payload = replace_once(payload, old, new)
    return payload


def closure(start: Path) -> tuple[list[Path], int]:
    root = ROOT.resolve()
    ordered: list[Path] = []
    visited: set[Path] = set()
    edges = 0

    def visit(path: Path) -> None:
        nonlocal edges
        resolved = path.resolve(strict=True)
        resolved.relative_to(root)
        if resolved in visited:
            return
        visited.add(resolved)
        ordered.append(resolved)
        document = parse(resolved)
        hrefs = document.xpath("//xi:include/@href", namespaces={"xi": XI_NS})
        edges += len(hrefs)
        for href in hrefs:
            visit((resolved.parent / href).resolve(strict=True))

    visit(start)
    return ordered, edges


def closure_identity(paths: list[Path]) -> tuple[str, int]:
    digest = hashlib.sha256()
    total = 0
    for path in sorted(paths, key=lambda value: value.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix().encode("utf-8")
        payload = path.read_bytes()
        digest.update(relative)
        digest.update(b"\0")
        digest.update(str(len(payload)).encode("ascii"))
        digest.update(b"\0")
        digest.update(payload)
        digest.update(b"\0")
        total += len(payload)
    return digest.hexdigest(), total


def expanded_and_validated(start: Path, relaxng: etree.RelaxNG) -> tuple[etree._ElementTree, list[str]]:
    document = parse(start)
    document.xinclude()
    valid = relaxng.validate(document)
    diagnostics = [str(entry) for entry in relaxng.error_log]
    if not valid or diagnostics:
        raise RuntimeError(f"schema validation failed for {start}: {diagnostics}")
    return document, diagnostics


def build_payloads() -> dict[Path, bytes]:
    schema_payload = SCHEMA.read_bytes()
    if sha256(schema_payload) != SCHEMA_SHA256 or len(schema_payload) != 101829:
        raise RuntimeError("pinned PreTeXt schema identity changed")
    relaxng = etree.RelaxNG(parse(SCHEMA))

    companion_paths, companion_edges = closure(COMPANION_WRAPPER)
    companion_expanded, companion_diagnostics = expanded_and_validated(COMPANION_WRAPPER, relaxng)
    companion_hrefs = tuple(parse(COMPANION_WRAPPER).xpath("//xi:include/@href", namespaces={"xi": XI_NS}))
    if companion_hrefs != EXPECTED_COMPANION_HREFS:
        raise RuntimeError(f"Chapter 18 companion include order changed: {companion_hrefs}")
    companion_schema = {
        "schema_version": 1,
        "status": "pass",
        "source": identity(COMPANION_WRAPPER, "companion/chapter_18_connected_spaces_self_study.ptx"),
        "schema": {"path": SCHEMA_DISPLAY, "bytes": len(schema_payload), "sha256": sha256(schema_payload)},
        "pretext_resource_commit": PRETEXT_RESOURCE_COMMIT,
        "validation_engine": {"name": "lxml.etree.RelaxNG", "lxml": list(etree.LXML_VERSION)},
        "xinclude": {
            "all_local": True,
            "closure_file_count": len(companion_paths),
            "closure": [path.relative_to(ROOT).as_posix() for path in companion_paths],
        },
        "expanded_element_count": sum(1 for node in companion_expanded.getroot().iter() if isinstance(node.tag, str)),
        "diagnostics": companion_diagnostics,
    }
    companion_schema_payload = json_bytes(companion_schema)

    if WRAPPER.read_bytes() != expected_wrapper_bytes():
        raise RuntimeError("Chapters 1–18 wrapper differs from the exact authorized transform of Chapters 1–17")
    wrapper_document = parse(WRAPPER)
    prior_document = parse(PRIOR)
    macros = wrapper_document.xpath("//macros")
    prior_macros = prior_document.xpath("//macros")
    if len(macros) != 1 or len(prior_macros) != 1:
        raise RuntimeError("wrapper macro block cardinality changed")
    macros_payload = etree.tostring(macros[0], method="c14n", with_comments=True)
    prior_macros_payload = etree.tostring(prior_macros[0], method="c14n", with_comments=True)
    if macros_payload != prior_macros_payload:
        raise RuntimeError("inherited macro block changed")

    wrapper_hrefs = tuple(wrapper_document.xpath("//xi:include/@href", namespaces={"xi": XI_NS}))
    if wrapper_hrefs.count(EXPECTED_CH18_SOURCE) != 1 or wrapper_hrefs.count(EXPECTED_CH18_COMPANION) != 1:
        raise RuntimeError("Chapter 18 source/companion include cardinality changed")
    if wrapper_hrefs.index(EXPECTED_CH18_SOURCE) != wrapper_hrefs.index("./chap_Compact_topology.ptx") + 1:
        raise RuntimeError("Chapter 18 source include is not immediately after Chapter 17")
    if wrapper_hrefs.index(EXPECTED_CH18_COMPANION) != wrapper_hrefs.index("../companion/chapter_17_compact_spaces_self_study.ptx") + 1:
        raise RuntimeError("Chapter 18 companion include is not immediately after Chapter 17 companion")

    cumulative_paths, cumulative_edges = closure(WRAPPER)
    expanded, diagnostics = expanded_and_validated(WRAPPER, relaxng)
    nodes = [node for node in expanded.getroot().iter() if isinstance(node.tag, str)]
    ids = [node.get(XML_ID) for node in nodes if node.get(XML_ID)]
    refs = [node.get("ref") for node in nodes if etree.QName(node).localname == "xref" and node.get("ref")]
    duplicate_ids = sorted(key for key, count in Counter(ids).items() if count > 1)
    unresolved = sorted(set(refs) - set(ids))
    if duplicate_ids or unresolved:
        raise RuntimeError(f"cumulative ID/xref gate failed: duplicates={duplicate_ids}, unresolved={unresolved}")
    closure_hash, closure_bytes = closure_identity(cumulative_paths)
    expanded_text = " ".join("".join(expanded.getroot().itertext()).split())
    exact_model_count = expanded_text.count(EXACT_MODEL)
    codex_count = expanded_text.count("OpenAI Codex")
    if exact_model_count != 9 or codex_count != 9:
        raise RuntimeError(f"model provenance count changed: exact={exact_model_count}, OpenAI Codex={codex_count}")

    companion_state = json.loads(COMPANION_QA.read_text(encoding="utf-8"))
    expected_counts = {
        "physical_prompt_occurrences": 128,
        "canonical_source_entries": 128,
        "occurrence_aliases": 0,
        "grouping_nodes": 6,
        "mastery_entries": 8,
        "total_entries": 136,
        "staged_surfaces": 544,
    }
    if companion_state.get("status") != "pass" or companion_state.get("counts") != expected_counts or companion_state.get("failures"):
        raise RuntimeError("Chapter 18 companion state is not sealed at 128/136/544")

    report = {
        "schema_version": 2,
        "status": "pass",
        "failures": [],
        "diagnostics": diagnostics,
        "source": identity(WRAPPER, "source/chapters_01_18_reader.ptx"),
        "prior_boundary": identity(PRIOR, "source/chapters_01_17_reader.ptx"),
        "schema": {"path": SCHEMA_DISPLAY, "bytes": len(schema_payload), "sha256": sha256(schema_payload)},
        "pretext_version_contract": PRETEXT_VERSION,
        "pretext_resource_commit": PRETEXT_RESOURCE_COMMIT,
        "runtime": {"engine": "lxml.etree.RelaxNG", "lxml": list(etree.LXML_VERSION), "python": platform.python_version()},
        "boundary": {
            "book_id": wrapper_document.getroot().xpath("string(//book/@xml:id)", namespaces={"xml": "http://www.w3.org/XML/1998/namespace"}),
            "edition_note_id": wrapper_document.getroot().xpath("string(//preface/@xml:id)", namespaces={"xml": "http://www.w3.org/XML/1998/namespace"}),
            "macros_c14n_sha256": sha256(macros_payload),
        },
        "checks": {
            "authorized_wrapper_delta_exact": True,
            "inherited_macros_unchanged": True,
            "chapter_18_source_order_exact": True,
            "chapter_18_companion_order_exact": True,
            "all_includes_local_and_resolved": True,
            "schema_valid": True,
            "all_xml_ids_unique": True,
            "all_xrefs_resolve": True,
            "model_provenance_exact": True,
            "companion_prompt_entry_stage_counts_exact": True,
        },
        "closure": {
            "hash_contract": "SHA-256 over sorted repo-relative UTF-8 path, NUL, decimal byte length, NUL, raw bytes, NUL",
            "sha256": closure_hash,
        },
        "counts": {
            "closure_files": len(cumulative_paths),
            "include_edges": cumulative_edges,
            "closure_total_bytes": closure_bytes,
            "expanded_elements": len(nodes),
            "xml_ids": len(ids),
            "unique_xml_ids": len(set(ids)),
            "xrefs": len(refs),
            "unique_xref_targets": len(set(refs)),
            "model_provenance_occurrences": exact_model_count,
            "canonical_source_entries": 128,
            "companion_entries": 136,
            "staged_surfaces": 544,
        },
        "duplicate_xml_ids": duplicate_ids,
        "unresolved_xrefs": unresolved,
        "model_provenance": {
            "required": EXACT_MODEL,
            "exact_required_occurrences": exact_model_count,
            "openai_codex_occurrences": codex_count,
            "chapter_18_wrapper_exact_count": " ".join("".join(companion_expanded.getroot().itertext()).split()).count(EXACT_MODEL),
            "edition_note_exact_count": " ".join("".join(wrapper_document.getroot().itertext()).split()).count(EXACT_MODEL),
        },
        "companion_schema": {
            "path": "qa/CHAPTER18_COMPANION_WRAPPER_SCHEMA_QA.json",
            "bytes": len(companion_schema_payload),
            "sha256": sha256(companion_schema_payload),
            "closure_files": len(companion_paths),
            "include_edges": companion_edges,
            "expanded_elements": companion_schema["expanded_element_count"],
        },
        "companion_state": identity(COMPANION_QA, "qa/CHAPTER18_COMPANION_QA.json"),
        "schema_admission_repairs": [
            identity(SOURCE / name, f"source/{name}")
            for name in ("sec_connect_sets.ptx", "sec_connect_subset_rn.ptx", "sec_ivt_fpt.ptx", "sec_connect_top_exer.ptx")
        ],
    }
    return {WRAPPER_SCHEMA_QA: companion_schema_payload, CUMULATIVE_QA: json_bytes(report)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated schema receipts byte for byte")
    args = parser.parse_args()
    payloads = build_payloads()
    if args.check:
        for path, expected in payloads.items():
            if not path.is_file() or path.read_bytes() != expected:
                raise SystemExit(f"deterministic Chapter 18 schema receipt differs: {path}")
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
