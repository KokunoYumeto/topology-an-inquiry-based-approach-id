#!/usr/bin/env python3
"""Fail-closed coverage, rights, and asset audit for the Chapter 6 companion."""

from __future__ import annotations

from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
import sys

from lxml import etree


XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"
SOURCE_FILES = (
    "chap_continuous_functions.ptx",
    "sec_cont_func_intro.ptx",
    "sec_cont_func_btwn.ptx",
    "sec_comp_cont_func.ptx",
    "sec_cont_func_summ.ptx",
    "sec_cont_func_exer.ptx",
)
PROMPT_GROUPS = (
    ("sec_cont_func_intro.ptx", "intro", 4),
    ("sec_cont_func_btwn.ptx", "between", 5),
    ("sec_comp_cont_func.ptx", "composition", 4),
    ("sec_cont_func_exer.ptx", "exercise", 26),
)
FRAGMENTS = (
    "chapter_06_source_guides.ptx",
    "chapter_06_exercise_guides_a.ptx",
    "chapter_06_exercise_guides_b.ptx",
    "chapter_06_mastery.ptx",
)
EXPECTED_AUTHORITY_ORDERED_SHA256 = (
    "6872eac9f833addfc84b711f5d1509ec00116db884ca509dc73f8f2763bd581a"
)
EXPECTED_TERM_IDS = {f"O003-T{number:03d}" for number in range(93, 98)}
EXPECTED_CORRECTION_IDS = {f"O003-C{number:03d}" for number in range(57, 66)}
EXPECTED_SOURCE_PROMPTS = 39
EXPECTED_ACTIVITY_PROMPTS = 13
EXPECTED_EXERCISE_PROMPTS = 26
EXPECTED_MASTERY = 6
LOCAL_LAB = "external/o003-epsilon-delta-lab.html"
UPSTREAM_INTERACTIVE = "https://www.geogebra.org/m/rym36sqs"
IMAGE_STEMS = ("Continuity_1", "Continuity_2")


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


def expected_source_entry_ids() -> list[str]:
    ids: list[str] = []
    for _, group, count in PROMPT_GROUPS:
        ids.extend(
            f"o003-c90-ch06-{group}-task-{number:02d}"
            for number in range(1, count + 1)
        )
    return ids


def expected_entry_ids() -> list[str]:
    return expected_source_entry_ids() + [
        f"o003-c90-ch06-mastery-{number:02d}"
        for number in range(1, EXPECTED_MASTERY + 1)
    ]


def prompt_nodes(tree: etree._ElementTree, name: str) -> list[tuple[etree._Element, str]]:
    root = tree.getroot()
    if name in {
        "sec_cont_func_intro.ptx",
        "sec_cont_func_btwn.ptx",
        "sec_comp_cont_func.ptx",
    }:
        return [
            (node, "statement_bearing_task")
            for node in root.iter("task")
            if node.find("statement") is not None
        ]
    if name != "sec_cont_func_exer.ptx":
        return []
    prompts: list[tuple[etree._Element, str]] = []
    for exercise in root.findall("exercise"):
        tasks = [
            node
            for node in exercise.iter("task")
            if node.find("statement") is not None
        ]
        if tasks:
            prompts.extend((node, "statement_bearing_task") for node in tasks)
        elif exercise.find("statement") is not None:
            prompts.append((exercise, "standalone_exercise"))
    return prompts


def nearest_context_id(node: etree._Element) -> str | None:
    for ancestor in node.iterancestors():
        if ancestor.get(XML_ID):
            return ancestor.get(XML_ID)
    return None


def source_prompt_mappings(
    repo: Path,
    authority_root: Path,
    parser: etree.XMLParser,
    failures: list[str],
) -> tuple[list[dict[str, object]], dict[str, int]]:
    mappings: list[dict[str, object]] = []
    counts = {name: 0 for name in SOURCE_FILES}
    expected_ids = expected_source_entry_ids()
    entry_offset = 0
    for name, group, expected_count in PROMPT_GROUPS:
        authority_tree = etree.parse(str(authority_root / name), parser)
        translated_tree = etree.parse(str(repo / "source" / name), parser)
        authority_prompts = prompt_nodes(authority_tree, name)
        translated_prompts = prompt_nodes(translated_tree, name)
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
        for ordinal, (authority_pair, translated_pair) in enumerate(
            zip(authority_prompts, translated_prompts), start=1
        ):
            authority_node, authority_kind = authority_pair
            translated_node, translated_kind = translated_pair
            if local_name(authority_node) != local_name(translated_node):
                failures.append(f"prompt element kind changed in {name}:{ordinal}")
            if authority_kind != translated_kind:
                failures.append(f"prompt classification changed in {name}:{ordinal}")
            authority_context = nearest_context_id(authority_node)
            translated_context = nearest_context_id(translated_node)
            if authority_context != translated_context:
                failures.append(f"prompt context ID changed in {name}:{ordinal}")
            entry_index = entry_offset + ordinal - 1
            if entry_index >= len(expected_ids):
                failures.append(f"unexpected prompt beyond expected sequence in {name}")
                continue
            mappings.append(
                {
                    "companion_entry_id": expected_ids[entry_index],
                    "source_anchor_id": (
                        f"o003-gvsu-ch06-{Path(name).stem}-prompt-{ordinal:02d}"
                    ),
                    "group": group,
                    "ordinal_within_group": ordinal,
                    "prompt_kind": authority_kind,
                    "source_context_id": authority_context,
                    "authority_file": f"source/{name}",
                    "authority_line": authority_node.sourceline,
                    "authority_selector": authority_tree.getpath(authority_node),
                    "translated_file": f"source/{name}",
                    "translated_line": translated_node.sourceline,
                    "translated_selector": translated_tree.getpath(translated_node),
                }
            )
        entry_offset += expected_count
    counts["chap_continuous_functions.ptx"] = 0
    counts["sec_cont_func_summ.ptx"] = 0
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
    companion = repo / "companion/chapter_06_continuous_functions_self_study.ptx"
    report_path = repo / "qa/CHAPTER06_COMPANION_QA.json"
    source_qa_path = repo / "qa/CHAPTER06_SOURCE_QA.json"
    terminology_path = lane / "00_control/TERMINOLOGY.csv"
    corrections_path = lane / "00_control/SOURCE_CORRECTIONS.csv"
    companion_rights_path = repo / "companion/RIGHTS.md"
    licenses_path = repo / "LICENSES.md"
    lab_path = repo / "assets/o003-epsilon-delta-lab.html"
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    failures: list[str] = []

    required_paths = [
        companion,
        source_qa_path,
        terminology_path,
        corrections_path,
        companion_rights_path,
        licenses_path,
        lab_path,
        *(repo / "companion" / name for name in FRAGMENTS),
        *(repo / "source" / name for name in SOURCE_FILES),
        *(authority_root / name for name in SOURCE_FILES),
    ]
    missing_paths = [str(path) for path in required_paths if not path.is_file()]
    if missing_paths:
        raise SystemExit(f"missing required Chapter 6 inputs: {missing_paths}")

    source_qa = json.loads(source_qa_path.read_text(encoding="utf-8"))
    if source_qa.get("status") != "pass":
        failures.append("Chapter 6 source QA is not passing")
    source_qa_files = {
        item.get("file"): item for item in source_qa.get("files", [])
    }
    for name in SOURCE_FILES:
        item = source_qa_files.get(name)
        if item is None:
            failures.append(f"source QA omits {name}")
            continue
        if item.get("authority", {}).get("sha256") != sha256(authority_root / name):
            failures.append(f"source QA authority identity is stale for {name}")
        if item.get("translated", {}).get("sha256") != sha256(repo / "source" / name):
            failures.append(f"source QA translated identity is stale for {name}")

    ordered_digest = hashlib.sha256()
    for name in SOURCE_FILES:
        ordered_digest.update(name.encode("utf-8"))
        ordered_digest.update(b"\0")
        ordered_digest.update((authority_root / name).read_bytes())
    if ordered_digest.hexdigest() != EXPECTED_AUTHORITY_ORDERED_SHA256:
        failures.append("frozen Chapter 6 authority closure identity changed")

    tree = etree.parse(str(companion), parser)
    try:
        tree.xinclude()
    except etree.XIncludeError as exc:
        failures.append(f"XInclude closure failed: {exc}")
    root = tree.getroot()
    if root.get(XML_ID) != "o003-c90-ch06-companion":
        failures.append("unexpected companion root ID")
    if root.get(XML_LANG) != "id-ID":
        failures.append("companion root is not explicitly id-ID")
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
    surface_counts: Counter[str] = Counter()
    minima = {"statement": 25, "hint": 18, "answer": 12, "solution": 75}
    for sequence, entry_id in enumerate(expected_ids, start=1):
        exercise = by_id.get(entry_id)
        if exercise is None or local_name(exercise) != "exercise":
            failures.append(f"missing exercise entry: {entry_id}")
            continue
        titles = exercise.findall("title")
        if len(titles) != 1 or len(normalized_text(titles[0])) < 5:
            failures.append(f"{entry_id} requires exactly one nonempty title")
        lengths: dict[str, int] = {}
        reveal_ids: dict[str, str] = {}
        surfaces: dict[str, dict[str, object]] = {}
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
            expected_surface_id = f"{entry_id}-{kind}"
            xml_id = child.get(XML_ID)
            if kind == "statement" and xml_id not in {None, expected_surface_id}:
                failures.append(f"{entry_id} has conflicting statement ID")
            surfaces[kind] = {
                "id": expected_surface_id,
                "id_origin": (
                    "xml_id" if xml_id == expected_surface_id else "assigned_backend_alias"
                ),
                "xml_id": xml_id,
            }
            surface_counts[kind] += 1
            if kind != "statement":
                reveal_counts[kind] += 1
                expected_reveal_id = expected_surface_id
                reveal_ids[kind] = expected_reveal_id
                if child.get(XML_ID) != expected_reveal_id:
                    failures.append(f"{entry_id} has noncanonical {kind} ID")
        entry_kind = "mastery_check" if "-mastery-" in entry_id else "source_prompt_guide"
        entries.append(
            {
                "id": entry_id,
                "kind": entry_kind,
                "sequence": sequence,
                "title": normalized_text(titles[0]) if len(titles) == 1 else None,
                "text_lengths": lengths,
                "reveals": reveal_ids,
                "surfaces": surfaces,
            }
        )

    mappings, source_prompt_counts = source_prompt_mappings(
        repo, authority_root, parser, failures
    )
    source_prompt_total = sum(source_prompt_counts.values())
    if source_prompt_total != EXPECTED_SOURCE_PROMPTS:
        failures.append(
            f"source prompt count changed: {source_prompt_total} != {EXPECTED_SOURCE_PROMPTS}"
        )
    if len(mappings) != EXPECTED_SOURCE_PROMPTS:
        failures.append(
            f"source mapping count changed: {len(mappings)} != {EXPECTED_SOURCE_PROMPTS}"
        )
    if [item["companion_entry_id"] for item in mappings] != expected_source_entry_ids():
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
    mojibake = sorted(set(re.findall(r"(?:Ã.|Â.|â..|\ufffd)", prose)))
    if mojibake:
        failures.append(f"mojibake residue: {mojibake}")

    normalized_wrapper = " ".join(companion.read_text(encoding="utf-8").split())
    normalized_rights = " ".join(companion_rights_path.read_text(encoding="utf-8").split())
    normalized_licenses = " ".join(licenses_path.read_text(encoding="utf-8").split())
    boundary_phrases = (
        "Creative Commons Attribution 4.0",
        "bukan teks Steven Schlicker atau GVSU",
        "tidak menyalin ungkapan dari karya Anton Petrunin",
        "CC BY-NC-SA 3.0",
    )
    for phrase in boundary_phrases:
        if phrase not in normalized_wrapper:
            failures.append(f"missing component-boundary phrase: {phrase}")
    for label, text in (("companion/RIGHTS.md", normalized_rights), ("LICENSES.md", normalized_licenses)):
        for phrase in (
            "o003-epsilon-delta-lab.html",
            "CC BY 4.0",
            "CC BY-NC-SA 3.0",
            "No endorsement" if label == "companion/RIGHTS.md" else "No endorsement is claimed",
        ):
            if phrase not in text:
                failures.append(f"{label} omits required rights phrase: {phrase}")
    if re.search(
        r"(?:C:\\Users\\|github_pat_|ghp_|ZENODO|api[_-]?token|access[_-]?token)",
        normalized_wrapper,
        flags=re.IGNORECASE,
    ):
        failures.append("local path or credential-like residue in companion")

    intro_tree = etree.parse(str(repo / "source/sec_cont_func_intro.ptx"), parser)
    descriptions: list[dict[str, object]] = []
    for stem in IMAGE_STEMS:
        images = intro_tree.xpath(f"//image[@source='{stem}']")
        if len(images) != 1:
            failures.append(f"expected exactly one active image use for {stem}")
            continue
        description_nodes = images[0].findall("description")
        if len(description_nodes) != 1:
            failures.append(f"{stem} requires exactly one Indonesian description")
            continue
        description = normalized_text(description_nodes[0])
        if len(description) < 80:
            failures.append(f"{stem} description is too short: {len(description)}")
        descriptions.append(
            {
                "stem": stem,
                "source_file": "source/sec_cont_func_intro.ptx",
                "source_line": description_nodes[0].sourceline,
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

    authority_intro = etree.parse(str(authority_root / "sec_cont_func_intro.ptx"), parser)
    translated_exercises = etree.parse(str(repo / "source/sec_cont_func_exer.ptx"), parser)
    authority_geogebra = authority_intro.xpath(
        f"//url[@href='{UPSTREAM_INTERACTIVE}']"
    )
    local_urls = intro_tree.xpath(f"//url[@href='{LOCAL_LAB}']") + translated_exercises.xpath(
        f"//url[@href='{LOCAL_LAB}']"
    )
    if len(authority_geogebra) != 1:
        failures.append("frozen authority no longer has exactly one GeoGebra dependency")
    if len(local_urls) != 2:
        failures.append(f"expected two local lab integration links, found {len(local_urls)}")
    intro_local_urls = intro_tree.xpath(f"//url[@href='{LOCAL_LAB}']")
    if len(intro_local_urls) != 1 or intro_local_urls[0].get("visual") != LOCAL_LAB:
        failures.append("introductory local lab link/visual pair is incomplete")

    lab = lab_path.read_text(encoding="utf-8")
    remote_dependency_patterns = (
        r"<(?:script|iframe|img|audio|video|source)\b[^>]*\bsrc\s*=\s*['\"](?:https?:)?//",
        r"<link\b[^>]*\bhref\s*=\s*['\"](?:https?:)?//",
        r"\b(?:fetch|importScripts|XMLHttpRequest|WebSocket)\s*\(",
    )
    remote_dependencies = [
        pattern for pattern in remote_dependency_patterns if re.search(pattern, lab, re.IGNORECASE)
    ]
    if remote_dependencies:
        failures.append(f"local lab has remote runtime dependencies: {remote_dependencies}")
    lab_markers = (
        '<html lang="id">',
        'role="img"',
        'role="status"',
        'aria-live="polite"',
        '<table',
        "Creative Commons Attribution 4.0 International",
    )
    for marker in lab_markers:
        if marker not in lab:
            failures.append(f"local lab omits accessibility/rights marker: {marker}")

    with terminology_path.open(encoding="utf-8-sig", newline="") as handle:
        all_terms = list(csv.DictReader(handle))
    terms = [row for row in all_terms if row.get("id") in EXPECTED_TERM_IDS]
    if {row.get("id") for row in terms} != EXPECTED_TERM_IDS:
        failures.append("Chapter 6 terminology controls O003-T093 through O003-T097 are incomplete")
    if any(row.get("status") != "approved" or not row.get("id_ID") for row in terms):
        failures.append("Chapter 6 terminology controls are not fully approved and populated")
    with corrections_path.open(encoding="utf-8-sig", newline="") as handle:
        corrections = [
            row
            for row in csv.DictReader(handle)
            if row.get("unit") == "chapter_06_continuous_functions"
        ]
    if {row.get("id") for row in corrections} != EXPECTED_CORRECTION_IDS:
        failures.append("Chapter 6 correction controls O003-C057 through O003-C065 are incomplete")
    if any(row.get("status") not in {"planned", "verified"} or not row.get("evidence") for row in corrections):
        failures.append("Chapter 6 correction controls contain an invalid state or empty evidence")

    report = {
        "schema_version": 2,
        "status": "pass" if not failures else "fail",
        "authority_ordered_sha256": ordered_digest.hexdigest(),
        "companion": identity(
            companion, "companion/chapter_06_continuous_functions_self_study.ptx"
        ),
        "fragments": [
            identity(repo / "companion" / name, f"companion/{name}")
            for name in FRAGMENTS
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
        "source_prompt_counts": source_prompt_counts,
        "source_prompt_total": source_prompt_total,
        "source_prompt_mappings": mappings,
        "xml_ids": len(ids),
        "xrefs": len(refs),
        "missing_xrefs": missing_refs,
        "entries": entries,
        "source_qa": identity(source_qa_path, "qa/CHAPTER06_SOURCE_QA.json"),
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
            "local_lab": identity(lab_path, "assets/o003-epsilon-delta-lab.html"),
            "local_lab_runtime_dependencies": [],
            "local_lab_integration_links": len(local_urls),
            "replaces": UPSTREAM_INTERACTIVE,
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
                "report": identity(report_path, "qa/CHAPTER06_COMPANION_QA.json"),
                "status": report["status"],
                "entry_counts": report["entry_counts"],
                "reveal_counts": report["reveal_counts"],
                "surface_counts": report["surface_counts"],
                "source_prompt_counts": source_prompt_counts,
                "described_images": len(descriptions),
                "local_lab_links": len(local_urls),
                "failures": failures,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
