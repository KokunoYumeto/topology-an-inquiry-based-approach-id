#!/usr/bin/env python3
"""Build the fail-closed cumulative Chapter 1-2 source manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "qa" / "CHAPTER02_SOURCE_MANIFEST.json"

CHAPTER_01 = [
    "chap_sets.ptx",
    "sec_sets_intro.ptx",
    "sec_basic_top.ptx",
    "sec_intervals.ptx",
    "sec_union_int_comp.ptx",
    "sec_cart_prod.ptx",
    "sec_sets_summ.ptx",
    "sec_sets_exer.ptx",
]
CHAPTER_02 = [
    "chap_functions.ptx",
    "sec_func_intro.ptx",
    "sec_comp_func.ptx",
    "sec_inv_func.ptx",
    "sec_fun_set.ptx",
    "sec_card_set.ptx",
    "sec_func_summ.ptx",
    "sec_func_exer.ptx",
]
ADDITIVE = [
    "companion/chapter_01_sets_self_study.ptx",
    "backend/chapter_01_entry_aliases.csv",
    "backend/chapter_01_companion_manifest.json",
    "companion/chapter_02_functions_self_study.ptx",
    "backend/chapter_02_entry_aliases.csv",
    "backend/chapter_02_companion_manifest.json",
    "companion/RIGHTS.md",
    "source/chapters_01_02_reader.ptx",
    "assets/o003-readable-layout.css",
    "xsl/custom-latex.xsl",
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


def combined_source(names: list[str]) -> str:
    digest = hashlib.sha256()
    for name in names:
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update((ROOT / "source" / name).read_bytes())
    return digest.hexdigest()


def read_json(relative: str) -> dict[str, object]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def main() -> int:
    source_qa = read_json("qa/CHAPTER02_SOURCE_QA.json")
    html_qa = read_json("qa/CHAPTER02_HTML_QA.json")
    browser_qa = read_json("qa/CHAPTER02_BROWSER_QA.json")
    pdf_qa = read_json("qa/CHAPTER02_PDF_VISUAL_QA.json")
    backend = read_json("backend/chapter_02_companion_manifest.json")

    for label, report in (
        ("Chapter 2 source", source_qa),
        ("HTML", html_qa),
        ("browser", browser_qa),
        ("PDF", pdf_qa),
    ):
        if report.get("status") != "pass":
            raise RuntimeError(f"{label} QA is not passing")

    source_rows_01 = [file_row(f"source/{name}") for name in CHAPTER_01]
    source_rows_02 = [file_row(f"source/{name}") for name in CHAPTER_02]
    source_qa_rows = {
        str(row["file"]): str(row["translated"]["sha256"])
        for row in source_qa["files"]
    }
    for name, row in zip(CHAPTER_02, source_rows_02, strict=True):
        if source_qa_rows.get(name) != row["sha256"]:
            raise RuntimeError(f"Chapter 2 source QA hash is stale for {name}")

    chapter_02_combined = combined_source(CHAPTER_02)
    if chapter_02_combined != source_qa["combined_translated_sha256"]:
        raise RuntimeError("Chapter 2 combined source hash disagrees with source QA")

    companion_row = file_row("companion/chapter_02_functions_self_study.ptx")
    if backend["component"]["identity"]["sha256"] != companion_row["sha256"]:
        raise RuntimeError("Chapter 2 backend is stale relative to its companion")

    pdf_path = ROOT / "output" / "chapters01-02-pdf" / "chapters_01_02_reader.pdf"
    if sha256(pdf_path) != pdf_qa["sha256"]:
        raise RuntimeError("PDF QA hash is stale")

    manifest = {
        "schema_version": 1,
        "lane": "O003/C90",
        "locale": "id-ID",
        "boundary": "chapters_01_02_with_separately_licensed_self_study_companions",
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
        "translated_source": {
            "chapter_01": {
                "files": source_rows_01,
                "combined_sha256": combined_source(CHAPTER_01),
                "structural_qa": "qa/CHAPTER01_SOURCE_MANIFEST.json (historical exact admission; superseded here after terminology-only normalization)",
            },
            "chapter_02": {
                "files": source_rows_02,
                "combined_sha256": chapter_02_combined,
                "source_qa": "repo/qa/CHAPTER02_SOURCE_QA.json",
                "xml_ids": source_qa["xml_ids"],
                "xrefs": source_qa["xrefs"],
                "exercises": sum(int(row["exercises"]) for row in source_qa["files"]),
                "tasks": sum(int(row["tasks"]) for row in source_qa["files"]),
                "activities_and_explorations": sum(
                    int(row["activities_and_explorations"]) for row in source_qa["files"]
                ),
            },
            "cumulative_combined_sha256": combined_source(CHAPTER_01 + CHAPTER_02),
            "combined_algorithm": "SHA-256 over each ordered source filename, one NUL byte, then exact file bytes",
        },
        "additive_components": [file_row(relative) for relative in ADDITIVE],
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
                "path": "repo/output/chapters01-02-html",
                "file_count": html_qa["file_count"],
                "html_files": html_qa["html_files"],
                "bytes": html_qa["total_bytes"],
                "canonical_manifest_sha256": html_qa["canonical_manifest_sha256"],
                "manifest_file_sha256": sha256(ROOT / "qa" / "CHAPTER02_HTML_MANIFEST.json"),
                "qa": "repo/qa/CHAPTER02_HTML_QA.json",
                "browser_qa": "repo/qa/CHAPTER02_BROWSER_QA.json",
                "offline_closed": False,
            },
            "pdf": {
                "path": "repo/output/chapters01-02-pdf/chapters_01_02_reader.pdf",
                "bytes": pdf_path.stat().st_size,
                "pages": pdf_qa["pages"],
                "sha256": pdf_qa["sha256"],
                "tagged": pdf_qa["tagged"],
                "visual_qa": "repo/qa/CHAPTER02_PDF_VISUAL_QA.json",
            },
        },
        "qa_receipts": {
            "companion": "repo/qa/CHAPTER02_COMPANION_AUDIT.md",
            "source": "repo/qa/CHAPTER02_SOURCE_QA.json",
            "html": "repo/qa/CHAPTER02_HTML_QA.json",
            "browser": "repo/qa/CHAPTER02_BROWSER_QA.json",
            "pdf": "repo/qa/CHAPTER02_PDF_VISUAL_QA.json",
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
        "chapter_01_combined_sha256": manifest["translated_source"]["chapter_01"]["combined_sha256"],
        "chapter_02_combined_sha256": chapter_02_combined,
        "cumulative_combined_sha256": manifest["translated_source"]["cumulative_combined_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
