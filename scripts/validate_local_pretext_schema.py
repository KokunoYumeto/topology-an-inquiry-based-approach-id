#!/usr/bin/env python3
"""Validate one local PreTeXt source and its XInclude closure against pinned RelaxNG."""

from __future__ import annotations

import argparse
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import sys

from lxml import etree


XI = "{http://www.w3.org/2001/XInclude}include"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def identity(path: Path, display: str) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": display, "bytes": len(data), "sha256": sha256(data)}


def closure(entry: Path, repo: Path) -> list[Path]:
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    pending = [entry.resolve()]
    seen: set[Path] = set()
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        if not current.is_file() or repo.resolve() not in (current, *current.parents):
            raise SystemExit(f"invalid local XInclude closure member: {current}")
        seen.add(current)
        document = etree.parse(str(current), parser)
        for include in document.iter(XI):
            href = include.get("href")
            if not href or "://" in href or href.startswith(("/", "\\")):
                raise SystemExit(f"nonlocal or empty XInclude in {current}: {href}")
            pending.append((current.parent / href).resolve())
    return sorted(seen, key=lambda path: path.relative_to(repo).as_posix().casefold())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--resource-commit", required=True)
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[1]
    source = (repo / args.source).resolve(strict=True)
    schema = Path(args.schema).resolve(strict=True)
    output = (repo / args.output).resolve()
    for label, path in (("source", source), ("output", output)):
        if repo.resolve() not in (path, *path.parents):
            raise SystemExit(f"{label} must remain inside the repository")

    parser_xml = etree.XMLParser(resolve_entities=False, no_network=True)
    document = etree.parse(str(source), parser_xml)
    members = closure(source, repo)
    document.xinclude()
    schema_doc = etree.parse(str(schema), parser_xml)
    validator = etree.RelaxNG(schema_doc)
    valid = validator.validate(document)
    diagnostics = [
        {
            "filename": item.filename,
            "line": item.line,
            "column": item.column,
            "level": item.level_name,
            "message": item.message,
        }
        for item in validator.error_log
    ]
    report = {
        "schema_version": 1,
        "status": "pass" if valid and not diagnostics else "fail",
        "source": identity(source, source.relative_to(repo).as_posix()),
        "schema": identity(schema, "pretext-user-cache/schema/pretext.rng"),
        "pretext_resource_commit": args.resource_commit,
        "runtime": {
            "python": sys.version.split()[0],
            "pretext": version("pretext"),
            "lxml": list(etree.LXML_VERSION),
        },
        "expanded_element_count": sum(
            1 for node in document.getroot().iter() if isinstance(node.tag, str)
        ),
        "diagnostics": diagnostics,
        "xinclude": {
            "all_local": True,
            "closure": [path.relative_to(repo).as_posix() for path in members],
            "closure_file_count": len(members),
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"status": report["status"], "output": args.output, "diagnostics": len(diagnostics)}))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
