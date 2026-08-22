#!/usr/bin/env python3
"""Fail-closed coverage, rights, and source-link audit for Chapter 9."""

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
    "chap_sequences.ptx",
    "sec_seq_intro.ptx",
    "sec_seq_cont_metric.ptx",
    "sec_seq_summ.ptx",
    "sec_seq_exer.ptx",
)
FILE_GROUPS = {
    "sec_seq_intro.ptx": (("sequence-intro", 3),),
    "sec_seq_cont_metric.ptx": (("sequence-continuity", 13),),
    "sec_seq_exer.ptx": (("exercise", 28),),
}
FRAGMENTS = (
    "chapter_09_source_guides.ptx",
    "chapter_09_exercise_guides_a.ptx",
    "chapter_09_exercise_guides_b.ptx",
    "chapter_09_mastery.ptx",
)
EXPECTED_AUTHORITY_ORDERED_SHA256 = (
    "c1bfefbb86f9f4a2dc0d19b1d73f50ec5de2ecd8aa188f24d271987cd44bc627"
)
EXPECTED_AUTHORITY_RAW_SHA256 = (
    "c6d2935beda94460617eeba29cf6bd181fd7d061bbd11ed6b8471b91d614cce9"
)
EXPECTED_TERM_IDS = {f"O003-T{number:03d}" for number in range(113, 122)}
EXPECTED_CORRECTION_IDS = {f"O003-C{number:03d}" for number in range(82, 97)}
EXPECTED_SOURCE_PROMPTS = 44
EXPECTED_ACTIVITY_PROMPTS = 16
EXPECTED_EXERCISE_PROMPTS = 28
EXPECTED_MASTERY = 6
EXPECTED_EXTERNAL_XREFS = {
    "act_MS_metrics",
    "ex_GLB_function_sup_metric",
    "ex_MS_Q_metric",
}
EXPECTED_INSERTIONS: dict[str, str] = {
    "sec_seq_intro.ptx:66:description": "description",
    "sec_seq_intro.ptx:67:m": "m",
    "sec_seq_intro.ptx:68:m": "m",
    "sec_seq_intro.ptx:69:m": "m",
    "sec_seq_intro.ptx:70:m": "m",
    "sec_seq_intro.ptx:71:m": "m",
}
IMAGE_USES: dict[str, str] = {"Sequence_limit": "sec_seq_intro.ptx"}
REMOTE_TAGS = {"url", "video", "interactive", "sage", "webwork", "iframe"}


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
    return {
        "path": display_path,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def normalized_text(node: etree._Element) -> str:
    return " ".join("".join(node.itertext()).split())


def element_sha256(node: etree._Element) -> str:
    data = etree.tostring(node, encoding="utf-8", with_tail=False)
    return hashlib.sha256(data).hexdigest()


def guide_id(sequence: int) -> str:
    return f"o003-c90-ch09-guide-{sequence:02d}"


def expected_source_entry_ids() -> list[str]:
    return [guide_id(sequence) for sequence in range(1, EXPECTED_SOURCE_PROMPTS + 1)]


def expected_entry_ids() -> list[str]:
    return expected_source_entry_ids() + [
        f"o003-c90-ch09-mastery-{ordinal:02d}"
        for ordinal in range(1, EXPECTED_MASTERY + 1)
    ]


def prompt_nodes(tree: etree._ElementTree, name: str) -> list[Prompt]:
    """Return every assessable Chapter 9 prompt in reader order."""
    root = tree.getroot()
    if name != "sec_seq_exer.ptx":
        prompts: list[Prompt] = []
        for task in root.iter("task"):
            prompts.extend(
                Prompt(task, statement, "statement_bearing_task")
                for statement in task.findall("statement")
            )
        return prompts

    prompts = []
    for exercise in root.findall("exercise"):
        nested: list[Prompt] = []
        for task in exercise.iter("task"):
            nested.extend(
                Prompt(task, statement, "statement_bearing_task")
                for statement in task.findall("statement")
            )
        if nested:
            prompts.extend(nested)
        else:
            statement = exercise.find("statement")
            if statement is not None:
                prompts.append(Prompt(exercise, statement, "standalone_exercise"))
    return prompts


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
    for name, groups in FILE_GROUPS.items():
        authority_tree = etree.parse(str(authority_root / name), parser)
        translated_tree = etree.parse(str(repo / "source" / name), parser)
        authority_prompts = prompt_nodes(authority_tree, name)
        translated_prompts = prompt_nodes(translated_tree, name)
        expected_count = sum(count for _, count in groups)
        counts[name] = len(translated_prompts)
        if len(authority_prompts) != expected_count:
            failures.append(
                f"authority prompt count changed in {name}: "
                f"{len(authority_prompts)} != {expected_count}"
            )
        if len(translated_prompts) != expected_count:
            failures.append(
                f"translated prompt count changed in {name}: "
                f"{len(translated_prompts)} != {expected_count}"
            )
        group_labels = [
            (group, ordinal)
            for group, count in groups
            for ordinal in range(1, count + 1)
        ]
        for sequence, (authority, translated) in enumerate(
            zip(authority_prompts, translated_prompts), start=1
        ):
            if sequence > len(group_labels):
                failures.append(f"unexpected prompt beyond contract in {name}")
                continue
            group, ordinal = group_labels[sequence - 1]
            if authority.kind != translated.kind:
                failures.append(f"prompt classification changed in {name}:{sequence}")
            authority_context = nearest_context_id(authority.anchor)
            translated_context = nearest_context_id(translated.anchor)
            if authority_context != translated_context:
                failures.append(f"prompt context ID changed in {name}:{sequence}")
            mappings.append(
                {
                    "companion_entry_id": guide_id(len(mappings) + 1),
                    "source_anchor_id": (
                        f"o003-gvsu-ch09-{Path(name).stem}-prompt-{sequence:02d}"
                    ),
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
                }
            )
    return mappings, counts


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    repo = Path(__file__).resolve().parent.parent
    lane = repo.parent
    authority_root = (
        lane
        / "authority/gvsu-pinned/topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9/source"
    )
    authority_assets = authority_root.parent / "assets"
    companion = repo / "companion/chapter_09_sequences_self_study.ptx"
    report_path = repo / "qa/CHAPTER09_COMPANION_QA.json"
    source_qa_path = repo / "qa/CHAPTER09_SOURCE_QA.json"
    terminology_path = lane / "00_control/TERMINOLOGY.csv"
    corrections_path = lane / "00_control/SOURCE_CORRECTIONS.csv"
    companion_rights_path = repo / "companion/RIGHTS.md"
    licenses_path = repo / "LICENSES.md"
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    failures: list[str] = []

    required_paths = [
        companion,
        source_qa_path,
        terminology_path,
        corrections_path,
        companion_rights_path,
        licenses_path,
        *(repo / "companion" / name for name in FRAGMENTS),
        *(repo / "source" / name for name in SOURCE_FILES),
        *(authority_root / name for name in SOURCE_FILES),
    ]
    missing = [str(path) for path in required_paths if not path.is_file()]
    if missing:
        raise SystemExit(f"missing required Chapter 9 inputs: {missing}")

    source_qa = json.loads(source_qa_path.read_text(encoding="utf-8"))
    if source_qa.get("status") != "pass":
        failures.append("Chapter 9 source QA is not passing")
    source_qa_files = {item.get("file"): item for item in source_qa.get("files", [])}
    for name in SOURCE_FILES:
        item = source_qa_files.get(name)
        if item is None:
            failures.append(f"source QA omits {name}")
            continue
        if item.get("authority", {}).get("sha256") != sha256(authority_root / name):
            failures.append(f"source QA authority identity is stale for {name}")
        if item.get("translated", {}).get("sha256") != sha256(repo / "source" / name):
            failures.append(f"source QA translated identity is stale for {name}")

    insertion_rows = source_qa.get("approved_element_insertions", [])
    actual_insertions = {row.get("key"): row for row in insertion_rows}
    if set(actual_insertions) != set(EXPECTED_INSERTIONS):
        failures.append("Chapter 9 approved element-insertion closure changed")
    else:
        for key, expected_tag in EXPECTED_INSERTIONS.items():
            raw = str(actual_insertions[key].get("element", "")).lstrip()
            if not raw.startswith(f"<{expected_tag}"):
                failures.append(f"approved insertion has the wrong element shell: {key}")
    if source_qa.get("approved_element_block_moves") not in ([], None):
        failures.append("unexpected approved Chapter 9 element block move")
    if source_qa.get("approved_element_shell_moves") not in ([], None):
        failures.append("unexpected approved Chapter 9 element shell move")
    math_changes = source_qa.get("approved_math_changes", [])
    if math_changes != [
        {
            "authority": "<mrow>n \\amp \\gt N \\gt \\frac{1}{\\epsilon} -1</mrow>",
            "key": "sec_seq_intro.ptx:62",
            "translated": "<mrow>n \\amp \\geq N \\gt \\frac{1}{\\epsilon} -1</mrow>",
        },
        {
            "authority": "<me> d_E(a,y) = | x-y | </me>",
            "key": "sec_seq_intro.ptx:113",
            "translated": "<me> d_E(x,y) = | x-y | </me>",
        },
        {
            "authority": "<me> d_T((x_1, x_2), (y_1, y_1)) = | x_1-y_1| + | x_2-y_2 | </me>",
            "key": "sec_seq_intro.ptx:117",
            "translated": "<me> d_T((x_1, x_2), (y_1, y_2)) = | x_1-y_1| + | x_2-y_2 | </me>",
        },
        {
            "authority": "<m>\\lim f(a_n) = a</m>",
            "key": "sec_seq_cont_metric.ptx:60",
            "translated": "<m>\\lim f(a_n) = f(a)</m>",
        },
        {
            "authority": "<me> d(x,A) = \\inf \\{d(x,a) \\mid a \\in A </me>",
            "key": "sec_seq_exer.ptx:27",
            "translated": "<me> d(x,A) = \\inf \\{d(x,a) \\mid a \\in A\\} </me>",
        },
        {
            "authority": "<m>(R,d)</m>",
            "key": "sec_seq_exer.ptx:57",
            "translated": "<m>(\\R,d)</m>",
        },
        {
            "authority": "<m>(f)</m>",
            "key": "sec_seq_exer.ptx:141",
            "translated": "<m>f</m>",
        },
        {
            "authority": "<m>\\R</m>",
            "key": "sec_seq_exer.ptx:145",
            "translated": "<m>[0,1]</m>",
        },
        {
            "authority": "<m>C[01]</m>",
            "key": "sec_seq_exer.ptx:149",
            "translated": "<m>C[0,1]</m>",
        },
    ]:
        failures.append("Chapter 9 protected-math repair closure changed")
    if set(source_qa.get("approved_external_xref_targets", [])) != EXPECTED_EXTERNAL_XREFS:
        failures.append("Chapter 9 approved external-xref closure changed")

    ordered_digest = hashlib.sha256()
    raw_digest = hashlib.sha256()
    for name in SOURCE_FILES:
        data = (authority_root / name).read_bytes()
        ordered_digest.update(name.encode("utf-8"))
        ordered_digest.update(b"\0")
        ordered_digest.update(data)
        raw_digest.update(data)
    if ordered_digest.hexdigest() != EXPECTED_AUTHORITY_ORDERED_SHA256:
        failures.append("frozen Chapter 9 authority name-delimited identity changed")
    if raw_digest.hexdigest() != EXPECTED_AUTHORITY_RAW_SHA256:
        failures.append("frozen Chapter 9 authority raw-concatenation identity changed")

    tree = etree.parse(str(companion), parser)
    try:
        tree.xinclude()
    except etree.XIncludeError as exc:
        failures.append(f"XInclude closure failed: {exc}")
    root = tree.getroot()
    if root.get(XML_ID) != "o003-c90-ch09-companion":
        failures.append("unexpected Chapter 9 companion root ID")
    if root.get(XML_LANG) != "id-ID":
        failures.append("Chapter 9 companion root is not explicitly id-ID")
    for name in FRAGMENTS:
        fragment_root = etree.parse(str(repo / "companion" / name), parser).getroot()
        if fragment_root.get(XML_LANG) != "id-ID":
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
        failures.append(
            f"companion entry sequence differs: found {len(actual_ids)}, "
            f"expected {len(expected_ids)}"
        )

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
                failures.append(f"{expected_id} has noncanonical {kind} ID")
            surfaces[kind] = {
                "id": expected_surface_id,
                "id_origin": "xml_id" if xml_id == expected_surface_id else "assigned_backend_alias",
                "xml_id": xml_id,
            }
            surface_counts[kind] += 1
            if kind != "statement":
                reveals[kind] = expected_surface_id
                reveal_counts[kind] += 1
        entries.append(
            {
                "id": expected_id,
                "kind": "mastery_check" if "-mastery-" in expected_id else "source_prompt_guide",
                "sequence": sequence,
                "title": title or None,
                "text_lengths": lengths,
                "reveals": reveals,
                "surfaces": surfaces,
            }
        )

    mappings, prompt_counts = source_prompt_mappings(repo, authority_root, parser, failures)
    source_prompt_total = sum(prompt_counts.values())
    if source_prompt_total != EXPECTED_SOURCE_PROMPTS:
        failures.append(
            f"source prompt count changed: {source_prompt_total} != {EXPECTED_SOURCE_PROMPTS}"
        )
    if [row["companion_entry_id"] for row in mappings] != expected_source_entry_ids():
        failures.append("source prompt mapping order does not match companion entry order")

    source_ids: set[str] = set()
    for name in SOURCE_FILES:
        source_root = etree.parse(str(repo / "source" / name), parser).getroot()
        source_ids.update(
            node.get(XML_ID)
            for node in source_root.iter()
            if isinstance(node.tag, str) and node.get(XML_ID)
        )
    refs = [
        node.get("ref")
        for node in elements
        if local_name(node) == "xref" and node.get("ref")
    ]
    missing_refs = sorted(set(refs) - source_ids - set(ids) - EXPECTED_EXTERNAL_XREFS)
    if missing_refs:
        failures.append(f"unresolved companion xrefs: {missing_refs}")

    protected = {"m", "me", "men", "md", "mrow", "c", "code", "sage"}
    prose_parts: list[str] = []
    for node in elements:
        if local_name(node) in protected:
            continue
        if node.text:
            prose_parts.append(node.text)
        if node.tail:
            prose_parts.append(node.tail)
    prose = " ".join(prose_parts)
    markers = sorted(
        set(
            re.findall(
                r"\b(?:Let|Show|Prove|Determine|Describe|Suppose|Recall|Hint|Answer|Solution|True|False)\b",
                prose,
                flags=re.IGNORECASE,
            )
        )
    )
    if markers:
        failures.append(f"active English instruction markers: {markers}")
    placeholders = sorted(
        set(re.findall(r"\b(?:TODO|TBD|FIXME|LOREM)\b|\?\?\?", prose, flags=re.IGNORECASE))
    )
    if placeholders:
        failures.append(f"placeholder residue: {placeholders}")
    mojibake = sorted(set(re.findall(r"(?:Ã.|Â.|â..|\ufffd)", prose)))
    if mojibake:
        failures.append(f"mojibake residue: {mojibake}")

    normalized_wrapper = " ".join(companion.read_text(encoding="utf-8").split())
    normalized_rights = " ".join(companion_rights_path.read_text(encoding="utf-8").split())
    normalized_licenses = " ".join(licenses_path.read_text(encoding="utf-8").split())
    for phrase in (
        "Creative Commons Attribution 4.0",
        "bukan teks Steven Schlicker atau GVSU",
        "tidak menyalin ungkapan dari karya Anton Petrunin",
        "CC BY-NC-SA 3.0",
    ):
        if phrase not in normalized_wrapper:
            failures.append(f"missing component-boundary phrase: {phrase}")
    for label, text in (("companion/RIGHTS.md", normalized_rights), ("LICENSES.md", normalized_licenses)):
        for phrase in ("CC BY 4.0", "CC BY-NC-SA 3.0"):
            if phrase not in text:
                failures.append(f"{label} omits required rights phrase: {phrase}")
        if "endorsement" not in text.lower():
            failures.append(f"{label} omits a non-endorsement statement")
    if re.search(
        r"(?:C:\\Users\\|github_pat_|ghp_|ZENODO|api[_-]?token|access[_-]?token)",
        normalized_wrapper,
        flags=re.IGNORECASE,
    ):
        failures.append("local path or credential-like residue in companion")

    descriptions: list[dict[str, object]] = []
    for stem, source_name in IMAGE_USES.items():
        translated_tree = etree.parse(str(repo / "source" / source_name), parser)
        images = translated_tree.xpath(f"//image[@source='{stem}']")
        if len(images) != 1:
            failures.append(f"expected exactly one active image use for {stem}")
            continue
        description_nodes = images[0].findall("description")
        if len(description_nodes) != 1:
            failures.append(f"{stem} requires exactly one Indonesian description")
            continue
        description_node = description_nodes[0]
        description = normalized_text(description_node)
        if len(description) < 80:
            failures.append(f"{stem} description is too short: {len(description)}")
        descriptions.append(
            {
                "stem": stem,
                "source_file": f"source/{source_name}",
                "source_line": description_node.sourceline,
                "source_selector": translated_tree.getpath(description_node),
                "text": description,
                "language": "id-ID",
            }
        )
        for suffix in ("svg", "pdf"):
            authority_asset = authority_assets / f"{stem}.{suffix}"
            repository_asset = repo / "assets" / f"{stem}.{suffix}"
            if not authority_asset.is_file() or not repository_asset.is_file():
                failures.append(f"missing paired {stem}.{suffix} asset")
            elif sha256(authority_asset) != sha256(repository_asset):
                failures.append(f"repository asset differs from authority: {stem}.{suffix}")

    remote_surfaces: list[dict[str, object]] = []
    for name in SOURCE_FILES:
        for surface, tree_label in (
            (authority_root / name, "authority"),
            (repo / "source" / name, "translated"),
        ):
            tree_root = etree.parse(str(surface), parser).getroot()
            for node in tree_root.iter():
                if isinstance(node.tag, str) and local_name(node) in REMOTE_TAGS:
                    remote_surfaces.append(
                        {"surface": tree_label, "file": name, "tag": local_name(node), "line": node.sourceline}
                    )
    if remote_surfaces:
        failures.append(f"unexpected interactive or remote surfaces: {remote_surfaces}")

    with terminology_path.open(encoding="utf-8-sig", newline="") as handle:
        terms = [row for row in csv.DictReader(handle) if row.get("id") in EXPECTED_TERM_IDS]
    if {row.get("id") for row in terms} != EXPECTED_TERM_IDS:
        failures.append("Chapter 9 terminology controls are incomplete")
    if any(row.get("status") != "approved" or not row.get("id_ID") for row in terms):
        failures.append("Chapter 9 terminology controls are not fully approved and populated")
    with corrections_path.open(encoding="utf-8-sig", newline="") as handle:
        corrections = [
            row for row in csv.DictReader(handle)
            if row.get("unit") == "chapter_09_sequences"
        ]
    if {row.get("id") for row in corrections} != EXPECTED_CORRECTION_IDS:
        failures.append("Chapter 9 correction controls O003-C082 through O003-C096 are incomplete")
    correction_statuses = {row.get("id"): row.get("status") for row in corrections}
    expected_statuses = {
        **{f"O003-C{number:03d}": "verified" for number in range(82, 97) if number != 95},
        "O003-C095": "verified",
    }
    if correction_statuses != expected_statuses or any(not row.get("evidence") for row in corrections):
        failures.append("Chapter 9 correction statuses or evidence differ from the frozen ledger")

    report = {
        "schema_version": 2,
        "status": "pass" if not failures else "fail",
        "authority_ordered_sha256": ordered_digest.hexdigest(),
        "authority_raw_concatenated_sha256": raw_digest.hexdigest(),
        "companion": identity(companion, "companion/chapter_09_sequences_self_study.ptx"),
        "fragments": [
            identity(repo / "companion" / name, f"companion/{name}") for name in FRAGMENTS
        ],
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
        "source_prompt_mappings": mappings,
        "xml_ids": len(ids),
        "xrefs": len(refs),
        "missing_xrefs": missing_refs,
        "entries": entries,
        "source_qa": identity(source_qa_path, "qa/CHAPTER09_SOURCE_QA.json"),
        "control_inputs": {
            "terminology": {
                **identity(terminology_path, "00_control/TERMINOLOGY.csv"),
                "required_ids": sorted(EXPECTED_TERM_IDS),
            },
            "source_corrections": {
                **identity(corrections_path, "00_control/SOURCE_CORRECTIONS.csv"),
                "required_ids": sorted(EXPECTED_CORRECTION_IDS),
            },
        },
        "rights_boundary": {
            "companion_license": "CC-BY-4.0",
            "translated_spine_license": "CC-BY-NC-SA-3.0",
            "companion_rights": identity(companion_rights_path, "companion/RIGHTS.md"),
            "collection_licenses": identity(licenses_path, "LICENSES.md"),
        },
        "assets": {
            "image_descriptions": descriptions,
            "described_images": len(descriptions),
            "interactive_or_remote_surfaces": remote_surfaces,
        },
        "failures": failures,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "report": identity(report_path, "qa/CHAPTER09_COMPANION_QA.json"),
                "status": report["status"],
                "entry_counts": report["entry_counts"],
                "reveal_counts": dict(reveal_counts),
                "surface_counts": dict(surface_counts),
                "source_prompt_counts": prompt_counts,
                "described_images": len(descriptions),
                "failures": failures,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
