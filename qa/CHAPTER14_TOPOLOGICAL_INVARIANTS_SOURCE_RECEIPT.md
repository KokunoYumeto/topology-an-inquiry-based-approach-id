# Chapter 14 source checkpoint through topological invariants

Verified: 2026-08-26 (Europe/Berlin)

Status: **six of eight source files translated; working source checkpoint,
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
topological-equivalence section, relations section, and topological-invariants
section are translated contiguously. The new file is:

| File | Bytes | SHA-256 |
|---|---:|---|
| `source/sec_top_invar.ptx` | 1,870 | `f17c8dcf9985e2dd80f324132bd25c3f0bdb4bc98ec90b158936ff310ea64f24` |

It covers the invariant/property definition and all five classification tasks
for indiscrete, discrete, finite-complement, membership, and cardinality
properties. No assets or interactive surfaces occur in this file.

## Fail-closed source and schema QA

`qa/CHAPTER14_SOURCE_THROUGH_TOPOLOGICAL_INVARIANTS_QA.json` is 5,681 bytes /
SHA-256 `84d723542287ac40324131bb12f2bdb0ce447f839aecd8c8fd405629d230dc26`;
status `pass`, zero failures. Across the six translated files it compares 576
elements, 308 protected math nodes, 14 XML IDs, 12 xrefs, 27 task nodes, and
six activity/exploration containers. Their framed combined translated
SHA-256 is
`3c92ca41e62058c2d3185c846590ebbb5f8763667e7408bec3bdc473c91c5d4c`.

All external xrefs resolve in the frozen cumulative source. A bounded
reader-visible English-residue scan found no English prose; narrow
`git diff --check` passes.

`qa/CHAPTER14_CUMULATIVE_SCHEMA_THROUGH_TOPOLOGICAL_INVARIANTS_QA.json` is
2,193 bytes / SHA-256
`9049643a4dda54216e24b640357c5a72d3d2e0992d8dd4c7bd67741e9a536451`.
The in-memory cumulative Chapters 1-14 tree has 37,709 expanded elements and
validates with zero diagnostics under Python 3.12.13, PreTeXt 1.7.5, lxml
4.9.4, schema SHA-256
`fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0`,
and resource commit `9bce7e55911fb14e3e6e362bfa78bd6431c38597`.

## Terminology and deterministic repair

Rows O003-T190 through O003-T194 bind *topological invariant*, *topological
property*, *indiscrete topology*, *discrete topology*, and *finite complement
topology*. The complete terminology ledger is 20,053 bytes / SHA-256
`a73465b827b19c88d712d87322eeed506f946cb4a62444504c10e6e80eb02996`.

Repair O003-C173 corrects the source activity's singular “homeomorphic space”
when it compares two named spaces; the Indonesian wording is plural and keeps
the intended classification question unchanged. The complete correction
ledger is 68,921 bytes / SHA-256
`ca0033cb3ae609a2d7a07bf9dc367a39326c714d1d029ee3f726baede2b57875`.

The translated section preserves its one ID, 13 math nodes, five atomic tasks,
two index entries, and all source topology. No accessibility or asset addition
is required.

## Remaining work

This is source-only and does not advance the admitted cumulative reader or
Zenodo edition beyond Chapters 1-13. Continue in source order with
`source/sec_cont_top_summ.ptx`, then the exercise file. After the full source
closure, close all 81 Chapter 14 learner prompts and three grouping relations
in the separately licensed staged companion/backend before the cumulative
HTML/PDF and preservation gates.
