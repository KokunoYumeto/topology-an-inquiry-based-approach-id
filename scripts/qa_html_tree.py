#!/usr/bin/env python3
"""Fail-closed local-link and reader-surface audit for a finalized HTML tree."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import posixpath
import re
from urllib.parse import unquote, urlsplit

from lxml import html


LINK_ATTRIBUTES = {
    "a": ("href",),
    "audio": ("src",),
    "iframe": ("src",),
    "img": ("src", "srcset"),
    "link": ("href",),
    "object": ("data",),
    "script": ("src",),
    "source": ("src", "srcset"),
    "video": ("src", "poster"),
}
IGNORED_SCHEMES = {"data", "javascript", "mailto", "tel"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_tree(root: Path) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    total = 0
    html_files = 0
    for path in sorted(
        (item for item in root.rglob("*") if item.is_file()),
        key=lambda item: item.relative_to(root).as_posix().casefold(),
    ):
        relative = path.relative_to(root).as_posix()
        size = path.stat().st_size
        total += size
        if path.suffix.lower() in {".html", ".htm"}:
            html_files += 1
        rows.append({"path": relative, "bytes": size, "sha256": sha256(path)})
    canonical = hashlib.sha256(
        "".join(
            f"{row['path']}\t{row['bytes']}\t{row['sha256']}\n" for row in rows
        ).encode("utf-8")
    ).hexdigest()
    return {
        "canonical_manifest_sha256": canonical,
        "file_count": len(rows),
        "html_files": html_files,
        "total_bytes": total,
    }


def candidate_values(attribute: str, value: str) -> list[str]:
    if attribute != "srcset":
        return [value]
    return [part.strip().split()[0] for part in value.split(",") if part.strip()]


def local_target(root: Path, source: Path, raw: str) -> tuple[Path | None, str | None]:
    parsed = urlsplit(raw)
    if parsed.scheme.lower() in IGNORED_SCHEMES:
        return None, None
    if parsed.scheme.lower() in {"http", "https"} or parsed.netloc:
        return None, parsed.hostname or parsed.netloc
    path = unquote(parsed.path)
    if not path:
        return source, None
    if path.startswith("/"):
        normalized = posixpath.normpath(path.lstrip("/"))
        target = root / Path(normalized)
    else:
        # PreTeXt knowl fragments are injected into their parent page at run
        # time, so their relative links are intentionally rooted at the main
        # reader directory rather than at the physical ``knowl`` directory.
        base = root if source.parent.name == "knowl" else source.parent
        normalized = posixpath.normpath((base.relative_to(root).as_posix() + "/" + path))
        target = root / Path(normalized)
    if path.endswith("/"):
        target = target / "index.html"
    return target, None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--require", action="append", default=[])
    args = parser.parse_args()

    root = args.root.resolve()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    failures: list[str] = []
    external_hosts: Counter[str] = Counter()
    links_checked = 0
    images_checked = 0
    id_cache: dict[Path, set[str]] = {}

    required = [root / Path(value) for value in args.require]
    for path in required:
        if not path.is_file():
            failures.append(f"required reader surface is missing: {path.relative_to(root)}")

    html_paths = sorted((*root.rglob("*.html"), *root.rglob("*.htm")))
    for source in html_paths:
        raw_bytes = source.read_bytes()
        try:
            document = html.fromstring(raw_bytes)
        except Exception as exc:  # pragma: no cover - diagnostic path
            failures.append(f"HTML parse failed: {source.relative_to(root)}: {exc}")
            continue
        lang = (document.get("lang") or "").lower()
        if lang != "id-id":
            failures.append(f"wrong or missing html lang: {source.relative_to(root)}: {lang!r}")
        text = " ".join(document.itertext())
        if re.search(r"\[(?:missing|unknown)[^\]]*\]", text, flags=re.IGNORECASE):
            failures.append(f"localization placeholder: {source.relative_to(root)}")

        for element in document.iter():
            tag = element.tag.lower() if isinstance(element.tag, str) else ""
            for attribute in LINK_ATTRIBUTES.get(tag, ()):
                value = element.get(attribute)
                if not value:
                    continue
                for candidate in candidate_values(attribute, value):
                    links_checked += 1
                    target, host = local_target(root, source, candidate)
                    if host:
                        external_hosts[host.lower()] += 1
                        continue
                    if target is None:
                        continue
                    if tag == "img":
                        images_checked += 1
                    if not target.is_file():
                        failures.append(
                            f"missing local target: {source.relative_to(root)} -> {candidate}"
                        )
                        continue
                    fragment = unquote(urlsplit(candidate).fragment)
                    if fragment and target.suffix.lower() in {".html", ".htm"}:
                        if target not in id_cache:
                            try:
                                target_document = html.fromstring(target.read_bytes())
                                id_cache[target] = {
                                    value for value in target_document.xpath("//@id") if value
                                }
                            except Exception:
                                id_cache[target] = set()
                        if fragment not in id_cache[target]:
                            failures.append(
                                f"missing fragment: {source.relative_to(root)} -> {candidate}"
                            )

    tree = canonical_tree(root)
    for key in ("canonical_manifest_sha256", "file_count", "html_files", "total_bytes"):
        if tree[key] != manifest.get(key):
            failures.append(
                f"manifest mismatch for {key}: {tree[key]} != {manifest.get(key)}"
            )

    report = {
        "schema_version": 1,
        "status": "pass" if not failures else "fail",
        **tree,
        "links_and_assets_checked": links_checked,
        "images_checked": images_checked,
        "external_hosts": dict(sorted(external_hosts.items())),
        "required_surfaces": [path.relative_to(root).as_posix() for path in required],
        "failures": failures,
    }
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
