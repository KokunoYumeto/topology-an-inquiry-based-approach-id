# Chapter 14 GitHub and Pages publication receipt

Published and anonymously verified: 2026-08-26 (Europe/Berlin)

Scope: the admitted O003/C90 Bahasa Indonesia cumulative Chapters 1–14
checkpoint, including the Chapter 14 self-study companion, modular backend,
source and QA receipts, responsive HTML reader, and corrected 407-page PDF.
This remains a partial 14-of-20 edition.

## Public lineage

- Repository: https://github.com/KokunoYumeto/topology-an-inquiry-based-approach-id
- Reader: https://kokunoyumeto.github.io/topology-an-inquiry-based-approach-id/
- Content commit and public `main` head:
  `489f9aa1bfd19299b6f5f84f8a500ca7cca67313`

The commit advanced the existing edition repository and Pages site. No
duplicate repository or publication lineage was created.

## Anonymous readback

The remote branch head was read without credentials and matched the local
content commit. Commit-pinned raw and public Pages bytes were then downloaded
without authentication:

| Surface | Bytes | SHA-256 | Result |
|---|---:|---|---|
| commit-pinned `README.md` | 5,530 | `9712d326c1a631726826d11198017158d979544ad5c63b702382164aac61acab` | exact |
| commit-pinned `qa/CHAPTER14_SOURCE_MANIFEST.json` | 162,840 | `1f2cb10b0678509c4ec15245e8e2238bad2f6b87ef3f625ee1c78abf619d86f8` | exact |
| commit-pinned Chapters 1–14 PDF | 3,303,987 | `1a1cdbdb8714071894206859696aa734541f4b7b48d13be1b65fa00f68e0b43a` | exact |
| Pages cumulative reader HTML | 50,054 | `7cc3822c23aa7cec1de2e112ccaa6088492ef77e7fbb13578229e5fc41d86650` | exact |
| Pages Chapters 1–14 PDF | 3,303,987 | `1a1cdbdb8714071894206859696aa734541f4b7b48d13be1b65fa00f68e0b43a` | exact |

Every request returned HTTP 200. Every byte count and SHA-256 matched the
frozen local file, including the corrected PDF produced by two strict,
byte-identical builds.

## Verdict

GitHub source preservation, public branch identity, Pages reader deployment,
and anonymous byte readback pass. Publication does not imply completion of
Chapters 15–20 or of the separately licensed original C90 completion modules.
