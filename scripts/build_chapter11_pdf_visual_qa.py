#!/usr/bin/env python3
"""Analyze the existing Chapter 11 PDF raster closure without rebuilding it.

The final receipt is written only when the PDF, its complete page-PNG render,
and an explicitly supplied build log all exist.  ``--check-only`` performs the
same bounded pixel analysis without requiring a log or writing the receipt.
"""

from __future__ import annotations

import argparse
from io import BytesIO
import hashlib
import json
from pathlib import Path
import re
from typing import Any

from PIL import Image

try:
    from PyPDF2 import PdfReader
except ModuleNotFoundError:  # pragma: no cover - runtime-dependent fallback
    from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output/chapters01-11-pdf/chapters_01_11_reader.pdf"
RENDER_DIR = ROOT / "tmp/pdfs/chapter11-render"
OUTPUT = ROOT / "qa/CHAPTER11_PDF_VISUAL_QA.json"
PDF_RELATIVE = "output/chapters01-11-pdf/chapters_01_11_reader.pdf"
RENDER_PATTERN = "tmp/pdfs/chapter11-render/page-NNN.png"
BOUNDARY_LABEL = "Chapter 11"
PAGE_NAME = re.compile(r"page-(\d{3})\.png\Z")

INK_THRESHOLD = 220
OUTER_BAND_PIXELS = 10
SPARSE_INK_FRACTION = 0.002
RENDER_DPI = 120
INTENTIONAL_BLANK_PAGES = {3}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def repo_relative(path: Path) -> str:
    resolved_root = ROOT.resolve()
    resolved = path.resolve()
    try:
        return resolved.relative_to(resolved_root).as_posix()
    except ValueError as exc:
        raise RuntimeError(f"path is outside the repository: {path}") from exc


def identity(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise FileNotFoundError(path)
    data = path.read_bytes()
    return {
        "path": repo_relative(path),
        "bytes": len(data),
        "sha256": sha256_bytes(data),
    }


def normalize_number(value: float) -> int | float:
    rounded = round(value)
    return int(rounded) if abs(value - rounded) < 1e-9 else round(value, 6)


def pdf_facts(path: Path) -> dict[str, Any]:
    reader = PdfReader(str(path))
    if reader.is_encrypted:
        if reader.decrypt("") == 0:
            raise RuntimeError(f"{BOUNDARY_LABEL} PDF is encrypted and cannot be inspected")
    sizes: list[list[int | float]] = []
    rotations: list[int] = []
    for page in reader.pages:
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        sizes.append([normalize_number(width), normalize_number(height)])
        rotations.append(int(page.get("/Rotate", 0)) % 360)
    root = reader.trailer["/Root"]
    mark_info = root.get("/MarkInfo")
    if hasattr(mark_info, "get_object"):
        mark_info = mark_info.get_object()
    marked = bool(mark_info.get("/Marked")) if isinstance(mark_info, dict) else False
    tagged = bool(root.get("/StructTreeRoot")) or marked
    return {
        "pages": len(reader.pages),
        "page_sizes_points": sizes,
        "rotations_degrees": rotations,
        "tagged": tagged,
    }


def expected_pixel_dimensions(
    size_points: list[int | float], rotation: int, dpi: int
) -> tuple[int, int]:
    width = float(size_points[0])
    height = float(size_points[1])
    if rotation in {90, 270}:
        width, height = height, width
    return round(width * dpi / 72), round(height * dpi / 72)


def ordered_manifest_sha256(rows: list[dict[str, object]]) -> str:
    digest = hashlib.sha256()
    for row in rows:
        relative = Path(str(row["path"])).name
        line = f"{relative}\t{row['bytes']}\t{row['sha256']}\n"
        digest.update(line.encode("utf-8"))
    return digest.hexdigest()


def page_files() -> list[tuple[int, Path]]:
    if not RENDER_DIR.is_dir():
        raise FileNotFoundError(RENDER_DIR)
    all_files = sorted(path for path in RENDER_DIR.iterdir() if path.is_file())
    unexpected = [path.name for path in all_files if PAGE_NAME.fullmatch(path.name) is None]
    if unexpected:
        raise RuntimeError(f"unexpected files in {BOUNDARY_LABEL} render directory: {unexpected[:8]}")
    numbered = [(int(PAGE_NAME.fullmatch(path.name).group(1)), path) for path in all_files]
    numbers = [number for number, _ in numbered]
    if len(numbers) != len(set(numbers)):
        raise RuntimeError(f"duplicate physical page numbers in {BOUNDARY_LABEL} render")
    return sorted(numbered)


def analyze_page(number: int, path: Path) -> tuple[dict[str, object], tuple[int, int, int]]:
    stat_before = path.stat()
    data = path.read_bytes()
    stat_after = path.stat()
    if (
        stat_before.st_size != stat_after.st_size
        or stat_before.st_mtime_ns != stat_after.st_mtime_ns
        or stat_after.st_size != len(data)
    ):
        raise RuntimeError(f"render page changed while being read: {path.name}")
    with Image.open(BytesIO(data)) as source:
        source.load()
        gray = source.convert("L")
    width, height = gray.size
    histogram = gray.histogram()
    ink_pixels = sum(histogram[:INK_THRESHOLD])
    ink_fraction = ink_pixels / (width * height)
    mask = gray.point(lambda value: 255 if value < INK_THRESHOLD else 0)
    bbox = mask.getbbox()
    flags: list[str] = []
    if bbox is None:
        margins: dict[str, int] | None = None
        bbox_row: dict[str, int] | None = None
        flags.append("blank")
        if number in INTENTIONAL_BLANK_PAGES:
            flags.append("intentional_blank")
    else:
        left, top, right_exclusive, bottom_exclusive = bbox
        margins = {
            "left": left,
            "right": width - right_exclusive,
            "top": top,
            "bottom": height - bottom_exclusive,
        }
        bbox_row = {
            "left": left,
            "top": top,
            "right_exclusive": right_exclusive,
            "bottom_exclusive": bottom_exclusive,
        }
        if ink_fraction < SPARSE_INK_FRACTION:
            flags.append("sparse")
        if any(value < OUTER_BAND_PIXELS for value in margins.values()):
            flags.append("edge_touching")
    row = {
        "physical_page": number,
        "path": repo_relative(path),
        "bytes": len(data),
        "sha256": sha256_bytes(data),
        "pixel_dimensions": [width, height],
        "ink_pixels": ink_pixels,
        "ink_fraction": round(ink_fraction, 9),
        "ink_bounding_box_pixels": bbox_row,
        "margins_pixels": margins,
        "flags": flags,
    }
    return row, (stat_after.st_size, stat_after.st_mtime_ns, number)


def stable_render_snapshot(
    numbered: list[tuple[int, Path]], snapshots: dict[str, tuple[int, int, int]]
) -> None:
    current = page_files()
    if [(number, path.name) for number, path in current] != [
        (number, path.name) for number, path in numbered
    ]:
        raise RuntimeError(f"{BOUNDARY_LABEL} render file closure changed during analysis")
    for number, path in current:
        stat = path.stat()
        expected = snapshots[path.name]
        if (stat.st_size, stat.st_mtime_ns, number) != expected:
            raise RuntimeError(f"render page changed during analysis: {path.name}")


def minimum_margins(page_rows: list[dict[str, object]]) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for side in ("left", "right", "top", "bottom"):
        candidates = [
            (int(row["margins_pixels"][side]), int(row["physical_page"]))
            for row in page_rows
            if isinstance(row.get("margins_pixels"), dict)
        ]
        pixels, page = min(candidates)
        result[side] = {"pixels": pixels, "physical_page": page}
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--build-log",
        type=Path,
        help="Exact Chapter 11 build log to bind; required unless --check-only is used.",
    )
    parser.add_argument(
        "--renderer-label",
        default="pdftoppm",
        help="Truthful renderer label for the already existing page PNGs.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Analyze current PDF/PNGs and print only a compact summary; write no receipt.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not PDF.is_file():
        raise SystemExit(f"missing {BOUNDARY_LABEL} PDF: {PDF_RELATIVE}")
    numbered = page_files()
    if not numbered:
        raise SystemExit(f"no rendered {BOUNDARY_LABEL} pages at {RENDER_PATTERN}")
    if args.build_log is None and not args.check_only:
        raise SystemExit(f"--build-log is required when writing {OUTPUT.name}")

    build_log: Path | None = None
    if args.build_log is not None:
        build_log = args.build_log
        if not build_log.is_absolute():
            build_log = ROOT / build_log
        repo_relative(build_log)
        if not build_log.is_file():
            raise SystemExit(f"missing {BOUNDARY_LABEL} build log: {repo_relative(build_log)}")

    pdf_stat_before = PDF.stat()
    pdf_row = identity(PDF)
    log_row = identity(build_log) if build_log is not None else None
    facts = pdf_facts(PDF)
    page_count = int(facts["pages"])
    failures: list[str] = []
    expected_numbers = list(range(1, page_count + 1))
    observed_numbers = [number for number, _ in numbered]
    if observed_numbers != expected_numbers:
        missing = sorted(set(expected_numbers) - set(observed_numbers))[:8]
        extra = sorted(set(observed_numbers) - set(expected_numbers))[:8]
        failures.append(f"render census differs from PDF: missing={missing}, extra={extra}")

    page_rows: list[dict[str, object]] = []
    snapshots: dict[str, tuple[int, int, int]] = {}
    for number, path in numbered:
        row, snapshot = analyze_page(number, path)
        page_rows.append(row)
        snapshots[path.name] = snapshot
        if 1 <= number <= page_count:
            expected_dimensions = expected_pixel_dimensions(
                facts["page_sizes_points"][number - 1],
                facts["rotations_degrees"][number - 1],
                RENDER_DPI,
            )
            if tuple(row["pixel_dimensions"]) != expected_dimensions:
                failures.append(
                    f"page {number} dimensions {row['pixel_dimensions']} != "
                    f"expected {list(expected_dimensions)} at {RENDER_DPI} dpi"
                )

    stable_render_snapshot(numbered, snapshots)
    if identity(PDF) != pdf_row or (
        PDF.stat().st_size != pdf_stat_before.st_size
        or PDF.stat().st_mtime_ns != pdf_stat_before.st_mtime_ns
    ):
        raise RuntimeError(f"{BOUNDARY_LABEL} PDF changed during visual analysis")
    if build_log is not None and identity(build_log) != log_row:
        raise RuntimeError(f"{BOUNDARY_LABEL} build log changed during visual analysis")

    blank_pages = [
        int(row["physical_page"])
        for row in page_rows
        if "blank" in row["flags"]
    ]
    sparse_pages = [
        int(row["physical_page"])
        for row in page_rows
        if "sparse" in row["flags"]
    ]
    edge_pages = [
        int(row["physical_page"])
        for row in page_rows
        if "edge_touching" in row["flags"]
    ]
    unexpected_blank = sorted(set(blank_pages) - INTENTIONAL_BLANK_PAGES)
    missing_intentional_blank = sorted(INTENTIONAL_BLANK_PAGES - set(blank_pages))
    if unexpected_blank:
        failures.append(f"unexpected blank physical pages: {unexpected_blank}")
    if missing_intentional_blank:
        failures.append(
            f"intentional blank physical pages contain detected ink: {missing_intentional_blank}"
        )
    if edge_pages:
        failures.append(f"dark pixels touch the {OUTER_BAND_PIXELS}-pixel outer band: {edge_pages}")
    stale_render_pages = [
        number
        for number, path in numbered
        if path.stat().st_mtime_ns < pdf_stat_before.st_mtime_ns
    ]
    if stale_render_pages:
        failures.append(
            "render pages predate the analyzed PDF; rerender required: "
            f"{stale_render_pages[:8]}"
        )

    image_rows = [
        {"path": row["path"], "bytes": row["bytes"], "sha256": row["sha256"]}
        for row in page_rows
    ]
    image_bytes = sum(int(row["bytes"]) for row in image_rows)
    unique_dimensions = sorted({tuple(row["pixel_dimensions"]) for row in page_rows})
    unique_page_sizes = sorted({tuple(size) for size in facts["page_sizes_points"]})
    unique_rotations = sorted(set(facts["rotations_degrees"]))
    status = "pass" if not failures else "fail"
    receipt = {
        "schema_version": 1,
        "status": status,
        "sha256": pdf_row["sha256"],
        "pages": page_count,
        "tagged": facts["tagged"],
        "pdf": {
            **pdf_row,
            "pages": page_count,
            "page_size_points": list(unique_page_sizes[0]) if len(unique_page_sizes) == 1 else None,
            "page_sizes_points": [list(size) for size in unique_page_sizes],
            "rotation_degrees": unique_rotations[0] if len(unique_rotations) == 1 else None,
            "rotations_degrees": unique_rotations,
            "tagged": facts["tagged"],
        },
        "build_log": log_row,
        "render_evidence": {
            "renderer": args.renderer_label,
            "resolution_dpi": RENDER_DPI,
            "page_image_dimensions_pixels": (
                list(unique_dimensions[0]) if len(unique_dimensions) == 1 else None
            ),
            "page_image_dimension_set_pixels": [list(size) for size in unique_dimensions],
            "page_images": {
                "path_pattern": RENDER_PATTERN,
                "files": len(page_rows),
                "bytes": image_bytes,
                "ordered_manifest_sha256": ordered_manifest_sha256(image_rows),
            },
            "manifest_algorithm": (
                "For page images ordered by physical page, SHA-256 of UTF-8 rows: "
                "filename TAB bytes TAB file_sha256 LF."
            ),
            "freshness_gate": "every page PNG modification time is at or after the analyzed PDF",
        },
        "pixel_analysis": {
            "ink_threshold": f"grayscale pixel value below {INK_THRESHOLD}",
            "outer_band_pixels_at_120_dpi": OUTER_BAND_PIXELS,
            "sparse_ink_fraction_below": SPARSE_INK_FRACTION,
            "intentional_blank_physical_pages": sorted(INTENTIONAL_BLANK_PAGES),
            "blank_physical_pages": blank_pages,
            "unexpected_blank_physical_pages": unexpected_blank,
            "sparse_nonblank_physical_pages": sparse_pages,
            "edge_touching_physical_pages": edge_pages,
            "minimum_observed_margins_pixels_at_120_dpi": minimum_margins(page_rows),
            "pages": page_rows,
        },
        "checks": {
            "pdf_render_page_census": "pass" if observed_numbers == expected_numbers else "fail",
            "page_image_dimensions": (
                "pass"
                if not any(" dimensions " in failure for failure in failures)
                else "fail"
            ),
            "intentional_blank_page_3": "pass" if blank_pages == [3] else "fail",
            "sparse_page_sweep": "review_flagged" if sparse_pages else "pass",
            "edge_content": "pass" if not edge_pages else "fail",
            "render_freshness": "pass" if not stale_render_pages else "fail",
            "concurrent_mutation_guard": "pass",
        },
        "non_blocking_flags": {
            "sparse_nonblank_physical_pages": sparse_pages,
            "note": "Sparse pages are reported for review but are not failures by themselves.",
        },
        "failures": failures,
    }

    summary = {
        "status": status,
        "pdf_sha256": pdf_row["sha256"],
        "pdf_pages": page_count,
        "rendered_pages": len(page_rows),
        "blank_pages": blank_pages,
        "sparse_pages": sparse_pages,
        "edge_touching_pages": edge_pages,
        "failures": failures,
    }
    if args.check_only:
        print(json.dumps(summary, sort_keys=True))
        return 0 if status == "pass" else 1

    payload = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    temporary = OUTPUT.with_name(f".{OUTPUT.name}.tmp")
    temporary.write_text(payload, encoding="utf-8", newline="\n")
    temporary.replace(OUTPUT)
    summary.update(
        {
            "output": repo_relative(OUTPUT),
            "output_bytes": OUTPUT.stat().st_size,
            "output_sha256": sha256(OUTPUT),
        }
    )
    print(json.dumps(summary, sort_keys=True))
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
