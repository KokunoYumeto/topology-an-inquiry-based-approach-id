#!/usr/bin/env python3
"""Emit a deterministic structural receipt for one bounded PDF artifact."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from PyPDF2 import PdfReader


def dereference(value):
    return value.get_object() if hasattr(value, "get_object") else value


def json_value(value):
    value = dereference(value)
    if isinstance(value, dict):
        return {str(key): json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_value(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def flatten_outlines(reader: PdfReader, nodes, depth: int = 0):
    rows = []
    for node in nodes:
        if isinstance(node, list):
            rows.extend(flatten_outlines(reader, node, depth + 1))
            continue
        title = getattr(node, "title", None) or str(node)
        try:
            page_index = reader.get_destination_page_number(node)
        except Exception:
            page_index = None
        rows.append({"depth": depth, "title": title, "physical_page": None if page_index is None else page_index + 1})
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    artifact_path = args.pdf.as_posix()
    pdf = args.pdf.resolve(strict=True)
    data = pdf.read_bytes()
    reader = PdfReader(str(pdf), strict=True)
    root = dereference(reader.trailer["/Root"])

    sizes = Counter()
    rotations = Counter()
    subtype_counts = Counter()
    uri_targets = []
    relative_uri_targets = []
    annotation_pages = []
    empty_text_pages = []
    extraction_errors = []
    bad_text = Counter()
    c0_controls = Counter()
    extracted_characters = 0

    for page_number, page in enumerate(reader.pages, start=1):
        media = page.mediabox
        sizes[(round(float(media.width), 4), round(float(media.height), 4))] += 1
        rotations[int(page.get("/Rotate", 0) or 0)] += 1
        try:
            text = page.extract_text() or ""
        except Exception as exc:
            extraction_errors.append({"physical_page": page_number, "error": str(exc)})
            text = ""
        extracted_characters += len(text)
        if not text.strip():
            empty_text_pages.append(page_number)
        bad_text["replacement_character"] += text.count("\ufffd")
        bad_text["nul"] += text.count("\x00")
        bad_text["cid_literal"] += len(re.findall(r"\(cid:\d+\)", text))
        for character in text:
            codepoint = ord(character)
            if codepoint < 32 and character not in "\t\n\r":
                c0_controls[f"U+{codepoint:04X}"] += 1

        page_annots = dereference(page.get("/Annots", [])) or []
        if page_annots:
            annotation_pages.append(page_number)
        for reference in page_annots:
            annot = dereference(reference)
            subtype_counts[str(annot.get("/Subtype", "unknown"))] += 1
            action = dereference(annot.get("/A", {})) or {}
            uri = action.get("/URI")
            if uri is not None:
                uri = str(uri)
                uri_targets.append(uri)
                split = urlsplit(uri)
                if not split.scheme and not split.netloc and not uri.startswith("#"):
                    relative_uri_targets.append(uri)

    try:
        outline_nodes = reader.outlines
    except Exception:
        outline_nodes = []
    outlines = flatten_outlines(reader, outline_nodes)
    outline_replacement_titles = [
        row for row in outlines if "\ufffd" in str(row.get("title", ""))
    ]

    names = dereference(root.get("/Names", {})) or {}
    mark_info = dereference(root.get("/MarkInfo", {})) or {}
    page_labels = json_value(root.get("/PageLabels")) if root.get("/PageLabels") is not None else None
    try:
        fields = reader.get_fields() or {}
    except Exception:
        fields = {}

    metadata = {str(key): str(value) for key, value in (reader.metadata or {}).items()}
    report = {
        "schema_version": 1,
        "status": "pass",
        "artifact": {
            "path": artifact_path,
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "pdf_header": data.splitlines()[0].decode("ascii", errors="replace"),
        },
        "pages": len(reader.pages),
        "page_sizes_points": [
            {"width": width, "height": height, "pages": count}
            for (width, height), count in sorted(sizes.items())
        ],
        "rotations": {str(key): value for key, value in sorted(rotations.items())},
        "encrypted": bool(reader.is_encrypted),
        "metadata": metadata,
        "page_labels": page_labels,
        "outlines": {
            "count": len(outlines),
            "max_depth": max((row["depth"] for row in outlines), default=0),
            "replacement_character_titles": outline_replacement_titles,
            "entries": outlines,
        },
        "annotations": {
            "count": sum(subtype_counts.values()),
            "subtypes": dict(sorted(subtype_counts.items())),
            "pages_with_annotations": annotation_pages,
            "uri_targets": uri_targets,
            "relative_uri_targets": relative_uri_targets,
        },
        "interactive": {
            "acroform_present": root.get("/AcroForm") is not None,
            "field_count": len(fields),
            "javascript_name_tree_present": "/JavaScript" in names,
            "open_action_present": root.get("/OpenAction") is not None,
            "additional_actions_present": root.get("/AA") is not None,
        },
        "accessibility": {
            "struct_tree_present": root.get("/StructTreeRoot") is not None,
            "marked": bool(mark_info.get("/Marked", False)),
        },
        "text_extraction": {
            "characters": extracted_characters,
            "empty_pages": empty_text_pages,
            "errors": extraction_errors,
            "replacement_characters": bad_text["replacement_character"],
            "nul_characters": bad_text["nul"],
            "cid_literals": bad_text["cid_literal"],
            "c0_controls": dict(sorted(c0_controls.items())),
        },
    }
    failures = []
    caveats = []
    if reader.is_encrypted:
        failures.append("PDF is encrypted")
    if extraction_errors:
        failures.append("text extraction errors")
    if any(bad_text.values()) or c0_controls:
        caveats.append(
            "PyPDF2 text extraction exposes missing or incomplete Unicode maps in some mathematical fonts; use the HTML reader as the primary accessible surface."
        )
    if relative_uri_targets:
        failures.append("relative URI annotation remains")
    if outline_replacement_titles:
        failures.append("outline title contains a replacement character")
    report["failures"] = failures
    report["caveats"] = caveats
    report["status"] = "pass" if not failures else "fail"

    payload = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8", newline="\n")
    print(payload, end="")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
