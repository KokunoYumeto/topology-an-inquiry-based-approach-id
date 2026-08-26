# Chapters 1-14 cumulative build and QA receipt

Verified: 2026-08-26 (Europe/Berlin)

Boundary: O003/C90 Bahasa Indonesia, the complete GVSU Chapter 14 boundary
through *Kekontinuan dan Homeomorfisme*, together with its separately licensed
original self-study companion. This is a coherent partial checkpoint (14 of 20
source chapters), not a claim that the complete GVSU book or the original O003
completion modules are finished.

## Frozen source and Chapter 14 translation

- Upstream authority remains Steven Schlicker's GVSU *Topology: An
  Inquiry-Based Approach* at commit
  `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
  `7df245934eedb7174d5ff8af18afff5a7abdde78`. The official 2,200,204-byte
  archive has SHA-256
  `d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3`.
- Chapter 14 closes over eight translated source files in frozen order. Their
  translated combined SHA-256 is
  `bc2c94ae8d6cd579e9babdce2aaf3694268093cd1d3f0a57fc8c635f190029df`.
  `CHAPTER14_SOURCE_COMPLETE_QA.json` is 6,902 bytes / SHA-256
  `120509adb21630235263555dc35019a88e9629e5ec8df3722c176b4670a8c4d4`;
  it verifies 1,028 elements, 534 protected math nodes, 19 IDs, 17 resolving
  xrefs, 80 task nodes, 13 exercises, six activities/explorations, one image,
  and zero failures. The independently frozen learner denominator is 81 source
  prompts plus three structural grouping nodes.
- The translated `Equivalence` figure has a faithful Indonesian description.
  Corrections O003-C162 through O003-C181 and terminology O003-T167 through
  O003-T194 are explicit and fail-closed. The correction ledger is 72,006
  bytes / SHA-256
  `a7b535992326f5651f91f5a73630b88f6a09e2733e4e5adc82afe593f48fe23a`;
  the terminology ledger is 20,054 bytes / SHA-256
  `51fa85741a48f48bc869b5b5e9ab66933155787619ac6c32872b9a6fda70498e`.

## Companion and modular backend

- Every one of the 81 source prompts has original staged support. Eight
  original mastery checks extend the closure to 89 entries with 89 statements,
  89 staged hints, 89 answers or rubrics, and 89 complete solutions: 356
  surfaces. The three grouping nodes remain separately mapped and are not
  double-counted as learner prompts.
- Deterministic regeneration reproduces the 47,375-byte prompt map at SHA-256
  `377e3251cafb42f5e307cf163a0b302529250f453adf6f5962890923273b9884`,
  the 2,984-byte grouping map at
  `d3204860900770fa814007b4e4db8e859caa0a5a479bbb54a00d56cd239d7e13`,
  the 23,073-byte alias table at
  `84996bf9180ad0dac064ebe3d12f75c97445f2565ff1f603c759cc3f97656d5e`,
  and the 159,465-byte companion manifest at
  `3520fb2096b959236229dce4512e1ad749cad945fd54d0bea92c50afee0f0300`.
  `CHAPTER14_COMPANION_QA.json` is 4,547 bytes / SHA-256
  `26137f716d00fb44afadbc4c2e7f181bb1cc521a3bac801f68722926ac1dee1f`.
- The 7,208-byte cumulative PreTeXt wrapper has SHA-256
  `a28ee54bc5db65792cfeebcf4044e83b9b293108cd863381555e5f11b3d21fa5`.
  Its 181-file local XInclude closure expands to 40,863 elements and passes the
  pinned PreTeXt RelaxNG schema with zero diagnostics. The 8,741-byte receipt
  has SHA-256
  `45303693f982c12c9196e8942eb2fd7cb221a7788e1cc5bb653fbe9012eee19a`.

## Deterministic HTML and responsive reader

Two clean finalized HTML builds produced the same 13,893-file tree, including
13,782 HTML documents and 36,198,109 bytes, at canonical SHA-256
`f9419cd3243e08fac8c1a6047d258a99769d9f2bde258ad6739c9122f8d7da2a`.
The final detailed manifest is 2,276,992 bytes / SHA-256
`cb84d215948e6fbe572fd510e767165b6797fff8fe5603ab155b007d40aa850d`;
the two 2,276,807-byte run manifests are byte-identical at SHA-256
`37580725449d67a678ae7bf35a43ab2bdd6ce7a2e8963d5ced93f171ddd5a959`.
`CHAPTER14_HTML_QA.json` is 864 bytes / SHA-256
`4273e132db82f7d1732ebf46a892042dfc3f98312fc94e9ec7857e3421f718f6`
and checks 60,157 local links/assets plus 42 image references with no failures.

Live in-app browser checks used a fresh local origin and covered 1440, 1280,
1024, 768, and 390 CSS-pixel widths. The reading measure is centered within
the actual main pane at every width with less than one pixel of left/right
delta. `lang="id-ID"`, localized navigation, the Chapter 14 source chapter,
exercise section, companion and mastery surfaces remain intact; no checked
surface has document-level horizontal overflow. At 390 pixels, the Chapter 14
guide `o003-c90-ch14-guide-02` opened its statement, hint, answer, and solution.
Long display mathematics scrolls locally instead of widening or clipping the
page. Console output contained no errors, only two repeated non-blocking
MathJax component-version notices. The 4,265-byte browser receipt has SHA-256
`18391381af744fb248aa4ad535a0f84d7e6f46449bd5cbf521a7f74178d3ac1b`.

## Deterministic PDF and all-page visual inspection

Two strict clean builds emitted the same 407-page US-Letter PDF: 3,303,987
bytes, SHA-256
`1a1cdbdb8714071894206859696aa734541f4b7b48d13be1b65fa00f68e0b43a`.
The run receipts are 479 bytes / SHA-256
`646cb7aee85583896c34653ec4288aef87d98eb09436c97ab2d087c13da4fa38`
and 701 bytes / SHA-256
`a594bd843da41413d66c07e36518e907993bb9606dee36e3b4cc8df3009f7184`.
The strict logs are 148,386 bytes each, with SHA-256 values
`f8499f1d43faf76811b23aa52b05ff6f3a348aa36f3b18133c2021ae539120cb`
and `0177e1fe6152830a145e50f64b84abeee88fa36c7f0f0f6ec3add8a09a260500`.
The 7,820-byte structure receipt has SHA-256
`d6edf21f3892bd2cb20c0acd0e3b29a0c9c53f17744fe95df038822c95cbcf40`:
34 outline entries, 381 link annotations, two exact public lab URLs, no
relative URI targets, correct Roman/Arabic page labels, and no failures.

The first deterministic candidate exposed real right-edge clipping in the
Chapter 14 guide on physical page 376. Its two topology definitions were
re-expressed as two mathematically equivalent display equations; the companion
backend and schema receipts were regenerated, and both strict PDF builds were
rerun from the corrected source. All 407 final pages were freshly rendered at
120 dpi with Poppler `pdftoppm 24.04.0` and inspected across all 34 contact
sheets. Physical page 3 is the intentional blank verso; physical page 148 is
the intentional sparse appendix divider. The repaired page 376 and every
warning/risk page were also inspected at full resolution. There are zero
unexpected blank pages, zero edge-touching pages, and no clipping, overlap,
broken formula, unreadable glyph, broken figure, or page-number defect. The
273,632-byte pixel receipt has SHA-256
`1b217b8a8db61879fb3c9a857bd8af572553adf7b90576dce2703c659f7bf597`.
The PDF is untagged; HTML remains the primary accessible surface.

The 15,384-byte standalone-asset metadata receipt remains pass at SHA-256
`7133da5332aefb493bc655d36e9cdf863fa7ebe23118ea8f38750b19b5b7bac7`.
It covers the twenty sanitized legacy figure PDFs while retaining the pinned
unaltered upstream archive as authority evidence.

## GitHub Pages publication tree

The non-destructive `docs/` overlay retains every historical entry point and
earlier PDF while adding the complete Chapters 1-14 reader and its primary
407-page PDF. It contains 13,919 files (13,794 HTML), totaling 57,919,130 bytes
at canonical SHA-256
`558084d5dcb049b3ba2c8d6a3c64db4537e03cab96ec72c55e86615380f977d2`.
The detailed manifest is 2,281,783 bytes / SHA-256
`0ecf12371b7087ed2b353bcdd429e68a166048c6bde9e44db69feebab97c501c`;
the compact admission receipt is 2,004 bytes / SHA-256
`50b3f9396ddb0efe64b9fc23a9ac0dd98aad554ac22df52d7ffb59a99f29c471`.
`CHAPTER14_DOCS_QA.json` is 1,049 bytes / SHA-256
`6b90471a643a8b59e7dc667c5b350200b0a8e2fd5ac8084d6cfac87275146712`,
checking 62,265 links/assets and 42 images with zero failures. The primary
download reproduces the deterministic PDF bytes above.

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
complete-edition gates. Chapters 15-20 and the separately licensed original
C90 completion modules remain unfinished, so this checkpoint remains labeled
partial.

## Verdict

Chapter 14 and its separate self-study/backend component pass the bounded
source, terminology, schema, deterministic HTML/PDF, responsive browser,
docs-tree, rights, privacy, and all-page visual gates. This is the next coherent
cumulative release boundary, not completion of the 20-chapter edition. It is
ready for the existing GitHub and Zenodo lineages.
