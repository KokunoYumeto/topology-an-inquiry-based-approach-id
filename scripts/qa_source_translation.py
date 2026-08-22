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
# Protect every leaf-level mathematics carrier used by this corpus.  Display
# rows hold the actual TeX payload inside <md>, so omitting <mrow> would allow
# a changed multiline formula to escape the source-fidelity comparison.
MATH_TAGS = {"m", "me", "men", "mrow"}
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
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
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
    parser.add_argument(
        "--allow-element-block-move",
        action="append",
        default=[],
        metavar="FILE:ZERO_BASED_TRANSLATED_START:ELEMENT_COUNT:ZERO_BASED_AUTHORITY_START:ROOT_TAG",
    )
    parser.add_argument(
        "--allow-element-shell-move",
        action="append",
        default=[],
        metavar="FILE:ZERO_BASED_TRANSLATED_START:ELEMENT_COUNT:ZERO_BASED_AUTHORITY_START:ROOT_TAG",
        help=(
            "Move a retained ancestor shell whose descendants were extracted by "
            "separately approved insertions; the shell must match the authority "
            "subtree prefix and the final complete element sequence must match."
        ),
    )
    parser.add_argument(
        "--allow-external-xref",
        action="append",
        default=[],
        metavar="XML_ID",
        help=(
            "Permit a referenced xml:id that is intentionally outside the explicit "
            "unit; every allowance must be used."
        ),
    )
    parser.add_argument(
        "--allow-attribute-change",
        action="append",
        default=[],
        metavar="FILE:ZERO_BASED_ADJUSTED_INDEX:ATTRIBUTE",
        help=(
            "Permit one intentional attribute-value change after approved element "
            "insertions/moves; every allowance must be used."
        ),
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
    attribute_change_allowances: dict[str, set[tuple[int, str]]] = {}
    for specification in args.allow_attribute_change:
        try:
            file_name, index_text, attribute = specification.split(":", 2)
            index = int(index_text)
        except ValueError as error:
            raise SystemExit(f"invalid --allow-attribute-change: {specification}") from error
        if index < 0 or not attribute:
            raise SystemExit(f"invalid --allow-attribute-change: {specification}")
        attribute_change_allowances.setdefault(file_name, set()).add((index, attribute))
    observed_attribute_changes: list[dict[str, object]] = []
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
    move_allowances: dict[str, list[tuple[int, int, int, str, str]]] = {}
    for specification in args.allow_element_block_move:
        try:
            file_name, start_text, count_text, authority_start_text, root_tag = specification.rsplit(":", 4)
            start = int(start_text)
            count = int(count_text)
            authority_start = int(authority_start_text)
        except (ValueError, TypeError):
            raise SystemExit(f"invalid --allow-element-block-move: {specification}")
        if count <= 0:
            raise SystemExit(f"element-block-move count must be positive: {specification}")
        move_allowances.setdefault(file_name, []).append(
            (start, count, authority_start, root_tag, specification)
        )
    observed_element_block_moves: list[dict[str, object]] = []
    shell_move_allowances: dict[str, list[tuple[int, int, int, str, str]]] = {}
    for specification in args.allow_element_shell_move:
        try:
            file_name, start_text, count_text, authority_start_text, root_tag = specification.rsplit(":", 4)
            start = int(start_text)
            count = int(count_text)
            authority_start = int(authority_start_text)
        except (ValueError, TypeError):
            raise SystemExit(f"invalid --allow-element-shell-move: {specification}")
        if count <= 0:
            raise SystemExit(f"element-shell-move count must be positive: {specification}")
        shell_move_allowances.setdefault(file_name, []).append(
            (start, count, authority_start, root_tag, specification)
        )
    observed_element_shell_moves: list[dict[str, object]] = []

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
        adjusted_translated_elements = list(translated_elements)
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
            adjusted_translated_elements.pop(index)
        for start, count, authority_start, expected_root_tag, specification in move_allowances.get(name, []):
            if start < 0 or start + count > len(adjusted_translated_elements):
                failures.append(f"element-block-move translated range out of bounds: {specification}")
                continue
            if authority_start < 0 or authority_start + count > len(authority_elements):
                failures.append(f"element-block-move authority range out of bounds: {specification}")
                continue
            if start == authority_start:
                failures.append(f"element-block-move is a no-op: {specification}")
                continue
            block = adjusted_translated_elements[start:start + count]
            if not block or local_name(block[0]) != expected_root_tag:
                actual = local_name(block[0]) if block else "<empty>"
                failures.append(
                    f"element-block-move root mismatch: {specification}; got {actual}"
                )
                continue
            retained_ids = {id(node) for node in adjusted_translated_elements}
            retained_subtree = [
                node
                for node in block[0].iter()
                if isinstance(node.tag, str) and id(node) in retained_ids
            ]
            if len(retained_subtree) != count or any(
                actual is not expected for actual, expected in zip(block, retained_subtree)
            ):
                failures.append(
                    f"element-block-move does not select exactly one retained subtree: {specification}"
                )
                continue
            authority_block = authority_elements[authority_start:authority_start + count]
            authority_subtree = [
                node
                for node in authority_block[0].iter()
                if isinstance(node.tag, str)
            ]
            if len(authority_subtree) != count or any(
                actual is not expected for actual, expected in zip(authority_block, authority_subtree)
            ):
                failures.append(
                    f"element-block-move authority range is not one subtree: {specification}"
                )
                continue
            translated_signature = [
                (local_name(node), sorted(node.attrib.items())) for node in block
            ]
            authority_signature = [
                (local_name(node), sorted(node.attrib.items())) for node in authority_block
            ]
            if translated_signature != authority_signature:
                failures.append(
                    f"element-block-move subtree topology differs from authority: {specification}"
                )
                continue
            del adjusted_translated_elements[start:start + count]
            adjusted_translated_elements[authority_start:authority_start] = block
            moved_payload = serialized(block[0]).encode("utf-8")
            observed_element_block_moves.append({
                "key": specification,
                "translated_start_after_insertions": start,
                "element_count": count,
                "authority_start": authority_start,
                "root_tag": expected_root_tag,
                "xml_id": block[0].get(XML_ID),
                "serialized_root_sha256": hashlib.sha256(moved_payload).hexdigest(),
            })
        for start, count, authority_start, expected_root_tag, specification in shell_move_allowances.get(name, []):
            if start < 0 or start + count > len(adjusted_translated_elements):
                failures.append(f"element-shell-move translated range out of bounds: {specification}")
                continue
            if authority_start < 0 or authority_start + count > len(authority_elements):
                failures.append(f"element-shell-move authority range out of bounds: {specification}")
                continue
            if start == authority_start:
                failures.append(f"element-shell-move is a no-op: {specification}")
                continue
            block = adjusted_translated_elements[start:start + count]
            if not block or local_name(block[0]) != expected_root_tag:
                actual = local_name(block[0]) if block else "<empty>"
                failures.append(
                    f"element-shell-move root mismatch: {specification}; got {actual}"
                )
                continue
            retained_ids = {id(node) for node in adjusted_translated_elements}
            retained_subtree = [
                node
                for node in block[0].iter()
                if isinstance(node.tag, str) and id(node) in retained_ids
            ]
            if len(retained_subtree) != count or any(
                actual is not expected for actual, expected in zip(block, retained_subtree)
            ):
                failures.append(
                    f"element-shell-move does not select exactly one retained ancestor shell: {specification}"
                )
                continue
            authority_root = authority_elements[authority_start]
            authority_subtree = [
                node for node in authority_root.iter() if isinstance(node.tag, str)
            ]
            authority_prefix = authority_subtree[:count]
            if len(authority_prefix) != count or any(
                actual is not expected
                for actual, expected in zip(
                    authority_elements[authority_start:authority_start + count],
                    authority_prefix,
                )
            ):
                failures.append(
                    f"element-shell-move authority range is not a subtree prefix: {specification}"
                )
                continue
            translated_signature = [
                (local_name(node), sorted(node.attrib.items())) for node in block
            ]
            authority_signature = [
                (local_name(node), sorted(node.attrib.items())) for node in authority_prefix
            ]
            if translated_signature != authority_signature:
                failures.append(
                    f"element-shell-move topology differs from authority prefix: {specification}"
                )
                continue
            del adjusted_translated_elements[start:start + count]
            adjusted_translated_elements[authority_start:authority_start] = block
            moved_payload = serialized(block[0]).encode("utf-8")
            observed_element_shell_moves.append({
                "key": specification,
                "translated_start_after_insertions_and_block_moves": start,
                "element_count": count,
                "authority_start": authority_start,
                "authority_subtree_element_count": len(authority_subtree),
                "root_tag": expected_root_tag,
                "xml_id": block[0].get(XML_ID),
                "serialized_root_sha256": hashlib.sha256(moved_payload).hexdigest(),
            })
        adjusted_translated_tags = [local_name(node) for node in adjusted_translated_elements]
        adjusted_translated_attributes = [
            sorted(node.attrib.items()) for node in adjusted_translated_elements
        ]
        if authority_tags != adjusted_translated_tags:
            first = next(
                (index for index, pair in enumerate(zip(authority_tags, adjusted_translated_tags)) if pair[0] != pair[1]),
                min(len(authority_tags), len(adjusted_translated_tags)),
            )
            failures.append(f"element sequence changed: {name}; first mismatch {first}")
        observed_file_attribute_changes: set[tuple[int, str]] = set()
        if len(authority_attributes) == len(adjusted_translated_attributes):
            permitted = attribute_change_allowances.get(name, set())
            for index, (authority_row, translated_row) in enumerate(
                zip(authority_attributes, adjusted_translated_attributes)
            ):
                authority_map = dict(authority_row)
                translated_map = dict(translated_row)
                for attribute in sorted(set(authority_map) | set(translated_map)):
                    if authority_map.get(attribute) == translated_map.get(attribute):
                        continue
                    key = (index, attribute)
                    if key not in permitted:
                        failures.append(
                            f"unapproved attribute change: {name}:{index}:{attribute}"
                        )
                        continue
                    observed_file_attribute_changes.add(key)
                    observed_attribute_changes.append(
                        {
                            "key": f"{name}:{index}:{attribute}",
                            "file": name,
                            "adjusted_element_index": index,
                            "element": local_name(adjusted_translated_elements[index]),
                            "attribute": attribute,
                            "authority_value": authority_map.get(attribute),
                            "translated_value": translated_map.get(attribute),
                        }
                    )
            unused = sorted(permitted - observed_file_attribute_changes)
            if unused:
                failures.append(
                    f"unused attribute-change allowances for {name}: {unused}"
                )
        elif authority_attributes != adjusted_translated_attributes:
            failures.append(f"attribute sequence changed: {name}")

        authority_math = [normalized_math(node) for node in authority_elements if local_name(node) in MATH_TAGS]
        translated_math = [
            normalized_math(node)
            for node in adjusted_translated_elements
            if local_name(node) in MATH_TAGS
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
        translated_protected = [
            serialized(node)
            for node in adjusted_translated_elements
            if local_name(node) in PROTECTED_TAGS
        ]
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
    external_xref_allowances = set(args.allow_external_xref)
    observed_external_xrefs = sorted((set(all_refs) - set(all_ids)) & external_xref_allowances)
    missing_refs = sorted(set(all_refs) - set(all_ids) - external_xref_allowances)
    if missing_refs:
        failures.append(f"xref targets absent from explicit unit: {missing_refs}")
    unused_external_xref_allowances = sorted(
        external_xref_allowances - set(observed_external_xrefs)
    )
    if unused_external_xref_allowances:
        failures.append(
            f"unused external-xref allowances: {unused_external_xref_allowances}"
        )
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
    unused_move_allowances = sorted(
        set(args.allow_element_block_move)
        - {str(row["key"]) for row in observed_element_block_moves}
    )
    if unused_move_allowances:
        failures.append(f"unused element-block-move allowances: {unused_move_allowances}")
    unused_shell_move_allowances = sorted(
        set(args.allow_element_shell_move)
        - {str(row["key"]) for row in observed_element_shell_moves}
    )
    if unused_shell_move_allowances:
        failures.append(f"unused element-shell-move allowances: {unused_shell_move_allowances}")

    combined = hashlib.sha256()
    for row in rows:
        name = str(row["file"])
        combined.update(name.encode("utf-8"))
        combined.update(b"\0")
        combined.update((translated_root / name).read_bytes())

    report = {
        "schema_version": 3,
        "status": "pass" if not failures else "fail",
        "files": rows,
        "combined_translated_sha256": combined.hexdigest(),
        "xml_ids": len(all_ids),
        "xrefs": len(all_refs),
        "missing_xref_targets": missing_refs,
        "approved_external_xref_targets": observed_external_xrefs,
        "approved_math_changes": observed_allowed_math_changes,
        "approved_element_insertions": observed_element_insertions,
        "approved_element_block_moves": observed_element_block_moves,
        "approved_element_shell_moves": observed_element_shell_moves,
        "approved_attribute_changes": observed_attribute_changes,
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
