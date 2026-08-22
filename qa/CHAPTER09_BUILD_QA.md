# Chapters 1-9 cumulative build and QA receipt

Verified: 2026-08-22 (Europe/Berlin)

Boundary: O003/C90 Bahasa Indonesia, complete GVSU Chapters 1-9 through
*Barisan di Ruang Metrik*, together with the separately licensed original
self-study companions for all nine chapters. This is a coherent incomplete
checkpoint of the 20-chapter edition, not a claim that the whole book or the
original O003 completion modules are finished.

## Frozen source and Chapter 9 translation

- Upstream authority remains GVSU commit
  `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
  `7df245934eedb7174d5ff8af18afff5a7abdde78`.
- Chapter 9 closes exactly over five source files / 34,075 authority bytes,
  with raw ordered SHA-256
  `c6d2935beda94460617eeba29cf6bd181fd7d061bbd11ed6b8471b91d614cce9`.
- The complete translated five-file chapter has ordered SHA-256
  `a653b56cdec48fe4497ba807bcc1bfb564019c1fc38805bb26d450f61ac1806e`.
  `CHAPTER09_SOURCE_QA.json` is 5,719 bytes / SHA-256
  `6697bd179dc1ac85986291437417672ba62cba735fd28b68d00ef07d86578328`
  and reports zero failures, 11 unique IDs and 12 resolving xrefs.
- The cumulative Chapters 1-9 source closure is 56 files. Its deterministic
  named-file SHA-256 is
  `0ebec21ae855f45842c0a475a3712b7a74d46e2660e322a5f755712a69f9c8fa`.
- `CHAPTER09_SOURCE_MANIFEST.json` is 49,185 bytes / SHA-256
  `a941e47b1d1fc7dc8f68d1a26471c8ccd69119f8f97e3eb90028224867a7e6f1`.
  It fails closed over the exact cumulative source, companion, rights, assets,
  corrections, backend, HTML, browser and PDF identities and has status
  `pass` with no pending evidence.

## Companion and modular backend

- The Chapter 9 companion covers all 44 source prompts: 16 exploration or
  activity-task guides and 28 exercise-prompt guides. Six additional mastery
  checks bring the total to 50 entries.
- Every entry has a statement, staged hint, answer and complete solution.
  `CHAPTER09_COMPANION_QA.json` is 97,616 bytes / SHA-256
  `09f2c1bd527ab8d1cf89b4feab48cf99289ccea1366817c8be68e91df6ecb492`
  and reports zero failures and one described Chapter 9 image.
- The stable-ID backend is 166,727 bytes / SHA-256
  `b1d3912e790273a1ece9d1f52530897c3dd10671de97c35991781867471da637`.
  Its 26,671-byte alias table has SHA-256
  `1623f26008ae191bf6426dd712c205a9d664c914c5d11cae07af79d1b3884852`.
  It binds all 50 entries and all 200 disclosure surfaces, the image, source
  locators, component rights and 15 verified Chapter 9 corrections.
- O003-C094 records the source-critical subspace-convergence correction;
  O003-C096 repairs the proposed-limit notation. O003-C095 is no longer
  pending: the cumulative wrapper passed the pinned PreTeXt 1.7.5 RelaxNG
  validation after the unchanged summary list became a sibling of its
  introductory paragraph; the pinned validation exited successfully.

## Deterministic HTML and reader behavior

- Two clean, fixed-epoch HTML builds followed by the idempotent Indonesian
  finalizer produced identical 7,038-file manifests. The tree contains 6,927
  HTML documents and 17,715,106 bytes; its canonical manifest SHA-256 is
  `373560dd1d3e2ddf4704688e3a0dbd22ef6a4eb7aa0cba94f2bf907dd3d61392`.
- The canonical file manifest is 1,153,907 bytes / SHA-256
  `d96bec7bc5b543b842fccb109506d61f4561d21fa49b867f958e183a11c26881`.
  Local QA checked 21,251 links/assets and 37 image references with zero
  failures; its 846-byte report has SHA-256
  `a1caf9b2acac995241c37373b3212599ee180ed27fdbdde3f3412077c9fc1d12`.
- Browser QA at 1440, 1280, 1024, 768 and 390 CSS-pixel widths found no
  document-level horizontal overflow. The desktop reading measure is centered
  at 960 px; intermediate and mobile widths reflow to 600 px and 318 px rather
  than remaining left-anchored. The long masthead, Indonesian navigation,
  Chapter 9 pages and companion pages remain readable.
- Browser interaction opened a source guide, exercise guide and mastery check
  and proved independent staged hint, answer and solution disclosures. The
  3,086-byte browser receipt has SHA-256
  `7c7a2d3146c79e3dd9a99fd2a77447180b78e50fc5038c7b70ee51d888faeede`.

## Deterministic PDF and visual inspection

- Two clean strict XeLaTeX builds used `SOURCE_DATE_EPOCH=1692057600` and the
  transcript error gate. Both emitted exactly 1,866,941 bytes with SHA-256
  `1ea66543c895f20472d273861847de09baf85299a87cd34a13b32566d1ad897a`.
  The two deterministic receipts are 314 bytes / SHA-256
  `a6851b5f7d608793ee654b7fdc7d00231ffd9666beca6b10c629ec1cbe5f5ed0`
  and 349 bytes / SHA-256
  `fcf05784d90f6bea0e0159db28825d40866e7318820b6216b8a852eb1ba2446a`.
- The PDF has 215 US-Letter pages, no rotation and 23 outline entries. Physical
  pages 1-6 use lowercase Roman page labels and physical page 7 begins Arabic
  page 1. All 218 link annotations are valid; the two interactive-lab links
  use the portable public HTTPS target and no relative URI remains.
- The 5,689-byte structure report has SHA-256
  `cbe4363464029ee043059b3ef73fa76ec99d29f07649a1577dae64be4e1c4188`
  and status `pass`.
- All 215 pages were inspected through all-page contact sheets; physical
  pages 82-90 (Chapter 9), 91-215 (appendices), and long titles on pages 65,
  73, 174 and 196 received closer inspection. No clipping, overlap, broken
  glyph box, illegible formula, title overflow, figure cutoff or faulty
  transition was found. A 10-pixel edge sweep at 120 dpi found no edge content.
  The 1,240-byte visual receipt has SHA-256
  `52fd3dcc712a00d510da0c7da8c73aa7021e314c07481cf6ed18a0c7b495860f`.
- Non-blocking TeX box warnings include inherited long headings and a 2.83 pt
  Chapter 9 line; targeted visual inspection proves that they do not clip.
  Sparse pages 90, 98, 109 and 142 arise from clean chapter/appendix breaks.

## Runtime, rights and open caveats

- Pinned runtime: Python 3.12.13, PreTeXt 1.7.5, setuptools 75.8.0 and
  MiKTeX 26.5. The wrapper targets are `chapters01-09-html` and
  `chapters01-09-pdf`.
- The translated GVSU spine remains conservatively CC BY-NC-SA 3.0. The
  independently authored self-study companion remains a separately identified
  CC BY 4.0 component. Figure/software notices remain component-specific; no
  endorsement is claimed and the collection is not flattened to one license.
- HTML remains the primary accessible surface. The PDF is untagged and its
  mathematical fonts have incomplete Unicode extraction maps. Complete-edition
  offline closure also remains open: the current bounded HTML still references
  documented PreTeXt, Runestone, MathJax, font, CDN and rights hosts.

## Verdict

Chapters 1-9 and their separately licensed self-study companions are admitted
as the current coherent cumulative reader boundary. Source, schema, companion,
backend, deterministic HTML/PDF, link/asset, responsive/reflow, staged
disclosure, PDF structure and all-page visual gates pass. Publication must say
truthfully that 9 of 20 GVSU chapters are available; production advances next
to Chapter 10 in source order after this boundary is preserved and anonymously
read back.
