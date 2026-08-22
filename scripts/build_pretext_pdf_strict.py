#!/usr/bin/env python3
"""Build one PreTeXt PDF target and reject hidden TeX failures.

PreTeXt CLI 1.7.5 can return success after XeLaTeX emits a partial PDF.  This
wrapper preserves the complete build transcript and turns TeX errors into a
nonzero process status before an artifact can be admitted.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


FATAL_TEX = (
    re.compile(r"(?m)^! "),
    re.compile(r"Undefined control sequence", re.IGNORECASE),
    re.compile(r"Emergency stop", re.IGNORECASE),
    re.compile(r"Fatal error occurred", re.IGNORECASE),
    re.compile(r"No pages of output", re.IGNORECASE),
    re.compile(r"(?m)^.*LaTeX Error:.*$"),
    re.compile(r"(?m)^.*Package\s+\S+\s+Error:.*$"),
)


def normalize_page_labels(pdf_path: Path, mainmatter_physical_page: int) -> str:
    """Replace a known-bad hyperref label tree with the printed book sequence.

    ``mainmatter_physical_page`` is one-based.  Pages before it use lowercase
    Roman labels; that page begins the Arabic sequence at 1.  PreTeXt's current
    LaTeX output can reset ``\\thepage`` before the final contents page is
    shipped, which otherwise makes the embedded viewer labels one page early.
    """

    from PyPDF2 import PdfReader, PdfWriter
    from PyPDF2.generic import ArrayObject, DictionaryObject, NameObject, NumberObject

    reader = PdfReader(str(pdf_path))
    if reader.is_encrypted:
        raise RuntimeError("cannot normalize labels in an encrypted PDF")
    page_count = len(reader.pages)
    if not 2 <= mainmatter_physical_page <= page_count:
        raise ValueError(
            "mainmatter physical page must be between 2 and "
            f"{page_count}, got {mainmatter_physical_page}"
        )
    main_index = mainmatter_physical_page - 1

    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    if reader.metadata:
        writer.add_metadata(
            {str(key): str(value) for key, value in reader.metadata.items()}
        )
    writer._root_object[NameObject("/PageLabels")] = DictionaryObject(
        {
            NameObject("/Nums"): ArrayObject(
                [
                    NumberObject(0),
                    DictionaryObject({NameObject("/S"): NameObject("/r")}),
                    NumberObject(main_index),
                    DictionaryObject({NameObject("/S"): NameObject("/D")}),
                ]
            )
        }
    )

    temporary = pdf_path.with_name(pdf_path.name + ".page-labels.tmp")
    try:
        with temporary.open("wb") as stream:
            writer.write(stream)
        check = PdfReader(str(temporary))
        if len(check.pages) != page_count:
            raise RuntimeError("page-label normalization changed the page count")
        nums = check.trailer["/Root"]["/PageLabels"]["/Nums"]
        observed = (
            int(nums[0]),
            str(nums[1]["/S"]),
            int(nums[2]),
            str(nums[3]["/S"]),
        )
        expected = (0, "/r", main_index, "/D")
        if observed != expected:
            raise RuntimeError(
                f"page-label verification failed: {observed!r} != {expected!r}"
            )
        os.replace(temporary, pdf_path)
    finally:
        if temporary.exists():
            temporary.unlink()

    return (
        "PDF PAGE LABELS NORMALIZED: lowercase Roman through physical page "
        f"{mainmatter_physical_page - 1}; Arabic 1 begins on physical page "
        f"{mainmatter_physical_page}."
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("--log", required=True, type=Path)
    parser.add_argument("--expect-pdf", required=True, type=Path)
    parser.add_argument("--source-date-epoch", default="1692057600")
    parser.add_argument("--clean", action="store_true")
    parser.add_argument(
        "--mainmatter-physical-page",
        type=int,
        help=(
            "normalize embedded PDF labels so this one-based physical page "
            "begins Arabic page 1 and all earlier pages use lowercase Roman labels"
        ),
    )
    args = parser.parse_args()

    environment = os.environ.copy()
    environment["SOURCE_DATE_EPOCH"] = args.source_date_epoch
    command = [sys.executable, "-m", "pretext", "build", args.target]
    if args.clean:
        command.append("--clean")
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=environment,
        check=False,
    )
    transcript = result.stdout
    reasons: list[str] = []
    if result.returncode != 0:
        reasons.append(f"PreTeXt exited with status {result.returncode}")
    for pattern in FATAL_TEX:
        if pattern.search(transcript):
            reasons.append(f"fatal transcript pattern: {pattern.pattern}")
    if "Success!" not in transcript:
        reasons.append("PreTeXt success marker absent")
    if not args.expect_pdf.is_file() or args.expect_pdf.stat().st_size == 0:
        reasons.append(f"expected nonempty PDF absent: {args.expect_pdf}")

    if not reasons and args.mainmatter_physical_page is not None:
        try:
            message = normalize_page_labels(
                args.expect_pdf, args.mainmatter_physical_page
            )
            transcript = transcript.rstrip("\n") + "\n" + message + "\n"
        except Exception as exc:
            reasons.append(f"PDF page-label normalization failed: {exc}")
            transcript = (
                transcript.rstrip("\n")
                + "\nPDF PAGE LABEL NORMALIZATION FAILED: "
                + str(exc)
                + "\n"
            )

    args.log.parent.mkdir(parents=True, exist_ok=True)
    args.log.write_text(transcript, encoding="utf-8", newline="\n")
    print(transcript, end="")

    if reasons:
        print("STRICT PDF BUILD REJECTED:", file=sys.stderr)
        for reason in reasons:
            print(f"- {reason}", file=sys.stderr)
        return 1
    print(f"STRICT PDF BUILD PASSED: {args.expect_pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
