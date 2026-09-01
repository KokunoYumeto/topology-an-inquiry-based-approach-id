#!/usr/bin/env python3
"""Publish the complete terminology revision through Zenodo's current RDM API.

The legacy deposition endpoint is not used.  This publisher advances only the
existing record/concept lineage, journals every mutating boundary, uploads the
seven already-admitted package files, publishes once, and anonymously reads
every public byte back before writing a sanitized receipt.
"""

from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any, Mapping
from urllib.parse import quote, urlparse

import requests

import publish_zenodo_complete_maintenance as legacy


ROOT = Path(__file__).resolve().parents[1]
QA_DIR = ROOT / "qa"
STATE_PATH = QA_DIR / "ZENODO_COMPLETE_MAINTENANCE_RDM_STATE.json"
RECEIPT_PATH = QA_DIR / "ZENODO_COMPLETE_MAINTENANCE_PUBLICATION_RECEIPT.md"
API = "https://zenodo.org/api"
MEDIA_TYPE = "application/vnd.inveniordm.v1+json"
PREDECESSOR_ID = "22164668"
CONCEPT_ID = "22059894"
CONCEPT_DOI = "10.5281/zenodo.22059894"
TITLE = "Topologi: Pendekatan Berbasis Inkuiri"
LICENSE_ID = "cc-by-nc-sa-3.0"
LANGUAGE_ID = "ind"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
EXPECTED_ORDER = tuple(legacy.EXPECTED_FILENAMES)
DRAFT_STATUSES = {"draft", "new_version_draft"}
PHASES = (
    "initialized",
    "draft_created",
    "inherited_files_deleted",
    "metadata_updated",
    "files_initialized",
    "files_uploaded",
    "prepublish_verified",
    "publish_requested",
    "published",
    "public_readback_verified",
    "receipt_written",
)
GET_BACKOFF = (0, 2, 5)
PUBLIC_BACKOFF = (0, 2, 5, 10, 15, 20)
REQUEST_TIMEOUT = (30, 900)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class RdmPublicationError(RuntimeError):
    """A fail-closed publication invariant was not satisfied."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RdmPublicationError(message)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def fingerprint(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def clean_server_value(value: Any) -> Any:
    """Strip server-expanded vocabulary titles while retaining submitted IDs."""
    if isinstance(value, list):
        return [clean_server_value(item) for item in value]
    if not isinstance(value, dict):
        return value
    result: dict[str, Any] = {}
    for key, item in value.items():
        if key in {"title", "description", "props", "icon"} and "id" in value:
            continue
        result[key] = clean_server_value(item)
    return result


def person_identity(value: Mapping[str, Any]) -> dict[str, Any]:
    person = value.get("person_or_org")
    require(isinstance(person, dict), "creator/contributor has no person_or_org object")
    keep = {
        key: person.get(key)
        for key in ("type", "name", "given_name", "family_name")
        if person.get(key) is not None
    }
    identifiers = person.get("identifiers", [])
    require(isinstance(identifiers, list), "creator/contributor identifiers are malformed")
    if identifiers:
        normalized_identifiers = []
        for identifier in identifiers:
            require(
                isinstance(identifier, dict)
                and isinstance(identifier.get("scheme"), str)
                and isinstance(identifier.get("identifier"), str),
                "creator/contributor identifier is malformed",
            )
            normalized_identifiers.append(
                {"scheme": identifier["scheme"], "identifier": identifier["identifier"]}
            )
        keep["identifiers"] = normalized_identifiers
    affiliations = value.get("affiliations", [])
    require(isinstance(affiliations, list), "creator/contributor affiliations are malformed")
    normalized_affiliations = []
    for affiliation in affiliations:
        require(isinstance(affiliation, dict) and isinstance(affiliation.get("name"), str), "affiliation is malformed")
        normalized = {"name": affiliation["name"]}
        if affiliation.get("id") is not None:
            require(isinstance(affiliation.get("id"), str), "affiliation ID is malformed")
            normalized["id"] = affiliation["id"]
        normalized_affiliations.append(normalized)
    result: dict[str, Any] = {"person_or_org": keep}
    if normalized_affiliations:
        result["affiliations"] = normalized_affiliations
    role = value.get("role")
    if role is not None:
        require(isinstance(role, dict) and isinstance(role.get("id"), str), "contributor role is malformed")
        result["role"] = {"id": role["id"]}
    return result


def metadata_projection(value: Mapping[str, Any]) -> dict[str, Any]:
    resource_type = value.get("resource_type")
    require(isinstance(resource_type, dict), "metadata resource_type is missing")
    creators = value.get("creators")
    contributors = value.get("contributors")
    require(isinstance(creators, list), "metadata creators are missing")
    require(isinstance(contributors, list), "metadata contributors are missing")

    subjects: list[dict[str, str]] = []
    for item in value.get("subjects", []):
        require(isinstance(item, dict) and isinstance(item.get("subject"), str), "subject is malformed")
        subjects.append({"subject": item["subject"]})

    languages: list[dict[str, str]] = []
    for item in value.get("languages", []):
        require(isinstance(item, dict) and isinstance(item.get("id"), str), "language is malformed")
        languages.append({"id": item["id"]})

    related: list[dict[str, Any]] = []
    for item in value.get("related_identifiers", []):
        require(isinstance(item, dict), "related identifier is malformed")
        relation = item.get("relation_type")
        resource = item.get("resource_type")
        require(isinstance(relation, dict) and isinstance(relation.get("id"), str), "relation type is malformed")
        require(isinstance(resource, dict) and isinstance(resource.get("id"), str), "related resource type is malformed")
        related.append(
            {
                "identifier": item.get("identifier"),
                "scheme": item.get("scheme"),
                "relation_type": {"id": relation["id"]},
                "resource_type": {"id": resource["id"]},
            }
        )

    rights: list[dict[str, str]] = []
    for item in value.get("rights", []):
        require(isinstance(item, dict) and isinstance(item.get("id"), str), "rights entry is malformed")
        rights.append({"id": item["id"]})

    additional: list[dict[str, Any]] = []
    for item in value.get("additional_descriptions", []):
        require(isinstance(item, dict), "additional description is malformed")
        kind = item.get("type")
        require(isinstance(kind, dict) and isinstance(kind.get("id"), str), "additional-description type is malformed")
        additional.append({"description": item.get("description"), "type": {"id": kind["id"]}})

    return {
        "resource_type": {"id": resource_type.get("id")},
        "creators": [person_identity(item) for item in creators],
        "title": value.get("title"),
        "publisher": value.get("publisher"),
        "publication_date": value.get("publication_date"),
        "subjects": subjects,
        "contributors": [person_identity(item) for item in contributors],
        "languages": languages,
        "related_identifiers": related,
        "version": value.get("version"),
        "rights": rights,
        "description": value.get("description"),
        "additional_descriptions": additional,
    }


def validate_predecessor(record: Mapping[str, Any], *, require_latest: bool) -> dict[str, Any]:
    require(str(record.get("id")) == PREDECESSOR_ID, "predecessor record ID differs")
    require(record.get("status") == "published" and record.get("is_published") is True, "predecessor is not published")
    versions = record.get("versions")
    require(isinstance(versions, dict), "predecessor versions block is missing")
    if require_latest:
        require(versions.get("is_latest") is True, "predecessor is not the latest public version")
    parent = record.get("parent")
    require(isinstance(parent, dict) and str(parent.get("id")) == CONCEPT_ID, "predecessor concept ID differs")
    pids = parent.get("pids")
    require(isinstance(pids, dict), "predecessor parent has no PID block")
    doi = pids.get("doi")
    require(isinstance(doi, dict) and doi.get("identifier") == CONCEPT_DOI, "predecessor concept DOI differs")
    access = record.get("access")
    require(
        isinstance(access, dict)
        and access.get("record") == "public"
        and access.get("files") == "public"
        and access.get("status") == "open",
        "predecessor access is not public/open",
    )
    metadata = record.get("metadata")
    require(isinstance(metadata, dict), "predecessor metadata is missing")
    preserved_metadata_keys = {
        "resource_type",
        "creators",
        "title",
        "publisher",
        "publication_date",
        "subjects",
        "contributors",
        "languages",
        "related_identifiers",
        "version",
        "rights",
        "description",
        "additional_descriptions",
    }
    nonempty_unpreserved = {
        key for key, item in metadata.items()
        if key not in preserved_metadata_keys and item not in (None, [], {})
    }
    require(not nonempty_unpreserved, f"predecessor has unpreserved metadata fields: {sorted(nonempty_unpreserved)}")
    require(record.get("custom_fields") in (None, {}), "predecessor has nonempty custom fields")
    projected = metadata_projection(metadata)
    require(projected["title"] == TITLE, "predecessor title differs")
    require(projected["resource_type"] == {"id": "publication-book"}, "predecessor is not publication/book")
    require(projected["languages"] == [{"id": LANGUAGE_ID}], "predecessor language differs")
    require(projected["rights"] == [{"id": LICENSE_ID}], "predecessor license differs")
    require(len(projected["creators"]) == 1, "predecessor creator count differs")
    creator = projected["creators"][0]
    require(creator["person_or_org"].get("name") == "Schlicker, Steven", "predecessor creator differs")
    require(creator.get("affiliations") == [{"name": "Grand Valley State University"}], "predecessor creator affiliation differs")
    require(len(projected["contributors"]) == 1, "predecessor contributor count differs")
    require(projected["contributors"][0]["person_or_org"].get("name") == "TTP", "predecessor contributor differs")
    require(len(projected["subjects"]) == 8, "predecessor subject count differs")
    require(len(projected["related_identifiers"]) == 2, "predecessor relation count differs")

    files = record.get("files")
    require(isinstance(files, dict) and files.get("enabled") is True, "predecessor files are disabled")
    entries = files.get("entries")
    require(isinstance(entries, dict), "predecessor file entries are missing")
    require(set(entries) == set(EXPECTED_ORDER), "predecessor has an unexpected file inventory")
    for key, entry in entries.items():
        require(isinstance(entry, dict), f"predecessor file entry is malformed: {key}")
        require(entry.get("key") == key, f"predecessor file key differs: {key}")
    return projected


def desired_metadata(predecessor: Mapping[str, Any], version: str, publication_date: str) -> dict[str, Any]:
    creators = copy.deepcopy(predecessor["creators"])
    subjects = copy.deepcopy(predecessor["subjects"])
    related = copy.deepcopy(predecessor["related_identifiers"])
    metadata = {
        "resource_type": {"id": "publication-book"},
        "creators": creators,
        "title": TITLE,
        "publisher": "Zenodo",
        "publication_date": publication_date,
        "subjects": subjects,
        "contributors": [
            {
                "person_or_org": {"type": "organizational", "name": "TTP"},
                "role": {"id": "other"},
            }
        ],
        "languages": [{"id": LANGUAGE_ID}],
        "related_identifiers": related,
        "version": version,
        "rights": [{"id": LICENSE_ID}],
        "description": legacy.DESCRIPTION,
        "additional_descriptions": [
            {"description": legacy.NOTES, "type": {"id": "notes"}}
        ],
    }
    serialized = json.dumps(metadata, ensure_ascii=False, sort_keys=True)
    require(serialized.count('"TTP"') == 1, "TTP must occur exactly once in metadata")
    require("Translation and Transcription Project" not in serialized, "forbidden organization expansion appears in metadata")
    require(not TITLE.startswith("TTP"), "canonical title is mangled")
    require(MODEL in serialized, "exact model provenance is absent")
    return metadata


def record_payload(metadata: Mapping[str, Any], *, ordered: bool) -> dict[str, Any]:
    files: dict[str, Any] = {"enabled": True}
    if ordered:
        files["order"] = list(EXPECTED_ORDER)
        files["default_preview"] = legacy.PDF_NAME
    return {
        "metadata": copy.deepcopy(dict(metadata)),
        "access": {"record": "public", "files": "public"},
        "files": files,
        "custom_fields": {},
    }


def safe_url(url: str) -> str:
    parsed = urlparse(url)
    require(parsed.scheme == "https" and parsed.hostname == "zenodo.org", f"unsafe Zenodo URL: {url}")
    require(parsed.port in (None, 443), f"unsafe Zenodo port: {url}")
    require(parsed.username is None and parsed.password is None and parsed.fragment == "", f"unsafe Zenodo URL: {url}")
    require(parsed.path.startswith("/api/"), f"unsafe Zenodo API path: {url}")
    return url


def session_for(token: str | None) -> requests.Session:
    session = requests.Session()
    session.trust_env = False
    session.auth = None
    session.cookies.clear()
    session.headers.update({"Accept": MEDIA_TYPE})
    if token is not None:
        session.headers["Authorization"] = f"Bearer {token}"
    return session


def response_json(response: requests.Response, label: str) -> dict[str, Any]:
    try:
        value = response.json()
    except (ValueError, json.JSONDecodeError) as exc:
        raise RdmPublicationError(f"{label} did not return JSON") from exc
    require(isinstance(value, dict), f"{label} JSON root is not an object")
    return value


def get_json(
    session: requests.Session,
    url: str,
    *,
    label: str,
    params: Mapping[str, Any] | None = None,
    allowed: tuple[int, ...] = (200,),
    backoff: tuple[int, ...] = GET_BACKOFF,
) -> tuple[int, dict[str, Any] | None]:
    safe_url(url)
    last_status = 0
    for delay in backoff:
        if delay:
            time.sleep(delay)
        response = session.get(url, params=params, timeout=REQUEST_TIMEOUT, allow_redirects=False)
        try:
            last_status = response.status_code
            if last_status in allowed:
                if last_status == 404:
                    return 404, None
                return last_status, response_json(response, label)
            if last_status not in {502, 503, 504}:
                break
        finally:
            response.close()
    raise RdmPublicationError(f"Zenodo returned HTTP {last_status} for {label}")


def mutate_json(
    session: requests.Session,
    method: str,
    url: str,
    *,
    label: str,
    expected: tuple[int, ...],
    payload: Any | None = None,
    raw: bytes | None = None,
) -> tuple[int, dict[str, Any] | None]:
    safe_url(url)
    require(not (payload is not None and raw is not None), "request cannot have both JSON and raw payloads")
    kwargs: dict[str, Any] = {
        "timeout": REQUEST_TIMEOUT,
        "allow_redirects": False,
    }
    if payload is not None:
        kwargs["json"] = payload
    if raw is not None:
        kwargs["data"] = raw
        kwargs["headers"] = {"Content-Type": "application/octet-stream", "Accept": MEDIA_TYPE}
    try:
        response = session.request(method, url, **kwargs)
    except requests.ConnectTimeout as exc:
        raise RdmPublicationError(f"connect timeout before {label}; request not retried") from exc
    except requests.RequestException as exc:
        raise RdmPublicationError(f"uncertain transport failure during {label}; reconcile before retry") from exc
    try:
        require(response.status_code in expected, f"Zenodo returned HTTP {response.status_code} for {label}")
        if response.status_code == 204 or not response.content:
            return response.status_code, None
        return response.status_code, response_json(response, label)
    finally:
        response.close()


def public_predecessor(session: requests.Session) -> dict[str, Any]:
    _, record = get_json(session, f"{API}/records/{PREDECESSOR_ID}", label="public predecessor")
    require(record is not None, "public predecessor is missing")
    return record


def owned_predecessor(session: requests.Session) -> dict[str, Any]:
    _, result = get_json(
        session,
        f"{API}/user/records",
        label="owned predecessor search",
        params={"q": f"id:{PREDECESSOR_ID}", "allversions": "true", "size": 10},
    )
    require(result is not None, "owned predecessor search is missing")
    hits = result.get("hits")
    require(isinstance(hits, dict), "owned predecessor search has no hits object")
    rows = hits.get("hits")
    require(isinstance(rows, list) and len(rows) == 1, "owned predecessor search did not return exactly one record")
    require(isinstance(rows[0], dict), "owned predecessor row is malformed")
    return rows[0]


def latest_owned_concept_draft(session: requests.Session) -> dict[str, Any] | None:
    _, result = get_json(
        session,
        f"{API}/user/records",
        label="owned concept-draft search",
        params={
            "q": f'metadata.title:"{TITLE}"',
            "allversions": "true",
            "size": 25,
            "sort": "newest",
        },
    )
    require(result is not None, "owned concept-draft search is missing")
    hits = result.get("hits")
    require(isinstance(hits, dict), "owned concept-draft search has no hits object")
    rows = hits.get("hits")
    require(isinstance(rows, list), "owned concept-draft search hits are malformed")
    candidates = []
    for row in rows:
        require(isinstance(row, dict), "owned concept-draft row is malformed")
        parent = row.get("parent")
        versions = row.get("versions")
        if (
            isinstance(parent, dict)
            and str(parent.get("id")) == CONCEPT_ID
            and row.get("is_published") is False
            and row.get("status") in DRAFT_STATUSES
            and isinstance(versions, dict)
            and versions.get("is_latest_draft") is True
        ):
            candidates.append(row)
    require(len(candidates) <= 1, "more than one latest draft exists in the concept")
    return candidates[0] if candidates else None


def draft_url(record_id: str) -> str:
    require(record_id.isdigit(), "draft ID is not numeric")
    return f"{API}/records/{record_id}/draft"


def file_url(record_id: str, key: str) -> str:
    require(key in EXPECTED_ORDER, "file key is outside the admitted package")
    return f"{draft_url(record_id)}/files/{quote(key, safe='')}"


def file_content_url(record_id: str, key: str) -> str:
    return f"{file_url(record_id, key)}/content"


def file_commit_url(record_id: str, key: str) -> str:
    return f"{file_url(record_id, key)}/commit"


def public_file_url(record_id: str, key: str) -> str:
    require(record_id.isdigit(), "public record ID is not numeric")
    require(key in EXPECTED_ORDER, "public file key is outside the admitted package")
    return f"{API}/records/{record_id}/files/{quote(key, safe='')}"


def state_base(
    version: str,
    publication_date: str,
    package_relative: str,
    identities: Mapping[str, Mapping[str, Any]],
    predecessor_fingerprint: str,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "operation": "zenodo_complete_maintenance_current_rdm",
        "phase": "initialized",
        "created_utc": now_utc(),
        "updated_utc": now_utc(),
        "predecessor_record_id": PREDECESSOR_ID,
        "concept_record_id": CONCEPT_ID,
        "concept_doi": CONCEPT_DOI,
        "version": version,
        "publication_date": publication_date,
        "package_dir": package_relative,
        "files": copy.deepcopy(dict(identities)),
        "predecessor_fingerprint": predecessor_fingerprint,
        "create_request": None,
        "draft_id": None,
        "deleted_inherited_files": [],
        "uploaded_files": {},
        "publish_request": None,
        "record_id": None,
        "doi": None,
        "public_readback": {},
    }


def save_state(state: dict[str, Any], token: str) -> None:
    state["updated_utc"] = now_utc()
    legacy.atomic_write(STATE_PATH, canonical_json(state), token)


def load_state(
    version: str,
    publication_date: str,
    package_relative: str,
    identities: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any] | None:
    if not STATE_PATH.is_file():
        return None
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RdmPublicationError("RDM publication state is malformed") from exc
    require(isinstance(state, dict) and state.get("schema_version") == 1, "RDM publication state schema differs")
    require(state.get("operation") == "zenodo_complete_maintenance_current_rdm", "RDM state belongs to another operation")
    require(state.get("version") == version and state.get("publication_date") == publication_date, "RDM state release identity differs")
    require(state.get("package_dir") == package_relative, "RDM state package path differs")
    require(state.get("phase") in PHASES, "RDM state phase differs")
    if state.get("files") != dict(identities):
        require(
            PHASES.index(str(state.get("phase"))) < PHASES.index("prepublish_verified"),
            "RDM state package bytes differ after prepublication verification",
        )
        require(state.get("publish_request") is None and state.get("record_id") is None, "RDM package changed after publication began")
        uploaded = state.get("uploaded_files")
        require(isinstance(uploaded, dict), "RDM uploaded-file state is malformed")
        state["uploaded_files"] = {
            key: value
            for key, value in uploaded.items()
            if key in identities and value == identities[key]
        }
        state["files"] = copy.deepcopy(dict(identities))
        state["package_resealed_utc"] = now_utc()
        if PHASES.index(str(state.get("phase"))) > PHASES.index("files_initialized"):
            state["phase"] = "files_initialized"
        state["_needs_save"] = True
    return state


def advance(state: dict[str, Any], phase: str, token: str) -> None:
    require(phase in PHASES, f"unknown phase: {phase}")
    require(PHASES.index(phase) >= PHASES.index(str(state["phase"])), "publication phase would regress")
    state["phase"] = phase
    save_state(state, token)


def current_draft(session: requests.Session, record_id: str) -> dict[str, Any] | None:
    status, draft = get_json(
        session,
        draft_url(record_id),
        label=f"draft {record_id}",
        allowed=(200, 404),
    )
    return draft if status == 200 else None


def create_version(session: requests.Session, state: dict[str, Any], token: str) -> dict[str, Any]:
    require(state.get("create_request") is None, "new-version request was already attempted without a bound draft")
    require(current_draft(session, PREDECESSOR_ID) is None, "an unbound draft already exists for the predecessor")
    state["create_request"] = {"intent_utc": now_utc(), "status": "intent_recorded"}
    save_state(state, token)
    _, response = mutate_json(
        session,
        "POST",
        f"{API}/records/{PREDECESSOR_ID}/versions",
        label="create new version",
        expected=(201,),
        payload={},
    )
    require(response is not None, "new-version response is empty")
    bind_created_draft(response, state, token)
    return response


def bind_created_draft(draft: Mapping[str, Any], state: dict[str, Any], token: str) -> None:
    draft_id = str(draft.get("id"))
    require(draft_id.isdigit() and draft_id != PREDECESSOR_ID, "new-version response has no distinct numeric draft ID")
    require(draft.get("status") in DRAFT_STATUSES and draft.get("is_published") is False, "new-version response is not a draft")
    parent = draft.get("parent")
    require(isinstance(parent, dict) and str(parent.get("id")) == CONCEPT_ID, "new-version draft belongs to another concept")
    validate_draft_lineage(draft, draft_id)
    create_request = state.get("create_request")
    require(isinstance(create_request, dict), "new-version intent is missing")
    state["create_request"] = {
        **create_request,
        "status": "response_bound",
        "response_utc": now_utc(),
        "draft_id": draft_id,
        "response_fingerprint": fingerprint(draft),
    }
    state["draft_id"] = draft_id
    advance(state, "draft_created", token)


def reconcile_create(session: requests.Session, state: dict[str, Any], token: str) -> dict[str, Any]:
    create_request = state.get("create_request")
    require(isinstance(create_request, dict) and create_request.get("status") == "intent_recorded", "new-version intent is not reconcilable")
    draft = current_draft(session, PREDECESSOR_ID)
    if draft is None:
        draft = latest_owned_concept_draft(session)
    require(draft is not None, "new-version request outcome is uncertain and no bound draft is visible; do not retry")
    bind_created_draft(draft, state, token)
    return draft


def validate_draft_lineage(draft: Mapping[str, Any], draft_id: str) -> None:
    require(str(draft.get("id")) == draft_id, "draft ID differs")
    require(draft.get("status") in DRAFT_STATUSES and draft.get("is_published") is False, "record is not an unpublished draft")
    parent = draft.get("parent")
    require(isinstance(parent, dict) and str(parent.get("id")) == CONCEPT_ID, "draft concept differs")
    versions = draft.get("versions")
    require(isinstance(versions, dict) and versions.get("is_latest_draft") is True, "draft is not the latest draft")


def draft_entries(draft: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    files = draft.get("files")
    require(isinstance(files, dict) and files.get("enabled") is True, "draft files are disabled")
    entries = files.get("entries")
    require(isinstance(entries, dict), "draft file entries are missing")
    require(all(isinstance(key, str) and isinstance(value, dict) for key, value in entries.items()), "draft file entry is malformed")
    return entries


def delete_inherited_files(session: requests.Session, state: dict[str, Any], token: str) -> None:
    draft_id = str(state.get("draft_id"))
    draft = current_draft(session, draft_id)
    require(draft is not None, "bound draft disappeared")
    validate_draft_lineage(draft, draft_id)
    entries = draft_entries(draft)
    require(set(entries).issubset(set(EXPECTED_ORDER)), "bound draft has an unexpected inherited file")
    deleted = set(state.get("deleted_inherited_files", []))
    require(deleted.issubset(set(EXPECTED_ORDER)), "state has an unexpected deleted-file key")
    for key in EXPECTED_ORDER:
        if key not in entries:
            deleted.add(key)
            continue
        mutate_json(session, "DELETE", file_url(draft_id, key), label=f"delete inherited file {key}", expected=(204,))
        deleted.add(key)
        state["deleted_inherited_files"] = sorted(deleted, key=str.casefold)
        save_state(state, token)
    draft = current_draft(session, draft_id)
    require(draft is not None and draft_entries(draft) == {}, "inherited files were not fully deleted")
    state["deleted_inherited_files"] = sorted(deleted, key=str.casefold)
    advance(state, "inherited_files_deleted", token)


def update_metadata(
    session: requests.Session,
    state: dict[str, Any],
    token: str,
    metadata: Mapping[str, Any],
    *,
    ordered: bool,
) -> dict[str, Any]:
    draft_id = str(state.get("draft_id"))
    _, response = mutate_json(
        session,
        "PUT",
        draft_url(draft_id),
        label="update draft metadata" if not ordered else "set draft file order",
        expected=(200,),
        payload=record_payload(metadata, ordered=ordered),
    )
    require(response is not None, "draft update response is empty")
    validate_draft_lineage(response, draft_id)
    require(metadata_projection(response.get("metadata", {})) == dict(metadata), "draft metadata differs after update")
    access = response.get("access")
    require(isinstance(access, dict) and access.get("record") == "public" and access.get("files") == "public", "draft access differs")
    return response


def initialize_files(session: requests.Session, state: dict[str, Any], token: str) -> None:
    draft_id = str(state.get("draft_id"))
    draft = current_draft(session, draft_id)
    require(draft is not None, "bound draft disappeared before file initialization")
    entries = draft_entries(draft)
    if not entries:
        mutate_json(
            session,
            "POST",
            f"{draft_url(draft_id)}/files",
            label="initialize seven release files",
            expected=(201,),
            payload=[{"key": key} for key in EXPECTED_ORDER],
        )
        draft = current_draft(session, draft_id)
        require(draft is not None, "bound draft disappeared after file initialization")
        entries = draft_entries(draft)
    require(set(entries) == set(EXPECTED_ORDER), "initialized file inventory differs")
    advance(state, "files_initialized", token)


def entry_bytes_match(entry: Mapping[str, Any], expected: Mapping[str, Any]) -> bool:
    checksum = entry.get("checksum")
    return (
        entry.get("size") == expected["bytes"]
        and checksum == f"md5:{expected['md5']}"
    )


def entry_matches(entry: Mapping[str, Any], expected: Mapping[str, Any]) -> bool:
    return entry.get("status") == "completed" and entry_bytes_match(entry, expected)


def current_file_entry(session: requests.Session, draft_id: str, key: str) -> dict[str, Any]:
    _, entry = get_json(
        session,
        file_url(draft_id, key),
        label=f"draft file detail {key}",
    )
    require(entry is not None and entry.get("key") == key, f"draft file detail differs: {key}")
    return entry


def reinitialize_file(session: requests.Session, draft_id: str, key: str) -> dict[str, Any]:
    mutate_json(
        session,
        "DELETE",
        file_url(draft_id, key),
        label=f"delete superseded draft file {key}",
        expected=(204,),
    )
    mutate_json(
        session,
        "POST",
        f"{draft_url(draft_id)}/files",
        label=f"reinitialize superseded draft file {key}",
        expected=(201,),
        payload=[{"key": key}],
    )
    return current_file_entry(session, draft_id, key)


def upload_files(
    session: requests.Session,
    state: dict[str, Any],
    token: str,
    package_dir: Path,
    identities: Mapping[str, Mapping[str, Any]],
) -> None:
    draft_id = str(state.get("draft_id"))
    uploaded = state.get("uploaded_files")
    require(isinstance(uploaded, dict), "uploaded-files state is malformed")
    for key in EXPECTED_ORDER:
        draft = current_draft(session, draft_id)
        require(draft is not None, "bound draft disappeared during upload")
        listed_entry = draft_entries(draft).get(key)
        require(isinstance(listed_entry, dict), f"initialized file entry disappeared: {key}")
        entry = current_file_entry(session, draft_id, key)
        if entry_matches(entry, identities[key]):
            uploaded[key] = copy.deepcopy(dict(identities[key]))
            save_state(state, token)
            continue
        if entry.get("status") == "completed":
            entry = reinitialize_file(session, draft_id, key)
        canonical_content_url = file_content_url(draft_id, key)
        canonical_commit_url = file_commit_url(draft_id, key)
        if not entry_bytes_match(entry, identities[key]):
            payload = (package_dir / key).read_bytes()
            require(len(payload) == identities[key]["bytes"], f"package file changed before upload: {key}")
            mutate_json(session, "PUT", canonical_content_url, label=f"upload {key}", expected=(200,), raw=payload)
        mutate_json(session, "POST", canonical_commit_url, label=f"commit {key}", expected=(200,))
        committed = current_file_entry(session, draft_id, key)
        require(entry_matches(committed, identities[key]), f"uploaded file identity differs: {key}")
        uploaded[key] = copy.deepcopy(dict(identities[key]))
        save_state(state, token)
    require(set(uploaded) == set(EXPECTED_ORDER), "not all seven files were uploaded")
    advance(state, "files_uploaded", token)


def verify_draft(
    session: requests.Session,
    state: dict[str, Any],
    metadata: Mapping[str, Any],
    identities: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    draft_id = str(state.get("draft_id"))
    draft = current_draft(session, draft_id)
    require(draft is not None, "bound draft disappeared before publish")
    validate_draft_lineage(draft, draft_id)
    require(metadata_projection(draft.get("metadata", {})) == dict(metadata), "prepublish metadata differs")
    access = draft.get("access")
    require(isinstance(access, dict) and access.get("record") == "public" and access.get("files") == "public", "prepublish access differs")
    files = draft.get("files")
    require(isinstance(files, dict), "prepublish files block is missing")
    order = files.get("order")
    require(isinstance(order, list) and (not order or tuple(order) == EXPECTED_ORDER), "prepublish file order differs")
    require(files.get("default_preview") == legacy.PDF_NAME, "prepublish default preview is not the PDF")
    entries = draft_entries(draft)
    require(set(entries) == set(EXPECTED_ORDER), "prepublish file inventory differs")
    for key in EXPECTED_ORDER:
        require(
            entry_matches(current_file_entry(session, draft_id, key), identities[key]),
            f"prepublish file identity differs: {key}",
        )
    return draft


def publish(session: requests.Session, state: dict[str, Any], token: str) -> dict[str, Any]:
    require(state.get("publish_request") is None, "publish request was already attempted without a bound result")
    draft_id = str(state.get("draft_id"))
    state["publish_request"] = {"intent_utc": now_utc(), "status": "intent_recorded"}
    advance(state, "publish_requested", token)
    _, response = mutate_json(
        session,
        "POST",
        f"{draft_url(draft_id)}/actions/publish",
        label="publish complete maintenance version",
        expected=(202,),
    )
    require(response is not None, "publish response is empty")
    bind_published_record(response, state, token)
    return response


def bind_published_record(record: Mapping[str, Any], state: dict[str, Any], token: str) -> None:
    record_id = str(record.get("id"))
    draft_id = str(state.get("draft_id"))
    require(record_id == draft_id and record.get("status") == "published", "publish response is not the bound public record")
    pids = record.get("pids")
    require(isinstance(pids, dict) and isinstance(pids.get("doi"), dict), "publish response has no DOI")
    doi = pids["doi"].get("identifier")
    require(doi == f"10.5281/zenodo.{record_id}", "publish response DOI differs")
    publish_request = state.get("publish_request")
    require(isinstance(publish_request, dict), "publish intent is missing")
    state["publish_request"] = {
        **publish_request,
        "status": "response_bound",
        "response_utc": now_utc(),
        "record_id": record_id,
        "response_fingerprint": fingerprint(record),
    }
    state["record_id"] = record_id
    state["doi"] = doi
    advance(state, "published", token)


def reconcile_publish(
    authenticated: requests.Session,
    anonymous: requests.Session,
    state: dict[str, Any],
    token: str,
) -> dict[str, Any]:
    publish_request = state.get("publish_request")
    require(isinstance(publish_request, dict) and publish_request.get("status") == "intent_recorded", "publish intent is not reconcilable")
    draft_id = str(state.get("draft_id"))
    status, record = get_json(
        anonymous,
        f"{API}/records/{draft_id}",
        label=f"reconcile public record {draft_id}",
        allowed=(200, 404),
        backoff=PUBLIC_BACKOFF,
    )
    if status == 200:
        require(record is not None, "reconciled public record is empty")
        bind_published_record(record, state, token)
        return record
    draft = current_draft(authenticated, draft_id)
    require(draft is None, "publish request outcome is uncertain and the draft still exists; do not retry")
    raise RdmPublicationError("publish request outcome is uncertain and neither public record nor draft is visible; do not retry")


def anonymous_record(session: requests.Session, record_id: str) -> dict[str, Any]:
    last_error: Exception | None = None
    for delay in PUBLIC_BACKOFF:
        if delay:
            time.sleep(delay)
        try:
            _, record = get_json(
                session,
                f"{API}/records/{record_id}",
                label=f"public record {record_id}",
                backoff=(0,),
            )
            require(record is not None, "public record response is empty")
            if record.get("status") == "published":
                return record
        except Exception as exc:  # bounded public integration backoff
            last_error = exc
    if last_error is not None:
        raise RdmPublicationError(f"public record did not integrate: {last_error}") from last_error
    raise RdmPublicationError("public record did not integrate")


def anonymous_file_identity(
    session: requests.Session,
    record_id: str,
    key: str,
    expected: Mapping[str, Any],
) -> dict[str, Any]:
    url = f"{API}/records/{record_id}/files/{quote(key, safe='')}/content"
    safe_url(url)
    response = session.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=False, stream=True)
    try:
        require(response.status_code == 200, f"public download returned HTTP {response.status_code}: {key}")
        sha = hashlib.sha256()
        md5 = hashlib.md5(usedforsecurity=False)
        total = 0
        for chunk in response.iter_content(1024 * 1024):
            if not chunk:
                continue
            total += len(chunk)
            require(total <= expected["bytes"], f"public download exceeds expected size: {key}")
            sha.update(chunk)
            md5.update(chunk)
        observed = {"bytes": total, "md5": md5.hexdigest(), "sha256": sha.hexdigest()}
        require(observed == dict(expected), f"public file bytes differ: {key}")
        return observed
    finally:
        response.close()


def anonymous_readback(
    session: requests.Session,
    state: dict[str, Any],
    metadata: Mapping[str, Any],
    identities: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    record_id = str(state.get("record_id"))
    record = anonymous_record(session, record_id)
    require(str(record.get("id")) == record_id, "public record ID differs")
    parent = record.get("parent")
    require(isinstance(parent, dict) and str(parent.get("id")) == CONCEPT_ID, "public concept ID differs")
    parent_pids = parent.get("pids")
    require(
        isinstance(parent_pids, dict)
        and isinstance(parent_pids.get("doi"), dict)
        and parent_pids["doi"].get("identifier") == CONCEPT_DOI,
        "public concept DOI differs",
    )
    pids = record.get("pids")
    require(
        isinstance(pids, dict)
        and isinstance(pids.get("doi"), dict)
        and pids["doi"].get("identifier") == state.get("doi"),
        "public version DOI differs",
    )
    access = record.get("access")
    require(
        isinstance(access, dict)
        and access.get("record") == "public"
        and access.get("files") == "public"
        and access.get("status") == "open",
        "public record is not open",
    )
    require(metadata_projection(record.get("metadata", {})) == dict(metadata), "public metadata differs")
    files = record.get("files")
    require(isinstance(files, dict), "public files block is missing")
    order = files.get("order")
    require(isinstance(order, list) and (not order or tuple(order) == EXPECTED_ORDER), "public file order differs")
    require(files.get("default_preview") == legacy.PDF_NAME, "public default preview is not the PDF")
    entries = draft_entries(record)
    require(set(entries) == set(EXPECTED_ORDER), "public file inventory differs")
    for key in EXPECTED_ORDER:
        require(entry_bytes_match(entries[key], identities[key]), f"public file metadata differs: {key}")
        _, detail = get_json(
            session,
            public_file_url(record_id, key),
            label=f"public file detail {key}",
            backoff=PUBLIC_BACKOFF,
        )
        require(detail is not None and entry_matches(detail, identities[key]), f"public file detail differs: {key}")

    downloaded: dict[str, dict[str, Any]] = {}
    for key in EXPECTED_ORDER:
        downloaded[key] = anonymous_file_identity(session, record_id, key, identities[key])
    require(next(iter(downloaded)) == legacy.PDF_NAME, "anonymous readback was not PDF-first")

    latest: dict[str, Any] | None = None
    for delay in PUBLIC_BACKOFF:
        if delay:
            time.sleep(delay)
        _, candidate = get_json(
            session,
            f"{API}/records/{PREDECESSOR_ID}/versions/latest",
            label="public latest version",
            backoff=(0,),
        )
        if candidate is not None and str(candidate.get("id")) == record_id:
            latest = candidate
            break
    require(latest is not None, "concept latest version does not resolve to the new record")
    return {
        "record_id": record_id,
        "doi": state.get("doi"),
        "record_url": f"https://zenodo.org/records/{record_id}",
        "concept_doi": CONCEPT_DOI,
        "concept_url": f"https://doi.org/{CONCEPT_DOI}",
        "file_order": list(EXPECTED_ORDER),
        "files": downloaded,
        "metadata_fingerprint": fingerprint(metadata_projection(record["metadata"])),
        "verified_utc": now_utc(),
    }


def receipt_payload(state: Mapping[str, Any], readback: Mapping[str, Any]) -> bytes:
    lines = [
        "# Complete-edition terminology-maintenance Zenodo receipt",
        "",
        "- **Status:** PASS",
        f"- **Verified:** {readback['verified_utc']}",
        f"- **Public record:** https://zenodo.org/records/{readback['record_id']}",
        f"- **Version DOI:** https://doi.org/{readback['doi']}",
        f"- **Concept DOI:** https://doi.org/{CONCEPT_DOI}",
        f"- **Version:** `{state['version']}`",
        "- **Access:** public record and public files",
        "- **Resource type:** publication/book",
        "- **Verification mode:** anonymous public metadata and full-byte readback; no credentials used",
        "",
        "## Public files",
        "",
        "The PDF is the public default preview and the first file in this receipt/package order.",
        "",
        "| Order | Filename | Bytes | SHA-256 | Result |",
        "| ---: | --- | ---: | --- | --- |",
    ]
    for index, key in enumerate(EXPECTED_ORDER, start=1):
        row = readback["files"][key]
        lines.append(f"| {index} | `{key}` | {row['bytes']:,} | `{row['sha256']}` | MATCH |")
    lines.extend(
        [
            "",
            "## Metadata and lineage",
            "",
            f"The public record remains in concept DOI `{CONCEPT_DOI}`, uses the exact title `{TITLE}`, language `ind`, and conservative collection license `{LICENSE_ID}`. The creator, single organization contributor, component-rights explanation, non-endorsement, and exact production provenance are retained.",
            "",
            "No credentials were used for readback, and this receipt contains no credential material.",
            "",
        ]
    )
    payload = "\n".join(lines).encode("utf-8")
    require(b"ZENODO_TOKEN" not in payload and b"Authorization" not in payload, "receipt contains a credential marker")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True)
    parser.add_argument("--publication-date", required=True)
    parser.add_argument("--package-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    version = legacy.validate_version(args.version)
    publication_date = legacy.validate_publication_date(args.publication_date)
    token_raw = os.environ.get("ZENODO_TOKEN")
    require(token_raw is not None and bool(token_raw.strip()), "ZENODO_TOKEN is required in the environment")
    token = token_raw.strip()
    require(len(token) >= 20 and not any(character.isspace() for character in token), "ZENODO_TOKEN is malformed")
    package_dir, package_relative, identities = legacy.validate_package_dir(args.package_dir, version)

    with legacy.publication_lock():
        authenticated = session_for(token)
        anonymous = session_for(None)
        try:
            state = load_state(version, publication_date, package_relative, identities)
            if state is not None and state.pop("_needs_save", False):
                save_state(state, token)
            already_published = (
                state is not None
                and PHASES.index(str(state["phase"])) >= PHASES.index("published")
            )
            public_source = public_predecessor(anonymous)
            owned_source = owned_predecessor(authenticated)
            public_projection = validate_predecessor(public_source, require_latest=not already_published)
            owned_projection = validate_predecessor(owned_source, require_latest=not already_published)
            require(public_projection == owned_projection, "public and owned predecessor metadata differ")
            predecessor_fingerprint = fingerprint(
                {
                    "metadata": public_projection,
                    "access": public_source.get("access"),
                    "files": {
                        key: {
                            "size": item.get("size"),
                            "checksum": item.get("checksum"),
                        }
                        for key, item in sorted(draft_entries(public_source).items())
                    },
                }
            )
            metadata = desired_metadata(public_projection, version, publication_date)
            if state is None:
                require(current_draft(authenticated, PREDECESSOR_ID) is None, "a predecessor draft existed before this operation")
                state = state_base(version, publication_date, package_relative, identities, predecessor_fingerprint)
                save_state(state, token)
            require(state.get("predecessor_fingerprint") == predecessor_fingerprint, "predecessor changed after operation initialization")

            if PHASES.index(state["phase"]) < PHASES.index("draft_created"):
                if state.get("create_request") is None:
                    create_version(authenticated, state, token)
                else:
                    reconcile_create(authenticated, state, token)
            draft_id = str(state.get("draft_id"))
            require(draft_id.isdigit(), "state has no bound draft ID")

            if PHASES.index(state["phase"]) < PHASES.index("inherited_files_deleted"):
                delete_inherited_files(authenticated, state, token)
            if PHASES.index(state["phase"]) < PHASES.index("metadata_updated"):
                update_metadata(authenticated, state, token, metadata, ordered=False)
                advance(state, "metadata_updated", token)
            if PHASES.index(state["phase"]) < PHASES.index("files_initialized"):
                initialize_files(authenticated, state, token)
            if PHASES.index(state["phase"]) < PHASES.index("files_uploaded"):
                upload_files(authenticated, state, token, package_dir, identities)
            if PHASES.index(state["phase"]) < PHASES.index("prepublish_verified"):
                update_metadata(authenticated, state, token, metadata, ordered=True)
                verify_draft(authenticated, state, metadata, identities)
                advance(state, "prepublish_verified", token)
            if PHASES.index(state["phase"]) < PHASES.index("published"):
                if state.get("publish_request") is None:
                    verify_draft(authenticated, state, metadata, identities)
                    publish(authenticated, state, token)
                else:
                    reconcile_publish(authenticated, anonymous, state, token)
            if PHASES.index(state["phase"]) < PHASES.index("public_readback_verified"):
                readback = anonymous_readback(anonymous, state, metadata, identities)
                state["public_readback"] = readback
                advance(state, "public_readback_verified", token)
            else:
                readback = state.get("public_readback")
                require(isinstance(readback, dict) and readback, "state has no public readback")
                repeated = anonymous_readback(anonymous, state, metadata, identities)
                stable_keys = tuple(key for key in repeated if key != "verified_utc")
                require(
                    {key: repeated[key] for key in stable_keys}
                    == {key: readback.get(key) for key in stable_keys},
                    "repeat public readback differs",
                )
                readback = repeated
                state["public_readback"] = repeated
                save_state(state, token)
            receipt = receipt_payload(state, readback)
            legacy.atomic_write(RECEIPT_PATH, receipt, token)
            advance(state, "receipt_written", token)
            print(json.dumps({"status": "pass", "record_id": state["record_id"], "doi": state["doi"], "receipt": "qa/" + RECEIPT_PATH.name}, sort_keys=True))
            return 0
        finally:
            authenticated.close()
            anonymous.close()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (legacy.PublicationError, RdmPublicationError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
