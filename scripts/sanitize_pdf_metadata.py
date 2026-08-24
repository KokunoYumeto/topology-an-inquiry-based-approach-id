#!/usr/bin/env python3
"""Remove absolute-path metadata from selected PDF assets without changing pages.

The source archive remains the byte-preserving upstream witness.  This script
operates only on the edition's working asset copies and verifies that page
count, page boxes, rotations, and decoded page-content streams are unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import tempfile

try:
    from PyPDF2 import PdfReader, PdfWriter
    from PyPDF2.generic import NameObject
except ImportError:  # pragma: no cover - newer package name
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject


def page_signature(reader: PdfReader) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for page in reader.pages:
        contents = page.get_contents()
        payload = b"" if contents is None else contents.get_data()
        rows.append(
            {
                "mediabox": tuple(float(value) for value in page.mediabox),
                "cropbox": tuple(float(value) for value in page.cropbox),
                "rotation": int(page.get("/Rotate", 0)),
                "content_sha256": hashlib.sha256(payload).hexdigest(),
            }
        )
    return rows


def sanitize(path: Path) -> tuple[str, str]:
    before_bytes = path.read_bytes()
    before_sha = hashlib.sha256(before_bytes).hexdigest()
    reader = PdfReader(path)
    before_pages = page_signature(reader)

    writer = PdfWriter()
    # Add only the page tree and its referenced resources.  Cloning the whole
    # document would leave the old /Info object as unreachable bytes even
    # after removing the trailer reference.
    for page in reader.pages:
        writer.add_page(page)
    writer.metadata = None
    writer.root_object.pop(NameObject("/Metadata"), None)

    with tempfile.NamedTemporaryFile(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False
    ) as stream:
        temporary = Path(stream.name)
        writer.write(stream)
    try:
        rewritten = PdfReader(temporary)
        if page_signature(rewritten) != before_pages:
            raise RuntimeError(f"page content or geometry changed: {path}")
        metadata_text = "\n".join(str(value) for value in (rewritten.metadata or {}).values())
        windows_user_prefix = "C:" + chr(92) + "Users" + chr(92)
        file_uri_prefix = "file:" + ("/" * 3)
        if windows_user_prefix in metadata_text or file_uri_prefix in metadata_text.casefold():
            raise RuntimeError(f"absolute-path metadata remains: {path}")
        root = rewritten.trailer.get("/Root")
        if root is not None and root.get_object().get("/Metadata") is not None:
            raise RuntimeError(f"XMP metadata remains: {path}")
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()

    after_sha = hashlib.sha256(path.read_bytes()).hexdigest()
    return before_sha, after_sha


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    for path in args.paths:
        before, after = sanitize(path.resolve(strict=True))
        print(f"{path.as_posix()}\t{before}\t{after}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
