#!/usr/bin/env python3
"""Bind the four terminology corrections to extracted final-PDF pages."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import unicodedata

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output/chapters01-20-complete-pdf/chapters_01_20_complete_reader.pdf"
OUTPUT = ROOT / "qa/NATIVE_INDONESIAN_TERMINOLOGY_PDF_TEXT_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
TARGETS = (
    (
        "point_set_distance_section",
        "Ruang topologi dapat dikelompokkan ke dalam berbagai kategori berdasarkan seberapa baik jenis-jenis himpunan tertentu dapat dipisahkan.",
    ),
    (
        "function_spaces_intro",
        "sebagai ruang topologi. Pilihan topologi pada ruang fungsi menentukan",
    ),
    (
        "exponential_law_scope",
        "Pada kategori ruang topologi biasa, hipotesis kekompakan lokal pada variabel domain",
    ),
    (
        "integrated_mastery_exercise_09",
        "Misalkan X kompak lokal Hausdorff dan Y ruang topologi.",
    ),
)


class ContractError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def identity(path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(payload), "sha256": digest(payload)}


def normalize(value: str) -> str:
    return " ".join(unicodedata.normalize("NFC", value).split())


def payload() -> bytes:
    require(PDF.is_file(), f"final PDF is missing: {PDF}")
    reader = PdfReader(str(PDF))
    require(len(reader.pages) == 645, f"expected 645 PDF pages, found {len(reader.pages)}")
    texts = [normalize(page.extract_text() or "") for page in reader.pages]
    corpus = "\n".join(texts)
    old_hits = len(re.findall(r"\bruang\s+topologis\b", corpus, flags=re.IGNORECASE))
    require(old_hits == 0, f"obsolete term remains in extracted PDF text: {old_hits}")

    rows = []
    for label, phrase in TARGETS:
        needle = normalize(phrase)
        pages = [number for number, text in enumerate(texts, start=1) if needle in text]
        require(pages, f"terminology phrase is absent from extracted PDF text: {label}")
        rows.append({"label": label, "phrase": phrase, "physical_pages": pages, "matches": len(pages)})

    value = {
        "schema_version": 1,
        "status": "pass",
        "failures": [],
        "pdf": {**identity(PDF), "pages": len(reader.pages)},
        "obsolete_phrase": {"phrase": "ruang topologis", "matches": old_hits},
        "corrected_phrases": rows,
        "normalization": "Unicode NFC; whitespace collapsed before exact phrase matching",
        "production_provenance": MODEL,
    }
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        data = payload()
        if args.check:
            require(OUTPUT.is_file() and OUTPUT.read_bytes() == data, "stored terminology PDF QA differs")
        else:
            temporary = OUTPUT.with_name(f".{OUTPUT.name}.tmp")
            require(not temporary.exists(), f"stale temporary output exists: {temporary}")
            temporary.write_bytes(data)
            require(temporary.read_bytes() == data, "temporary terminology PDF QA readback failed")
            temporary.replace(OUTPUT)
        print(json.dumps({"status": "pass", "check_only": args.check, "output": identity(OUTPUT)}, sort_keys=True))
        return 0
    except (ContractError, OSError, ValueError) as exc:
        raise SystemExit(f"terminology PDF QA failed: {exc}") from exc


if __name__ == "__main__":
    raise SystemExit(main())
