#!/usr/bin/env python3
"""Generate and fail-closed validate the Chapter 6 modular backend."""

from __future__ import annotations

from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import sys

from lxml import etree


XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
SOURCE_FILES = (
    ("chap_continuous_functions.ptx", "chapter_container"),
    ("sec_cont_func_intro.ptx", "pointwise_continuity_real_functions"),
    ("sec_cont_func_btwn.ptx", "metric_space_continuity"),
    ("sec_comp_cont_func.ptx", "composition_of_continuous_functions"),
    ("sec_cont_func_summ.ptx", "chapter_summary"),
    ("sec_cont_func_exer.ptx", "chapter_exercises"),
)
PROMPT_GROUPS = (
    ("sec_cont_func_intro.ptx", "intro", 4),
    ("sec_cont_func_btwn.ptx", "between", 5),
    ("sec_comp_cont_func.ptx", "composition", 4),
    ("sec_cont_func_exer.ptx", "exercise", 26),
)
COMPANION_FRAGMENTS = (
    "chapter_06_source_guides.ptx",
    "chapter_06_exercise_guides_a.ptx",
    "chapter_06_exercise_guides_b.ptx",
    "chapter_06_mastery.ptx",
)
ALIAS_FIELDS = (
    "companion_entry_id",
    "entry_kind",
    "sequence",
    "source_anchor_id",
    "anchor_origin",
    "source_group",
    "ordinal_within_group",
    "prompt_kind",
    "source_context_id",
    "authority_file",
    "authority_line",
    "authority_selector",
    "authority_statement_sha256",
    "translated_file",
    "translated_line",
    "translated_selector",
    "translated_statement_sha256",
    "relationship",
    "concept_ids",
)
STRUCTURAL_TAGS = {
    "definition",
    "theorem",
    "lemma",
    "corollary",
    "example",
    "exploration",
    "activity",
    "exercise",
    "task",
}
EXPECTED_AUTHORITY_ORDERED_SHA256 = (
    "6872eac9f833addfc84b711f5d1509ec00116db884ca509dc73f8f2763bd581a"
)
EXPECTED_TERM_IDS = {f"O003-T{number:03d}" for number in range(93, 98)}
EXPECTED_CORRECTION_IDS = {f"O003-C{number:03d}" for number in range(57, 66)}
LOCAL_LAB = "external/o003-epsilon-delta-lab.html"
UPSTREAM_INTERACTIVE = "https://www.geogebra.org/m/rym36sqs"
IMAGE_STEMS = ("Continuity_1", "Continuity_2")


def local_name(node: etree._Element) -> str:
    return etree.QName(node).localname


def file_identity(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def normalized_text(node: etree._Element) -> str:
    return " ".join("".join(node.itertext()).split())


def element_sha256(node: etree._Element) -> str:
    data = etree.tostring(node, encoding="utf-8", with_tail=False)
    return hashlib.sha256(data).hexdigest()


def source_entry_ids() -> list[str]:
    ids: list[str] = []
    for _, group, count in PROMPT_GROUPS:
        ids.extend(
            f"o003-c90-ch06-{group}-task-{number:02d}"
            for number in range(1, count + 1)
        )
    return ids


def mastery_entry_ids() -> list[str]:
    return [f"o003-c90-ch06-mastery-{number:02d}" for number in range(1, 7)]


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


def concepts_for(entry_id: str) -> list[str]:
    base = ["metric_space_continuity"]
    suffix = entry_id.removeprefix("o003-c90-ch06-")
    concepts: dict[str, tuple[str, ...]] = {
        "intro-task-01": ("epsilon_delta_continuity", "interactive_numerical_validation", "function_x_sine_x"),
        "intro-task-02": ("epsilon_delta_continuity", "interactive_numerical_validation", "function_x_sine_x"),
        "intro-task-03": ("negation_of_pointwise_continuity", "quantifier_negation"),
        "intro-task-04": ("discontinuity_counterexample", "jump_function"),
        "between-task-01": ("constant_function_continuity",),
        "between-task-02": ("identity_function_continuity",),
        "between-task-03": ("metric_dependence_of_continuity", "identity_map"),
        "between-task-04": ("comparison_of_metrics", "taxicab_metric", "maximum_metric"),
        "between-task-05": ("comparison_of_metrics", "taxicab_metric", "maximum_metric"),
        "composition-task-01": ("composition_of_continuous_functions", "proof_planning"),
        "composition-task-02": ("composition_of_continuous_functions", "intermediate_space_tolerance"),
        "composition-task-03": ("composition_of_continuous_functions", "domain_tolerance_pullback"),
        "composition-task-04": ("composition_of_continuous_functions", "epsilon_delta_proof"),
        "exercise-task-01": ("absolute_value_function", "pointwise_continuity"),
        "exercise-task-02": ("sign_function", "pointwise_discontinuity"),
        "exercise-task-03": ("coordinate_sum", "euclidean_metric"),
        "exercise-task-04": ("coordinate_sum", "maximum_metric"),
        "exercise-task-05": ("discrete_metric", "discrete_domain"),
        "exercise-task-06": ("scalar_multiple_of_continuous_function",),
        "exercise-task-07": ("sum_of_continuous_functions",),
        "exercise-task-08": ("product_of_continuous_functions", "algebraic_decomposition"),
        "exercise-task-09": ("product_of_continuous_functions", "epsilon_delta_bounds"),
        "exercise-task-10": ("product_of_continuous_functions", "epsilon_delta_proof"),
        "exercise-task-11": ("converse_of_sum_rule", "counterexample"),
        "exercise-task-12": ("converse_of_product_rule", "counterexample"),
        "exercise-task-13": ("quadratic_function", "explicit_delta_selection", "interactive_numerical_validation"),
        "exercise-task-14": ("quadratic_function", "pointwise_continuity"),
        "exercise-task-15": ("truncated_metric", "triangle_inequality"),
        "exercise-task-16": ("dense_subsets", "uniqueness_of_continuous_extension"),
        "exercise-task-17": ("dirichlet_function", "nowhere_continuous_function"),
        "exercise-task-18": ("modified_dirichlet_function", "single_point_continuity"),
        "exercise-task-19": ("l1_integral_metric", "function_space_distance"),
        "exercise-task-20": ("integral_functional", "definite_integral"),
        "exercise-task-21": ("integral_functional", "lipschitz_continuity"),
        "exercise-task-22": ("discrete_domain", "true_false_counterexample"),
        "exercise-task-23": ("discrete_codomain", "true_false_counterexample"),
        "exercise-task-24": ("identity_map", "comparison_of_metrics", "true_false_counterexample"),
        "exercise-task-25": ("sum_of_continuous_functions", "taxicab_metric"),
        "exercise-task-26": ("constant_function_continuity",),
        "mastery-01": ("epsilon_delta_continuity", "quantifier_negation"),
        "mastery-02": ("lipschitz_continuity",),
        "mastery-03": ("euclidean_metric", "truncated_metric", "discrete_metric"),
        "mastery-04": ("sum_of_continuous_functions",),
        "mastery-05": ("composition_of_continuous_functions",),
        "mastery-06": ("converse_of_sum_rule", "counterexample"),
    }
    if suffix not in concepts:
        raise SystemExit(f"missing concept mapping for {entry_id}")
    return base + list(concepts[suffix])


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
    companion_path = repo / "companion/chapter_06_continuous_functions_self_study.ptx"
    aliases_path = repo / "backend/chapter_06_entry_aliases.csv"
    output_path = repo / "backend/chapter_06_companion_manifest.json"
    terminology_path = lane / "00_control/TERMINOLOGY.csv"
    corrections_path = lane / "00_control/SOURCE_CORRECTIONS.csv"
    source_qa_path = repo / "qa/CHAPTER06_SOURCE_QA.json"
    companion_qa_path = repo / "qa/CHAPTER06_COMPANION_QA.json"
    lab_path = repo / "assets/o003-epsilon-delta-lab.html"
    parser = etree.XMLParser(resolve_entities=False, no_network=True)

    source_qa = json.loads(source_qa_path.read_text(encoding="utf-8"))
    companion_qa = json.loads(companion_qa_path.read_text(encoding="utf-8"))
    if source_qa.get("status") != "pass":
        raise SystemExit("Chapter 6 source QA is not passing")
    if companion_qa.get("status") != "pass":
        raise SystemExit("Chapter 6 companion QA is not passing")
    if companion_qa.get("companion", {}).get("sha256") != file_identity(companion_path)["sha256"]:
        raise SystemExit("Chapter 6 companion QA is stale")
    qa_fragment_hashes = {
        Path(item["path"]).name: item["sha256"]
        for item in companion_qa.get("fragments", [])
    }
    for name in COMPANION_FRAGMENTS:
        if qa_fragment_hashes.get(name) != file_identity(repo / "companion" / name)["sha256"]:
            raise SystemExit(f"Chapter 6 companion QA fragment identity is stale: {name}")

    ordered_digest = hashlib.sha256()
    for name, _ in SOURCE_FILES:
        ordered_digest.update(name.encode("utf-8"))
        ordered_digest.update(b"\0")
        ordered_digest.update((authority_root / name).read_bytes())
    if ordered_digest.hexdigest() != EXPECTED_AUTHORITY_ORDERED_SHA256:
        raise SystemExit("frozen Chapter 6 authority closure identity changed")

    companion_tree = etree.parse(str(companion_path), parser)
    companion_tree.xinclude()
    companion_root = companion_tree.getroot()
    if companion_root.get(XML_ID) != "o003-c90-ch06-companion":
        raise SystemExit("unexpected Chapter 6 companion root ID")
    companion_elements = [
        node for node in companion_root.iter() if isinstance(node.tag, str)
    ]
    companion_by_id = {
        node.get(XML_ID): node for node in companion_elements if node.get(XML_ID)
    }

    dependencies: list[dict[str, object]] = []
    structural_nodes: list[dict[str, object]] = []
    authority_trees: dict[str, etree._ElementTree] = {}
    translated_trees: dict[str, etree._ElementTree] = {}
    for order, (name, role) in enumerate(SOURCE_FILES):
        authority_path = authority_root / name
        translated_path = repo / "source" / name
        authority_tree = etree.parse(str(authority_path), parser)
        translated_tree = etree.parse(str(translated_path), parser)
        authority_trees[name] = authority_tree
        translated_trees[name] = translated_tree
        dependencies.append(
            {
                "order": order,
                "path": f"source/{name}",
                "xml_id": translated_tree.getroot().get(XML_ID),
                "role": role,
                "authority": file_identity(authority_path),
                "translated": file_identity(translated_path),
            }
        )
        ordinal_by_tag: Counter[str] = Counter()
        for node in translated_tree.getroot().iter():
            if not isinstance(node.tag, str):
                continue
            tag = local_name(node)
            if tag not in STRUCTURAL_TAGS:
                continue
            ordinal_by_tag[tag] += 1
            xml_id = node.get(XML_ID)
            structural_nodes.append(
                {
                    "id": xml_id
                    or f"o003-gvsu-ch06-{Path(name).stem}-{tag}-{ordinal_by_tag[tag]:02d}",
                    "id_origin": "upstream_xml_id" if xml_id else "assigned_locale_neutral",
                    "source_xml_id": xml_id,
                    "kind": tag,
                    "file": f"source/{name}",
                    "ordinal_within_file_and_kind": ordinal_by_tag[tag],
                    "translated_line": node.sourceline,
                    "translated_selector": translated_tree.getpath(node),
                }
            )

    source_ids = source_entry_ids()
    source_prompts: list[dict[str, object]] = []
    entry_offset = 0
    for name, group, expected_count in PROMPT_GROUPS:
        authority_tree = authority_trees[name]
        translated_tree = translated_trees[name]
        authority_prompts = prompt_nodes(authority_tree, name)
        translated_prompts = prompt_nodes(translated_tree, name)
        if len(authority_prompts) != expected_count or len(translated_prompts) != expected_count:
            raise SystemExit(f"source prompt topology changed in {name}")
        for ordinal, ((authority_node, prompt_kind), (translated_node, translated_kind)) in enumerate(
            zip(authority_prompts, translated_prompts, strict=True), start=1
        ):
            if prompt_kind != translated_kind or local_name(authority_node) != local_name(translated_node):
                raise SystemExit(f"source prompt kind changed in {name}:{ordinal}")
            authority_context = nearest_context_id(authority_node)
            translated_context = nearest_context_id(translated_node)
            if authority_context != translated_context:
                raise SystemExit(f"source prompt context changed in {name}:{ordinal}")
            entry_id = source_ids[entry_offset + ordinal - 1]
            authority_statement = authority_node.find("statement")
            translated_statement = translated_node.find("statement")
            if authority_statement is None or translated_statement is None:
                raise SystemExit(f"statement surface missing in {name}:{ordinal}")
            source_prompts.append(
                {
                    "companion_entry_id": entry_id,
                    "source_anchor_id": f"o003-gvsu-ch06-{Path(name).stem}-prompt-{ordinal:02d}",
                    "source_group": group,
                    "ordinal_within_group": ordinal,
                    "prompt_kind": prompt_kind,
                    "source_context_id": authority_context,
                    "authority_file": f"source/{name}",
                    "authority_line": authority_node.sourceline,
                    "authority_selector": authority_tree.getpath(authority_node),
                    "authority_statement_sha256": element_sha256(authority_statement),
                    "translated_file": f"source/{name}",
                    "translated_line": translated_node.sourceline,
                    "translated_selector": translated_tree.getpath(translated_node),
                    "translated_statement_sha256": element_sha256(translated_statement),
                }
            )
        entry_offset += expected_count
    if len(source_prompts) != 39 or [item["companion_entry_id"] for item in source_prompts] != source_ids:
        raise SystemExit("expected exactly 39 ordered source prompt mappings")

    alias_rows: list[dict[str, object]] = []
    for sequence, prompt in enumerate(source_prompts, start=1):
        entry_id = str(prompt["companion_entry_id"])
        alias_rows.append(
            {
                "companion_entry_id": entry_id,
                "entry_kind": "source_prompt_guide",
                "sequence": sequence,
                "source_anchor_id": prompt["source_anchor_id"],
                "anchor_origin": "assigned_locale_neutral",
                "source_group": prompt["source_group"],
                "ordinal_within_group": prompt["ordinal_within_group"],
                "prompt_kind": prompt["prompt_kind"],
                "source_context_id": prompt["source_context_id"] or "",
                "authority_file": prompt["authority_file"],
                "authority_line": prompt["authority_line"],
                "authority_selector": prompt["authority_selector"],
                "authority_statement_sha256": prompt["authority_statement_sha256"],
                "translated_file": prompt["translated_file"],
                "translated_line": prompt["translated_line"],
                "translated_selector": prompt["translated_selector"],
                "translated_statement_sha256": prompt["translated_statement_sha256"],
                "relationship": "provides_staged_support_for_source_prompt",
                "concept_ids": ";".join(concepts_for(entry_id)),
            }
        )
    for offset, entry_id in enumerate(mastery_entry_ids(), start=1):
        alias_rows.append(
            {
                "companion_entry_id": entry_id,
                "entry_kind": "mastery_check",
                "sequence": len(source_ids) + offset,
                "source_anchor_id": f"o003-c90-ch06-original-mastery-{offset:02d}",
                "anchor_origin": "original",
                "source_group": "mastery",
                "ordinal_within_group": offset,
                "prompt_kind": "original_mastery_exercise",
                "source_context_id": "o003-c90-ch06-mastery",
                "authority_file": "",
                "authority_line": "",
                "authority_selector": "",
                "authority_statement_sha256": "",
                "translated_file": "",
                "translated_line": "",
                "translated_selector": "",
                "translated_statement_sha256": "",
                "relationship": "original_transfer_and_mastery_check",
                "concept_ids": ";".join(concepts_for(entry_id)),
            }
        )
    aliases_path.parent.mkdir(parents=True, exist_ok=True)
    with aliases_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ALIAS_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(alias_rows)

    entries: list[dict[str, object]] = []
    counts: Counter[str] = Counter()
    surface_counts: Counter[str] = Counter()
    for row in alias_rows:
        entry_id = str(row["companion_entry_id"])
        entry = companion_by_id.get(entry_id)
        if entry is None or local_name(entry) != "exercise":
            raise SystemExit(f"alias entry does not resolve: {entry_id}")
        title_nodes = entry.findall("title")
        if len(title_nodes) != 1:
            raise SystemExit(f"{entry_id} does not have exactly one title")
        surfaces: dict[str, dict[str, object]] = {}
        for kind in ("statement", "hint", "answer", "solution"):
            children = entry.findall(kind)
            if len(children) != 1:
                raise SystemExit(f"{entry_id} has invalid {kind} surface count")
            child = children[0]
            expected_id = f"{entry_id}-{kind}"
            xml_id = child.get(XML_ID)
            if kind != "statement" and xml_id != expected_id:
                raise SystemExit(f"{entry_id} has invalid {kind} reveal ID")
            if kind == "statement" and xml_id not in {None, expected_id}:
                raise SystemExit(f"{entry_id} has conflicting statement ID")
            surfaces[kind] = {
                "id": expected_id,
                "id_origin": "upstream_xml_id" if xml_id == expected_id else "assigned_backend_alias",
                "xml_id": xml_id,
                "companion_selector": companion_tree.getpath(child),
                "text_sha256": hashlib.sha256(normalized_text(child).encode("utf-8")).hexdigest(),
            }
            surface_counts[kind] += 1
        entry_kind = str(row["entry_kind"])
        counts[entry_kind] += 1
        authority_locator = None
        translated_locator = None
        if row["anchor_origin"] == "assigned_locale_neutral":
            name = str(row["authority_file"]).removeprefix("source/")
            authority_selected = authority_trees[name].xpath(str(row["authority_selector"]))
            translated_selected = translated_trees[name].xpath(str(row["translated_selector"]))
            if len(authority_selected) != 1 or authority_selected[0].sourceline != int(row["authority_line"]):
                raise SystemExit(f"stale authority locator for {entry_id}")
            if len(translated_selected) != 1 or translated_selected[0].sourceline != int(row["translated_line"]):
                raise SystemExit(f"stale translated locator for {entry_id}")
            authority_locator = {
                "file": row["authority_file"],
                "line": int(row["authority_line"]),
                "selector": row["authority_selector"],
                "statement_sha256": row["authority_statement_sha256"],
            }
            translated_locator = {
                "file": row["translated_file"],
                "line": int(row["translated_line"]),
                "selector": row["translated_selector"],
                "statement_sha256": row["translated_statement_sha256"],
            }
        entries.append(
            {
                "id": entry_id,
                "kind": entry_kind,
                "sequence": int(row["sequence"]),
                "title": normalized_text(title_nodes[0]),
                "concepts": str(row["concept_ids"]).split(";"),
                "source_anchor": row["source_anchor_id"],
                "anchor_origin": row["anchor_origin"],
                "source_group": row["source_group"],
                "ordinal_within_group": int(row["ordinal_within_group"]),
                "prompt_kind": row["prompt_kind"],
                "source_context_id": row["source_context_id"] or None,
                "authority_locator": authority_locator,
                "translated_locator": translated_locator,
                "relationship": row["relationship"],
                "surfaces": surfaces,
            }
        )
    expected_counts = {"source_prompt_guide": 39, "mastery_check": 6}
    if dict(counts) != expected_counts:
        raise SystemExit(f"entry coverage mismatch: {dict(counts)}")
    if dict(surface_counts) != {kind: 45 for kind in ("statement", "hint", "answer", "solution")}:
        raise SystemExit(f"entry surface coverage mismatch: {dict(surface_counts)}")

    with terminology_path.open(encoding="utf-8-sig", newline="") as handle:
        all_terms = list(csv.DictReader(handle))
    terms = [row for row in all_terms if row.get("id") in EXPECTED_TERM_IDS]
    if {row.get("id") for row in terms} != EXPECTED_TERM_IDS:
        raise SystemExit("Chapter 6 terminology controls are incomplete")
    with corrections_path.open(encoding="utf-8-sig", newline="") as handle:
        corrections = [
            row
            for row in csv.DictReader(handle)
            if row.get("unit") == "chapter_06_continuous_functions"
        ]
    if {row.get("id") for row in corrections} != EXPECTED_CORRECTION_IDS:
        raise SystemExit("Chapter 6 source-correction controls are incomplete")

    intro_tree = translated_trees["sec_cont_func_intro.ptx"]
    image_assets: list[dict[str, object]] = []
    for stem in IMAGE_STEMS:
        image_nodes = intro_tree.xpath(f"//image[@source='{stem}']")
        if len(image_nodes) != 1 or len(image_nodes[0].findall("description")) != 1:
            raise SystemExit(f"image accessibility mapping is incomplete for {stem}")
        description_node = image_nodes[0].find("description")
        assert description_node is not None
        formats: list[dict[str, object]] = []
        for suffix in ("svg", "pdf"):
            authority_path = authority_assets / f"{stem}.{suffix}"
            repo_path = repo / "assets" / f"{stem}.{suffix}"
            authority_identity = file_identity(authority_path)
            repository_identity = file_identity(repo_path)
            if authority_identity != repository_identity:
                raise SystemExit(f"repository asset differs from authority: {stem}.{suffix}")
            formats.append(
                {
                    "format": suffix,
                    "path": f"repo/assets/{stem}.{suffix}",
                    "authority_path": f"assets/{stem}.{suffix}",
                    **repository_identity,
                }
            )
        image_assets.append(
            {
                "id": f"o003-gvsu-ch06-{stem.lower().replace('_', '-')}",
                "type": "upstream_figure",
                "stem": stem,
                "formats": formats,
                "rights": {
                    "license": "per-component-notices-provenance-pending",
                    "status": "upstream_figure_provenance_pending_final_audit",
                    "not_relicensed": True,
                },
                "accessibility": {
                    "status": "described",
                    "language": "id-ID",
                    "description": normalized_text(description_node),
                    "source_file": "source/sec_cont_func_intro.ptx",
                    "source_line": description_node.sourceline,
                    "source_selector": intro_tree.getpath(description_node),
                },
            }
        )

    authority_intro = authority_trees["sec_cont_func_intro.ptx"]
    translated_exercises = translated_trees["sec_cont_func_exer.ptx"]
    authority_urls = authority_intro.xpath(f"//url[@href='{UPSTREAM_INTERACTIVE}']")
    local_intro_urls = intro_tree.xpath(f"//url[@href='{LOCAL_LAB}']")
    local_exercise_urls = translated_exercises.xpath(f"//url[@href='{LOCAL_LAB}']")
    if len(authority_urls) != 1 or len(local_intro_urls) != 1 or len(local_exercise_urls) != 1:
        raise SystemExit("interactive replacement integration topology changed")
    local_integrations = [
        {
            "file": "source/sec_cont_func_intro.ptx",
            "line": local_intro_urls[0].sourceline,
            "selector": intro_tree.getpath(local_intro_urls[0]),
            "href": local_intro_urls[0].get("href"),
            "visual": local_intro_urls[0].get("visual"),
        },
        {
            "file": "source/sec_cont_func_exer.ptx",
            "line": local_exercise_urls[0].sourceline,
            "selector": translated_exercises.getpath(local_exercise_urls[0]),
            "href": local_exercise_urls[0].get("href"),
            "visual": local_exercise_urls[0].get("visual"),
        },
    ]
    lab_asset = {
        "id": "o003-c90-ch06-epsilon-delta-lab",
        "type": "original_interactive_lab",
        "path": "repo/assets/o003-epsilon-delta-lab.html",
        **file_identity(lab_path),
        "rights": {
            "license": "CC-BY-4.0",
            "attribution": "Original epsilon-delta lab for this Bahasa Indonesia edition",
            "original_expression": True,
            "copies_upstream_geogebra_object": False,
        },
        "accessibility": {
            "language": "id",
            "keyboard_operable_controls": True,
            "live_status": True,
            "svg_accessible_name_and_description": True,
            "tabular_numeric_fallback": True,
            "responsive_layout": True,
        },
        "runtime": {
            "offline_capable": True,
            "network_dependencies": [],
            "external_scripts": [],
            "external_stylesheets": [],
        },
    }

    manifest = {
        "schema_version": "2.0.0",
        "lane_id": "O003-C90",
        "locale": "id-ID",
        "stable_id_namespace": {
            "prefix": "o003-c90-ch06",
            "source_anchor_prefix": "o003-gvsu-ch06",
            "policy": "locale-neutral deterministic IDs; upstream XML IDs retained where present",
        },
        "unit": {
            "id": "o003-c90-ch06-continuous-functions-metric-spaces",
            "sequence": 6,
            "title": "Fungsi Kontinu di Ruang Metrik",
            "prerequisites": [
                "o003-c90-ch03-metric-spaces",
                "o003-c90-ch05-greatest-lower-bound",
            ],
            "concepts": [
                "epsilon_delta_continuity",
                "negation_of_pointwise_continuity",
                "metric_space_continuity",
                "constant_and_identity_functions",
                "composition_of_continuous_functions",
                "algebra_of_continuous_real_functions",
                "discrete_metric_continuity",
                "dense_set_determination",
                "function_space_metrics",
                "integral_functional_continuity",
            ],
        },
        "component": {
            "id": "o003-c90-ch06-companion",
            "type": "self_study_companion",
            "title": "Pendamping Mandiri Bab 6: Fungsi Kontinu pada Ruang Metrik",
            "path": "repo/companion/chapter_06_continuous_functions_self_study.ptx",
            "fragments": [
                {"path": f"repo/companion/{name}", **file_identity(repo / "companion" / name)}
                for name in COMPANION_FRAGMENTS
            ],
            "entry_alias_map": {
                "path": "repo/backend/chapter_06_entry_aliases.csv",
                **file_identity(aliases_path),
            },
            "rights_note": "repo/companion/RIGHTS.md",
            "relationship_to_core": "supplements",
            "original_expression": True,
            "copies_petrunin_expression": False,
            "identity": file_identity(companion_path),
        },
        "authority": {
            "work": "Topology: An Inquiry-Based Approach",
            "author": "Steven Schlicker",
            "edition": "August 2023 institutional work; no numbered-edition claim",
            "publisher_record": "Grand Valley State University ScholarWorks",
            "repository": "https://github.com/gvsuoer/topology",
            "commit": "0c2d8f614ef87aa00de373f3418146c2f1d13bb9",
            "tree": "7df245934eedb7174d5ff8af18afff5a7abdde78",
            "archive_sha256": "d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3",
            "official_record": "https://scholarworks.gvsu.edu/books/30/",
            "controlling_core_license": "CC-BY-NC-SA-3.0",
            "chapter_ordered_sha256": ordered_digest.hexdigest(),
        },
        "translated_unit_source_qa": {
            "path": "repo/qa/CHAPTER06_SOURCE_QA.json",
            "status": source_qa.get("status"),
            "combined_translated_sha256": source_qa.get("combined_translated_sha256"),
            **file_identity(source_qa_path),
        },
        "companion_qa": {
            "path": "repo/qa/CHAPTER06_COMPANION_QA.json",
            "status": companion_qa.get("status"),
            **file_identity(companion_qa_path),
        },
        "control_inputs": {
            "terminology": {
                "path": "00_control/TERMINOLOGY.csv",
                "selected_ids": sorted(EXPECTED_TERM_IDS),
                **file_identity(terminology_path),
            },
            "source_corrections": {
                "path": "00_control/SOURCE_CORRECTIONS.csv",
                "selected_ids": sorted(EXPECTED_CORRECTION_IDS),
                **file_identity(corrections_path),
            },
        },
        "unit_dependencies": dependencies,
        "structural_nodes": structural_nodes,
        "terms": terms,
        "entries": entries,
        "assets": image_assets + [lab_asset],
        "external_dependency_replacement": {
            "relationship": "independent_open_replacement_not_a_copy",
            "upstream_surface": {
                "url": UPSTREAM_INTERACTIVE,
                "archived_in_frozen_source": False,
                "copy_grant_established": False,
                "authority_file": "source/sec_cont_func_intro.ptx",
                "authority_line": authority_urls[0].sourceline,
                "authority_selector": authority_intro.getpath(authority_urls[0]),
            },
            "replacement_asset_id": "o003-c90-ch06-epsilon-delta-lab",
            "replacement_license": "CC-BY-4.0",
            "local_reader_path": LOCAL_LAB,
            "integration_points": local_integrations,
            "ledger_records": ["O003-C062", "O003-C064"],
        },
        "source_corrections": corrections,
        "rights": [
            {
                "component": "upstream_text_and_id_ID_derivative",
                "license": "CC-BY-NC-SA-3.0",
                "attribution": "Steven Schlicker, Grand Valley State University",
                "noncommercial": True,
                "sharealike": True,
                "nonendorsement": True,
            },
            {
                "component": "original_id_ID_self_study_companion",
                "license": "CC-BY-4.0",
                "attribution": "Original companion for this Bahasa Indonesia edition",
                "noncommercial": False,
                "sharealike": False,
            },
            {
                "component": "original_epsilon_delta_lab",
                "license": "CC-BY-4.0",
                "attribution": "Original lab for this Bahasa Indonesia edition",
                "copies_upstream_interactive": False,
            },
            {
                "component": "upstream_figures",
                "license": "per-component-notices-provenance-pending",
                "not_relicensed": True,
            },
            {
                "component": "software_xsl_fonts_and_runtime",
                "license": "per-component-notices",
                "attribution": "Not relicensed by this manifest",
            },
        ],
        "coverage_contract": {
            "source_prompt_guides": 39,
            "activity_or_task_guides": 13,
            "exercise_prompt_guides": 26,
            "mastery_checks": 6,
            "total_entries": 45,
            "statements": surface_counts["statement"],
            "hints": surface_counts["hint"],
            "answers": surface_counts["answer"],
            "solutions": surface_counts["solution"],
            "all_entries_have_statement_hint_answer_solution": True,
            "active_images_with_id_ID_descriptions": len(image_assets),
            "original_offline_interactive_replacements": 1,
            "local_interactive_integration_points": len(local_integrations),
            "source_correction_records": len(corrections),
            "answer_reveal_policy": "delayed_or_collapsible_in_reader",
        },
    }
    output_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "aliases": {"path": str(aliases_path), **file_identity(aliases_path)},
                "output": {"path": str(output_path), **file_identity(output_path)},
                "entries": dict(counts),
                "surfaces": dict(surface_counts),
                "assets": len(image_assets) + 1,
                "source_corrections": len(corrections),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
