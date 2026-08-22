#!/usr/bin/env python3
"""Build the fail-closed cumulative Chapters 1-4 source manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
OUTPUT = ROOT / "qa" / "CHAPTER04_SOURCE_MANIFEST.json"

CHAPTER_04 = [
    "chap_metric_spaces_apps.ptx",
    "sec_met_space_app.ptx",
    "sec_hamming.ptx",
    "sec_levenshtein.ptx",
]

NEW_ADDITIVE = [
    "companion/chapter_04_metric_space_applications_self_study.ptx",
    "backend/chapter_04_entry_aliases.csv",
    "backend/chapter_04_companion_manifest.json",
    "source/chapters_01_04_reader.ptx",
]

IMPLEMENTATION = [
    "scripts/qa_source_translation.py",
    "scripts/qa_chapter04_companion.py",
    "scripts/build_chapter04_backend.py",
    "scripts/build_chapter04_source_manifest.py",
    "scripts/build_pretext_pdf_strict.py",
    "assets/o003-readable-layout.css",
    "xsl/custom-latex.xsl",
    "project.ptx",
]

# These cumulative build surfaces legitimately evolve at each reader boundary.
# Preserve the prior identity as evidence, but bind the new boundary to the
# current bytes in ``production_implementation`` rather than treating an
# intentional layout/target update as drift in admitted mathematical content.
EVOLVING_IMPLEMENTATION = {
    "assets/o003-readable-layout.css",
    "xsl/custom-latex.xsl",
    "project.ptx",
}

CONTROL_INPUTS = [
    "00_control/TERMINOLOGY.csv",
    "00_control/SOURCE_CORRECTIONS.csv",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_row(relative: str, prefix: str = "repo/") -> dict[str, object]:
    path = ROOT / relative
    if not path.is_file():
        raise FileNotFoundError(path)
    return {
        "path": f"{prefix}{relative}",
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def control_row(relative: str) -> dict[str, object]:
    path = LANE / relative
    if not path.is_file():
        raise FileNotFoundError(path)
    return {
        "path": relative,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def combined_source(names: list[str]) -> str:
    digest = hashlib.sha256()
    for name in names:
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update((ROOT / "source" / name).read_bytes())
    return digest.hexdigest()


def read_json(relative: str) -> dict[str, object]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def repo_relative(path: object) -> str:
    value = str(path)
    if not value.startswith("repo/"):
        raise RuntimeError(f"manifest path is not repo-relative: {value}")
    return value.removeprefix("repo/")


def main() -> int:
    prior = read_json("qa/CHAPTER03_SOURCE_MANIFEST.json")
    source_qa = read_json("qa/CHAPTER04_SOURCE_QA.json")
    companion_qa = read_json("qa/CHAPTER04_COMPANION_QA.json")
    html_qa = read_json("qa/CHAPTER04_HTML_QA.json")
    browser_qa = read_json("qa/CHAPTER04_BROWSER_QA.json")
    pdf_qa = read_json("qa/CHAPTER04_PDF_VISUAL_QA.json")
    backend = read_json("backend/chapter_04_companion_manifest.json")

    for label, report in (
        ("prior Chapters 1-3 source manifest", prior),
        ("Chapter 4 source", source_qa),
        ("Chapter 4 companion", companion_qa),
        ("HTML", html_qa),
        ("browser", browser_qa),
        ("PDF", pdf_qa),
    ):
        if report.get("status") != "pass":
            raise RuntimeError(f"{label} QA is not passing")

    chapters: dict[str, list[str]] = {}
    inherited_source: dict[str, dict[str, object]] = {}
    for chapter in ("chapter_01", "chapter_02", "chapter_03"):
        prior_chapter = prior["translated_source"][chapter]
        names = [repo_relative(row["path"]).removeprefix("source/") for row in prior_chapter["files"]]
        chapters[chapter] = names
        current_rows = [file_row(f"source/{name}") for name in names]
        for old, current in zip(prior_chapter["files"], current_rows, strict=True):
            if old["sha256"] != current["sha256"] or old["bytes"] != current["bytes"]:
                raise RuntimeError(f"previously admitted source drifted: {current['path']}")
        inherited_source[chapter] = {
            "files": current_rows,
            "combined_sha256": combined_source(names),
            "admission": "identity preserved from repo/qa/CHAPTER03_SOURCE_MANIFEST.json",
        }
        if inherited_source[chapter]["combined_sha256"] != prior_chapter["combined_sha256"]:
            raise RuntimeError(f"previously admitted combined source identity drifted: {chapter}")

    chapters["chapter_04"] = CHAPTER_04
    chapter_04_rows = [file_row(f"source/{name}") for name in CHAPTER_04]
    source_qa_hashes = {
        str(row["file"]): str(row["translated"]["sha256"])
        for row in source_qa["files"]
    }
    for name, row in zip(CHAPTER_04, chapter_04_rows, strict=True):
        if source_qa_hashes.get(name) != row["sha256"]:
            raise RuntimeError(f"Chapter 4 source QA hash is stale for {name}")
    chapter_04_combined = combined_source(CHAPTER_04)
    if chapter_04_combined != source_qa["combined_translated_sha256"]:
        raise RuntimeError("Chapter 4 combined source hash disagrees with source QA")

    companion_row = file_row("companion/chapter_04_metric_space_applications_self_study.ptx")
    if companion_qa["companion"]["sha256"] != companion_row["sha256"]:
        raise RuntimeError("Chapter 4 companion QA is stale")
    if backend["component"]["identity"]["sha256"] != companion_row["sha256"]:
        raise RuntimeError("Chapter 4 backend is stale relative to its companion")
    alias_row = file_row("backend/chapter_04_entry_aliases.csv")
    if companion_qa["aliases"]["sha256"] != alias_row["sha256"]:
        raise RuntimeError("Chapter 4 companion QA is stale relative to its aliases")

    current_controls = {row["path"]: row for row in (control_row(relative) for relative in CONTROL_INPUTS)}
    backend_controls = backend.get("control_inputs", {})
    for key, relative in (
        ("terminology", "00_control/TERMINOLOGY.csv"),
        ("source_corrections", "00_control/SOURCE_CORRECTIONS.csv"),
    ):
        if backend_controls.get(key, {}).get("sha256") != current_controls[relative]["sha256"]:
            raise RuntimeError(f"Chapter 4 backend is stale relative to {relative}")

    inherited_additive: list[dict[str, object]] = []
    inherited_implementation_updates: list[dict[str, object]] = []
    for row in prior["additive_components"]:
        relative = repo_relative(row["path"])
        if relative in EVOLVING_IMPLEMENTATION:
            inherited_implementation_updates.append({
                "path": row["path"],
                "previous_bytes": row["bytes"],
                "previous_sha256": row["sha256"],
                "current": file_row(relative),
                "reason": "intentional cumulative reader implementation update",
            })
            continue
        current = file_row(relative)
        if row["sha256"] != current["sha256"] or row["bytes"] != current["bytes"]:
            raise RuntimeError(f"previously admitted additive component drifted: {relative}")
        inherited_additive.append(current)

    pdf_path = ROOT / "output" / "chapters01-04-pdf" / "chapters_01_04_reader.pdf"
    if sha256(pdf_path) != pdf_qa["sha256"]:
        raise RuntimeError("PDF QA hash is stale")

    ordered_names = [name for chapter in ("chapter_01", "chapter_02", "chapter_03", "chapter_04") for name in chapters[chapter]]
    translated_source = dict(inherited_source)
    translated_source["chapter_04"] = {
        "files": chapter_04_rows,
        "combined_sha256": chapter_04_combined,
        "source_qa": "repo/qa/CHAPTER04_SOURCE_QA.json",
        "xml_ids": source_qa["xml_ids"],
        "xrefs": source_qa["xrefs"],
        "exercises": sum(int(row["exercises"]) for row in source_qa["files"]),
        "tasks": sum(int(row["tasks"]) for row in source_qa["files"]),
        "activities_and_explorations": sum(
            int(row["activities_and_explorations"]) for row in source_qa["files"]
        ),
    }
    translated_source["cumulative_combined_sha256"] = combined_source(ordered_names)
    translated_source["combined_algorithm"] = (
        "SHA-256 over each ordered source filename, one NUL byte, then exact file bytes"
    )

    implementation_rows: list[dict[str, object]] = []
    seen_implementation: set[str] = set()
    for relative in IMPLEMENTATION:
        if relative not in seen_implementation:
            implementation_rows.append(file_row(relative))
            seen_implementation.add(relative)

    manifest = {
        "schema_version": 1,
        "lane": "O003/C90",
        "locale": "id-ID",
        "boundary": "chapters_01_04_with_separately_licensed_self_study_companions",
        "status": "pass",
        "authority": {
            "work": "Topology: An Inquiry-Based Approach",
            "author": "Steven Schlicker",
            "official_record": "https://scholarworks.gvsu.edu/books/30/",
            "repository": "https://github.com/gvsuoer/topology",
            "commit": "0c2d8f614ef87aa00de373f3418146c2f1d13bb9",
            "tree": "7df245934eedb7174d5ff8af18afff5a7abdde78",
            "archive_sha256": "d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3",
            "controlling_core_license": "CC-BY-NC-SA-3.0",
        },
        "translated_source": translated_source,
        "additive_components": inherited_additive + [file_row(relative) for relative in NEW_ADDITIVE],
        "control_inputs": [current_controls[relative] for relative in CONTROL_INPUTS],
        "production_implementation": implementation_rows,
        "inherited_implementation_updates": inherited_implementation_updates,
        "companion_coverage": backend["coverage_contract"],
        "rights": {
            "translated_gvsu_spine": "CC-BY-NC-SA-3.0 (conservative determination)",
            "original_self_study_companions": "CC-BY-4.0",
            "collection_policy": "per-component rights; no flattened license",
            "rights_note": "repo/companion/RIGHTS.md",
            "non_endorsement": True,
        },
        "reader_artifacts": {
            "html": {
                "path": "repo/output/chapters01-04-html",
                "file_count": html_qa["file_count"],
                "html_files": html_qa["html_files"],
                "bytes": html_qa["total_bytes"],
                "canonical_manifest_sha256": html_qa["canonical_manifest_sha256"],
                "manifest_file_sha256": sha256(ROOT / "qa" / "CHAPTER04_HTML_MANIFEST.json"),
                "qa": "repo/qa/CHAPTER04_HTML_QA.json",
                "browser_qa": "repo/qa/CHAPTER04_BROWSER_QA.json",
                "offline_closed": False,
            },
            "pdf": {
                "path": "repo/output/chapters01-04-pdf/chapters_01_04_reader.pdf",
                "bytes": pdf_path.stat().st_size,
                "pages": pdf_qa["pages"],
                "sha256": pdf_qa["sha256"],
                "tagged": pdf_qa["tagged"],
                "visual_qa": "repo/qa/CHAPTER04_PDF_VISUAL_QA.json",
            },
        },
        "qa_receipts": {
            "companion": "repo/qa/CHAPTER04_COMPANION_QA.json",
            "source": "repo/qa/CHAPTER04_SOURCE_QA.json",
            "html": "repo/qa/CHAPTER04_HTML_QA.json",
            "browser": "repo/qa/CHAPTER04_BROWSER_QA.json",
            "pdf": "repo/qa/CHAPTER04_PDF_VISUAL_QA.json",
        },
        "known_caveats": [
            "HTML still uses remote PreTeXt, Runestone, MathJax, font, CSS, and JavaScript dependencies.",
            "PDF is not tagged; HTML remains the primary accessible surface.",
            "Whole-book figure provenance and offline closure remain release gates.",
        ],
    }

    payload = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(payload, encoding="utf-8", newline="\n")
    print(json.dumps({
        "status": "pass",
        "output": str(OUTPUT),
        "bytes": OUTPUT.stat().st_size,
        "sha256": sha256(OUTPUT),
        "chapter_04_combined_sha256": chapter_04_combined,
        "cumulative_combined_sha256": translated_source["cumulative_combined_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
