#!/usr/bin/env python3
"""Freeze Chapter 20 source identity, bounded QA, and prompt inventory.

The script deliberately inspects only the nine Chapter 20 source files, their
frozen upstream counterparts, the pinned schema, and the task-local correction
ledger.  It writes deterministic JSON/CSV receipts and supports ``--check``.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import re

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
SOURCE = ROOT / "source"
AUTHORITY = (
    LANE
    / "authority"
    / "gvsu-pinned"
    / "topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9"
    / "source"
)
SCHEMA = Path.home() / ".ptx" / "schema" / "pretext.rng"
CORRECTIONS = LANE / "00_control" / "SOURCE_CORRECTIONS.csv"
WRAPPER = ROOT / "tmp" / "chapter20_schema_wrapper.ptx"

SOURCE_QA = ROOT / "qa" / "CHAPTER20_SOURCE_IDENTITY_QA.json"
PROMPT_JSON = ROOT / "backend" / "chapter_20_prompt_inventory.json"
PROMPT_CSV = ROOT / "backend" / "chapter_20_source_prompt_map.csv"
GROUPING_JSON = ROOT / "backend" / "chapter_20_grouping_nodes.json"

UPSTREAM_COMMIT = "0c2d8f614ef87aa00de373f3418146c2f1d13bb9"
SCHEMA_SHA256 = "fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0"
SCHEMA_BYTES = 101829
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"

FILES = (
    "chap_Product_topology.ptx",
    "sec_prod_top.ptx",
    "sec_top_prod_space.ptx",
    "sec_prod_top_exam.ptx",
    "sec_proj_cont_prod.ptx",
    "sec_prop_prod_top.ptx",
    "sec_prod_top_summ.ptx",
    "sec_prod_top_exer.ptx",
    "sec_prod_top_app.ptx",
)


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def identity(path: Path, root: Path = ROOT) -> dict[str, object]:
    payload = path.read_bytes()
    try:
        display = path.relative_to(root).as_posix()
    except ValueError:
        display = path.as_posix()
    return {"path": display, "bytes": len(payload), "sha256": sha256(payload)}


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def csv_bytes(rows: list[dict[str, object]], fields: tuple[str, ...]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return ("\ufeff" + stream.getvalue()).encode("utf-8")


def parse(path: Path) -> etree._ElementTree:
    return etree.parse(
        str(path),
        etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False, huge_tree=True),
    )


def qname(node: etree._Element) -> str:
    return etree.QName(node).localname


def xpath(node: etree._Element) -> str:
    return node.getroottree().getpath(node)


def nearest_real_id(node: etree._Element) -> str:
    cur: etree._Element | None = node
    while cur is not None:
        value = cur.get(XML_ID)
        if value:
            return value
        cur = cur.getparent()
    return qname(node.getroottree().getroot())


def c14n_hash(node: etree._Element) -> str:
    return sha256(etree.tostring(node, method="c14n", with_comments=True))


def carrier_nodes(root: etree._Element) -> list[tuple[etree._Element, str]]:
    result: list[tuple[etree._Element, str]] = []
    for node in root.iter():
        if not isinstance(node.tag, str):
            continue
        tag = qname(node)
        if tag == "task" and not node.xpath(".//task"):
            result.append((node, "atomic_task"))
        elif tag in {"exercise", "activity", "exploration"} and not node.xpath(".//task"):
            statement = node.find("statement")
            if statement is not None:
                result.append((statement, "direct_statement"))
            elif tag in {"activity", "exploration"} and node.find("p") is not None:
                result.append((node, "direct_body"))
    return result


def grouping_nodes(root: etree._Element) -> list[etree._Element]:
    return list(root.xpath(".//task[.//task]"))


def anchor_records(path: Path, source_file: str) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    root = parse(path).getroot()
    counters: Counter[tuple[str, str]] = Counter()
    prompts: list[dict[str, object]] = []
    for node, carrier in carrier_nodes(root):
        anchor_node = node.getparent() if carrier == "direct_statement" else node
        nearest = nearest_real_id(anchor_node)
        label = {"atomic_task": "task", "direct_statement": "statement", "direct_body": "body"}[carrier]
        counters[(nearest, label)] += 1
        synthetic = f"o003-gvsu-ch20-{nearest}-{label}-{counters[(nearest, label)]:02d}"
        prompts.append(
            {
                "source_anchor": synthetic,
                "source_anchor_kind": "synthetic_locale_neutral_alias",
                "authority_source_file": f"source/{source_file}",
                "authority_line": int(anchor_node.sourceline or node.sourceline or 0),
                "prompt_carrier": carrier,
                "xpath": xpath(anchor_node),
                "nearest_real_xml_id": nearest,
                "subtree_sha256": c14n_hash(anchor_node),
            }
        )
    groups: list[dict[str, object]] = []
    group_counter: Counter[str] = Counter()
    for node in grouping_nodes(root):
        nearest = nearest_real_id(node)
        group_counter[nearest] += 1
        groups.append(
            {
                "source_anchor": f"o003-gvsu-ch20-{nearest}-group-{group_counter[nearest]:02d}",
                "authority_source_file": f"source/{source_file}",
                "authority_line": int(node.sourceline or 0),
                "xpath": xpath(node),
                "nearest_real_xml_id": nearest,
                "subtree_sha256": c14n_hash(node),
                "child_prompt_count": len(node.xpath(".//task[not(.//task)]")),
            }
        )
    return prompts, groups


def collect(root: etree._Element, expression: str, attribute: str | None = None) -> list[str]:
    nodes = root.xpath(expression)
    if attribute is None:
        return ["".join(node.itertext()) for node in nodes]
    return [str(node.get(attribute)) for node in nodes if node.get(attribute)]


def latex_controls(root: etree._Element) -> Counter[str]:
    text = "\n".join(collect(root, ".//*[self::m or self::me or self::men or self::md or self::mrow]"))
    return Counter(re.findall(r"\\[A-Za-z]+|\\.", text))


def english_residue() -> list[dict[str, object]]:
    allowed_phrases = (
        "A Topological Approach to Digital Topology",
        "American Mathematical Monthly",
        "Applications of connected ordered topological spaces in topology",
        "Conference of math. departments of Povolsia",
        "Discrete Geometry for Computer Imagery",
    )
    pattern = re.compile(
        r"\b(the|and|prove|show|find|explain|let|suppose|assume|then|with|from|that|this|we|you|are|is|into|onto)\b",
        re.IGNORECASE,
    )
    hits: list[dict[str, object]] = []
    for filename in FILES:
        root = parse(SOURCE / filename).getroot()
        for text_node in root.xpath(
            "//text()[not(ancestor::m) and not(ancestor::me) and not(ancestor::men) "
            "and not(ancestor::md) and not(ancestor::mrow) and not(ancestor::pre) "
            "and not(ancestor::code) and not(ancestor::url) and not(ancestor::pubtitle)]"
        ):
            text = " ".join(str(text_node).split())
            for phrase in allowed_phrases:
                text = text.replace(phrase, "")
            match = pattern.search(text)
            if match:
                parent = text_node.getparent()
                hits.append(
                    {
                        "file": f"source/{filename}",
                        "line": int(parent.sourceline or 0),
                        "token": match.group(0),
                        "excerpt": text[:240],
                    }
                )
    return hits


def ordered_identity(root: Path) -> dict[str, object]:
    records = [identity(root / filename, root) for filename in FILES]
    joined = b"".join((root / filename).read_bytes() for filename in FILES)
    return {
        "ordered_hash_contract": "sha256(concatenation of exact file bytes in ordered_files order; no separators)",
        "ordered_sha256": sha256(joined),
        "ordered_files": records,
    }


def build() -> dict[Path, bytes]:
    if not SCHEMA.exists() or len(SCHEMA.read_bytes()) != SCHEMA_BYTES or sha256(SCHEMA.read_bytes()) != SCHEMA_SHA256:
        raise SystemExit("pinned PreTeXt schema identity changed or is unavailable")
    if not CORRECTIONS.exists():
        raise SystemExit("task-local correction ledger is unavailable")

    source_roots: dict[str, etree._Element] = {}
    authority_roots: dict[str, etree._Element] = {}
    file_checks: list[dict[str, object]] = []
    for filename in FILES:
        source_root = parse(SOURCE / filename).getroot()
        authority_root = parse(AUTHORITY / filename).getroot()
        source_roots[filename] = source_root
        authority_roots[filename] = authority_root
        source_ids = collect(source_root, ".//*[@xml:id]", XML_ID)
        authority_ids = collect(authority_root, ".//*[@xml:id]", XML_ID)
        source_refs = collect(source_root, ".//xref", "ref")
        authority_refs = collect(authority_root, ".//xref", "ref")
        source_images = collect(source_root, ".//image", "source")
        authority_images = collect(authority_root, ".//image", "source")
        file_checks.append(
            {
                "source_file": f"source/{filename}",
                "source": identity(SOURCE / filename),
                "authority": identity(AUTHORITY / filename, AUTHORITY),
                "xml_id_sequence_match": source_ids == authority_ids,
                "xref_target_set_match": set(source_refs) == set(authority_refs),
                "image_source_sequence_match": source_images == authority_images,
                "counts": {
                    "elements": sum(1 for n in source_root.iter() if isinstance(n.tag, str)),
                    "xml_ids": len(source_ids),
                    "xrefs": len(source_refs),
                    "math_nodes": len(source_root.xpath(".//*[self::m or self::me or self::men or self::md or self::mrow]")),
                    "images": len(source_images),
                    "descriptions": len(source_root.xpath(".//image/description")),
                    "tasks": len(source_root.xpath(".//task")),
                    "exercises": len(source_root.xpath(".//exercise")),
                    "activities_and_explorations": len(source_root.xpath(".//activity | .//exploration")),
                },
            }
        )

    if not all(
        row[check]
        for row in file_checks
        for check in ("xml_id_sequence_match", "xref_target_set_match", "image_source_sequence_match")
    ):
        raise SystemExit("Chapter 20 protected ID/xref/image topology diverged from authority")

    source_controls = Counter()
    authority_controls = Counter()
    for filename in FILES:
        source_controls.update(latex_controls(source_roots[filename]))
        authority_controls.update(latex_controls(authority_roots[filename]))
    control_added = dict(sorted((source_controls - authority_controls).items()))
    control_removed = dict(sorted((authority_controls - source_controls).items()))
    if control_added != {"\\Z": 1} or control_removed != {"\\frac": 2}:
        raise SystemExit(f"unexpected protected LaTeX control delta: added={control_added}, removed={control_removed}")

    residue = english_residue()
    if residue:
        raise SystemExit(f"active English residue detected: {residue}")

    wrapper_tree = parse(WRAPPER)
    wrapper_tree.xinclude()
    validator = etree.RelaxNG(parse(SCHEMA))
    schema_valid = validator.validate(wrapper_tree)
    diagnostics = [str(entry) for entry in validator.error_log]
    if not schema_valid or diagnostics:
        raise SystemExit(f"Chapter 20 schema validation failed: {diagnostics}")

    expanded_root = wrapper_tree.getroot()
    expanded_ids = collect(expanded_root, ".//*[@xml:id]", XML_ID)
    duplicates = sorted(key for key, value in Counter(expanded_ids).items() if value > 1)
    expanded_refs = collect(expanded_root, ".//xref", "ref")
    unresolved = sorted(set(expanded_refs) - set(expanded_ids))
    # Cross-chapter references are lawful and intentionally unresolved in the isolated wrapper.
    expected_external = sorted(
        {
            "chap_metric_subspaces",
            "chap_top_spaces",
            "act_connected_compenent",
            "chap_Connected_topology",
            "ex_inverse_composite_sets",
        }
    )
    if duplicates or sorted(unresolved) != expected_external:
        raise SystemExit(f"unexpected isolated ID/xref state: duplicates={duplicates}, unresolved={unresolved}")

    correction_rows = list(csv.DictReader(CORRECTIONS.open("r", encoding="utf-8-sig", newline="")))
    required_corrections = [f"O003-C{i}" for i in range(300, 326)]
    correction_map = {row["id"]: row for row in correction_rows if row.get("id") in required_corrections}
    if sorted(correction_map) != sorted(required_corrections):
        raise SystemExit("Chapter 20 correction ledger is not the exact contiguous O003-C300--C325 block")
    if any(row.get("status") != "verified" for row in correction_map.values()):
        raise SystemExit("one or more Chapter 20 corrections are not verified")

    authority_prompts: list[dict[str, object]] = []
    translated_prompts: list[dict[str, object]] = []
    groups: list[dict[str, object]] = []
    per_file_counts: defaultdict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for filename in FILES:
        authority_file_prompts, authority_file_groups = anchor_records(AUTHORITY / filename, filename)
        translated_file_prompts, translated_file_groups = anchor_records(SOURCE / filename, filename)
        if len(authority_file_prompts) != len(translated_file_prompts):
            raise SystemExit(f"prompt count changed in {filename}")
        if [row["prompt_carrier"] for row in authority_file_prompts] != [row["prompt_carrier"] for row in translated_file_prompts]:
            raise SystemExit(f"prompt carrier sequence changed in {filename}")
        if len(authority_file_groups) != len(translated_file_groups):
            raise SystemExit(f"grouping-node count changed in {filename}")
        authority_prompts.extend(authority_file_prompts)
        translated_prompts.extend(translated_file_prompts)
        groups.extend(authority_file_groups)

    if len(authority_prompts) != 56 or len(groups) != 1:
        raise SystemExit(f"unexpected Chapter 20 prompt census: prompts={len(authority_prompts)}, groups={len(groups)}")

    entries: list[dict[str, object]] = []
    csv_rows: list[dict[str, object]] = []
    nonexercise_sequence = 0
    exercise_sequence = 0
    for sequence, (authority_prompt, translated_prompt) in enumerate(zip(authority_prompts, translated_prompts), 1):
        if authority_prompt["source_anchor"] != translated_prompt["source_anchor"]:
            raise SystemExit(f"source anchor changed at prompt {sequence}")
        partition = "exercise" if authority_prompt["authority_source_file"] == "source/sec_prod_top_exer.ptx" else "nonexercise"
        if partition == "exercise":
            exercise_sequence += 1
            batch_index = (exercise_sequence - 1) // 10
            batch = chr(ord("a") + batch_index)
            batch_sequence = ((exercise_sequence - 1) % 10) + 1
            entry_id = f"o003-c90-ch20-exer-{batch}-{batch_sequence:02d}"
            partition_sequence = exercise_sequence
        else:
            nonexercise_sequence += 1
            entry_id = f"o003-c90-ch20-guide-{nonexercise_sequence:02d}"
            batch = ""
            batch_sequence = 0
            partition_sequence = nonexercise_sequence
        locator = {
            "authority_commit": UPSTREAM_COMMIT,
            "authority_source_file": authority_prompt["authority_source_file"],
            "authority_line": authority_prompt["authority_line"],
            "element_tag": {"atomic_task": "task", "direct_statement": "statement", "direct_body": "activity"}[
                str(authority_prompt["prompt_carrier"])
            ],
            "nearest_ancestor_or_self_xml_id": authority_prompt["nearest_real_xml_id"],
            "xpath": authority_prompt["xpath"],
            "subtree_hash_contract": "sha256-c14n-1.0-with-comments",
            "subtree_sha256": authority_prompt["subtree_sha256"],
        }
        entry = {
            "sequence": sequence,
            "id": entry_id,
            "entry_type": "source_prompt_support",
            "source_anchor": authority_prompt["source_anchor"],
            "source_anchor_kind": "synthetic_locale_neutral_alias",
            "authority_source_file": authority_prompt["authority_source_file"],
            "authority_line": authority_prompt["authority_line"],
            "prompt_carrier": authority_prompt["prompt_carrier"],
            "authority_locator": locator,
            "parent_group_anchor": "",
            "support_status": "covered",
            "partition": partition,
            "partition_sequence": partition_sequence,
            "exercise_batch": batch,
            "exercise_batch_sequence": batch_sequence,
            "translated_source_subtree_sha256": translated_prompt["subtree_sha256"],
        }
        entries.append(entry)
        csv_rows.append(
            {
                "sequence": sequence,
                "entry_id": entry_id,
                "source_anchor": authority_prompt["source_anchor"],
                "source_anchor_kind": "synthetic_locale_neutral_alias",
                "authority_source_file": authority_prompt["authority_source_file"],
                "authority_line": authority_prompt["authority_line"],
                "prompt_carrier": authority_prompt["prompt_carrier"],
                "authority_locator": json.dumps(locator, ensure_ascii=False, separators=(",", ":")),
                "parent_group_anchor": "",
                "support_status": "covered",
            }
        )
        per_file_counts[str(authority_prompt["authority_source_file"])][partition] += 1

    fields = (
        "sequence",
        "entry_id",
        "source_anchor",
        "source_anchor_kind",
        "authority_source_file",
        "authority_line",
        "prompt_carrier",
        "authority_locator",
        "parent_group_anchor",
        "support_status",
    )
    prompt_csv_payload = csv_bytes(csv_rows, fields)

    grouping_payload = {
        "schema_version": 1,
        "status": "complete",
        "lane_id": "O003/C90",
        "locale": "id-ID",
        "unit": "chapter_20_product_topology",
        "node_count": len(groups),
        "nodes": groups,
    }
    grouping_bytes = json_bytes(grouping_payload)

    prompt_payload = {
        "schema_version": 2,
        "status": "prompt_inventory_complete_companion_covered",
        "partial": False,
        "lane_id": "O003/C90",
        "locale": "id-ID",
        "unit": {"id": "chapter_20_product_topology", "sequence": 20, "source_chapter_xml_id": "chap_Product_topology"},
        "authority": {
            "root": AUTHORITY.as_posix(),
            "lineage_upstream_commit": UPSTREAM_COMMIT,
            **ordered_identity(AUTHORITY),
        },
        "carrier_contract": {
            "atomic_task": "task element with no descendant task element",
            "grouping_task": "task element with descendant task elements; backend-only, not a prompt occurrence",
            "direct_statement": "direct statement child of a taskless exercise, activity, or exploration",
            "direct_body": "taskless activity or exploration with a direct p child and no direct statement",
        },
        "source_anchor_contract": {
            "kind": "synthetic_locale_neutral_alias",
            "format": "o003-gvsu-ch20-{nearest-real-xml-id}-{task|statement|body|group}-NN",
            "sequence_scope": "nearest real xml:id plus carrier label in authority order",
            "translated_titles_used": False,
        },
        "entry_id_contract": {
            "nonexercise": {
                "format": "o003-c90-ch20-guide-NN",
                "canonical_entry_count": nonexercise_sequence,
                "first": "o003-c90-ch20-guide-01",
                "last": f"o003-c90-ch20-guide-{nonexercise_sequence:02d}",
            },
            "exercise": {
                "format": "o003-c90-ch20-exer-{batch}-{NN}",
                "canonical_entry_count": exercise_sequence,
                "batch_derivation": "authority-order exercise entries partitioned into batches of at most 10",
                "batches": [{"letter": "a", "count": 10}, {"letter": "b", "count": 10}, {"letter": "c", "count": 5}],
                "first": "o003-c90-ch20-exer-a-01",
                "last": "o003-c90-ch20-exer-c-05",
            },
        },
        "census": {
            "physical_prompt_occurrence_total": len(entries),
            "canonical_source_support_entry_total": len(entries),
            "nonexercise_prompt_total": nonexercise_sequence,
            "exercise_prompt_total": exercise_sequence,
            "atomic_prompt_total": sum(row["prompt_carrier"] == "atomic_task" for row in entries),
            "direct_statement_prompt_total": sum(row["prompt_carrier"] == "direct_statement" for row in entries),
            "direct_body_prompt_total": sum(row["prompt_carrier"] == "direct_body" for row in entries),
            "grouping_node_total": len(groups),
            "pending_support_total": 0,
            "covered_support_total": len(entries),
            "by_source_file": [
                {
                    "authority_source_file": f"source/{filename}",
                    "canonical_entry_total": per_file_counts[f"source/{filename}"]["nonexercise"]
                    + per_file_counts[f"source/{filename}"]["exercise"],
                    "nonexercise_canonical_entry_total": per_file_counts[f"source/{filename}"]["nonexercise"],
                    "exercise_canonical_entry_total": per_file_counts[f"source/{filename}"]["exercise"],
                }
                for filename in FILES
            ],
        },
        "prompt_map": {
            "path": "backend/chapter_20_source_prompt_map.csv",
            "bytes": len(prompt_csv_payload),
            "sha256": sha256(prompt_csv_payload),
            "fields": list(fields),
            "row_count": len(csv_rows),
        },
        "grouping_backend": {
            "path": "backend/chapter_20_grouping_nodes.json",
            "bytes": len(grouping_bytes),
            "sha256": sha256(grouping_bytes),
            "node_count": len(groups),
        },
        "entries": entries,
        "translated_source": {
            "root": SOURCE.as_posix(),
            "lineage_upstream_commit": UPSTREAM_COMMIT,
            **ordered_identity(SOURCE),
            "xml_id_sequence_match": True,
            "xref_target_set_match": True,
            "image_source_sequence_match": True,
            "physical_prompt_occurrence_total": len(entries),
            "canonical_source_support_entry_total": len(entries),
            "grouping_node_total": len(groups),
        },
    }

    source_qa_payload = {
        "schema_version": 1,
        "status": "pass",
        "partial": False,
        "lane_id": "O003/C90",
        "locale": "id-ID",
        "unit": "chapter_20_product_topology",
        "authority_commit": UPSTREAM_COMMIT,
        "authority": ordered_identity(AUTHORITY),
        "translated_source": ordered_identity(SOURCE),
        "source_file_count": len(FILES),
        "file_checks": file_checks,
        "schema": {"path": "pretext-user-cache/schema/pretext.rng", "bytes": SCHEMA_BYTES, "sha256": SCHEMA_SHA256},
        "schema_validation": {
            "status": "pass",
            "diagnostics": diagnostics,
            "expanded_element_count": sum(1 for n in expanded_root.iter() if isinstance(n.tag, str)),
        },
        "protected_content": {
            "xml_id_sequence_match_all_files": True,
            "xref_target_set_match_all_files": True,
            "image_source_sequence_match_all_files": True,
            "latex_control_multiset_delta": {
                "added": control_added,
                "removed": control_removed,
                "covered_by_verified_corrections": ["O003-C302", "O003-C304", "O003-C319"],
            },
            "isolated_wrapper_duplicate_xml_ids": duplicates,
            "isolated_wrapper_external_xrefs": unresolved,
        },
        "active_english_residue": {"status": "pass", "hit_count": len(residue), "hits": residue},
        "corrections": {
            "status": "verified",
            "first": "O003-C300",
            "last": "O003-C325",
            "count": len(correction_map),
            "ids": required_corrections,
        },
        "prompt_census": {
            "canonical_support_entries": len(entries),
            "nonexercise": nonexercise_sequence,
            "exercise": exercise_sequence,
            "grouping_nodes": len(groups),
        },
    }

    return {
        SOURCE_QA: json_bytes(source_qa_payload),
        PROMPT_CSV: prompt_csv_payload,
        GROUPING_JSON: grouping_bytes,
        PROMPT_JSON: json_bytes(prompt_payload),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = build()
    if args.check:
        stale = [str(path.relative_to(ROOT)) for path, payload in outputs.items() if not path.exists() or path.read_bytes() != payload]
        if stale:
            raise SystemExit("stale Chapter 20 source state: " + ", ".join(stale))
        print("PASS: Chapter 20 source identity and 56-entry prompt inventory are deterministic")
        return
    for path, payload in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        print(f"WROTE {path.relative_to(ROOT)} {len(payload)} bytes sha256={sha256(payload)}")


if __name__ == "__main__":
    main()
