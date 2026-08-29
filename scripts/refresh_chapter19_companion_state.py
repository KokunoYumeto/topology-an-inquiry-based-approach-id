#!/usr/bin/env python3
"""Seal the complete Chapter 19 staged companion and stable-ID backend."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PREVIOUS = ROOT / "scripts" / "refresh_chapter18_companion_state.py"
PREVIOUS_SHA256 = "f27427a19decc875208586821951e633b057cbe405f251f798954b2879cd7ee9"


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def replace_once(source: str, old: str, new: str) -> str:
    count = source.count(old)
    if count != 1:
        raise SystemExit(f"Chapter 18 companion adaptation expected one occurrence, found {count}: {old!r}")
    return source.replace(old, new)


def load_adapted_previous() -> dict[str, Any]:
    payload = PREVIOUS.read_bytes()
    actual = sha256(payload)
    if actual != PREVIOUS_SHA256:
        raise SystemExit(f"Chapter 18 companion-state builder changed: expected {PREVIOUS_SHA256}, found {actual}")
    source = payload.decode("utf-8")
    source = source.replace("Chapter 18", "Chapter 19")
    source = source.replace("CHAPTER18", "CHAPTER19")
    source = source.replace("chapter_18", "chapter_19")
    source = source.replace("chapter18", "chapter19")
    source = source.replace("ch18", "ch19")
    source = source.replace("connected_spaces", "path_connected_spaces")
    source = replace_once(source, "EXPECTED_PHYSICAL_PROMPTS = 128", "EXPECTED_PHYSICAL_PROMPTS = 39")
    source = replace_once(source, "EXPECTED_CANONICAL_SOURCE = 128", "EXPECTED_CANONICAL_SOURCE = 39")
    source = replace_once(source, "EXPECTED_GROUPING = 6", "EXPECTED_GROUPING = 2")
    source = replace_once(
        source,
        '("CC BY 4.0", "CC BY-NC-SA 3.0", EXACT_MODEL, "128", "136", "544")',
        '("CC BY 4.0", "CC BY-NC-SA 3.0", EXACT_MODEL, "39", "47", "188")',
    )
    source = replace_once(source, '"unit": "Chapter 19 — Ruang Topologi Terhubung",', '"unit": "Chapter 19 — Ruang Terhubung Lintasan",')
    namespace: dict[str, Any] = {
        "__name__": "_chapter19_companion_state_adaptation",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(source, str(PREVIOUS), "exec"), namespace)
    return namespace


def main() -> int:
    namespace = load_adapted_previous()
    return int(namespace["main"]())


if __name__ == "__main__":
    raise SystemExit(main())
