# Chapter 14 source checkpoint through topological equivalence

Verified: 2026-08-26 (Europe/Berlin)

Status: **four of eight source files translated; working source checkpoint,
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

The chapter wrapper, complete introduction, metric-equivalence section, and
topological-equivalence section are translated contiguously. The new file is:

| File | Bytes | SHA-256 |
|---|---:|---|
| `source/sec_top_equiv.ptx` | 5,634 | `923c9f8001a0002bee6bccb9dfcff9d04e0a3049f3a23a7acf1743d7ef4b3d9f` |

It covers topological equivalence, homeomorphisms, homeomorphic spaces, the
two-sided metric-bound sufficient condition, its proof via the identity map,
and all three learner tasks.

## Fail-closed source and schema QA

`qa/CHAPTER14_SOURCE_THROUGH_TOPOLOGICAL_EQUIVALENCE_QA.json` is 4,539 bytes /
SHA-256 `93074988aafb9e342abd0711a066220f1c339a79ffb632fb55c0a32560775d27`;
status `pass`, zero failures. Across the four translated files it compares 455
elements, 261 protected math nodes, 12 XML IDs, 12 xrefs, 20 task nodes, and
four activity/exploration containers. Their framed combined translated
SHA-256 is
`931c6e39e8420f20cb085490f4c4708056f7c371c8eb5b4a08756d4b1d03eaf9`.

The only new protected-math changes are the two exact O003-C167 topology-symbol
repairs. All prior Chapter 14 allowances remain separately scoped: three math
repairs and one intact definition move in the introduction, plus the additive
figure description in metric equivalence. All external xrefs resolve in the
frozen cumulative source. A bounded reader-visible English-residue scan found
only XML tag or attribute names; narrow `git diff --check` passes.

`qa/CHAPTER14_CUMULATIVE_SCHEMA_THROUGH_TOPOLOGICAL_EQUIVALENCE_QA.json` is
2,193 bytes / SHA-256
`8630b521788019a835941a4f2b268f77eb3176c4a498977fbb1098e13d83d898`.
The in-memory cumulative Chapters 1-14 tree has 37,709 expanded elements and
validates with zero diagnostics under Python 3.12.13, PreTeXt 1.7.5, lxml
4.9.4, schema SHA-256
`fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0`,
and resource commit `9bce7e55911fb14e3e6e362bfa78bd6431c38597`.

## Terminology and deterministic repairs

Rows O003-T176 through O003-T179 bind *topologically equivalent*, *identity
mapping*, *underlying set*, and informal *deformation*. The complete
terminology ledger is 18,556 bytes / SHA-256
`8bb69d5b2465f210e72efd630017ad74db2d9d991b9ccbd8f433cea55258865f`.

Repairs O003-C167 through O003-C170 are bounded and high-confidence:

- arbitrary topological spaces use `\tau_X,\tau_Y`, not metric symbols;
- the two named spaces are joined grammatically by *dan*;
- homeomorphism is not said to imply differentiable smoothness or a global
  bi-Lipschitz bound; two-sided distance bounds are presented as the stronger
  sufficient condition proved immediately afterward; and
- the final activity is rendered as an actual question.

The complete correction ledger is 67,526 bytes / SHA-256
`ccb2f8f48a8f53a4b138c759b6b5c159a170c150f6d1dc09a56a19b5c78a4bb4`.
An independent review found no actionable issue: all tag topology, 70 math
elements (including nested rows), three IDs, two xrefs, three atomic learner
tasks, six statements, and every attribute are retained; only the two ledgered
math carriers differ.

## Remaining work

This is source-only and does not advance the admitted cumulative reader or
Zenodo edition beyond Chapters 1-13. Continue in source order with
`source/sec_relations.ptx`, followed by topological invariants, summary, and
exercises. Then close all 81 Chapter 14 learner prompts and three grouping
relations in the separately licensed staged companion/backend before the
cumulative HTML/PDF and preservation gates.
