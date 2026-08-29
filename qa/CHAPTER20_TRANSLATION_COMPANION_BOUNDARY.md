# Chapter 20 translation and self-study boundary

Frozen: 2026-08-29  
Lane: O003/C90, id-ID  
Unit: Chapter 20, `chap_Product_topology` — *Hasil Kali Ruang Topologi*

## Source boundary

- Complete contiguous translated closure: 9 PreTeXt files, in the exact chapter include order.
- Frozen upstream commit: `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`.
- Upstream ordered source SHA-256: `1aad6a87b24c6e303382528915cd94bf3139f652a8035e5590b7037b5a97cff1`.
- Translated ordered source SHA-256: `e259eade8f3421308feaf5ca026698a3285c79fdf22c014d738b59baefe01375`.
- Pinned RelaxNG validation: pass, zero diagnostics, 1,207 expanded elements.
- Protected topology gates: all per-file XML-ID sequences match; all xref target sets match; all image-source sequences match.
- Active English-residue gate: pass. Bibliographic titles remain in their original language by design.
- Deterministic source repairs: exactly `O003-C300` through `O003-C325`, all verified in `../00_control/SOURCE_CORRECTIONS.csv`.
- Controlling receipt: `qa/CHAPTER20_SOURCE_IDENTITY_QA.json`, 12,758 bytes, SHA-256 `55f08945b995919f94ca27d767d794552f8f1bf2b48a2199240e71c302935001`.

## Prompt and companion boundary

- Canonical source prompts: 56 physical/canonical entries, consisting of 31 nonexercise prompts and 25 exercise prompts; one nested task is retained as a backend grouping node rather than double-counted as a prompt.
- Prompt inventory: `backend/chapter_20_prompt_inventory.json`, 75,838 bytes, SHA-256 `19f85a7ef1928b451d6026f26475dd19e46d1890777789e19d053216b4e8de10`.
- Source prompt map: `backend/chapter_20_source_prompt_map.csv`, 32,705 bytes, SHA-256 `93dc29de003af8f694a30500cb7468c61ea3c4638a54cd51599ca096dd80d7bc`.
- Original self-study support: 56/56 source prompts covered, each with statement, staged hint, direct answer, complete solution, and an explicit assessment criterion; no pending source prompt.
- Original mastery layer: 8 additional fully solved checks.
- Total staged surfaces: 256 (224 source-support surfaces plus 32 mastery surfaces).
- Companion ordered SHA-256: `6679adcc5e5d1e4da8513efbf7097264620d7193da69049edafa652d4cfc6f58`.
- Standalone companion reader: `source/chapter_20_companion_reader.ptx`, 1,652 bytes, SHA-256 `50bfbc0f9321b579321274474f0e79231ced1eacf20b3fbadfa5a50b49f71fff`.
- Companion schema receipt: `qa/CHAPTER20_COMPANION_SCHEMA_QA.json`, 1,359 bytes, SHA-256 `85d4892033730aed0697205463f8895c6e42581dbf2966d2aceabf8603ffe121`.
- Companion content receipt: `qa/CHAPTER20_COMPANION_QA.json`, 32,674 bytes, SHA-256 `38041bbcb64c85cde172fdc4fd20e5e967c1e5b69a1e608a594ce2e5c79fc16d`.
- Companion manifest: `backend/chapter_20_companion_manifest.json`, 34,197 bytes, SHA-256 `3c709e94e7b500fcc57c523f34ded14f91330d0d424543d550b231f1e60b62a2`.
- Rights remain separate: the GVSU derivative is treated conservatively as CC BY-NC-SA 3.0; the original companion is CC BY 4.0. Non-endorsement and model provenance (`OpenAI Codex gpt-5.6-sol, Ultra`) appear in the reader.

## Determinism and next action

Both commands pass without changing bytes:

```text
python scripts/refresh_chapter20_source_state.py --check
python scripts/refresh_chapter20_companion_state.py --check
```

This lane did not edit Chapters 1–19, the original completion modules, `project.ptx`, the cumulative reader, the global cursor, Git, or public lineages. The next owner action is to include this complete Chapter 20 source and companion closure in the cumulative Chapter 1–20 reader/backend, run the cumulative deterministic HTML/PDF and visual/accessibility gates, then publish through the existing lineages.
