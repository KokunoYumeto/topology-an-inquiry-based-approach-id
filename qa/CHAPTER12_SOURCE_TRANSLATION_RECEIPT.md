# Chapter 12 source-translation checkpoint

Verified: 2026-08-23 (Europe/Berlin)

This is a source/translation checkpoint, not an admitted reader boundary.
Chapters 1–11 remain the latest complete cumulative reader release. Chapter 12
(*Ruang Topologi*) is translated across its exact nine-file direct XInclude
closure; its staged companion, cumulative reader build, and publication remain
pending.

## Frozen authority

- Official source: Steven Schlicker, *Topology: An Inquiry-Based Approach*.
- Commit: `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`.
- Tree: `7df245934eedb7174d5ff8af18afff5a7abdde78`.
- Authority audit: `00_control/CHAPTER12_AUTHORITY_AUDIT.md`.
- Closure: 9 files / 59,268 bytes.
- Ordered authority SHA-256: `dde360d7ec1d62d22d5a5afdbaad2055665d57b67e2b4aac6ae43636b84fda47`.

## Translation QA

`repo/qa/CHAPTER12_SOURCE_QA.json` passes fail-closed structural comparison:
25 IDs, 14 xrefs (one explicitly approved external target,
`chap_Product_topology`), 78 learner prompt units (73 atomic plus five
grouping units), 13 exercises, 5 hints, 0 source answers, and 0 source
solutions. The nine translated files have combined SHA-256
`d42badd8918f6c4bc92f23654f8e62204886be82de5fac05bbdf9a75efde75d9`.

Two source-critical repairs are explicitly ledgered and approved by the QA
receipt: O003-C131 corrects the neighborhood ball's center from the source's
literal `X` to the introduced point `a`; O003-C132 restores the integer-set
macro `\Z` in one exercise formula. All identifiers, topology, xrefs, image
reference, and remaining mathematics are retained.

The Indonesian terms are frozen in O003-T142–O003-T153, including *basis untuk
topologi*, *topologi indiskret*, *topologi kofinit*, *termetriskan*, *topologi
garis digital*, and *topologi Zariski*. The complete staged companion and
stable-ID backend must be produced before Chapter 12 can be admitted.
