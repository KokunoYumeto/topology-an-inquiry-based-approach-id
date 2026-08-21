#!/usr/bin/env python3
"""Fail-closed structural comparison for an explicit translated PreTeXt unit."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

from lxml import etree


XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
MATH_TAGS = {"m", "me", "men"}
PROTECTED_TAGS = {"c", "code", "program", "sage"}


def local_name(node: etree._Element) -> str:
    return etree.QName(node).localname if isinstance(node.tag, str) else ""


def elements(root: etree._Element) -> list[etree._Element]:
    return [node for node in root.iter() if isinstance(node.tag, str)]


def serialized(node: etree._Element) -> str:
    return etree.tostring(node, encoding="unicode", with_tail=False)


def normalized_math(node: etree._Element) -> str:
    value = serialized(node)
    value = re.sub(r"\\text\s*\{[^{}]*\}", r"\\text{#localized-text#}", value)
    return " ".join(value.split())


def hash_file(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "path": path.name,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authority-root", required=True, type=Path)
    parser.add_argument("--translated-root", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument(
        "--allow-math-change",
        action="append",
        default=[],
        metavar="FILE:ZERO_BASED_INDEX",
    )
    parser.add_argument(
        "--allow-element-insertion",
        action="append",
        default=[],
        metavar="FILE:ZERO_BASED_TRANSLATED_INDEX:TAG",
    )
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    authority_root = args.authority_root.resolve(strict=True)
    translated_root = args.translated_root.resolve(strict=True)
    xml_parser = etree.XMLParser(resolve_entities=False, no_network=True)
    failures: list[str] = []
    rows: list[dict[str, object]] = []
    all_ids: list[str] = []
    all_refs: list[str] = []
    allowed_math_changes = set(args.allow_math_change)
    observed_allowed_math_changes: list[dict[str, object]] = []
    insertion_allowances: dict[str, list[tuple[int, str, str]]] = {}
    for specification in args.allow_element_insertion:
        try:
            file_name, index_text, tag = specification.rsplit(":", 2)
            index = int(index_text)
        except (ValueError, TypeError):
            raise SystemExit(f"invalid --allow-element-insertion: {specification}")
        insertion_allowances.setdefault(file_name, []).append((index, tag, specification))
    observed_element_insertions: list[dict[str, object]] = []

    for name in args.files:
        authority_path = (authority_root / name).resolve(strict=True)
        translated_path = (translated_root / name).resolve(strict=True)
        try:
            authority_path.relative_to(authority_root)
            translated_path.relative_to(translated_root)
        except ValueError:
            failures.append(f"path escapes an allowed root: {name}")
            continue

        try:
            authority_root_node = etree.parse(str(authority_path), xml_parser).getroot()
            translated_root_node = etree.parse(str(translated_path), xml_parser).getroot()
        except (etree.XMLSyntaxError, OSError) as exc:
            failures.append(f"XML parse failure in {name}: {exc}")
            continue

        authority_elements = elements(authority_root_node)
        translated_elements = elements(translated_root_node)
        authority_tags = [local_name(node) for node in authority_elements]
        translated_tags = [local_name(node) for node in translated_elements]
        authority_attributes = [sorted(node.attrib.items()) for node in authority_elements]
        translated_attributes = [sorted(node.attrib.items()) for node in translated_elements]
        adjusted_translated_tags = list(translated_tags)
        adjusted_translated_attributes = list(translated_attributes)
        allowed_insertion_indices_for_file: set[int] = set()
        for index, expected_tag, specification in sorted(
            insertion_allowances.get(name, []), reverse=True
        ):
            if index < 0 or index >= len(translated_elements):
                failures.append(f"element-insertion allowance index out of range: {specification}")
                continue
            actual_tag = translated_tags[index]
            if actual_tag != expected_tag:
                failures.append(
                    f"element-insertion allowance tag mismatch: {specification}; got {actual_tag}"
                )
                continue
            observed_element_insertions.append({
                "key": specification,
                "element": serialized(translated_elements[index]),
            })
            allowed_insertion_indices_for_file.add(index)
            adjusted_translated_tags.pop(index)
            adjusted_translated_attributes.pop(index)
        if authority_tags != adjusted_translated_tags:
            first = next(
                (index for index, pair in enumerate(zip(authority_tags, adjusted_translated_tags)) if pair[0] != pair[1]),
                min(len(authority_tags), len(adjusted_translated_tags)),
            )
            failures.append(f"element sequence changed: {name}; first mismatch {first}")
        if authority_attributes != adjusted_translated_attributes:
            failures.append(f"attribute sequence changed: {name}")

        authority_math = [normalized_math(node) for node in authority_elements if local_name(node) in MATH_TAGS]
        translated_math = [
            normalized_math(node)
            for index, node in enumerate(translated_elements)
            if local_name(node) in MATH_TAGS
            and index not in allowed_insertion_indices_for_file
        ]
        if len(authority_math) != len(translated_math):
            failures.append(f"protected mathematics count changed: {name}")
        else:
            for index, (authority_value, translated_value) in enumerate(zip(authority_math, translated_math)):
                if authority_value == translated_value:
                    continue
                key = f"{name}:{index}"
                if key not in allowed_math_changes:
                    failures.append(f"unapproved protected-math change: {key}")
                    continue
                observed_allowed_math_changes.append({
                    "key": key,
                    "authority": authority_value,
                    "translated": translated_value,
                })

        authority_protected = [serialized(node) for node in authority_elements if local_name(node) in PROTECTED_TAGS]
        translated_protected = [serialized(node) for node in translated_elements if local_name(node) in PROTECTED_TAGS]
        if authority_protected != translated_protected:
            failures.append(f"protected code changed: {name}")

        ids = [node.get(XML_ID) for node in translated_elements if node.get(XML_ID)]
        refs = [node.get("ref") for node in translated_elements if local_name(node) == "xref" and node.get("ref")]
        all_ids.extend(ids)
        all_refs.extend(refs)
        tag_counts = Counter(translated_tags)
        rows.append({
            "file": name,
            "authority": hash_file(authority_path),
            "translated": hash_file(translated_path),
            "elements": len(translated_elements),
            "ids": len(ids),
            "xrefs": len(refs),
            "math": len(translated_math),
            "tasks": tag_counts["task"],
            "activities_and_explorations": tag_counts["activity"] + tag_counts["exploration"],
            "exercises": tag_counts["exercise"],
            "images": tag_counts["image"],
        })

    duplicate_ids = sorted(name for name, count in Counter(all_ids).items() if count > 1)
    if duplicate_ids:
        failures.append(f"duplicate xml:id values: {duplicate_ids}")
    missing_refs = sorted(set(all_refs) - set(all_ids))
    if missing_refs:
        failures.append(f"xref targets absent from explicit unit: {missing_refs}")
    unused_math_allowances = sorted(
        allowed_math_changes - {str(row["key"]) for row in observed_allowed_math_changes}
    )
    if unused_math_allowances:
        failures.append(f"unused protected-math allowances: {unused_math_allowances}")
    unused_insertion_allowances = sorted(
        set(args.allow_element_insertion)
        - {str(row["key"]) for row in observed_element_insertions}
    )
    if unused_insertion_allowances:
        failures.append(f"unused element-insertion allowances: {unused_insertion_allowances}")

    combined = hashlib.sha256()
    for row in rows:
        name = str(row["file"])
        combined.update(name.encode("utf-8"))
        combined.update(b"\0")
        combined.update((translated_root / name).read_bytes())

    report = {
        "schema_version": 1,
        "status": "pass" if not failures else "fail",
        "files": rows,
        "combined_translated_sha256": combined.hexdigest(),
        "xml_ids": len(all_ids),
        "xrefs": len(all_refs),
        "missing_xref_targets": missing_refs,
        "approved_math_changes": observed_allowed_math_changes,
        "approved_element_insertions": observed_element_insertions,
        "failures": failures,
    }
    payload = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(payload, encoding="utf-8", newline="\n")
    print(payload, end="")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
