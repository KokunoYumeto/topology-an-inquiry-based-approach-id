#!/usr/bin/env python3
"""Analyze the existing cumulative Chapter 17 PDF raster closure.

This is the Chapter 17 configuration of the maintained Chapter 11 pixel-QA
engine. It never builds or renders the PDF and does not create contact sheets.
The deterministic build, hash, structure, all-page Poppler render, and contact
sheet inventory are separate inputs to the final Chapter 17 QA workflow.
``--check-only`` performs the bounded analysis without requiring a build log
or writing a receipt.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import build_chapter11_pdf_visual_qa as engine


ROOT = Path(__file__).resolve().parents[1]

# External pipeline contracts. The shared engine consumes the final PDF,
# all-page render, and explicitly supplied build log; the remaining identities
# are bound by the Chapter 17 source-manifest gate after their own producers run.
BUILD_LOG_RUN1 = ROOT / "qa/CHAPTER17_PDF_BUILD_RUN1.log"
BUILD_LOG_RUN2 = ROOT / "qa/CHAPTER17_PDF_BUILD_RUN2.log"
HASH_RECEIPT_RUN1 = ROOT / "qa/CHAPTER17_PDF_RUN1_HASH.json"
HASH_RECEIPT_RUN2 = ROOT / "qa/CHAPTER17_PDF_RUN2_HASH.json"
STRUCTURE_RECEIPT = ROOT / "qa/CHAPTER17_PDF_STRUCTURE.json"
VISUAL_RECEIPT = ROOT / "qa/CHAPTER17_PDF_VISUAL_QA.json"
RUN1_PDF = ROOT / "tmp/pdfs/chapter17-run1.pdf"
RENDER_DIR = ROOT / "tmp/pdfs/chapter17-render"
CONTACT_SHEET_DIR = ROOT / "tmp/pdfs/chapter17-contact"
CONTACT_SHEET_PATTERN = "tmp/pdfs/chapter17-contact/contact-NN.png"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=(
            "Chapter 17 pipeline contracts: "
            f"{BUILD_LOG_RUN1.relative_to(ROOT).as_posix()}, "
            f"{BUILD_LOG_RUN2.relative_to(ROOT).as_posix()}, "
            f"{HASH_RECEIPT_RUN1.relative_to(ROOT).as_posix()}, "
            f"{HASH_RECEIPT_RUN2.relative_to(ROOT).as_posix()}, "
            f"{STRUCTURE_RECEIPT.relative_to(ROOT).as_posix()}, and the contact-sheet "
            f"inventory {CONTACT_SHEET_PATTERN}."
        ),
    )
    parser.add_argument(
        "--build-log",
        type=Path,
        help=(
            "Exact Chapter 17 cumulative build log; required unless --check-only "
            f"is used (the final run is normally {BUILD_LOG_RUN2.relative_to(ROOT).as_posix()})."
        ),
    )
    parser.add_argument(
        "--renderer-label",
        default="pdftoppm",
        help="Truthful renderer label for the already existing all-page PNG raster.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Analyze current PDF/PNGs and print only a compact summary; write no receipt.",
    )
    return parser.parse_args()


def configure_engine() -> None:
    """Bind the shared, read-only analysis engine to the Chapter 17 closure."""
    engine.__doc__ = __doc__
    engine.ROOT = ROOT
    engine.PDF = ROOT / "output/chapters01-17-pdf/chapters_01_17_reader.pdf"
    engine.RENDER_DIR = RENDER_DIR
    engine.OUTPUT = VISUAL_RECEIPT
    engine.PDF_RELATIVE = "output/chapters01-17-pdf/chapters_01_17_reader.pdf"
    engine.RENDER_PATTERN = "tmp/pdfs/chapter17-render/page-NNN.png"
    engine.BOUNDARY_LABEL = "Chapter 17"
    # The cumulative wrapper retains the intentional verso blank after the
    # title/frontmatter. The engine verifies page 3 is actually blank and then
    # sweeps every remaining physical page for blank or edge-touching output.
    engine.INTENTIONAL_BLANK_PAGES = {3}
    engine.parse_args = parse_args


def main() -> int:
    configure_engine()
    return engine.main()


if __name__ == "__main__":
    raise SystemExit(main())
