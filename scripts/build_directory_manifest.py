#!/usr/bin/env python3
"""Write a deterministic identity manifest for one bounded artifact directory."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--glob", default="**/*")
    parser.add_argument("--label", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--relative-to", type=Path)
    args = parser.parse_args()

    directory = args.directory.resolve()
    relative_root = (args.relative_to or directory).resolve()
    files = sorted(
        (path for path in directory.glob(args.glob) if path.is_file()),
        key=lambda path: path.relative_to(directory).as_posix().casefold(),
    )
    if not files:
        raise SystemExit("no files matched the bounded manifest request")

    rows: list[dict[str, object]] = []
    for path in files:
        relative = path.relative_to(relative_root).as_posix()
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        rows.append({"path": relative, "bytes": len(data), "sha256": digest})

    canonical = hashlib.sha256(
        "".join(
            f"{row['path']}\t{row['bytes']}\t{row['sha256']}\n" for row in rows
        ).encode("utf-8")
    ).hexdigest()

    manifest = {
        "schema_version": 1,
        "label": args.label,
        "source_directory": directory.relative_to(relative_root).as_posix(),
        "glob": args.glob,
        "combined_algorithm": (
            "SHA-256 over UTF-8 lines: relative path, TAB, byte count, TAB, "
            "file SHA-256, LF; paths ordered case-insensitively"
        ),
        "canonical_manifest_sha256": canonical,
        "file_count": len(rows),
        "html_files": sum(
            1 for path in files if path.suffix.lower() in {".html", ".htm"}
        ),
        "total_bytes": sum(int(row["bytes"]) for row in rows),
        "files": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "output": str(args.output),
                "file_count": manifest["file_count"],
                "total_bytes": manifest["total_bytes"],
                "canonical_manifest_sha256": manifest[
                    "canonical_manifest_sha256"
                ],
                "output_sha256": sha256(args.output),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
