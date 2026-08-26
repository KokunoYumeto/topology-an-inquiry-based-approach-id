# Chapter 14 source checkpoint through summary

Verified: 2026-08-26 (Europe/Berlin)

Status: **seven of eight source files translated; working source checkpoint,
not an admitted Chapter 14 reader release**.

## Authority and contiguous scope

The controlling source is Steven Schlicker's August 2023 GVSU *Topology: An
Inquiry-Based Approach* at commit
`0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
`7df245934eedb7174d5ff8af18afff5a7abdde78`. Chapter 14's complete eight-file
closure remains frozen at 44,794 raw bytes and ordered basename-plus-NUL
SHA-256 `e36457d2a351d3d77a35234c5e39b13ff2dc0163e7099ab17e95ac60294468e5`.
The derivative remains conservatively CC BY-NC-SA 3.0; no rights or attribution
boundary changes at this source checkpoint.

The chapter wrapper, complete introduction, metric-equivalence section,
topological-equivalence section, relations section, topological-invariants
section, and summary are translated contiguously. The new file is:

| File | Authority bytes / SHA-256 | Translated bytes / SHA-256 |
|---|---:|---:|
| `source/sec_cont_top_summ.ptx` | 2,064 / `c2b097654aa77dbbcfa4925c220d97b935a515e7faf3cff255d0f372bb316b72` | 2,140 / `8e01cce0f31344b84c7504b540a9c5fe3879b4c3213704aa48975529743fc95a` |

It preserves the four summary statements and all 41 protected math nodes; no
assets, activities, exercises, or interactive surfaces occur in this file.

## Fail-closed source and schema QA

`qa/CHAPTER14_SOURCE_THROUGH_SUMMARY_QA.json` is 6,264 bytes /
SHA-256 `9c6880ee4c1d39bdc78cbfc7bc878c54d7fe3406c209ac4c1d458d376eb2d732`;
status `pass`, zero failures. Across the seven translated files it compares
630 elements, 349 protected math nodes, 15 XML IDs, 12 xrefs, 27 task nodes,
and six activity/exploration containers. Their framed combined translated
SHA-256 is
`735a9e850fae378cf46b314d46538d102705678e932cfb54c45be83308bc66c0`.

All external xrefs resolve in the frozen cumulative source. A bounded
reader-visible English-residue scan found no English prose; narrow
`git diff --check` passes.

`qa/CHAPTER14_CUMULATIVE_SCHEMA_THROUGH_SUMMARY_QA.json` is 2,193 bytes /
SHA-256 `aae28625cb21fc4b2a2c3ef06dbbb48dca2b00d6f5709a0ee6069eecc5150cf8`.
The in-memory cumulative Chapters 1-14 tree has 37,709 expanded elements and
validates with zero diagnostics under Python 3.12.13, PreTeXt 1.7.5, lxml
4.9.4, schema SHA-256
`fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0`, and
resource commit `9bce7e55911fb14e3e6e362bfa78bd6431c38597`.

## Terminology and deterministic repair

Existing approved terminology rows through O003-T194 remain in force; no new
term was needed. Repairs O003-C175 through O003-C177 correct three unambiguous
English grammar slips in the summary (the article before *isometry*, the
preposition in “homeomorphism between X to Y,” and the missing article before
“topological space X”). The mathematical content and every protected math node
are unchanged. The complete terminology ledger is 20,054 bytes / SHA-256
`51fa85741a48f48bc869b5b5e9ab66933155787619ac6c32872b9a6fda70498e`; the
complete correction ledger is 70,370 bytes / SHA-256
`208d2a1474910e10be76717824042c4d14fb68cb54f774765959b80eacfe4769`.

## Remaining work

This is source-only and does not advance the admitted cumulative reader or
Zenodo edition beyond Chapters 1-13. Continue in source order with the final
exercise file `source/sec_cont_top_exer.ptx`. After the full source closure,
close all 81 Chapter 14 learner prompts and three grouping relations in the
separately licensed staged companion/backend before the cumulative HTML/PDF
and preservation gates.
