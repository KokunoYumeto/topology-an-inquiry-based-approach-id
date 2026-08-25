# Chapter 13 GitHub and Pages publication receipt

Published and anonymously verified: 2026-08-26 (Europe/Berlin)

Scope: the admitted O003/C90 Bahasa Indonesia cumulative Chapters 1–13
checkpoint, including the Chapter 13 self-study companion, modular backend,
source/QA receipts, responsive HTML reader, and 368-page PDF. This remains a
partial 13-of-20 edition.

## Public lineage

- Repository: https://github.com/KokunoYumeto/topology-an-inquiry-based-approach-id
- Reader: https://kokunoyumeto.github.io/topology-an-inquiry-based-approach-id/
- Content commit and public `main` head:
  `f98900a45c3521df3d8a2d3b17efdf6f8bbfce00`

The commit was pushed directly into the existing edition lineage. No duplicate
repository or Pages site was created.

## Anonymous readback

The remote branch head was read without credentials and matched the local
content commit. Commit-pinned raw and public Pages bytes were then downloaded
without authentication:

| Surface | Bytes | SHA-256 | Result |
|---|---:|---|---|
| commit-pinned `README.md` | 5,431 | `3a7b84ebbbb84d0eb7056393890a0facec68b4a3019af39bffecfb35e0fc50d4` | exact |
| commit-pinned `qa/CHAPTER13_SOURCE_MANIFEST.json` | 146,518 | `c485aaeb47a5ade57f1cd0c16ec1e65520f30795bfdf0a18f9138f5369f40ad4` | exact |
| commit-pinned Chapter 13 PDF | 3,012,937 | `746cdd14604cae66f3cb8f6de27ddf6043749dede2c22dc725da9be0ffaa31d1` | exact |
| Pages cumulative reader HTML | 46,881 | `4d17ef1cc5c6b3a3fb8b1d0d84fa5ffbae47176c2877a3ddadd94ee210fe9ddd` | exact |
| Pages Chapter 13 PDF | 3,012,937 | `746cdd14604cae66f3cb8f6de27ddf6043749dede2c22dc725da9be0ffaa31d1` | exact |

Every request returned HTTP 200 and every public byte count and SHA-256 matched
the admitted local file. The Pages reader and PDF had already completed
deployment when checked.

## Verdict

GitHub source preservation, public branch identity, Pages reader deployment,
and anonymous byte readback pass. Publication does not imply completion of
Chapters 14–20 or of the separately licensed original C90 completion modules.
