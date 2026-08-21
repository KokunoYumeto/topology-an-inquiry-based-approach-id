# Chapter 1 reader — admitted build and QA receipt

> Historical receipt. The exact standalone hashes below describe the original
> Chapter 1 admission. After a terminology-only normalization and the
> companion-rights clarification, current Chapter 1 hashes and artifacts are
> controlled by \`CHAPTER02_SOURCE_MANIFEST.json\` and
> \`CHAPTER02_BUILD_QA.md\`.

Date: 2026-08-21 (Europe/Berlin)  
Lane: O003/C90, id-ID  
Boundary: Chapter 1, “Himpunan,” plus the separately identified self-study companion

## Result

The Chapter 1 boundary is admitted for continued edition production. The
standalone PreTeXt wrapper passed schema validation, deterministic HTML and PDF
builds, structural/source comparison, local link and asset checks, responsive
browser inspection, companion-disclosure testing, and bounded PDF visual QA.
This is not a claim that the untranslated whole-book `main.ptx` is already a
valid Indonesian reader or that the complete edition is finished.

## Source and structure

- Exact translated-source manifest: `CHAPTER01_SOURCE_MANIFEST.json`.
- Eight-file combined SHA-256: `b9ae4219f796c99c9ddd3ebc738666bc61122fc205ab0ae43ee0584843ffc333`.
- Upstream IDs, xref order, and image-source order match the pinned authority.
- Expected deltas only: one malformed literal `\\item` became a fourth task;
  six active Venn images gained Indonesian descriptions; a missing-font star
  became semantic math `\\star`; 16 `\\text{...}` fragments inside otherwise
  preserved mathematics were localized.
- Companion checks: 97 unique XML IDs, no duplicates; 7 activity checkpoints,
  10 source-exercise guides, 6 mastery checks, and 23 each of hints, answers,
  and solutions. Its JSON/CSV/XML entry sets and all 69 reveal references agree.

## HTML

- Toolchain: pinned local PreTeXt CLI 1.7.5.
- Both clean runs report `PreTeXt source passed schema validation`.
- Two independently finalized runs produced the same canonical manifest:
  `4c77676c884c98073cae5d2b4cf85361fa01a9354e3a314f7700cbf18bf5fad1`.
- Manifest file SHA-256 on both runs:
  `a6319db5af80ed5a99e5e0295a9261d5c7bc37d7abee2f628254c7a9e14f6b09`.
- Closure: 769 files, 658 HTML files, 3,546,395 bytes.
- Automated QA: 1,908 links/assets and 50 images checked; `lang=id-ID`;
  no duplicate IDs, missing local targets/fragments, missing alt attributes,
  generated-English denylist hits, privacy/secret hits, or other failures.
- The build still references these network hosts: `cdn.jsdelivr.net`,
  `cdnjs.cloudflare.com`, `fonts.cdnfonts.com`, `fonts.googleapis.com`,
  `fonts.gstatic.com`, `pretextbook.org`, `runestone.academy`, and
  `www.mathjax.org`. Whole-edition release therefore still requires the planned
  offline/vendor decision. Network widgets and audio were not exercised because
  this boundary contains neither; the companion's local knowl disclosure was.
- The CLI's online Runestone version announcement changed from 8.2.6 to 8.2.7
  between the two runs, but the finalized reader bytes remained identical.

## Responsive browser QA

- Desktop, 1440 x 900: page and navigation width 1,424.9 px after scrollbar;
  open-TOC reading column 944 px at x=240.9, centered in the page; document
  scroll width 1,425 px, so no horizontal overflow.
- Desktop with TOC collapsed: main width 1,424.9 px; reading column 960 px at
  x=232.9, centered; no horizontal overflow.
- Mobile, 390 x 844: sidebar hidden by the stock compact layout; reading column
  318.2 px at x=28.9; document scroll width 375 px; no horizontal overflow.
- Companion at 1,280 px: 784 px centered reading column. A visible `Petunjuk`
  control opened one Indonesian knowl panel successfully.
- All six Venn images loaded with detailed id-ID alternatives. Browser console
  showed only MathJax's component-version warnings, not application errors.

## PDF

- Fixed `SOURCE_DATE_EPOCH=1692057600`; two builds produced identical bytes.
- Artifact: `output/chapter01-pdf/chapter_01_reader.pdf`.
- Size/SHA-256: 162,290 bytes;
  `b82f6b8ba4c2502c6e943e5b9919ce61fa40e243cc7f89ee6f500a3463b65e09`.
- 25 pages, Letter, PDF 1.7, unencrypted, no JavaScript. The PDF is not tagged;
  accessible HTML remains the primary reader surface.
- All 25 pages were rendered and inspected. Contact sheet SHA-256:
  `649ba0a8930041b8dd323a485a4e4de9c158b35e4533c486072adca6b09624ab`.
  The semantic star (page 7), set-difference symbols (including page 10), long
  companion heading (page 18), Venn figures, and final pages render without
  clipping or mojibake.
- The final LaTeX pass has three accepted overfull boxes (11.15 pt, 9.82 pt,
  6.48 pt); visual inspection confirms none clips. First internal LaTeX passes
  report temporary undefined references; the final passes resolve them.

## Next cursor

Continue in source order with Chapter 2, “Fungsi”: first
`chap_functions.ptx` and `sec_func_intro.ptx`, then the remaining five sections
and the 17-exercise closure. Do not treat this admitted unit as evidence that
the complete edition or curriculum-selection decision is complete.
