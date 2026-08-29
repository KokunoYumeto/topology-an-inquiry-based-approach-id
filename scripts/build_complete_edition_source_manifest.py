#!/usr/bin/env python3
"""Freeze the compact editable-source/backend closure for the complete edition.

The manifest is rooted in the exact XInclude closure admitted by
``CHAPTERS01_20_COMPLETE_SCHEMA_QA.json``.  It adds only active figure assets,
the reader-interface assets, current modular backend, essential build/QA code,
component-rights files, and a small public control set.  Historical partial
packages, caches, raw logs, temporary files, and superseded cumulative backend
snapshots are deliberately excluded.

``--preflight`` validates the complete static closure without requiring the
still-running final PDF/HTML gates and never writes a file.  A normal run is
fail-closed on the final HTML and PDF receipts.  ``--check`` recomputes the
normal manifest and compares it byte for byte with the stored result.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
BOUNDARY = "complete_chapters_01_20_plus_completion_modules_01_08"

READER = ROOT / "source/chapters_01_20_complete_reader.ptx"
SCHEMA_QA = ROOT / "qa/CHAPTERS01_20_COMPLETE_SCHEMA_QA.json"
CLOSURE_MANIFEST = ROOT / "backend/chapters_01_20_full_corpus_closure_manifest.json"
CLOSURE_QA = ROOT / "qa/CHAPTERS01_20_FULL_CORPUS_CLOSURE_QA.json"
COMPLETION_MANIFEST = ROOT / "backend/o003_completion_current_manifest.json"
COMPLETION_SCHEMA_QA = ROOT / "qa/O003_COMPLETION_MODULES01_08_SCHEMA_QA.json"
HTML_MANIFEST = ROOT / "qa/CHAPTER20_COMPLETE_HTML_MANIFEST.json"
HTML_QA = ROOT / "qa/CHAPTER20_COMPLETE_HTML_QA.json"
HTML_VENDOR_MANIFEST = ROOT / "qa/CHAPTER20_COMPLETE_HTML_VENDOR_MANIFEST.json"
PDF_QA = ROOT / "qa/CHAPTERS01_20_COMPLETE_PDF_QA.json"
FINAL_PDF = ROOT / "output/chapters01-20-complete-pdf/chapters_01_20_complete_reader.pdf"
OFFLINE_RUNTIME_VENDOR_ROOT = ROOT / "external/vendor"
AUTHORITY_ARCHIVE = (
    LANE
    / "authority/archives"
    / "gvsuoer-topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9.zip"
)
DEFAULT_OUTPUT = ROOT / "backend/complete_edition_source_backend_manifest.json"

EXPECTED_AUTHORITY_ARCHIVE = {
    "bytes": 2_200_204,
    "sha256": "d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3",
}
EXPECTED_COUNTS = {
    "main_chapter_includes": 20,
    "chapter_companion_includes": 20,
    "chapter_companion_manifests": 20,
    "chapter_companion_closure_files": 121,
    "chapter20_source_support_entries": 56,
    "chapter20_mastery_entries": 8,
    "chapter20_staged_surfaces": 256,
    "completion_modules": 8,
    "completion_mastery_exercises": 56,
    "completion_staged_surfaces": 224,
}

TOP_LEVEL_PATHS = (
    "repo/README.md",
    "repo/LICENSES.md",
    "repo/requirements.txt",
    "repo/project.ptx",
    "repo/companion/RIGHTS.md",
    "repo/xsl/custom-latex.xsl",
    "repo/xsl/topology-style.xsl",
)
INTERFACE_ASSETS = (
    "repo/assets/o003-epsilon-delta-lab.html",
    "repo/assets/o003-favicon.svg",
    "repo/assets/o003-readable-layout.css",
)
ESSENTIAL_SCRIPTS = (
    "repo/scripts/build_chapter11_pdf_visual_qa.py",
    "repo/scripts/build_chapters01_20_complete_pdf_visual_qa.py",
    "repo/scripts/build_complete_edition_source_manifest.py",
    "repo/scripts/build_directory_manifest.py",
    "repo/scripts/build_pretext_pdf_strict.py",
    "repo/scripts/build_zenodo_complete_edition_package.py",
    "repo/scripts/finalize_and_qa_chapter20_complete_html.py",
    "repo/scripts/finalize_chapter17_html.py",
    "repo/scripts/qa_chapters01_20_complete_pdf_pipeline.py",
    "repo/scripts/qa_chapters01_20_complete_schema.py",
    "repo/scripts/qa_chapters01_20_full_corpus_closure.py",
    "repo/scripts/qa_o003_completion_current.py",
    "repo/scripts/qa_o003_completion_modules01_02.py",
    "repo/scripts/qa_o003_completion_modules01_08_html.py",
    "repo/scripts/qa_o003_completion_modules01_08_schema.py",
    "repo/scripts/refresh_chapter20_companion_state.py",
    "repo/scripts/refresh_chapter20_source_state.py",
)
PUBLIC_CONTROLS = (
    "00_control/AUTHORITY_BUILD_RIGHTS.md",
    "00_control/CHAPTER20_AUTHORITY_AUDIT.md",
    "00_control/FINAL_SELECTION_AND_COMPLETION_SCOPE.md",
    "00_control/SOURCE_CORRECTIONS.csv",
    "00_control/TERMINOLOGY.csv",
)
STATIC_QA = (
    "repo/qa/CHAPTER20_COMPANION_QA.json",
    "repo/qa/CHAPTER20_COMPANION_SCHEMA_QA.json",
    "repo/qa/CHAPTER20_SOURCE_IDENTITY_QA.json",
    "repo/qa/CHAPTER20_COMPLETE_HTML_VENDOR_MANIFEST.json",
    "repo/qa/CHAPTERS01_20_COMPLETE_SCHEMA_QA.json",
    "repo/qa/CHAPTERS01_20_FULL_CORPUS_CLOSURE_QA.json",
    "repo/qa/O003_COMPLETION_CURRENT_QA.json",
    "repo/qa/O003_COMPLETION_MODULES01_08_SCHEMA_QA.json",
)
FINAL_QA = (
    "repo/qa/CHAPTER20_COMPLETE_HTML_MANIFEST.json",
    "repo/qa/CHAPTER20_COMPLETE_HTML_QA.json",
    "repo/qa/CHAPTER20_COMPLETE_DOCS_MANIFEST.json",
    "repo/qa/CHAPTER20_COMPLETE_DOCS_QA.json",
    "repo/qa/CHAPTERS01_20_COMPLETE_PDF_QA.json",
    "repo/qa/CHAPTERS01_20_COMPLETE_PDF_MANUAL_VISUAL_QA.md",
)

EXCLUDED_NAME_TOKENS = (
    ".partial.",
    "__pycache__",
    "chapter12_companion_partial",
    "zenodo-chapters",
)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def require_sha256(value: Any, label: str) -> str:
    require(
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value),
        f"{label} is not a lowercase SHA-256 digest",
    )
    return value


def safe_relative(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    require(
        not path.is_absolute()
        and bool(path.parts)
        and ".." not in path.parts
        and "\\" not in value,
        f"unsafe inventory path: {value!r}",
    )
    return path


def inventory_disk_path(value: str) -> Path:
    relative = safe_relative(value)
    if relative.parts[0] == "repo":
        candidate = ROOT.joinpath(*relative.parts[1:]).resolve()
        candidate.relative_to(ROOT.resolve())
        return candidate
    if relative.parts[0] == "00_control":
        candidate = LANE.joinpath(*relative.parts).resolve()
        candidate.relative_to(LANE.resolve())
        return candidate
    raise RuntimeError(f"unsupported inventory root: {value}")


def identity(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {"bytes": len(payload), "sha256": sha256_bytes(payload)}


def require_identity(path: Path, expected: dict[str, Any], label: str) -> None:
    require(path.is_file(), f"missing {label}: {path}")
    expected_identity = {
        "bytes": expected.get("bytes"),
        "sha256": require_sha256(expected.get("sha256"), f"{label} SHA-256"),
    }
    require(identity(path) == expected_identity, f"{label} identity changed")


def inventory_row(value: str, category: str) -> dict[str, Any]:
    relative = safe_relative(value)
    folded = relative.as_posix().casefold()
    require(
        not any(token in folded for token in EXCLUDED_NAME_TOKENS),
        f"excluded historical/transient path selected: {value}",
    )
    require(
        not folded.endswith((".log", ".tmp", ".pyc", ".part", ".partial")),
        f"disallowed transient/log selected: {value}",
    )
    path = inventory_disk_path(relative.as_posix())
    require(path.is_file(), f"inventory path is missing: {value}")
    return {"path": relative.as_posix(), **identity(path), "category": category}


def canonical_inventory_sha256(rows: Iterable[dict[str, Any]]) -> str:
    hasher = hashlib.sha256()
    for row in sorted(rows, key=lambda value: str(value["path"]).casefold()):
        hasher.update(str(row["path"]).encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(str(row["bytes"]).encode("ascii"))
        hasher.update(b"\0")
        hasher.update(bytes.fromhex(str(row["sha256"])))
        hasher.update(b"\0")
    return hasher.hexdigest()


def validate_authority() -> dict[str, Any]:
    require_identity(AUTHORITY_ARCHIVE, EXPECTED_AUTHORITY_ARCHIVE, "authority archive")
    return {
        "work": "Topology: An Inquiry-Based Approach",
        "author": "Steven Schlicker",
        "institution": "Grand Valley State University",
        "commit": "0c2d8f614ef87aa00de373f3418146c2f1d13bb9",
        "tree": "7df245934eedb7174d5ff8af18afff5a7abdde78",
        "archive": {
            "path": f"authority/archives/{AUTHORITY_ARCHIVE.name}",
            **identity(AUTHORITY_ARCHIVE),
            "included_in_public_source_zip": False,
            "omission_reason": (
                "The exact archive is hash-bound but omitted because legacy upstream "
                "PDF metadata contains author-workstation paths."
            ),
        },
    }


def validate_closure_contract() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    schema = read_json(SCHEMA_QA)
    require(schema.get("status") == "pass", "complete-reader schema receipt did not pass")
    require(schema.get("failures") == [], "complete-reader schema receipt has failures")
    source = schema.get("source")
    require(isinstance(source, dict), "complete-reader schema source identity is missing")
    require(source.get("path") == "source/chapters_01_20_complete_reader.ptx", "schema receipt points to a different reader")
    require_identity(READER, source, "complete reader")

    closure = schema.get("xinclude_closure")
    require(isinstance(closure, dict), "schema receipt has no XInclude closure")
    raw_files = closure.get("files")
    require(isinstance(raw_files, list), "schema XInclude closure has no file inventory")
    require(closure.get("file_count") == len(raw_files) == 278, "complete reader XInclude file count changed")
    require(closure.get("include_edges") == 277, "complete reader XInclude edge count changed")
    require(closure.get("all_local_and_repo_bounded") is True, "reader XIncludes are not repo-bounded")

    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    closure_payloads: list[tuple[str, bytes]] = []
    total_bytes = 0
    for raw in raw_files:
        require(isinstance(raw, dict), "XInclude closure row is not an object")
        value = raw.get("path")
        require(isinstance(value, str), "XInclude closure row has no path")
        relative = safe_relative(value)
        require(relative.as_posix() not in seen, f"duplicate XInclude closure path: {value}")
        seen.add(relative.as_posix())
        path = ROOT.joinpath(*relative.parts).resolve()
        path.relative_to(ROOT.resolve())
        require_identity(path, raw, f"XInclude closure file {value}")
        payload = path.read_bytes()
        total_bytes += len(payload)
        closure_payloads.append((relative.as_posix(), payload))
        rows.append(
            {
                "path": f"repo/{relative.as_posix()}",
                "bytes": len(payload),
                "sha256": sha256_bytes(payload),
                "category": "reader_xinclude_closure",
            }
        )
    closure_hasher = hashlib.sha256()
    for relative, payload in sorted(
        closure_payloads, key=lambda item: item[0].encode("utf-8")
    ):
        closure_hasher.update(relative.encode("utf-8"))
        closure_hasher.update(b"\0")
        closure_hasher.update(str(len(payload)).encode("ascii"))
        closure_hasher.update(b"\0")
        closure_hasher.update(payload)
        closure_hasher.update(b"\0")
    require(total_bytes == closure.get("bytes"), "XInclude closure byte total changed")
    require(
        closure_hasher.hexdigest() == closure.get("sha256"),
        "XInclude closure canonical SHA-256 changed",
    )

    full_manifest = read_json(CLOSURE_MANIFEST)
    require(full_manifest.get("status") == "pass", "full-corpus closure manifest did not pass")
    require(full_manifest.get("partial") is False, "full-corpus closure is still marked partial")
    require(full_manifest.get("reader") == source, "full-corpus closure binds a different reader")
    counts = full_manifest.get("counts")
    require(isinstance(counts, dict), "full-corpus closure counts are missing")
    for key, expected in EXPECTED_COUNTS.items():
        require(counts.get(key) == expected, f"full-corpus closure count changed: {key}")
    rights = full_manifest.get("rights_and_provenance")
    require(isinstance(rights, dict), "full-corpus rights/provenance block is missing")
    require(rights.get("source_derivative") == "CC BY-NC-SA 3.0 (conservative treatment)", "spine rights marker changed")
    require(rights.get("original_companions_and_completion") == "CC BY 4.0 separate components", "original-component rights marker changed")
    require(rights.get("licenses_not_flattened") is True, "component licenses were flattened")
    require(rights.get("nonendorsement") is True, "non-endorsement marker is absent")
    require(rights.get("model_provenance") == MODEL, "model provenance changed")

    full_qa = read_json(CLOSURE_QA)
    require(full_qa.get("status") == "pass" and full_qa.get("failures") == [], "full-corpus closure QA did not pass")
    checks = full_qa.get("checks")
    require(isinstance(checks, dict) and checks and all(value is True for value in checks.values()), "full-corpus closure QA checks are not all true")
    return schema, rows


def active_asset_rows(closure_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str]]:
    parser = etree.XMLParser(resolve_entities=False, no_network=True, recover=False)
    stems: set[str] = set()
    for row in closure_rows:
        value = str(row["path"])
        if not value.endswith((".ptx", ".xml")):
            continue
        path = inventory_disk_path(value)
        tree = etree.parse(str(path), parser)
        for node in tree.xpath("//*[local-name()='image' and @source]"):
            raw = str(node.get("source") or "").strip()
            require(raw and "/" not in raw and "\\" not in raw and ".." not in raw, f"unsafe image source: {raw!r}")
            stems.add(raw)
    # The exact complete-reader closure contains 52 active stems.  The inactive
    # commented ``star`` stem is intentionally outside this compact package.
    require(len(stems) == 52, f"active image-stem census changed: {len(stems)}")

    selected: set[str] = set(INTERFACE_ASSETS)
    for stem in sorted(stems, key=str.casefold):
        suffix = PurePosixPath(stem).suffix.casefold()
        candidates = (stem,) if suffix else (f"{stem}.svg", f"{stem}.pdf")
        matched = 0
        for name in candidates:
            value = f"repo/assets/{name}"
            if inventory_disk_path(value).is_file():
                selected.add(value)
                matched += 1
        require(matched > 0, f"no packaged asset resolves active image source: {stem}")
    rows = [inventory_row(value, "active_reader_asset") for value in sorted(selected, key=str.casefold)]
    return rows, sorted(stems, key=str.casefold)


def offline_runtime_vendor_rows() -> list[dict[str, Any]]:
    """Validate and inventory the pinned offline reader-runtime closure.

    The finalized HTML reader is intentionally offline-closed.  Its vendored
    MathJax, Lunr, and PreTeXt runtime files therefore belong to the compact
    reproducible source package as well as to the generated HTML tree.  The
    finalizer emits a lock manifest whose output paths are mapped back to this
    exact repository tree; comparing every byte here prevents a stale or
    incomplete vendor copy from being silently packaged.
    """
    require(
        OFFLINE_RUNTIME_VENDOR_ROOT.is_dir(),
        f"offline runtime vendor tree is missing: {OFFLINE_RUNTIME_VENDOR_ROOT}",
    )
    require(HTML_VENDOR_MANIFEST.is_file(), "offline runtime vendor lock manifest is missing")
    lock = read_json(HTML_VENDOR_MANIFEST)
    require(lock.get("schema_version") == 1, "offline runtime vendor lock schema changed")
    require(lock.get("source") == "repo/external/vendor", "offline runtime vendor lock source changed")
    raw_files = lock.get("files")
    require(isinstance(raw_files, list) and raw_files, "offline runtime vendor lock has no files")

    output_prefix = "output/chapters01-20-complete-html/external/vendor/"
    locked: dict[str, dict[str, Any]] = {}
    for row in raw_files:
        require(isinstance(row, dict) and isinstance(row.get("path"), str), "malformed offline runtime vendor lock row")
        output_path = safe_relative(str(row["path"])).as_posix()
        require(output_path.startswith(output_prefix), f"offline runtime vendor lock path is outside output vendor tree: {output_path}")
        relative = output_path.removeprefix("output/chapters01-20-complete-html/")
        source_value = f"repo/{relative}"
        require(source_value not in locked, f"duplicate offline runtime vendor lock path: {source_value}")
        locked[source_value] = row

    actual: list[dict[str, Any]] = []
    for path in sorted(OFFLINE_RUNTIME_VENDOR_ROOT.rglob("*"), key=lambda value: value.relative_to(ROOT).as_posix().casefold()):
        if not path.is_file():
            continue
        resolved = path.resolve()
        resolved.relative_to(OFFLINE_RUNTIME_VENDOR_ROOT.resolve())
        value = f"repo/{path.relative_to(ROOT).as_posix()}"
        require(value in locked, f"unlocked offline runtime vendor file: {value}")
        actual.append(inventory_row(value, "offline_runtime_vendor"))
        require_identity(path, locked[value], f"offline runtime vendor file {value}")
    require(len(actual) == len(locked), "offline runtime vendor lock does not match the complete tree")
    return actual


def backend_rows() -> list[dict[str, Any]]:
    selected: set[str] = set()
    for chapter in range(1, 21):
        prefix = f"chapter_{chapter:02d}_"
        chapter_files = sorted(
            (
                path
                for path in (ROOT / "backend").glob(f"{prefix}*")
                if path.is_file()
                and path.suffix.casefold() in {".json", ".csv"}
                and ".partial." not in path.name.casefold()
                # This raw diagnostic inventory embeds machine-local absolute
                # roots.  The relative prompt map, grouping nodes, and complete
                # companion manifest remain packaged as the resumable backend.
                and path.name != "chapter_20_prompt_inventory.json"
            ),
            key=lambda path: path.name.casefold(),
        )
        require(
            any(path.name == f"chapter_{chapter:02d}_companion_manifest.json" for path in chapter_files),
            f"Chapter {chapter} companion manifest is missing",
        )
        selected.update(f"repo/backend/{path.name}" for path in chapter_files)
    selected.update(
        {
            "repo/backend/chapters_01_20_full_corpus_closure_manifest.json",
            "repo/backend/o003_completion_current_manifest.json",
        }
    )
    selected.discard("repo/backend/complete_edition_source_backend_manifest.json")
    return [inventory_row(value, "current_modular_backend") for value in sorted(selected, key=str.casefold)]


def validate_completion() -> dict[str, Any]:
    manifest = read_json(COMPLETION_MANIFEST)
    require(manifest.get("status") == "modules_01_08_complete_schema_and_backend_qa_pass", "completion manifest is not complete")
    require(manifest.get("component_license") == "CC BY 4.0", "completion component license changed")
    require(manifest.get("source_spine_license_context") == "CC BY-NC-SA 3.0 (conservative treatment)", "completion spine-license context changed")
    require(manifest.get("nonendorsement") is True, "completion non-endorsement marker is absent")
    require(manifest.get("model_provenance") == MODEL, "completion model provenance changed")
    require(manifest.get("remaining_modules") == [], "completion modules remain unfinished")
    counts = manifest.get("cumulative_counts")
    require(isinstance(counts, dict), "completion cumulative counts are missing")
    expected = {"modules": 8, "mastery_exercises": 56, "hints": 56, "answers": 56, "solutions": 56, "staged_surfaces": 224}
    for key, value in expected.items():
        require(counts.get(key) == value, f"completion count changed: {key}")
    modules = manifest.get("modules")
    require(isinstance(modules, list) and len(modules) == 8, "completion manifest does not contain Modules 1--8")
    schema = read_json(COMPLETION_SCHEMA_QA)
    require(schema.get("status") == "pass" and schema.get("failures") == [], "completion schema receipt did not pass")
    return {
        "manifest": {"path": "backend/o003_completion_current_manifest.json", **identity(COMPLETION_MANIFEST)},
        "schema_receipt": {"path": "qa/O003_COMPLETION_MODULES01_08_SCHEMA_QA.json", **identity(COMPLETION_SCHEMA_QA)},
        "modules": 8,
        "mastery_exercises": 56,
        "staged_surfaces": 224,
    }


def validate_rights_files() -> None:
    collection = (ROOT / "LICENSES.md").read_text(encoding="utf-8")
    companion = (ROOT / "companion/RIGHTS.md").read_text(encoding="utf-8")
    for marker in ("CC BY-NC-SA 3.0", "CC BY 4.0", "No endorsement"):
        require(marker.casefold() in collection.casefold(), f"LICENSES.md lacks marker: {marker}")
    for marker in ("CC BY-NC-SA 3.0", "CC BY 4.0", "No endorsement"):
        require(marker.casefold() in companion.casefold(), f"companion/RIGHTS.md lacks marker: {marker}")


def validate_final_receipts() -> dict[str, Any]:
    html_manifest = read_json(HTML_MANIFEST)
    require(html_manifest.get("schema_version") == 1, "final HTML manifest schema changed")
    require(html_manifest.get("stage") == "finalized", "HTML tree is not finalized")
    require(html_manifest.get("target") == "chapters01-20-complete-html", "HTML target changed")
    require(html_manifest.get("root") == "output/chapters01-20-complete-html", "HTML root changed")
    files = html_manifest.get("files")
    require(isinstance(files, list) and len(files) == html_manifest.get("file_count"), "HTML manifest file census is malformed")
    require(int(html_manifest.get("file_count", 0)) >= 20_000, "HTML tree is implausibly incomplete")
    require(int(html_manifest.get("html_files", 0)) >= 19_800, "HTML page census is implausibly incomplete")
    require_sha256(html_manifest.get("canonical_manifest_sha256"), "HTML canonical manifest")

    html_qa = read_json(HTML_QA)
    require(html_qa.get("status") == "pass" and html_qa.get("failures") == [], "complete HTML QA did not pass")
    checks = html_qa.get("checks")
    require(isinstance(checks, dict) and checks and all(value is True for value in checks.values()), "complete HTML checks are not all true")
    admitted = html_qa.get("final_manifest")
    require(isinstance(admitted, dict), "HTML QA does not bind the final manifest")
    for key in ("canonical_manifest_sha256", "file_count", "html_files", "total_bytes"):
        require(admitted.get(key) == html_manifest.get(key), f"HTML QA/manifest mismatch: {key}")

    pdf_qa = read_json(PDF_QA)
    require(pdf_qa.get("status") == "pass" and pdf_qa.get("failures") == [], "complete PDF QA did not pass")
    checks = pdf_qa.get("checks")
    require(isinstance(checks, dict) and checks and all(value is True for value in checks.values()), "complete PDF checks are not all true")
    artifact = pdf_qa.get("artifact")
    require(isinstance(artifact, dict), "complete PDF QA has no artifact identity")
    require(artifact.get("path") == "output/chapters01-20-complete-pdf/chapters_01_20_complete_reader.pdf", "complete PDF path changed")
    require(isinstance(artifact.get("pages"), int) and artifact["pages"] > 0, "complete PDF page count is invalid")
    require_identity(FINAL_PDF, artifact, "complete PDF")
    return {
        "html": {
            "manifest": {"path": "qa/CHAPTER20_COMPLETE_HTML_MANIFEST.json", **identity(HTML_MANIFEST)},
            "qa": {"path": "qa/CHAPTER20_COMPLETE_HTML_QA.json", **identity(HTML_QA)},
            "files": html_manifest["file_count"],
            "html_files": html_manifest["html_files"],
            "bytes": html_manifest["total_bytes"],
            "canonical_manifest_sha256": html_manifest["canonical_manifest_sha256"],
        },
        "pdf": {
            "qa": {"path": "qa/CHAPTERS01_20_COMPLETE_PDF_QA.json", **identity(PDF_QA)},
            "artifact": artifact,
        },
    }


def build_manifest(require_final: bool) -> dict[str, Any]:
    authority = validate_authority()
    schema, closure_rows = validate_closure_contract()
    completion = validate_completion()
    validate_rights_files()

    rows = list(closure_rows)
    asset_rows, active_stems = active_asset_rows(closure_rows)
    rows.extend(asset_rows)
    vendor_rows = offline_runtime_vendor_rows()
    rows.extend(vendor_rows)
    rows.extend(backend_rows())
    for value in TOP_LEVEL_PATHS:
        rows.append(inventory_row(value, "build_and_rights_root"))
    for value in ESSENTIAL_SCRIPTS:
        rows.append(inventory_row(value, "essential_build_qa_script"))
    for value in PUBLIC_CONTROLS:
        rows.append(inventory_row(value, "public_reproducibility_control"))
    for value in STATIC_QA:
        rows.append(inventory_row(value, "essential_static_qa"))

    release_artifacts: dict[str, Any] | None = None
    if require_final:
        release_artifacts = validate_final_receipts()
        for value in FINAL_QA:
            rows.append(inventory_row(value, "final_reader_qa"))

    paths = [str(row["path"]) for row in rows]
    duplicates = sorted(path for path, count in Counter(paths).items() if count > 1)
    require(not duplicates, f"duplicate source/backend inventory paths: {duplicates}")
    rows.sort(key=lambda row: str(row["path"]).casefold())
    category_counts = dict(sorted(Counter(str(row["category"]) for row in rows).items()))

    source_identity = schema["source"]
    return {
        "schema_version": 1,
        "status": "pass" if require_final else "static_preflight_pass",
        "partial": False,
        "boundary_complete": True,
        "boundary": BOUNDARY,
        "complete_edition": True,
        "completion": {
            "chapters_verified": 20,
            "chapters_total": 20,
            "completion_modules_verified": 8,
            "completion_modules_total": 8,
            "chapter20_source_supports": 56,
            "chapter20_mastery_entries": 8,
            "chapter20_staged_surfaces": 256,
            "completion_mastery_exercises": 56,
            "completion_staged_surfaces": 224,
        },
        "reader": source_identity,
        "xinclude_closure": {
            "receipt": {"path": "qa/CHAPTERS01_20_COMPLETE_SCHEMA_QA.json", **identity(SCHEMA_QA)},
            "file_count": len(closure_rows),
            "include_edges": schema["xinclude_closure"]["include_edges"],
            "bytes": schema["xinclude_closure"]["bytes"],
            "sha256": schema["xinclude_closure"]["sha256"],
        },
        "full_corpus_backend_closure": {
            "manifest": {"path": "backend/chapters_01_20_full_corpus_closure_manifest.json", **identity(CLOSURE_MANIFEST)},
            "qa": {"path": "qa/CHAPTERS01_20_FULL_CORPUS_CLOSURE_QA.json", **identity(CLOSURE_QA)},
        },
        "completion_component": completion,
        "authority": authority,
        "rights": {
            "collection_policy": "per-component rights; no flattened license",
            "translated_gvsu_spine": "CC BY-NC-SA 3.0 (conservative determination)",
            "original_self_study_companions_and_completion": "CC BY 4.0",
            "software_figures_fonts_and_assets": "per-component notices retained",
            "collection_licenses": {"path": "repo/LICENSES.md", **identity(ROOT / "LICENSES.md")},
            "companion_rights": {"path": "repo/companion/RIGHTS.md", **identity(ROOT / "companion/RIGHTS.md")},
            "non_endorsement": True,
        },
        "production_provenance": {
            "tool": MODEL,
            "direction": "the user",
            "scope": "translation drafting, original companion/completion, modular backend, and edition QA",
            "credit_note": "This provenance does not replace source-author, institutional, or human-contributor credits.",
        },
        "active_reader_assets": {
            "image_stems": len(active_stems),
            "interface_assets": list(INTERFACE_ASSETS),
            "inactive_or_unreferenced_assets_not_swept_into_package": True,
        },
        "offline_runtime_vendor": {
            "lock_manifest": {"path": "repo/qa/CHAPTER20_COMPLETE_HTML_VENDOR_MANIFEST.json", **identity(HTML_VENDOR_MANIFEST)},
            "files": len(vendor_rows),
            "bytes": sum(int(row["bytes"]) for row in vendor_rows),
            "canonical_inventory_sha256": canonical_inventory_sha256(vendor_rows),
            "purpose": "pinned local MathJax, Lunr, and PreTeXt runtime closure for offline HTML",
        },
        "release_artifact_receipts": release_artifacts,
        "package_source_inventory_contract": (
            "SHA-256 over inventory path UTF-8, NUL, decimal byte count, NUL, "
            "raw 32-byte file SHA-256, NUL; rows sorted case-insensitively"
        ),
        "package_source_inventory_sha256": canonical_inventory_sha256(rows),
        "package_source_inventory_counts": {
            "files": len(rows),
            "bytes": sum(int(row["bytes"]) for row in rows),
            "by_category": category_counts,
        },
        "package_source_inventory": rows,
        "exclusions": [
            "all output build trees and package directories",
            "all raw build logs, caches, temporary files, and bytecode",
            "all historical partial package artifacts",
            "superseded cumulative backend snapshots",
            "inactive or unreferenced figure assets",
            "the raw Chapter 20 prompt diagnostic containing machine-local roots",
            "the hash-bound upstream archive with legacy workstation-path PDF metadata",
        ],
    }


def write_exact(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    require(not temporary.exists(), f"stale temporary manifest exists: {temporary}")
    temporary.write_bytes(payload)
    require(temporary.read_bytes() == payload, "temporary manifest readback failed")
    temporary.replace(path)
    require(path.read_bytes() == payload, "manifest readback failed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--preflight", action="store_true", help="validate static complete-edition inputs without final reader artifacts or writes")
    mode.add_argument("--check", action="store_true", help="recompute the final manifest and compare byte for byte")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="complete source/backend manifest path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = build_manifest(require_final=not args.preflight)
        payload = json_bytes(manifest)
        if args.preflight:
            print(
                json.dumps(
                    {
                        "status": "pass",
                        "preflight": True,
                        "complete_edition": True,
                        "chapters": "20/20",
                        "completion_modules": "8/8",
                        "inventory_files_if_frozen_now": manifest["package_source_inventory_counts"]["files"],
                        "inventory_bytes_if_frozen_now": manifest["package_source_inventory_counts"]["bytes"],
                        "pending_final_receipts": [value.removeprefix("repo/") for value in FINAL_QA if not inventory_disk_path(value).is_file()],
                    },
                    sort_keys=True,
                )
            )
            return 0
        output = args.output.resolve()
        output.relative_to(ROOT.resolve())
        if args.check:
            require(output.is_file(), f"stored complete-edition source manifest is missing: {output}")
            require(output.read_bytes() == payload, "stored complete-edition source manifest is not deterministic")
        else:
            write_exact(output, payload)
        print(
            json.dumps(
                {
                    "status": "pass",
                    "check_only": args.check,
                    "complete_edition": True,
                    "chapters": "20/20",
                    "completion_modules": "8/8",
                    "output": output.relative_to(ROOT).as_posix(),
                    "bytes": len(payload),
                    "sha256": sha256_bytes(payload),
                    "inventory_files": manifest["package_source_inventory_counts"]["files"],
                    "inventory_bytes": manifest["package_source_inventory_counts"]["bytes"],
                },
                sort_keys=True,
            )
        )
        return 0
    except (FileNotFoundError, RuntimeError, json.JSONDecodeError, etree.XMLSyntaxError, ValueError) as exc:
        raise SystemExit(f"complete-edition source manifest gate failed: {exc}") from exc


if __name__ == "__main__":
    raise SystemExit(main())
