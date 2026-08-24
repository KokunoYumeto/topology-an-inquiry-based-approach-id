# Chapter 12 companion and backend closure

Verified: 2026-08-23 (Europe/Berlin)

Status: **complete authored companion; cumulative reader admission pending**.
This receipt proves the complete Chapter 12 self-study component and its
machine-readable mappings. It does not claim that the cumulative HTML/PDF
reader has passed its build and visual gates.

## Authority, source, and terminology

- Frozen GVSU commit: `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`;
  tree: `7df245934eedb7174d5ff8af18afff5a7abdde78`.
- Authority closure: 9 files / 59,268 bytes; ordered SHA-256
  `dde360d7ec1d62d22d5a5afdbaad2055665d57b67e2b4aac6ae43636b84fda47`.
- Translated nine-file closure combined SHA-256:
  `a8d8a40bced406d284d94a6b9549f6b143453fafae4d862a890959b7b980cfdb`.
- `qa/CHAPTER12_SOURCE_QA.json`: 8,016 bytes; SHA-256
  `6839eb6a1dd73aac8c288c3dd8da4abafbba8f8b051847c49fa59895be6f4cdc`;
  schema version 4, status `pass`, zero failures. It proves seven approved
  source-critical math repairs, one same-file intact subtree move, one
  cross-file intact subtree move, 25 IDs, 14 resolving xrefs, and the single
  intentionally external Chapter 13 target.
- The cumulative Chapters 1--12 wrapper resolves that forward target to an
  explicit Indonesian next-boundary placeholder; no broken reader xref is
  accepted and no untranslated Chapter 13 prose is imported.
- The bounded official-arXiv search found no suitable Indonesian-language
  point-set-topology TeX package. Direct re-inspection of the Universitas
  Terbuka and Badrulfalah--Joebaedi--Irianingsih primary PDF witnesses supports
  the frozen house terminology, so no glossary propagation change was
  justified. Evidence is `00_control/CHAPTER12_TERMINOLOGY_AUDIT.md`.
- Exact production-model provenance is `OpenAI Codex gpt-5.6-sol, Ultra`; it
  does not displace Steven Schlicker, GVSU, source, institution, or human
  credits and does not imply endorsement.

## Complete staged support

- Source denominator: 79 independent prompts: 73 atomic tasks, one direct
  activity-body prompt, and five direct statement prompts.
- All 79 have a statement, staged hint, answer, and complete solution or
  assessment rubric: 316 source-support surfaces and zero pending prompts.
- Five upstream grouping tasks are preserved as explicit parent-child backend
  nodes and are not counted again as learner responses; all child IDs resolve.
- Eight original synthesis/mastery exercises each contain exactly one
  statement, hint, answer, and complete solution: 32 further surfaces.
- `companion/chapter_12_mastery.ptx`: 26,202 bytes; SHA-256
  `caf3460a07977682cf6a5ed6959fff7b1e892a0ce930f39b658c1467d0a9a9d5`;
  8 exercises and 33/33 unique IDs. Independent review found all eight
  mathematically and linguistically sound, including the basis-refinement and
  truncated-metric proofs and the infinite, empty, and singleton edge cases.
- `companion/chapter_12_topological_spaces_self_study.ptx`: 2,057 bytes;
  SHA-256 `4d57e83f5de28377a32ffd3f1766f97f9f37e3add2e8e748598d48d688db24dc`.
  Its exact 15-file XInclude closure expands to 3,689 elements and passes the
  pinned PreTeXt 1.7.5 RelaxNG schema with zero diagnostics.
- Mastery schema receipt: `qa/CHAPTER12_MASTERY_SCHEMA_QA.json`, 776 bytes,
  SHA-256 `3db4fff067e33774dc8690386744423c8620866813a65170d67b1ec00c3d7d0a`.
- Wrapper schema receipt: `qa/CHAPTER12_COMPANION_WRAPPER_SCHEMA_QA.json`,
  1,527 bytes, SHA-256
  `410ca4ae50080a15f2a8f2a1e39492ab8f816c865bd33aa456f08c4222ccedc3`.
- The strict XeLaTeX admission gate subsequently exposed two source-native
  typesetting defects that HTML/schema checks did not: a missing literal-set
  opener in guide 21 and math commands placed inside `\text{...}` in two
  mastery case distinctions. The repaired expressions preserve the reviewed
  mathematical claims; the individual, wrapper, and cumulative schema
  receipts were rerun before the backend was regenerated. The all-page pixel
  gate then required the eight-set neighborhood answer to be reflowed as a
  two-line aligned display so it no longer reached the page edge.

## Final stable-ID backend

The final backend is explicitly non-partial and remains a separate CC BY 4.0
component alongside the conservatively CC BY-NC-SA 3.0 GVSU derivative.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `backend/chapter_12_source_prompt_map.csv` | 47,950 | `0deb6ece6d5bf8a6152b934843ab65252fc082f7de5419f1acb6df090307a4c5` |
| `backend/chapter_12_grouping_nodes.json` | 4,940 | `37801610bced290913f8e7e93004b5f4c1d5ecbdda2bb230ee5c60de9059e39e` |
| `backend/chapter_12_companion_manifest.json` | 116,133 | `c80c517b69e87b79e02f799980bc5a48fdef76b1b9b27f9fe6bddf1ee843b21e` |
| `qa/CHAPTER12_COMPANION_QA.json` | 115,942 | `ae9ce8ce60539d2a907a51d86394f9ee394ca38f64285faae02c37f4f5115740` |
| `backend/chapter_12_entry_aliases.csv` | 23,206 | `4a8e979717fcc9db27d408980db5e9ec7d222b28aa0823a5cf8483b1095c5c10` |

The final mapping contains 79 source entries plus eight explicitly original
mastery entries, sequences 1--87, 87 aliases, and 348 staged surfaces. Its
canonical prompt-mapping SHA-256 is
`ac30b9909de52371d5f0b44987246fd718bd90a100c3681f5b4db72290e95836`.
Every source entry and all five grouping nodes carry a structured locator that
re-resolves against the pinned authority by exact file, carrier-start line,
element tag, nearest real `xml:id`, XPath, and canonical-subtree SHA-256. The
unique `source_anchor` values are explicitly classified as synthetic
locale-neutral aliases, not falsely represented as upstream IDs. Original
mastery entries carry no upstream anchor or locator. Six mutation tests prove
that locator path/file/line/subtree, license, and model drift fail closed.
Three consecutive deterministic refreshes reproduced every live identity. The
script also proves that the historical `.partial` manifest, QA, and alias
artifacts are never write targets and preserved their exact prior hashes.

## Remaining admission work

The cumulative Chapters 1--12 reader must still pass deterministic HTML and
strict PDF builds, complete local-link and ID/xref closure, responsive and
staged-disclosure browser checks, accessibility and rights/provenance checks,
PDF structure, all-page raster inspection, package validation, publication,
and anonymous byte/hash readback. Chapter 11 therefore remains the latest
admitted public reader until those deterministic gates close.
