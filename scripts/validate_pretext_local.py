#!/usr/bin/env python3
"""Validate a cumulative PreTeXt wrapper against the pinned local RelaxNG schema.

This validator fails closed.  It expands the complete XInclude closure without
network access, validates the expanded tree directly with lxml's RelaxNG
engine, and writes a portable JSON receipt with exact input identities.
"""

from __future__ import annotations

import argparse
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import sys

from lxml import etree


XI = "{http://www.w3.org/2001/XInclude}include"


def identity(path: Path, display: str) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "path": display,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def include_closure(entry: Path, root: Path) -> list[str]:
    """Return the bounded local XML XInclude closure, entry included."""
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    pending = [entry.resolve()]
    seen: set[Path] = set()
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        if not current.is_file():
            raise FileNotFoundError(current)
        if root.resolve() not in (current, *current.parents):
            raise RuntimeError(f"XInclude escaped repository root: {current}")
        seen.add(current)
        tree = etree.parse(str(current), parser)
        for node in tree.iter(XI):
            href = node.get("href")
            if not href:
                raise RuntimeError(f"empty XInclude href in {current}")
            if "://" in href or href.startswith(("/", "\\")):
                raise RuntimeError(f"nonlocal XInclude in {current}: {href}")
            pending.append((current.parent / href).resolve())
    return sorted(path.relative_to(root).as_posix() for path in seen)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--resource-commit", required=True)
    args = parser.parse_args()

    repo = Path(__file__).resolve().parent.parent
    source = (repo / args.source).resolve()
    schema = Path(args.schema).resolve()
    output = (repo / args.output).resolve()
    if repo.resolve() not in (source, *source.parents):
        raise SystemExit("source must remain inside the repository")
    if repo.resolve() not in (output, *output.parents):
        raise SystemExit("output must remain inside the repository")

    closure = include_closure(source, repo)
    xml_parser = etree.XMLParser(resolve_entities=False, no_network=True)
    tree = etree.parse(str(source), xml_parser)
    tree.xinclude()
    schema_doc = etree.parse(str(schema), xml_parser)
    validator = etree.RelaxNG(schema_doc)
    valid = validator.validate(tree)
    diagnostics = [
        {
            "line": entry.line,
            "column": entry.column,
            "level": entry.level_name,
            "message": entry.message,
        }
        for entry in validator.error_log
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
            "lxml": etree.LXML_VERSION,
        },
        "xinclude": {
            "all_local": True,
            "closure_file_count": len(closure),
            "closure": closure,
        },
        "expanded_element_count": sum(1 for node in tree.getroot().iter() if isinstance(node.tag, str)),
        "diagnostics": diagnostics,
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
