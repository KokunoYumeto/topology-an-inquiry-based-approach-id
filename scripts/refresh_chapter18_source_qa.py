#!/usr/bin/env python3
"""Regenerate bounded Chapter 18 authority/source translation evidence."""

from __future__ import annotations

import argparse
from collections import Counter
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
AUTHORITY_COMMIT = "0c2d8f614ef87aa00de373f3418146c2f1d13bb9"
AUTHORITY = (
    LANE
    / "authority"
    / "gvsu-pinned"
    / f"topology-{AUTHORITY_COMMIT}"
    / "source"
)
SOURCE = ROOT / "source"
CONTROL = LANE / "00_control"
COMPARATOR = ROOT / "scripts" / "qa_source_translation.py"
CORRECTIONS = CONTROL / "SOURCE_CORRECTIONS.csv"
AUDIT = CONTROL / "CHAPTER18_AUTHORITY_AUDIT.md"
QA = ROOT / "qa" / "CHAPTER18_SOURCE_COMPLETE_QA.json"
RECEIPT = ROOT / "qa" / "CHAPTER18_SOURCE_TRANSLATION_RECEIPT.md"

FILES = (
    "chap_Connected_topology.ptx",
    "sec_connect_top_intro.ptx",
    "sec_connect_sets.ptx",
    "sec_connect_subset_rn.ptx",
    "sec_components.ptx",
    "sec_cut_sets.ptx",
    "sec_ivt_fpt.ptx",
    "sec_connect_top_summ.ptx",
    "sec_connect_top_exer.ptx",
)
EXTERNAL_XREFS = (
    "def_weaker_topologies",
    "ex_excluded_point_topology",
    "ex_particular_point_topology",
    "exp_K_topology",
    "thm_max_min",
)
CORRECTION_IDS = ("O003-C235", "O003-C236", "O003-C237", "O003-C238")
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XI_NS = "http://www.w3.org/2001/XInclude"
MATH_TAGS = {"m", "me", "men", "mrow"}
PROTECTED_TAGS = {"c", "code", "program", "sage"}
READER_CARRIERS = {"title", "p", "caption", "h", "term", "em"}

REPAIRS = (
    {
        "correction_id": "O003-C235",
        "file": "sec_connect_sets.ptx",
        "authority_lines": "171-187",
        "before": "theorem thm_connected_invariant was a child of the final activity task statement",
        "after": "the unchanged theorem is a section child immediately after the activity; the task prompt remains in place",
        "root_tag": "theorem",
        "xml_id": "thm_connected_invariant",
        "kind": "parent_hoist_after_activity",
    },
    {
        "correction_id": "O003-C236",
        "file": "sec_connect_subset_rn.ptx",
        "authority_lines": "41-58",
        "before": "lemma lem_separation_subset was a child of the final activity task statement",
        "after": "the unchanged lemma is a section child immediately after the activity; the task prompt remains in place",
        "root_tag": "lemma",
        "xml_id": "lem_separation_subset",
        "kind": "parent_hoist_after_activity",
    },
    {
        "correction_id": "O003-C237",
        "file": "sec_ivt_fpt.ptx",
        "authority_lines": "77-96",
        "before": "the fixed-point theorem was a child of the second activity introduction",
        "after": "the unchanged theorem is a section child immediately before that activity; the proof lead and hypotheses remain in its introduction",
        "root_tag": "theorem",
        "xml_id": None,
        "kind": "block_hoist_before_activity",
    },
    {
        "correction_id": "O003-C238",
        "file": "sec_connect_top_exer.ptx",
        "authority_lines": "153-170",
        "before": "an un-IDed definition/statement shell was nested in a divisional-exercise introduction",
        "after": "the same index term, reader text, inline markup, and mathematics form one paragraph labeled Definisi in that introduction",
        "root_tag": "definition",
        "xml_id": None,
        "kind": "definition_shell_flatten",
    },
)

UPSTREAM_DEFECTS = (
    ("sec_connect_top_intro.ptx", [12], "The phrase 'in the spaced' should read 'in the space'.", "Normalized in Indonesian prose and recorded here."),
    ("sec_connect_top_intro.ptx", [52], "The phrase 'topological space' is duplicated.", "Normalized in Indonesian prose and recorded here."),
    ("sec_connect_sets.ptx", [76, 77], "The proof asserts x+epsilon<v although the preceding distance bound establishes only x+epsilon<=v; the non-strict inequality is sufficient.", "Preserved; no silent mathematical rewrite."),
    ("sec_connect_sets.ptx", [86, 87, 88, 89], "The constructed interval shows that x is not a lower bound for V-prime, but the proof says V.", "Preserved; no silent proof rewrite."),
    ("sec_connect_subset_rn.ptx", [27], "The phrase 'to wxplain' contains a typographical error.", "Normalized in Indonesian prose and recorded here."),
    ("sec_components.ptx", [25], "The word 'compenents' is misspelled.", "Normalized in Indonesian prose and recorded here."),
    ("sec_components.ptx", [61], "The ambient-space statement says every element of lowercase x instead of X.", "Repaired explicitly as the sole approved non-text mathematics change."),
    ("sec_components.ptx", [28, 100], "The identifier act_connected_compenent contains the source misspelling.", "Preserved exactly as a protected identifier."),
    ("sec_cut_sets.ptx", [96, 97, 98], "For x in V and y=f(x), the proof writes x=f(y) in f(V) instead of y=f(x) in f(V).", "Preserved; no silent mathematical rewrite."),
    ("sec_cut_sets.ptx", [115, 116, 117, 118, 119, 120, 121, 122], "The proof concludes x is in U intersection V after explicitly deriving only x in U; it omits the parallel inference from y in f(V) to x in V.", "Preserved; no silent proof rewrite."),
    ("sec_connect_top_summ.ptx", [14], "The phrase 'topological space' is duplicated.", "Normalized in Indonesian prose and recorded here."),
    ("sec_connect_top_exer.ptx", [13, 14, 15, 16, 17], "The exercise introduces propagation of compactness but asks what connectedness implies about compactness under the other topology.", "Preserved faithfully rather than silently choosing an intended property."),
    ("sec_connect_top_exer.ptx", [139, 140], "The sentence 'no two ... homeomorphic' is missing 'are'.", "Normalized in Indonesian grammar and recorded here."),
    ("sec_connect_top_exer.ptx", [291], "The phrase 'a topological spaces' has inconsistent article and number.", "Normalized in Indonesian grammar and recorded here."),
    ("sec_connect_top_exer.ptx", [297, 305], "Two statements omit 'are' before 'homeomorphic spaces'.", "Normalized in Indonesian grammar and recorded here."),
    ("sec_connect_top_exer.ptx", [834], "The set entry {a,b,c,} has a stray trailing comma.", "Preserved exactly in protected mathematics and recorded here."),
)


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def identity(path: Path, display: str | None = None) -> dict[str, Any]:
    payload = path.read_bytes()
    return {"path": display or path.name, "bytes": len(payload), "sha256": sha256(payload)}


def parse(path: Path) -> etree._ElementTree:
    return etree.parse(str(path), etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False))


def local(node: etree._Element) -> str:
    return etree.QName(node).localname


def element_nodes(root: etree._Element) -> list[etree._Element]:
    return [node for node in root.iter() if isinstance(node.tag, str)]


def structural_signature(root: etree._Element) -> list[list[Any]]:
    result: list[list[Any]] = []

    def visit(node: etree._Element, parent: int) -> None:
        index = len(result)
        result.append([local(node), sorted(node.attrib.items()), parent])
        for child in node:
            if isinstance(child.tag, str):
                visit(child, index)

    visit(root, -1)
    return result


def serialized(node: etree._Element) -> str:
    return etree.tostring(node, encoding="unicode", with_tail=False)


def normalized_math(node: etree._Element) -> str:
    value = re.sub(r"\\text\s*\{[^{}]*\}", r"\\text{#localized-text#}", serialized(node))
    return " ".join(value.split())


def normalized_serialized(node: etree._Element) -> str:
    return " ".join(serialized(node).split())


def exact_one(nodes: list[Any], label: str) -> Any:
    if len(nodes) != 1:
        raise RuntimeError(f"{label}: expected exactly one node, found {len(nodes)}")
    return nodes[0]


def apply_approved_repairs(documents: dict[str, etree._ElementTree]) -> None:
    namespaces = {"xml": "http://www.w3.org/XML/1998/namespace"}
    for file_name, tag_name, xml_id in (
        ("sec_connect_sets.ptx", "theorem", "thm_connected_invariant"),
        ("sec_connect_subset_rn.ptx", "lemma", "lem_separation_subset"),
    ):
        root = documents[file_name].getroot()
        target = exact_one(root.xpath(f"//{tag_name}[@xml:id='{xml_id}']", namespaces=namespaces), f"{file_name}/{xml_id}")
        activity = exact_one(target.xpath("ancestor::activity"), f"{file_name}/{xml_id}/activity")
        section = activity.getparent()
        target.getparent().remove(target)
        section.insert(section.index(activity) + 1, target)

    root = documents["sec_ivt_fpt.ptx"].getroot()
    activity = exact_one(root.xpath("./activity[2]"), "sec_ivt_fpt.ptx/activity[2]")
    target = exact_one(activity.xpath("./introduction/theorem"), "sec_ivt_fpt.ptx/fixed-point theorem")
    section = activity.getparent()
    target.getparent().remove(target)
    section.insert(section.index(activity), target)

    root = documents["sec_connect_top_exer.ptx"].getroot()
    definition = exact_one(root.xpath("./exercise/introduction/definition"), "sec_connect_top_exer.ptx/local-connectedness definition")
    idx = exact_one(definition.xpath("./idx"), "local-connectedness idx")
    statement_p = exact_one(definition.xpath("./statement/p"), "local-connectedness statement/p")
    replacement = etree.Element("p")
    replacement.append(copy.deepcopy(idx))
    label = etree.Element("em")
    label.text = "Definition."
    replacement.append(label)
    for child in statement_p:
        replacement.append(copy.deepcopy(child))
    definition.getparent().replace(definition, replacement)


def run_shared_comparator() -> dict[str, Any]:
    command = [
        sys.executable,
        str(COMPARATOR),
        "--authority-root", str(AUTHORITY),
        "--translated-root", str(SOURCE),
        "--allow-math-change", "sec_components.ptx:28",
        "--allow-element-block-move", "sec_ivt_fpt.ptx:57:8:60:theorem",
        "--allow-authority-shell-removal", "sec_connect_top_exer.ptx:128:definition",
        "--allow-authority-shell-removal", "sec_connect_top_exer.ptx:131:statement",
        "--allow-authority-shell-removal", "sec_connect_top_exer.ptx:132:p",
        "--allow-element-insertion", "sec_connect_top_exer.ptx:128:p",
        "--allow-element-insertion", "sec_connect_top_exer.ptx:131:em",
    ]
    for target in EXTERNAL_XREFS:
        command.extend(("--allow-external-xref", target))
    command.extend(FILES)
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=False)
    if result.returncode != 0:
        raise RuntimeError(f"shared comparator failed ({result.returncode}): {result.stdout}{result.stderr}")
    report = json.loads(result.stdout)
    if report.get("status") != "pass" or report.get("failures"):
        raise RuntimeError(f"shared comparator did not pass: {report.get('failures')}")
    return report


def combined_identity(root: Path, framed: bool) -> dict[str, Any]:
    digest = hashlib.sha256()
    total = 0
    for name in FILES:
        payload = (root / name).read_bytes()
        if framed:
            prefix = name.encode("utf-8") + b"\0"
            digest.update(prefix)
            total += len(prefix)
        digest.update(payload)
        total += len(payload)
    value: dict[str, Any] = {"bytes": total, "sha256": digest.hexdigest()}
    if framed:
        value["contract"] = "For each file in the stated order: UTF-8 basename, one NUL byte, exact file bytes."
    return value


def correction_rows() -> dict[str, Any]:
    payload = CORRECTIONS.read_text(encoding="utf-8")
    rows = list(csv.DictReader(io.StringIO(payload, newline="")))
    selected = [row for row in rows if row["id"] in CORRECTION_IDS]
    if [row["id"] for row in selected] != list(CORRECTION_IDS):
        raise RuntimeError(f"Chapter 18 correction rows are missing or reordered: {[row['id'] for row in selected]}")
    canonical = "\n".join(",".join(row[field] for field in rows[0]) for row in selected).encode("utf-8")
    return {
        "path": "00_control/SOURCE_CORRECTIONS.csv",
        "ids": list(CORRECTION_IDS),
        "rows_sha256": sha256(canonical),
    }


def prior_source_ids() -> tuple[set[str], dict[str, Any]]:
    source_root = SOURCE.resolve()
    start = (SOURCE / "chapters_01_17_reader.ptx").resolve(strict=True)
    visited: set[Path] = set()
    ids: list[str] = []
    skipped = 0

    def visit(path: Path) -> None:
        nonlocal skipped
        resolved = path.resolve(strict=True)
        if resolved in visited:
            return
        try:
            resolved.relative_to(source_root)
        except ValueError:
            skipped += 1
            return
        visited.add(resolved)
        document = parse(resolved)
        ids.extend(node.get(XML_ID) for node in element_nodes(document.getroot()) if node.get(XML_ID))
        for href in document.xpath("//xi:include/@href", namespaces={"xi": XI_NS}):
            candidate = (resolved.parent / href).resolve(strict=True)
            try:
                candidate.relative_to(source_root)
            except ValueError:
                skipped += 1
                continue
            visit(candidate)

    visit(start)
    duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
    return set(ids), {
        "prior_source_closure_file_count": len(visited),
        "prior_source_xml_id_occurrences": len(ids),
        "prior_source_distinct_xml_ids": len(set(ids)),
        "prior_duplicate_ids": duplicates,
        "skipped_non_source_include_count": skipped,
        "method": "Recursive local XInclude traversal rooted at source/chapters_01_17_reader.ptx and restricted to repo/source; no directory scan.",
    }


def english_residue(documents: dict[str, etree._ElementTree]) -> list[dict[str, Any]]:
    pattern = re.compile(r"\b(the|and|are|with|that|this|prove|show|explain|assume|topological|connected|function|every|neighborhood|subset|space)\b", re.IGNORECASE)
    candidates: list[dict[str, Any]] = []
    for name, document in documents.items():
        for text_node in document.xpath("//text()"):
            parent = text_node.getparent()
            if parent is None or any(local(ancestor) in MATH_TAGS | PROTECTED_TAGS for ancestor in parent.iterancestors()) or local(parent) in MATH_TAGS | PROTECTED_TAGS:
                continue
            text = " ".join(str(text_node).split())
            hits = pattern.findall(text)
            if len(hits) >= 2:
                candidates.append({"file": name, "line": parent.sourceline, "text": text[:240], "hits": [hit.lower() for hit in hits]})
    return candidates


def build_payloads() -> dict[Path, bytes]:
    comparator_report = run_shared_comparator()
    authority_original = {name: parse(AUTHORITY / name) for name in FILES}
    translated = {name: parse(SOURCE / name) for name in FILES}
    authority_adjusted = {name: etree.ElementTree(copy.deepcopy(authority_original[name].getroot())) for name in FILES}
    apply_approved_repairs(authority_adjusted)

    rows: list[dict[str, Any]] = []
    all_ids: list[str] = []
    all_refs: list[str] = []
    localizations: list[dict[str, Any]] = []
    approved_math: list[dict[str, Any]] = []
    asset_occurrences: list[dict[str, Any]] = []
    reader_surface_count = 0
    failures: list[str] = []
    repair_evidence: list[dict[str, Any]] = []

    for repair in REPAIRS:
        name = str(repair["file"])
        original = authority_original[name].getroot()
        derivative = translated[name].getroot()
        if repair["xml_id"]:
            selector = f"//*[@xml:id='{repair['xml_id']}']"
            namespaces = {"xml": "http://www.w3.org/XML/1998/namespace"}
            source_node = exact_one(original.xpath(selector, namespaces=namespaces), f"{name}/{repair['xml_id']}/authority")
            target_node = exact_one(derivative.xpath(selector, namespaces=namespaces), f"{name}/{repair['xml_id']}/translated")
        elif name == "sec_ivt_fpt.ptx":
            source_node = exact_one(original.xpath("./activity[2]/introduction/theorem"), "authority fixed-point theorem")
            target_node = exact_one(derivative.xpath("./theorem[2]"), "translated fixed-point theorem")
        else:
            source_node = exact_one(original.xpath("./exercise/introduction/definition"), "authority local-connectedness definition")
            target_node = exact_one(derivative.xpath("./exercise/introduction/p[idx and em]"), "translated local-connectedness paragraph")
        evidence = dict(repair)
        evidence["authority_line"] = source_node.sourceline
        evidence["translated_line"] = target_node.sourceline
        evidence["authority_parent"] = local(source_node.getparent())
        evidence["translated_parent"] = local(target_node.getparent())
        if repair["kind"] != "definition_shell_flatten":
            source_topology = structural_signature(source_node)
            target_topology = structural_signature(target_node)
            if source_topology != target_topology:
                failures.append(f"formal-result subtree topology changed: {name}")
            evidence["retained_subtree_elements"] = len(source_topology)
            evidence["subtree_topology_sha256"] = sha256(json_bytes(source_topology))
        else:
            evidence["retained_math_nodes"] = sum(1 for node in source_node.iter() if isinstance(node.tag, str) and local(node) in MATH_TAGS)
            evidence["retained_index_nodes"] = len(target_node.xpath("./idx"))
            evidence["inserted_label"] = "Definisi."
        repair_evidence.append(evidence)

    for order, name in enumerate(FILES, start=1):
        authority_root = authority_adjusted[name].getroot()
        translated_root = translated[name].getroot()
        authority_nodes = element_nodes(authority_root)
        translated_nodes = element_nodes(translated_root)
        topology_ok = structural_signature(authority_root) == structural_signature(translated_root)
        if not topology_ok:
            failures.append(f"adjusted full element/attribute/parent topology differs: {name}")

        original_ids = [node.get(XML_ID) for node in element_nodes(authority_original[name].getroot()) if node.get(XML_ID)]
        translated_ids = [node.get(XML_ID) for node in translated_nodes if node.get(XML_ID)]
        ids_ok = original_ids == translated_ids
        if not ids_ok:
            failures.append(f"xml:id sequence differs: {name}")
        all_ids.extend(translated_ids)

        original_refs = [node.get("ref") for node in element_nodes(authority_original[name].getroot()) if local(node) == "xref" and node.get("ref")]
        translated_refs = [node.get("ref") for node in translated_nodes if local(node) == "xref" and node.get("ref")]
        refs_ok = original_refs == translated_refs
        if not refs_ok:
            failures.append(f"xref sequence differs: {name}")
        all_refs.extend(translated_refs)

        authority_math = [node for node in authority_nodes if local(node) in MATH_TAGS]
        translated_math = [node for node in translated_nodes if local(node) in MATH_TAGS]
        math_ok = len(authority_math) == len(translated_math)
        for index, (left, right) in enumerate(zip(authority_math, translated_math)):
            raw_left = normalized_serialized(left)
            raw_right = normalized_serialized(right)
            if raw_left == raw_right:
                continue
            if normalized_math(left) == normalized_math(right):
                source_text = re.findall(r"\\text\s*\{([^{}]*)\}", raw_left)
                translated_text = re.findall(r"\\text\s*\{([^{}]*)\}", raw_right)
                if len(source_text) != len(translated_text):
                    failures.append(f"math text localization cardinality differs: {name}:{index}")
                    math_ok = False
                else:
                    for source_value, target_value in zip(source_text, translated_text):
                        if source_value != target_value:
                            localizations.append({"file": name, "math_ordinal": index + 1, "authority_line": left.sourceline, "source_text": source_value, "translated_text": target_value})
                continue
            if name == "sec_components.ptx" and index == 28 and raw_left == "<m>x</m>" and raw_right == "<m>X</m>":
                approved_math.append({"key": f"{name}:{index}", "file": name, "authority_line": left.sourceline, "authority": raw_left, "translated": raw_right, "reason": "The prose quantifies every element of the ambient space X; lowercase x is a source symbol typo."})
                continue
            math_ok = False
            failures.append(f"unapproved protected-math change: {name}:{index}")
        if not math_ok:
            failures.append(f"math topology/content check failed: {name}")

        authority_protected = [normalized_serialized(node) for node in authority_nodes if local(node) in PROTECTED_TAGS]
        translated_protected = [normalized_serialized(node) for node in translated_nodes if local(node) in PROTECTED_TAGS]
        protected_ok = authority_protected == translated_protected
        if not protected_ok:
            failures.append(f"protected code differs: {name}")

        for left, right in zip(authority_nodes, translated_nodes):
            if local(left) in READER_CARRIERS and " ".join("".join(left.itertext()).split()):
                reader_surface_count += 1
                if not " ".join("".join(right.itertext()).split()):
                    failures.append(f"reader-facing surface became empty: {name}:{right.sourceline}")

        images = [node for node in translated_nodes if local(node) == "image"]
        descriptions = [node for node in translated_nodes if local(node) == "description"]
        for image in images:
            asset_occurrences.append({"file": name, "tag": "image", "attributes": dict(sorted(image.attrib.items()))})
        counts = Counter(local(node) for node in translated_nodes)
        rows.append({
            "order": order,
            "file": name,
            "authority": identity(AUTHORITY / name),
            "translated": identity(SOURCE / name),
            "elements": len(translated_nodes),
            "attributes": sum(len(node.attrib) for node in translated_nodes),
            "xml_ids": len(translated_ids),
            "xrefs": len(translated_refs),
            "tasks": counts["task"],
            "exercises": counts["exercise"],
            "activities_and_explorations": counts["activity"] + counts["exploration"],
            "math": sum(counts[tag] for tag in MATH_TAGS),
            "images": len(images),
            "descriptions": len(descriptions),
            "checks": {
                "xml_well_formed": True,
                "element_parent_topology_after_approved_repairs": topology_ok,
                "attributes": topology_ok,
                "xml_ids": ids_ok,
                "xrefs": refs_ok,
                "task_topology": topology_ok,
                "exercise_topology": topology_ok,
                "math_topology": math_ok,
                "protected_code": protected_ok,
                "asset_topology": topology_ok,
            },
        })

    duplicates = sorted(key for key, count in Counter(all_ids).items() if count > 1)
    if duplicates:
        failures.append(f"duplicate Chapter 18 xml:ids: {duplicates}")
    if len(localizations) != 7:
        failures.append(f"expected seven reader-facing math-text localizations, found {len(localizations)}")
    if len(approved_math) != 1:
        failures.append(f"expected one approved non-text math repair, found {len(approved_math)}")

    residue = english_residue(translated)
    if residue:
        failures.append(f"reader-facing English residue candidates found: {len(residue)}")

    prior_ids, xref_meta = prior_source_ids()
    if xref_meta["prior_duplicate_ids"]:
        failures.append(f"prior source closure has duplicate IDs: {xref_meta['prior_duplicate_ids']}")
    chapter_ids = set(all_ids)
    unique_refs = set(all_refs)
    internal_targets = sorted(unique_refs & chapter_ids)
    cumulative_targets = sorted(unique_refs - chapter_ids)
    missing_targets = sorted(unique_refs - chapter_ids - prior_ids)
    if tuple(cumulative_targets) != EXTERNAL_XREFS:
        failures.append(f"cumulative xref target set changed: {cumulative_targets}")
    if missing_targets:
        failures.append(f"unresolved xrefs: {missing_targets}")

    totals = {
        "files": len(rows),
        "elements": sum(row["elements"] for row in rows),
        "attributes": sum(row["attributes"] for row in rows),
        "xml_ids": len(all_ids),
        "distinct_xml_ids": len(set(all_ids)),
        "xrefs": len(all_refs),
        "distinct_xrefs": len(set(all_refs)),
        "tasks": sum(row["tasks"] for row in rows),
        "exercises": sum(row["exercises"] for row in rows),
        "activities_and_explorations": sum(row["activities_and_explorations"] for row in rows),
        "math": sum(row["math"] for row in rows),
        "images": sum(row["images"] for row in rows),
        "descriptions": sum(row["descriptions"] for row in rows),
        "reader_text_surfaces_verified_nonempty": reader_surface_count,
    }
    if failures:
        raise RuntimeError("; ".join(failures))

    report = {
        "schema_version": 6,
        "status": "pass",
        "failures": [],
        "authority": {"commit": AUTHORITY_COMMIT, "root": f"authority/gvsu-pinned/topology-{AUTHORITY_COMMIT}/source"},
        "comparator": identity(COMPARATOR, "scripts/qa_source_translation.py"),
        "generator": identity(Path(__file__), "scripts/refresh_chapter18_source_qa.py"),
        "source_corrections": correction_rows(),
        "checks": {
            "shared_comparator_with_narrow_allowances": True,
            "all_files_xml_well_formed": True,
            "all_element_attribute_parent_topology_preserved_after_four_repairs": True,
            "all_ids_preserved": True,
            "all_xrefs_preserved_and_resolved": True,
            "all_task_and_exercise_topology_preserved": True,
            "all_math_topology_preserved": True,
            "protected_code_preserved": True,
            "all_image_paths_attributes_and_descriptions_preserved": True,
            "reader_text_surfaces_nonempty": True,
            "reader_facing_english_residue_zero": True,
        },
        "approved_schema_admission_repairs": repair_evidence,
        "shared_comparator_allowance_evidence": {
            "element_block_moves": comparator_report["approved_element_block_moves"],
            "authority_shell_removals": comparator_report["approved_authority_shell_removals"],
            "element_insertions": comparator_report["approved_element_insertions"],
        },
        "approved_external_xref_targets": comparator_report["approved_external_xref_targets"],
        "approved_math_changes": approved_math,
        "math_text_localizations": localizations,
        "reader_facing_english_residue": {
            "candidate_count": 0,
            "candidates": [],
            "method": "Case-insensitive conservative multi-token English scan over translated text/tails, excluding mathematics and protected code carriers.",
        },
        "asset_topology": {"occurrences": asset_occurrences, "descriptions": totals["descriptions"], "preserved": True},
        "combined": {
            "authority_raw": combined_identity(AUTHORITY, False),
            "authority_framed": combined_identity(AUTHORITY, True),
            "translated_raw": combined_identity(SOURCE, False),
            "translated_framed": combined_identity(SOURCE, True),
        },
        "files": rows,
        "totals": totals,
        "xref_resolution": {
            **xref_meta,
            "internal_targets": internal_targets,
            "cumulative_targets": cumulative_targets,
            "missing_targets": missing_targets,
        },
        "upstream_defects": [
            {"file": file_name, "authority_lines": lines, "defect": defect, "action": action}
            for file_name, lines, defect, action in UPSTREAM_DEFECTS
        ],
    }
    qa_payload = json_bytes(report)

    table_lines = ["| # | File | Authority bytes / SHA-256 | Translation bytes / SHA-256 |", "|---:|---|---|---|"]
    for row in rows:
        table_lines.append(f"| {row['order']} | `{row['file']}` | {row['authority']['bytes']} / `{row['authority']['sha256']}` | {row['translated']['bytes']} / `{row['translated']['sha256']}` |")
    repair_lines = [f"- `{item['correction_id']}` — `{item['file']}` authority lines {item['authority_lines']}: {item['before']}; {item['after']}." for item in REPAIRS]
    defect_lines = [f"- `{file_name}` authority line(s) {', '.join(str(line) for line in lines)}: {defect} Action: {action}" for file_name, lines, defect, action in UPSTREAM_DEFECTS]
    audit_text = f"""# Chapter 18 authority audit

Status: **pass**

This bounded audit compares exactly the nine Chapter 18 files, in declared source order, against pinned authority commit `{AUTHORITY_COMMIT}`. It neither scans the repository nor alters source.

## Ordered file identities

{chr(10).join(table_lines)}

- Authority framed SHA-256: `{report['combined']['authority_framed']['sha256']}`.
- Translation framed SHA-256: `{report['combined']['translated_framed']['sha256']}`.

## Four schema-admission repairs

{chr(10).join(repair_lines)}

The shared comparator retains every descendant, attribute, ID, xref, math, code, task, exercise, and asset surface under explicit shell/block allowances. A second full parent-topology comparison applies only these four transforms in memory and then matches every adjusted authority element and parent exactly.

## Deterministic upstream defects

{chr(10).join(defect_lines)}

The complete machine report is `repo/qa/CHAPTER18_SOURCE_COMPLETE_QA.json` with SHA-256 `{sha256(qa_payload)}`.
"""
    audit_payload = audit_text.encode("utf-8")
    receipt_text = f"""# Chapter 18 source translation receipt

Status: **pass**

- Exact ordered scope: {len(FILES)} authority files and {len(FILES)} translated files.
- Preserved after exactly four declared schema-admission repairs: {totals['elements']} elements, {totals['attributes']} attributes, {totals['xml_ids']} unique IDs, {totals['xrefs']} xrefs, {totals['tasks']} tasks, {totals['exercises']} exercises, {totals['activities_and_explorations']} activities/explorations, {totals['math']} math nodes, {totals['images']} image occurrence, and {totals['descriptions']} descriptions.
- Reader-facing math text localizations: {len(localizations)}; approved non-text math repair: {len(approved_math)}.
- Reader-facing English residue candidates: 0.
- Duplicate Chapter 18 IDs: 0; unresolved local/cumulative xrefs: 0.
- Authority framed SHA-256: `{report['combined']['authority_framed']['sha256']}`.
- Translation framed SHA-256: `{report['combined']['translated_framed']['sha256']}`.
- Source QA SHA-256: `{sha256(qa_payload)}`.
- Authority audit SHA-256: `{sha256(audit_payload)}`.

The shared `qa_source_translation.py` gate passes with exact, used allowances for the fixed-point theorem block and the local-connectedness shell flatten. The two formal-result hoists that retain preorder position are additionally proven by the full parent-topology normalization gate. All five external Chapter 18 xrefs resolve through a bounded recursive source-only traversal rooted at `source/chapters_01_17_reader.ptx`.

All reported upstream defects remain explicitly recorded. Natural-language typos were translated according to their evident meaning, the single lowercase ambient-space symbol was repaired under an explicit math allowance, and substantive proof/prompt defects plus protected identifiers/math were not silently rewritten.
"""
    return {QA: qa_payload, AUDIT: audit_payload, RECEIPT: receipt_text.encode("utf-8")}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated evidence byte for byte")
    args = parser.parse_args()
    payloads = build_payloads()
    if args.check:
        for path, expected in payloads.items():
            if not path.is_file() or path.read_bytes() != expected:
                raise SystemExit(f"deterministic Chapter 18 source evidence differs: {path}")
    else:
        for path, payload in payloads.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        for path, payload in payloads.items():
            if path.read_bytes() != payload:
                raise SystemExit(f"byte-for-byte readback failed: {path}")
    print(json.dumps({"status": "pass", "check_only": args.check, "outputs": {path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.relative_to(LANE).as_posix(): {"bytes": len(payload), "sha256": sha256(payload)} for path, payload in payloads.items()}}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
