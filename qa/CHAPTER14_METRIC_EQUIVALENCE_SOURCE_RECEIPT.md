# Chapter 14 source checkpoint through metric equivalence

Verified: 2026-08-26 (Europe/Berlin)

Status: **three of eight source files translated; working source checkpoint,
not an admitted Chapter 14 reader release**.

## Authority and contiguous scope

The controlling source is Steven Schlicker's August 2023 GVSU *Topology: An
Inquiry-Based Approach* at commit
`0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
`7df245934eedb7174d5ff8af18afff5a7abdde78`. Chapter 14's complete eight-file
closure remains frozen at 44,794 raw bytes and ordered basename-plus-NUL
SHA-256 `e36457d2a351d3d77a35234c5e39b13ff2dc0163e7099ab17e95ac60294468e5`.
The derivative remains conservatively CC BY-NC-SA 3.0; no license or
attribution boundary changes at this source checkpoint.

The following contiguous source-order files are now translated into natural
id-ID:

| File | Bytes | SHA-256 |
|---|---:|---|
| `source/chap_continuity_topology.ptx` | 1,128 | `a58657e0ee50e1155c5e4bda648366db27692210e3b0973b7c1a8736992ea495` |
| `source/sec_cont_top_intro.ptx` | 9,801 | `867752285d688dbdb1048f0797be04a0e96e7a33b7a28f7cb3d99152ae173857` |
| `source/sec_metric_equiv.ptx` | 5,564 | `34db0fd00a0a3f489f13df56568166eb5297253a5e63328c8e44f50c5f54e6ea` |

The third file covers metric equivalence and isometries, distinguishes metric
from topological equivalence, and preserves the two learner tasks. It adds a
faithful Indonesian description of the `Equivalence` figure: the open
Euclidean unit disk and open maximum-metric unit square, their dashed excluded
boundaries, and the labelled coordinate extents.

## Fail-closed source and schema QA

`qa/CHAPTER14_SOURCE_THROUGH_METRIC_EQUIVALENCE_QA.json` is 3,688 bytes /
SHA-256 `b6490091aff8672a8ddee6394659f9f2eadad4b68726a31e391b4167e880524f`;
status `pass`, zero failures. Across the three translated files it compares
343 elements, 193 protected math nodes, nine XML IDs, ten xrefs, 17 task nodes,
and three activity/exploration containers. Their framed combined translated
SHA-256 is
`69a5e5ad2f70f4c0658c6e58e212d99e5ff5ed0bca744b2ae99b775edb37d4c1`.
All external-xref allowances resolve in the frozen cumulative source.

The only new structural insertion is the exact `description` child of the
figure image. The existing introduction allowances remain restricted to the
three ledgered math repairs and one intact schema-valid definition move.
A bounded reader-visible English-residue scan found no English prose; matches
were XML tag or attribute names only. Narrow `git diff --check` passes.

`qa/CHAPTER14_CUMULATIVE_SCHEMA_THROUGH_METRIC_EQUIVALENCE_QA.json` is 2,193
bytes / SHA-256
`1dd27c2dee3f2afeb9517cc584013c14502d4a7f303227c60566f80b413debc1`.
The in-memory cumulative Chapters 1-14 tree has 37,709 expanded elements and
validates with zero diagnostics under Python 3.12.13, PreTeXt 1.7.5, lxml
4.9.4, schema SHA-256
`fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0`,
and resource commit `9bce7e55911fb14e3e6e362bfa78bd6431c38597`.

## Terminology and deterministic repair

Terminology rows O003-T174 and O003-T175 bind *metrically equivalent* to
*ekuivalen secara metrik* and *isometry* to *isometri*. The complete
terminology ledger is 18,086 bytes / SHA-256
`afacea91c3c357a527af3caa625045482f0f3f8bd69bd8c0fd5b921c68d9e547`.

O003-C166 makes one narrow consistency repair: the upstream prose calls any
distance-preserving function an isometry, while the adjacent formal definition
requires a bijection. The Indonesian prose explicitly says *fungsi bijektif*,
matching that formal convention without changing the metric-equivalence
criterion. The complete source-correction ledger is 65,667 bytes / SHA-256
`85775fbfdc109ed7f21bed22e7371909f140dc2009ece0efec7cd15550a34edd`.

An independent semantic and structural review found no actionable issue:
all 54 inline formulas, two display formulas, one numbered formula, four IDs,
four xrefs, two task structures, image source, and image width in the third
file are retained exactly.

## Remaining work

This remains source-only and does not advance the public cumulative reader or
Zenodo edition beyond Chapters 1-13. Continue in source order with
`source/sec_top_equiv.ptx`, followed by relations, topological invariants,
summary, and exercises. Then close all 81 Chapter 14 learner prompts and three
grouping relations in the separately licensed staged companion/backend before
the cumulative HTML/PDF and preservation gates.
