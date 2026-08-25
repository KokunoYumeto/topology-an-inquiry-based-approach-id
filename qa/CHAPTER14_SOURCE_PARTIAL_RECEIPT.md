# Chapter 14 source checkpoint — wrapper and complete introduction

Verified: 2026-08-26 (Europe/Berlin)

Status: **two of eight source files translated; working source checkpoint, not
an admitted Chapter 14 reader release**.

## Authority and scope

The controlling source is Steven Schlicker's GVSU *Topology: An Inquiry-Based
Approach* at commit
`0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
`7df245934eedb7174d5ff8af18afff5a7abdde78`. Chapter 14's exact direct closure
is eight PreTeXt files / 44,794 raw bytes. Under the established ordered
basename-plus-NUL framing contract, its 44,965-byte framed identity is SHA-256
`e36457d2a351d3d77a35234c5e39b13ff2dc0163e7099ab17e95ac60294468e5`;
the raw concatenation is
`6bb07ba88298316262ecb593059d502f6ec76ebe74a2a2a79b62e268ba3c88f0`.
The full freeze, per-file hashes, prompt census, xref closure, asset identity,
and accessibility gap are recorded in
`../00_control/CHAPTER14_AUTHORITY_AUDIT.md`.

The GVSU derivative remains conservatively CC BY-NC-SA 3.0. This checkpoint
does not contain or license-flatten the separately identified CC BY 4.0
self-study companion.

The following contiguous source-order files are translated into natural
id-ID:

| File | Bytes | SHA-256 |
|---|---:|---|
| `source/chap_continuity_topology.ptx` | 1,128 | `a58657e0ee50e1155c5e4bda648366db27692210e3b0973b7c1a8736992ea495` |
| `source/sec_cont_top_intro.ptx` | 9,801 | `867752285d688dbdb1048f0797be04a0e96e7a33b7a28f7cb3d99152ae173857` |

The slice covers all chapter objectives, continuity between topological
spaces, the open-set characterization and its proof, finite examples, open
and closed mappings, the basis criterion activity, and the closed-set
characterization. The next source file is `source/sec_metric_equiv.ptx`.

## Fail-closed source QA

`qa/CHAPTER14_SOURCE_PARTIAL_QA.json` is 2,579 bytes / SHA-256
`357e7d04f6d98a9b30b068b0a218783921998982a217c80a48ffaef136e060e5`;
status `pass`, zero failures. It compares 242 elements, 136 protected math
nodes, five XML IDs, six xrefs, 15 task nodes, and two activity/exploration
containers against the pinned authority. The two translated files have the
framed combined SHA-256
`71522ce1d584a057b7d828de697bb6d3301d3c515526528beb05db8a8a42341d`.

The three xref allowances are scoped external only to this two-file slice and
resolve in the cumulative source: `thm_Open_continuity` and
`thm_closed_sets_continuity_MS` are in admitted metric-space chapters, while
`ex_closed_sets_continuity_TS` is in Chapter 14's frozen exercise file. A
bounded reader-visible prose scan found no unintended active English; the
single-letter matches were mathematical variables only.

## Schema and source repairs

PreTeXt validates a chapter in book context rather than through the standalone
chapter start pattern. The bounded checker
`scripts/validate_chapter14_partial_schema.py` inserts the Chapter 14 include
in memory immediately after Chapter 13 in the admitted cumulative wrapper,
expands local XIncludes, and writes a fail-closed receipt without creating a
misleading partial reader. The 2,193-byte
`qa/CHAPTER14_CUMULATIVE_SCHEMA_PARTIAL_QA.json` has SHA-256
`eca808850ec8b41707eb4f1bab5111725032d30e4bc8f7cdf1701402af087a21`;
37,708 expanded elements validate with zero diagnostics under Python 3.12.13,
PreTeXt 1.7.5, lxml 4.9.4, schema SHA-256
`fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0`,
and resource commit `9bce7e55911fb14e3e6e362bfa78bd6431c38597`.

Four deterministic repairs are ledgered as O003-C162 through O003-C165:

- the malformed `f^{-1}O)` is restored as `f^{-1}(O)`;
- topological spaces mislabeled by `d_X,d_Y` use `\tau_X,\tau_Y`;
- `topologicval` is rendered as the intended *topological*; and
- the intact formal open-map definition is moved from a schema-invalid task
  statement to section level immediately after the same exploration.

QA admits exactly the three protected-math changes above and the one 17-node
definition-subtree move; every other element, attribute, ID, xref, formula,
and prompt surface must match authority. Terminology rows O003-T167 through
O003-T173 bind *homeomorfisme*, *homeomorfik*, *ekuivalensi metrik*,
*ekuivalensi topologis*, *invarian topologis*, *pemetaan terbuka*, and
*pemetaan tertutup*.

## Remaining work

This is source-only. Continue with `sec_metric_equiv.ptx`, add the faithful
Indonesian description for the `Equivalence` figure, then translate the
remaining five files in source order. After that, close all 81 learner prompts
and three grouping relations in the staged companion/backend. Chapter 14 may
join the cumulative HTML/PDF and preservation lineages only after the complete
source, companion, schema, deterministic build, link, responsive,
accessibility, structure, visual, package, publication, and anonymous-readback
gates pass.
