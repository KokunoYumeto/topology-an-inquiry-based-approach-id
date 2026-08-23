#!/usr/bin/env python3
"""Build a deterministic, privacy-sanitized Chapter 12 Zenodo checkpoint.

The reader remains the verified Chapters 1-11 PDF/HTML boundary.  The source
archive is advanced with the translated Chapter 12 closure and the partial
41-of-78 companion/backend checkpoint; no completion claim is made.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import zipfile

from build_zenodo_chapter11_package import (
    assert_pdf_privacy,
    assert_sanitized,
    deterministic_zip,
    digest,
    identity,
)


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
OLD = ROOT / "publication" / "zenodo_chapters01_11_package"
OUT = ROOT / "publication" / "zenodo_chapter12_partial_package"
BASE = "topologi-pendekatan-berbasis-inkuiri-bab-01-11"
PDF_NAME = f"{BASE}-id.pdf"
HTML_NAME = f"{BASE}-html.zip"
SOURCE_NAME = f"{BASE}-sumber.zip"
LICENSES_NAME = f"{BASE}-licenses.md"
RIGHTS_NAME = f"{BASE}-rights-companion.md"
MANIFEST_NAME = f"{BASE}-manifest.json"
CHECKSUMS_NAME = f"{BASE}-checksums.sha256"

OLD_FILES = {
    PDF_NAME,
    HTML_NAME,
    SOURCE_NAME,
    LICENSES_NAME,
    RIGHTS_NAME,
    f"{BASE}-manifest.json",
}

SOURCE_FILES = [
    # Durable lane controls; the raw authority audit is intentionally omitted
    # because it contains local paths and is represented by its exact hash.
    ("00_control/CHAPTER12_TERMINOLOGY_AUDIT.md", LANE / "00_control" / "CHAPTER12_TERMINOLOGY_AUDIT.md"),
    ("00_control/SOURCE_CORRECTIONS.csv", LANE / "00_control" / "SOURCE_CORRECTIONS.csv"),
    ("00_control/TERMINOLOGY.csv", LANE / "00_control" / "TERMINOLOGY.csv"),
    ("00_control/CURRENT_GOAL_AND_WORKFLOW.md", LANE / "00_control" / "CURRENT_GOAL_AND_WORKFLOW.md"),
    ("00_control/PRODUCTION_CURSOR.json", LANE / "00_control" / "PRODUCTION_CURSOR.json"),
    ("00_control/RECOVERY_POINTER.json", LANE / "00_control" / "RECOVERY_POINTER.json"),
    ("00_control/DECISION_LOG.md", LANE / "00_control" / "DECISION_LOG.md"),
    # Current Chapter 12 source closure.
    *[(f"repo/source/{name}", ROOT / "source" / name) for name in (
        "chap_top_spaces.ptx",
        "sec_top_space_intro.ptx",
        "sec_exam_top.ptx",
        "sec_base_top.ptx",
        "sec_metric_top_space.ptx",
        "sec_neighborhood_top_space.ptx",
        "sec_interior_set_top.ptx",
        "sec_top_space_summ.ptx",
        "sec_top_space_exer.ptx",
    )],
    # Original CC BY 4.0 companion and additive backend.
    *[(f"repo/companion/{name}", ROOT / "companion" / name) for name in (
        "chapter_12_source_guides_a.ptx",
        "chapter_12_source_guides_b.ptx",
        "chapter_12_source_guides_c.ptx",
        "chapter_12_source_guides_d.ptx",
        "chapter_12_source_guides_e.ptx",
        "chapter_12_source_guides_f.ptx",
        "chapter_12_exercise_guides_a.ptx",
        "chapter_12_topological_spaces_self_study.ptx",
    )],
    ("repo/backend/chapter_12_companion_manifest.partial.json", ROOT / "backend" / "chapter_12_companion_manifest.partial.json"),
    ("repo/backend/chapter_12_entry_aliases.partial.csv", ROOT / "backend" / "chapter_12_entry_aliases.partial.csv"),
    # Compact current QA/provenance receipts.
    *[(f"repo/qa/{name}", ROOT / "qa" / name) for name in (
        "CHAPTER12_SOURCE_QA.json",
        "CHAPTER12_SOURCE_TRANSLATION_RECEIPT.md",
        "CHAPTER12_COMPANION_PARTIAL_QA.json",
        "CHAPTER12_EXERCISE_GUIDES_A_SCHEMA_QA.json",
        "CHAPTER12_EXERCISE_GUIDES_B_SCHEMA_QA.json",
        "CHAPTER12_SUMMARY_SCHEMA_QA.json",
        "CHAPTER12_COMPANION_WRAPPER_SCHEMA_QA.json",
        "CHAPTER12_INTERIOR_GUIDE_SCHEMA_QA.json",
        "CHAPTER12_EXERCISE_A_GITHUB_RECEIPT.md",
        "CHAPTER12_EXERCISE_B_GITHUB_RECEIPT.md",
    )],
    ("repo/README.md", ROOT / "README.md"),
    ("repo/LICENSES.md", ROOT / "LICENSES.md"),
    ("repo/companion/RIGHTS.md", ROOT / "companion" / "RIGHTS.md"),
    ("repo/scripts/validate_pretext_local.py", ROOT / "scripts" / "validate_pretext_local.py"),
    ("repo/scripts/qa_source_translation.py", ROOT / "scripts" / "qa_source_translation.py"),
    ("repo/scripts/build_zenodo_chapter12_partial_package.py", ROOT / "scripts" / "build_zenodo_chapter12_partial_package.py"),
]

EXPECTED_READER = {
    PDF_NAME: {"bytes": 2_322_239, "sha256": "a00ad9c4ea949edc7b90c18534386cea23efd6093b47bc57bae8da387c8ee034"},
    HTML_NAME: {"bytes": 8_569_809, "sha256": "b0a9f7392c0e7c28ed48df983eb96ad5b71c6f0b97c45c8e23a59f43ef1e7370"},
    LICENSES_NAME: {"bytes": 2_277, "sha256": "408eeec186fd9b34660ea5d6df19df5d0e0da7ae63e8681852ff5eaa7b6fb941"},
    RIGHTS_NAME: {"bytes": 2_181, "sha256": "ef9e9960775b17d187cc655fc73a6f7d76b3d8fe05b9960d3e168ae9fc4fcfe7"},
}


def checked(path: Path, expected: dict[str, object] | None = None) -> bytes:
    data = path.read_bytes()
    assert_sanitized(path.name, data)
    if expected is not None and {"bytes": len(data), "sha256": digest(data)} != expected:
        raise RuntimeError(f"identity changed: {path}")
    return data


def build_source_zip() -> dict[str, object]:
    old_path = OLD / SOURCE_NAME
    if not old_path.is_file():
        raise FileNotFoundError(old_path)
    with zipfile.ZipFile(old_path, "r") as archive:
        entries = {info.filename: archive.read(info.filename) for info in archive.infolist()}
    for relative, path in SOURCE_FILES:
        if not path.is_file():
            raise FileNotFoundError(path)
        data = checked(path)
        archive_name = f"point-set-topology-id/{relative}"
        entries[archive_name] = data
    output = OUT / SOURCE_NAME
    result = deterministic_zip(output, entries)
    result["source_entry_count"] = len(entries)
    return result


def write_manifest(source_zip: dict[str, object]) -> Path:
    pdf = OUT / PDF_NAME
    html = OUT / HTML_NAME
    licenses = OUT / LICENSES_NAME
    rights = OUT / RIGHTS_NAME
    qa = ROOT / "qa" / "CHAPTER12_COMPANION_PARTIAL_QA.json"
    manifest = {
        "schema_version": 1,
        "status": "partial_checkpoint",
        "record": {
            "concept_doi": "10.5281/zenodo.22059894",
            "predecessor_record_id": 22070455,
            "publication_target": "new version of the existing concept lineage",
            "title": "Topologi: Pendekatan Berbasis Inkuiri",
            "version": "2026.08.23-ch12-exercise-a",
            "language": "ind",
            "reader_boundary": {"chapters_verified": 11, "chapters_total": 20, "complete": False},
            "source_checkpoint": {
                "chapter": 12,
                "title": "Ruang Topologi",
                "source_files": 9,
                "source_prompt_units": 78,
                "companion_prompt_units_covered": 51,
                "companion_prompt_units_pending": 27,
                "companion_surfaces": 204,
                "status": "partial_not_admitted",
            },
        },
        "authority": {
            "work": "Topology: An Inquiry-Based Approach",
            "author": "Steven Schlicker",
            "institution": "Grand Valley State University",
            "commit": "0c2d8f614ef87aa00de373f3418146c2f1d13bb9",
            "tree": "7df245934eedb7174d5ff8af18afff5a7abdde78",
            "archive": {
                "path": "gvsuoer-topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9.zip",
                "bytes": 2_200_204,
                "sha256": "d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3",
            },
            "audit_sha256": "5fec6d8cf2e37e3616024a257c8c10b9a37e38ee7d1778960c1ecbde2555034f",
        },
        "source_checkpoint": {
            "translated_combined_sha256": "ce64a4bdde0de700eeb5fe6f084b4882b5845ebc6246055a2cfdad354bdf0a3f",
            "source_qa": {"path": "repo/qa/CHAPTER12_SOURCE_QA.json", **identity(ROOT / "qa" / "CHAPTER12_SOURCE_QA.json")},
            "source_corrections_sha256": digest((LANE / "00_control" / "SOURCE_CORRECTIONS.csv").read_bytes()),
            "companion_qa": {"path": "repo/qa/CHAPTER12_COMPANION_PARTIAL_QA.json", **identity(qa)},
            "companion_manifest_sha256": digest((ROOT / "backend" / "chapter_12_companion_manifest.partial.json").read_bytes()),
            "github_content_commit": "97732bc2930ec4a25c3510c80891370a2d3943a3",
            "github_receipt_commit": "0387c43c3fe8d9f377ed7d89f87c7c17705ee35b",
            "github_receipt_sha256": digest((ROOT / "qa" / "CHAPTER12_EXERCISE_B_GITHUB_RECEIPT.md").read_bytes()),
        },
        "reader": {
            "pdf": {"pages": 276, **identity(pdf)},
            "html": {"bytes": identity(html)["bytes"], "sha256": identity(html)["sha256"], "status": "unchanged_11_chapter_reader"},
            "source_files_translated": 72,
        },
        "rights": [
            {"component": "translated GVSU instructional text", "license": "CC BY-NC-SA 3.0", "url": "https://creativecommons.org/licenses/by-nc-sa/3.0/", "basis": "conservative determination because upstream metadata conflicts"},
            {"component": "original self-study companions and completion material", "license": "CC BY 4.0", "url": "https://creativecommons.org/licenses/by/4.0/"},
            {"component": "software, XSLT, fonts, figures, and separately noticed assets", "license": "component notices retained"},
        ],
        "caveats": [
            "The public reader remains the verified Chapters 1-11 boundary; Chapter 12 source and companion are a partial, non-admitted checkpoint.",
            "Chapters 12-20, the original C90 completion modules, full offline closure, whole-book figure provenance, and tagged PDF remain unfinished.",
            "HTML is the primary accessible surface; the PDF is untagged and some mathematical fonts have incomplete Unicode maps.",
        ],
        "production_provenance": {
            "tool": "OpenAI Codex gpt-5.6-sol, Ultra",
            "direction": "the user",
            "scope": "translation drafting, original companion, modular backend, and edition QA",
            "credit_note": "This provenance does not replace source-author, institutional, or human-contributor credits.",
        },
        "files": [
            {"path": PDF_NAME, **identity(pdf), "role": "276-page Indonesian reader PDF (Chapters 1-11 boundary)"},
            {"path": HTML_NAME, **identity(html), "role": "cumulative HTML reader (Chapters 1-11 boundary)"},
            {"path": SOURCE_NAME, **source_zip, "role": "editable source, Chapter 12 partial companion/backend, authority lineage, and sanitized QA"},
            {"path": LICENSES_NAME, **identity(licenses), "role": "collection component-rights map"},
            {"path": RIGHTS_NAME, **identity(rights), "role": "original companion rights and attribution"},
        ],
        "package_validation": {
            "zip_crc_test": "pass",
            "zip_inventory": "pass",
            "zip_deterministic_double_build": "pass",
            "textual_privacy_scan": "pass",
            "binary_credential_marker_scan": "pass",
            "pdf_metadata_and_xmp_privacy_scan": "pass",
            "raw_build_logs_included": False,
        },
        "supplemental_checksums_file": CHECKSUMS_NAME,
    }
    target = OUT / MANIFEST_NAME
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    checked(target)
    return target


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    allowed = {PDF_NAME, HTML_NAME, SOURCE_NAME, LICENSES_NAME, RIGHTS_NAME, MANIFEST_NAME, CHECKSUMS_NAME}
    unexpected = {p.name for p in OUT.iterdir() if p.is_file()} - allowed
    if unexpected:
        raise RuntimeError(f"unexpected output files: {sorted(unexpected)}")
    for name, expected in EXPECTED_READER.items():
        src = OLD / name
        data = checked(src, expected)
        (OUT / name).write_bytes(data)
    assert_pdf_privacy(OUT / PDF_NAME)
    source_zip = build_source_zip()
    manifest = write_manifest(source_zip)
    checksums = []
    for name in (PDF_NAME, HTML_NAME, SOURCE_NAME, LICENSES_NAME, RIGHTS_NAME, MANIFEST_NAME):
        path = OUT / name
        checksums.append(f"{digest(path.read_bytes())}  {name}")
    checksum_path = OUT / CHECKSUMS_NAME
    checksum_path.write_text("\n".join(checksums) + "\n", encoding="utf-8", newline="\n")
    checked(checksum_path)
    print(json.dumps({"status": "pass", "output": OUT.name, "manifest": identity(manifest), "checksums": identity(checksum_path), "source_zip": source_zip}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
