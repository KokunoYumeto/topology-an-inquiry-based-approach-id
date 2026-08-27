# Chapters 1–15 cumulative build and QA receipt

Verified: 2026-08-27 (Europe/Berlin)

Boundary: O003/C90 Bahasa Indonesia, the complete GVSU Chapter 15 boundary
through *Subruang*, together with its separately licensed original self-study
companion. This is a coherent partial checkpoint (15 of 20 source chapters),
not a claim that the complete GVSU book or the original O003 completion modules
are finished.

## Frozen source and Chapter 15 translation

- Upstream authority remains Steven Schlicker's GVSU *Topology: An
  Inquiry-Based Approach* at commit
  `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
  `7df245934eedb7174d5ff8af18afff5a7abdde78`. The official 2,200,204-byte
  archive has SHA-256
  `d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3`.
- Chapter 15 closes over seven translated source files in frozen order. Their
  translated combined SHA-256 is
  `37de2f5158dff6a266dc79297ebddc216dd053ea5a037e2e08ebab9042afa215`.
  `CHAPTER15_SOURCE_COMPLETE_QA.json` is 6,279 bytes / SHA-256
  `c4f20c003f136af40025f21291c454bc25c25e3d50060d577371ab1ded0cde11`;
  it verifies 464 elements, 258 protected mathematics nodes, 11 IDs, four
  resolving xrefs, 27 task nodes, eight exercises, four activities, one image,
  and zero failures. The independently frozen learner denominator is 30 source
  prompts plus two structural grouping nodes.
- The `Subspace_open` figure was checked against the frozen upstream PDF and
  has a faithful Indonesian description of the ambient space, subspace, open
  set, and relative intersection. Corrections O003-C182 through O003-C187 and
  terminology O003-T195 through O003-T203 are explicit and fail-closed. The
  correction ledger is 74,870 bytes / SHA-256
  `1a99e094715799faf8c9d19a688ab66278007e72dfff18c7bb4584bd38007a33`;
  the terminology ledger is 21,270 bytes / SHA-256
  `01eb146a691688722e18703941c2a27d3d283650aaa32ef99dc1edd451dcb836`.

## Companion and modular backend

- Every one of the 30 Chapter 15 source prompts has original staged support.
  Eight original mastery checks extend the closure to 38 entries with 38
  statements, 38 hints, 38 answers or rubrics, and 38 complete solutions: 152
  staged surfaces. The two grouping nodes are mapped separately and are not
  double-counted as learner prompts.
- Deterministic regeneration reproduces the 17,335-byte prompt map at SHA-256
  `ad8eccbb1ceb14f948886203563d7a1a360dc474fff21a0273928b55691138b5`,
  the 2,281-byte grouping map at
  `bbd38e4c39f02ee44e48ab33068ccf6c697d350767f3458211dc3a56706c4488`,
  the 9,584-byte alias table at
  `0912786d7899f9222bd1c4f2018e9b27d64815e51e6ebd9eee291d0d6916d2f0`,
  and the 68,566-byte companion manifest at
  `d3acc8a08bee53cfa63f49b782c8e33f80dff54b43bf40c50b8064fb438bd784`.
  `CHAPTER15_COMPANION_QA.json` is 5,459 bytes / SHA-256
  `4b743b8e63a7c023e0297ef586da22c39a70f8658b008dc4c5eaa0c8cb072590`.
- The 7,356-byte cumulative PreTeXt wrapper has SHA-256
  `1a7b1681dd664d40aee8f2a19c04a6e14499897217edb7e7a419a09f9176acc8`.
  Its 194-file local XInclude closure contains 2,191,387 bytes, 3,514 unique
  IDs, and 227 resolving xref occurrences. The expanded 43,131-element reader
  passes the pinned PreTeXt RelaxNG schema with zero diagnostics. The 9,277-byte
  receipt has SHA-256
  `3f640b45b1267feeab9a19abe2a3c8a9ad0a2eabfc31bd49ceb983d989364973`.

## Deterministic HTML and responsive reader

Two clean finalized HTML builds produced the same 14,566-file tree, including
14,455 HTML documents and 38,545,201 bytes, at canonical SHA-256
`b42c7c252ceb49745ca13f4bb890a2149e01358ceb8e343ac3fa772e11fc1ee7`.
The two 2,387,209-byte run manifests are byte-identical at SHA-256
`95063b0e55e780fdd30b9b6cd4ca5ba4f6f076b5eccda3a6a99ab64ed3b5ddb1`;
the final 2,387,394-byte detailed manifest has SHA-256
`a3758c2d90d9838771a4cedae3ac29b513442462774bc7db73453ef11fa58616`.
`CHAPTER15_HTML_QA.json` is 891 bytes / SHA-256
`e2d686f55ed33d4808f927d1d3a40b0bf007c9e9be56a353c29aa6c49d864b08`
and checks 66,653 local links/assets plus 44 image references with no failures.

Live in-app browser checks used a fresh byte-verified local origin at 1440,
1280, 1024, 768, and 390 CSS-pixel widths. The reading measure is centered in
the actual main pane, fills the available reader width, and has no document-
level horizontal overflow. `lang="id-ID"`, localized navigation, Chapter 15,
its exercises, companion, mastery surface, and live staged disclosure all
pass. The first guide opened its statement, hint, answer, and solution at the
390-pixel viewport. Console and page-error counts are zero; 26 repeated MathJax
component-version metadata warnings are benign. The 8,218-byte browser receipt
has SHA-256
`54981e2d1b37ef7a9c949b3ef23cf7318c73e39cb80a5cfd30079966cd5f99f7`.

## Deterministic PDF and all-page visual inspection

Two strict clean builds emitted the same 428-page US-Letter PDF: 3,453,492
bytes, SHA-256
`b62c1a6ff498cce11312fcb412ee74f47a8893a3363395414eb8f526dbf0456e`.
The run receipts are 479 bytes / SHA-256
`1dec7c59af59378d04f34620602448fecd926df18bc8723f44fc72367bc8e24b`
and 701 bytes / SHA-256
`a273ae2471f9b907958e228db45d59b9afac7f6b85eb3229484fe12b1015efb0`.
The strict logs are 152,822 and 152,824 bytes, with SHA-256 values
`305fa84b3450c3d25bc731540ea762ac24c975eba27940922baba3b886a30626`
and `013ec60dc4869d59784f7f9c9dc483e3af6dedbb8b7c2c43a15b1e2fffcfbf72`.
The 8,087-byte structure receipt has SHA-256
`e0f6fcdf0864efd8f61ef5d09001b2b9f23a839e1c60195b97c019332bf614a5`:
36 outline entries, 393 link annotations, two exact public lab URLs, no
relative URI targets, correct Roman/Arabic page labels, and no failures.

All 428 final pages were freshly rendered at 120 dpi with Poppler and inspected
across all 36 contact sheets. Physical page 3 is the intentional blank verso;
physical page 153 is the intentional sparse appendix divider. Physical page 73
contains the intact final one-line exercise item on the last verso before the
recto Chapter 8 opener; moving it would merely create a blank verso, so it is
accepted as open-right book pagination rather than missing content. The
Chapter 15 figure on physical page 148, companion pages 410–425, index, and
colophon were also inspected individually at full resolution. There are zero
unexpected blank pages, zero edge-touching pages, and no clipping, overlap,
broken formula, unreadable glyph, broken figure, or page-number defect. The
287,601-byte pixel receipt has SHA-256
`7a7200598293d19265bd40cf902928ae3c12dad87dfd0694a260b6ecc9d7e937`.
The PDF is untagged; HTML remains the primary accessible surface.

The 15,384-byte standalone-asset metadata receipt passes at SHA-256
`254ab40ede47fd6ad5e87f76fcff4f80bba082fb561f006584efb52dd71f5d08`.
It covers the twenty sanitized legacy figure PDFs while retaining the pinned,
unaltered upstream archive as authority evidence.

## GitHub Pages publication tree

The non-destructive `docs/` overlay retains every historical entry point and
earlier PDF while adding the complete Chapters 1–15 reader and its primary
428-page PDF. It contains 14,595 files (14,469 HTML), totaling 63,820,708 bytes
at canonical SHA-256
`8a4c1c8620a90d4bb4beb6f70b2efe2732a64e092a67cd1f95cdb0abb67a31f1`.
The detailed manifest is 2,392,724 bytes / SHA-256
`7df4bbf38e8b626c7313ce40e184a55152b761f19e0a11c230d7ad2835cea2ba`;
the compact admission receipt is 2,004 bytes / SHA-256
`0b45434464216120766e6f7394a9dd9e8e0ac72b2c7bc996eca2ed0fd5848980`.
`CHAPTER15_DOCS_QA.json` is 1,034 bytes / SHA-256
`2392533a4e2bfc6046596de7c1b6cc8d3ba20c2fb5883c505244dbfef92a2cfe`,
checking 69,250 links/assets and 44 images with zero failures. The primary
download reproduces the deterministic PDF bytes above.

## Rights, provenance, and open caveats

The translated GVSU spine remains conservatively CC BY-NC-SA 3.0. The original
self-study companion remains a separate CC BY 4.0 component. Figure, software,
XSL, font, and other notices retain their component-specific rights; the
collection is not flattened to one license, and no endorsement by the source
author or institution is claimed. `LICENSES.md` is 2,277 bytes / SHA-256
`408eeec186fd9b34660ea5d6df19df5d0e0da7ae63e8681852ff5eaa7b6fb941`;
`companion/RIGHTS.md` is 2,181 bytes / SHA-256
`ef9e9960775b17d187cc655fc73a6f7d76b3d8fe05b9960d3e168ae9fc4fcfe7`.
The exact production-model provenance is `OpenAI Codex gpt-5.6-sol, Ultra`;
source-author, institutional, source, and human-contributor credits remain
intact.

Remote PreTeXt/Runestone/MathJax/font dependencies remain explicitly recorded;
whole-book offline closure, figure-provenance closure, and PDF tagging remain
complete-edition gates. Chapters 16–20 and the separately licensed original
C90 completion modules remain unfinished, so this checkpoint remains labeled
partial.

## Verdict

Chapter 15 and its separate self-study/backend component pass the bounded
source, terminology, schema, deterministic HTML/PDF, responsive browser,
documentation-tree, rights, privacy, and all-page visual gates. This is the
next coherent cumulative release boundary, not completion of the 20-chapter
edition. It is ready for the existing GitHub and Zenodo lineages.
