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


def normalize_pdf(
    pdf_path: Path,
    mainmatter_physical_page: int,
    uri_rewrites: dict[str, str],
) -> str:
    """Normalize labels and rewrite explicitly declared relative URI targets.

    ``mainmatter_physical_page`` is one-based.  Pages before it use lowercase
    Roman labels; that page begins the Arabic sequence at 1.  PreTeXt's current
    LaTeX output can reset ``\\thepage`` before the final contents page is
    shipped, which otherwise makes the embedded viewer labels one page early.

    PreTeXt emits an HTML-relative URI unchanged into PDF annotations.  Such a
    link is not portable with a downloaded PDF, so callers may declare an
    exact source-to-public-URL rewrite.  Only exact declared targets change.
    """

    from PyPDF2 import PdfReader, PdfWriter
    from PyPDF2.generic import (
        ArrayObject,
        DictionaryObject,
        NameObject,
        NumberObject,
        TextStringObject,
    )

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

    rewrite_counts = {source: 0 for source in uri_rewrites}
    for page in writer.pages:
        annotations = page.get("/Annots")
        if annotations is None:
            continue
        if hasattr(annotations, "get_object"):
            annotations = annotations.get_object()
        for reference in annotations:
            annotation = reference.get_object()
            action = annotation.get("/A")
            if action is None:
                continue
            if hasattr(action, "get_object"):
                action = action.get_object()
            uri = action.get("/URI")
            if uri is None:
                continue
            source = str(uri)
            if source in uri_rewrites:
                action[NameObject("/URI")] = TextStringObject(uri_rewrites[source])
                rewrite_counts[source] += 1

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
        observed_uris: list[str] = []
        for page in check.pages:
            annotations = page.get("/Annots")
            if annotations is None:
                continue
            if hasattr(annotations, "get_object"):
                annotations = annotations.get_object()
            for reference in annotations:
                annotation = reference.get_object()
                action = annotation.get("/A")
                if action is None:
                    continue
                if hasattr(action, "get_object"):
                    action = action.get_object()
                uri = action.get("/URI")
                if uri is not None:
                    observed_uris.append(str(uri))
        for source, target in uri_rewrites.items():
            if rewrite_counts[source] == 0:
                raise RuntimeError(f"declared URI rewrite source absent: {source}")
            if source in observed_uris:
                raise RuntimeError(f"relative URI survived normalization: {source}")
            if observed_uris.count(target) != rewrite_counts[source]:
                raise RuntimeError(
                    "URI rewrite verification failed for "
                    f"{source}: expected {rewrite_counts[source]} target annotations, "
                    f"found {observed_uris.count(target)}"
                )
        os.replace(temporary, pdf_path)
    finally:
        if temporary.exists():
            temporary.unlink()

    label_message = (
        "PDF PAGE LABELS NORMALIZED: lowercase Roman through physical page "
        f"{mainmatter_physical_page - 1}; Arabic 1 begins on physical page "
        f"{mainmatter_physical_page}."
    )
    if not uri_rewrites:
        return label_message
    rewrite_message = "; ".join(
        f"{source} -> {target} ({rewrite_counts[source]} annotations)"
        for source, target in uri_rewrites.items()
    )
    return label_message + "\nPDF URI TARGETS REWRITTEN: " + rewrite_message + "."


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
    parser.add_argument(
        "--rewrite-uri",
        action="append",
        default=[],
        metavar="SOURCE=TARGET",
        help=(
            "rewrite one exact PDF URI annotation target; may be repeated. "
            "This does not alter the HTML source link."
        ),
    )
    args = parser.parse_args()

    uri_rewrites: dict[str, str] = {}
    for declaration in args.rewrite_uri:
        if "=" not in declaration:
            parser.error(f"--rewrite-uri requires SOURCE=TARGET, got {declaration!r}")
        source, target = declaration.split("=", 1)
        if not source or not target:
            parser.error(f"--rewrite-uri requires nonempty SOURCE and TARGET")
        if source in uri_rewrites and uri_rewrites[source] != target:
            parser.error(f"conflicting rewrites declared for {source!r}")
        uri_rewrites[source] = target

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
            message = normalize_pdf(
                args.expect_pdf,
                args.mainmatter_physical_page,
                uri_rewrites,
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
