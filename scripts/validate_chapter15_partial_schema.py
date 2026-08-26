#!/usr/bin/env python3
"""Validate Chapter 15 in the sealed cumulative Chapters 1--14 context.

The checker inserts the Chapter 15 XInclude in memory immediately after the
admitted Chapter 14 include, expands only the local closure, validates it
against the pinned PreTeXt RelaxNG schema, and writes a portable JSON receipt.
It does not create or imply admission of a cumulative Chapters 1--15 reader.
"""

from __future__ import annotations

import argparse
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import sys

from lxml import etree


XI_NS = "http://www.w3.org/2001/XInclude"
XI = f"{{{XI_NS}}}include"


def identity(path: Path, display: str) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "path": display,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def chapter_closure(entry: Path, repo: Path) -> list[Path]:
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    ordered: list[Path] = []
    pending = [entry.resolve()]
    seen: set[Path] = set()
    while pending:
        current = pending.pop(0)
        if current in seen:
            continue
        if not current.is_file() or repo.resolve() not in (current, *current.parents):
            raise RuntimeError(f"invalid local Chapter 15 include: {current}")
        seen.add(current)
        ordered.append(current)
        tree = etree.parse(str(current), parser)
        additions: list[Path] = []
        for node in tree.iter(XI):
            href = node.get("href")
            if not href or "://" in href or href.startswith(("/", "\\")):
                raise RuntimeError(f"nonlocal Chapter 15 include in {current}: {href}")
            additions.append((current.parent / href).resolve())
        pending[0:0] = additions
    return ordered


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--resource-commit", required=True)
    args = parser.parse_args()

    repo = Path(__file__).resolve().parent.parent
    base = repo / "source" / "chapters_01_14_reader.ptx"
    chapter = repo / "source" / "chap_subspaces.ptx"
    schema = Path(args.schema).resolve(strict=True)
    output = (repo / args.output).resolve()
    if repo.resolve() not in (output, *output.parents):
        raise SystemExit("output must remain inside the repository")

    xml_parser = etree.XMLParser(resolve_entities=False, no_network=True)
    tree = etree.parse(str(base), xml_parser)
    namespace = {"xi": XI_NS}
    prior = tree.xpath(
        '//xi:include[@href="./chap_continuity_topology.ptx"]',
        namespaces=namespace,
    )
    if len(prior) != 1:
        raise RuntimeError("could not identify the unique admitted Chapter 14 include")
    if tree.xpath(
        '//xi:include[@href="./chap_subspaces.ptx"]',
        namespaces=namespace,
    ):
        raise RuntimeError("base wrapper already includes Chapter 15")

    include = etree.Element(XI)
    include.set("href", "./chap_subspaces.ptx")
    prior[0].addnext(include)
    tree.xinclude()

    schema_doc = etree.parse(str(schema), xml_parser)
    validator = etree.RelaxNG(schema_doc)
    valid = validator.validate(tree)
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
    closure = chapter_closure(chapter, repo)
    report = {
        "schema_version": 1,
        "status": "pass" if valid and not diagnostics else "fail",
        "validation_context": (
            "Chapter 15 inserted in memory immediately after Chapter 14 in "
            "the sealed cumulative Chapters 1-14 book wrapper"
        ),
        "base_wrapper": identity(base, base.relative_to(repo).as_posix()),
        "inserted_include": "./chap_subspaces.ptx",
        "chapter_closure": [
            identity(path, path.relative_to(repo).as_posix()) for path in closure
        ],
        "chapter_closure_file_count": len(closure),
        "schema": identity(schema, "pretext-user-cache/schema/pretext.rng"),
        "pretext_resource_commit": args.resource_commit,
        "runtime": {
            "python": sys.version.split()[0],
            "pretext": version("pretext"),
            "lxml": etree.LXML_VERSION,
        },
        "expanded_element_count": sum(
            1 for node in tree.getroot().iter() if isinstance(node.tag, str)
        ),
        "diagnostics": diagnostics,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "output": args.output,
                "diagnostics": len(diagnostics),
            }
        )
    )
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
