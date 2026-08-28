# Chapter 16 complete companion and backend receipt

Verified: 2026-08-28 (Europe/Berlin)

Boundary: O003/C90 Chapter 16, *Ruang Hasil Bagi*. This receipt closes the
separately licensed staged self-study component and locale-neutral backend for
the chapter. It does not claim completion of Chapters 17–20 or of the original
C90 completion modules.

## Coverage and mapping

- Frozen authority: GVSU commit
  `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`.
- Seven translated source files total 58,310 bytes; their ordered combined
  SHA-256 is
  `158afadc3f4ec7be7cae2542381975cb006617ff666bac145acdc205026d4ee6`.
- The source contains 54 physical prompt occurrences representing 52 canonical
  learner prompts, with two explicit occurrence aliases and three structural
  grouping nodes. None is double-counted.
- All 52 canonical prompts have original staged support. Eight original mastery
  checks produce 60 entries and 240 nonempty statement, hint, answer/rubric,
  and solution surfaces. Pending source guides: zero.
- The cumulative closure contains 209 local XInclude files / 2,390,442 bytes,
  3,783 unique IDs, and 254 resolving xref occurrences. Its ordered closure
  SHA-256 is
  `aa6baf8576a84ab6c1eb594538b69882c07643fe8c8bb04af9d9b609b672297a`.

## Deterministic backend and schema gates

| Output | Bytes | SHA-256 |
|---|---:|---|
| `backend/chapter_16_prompt_inventory.json` | 145,530 | `ad56dc8745c84b5bad9e9c8824bb528577a66aaa9671500a21a1d8dac2896d89` |
| `backend/chapter_16_source_prompt_map.csv` | 32,059 | `6fd49fe15b0ef75b2af2578cf590003165da35eeb566982a625de26e4eecc53d` |
| `backend/chapter_16_grouping_nodes.json` | 3,013 | `668d2c9d382aa1aec39d2aef05adac09c5da75e358194bade432ee9924993505` |
| `backend/chapter_16_entry_aliases.csv` | 15,551 | `2ff9878d599937e8d0a5f975360f6fefa48fce2eef44b10684c97139f03461d2` |
| `backend/chapter_16_occurrence_entry_aliases.csv` | 2,587 | `66d5e44c91a977c126439b4a38c7fc091a03634d37387eb9383b19979e269e36` |
| `backend/chapter_16_companion_manifest.json` | 112,526 | `4d4315150b8cfa45114e7567266ba2c4fac8cc23a8c34d82b6dd6039b7ee8ce2` |
| `qa/CHAPTER16_COMPANION_QA.json` | 7,472 | `15cda17f4853fcbf7fcc4c18f91506493c45ef9ce9f5e92c1129ab6e6cbc5e22` |

Pinned PreTeXt 1.7.5 RelaxNG validation reports zero diagnostics for the
mastery file, complete companion wrapper, and cumulative Chapters 1–16
wrapper. The cumulative wrapper is 7,594 bytes at SHA-256
`82b8278d2744e84183a5092bebe94ac340a6f7514194cb1d90eb7bb4556d974b`;
its schema receipt is 9,955 bytes at SHA-256
`13de698dbfdd7cf9752785e2c8340eef9bdbe865acdbab4bf652754678bca1c0`.

The translated GVSU source remains conservatively CC BY-NC-SA 3.0. The
independently authored companion remains a separately identified CC BY 4.0
component. Production provenance is `OpenAI Codex gpt-5.6-sol, Ultra`; source,
author, institutional, and human-contributor credits remain intact.

Verdict: the Chapter 16 companion/backend boundary is complete and passes its
deterministic validation gates.
