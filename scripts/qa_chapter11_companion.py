#!/usr/bin/env python3
"""Fail-closed coverage, rights, and source-link audit for Chapter 11."""

from __future__ import annotations

from collections import Counter
import csv
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import sys

from lxml import etree


XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"
SOURCE_FILES = (
    "chap_metric_subspaces.ptx",
    "sec_sub_metric_intro.ptx",
    "sec_open_closed_sub.ptx",
    "sec_prod_metric.ptx",
    "sec_sub_metric_summ.ptx",
    "sec_sub_metric_exer.ptx",
)
FILE_GROUPS = {
    "sec_sub_metric_intro.ptx": (("sec_sub_metric_intro", 6),),
    "sec_open_closed_sub.ptx": (("sec_open_closed_sub", 3),),
    "sec_prod_metric.ptx": (("sec_prod_metric", 7),),
    "sec_sub_metric_exer.ptx": (("sec_sub_metric_exer", 19),),
}
FRAGMENTS = (
    "chapter_11_source_guides_a.ptx",
    "chapter_11_source_guides_b.ptx",
    "chapter_11_exercise_guides_a.ptx",
    "chapter_11_exercise_guides_b.ptx",
    "chapter_11_mastery.ptx",
)
EXPECTED_AUTHORITY_ORDERED_SHA256 = (
    "b36b91c1d1826cef631953a9c8fd05a00aa09ae051b5782ff21e0185b7119d90"
)
EXPECTED_AUTHORITY_RAW_SHA256 = (
    "a285e2001e841097c5e1a9f6b53be1304b7982ae8e0e81844d966e4051c4c12e"
)
EXPECTED_TERM_IDS = {f"O003-T{number:03d}" for number in range(133, 142)}
EXPECTED_CORRECTION_IDS = {
    *(f"O003-C{number:03d}" for number in range(113, 122)),
    *(f"O003-C{number:03d}" for number in range(123, 129)),
}
EXPECTED_SOURCE_PROMPTS = 35
EXPECTED_ACTIVITY_PROMPTS = 16
EXPECTED_EXERCISE_PROMPTS = 19
EXPECTED_MASTERY = 8
EXPECTED_GROUPING_TASKS = 1
REMOTE_TAGS = {"url", "video", "interactive", "sage", "webwork", "iframe"}
EXPECTED_MATH_CHANGES = [
    {
        "authority": "<m>a \\in A</m>",
        "key": "sec_open_closed_sub.ptx:14",
        "translated": "<m>a \\in O_A</m>",
    },
    {
        "authority": "<m>A</m>",
        "key": "sec_open_closed_sub.ptx:54",
        "translated": "<m>O_A</m>",
    },
    {
        "authority": "<m>(X, d_1)</m>",
        "key": "sec_prod_metric.ptx:0",
        "translated": "<m>(X_1, d_1)</m>",
    },
    {
        "authority": "<m>(X, d_1)</m>",
        "key": "sec_prod_metric.ptx:20",
        "translated": "<m>(X_1, d_1)</m>",
    },
    {
        "authority": "<mrow> \\amp \\leq d(x,y)^2 + d(y,z)^2</mrow>",
        "key": "sec_prod_metric.ptx:43",
        "translated": "<mrow> \\amp \\leq d(x,y)^2 + 2d(x,y)d(y,z) + d(y,z)^2</mrow>",
    },
    {
        "authority": "<mrow>d(x,z) \\leq \\sqrt{d(x,y)^2 + d(y,z)^2} \\amp \\leq \\sqrt{d(x,y)^2 + 2 d(x,y)d(y,z) + d(y,z)^2} </mrow>",
        "key": "sec_prod_metric.ptx:44",
        "translated": "<mrow>d(x,z) \\amp \\leq \\sqrt{d(x,y)^2 + 2 d(x,y)d(y,z) + d(y,z)^2} </mrow>",
    },
    {
        "authority": "<m>\\R^2</m>",
        "key": "sec_prod_metric.ptx:51",
        "translated": "<m>\\R</m>",
    },
    {
        "authority": "<m>O_A = X \\cap O</m>",
        "key": "sec_sub_metric_summ.ptx:10",
        "translated": "<m>O_A = A \\cap O</m>",
    },
    {
        "authority": "<m>C_A = A \\cap O_A</m>",
        "key": "sec_sub_metric_summ.ptx:16",
        "translated": "<m>C_A = A \\setminus O_A</m>",
    },
    {
        "authority": "<m>(O, d|_O)</m>",
        "key": "sec_sub_metric_exer.ptx:13",
        "translated": "<m>(O, d|_{O \\times O})</m>",
    },
    {
        "authority": "<m>d: X \\times Y \\to \\R</m>",
        "key": "sec_sub_metric_exer.ptx:37",
        "translated": "<m>d: (X \\times Y) \\times (X \\times Y) \\to \\R</m>",
    },
    {
        "authority": "<m>d: \\prod_{i=1}^n X_i \\to \\R</m>",
        "key": "sec_sub_metric_exer.ptx:44",
        "translated": "<m>X = \\prod_{i=1}^n X_i,\\ d: X \\times X \\to \\R</m>",
    },
    {
        "authority": "<m>H</m>",
        "key": "sec_sub_metric_exer.ptx:92",
        "translated": "<m>E^m</m>",
    },
    {
        "authority": "<m>d: X \\times Y \\to \\R</m>",
        "key": "sec_sub_metric_exer.ptx:128",
        "translated": "<m>d: (X \\times Y) \\times (X \\times Y) \\to \\R</m>",
    },
    {
        "authority": "<m>d: X \\times Y \\to \\R</m>",
        "key": "sec_sub_metric_exer.ptx:133",
        "translated": "<m>d: (X \\times Y) \\times (X \\times Y) \\to \\R</m>",
    },
]


@dataclass(frozen=True)
class Prompt:
    anchor: etree._Element
    statement: etree._Element
    kind: str


def local_name(node: etree._Element) -> str:
    return etree.QName(node).localname


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path: Path, display_path: str) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": display_path, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def normalized_text(node: etree._Element) -> str:
    return " ".join("".join(node.itertext()).split())


def element_sha256(node: etree._Element) -> str:
    return hashlib.sha256(etree.tostring(node, encoding="utf-8", with_tail=False)).hexdigest()


def guide_id(sequence: int) -> str:
    return f"o003-c90-ch11-guide-{sequence:02d}"


def expected_source_entry_ids() -> list[str]:
    return [guide_id(sequence) for sequence in range(1, EXPECTED_SOURCE_PROMPTS + 1)]


def expected_entry_ids() -> list[str]:
    return expected_source_entry_ids() + [
        f"o003-c90-ch11-mastery-{ordinal:02d}" for ordinal in range(1, EXPECTED_MASTERY + 1)
    ]


def prompt_nodes(tree: etree._ElementTree, name: str) -> list[Prompt]:
    """Return atomic prompts, excluding statement-less grouping tasks."""
    root = tree.getroot()
    if name != "sec_sub_metric_exer.ptx":
        return [
            Prompt(task, statement, "statement_bearing_task")
            for task in root.iter("task")
            for statement in task.findall("statement")
        ]
    prompts: list[Prompt] = []
    for exercise in root.findall("exercise"):
        nested = [
            Prompt(task, statement, "statement_bearing_task")
            for task in exercise.iter("task")
            for statement in task.findall("statement")
        ]
        if nested:
            prompts.extend(nested)
        else:
            statement = exercise.find("statement")
            if statement is not None:
                prompts.append(Prompt(exercise, statement, "standalone_exercise"))
    return prompts


def grouping_task_count(tree: etree._ElementTree) -> int:
    return sum(1 for task in tree.getroot().iter("task") if not task.findall("statement"))


def nearest_context_id(node: etree._Element) -> str | None:
    for candidate in (node, *node.iterancestors()):
        if candidate.get(XML_ID):
            return candidate.get(XML_ID)
    return None


def source_prompt_mappings(
    repo: Path,
    authority_root: Path,
    parser: etree.XMLParser,
    failures: list[str],
) -> tuple[list[dict[str, object]], dict[str, int]]:
    mappings: list[dict[str, object]] = []
    counts = {name: 0 for name in SOURCE_FILES}
    grouping_counts = {"authority": 0, "translated": 0}
    for name, groups in FILE_GROUPS.items():
        authority_tree = etree.parse(str(authority_root / name), parser)
        translated_tree = etree.parse(str(repo / "source" / name), parser)
        authority_prompts = prompt_nodes(authority_tree, name)
        translated_prompts = prompt_nodes(translated_tree, name)
        grouping_counts["authority"] += grouping_task_count(authority_tree)
        grouping_counts["translated"] += grouping_task_count(translated_tree)
        expected_count = sum(count for _, count in groups)
        counts[name] = len(translated_prompts)
        if len(authority_prompts) != expected_count:
            failures.append(f"authority prompt count changed in {name}: {len(authority_prompts)} != {expected_count}")
        if len(translated_prompts) != expected_count:
            failures.append(f"translated prompt count changed in {name}: {len(translated_prompts)} != {expected_count}")
        labels = [(group, ordinal) for group, count in groups for ordinal in range(1, count + 1)]
        for sequence, (authority, translated) in enumerate(zip(authority_prompts, translated_prompts), start=1):
            if sequence > len(labels):
                failures.append(f"unexpected prompt beyond contract in {name}")
                continue
            group, ordinal = labels[sequence - 1]
            if authority.kind != translated.kind:
                failures.append(f"prompt classification changed in {name}:{sequence}")
            authority_context = nearest_context_id(authority.anchor)
            translated_context = nearest_context_id(translated.anchor)
            if authority_context != translated_context:
                failures.append(f"prompt context ID changed in {name}:{sequence}")
            mappings.append({
                "companion_entry_id": guide_id(len(mappings) + 1),
                "source_anchor_id": f"o003-gvsu-ch11-{Path(name).stem}-prompt-{sequence:02d}",
                "group": group,
                "ordinal_within_group": ordinal,
                "prompt_kind": authority.kind,
                "source_context_id": authority_context,
                "authority_file": f"source/{name}",
                "authority_line": authority.statement.sourceline,
                "authority_selector": authority_tree.getpath(authority.statement),
                "authority_statement_sha256": element_sha256(authority.statement),
                "translated_file": f"source/{name}",
                "translated_line": translated.statement.sourceline,
                "translated_selector": translated_tree.getpath(translated.statement),
                "translated_statement_sha256": element_sha256(translated.statement),
            })
    if grouping_counts != {"authority": EXPECTED_GROUPING_TASKS, "translated": EXPECTED_GROUPING_TASKS}:
        failures.append(f"statement-less grouping-task census changed: {grouping_counts}")
    return mappings, counts


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    repo = Path(__file__).resolve().parent.parent
    lane = repo.parent
    authority_root = lane / "authority/gvsu-pinned/topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9/source"
    companion = repo / "companion/chapter_11_metric_subspaces_self_study.ptx"
    report_path = repo / "qa/CHAPTER11_COMPANION_QA.json"
    source_qa_path = repo / "qa/CHAPTER11_SOURCE_QA.json"
    terminology_path = lane / "00_control/TERMINOLOGY.csv"
    corrections_path = lane / "00_control/SOURCE_CORRECTIONS.csv"
    rights_path = repo / "companion/RIGHTS.md"
    licenses_path = repo / "LICENSES.md"
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    failures: list[str] = []

    required = [companion, source_qa_path, terminology_path, corrections_path, rights_path, licenses_path]
    required += [repo / "companion" / name for name in FRAGMENTS]
    required += [repo / "source" / name for name in SOURCE_FILES]
    required += [authority_root / name for name in SOURCE_FILES]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"missing required Chapter 11 inputs: {missing}")

    source_qa = json.loads(source_qa_path.read_text(encoding="utf-8"))
    if source_qa.get("status") != "pass":
        failures.append("Chapter 11 source QA is not passing")
    source_qa_files = {item.get("file"): item for item in source_qa.get("files", [])}
    if set(source_qa_files) != set(SOURCE_FILES):
        failures.append("Chapter 11 source QA file closure changed")
    for name in SOURCE_FILES:
        item = source_qa_files.get(name, {})
        if item.get("authority", {}).get("sha256") != sha256(authority_root / name):
            failures.append(f"source QA authority identity is stale for {name}")
        if item.get("translated", {}).get("sha256") != sha256(repo / "source" / name):
            failures.append(f"source QA translated identity is stale for {name}")
    for key in (
        "approved_attribute_changes",
        "approved_element_block_moves",
        "approved_element_shell_moves",
        "approved_external_xref_targets",
    ):
        if source_qa.get(key) not in ([], None):
            failures.append(f"unexpected Chapter 11 source QA closure: {key}")
    insertion_keys = [row.get("key") for row in source_qa.get("approved_element_insertions", [])]
    if insertion_keys != ["sec_sub_metric_intro.ptx:57:exploration"]:
        failures.append(f"Chapter 11 schema-repair insertion closure changed: {insertion_keys}")
    if source_qa.get("approved_math_changes") != EXPECTED_MATH_CHANGES:
        failures.append("Chapter 11 protected-math repair closure changed")

    ordered_digest = hashlib.sha256()
    raw_digest = hashlib.sha256()
    for name in SOURCE_FILES:
        data = (authority_root / name).read_bytes()
        ordered_digest.update(name.encode("utf-8"))
        ordered_digest.update(b"\0")
        ordered_digest.update(data)
        raw_digest.update(data)
    if ordered_digest.hexdigest() != EXPECTED_AUTHORITY_ORDERED_SHA256:
        failures.append("frozen Chapter 11 authority name-delimited identity changed")
    if raw_digest.hexdigest() != EXPECTED_AUTHORITY_RAW_SHA256:
        failures.append("frozen Chapter 11 authority raw-concatenation identity changed")

    tree = etree.parse(str(companion), parser)
    try:
        tree.xinclude()
    except etree.XIncludeError as exc:
        failures.append(f"XInclude closure failed: {exc}")
    root = tree.getroot()
    if root.get(XML_ID) != "o003-c90-ch11-companion":
        failures.append("unexpected Chapter 11 companion root ID")
    if root.get(XML_LANG) != "id-ID":
        failures.append("Chapter 11 companion root is not explicitly id-ID")
    for name in FRAGMENTS:
        if etree.parse(str(repo / "companion" / name), parser).getroot().get(XML_LANG) != "id-ID":
            failures.append(f"companion fragment is not explicitly id-ID: {name}")

    elements = [node for node in root.iter() if isinstance(node.tag, str)]
    ids = [node.get(XML_ID) for node in elements if node.get(XML_ID)]
    duplicates = sorted(value for value, count in Counter(ids).items() if count > 1)
    if duplicates:
        failures.append(f"duplicate companion IDs: {duplicates}")
    by_id = {node.get(XML_ID): node for node in elements if node.get(XML_ID)}
    expected_ids = expected_entry_ids()
    actual_ids = [node.get(XML_ID) for node in elements if local_name(node) == "exercise"]
    if actual_ids != expected_ids:
        failures.append(f"companion entry sequence differs: found {len(actual_ids)}, expected {len(expected_ids)}")

    entries: list[dict[str, object]] = []
    reveal_counts: Counter[str] = Counter()
    surface_counts: Counter[str] = Counter()
    minima = {"statement": 25, "hint": 18, "answer": 12, "solution": 75}
    for sequence, expected_id in enumerate(expected_ids, start=1):
        exercise = by_id.get(expected_id)
        if exercise is None or local_name(exercise) != "exercise":
            failures.append(f"missing exercise entry: {expected_id}")
            continue
        titles = exercise.findall("title")
        title = normalized_text(titles[0]) if len(titles) == 1 else ""
        if len(titles) != 1 or len(title) < 5:
            failures.append(f"{expected_id} requires exactly one nonempty title")
        lengths: dict[str, int] = {}
        surfaces: dict[str, dict[str, object]] = {}
        reveals: dict[str, str] = {}
        for kind, minimum in minima.items():
            children = exercise.findall(kind)
            if len(children) != 1:
                failures.append(f"{expected_id} has {len(children)} direct {kind} children")
                continue
            child = children[0]
            text_length = len(normalized_text(child))
            lengths[kind] = text_length
            if text_length < minimum:
                failures.append(f"{expected_id} {kind} is too short: {text_length} < {minimum}")
            expected_surface_id = f"{expected_id}-{kind}"
            xml_id = child.get(XML_ID)
            if kind == "statement" and xml_id not in {None, expected_surface_id}:
                failures.append(f"{expected_id} has conflicting statement ID")
            if kind != "statement" and xml_id != expected_surface_id:
                failures.append(f"{expected_id} has noncanonical {kind} reveal ID")
            surfaces[kind] = {
                "id": expected_surface_id,
                "id_origin": "xml_id" if xml_id == expected_surface_id else "assigned_backend_alias",
                "xml_id": xml_id,
            }
            surface_counts[kind] += 1
            if kind != "statement":
                reveals[kind] = expected_surface_id
                reveal_counts[kind] += 1
        entries.append({
            "id": expected_id,
            "kind": "mastery_check" if "-mastery-" in expected_id else "source_prompt_guide",
            "sequence": sequence,
            "title": title or None,
            "text_lengths": lengths,
            "reveals": reveals,
            "surfaces": surfaces,
        })

    mappings, prompt_counts = source_prompt_mappings(repo, authority_root, parser, failures)
    source_prompt_total = sum(prompt_counts.values())
    if source_prompt_total != EXPECTED_SOURCE_PROMPTS:
        failures.append(f"source prompt count changed: {source_prompt_total} != {EXPECTED_SOURCE_PROMPTS}")
    if [row["companion_entry_id"] for row in mappings] != expected_source_entry_ids():
        failures.append("source prompt mapping order does not match companion entry order")

    source_ids: set[str] = set()
    for name in SOURCE_FILES:
        source_root = etree.parse(str(repo / "source" / name), parser).getroot()
        source_ids.update(node.get(XML_ID) for node in source_root.iter() if isinstance(node.tag, str) and node.get(XML_ID))
    refs = [node.get("ref") for node in elements if local_name(node) == "xref" and node.get("ref")]
    missing_refs = sorted(set(refs) - source_ids - set(ids))
    if missing_refs:
        failures.append(f"unresolved companion xrefs: {missing_refs}")

    protected = {"m", "me", "men", "md", "mrow", "c", "code", "sage"}
    prose = " ".join(
        text
        for node in elements if local_name(node) not in protected
        for text in (node.text, node.tail) if text
    )
    markers = sorted(set(re.findall(r"\b(?:Let|Show|Prove|Determine|Describe|Suppose|Recall|Hint|Answer|Solution|True|False)\b", prose, re.I)))
    if markers:
        failures.append(f"active English instruction markers: {markers}")
    placeholders = sorted(set(re.findall(r"\b(?:TODO|TBD|FIXME|LOREM)\b|\?\?\?", prose, re.I)))
    if placeholders:
        failures.append(f"placeholder residue: {placeholders}")
    mojibake = sorted(set(re.findall(r"(?:Ã.|Â.|â..|\ufffd)", prose)))
    if mojibake:
        failures.append(f"mojibake residue: {mojibake}")

    wrapper_text = " ".join(companion.read_text(encoding="utf-8").split())
    for phrase in ("Creative Commons Attribution 4.0", "bukan teks Steven Schlicker", "CC BY-NC-SA 3.0"):
        if phrase not in wrapper_text:
            failures.append(f"missing component-boundary phrase: {phrase}")
    for label, path in (("companion/RIGHTS.md", rights_path), ("LICENSES.md", licenses_path)):
        text = " ".join(path.read_text(encoding="utf-8").split())
        for phrase in ("CC BY 4.0", "CC BY-NC-SA 3.0"):
            if phrase not in text:
                failures.append(f"{label} omits required rights phrase: {phrase}")
        if "endorsement" not in text.lower():
            failures.append(f"{label} omits a non-endorsement statement")
    if re.search(r"(?:C:\\Users\\|github_pat_|ghp_|ZENODO|api[_-]?token|access[_-]?token)", wrapper_text, re.I):
        failures.append("local path or credential-like residue in companion")

    forbidden_surfaces: list[dict[str, object]] = []
    for surface, label in [
        *[(authority_root / name, "authority") for name in SOURCE_FILES],
        *[(repo / "source" / name, "translated") for name in SOURCE_FILES],
        *[(repo / "companion" / name, "companion") for name in FRAGMENTS],
    ]:
        tree_root = etree.parse(str(surface), parser).getroot()
        for node in tree_root.iter():
            if isinstance(node.tag, str) and (local_name(node) in REMOTE_TAGS or local_name(node) == "image"):
                forbidden_surfaces.append({"surface": label, "file": surface.name, "tag": local_name(node), "line": node.sourceline})
    if forbidden_surfaces:
        failures.append(f"unexpected image, interactive, or remote surfaces: {forbidden_surfaces}")

    with terminology_path.open(encoding="utf-8-sig", newline="") as handle:
        terms = [row for row in csv.DictReader(handle) if row.get("id") in EXPECTED_TERM_IDS]
    if {row.get("id") for row in terms} != EXPECTED_TERM_IDS:
        failures.append("Chapter 11 terminology controls are incomplete")
    if any(row.get("status") != "approved" or not row.get("id_ID") for row in terms):
        failures.append("Chapter 11 terminology controls are not fully approved and populated")
    with corrections_path.open(encoding="utf-8-sig", newline="") as handle:
        corrections = [row for row in csv.DictReader(handle) if row.get("id") in EXPECTED_CORRECTION_IDS]
    if {row.get("id") for row in corrections} != EXPECTED_CORRECTION_IDS:
        failures.append("Chapter 11 correction controls are incomplete")
    if any(row.get("status") != "verified" or not row.get("evidence") for row in corrections):
        failures.append("Chapter 11 correction statuses or evidence differ from the frozen ledger")

    report = {
        "schema_version": 2,
        "status": "pass" if not failures else "fail",
        "authority_ordered_sha256": ordered_digest.hexdigest(),
        "authority_raw_concatenated_sha256": raw_digest.hexdigest(),
        "companion": identity(companion, "companion/chapter_11_metric_subspaces_self_study.ptx"),
        "fragments": [identity(repo / "companion" / name, f"companion/{name}") for name in FRAGMENTS],
        "entry_counts": {
            "source_prompt_guide": EXPECTED_SOURCE_PROMPTS,
            "activity_or_task_guide": EXPECTED_ACTIVITY_PROMPTS,
            "exercise_prompt_guide": EXPECTED_EXERCISE_PROMPTS,
            "mastery_check": EXPECTED_MASTERY,
            "total": EXPECTED_SOURCE_PROMPTS + EXPECTED_MASTERY,
        },
        "reveal_counts": dict(reveal_counts),
        "surface_counts": dict(surface_counts),
        "source_prompt_counts": prompt_counts,
        "source_prompt_total": source_prompt_total,
        "excluded_grouping_tasks": EXPECTED_GROUPING_TASKS,
        "source_prompt_mappings": mappings,
        "xml_ids": len(ids),
        "xrefs": len(refs),
        "missing_xrefs": missing_refs,
        "entries": entries,
        "source_qa": identity(source_qa_path, "qa/CHAPTER11_SOURCE_QA.json"),
        "control_inputs": {
            "terminology": {**identity(terminology_path, "00_control/TERMINOLOGY.csv"), "required_ids": sorted(EXPECTED_TERM_IDS)},
            "source_corrections": {**identity(corrections_path, "00_control/SOURCE_CORRECTIONS.csv"), "required_ids": sorted(EXPECTED_CORRECTION_IDS)},
        },
        "rights_boundary": {
            "companion_license": "CC-BY-4.0",
            "translated_spine_license": "CC-BY-NC-SA-3.0",
            "companion_rights": identity(rights_path, "companion/RIGHTS.md"),
            "collection_licenses": identity(licenses_path, "LICENSES.md"),
        },
        "assets": {"images": [], "interactive_or_remote_surfaces": forbidden_surfaces},
        "failures": failures,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "report": identity(report_path, "qa/CHAPTER11_COMPANION_QA.json"),
        "status": report["status"],
        "entry_counts": report["entry_counts"],
        "reveal_counts": dict(reveal_counts),
        "surface_counts": dict(surface_counts),
        "source_prompt_counts": prompt_counts,
        "failures": failures,
    }, ensure_ascii=False, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
