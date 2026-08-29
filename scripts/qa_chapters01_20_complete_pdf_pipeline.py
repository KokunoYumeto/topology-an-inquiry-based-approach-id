#!/usr/bin/env python3
"""Prepare, record, and compactly admit the complete-reader PDF QA pipeline.

The ``config`` command is safe before any PDF exists.  ``record-run`` is used
after each strict normalized build.  ``prepare-render`` clears only the two
exact task-local raster directories.  ``finalize`` consumes the generic PDF
structure receipt and the complete-reader all-page visual receipt.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
from typing import Any
from urllib.parse import urlsplit

from PIL import Image
from PyPDF2 import PdfReader

import build_pretext_pdf_strict as strict_builder


ROOT = Path(__file__).resolve().parents[1]
TARGET = "chapters01-20-complete-pdf"
SOURCE_DATE_EPOCH = 1692057600
MAINMATTER_PHYSICAL_PAGE = 7
RENDER_DPI = 120
EXPECTED_RENDERER_LABEL = "Poppler pdftoppm 120 dpi"
CONTACT_COLUMNS = 4
CONTACT_ROWS = 3
CONTACT_PAGES_PER_SHEET = CONTACT_COLUMNS * CONTACT_ROWS
EXPECTED_PAGE_SIZE = (612.0, 792.0)
MINIMUM_OUTLINES = 43
MINIMUM_TEXT_CHARACTERS_PER_PAGE = 500
INTENTIONAL_BLANK_PAGES = [3]
URI_SOURCE = "external/o003-epsilon-delta-lab.html"
URI_TARGET = "https://kokunoyumeto.github.io/topology-an-inquiry-based-approach-id/external/o003-epsilon-delta-lab.html"

FINAL_PDF = ROOT / "output/chapters01-20-complete-pdf/chapters_01_20_complete_reader.pdf"
RUN1_PDF = ROOT / "tmp/pdfs/chapters01-20-complete-run1.pdf"
RUN1_LOG = ROOT / "qa/CHAPTERS01_20_COMPLETE_PDF_BUILD_RUN1.log"
RUN2_LOG = ROOT / "qa/CHAPTERS01_20_COMPLETE_PDF_BUILD_RUN2.log"
RUN1_RECEIPT = ROOT / "qa/CHAPTERS01_20_COMPLETE_PDF_RUN1_HASH.json"
RUN2_RECEIPT = ROOT / "qa/CHAPTERS01_20_COMPLETE_PDF_RUN2_HASH.json"
STRUCTURE_RECEIPT = ROOT / "qa/CHAPTERS01_20_COMPLETE_PDF_STRUCTURE.json"
VISUAL_RECEIPT = ROOT / "qa/CHAPTERS01_20_COMPLETE_PDF_VISUAL_QA.json"
RENDER_DIR = ROOT / "tmp/pdfs/chapters01-20-complete-render"
CONTACT_DIR = ROOT / "tmp/pdfs/chapters01-20-complete-contact"
CONFIG_RECEIPT = ROOT / "qa/CHAPTERS01_20_COMPLETE_PDF_PIPELINE_CONFIG.json"
FINAL_RECEIPT = ROOT / "qa/CHAPTERS01_20_COMPLETE_PDF_QA.json"

PIPELINE_SCRIPT = ROOT / "scripts/qa_chapters01_20_complete_pdf_pipeline.py"
STRICT_BUILD_SCRIPT = ROOT / "scripts/build_pretext_pdf_strict.py"
STRUCTURE_SCRIPT = ROOT / "scripts/inspect_pdf_structure.py"
VISUAL_WRAPPER_SCRIPT = ROOT / "scripts/build_chapters01_20_complete_pdf_visual_qa.py"
PIXEL_ENGINE_SCRIPT = ROOT / "scripts/build_chapter11_pdf_visual_qa.py"
CONTACT_SCRIPT = ROOT / "scripts/make_pdf_contact_sheets.py"

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
CONTACT_NAME = re.compile(r"contact-(\d{2,})\.png\Z")
NORMALIZATION_LABEL = (
    "PDF PAGE LABELS NORMALIZED: lowercase Roman through physical page 6; "
    "Arabic 1 begins on physical page 7."
)
URI_LOG_RE = re.compile(
    re.escape(URI_SOURCE)
    + r"\s*->\s*"
    + re.escape(URI_TARGET)
    + r"\s*\((\d+) annotations\)"
)


class ContractError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def repo_relative(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError as exc:
        raise ContractError(f"path leaves repository: {path}") from exc


def identity(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"required file missing: {repo_relative(path)}")
    payload = path.read_bytes()
    return {"path": repo_relative(path), "bytes": len(payload), "sha256": sha256(payload)}


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(payload)
    if temporary.read_bytes() != payload:
        raise ContractError(f"temporary write/readback failed: {repo_relative(path)}")
    temporary.replace(path)


def read_json(path: Path, label: str) -> dict[str, Any]:
    require(path.is_file(), f"{label} missing: {repo_relative(path)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"{label} is not valid UTF-8 JSON: {exc}") from exc
    require(isinstance(value, dict), f"{label} is not a JSON object")
    return value


def dereference(value: Any) -> Any:
    return value.get_object() if hasattr(value, "get_object") else value


def pdf_facts(path: Path) -> dict[str, Any]:
    reader = PdfReader(str(path), strict=True)
    require(not reader.is_encrypted, "normalized PDF is encrypted")
    sizes = Counter(
        (round(float(page.mediabox.width), 4), round(float(page.mediabox.height), 4))
        for page in reader.pages
    )
    rotations = Counter(int(page.get("/Rotate", 0) or 0) % 360 for page in reader.pages)
    root = dereference(reader.trailer["/Root"])
    labels = dereference(root.get("/PageLabels"))
    require(isinstance(labels, dict), "normalized PDF lacks /PageLabels")
    nums = dereference(labels.get("/Nums"))
    require(nums is not None and len(nums) == 4, "normalized PDF page-label array differs")
    first_style = dereference(nums[1])
    second_style = dereference(nums[3])
    page_label_tuple = (int(nums[0]), str(first_style.get("/S")), int(nums[2]), str(second_style.get("/S")))
    expected_labels = (0, "/r", MAINMATTER_PHYSICAL_PAGE - 1, "/D")
    require(page_label_tuple == expected_labels, f"normalized page labels differ: {page_label_tuple}")

    uris: list[str] = []
    relative_uris: list[str] = []
    for page in reader.pages:
        annotations = dereference(page.get("/Annots", [])) or []
        for reference in annotations:
            annotation = dereference(reference)
            action = dereference(annotation.get("/A", {})) or {}
            uri = action.get("/URI")
            if uri is None:
                continue
            text = str(uri)
            uris.append(text)
            parsed = urlsplit(text)
            if not parsed.scheme and not parsed.netloc and not text.startswith("#"):
                relative_uris.append(text)
    require(not relative_uris, f"normalized PDF retains relative URI annotations: {relative_uris[:4]}")
    require(URI_SOURCE not in uris, "declared relative epsilon-delta URI survived normalization")
    target_count = uris.count(URI_TARGET)
    require(target_count > 0, "canonical epsilon-delta HTTPS annotation is absent")
    return {
        "pages": len(reader.pages),
        "page_sizes_points": [
            {"width": width, "height": height, "pages": count}
            for (width, height), count in sorted(sizes.items())
        ],
        "rotations": {str(rotation): count for rotation, count in sorted(rotations.items())},
        "page_labels": [0, "/r", MAINMATTER_PHYSICAL_PAGE - 1, "/D"],
        "uri_annotation_count": len(uris),
        "epsilon_delta_https_annotation_count": target_count,
        "relative_uri_targets": [],
    }


def validate_transcript(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    transcript = payload.decode("utf-8", errors="replace")
    fatal_matches = [pattern.pattern for pattern in strict_builder.FATAL_TEX if pattern.search(transcript)]
    require(not fatal_matches, f"strict build transcript contains fatal TeX: {fatal_matches}")
    require("Success!" in transcript, "PreTeXt success marker absent from strict transcript")
    require(
        re.search(r"Destroying directory .* to clean previously built files", transcript) is not None,
        "strict transcript does not prove a clean build",
    )
    require(NORMALIZATION_LABEL in transcript, "mainmatter physical-page-7 normalization marker absent")
    rewrite = URI_LOG_RE.search(transcript)
    require(rewrite is not None, "epsilon-delta URI rewrite marker absent")
    rewrite_count = int(rewrite.group(1))
    require(rewrite_count > 0, "epsilon-delta URI rewrite count is zero")
    return {
        "identity": {"path": repo_relative(path), "bytes": len(payload), "sha256": sha256(payload)},
        "clean_build": True,
        "fatal_tex_patterns": [],
        "pretext_success_marker": True,
        "page_label_normalization_marker": True,
        "epsilon_delta_uri_rewrite_count": rewrite_count,
    }


def run_receipt_payload(run: int, artifact: Path, log: Path) -> bytes:
    require(run in {1, 2}, "run must be 1 or 2")
    transcript = validate_transcript(log)
    artifact_row = identity(artifact)
    facts = pdf_facts(artifact)
    require(
        facts["epsilon_delta_https_annotation_count"] == transcript["epsilon_delta_uri_rewrite_count"],
        "PDF URI count differs from strict transcript rewrite count",
    )
    receipt: dict[str, Any] = {
        "schema_version": 1,
        "status": "pass",
        "run": run,
        "path": artifact_row["path"],
        "bytes": artifact_row["bytes"],
        "sha256": artifact_row["sha256"],
        "pages": facts["pages"],
        "page_sizes_points": facts["page_sizes_points"],
        "source_date_epoch": SOURCE_DATE_EPOCH,
        "clean_build": True,
        "strict_transcript_gate": True,
        "normalized": {
            "mainmatter_physical_page": MAINMATTER_PHYSICAL_PAGE,
            "page_labels": facts["page_labels"],
            "uri_source": URI_SOURCE,
            "uri_target": URI_TARGET,
            "uri_rewrite_count": transcript["epsilon_delta_uri_rewrite_count"],
            "relative_uri_targets": [],
        },
        "transcript": transcript["identity"],
    }
    if run == 2:
        run1 = read_json(RUN1_RECEIPT, "run-one normalized-byte receipt")
        run1_artifact = identity(RUN1_PDF)
        require(run1.get("status") == "pass" and run1.get("run") == 1, "run-one receipt is not passing")
        require(
            run1.get("bytes") == run1_artifact["bytes"] and run1.get("sha256") == run1_artifact["sha256"],
            "saved run-one PDF differs from its receipt",
        )
        require(run1_artifact["bytes"] == artifact_row["bytes"] and run1_artifact["sha256"] == artifact_row["sha256"], "normalized run-one and run-two PDF bytes differ")
        require(run1.get("pages") == facts["pages"], "normalized PDF page counts differ")
        receipt["byte_identical_to_run_1"] = True
        receipt["run_1"] = run1_artifact
    return json_bytes(receipt)


def command_config() -> dict[str, Any]:
    python = "../toolchain/pretext-1.7.5-py312/Scripts/python.exe"
    strict_common = (
        f'& "{python}" scripts/build_pretext_pdf_strict.py {TARGET} --clean '
        f'--expect-pdf "{repo_relative(FINAL_PDF)}" '
        f'--source-date-epoch {SOURCE_DATE_EPOCH} '
        f'--mainmatter-physical-page {MAINMATTER_PHYSICAL_PAGE} '
        f'--rewrite-uri "{URI_SOURCE}={URI_TARGET}"'
    )
    invocations = [
        strict_common + f' --log "{repo_relative(RUN1_LOG)}"',
        f'& "{python}" scripts/qa_chapters01_20_complete_pdf_pipeline.py record-run 1',
        strict_common + f' --log "{repo_relative(RUN2_LOG)}"',
        f'& "{python}" scripts/qa_chapters01_20_complete_pdf_pipeline.py record-run 2',
        f'& "{python}" scripts/inspect_pdf_structure.py "{repo_relative(FINAL_PDF)}" --output "{repo_relative(STRUCTURE_RECEIPT)}"',
        f'& "{python}" scripts/qa_chapters01_20_complete_pdf_pipeline.py prepare-render',
        f'pdftoppm -r {RENDER_DPI} -png "{repo_relative(FINAL_PDF)}" "{repo_relative(RENDER_DIR)}/page"',
        f'& "{python}" scripts/make_pdf_contact_sheets.py "{repo_relative(RENDER_DIR)}" --output-dir "{repo_relative(CONTACT_DIR)}" --columns {CONTACT_COLUMNS} --rows {CONTACT_ROWS} --thumbnail-width 280',
        f'& "{python}" scripts/build_chapters01_20_complete_pdf_visual_qa.py --build-log "{repo_relative(RUN2_LOG)}" --renderer-label "{EXPECTED_RENDERER_LABEL}"',
        f'& "{python}" scripts/qa_chapters01_20_complete_pdf_pipeline.py finalize',
        f'& "{python}" scripts/qa_chapters01_20_complete_pdf_pipeline.py finalize --check',
    ]
    return {
        "schema_version": 1,
        "status": "pipeline_configured_not_executed",
        "target": TARGET,
        "source_date_epoch": SOURCE_DATE_EPOCH,
        "mainmatter_physical_page": MAINMATTER_PHYSICAL_PAGE,
        "uri_rewrite": {"source": URI_SOURCE, "target": URI_TARGET},
        "expected_page_size_points": list(EXPECTED_PAGE_SIZE),
        "minimum_outline_entries": MINIMUM_OUTLINES,
        "minimum_extracted_characters_per_page": MINIMUM_TEXT_CHARACTERS_PER_PAGE,
        "intentional_blank_physical_pages": INTENTIONAL_BLANK_PAGES,
        "render_dpi": RENDER_DPI,
        "renderer_label": EXPECTED_RENDERER_LABEL,
        "contact_sheet": {
            "columns": CONTACT_COLUMNS,
            "rows": CONTACT_ROWS,
            "pages_per_sheet": CONTACT_PAGES_PER_SHEET,
        },
        "paths": {
            "configuration_receipt": repo_relative(CONFIG_RECEIPT),
            "run_1_log": repo_relative(RUN1_LOG),
            "run_2_log": repo_relative(RUN2_LOG),
            "saved_run_1_pdf": repo_relative(RUN1_PDF),
            "run_1_hash_receipt": repo_relative(RUN1_RECEIPT),
            "run_2_hash_receipt": repo_relative(RUN2_RECEIPT),
            "final_pdf": repo_relative(FINAL_PDF),
            "structure_receipt": repo_relative(STRUCTURE_RECEIPT),
            "render_directory": repo_relative(RENDER_DIR),
            "render_pattern": repo_relative(RENDER_DIR / "page-NNN.png"),
            "contact_directory": repo_relative(CONTACT_DIR),
            "contact_pattern": repo_relative(CONTACT_DIR / "contact-NN.png"),
            "visual_receipt": repo_relative(VISUAL_RECEIPT),
            "compact_final_receipt": repo_relative(FINAL_RECEIPT),
        },
        "pipeline_scripts": [
            identity(path)
            for path in (
                PIPELINE_SCRIPT,
                STRICT_BUILD_SCRIPT,
                STRUCTURE_SCRIPT,
                VISUAL_WRAPPER_SCRIPT,
                PIXEL_ENGINE_SCRIPT,
                CONTACT_SCRIPT,
            )
        ],
        "invocation_sequence": invocations,
    }


def config_command(check: bool) -> int:
    payload = json_bytes(command_config())
    if check:
        require(CONFIG_RECEIPT.is_file() and CONFIG_RECEIPT.read_bytes() == payload, "pipeline configuration receipt differs")
    else:
        atomic_write(CONFIG_RECEIPT, payload)
    print(json.dumps({"status": "pass", "check_only": check, "output": {"path": repo_relative(CONFIG_RECEIPT), "bytes": len(payload), "sha256": sha256(payload)}}, sort_keys=True))
    return 0


def record_run_command(run: int, check: bool) -> int:
    log = RUN1_LOG if run == 1 else RUN2_LOG
    output = RUN1_RECEIPT if run == 1 else RUN2_RECEIPT
    if run == 1 and not check:
        require(FINAL_PDF.is_file(), f"run-one normalized output missing: {repo_relative(FINAL_PDF)}")
        validate_transcript(log)
        pdf_facts(FINAL_PDF)
        RUN1_PDF.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(FINAL_PDF, RUN1_PDF)
        require(RUN1_PDF.read_bytes() == FINAL_PDF.read_bytes(), "saved run-one PDF copy differs")
    artifact = RUN1_PDF if run == 1 else FINAL_PDF
    payload = run_receipt_payload(run, artifact, log)
    if check:
        require(output.is_file() and output.read_bytes() == payload, f"run-{run} receipt differs")
    else:
        atomic_write(output, payload)
    value = json.loads(payload)
    print(json.dumps({"status": "pass", "run": run, "check_only": check, "pdf": {"path": value["path"], "bytes": value["bytes"], "sha256": value["sha256"], "pages": value["pages"]}, "output": {"path": repo_relative(output), "bytes": len(payload), "sha256": sha256(payload)}}, sort_keys=True))
    return 0


def prepare_render_command() -> int:
    allowed_parent = (ROOT / "tmp/pdfs").resolve()
    for path in (RENDER_DIR, CONTACT_DIR):
        resolved = path.resolve()
        require(resolved.parent == allowed_parent, f"refusing to clean unexpected raster path: {resolved}")
        if resolved.is_dir():
            shutil.rmtree(resolved)
        elif resolved.exists():
            raise ContractError(f"raster target exists but is not a directory: {repo_relative(path)}")
        resolved.mkdir(parents=True, exist_ok=False)
    print(json.dumps({"status": "pass", "prepared": [repo_relative(RENDER_DIR), repo_relative(CONTACT_DIR)]}, sort_keys=True))
    return 0


def validate_contact_sheets(page_count: int) -> dict[str, Any]:
    require(CONTACT_DIR.is_dir(), f"contact-sheet directory missing: {repo_relative(CONTACT_DIR)}")
    files = sorted(path for path in CONTACT_DIR.iterdir() if path.is_file())
    unexpected = [path.name for path in files if CONTACT_NAME.fullmatch(path.name) is None]
    require(not unexpected, f"unexpected contact-sheet files: {unexpected[:8]}")
    numbered = sorted((int(CONTACT_NAME.fullmatch(path.name).group(1)), path) for path in files)
    expected_count = math.ceil(page_count / CONTACT_PAGES_PER_SHEET)
    require([number for number, _ in numbered] == list(range(1, expected_count + 1)), "contact-sheet sequence or count differs")
    rows: list[dict[str, Any]] = []
    for _, path in numbered:
        payload = path.read_bytes()
        require(payload, f"empty contact sheet: {path.name}")
        with Image.open(path) as image:
            image.verify()
        rows.append({"path": repo_relative(path), "bytes": len(payload), "sha256": sha256(payload)})
    digest = hashlib.sha256()
    for row in rows:
        digest.update(f"{Path(str(row['path'])).name}\t{row['bytes']}\t{row['sha256']}\n".encode("utf-8"))
    return {
        "path_pattern": repo_relative(CONTACT_DIR / "contact-NN.png"),
        "files": len(rows),
        "bytes": sum(int(row["bytes"]) for row in rows),
        "ordered_manifest_sha256": digest.hexdigest(),
        "pages_per_sheet": CONTACT_PAGES_PER_SHEET,
        "expected_files": expected_count,
    }


def validate_final_inputs() -> dict[str, Any]:
    expected_config = json_bytes(command_config())
    require(
        CONFIG_RECEIPT.is_file() and CONFIG_RECEIPT.read_bytes() == expected_config,
        "pipeline configuration receipt is absent or stale",
    )
    config_identity = identity(CONFIG_RECEIPT)
    final_identity = identity(FINAL_PDF)
    run1_identity = identity(RUN1_PDF)
    require(
        final_identity["bytes"] == run1_identity["bytes"]
        and final_identity["sha256"] == run1_identity["sha256"],
        "saved run-one and final run-two normalized bytes differ",
    )
    run1 = read_json(RUN1_RECEIPT, "run-one receipt")
    run2 = read_json(RUN2_RECEIPT, "run-two receipt")
    for number, value, artifact in ((1, run1, run1_identity), (2, run2, final_identity)):
        require(value.get("status") == "pass" and value.get("run") == number, f"run-{number} receipt is not passing")
        require(value.get("bytes") == artifact["bytes"] and value.get("sha256") == artifact["sha256"], f"run-{number} artifact identity differs")
    require(run2.get("byte_identical_to_run_1") is True, "run-two receipt does not prove normalized-byte identity")
    require(run1.get("pages") == run2.get("pages"), "run receipt page counts differ")
    page_count = int(run2["pages"])
    require(page_count > 0, "PDF page count is not positive")
    validate_transcript(RUN1_LOG)
    validate_transcript(RUN2_LOG)
    facts = pdf_facts(FINAL_PDF)
    require(facts["pages"] == page_count, "final PDF page count differs from run receipts")
    require(facts["page_sizes_points"] == [{"width": EXPECTED_PAGE_SIZE[0], "height": EXPECTED_PAGE_SIZE[1], "pages": page_count}], "final PDF is not uniformly US Letter")
    require(facts["rotations"] == {"0": page_count}, "final PDF contains rotated pages")

    structure = read_json(STRUCTURE_RECEIPT, "PDF structure receipt")
    require(structure.get("status") == "pass" and structure.get("failures") == [], "PDF structure receipt did not pass")
    require(structure.get("artifact", {}).get("path") == repo_relative(FINAL_PDF), "structure receipt PDF path differs")
    require(structure.get("artifact", {}).get("bytes") == final_identity["bytes"] and structure.get("artifact", {}).get("sha256") == final_identity["sha256"], "structure receipt PDF identity differs")
    require(structure.get("pages") == page_count, "structure receipt page count differs")
    require(structure.get("annotations", {}).get("relative_uri_targets") == [], "structure receipt contains relative URIs")
    labels = structure.get("page_labels", {}).get("/Nums") if isinstance(structure.get("page_labels"), dict) else None
    require(labels == [0, {"/S": "/r"}, MAINMATTER_PHYSICAL_PAGE - 1, {"/S": "/D"}], "structure receipt page labels differ")
    outlines = structure.get("outlines", {})
    entries = outlines.get("entries", []) if isinstance(outlines, dict) else []
    require(isinstance(entries, list) and outlines.get("count", 0) >= MINIMUM_OUTLINES, "outline census is implausibly small")
    require(outlines.get("max_depth", 0) >= 1, "outline hierarchy has no nested entries")
    require(outlines.get("replacement_character_titles") == [], "outline title replacement characters remain")
    require(all(isinstance(row.get("physical_page"), int) and 1 <= row["physical_page"] <= page_count for row in entries), "outline destination lies outside PDF")
    extraction = structure.get("text_extraction", {})
    require(extraction.get("errors") == [], "PDF text extraction errors remain")
    require(extraction.get("replacement_characters") == 0 and extraction.get("cid_literals") == 0, "PDF text extraction contains replacement/CID literals")
    require(extraction.get("empty_pages") == INTENTIONAL_BLANK_PAGES, "text-empty page census differs from intentional blank page")
    require(int(extraction.get("characters", 0)) >= page_count * MINIMUM_TEXT_CHARACTERS_PER_PAGE, "extracted text volume is implausibly small")

    visual = read_json(VISUAL_RECEIPT, "all-page visual receipt")
    require(visual.get("status") == "pass" and visual.get("failures") == [], "all-page visual receipt did not pass")
    visual_pdf = visual.get("pdf", {})
    require(visual_pdf.get("bytes") == final_identity["bytes"] and visual_pdf.get("sha256") == final_identity["sha256"] and visual_pdf.get("pages") == page_count, "visual receipt PDF identity differs")
    require(visual.get("build_log") == identity(RUN2_LOG), "visual receipt is not bound to the strict run-two log")
    render_evidence = visual.get("render_evidence", {})
    require(render_evidence.get("renderer") == EXPECTED_RENDERER_LABEL, "visual receipt renderer label differs")
    require(render_evidence.get("resolution_dpi") == RENDER_DPI, "visual receipt render resolution differs")
    require(render_evidence.get("page_image_dimensions_pixels") == [1020, 1320], "visual receipt page-image dimensions differ from US Letter at 120 dpi")
    render = render_evidence.get("page_images", {})
    require(render.get("path_pattern") == repo_relative(RENDER_DIR / "page-NNN.png"), "all-page render path pattern differs")
    require(render.get("files") == page_count and int(render.get("bytes", 0)) > 0 and SHA256_RE.fullmatch(str(render.get("ordered_manifest_sha256", ""))) is not None, "all-page Poppler render inventory differs")
    checks = visual.get("checks", {})
    for key in ("pdf_render_page_census", "page_image_dimensions", "intentional_blank_page_3", "edge_content", "render_freshness", "concurrent_mutation_guard"):
        require(checks.get(key) == "pass", f"visual pixel-layout check did not pass: {key}")
    require(visual.get("pixel_analysis", {}).get("unexpected_blank_physical_pages") == [], "visual sweep found unexpected blank pages")
    require(visual.get("pixel_analysis", {}).get("edge_touching_physical_pages") == [], "visual sweep found edge-touching content")
    contacts = validate_contact_sheets(page_count)
    return {
        "config_identity": config_identity,
        "final_identity": final_identity,
        "page_count": page_count,
        "facts": facts,
        "run1": run1,
        "run2": run2,
        "structure": structure,
        "visual": visual,
        "contacts": contacts,
    }


def final_payload() -> bytes:
    value = validate_final_inputs()
    final_identity = value["final_identity"]
    structure = value["structure"]
    visual = value["visual"]
    page_count = value["page_count"]
    receipt = {
        "schema_version": 1,
        "status": "pass",
        "failures": [],
        "artifact": {**final_identity, "pages": page_count, "page_size_points": list(EXPECTED_PAGE_SIZE)},
        "pipeline_configuration": value["config_identity"],
        "deterministic_builds": {
            "source_date_epoch": SOURCE_DATE_EPOCH,
            "normalized_byte_identical": True,
            "mainmatter_physical_page": MAINMATTER_PHYSICAL_PAGE,
            "run_1": identity(RUN1_RECEIPT),
            "run_2": identity(RUN2_RECEIPT),
            "run_1_log": identity(RUN1_LOG),
            "run_2_log": identity(RUN2_LOG),
            "fatal_tex_patterns": [],
        },
        "structure": {
            "receipt": identity(STRUCTURE_RECEIPT),
            "outlines": structure["outlines"]["count"],
            "outline_max_depth": structure["outlines"]["max_depth"],
            "extracted_characters": structure["text_extraction"]["characters"],
            "empty_text_pages": structure["text_extraction"]["empty_pages"],
            "relative_uri_targets": [],
            "epsilon_delta_https_annotation_count": value["facts"]["epsilon_delta_https_annotation_count"],
            "page_labels": value["facts"]["page_labels"],
            "tagged": bool(structure.get("accessibility", {}).get("struct_tree_present") or structure.get("accessibility", {}).get("marked")),
        },
        "all_page_visual": {
            "receipt": identity(VISUAL_RECEIPT),
            "renderer": visual["render_evidence"]["renderer"],
            "resolution_dpi": visual["render_evidence"]["resolution_dpi"],
            "page_images": visual["render_evidence"]["page_images"],
            "blank_pages": visual["pixel_analysis"]["blank_physical_pages"],
            "sparse_nonblocking_pages": visual["non_blocking_flags"]["sparse_nonblank_physical_pages"],
            "minimum_margins": visual["pixel_analysis"]["minimum_observed_margins_pixels_at_120_dpi"],
            "contact_sheets": value["contacts"],
        },
        "checks": {
            "two_clean_strict_builds": True,
            "identical_normalized_pdf_bytes": True,
            "positive_page_count_uniform_us_letter": True,
            "mainmatter_page_7_labels": True,
            "epsilon_delta_uri_rewrite_exact": True,
            "no_relative_uri_annotations": True,
            "outline_census_and_destinations_sane": True,
            "text_extraction_sane": True,
            "all_page_poppler_render_complete": True,
            "pixel_layout_sweep_pass": True,
            "contact_sheet_inventory_complete": True,
        },
        "caveat": "The PDF may remain untagged; the localized HTML reader is the primary accessible surface.",
    }
    return json_bytes(receipt)


def finalize_command(check: bool) -> int:
    payload = final_payload()
    if check:
        require(FINAL_RECEIPT.is_file() and FINAL_RECEIPT.read_bytes() == payload, "compact final PDF receipt differs")
    else:
        atomic_write(FINAL_RECEIPT, payload)
    value = json.loads(payload)
    print(json.dumps({"status": "pass", "check_only": check, "pdf": value["artifact"], "output": {"path": repo_relative(FINAL_RECEIPT), "bytes": len(payload), "sha256": sha256(payload)}}, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    config_parser = subparsers.add_parser("config", help="write or check the non-executing pipeline configuration")
    config_parser.add_argument("--check", action="store_true")
    record_parser = subparsers.add_parser("record-run", help="record one already-completed strict normalized build")
    record_parser.add_argument("run", type=int, choices=(1, 2))
    record_parser.add_argument("--check", action="store_true")
    subparsers.add_parser("prepare-render", help="clear and recreate only the exact task-local render/contact directories")
    finalize_parser = subparsers.add_parser("finalize", help="write or check the compact complete PDF QA receipt")
    finalize_parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "config":
            return config_command(args.check)
        if args.command == "record-run":
            return record_run_command(args.run, args.check)
        if args.command == "prepare-render":
            return prepare_render_command()
        if args.command == "finalize":
            return finalize_command(args.check)
        raise ContractError(f"unknown command: {args.command}")
    except ContractError as exc:
        raise SystemExit(f"PDF pipeline gate failed: {exc}") from exc


if __name__ == "__main__":
    raise SystemExit(main())
