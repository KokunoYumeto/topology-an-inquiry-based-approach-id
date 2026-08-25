# Chapters 1-13 cumulative build and QA receipt

Verified: 2026-08-26 (Europe/Berlin)

Boundary: O003/C90 Bahasa Indonesia, the complete GVSU Chapter 13 boundary
through *Himpunan Tertutup dalam Ruang Topologi*, together with its separately
licensed original self-study companion. This is a coherent partial checkpoint
(13 of 20 source chapters), not a claim that the complete GVSU book or the
original O003 completion modules are finished.

## Frozen source and Chapter 13 translation

- Upstream authority remains Steven Schlicker's GVSU *Topology: An
  Inquiry-Based Approach* at commit
  `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
  `7df245934eedb7174d5ff8af18afff5a7abdde78`. The official 2,200,204-byte
  archive has SHA-256
  `d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3`.
- Chapter 13 closes over nine translated source files in frozen order. Their
  translated combined SHA-256 is
  `d15a1182cd12f84eb54ade92316de6f6d281936294fe5120c8f282406e371253`.
  `CHAPTER13_SOURCE_QA.json` is 8,988 bytes / SHA-256
  `45ef76db9669c9840f4ca71d4af53089051a4dd7f8858f81078964577314f8ba`;
  it records 23 unique IDs, 25 cumulative-resolving xrefs, 76 independent
  learner prompts, seven structural grouping tasks, zero assets, zero
  interactive surfaces, and zero failures.
- Corrections O003-C146 through O003-C161 are explicit and fail-closed. They
  repair source-critical notation, a finite-union proof, ambiguous or malformed
  task shells, and one schema-invalid definition/statement shell without
  silently deleting descendants. `SOURCE_CORRECTIONS.csv` has SHA-256
  `1c33b5f2710d0af037087cf3bed8fdd0af58f9efba6f40ef1073401a1b170746`.
  The terminology ledger has SHA-256
  `67ffe90c191d7cfe1222ec85e0efadae460847751a5989aa2c6b8d172d4ede40`.

## Companion and modular backend

- Every one of the 76 source prompts has original staged support. Eight
  original mastery checks extend the closure to 84 entries with 84 statements,
  84 staged hints, 84 answers or rubrics, and 84 complete solutions: 336
  surfaces. The seven grouping nodes remain separately mapped and are not
  double-counted as learner prompts.
- Two deterministic refreshes reproduced the 46,760-byte prompt map at
  SHA-256
  `49aa64a71a6bdb16a3ea98362809162e5e4be04c10300a657e5450db4fde4471`,
  the 6,645-byte grouping map at
  `b0838f0abd6cb93b60066386a09f45fe19f6388a66e7608b30b787ef69dc473e`,
  the 22,099-byte alias table at
  `0201894e8726976f30f862748f9fd94b6a947f082035df887cc48e600fb9a875`,
  and the 153,823-byte companion manifest at
  `3f263c32be4c853794d09a3f132c86c737c461f529cf737b2b5ffe0d1ca538a0`.
  `CHAPTER13_COMPANION_QA.json` is 4,139 bytes / SHA-256
  `5cd319c435b09e6c9bfec3df1f19c27005e9731e489b59f5c977e8e74b764c6d`.
- The 7,040-byte cumulative PreTeXt wrapper has SHA-256
  `399e8159df5896c0f8fe32c5429ea0482e952f3652b763a584d34c7429a862d5`.
  Its complete local XInclude closure passes the pinned PreTeXt RelaxNG schema
  with zero diagnostics. `CHAPTER13_CUMULATIVE_SCHEMA_QA.json` is 7,867 bytes
  / SHA-256
  `b0c8ed3952868f427f5951c390ebe822a04874bb0c1e0b0426763bd71fd838cf`.

## Deterministic HTML and responsive reader

Two clean finalized HTML builds produced the same 12,388-file tree, including
12,277 HTML documents and 32,104,875 bytes, at canonical SHA-256
`d79425dbc64176d50ecfcc1ffc926940244bb4d08a5446a341a018bb3bfed28c`.
The canonical manifest is 2,029,759 bytes / SHA-256
`3f31ee677035759eedf7eb3b4cc0aa7edf007610efe2724ceabe7d209ff0cd21`;
the two 2,029,574-byte run manifests are byte-identical at SHA-256
`a9c017cb0df970ec489e8a82ff396dd91690d4b709e95efb4ca48d6dec05728f`.
`CHAPTER13_HTML_QA.json` is 829 bytes / SHA-256
`559c91b2fb336990ec69f08c2d790ee479c1efbb12d75fa7f4a82967d268a977`
and checks 50,890 local links/assets plus 40 image references with no failures.

Live browser checks covered 1440, 1280, 1024, 768, and 390 CSS-pixel widths.
The reading column fills and centers within the main panel, `lang="id-ID"` and
localized chrome remain intact, and no checked surface has document-level
horizontal overflow. A Chapter 13 guide opened its statement, hint, answer,
and solution at 390 pixels without overflow. The 6,459-byte browser receipt has
SHA-256
`03d70255fbd25d153a7a9e41fea3304d92698a3887e35765f6c5a90ed0c6093b`.

## Deterministic PDF and all-page visual inspection

Two strict clean builds emitted the same 368-page US-Letter PDF: 3,012,937
bytes, SHA-256
`746cdd14604cae66f3cb8f6de27ddf6043749dede2c22dc725da9be0ffaa31d1`.
The run receipts are 479 bytes / SHA-256
`b4935bd36b157e1f6dae658d6b010eb1ff087fa5206ab496c76541aeaf49cb79`
and 701 bytes / SHA-256
`cc9464f5d6d0d5788d74246172c72e1ae747510a110f330e81285d74a0691af1`.
The strict logs are 129,512 bytes each, with SHA-256 values
`a0610c73e36d31a04dc5ba3955d4bc1a1f18bdcdec59625c39b2e011aca937b0`
and `63920f7e09d944c33287061367e60a67e909d60505973dbaac4e4fab7288defe`.
The 7,303-byte structure receipt has SHA-256
`9fc2c03cfbf53d41d4e4388ba361dfeac18a563ea1ce2d2d8420884e68d3efaf`:
32 outline entries, 350 link annotations, no replacement-character titles,
no relative URI targets, and no failures.

The first visually inspected deterministic candidate exposed one clipped long
Chapter 13 companion title on physical page 340. The LaTeX chapter-heading
template now permits ragged-right wrapping while retaining the existing
no-intra-word-hyphenation rule. Both strict builds were rerun after that repair.
All 368 final pages were freshly rendered at 120 dpi with Poppler `pdftoppm
24.04.0` and inspected in 31 contact sheets. Pages 7 and 138 are intentional
sparse contents/divider pages, page 3 is the intentional blank verso, and the
corrected page 340 wraps cleanly. There are zero unexpected blank pages, zero
edge-touching pages, and no clipping, overlap, broken formula, or unreadable
glyph. The 247,667-byte final visual receipt has SHA-256
`812f3bb7da2f815f8fb6fd92ba95af3945166b470f57735f9f5de5bc423ea880`.
The PDF is not tagged; HTML remains the primary accessible surface.

The 15,384-byte standalone-asset metadata receipt remains pass at SHA-256
`7133da5332aefb493bc655d36e9cdf863fa7ebe23118ea8f38750b19b5b7bac7`.
It covers the twenty sanitized legacy figure PDFs while retaining the pinned
unaltered upstream archive as authority evidence.

## GitHub Pages publication tree

The non-destructive `docs/` overlay retains historical entry points and earlier
PDFs while adding the complete Chapters 1-13 reader and its primary 368-page
PDF. It contains 12,411 files (12,287 HTML), totaling 50,427,230 bytes at
canonical SHA-256
`865fe7790ef2774ed25dfbd171f2a4d67c14e5a6cebaba35ab95fd8f150fd554`.
The detailed manifest is 2,034,011 bytes / SHA-256
`aa1e088fdee15d6f53d2150d711baede44b758778cef71749799b44d2f713f09`;
the compact manifest is 1,067 bytes / SHA-256
`5abd45d74555c80983d24afb578674a747e437101ef79d26025ec3ba8e029205`.
`CHAPTER13_DOCS_QA.json` is 1,039 bytes / SHA-256
`568a75f042647681cf4f045bfeab504c1f23ee3e4fa2e609caf7ff8659881c84`,
checking 52,547 links/assets and 40 images with zero failures. The primary
download reproduces the verified PDF bytes above.

## Rights, provenance, and open caveats

The translated GVSU spine remains conservatively CC BY-NC-SA 3.0. The
original self-study companion remains a separate CC BY 4.0 component. Figure,
software, XSL, font, and other notices retain their component-specific rights;
the collection is not flattened to one license, and no endorsement by the
source author or institution is claimed. `LICENSES.md` is 2,277 bytes / SHA-
256 `408eeec186fd9b34660ea5d6df19df5d0e0da7ae63e8681852ff5eaa7b6fb941`;
`companion/RIGHTS.md` is 2,181 bytes / SHA-256
`ef9e9960775b17d187cc655fc73a6f7d76b3d8fe05b9960d3e168ae9fc4fcfe7`.
The exact production-model provenance is `OpenAI Codex gpt-5.6-sol, Ultra`;
source-author, institutional, source, and human-contributor credits remain
intact.

Remote PreTeXt/Runestone/MathJax/font dependencies remain explicitly recorded;
whole-book offline closure, figure-provenance closure, and PDF tagging remain
complete-edition gates. Chapters 14-20 and the separately licensed original C90
completion modules remain unfinished, so this checkpoint remains labeled
partial.

## Verdict

Chapter 13 and its separate self-study/backend component pass the bounded
source, terminology, schema, deterministic HTML/PDF, responsive browser,
docs-tree, and all-page visual gates. This is the next coherent cumulative
release boundary, not completion of the 20-chapter edition. It is ready for the
existing GitHub and Zenodo lineages.
