# Chapter 15 complete companion and backend receipt

Verified: 2026-08-26 (Europe/Berlin)

Boundary: O003/C90 Chapter 15, *Subruang*. This receipt closes the separately
licensed staged self-study component and locale-neutral backend for the
chapter. The Chapter 15 source is already complete; the cumulative Chapters
1–15 reader is admitted and is undergoing deterministic HTML/PDF build QA.

## Coverage and mapping

- Frozen authority: GVSU commit
  `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`.
- Canonical prompt-mapping SHA-256:
  `ea0abf0e374171141a1ad8907f1ca53a524c0ba47a4c99aca0d174bc9740b084`.
- Source denominator: 30 learner prompts: 25 atomic task carriers and five
  direct statement carriers. Two structural grouping nodes remain separately
  mapped and are not double-counted.
- Complete staged support: 30 source guides plus eight original mastery checks,
  yielding 38 entries and 152 nonempty statement, hint, answer or rubric, and
  solution surfaces. Pending source guides: zero.
- The cumulative closure contains 194 local XInclude files / 2,191,387 bytes,
  3,514 unique IDs, and 227 xref occurrences. Every xref resolves and every
  companion ID is unique. Its ordered closure SHA-256 is
  `3ccfe7246e7d0098940f05ef53c248f3bf7a3d0a64b3fbd39dac015f4a2f960d`.

## Authored companion identities

| Path | Bytes | SHA-256 |
|---|---:|---|
| `companion/chapter_15_source_guides_a.ptx` | 19,752 | `87b0197b76fa705f054bd2151a8c27d4406ed1e7c65b69988b0080e101c17496` |
| `companion/chapter_15_source_guides_b.ptx` | 12,258 | `191164f83b051484de211c3b3287c494e6294144b4cbafe5ca320d7db0c0dd4e` |
| `companion/chapter_15_exercise_guides_a.ptx` | 20,492 | `d5472bd169474512ce9001fef404ea738fc8802214e78c1854c60dd0aadfcc66` |
| `companion/chapter_15_exercise_guides_b.ptx` | 7,880 | `bb11647af285875c092181b8f78a43f50ea953de4969deecf6d04cd06076c00f` |
| `companion/chapter_15_mastery.ptx` | 22,279 | `448765c46be6901a032204c76862266844421d9759e1cf87337a7a7b198b3173` |
| `companion/chapter_15_subspaces_self_study.ptx` | 1,771 | `ef357c785c9802f955024c716b1dbb8f30d0e2321737dbfd4decd1eb1714e2f8` |

Two independent mathematical reviews checked the 30 guides against their
translated source carriers and inherited grouping context. All 16 nonexercise
guides passed without defect. The exercise/mastery review found and corrected
two malformed ambient-closure notations, completed the arbitrary-neighborhood
argument in mastery 04, normalized the established Indonesian topology terms,
introduced *buka-tutup (klopen)* on first use, corrected one separation-axiom
title, and made three small clarity edits. A second schema/backend run after
those corrections passed. No wrong-prompt binding, unresolved cross-reference,
or remaining mathematical overclaim was found.

The single active Chapter 15 source figure was visually inspected. Its
Indonesian description accurately records the ambient rectangle, the shaded
subspace, and the dashed ambient-open disk whose intersection represents the
relative open set. No replacement image or semantic change was needed.

## Deterministic backend and schema gates

The prompt inventory now recognizes both its deterministic bootstrap phase and
the covered companion phase. A write refresh followed by read-only checks
reproduced the covered map, derived reader admission from the live cumulative
include order, and bound all three schema receipts:

| Output | Bytes | SHA-256 |
|---|---:|---|
| `backend/chapter_15_prompt_inventory.json` | 39,979 | `f9f83fc944a31e694f183c23ef85603c8bc62abcc4202d7232ccdb85365bc3b6` |
| `backend/chapter_15_source_prompt_map.csv` | 17,335 | `ad8eccbb1ceb14f948886203563d7a1a360dc474fff21a0273928b55691138b5` |
| `backend/chapter_15_grouping_nodes.json` | 2,281 | `bbd38e4c39f02ee44e48ab33068ccf6c697d350767f3458211dc3a56706c4488` |
| `backend/chapter_15_entry_aliases.csv` | 9,584 | `0912786d7899f9222bd1c4f2018e9b27d64815e51e6ebd9eee291d0d6916d2f0` |
| `backend/chapter_15_companion_manifest.json` | 68,566 | `d3acc8a08bee53cfa63f49b782c8e33f80dff54b43bf40c50b8064fb438bd784` |
| `qa/CHAPTER15_COMPANION_QA.json` | 5,459 | `4b743b8e63a7c023e0297ef586da22c39a70f8658b008dc4c5eaa0c8cb072590` |

Pinned PreTeXt 1.7.5 RelaxNG validation reports zero diagnostics for the
mastery file, complete companion wrapper, and cumulative Chapters 1–15
wrapper. The exact schema-receipt identities are:

| Receipt | Bytes | SHA-256 |
|---|---:|---|
| `qa/CHAPTER15_MASTERY_SCHEMA_QA.json` | 776 | `c291113c0f37a35acdc8a60fc582bb4ea0a882cc1761d2f0ef4f62bfbdd755ac` |
| `qa/CHAPTER15_COMPANION_WRAPPER_SCHEMA_QA.json` | 1,048 | `797c47f8463fd7dd7f672f5c9e99e3e23323d3ad8cfe607602421ae581203844` |
| `qa/CHAPTER15_CUMULATIVE_SCHEMA_QA.json` | 9,277 | `3f640b45b1267feeab9a19abe2a3c8a9ad0a2eabfc31bd49ceb983d989364973` |

The translated GVSU source remains conservatively CC BY-NC-SA 3.0. The
independently authored companion remains a separately identified CC BY 4.0
component and is not represented as source-author or institutional prose. The
recorded production model is `OpenAI Codex gpt-5.6-sol, Ultra`; all source,
author, institutional, and human-contributor credits remain intact.

Verdict: the Chapter 15 companion/backend boundary is complete and passes its
deterministic validation gates. The next gate is the cumulative Chapters 1–15
HTML/PDF identity, visual, packaging, publication, and anonymous-readback
closure.
