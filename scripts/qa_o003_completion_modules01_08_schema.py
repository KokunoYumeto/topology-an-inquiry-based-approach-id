#!/usr/bin/env python3
"""Pinned cumulative schema/ID/xref receipt for O003 completion Modules 1–8."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "source" / "o003_completion_modules_01_08_reader.ptx"
WRAPPER = ROOT / "completion" / "o003_c90_completion_self_study.ptx"
OUTPUT = ROOT / "qa" / "O003_COMPLETION_MODULES01_08_SCHEMA_QA.json"
SCHEMA = Path.home() / ".ptx" / "schema" / "pretext.rng"
SCHEMA_BYTES = 101829
SCHEMA_SHA256 = "fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0"
PRETEXT_RESOURCE_COMMIT = "9bce7e55911fb14e3e6e362bfa78bd6431c38597"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XI_NS = "http://www.w3.org/2001/XInclude"
NAMES = (
    "separation_completion",
    "countability_size",
    "nets_general_convergence",
    "arbitrary_products",
    "local_compactness",
    "metrization",
    "function_spaces",
    "integrated_mastery",
)
EXPECTED_READER_HREFS = tuple(f"../completion/module_{number:02d}_{name}.ptx" for number, name in enumerate(NAMES, 1))


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def identity(path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(payload), "sha256": sha256(payload)}


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def parse(path: Path) -> etree._ElementTree:
    return etree.parse(str(path), etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False))


def build() -> bytes:
    schema_payload = SCHEMA.read_bytes()
    if len(schema_payload) != SCHEMA_BYTES or sha256(schema_payload) != SCHEMA_SHA256:
        raise SystemExit("pinned PreTeXt schema identity changed")
    reader_unexpanded = parse(READER)
    hrefs = tuple(reader_unexpanded.xpath("//xi:include/@href", namespaces={"xi": XI_NS}))
    if hrefs != EXPECTED_READER_HREFS:
        raise SystemExit(f"cumulative reader include closure changed: {hrefs}")
    wrapper_hrefs = tuple(parse(WRAPPER).xpath("//xi:include/@href", namespaces={"xi": XI_NS}))
    expected_wrapper_hrefs = tuple(href.replace("../completion/", "./") for href in EXPECTED_READER_HREFS)
    if wrapper_hrefs != expected_wrapper_hrefs:
        raise SystemExit(f"shared wrapper include closure changed: {wrapper_hrefs}")
    reader_unexpanded.xinclude()
    relaxng = etree.RelaxNG(parse(SCHEMA))
    valid = relaxng.validate(reader_unexpanded)
    diagnostics = [str(entry) for entry in relaxng.error_log]
    if not valid or diagnostics:
        raise SystemExit(f"cumulative Modules 1–8 schema validation failed: {diagnostics}")
    nodes = [node for node in reader_unexpanded.getroot().iter() if isinstance(node.tag, str)]
    ids = [node.get(XML_ID) for node in nodes if node.get(XML_ID)]
    refs = [node.get("ref") for node in nodes if etree.QName(node).localname == "xref" and node.get("ref")]
    duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
    unresolved = sorted(set(refs) - set(ids))
    if duplicates or unresolved:
        raise SystemExit(f"cumulative ID/xref gate failed: duplicates={duplicates}, unresolved={unresolved}")
    modules = [ROOT / href.replace("../", "") for href in hrefs]
    report = {
        "schema_version": 1,
        "status": "pass",
        "failures": [],
        "diagnostics": diagnostics,
        "source": identity(READER),
        "wrapper": identity(WRAPPER),
        "modules": [identity(path) for path in modules],
        "schema": {"path": "pretext-user-cache/schema/pretext.rng", "bytes": SCHEMA_BYTES, "sha256": SCHEMA_SHA256},
        "pretext_resource_commit": PRETEXT_RESOURCE_COMMIT,
        "validation_engine": {"name": "lxml.etree.RelaxNG", "lxml": list(etree.LXML_VERSION)},
        "xinclude": {"all_local": True, "closure_file_count": 9, "closure": [READER.relative_to(ROOT).as_posix()] + [path.relative_to(ROOT).as_posix() for path in modules]},
        "checks": {"xml_well_formed": True, "schema_valid": True, "xml_ids_unique": True, "all_xrefs_resolve": True, "shared_wrapper_matches_reader": True},
        "counts": {"modules": 8, "expanded_elements": len(nodes), "xml_ids": len(ids), "unique_xml_ids": len(set(ids)), "xrefs": len(refs), "unique_xref_targets": len(set(refs))},
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
            raise SystemExit("schema receipt readback failed")
    print(json.dumps({"status": "pass", "check_only": args.check, "output": {"path": OUTPUT.relative_to(ROOT).as_posix(), "bytes": len(payload), "sha256": sha256(payload)}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
