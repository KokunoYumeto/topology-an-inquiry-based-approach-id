# Chapter 12 exercise-companion checkpoint: GitHub receipt

Status: public, partial, not an admitted complete-reader boundary.

The narrow checkpoint was pushed to the existing Indonesian mirror on 2026-08-23.
It contains the first ten source-order exercise guides for `sec_top_space_exer.ptx`,
the companion wrapper/manifest/backend update, the source correction O003-C142,
and the pinned local schema receipts. The source QA remains fail-closed `pass`.

## Public identity

- Repository: https://github.com/KokunoYumeto/topology-an-inquiry-based-approach-id
- Branch: `main`
- Content commit: `3fee7441575e3921e00fed93006df040b12711ee`
- Anonymous raw base: `https://raw.githubusercontent.com/KokunoYumeto/topology-an-inquiry-based-approach-id/3fee7441575e3921e00fed93006df040b12711ee/`
- Readback: every file listed below returned HTTP 200; downloaded byte counts and SHA-256 values matched the local files exactly.

## Readback inventory

| Path | Bytes | SHA-256 |
|---|---:|---|
| `source/sec_top_space_exer.ptx` | 24075 | `a249df5c36bbc2f4741b0da9d119cab140803b27913ca4caccac88837781e37a` |
| `companion/chapter_12_exercise_guides_a.ptx` | 19258 | `ff23ffa0a7f268007faff8dd48e0059500ac900cf5d2f14156cbc9b4f34fbfd9` |
| `companion/chapter_12_topological_spaces_self_study.ptx` | 1438 | `6e4767dbb407a3d33d722fbd704397a2184a883fd0e10ad635efe96edff37230` |
| `qa/CHAPTER12_EXERCISE_GUIDES_A_SCHEMA_QA.json` | 796 | `4e77adcaeddc074e984c428dc521d7a3c30e62e259ae067340a101ba45b598df` |
| `qa/CHAPTER12_SUMMARY_SCHEMA_QA.json` | 768 | `4bb200f57798ea9ac065812c515fc87532b5271e7e2f84f03607a94bc68ecdfa` |
| `qa/CHAPTER12_COMPANION_WRAPPER_SCHEMA_QA.json` | 1172 | `a92169ee4e48e2bcbfe1520918a65cf7ba8d971c1acfcbd3f028e198b560edaf` |
| `qa/CHAPTER12_COMPANION_PARTIAL_QA.json` | 17959 | `7342ae4412f0be8057007f4e18c951b28804510f81cb148bb6802e70746ebff1` |
| `qa/CHAPTER12_SOURCE_QA.json` | 7177 | `a6d260d2110e713db8ef69e9afe54a57e0ef7f0830f41d05279cb9967b6c6aca` |
| `qa/CHAPTER12_SOURCE_TRANSLATION_RECEIPT.md` | 2557 | `ab4ca259db4952e8a52df41dc7b6832499e48e9dfd0220b92066b67b7213e484` |
| `backend/chapter_12_companion_manifest.partial.json` | 17658 | `1c223671d19d04bd406ee3f021cb859e51b93e8cc00385c916e3dffaae91e4c7` |
| `backend/chapter_12_entry_aliases.partial.csv` | 8272 | `380eb34e629a3b74e45f7b7a9d460bfef83aa867d9a4c5dcd61562043a6f9526` |

The companion now records 41 covered atomic prompt units (37 of 78 source prompt
units remain), 164 staged statement/hint/answer/solution surfaces, and ten
exercise entries anchored to the source file. The exercise and wrapper XInclude
trees both pass the pinned PreTeXt 1.7.5 / Python 3.12.13 RelaxNG validation with
zero diagnostics. The cumulative HTML/PDF reader has not been rebuilt; this is
not a complete or admitted Chapter 12 release.

The source correction O003-C142 closes the upstream malformed finite-topology
set entry `{a,b,c,}` as `{a,b,c}`. It is recorded in the correction ledger and
the source QA receipt. No upstream contact was made.

Provenance: OpenAI Codex gpt-5.6-sol, Ultra, at the user's direction; source,
author, institutional, and human-contributor credits remain unchanged.
