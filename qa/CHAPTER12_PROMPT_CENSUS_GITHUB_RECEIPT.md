# Chapter 12 prompt-census correction — GitHub receipt

Verified: 2026-08-23 (Europe/Berlin)

This checkpoint corrects the Chapter 12 learner-response denominator from 78
to 79. The omitted unit was the direct question in `act_top_basis`, which the
upstream PreTeXt encodes as an activity-body paragraph rather than as a child
`task` or `statement`. Existing guide `o003-c90-ch12-guide-11` already covers
that question. The correction changes no translated mathematics and makes the
current state 51 covered prompt units / 204 staged surfaces / 28 pending prompt
units. The five grouping task nodes are structural parents, not additional
learner-response units.

- Content commit: `0fe620e1ee8fa8e6a0ba20fc24c3cfc70c240c15`
- Repository: `https://github.com/KokunoYumeto/topology-an-inquiry-based-approach-id`
- Anonymous raw base: `https://raw.githubusercontent.com/KokunoYumeto/topology-an-inquiry-based-approach-id/0fe620e1ee8fa8e6a0ba20fc24c3cfc70c240c15/`

| Public path | Bytes | SHA-256 | HTTP / identity |
|---|---:|---|---|
| `backend/chapter_12_companion_manifest.partial.json` | 21,691 | `a1adaf21af8750d658ebeb12779118572739e76b52739b7afadc9987a56cff20` | 200 / exact |
| `qa/CHAPTER12_COMPANION_PARTIAL_QA.json` | 22,289 | `3be4a7bd35e231c257b6648a54139c225f8acb14216d85270a63662ebb0fa4cc` | 200 / exact |
| `qa/CHAPTER12_SOURCE_TRANSLATION_RECEIPT.md` | 2,887 | `a97bf64b17decd6dc1860a6a54e69971aece6ac1c39ae3d9ba6aa3bb9c65eaf7` | 200 / exact |
| `scripts/build_zenodo_chapter12_partial_package.py` | 12,631 | `6c4f965ebed7229215b5227d9dd9b1c26ec7323485d749ec09456db1ecc89159` | 200 / exact |

All four anonymous downloads matched local bytes and SHA-256. This remains a
partial, non-admitted Chapter 12 checkpoint; Chapters 1–11 remain the verified
public reader boundary.
