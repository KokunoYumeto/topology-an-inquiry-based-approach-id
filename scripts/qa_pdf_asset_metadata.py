#!/usr/bin/env python3
"""Verify metadata sanitation and pixel identity for the 20 affected PDFs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

try:
    from PyPDF2 import PdfReader
except ImportError:  # pragma: no cover - newer package name
    from pypdf import PdfReader


MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
NAMES = (
    "Cylinder_identification.pdf",
    "Equivalence.pdf",
    "Euclidean_metric.pdf",
    "HB_cube.pdf",
    "HB_cube_2.pdf",
    "HB_cube_3.pdf",
    "HM_Example.pdf",
    "Klein_identification.pdf",
    "Mobius_identification.pdf",
    "Open_ball_neighborhood.pdf",
    "Quotient_sphere_1.pdf",
    "Subspace_open.pdf",
    "Taxicab.pdf",
    "Torus_identification.pdf",
    "Venn_Diagram_A.pdf",
    "Venn_Diagram_A_complement.pdf",
    "Venn_Diagram_B.pdf",
    "Venn_Diagram_B_complement.pdf",
    "Venn_Diagram_intersection.pdf",
    "Venn_Diagram_union.pdf",
)
ABSOLUTE_USER_PATH = re.compile(
    rb"[A-Za-z]:" + re.escape(bytes([92])) + rb"Users" + re.escape(bytes([92])),
    re.IGNORECASE,
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def page_signature(reader: PdfReader) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for page in reader.pages:
        contents = page.get_contents()
        payload = b"" if contents is None else contents.get_data()
        rows.append(
            {
                "mediabox": [float(value) for value in page.mediabox],
                "cropbox": [float(value) for value in page.cropbox],
                "rotation": int(page.get("/Rotate", 0)),
                "content_sha256": digest(payload),
            }
        )
    return rows


def metadata_text(reader: PdfReader) -> str:
    return "\n".join(str(value) for value in (reader.metadata or {}).values())


def render(path: Path, destination: Path, executable: str) -> bytes:
    prefix = destination / path.stem
    completed = subprocess.run(
        [executable, "-f", "1", "-singlefile", "-r", "150", "-png", str(path), str(prefix)],
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(f"Poppler render failed for {path.name}")
    return prefix.with_suffix(".png").read_bytes()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--authority-assets", required=True, type=Path)
    parser.add_argument("--edition-assets", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    authority = args.authority_assets.resolve(strict=True)
    edition = args.edition_assets.resolve(strict=True)
    pdftoppm = shutil.which("pdftoppm")
    if pdftoppm is None:
        raise SystemExit("pdftoppm is required")

    failures: list[str] = []
    rows: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="o003-pdf-metadata-qa-") as raw:
        temporary = Path(raw)
        before_dir = temporary / "before"
        after_dir = temporary / "after"
        before_dir.mkdir()
        after_dir.mkdir()
        for name in NAMES:
            original_path = authority / name
            current_path = edition / name
            original_data = original_path.read_bytes()
            current_data = current_path.read_bytes()
            original_reader = PdfReader(original_path)
            current_reader = PdfReader(current_path)
            original_signature = page_signature(original_reader)
            current_signature = page_signature(current_reader)
            original_render = render(original_path, before_dir, pdftoppm)
            current_render = render(current_path, after_dir, pdftoppm)
            original_has_path = bool(ABSOLUTE_USER_PATH.search(original_data))
            current_has_path = bool(ABSOLUTE_USER_PATH.search(current_data))
            current_metadata = metadata_text(current_reader)
            current_root = current_reader.trailer.get("/Root")
            current_has_xmp = bool(
                current_root is not None
                and current_root.get_object().get("/Metadata") is not None
            )
            if not original_has_path:
                failures.append(f"expected legacy path marker absent: {name}")
            if current_has_path or current_metadata or current_has_xmp:
                failures.append(f"metadata sanitation failed: {name}")
            if original_signature != current_signature:
                failures.append(f"page content or geometry changed: {name}")
            if original_render != current_render:
                failures.append(f"pixel render changed: {name}")
            rows.append(
                {
                    "name": name,
                    "authority": {"bytes": len(original_data), "sha256": digest(original_data)},
                    "sanitized": {"bytes": len(current_data), "sha256": digest(current_data)},
                    "pages": len(current_reader.pages),
                    "page_signature_sha256": digest(
                        json.dumps(current_signature, sort_keys=True).encode("utf-8")
                    ),
                    "render_150dpi_sha256": digest(current_render),
                    "legacy_absolute_path_present_in_authority": original_has_path,
                    "absolute_path_absent_after_sanitation": not current_has_path,
                    "info_and_xmp_absent_after_sanitation": not current_metadata and not current_has_xmp,
                    "page_and_pixel_identity": original_signature == current_signature and original_render == current_render,
                }
            )

    report = {
        "schema_version": 1,
        "status": "pass" if not failures else "fail",
        "scope": "20 edition-working PDF assets with legacy absolute-path Info metadata",
        "authority_root": "authority/gvsu-pinned/topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9/assets",
        "edition_root": "repo/assets",
        "sanitation": "Info and XMP removed; page content and visual appearance preserved",
        "render": {"engine": "Poppler pdftoppm", "dpi": 150, "pairs_checked": len(rows)},
        "production_provenance": MODEL,
        "assets": rows,
        "failures": failures,
    }
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"status": report["status"], "assets": len(rows), "failures": len(failures)}))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
