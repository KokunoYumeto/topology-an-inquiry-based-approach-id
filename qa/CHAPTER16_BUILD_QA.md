# Chapters 1–16 cumulative build and QA receipt

Verified: 2026-08-28 (Europe/Berlin)

Boundary: O003/C90 Bahasa Indonesia through the complete GVSU Chapter 16,
*Ruang Hasil Bagi*, plus its separately licensed original self-study companion.
This is a coherent 16-of-20 checkpoint, not a complete-edition claim.

## Source, companion, and schema

Authority remains Steven Schlicker's GVSU *Topology: An Inquiry-Based
Approach* at commit `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
`7df245934eedb7174d5ff8af18afff5a7abdde78`. The official 2,200,204-byte
archive has SHA-256
`d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3`.

Chapter 16's seven translated files total 58,310 bytes at ordered combined
SHA-256 `158afadc3f4ec7be7cae2542381975cb006617ff666bac145acdc205026d4ee6`.
`CHAPTER16_SOURCE_COMPLETE_QA.json` is 12,403 bytes / SHA-256
`52afa5f8b4919d6a14f21d105210c0b57a1249ede5c18923b7aae822adcea5bd`;
it verifies 1,106 elements, 667 protected mathematics nodes, 21 IDs, 25 xrefs,
53 tasks, 13 exercises, six activities, 16 image references, and no failures.
Faithful Indonesian descriptions were added for the active Chapter 16 figures.

The separately authored companion covers all 52 canonical prompts plus eight
mastery checks: 60 entries and 240 staged surfaces. The cumulative 209-file
closure contains 2,390,442 bytes, 3,783 unique IDs, and 254 resolving xrefs.
The cumulative PreTeXt wrapper passes RelaxNG with zero diagnostics.

## Deterministic HTML and responsive reader

Two clean finalized builds produced the same 15,690-file tree, including
15,578 HTML documents and 43,189,287 bytes, at canonical SHA-256
`03bceb9b8c1a5455f08eb95283925e242109b14e146dc47a0913dec1b24d11f9`.
The run manifests are byte-identical at 2,572,200 bytes / SHA-256
`fc184d5c63cc4d83454eca36af8ef8acd1dad798b6f79dba03ce97b232064633`;
the final detailed manifest is 2,572,385 bytes / SHA-256
`d6817b3db305cba28ce0f73b599fc7ccd9a20b75fcc4231f0af4dc7a844c8df7`.
HTML QA checks 90,483 local links/assets and 109 images with zero failures.

Live browser checks at 1440, 1280, 1024, 768, and 390 CSS pixels confirm
`lang="id-ID"`, centered content that fills the actual reader pane, no
document-level horizontal overflow, localized navigation, and working staged
disclosure. The 17,426-byte receipt has SHA-256
`0e022a2f264391181aad8ace320ff1f6034f1acaf4efa758b10362c77ff62390`.

## Deterministic PDF and all-page visual QA

Two strict clean builds emitted the same 467-page US-Letter PDF: 3,810,136
bytes, SHA-256
`0a240d7416b6730e8e69c7485524fb5309a1153ec4b07e97dd4db080e76a1fd7`.
The structure receipt records 38 outline entries, 434 annotations, correct
Roman/Arabic page labels, no relative URI targets, and no failures. All 467
pages were freshly rendered at 120 dpi and inspected across 39 contact sheets;
physical page 3 is the intentional blank verso and page 166 the intentional
sparse appendix divider. There are no unexpected blank or edge-touching pages,
and no clipping, overlap, broken formula, unreadable glyph, or figure defect.
The PDF is untagged, so HTML remains the primary accessible surface.

## GitHub Pages tree

The non-destructive `docs/` overlay retains the exact historical reader entry
points and PDFs while adding Chapters 1–16. It contains 15,722 files (15,594
HTML), totaling 72,380,179 bytes at canonical SHA-256
`bad8c4a4e70e3f76e3ab6d22b68743879d9d1d185df9b4e086b08fce53a0b809`.
Its detailed manifest is 2,578,254 bytes / SHA-256
`db1fc2d637de097dc182232300258c13efade30d0bc0ecb944935cfb69a1c8df`;
the compact admission receipt is 2,004 bytes / SHA-256
`26684fdf1773ae1ba23852c2648b8267b369c029f5372192a9b70f3374ea0253`.
Docs QA checks 93,595 links/assets and 109 images with zero failures. The
primary download exactly reproduces the deterministic PDF.

## Rights and remaining work

The translated GVSU spine remains conservatively CC BY-NC-SA 3.0; the original
self-study companion remains CC BY 4.0. Component-specific figure, software,
XSL, and font notices remain intact. Production provenance is `OpenAI Codex
gpt-5.6-sol, Ultra`; no endorsement is claimed. Remote reader dependencies,
whole-book figure-provenance closure, PDF tagging, Chapters 17–20, and the
original C90 completion modules remain complete-edition work.

Verdict: Chapters 1–16 pass the bounded source, schema, deterministic build,
responsive layout, documentation-tree, rights, privacy, and all-page visual
gates and are ready for the existing GitHub and Zenodo lineages.
