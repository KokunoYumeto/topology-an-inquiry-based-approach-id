#!/usr/bin/env python3
"""Generate and fail-closed validate the Chapter 9 modular backend."""

from __future__ import annotations

from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import sys

from lxml import etree

from qa_chapter09_companion import (
    EXPECTED_AUTHORITY_ORDERED_SHA256,
    EXPECTED_CORRECTION_IDS,
    EXPECTED_SOURCE_PROMPTS,
    EXPECTED_TERM_IDS,
    FILE_GROUPS,
    FRAGMENTS,
    IMAGE_USES,
    SOURCE_FILES,
    XML_ID,
    element_sha256,
    expected_source_entry_ids,
    identity,
    local_name,
    nearest_context_id,
    normalized_text,
    prompt_nodes,
    source_prompt_mappings,
)


SOURCE_ROLES = {
    "chap_sequences.ptx": "chapter_container",
    "sec_seq_intro.ptx": "sequences_and_limits_in_metric_spaces",
    "sec_seq_cont_metric.ptx": "sequential_characterization_of_continuity",
    "sec_seq_summ.ptx": "chapter_summary",
    "sec_seq_exer.ptx": "chapter_exercises",
}
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
CONCEPTS_BY_GROUP: dict[str, tuple[tuple[str, ...], ...]] = {
    "sequence-intro": (
        ("epsilon_N_definition", "reciprocal_sequence", "euclidean_metric"),
        ("coordinate_sequence", "taxicab_metric", "limit_proof"),
        ("discrete_metric", "eventually_constant", "divergence"),
    ),
    "sequence-continuity": (
        ("uniqueness_of_limit", "epsilon_half", "eventual_bound"),
        ("uniqueness_of_limit", "second_eventual_bound"),
        ("maximum_of_indices", "simultaneous_eventual_bounds"),
        ("triangle_inequality", "uniqueness_of_limit"),
        ("sequential_continuity", "contrapositive", "negated_continuity"),
        ("archimedean_property", "reciprocal_radius"),
        ("witness_sequence", "failure_of_continuity"),
        ("convergence_to_base_point", "shrinking_balls"),
        ("image_sequence", "sequential_discontinuity"),
        ("oscillatory_function", "graphical_intuition", "limit"),
        ("sine_extrema", "input_sequence"),
        ("counterexample_sequence", "convergence_to_zero"),
        ("sequential_criterion", "discontinuity_at_zero"),
    ),
    "exercise": (
        ("epsilon_N_definition", "reciprocal_sequence", "euclidean_metric"),
        ("coordinate_sequence", "maximum_metric", "divergence"),
        ("function_sequence", "supremum_metric", "uniform_convergence"),
        ("supremum", "approximating_sequence"),
        ("infimum", "approximating_sequence"),
        ("extremum_membership", "counterexample"),
        ("point_to_set_distance", "open_ball", "infimum"),
        ("point_to_set_distance", "approximating_sequence", "construction"),
        ("subspace_metric", "ambient_convergence", "same_limit"),
        ("ambient_limit_outside_subspace", "cauchy_property", "rational_sequence"),
        ("limit_laws", "scalar_multiple"),
        ("limit_laws", "sum"),
        ("convergent_sequence", "boundedness"),
        ("limit_laws", "product", "boundedness"),
        ("limit_laws", "quotient", "nonzero_denominator"),
        ("sequential_continuity", "product_of_functions"),
        ("continuity", "quotient_of_functions", "epsilon_delta_proof"),
        ("coordinatewise_convergence", "euclidean_metric"),
        ("rational_irrational_function", "continuity_at_zero"),
        ("prescribed_continuity_set", "finite_set"),
        ("geometric_sequence", "epsilon_N_definition"),
        ("pointwise_convergence", "uniform_metric", "discontinuous_limit"),
        ("L1_metric", "function_sequence", "continuous_limit_candidate"),
        ("monotone_sequence", "boundedness", "infimum"),
        ("closure", "sequence_characterization", "metric_space"),
        ("supremum_infimum", "order_bounds"),
        ("rational_metric", "false_convergence_claim"),
        ("discrete_metric", "eventually_constant", "convergence_characterization"),
    ),
    "mastery": (
        ("epsilon_N_definition", "explicit_index_bound"),
        ("uniqueness_of_limit", "triangle_inequality"),
        ("metric_dependence", "discrete_metric", "eventually_constant"),
        ("sequential_continuity", "counterexample_sequence"),
        ("subspace_metric", "ambient_limit_outside_subspace"),
        ("pointwise_convergence", "uniform_convergence", "function_sequence"),
    ),
}


def file_identity(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def mastery_entry_ids() -> list[str]:
    return [f"o003-c90-ch09-mastery-{ordinal:02d}" for ordinal in range(1, 7)]


def concepts_for(group: str, ordinal: int) -> list[str]:
    rows = CONCEPTS_BY_GROUP.get(group)
    if rows is None or ordinal < 1 or ordinal > len(rows):
        raise SystemExit(f"missing concept mapping for {group}:{ordinal}")
    base = ["metric_space", "sequences_in_metric_spaces"]
    return base + list(rows[ordinal - 1])


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
    companion_path = repo / "companion/chapter_09_sequences_self_study.ptx"
    aliases_path = repo / "backend/chapter_09_entry_aliases.csv"
    output_path = repo / "backend/chapter_09_companion_manifest.json"
    terminology_path = lane / "00_control/TERMINOLOGY.csv"
    corrections_path = lane / "00_control/SOURCE_CORRECTIONS.csv"
    source_qa_path = repo / "qa/CHAPTER09_SOURCE_QA.json"
    companion_qa_path = repo / "qa/CHAPTER09_COMPANION_QA.json"
    parser = etree.XMLParser(resolve_entities=False, no_network=True)

    required = [
        companion_path,
        source_qa_path,
        companion_qa_path,
        terminology_path,
        corrections_path,
        *(repo / "companion" / name for name in FRAGMENTS),
        *(repo / "source" / name for name in SOURCE_FILES),
        *(authority_root / name for name in SOURCE_FILES),
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"missing Chapter 9 backend inputs: {missing}")

    source_qa = json.loads(source_qa_path.read_text(encoding="utf-8"))
    companion_qa = json.loads(companion_qa_path.read_text(encoding="utf-8"))
    if source_qa.get("status") != "pass":
        raise SystemExit("Chapter 9 source QA is not passing")
    if companion_qa.get("status") != "pass":
        raise SystemExit("Chapter 9 companion QA is not passing")
    if companion_qa.get("companion", {}).get("sha256") != file_identity(companion_path)["sha256"]:
        raise SystemExit("Chapter 9 companion QA is stale")
    fragment_hashes = {
        Path(item["path"]).name: item["sha256"]
        for item in companion_qa.get("fragments", [])
    }
    for name in FRAGMENTS:
        if fragment_hashes.get(name) != file_identity(repo / "companion" / name)["sha256"]:
            raise SystemExit(f"Chapter 9 companion QA fragment identity is stale: {name}")

    ordered_digest = hashlib.sha256()
    for name in SOURCE_FILES:
        ordered_digest.update(name.encode("utf-8"))
        ordered_digest.update(b"\0")
        ordered_digest.update((authority_root / name).read_bytes())
    if ordered_digest.hexdigest() != EXPECTED_AUTHORITY_ORDERED_SHA256:
        raise SystemExit("frozen Chapter 9 authority closure identity changed")

    companion_tree = etree.parse(str(companion_path), parser)
    companion_tree.xinclude()
    companion_root = companion_tree.getroot()
    if companion_root.get(XML_ID) != "o003-c90-ch09-companion":
        raise SystemExit("unexpected Chapter 9 companion root ID")
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
    for order, name in enumerate(SOURCE_FILES):
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
                "role": SOURCE_ROLES[name],
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
                    or f"o003-gvsu-ch09-{Path(name).stem}-{tag}-{ordinal_by_tag[tag]:02d}",
                    "id_origin": "upstream_xml_id" if xml_id else "assigned_locale_neutral",
                    "source_xml_id": xml_id,
                    "kind": tag,
                    "file": f"source/{name}",
                    "ordinal_within_file_and_kind": ordinal_by_tag[tag],
                    "translated_line": node.sourceline,
                    "translated_selector": translated_tree.getpath(node),
                }
            )

    mapping_failures: list[str] = []
    qa_mappings, prompt_counts = source_prompt_mappings(
        repo, authority_root, parser, mapping_failures
    )
    if mapping_failures:
        raise SystemExit(f"Chapter 9 prompt mapping failed: {mapping_failures}")
    if len(qa_mappings) != EXPECTED_SOURCE_PROMPTS:
        raise SystemExit("expected exactly 44 ordered Chapter 9 source prompt mappings")
    source_ids = expected_source_entry_ids()
    if [row["companion_entry_id"] for row in qa_mappings] != source_ids:
        raise SystemExit("Chapter 9 source prompt mapping IDs changed")
    if companion_qa.get("source_prompt_mappings") != qa_mappings:
        raise SystemExit("Chapter 9 companion QA prompt mappings are stale")

    alias_rows: list[dict[str, object]] = []
    for sequence, prompt in enumerate(qa_mappings, start=1):
        group = str(prompt["group"])
        ordinal = int(prompt["ordinal_within_group"])
        alias_rows.append(
            {
                "companion_entry_id": prompt["companion_entry_id"],
                "entry_kind": "source_prompt_guide",
                "sequence": sequence,
                "source_anchor_id": prompt["source_anchor_id"],
                "anchor_origin": "assigned_locale_neutral",
                "source_group": group,
                "ordinal_within_group": ordinal,
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
                "concept_ids": ";".join(concepts_for(group, ordinal)),
            }
        )
    for ordinal, mastery_id in enumerate(mastery_entry_ids(), start=1):
        alias_rows.append(
            {
                "companion_entry_id": mastery_id,
                "entry_kind": "mastery_check",
                "sequence": len(source_ids) + ordinal,
                "source_anchor_id": f"o003-c90-ch09-original-mastery-{ordinal:02d}",
                "anchor_origin": "original",
                "source_group": "mastery",
                "ordinal_within_group": ordinal,
                "prompt_kind": "original_mastery_exercise",
                "source_context_id": "o003-c90-ch09-mastery",
                "authority_file": "",
                "authority_line": "",
                "authority_selector": "",
                "authority_statement_sha256": "",
                "translated_file": "",
                "translated_line": "",
                "translated_selector": "",
                "translated_statement_sha256": "",
                "relationship": "original_transfer_and_mastery_check",
                "concept_ids": ";".join(concepts_for("mastery", ordinal)),
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
        current_id = str(row["companion_entry_id"])
        exercise = companion_by_id.get(current_id)
        if exercise is None or local_name(exercise) != "exercise":
            raise SystemExit(f"alias entry does not resolve: {current_id}")
        titles = exercise.findall("title")
        if len(titles) != 1:
            raise SystemExit(f"{current_id} does not have exactly one title")
        surfaces: dict[str, dict[str, object]] = {}
        for kind in ("statement", "hint", "answer", "solution"):
            children = exercise.findall(kind)
            if len(children) != 1:
                raise SystemExit(f"{current_id} has invalid {kind} surface count")
            child = children[0]
            expected_surface_id = f"{current_id}-{kind}"
            xml_id = child.get(XML_ID)
            if kind != "statement" and xml_id != expected_surface_id:
                raise SystemExit(f"{current_id} has invalid {kind} reveal ID")
            if kind == "statement" and xml_id not in {None, expected_surface_id}:
                raise SystemExit(f"{current_id} has conflicting statement ID")
            surfaces[kind] = {
                "id": expected_surface_id,
                "id_origin": "xml_id" if xml_id == expected_surface_id else "assigned_backend_alias",
                "xml_id": xml_id,
                "companion_selector": companion_tree.getpath(child),
                "text_sha256": hashlib.sha256(
                    normalized_text(child).encode("utf-8")
                ).hexdigest(),
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
                raise SystemExit(f"stale authority locator for {current_id}")
            if len(translated_selected) != 1 or translated_selected[0].sourceline != int(row["translated_line"]):
                raise SystemExit(f"stale translated locator for {current_id}")
            if element_sha256(authority_selected[0]) != row["authority_statement_sha256"]:
                raise SystemExit(f"stale authority statement identity for {current_id}")
            if element_sha256(translated_selected[0]) != row["translated_statement_sha256"]:
                raise SystemExit(f"stale translated statement identity for {current_id}")
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
                "id": current_id,
                "kind": entry_kind,
                "sequence": int(row["sequence"]),
                "title": normalized_text(titles[0]),
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
    if dict(counts) != {"source_prompt_guide": 44, "mastery_check": 6}:
        raise SystemExit(f"entry coverage mismatch: {dict(counts)}")
    expected_surfaces = {kind: 50 for kind in ("statement", "hint", "answer", "solution")}
    if dict(surface_counts) != expected_surfaces:
        raise SystemExit(f"entry surface coverage mismatch: {dict(surface_counts)}")

    with terminology_path.open(encoding="utf-8-sig", newline="") as handle:
        terms = sorted(
            (row for row in csv.DictReader(handle) if row.get("id") in EXPECTED_TERM_IDS),
            key=lambda row: str(row.get("id")),
        )
    if {row.get("id") for row in terms} != EXPECTED_TERM_IDS:
        raise SystemExit("Chapter 9 terminology controls are incomplete")
    with corrections_path.open(encoding="utf-8-sig", newline="") as handle:
        corrections = sorted(
            (
                row for row in csv.DictReader(handle)
                if row.get("unit") == "chapter_09_sequences"
            ),
            key=lambda row: str(row.get("id")),
        )
    if {row.get("id") for row in corrections} != EXPECTED_CORRECTION_IDS:
        raise SystemExit("Chapter 9 source-correction controls are incomplete")

    image_assets: list[dict[str, object]] = []
    for stem, source_name in IMAGE_USES.items():
        tree = translated_trees[source_name]
        images = tree.xpath(f"//image[@source='{stem}']")
        if len(images) != 1 or len(images[0].findall("description")) != 1:
            raise SystemExit(f"image accessibility mapping is incomplete for {stem}")
        description = images[0].find("description")
        assert description is not None
        formats: list[dict[str, object]] = []
        for suffix in ("svg", "pdf"):
            authority_path = authority_assets / f"{stem}.{suffix}"
            repository_path = repo / "assets" / f"{stem}.{suffix}"
            authority_identity = file_identity(authority_path)
            repository_identity = file_identity(repository_path)
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
                "id": f"o003-gvsu-ch09-{stem.lower().replace('_', '-')}",
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
                    "description": normalized_text(description),
                    "source_file": f"source/{source_name}",
                    "source_line": description.sourceline,
                    "source_selector": tree.getpath(description),
                },
            }
        )

    manifest = {
        "schema_version": "2.0.0",
        "lane_id": "O003-C90",
        "locale": "id-ID",
        "stable_id_namespace": {
            "prefix": "o003-c90-ch09",
            "source_anchor_prefix": "o003-gvsu-ch09",
            "policy": "locale-neutral deterministic IDs; upstream XML IDs retained where present",
        },
        "unit": {
            "id": "o003-c90-ch09-sequences-metric-spaces",
            "sequence": 9,
            "title": "Barisan dalam Ruang Metrik",
            "prerequisites": [
                "o003-c90-ch03-metric-spaces",
                "o003-c90-ch06-continuous-functions-metric-spaces",
            ],
            "concepts": [
                "sequences_in_metric_spaces",
                "epsilon_N_definition",
                "uniqueness_of_limit",
                "sequential_continuity",
                "subspace_and_ambient_convergence",
                "coordinatewise_convergence",
                "pointwise_and_uniform_convergence",
                "eventually_constant_sequences",
            ],
        },
        "component": {
            "id": "o003-c90-ch09-companion",
            "type": "self_study_companion",
            "title": "Pendamping Mandiri Bab 9: Barisan dalam Ruang Metrik",
            "path": "repo/companion/chapter_09_sequences_self_study.ptx",
            "fragments": [
                {"path": f"repo/companion/{name}", **file_identity(repo / "companion" / name)}
                for name in FRAGMENTS
            ],
            "entry_alias_map": {
                "path": "repo/backend/chapter_09_entry_aliases.csv",
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
            "path": "repo/qa/CHAPTER09_SOURCE_QA.json",
            "status": source_qa.get("status"),
            "combined_translated_sha256": source_qa.get("combined_translated_sha256"),
            **file_identity(source_qa_path),
        },
        "companion_qa": {
            "path": "repo/qa/CHAPTER09_COMPANION_QA.json",
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
        "assets": image_assets,
        "external_dependency_surface": {
            "authority_remote_or_interactive_nodes": 0,
            "translated_remote_or_interactive_nodes": 0,
            "local_replacement_required": False,
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
            "source_prompt_guides": 44,
            "activity_or_task_guides": 16,
            "exercise_prompt_guides": 28,
            "mastery_checks": 6,
            "total_entries": 50,
            "statements": surface_counts["statement"],
            "hints": surface_counts["hint"],
            "answers": surface_counts["answer"],
            "solutions": surface_counts["solution"],
            "all_entries_have_statement_hint_answer_solution": True,
            "active_images_with_id_ID_descriptions": len(image_assets),
            "remote_or_interactive_surfaces": 0,
            "source_correction_records": len(corrections),
            "answer_reveal_policy": "delayed_or_collapsible_in_reader",
            "source_prompt_counts": prompt_counts,
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
                "assets": len(image_assets),
                "source_corrections": len(corrections),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
