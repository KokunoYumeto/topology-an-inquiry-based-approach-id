#!/usr/bin/env python3
"""Publish one complete-edition maintenance release to the existing Zenodo line.

This is deliberately a narrow, fail-closed publisher.  It advances record
22164668 in concept 22059894 through Zenodo's legacy deposition API, replaces
all inherited draft files with the seven files produced by the complete-edition
package builder, publishes exactly once, and verifies every public byte without
authentication.  Durable state and the final receipt contain no credentials or
authenticated API links.

The access token is accepted only through ``ZENODO_TOKEN``.  There is no token,
API-base, record, concept, metadata, state-path, or receipt-path CLI override.
"""

from __future__ import annotations

import argparse
import copy
from contextlib import contextmanager
from datetime import date, datetime, timezone
import hashlib
import html
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
import time
from typing import Any, Iterable, Iterator, Mapping
from urllib.parse import urljoin, urlparse
import zipfile
import zlib

try:
    import requests
except ModuleNotFoundError as exc:  # pragma: no cover - environment preflight
    raise SystemExit("The 'requests' package is required for Zenodo publication.") from exc


ROOT = Path(__file__).resolve().parents[1]
QA_DIR = ROOT / "qa"
STATE_PATH = QA_DIR / "ZENODO_COMPLETE_MAINTENANCE_STATE.json"
RECEIPT_PATH = QA_DIR / "ZENODO_COMPLETE_MAINTENANCE_PUBLICATION_RECEIPT.md"
LOCK_PATH = QA_DIR / ".zenodo-complete-maintenance.lock"

API_BASE = "https://zenodo.org/api"
PUBLIC_BASE = "https://zenodo.org"
PREDECESSOR_RECORD_ID = 22164668
CONCEPT_RECORD_ID = 22059894
CONCEPT_DOI = "10.5281/zenodo.22059894"
TITLE = "Topologi: Pendekatan Berbasis Inkuiri"
LICENSE_ID = "cc-by-nc-sa-3.0"
LANGUAGE = "ind"

BASE = "topologi-pendekatan-berbasis-inkuiri-edisi-lengkap"
PDF_NAME = f"{BASE}-id.pdf"
HTML_ZIP_NAME = f"{BASE}-html.zip"
SOURCE_ZIP_NAME = f"{BASE}-sumber-backend.zip"
EXPECTED_FILENAMES = (
    PDF_NAME,
    f"{BASE}-checksums.sha256",
    HTML_ZIP_NAME,
    f"{BASE}-licenses.md",
    f"{BASE}-manifest.json",
    f"{BASE}-rights-companion.md",
    SOURCE_ZIP_NAME,
)
MANIFEST_NAME = f"{BASE}-manifest.json"
CHECKSUMS_NAME = f"{BASE}-checksums.sha256"

DESCRIPTION_LEAD = (
    "Edisi Bahasa Indonesia lengkap dari Topology: An Inquiry-Based Approach "
    "karya Steven Schlicker. Rilis ini memuat seluruh 20 bab, 20 pendamping "
    "belajar mandiri, dan delapan modul penyelesaian O003/C90, dengan pembaca "
    "HTML luring/reflow, PDF, sumber PreTeXt, backend modular, dan bukti QA. "
    "Revisi 2026-09-01 menyeragamkan empat pemakaian istilah menjadi ruang "
    "topologi berdasarkan perbandingan terbatas dengan sumber pengajaran "
    "topologi berbahasa Indonesia."
)
DESCRIPTION = (
    f"<p>{html.escape(DESCRIPTION_LEAD)}</p>"
    "<p>Edisi lengkap ini mempertahankan struktur, rumus, aktivitas, latihan, "
    "petunjuk, jawaban, solusi, aset, atribusi, serta pengenal sumber. Paket "
    "rilis menyediakan PDF pembaca, pembaca HTML luring yang dapat direflow, "
    "sumber dan backend yang dapat dilanjutkan, peta hak komponen, manifes, dan "
    "checksum.</p>"
)
NOTES = (
    "<p>Turunan materi GVSU diperlakukan secara konservatif sebagai CC "
    "BY-NC-SA 3.0. Pendamping belajar mandiri dan modul penyelesaian asli "
    "berlisensi CC BY 4.0. Hak berlaku per komponen; tidak ada pelisensian "
    "tunggal yang meratakan seluruh koleksi.</p>"
    "<p>HTML merupakan permukaan aksesibel utama. PDF mungkin belum bertag. "
    "Provenans produksi: OpenAI Codex gpt-5.6-sol, Ultra. Provenans ini tidak "
    "menggantikan kredit penulis sumber, institusi, atau kontributor manusia "
    "dan tidak menyatakan dukungan, persetujuan, sertifikasi, atau afiliasi "
    "resmi.</p>"
)

METADATA_WHITELIST = frozenset(
    {
        "title",
        "upload_type",
        "publication_type",
        "description",
        "creators",
        "access_right",
        "license",
        "publication_date",
        "version",
        "language",
        "keywords",
        "contributors",
        "related_identifiers",
        "notes",
    }
)
SERVER_MANAGED_DEPOSITION_METADATA = frozenset({"doi", "prereserve_doi"})
PHASES = (
    "initialized",
    "draft_created",
    "inherited_files_deleted",
    "metadata_updated",
    "files_uploaded",
    "files_sorted",
    "prepublish_verified",
    "publish_attempted",
    "published",
    "public_readback_verified",
    "receipt_written",
)

PUBLIC_RECORD_BACKOFF_SECONDS = (0, 1, 2, 4, 8, 12, 16, 20)
PUBLIC_FILE_BACKOFF_SECONDS = (0, 2, 5)
PUBLISH_RECONCILE_BACKOFF_SECONDS = (0, 1, 2, 4, 8)
REQUEST_TIMEOUT = (30, 900)
CONTROL_CHARACTER = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
ABSOLUTE_PATH = re.compile(r"(?i)(?:[A-Z]:[\\/]|file://|/(?:home|Users)/)")
CREDENTIAL_MARKER = re.compile(
    r"(?i)(?:authorization\s*:\s*bearer|access_token\s*[=:]|zenodo_token\s*[=:])"
)


class PublicationError(RuntimeError):
    """A fail-closed publication or verification error."""


def canonical_json(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_fingerprint(value: Any) -> str:
    return sha256_bytes(canonical_json(value))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PublicationError(message)


def require_int(value: Any, label: str) -> int:
    require(isinstance(value, int) and not isinstance(value, bool), f"{label} is not an integer")
    return value


def api_record_id(value: Any, label: str) -> int:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str) and re.fullmatch(r"[1-9][0-9]*", value):
        return int(value)
    raise PublicationError(f"{label} is not a record ID")


def strict_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        require(key not in value, f"JSON object repeats key: {key}")
        value[key] = item
    return value


def reject_nonfinite_json(value: str) -> Any:
    raise PublicationError(f"JSON contains a non-finite number: {value}")


def is_link_like(path: Path) -> bool:
    if path.is_symlink():
        return True
    is_junction = getattr(path, "is_junction", None)
    if callable(is_junction) and is_junction():
        return True
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    try:
        attributes = getattr(os.lstat(path), "st_file_attributes", 0)
    except OSError:
        return False
    return bool(reparse_flag and attributes & reparse_flag)


@contextmanager
def publication_lock() -> Iterator[None]:
    """Hold one non-blocking, process-scoped lock for the publication transaction."""

    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    handle = LOCK_PATH.open("a+b")
    handle.seek(0, os.SEEK_END)
    if handle.tell() == 0:
        handle.write(b"\0")
        handle.flush()
        os.fsync(handle.fileno())
    handle.seek(0)
    try:
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:  # pragma: no cover - the publisher's production host is Windows
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except (BlockingIOError, OSError) as exc:
        handle.close()
        raise PublicationError(
            "another complete-maintenance publication process holds the repository lock"
        ) from exc

    try:
        yield
    finally:
        try:
            handle.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:  # pragma: no cover - the publisher's production host is Windows
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        finally:
            handle.close()


def validate_public_scalar(label: str, value: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{label} is empty")
    require(value == value.strip(), f"{label} has leading or trailing whitespace")
    require(not CONTROL_CHARACTER.search(value), f"{label} contains a control character")
    require(not ABSOLUTE_PATH.search(value), f"{label} contains a local absolute path")
    require(not CREDENTIAL_MARKER.search(value), f"{label} contains a credential marker")
    return value


def validate_version(raw: str) -> str:
    value = validate_public_scalar("version", raw)
    require(len(value) <= 100, "version is longer than 100 characters")
    require(
        re.fullmatch(r"[0-9A-Za-z][0-9A-Za-z._+-]*", value) is not None,
        "version must use only letters, digits, '.', '_', '+', and '-'",
    )
    return value


def validate_publication_date(raw: str) -> str:
    value = validate_public_scalar("publication date", raw)
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise PublicationError("publication date must be YYYY-MM-DD") from exc
    require(parsed.isoformat() == value, "publication date must be canonical YYYY-MM-DD")
    return value


def file_identity(path: Path) -> dict[str, Any]:
    md5 = hashlib.md5(usedforsecurity=False)
    sha256 = hashlib.sha256()
    total = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            total += len(chunk)
            md5.update(chunk)
            sha256.update(chunk)
    return {"bytes": total, "md5": md5.hexdigest(), "sha256": sha256.hexdigest()}


def safe_zip_member_name(raw: Any, archive_name: str) -> str:
    require(isinstance(raw, str) and bool(raw), f"{archive_name} has an empty member name")
    require("\0" not in raw, f"{archive_name} has a NUL in a member name")
    require(not CONTROL_CHARACTER.search(raw), f"{archive_name} has a control character in a member name")
    require("\\" not in raw, f"{archive_name} has a backslash member path: {raw!r}")
    path = PurePosixPath(raw)
    require(not path.is_absolute(), f"{archive_name} has an absolute member path: {raw!r}")
    require(
        bool(path.parts)
        and all(part not in ("", ".", "..") for part in path.parts)
        and path.as_posix() == raw,
        f"{archive_name} has a non-canonical member path: {raw!r}",
    )
    require(
        not re.match(r"^[A-Za-z]:", path.parts[0]),
        f"{archive_name} has a drive-qualified member path: {raw!r}",
    )
    windows_reserved = {
        "con",
        "prn",
        "aux",
        "nul",
        *(f"com{index}" for index in range(1, 10)),
        *(f"lpt{index}" for index in range(1, 10)),
    }
    for part in path.parts:
        require(":" not in part, f"{archive_name} has an alternate-stream member path: {raw!r}")
        require(
            not part.endswith((" ", ".")),
            f"{archive_name} has a Windows-ambiguous member path: {raw!r}",
        )
        require(
            part.split(".", 1)[0].casefold() not in windows_reserved,
            f"{archive_name} has a reserved member path: {raw!r}",
        )
    require(not raw.endswith("/"), f"{archive_name} contains a directory entry: {raw!r}")
    return raw


def manifest_payload_rows(
    manifest: Mapping[str, Any], identities: Mapping[str, Mapping[str, Any]]
) -> dict[str, Mapping[str, Any]]:
    expected = set(EXPECTED_FILENAMES) - {MANIFEST_NAME, CHECKSUMS_NAME}
    raw_rows = manifest.get("files")
    require(isinstance(raw_rows, list), "package manifest files field is not a list")
    rows: dict[str, Mapping[str, Any]] = {}
    for raw_row in raw_rows:
        require(isinstance(raw_row, dict), "package manifest files list has a non-object")
        name = raw_row.get("path")
        require(isinstance(name, str), "package manifest file row has no path")
        require(name in expected, f"package manifest has an unexpected payload path: {name}")
        require(name not in rows, f"package manifest repeats a payload path: {name}")
        require(
            require_int(raw_row.get("bytes"), f"package manifest byte count for {name}")
            == identities[name]["bytes"],
            f"package manifest byte count differs: {name}",
        )
        digest = raw_row.get("sha256")
        require(
            isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest) is not None,
            f"package manifest SHA-256 is malformed: {name}",
        )
        require(digest == identities[name]["sha256"], f"package manifest SHA-256 differs: {name}")
        rows[name] = raw_row
    require(set(rows) == expected, "package manifest payload inventory is not exact")
    return rows


def validate_zip_file(path: Path, manifest_row: Mapping[str, Any]) -> None:
    archive_name = path.name
    expected_count = require_int(
        manifest_row.get("entry_count"), f"package manifest ZIP entry count for {archive_name}"
    )
    expected_bytes = require_int(
        manifest_row.get("uncompressed_bytes"),
        f"package manifest ZIP uncompressed byte count for {archive_name}",
    )
    expected_canonical = manifest_row.get("canonical_entry_sha256")
    require(
        manifest_row.get("deterministic_double_build") is True,
        f"package manifest lacks deterministic ZIP evidence: {archive_name}",
    )
    require(expected_count > 0, f"{archive_name} has no expected entries")
    require(expected_bytes > 0, f"{archive_name} has no expected uncompressed bytes")
    require(
        isinstance(expected_canonical, str)
        and re.fullmatch(r"[0-9a-f]{64}", expected_canonical) is not None,
        f"package manifest canonical ZIP fingerprint is malformed: {archive_name}",
    )

    try:
        with zipfile.ZipFile(path, "r") as archive:
            infos = archive.infolist()
            require(len(infos) == expected_count, f"ZIP entry count differs: {archive_name}")
            names = [safe_zip_member_name(info.filename, archive_name) for info in infos]
            require(len(names) == len(set(names)), f"ZIP repeats a member name: {archive_name}")
            require(
                len(names) == len({name.casefold() for name in names}),
                f"ZIP has case-colliding member names: {archive_name}",
            )
            require(
                names == sorted(names, key=str.casefold),
                f"ZIP member inventory/order differs: {archive_name}",
            )
            for info in infos:
                mode = (info.external_attr >> 16) & 0xFFFF
                require(not info.is_dir(), f"ZIP contains a directory entry: {archive_name}")
                require(not (info.flag_bits & 0x1), f"ZIP contains an encrypted entry: {archive_name}")
                require(
                    mode == 0 or stat.S_ISREG(mode),
                    f"ZIP contains a symlink or special entry: {archive_name}",
                )
                require(info.file_size >= 0, f"ZIP has an invalid member size: {archive_name}")
            require(
                sum(info.file_size for info in infos) == expected_bytes,
                f"ZIP uncompressed byte count differs: {archive_name}",
            )
            require(archive.testzip() is None, f"ZIP CRC verification failed: {archive_name}")

            canonical = hashlib.sha256()
            for info in infos:
                canonical.update(info.filename.encode("utf-8"))
                canonical.update(b"\0")
                canonical.update(str(info.file_size).encode("ascii"))
                canonical.update(b"\0")
                member_bytes = 0
                with archive.open(info, "r") as member:
                    for chunk in iter(lambda: member.read(1024 * 1024), b""):
                        member_bytes += len(chunk)
                        canonical.update(chunk)
                require(
                    member_bytes == info.file_size,
                    f"ZIP member byte count differs: {archive_name}:{info.filename}",
                )
                canonical.update(b"\0")
            require(
                canonical.hexdigest() == expected_canonical,
                f"ZIP exact entry fingerprint differs: {archive_name}",
            )
    except PublicationError:
        raise
    except (
        zipfile.BadZipFile,
        zipfile.LargeZipFile,
        zlib.error,
        NotImplementedError,
        RuntimeError,
        EOFError,
        OSError,
        UnicodeError,
        ValueError,
    ) as exc:
        raise PublicationError(f"invalid ZIP structure: {archive_name}") from exc


def assert_package_file_path(package_dir: Path, path: Path) -> Path:
    require(path.parent == package_dir, f"package file has another parent: {path.name}")
    require(not is_link_like(path), f"package file may not be a symlink or junction: {path.name}")
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(ROOT.resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise PublicationError(f"package file resolves outside the repository: {path.name}") from exc
    require(resolved.parent == package_dir, f"package file escapes its directory: {path.name}")
    require(path.is_file(), f"package file is not a regular file: {path.name}")
    return resolved


def validate_package_dir(raw: Path, version: str) -> tuple[Path, str, dict[str, dict[str, Any]]]:
    root_absolute = Path(os.path.abspath(os.fspath(ROOT)))
    raw_absolute = Path(os.path.abspath(os.fspath(raw)))
    try:
        lexical_relative = raw_absolute.relative_to(root_absolute)
    except ValueError as exc:
        raise PublicationError("--package-dir must resolve inside the task repository") from exc
    cursor = root_absolute
    for part in lexical_relative.parts:
        cursor /= part
        require(not is_link_like(cursor), "--package-dir may not traverse a symlink or junction")
    require(raw_absolute.is_dir(), "--package-dir is not an existing directory")
    package_dir = raw_absolute.resolve(strict=True)
    try:
        relative = package_dir.relative_to(ROOT.resolve(strict=True)).as_posix()
    except ValueError as exc:
        raise PublicationError("--package-dir resolves outside the task repository") from exc

    entries = list(package_dir.iterdir())
    for path in entries:
        assert_package_file_path(package_dir, path)
    actual = sorted(path.name for path in entries)
    require(
        actual == sorted(EXPECTED_FILENAMES),
        "package directory must contain exactly the seven complete-edition files",
    )

    identities = {name: file_identity(package_dir / name) for name in EXPECTED_FILENAMES}
    require(all(row["bytes"] > 0 for row in identities.values()), "a package file is empty")
    require((package_dir / PDF_NAME).read_bytes()[:5] == b"%PDF-", "reader file is not a PDF")

    try:
        manifest = json.loads(
            (package_dir / MANIFEST_NAME).read_text(encoding="utf-8"),
            object_pairs_hook=strict_json_object,
            parse_constant=reject_nonfinite_json,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PublicationError("package manifest is not valid UTF-8 JSON") from exc
    require(isinstance(manifest, dict), "package manifest root is not an object")
    require(manifest.get("schema_version") == 1, "package manifest schema is not version 1")
    require(manifest.get("status") == "pass", "package manifest status is not pass")
    require(manifest.get("partial") is False, "package manifest describes a partial release")
    require(manifest.get("boundary_complete") is True, "package boundary is not complete")
    record = manifest.get("record")
    require(isinstance(record, dict), "package manifest has no record object")
    require(record.get("title") == TITLE, "package manifest title differs from the release title")
    require(record.get("version") == version, "package manifest version differs from --version")
    require(record.get("language") == LANGUAGE, "package manifest language is not ind")
    require(
        record.get("concept_doi") == CONCEPT_DOI,
        "package manifest concept DOI differs from the existing lineage",
    )
    require(
        require_int(
            record.get("predecessor_record_id"), "package manifest predecessor record ID"
        )
        == PREDECESSOR_RECORD_ID,
        "package manifest predecessor is not record 22164668",
    )
    completion = record.get("completion")
    require(isinstance(completion, dict), "package manifest completion field is not an object")
    require(completion.get("chapters_verified") == 20, "package does not verify 20 chapters")
    require(completion.get("chapters_total") == 20, "package chapter total is not 20")
    require(
        completion.get("completion_modules_verified") == 8,
        "package does not verify eight completion modules",
    )
    require(completion.get("complete_edition") is True, "package is not a complete edition")

    payload_rows = manifest_payload_rows(manifest, identities)
    validate_zip_file(package_dir / HTML_ZIP_NAME, payload_rows[HTML_ZIP_NAME])
    validate_zip_file(package_dir / SOURCE_ZIP_NAME, payload_rows[SOURCE_ZIP_NAME])

    try:
        checksum_lines = (package_dir / CHECKSUMS_NAME).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        raise PublicationError("checksums file is not valid UTF-8 text") from exc
    parsed_checksums: dict[str, str] = {}
    for line in checksum_lines:
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\]+)", line)
        require(match is not None, "checksums file has a malformed line")
        digest, name = match.groups()
        require(name not in parsed_checksums, "checksums file repeats a filename")
        parsed_checksums[name] = digest
    checksum_scope = set(EXPECTED_FILENAMES) - {CHECKSUMS_NAME}
    require(set(parsed_checksums) == checksum_scope, "checksums file has the wrong file scope")
    for name, digest in parsed_checksums.items():
        require(digest == identities[name]["sha256"], f"SHA-256 mismatch in checksums file: {name}")
    return package_dir, relative, identities


def assert_sanitized_payload(label: str, payload: bytes, token: str | None = None) -> None:
    text = payload.decode("utf-8")
    require(not ABSOLUTE_PATH.search(text), f"{label} contains a local absolute path")
    require(not CREDENTIAL_MARKER.search(text), f"{label} contains a credential marker")
    if token:
        require(token not in text, f"{label} contains the active access token")


def atomic_write(path: Path, payload: bytes, token: str | None = None) -> None:
    assert_sanitized_payload(path.name, payload, token)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        require(
            temporary.read_bytes() == payload,
            f"temporary write readback failed: {path.name}",
        )
        os.replace(temporary, path)
        require(path.read_bytes() == payload, f"atomic write readback failed: {path.name}")
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def phase_index(phase: str) -> int:
    try:
        return PHASES.index(phase)
    except ValueError as exc:
        raise PublicationError(f"unknown durable-state phase: {phase}") from exc


def at_least(state: Mapping[str, Any], phase: str) -> bool:
    return phase_index(str(state.get("phase"))) >= phase_index(phase)


def save_state(state: dict[str, Any], token: str | None) -> None:
    state["updated_utc"] = now_utc()
    atomic_write(STATE_PATH, canonical_json(state), token)


def load_or_initialize_state(
    *,
    version: str,
    publication_date: str,
    package_relative: str,
    identities: Mapping[str, Mapping[str, Any]],
    predecessor_metadata_fingerprint: str,
    token: str,
) -> dict[str, Any]:
    expected_files = {name: dict(identities[name]) for name in EXPECTED_FILENAMES}
    if STATE_PATH.exists():
        try:
            state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PublicationError("durable publication state is not valid UTF-8 JSON") from exc
        require(isinstance(state, dict), "durable publication state root is not an object")
        require(state.get("schema_version") == 1, "unsupported durable-state schema")
        require(
            state.get("operation") == "zenodo_complete_maintenance",
            "durable state belongs to another operation",
        )
        require(state.get("version") == version, "durable-state version differs from --version")
        require(
            state.get("publication_date") == publication_date,
            "durable-state date differs from --publication-date",
        )
        require(
            state.get("package_dir") == package_relative,
            "durable-state package directory differs from --package-dir",
        )
        require(state.get("files") == expected_files, "package bytes changed after state creation")
        require(
            state.get("predecessor_record_id") == PREDECESSOR_RECORD_ID,
            "durable state names another predecessor record",
        )
        require(
            state.get("concept_record_id") == CONCEPT_RECORD_ID,
            "durable state names another concept record",
        )
        require(state.get("concept_doi") == CONCEPT_DOI, "durable state names another concept DOI")
        require(
            state.get("predecessor_metadata_fingerprint") == predecessor_metadata_fingerprint,
            "the frozen predecessor metadata arrays changed",
        )
        phase_index(str(state.get("phase")))
        return state

    state = {
        "schema_version": 1,
        "operation": "zenodo_complete_maintenance",
        "phase": "initialized",
        "predecessor_record_id": PREDECESSOR_RECORD_ID,
        "concept_record_id": CONCEPT_RECORD_ID,
        "concept_doi": CONCEPT_DOI,
        "version": version,
        "publication_date": publication_date,
        "package_dir": package_relative,
        "files": expected_files,
        "predecessor_metadata_fingerprint": predecessor_metadata_fingerprint,
        "newversion_attempted": False,
        "newversion_attempt": None,
        "deleted_inherited_files": [],
        "uploaded_files": {},
        "publish_attempted": False,
        "publish_request": None,
        "public_readback": {},
        "created_utc": now_utc(),
    }
    save_state(state, token)
    return state


def safe_endpoint_label(url: str) -> str:
    parsed = urlparse(url)
    return parsed.path or "/"


def require_zenodo_url(url: str, label: str) -> str:
    parsed = urlparse(url)
    require(parsed.scheme == "https", f"{label} is not HTTPS")
    hostname = (parsed.hostname or "").casefold()
    require(
        hostname == "zenodo.org" or hostname.endswith(".zenodo.org"),
        f"{label} does not point to Zenodo",
    )
    require(not parsed.username and not parsed.password, f"{label} contains user information")
    require(not parsed.query, f"{label} unexpectedly contains a query string")
    return url


def request_json(
    session: requests.Session,
    method: str,
    url: str,
    *,
    expected_statuses: Iterable[int],
    **kwargs: Any,
) -> dict[str, Any]:
    require_zenodo_url(url, "API endpoint")
    response = session.request(
        method,
        url,
        timeout=REQUEST_TIMEOUT,
        allow_redirects=False,
        **kwargs,
    )
    if response.status_code not in set(expected_statuses):
        raise PublicationError(
            f"Zenodo returned HTTP {response.status_code} for {method} "
            f"{safe_endpoint_label(url)}"
        )
    if not response.content:
        return {}
    try:
        value = response.json()
    except ValueError as exc:
        raise PublicationError(
            f"Zenodo returned non-JSON content for {method} {safe_endpoint_label(url)}"
        ) from exc
    require(isinstance(value, dict), "Zenodo JSON response is not an object")
    return value


def request_no_content(
    session: requests.Session,
    method: str,
    url: str,
    *,
    expected_statuses: Iterable[int],
) -> None:
    require_zenodo_url(url, "API endpoint")
    response = session.request(
        method,
        url,
        timeout=REQUEST_TIMEOUT,
        allow_redirects=False,
    )
    if response.status_code not in set(expected_statuses):
        raise PublicationError(
            f"Zenodo returned HTTP {response.status_code} for {method} "
            f"{safe_endpoint_label(url)}"
        )


def extract_license_id(value: Any) -> str | None:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        candidate = value.get("id")
        return candidate if isinstance(candidate, str) else None
    return None


def assert_publication_book(metadata: Mapping[str, Any], label: str) -> None:
    legacy_upload = metadata.get("upload_type")
    legacy_publication = metadata.get("publication_type")
    legacy_exposed = legacy_upload is not None or legacy_publication is not None
    if legacy_exposed:
        require(legacy_upload == "publication", f"{label} upload type is not publication")
        require(legacy_publication == "book", f"{label} publication type is not book")

    resource = metadata.get("resource_type")
    resource_exposed = resource is not None
    if resource_exposed:
        require(isinstance(resource, dict), f"{label} resource type is not an object")
        resource_id = resource.get("id")
        resource_type = resource.get("type")
        resource_subtype = resource.get("subtype")
        if resource_id is not None:
            require(resource_id == "publication-book", f"{label} resource type is not publication/book")
        if resource_type is not None or resource_subtype is not None:
            require(resource_type == "publication", f"{label} resource type is not publication")
            require(resource_subtype == "book", f"{label} resource subtype is not book")
        require(
            resource_id == "publication-book"
            or (resource_type == "publication" and resource_subtype == "book"),
            f"{label} does not expose a publication/book resource type",
        )
    require(legacy_exposed or resource_exposed, f"{label} does not expose a resource type")


def assert_concept_identity(record: Mapping[str, Any], label: str) -> None:
    concept_id = record.get("conceptrecid")
    concept_doi = record.get("conceptdoi")
    checks = 0
    if concept_id is not None:
        require(
            api_record_id(concept_id, f"{label} concept record ID") == CONCEPT_RECORD_ID,
            f"{label} is in another concept record",
        )
        checks += 1
    if concept_doi is not None:
        require(concept_doi == CONCEPT_DOI, f"{label} has another concept DOI")
        checks += 1
    require(checks > 0, f"{label} does not expose concept identity")


def assert_no_project_label_outside_contributor(value: Any, label: str) -> None:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True)
    require("Translation and Transcription Project" not in serialized, f"{label} contains a forbidden expansion")
    require("TTP" not in serialized, f"{label} contains the organization label outside its contributor entry")


def predecessor_arrays(record: Mapping[str, Any]) -> dict[str, list[Any]]:
    require(
        api_record_id(record.get("id"), "anonymous predecessor record ID")
        == PREDECESSOR_RECORD_ID,
        "anonymous record ID mismatch",
    )
    assert_concept_identity(record, "predecessor record")
    metadata = record.get("metadata")
    require(isinstance(metadata, dict), "anonymous predecessor has no metadata object")
    require(metadata.get("title") == TITLE, "predecessor title differs from the canonical title")
    require(metadata.get("language") == LANGUAGE, "predecessor language is not ind")
    require(extract_license_id(metadata.get("license")) == LICENSE_ID, "predecessor license differs")

    access = metadata.get("access_right")
    if access is None and isinstance(record.get("access"), dict):
        access = record["access"].get("status")
    require(access == "open", "predecessor is not openly accessible")

    assert_publication_book(metadata, "predecessor")

    creators = metadata.get("creators")
    contributors = metadata.get("contributors")
    keywords = metadata.get("keywords")
    relations = metadata.get("related_identifiers")
    require(isinstance(creators, list) and len(creators) == 1, "predecessor must have one creator")
    require(isinstance(creators[0], dict), "predecessor creator is not an object")
    require(creators[0].get("name") == "Schlicker, Steven", "predecessor creator name differs")
    require(
        creators[0].get("affiliation") == "Grand Valley State University",
        "predecessor creator affiliation differs",
    )
    assert_no_project_label_outside_contributor(creators, "creators")

    require(isinstance(contributors, list) and len(contributors) == 1, "predecessor must have one contributor")
    require(isinstance(contributors[0], dict), "predecessor contributor is not an object")
    require(contributors[0].get("name") == "TTP", "predecessor contributor name differs")
    require(contributors[0].get("type") == "Other", "predecessor contributor type differs")
    contributor_other_values = {
        key: item for key, item in contributors[0].items() if key != "name"
    }
    assert_no_project_label_outside_contributor(contributor_other_values, "contributor metadata")

    require(isinstance(keywords, list) and len(keywords) == 8, "predecessor must have exactly eight keywords")
    require(all(isinstance(item, str) and item.strip() for item in keywords), "predecessor has an invalid keyword")
    require(len(set(keywords)) == 8, "predecessor keywords are not unique")
    assert_no_project_label_outside_contributor(keywords, "keywords")

    require(isinstance(relations, list) and len(relations) == 2, "predecessor must have two related identifiers")
    require(all(isinstance(item, dict) for item in relations), "a predecessor relation is not an object")
    require(
        all(item.get("relation") == "isDerivedFrom" for item in relations),
        "both predecessor relations must be isDerivedFrom",
    )
    require(
        len({item.get("identifier") for item in relations}) == 2,
        "predecessor relations do not have two unique identifiers",
    )
    require(
        all(isinstance(item.get("identifier"), str) and item["identifier"].strip() for item in relations),
        "a predecessor relation has no identifier",
    )
    assert_no_project_label_outside_contributor(relations, "related identifiers")

    arrays = {
        "creators": copy.deepcopy(creators),
        "contributors": copy.deepcopy(contributors),
        "keywords": copy.deepcopy(keywords),
        "related_identifiers": copy.deepcopy(relations),
    }
    return arrays


def desired_metadata(
    *, version: str, publication_date: str, arrays: Mapping[str, list[Any]]
) -> dict[str, Any]:
    metadata = {
        "title": TITLE,
        "upload_type": "publication",
        "publication_type": "book",
        "description": DESCRIPTION,
        "creators": copy.deepcopy(arrays["creators"]),
        "access_right": "open",
        "license": LICENSE_ID,
        "publication_date": publication_date,
        "version": version,
        "language": LANGUAGE,
        "keywords": copy.deepcopy(arrays["keywords"]),
        "contributors": copy.deepcopy(arrays["contributors"]),
        "related_identifiers": copy.deepcopy(arrays["related_identifiers"]),
        "notes": NOTES,
    }
    require(set(metadata) == METADATA_WHITELIST, "internal metadata whitelist mismatch")
    require(metadata["description"].startswith(f"<p>{html.escape(DESCRIPTION_LEAD)}</p>"), "description lead changed")
    for key in ("title", "description", "notes", "version", "publication_date"):
        assert_no_project_label_outside_contributor(metadata[key], f"metadata.{key}")
    serialized = json.dumps(metadata, ensure_ascii=False, sort_keys=True)
    require(serialized.count('"TTP"') == 1, "organization label must occur exactly once in metadata")
    require("Translation and Transcription Project" not in serialized, "metadata contains a forbidden expansion")
    return metadata


def normalized_metadata_subset(metadata: Mapping[str, Any]) -> dict[str, Any]:
    return {key: metadata.get(key) for key in METADATA_WHITELIST}


def assert_draft_metadata(actual: Any, expected: Mapping[str, Any]) -> None:
    require(isinstance(actual, dict), "draft does not expose metadata")
    extras = set(actual) - METADATA_WHITELIST - SERVER_MANAGED_DEPOSITION_METADATA
    require(not extras, f"draft retained non-whitelisted metadata keys: {sorted(extras)}")
    require(
        normalized_metadata_subset(actual) == dict(expected),
        "draft metadata differs from the exact release metadata",
    )


def remote_file_name(item: Mapping[str, Any]) -> str:
    for key in ("filename", "name", "key"):
        value = item.get(key)
        if isinstance(value, str) and value:
            return value
    raise PublicationError("Zenodo file object has no filename")


def remote_file_size(item: Mapping[str, Any]) -> int:
    for key in ("filesize", "size"):
        value = item.get(key)
        if isinstance(value, int):
            return value
    raise PublicationError(f"Zenodo file {remote_file_name(item)} has no integer size")


def remote_file_md5(item: Mapping[str, Any]) -> str:
    value = item.get("checksum")
    if isinstance(value, str):
        match = re.fullmatch(r"(?:md5:)?([0-9a-fA-F]{32})", value)
        if match:
            return match.group(1).lower()
    value = item.get("md5")
    if isinstance(value, str) and re.fullmatch(r"[0-9a-fA-F]{32}", value):
        return value.lower()
    raise PublicationError(f"Zenodo file {remote_file_name(item)} has no MD5 checksum")


def files_from_deposition(deposition: Mapping[str, Any]) -> list[dict[str, Any]]:
    files = deposition.get("files")
    require(isinstance(files, list), "draft does not expose a files list")
    require(all(isinstance(item, dict) for item in files), "draft files list contains a non-object")
    return files


def assert_remote_file_identity(
    item: Mapping[str, Any], expected_name: str, expected: Mapping[str, Any]
) -> None:
    require(remote_file_name(item) == expected_name, f"remote filename differs: {expected_name}")
    require(remote_file_size(item) == expected["bytes"], f"remote byte count differs: {expected_name}")
    require(remote_file_md5(item) == expected["md5"], f"remote MD5 differs: {expected_name}")


def assert_exact_remote_files(
    files: Iterable[Mapping[str, Any]], identities: Mapping[str, Mapping[str, Any]]
) -> dict[str, Mapping[str, Any]]:
    by_name: dict[str, Mapping[str, Any]] = {}
    for item in files:
        name = remote_file_name(item)
        require(name not in by_name, f"draft repeats remote filename: {name}")
        by_name[name] = item
    require(set(by_name) == set(EXPECTED_FILENAMES), "draft file inventory is not the exact seven-file package")
    for name in EXPECTED_FILENAMES:
        assert_remote_file_identity(by_name[name], name, identities[name])
    return by_name


def deposition_url(record_id: int) -> str:
    return f"{API_BASE}/deposit/depositions/{record_id}"


def auth_get_deposition(session: requests.Session, record_id: int) -> dict[str, Any]:
    deposition = request_json(
        session, "GET", deposition_url(record_id), expected_statuses=(200,)
    )
    require(
        api_record_id(deposition.get("id"), "authenticated deposition record ID")
        == record_id,
        "authenticated deposition response names another record",
    )
    return deposition


def extract_record_id_from_url(url: str, label: str) -> int:
    require_zenodo_url(url, label)
    match = re.search(r"/(?:depositions|records)/(\d+)(?:/)?$", urlparse(url).path)
    require(match is not None, f"{label} has no terminal record ID")
    return int(match.group(1))


def draft_id_from_newversion_response(response: Mapping[str, Any]) -> int:
    links = response.get("links")
    if isinstance(links, dict) and isinstance(links.get("latest_draft"), str):
        return extract_record_id_from_url(links["latest_draft"], "latest draft link")
    if response.get("submitted") is False and response.get("id") is not None:
        return api_record_id(response["id"], "new-version response draft ID")
    raise PublicationError("new-version response does not expose a draft ID")


def latest_draft_id(record: Mapping[str, Any], label: str) -> int:
    links = record.get("links")
    require(isinstance(links, dict), f"{label} has no links object")
    value = links.get("latest_draft")
    require(isinstance(value, str), f"{label} has no latest-draft link")
    return extract_record_id_from_url(value, f"{label} latest-draft link")


def clone_payload_fingerprint(deposition: Mapping[str, Any], label: str) -> str:
    metadata = deposition.get("metadata")
    require(isinstance(metadata, dict), f"{label} has no metadata object")
    file_rows: list[dict[str, Any]] = []
    names: set[str] = set()
    for item in files_from_deposition(deposition):
        name = remote_file_name(item)
        require(name not in names, f"{label} repeats filename: {name}")
        names.add(name)
        file_rows.append(
            {
                "name": name,
                "bytes": remote_file_size(item),
                "md5": remote_file_md5(item),
            }
        )
    return canonical_fingerprint(
        {
            "metadata": normalized_metadata_subset(metadata),
            "files": file_rows,
        }
    )


def draft_file_inventory(deposition: Mapping[str, Any], label: str) -> list[dict[str, Any]]:
    inventory: list[dict[str, Any]] = []
    names: set[str] = set()
    for item in files_from_deposition(deposition):
        name = remote_file_name(item)
        require(name not in names, f"{label} repeats filename: {name}")
        names.add(name)
        file_id = item.get("id")
        require(isinstance(file_id, str) and file_id, f"{label} file has no ID: {name}")
        inventory.append(
            {
                "id": file_id,
                "name": name,
                "bytes": remote_file_size(item),
                "md5": remote_file_md5(item),
            }
        )
    return inventory


def bind_inherited_file_inventory(
    draft: Mapping[str, Any], state: dict[str, Any], token: str
) -> None:
    inventory = draft_file_inventory(draft, "new-version candidate")
    frozen = state.get("inherited_file_inventory")
    if frozen is None:
        state["inherited_file_inventory"] = inventory
        save_state(state, token)
    else:
        require(
            frozen == inventory,
            "new-version candidate differs from the frozen inherited file inventory",
        )


def validate_newversion_candidate(
    session: requests.Session,
    candidate_id: int,
    attempt: Mapping[str, Any],
) -> dict[str, Any]:
    require(
        attempt.get("predecessor_record_id") == PREDECESSOR_RECORD_ID,
        "new-version journal names another predecessor",
    )
    require(
        attempt.get("pre_latest_draft_id") == PREDECESSOR_RECORD_ID,
        "new-version journal did not freeze the pristine predecessor latest-draft identity",
    )
    require(candidate_id != PREDECESSOR_RECORD_ID, "Zenodo did not allocate a new record ID")
    require(
        attempt.get("response_draft_id") == candidate_id,
        "candidate draft was not identified by this operation's new-version response",
    )

    predecessor = auth_get_deposition(session, PREDECESSOR_RECORD_ID)
    require(predecessor.get("submitted") is True, "predecessor deposition is not published")
    assert_concept_identity(predecessor, "authenticated predecessor")
    require(
        latest_draft_id(predecessor, "authenticated predecessor") == candidate_id,
        "predecessor latest-draft identity does not match this operation's response",
    )

    draft = auth_get_deposition(session, candidate_id)
    require(draft.get("submitted") is False, "new-version candidate is already submitted")
    assert_concept_identity(draft, "new-version candidate")
    require(
        clone_payload_fingerprint(draft, "new-version candidate")
        == attempt.get("pre_clone_payload_fingerprint"),
        "new-version candidate is not the pristine clone frozen before this operation",
    )
    links = draft.get("links")
    if isinstance(links, dict) and isinstance(links.get("self"), str):
        require(
            extract_record_id_from_url(links["self"], "new-version candidate self link")
            == candidate_id,
            "new-version candidate self link names another record",
        )
    return draft


def recover_draft_after_interrupted_newversion(
    session: requests.Session, state: Mapping[str, Any]
) -> tuple[int, dict[str, Any]]:
    attempt = state.get("newversion_attempt")
    require(isinstance(attempt, dict), "new-version attempt has no durable identity journal")
    response_draft_id = attempt.get("response_draft_id")
    require(
        isinstance(response_draft_id, int) and not isinstance(response_draft_id, bool),
        "prior new-version outcome is indeterminate; refusing to adopt the current latest draft",
    )
    draft_id = response_draft_id
    draft = validate_newversion_candidate(session, draft_id, attempt)
    return draft_id, draft


def advance(state: dict[str, Any], phase: str, token: str) -> None:
    require(phase_index(phase) >= phase_index(str(state["phase"])), "state phase would move backwards")
    state["phase"] = phase
    save_state(state, token)


def ensure_draft(
    session: requests.Session, state: dict[str, Any], token: str
) -> tuple[int, dict[str, Any]]:
    draft: dict[str, Any] | None = None
    draft_id = state.get("draft_id")
    if draft_id is None and state.get("newversion_attempted"):
        draft_id, draft = recover_draft_after_interrupted_newversion(session, state)
        state["draft_id"] = draft_id
        bind_inherited_file_inventory(draft, state, token)
        advance(state, "draft_created", token)
    elif draft_id is None:
        predecessor = auth_get_deposition(session, PREDECESSOR_RECORD_ID)
        require(predecessor.get("submitted") is True, "predecessor deposition is not published")
        assert_concept_identity(predecessor, "authenticated predecessor")
        pre_latest_draft_id = latest_draft_id(predecessor, "authenticated predecessor")
        require(
            pre_latest_draft_id == PREDECESSOR_RECORD_ID,
            "predecessor already exposes another latest draft; refusing new-version creation",
        )
        attempt = {
            "predecessor_record_id": PREDECESSOR_RECORD_ID,
            "pre_latest_draft_id": pre_latest_draft_id,
            "pre_clone_payload_fingerprint": clone_payload_fingerprint(
                predecessor, "authenticated predecessor"
            ),
            "request_started_utc": now_utc(),
            "response_draft_id": None,
        }
        state["newversion_attempted"] = True
        state["newversion_attempt"] = attempt
        save_state(state, token)
        response = request_json(
            session,
            "POST",
            f"{deposition_url(PREDECESSOR_RECORD_ID)}/actions/newversion",
            expected_statuses=(201,),
        )
        draft_id = draft_id_from_newversion_response(response)
        attempt["response_draft_id"] = draft_id
        attempt["response_received_utc"] = now_utc()
        save_state(state, token)
        draft = validate_newversion_candidate(session, draft_id, attempt)
        state["draft_id"] = draft_id
        bind_inherited_file_inventory(draft, state, token)
        advance(state, "draft_created", token)
    else:
        draft_id = require_int(draft_id, "durable draft ID")
        attempt = state.get("newversion_attempt")
        require(isinstance(attempt, dict), "durable draft has no new-version identity journal")
        require(
            attempt.get("response_draft_id") == draft_id,
            "durable draft ID is not bound to this operation's new-version response",
        )

    if draft is None:
        draft = auth_get_deposition(session, draft_id)
    assert_concept_identity(draft, "maintenance draft")
    if not at_least(state, "draft_created"):
        bind_inherited_file_inventory(draft, state, token)
        advance(state, "draft_created", token)
    if not at_least(state, "published"):
        submitted = draft.get("submitted")
        require(isinstance(submitted, bool), "maintenance draft has no submitted state")
        require(
            submitted is False
            or (
                str(state.get("phase")) == "publish_attempted"
                and state.get("publish_attempted") is True
            ),
            "maintenance draft was submitted outside the recorded publish step",
        )
    return draft_id, draft


def delete_inherited_files(
    session: requests.Session,
    draft_id: int,
    draft: Mapping[str, Any],
    state: dict[str, Any],
    token: str,
) -> dict[str, Any]:
    if at_least(state, "inherited_files_deleted"):
        return dict(draft)
    deleted = state.setdefault("deleted_inherited_files", [])
    require(isinstance(deleted, list), "durable deleted-files field is invalid")
    require(
        all(isinstance(name, str) for name in deleted) and len(deleted) == len(set(deleted)),
        "durable deleted-files inventory is malformed",
    )
    frozen = state.get("inherited_file_inventory")
    require(isinstance(frozen, list), "durable inherited-file inventory is absent")
    require(all(isinstance(row, dict) for row in frozen), "durable inherited-file inventory is malformed")
    frozen_names = [row.get("name") for row in frozen]
    require(
        all(isinstance(name, str) for name in frozen_names)
        and len(frozen_names) == len(set(frozen_names)),
        "durable inherited-file inventory has invalid names",
    )
    require(set(deleted) <= set(frozen_names), "deleted-files journal names a non-inherited file")
    remaining = [row for row in frozen if row["name"] not in deleted]
    require(
        draft_file_inventory(draft, "maintenance draft before inherited-file deletion")
        == remaining,
        "maintenance draft changed outside the recorded inherited-file deletions",
    )
    for row in remaining:
        file_id = row.get("id")
        name = row.get("name")
        require(isinstance(file_id, str) and file_id, "frozen inherited file has no ID")
        require(isinstance(name, str) and name, "frozen inherited file has no name")
        request_no_content(
            session,
            "DELETE",
            f"{deposition_url(draft_id)}/files/{file_id}",
            expected_statuses=(204,),
        )
        if name not in deleted:
            deleted.append(name)
            deleted.sort(key=str.casefold)
        save_state(state, token)
    refreshed = auth_get_deposition(session, draft_id)
    require(files_from_deposition(refreshed) == [], "inherited draft files were not completely removed")
    advance(state, "inherited_files_deleted", token)
    return refreshed


def apply_metadata(
    session: requests.Session,
    draft_id: int,
    expected: Mapping[str, Any],
    state: dict[str, Any],
    token: str,
) -> dict[str, Any]:
    if not at_least(state, "metadata_updated"):
        updated = request_json(
            session,
            "PUT",
            deposition_url(draft_id),
            expected_statuses=(200,),
            json={"metadata": dict(expected)},
        )
        assert_draft_metadata(updated.get("metadata"), expected)
        state["metadata_sha256"] = canonical_fingerprint(expected)
        advance(state, "metadata_updated", token)
        return updated
    refreshed = auth_get_deposition(session, draft_id)
    assert_draft_metadata(refreshed.get("metadata"), expected)
    require(
        state.get("metadata_sha256") == canonical_fingerprint(expected),
        "durable metadata fingerprint differs",
    )
    return refreshed


def upload_one_file(
    session: requests.Session, draft_id: int, path: Path
) -> dict[str, Any]:
    url = f"{deposition_url(draft_id)}/files"
    require_zenodo_url(url, "file upload endpoint")
    with path.open("rb") as handle:
        response = session.post(
            url,
            data={"name": path.name},
            files={"file": (path.name, handle, "application/octet-stream")},
            timeout=REQUEST_TIMEOUT,
            allow_redirects=False,
        )
    if response.status_code != 201:
        raise PublicationError(
            f"Zenodo returned HTTP {response.status_code} for POST {safe_endpoint_label(url)}"
        )
    try:
        value = response.json()
    except ValueError as exc:
        raise PublicationError("Zenodo returned non-JSON content after file upload") from exc
    require(isinstance(value, dict), "Zenodo file-upload response is not an object")
    return value


def upload_package_files(
    session: requests.Session,
    draft_id: int,
    package_dir: Path,
    identities: Mapping[str, Mapping[str, Any]],
    state: dict[str, Any],
    token: str,
) -> dict[str, Any]:
    draft = auth_get_deposition(session, draft_id)
    existing: dict[str, dict[str, Any]] = {}
    for item in files_from_deposition(draft):
        name = remote_file_name(item)
        require(name in EXPECTED_FILENAMES, f"unexpected file appeared in maintenance draft: {name}")
        require(name not in existing, f"maintenance draft repeats filename: {name}")
        existing[name] = item

    uploaded = state.setdefault("uploaded_files", {})
    require(isinstance(uploaded, dict), "durable uploaded-files field is invalid")
    for name in EXPECTED_FILENAMES:
        expected = identities[name]
        item = existing.get(name)
        if item is not None:
            if name in uploaded:
                assert_remote_file_identity(item, name, expected)
            else:
                try:
                    assert_remote_file_identity(item, name, expected)
                except PublicationError:
                    file_id = item.get("id")
                    require(isinstance(file_id, str) and file_id, f"mismatched remote file has no ID: {name}")
                    request_no_content(
                        session,
                        "DELETE",
                        f"{deposition_url(draft_id)}/files/{file_id}",
                        expected_statuses=(204,),
                    )
                    item = None
            if item is not None:
                uploaded[name] = {"bytes": expected["bytes"], "md5": expected["md5"]}
                save_state(state, token)
                continue

        local_path = assert_package_file_path(package_dir, package_dir / name)
        require(
            file_identity(local_path) == dict(expected),
            f"package file changed before upload: {name}",
        )
        response_file = upload_one_file(session, draft_id, local_path)
        assert_remote_file_identity(response_file, name, expected)
        uploaded[name] = {"bytes": expected["bytes"], "md5": expected["md5"]}
        save_state(state, token)

    refreshed = auth_get_deposition(session, draft_id)
    assert_exact_remote_files(files_from_deposition(refreshed), identities)
    require(set(uploaded) == set(EXPECTED_FILENAMES), "durable upload inventory is incomplete")
    if not at_least(state, "files_uploaded"):
        advance(state, "files_uploaded", token)
    return refreshed


def sort_files_pdf_first(
    session: requests.Session,
    draft_id: int,
    identities: Mapping[str, Mapping[str, Any]],
    state: dict[str, Any],
    token: str,
) -> dict[str, Any]:
    desired_order = list(EXPECTED_FILENAMES)
    if not at_least(state, "files_sorted"):
        current = auth_get_deposition(session, draft_id)
        by_name = {remote_file_name(item): item for item in files_from_deposition(current)}
        require(set(by_name) == set(desired_order), "cannot sort an incomplete draft file inventory")
        order_payload = []
        for name in desired_order:
            file_id = by_name[name].get("id")
            require(isinstance(file_id, str) and file_id, f"draft file has no ID: {name}")
            order_payload.append({"id": file_id})
        url = f"{deposition_url(draft_id)}/files"
        require_zenodo_url(url, "file ordering endpoint")
        response = session.put(
            url,
            json=order_payload,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=False,
        )
        require(response.status_code == 200, f"Zenodo returned HTTP {response.status_code} for PUT {safe_endpoint_label(url)}")
        state["file_order"] = desired_order
        advance(state, "files_sorted", token)
    refreshed = auth_get_deposition(session, draft_id)
    files = files_from_deposition(refreshed)
    assert_exact_remote_files(files, identities)
    actual_order = [remote_file_name(item) for item in files]
    require(actual_order == desired_order, "Zenodo draft did not retain PDF-first file order")
    require(actual_order[0] == PDF_NAME, "reader PDF is not the primary visible file")
    return refreshed


def prepublish_verify(
    draft: Mapping[str, Any],
    expected_metadata: Mapping[str, Any],
    identities: Mapping[str, Mapping[str, Any]],
    state: dict[str, Any],
    token: str,
) -> None:
    require(draft.get("submitted") is False, "prepublish draft is already submitted")
    assert_concept_identity(draft, "prepublish draft")
    assert_draft_metadata(draft.get("metadata"), expected_metadata)
    files = files_from_deposition(draft)
    assert_exact_remote_files(files, identities)
    require([remote_file_name(item) for item in files] == list(EXPECTED_FILENAMES), "prepublish file order differs")
    state["prepublish_verification"] = {
        "metadata_sha256": canonical_fingerprint(expected_metadata),
        "draft_fingerprint": release_draft_fingerprint(draft, "prepublish draft"),
        "file_count": len(EXPECTED_FILENAMES),
        "file_bytes": sum(int(row["bytes"]) for row in identities.values()),
        "pdf_first": True,
        "remote_size_md5": "pass",
    }
    if not at_least(state, "prepublish_verified"):
        advance(state, "prepublish_verified", token)
    else:
        save_state(state, token)


def release_draft_fingerprint(draft: Mapping[str, Any], label: str) -> str:
    record_id = api_record_id(draft.get("id"), f"{label} record ID")
    assert_concept_identity(draft, label)
    metadata = draft.get("metadata")
    require(isinstance(metadata, dict), f"{label} has no metadata object")
    file_rows: list[dict[str, Any]] = []
    for item in files_from_deposition(draft):
        file_id = item.get("id")
        require(isinstance(file_id, str) and file_id, f"{label} file has no ID")
        file_rows.append(
            {
                "id": file_id,
                "name": remote_file_name(item),
                "bytes": remote_file_size(item),
                "md5": remote_file_md5(item),
            }
        )
    return canonical_fingerprint(
        {
            "record_id": record_id,
            "concept_record_id": CONCEPT_RECORD_ID,
            "metadata": normalized_metadata_subset(metadata),
            "files": file_rows,
        }
    )


def publish_journal(
    state: dict[str, Any], draft_id: int, expected_fingerprint: str
) -> dict[str, Any] | None:
    value = state.get("publish_request")
    if value is None:
        require(
            state.get("publish_attempted") is not True,
            "legacy publish-attempt state has no request identity journal",
        )
        return None
    require(isinstance(value, dict), "durable publish-request journal is not an object")
    require(value.get("schema_version") == 1, "unsupported publish-request journal schema")
    require(value.get("method") == "POST", "publish-request journal method differs")
    require(value.get("action") == "publish", "publish-request journal action differs")
    require(value.get("draft_id") == draft_id, "publish-request journal names another draft")
    require(
        value.get("prepublish_fingerprint") == expected_fingerprint,
        "publish-request journal has another prepublish fingerprint",
    )
    attempts = require_int(value.get("attempts_started"), "publish-request attempt count")
    require(1 <= attempts <= 2, "publish-request attempt count is outside the bounded policy")
    history = value.get("history")
    require(isinstance(history, list), "publish-request history is not a list")
    require(len(history) == attempts, "publish-request history length differs from attempt count")
    for ordinal, row in enumerate(history, start=1):
        require(isinstance(row, dict), "publish-request history contains a non-object")
        require(row.get("ordinal") == ordinal, "publish-request history ordinal differs")
        require(isinstance(row.get("outcome"), str), "publish-request history has no outcome")
    require(
        value.get("accepted_http_202") in (True, False),
        "publish-request acceptance marker is invalid",
    )
    require(
        value.get("accepted_request") in (True, False),
        "publish-request reconciliation marker is invalid",
    )
    return value


def mark_published(
    draft: Mapping[str, Any],
    draft_id: int,
    expected_fingerprint: str,
    state: dict[str, Any],
    token: str,
) -> int:
    require(draft.get("submitted") is True, "published deposition is not marked submitted")
    require(
        api_record_id(draft.get("id"), "published deposition record ID") == draft_id,
        "published deposition names another record",
    )
    assert_concept_identity(draft, "published deposition")
    require(
        release_draft_fingerprint(draft, "published deposition") == expected_fingerprint,
        "published deposition differs from the frozen prepublish draft",
    )
    state["published_record_id"] = draft_id
    state["record_doi"] = f"10.5281/zenodo.{draft_id}"
    state["published_utc"] = now_utc()
    advance(state, "published", token)
    return draft_id


def begin_publish_attempt(
    journal: dict[str, Any], state: dict[str, Any], token: str
) -> dict[str, Any]:
    attempts = require_int(journal.get("attempts_started"), "publish-request attempt count")
    require(attempts < 2, "bounded publish retry has already been consumed")
    ordinal = attempts + 1
    row = {
        "ordinal": ordinal,
        "prepared_utc": now_utc(),
        "outcome": "prepared_not_sent",
    }
    history = journal.get("history")
    require(isinstance(history, list), "publish-request history is not a list")
    history.append(row)
    journal["attempts_started"] = ordinal
    journal["last_outcome"] = row["outcome"]
    state["publish_attempted"] = True
    if state.get("publish_attempted_utc") is None:
        state["publish_attempted_utc"] = row["prepared_utc"]
    advance(state, "publish_attempted", token)
    return row


def send_publish_attempt(
    session: requests.Session,
    draft_id: int,
    journal: dict[str, Any],
    row: dict[str, Any],
    expected_fingerprint: str,
    state: dict[str, Any],
    token: str,
) -> int:
    url = f"{deposition_url(draft_id)}/actions/publish"
    require_zenodo_url(url, "publish endpoint")
    try:
        response = session.post(
            url,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=False,
        )
    except requests.exceptions.ConnectTimeout as exc:
        row["outcome"] = "connect_timeout_before_request_acceptance"
        row["failed_utc"] = now_utc()
        journal["last_outcome"] = row["outcome"]
        save_state(state, token)
        raise PublicationError(
            "publish connection timed out before request acceptance; rerun to reconcile the unchanged draft"
        ) from exc
    except requests.RequestException as exc:
        row["outcome"] = "transport_outcome_indeterminate"
        row["failed_utc"] = now_utc()
        journal["last_outcome"] = row["outcome"]
        save_state(state, token)
        raise PublicationError(
            "publish transport outcome is indeterminate; a second request is forbidden"
        ) from exc

    row["http_status"] = response.status_code
    row["response_utc"] = now_utc()
    if response.status_code != 202:
        row["outcome"] = "nonaccepting_http_response"
        journal["last_outcome"] = row["outcome"]
        save_state(state, token)
        raise PublicationError(
            f"Zenodo returned HTTP {response.status_code} for POST {safe_endpoint_label(url)}"
        )

    row["outcome"] = "http_202_accepted"
    journal["last_outcome"] = row["outcome"]
    journal["accepted_http_202"] = True
    journal["accepted_request"] = True
    save_state(state, token)
    try:
        published = response.json()
    except ValueError as exc:
        raise PublicationError("Zenodo returned non-JSON content after accepting publish") from exc
    require(isinstance(published, dict), "publish response is not an object")
    require(
        api_record_id(published.get("id"), "publish response record ID") == draft_id,
        "publish response names an unexpected record",
    )
    require(published.get("submitted") is True, "accepted publish response is not yet submitted")
    return mark_published(
        published, draft_id, expected_fingerprint, state, token
    )


def reconcile_publish_request(
    session: requests.Session,
    draft_id: int,
    journal: dict[str, Any],
    expected_fingerprint: str,
    state: dict[str, Any],
    token: str,
) -> int | None:
    observations = 0
    last_transport_error: Exception | None = None
    for delay in PUBLISH_RECONCILE_BACKOFF_SECONDS:
        if delay:
            time.sleep(delay)
        try:
            draft = auth_get_deposition(session, draft_id)
        except (requests.RequestException, PublicationError) as exc:
            last_transport_error = exc
            continue
        submitted = draft.get("submitted")
        require(isinstance(submitted, bool), "reconciled deposition has no submitted state")
        require(
            release_draft_fingerprint(draft, "reconciled deposition")
            == expected_fingerprint,
            "reconciled deposition changed after the publish request was recorded",
        )
        observations += 1
        if submitted:
            journal["accepted_request"] = True
            journal["accepted_by_reconciliation"] = True
            journal["accepted_reconciled_utc"] = now_utc()
            save_state(state, token)
            return mark_published(
                draft, draft_id, expected_fingerprint, state, token
            )

    require(
        observations == len(PUBLISH_RECONCILE_BACKOFF_SECONDS),
        "publish reconciliation could not prove a continuously unchanged, unsubmitted draft",
    )
    journal["last_reconciliation"] = {
        "checked_utc": now_utc(),
        "observations": observations,
        "draft_unsubmitted": True,
        "draft_unchanged": True,
    }
    save_state(state, token)
    attempts = require_int(journal.get("attempts_started"), "publish-request attempt count")
    require(
        journal.get("accepted_request") is False,
        "an accepted publish request remains pending; refusing a second request",
    )
    require(
        attempts == 1
        and journal.get("last_outcome")
        == "connect_timeout_before_request_acceptance",
        "recorded publish outcome does not prove that a retry is safe",
    )
    require(last_transport_error is None, "publish reconciliation had an unresolved transport error")
    journal["retry_authorized_utc"] = now_utc()
    journal["retry_basis"] = "connect_timeout plus complete unchanged-unsubmitted reconciliation"
    save_state(state, token)
    return None


def publish_once(
    session: requests.Session,
    draft_id: int,
    state: dict[str, Any],
    token: str,
) -> int:
    if at_least(state, "published"):
        return require_int(state.get("published_record_id"), "durable published record ID")

    verification = state.get("prepublish_verification")
    require(isinstance(verification, dict), "prepublish verification is not recorded")
    expected_fingerprint = verification.get("draft_fingerprint")
    require(
        isinstance(expected_fingerprint, str)
        and re.fullmatch(r"[0-9a-f]{64}", expected_fingerprint) is not None,
        "prepublish draft fingerprint is missing or malformed",
    )
    draft = auth_get_deposition(session, draft_id)
    require(
        release_draft_fingerprint(draft, "publish target") == expected_fingerprint,
        "publish target differs from the frozen prepublish draft",
    )
    journal = publish_journal(state, draft_id, expected_fingerprint)
    if draft.get("submitted") is True:
        require(journal is not None, "draft was published outside this recorded operation")
        journal["accepted_request"] = True
        journal["accepted_by_reconciliation"] = True
        journal["accepted_reconciled_utc"] = now_utc()
        save_state(state, token)
        return mark_published(draft, draft_id, expected_fingerprint, state, token)

    require(at_least(state, "prepublish_verified"), "prepublish verification was not recorded")
    require(draft.get("submitted") is False, "publish target has no valid submitted state")
    if journal is None:
        journal = {
            "schema_version": 1,
            "method": "POST",
            "action": "publish",
            "draft_id": draft_id,
            "prepublish_fingerprint": expected_fingerprint,
            "attempts_started": 0,
            "accepted_http_202": False,
            "accepted_request": False,
            "history": [],
        }
        state["publish_request"] = journal
    else:
        published_id = reconcile_publish_request(
            session, draft_id, journal, expected_fingerprint, state, token
        )
        if published_id is not None:
            return published_id
    row = begin_publish_attempt(journal, state, token)
    return send_publish_attempt(
        session,
        draft_id,
        journal,
        row,
        expected_fingerprint,
        state,
        token,
    )


def assert_anonymous_session(session: requests.Session) -> None:
    require(session.trust_env is False, "anonymous session must not trust the environment")
    require(session.auth is None, "anonymous session has an authentication handler")
    forbidden = {"authorization", "proxy-authorization", "cookie"}
    require(
        not any(str(key).casefold() in forbidden for key in session.headers),
        "anonymous session contains an authentication header",
    )
    require(not session.proxies, "anonymous session contains an explicit proxy")
    require(not session.cookies, "anonymous session contains cookies")


def anonymous_get(
    session: requests.Session, url: str, *, stream: bool = False
) -> requests.Response:
    current = require_zenodo_url(url, "anonymous endpoint")
    for redirect_count in range(4):
        session.cookies.clear()
        assert_anonymous_session(session)
        response = session.get(
            current,
            stream=stream,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=False,
        )
        session.cookies.clear()
        if response.status_code not in (301, 302, 303, 307, 308):
            require_zenodo_url(response.url, "anonymous response URL")
            return response
        location = response.headers.get("Location")
        response.close()
        require(isinstance(location, str) and location, "anonymous redirect has no Location")
        require(redirect_count < 3, "anonymous Zenodo redirect limit exceeded")
        current = require_zenodo_url(
            urljoin(current, location), "anonymous redirect destination"
        )
    raise PublicationError("anonymous Zenodo redirect limit exceeded")


def anonymous_json_once(session: requests.Session, url: str) -> dict[str, Any]:
    response = anonymous_get(session, url)
    if response.status_code != 200:
        raise PublicationError(
            f"anonymous Zenodo read returned HTTP {response.status_code} for {safe_endpoint_label(url)}"
        )
    try:
        value = response.json()
    except ValueError as exc:
        raise PublicationError("anonymous Zenodo read returned non-JSON content") from exc
    require(isinstance(value, dict), "anonymous Zenodo record is not an object")
    return value


def anonymous_predecessor(session: requests.Session) -> dict[str, Any]:
    last_error: Exception | None = None
    url = f"{API_BASE}/records/{PREDECESSOR_RECORD_ID}"
    for delay in PUBLIC_FILE_BACKOFF_SECONDS:
        if delay:
            time.sleep(delay)
        try:
            return anonymous_json_once(session, url)
        except (requests.RequestException, PublicationError) as exc:
            last_error = exc
    raise PublicationError("bounded anonymous predecessor read failed") from last_error


def public_metadata_matches(actual: Mapping[str, Any], expected: Mapping[str, Any]) -> None:
    require(isinstance(actual, dict), "public metadata is not an object")
    require(actual.get("title") == TITLE, "public title differs")
    require(actual.get("language") == LANGUAGE, "public language differs")
    require(actual.get("version") == expected["version"], "public version differs")
    require(actual.get("publication_date") == expected["publication_date"], "public date differs")
    require(extract_license_id(actual.get("license")) == LICENSE_ID, "public license differs")
    require(actual.get("creators") == expected["creators"], "public creators array differs")
    require(actual.get("contributors") == expected["contributors"], "public contributors array differs")
    require(actual.get("keywords") == expected["keywords"], "public keywords array differs")
    require(
        actual.get("related_identifiers") == expected["related_identifiers"],
        "public related-identifiers array differs",
    )
    access = actual.get("access_right")
    require(access == "open", "public record is not open access")
    require(actual.get("description") == DESCRIPTION, "public description differs")
    require(actual.get("notes") == NOTES, "public notes differ")
    assert_publication_book(actual, "public record")


def public_files(record: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    raw = record.get("files")
    require(isinstance(raw, list), "public record has no files list")
    by_name: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    for item in raw:
        require(isinstance(item, dict), "public files list contains a non-object")
        name = remote_file_name(item)
        require(name not in by_name, f"public record repeats filename: {name}")
        by_name[name] = item
        order.append(name)
    require(
        order == list(EXPECTED_FILENAMES),
        "public record did not preserve the exact PDF-first file order",
    )
    require(order[0] == PDF_NAME, "public record does not expose the reader PDF first")
    return by_name


def public_download_url(item: Mapping[str, Any]) -> str:
    links = item.get("links")
    require(isinstance(links, dict), f"public file {remote_file_name(item)} has no links")
    for key in ("download", "content", "self"):
        value = links.get(key)
        if isinstance(value, str):
            return require_zenodo_url(value, f"public file {remote_file_name(item)} URL")
    raise PublicationError(f"public file {remote_file_name(item)} has no download URL")


def wait_for_public_record(
    session: requests.Session,
    record_id: int,
    expected_metadata: Mapping[str, Any],
    identities: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    last_error: Exception | None = None
    url = f"{API_BASE}/records/{record_id}"
    for delay in PUBLIC_RECORD_BACKOFF_SECONDS:
        if delay:
            time.sleep(delay)
        try:
            record = anonymous_json_once(session, url)
            require(
                api_record_id(record.get("id"), "public record ID") == record_id,
                "public record ID differs",
            )
            assert_concept_identity(record, "public maintenance record")
            public_metadata_matches(record.get("metadata", {}), expected_metadata)
            by_name = public_files(record)
            for name, item in by_name.items():
                require(remote_file_size(item) == identities[name]["bytes"], f"public byte count differs: {name}")
                if item.get("checksum") is not None or item.get("md5") is not None:
                    require(remote_file_md5(item) == identities[name]["md5"], f"public MD5 differs: {name}")
            return record, by_name
        except (requests.RequestException, PublicationError) as exc:
            last_error = exc
    raise PublicationError("bounded anonymous public-record readback did not converge") from last_error


def anonymous_file_identity(
    session: requests.Session, item: Mapping[str, Any], expected_bytes: int
) -> dict[str, Any]:
    url = public_download_url(item)
    last_error: Exception | None = None
    for delay in PUBLIC_FILE_BACKOFF_SECONDS:
        if delay:
            time.sleep(delay)
        try:
            response = anonymous_get(session, url, stream=True)
            if response.status_code != 200:
                raise PublicationError(
                    f"anonymous file read returned HTTP {response.status_code}: {remote_file_name(item)}"
                )
            require_zenodo_url(response.url, f"public file {remote_file_name(item)} response URL")
            digest = hashlib.sha256()
            total = 0
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    total += len(chunk)
                    digest.update(chunk)
            response.close()
            require(total == expected_bytes, f"anonymous byte count differs: {remote_file_name(item)}")
            return {"bytes": total, "sha256": digest.hexdigest(), "http": 200}
        except (requests.RequestException, PublicationError) as exc:
            last_error = exc
    raise PublicationError(f"bounded anonymous file readback failed: {remote_file_name(item)}") from last_error


def anonymous_readback(
    session: requests.Session,
    record_id: int,
    expected_metadata: Mapping[str, Any],
    identities: Mapping[str, Mapping[str, Any]],
    state: dict[str, Any],
    token: str,
) -> None:
    _record, by_name = wait_for_public_record(
        session, record_id, expected_metadata, identities
    )
    require(
        list(by_name) == list(EXPECTED_FILENAMES),
        "public readback mapping lost the PDF-first order",
    )
    state["public_file_order"] = list(by_name)
    state["public_resource_type"] = "publication/book"
    readback = state.setdefault("public_readback", {})
    require(isinstance(readback, dict), "durable public-readback field is invalid")
    for name in EXPECTED_FILENAMES:
        expected = identities[name]
        prior = readback.get(name)
        if prior == {
            "bytes": expected["bytes"],
            "sha256": expected["sha256"],
            "http": 200,
        }:
            continue
        actual = anonymous_file_identity(session, by_name[name], int(expected["bytes"]))
        require(actual["sha256"] == expected["sha256"], f"anonymous SHA-256 differs: {name}")
        readback[name] = actual
        save_state(state, token)
    require(set(readback) == set(EXPECTED_FILENAMES), "public-readback inventory is incomplete")
    state["public_record_url"] = f"{PUBLIC_BASE}/records/{record_id}"
    state["anonymous_record_http"] = 200
    if not at_least(state, "public_readback_verified"):
        advance(state, "public_readback_verified", token)
    else:
        save_state(state, token)


def markdown_receipt(
    *,
    state: Mapping[str, Any],
    identities: Mapping[str, Mapping[str, Any]],
) -> bytes:
    record_id = require_int(state.get("published_record_id"), "published receipt record ID")
    request = state.get("publish_request")
    require(isinstance(request, dict), "published state has no publish-request journal")
    publish_attempts = require_int(
        request.get("attempts_started"), "published request attempt count"
    )
    require(request.get("accepted_request") is True, "published request lacks acceptance evidence")
    require(
        state.get("public_file_order") == list(EXPECTED_FILENAMES),
        "published receipt lacks verified PDF-first public order",
    )
    require(
        state.get("public_resource_type") == "publication/book",
        "published receipt lacks verified publication/book resource type",
    )
    total_bytes = sum(int(identities[name]["bytes"]) for name in EXPECTED_FILENAMES)
    lines = [
        "# Zenodo Complete-Edition Maintenance Publication Receipt",
        "",
        "## Publication status",
        "",
        "**Status: PASS**",
        "",
        "The complete maintenance edition was published into the existing concept "
        "lineage and every released file was read back anonymously with exact byte "
        "and SHA-256 identity.",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Title | {TITLE} |",
        f"| Version | `{state['version']}` |",
        f"| Publication date | `{state['publication_date']}` |",
        f"| Existing concept DOI | `{CONCEPT_DOI}` |",
        f"| Predecessor record | `{PREDECESSOR_RECORD_ID}` |",
        f"| New record | `{record_id}` |",
        f"| New record DOI | `10.5281/zenodo.{record_id}` |",
        f"| Public record | <{PUBLIC_BASE}/records/{record_id}> |",
        "| Access | Open access |",
        "| Record-level license | CC BY-NC-SA 3.0 (`cc-by-nc-sa-3.0`) |",
        "| Language | Indonesian (`ind`) |",
        "| Resource type | Publication / book |",
        "| File order | Reader PDF first |",
        f"| Publish POST attempts | {publish_attempts} |",
        "| Accepted publish requests | One |",
        "",
        "The record-level license does not supersede the separate CC BY 4.0 license "
        "for original companions and completion modules. Rights remain per component; "
        "the collection has no flattened blanket license.",
        "",
        "## Anonymous public-byte verification",
        "",
        "| Filename | Bytes | HTTP | SHA-256 |",
        "|---|---:|---:|---|",
    ]
    for name in EXPECTED_FILENAMES:
        row = state["public_readback"][name]
        lines.append(f"| `{name}` | {row['bytes']:,} | {row['http']} | `{row['sha256']}` |")
    lines.extend(
        [
            f"| **Total** | **{total_bytes:,}** |  | **PASS** |",
            "",
            "## Metadata and accessibility",
            "",
            "The exact source-author creator entry, the single organization contributor "
            "entry, all eight keywords, and both source-derivation relations were "
            "preserved from the immutable predecessor record after strict validation. "
            "Stale partial-release wording was not retained.",
            "",
            "The localized offline/reflow HTML is the primary accessible surface; the "
            "PDF may remain untagged. Production provenance is OpenAI Codex "
            "gpt-5.6-sol, Ultra. This does not imply official endorsement.",
            "",
        ]
    )
    return "\n".join(lines).encode("utf-8")


def write_receipt(
    state: dict[str, Any], identities: Mapping[str, Mapping[str, Any]], token: str
) -> None:
    require(at_least(state, "public_readback_verified"), "public readback is not complete")
    payload = markdown_receipt(state=state, identities=identities)
    atomic_write(RECEIPT_PATH, payload, token)
    state["receipt"] = {
        "path": RECEIPT_PATH.relative_to(ROOT).as_posix(),
        "bytes": len(payload),
        "sha256": sha256_bytes(payload),
    }
    advance(state, "receipt_written", token)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish the seven-file complete maintenance package to the existing Zenodo concept."
    )
    parser.add_argument("--version", required=True, help="new public release version label")
    parser.add_argument("--publication-date", required=True, help="public date in YYYY-MM-DD form")
    parser.add_argument("--package-dir", required=True, type=Path, help="directory containing exactly seven release files")
    return parser.parse_args(argv)


def make_anonymous_session() -> requests.Session:
    session = requests.Session()
    session.trust_env = False
    session.auth = None
    session.proxies.clear()
    session.cookies.clear()
    session.headers.clear()
    session.headers.update({"User-Agent": "o003-complete-maintenance-publisher/1"})
    assert_anonymous_session(session)
    return session


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    version = validate_version(args.version)
    publication_date = validate_publication_date(args.publication_date)
    package_dir, package_relative, identities = validate_package_dir(args.package_dir, version)

    raw_token = os.environ.get("ZENODO_TOKEN")
    require(raw_token is not None and bool(raw_token.strip()), "ZENODO_TOKEN is required in the environment")
    token = raw_token.strip()
    require(len(token) >= 20, "ZENODO_TOKEN is implausibly short")
    require(not any(character.isspace() for character in token), "ZENODO_TOKEN contains whitespace")

    with publication_lock():
        with make_anonymous_session() as anonymous, requests.Session() as authenticated:
            authenticated.trust_env = False
            authenticated.auth = None
            authenticated.proxies.clear()
            authenticated.headers.clear()
            authenticated.headers.update(
                {
                    "Authorization": f"Bearer {token}",
                    "User-Agent": "o003-complete-maintenance-publisher/1",
                }
            )

            predecessor = anonymous_predecessor(anonymous)
            arrays = predecessor_arrays(predecessor)
            arrays_fingerprint = canonical_fingerprint(arrays)
            metadata = desired_metadata(
                version=version, publication_date=publication_date, arrays=arrays
            )

            state = load_or_initialize_state(
                version=version,
                publication_date=publication_date,
                package_relative=package_relative,
                identities=identities,
                predecessor_metadata_fingerprint=arrays_fingerprint,
                token=token,
            )
            if at_least(state, "receipt_written"):
                require(RECEIPT_PATH.is_file(), "state says complete but the receipt is absent")
                expected_receipt = state.get("receipt")
                require(isinstance(expected_receipt, dict), "durable receipt identity is invalid")
                actual_receipt = file_identity(RECEIPT_PATH)
                require(
                    actual_receipt["bytes"] == expected_receipt.get("bytes")
                    and actual_receipt["sha256"] == expected_receipt.get("sha256"),
                    "final receipt identity differs from durable state",
                )
                print(
                    f"PASS: Zenodo maintenance record {state['published_record_id']} "
                    "was already verified."
                )
                return 0

            if not at_least(state, "published"):
                draft_id, draft = ensure_draft(authenticated, state, token)
                if draft.get("submitted") is False:
                    draft = delete_inherited_files(authenticated, draft_id, draft, state, token)
                    draft = apply_metadata(authenticated, draft_id, metadata, state, token)
                    draft = upload_package_files(
                        authenticated,
                        draft_id,
                        package_dir,
                        identities,
                        state,
                        token,
                    )
                    draft = sort_files_pdf_first(
                        authenticated, draft_id, identities, state, token
                    )
                    prepublish_verify(draft, metadata, identities, state, token)
                record_id = publish_once(authenticated, draft_id, state, token)
            else:
                record_id = require_int(
                    state.get("published_record_id"), "durable published record ID"
                )

            anonymous_readback(
                anonymous, record_id, metadata, identities, state, token
            )
            write_receipt(state, identities, token)
            print(
                f"PASS: published and anonymously verified {PUBLIC_BASE}/records/{record_id}; "
                f"receipt: {RECEIPT_PATH.relative_to(ROOT).as_posix()}"
            )
            return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (PublicationError, requests.RequestException, OSError) as exc:
        message = str(exc)
        active_token = os.environ.get("ZENODO_TOKEN")
        if active_token:
            message = message.replace(active_token, "[redacted]")
            stripped_token = active_token.strip()
            if stripped_token:
                message = message.replace(stripped_token, "[redacted]")
        print(f"ERROR: {message}", file=sys.stderr)
        raise SystemExit(1)
