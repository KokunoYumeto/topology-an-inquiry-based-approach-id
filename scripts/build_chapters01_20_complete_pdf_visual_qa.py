#!/usr/bin/env python3
"""Analyze the existing complete Chapters 1--20 PDF raster closure.

This is the complete-reader configuration of the maintained Chapter 11 pixel
QA engine.  It never builds or renders the PDF and does not create contact
sheets.  The two strict builds, normalized-byte receipts, structural receipt,
all-page Poppler render, and contact-sheet inventory are separate pipeline
inputs.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import build_chapter11_pdf_visual_qa as engine


ROOT = Path(__file__).resolve().parents[1]

BUILD_LOG_RUN1 = ROOT / "qa/CHAPTERS01_20_COMPLETE_PDF_BUILD_RUN1.log"
BUILD_LOG_RUN2 = ROOT / "qa/CHAPTERS01_20_COMPLETE_PDF_BUILD_RUN2.log"
HASH_RECEIPT_RUN1 = ROOT / "qa/CHAPTERS01_20_COMPLETE_PDF_RUN1_HASH.json"
HASH_RECEIPT_RUN2 = ROOT / "qa/CHAPTERS01_20_COMPLETE_PDF_RUN2_HASH.json"
STRUCTURE_RECEIPT = ROOT / "qa/CHAPTERS01_20_COMPLETE_PDF_STRUCTURE.json"
VISUAL_RECEIPT = ROOT / "qa/CHAPTERS01_20_COMPLETE_PDF_VISUAL_QA.json"
RUN1_PDF = ROOT / "tmp/pdfs/chapters01-20-complete-run1.pdf"
FINAL_PDF = ROOT / "output/chapters01-20-complete-pdf/chapters_01_20_complete_reader.pdf"
RENDER_DIR = ROOT / "tmp/pdfs/chapters01-20-complete-render"
CONTACT_SHEET_DIR = ROOT / "tmp/pdfs/chapters01-20-complete-contact"
CONTACT_SHEET_PATTERN = "tmp/pdfs/chapters01-20-complete-contact/contact-NN.png"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=(
            "Complete-reader pipeline contracts: "
            f"{BUILD_LOG_RUN1.relative_to(ROOT).as_posix()}, "
            f"{BUILD_LOG_RUN2.relative_to(ROOT).as_posix()}, "
            f"{HASH_RECEIPT_RUN1.relative_to(ROOT).as_posix()}, "
            f"{HASH_RECEIPT_RUN2.relative_to(ROOT).as_posix()}, "
            f"{STRUCTURE_RECEIPT.relative_to(ROOT).as_posix()}, and "
            f"{CONTACT_SHEET_PATTERN}."
        ),
    )
    parser.add_argument(
        "--build-log",
        type=Path,
        help=(
            "Exact complete-reader strict build log; required unless "
            "--check-only is used (normally qa/CHAPTERS01_20_COMPLETE_PDF_BUILD_RUN2.log)."
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
        help="Analyze current PDF/PNGs and print a compact summary without writing a receipt.",
    )
    return parser.parse_args()


def configure_engine() -> None:
    engine.__doc__ = __doc__
    engine.ROOT = ROOT
    engine.PDF = FINAL_PDF
    engine.RENDER_DIR = RENDER_DIR
    engine.OUTPUT = VISUAL_RECEIPT
    engine.PDF_RELATIVE = FINAL_PDF.relative_to(ROOT).as_posix()
    engine.RENDER_PATTERN = "tmp/pdfs/chapters01-20-complete-render/page-NNN.png"
    engine.BOUNDARY_LABEL = "complete Chapters 1--20 reader"
    # The cumulative book retains the intentional blank title/frontmatter
    # verso at physical page 3.  Every other physical page must contain ink.
    engine.INTENTIONAL_BLANK_PAGES = {3}
    engine.parse_args = parse_args


def main() -> int:
    configure_engine()
    return engine.main()


if __name__ == "__main__":
    raise SystemExit(main())
