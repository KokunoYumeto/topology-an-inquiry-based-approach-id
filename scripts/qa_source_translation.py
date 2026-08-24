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


def subtree_topology_signature(
    root: etree._Element,
) -> list[tuple[str, tuple[tuple[str, str], ...], int]]:
    """Return preorder tags/attributes plus parent indices for one subtree."""
    signature: list[tuple[str, tuple[tuple[str, str], ...], int]] = []

    def visit(node: etree._Element, parent_index: int) -> None:
        node_index = len(signature)
        signature.append(
            (local_name(node), tuple(sorted(node.attrib.items())), parent_index)
        )
        for child in node:
            if isinstance(child.tag, str):
                visit(child, node_index)

    visit(root, -1)
    return signature


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
        "--allow-cross-file-element-block-move",
        action="append",
        default=[],
        metavar=(
            "SOURCE_FILE:ZERO_BASED_AUTHORITY_START:ELEMENT_COUNT:"
            "TARGET_FILE:ZERO_BASED_TRANSLATED_START:ROOT_TAG"
        ),
        help=(
            "Approve one complete authority subtree moved to another translated "
            "file. The subtree's element/attribute topology, xml:id values, and "
            "protected mathematics/code must be retained; prose may be localized."
        ),
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
    cross_file_move_allowances: list[dict[str, object]] = []
    for ordinal, specification in enumerate(args.allow_cross_file_element_block_move):
        try:
            (
                source_file,
                authority_start_text,
                count_text,
                target_file,
                translated_start_text,
                root_tag,
            ) = specification.rsplit(":", 5)
            authority_start = int(authority_start_text)
            count = int(count_text)
            translated_start = int(translated_start_text)
        except (ValueError, TypeError):
            raise SystemExit(
                f"invalid --allow-cross-file-element-block-move: {specification}"
            )
        if (
            not source_file
            or not target_file
            or not root_tag
            or count <= 0
        ):
            raise SystemExit(
                f"invalid --allow-cross-file-element-block-move: {specification}"
            )
        cross_file_move_allowances.append(
            {
                "ordinal": ordinal,
                "key": specification,
                "source_file": source_file,
                "authority_start": authority_start,
                "element_count": count,
                "target_file": target_file,
                "translated_start": translated_start,
                "root_tag": root_tag,
            }
        )
    observed_cross_file_element_block_moves: list[dict[str, object]] = []
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

    parsed_files: dict[
        str,
        tuple[Path, Path, etree._Element, etree._Element],
    ] = {}
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
        parsed_files[name] = (
            authority_path,
            translated_path,
            authority_root_node,
            translated_root_node,
        )

    colliding_cross_file_allowances: set[int] = set()
    for left_index, left in enumerate(cross_file_move_allowances):
        left_source_file = str(left["source_file"])
        left_target_file = str(left["target_file"])
        left_source_identity: object = left_source_file
        left_target_identity: object = left_target_file
        if left_source_file in parsed_files:
            left_source_identity = parsed_files[left_source_file][0].relative_to(
                authority_root
            )
        if left_target_file in parsed_files:
            left_target_identity = parsed_files[left_target_file][1].relative_to(
                translated_root
            )
        if left_source_identity == left_target_identity:
            failures.append(
                "cross-file element-block-move uses the same source and target file: "
                f"{left['key']}"
            )
            colliding_cross_file_allowances.add(int(left["ordinal"]))
        for right in cross_file_move_allowances[left_index + 1:]:
            right_source_file = str(right["source_file"])
            right_target_file = str(right["target_file"])
            right_source_identity: object = right_source_file
            right_target_identity: object = right_target_file
            if right_source_file in parsed_files:
                right_source_identity = parsed_files[right_source_file][0].relative_to(
                    authority_root
                )
            if right_target_file in parsed_files:
                right_target_identity = parsed_files[right_target_file][1].relative_to(
                    translated_root
                )
            source_overlap = (
                left_source_identity == right_source_identity
                and int(left["authority_start"])
                < int(right["authority_start"]) + int(right["element_count"])
                and int(right["authority_start"])
                < int(left["authority_start"]) + int(left["element_count"])
            )
            target_overlap = (
                left_target_identity == right_target_identity
                and int(left["translated_start"])
                < int(right["translated_start"]) + int(right["element_count"])
                and int(right["translated_start"])
                < int(left["translated_start"]) + int(left["element_count"])
            )
            if source_overlap or target_overlap:
                collision_kinds = []
                if source_overlap:
                    collision_kinds.append("authority-source")
                if target_overlap:
                    collision_kinds.append("translated-target")
                failures.append(
                    "colliding cross-file element-block-move allowances "
                    f"({'+'.join(collision_kinds)}): {left['key']} ; {right['key']}"
                )
                colliding_cross_file_allowances.update(
                    {int(left["ordinal"]), int(right["ordinal"])}
                )

    removed_authority_indices: dict[str, set[int]] = {}
    removed_translated_indices: dict[str, set[int]] = {}
    for allowance in cross_file_move_allowances:
        ordinal = int(allowance["ordinal"])
        specification = str(allowance["key"])
        if ordinal in colliding_cross_file_allowances:
            continue
        source_file = str(allowance["source_file"])
        target_file = str(allowance["target_file"])
        authority_start = int(allowance["authority_start"])
        translated_start = int(allowance["translated_start"])
        count = int(allowance["element_count"])
        expected_root_tag = str(allowance["root_tag"])
        if source_file not in parsed_files:
            failures.append(
                "cross-file element-block-move source is not a parsed input file: "
                f"{specification}"
            )
            continue
        if target_file not in parsed_files:
            failures.append(
                "cross-file element-block-move target is not a parsed input file: "
                f"{specification}"
            )
            continue

        source_authority_elements = elements(parsed_files[source_file][2])
        target_translated_elements = elements(parsed_files[target_file][3])
        if (
            authority_start < 0
            or authority_start + count > len(source_authority_elements)
        ):
            failures.append(
                "cross-file element-block-move authority range out of bounds: "
                f"{specification}"
            )
            continue
        if (
            translated_start < 0
            or translated_start + count > len(target_translated_elements)
        ):
            failures.append(
                "cross-file element-block-move translated range out of bounds: "
                f"{specification}"
            )
            continue

        authority_block = source_authority_elements[
            authority_start:authority_start + count
        ]
        translated_block = target_translated_elements[
            translated_start:translated_start + count
        ]
        authority_subtree = elements(authority_block[0])
        translated_subtree = elements(translated_block[0])
        if len(authority_subtree) != count or any(
            actual is not expected
            for actual, expected in zip(authority_block, authority_subtree)
        ):
            failures.append(
                "cross-file element-block-move authority range is not one complete "
                f"subtree: {specification}"
            )
            continue
        if len(translated_subtree) != count or any(
            actual is not expected
            for actual, expected in zip(translated_block, translated_subtree)
        ):
            failures.append(
                "cross-file element-block-move translated range is not one complete "
                f"subtree: {specification}"
            )
            continue
        authority_root_tag = local_name(authority_block[0])
        translated_root_tag = local_name(translated_block[0])
        if (
            authority_root_tag != expected_root_tag
            or translated_root_tag != expected_root_tag
        ):
            failures.append(
                "cross-file element-block-move root mismatch: "
                f"{specification}; authority={authority_root_tag}, "
                f"translated={translated_root_tag}"
            )
            continue

        authority_signature = subtree_topology_signature(authority_block[0])
        translated_signature = subtree_topology_signature(translated_block[0])
        if authority_signature != translated_signature:
            failures.append(
                "cross-file element-block-move subtree topology/attributes differ "
                f"from authority: {specification}"
            )
            continue
        authority_ids = [node.get(XML_ID) for node in authority_block if node.get(XML_ID)]
        translated_ids = [node.get(XML_ID) for node in translated_block if node.get(XML_ID)]
        if authority_ids != translated_ids:
            failures.append(
                "cross-file element-block-move xml:id sequence differs from "
                f"authority: {specification}"
            )
            continue
        authority_math = [
            (local_name(node), normalized_math(node))
            for node in authority_block
            if local_name(node) in MATH_TAGS
        ]
        translated_math = [
            (local_name(node), normalized_math(node))
            for node in translated_block
            if local_name(node) in MATH_TAGS
        ]
        if authority_math != translated_math:
            failures.append(
                "cross-file element-block-move protected mathematics differs from "
                f"authority: {specification}"
            )
            continue
        authority_code = [
            (local_name(node), serialized(node))
            for node in authority_block
            if local_name(node) in PROTECTED_TAGS
        ]
        translated_code = [
            (local_name(node), serialized(node))
            for node in translated_block
            if local_name(node) in PROTECTED_TAGS
        ]
        if authority_code != translated_code:
            failures.append(
                "cross-file element-block-move protected code differs from "
                f"authority: {specification}"
            )
            continue

        removed_authority_indices.setdefault(source_file, set()).update(
            range(authority_start, authority_start + count)
        )
        removed_translated_indices.setdefault(target_file, set()).update(
            range(translated_start, translated_start + count)
        )
        target_payload = serialized(translated_block[0]).encode("utf-8")
        observed_cross_file_element_block_moves.append(
            {
                "key": specification,
                "source_file": source_file,
                "source_authority_start": authority_start,
                "element_count": count,
                "target_file": target_file,
                "target_translated_start": translated_start,
                "root_tag": expected_root_tag,
                "xml_id": translated_block[0].get(XML_ID),
                "target_serialized_sha256": hashlib.sha256(target_payload).hexdigest(),
            }
        )

    for name in args.files:
        if name not in parsed_files:
            continue
        (
            authority_path,
            translated_path,
            authority_root_node,
            translated_root_node,
        ) = parsed_files[name]
        all_authority_elements = elements(authority_root_node)
        all_translated_elements = elements(translated_root_node)
        authority_elements = [
            node
            for index, node in enumerate(all_authority_elements)
            if index not in removed_authority_indices.get(name, set())
        ]
        translated_elements = [
            node
            for index, node in enumerate(all_translated_elements)
            if index not in removed_translated_indices.get(name, set())
        ]
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

        ids = [node.get(XML_ID) for node in all_translated_elements if node.get(XML_ID)]
        refs = [
            node.get("ref")
            for node in all_translated_elements
            if local_name(node) == "xref" and node.get("ref")
        ]
        all_ids.extend(ids)
        all_refs.extend(refs)
        complete_translated_tags = [local_name(node) for node in all_translated_elements]
        complete_translated_math = [
            node for node in all_translated_elements if local_name(node) in MATH_TAGS
        ]
        tag_counts = Counter(complete_translated_tags)
        rows.append({
            "file": name,
            "authority": hash_file(authority_path),
            "translated": hash_file(translated_path),
            "elements": len(all_translated_elements),
            "ids": len(ids),
            "xrefs": len(refs),
            "math": len(complete_translated_math),
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
    requested_cross_file_move_counts = Counter(
        args.allow_cross_file_element_block_move
    )
    observed_cross_file_move_counts = Counter(
        str(row["key"]) for row in observed_cross_file_element_block_moves
    )
    for specification, requested_count in sorted(
        requested_cross_file_move_counts.items()
    ):
        observed_count = observed_cross_file_move_counts.get(specification, 0)
        if requested_count != 1:
            failures.append(
                "cross-file element-block-move allowance must be specified exactly "
                f"once: {specification}; requested {requested_count} times"
            )
        if observed_count != 1:
            failures.append(
                "cross-file element-block-move allowance was not used exactly once: "
                f"{specification}; observed {observed_count} times"
            )
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
        "schema_version": 4,
        "status": "pass" if not failures else "fail",
        "files": rows,
        "combined_translated_sha256": combined.hexdigest(),
        "xml_ids": len(all_ids),
        "xrefs": len(all_refs),
        "missing_xref_targets": missing_refs,
        "approved_external_xref_targets": observed_external_xrefs,
        "approved_math_changes": observed_allowed_math_changes,
        "approved_element_insertions": observed_element_insertions,
        "approved_cross_file_element_block_moves": (
            observed_cross_file_element_block_moves
        ),
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
