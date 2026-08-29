#!/usr/bin/env python3
"""Regenerate the deterministic Chapters 1–19 schema and backend receipts."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
from typing import Any

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
COMPANION = ROOT / "companion"
BACKEND = ROOT / "backend"
QA = ROOT / "qa"
WRAPPER = SOURCE / "chapters_01_19_reader.ptx"
PRIOR = SOURCE / "chapters_01_18_reader.ptx"
COMPANION_WRAPPER = COMPANION / "chapter_19_path_connected_spaces_self_study.ptx"
SOURCE_QA = QA / "CHAPTER19_SOURCE_COMPLETE_QA.json"
COMPANION_QA = QA / "CHAPTER19_COMPANION_QA.json"
COMPANION_SCHEMA_QA = QA / "CHAPTER19_COMPANION_WRAPPER_SCHEMA_QA.json"
CUMULATIVE_QA = QA / "CHAPTER19_CUMULATIVE_SCHEMA_QA.json"
BACKEND_MANIFEST = BACKEND / "chapters_01_19_reader_manifest.json"
BACKEND_QA = QA / "CHAPTER19_BACKEND_QA.json"
SCHEMA = Path.home() / ".ptx" / "schema" / "pretext.rng"
SCHEMA_DISPLAY = "pretext-user-cache/schema/pretext.rng"
SCHEMA_SHA256 = "fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0"
PRETEXT_VERSION = "1.7.5"
PRETEXT_RESOURCE_COMMIT = "9bce7e55911fb14e3e6e362bfa78bd6431c38597"
UPSTREAM_COMMIT = "0c2d8f614ef87aa00de373f3418146c2f1d13bb9"
EXACT_MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XI_NS = "http://www.w3.org/2001/XInclude"
EXPECTED_CH19_SOURCE = "./chap_Path_connected_topology.ptx"
EXPECTED_CH19_COMPANION = "../companion/chapter_19_path_connected_spaces_self_study.ptx"
EXPECTED_COMPANION_HREFS = (
    "./chapter_19_source_guides_a.ptx",
    "./chapter_19_exercise_guides_a.ptx",
    "./chapter_19_exercise_guides_b.ptx",
    "./chapter_19_mastery.ptx",
)
EXPECTED_COMPANION_COUNTS = {
    "physical_prompt_occurrences": 39,
    "canonical_source_entries": 39,
    "occurrence_aliases": 0,
    "grouping_nodes": 2,
    "mastery_entries": 8,
    "total_entries": 47,
    "staged_surfaces": 188,
}


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def identity(path: Path, display: str | None = None) -> dict[str, Any]:
    payload = path.read_bytes()
    return {
        "path": display or path.relative_to(ROOT).as_posix(),
        "bytes": len(payload),
        "sha256": sha256(payload),
    }


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def parse(path: Path) -> etree._ElementTree:
    return etree.parse(
        str(path),
        etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False),
    )


def replace_once(payload: bytes, old: bytes, new: bytes) -> bytes:
    count = payload.count(old)
    if count != 1:
        raise RuntimeError(
            f"authorized wrapper transform expected one occurrence, found {count}: {old!r}"
        )
    return payload.replace(old, new)


def expected_wrapper_bytes() -> bytes:
    payload = PRIOR.read_bytes()
    replacements = (
        (b"o003-c90-chapters-01-18-reader", b"o003-c90-chapters-01-19-reader"),
        (
            "Bab 1-18 - Himpunan, Fungsi, Ruang Metrik, Ruang Topologi, Kekontinuan, Homeomorfisme, Subruang, Ruang Kuosien, Ruang Kompak, Keterhubungan, serta Pendamping Belajar Mandiri".encode(),
            "Bab 1-19 - Himpunan, Fungsi, Ruang Metrik, Ruang Topologi, Kekontinuan, Homeomorfisme, Subruang, Ruang Kuosien, Ruang Kompak, Keterhubungan, Keterhubungan Lintasan, serta Pendamping Belajar Mandiri".encode(),
        ),
        (b"o003-c90-ch18-edition-note", b"o003-c90-ch19-edition-note"),
        ("delapan belas bab pertama".encode(), "sembilan belas bab pertama".encode()),
        (
            "Ruang Topologi, Kekontinuan, Homeomorfisme, Subruang, Ruang Kuosien, Kekompakan, dan Keterhubungan".encode(),
            "Ruang Topologi, Kekontinuan, Homeomorfisme, Subruang, Ruang Kuosien, Kekompakan, Keterhubungan, dan Keterhubungan Lintasan".encode(),
        ),
        (
            b'      <xi:include href="./chap_Connected_topology.ptx"/>',
            b'      <xi:include href="./chap_Connected_topology.ptx"/>\n      <xi:include href="./chap_Path_connected_topology.ptx"/>',
        ),
        (
            b'      <xi:include href="../companion/chapter_18_connected_spaces_self_study.ptx"/>',
            b'      <xi:include href="../companion/chapter_18_connected_spaces_self_study.ptx"/>\n      <xi:include href="../companion/chapter_19_path_connected_spaces_self_study.ptx"/>',
        ),
        (b"Bab 1-18 ini", b"Bab 1-19 ini"),
        (
            b"Produksi berlanjut menurut urutan sumber dengan\n          Bab 19; isi lengkap Bab 20",
            b"Produksi berlanjut menurut urutan sumber dengan\n          Bab 20; isi lengkap Bab 20",
        ),
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


def expanded_and_validated(
    start: Path, relaxng: etree.RelaxNG
) -> tuple[etree._ElementTree, list[str]]:
    document = parse(start)
    document.xinclude()
    valid = relaxng.validate(document)
    diagnostics = [str(entry) for entry in relaxng.error_log]
    if not valid or diagnostics:
        raise RuntimeError(f"schema validation failed for {start}: {diagnostics}")
    return document, diagnostics


def normalized_text(document: etree._ElementTree) -> str:
    return " ".join("".join(document.getroot().itertext()).split())


def direct_units(wrapper_document: etree._ElementTree) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    source_hrefs = wrapper_document.xpath(
        "//part/xi:include/@href", namespaces={"xi": XI_NS}
    )
    companion_hrefs = wrapper_document.xpath(
        "//backmatter/xi:include/@href", namespaces={"xi": XI_NS}
    )

    def rows(hrefs: list[str], base: Path, license_id: str, component: str) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for number, href in enumerate(hrefs, start=1):
            path = (base / href).resolve(strict=True)
            document = parse(path)
            root = document.getroot()
            title = " ".join("".join(root.xpath("./title[1]//text()")) .split())
            result.append(
                {
                    "chapter": number,
                    "component": component,
                    "stable_unit_id": root.get(XML_ID),
                    "title": title,
                    "include_href": href,
                    "file": identity(path),
                    "license": license_id,
                }
            )
        return result

    return (
        rows(source_hrefs, SOURCE, "CC BY-NC-SA 3.0 (conservative treatment)", "GVSU translated spine"),
        rows(companion_hrefs, SOURCE, "CC BY 4.0", "original self-study companion"),
    )


def build_payloads() -> dict[Path, bytes]:
    schema_payload = SCHEMA.read_bytes()
    if sha256(schema_payload) != SCHEMA_SHA256 or len(schema_payload) != 101829:
        raise RuntimeError("pinned PreTeXt schema identity changed")
    relaxng = etree.RelaxNG(parse(SCHEMA))

    if WRAPPER.read_bytes() != expected_wrapper_bytes():
        raise RuntimeError(
            "Chapters 1–19 wrapper differs from the exact authorized transform of Chapters 1–18"
        )

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

    wrapper_hrefs = tuple(
        wrapper_document.xpath("//xi:include/@href", namespaces={"xi": XI_NS})
    )
    if wrapper_hrefs.count(EXPECTED_CH19_SOURCE) != 1:
        raise RuntimeError("Chapter 19 source include cardinality changed")
    if wrapper_hrefs.count(EXPECTED_CH19_COMPANION) != 1:
        raise RuntimeError("Chapter 19 companion include cardinality changed")
    if wrapper_hrefs.index(EXPECTED_CH19_SOURCE) != wrapper_hrefs.index("./chap_Connected_topology.ptx") + 1:
        raise RuntimeError("Chapter 19 source is not immediately after Chapter 18")
    if wrapper_hrefs.index(EXPECTED_CH19_COMPANION) != wrapper_hrefs.index("../companion/chapter_18_connected_spaces_self_study.ptx") + 1:
        raise RuntimeError("Chapter 19 companion is not immediately after Chapter 18 companion")

    companion_document = parse(COMPANION_WRAPPER)
    companion_hrefs = tuple(
        companion_document.xpath("//xi:include/@href", namespaces={"xi": XI_NS})
    )
    if companion_hrefs != EXPECTED_COMPANION_HREFS:
        raise RuntimeError(f"Chapter 19 companion include order changed: {companion_hrefs}")
    companion_paths, companion_edges = closure(COMPANION_WRAPPER)
    companion_expanded, companion_diagnostics = expanded_and_validated(
        COMPANION_WRAPPER, relaxng
    )

    cumulative_paths, cumulative_edges = closure(WRAPPER)
    expanded, diagnostics = expanded_and_validated(WRAPPER, relaxng)
    prior_expanded, _ = expanded_and_validated(PRIOR, relaxng)
    nodes = [node for node in expanded.getroot().iter() if isinstance(node.tag, str)]
    ids = [node.get(XML_ID) for node in nodes if node.get(XML_ID)]
    refs = [
        node.get("ref")
        for node in nodes
        if etree.QName(node).localname == "xref" and node.get("ref")
    ]
    duplicate_ids = sorted(key for key, count in Counter(ids).items() if count > 1)
    unresolved = sorted(set(refs) - set(ids))
    if duplicate_ids or unresolved:
        raise RuntimeError(
            f"cumulative ID/xref gate failed: duplicates={duplicate_ids}, unresolved={unresolved}"
        )

    source_state = json.loads(SOURCE_QA.read_text(encoding="utf-8"))
    source_counts = source_state.get("counts", {})
    if (
        source_state.get("status") != "pass"
        or source_counts.get("expanded_elements") != 1003
        or source_counts.get("unique_xml_ids") != 23
        or source_counts.get("xrefs") != 25
        or source_counts.get("tasks") != 35
        or source_counts.get("exercises") != 9
        or source_counts.get("images") != 5
        or source_state.get("failures")
    ):
        raise RuntimeError("Chapter 19 translated source state is not sealed")

    companion_state = json.loads(COMPANION_QA.read_text(encoding="utf-8"))
    if (
        companion_state.get("status") != "pass"
        or companion_state.get("counts") != EXPECTED_COMPANION_COUNTS
        or companion_state.get("failures")
    ):
        raise RuntimeError("Chapter 19 companion state is not sealed at 39/47/188")

    current_text = normalized_text(expanded)
    prior_model_count = normalized_text(prior_expanded).count(EXACT_MODEL)
    companion_model_count = normalized_text(companion_expanded).count(EXACT_MODEL)
    model_count = current_text.count(EXACT_MODEL)
    codex_count = current_text.count("OpenAI Codex")
    expected_model_count = prior_model_count + companion_model_count
    if companion_model_count != 5 or model_count != expected_model_count or codex_count != model_count:
        raise RuntimeError(
            f"model provenance count changed: prior={prior_model_count}, companion={companion_model_count}, current={model_count}, OpenAI Codex={codex_count}"
        )

    closure_hash, closure_bytes = closure_identity(cumulative_paths)
    source_units, companion_units = direct_units(wrapper_document)
    source_ids = [row["stable_unit_id"] for row in source_units]
    companion_ids = [row["stable_unit_id"] for row in companion_units]
    if (
        len(source_units) != 19
        or len(companion_units) != 19
        or any(value is None for value in source_ids + companion_ids)
        or len(set(source_ids + companion_ids)) != 38
        or source_units[-1]["include_href"] != EXPECTED_CH19_SOURCE
        or companion_units[-1]["include_href"] != EXPECTED_CH19_COMPANION
    ):
        raise RuntimeError("locale-neutral chapter/companion unit map is incomplete or unstable")

    manifest = {
        "schema_version": 1,
        "status": "pass",
        "role": "O003/C90 Point-Set Topology",
        "locale": "id-ID",
        "boundary": "complete translated GVSU Chapters 1–19 plus staged self-study companions",
        "source_authority": {
            "work": "Topology: An Inquiry-Based Approach",
            "author": "Steven Schlicker",
            "upstream_commit": UPSTREAM_COMMIT,
            "spine_license": "CC BY-NC-SA 3.0 (conservative treatment because source metadata conflicts)",
            "companion_license": "CC BY 4.0",
            "license_policy": "collection with per-component rights; licenses are not flattened",
            "non_endorsement": True,
        },
        "reader": identity(WRAPPER),
        "prior_boundary": identity(PRIOR),
        "source_units": source_units,
        "companion_units": companion_units,
        "closure": {
            "hash_contract": "SHA-256 over sorted repo-relative UTF-8 path, NUL, decimal byte length, NUL, raw bytes, NUL",
            "sha256": closure_hash,
            "files": len(cumulative_paths),
            "include_edges": cumulative_edges,
            "bytes": closure_bytes,
        },
        "topology": {
            "expanded_elements": len(nodes),
            "xml_ids": len(ids),
            "unique_xml_ids": len(set(ids)),
            "xrefs": len(refs),
            "unique_xref_targets": len(set(refs)),
            "duplicate_xml_ids": duplicate_ids,
            "unresolved_xrefs": unresolved,
        },
        "chapter_19_evidence": {
            "source_qa": identity(SOURCE_QA),
            "companion_qa": identity(COMPANION_QA),
            "companion_schema_qa": identity(COMPANION_SCHEMA_QA),
        },
        "model_provenance": {
            "exact_identity": EXACT_MODEL,
            "occurrences": model_count,
        },
    }
    manifest_payload = json_bytes(manifest)

    backend_qa = {
        "schema_version": 1,
        "status": "pass",
        "failures": [],
        "manifest": {
            "path": "backend/chapters_01_19_reader_manifest.json",
            "bytes": len(manifest_payload),
            "sha256": sha256(manifest_payload),
        },
        "checks": {
            "nineteen_ordered_source_units": True,
            "nineteen_ordered_companion_units": True,
            "all_stable_unit_ids_present_and_unique": True,
            "chapter_19_source_is_last": True,
            "chapter_19_companion_is_last": True,
            "per_component_rights_preserved": True,
            "closure_identity_bound": True,
            "source_and_companion_receipts_bound": True,
        },
        "counts": {
            "source_units": len(source_units),
            "companion_units": len(companion_units),
            "stable_unit_ids": len(set(source_ids + companion_ids)),
            "closure_files": len(cumulative_paths),
            "include_edges": cumulative_edges,
        },
    }
    backend_qa_payload = json_bytes(backend_qa)

    report = {
        "schema_version": 2,
        "status": "pass",
        "failures": [],
        "diagnostics": diagnostics,
        "source": identity(WRAPPER),
        "prior_boundary": identity(PRIOR),
        "schema": {
            "path": SCHEMA_DISPLAY,
            "bytes": len(schema_payload),
            "sha256": sha256(schema_payload),
        },
        "pretext_version_contract": PRETEXT_VERSION,
        "pretext_resource_commit": PRETEXT_RESOURCE_COMMIT,
        "runtime": {
            "engine": "lxml.etree.RelaxNG",
            "lxml": list(etree.LXML_VERSION),
            "python": platform.python_version(),
        },
        "boundary": {
            "book_id": wrapper_document.getroot().xpath(
                "string(//book/@xml:id)",
                namespaces={"xml": "http://www.w3.org/XML/1998/namespace"},
            ),
            "edition_note_id": wrapper_document.getroot().xpath(
                "string(//preface/@xml:id)",
                namespaces={"xml": "http://www.w3.org/XML/1998/namespace"},
            ),
            "macros_c14n_sha256": sha256(macros_payload),
        },
        "checks": {
            "authorized_wrapper_delta_exact": True,
            "inherited_macros_unchanged": True,
            "chapter_19_source_order_exact": True,
            "chapter_19_companion_order_exact": True,
            "all_includes_local_and_resolved": True,
            "schema_valid": True,
            "all_xml_ids_unique": True,
            "all_xrefs_resolve": True,
            "model_provenance_exact": True,
            "source_receipt_sealed": True,
            "companion_prompt_entry_stage_counts_exact": True,
            "backend_unit_map_exact": True,
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
            "model_provenance_occurrences": model_count,
            "canonical_source_entries": 39,
            "companion_entries": 47,
            "staged_surfaces": 188,
        },
        "duplicate_xml_ids": duplicate_ids,
        "unresolved_xrefs": unresolved,
        "model_provenance": {
            "required": EXACT_MODEL,
            "prior_boundary_occurrences": prior_model_count,
            "chapter_19_companion_occurrences": companion_model_count,
            "current_boundary_occurrences": model_count,
            "openai_codex_occurrences": codex_count,
        },
        "chapter_19_companion": {
            "closure_files": len(companion_paths),
            "include_edges": companion_edges,
            "expanded_elements": sum(
                1 for node in companion_expanded.getroot().iter() if isinstance(node.tag, str)
            ),
            "diagnostics": companion_diagnostics,
        },
        "source_state": identity(SOURCE_QA),
        "companion_state": identity(COMPANION_QA),
        "companion_schema_state": identity(COMPANION_SCHEMA_QA),
        "backend_manifest": {
            "path": "backend/chapters_01_19_reader_manifest.json",
            "bytes": len(manifest_payload),
            "sha256": sha256(manifest_payload),
        },
        "backend_qa": {
            "path": "qa/CHAPTER19_BACKEND_QA.json",
            "bytes": len(backend_qa_payload),
            "sha256": sha256(backend_qa_payload),
        },
    }
    return {
        BACKEND_MANIFEST: manifest_payload,
        BACKEND_QA: backend_qa_payload,
        CUMULATIVE_QA: json_bytes(report),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="verify generated receipts byte for byte"
    )
    args = parser.parse_args()
    payloads = build_payloads()
    if args.check:
        for path, expected in payloads.items():
            if not path.is_file() or path.read_bytes() != expected:
                raise SystemExit(f"deterministic Chapter 19 receipt differs: {path}")
    else:
        for path, payload in payloads.items():
            path.write_bytes(payload)
        for path, payload in payloads.items():
            if path.read_bytes() != payload:
                raise SystemExit(f"Chapter 19 receipt readback failed: {path}")
    print(
        json.dumps(
            {
                "status": "pass",
                "check_only": args.check,
                "outputs": {
                    path.relative_to(ROOT).as_posix(): {
                        "bytes": len(payload),
                        "sha256": sha256(payload),
                    }
                    for path, payload in payloads.items()
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
