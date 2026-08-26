# Chapter 14 complete companion and backend receipt

Verified: 2026-08-26 (Europe/Berlin)

Boundary: O003/C90 Chapter 14, *Kekontinuan dan Homeomorfisme*. This receipt
closes the separately licensed staged self-study component and locale-neutral
backend for the chapter. It does not yet admit or publish the cumulative
Chapters 1-14 HTML/PDF reader.

## Coverage and mapping

- Frozen authority: GVSU commit
  `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`.
- Canonical prompt-mapping SHA-256:
  `ee610085d17009e74afd6776ecb62838a764fb77bc419a53ee4a9e5c17960ab7`.
- Source denominator: 81 learner prompts, consisting of 77 atomic task
  carriers and four direct statement carriers. Three structural grouping
  nodes remain separately mapped and are not double-counted.
- Complete staged support: 81 source guides plus eight original mastery
  checks, yielding 89 entries and 356 nonempty statement, hint, answer or
  rubric, and solution surfaces. Pending source guides: zero.
- The cumulative closure contains 181 local XInclude files, 3,337 unique IDs,
  and 223 xref occurrences; every xref resolves and all companion IDs are
  unique.

## Authored companion identities

| Path | Bytes | SHA-256 |
|---|---:|---|
| `companion/chapter_14_source_guides_a.ptx` | 18,289 | `eefc238570215fa78232030cc5cb7026f83a02edfd54308f5de314382c40d0aa` |
| `companion/chapter_14_source_guides_b.ptx` | 18,389 | `d5593e324e3dd4a087811ffc5290f64988ab8111541ba24df1c81afaeba9722f` |
| `companion/chapter_14_source_guides_c.ptx` | 7,081 | `c4119fdba67c549309a5965805d57d193e4080405f37884131d81fcfb5ee439c` |
| `companion/chapter_14_exercise_guides_a.ptx` | 17,806 | `ac772355a15b250b6e1a1e7223b9059dfa010a766d7d44313b349a170e0a610a` |
| `companion/chapter_14_exercise_guides_b.ptx` | 16,632 | `f8cc5e435419c45af76b19d6ce8dcb9649d38e786d206305bc9e4cca20daf04f` |
| `companion/chapter_14_exercise_guides_c.ptx` | 19,394 | `91a8323a2f2766098494d49966797a70d5318d8133d1fdbe1a59f6bc4ee908fb` |
| `companion/chapter_14_exercise_guides_d.ptx` | 20,990 | `0271abe76bc8729033bf550071fe98e051e127951374671a901b4fbbf512cd89` |
| `companion/chapter_14_exercise_guides_e.ptx` | 16,299 | `69e39e85fa825066385a7575cbb2885debadc926581308bc4cb14c2582ec2fac` |
| `companion/chapter_14_exercise_guides_f.ptx` | 11,331 | `0760a47e4fef2d84f94d9e7cc16c984e2d007a7afe8e3d25d1fe12bb66b473f2` |
| `companion/chapter_14_mastery.ptx` | 21,687 | `66f49505d11f72c3311f9f987078ada794ac95c8ea3b6a3d25d2c10560b632dd` |
| `companion/chapter_14_continuity_homeomorphisms_self_study.ptx` | 1,707 | `74582f034d7101c19941c616ce950a6cd91ed0e91ed8158883419faad45f97b8` |

An independent cross-file review compared all 81 source guides against the
translated carriers and inherited grouping context. It found and corrected
eight literal tab corruptions of `\tau_X` and `\tau_Y` in guides 01-04; no
other wrong-prompt, grouping, or mathematical defect remained. A separate
review passed all eight mastery solutions after two Indonesian copy edits.

The cumulative PDF visual gate subsequently exposed physical-page clipping in
guide 02. Its two topology definitions were changed from one overlong inline
expression to two display equations. This is a mathematically equivalent
layout repair: it supersedes the prior companion file and manifest hashes in
this receipt, but does not alter the already public companion checkpoint.

## Deterministic backend and schema gates

Two immediate refresh runs, one write and one read-only check, reproduced:

| Output | Bytes | SHA-256 |
|---|---:|---|
| `backend/chapter_14_source_prompt_map.csv` | 47,375 | `377e3251cafb42f5e307cf163a0b302529250f453adf6f5962890923273b9884` |
| `backend/chapter_14_grouping_nodes.json` | 2,984 | `d3204860900770fa814007b4e4db8e859caa0a5a479bbb54a00d56cd239d7e13` |
| `backend/chapter_14_entry_aliases.csv` | 23,073 | `84996bf9180ad0dac064ebe3d12f75c97445f2565ff1f603c759cc3f97656d5e` |
| `backend/chapter_14_companion_manifest.json` | 159,465 | `3520fb2096b959236229dce4512e1ad749cad945fd54d0bea92c50afee0f0300` |
| `qa/CHAPTER14_COMPANION_QA.json` | 4,547 | `26137f716d00fb44afadbc4c2e7f181bb1cc521a3bac801f68722926ac1dee1f` |

Pinned PreTeXt 1.7.5 RelaxNG validation reports zero diagnostics for the
mastery file, complete companion wrapper, and cumulative Chapters 1-14
wrapper. The exact schema-receipt identities are:

| Receipt | Bytes | SHA-256 |
|---|---:|---|
| `qa/CHAPTER14_COMPANION_WRAPPER_SCHEMA_QA.json` | 1,339 | `c574f10d3b2a0c0360e3f13d0e4b83d26aae5ba9806e682cea49e0e6df600389` |
| `qa/CHAPTER14_MASTERY_SCHEMA_QA.json` | 776 | `9708d74673e4c1b6179656f2f3ed07c4a235cbee871e63d8b209fafe82beef8a` |
| `qa/CHAPTER14_CUMULATIVE_SCHEMA_QA.json` | 8,741 | `45303693f982c12c9196e8942eb2fd7cb221a7788e1cc5bb653fbe9012eee19a` |

The translated GVSU source remains conservatively CC BY-NC-SA 3.0. The
independently authored companion remains a separately identified CC BY 4.0
component and is not represented as source-author or institutional prose. The
recorded production model is `OpenAI Codex gpt-5.6-sol, Ultra`; all source,
author, institutional, and human-contributor credits remain intact.

Verdict: the Chapter 14 companion/backend boundary is complete and passes its
deterministic validation gates. The next gate is the cumulative Chapters 1-14
HTML/PDF build, visual QA, release packaging, publication, and anonymous
readback.
