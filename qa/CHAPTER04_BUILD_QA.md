# Chapters 1-4 reader - admitted build and QA receipt

Date: 2026-08-22 (Europe/Berlin)  
Lane: O003/C90, id-ID  
Boundary: Chapters 1-4, *Himpunan*, *Fungsi*, *Ruang Metrik*, and
*Penerapan Ruang Metrik*, plus separately licensed self-study companions

## Result

This cumulative Chapter 4 boundary is admitted for continued edition
production and public preservation. It supersedes the Chapters 1-3 reader as
the current public boundary without claiming that the complete 20-chapter
edition or the original O003 completion modules are finished.

## Source and companion

- Exact cumulative manifest: `qa/CHAPTER04_SOURCE_MANIFEST.json`, 14,455
  bytes, SHA-256
  `7598726f8fb286105bc13187949b0c80fe73263d509b34d01bdb890958be1999`.
- Chapter 4 ordered four-file source SHA-256:
  `38be25dc99368f1dbc2cf03d9d268c7fe1fcf5c01d16fea24d61bfa3e5050c5b`.
- Cumulative 26-file source SHA-256:
  `4d6aa5b59d4ef44eecc6ef30590fecdb4ff01caf8e9b3e56e6032276442bbdc7`.
- Chapter 4 source QA passed for five IDs, three activities, eight tasks, zero
  source exercises, zero images and zero xrefs. Protected mathematics,
  attributes, IDs and task order agree except for the five deterministic
  repairs O003-C039 through O003-C043: the repeated Hamming coordinate, the
  `sting` typo, the invalid nested-definition structure, the unbalanced
  quotation mark, and the missing fixed-alphabet domain.
- Source QA: `qa/CHAPTER04_SOURCE_QA.json`, 4,759 bytes, SHA-256
  `7b7fb1b1c6600fd7cb1dc6e77a39e22d7b8df208619c3d1225c6ae0a46ff3f84`.
- Original Chapter 4 companion: 25,306 bytes, SHA-256
  `124fb57529796cd6b3a3cf972d3a19c164660ad5d5d3e687c161899dd5b20d9e`.
  QA passed all eight keyed source-task guides, four mastery checks, and 12
  each of staged hints, answers and complete solutions, with 51 unique IDs
  and two resolving xrefs.
- Companion QA: `qa/CHAPTER04_COMPANION_QA.json`, 3,465 bytes, SHA-256
  `7389855d3d2542f2bdea10d52c22597ac4efde9c66cf84e6c84901332934d6bf`.
- Backend manifest: `backend/chapter_04_companion_manifest.json`, 30,644
  bytes, SHA-256
  `c63a9efb46e3828b56d86e9d4be96444e5b53622c4b91faa0ee765c8249ae568`.
- The cumulative wrapper and all repaired source/companion components validate
  against the pinned PreTeXt 1.7.5 RelaxNG schema.

## HTML

- Runtime: Python 3.12.13, PreTeXt 1.7.5 and setuptools 75.8.0.
- Two clean builds at `SOURCE_DATE_EPOCH=1692057600` produced identical
  finalized manifests and QA reports.
- Canonical tree SHA-256:
  `fdebfdded75e228484237931e86b34148408d75bc591451fcad8af86fa29b1e2`.
- Manifest file: 407,785 bytes, SHA-256
  `6eef77270cfef31a7cbf22a05c69c19a63f6fbfdfc1e8ef5c2d985fe1c1cbd50`.
- Closure: 2,530 files, 2,419 HTML files, 7,374,549 bytes.
- Automated QA checked 7,513 links/assets and 123 images with no failures,
  duplicate IDs, missing local targets/fragments, generated-English denylist
  hits, missing image alternatives, privacy hits, or credential patterns.
- Responsive browser QA passed at 1280 x 900 and 390 x 844. With the desktop
  TOC visible, the reading column is 960 px and centered inside the available
  main pane with 32.89/32.00 px margins; hiding the TOC centers it with
  152.89/152.00 px margins. Mobile reflows to 318.22 px with no horizontal
  overflow, and its TOC drawer opens and closes without widening the page.
- Chapter 4, Hamming and Levenshtein pages render in id-ID. The first Chapter
  4 exercise, its `Petunjuk`, and its `Jawaban` opened and exposed the expected
  staged Indonesian content. Browser console errors: zero. The only warnings
  are two known MathJax component-version notices repeated across page loads.
- Browser QA: `qa/CHAPTER04_BROWSER_QA.json`, 4,631 bytes, SHA-256
  `38cc550d3644e44e52102768f51c360374e481d6449693b20d2aab22eb6174d2`.
- Current caveat: this bounded reader still references remote PreTeXt,
  Runestone, MathJax, font, CSS and JavaScript hosts. Whole-edition offline
  closure remains a release gate and is not falsely claimed here.

## PDF

- Runtime: MiKTeX 26.5 with XeLaTeX. The strict wrapper cleans the target and
  rejects hidden TeX failures even when the PreTeXt CLI reports success.
- Two clean strict builds at the fixed epoch produced identical bytes.
- Artifact: `output/chapters01-04-pdf/chapters_01_04_reader.pdf`.
- 462,645 bytes; 81 US Letter pages; PDF 1.7; SHA-256
  `1526cd465540617f3261047783d23f824d05d261635cc0fa2558e16aedbea676`.
- Unencrypted, no JavaScript, not tagged. HTML remains the primary accessible
  surface.
- All 81 pages were rendered at 120 dpi and inspected through seven contact
  sheets. Pages 5, 48, 49 and 76 were also inspected full-size after the two
  caught defects were repaired: the contents/divider now use `Lampiran` and
  `Bagian Akhir`, and `Himpunan`/`Penerapan` remain intact in large titles.
  No clipping, overlap, missing glyph, broken equation, or pagination defect
  remains.
- The final TeX pass has no fatal, undefined-reference, LaTeX-warning or
  underfull diagnostics. Three overfull diagnostics remain: the known 6.48035
  pt Chapter 1 answer line and two 9.81952/10.19273 pt unhyphenated title
  measures. Full-size pixels show all three safely inside the page without
  collision or clipping.
- PDF visual QA: `qa/CHAPTER04_PDF_VISUAL_QA.json`, 6,578 bytes, SHA-256
  `1d8608eed9c1247447a0748502db7bd647492bdf6b39a23a4d24a8fa932fd277`.

## Rights and release scope

- The translated GVSU spine is handled conservatively as CC BY-NC-SA 3.0.
- Independently authored companions are separately CC BY 4.0.
- The edition is a collection with per-component rights and explicit
  non-endorsement; it has no flattened blanket license.
- Publication must identify this truthfully as a Chapters 1-4 boundary and
  retain the prior Chapters 1-2 and Chapters 1-3 PDFs as historical artifacts.

## Next cursor

After publication and anonymous byte readback, continue immediately in source
order with Chapter 5, Greatest Lower Bounds: `chap_glb.ptx`, plus its original
staged self-study companion and modular backend.

## Publication

The GitHub commit, Pages deployment, public reader inventory and anonymous
byte-for-byte readback are recorded in `qa/CHAPTER04_PUBLICATION_RECEIPT.md`
after the transaction completes.
