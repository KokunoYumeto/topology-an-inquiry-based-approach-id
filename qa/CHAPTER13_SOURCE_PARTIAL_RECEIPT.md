# Chapter 13 source checkpoint — through set boundaries

Verified: 2026-08-25 (Europe/Berlin)

Status: **six of nine source files translated; working checkpoint, not an
admitted cumulative reader release**.

## Authority and scope

The controlling source is Steven Schlicker's GVSU *Topology: An Inquiry-Based
Approach* at commit `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
`7df245934eedb7174d5ff8af18afff5a7abdde78`. Chapter 13's exact nine-file
direct closure is 61,337 raw bytes and has ordered basename-plus-NUL SHA-256
`9ca7295746f9916cea625420370e0ee1f09d28c4d6c940b03f22d75251235313`.
The GVSU derivative remains conservatively CC BY-NC-SA 3.0; this checkpoint
does not yet contain or admit the separately licensed Chapter 13 companion.

The following contiguous source-order files are translated into natural id-ID:

| File | Bytes | SHA-256 |
|---|---:|---|
| `source/chap_Closed_sets_topology.ptx` | 2,149 | `9239ee236675d6f734cb9325860d866a9c9a013780664d9acf57cebb045f12a8` |
| `source/sec_closed_sets_top_intro.ptx` | 4,049 | `81a783cad1430e39fbbfed4dd601661acacbb69b833ce230de8b4d4ca5b0084b` |
| `source/sec_union_inter_closed.ptx` | 3,760 | `e9ef4c2372e590174f29c79df90d6f906128cecbe55d1c184f98fe5c3672de71` |
| `source/sec_limit_points.ptx` | 7,737 | `e66d2f03a8fc9f08b300b4beef5f34904e8c357f67508b8c4bb15f26c0450d07` |
| `source/sec_top_closure.ptx` | 4,336 | `fb0005a38e4188ef75ea200bb8ce4b56333820c40965645a9611d88b0da5b0af` |
| `source/sec_set_boundary.ptx` | 2,879 | `34bc5f2f4fe11ded3170153e584f8227c29fd8f9ff52290288eb5bdd4aec6049` |

The slice covers the chapter objectives, the complete introductory
exploration, unions/intersections, limit points and topological sequences,
closure, and set boundaries. The next source file is
`source/sec_separation_ax.ptx`, followed by the summary and exercises.

## Fail-closed QA and corrections

`qa/CHAPTER13_SOURCE_PARTIAL_QA.json` is 4,898 bytes / SHA-256
`c97fae42e9d4b3c37aaea1fa619189757680f4d65bbe3ef4fb75ec57e82ab917`;
status `pass`, zero failures. It compares 494 elements, 255 protected math
nodes, 12 XML IDs, six xrefs, 26 task nodes, and six activity/exploration
containers against exact authority topology. The two allowed external xrefs
are real cumulative targets: `ex_digital_line_topology` in admitted Chapter 12
and `ex_TS_Closed_boundary` in the still-untranslated Chapter 13 exercise file.
Both resolve in the complete pinned/local ID universe.

Three high-confidence source corrections are ledgered:

- O003-C146 repairs the finite-union proof so that it defines
  `C = \bigcup_{k=1}^n C_k` and uses the same finite family in De Morgan's
  identity and conclusion. The authority instead begins with an intersection
  and then switches to an unrelated arbitrarily indexed family.
- O003-C147 replaces the activity's metric notation `(X,d)` with `(X,\tau)`
  because the hypothesis is an arbitrary topological space.
- O003-C148 replaces the metric-specific phrase “centered at x” by the exact
  topological neighborhood relation: the open set contains `x` and lies in
  `N`.

The four protected-math differences admitted by QA are precisely the three
O003-C146 expressions and the O003-C147 structure symbol. Reader-visible text
inside mathematical `\text{...}` commands is localized without changing the
formula topology. No other math, ID, xref, attribute, or element-order change
is accepted.

Terminology entries O003-T154 through O003-T160 bind the new forms including
*himpunan tertutup dalam ruang topologi*, *ruang Hausdorff*, *aksioma
pemisahan*, *himpunan buka-tutup*, and *himpunan turunan*. The live terminology
ledger is 16,156 bytes / SHA-256
`f2896983735468e20ac4f67f89c514955abc3ecaae5b538113a99bac12894326`;
the correction ledger is 57,604 bytes / SHA-256
`a52b1c639a412f2c474dcc1dbd192b9ea345efcd4db6e4a7593a56f945b06d29`.

## Remaining work

This checkpoint is source-only and must not be represented as a Chapter 13
reader release. Translate `sec_separation_ax.ptx`,
`sec_closed_sets_top_summ.ptx`, and `sec_closed_sets_top_exer.ptx` in order;
then close all 76 source prompts with staged companion support and stable-ID
mappings. Only after cumulative schema, deterministic HTML/PDF, link, browser,
accessibility, structure, visual, packaging, publication, and anonymous
readback gates pass may Chapter 13 be admitted.
