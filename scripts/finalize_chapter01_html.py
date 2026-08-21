#!/usr/bin/env python3
"""Deterministically localize the PreTeXt 1.7.5 Chapter 1 HTML boundary."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys

from lxml import etree, html


TEXT = {
    "Contents": "Daftar Isi",
    "Index": "Indeks",
    "You!": "Anda!",
    "Choose avatar": "Pilih avatar",
    "Font family": "Keluarga font",
    "Adjust font": "Sesuaikan font",
    "Size": "Ukuran",
    "Smaller": "Lebih kecil",
    "Larger": "Lebih besar",
    "Width": "Lebar",
    "narrower": "lebih sempit",
    "wider": "lebih lebar",
    "Weight": "Ketebalan",
    "thinner": "lebih tipis",
    "heavier": "lebih tebal",
    "Letter spacing": "Jarak huruf",
    "closer": "lebih rapat",
    "f a r t h e r": "lebih renggang",
    "further": "lebih renggang",
    "Word spacing": "Jarak kata",
    "smaller gap": "celah lebih kecil",
    "larger gap": "celah lebih besar",
    "Line Spacing": "Jarak baris",
    "together": "merapat",
    "apart": "merenggang",
    "Light/dark mode": "Mode terang/gelap",
    "default": "bawaan",
    "pastel": "pastel",
    "twilight": "senja",
    "dark": "gelap",
    "midnight": "tengah malam",
    "Reading ruler": "Penggaris baca",
    "none": "tanpa penggaris",
    "underline": "garis bawah",
    "L-underline": "garis bawah-L",
    "grey bar": "bilah abu-abu",
    "light box": "kotak terang",
    "sunrise": "fajar",
    "sunrise underline": "garis bawah fajar",
    "Motion by:": "Gerakkan dengan:",
    "follow the mouse": "ikuti tetikus",
    "up/down arrows - not yet": "panah atas/bawah — belum tersedia",
    "eye tracking - not yet": "pelacakan mata — belum tersedia",
    "Prev": "Sebelumnya",
    "Previous": "Sebelumnya",
    "Up": "Naik",
    "Top": "Atas",
    "Next": "Berikutnya",
    "Search": "Cari",
    "Front Matter": "Bagian Awal",
    "Back Matter": "Bagian Akhir",
    "Table of Contents": "Daftar Isi",
    "Search Results": "Hasil Pencarian",
    "Search Results:": "Hasil Pencarian:",
    "No results were found.": "Tidak ada hasil yang ditemukan.",
    "No results.": "Tidak ada hasil.",
    "Skip to main content": "Lompat ke konten utama",
    "Jump to:": "Lompat ke:",
}

ATTR = {
    "Show or hide table of contents": "Tampilkan atau sembunyikan daftar isi",
    "Modify user preferences": "Ubah preferensi pengguna",
    "Previous": "Sebelumnya",
    "Up": "Naik",
    "Top": "Atas",
    "Next": "Berikutnya",
    "Search": "Cari",
    "Index": "Indeks",
    "Contents": "Daftar Isi",
}

SKIP_TAGS = {"script", "style", "math", "svg"}
FORBIDDEN_VISIBLE = {
    "Contents",
    "Index",
    "Choose avatar",
    "Font family",
    "Adjust font",
    "Light/dark mode",
    "Reading ruler",
    "Previous",
    "Prev",
    "Next",
    "Search",
    "Front Matter",
    "Back Matter",
    "further",
}


def preserve_space(value: str, replacement: str) -> str:
    match = re.fullmatch(r"(\s*)(.*?)(\s*)", value, flags=re.DOTALL)
    assert match is not None
    return f"{match.group(1)}{replacement}{match.group(3)}"


def local_name(node: etree._Element) -> str:
    tag = node.tag
    if not isinstance(tag, str):
        return ""
    return tag.rsplit("}", 1)[-1].lower()


def transform(path: Path, check_only: bool) -> tuple[int, list[str]]:
    parser = html.HTMLParser(encoding="utf-8", remove_comments=False)
    tree = html.parse(str(path), parser=parser)
    root = tree.getroot()
    changes = 0
    if root.get("lang") != "id-ID":
        root.set("lang", "id-ID")
        changes += 1
    if root.get("xml:lang") != "id-ID":
        root.set("xml:lang", "id-ID")
        changes += 1

    for node in root.iter():
        if local_name(node) in SKIP_TAGS:
            continue
        if node.text is not None:
            key = " ".join(node.text.split())
            if key in TEXT:
                updated = preserve_space(node.text, TEXT[key])
                if updated != node.text:
                    node.text = updated
                    changes += 1
        if node.tail is not None:
            key = " ".join(node.tail.split())
            if key in TEXT:
                updated = preserve_space(node.tail, TEXT[key])
                if updated != node.tail:
                    node.tail = updated
                    changes += 1
        for name in ("aria-label", "title", "placeholder"):
            value = node.get(name)
            if value in ATTR:
                node.set(name, ATTR[value])
                changes += 1

    # The legacy theme emits two linked footer logos without alternate text.
    # Their link titles are stable, useful accessible names.
    for image in root.xpath("//img[not(@alt)]"):
        link_titles = image.xpath("ancestor::a[@title][1]/@title")
        image.set("alt", link_titles[0] if link_titles else "")
        changes += 1

    # The generated index jump bar links every alphabetic letter, including
    # letters absent from this bounded reader.  Downgrade only dead same-page
    # jumps to inert text rather than shipping broken controls.
    ids = set(root.xpath("//*[@id]/@id"))
    for anchor in list(root.xpath("//span[contains(concat(' ', normalize-space(@class), ' '), ' indexjump ')]/a[starts-with(@href, '#')]")):
        fragment = anchor.get("href", "")[1:]
        if fragment and fragment not in ids:
            replacement = etree.Element("span")
            replacement.set("class", "indexjump-missing")
            replacement.text = anchor.text
            replacement.tail = anchor.tail
            anchor.getparent().replace(anchor, replacement)
            changes += 1

    # The redirect page embeds wall-clock build time in a comment.  It has no
    # reader meaning, so normalize just that comment for byte-reproducibility.
    for comment in root.xpath("//comment()"):
        value = comment.text or ""
        if re.search(r"\bon \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}\b", value):
            normalized = re.sub(
                r"\bon \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}\b",
                "build timestamp normalized",
                value,
            )
            if normalized != value:
                comment.text = normalized
                changes += 1

    visible_residue: list[str] = []
    for node in root.iter():
        if local_name(node) in SKIP_TAGS:
            continue
        for value in (node.text, node.tail):
            if value is not None and value.strip() in FORBIDDEN_VISIBLE:
                visible_residue.append(value.strip())
        for name in ("aria-label", "title", "placeholder"):
            value = node.get(name)
            if value in ATTR:
                visible_residue.append(f"{name}={value}")

    if not check_only:
        doctype = tree.docinfo.doctype or "<!DOCTYPE html>"
        data = etree.tostring(
            tree,
            method="html",
            encoding="utf-8",
            doctype=doctype,
            pretty_print=False,
        )
        temporary = path.with_name(f".{path.name}.o003-finalize.tmp")
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        descriptor = os.open(temporary, flags, 0o600)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        except BaseException:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass
            raise
    return changes, visible_residue


def manifest(root: Path) -> dict[str, object]:
    rows = []
    for path in sorted(
        (item for item in root.rglob("*") if item.is_file()),
        key=lambda item: item.relative_to(root).as_posix().casefold(),
    ):
        data = path.read_bytes()
        rows.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    canonical = "".join(
        f"{row['path']}\t{row['bytes']}\t{row['sha256']}\n" for row in rows
    ).encode("utf-8")
    return {
        "schema_version": 1,
        "file_count": len(rows),
        "total_bytes": sum(int(row["bytes"]) for row in rows),
        "canonical_manifest_sha256": hashlib.sha256(canonical).hexdigest(),
        "files": rows,
    }


def main() -> int:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("root", type=Path)
    argument_parser.add_argument("--check-only", action="store_true")
    argument_parser.add_argument("--manifest", type=Path)
    arguments = argument_parser.parse_args()
    root = arguments.root.resolve(strict=True)
    html_files = sorted(root.rglob("*.html"), key=lambda item: item.as_posix().casefold())
    if not html_files:
        raise SystemExit("no HTML files found")

    total_changes = 0
    residue: dict[str, list[str]] = {}
    for path in html_files:
        changes, findings = transform(path, arguments.check_only)
        total_changes += changes
        if findings:
            residue[path.relative_to(root).as_posix()] = findings
    if residue:
        print(json.dumps({"forbidden_visible_residue": residue}, ensure_ascii=False, indent=2))
        return 1
    if arguments.check_only and total_changes:
        print(json.dumps({"unapplied_localizations": total_changes}, ensure_ascii=False))
        return 1

    result = manifest(root)
    result["html_files"] = len(html_files)
    result["localized_nodes_and_attributes"] = total_changes
    if arguments.manifest is not None and not arguments.check_only:
        arguments.manifest.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        arguments.manifest.write_text(payload, encoding="utf-8", newline="\n")
    print(json.dumps(result | {"files": "omitted"}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
