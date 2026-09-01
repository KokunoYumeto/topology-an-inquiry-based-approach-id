#!/usr/bin/env python3
"""Verify the public GitHub terminology-maintenance checkpoint anonymously.

The verifier is intentionally bounded to the immutable repository files and
GitHub Pages surfaces affected by the post-completion terminology maintenance.
It never reads credentials and writes only the sanitized publication receipt.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = (
    ROOT
    / "qa"
    / "CHAPTER20_COMPLETE_TERMINOLOGY_MAINTENANCE_GITHUB_RECEIPT.md"
)
PUBLIC_REPOSITORY = (
    "https://github.com/KokunoYumeto/topology-an-inquiry-based-approach-id"
)
RAW_BASE = (
    "https://raw.githubusercontent.com/KokunoYumeto/"
    "topology-an-inquiry-based-approach-id"
)
PAGES_BASE = (
    "https://kokunoyumeto.github.io/"
    "topology-an-inquiry-based-approach-id"
)


@dataclass(frozen=True)
class Target:
    label: str
    public_path: str
    local_path: Path


@dataclass
class Check:
    label: str
    public_url: str
    local_path: str
    http_status: int | None = None
    expected_bytes: int | None = None
    actual_bytes: int | None = None
    expected_sha256: str | None = None
    actual_sha256: str | None = None
    attempts: int = 0
    result: str = "NOT RUN"
    detail: str = ""


RAW_TARGETS = (
    Target("README", "README.md", ROOT / "README.md"),
    Target(
        "complete docs manifest",
        "qa/CHAPTER20_COMPLETE_DOCS_MANIFEST.json",
        ROOT / "qa" / "CHAPTER20_COMPLETE_DOCS_MANIFEST.json",
    ),
    Target(
        "native Indonesian terminology QA receipt",
        "qa/NATIVE_INDONESIAN_TERMINOLOGY_QA_2026-08-31.md",
        ROOT / "qa" / "NATIVE_INDONESIAN_TERMINOLOGY_QA_2026-08-31.md",
    ),
)


PAGES_TARGETS = (
    Target(
        "complete reader landing route",
        "reader/complete/",
        ROOT / "docs" / "reader" / "complete" / "index.html",
    ),
    Target(
        "affected point-to-set-distance section",
        "reader/complete/sec_dist_point_set.html",
        ROOT / "docs" / "reader" / "complete" / "sec_dist_point_set.html",
    ),
    Target(
        "affected function-spaces module page",
        "reader/complete/o003-c90-completion-function-spaces.html",
        ROOT
        / "docs"
        / "reader"
        / "complete"
        / "o003-c90-completion-function-spaces.html",
    ),
    Target(
        "affected exponential-law remark knowl",
        "reader/complete/knowl/o003-c90-remark-exponential-law-scope.html",
        ROOT
        / "docs"
        / "reader"
        / "complete"
        / "knowl"
        / "o003-c90-remark-exponential-law-scope.html",
    ),
    Target(
        "affected integrated-mastery module page",
        "reader/complete/o003-c90-completion-integrated-mastery.html",
        ROOT
        / "docs"
        / "reader"
        / "complete"
        / "o003-c90-completion-integrated-mastery.html",
    ),
    Target(
        "affected integrated exercise 9 knowl",
        "reader/complete/knowl/o003-c90-completion-integrated-ex-09.html",
        ROOT
        / "docs"
        / "reader"
        / "complete"
        / "knowl"
        / "o003-c90-completion-integrated-ex-09.html",
    ),
    Target(
        "affected integrated exercise 9 hidden knowl",
        "reader/complete/knowl/o003-c90-completion-integrated-ex-09-hidden.html",
        ROOT
        / "docs"
        / "reader"
        / "complete"
        / "knowl"
        / "o003-c90-completion-integrated-ex-09-hidden.html",
    ),
    Target(
        "public complete-edition manifest",
        "reader/complete-edition-manifest.json",
        ROOT / "docs" / "reader" / "complete-edition-manifest.json",
    ),
    Target(
        "complete-edition PDF",
        "downloads/topologi-pendekatan-berbasis-inkuiri-edisi-lengkap-id.pdf",
        ROOT
        / "docs"
        / "downloads"
        / "topologi-pendekatan-berbasis-inkuiri-edisi-lengkap-id.pdf",
    ),
)


class VerificationError(RuntimeError):
    """A controlled verification failure safe to summarize in the receipt."""


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return "<outside-repository>"


def require_local_file(target: Target) -> bytes:
    if not target.local_path.is_file():
        raise VerificationError(
            f"required local file is missing: {repo_relative(target.local_path)}"
        )
    return target.local_path.read_bytes()


def public_opener() -> urllib.request.OpenerDirector:
    # No Authorization or Cookie handlers are installed. Requests are public,
    # cache-busted, and carry only a descriptive user agent.
    return urllib.request.build_opener()


def fetch_public(
    opener: urllib.request.OpenerDirector, url: str, timeout: float
) -> tuple[int, bytes]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "O003-public-readback/1.0",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
        method="GET",
    )
    with opener.open(request, timeout=timeout) as response:
        status = int(response.getcode())
        payload = response.read()
    return status, payload


def verify_main_ref(commit: str, timeout: float) -> str:
    environment = os.environ.copy()
    environment["GIT_TERMINAL_PROMPT"] = "0"
    environment["GCM_INTERACTIVE"] = "Never"
    process = subprocess.run(
        [
            "git",
            "-c",
            "credential.helper=",
            "ls-remote",
            "--heads",
            PUBLIC_REPOSITORY,
            "refs/heads/main",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=environment,
    )
    if process.returncode != 0:
        raise VerificationError(
            f"anonymous git ls-remote failed with exit code {process.returncode}"
        )
    matches: list[str] = []
    for line in process.stdout.splitlines():
        fields = line.split()
        if len(fields) == 2 and fields[1] == "refs/heads/main":
            matches.append(fields[0].lower())
    if len(matches) != 1 or not re.fullmatch(r"[0-9a-f]{40}", matches[0]):
        raise VerificationError(
            "anonymous git ls-remote did not return exactly one valid main ref"
        )
    if matches[0] != commit:
        raise VerificationError(
            f"public main ref is {matches[0]}, expected {commit}"
        )
    return matches[0]


def raw_url(commit: str, path: str) -> str:
    encoded = urllib.parse.quote(path, safe="/")
    return f"{RAW_BASE}/{commit}/{encoded}"


def pages_url(path: str, commit: str, attempt: int) -> str:
    encoded = urllib.parse.quote(path, safe="/")
    base = f"{PAGES_BASE}/{encoded}"
    query = urllib.parse.urlencode(
        {"o003_readback": f"{commit}-{attempt}"}
    )
    return f"{base}?{query}"


def evaluate_payload(check: Check, expected: bytes, status: int, actual: bytes) -> bool:
    check.http_status = status
    check.expected_bytes = len(expected)
    check.actual_bytes = len(actual)
    check.expected_sha256 = sha256(expected)
    check.actual_sha256 = sha256(actual)
    matched = (
        status == 200
        and check.actual_bytes == check.expected_bytes
        and check.actual_sha256 == check.expected_sha256
        and actual == expected
    )
    check.result = "MATCH" if matched else "MISMATCH"
    check.detail = ""
    return matched


def verify_raw_targets(
    opener: urllib.request.OpenerDirector,
    commit: str,
    timeout: float,
) -> list[Check]:
    checks: list[Check] = []
    for target in RAW_TARGETS:
        expected = require_local_file(target)
        url = raw_url(commit, target.public_path)
        check = Check(
            label=target.label,
            public_url=url,
            local_path=repo_relative(target.local_path),
            attempts=1,
        )
        try:
            status, actual = fetch_public(opener, url, timeout)
            if not evaluate_payload(check, expected, status, actual):
                checks.append(check)
                raise VerificationError(
                    f"commit-pinned raw byte mismatch: {target.public_path}"
                )
        except urllib.error.HTTPError as error:
            check.http_status = error.code
            check.result = "HTTP ERROR"
            check.detail = f"HTTP {error.code}"
            checks.append(check)
            raise VerificationError(
                f"commit-pinned raw fetch returned HTTP {error.code}: "
                f"{target.public_path}"
            ) from None
        except urllib.error.URLError as error:
            check.result = "FETCH ERROR"
            check.detail = "public fetch failed"
            checks.append(check)
            raise VerificationError(
                f"commit-pinned raw fetch failed: {target.public_path}"
            ) from error
        checks.append(check)
    return checks


def verify_pages_targets(
    opener: urllib.request.OpenerDirector,
    commit: str,
    timeout: float,
    max_attempts: int,
    poll_seconds: float,
) -> list[Check]:
    expected_payloads = {
        target.public_path: require_local_file(target) for target in PAGES_TARGETS
    }
    checks = {
        target.public_path: Check(
            label=target.label,
            public_url=f"{PAGES_BASE}/{target.public_path}",
            local_path=repo_relative(target.local_path),
        )
        for target in PAGES_TARGETS
    }
    pending = {target.public_path: target for target in PAGES_TARGETS}

    for attempt in range(1, max_attempts + 1):
        for public_path, target in tuple(pending.items()):
            expected = expected_payloads[public_path]
            check = checks[public_path]
            check.attempts = attempt
            url = pages_url(public_path, commit, attempt)
            try:
                status, actual = fetch_public(opener, url, timeout)
                if evaluate_payload(check, expected, status, actual):
                    del pending[public_path]
            except urllib.error.HTTPError as error:
                check.http_status = error.code
                check.result = "PENDING"
                check.detail = f"last response HTTP {error.code}"
            except urllib.error.URLError:
                check.result = "PENDING"
                check.detail = "last public fetch failed"

        if not pending:
            return [checks[target.public_path] for target in PAGES_TARGETS]
        if attempt < max_attempts:
            time.sleep(poll_seconds)

    unresolved = ", ".join(sorted(pending))
    raise VerificationError(
        f"GitHub Pages did not converge within {max_attempts} attempts: {unresolved}"
    )


def sanitized_failure(error: BaseException) -> str:
    message = str(error).replace(str(ROOT), "<repository>")
    message = message.replace("\r", " ").replace("\n", " ")
    message = re.sub(
        r"(?i)(authorization|access[_-]?token|token|password)=([^&\s]+)",
        r"\1=<redacted>",
        message,
    )
    return re.sub(r"\s+", " ", message).strip()[:1000]


def markdown_table(checks: Iterable[Check]) -> list[str]:
    rows = [
        "| Public resource | HTTP | Attempts | Bytes | SHA-256 | Result |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for check in checks:
        status = str(check.http_status) if check.http_status is not None else "—"
        size = (
            f"{check.actual_bytes:,}"
            if check.actual_bytes is not None
            else "—"
        )
        digest = (
            f"`{check.actual_sha256}`"
            if check.actual_sha256 is not None
            else "—"
        )
        result = check.result
        if check.detail:
            result = f"{result} ({check.detail})"
        rows.append(
            f"| [{check.label}]({check.public_url}) | {status} | "
            f"{check.attempts} | {size} | {digest} | {result} |"
        )
    return rows


def write_receipt(
    commit: str,
    main_ref: str | None,
    raw_checks: list[Check],
    pages_checks: list[Check],
    failure: str | None,
) -> None:
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    status = "FAIL" if failure else "PASS"
    lines = [
        "# Complete-edition terminology-maintenance GitHub receipt",
        "",
        f"- **Status:** {status}",
        f"- **Verified:** {timestamp}",
        f"- **Public repository:** {PUBLIC_REPOSITORY}",
        "- **Published branch:** `main`",
        f"- **Expected publication commit:** `{commit}`",
        "- **Verification mode:** anonymous public readback; no credentials used",
        "",
        "## Public branch identity",
        "",
    ]
    if main_ref is not None:
        lines.extend(
            [
                "Anonymous `git -c credential.helper= ls-remote` returned ",
                f"`{main_ref}` for `refs/heads/main`, exactly matching the ",
                "expected publication commit.",
            ]
        )
    else:
        lines.append("The public `main` ref did not pass exact verification.")

    lines.extend(["", "## Commit-pinned raw readback", ""])
    if raw_checks:
        lines.extend(markdown_table(raw_checks))
    else:
        lines.append("No raw resource completed verification.")

    lines.extend(["", "## GitHub Pages readback", ""])
    if pages_checks:
        lines.extend(markdown_table(pages_checks))
    else:
        lines.append("No Pages resource completed verification.")

    lines.extend(["", "## Conclusion", ""])
    if failure:
        lines.append(f"Verification failed: {failure}.")
    else:
        lines.append(
            "The public `main` branch, commit-pinned repository evidence, "
            "complete reader route, affected pages and knowls, public edition "
            "manifest, and complete-edition PDF all match their verified local "
            "bytes. This proves public availability and exact readback identity "
            "for the terminology-maintenance checkpoint."
        )
    lines.extend(
        [
            "",
            "No credentials were used, and this receipt contains no credential "
            "material.",
            "",
        ]
    )
    payload = "\n".join(lines).encode("utf-8")
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    temporary = RECEIPT.with_suffix(RECEIPT.suffix + ".tmp")
    temporary.write_bytes(payload)
    if temporary.read_bytes() != payload:
        raise VerificationError("temporary receipt write/readback failed")
    temporary.replace(RECEIPT)
    if RECEIPT.read_bytes() != payload:
        raise VerificationError("receipt write/readback failed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--commit",
        required=True,
        help="expected 40-character publication commit on public main",
    )
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=12,
        help="maximum GitHub Pages propagation checks per target (default: 12)",
    )
    parser.add_argument(
        "--poll-seconds",
        type=float,
        default=15.0,
        help="seconds between bounded Pages checks (default: 15)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="per-operation network timeout in seconds (default: 60)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    commit = args.commit.strip().lower()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise SystemExit("--commit must be exactly 40 hexadecimal characters")
    if args.max_attempts < 1 or args.max_attempts > 120:
        raise SystemExit("--max-attempts must be between 1 and 120")
    if args.poll_seconds < 0 or args.poll_seconds > 300:
        raise SystemExit("--poll-seconds must be between 0 and 300")
    if args.timeout <= 0 or args.timeout > 300:
        raise SystemExit("--timeout must be greater than 0 and at most 300")

    opener = public_opener()
    main_ref: str | None = None
    raw_checks: list[Check] = []
    pages_checks: list[Check] = []
    failure: str | None = None

    try:
        # Validate every local comparison source before any public request.
        for target in (*RAW_TARGETS, *PAGES_TARGETS):
            require_local_file(target)
        main_ref = verify_main_ref(commit, args.timeout)
        raw_checks = verify_raw_targets(opener, commit, args.timeout)
        pages_checks = verify_pages_targets(
            opener,
            commit,
            args.timeout,
            args.max_attempts,
            args.poll_seconds,
        )
    except (VerificationError, OSError, subprocess.SubprocessError) as error:
        failure = sanitized_failure(error)

    write_receipt(commit, main_ref, raw_checks, pages_checks, failure)
    if failure:
        print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print(
        f"PASS: wrote {repo_relative(RECEIPT)} for public commit {commit}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
