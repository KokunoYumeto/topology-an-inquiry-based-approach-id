# Chapters 1-17 cumulative build and QA receipt

Verified: 2026-08-29 (Europe/Berlin)

Boundary: O003/C90 Bahasa Indonesia through the complete GVSU Chapter 17,
*Ruang Kompak*, plus its separately licensed original self-study companion.
This is a coherent 17-of-20 checkpoint, not a complete-edition claim.

## Source, companion, and schema

Authority remains Steven Schlicker's GVSU *Topology: An Inquiry-Based
Approach* at commit `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
`7df245934eedb7174d5ff8af18afff5a7abdde78`. The official 2,200,204-byte
archive has SHA-256
`d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3`.

Chapter 17's eight translated source files total 69,034 bytes at ordered
combined SHA-256
`e4e9955460ce4af294b6ea0b0e00d9c9766c9d95e460aa1c16b56cf0ddd0bbb1`.
Bounded source QA verifies 1,365 elements, 801 protected mathematics nodes,
29 IDs, 36 resolving xrefs, 73 tasks, 17 exercises, ten activities, nine image
uses, and no failures. Faithful Indonesian descriptions are present for all
active Chapter 17 figures.

The separately authored companion covers all 75 canonical source prompts plus
eight mastery checks: 83 entries and 332 staged statement, hint, answer, and
solution surfaces. The cumulative reader passes the pinned PreTeXt RelaxNG
schema with zero diagnostics. The complete portable source admission manifest
contains 120 translated source files and 639 package-inventory entries; it is
209,866 bytes at SHA-256
`69aec9dfff5250b8fd3827a02ecb51e14543c3c6ba39cc8a550cf9ece5909348`.

## Deterministic HTML and responsive reader

Two clean finalized builds produced the same 17,244-file tree, including
17,132 HTML documents and 47,658,330 bytes, at canonical SHA-256
`76bc4dea7d56f34cb48b2c93951f7864800611bcb1397a714a820ac06b242a9c`.
The run manifests are byte-identical at 2,825,763 bytes / SHA-256
`c3a9285b9ef237cf6485509c20313e8b64113260e6d9fad35e04b7ce6730735d`.
HTML QA checks 101,578 local links/assets and 143 images with zero failures.

Live browser checks at 1440, 1280, 1024, 768, and 390 CSS pixels confirm
`lang="id-ID"`, centered page fill, no document-level horizontal overflow,
localized navigation, and working staged disclosure. The browser receipt is
17,470 bytes / SHA-256
`a662c57b42db04125a2484451aa29ce88baeed98c354dc230aa2ec27fca4c5a9`.

## Deterministic PDF and all-page visual QA

Two strict clean builds emitted the same 513-page US-Letter PDF: 4,187,800
bytes, SHA-256
`278d604c336add952a1267fa0f422a8286ba9d3060c2fd741add4e991f364490`.
The structure gate records 479 link annotations, correct Roman/Arabic page
labels, no relative URI targets, and no failures. All 513 pages were freshly
rendered at 120 dpi and inspected across 43 contact sheets. Physical page 3 is
the intentional blank front-matter verso; page 181 is the intentional sparse
appendix divider; pages 511 and 513 are the index divider and colophon. There
is no clipping, overlap, broken figure, broken formula or glyph, unreadable
content, unexpected blank/sparse page, or pagination/header defect. The PDF is
untagged, so HTML remains the primary accessible surface.

## GitHub Pages tree

The non-destructive `docs/` overlay retains historical reader entry points and
PDFs while adding Chapters 1-17. It contains 17,288 files (17,159 HTML),
81,157,293 bytes, at canonical SHA-256
`d4619cecc6c388f64d702aaeff7818d18ec69c3fb8f6656a70cf9238804ba0dc`.
Its detailed manifest is 2,833,726 bytes / SHA-256
`3da8b3f0969b1f897f114a34f4b973a1a0d776b463d28e2026939bc7eae71777`;
the compact admission receipt is 3,855 bytes / SHA-256
`8f1cde6705387a6503266cc999a78840691935682dee7c721f585f1a3bddc643`.
Docs QA checks 111,841 links/assets and 143 image references with zero
failures. The primary download exactly reproduces the deterministic PDF.

## Release package, rights, and remaining work

The deterministic release payload contains six files: the 513-page PDF;
16,671,860-byte HTML ZIP; 16,124,658-byte editable source/backend/QA ZIP;
component-license and companion-rights notes; and a 7,157-byte manifest. The
HTML and source ZIPs were independently assembled twice with identical entry
manifests.

The translated GVSU spine remains conservatively CC BY-NC-SA 3.0; the original
self-study companion remains CC BY 4.0. Component-specific figure, software,
XSL, and font notices remain intact. Production provenance is `OpenAI Codex
gpt-5.6-sol, Ultra`; no endorsement is claimed. Remote reader dependencies,
whole-book figure-provenance closure, PDF tagging, Chapters 18-20, and the
original C90 completion modules remain complete-edition work.

Verdict: Chapters 1-17 pass the bounded source, schema, deterministic build,
responsive layout, docs-tree, rights, privacy, and all-page visual gates and
are ready for the existing GitHub and Zenodo lineages.
