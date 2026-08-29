#!/usr/bin/env python3
"""Generate the pinned-schema and ID/xref receipt for completion Module 7."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "completion" / "module_07_function_spaces.ptx"
READER = ROOT / "source" / "o003_completion_module_07_reader.ptx"
OUTPUT = ROOT / "qa" / "O003_COMPLETION_MODULE07_SCHEMA_QA.json"
SCHEMA = Path.home() / ".ptx" / "schema" / "pretext.rng"
SCHEMA_BYTES = 101829
SCHEMA_SHA256 = "fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0"
PRETEXT_RESOURCE_COMMIT = "9bce7e55911fb14e3e6e362bfa78bd6431c38597"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XI_NS = "http://www.w3.org/2001/XInclude"


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
    parse(MODULE)
    reader_tree = parse(READER)
    hrefs = tuple(reader_tree.xpath("//xi:include/@href", namespaces={"xi": XI_NS}))
    if hrefs != ("../completion/module_07_function_spaces.ptx",):
        raise SystemExit(f"standalone Module 7 include closure changed: {hrefs}")
    reader_tree.xinclude()
    relaxng = etree.RelaxNG(parse(SCHEMA))
    valid = relaxng.validate(reader_tree)
    diagnostics = [str(entry) for entry in relaxng.error_log]
    if not valid or diagnostics:
        raise SystemExit(f"Module 7 schema validation failed: {diagnostics}")
    nodes = [node for node in reader_tree.getroot().iter() if isinstance(node.tag, str)]
    ids = [node.get(XML_ID) for node in nodes if node.get(XML_ID)]
    refs = [node.get("ref") for node in nodes if etree.QName(node).localname == "xref" and node.get("ref")]
    duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
    unresolved = sorted(set(refs) - set(ids))
    if duplicates or unresolved:
        raise SystemExit(f"Module 7 ID/xref gate failed: duplicates={duplicates}, unresolved={unresolved}")
    report = {
        "schema_version": 1,
        "status": "pass",
        "failures": [],
        "diagnostics": diagnostics,
        "source": identity(READER),
        "module": identity(MODULE),
        "schema": {"path": "pretext-user-cache/schema/pretext.rng", "bytes": SCHEMA_BYTES, "sha256": SCHEMA_SHA256},
        "pretext_resource_commit": PRETEXT_RESOURCE_COMMIT,
        "validation_engine": {"name": "lxml.etree.RelaxNG", "lxml": list(etree.LXML_VERSION)},
        "xinclude": {"all_local": True, "closure_file_count": 2, "closure": [READER.relative_to(ROOT).as_posix(), MODULE.relative_to(ROOT).as_posix()]},
        "checks": {"xml_well_formed": True, "schema_valid": True, "xml_ids_unique": True, "all_xrefs_resolve": True},
        "counts": {"expanded_elements": len(nodes), "xml_ids": len(ids), "unique_xml_ids": len(set(ids)), "xrefs": len(refs), "unique_xref_targets": len(set(refs))},
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
