#!/usr/bin/env python3
"""Analyze the existing cumulative Chapter 12 PDF raster closure.

This is the Chapter 12 configuration of the maintained Chapter 11 pixel-QA
engine.  It never builds or renders the PDF.  ``--check-only`` performs the
bounded analysis without requiring a build log or writing a receipt.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import build_chapter11_pdf_visual_qa as engine


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--build-log",
        type=Path,
        help="Exact Chapter 12 cumulative build log; required unless --check-only is used.",
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


def configure_engine() -> None:
    """Bind the shared, read-only analysis engine to the Chapter 12 closure."""
    engine.__doc__ = __doc__
    engine.ROOT = ROOT
    engine.PDF = ROOT / "output/chapters01-12-pdf/chapters_01_12_reader.pdf"
    engine.RENDER_DIR = ROOT / "tmp/pdfs/chapter12-render"
    engine.OUTPUT = ROOT / "qa/CHAPTER12_PDF_VISUAL_QA.json"
    engine.PDF_RELATIVE = "output/chapters01-12-pdf/chapters_01_12_reader.pdf"
    engine.RENDER_PATTERN = "tmp/pdfs/chapter12-render/page-NNN.png"
    engine.BOUNDARY_LABEL = "Chapter 12"
    # The cumulative wrappers retain the intentional verso blank after the
    # title/frontmatter.  The receipt still verifies that page 3 is actually
    # blank rather than merely trusting this declaration.
    engine.INTENTIONAL_BLANK_PAGES = {3}
    engine.parse_args = parse_args


def main() -> int:
    configure_engine()
    return engine.main()


if __name__ == "__main__":
    raise SystemExit(main())
