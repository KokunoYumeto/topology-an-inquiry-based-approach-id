#!/usr/bin/env python3
"""Fail-closed coverage and structure audit for the Chapter 5 companion."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

from lxml import etree


XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"
SOURCE_FILES = (
    "chap_glb.ptx",
    "sec_glb_intro.ptx",
    "sec_dist_point_set.ptx",
    "sec_glb_summ.ptx",
    "sec_glb_exer.ptx",
)
FRAGMENTS = (
    "chapter_05_intro_guides.ptx",
    "chapter_05_point_set_guides.ptx",
    "chapter_05_exercise_guides_a.ptx",
    "chapter_05_exercise_guides_b.ptx",
    "chapter_05_mastery.ptx",
)
EXPECTED_SOURCE_PROMPTS = 48
EXPECTED_MASTERY = 6


def local_name(node: etree._Element) -> str:
    return etree.QName(node).localname


def identity(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def normalized_text(node: etree._Element) -> str:
    return " ".join("".join(node.itertext()).split())


def expected_entry_ids() -> list[str]:
    return (
        [f"o003-c90-ch05-intro-task-{number:02d}" for number in range(1, 6)]
        + [f"o003-c90-ch05-pointset-task-{number:02d}" for number in range(1, 7)]
        + [f"o003-c90-ch05-exercise-task-{number:02d}" for number in range(1, 38)]
        + [f"o003-c90-ch05-mastery-{number:02d}" for number in range(1, 7)]
    )


def main() -> int:
    repo = Path(__file__).resolve().parent.parent
    companion = repo / "companion/chapter_05_greatest_lower_bound_self_study.ptx"
    report_path = repo / "qa/CHAPTER05_COMPANION_QA.json"
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    failures: list[str] = []

    tree = etree.parse(str(companion), parser)
    try:
        tree.xinclude()
    except etree.XIncludeError as exc:
        failures.append(f"XInclude closure failed: {exc}")
    root = tree.getroot()
    if root.get(XML_ID) != "o003-c90-ch05-companion":
        failures.append("unexpected companion root ID")
    if root.get(XML_LANG) != "id-ID":
        failures.append("companion root is not explicitly id-ID")

    elements = [node for node in root.iter() if isinstance(node.tag, str)]
    ids = [node.get(XML_ID) for node in elements if node.get(XML_ID)]
    duplicates = sorted(value for value, count in Counter(ids).items() if count > 1)
    if duplicates:
        failures.append(f"duplicate companion IDs: {duplicates}")
    by_id = {node.get(XML_ID): node for node in elements if node.get(XML_ID)}

    exercises = [node for node in elements if local_name(node) == "exercise"]
    actual_entry_ids = [node.get(XML_ID) for node in exercises]
    expected_ids = expected_entry_ids()
    if actual_entry_ids != expected_ids:
        first = next(
            (
                index
                for index, pair in enumerate(zip(actual_entry_ids, expected_ids))
                if pair[0] != pair[1]
            ),
            min(len(actual_entry_ids), len(expected_ids)),
        )
        failures.append(
            f"companion entry sequence differs at {first}: "
            f"found {len(actual_entry_ids)}, expected {len(expected_ids)}"
        )

    entries: list[dict[str, object]] = []
    reveal_counts: Counter[str] = Counter()
    minima = {"statement": 35, "hint": 20, "answer": 18, "solution": 120}
    for entry_id in expected_ids:
        exercise = by_id.get(entry_id)
        if exercise is None or local_name(exercise) != "exercise":
            failures.append(f"missing exercise entry: {entry_id}")
            continue
        lengths: dict[str, int] = {}
        for kind, minimum in minima.items():
            children = exercise.findall(kind)
            if len(children) != 1:
                failures.append(f"{entry_id} has {len(children)} direct {kind} children")
                continue
            child = children[0]
            length = len(normalized_text(child))
            lengths[kind] = length
            if length < minimum:
                failures.append(f"{entry_id} {kind} is too short: {length} < {minimum}")
            if kind != "statement":
                reveal_counts[kind] += 1
                expected_reveal_id = f"{entry_id}-{kind}"
                if child.get(XML_ID) != expected_reveal_id:
                    failures.append(f"{entry_id} has noncanonical {kind} ID")
        kind = "mastery_check" if "-mastery-" in entry_id else "source_prompt_guide"
        entries.append({"id": entry_id, "kind": kind, "text_lengths": lengths})

    source_prompt_counts: dict[str, int] = {}
    source_ids: set[str] = set()
    for name in SOURCE_FILES:
        source_root = etree.parse(str(repo / "source" / name), parser).getroot()
        for node in source_root.iter():
            if isinstance(node.tag, str) and node.get(XML_ID):
                source_ids.add(node.get(XML_ID))
        statement_tasks = [
            node
            for node in source_root.iter("task")
            if node.find("statement") is not None
        ]
        standalone_exercises = [
            node
            for node in source_root.iter("exercise")
            if node.find("statement") is not None and not list(node.iter("task"))
        ]
        source_prompt_counts[name] = len(statement_tasks) + len(standalone_exercises)
    source_prompt_total = sum(source_prompt_counts.values())
    if source_prompt_total != EXPECTED_SOURCE_PROMPTS:
        failures.append(
            f"source prompt count changed: {source_prompt_total} != {EXPECTED_SOURCE_PROMPTS}"
        )

    refs = [
        node.get("ref")
        for node in elements
        if local_name(node) == "xref" and node.get("ref")
    ]
    missing_refs = sorted(set(refs) - source_ids - set(ids))
    if missing_refs:
        failures.append(f"unresolved companion xrefs: {missing_refs}")

    prose_parts: list[str] = []
    protected = {"m", "me", "men", "md", "mrow", "c", "code", "sage"}
    for node in elements:
        if local_name(node) in protected:
            continue
        if node.text:
            prose_parts.append(node.text)
        if node.tail:
            prose_parts.append(node.tail)
    prose = " ".join(prose_parts)
    english_markers = sorted(
        set(
            re.findall(
                r"\b(?:Let|Show|Prove|Determine|Describe|Suppose|Recall|Hint|Answer|Solution|True|False)\b",
                prose,
                flags=re.IGNORECASE,
            )
        )
    )
    if english_markers:
        failures.append(f"active English instruction markers: {english_markers}")
    placeholders = sorted(
        set(re.findall(r"\b(?:TODO|TBD|FIXME|LOREM)\b|\?\?\?", prose, flags=re.IGNORECASE))
    )
    if placeholders:
        failures.append(f"placeholder residue: {placeholders}")

    normalized_raw = " ".join(companion.read_text(encoding="utf-8").split())
    for phrase in (
        "Creative Commons Attribution 4.0",
        "bukan teks Steven Schlicker atau GVSU",
        "tidak menyalin ungkapan dari karya Anton Petrunin",
        "CC BY-NC-SA 3.0",
    ):
        if phrase not in normalized_raw:
            failures.append(f"missing component-boundary phrase: {phrase}")
    if re.search(
        r"(?:C:\\Users\\|github_pat_|ghp_|ZENODO|api[_-]?token|access[_-]?token)",
        normalized_raw,
        flags=re.IGNORECASE,
    ):
        failures.append("local path or credential-like residue in companion")

    report = {
        "schema_version": 1,
        "status": "pass" if not failures else "fail",
        "companion": identity(companion),
        "fragments": [identity(repo / "companion" / name) for name in FRAGMENTS],
        "entry_counts": {
            "source_prompt_guide": EXPECTED_SOURCE_PROMPTS,
            "mastery_check": EXPECTED_MASTERY,
        },
        "reveal_counts": dict(reveal_counts),
        "source_prompt_counts": source_prompt_counts,
        "source_prompt_total": source_prompt_total,
        "xml_ids": len(ids),
        "xrefs": len(refs),
        "missing_xrefs": missing_refs,
        "entries": entries,
        "failures": failures,
    }
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "report": identity(report_path),
                "status": report["status"],
                "entry_counts": report["entry_counts"],
                "reveal_counts": report["reveal_counts"],
                "source_prompt_counts": source_prompt_counts,
                "xml_ids": len(ids),
                "failures": failures,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
