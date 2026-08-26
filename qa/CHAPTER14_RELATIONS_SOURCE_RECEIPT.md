# Chapter 14 source checkpoint through relations

Verified: 2026-08-26 (Europe/Berlin)

Status: **five of eight source files translated; working source checkpoint,
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
topological-equivalence section, and relations section are translated
contiguously. The new file is:

| File | Bytes | SHA-256 |
|---|---:|---|
| `source/sec_relations.ptx` | 3,791 | `76c082e1ec59a289178b1b72074fc8aeae35bf07569fad972acdb52fdd378ae3` |

It covers relations, reflexivity/symmetry/transitivity, equivalence relations,
both metric/topological equivalence exercises, and the homeomorphism-class
conclusion. It preserves the exact 34 inline formulas, one section ID, two
atomic tasks, six term surfaces, two index entries, and zero xrefs.

## Fail-closed source and schema QA

`qa/CHAPTER14_SOURCE_THROUGH_RELATIONS_QA.json` is 5,110 bytes / SHA-256
`5763104b22af86f8e6ae33bb5d9e07f89f862459a54cc73b2bc835427badff82`;
status `pass`, zero failures. Across the five translated files it compares
531 elements, 295 protected math nodes, 13 XML IDs, 12 xrefs, 22 task nodes,
and five activity/exploration containers. Their framed combined translated
SHA-256 is
`faa81c43733bbbaf863e20eb4dd539610611765109eb14cdcc1f203b2aa9d4ac`.

The only protected-math changes in this cumulative slice remain the five
previously ledgered topology/notation repairs in Chapters 14's introduction
and topological-equivalence section. The relations translation preserves all
34 authority math nodes in order. All external xrefs resolve in the frozen
cumulative source. A bounded reader-visible English-residue scan found no
English prose; narrow `git diff --check` passes.

`qa/CHAPTER14_CUMULATIVE_SCHEMA_THROUGH_RELATIONS_QA.json` is 2,193 bytes /
SHA-256 `f5bb3774feba895ad74d2d91540b444592265388c47f1cc9fa7bad9161aea363`.
The in-memory cumulative Chapters 1-14 tree has 37,709 expanded elements and
validates with zero diagnostics under Python 3.12.13, PreTeXt 1.7.5, lxml
4.9.4, schema SHA-256
`fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0`,
and resource commit `9bce7e55911fb14e3e6e362bfa78bd6431c38597`.

## Terminology and deterministic repairs

Rows O003-T180 through O003-T189 bind *relation*, *related to*, *reflexive*,
*symmetric*, *transitive*, *equivalence relation*, *equivalence class*,
*disjoint union*, *equals relation*, and *homeomorphism class*. The complete
terminology ledger is 19,524 bytes / SHA-256
`041936a5ce9a2a2d939ce33921d81a29ffdeb4ec3b2973c5b6ed1364f45bb661`.

Repairs O003-C171 and O003-C172 are bounded and high-confidence: symmetry and
transitivity now explicitly quantify the relevant choices of elements while
retaining the authority math-node order, and the two learner tasks state that
the relation is considered on a selected set of metric or topological spaces.
The complete correction ledger is 68,534 bytes / SHA-256
`6f0923aa81d061924308337b89a8d875c48e36dddea759f9fad73ec605dbfc58`.

An independent review found no actionable issue after the wording refinement:
the relation clauses are explicit in Indonesian, all protected surfaces and
task topology are exact, and no assets or accessibility additions are needed.

## Remaining work

This is source-only and does not advance the admitted cumulative reader or
Zenodo edition beyond Chapters 1-13. Continue in source order with
`source/sec_top_invar.ptx`, then the summary and exercise files. After the full
source closure, close all 81 Chapter 14 learner prompts and three grouping
relations in the separately licensed staged companion/backend before the
cumulative HTML/PDF and preservation gates.
