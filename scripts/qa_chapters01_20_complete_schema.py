#!/usr/bin/env python3
"""Fail-closed pinned-schema and ID/xref QA for the complete Chapters 1--20 reader."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
from typing import Any
from urllib.parse import unquote, urlsplit

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "source" / "chapters_01_20_complete_reader.ptx"
COMPLETION_WRAPPER = ROOT / "completion" / "o003_c90_completion_self_study.ptx"
CHAPTER20_COMPANION = ROOT / "companion" / "chapter_20_product_topology_self_study.ptx"
CHAPTER20_APPENDIX_ADAPTER = ROOT / "companion" / "chapter_20_product_topology_self_study_appendix.ptx"
OUTPUT = ROOT / "qa" / "CHAPTERS01_20_COMPLETE_SCHEMA_QA.json"
SCHEMA = Path.home() / ".ptx" / "schema" / "pretext.rng"
SCHEMA_DISPLAY = "pretext-user-cache/schema/pretext.rng"
SCHEMA_BYTES = 101829
SCHEMA_SHA256 = "fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0"
PRETEXT_VERSION = "1.7.5"
PRETEXT_RESOURCE_COMMIT = "9bce7e55911fb14e3e6e362bfa78bd6431c38597"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XI_NS = "http://www.w3.org/2001/XInclude"

COMPLETION_RECEIPTS = (
    ROOT / "qa" / "O003_COMPLETION_MODULES01_08_SCHEMA_QA.json",
    ROOT / "qa" / "O003_COMPLETION_CURRENT_QA.json",
    ROOT / "backend" / "o003_completion_current_manifest.json",
)
CHAPTER20_RECEIPTS = (
    ROOT / "qa" / "CHAPTER20_SOURCE_IDENTITY_QA.json",
    ROOT / "qa" / "CHAPTER20_SOURCE_SCHEMA_QA.json",
    ROOT / "qa" / "CHAPTER20_COMPANION_QA.json",
    ROOT / "qa" / "CHAPTER20_COMPANION_SCHEMA_QA.json",
)

EXPECTED_SOURCE_HREFS = (
    "./chap_sets.ptx",
    "./chap_functions.ptx",
    "./chap_metric_spaces.ptx",
    "./chap_metric_spaces_apps.ptx",
    "./chap_glb.ptx",
    "./chap_continuous_functions.ptx",
    "./chap_open_balls.ptx",
    "./chap_open_sets.ptx",
    "./chap_sequences.ptx",
    "./chap_closed_sets.ptx",
    "./chap_metric_subspaces.ptx",
    "./chap_top_spaces.ptx",
    "./chap_Closed_sets_topology.ptx",
    "./chap_continuity_topology.ptx",
    "./chap_subspaces.ptx",
    "./chap_quotients.ptx",
    "./chap_Compact_topology.ptx",
    "./chap_Connected_topology.ptx",
    "./chap_Path_connected_topology.ptx",
    "./chap_Product_topology.ptx",
)
EXPECTED_BACKMATTER_HREFS = tuple(
    f"../companion/chapter_{number:02d}_{slug}_self_study.ptx"
    for number, slug in (
        (1, "sets"),
        (2, "functions"),
        (3, "metric_spaces"),
        (4, "metric_space_applications"),
        (5, "greatest_lower_bound"),
        (6, "continuous_functions"),
        (7, "open_balls"),
        (8, "open_sets"),
        (9, "sequences"),
        (10, "closed_sets"),
        (11, "metric_subspaces"),
        (12, "topological_spaces"),
        (13, "closed_sets_topological_spaces"),
        (14, "continuity_homeomorphisms"),
        (15, "subspaces"),
        (16, "quotient_spaces"),
        (17, "compact_spaces"),
        (18, "connected_spaces"),
        (19, "path_connected_spaces"),
    )
) + (
    "../companion/chapter_20_product_topology_self_study_appendix.ptx",
    "../completion/o003_c90_completion_self_study.ptx",
)
EXPECTED_COMPLETION_HREFS = tuple(f"./module_{number:02d}_{slug}.ptx" for number, slug in (
    (1, "separation_completion"),
    (2, "countability_size"),
    (3, "nets_general_convergence"),
    (4, "arbitrary_products"),
    (5, "local_compactness"),
    (6, "metrization"),
    (7, "function_spaces"),
    (8, "integrated_mastery"),
))


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


def sanitize(value: str) -> str:
    variants = {str(ROOT), str(ROOT).replace("\\", "/"), ROOT.as_uri()}
    result = value
    for prefix in sorted(variants, key=len, reverse=True):
        result = result.replace(prefix, "<repo>")
    return result


def resolve_include(source: Path, href: str) -> Path:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError(f"non-local or decorated XInclude href in {source.relative_to(ROOT)}: {href!r}")
    decoded = unquote(parsed.path)
    if not decoded:
        raise ValueError(f"empty XInclude href in {source.relative_to(ROOT)}")
    target = (source.parent / decoded).resolve(strict=True)
    try:
        target.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"XInclude target escapes repository: {href!r}") from exc
    if not target.is_file():
        raise ValueError(f"XInclude target is not a file: {href!r}")
    return target


def closure(start: Path) -> tuple[list[Path], list[dict[str, str]]]:
    ordered: list[Path] = []
    visited: set[Path] = set()
    active: list[Path] = []
    edges: list[dict[str, str]] = []

    def visit(path: Path) -> None:
        resolved = path.resolve(strict=True)
        if resolved in active:
            cycle = " -> ".join(item.relative_to(ROOT).as_posix() for item in (*active, resolved))
            raise ValueError(f"XInclude cycle: {cycle}")
        if resolved in visited:
            return
        visited.add(resolved)
        ordered.append(resolved)
        active.append(resolved)
        document = parse(resolved)
        for href in document.xpath("//xi:include/@href", namespaces={"xi": XI_NS}):
            target = resolve_include(resolved, href)
            edges.append({
                "source": resolved.relative_to(ROOT).as_posix(),
                "href": href,
                "target": target.relative_to(ROOT).as_posix(),
            })
            visit(target)
        active.pop()

    visit(start)
    return ordered, edges


def closure_identity(paths: list[Path]) -> tuple[str, int]:
    digest = hashlib.sha256()
    total = 0
    for path in sorted(paths, key=lambda value: value.relative_to(ROOT).as_posix().encode("utf-8")):
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


def check_receipt(path: Path, failures: list[str]) -> dict[str, Any]:
    if not path.is_file():
        failures.append(f"missing prerequisite receipt: {path.relative_to(ROOT).as_posix()}")
        return {"path": path.relative_to(ROOT).as_posix(), "missing": True}
    row = identity(path)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"invalid prerequisite JSON: {path.relative_to(ROOT).as_posix()}: {type(exc).__name__}")
        return row
    status = value.get("status")
    accepted = status == "pass" or (
        path == ROOT / "backend" / "o003_completion_current_manifest.json"
        and status == "modules_01_08_complete_schema_and_backend_qa_pass"
    )
    if not accepted:
        failures.append(f"prerequisite receipt is not passing: {path.relative_to(ROOT).as_posix()}: {status!r}")
    if isinstance(value.get("failures"), list) and value["failures"]:
        failures.append(f"prerequisite receipt contains failures: {path.relative_to(ROOT).as_posix()}")
    if isinstance(value.get("diagnostics"), list) and value["diagnostics"]:
        failures.append(f"prerequisite receipt contains diagnostics: {path.relative_to(ROOT).as_posix()}")
    return row


def build() -> bytes:
    failures: list[str] = []
    diagnostics: list[str] = []
    duplicate_ids: list[str] = []
    unresolved_refs: list[str] = []
    closure_paths: list[Path] = []
    edges: list[dict[str, str]] = []
    expanded_elements = 0
    ids: list[str] = []
    refs: list[str] = []
    tag_counts: Counter[str] = Counter()

    schema_payload = SCHEMA.read_bytes()
    schema_identity = identity(SCHEMA, SCHEMA_DISPLAY)
    if len(schema_payload) != SCHEMA_BYTES or sha256(schema_payload) != SCHEMA_SHA256:
        failures.append("pinned PreTeXt schema identity changed")

    receipt_rows = [check_receipt(path, failures) for path in (*CHAPTER20_RECEIPTS, *COMPLETION_RECEIPTS)]

    reader_document = parse(READER)
    root = reader_document.getroot()
    book_ids = reader_document.xpath("/pretext/book/@xml:id", namespaces={"xml": "http://www.w3.org/XML/1998/namespace"})
    if book_ids != ["o003-c90-complete-reader"]:
        failures.append(f"complete-reader book ID changed: {book_ids}")
    source_hrefs = tuple(reader_document.xpath("/pretext/book/part/xi:include/@href", namespaces={"xi": XI_NS}))
    backmatter_hrefs = tuple(reader_document.xpath("/pretext/book/backmatter/xi:include/@href", namespaces={"xi": XI_NS}))
    if source_hrefs != EXPECTED_SOURCE_HREFS:
        failures.append(f"ordered 20-chapter include list changed: {source_hrefs}")
    if backmatter_hrefs != EXPECTED_BACKMATTER_HREFS:
        failures.append(f"ordered companion/completion include list changed: {backmatter_hrefs}")

    completion_document = parse(COMPLETION_WRAPPER)
    completion_hrefs = tuple(completion_document.xpath("//xi:include/@href", namespaces={"xi": XI_NS}))
    if completion_hrefs != EXPECTED_COMPLETION_HREFS:
        failures.append(f"ordered completion-module include list changed: {completion_hrefs}")

    companion_payload = CHAPTER20_COMPANION.read_bytes()
    expected_adapter_payload = companion_payload.replace(b"<chapter ", b"<appendix ", 1)
    if expected_adapter_payload == companion_payload or expected_adapter_payload.count(b"</chapter>") != 1:
        failures.append("canonical Chapter 20 companion wrapper no longer has one chapter root")
    else:
        expected_adapter_payload = expected_adapter_payload.replace(b"</chapter>", b"</appendix>", 1)
        if CHAPTER20_APPENDIX_ADAPTER.read_bytes() != expected_adapter_payload:
            failures.append("Chapter 20 appendix adapter differs from the exact root-tag-only transform")

    try:
        closure_paths, edges = closure(READER)
    except Exception as exc:
        failures.append(sanitize(f"XInclude closure failed: {type(exc).__name__}: {exc}"))

    if closure_paths and len(schema_payload) == SCHEMA_BYTES and sha256(schema_payload) == SCHEMA_SHA256:
        expanded = parse(READER)
        try:
            expanded.xinclude()
        except Exception as exc:
            failures.append(sanitize(f"XInclude expansion failed: {type(exc).__name__}: {exc}"))
        else:
            relaxng = etree.RelaxNG(parse(SCHEMA))
            valid = relaxng.validate(expanded)
            diagnostics = [sanitize(str(entry)) for entry in relaxng.error_log]
            if not valid or diagnostics:
                failures.append(f"pinned RelaxNG validation failed with {len(diagnostics)} diagnostic(s)")
            nodes = [node for node in expanded.getroot().iter() if isinstance(node.tag, str)]
            expanded_elements = len(nodes)
            tag_counts = Counter(etree.QName(node).localname for node in nodes)
            ids = [node.get(XML_ID) for node in nodes if node.get(XML_ID)]
            refs = [
                node.get("ref")
                for node in nodes
                if etree.QName(node).localname == "xref" and node.get("ref")
            ]
            duplicate_ids = sorted(key for key, count in Counter(ids).items() if count > 1)
            unresolved_refs = sorted(set(refs) - set(ids))
            if duplicate_ids:
                failures.append(f"duplicate expanded XML IDs: {len(duplicate_ids)}")
            if unresolved_refs:
                failures.append(f"unresolved expanded xrefs: {len(unresolved_refs)}")

    closure_hash, closure_bytes = closure_identity(closure_paths) if closure_paths else (None, 0)
    closure_inventory = [identity(path) for path in closure_paths]
    report = {
        "schema_version": 1,
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "diagnostics": diagnostics,
        "source": identity(READER),
        "schema": schema_identity,
        "pretext_version_contract": PRETEXT_VERSION,
        "pretext_resource_commit": PRETEXT_RESOURCE_COMMIT,
        "runtime": {
            "engine": "lxml.etree.RelaxNG",
            "lxml": list(etree.LXML_VERSION),
            "python": platform.python_version(),
        },
        "direct_structure": {
            "book_id": book_ids[0] if len(book_ids) == 1 else None,
            "ordered_source_chapter_hrefs": list(source_hrefs),
            "ordered_backmatter_hrefs": list(backmatter_hrefs),
            "ordered_completion_module_hrefs": list(completion_hrefs),
            "source_chapters": len(source_hrefs),
            "self_study_companions": max(0, len(backmatter_hrefs) - 1),
            "completion_modules": len(completion_hrefs),
            "chapter_20_appendix_adapter": identity(CHAPTER20_APPENDIX_ADAPTER),
            "chapter_20_canonical_companion": identity(CHAPTER20_COMPANION),
        },
        "xinclude_closure": {
            "all_local_and_repo_bounded": bool(closure_paths) and not any("XInclude" in failure for failure in failures),
            "file_count": len(closure_paths),
            "include_edges": len(edges),
            "bytes": closure_bytes,
            "sha256": closure_hash,
            "hash_contract": "SHA-256 over UTF-8 repo-relative POSIX path, NUL, decimal byte length, NUL, exact raw bytes, NUL; files sorted by UTF-8 path bytes",
            "files": closure_inventory,
            "edges": edges,
        },
        "expanded_document": {
            "elements": expanded_elements,
            "tag_counts": dict(sorted(tag_counts.items())),
            "xml_ids": len(ids),
            "unique_xml_ids": len(set(ids)),
            "xrefs": len(refs),
            "unique_xref_targets": len(set(refs)),
            "duplicate_xml_ids": duplicate_ids,
            "unresolved_xrefs": unresolved_refs,
        },
        "checks": {
            "reader_well_formed": True,
            "exact_ordered_20_chapter_includes": source_hrefs == EXPECTED_SOURCE_HREFS,
            "exact_ordered_20_companion_plus_completion_includes": backmatter_hrefs == EXPECTED_BACKMATTER_HREFS,
            "exact_ordered_8_completion_modules": completion_hrefs == EXPECTED_COMPLETION_HREFS,
            "chapter_20_appendix_adapter_is_exact_root_transform": "Chapter 20 appendix adapter differs from the exact root-tag-only transform" not in failures,
            "xinclude_closure_complete_local_and_bounded": bool(closure_paths) and not any("XInclude" in failure for failure in failures),
            "pinned_schema_identity": len(schema_payload) == SCHEMA_BYTES and sha256(schema_payload) == SCHEMA_SHA256,
            "relaxng_valid": not diagnostics and not any("RelaxNG" in failure for failure in failures),
            "xml_ids_unique": not duplicate_ids,
            "all_xrefs_resolve": not unresolved_refs,
            "prerequisite_receipts_bound_and_passing": not any("prerequisite" in failure for failure in failures),
        },
        "prerequisite_receipts": receipt_rows,
    }
    return json_bytes(report)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = build()
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_bytes() != payload:
            raise SystemExit(f"deterministic schema receipt differs: {OUTPUT.relative_to(ROOT)}")
    else:
        OUTPUT.write_bytes(payload)
        if OUTPUT.read_bytes() != payload:
            raise SystemExit("schema receipt write/readback failed")
    report = json.loads(payload)
    print(json.dumps({
        "status": report["status"],
        "check_only": args.check,
        "failures": report["failures"],
        "output": {
            "path": OUTPUT.relative_to(ROOT).as_posix(),
            "bytes": len(payload),
            "sha256": sha256(payload),
        },
        "counts": {
            "closure_files": report["xinclude_closure"]["file_count"],
            "include_edges": report["xinclude_closure"]["include_edges"],
            "expanded_elements": report["expanded_document"]["elements"],
            "xml_ids": report["expanded_document"]["xml_ids"],
            "xrefs": report["expanded_document"]["xrefs"],
        },
    }, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
