#!/usr/bin/env python3
"""Build the fail-closed cumulative Chapters 1-6 source manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parent
OUTPUT = ROOT / "qa" / "CHAPTER06_SOURCE_MANIFEST.json"
AUTHORITY_SOURCE = (
    LANE
    / "authority/gvsu-pinned/topology-0c2d8f614ef87aa00de373f3418146c2f1d13bb9/source"
)

PRIOR_MANIFEST = "qa/CHAPTER05_SOURCE_MANIFEST.json"
PRIOR_MANIFEST_IDENTITY = {
    "bytes": 16_115,
    "sha256": "46971569bd005290aea45d840da8a331f754268b4d08e0e4b0b36daa8cf0b2e7",
}

CHAPTER_ORDER = (
    "chapter_01",
    "chapter_02",
    "chapter_03",
    "chapter_04",
    "chapter_05",
    "chapter_06",
)

CHAPTER_06 = (
    "chap_continuous_functions.ptx",
    "sec_cont_func_intro.ptx",
    "sec_cont_func_btwn.ptx",
    "sec_comp_cont_func.ptx",
    "sec_cont_func_summ.ptx",
    "sec_cont_func_exer.ptx",
)

COMPANION_WRAPPER = "companion/chapter_06_continuous_functions_self_study.ptx"
COMPANION_FRAGMENTS = (
    "companion/chapter_06_source_guides.ptx",
    "companion/chapter_06_exercise_guides_a.ptx",
    "companion/chapter_06_exercise_guides_b.ptx",
    "companion/chapter_06_mastery.ptx",
)
LOCAL_LAB = "assets/o003-epsilon-delta-lab.html"
ALIAS_MAP = "backend/chapter_06_entry_aliases.csv"
BACKEND_MANIFEST = "backend/chapter_06_companion_manifest.json"

NEW_ADDITIVE = (
    COMPANION_WRAPPER,
    *COMPANION_FRAGMENTS,
    ALIAS_MAP,
    BACKEND_MANIFEST,
    LOCAL_LAB,
)

CHAPTER_06_IMPLEMENTATION = (
    "scripts/qa_source_translation.py",
    "scripts/qa_chapter06_companion.py",
    "scripts/build_chapter06_backend.py",
    "scripts/build_chapter06_source_manifest.py",
    "scripts/build_pretext_pdf_strict.py",
    "assets/o003-readable-layout.css",
    "xsl/custom-latex.xsl",
    "source/chapters_01_06_reader.ptx",
    "project.ptx",
    "companion/RIGHTS.md",
    "LICENSES.md",
)

# Only these cumulative implementation surfaces may legitimately differ from
# their Chapter 5 identities. All other inherited implementation bytes remain
# immutable evidence. Each permitted change is still preserved as an explicit
# old/current identity pair in the Chapter 6 manifest.
EVOLVING_PRIOR_IMPLEMENTATION = {
    "scripts/qa_source_translation.py": (
        "Chapter 6 external-xref and approved-attribute-change validation"
    ),
    "scripts/build_pretext_pdf_strict.py": (
        "Windows-safe transcript handling and verified deterministic PDF "
        "page-label normalization"
    ),
    "assets/o003-readable-layout.css": "cumulative reader layout update",
    "xsl/custom-latex.xsl": "cumulative PDF reader implementation update",
    "project.ptx": "addition of the cumulative Chapters 1-6 build targets",
}

EVOLVING_PRIOR_ADDITIVE = {
    "companion/RIGHTS.md": (
        "append-only cumulative rights note for the Chapter 6 companion and "
        "original epsilon-delta lab"
    ),
}

CONTROL_INPUTS = (
    "00_control/TERMINOLOGY.csv",
    "00_control/SOURCE_CORRECTIONS.csv",
)

EXPECTED_TERM_IDS = {f"O003-T{number:03d}" for number in range(93, 98)}
EXPECTED_CORRECTION_IDS = {f"O003-C{number:03d}" for number in range(57, 66)}
EXPECTED_EXTERNAL_XREFS = {
    "ex_MS_discrete",
    "ex_GLB_rational",
    "ex_GLB_irrational",
}
CHAPTER_06_AUTHORITY_COMBINED_SHA256 = (
    "6872eac9f833addfc84b711f5d1509ec00116db884ca509dc73f8f2763bd581a"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise FileNotFoundError(path)
    return {"bytes": path.stat().st_size, "sha256": sha256(path)}


def file_row(relative: str, prefix: str = "repo/") -> dict[str, object]:
    path = ROOT / relative
    return {"path": f"{prefix}{relative}", **identity(path)}


def authority_row(name: str) -> dict[str, object]:
    return {"path": f"authority/source/{name}", **identity(AUTHORITY_SOURCE / name)}


def control_row(relative: str) -> dict[str, object]:
    return {"path": relative, **identity(LANE / relative)}


def read_json(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"{path} does not contain a JSON object")
    return value


def require_dict(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} is not an object")
    return value


def require_list(value: object, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise RuntimeError(f"{label} is not a list")
    return value


def require_pass(report: dict[str, Any], label: str) -> None:
    if report.get("status") != "pass":
        raise RuntimeError(f"{label} is not passing")


def assert_identity(label: str, expected: object, current: dict[str, object]) -> None:
    expected_row = require_dict(expected, label)
    if (
        expected_row.get("sha256") != current["sha256"]
        or expected_row.get("bytes") != current["bytes"]
    ):
        raise RuntimeError(
            f"{label} identity is stale: expected "
            f"{expected_row.get('bytes')} bytes/{expected_row.get('sha256')}, "
            f"found {current['bytes']} bytes/{current['sha256']}"
        )


def safe_relative_path(value: object, label: str) -> str:
    text = str(value).replace("\\", "/")
    if text.startswith("repo/"):
        text = text.removeprefix("repo/")
    candidate = PurePosixPath(text)
    if not text or candidate.is_absolute() or ".." in candidate.parts:
        raise RuntimeError(f"unsafe or missing {label} path: {value!r}")
    return candidate.as_posix()


def assert_path(label: str, reported: object, expected: str) -> None:
    if safe_relative_path(reported, label) != expected:
        raise RuntimeError(f"{label} path is stale: {reported!r} != {expected!r}")


def combined_named_files(
    root: Path, names: list[str] | tuple[str, ...]
) -> str:
    digest = hashlib.sha256()
    for name in names:
        path = root / name
        if not path.is_file():
            raise FileNotFoundError(path)
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return digest.hexdigest()


def combined_source(names: list[str] | tuple[str, ...]) -> str:
    return combined_named_files(ROOT / "source", names)


def rows_by_path(rows: object, label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for raw_row in require_list(rows, label):
        row = require_dict(raw_row, f"{label} row")
        path = safe_relative_path(row.get("path"), f"{label} row")
        if path in result:
            raise RuntimeError(f"{label} contains duplicate path {path}")
        result[path] = row
    return result


def validate_html_tree(
    html_root: Path, manifest: dict[str, Any]
) -> tuple[int, int, int]:
    if not html_root.is_dir():
        raise FileNotFoundError(html_root)
    rows = rows_by_path(manifest.get("files"), "canonical HTML manifest files")
    actual_paths = {
        path.relative_to(html_root).as_posix()
        for path in html_root.rglob("*")
        if path.is_file()
    }
    if set(rows) != actual_paths:
        missing = sorted(set(rows) - actual_paths)[:10]
        unexpected = sorted(actual_paths - set(rows))[:10]
        raise RuntimeError(
            "canonical HTML manifest closure disagrees with output tree; "
            f"missing={missing}, unexpected={unexpected}"
        )

    total_bytes = 0
    html_files = 0
    for relative, expected in rows.items():
        current = identity(html_root / relative)
        assert_identity(f"HTML output {relative}", expected, current)
        total_bytes += int(current["bytes"])
        html_files += relative.lower().endswith(".html")

    counts = {
        "file_count": len(rows),
        "html_files": html_files,
        "total_bytes": total_bytes,
    }
    for key, current in counts.items():
        if manifest.get(key) != current:
            raise RuntimeError(
                f"canonical HTML manifest has stale {key}: "
                f"{manifest.get(key)!r} != {current!r}"
            )
    return len(rows), html_files, total_bytes


def backend_asset_identity(
    backend: dict[str, Any], expected_path: str
) -> dict[str, Any]:
    matches: list[dict[str, Any]] = []
    for raw_row in require_list(backend.get("assets"), "Chapter 6 backend assets"):
        row = require_dict(raw_row, "Chapter 6 backend asset")
        if safe_relative_path(row.get("path"), "Chapter 6 backend asset") == expected_path:
            matches.append(row)
    if len(matches) != 1:
        raise RuntimeError(
            f"Chapter 6 backend must bind exactly one {expected_path} asset; "
            f"found {len(matches)}"
        )
    row = matches[0]
    nested = row.get("identity")
    return require_dict(nested, "Chapter 6 backend asset identity") if nested else row


def main() -> int:
    prior_manifest_row = file_row(PRIOR_MANIFEST)
    assert_identity(
        "published Chapters 1-5 source manifest",
        PRIOR_MANIFEST_IDENTITY,
        prior_manifest_row,
    )
    prior = read_json(PRIOR_MANIFEST)
    require_pass(prior, "prior Chapters 1-5 source manifest")

    expected_authority = {
        "commit": "0c2d8f614ef87aa00de373f3418146c2f1d13bb9",
        "tree": "7df245934eedb7174d5ff8af18afff5a7abdde78",
        "archive_sha256": "d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3",
        "controlling_core_license": "CC-BY-NC-SA-3.0",
    }
    prior_authority = require_dict(prior.get("authority"), "prior authority")
    for key, expected in expected_authority.items():
        if prior_authority.get(key) != expected:
            raise RuntimeError(f"prior authority drifted for {key}")

    prior_translated = require_dict(
        prior.get("translated_source"), "prior translated source"
    )
    chapters: dict[str, list[str]] = {}
    translated_source: dict[str, object] = {}
    inherited_names: list[str] = []
    seen_source_paths: set[str] = set()
    for chapter in CHAPTER_ORDER[:-1]:
        prior_chapter = require_dict(
            prior_translated.get(chapter), f"prior translated source {chapter}"
        )
        old_rows = require_list(prior_chapter.get("files"), f"prior {chapter} files")
        names: list[str] = []
        current_rows: list[dict[str, object]] = []
        for raw_old in old_rows:
            old = require_dict(raw_old, f"prior {chapter} file")
            relative = safe_relative_path(old.get("path"), f"prior {chapter} file")
            if not relative.startswith("source/"):
                raise RuntimeError(f"prior source path is outside repo/source: {relative}")
            if relative in seen_source_paths:
                raise RuntimeError(f"duplicate inherited source path: {relative}")
            seen_source_paths.add(relative)
            name = relative.removeprefix("source/")
            current = file_row(relative)
            assert_identity(f"previously admitted source {relative}", old, current)
            names.append(name)
            current_rows.append(current)
        current_combined = combined_source(names)
        if prior_chapter.get("combined_sha256") != current_combined:
            raise RuntimeError(f"previously admitted combined source drifted: {chapter}")
        chapters[chapter] = names
        inherited_names.extend(names)
        translated_source[chapter] = {
            **prior_chapter,
            "files": current_rows,
            "combined_sha256": current_combined,
            "admission": (
                "identity preserved from repo/qa/CHAPTER05_SOURCE_MANIFEST.json"
            ),
        }

    inherited_cumulative = combined_source(inherited_names)
    if prior_translated.get("cumulative_combined_sha256") != inherited_cumulative:
        raise RuntimeError("prior cumulative Chapters 1-5 source identity drifted")

    source_qa = read_json("qa/CHAPTER06_SOURCE_QA.json")
    companion_qa = read_json("qa/CHAPTER06_COMPANION_QA.json")
    backend = read_json(BACKEND_MANIFEST)
    require_pass(source_qa, "Chapter 6 source QA")
    require_pass(companion_qa, "Chapter 6 companion QA")
    if "status" in backend:
        require_pass(backend, "Chapter 6 backend")
    if source_qa.get("failures") != []:
        raise RuntimeError("Chapter 6 source QA has recorded failures")
    if companion_qa.get("failures") != [] or companion_qa.get("missing_xrefs") != []:
        raise RuntimeError("Chapter 6 companion QA has failures or missing xrefs")

    source_qa_rows: dict[str, dict[str, Any]] = {}
    for raw in require_list(source_qa.get("files"), "Chapter 6 source QA files"):
        row = require_dict(raw, "Chapter 6 source QA file")
        name = str(row.get("file", ""))
        if not name or name in source_qa_rows:
            raise RuntimeError(f"missing or duplicate Chapter 6 source QA file: {name!r}")
        source_qa_rows[name] = row
    if set(source_qa_rows) != set(CHAPTER_06):
        raise RuntimeError("Chapter 6 source QA closure disagrees with the frozen six files")

    chapter_06_rows: list[dict[str, object]] = []
    chapter_06_authority_rows: list[dict[str, object]] = []
    for name in CHAPTER_06:
        qa_row = source_qa_rows[name]
        current = file_row(f"source/{name}")
        translated_qa = require_dict(
            qa_row.get("translated"), f"Chapter 6 translated QA {name}"
        )
        assert_path(
            f"Chapter 6 translated QA {name}", translated_qa.get("path"), name
        )
        assert_identity(f"Chapter 6 translated QA {name}", translated_qa, current)

        current_authority = authority_row(name)
        authority_qa = require_dict(
            qa_row.get("authority"), f"Chapter 6 authority QA {name}"
        )
        assert_path(f"Chapter 6 authority QA {name}", authority_qa.get("path"), name)
        assert_identity(
            f"Chapter 6 authority QA {name}", authority_qa, current_authority
        )
        chapter_06_rows.append(current)
        chapter_06_authority_rows.append(current_authority)

    chapter_06_authority_combined = combined_named_files(
        AUTHORITY_SOURCE, CHAPTER_06
    )
    if chapter_06_authority_combined != CHAPTER_06_AUTHORITY_COMBINED_SHA256:
        raise RuntimeError("frozen Chapter 6 authority combined identity drifted")
    chapter_06_combined = combined_source(CHAPTER_06)
    if source_qa.get("combined_translated_sha256") != chapter_06_combined:
        raise RuntimeError("Chapter 6 combined source hash disagrees with source QA")
    approved_external = set(
        require_list(
            source_qa.get("approved_external_xref_targets"),
            "Chapter 6 approved external xrefs",
        )
    )
    if approved_external != EXPECTED_EXTERNAL_XREFS:
        raise RuntimeError(
            "Chapter 6 external-xref exception closure disagrees with the frozen set"
        )
    if source_qa.get("missing_xref_targets") != []:
        raise RuntimeError("Chapter 6 source QA has unresolved internal xrefs")

    chapters["chapter_06"] = list(CHAPTER_06)
    translated_source["chapter_06"] = {
        "files": chapter_06_rows,
        "authority_files": chapter_06_authority_rows,
        "authority_combined_sha256": chapter_06_authority_combined,
        "combined_sha256": chapter_06_combined,
        "source_qa": "repo/qa/CHAPTER06_SOURCE_QA.json",
        "xml_ids": source_qa.get("xml_ids"),
        "xrefs": source_qa.get("xrefs"),
        "approved_external_xrefs": sorted(approved_external),
        "exercises": sum(int(source_qa_rows[name]["exercises"]) for name in CHAPTER_06),
        "tasks": sum(int(source_qa_rows[name]["tasks"]) for name in CHAPTER_06),
        "activities_and_explorations": sum(
            int(source_qa_rows[name]["activities_and_explorations"])
            for name in CHAPTER_06
        ),
    }
    cumulative_names = [
        name for chapter in CHAPTER_ORDER for name in chapters[chapter]
    ]
    translated_source["cumulative_combined_sha256"] = combined_source(cumulative_names)
    translated_source["combined_algorithm"] = (
        "SHA-256 over each ordered source filename, one NUL byte, then exact file bytes"
    )

    source_qa_row = file_row("qa/CHAPTER06_SOURCE_QA.json")
    companion_qa_row = file_row("qa/CHAPTER06_COMPANION_QA.json")
    backend_row = file_row(BACKEND_MANIFEST)
    companion_row = file_row(COMPANION_WRAPPER)
    lab_row = file_row(LOCAL_LAB)
    alias_row = file_row(ALIAS_MAP)

    assert_path(
        "Chapter 6 companion QA wrapper",
        require_dict(companion_qa.get("companion"), "Chapter 6 companion QA wrapper").get(
            "path"
        ),
        COMPANION_WRAPPER,
    )
    assert_identity(
        "Chapter 6 companion QA wrapper", companion_qa["companion"], companion_row
    )

    qa_fragments = rows_by_path(
        companion_qa.get("fragments"), "Chapter 6 companion QA fragments"
    )
    if set(qa_fragments) != set(COMPANION_FRAGMENTS):
        raise RuntimeError("Chapter 6 companion QA fragment closure is stale")
    for relative in COMPANION_FRAGMENTS:
        assert_identity(
            f"Chapter 6 companion QA fragment {relative}",
            qa_fragments[relative],
            file_row(relative),
        )

    companion_source_qa = require_dict(
        companion_qa.get("source_qa"), "Chapter 6 companion source-QA identity"
    )
    assert_path(
        "Chapter 6 companion source-QA identity",
        companion_source_qa.get("path"),
        "qa/CHAPTER06_SOURCE_QA.json",
    )
    assert_identity(
        "Chapter 6 companion source-QA identity", companion_source_qa, source_qa_row
    )

    companion_assets = require_dict(
        companion_qa.get("assets"), "Chapter 6 companion QA assets"
    )
    companion_lab = require_dict(
        companion_assets.get("local_lab"), "Chapter 6 companion QA local lab"
    )
    assert_path("Chapter 6 companion QA local lab", companion_lab.get("path"), LOCAL_LAB)
    assert_identity("Chapter 6 companion QA local lab", companion_lab, lab_row)
    if companion_assets.get("local_lab_integration_links") != 2:
        raise RuntimeError("Chapter 6 local lab must have exactly two integration links")
    if companion_assets.get("local_lab_runtime_dependencies") != []:
        raise RuntimeError("Chapter 6 local lab is not offline/self-contained")
    if companion_assets.get("described_images") != 2:
        raise RuntimeError("Chapter 6 must preserve two Indonesian image descriptions")

    entry_counts = require_dict(
        companion_qa.get("entry_counts"), "Chapter 6 companion entry counts"
    )
    expected_entry_counts = {
        "source_prompt_guide": 39,
        "mastery_check": 6,
        "total": 45,
    }
    for key, expected in expected_entry_counts.items():
        if entry_counts.get(key) != expected:
            raise RuntimeError(f"Chapter 6 companion coverage is stale for {key}")
    if companion_qa.get("source_prompt_total") != 39:
        raise RuntimeError("Chapter 6 companion must map all 39 source prompts")
    reveal_counts = require_dict(
        companion_qa.get("reveal_counts"), "Chapter 6 companion reveal counts"
    )
    if any(reveal_counts.get(kind) != 45 for kind in ("hint", "answer", "solution")):
        raise RuntimeError("Chapter 6 companion does not provide 45 staged reveals")
    companion_entries = require_list(
        companion_qa.get("entries"), "Chapter 6 companion entries"
    )
    companion_ids = [
        str(require_dict(row, "Chapter 6 companion entry").get("id", ""))
        for row in companion_entries
    ]
    if len(companion_ids) != 45 or len(set(companion_ids)) != 45 or "" in companion_ids:
        raise RuntimeError("Chapter 6 companion IDs are missing or duplicated")

    backend_authority = require_dict(
        backend.get("authority"), "Chapter 6 backend authority"
    )
    for key, expected in expected_authority.items():
        if backend_authority.get(key) != expected:
            raise RuntimeError(f"Chapter 6 backend authority drifted for {key}")
    if (
        backend_authority.get("chapter_ordered_sha256")
        != chapter_06_authority_combined
    ):
        raise RuntimeError("Chapter 6 backend authority source closure is stale")

    component = require_dict(backend.get("component"), "Chapter 6 backend component")
    assert_path("Chapter 6 backend companion", component.get("path"), COMPANION_WRAPPER)
    assert_path(
        "Chapter 6 backend companion rights note",
        component.get("rights_note"),
        "companion/RIGHTS.md",
    )
    assert_identity(
        "Chapter 6 backend companion",
        component.get("identity"),
        companion_row,
    )
    backend_fragments = rows_by_path(
        component.get("fragments"), "Chapter 6 backend fragments"
    )
    if set(backend_fragments) != set(COMPANION_FRAGMENTS):
        raise RuntimeError("Chapter 6 backend fragment closure is stale")
    for relative in COMPANION_FRAGMENTS:
        current = file_row(relative)
        assert_identity(
            f"Chapter 6 backend fragment {relative}",
            backend_fragments[relative],
            current,
        )
    backend_alias = require_dict(
        component.get("entry_alias_map"), "Chapter 6 backend alias map"
    )
    assert_path(
        "Chapter 6 backend alias map", backend_alias.get("path"), ALIAS_MAP
    )
    assert_identity("Chapter 6 backend alias map", backend_alias, alias_row)
    backend_source_qa = require_dict(
        backend.get("translated_unit_source_qa"),
        "Chapter 6 backend source-QA receipt",
    )
    assert_path(
        "Chapter 6 backend source-QA receipt",
        backend_source_qa.get("path"),
        "qa/CHAPTER06_SOURCE_QA.json",
    )
    assert_identity(
        "Chapter 6 backend source-QA receipt", backend_source_qa, source_qa_row
    )
    if (
        backend_source_qa.get("status") != "pass"
        or backend_source_qa.get("combined_translated_sha256")
        != chapter_06_combined
    ):
        raise RuntimeError("Chapter 6 backend source-QA metadata is stale")

    backend_companion_qa = require_dict(
        backend.get("companion_qa"), "Chapter 6 backend companion-QA receipt"
    )
    assert_path(
        "Chapter 6 backend companion-QA receipt",
        backend_companion_qa.get("path"),
        "qa/CHAPTER06_COMPANION_QA.json",
    )
    assert_identity(
        "Chapter 6 backend companion-QA receipt",
        backend_companion_qa,
        companion_qa_row,
    )
    if backend_companion_qa.get("status") != "pass":
        raise RuntimeError("Chapter 6 backend companion-QA metadata is stale")
    backend_lab = backend_asset_identity(backend, LOCAL_LAB)
    assert_identity("Chapter 6 backend local lab", backend_lab, lab_row)
    backend_lab_runtime = require_dict(
        backend_lab.get("runtime"), "Chapter 6 backend local-lab runtime"
    )
    if (
        backend_lab_runtime.get("offline_capable") is not True
        or backend_lab_runtime.get("network_dependencies") != []
        or backend_lab_runtime.get("external_scripts") != []
        or backend_lab_runtime.get("external_stylesheets") != []
    ):
        raise RuntimeError("Chapter 6 backend local lab is not offline closed")
    replacement = require_dict(
        backend.get("external_dependency_replacement"),
        "Chapter 6 external dependency replacement",
    )
    if (
        replacement.get("local_reader_path")
        != "external/o003-epsilon-delta-lab.html"
        or replacement.get("replacement_license") != "CC-BY-4.0"
        or replacement.get("relationship")
        != "independent_open_replacement_not_a_copy"
        or len(
            require_list(
                replacement.get("integration_points"),
                "Chapter 6 lab integration points",
            )
        )
        != 2
    ):
        raise RuntimeError("Chapter 6 local replacement contract is stale")

    backend_entries = require_list(backend.get("entries"), "Chapter 6 backend entries")
    backend_ids = [
        str(require_dict(row, "Chapter 6 backend entry").get("id", ""))
        for row in backend_entries
    ]
    if backend_ids != companion_ids:
        raise RuntimeError("Chapter 6 companion/backend entry order or IDs disagree")

    expected_coverage = {
        "source_prompt_guides": 39,
        "mastery_checks": 6,
        "hints": 45,
        "answers": 45,
        "solutions": 45,
        "active_images_with_id_ID_descriptions": 2,
    }
    backend_coverage = require_dict(
        backend.get("coverage_contract"), "Chapter 6 backend coverage"
    )
    for key, expected in expected_coverage.items():
        if backend_coverage.get(key) != expected:
            raise RuntimeError(f"Chapter 6 backend coverage is stale for {key}")

    current_controls = {
        relative: control_row(relative) for relative in CONTROL_INPUTS
    }
    companion_controls = require_dict(
        companion_qa.get("control_inputs"), "Chapter 6 companion controls"
    )
    backend_controls = require_dict(
        backend.get("control_inputs"), "Chapter 6 backend controls"
    )
    for key, relative, required_ids in (
        ("terminology", "00_control/TERMINOLOGY.csv", EXPECTED_TERM_IDS),
        (
            "source_corrections",
            "00_control/SOURCE_CORRECTIONS.csv",
            EXPECTED_CORRECTION_IDS,
        ),
    ):
        companion_control = require_dict(
            companion_controls.get(key), f"Chapter 6 companion control {key}"
        )
        assert_path(
            f"Chapter 6 companion control {key}",
            companion_control.get("path"),
            relative,
        )
        assert_identity(
            f"Chapter 6 companion control {key}",
            companion_control,
            current_controls[relative],
        )
        if set(require_list(companion_control.get("required_ids"), f"{key} required IDs")) != required_ids:
            raise RuntimeError(f"Chapter 6 companion control {key} ID closure is stale")

        backend_control = require_dict(
            backend_controls.get(key), f"Chapter 6 backend control {key}"
        )
        assert_path(
            f"Chapter 6 backend control {key}", backend_control.get("path"), relative
        )
        assert_identity(
            f"Chapter 6 backend control {key}",
            backend_control,
            current_controls[relative],
        )
        if set(
            require_list(
                backend_control.get("selected_ids"),
                f"Chapter 6 backend control {key} selected IDs",
            )
        ) != required_ids:
            raise RuntimeError(f"Chapter 6 backend control {key} ID closure is stale")

    rights_boundary = require_dict(
        companion_qa.get("rights_boundary"), "Chapter 6 rights boundary"
    )
    rights_row = file_row("companion/RIGHTS.md")
    licenses_row = file_row("LICENSES.md")
    companion_rights = require_dict(
        rights_boundary.get("companion_rights"), "Chapter 6 companion rights note"
    )
    collection_licenses = require_dict(
        rights_boundary.get("collection_licenses"), "Chapter 6 collection licenses"
    )
    assert_path(
        "Chapter 6 companion rights note",
        companion_rights.get("path"),
        "companion/RIGHTS.md",
    )
    assert_identity("Chapter 6 companion rights note", companion_rights, rights_row)
    assert_path(
        "Chapter 6 collection licenses",
        collection_licenses.get("path"),
        "LICENSES.md",
    )
    assert_identity("Chapter 6 collection licenses", collection_licenses, licenses_row)
    if rights_boundary.get("translated_spine_license") != "CC-BY-NC-SA-3.0":
        raise RuntimeError("Chapter 6 translated-spine license boundary drifted")
    if rights_boundary.get("companion_license") != "CC-BY-4.0":
        raise RuntimeError("Chapter 6 companion license boundary drifted")

    backend_rights = require_list(backend.get("rights"), "Chapter 6 backend rights")
    backend_licenses = {
        str(require_dict(row, "Chapter 6 backend rights row").get("license", ""))
        for row in backend_rights
    }
    if not {"CC-BY-NC-SA-3.0", "CC-BY-4.0"}.issubset(backend_licenses):
        raise RuntimeError("Chapter 6 backend does not preserve both license boundaries")

    inherited_additive: list[dict[str, object]] = []
    inherited_additive_updates: list[dict[str, object]] = []
    inherited_additive_paths: set[str] = set()
    for raw_row in require_list(prior.get("additive_components"), "prior additive components"):
        row = require_dict(raw_row, "prior additive component")
        relative = safe_relative_path(row.get("path"), "prior additive component")
        if relative in inherited_additive_paths:
            raise RuntimeError(f"duplicate prior additive component: {relative}")
        current = file_row(relative)
        changed = (
            row.get("bytes") != current["bytes"]
            or row.get("sha256") != current["sha256"]
        )
        if changed and relative not in EVOLVING_PRIOR_ADDITIVE:
            assert_identity(
                f"previously admitted additive component {relative}", row, current
            )
        if changed:
            inherited_additive_updates.append(
                {
                    "path": current["path"],
                    "previous_bytes": row["bytes"],
                    "previous_sha256": row["sha256"],
                    "current": current,
                    "reason": EVOLVING_PRIOR_ADDITIVE[relative],
                }
            )
        inherited_additive_paths.add(relative)
        inherited_additive.append(current)
    if inherited_additive_paths.intersection(NEW_ADDITIVE):
        raise RuntimeError("Chapter 6 additive component duplicates a prior component")

    prior_control_rows = rows_by_path(
        prior.get("control_inputs"), "prior control inputs"
    )
    if set(prior_control_rows) != set(CONTROL_INPUTS):
        raise RuntimeError("prior control-input closure is stale")
    inherited_control_updates = [
        {
            "path": relative,
            "previous_bytes": prior_control_rows[relative]["bytes"],
            "previous_sha256": prior_control_rows[relative]["sha256"],
            "current": current_controls[relative],
            "reason": "append-only cumulative terminology/correction ledger update",
        }
        for relative in CONTROL_INPUTS
    ]

    implementation_by_path: dict[str, dict[str, object]] = {}
    inherited_implementation_updates: list[dict[str, object]] = []
    for raw_row in require_list(
        prior.get("production_implementation"), "prior production implementation"
    ):
        row = require_dict(raw_row, "prior production implementation row")
        relative = safe_relative_path(row.get("path"), "prior implementation row")
        if relative in implementation_by_path:
            raise RuntimeError(f"duplicate prior implementation path: {relative}")
        current = file_row(relative)
        changed = (
            row.get("bytes") != current["bytes"]
            or row.get("sha256") != current["sha256"]
        )
        if changed and relative not in EVOLVING_PRIOR_IMPLEMENTATION:
            raise RuntimeError(f"unapproved inherited implementation drift: {relative}")
        if changed:
            inherited_implementation_updates.append(
                {
                    "path": current["path"],
                    "previous_bytes": row["bytes"],
                    "previous_sha256": row["sha256"],
                    "current": current,
                    "reason": EVOLVING_PRIOR_IMPLEMENTATION[relative],
                }
            )
        implementation_by_path[relative] = current
    for relative in CHAPTER_06_IMPLEMENTATION:
        implementation_by_path[relative] = file_row(relative)

    html_manifest = read_json("qa/CHAPTER06_HTML_MANIFEST.json")
    html_run_1 = read_json("qa/CHAPTER06_HTML_MANIFEST_RUN1.json")
    html_run_2 = read_json("qa/CHAPTER06_HTML_MANIFEST_RUN2.json")
    html_qa = read_json("qa/CHAPTER06_HTML_QA.json")
    browser_qa = read_json("qa/CHAPTER06_BROWSER_QA.json")
    require_pass(html_qa, "Chapter 6 HTML QA")
    require_pass(browser_qa, "Chapter 6 browser QA")
    if html_qa.get("failures") != []:
        raise RuntimeError("Chapter 6 HTML QA has recorded failures")

    canonical_files = require_list(
        html_manifest.get("files"), "canonical Chapter 6 HTML manifest files"
    )
    html_identity_keys = (
        "file_count",
        "html_files",
        "total_bytes",
        "canonical_manifest_sha256",
    )
    for label, report in (
        ("HTML deterministic run 1", html_run_1),
        ("HTML deterministic run 2", html_run_2),
    ):
        if report.get("files") != canonical_files:
            raise RuntimeError(f"{label} file identities disagree with canonical HTML")
        for key in html_identity_keys:
            if report.get(key) != html_manifest.get(key):
                raise RuntimeError(f"{label} disagrees with canonical HTML for {key}")
    for key in html_identity_keys:
        if html_qa.get(key) != html_manifest.get(key):
            raise RuntimeError(f"HTML QA disagrees with canonical HTML for {key}")

    html_root = ROOT / "output" / "chapters01-06-html"
    html_file_count, html_files, html_bytes = validate_html_tree(
        html_root, html_manifest
    )

    pdf_run_1 = read_json("qa/CHAPTER06_PDF_RUN1_HASH.json")
    pdf_run_2 = read_json("qa/CHAPTER06_PDF_RUN2_HASH.json")
    pdf_qa = read_json("qa/CHAPTER06_PDF_VISUAL_QA.json")
    require_pass(pdf_run_1, "Chapter 6 PDF deterministic run 1")
    require_pass(pdf_run_2, "Chapter 6 PDF deterministic run 2")
    require_pass(pdf_qa, "Chapter 6 PDF visual QA")

    pdf_relative = "output/chapters01-06-pdf/chapters_01_06_reader.pdf"
    pdf_path = ROOT / pdf_relative
    pdf_row = file_row(pdf_relative)
    assert_identity("Chapter 6 PDF deterministic run 1", pdf_run_1, pdf_row)
    assert_identity("Chapter 6 PDF deterministic run 2", pdf_run_2, pdf_row)
    pdf_visual_row = require_dict(pdf_qa.get("pdf"), "Chapter 6 PDF visual identity")
    assert_path("Chapter 6 PDF visual identity", pdf_visual_row.get("path"), pdf_relative)
    assert_identity("Chapter 6 PDF visual identity", pdf_visual_row, pdf_row)
    if pdf_qa.get("sha256") != pdf_row["sha256"]:
        raise RuntimeError("Chapter 6 PDF top-level visual-QA hash is stale")
    if not isinstance(pdf_qa.get("pages"), int) or int(pdf_qa["pages"]) <= 0:
        raise RuntimeError("Chapter 6 PDF visual QA has no valid page count")

    qa_receipts = {
        "prior_source_manifest": prior_manifest_row,
        "source": source_qa_row,
        "companion": companion_qa_row,
        "backend": backend_row,
        "html_manifest": file_row("qa/CHAPTER06_HTML_MANIFEST.json"),
        "html_run_1": file_row("qa/CHAPTER06_HTML_MANIFEST_RUN1.json"),
        "html_run_2": file_row("qa/CHAPTER06_HTML_MANIFEST_RUN2.json"),
        "html": file_row("qa/CHAPTER06_HTML_QA.json"),
        "browser": file_row("qa/CHAPTER06_BROWSER_QA.json"),
        "pdf_run_1": file_row("qa/CHAPTER06_PDF_RUN1_HASH.json"),
        "pdf_run_2": file_row("qa/CHAPTER06_PDF_RUN2_HASH.json"),
        "pdf": file_row("qa/CHAPTER06_PDF_VISUAL_QA.json"),
    }

    offline_closed = not bool(html_qa.get("external_hosts"))
    known_caveats: list[str] = []
    if not offline_closed:
        known_caveats.append(
            "The cumulative HTML reader still has recorded remote dependencies; "
            "whole-edition offline closure remains a release gate."
        )
    if pdf_qa.get("tagged") is not True:
        known_caveats.append(
            "PDF is not tagged; HTML remains the primary accessible surface."
        )
    known_caveats.append(
        "Whole-book figure provenance remains a final-release gate; the two active "
        "Chapter 6 figures have Indonesian descriptions."
    )
    known_caveats.append(
        "The original local epsilon-delta lab replaces the unavailable remote "
        "GeoGebra dependency and is separately identified under CC BY 4.0."
    )

    manifest = {
        "schema_version": 1,
        "lane": "O003/C90",
        "locale": "id-ID",
        "boundary": "chapters_01_06_with_separately_licensed_self_study_companions",
        "status": "pass",
        "prior_admission": {
            **prior_manifest_row,
            "published_identity_pinned": True,
        },
        "authority": {
            "work": "Topology: An Inquiry-Based Approach",
            "author": "Steven Schlicker",
            "official_record": "https://scholarworks.gvsu.edu/books/30/",
            "repository": "https://github.com/gvsuoer/topology",
            "chapter_06_ordered_sha256": chapter_06_authority_combined,
            **expected_authority,
        },
        "translated_source": translated_source,
        "additive_components": inherited_additive
        + [file_row(relative) for relative in NEW_ADDITIVE],
        "inherited_additive_updates": inherited_additive_updates,
        "control_inputs": [current_controls[relative] for relative in CONTROL_INPUTS],
        "inherited_control_updates": inherited_control_updates,
        "production_implementation": [
            implementation_by_path[path] for path in sorted(implementation_by_path)
        ],
        "inherited_implementation_updates": inherited_implementation_updates,
        "chapter_06_identity_bundle": {
            "source_qa": source_qa_row,
            "companion_qa": companion_qa_row,
            "backend": backend_row,
            "companion_wrapper": companion_row,
            "companion_fragments": [file_row(path) for path in COMPANION_FRAGMENTS],
            "entry_alias_map": alias_row,
            "local_epsilon_delta_lab": lab_row,
            "cumulative_reader_wrapper": file_row("source/chapters_01_06_reader.ptx"),
            "project": file_row("project.ptx"),
            "rights_note": rights_row,
            "collection_licenses": licenses_row,
        },
        "companion_coverage": {
            "contract": backend_coverage,
            "entry_counts": entry_counts,
            "source_prompt_counts": companion_qa.get("source_prompt_counts"),
            "reveal_counts": reveal_counts,
            "described_images": companion_assets["described_images"],
            "local_interactive_labs": 1,
            "local_lab_integration_links": companion_assets[
                "local_lab_integration_links"
            ],
        },
        "rights": {
            "translated_gvsu_spine": "CC-BY-NC-SA-3.0 (conservative determination)",
            "original_self_study_companions": "CC-BY-4.0",
            "original_epsilon_delta_lab": "CC-BY-4.0",
            "collection_policy": "per-component rights; no flattened license",
            "rights_note": rights_row,
            "collection_licenses": licenses_row,
            "non_endorsement": True,
        },
        "reader_artifacts": {
            "html": {
                "path": "repo/output/chapters01-06-html",
                "file_count": html_file_count,
                "html_files": html_files,
                "bytes": html_bytes,
                "canonical_manifest_sha256": html_manifest[
                    "canonical_manifest_sha256"
                ],
                "manifest": qa_receipts["html_manifest"],
                "deterministic_run_1": qa_receipts["html_run_1"],
                "deterministic_run_2": qa_receipts["html_run_2"],
                "qa": qa_receipts["html"],
                "browser_qa": qa_receipts["browser"],
                "offline_closed": offline_closed,
            },
            "pdf": {
                **pdf_row,
                "pages": pdf_qa["pages"],
                "tagged": pdf_qa.get("tagged"),
                "deterministic_run_1": qa_receipts["pdf_run_1"],
                "deterministic_run_2": qa_receipts["pdf_run_2"],
                "visual_qa": qa_receipts["pdf"],
            },
        },
        "qa_receipts": qa_receipts,
        "known_caveats": known_caveats,
    }

    payload = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(payload, encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": "pass",
                "output": str(OUTPUT),
                "bytes": OUTPUT.stat().st_size,
                "sha256": sha256(OUTPUT),
                "chapter_06_combined_sha256": chapter_06_combined,
                "cumulative_combined_sha256": translated_source[
                    "cumulative_combined_sha256"
                ],
                "html_files": html_file_count,
                "pdf_pages": pdf_qa["pages"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
