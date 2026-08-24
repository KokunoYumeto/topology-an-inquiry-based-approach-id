# Chapter 12 source-translation checkpoint

Verified: 2026-08-23 (Europe/Berlin)

This is a source/translation checkpoint, not an admitted reader boundary.
Chapters 1–11 remain the latest complete cumulative reader release. Chapter 12
(*Ruang Topologi*) is translated across its exact nine-file direct XInclude
closure. All staged source-prompt support and eight original mastery checks
are now authored; the final backend freeze, cumulative reader build, and
publication remain pending.

## Frozen authority

- Official source: Steven Schlicker, *Topology: An Inquiry-Based Approach*.
- Commit: `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`.
- Tree: `7df245934eedb7174d5ff8af18afff5a7abdde78`.
- Authority audit: `00_control/CHAPTER12_AUTHORITY_AUDIT.md`.
- Closure: 9 files / 59,268 bytes.
- Ordered authority SHA-256: `dde360d7ec1d62d22d5a5afdbaad2055665d57b67e2b4aac6ae43636b84fda47`.

## Translation QA

`repo/qa/CHAPTER12_SOURCE_QA.json` (SHA-256
`6839eb6a1dd73aac8c288c3dd8da4abafbba8f8b051847c49fa59895be6f4cdc`) passes
fail-closed structural comparison:
25 IDs, 14 xrefs (one explicitly approved external target,
`chap_Product_topology`), 79 learner-response units (73 atomic task prompts,
six direct prompts, and five non-response grouping task nodes), 13 exercises,
5 hints, 0 source answers, and 0 source
solutions. The nine translated files have combined SHA-256
`a8d8a40bced406d284d94a6b9549f6b143453fafae4d862a890959b7b980cfdb`.

Twelve source-critical repairs are explicitly ledgered and approved by the QA
receipt: O003-C131 corrects the neighborhood ball's center from the source's
literal `X` to the introduced point `a`; O003-C132 restores the integer-set
macro `\Z` in one exercise formula; O003-C136 restores the closing set brace
in the finite topology displayed in `sec_base_top.ptx`; O003-C137 removes
circular scope wording in the basis theorem proof; O003-C138 makes the
discrete-topology basis task's intended topology explicit; and O003-C139 and
O003-C140 replace the source's metric symbol `d` with the topology symbol
`\tau` where the theorem and follow-up activity explicitly assume an arbitrary
topological space; O003-C141 normalizes the repeated Zariski spelling in the
exercise text; O003-C142 closes the malformed finite-topology set entry
`{a,b,c,}` as `{a,b,c}`; and O003-C143 reconciles the exercise's claim of
nine topologies with its ten displayed items by naming item 1 as the
indiscrete starting topology and items 2--10 as the nine targets. O003-C144
moves the intact `lem_Basis` subtree out of a schema-invalid task container,
and O003-C145 moves the intact `def_weaker_topologies` subtree from a
schema-invalid exercise introduction to the immediately preceding summary.
The QA tool proves both moves fail-closed, including element/attribute
topology, IDs, protected mathematics, and protected code. All identifiers,
xrefs, image references, and remaining mathematics are retained. The
cumulative Chapters 1--12 wrapper passes the pinned PreTeXt 1.7.5 RelaxNG
schema with zero diagnostics.

The Indonesian terms are frozen in O003-T142–O003-T153, including *basis untuk
topologi*, *topologi indiskret*, *topologi kofinit*, *termetriskan*, *topologi
garis digital*, and *topologi Zariski*. The staged companion is authored; its
final stable-ID/backend freeze and cumulative reader gates remain before
Chapter 12 can be admitted.

The denominator supersedes the earlier 78-unit census: the upstream
`act_top_basis` question is encoded directly in an activity body paragraph,
not in a child `task` or `statement`, but it is still an independent learner
prompt and has guide `o003-c90-ch12-guide-11`. All 79 prompts now have staged
statement, hint, answer, and complete solution/rubric support; the eight
mastery checks likewise have complete staged support. Those companion
surfaces remain a separate CC BY 4.0 component and are not represented as
upstream GVSU prose.
