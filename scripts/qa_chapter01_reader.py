#!/usr/bin/env python3
"""Fail-closed structural QA for the localized Chapter 1 HTML boundary."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

from lxml import html


LINK_ATTRS = (("a", "href"), ("a", "data-knowl"), ("img", "src"), ("script", "src"), ("link", "href"),
              ("iframe", "src"), ("source", "src"))
EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}
FORBIDDEN_VISIBLE = re.compile(
    r"\b(?:Contents|Chapter|Appendix|Checkpoint|Exercise|Previous|Next|Search|Top|Item|"
    r"List|Definition|Theorem|Activity|Figure|Statement|Proof|Example|Remark|"
    r"Front Matter|Back Matter|further)\b",
    re.IGNORECASE,
)
FORBIDDEN_PUBLIC_TEXT = (
    re.compile(rb"C:[\\/]Users[\\/]", re.IGNORECASE),
    re.compile(rb"\bFloris\b", re.IGNORECASE),
    re.compile(rb"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(rb"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(rb"sk-[A-Za-z0-9_-]{20,}"),
)
TEXT_SUFFIXES = {".html", ".htm", ".css", ".js", ".json", ".xml", ".txt", ".map"}


def file_rows(root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    paths = sorted(
        (item for item in root.rglob("*") if item.is_file()),
        key=lambda item: item.relative_to(root).as_posix().casefold(),
    )
    for path in paths:
        data = path.read_bytes()
        rows.append({
            "path": path.relative_to(root).as_posix(),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        })
    return rows


def canonical_manifest(rows: list[dict[str, object]]) -> str:
    payload = "".join(
        f"{row['path']}\t{row['bytes']}\t{row['sha256']}\n" for row in rows
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def visible_text(document: html.HtmlElement) -> str:
    chunks = document.xpath(
        "//text()[not(ancestor::script) and not(ancestor::style) and "
        "not(ancestor::math) and not(ancestor::svg) and not(ancestor::code) and "
        "not(ancestor::pre)]"
    )
    return " ".join(" ".join(str(chunk).split()) for chunk in chunks if str(chunk).strip())


def local_target(root: Path, source: Path, raw: str) -> tuple[Path | None, str]:
    parsed = urlsplit(raw)
    if parsed.scheme.lower() in EXTERNAL_SCHEMES or parsed.netloc:
        return None, parsed.hostname or parsed.scheme.lower()
    path_text = unquote(parsed.path)
    relative_parts = source.relative_to(root).parts
    base = root if relative_parts and relative_parts[0].casefold() == "knowl" else source.parent
    target = source if not path_text else (base / path_text)
    try:
        target = target.resolve(strict=False)
        target.relative_to(root)
    except (OSError, ValueError):
        raise ValueError(f"target escapes reader root: {source}: {raw}")
    if target.is_dir():
        target /= "index.html"
    return target, unquote(parsed.fragment)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    root = args.root.resolve(strict=True)
    rows = file_rows(root)
    path_names = [str(row["path"]) for row in rows]
    folded = Counter(name.casefold() for name in path_names)
    failures: list[str] = []
    failures.extend(f"casefold collision: {name}" for name, count in folded.items() if count != 1)
    failures.extend(f"AppleDouble debris: {name}" for name in path_names if Path(name).name.startswith("._"))

    actual_manifest = {
        "schema_version": 1,
        "file_count": len(rows),
        "total_bytes": sum(int(row["bytes"]) for row in rows),
        "canonical_manifest_sha256": canonical_manifest(rows),
        "files": rows,
    }
    expected_manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    expected_core = {
        key: expected_manifest[key]
        for key in ("schema_version", "file_count", "total_bytes", "canonical_manifest_sha256", "files")
    }
    if actual_manifest != expected_core:
        failures.append("HTML tree does not exactly match the frozen manifest")

    documents: dict[Path, html.HtmlElement] = {}
    ids: dict[Path, set[str]] = {}
    html_paths = [root / name for name in path_names if name.lower().endswith((".html", ".htm"))]
    external_hosts: Counter[str] = Counter()
    link_count = 0
    image_count = 0
    for path in html_paths:
        try:
            document = html.parse(str(path)).getroot()
        except Exception as exc:  # pragma: no cover - exact exception is parser-dependent
            failures.append(f"HTML parse failure: {path.relative_to(root)}: {exc}")
            continue
        documents[path.resolve()] = document
        lang = (document.get("lang") or "").strip().lower()
        if lang != "id-id":
            failures.append(f"wrong html lang={lang!r}: {path.relative_to(root)}")
        raw_ids = [value for value in document.xpath("//*[@id]/@id") if value]
        duplicates = [name for name, count in Counter(raw_ids).items() if count > 1]
        if duplicates:
            failures.append(f"duplicate ids in {path.relative_to(root)}: {duplicates[:5]}")
        ids[path.resolve()] = set(raw_ids)
        residue = sorted(set(FORBIDDEN_VISIBLE.findall(visible_text(document))))
        if residue:
            failures.append(f"generated English in {path.relative_to(root)}: {residue}")
        for image in document.xpath("//img"):
            image_count += 1
            if "alt" not in image.attrib:
                failures.append(f"image lacks alt in {path.relative_to(root)}")

    for source, document in documents.items():
        for tag, attribute in LINK_ATTRS:
            for raw in document.xpath(f"//{tag}[@{attribute}]/@{attribute}"):
                if not raw or raw.startswith("//"):
                    if raw.startswith("//"):
                        external_hosts[urlsplit("https:" + raw).hostname or "protocol-relative"] += 1
                    continue
                link_count += 1
                try:
                    target, fragment_or_host = local_target(root, source, raw)
                except ValueError as exc:
                    failures.append(str(exc))
                    continue
                if target is None:
                    external_hosts[fragment_or_host] += 1
                    continue
                if not target.is_file():
                    failures.append(
                        f"missing local target: {source.relative_to(root)} -> {raw}"
                    )
                    continue
                if fragment_or_host and target.suffix.lower() in {".html", ".htm"}:
                    resolved = target.resolve()
                    if resolved not in documents:
                        try:
                            target_doc = html.parse(str(resolved)).getroot()
                            documents[resolved] = target_doc
                            ids[resolved] = set(target_doc.xpath("//*[@id]/@id"))
                        except Exception as exc:
                            failures.append(f"linked HTML parse failure: {target.relative_to(root)}: {exc}")
                            continue
                    if fragment_or_host not in ids.get(resolved, set()):
                        failures.append(
                            f"missing fragment: {source.relative_to(root)} -> {raw}"
                        )

    for row in rows:
        path = root / str(row["path"])
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        data = path.read_bytes()
        for pattern in FORBIDDEN_PUBLIC_TEXT:
            if pattern.search(data):
                failures.append(f"privacy/secret pattern in {path.relative_to(root)}: {pattern.pattern!r}")

    report = {
        "schema_version": 1,
        "status": "pass" if not failures else "fail",
        "file_count": len(rows),
        "total_bytes": actual_manifest["total_bytes"],
        "canonical_manifest_sha256": actual_manifest["canonical_manifest_sha256"],
        "html_files": len(html_paths),
        "links_and_assets_checked": link_count,
        "images_checked": image_count,
        "external_hosts": dict(sorted(external_hosts.items())),
        "failures": failures,
        "audio_widgets_exercised": False,
        "network_widgets_exercised": False,
    }
    payload = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(payload, encoding="utf-8", newline="\n")
    print(payload, end="")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
