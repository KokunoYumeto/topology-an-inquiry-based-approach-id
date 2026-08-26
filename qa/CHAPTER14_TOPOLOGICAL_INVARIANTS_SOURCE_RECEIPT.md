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
| `source/sec_top_invar.ptx` | 1,875 | `8c7ed840c32b92735995b0874e53f306ebb5cec691b608fa44464e924f447e92` |

It covers the invariant/property definition and all five classification tasks
for indiscrete, discrete, finite-complement, membership, and cardinality
properties. No assets or interactive surfaces occur in this file.

## Fail-closed source and schema QA

`qa/CHAPTER14_SOURCE_THROUGH_TOPOLOGICAL_INVARIANTS_QA.json` is 5,681 bytes /
SHA-256 `f98512c23921b7c294d880ab812428f8215971fb0585073fbc0a5a9e1a895de2`;
status `pass`, zero failures. Across the six translated files it compares 576
elements, 308 protected math nodes, 14 XML IDs, 12 xrefs, 27 task nodes, and
six activity/exploration containers. Their framed combined translated
SHA-256 is
`bb4347a6328eaf0b5bafa7dde12ef6398cad199763667ca24442552dce6065d8`.

All external xrefs resolve in the frozen cumulative source. A bounded
reader-visible English-residue scan found no English prose; narrow
`git diff --check` passes.

`qa/CHAPTER14_CUMULATIVE_SCHEMA_THROUGH_TOPOLOGICAL_INVARIANTS_QA.json` is
2,193 bytes / SHA-256
`6b17634fae55016342eceb616ac2cbcdb331c88a9fd40307afd94f0ac7b2b83f`.
The in-memory cumulative Chapters 1-14 tree has 37,709 expanded elements and
validates with zero diagnostics under Python 3.12.13, PreTeXt 1.7.5, lxml
4.9.4, schema SHA-256
`fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0`,
and resource commit `9bce7e55911fb14e3e6e362bfa78bd6431c38597`.

## Terminology and deterministic repair

Rows O003-T190 through O003-T194 bind *topological invariant*, *topological
property*, *indiscrete topology*, *discrete topology*, and *finite complement
topology*. The complete terminology ledger is 20,053 bytes / SHA-256
`51fa85741a48f48bc869b5b5e9ab66933155787619ac6c32872b9a6fda70498e`.

Repairs O003-C173 and O003-C174 correct the source activity's singular
“homeomorphic space” when it compares two named spaces and normalize the
established spelling *indiskret*. The Indonesian wording is plural and keeps
the intended classification question unchanged. The complete correction
ledger is 69,298 bytes / SHA-256
`e69b79a54e916a2205bc608af98245f443bc1ff9c18c2d4b848ec80a6b0f7b06`.

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
