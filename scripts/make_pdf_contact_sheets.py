#!/usr/bin/env python3
"""Create numbered contact sheets from rendered PDF page PNGs."""

from __future__ import annotations

import argparse
from pathlib import Path
import re

from PIL import Image, ImageDraw


def page_number(path: Path) -> int:
    match = re.search(r"(\d+)$", path.stem)
    if match is None:
        raise ValueError(f"page number missing from {path.name}")
    return int(match.group(1))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("render_dir", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--rows", type=int, default=3)
    parser.add_argument("--thumbnail-width", type=int, default=280)
    args = parser.parse_args()

    pages = sorted(args.render_dir.glob("page-*.png"), key=page_number)
    if not pages:
        raise SystemExit("no rendered pages found")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    per_sheet = args.columns * args.rows
    margin = 20
    label_height = 28
    created: list[Path] = []
    for sheet_index, start in enumerate(range(0, len(pages), per_sheet), start=1):
        group = pages[start:start + per_sheet]
        with Image.open(group[0]) as sample:
            thumb_height = round(sample.height * args.thumbnail_width / sample.width)
        width = margin + args.columns * (args.thumbnail_width + margin)
        height = margin + args.rows * (thumb_height + label_height + margin)
        sheet = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(sheet)

        for index, page_path in enumerate(group):
            row, column = divmod(index, args.columns)
            x = margin + column * (args.thumbnail_width + margin)
            y = margin + row * (thumb_height + label_height + margin)
            with Image.open(page_path) as page:
                thumb = page.convert("RGB")
                thumb.thumbnail((args.thumbnail_width, thumb_height), Image.Resampling.LANCZOS)
                sheet.paste(thumb, (x, y + label_height))
            draw.text((x, y + 4), f"Page {page_number(page_path)}", fill="black")

        destination = args.output_dir / f"contact-{sheet_index:02d}.png"
        sheet.save(destination, optimize=True)
        created.append(destination)

    print(f"pages={len(pages)} sheets={len(created)}")
    for path in created:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
