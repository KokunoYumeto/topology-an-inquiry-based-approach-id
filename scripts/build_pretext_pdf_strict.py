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


FATAL_TEX = (
    re.compile(r"(?m)^! "),
    re.compile(r"Undefined control sequence", re.IGNORECASE),
    re.compile(r"Emergency stop", re.IGNORECASE),
    re.compile(r"Fatal error occurred", re.IGNORECASE),
    re.compile(r"No pages of output", re.IGNORECASE),
    re.compile(r"(?m)^.*LaTeX Error:.*$"),
    re.compile(r"(?m)^.*Package\s+\S+\s+Error:.*$"),
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("--log", required=True, type=Path)
    parser.add_argument("--expect-pdf", required=True, type=Path)
    parser.add_argument("--source-date-epoch", default="1692057600")
    args = parser.parse_args()

    environment = os.environ.copy()
    environment["SOURCE_DATE_EPOCH"] = args.source_date_epoch
    command = [sys.executable, "-m", "pretext", "build", args.target]
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
    args.log.parent.mkdir(parents=True, exist_ok=True)
    args.log.write_text(transcript, encoding="utf-8", newline="\n")
    print(transcript, end="")

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

    if reasons:
        print("STRICT PDF BUILD REJECTED:", file=sys.stderr)
        for reason in reasons:
            print(f"- {reason}", file=sys.stderr)
        return 1
    print(f"STRICT PDF BUILD PASSED: {args.expect_pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
