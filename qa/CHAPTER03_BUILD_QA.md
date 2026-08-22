# Chapters 1-3 reader - admitted build and QA receipt

Date: 2026-08-22 (Europe/Berlin)  
Lane: O003/C90, id-ID  
Boundary: Chapters 1-3, Himpunan, Fungsi, and Ruang Metrik, plus separately
licensed self-study companions

## Result

This cumulative Chapter 3 boundary is admitted for continued edition
production and public preservation. It supersedes the Chapters 1-2 reader as
the current public boundary without claiming that the complete 20-chapter
edition is finished.

## Source and companion

- Exact cumulative manifest: `qa/CHAPTER03_SOURCE_MANIFEST.json`, 10,269 bytes,
  SHA-256 `3e4b243aa5470ec3708829bcf197554df1a11d3f7aee644cff341d6be2792d4b`.
- Chapter 1 source combined SHA-256:
  `a4378df30a25d675ac4261d8aa0266a8368bf99d9a405632cc00c8506127bbf3`.
- Chapter 2 source combined SHA-256 after the schema-only relocation recorded
  as O003-C036:
  `3b8c9bea710e3da381264f9ab669bcac6d40103362172a938cb33a6bb2b091e5`.
- Chapter 3 source combined SHA-256:
  `9f5800e34ea18be9c3eaca9ae7d30d93f502438f95aad2ed4feab2c53e8a7037`.
- Cumulative 22-file source SHA-256:
  `a66f848c25f05df0cd3f3492bd02c4fabbfe73af5b38589bf2583629c05df3ce`.
- Chapter 3 source QA passed for six files, 27 IDs, 26 xrefs, six
  explorations/activities, 14 exercises, and 47 tasks. Protected mathematics,
  code, attributes, IDs, and xrefs agree except for ledgered deterministic
  repairs and additive accessibility descriptions. The checker explicitly
  reconstructs the three documented schema relocations before comparing
  topology; it does not ignore reordered mathematics or code.
- The cumulative wrapper and each repaired source/companion component validate
  against the pinned PreTeXt 1.7.5 RelaxNG schema. O003-C036 moves the Chapter 2
  restriction definition out of a task introduction; O003-C037 moves the
  absolute-value lemma out of a task statement; O003-C038 moves the open-ball
  definition into the exercises-level introduction. Their IDs, statements,
  mathematics, and pedagogical order are retained.
- Original Chapter 3 companion: 51,131 bytes, SHA-256
  `59866e6c02852e39029dde8a1a2e21b4148b180c7c853894ddfdb9666a2878cb`.
  QA passed all six activity checkpoints, 14 source-exercise guides, eight
  mastery checks, and all 28 hints, answers, and complete solutions, with 117
  unique IDs and 12 resolving xrefs.
- Backend manifest: `backend/chapter_03_companion_manifest.json`, 50,334 bytes,
  SHA-256 `31c7aaa7a3c5041737cdf02a68271eb8f0b71d51e7fc0f3a0346d3c0229cc626`.

## HTML

- Runtime: Python 3.12.13, PreTeXt 1.7.5, setuptools 75.8.0.
- Two clean builds at `SOURCE_DATE_EPOCH=1692057600` produced identical
  finalized manifests.
- Canonical tree SHA-256:
  `bd83625b129eef7a89c6c53a0b4073c39ce3cc76603363295a6a383fb881740c`.
- Manifest file SHA-256:
  `9d99eb804e65888df46568e65013503ab613c395e3056f860ea4969e6e6979fd`.
- Closure: 2,306 files, 2,195 HTML files, 6,784,139 bytes.
- Automated QA checked 6,314 links/assets and 109 images with no failures,
  duplicate IDs, missing local targets/fragments, generated-English denylist
  hits, missing image alternatives, privacy hits, or credential patterns.
- Responsive browser QA passed at 1280 x 900 and 390 x 844 with zero horizontal
  overflow. The desktop reading column is 784 px centered between the 240 px
  TOC and matching right margin; the mobile reading column is 318.22 px and the
  sidebar is hidden. Navigation labels are not clipped.
- The first Chapter 3 checkpoint and its staged `Petunjuk` opened successfully
  and exposed Indonesian hint content. Browser console errors: zero. The only
  six warnings are the known MathJax component-version notices.
- Current caveat: this bounded reader still references remote PreTeXt,
  Runestone, MathJax, font, CSS, and JavaScript hosts. Whole-edition offline
  closure remains a release gate and is not falsely claimed here.

## PDF

- Runtime: MiKTeX 26.5 with XeLaTeX. The strict wrapper uses a clean target and
  rejects TeX errors even when the PreTeXt CLI reports success.
- Two clean strict builds at the fixed epoch produced identical bytes.
- Artifact: `output/chapters01-03-pdf/chapters_01_03_reader.pdf`.
- 428,309 bytes; 73 Letter pages; PDF 1.7; SHA-256
  `0aee368b729a42f75ef8ee85b13e52c275c068087df13498a3776b2abf76f681`.
- Unencrypted, no JavaScript, not tagged. HTML remains the primary accessible
  surface.
- All 73 pages were rendered at 120 dpi and inspected through seven contact
  sheets. The relocated lemma, open-ball definition, Chapter 3 mastery
  equations, diagnostics, exercise solutions, transitions, and index were
  inspected at full size. No clipping, overlap, missing glyph, broken
  mathematics, or bad pagination remains.
- The final LaTeX pass retains one accepted 6.48035 pt overfull box in a
  Chapter 1 answer. It does not clip. Chapter 3 adds no overfull box.

## Rights and release scope

- The translated GVSU spine is handled conservatively as CC BY-NC-SA 3.0.
- Independently authored companions are separately CC BY 4.0.
- The edition is a collection with per-component rights and explicit
  non-endorsement; it has no flattened blanket license.
- Publication must identify this truthfully as a Chapters 1-3 boundary and
  retain the prior Chapters 1-2 PDF as an inherited historical artifact.

## Next cursor

Continue immediately in source order with Chapter 4, Applications of Metric
Spaces: `chap_metric_spaces_apps.ptx`, `sec_met_space_app.ptx`,
`sec_hamming.ptx`, then `sec_levenshtein.ptx`, plus its original staged
self-study companion and modular backend.

## Publication

The GitHub commit, Pages build, public reader inventory, and anonymous
byte-for-byte readback are recorded in `qa/CHAPTER03_PUBLICATION_RECEIPT.md`
after the transaction completes.
