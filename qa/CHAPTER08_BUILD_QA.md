# Chapters 1-8 reader — admitted build and QA receipt

Date: 2026-08-22 (Europe/Berlin)  
Lane: O003/C90, id-ID  
Boundary: Chapters 1-8 through *Himpunan Terbuka dalam Ruang Metrik*, plus
separately licensed self-study companions and the original epsilon-delta lab

## Result

This cumulative Chapters 1-8 boundary is locally admitted for continued
edition production and public preservation. It supersedes Chapters 1-7 as the
current verified local boundary without claiming that the complete 20-chapter
edition or the original O003 completion modules are finished. GitHub write
access remains externally blocked by the account suspension; that does not
reduce the validity of this build and does not block preservation on Zenodo.

## Source, corrections, companion, and backend

- Exact cumulative manifest: `qa/CHAPTER08_SOURCE_MANIFEST.json`, 44,745
  bytes, SHA-256
  `5a324f70f61d6e52b69ce9b1245ded596c171b769155b1145330b311580e061d`.
- Chapter 8 authority is the eight-file, 36,417-byte closure at frozen GVSU
  commit `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`; its ordered raw-byte
  SHA-256 is
  `22ea6d5e193fd6b209ecfb7fe36233a3fa3a94e8630dc907f390efd137faef3f`.
- Chapter 8 translated-source SHA-256 is
  `9a501aeada00c51dbc5cee7ffe2bc1ebff31f134477ee08d9cbd7992e7f59463`.
  The cumulative 51-file translated-source SHA-256 is
  `86ce07735dc03b1e732ab6c2eae0e0896c45f5f73b548b95969822b723723933`.
- Source QA passes for all eight files, 17 IDs, 18 resolving xrefs and 55
  assessable prompts. Source order, XML topology, identifiers, attributes,
  cross-references and protected mathematics agree with authority except for
  the explicit `O003-C073` through `O003-C081` ledger entries. The deterministic
  `O003-C076` repair changes the undefined complement
  `R^2 \setminus A` to `R^2 \setminus S`. `O003-C078` (the dangling “Use
  Theorem” reference) and `O003-C079` (the source calling an arbitrary affine
  map linear) remain explicitly unresolved rather than guessed. Source QA:
  `qa/CHAPTER08_SOURCE_QA.json`, 5,381 bytes, SHA-256
  `e67e0df464c41538fd37b8822a6a8e59eee78373a6b0c619aa31b5a9803d9ceb`.
- The original Chapter 8 companion gives keyed staged support for all 55 source
  prompts plus six mastery checks. All 61 entries have one statement, hint,
  answer and complete solution or rubric. Companion QA:
  `qa/CHAPTER08_COMPANION_QA.json`, 119,557 bytes, SHA-256
  `b3333009e3d868003f15b79e5f668c963476b4a25f1b25af6239514083fe4c71`.
- Backend manifest: `backend/chapter_08_companion_manifest.json`, 199,693
  bytes, SHA-256
  `6ad0a0440d6bb1efa6d1be91198373f7494683dfd701adb064f7dce3d441a80e`;
  stable entry-alias map: 33,079 bytes, SHA-256
  `104d7f807f449c94ba4d12911d5928f75f2c9c0627c4af363750894d438a6157`.
- The cumulative wrapper and all included source and companion components pass
  the pinned PreTeXt 1.7.5 RelaxNG validation. A first strict PDF attempt
  correctly rejected the missing wrapper macro `\Int`; adding
  `\newcommand{\Int}{\text{Int}}` closed the standalone reader wrapper without
  modifying upstream mathematical prose. The rejected transcript remains local
  and is not part of the publication package.

## HTML

- Runtime: Python 3.12.13, PreTeXt 1.7.5, setuptools 75.8.0.
- Two clean fixed-epoch builds produced identical finalized manifests. The
  canonical tree SHA-256 is
  `5877bcaf7c08baf2d56e58a36fe9097af3b902f2315f86e667f82dd3118dbdab`.
- Canonical manifest: 1,012,099 bytes, SHA-256
  `f88d5719051037a0bc02132b34663051012315e1677a381d14c9fca440f03fc7`.
  Closure: 6,172 files, including 6,061 HTML documents, and 15,657,116 bytes.
- Automated QA checked 20,420 local links, fragments, knowls and assets and 226
  images with no failures. All documents use `lang=id-ID` and localized chrome.
  Chapter 8 introduces no new figures or remote interactive surfaces.
- Responsive browser QA passes at 1280 x 900 and 390 x 844. The desktop reading
  column is 960 CSS px and centered in the available pane; the mobile column
  reflows to 318.22 CSS px with no horizontal overflow, and the 240 CSS px
  contents drawer opens correctly. A source-guide entry and its `Petunjuk`
  disclosure open independently, with `Jawaban` and `Solusi` controls present.
  The restored `\Int` macro renders correctly on the interior page. Browser QA:
  `qa/CHAPTER08_BROWSER_QA.json`, 4,375 bytes, SHA-256
  `6d60d92b2fe904d4bca542b4ca0102fdb03413a797e5f41fbe04a4e9ca42906b`.
- Current caveat: the bounded HTML reader records nine remote runtime host
  families from PreTeXt, Runestone, MathJax, fonts, CSS, JavaScript and license
  links. Complete-edition offline closure remains open and is not claimed.

## PDF

- Runtime: MiKTeX 26.5 with XeLaTeX, PyPDF2 2.5.0 and Poppler 24.04.0.
- Two clean fixed-epoch strict builds produced byte-identical PDFs after page
  label normalization and exact rewriting of the two relative epsilon-delta
  lab annotations to the canonical HTTPS target.
- Artifact: `output/chapters01-08-pdf/chapters_01_08_reader.pdf`.
- 1,653,047 bytes; 187 US Letter pages; PDF 1.7; SHA-256
  `78c076c58839dfd1a18cca663e58accdee2a391e429d5f38e6c71ac3c3e7937d`.
- The file is unencrypted, has no JavaScript, forms, widgets or attachments,
  and is not tagged. Its title metadata is Indonesian and its creation date is
  fixed to the frozen source date.
- The page-label tree maps physical pages 1–6 to Roman `i`–`vi` and physical
  page 7 onward to Arabic 1–181. The outline has 21 destinations: four
  top-level entries, eight chapter entries and eight appendix entries plus the
  remaining hierarchy. All 200 links are valid: 198 internal destinations and
  two canonical HTTPS lab links; no relative URI remains.
- All 187 pages were rendered at 100 dpi and inspected through 16 contact
  sheets. Full-size checks covered the cover/front matter, every chapter and
  appendix transition, Chapter 8 start, representative definitions,
  activities and exercises, dense companion pages, warning locations and the
  index. Every final overfull/underfull diagnostic is visually contained; no
  clipping, overlap, missing glyph, broken equation, margin, header/footer or
  pagination defect remains. Render manifest: 34,819 bytes, SHA-256
  `9e543b4571cf9f8ff0c76db4313be894c15fedb6ae4ce214922963c5d9c31d04`;
  contact-sheet manifest: 3,444 bytes, SHA-256
  `156c5eddcba7bbb35588d98d0718c3e172059178814acfb4bfc5172bdeb62757`.
- The final XeLaTeX pass has no TeX/package errors, undefined or multiply
  defined references, missing glyph warnings or LaTeX warnings. Structural QA:
  `qa/CHAPTER08_PDF_STRUCTURE.json`, 5,362 bytes, SHA-256
  `175f6916b30d9b1da6649b29a922a28d1ed44f97ba47850bbe6f1cf8b0ef37dc`;
  visual QA: `qa/CHAPTER08_PDF_VISUAL_QA.json`, 16,264 bytes, SHA-256
  `ea8132092df59ebdb157bcf898bb8c88b26c1f3ecc081e3ef50d6901ea1020cf`.
- Accessibility caveat: Poppler extraction has no U+FFFD, NUL or literal CID
  markers, but yields 84 C0 control characters in mathematical expressions;
  15 of 37 font-resource rows lack Unicode maps. PyPDF2 extraction is worse.
  The visible PDF passes visual QA, but HTML remains the primary accessible and
  reliably extractable surface.

## Rights and preservation scope

- The translated GVSU instructional text is handled conservatively as CC
  BY-NC-SA 3.0.
- Independently authored companions and the epsilon-delta lab are separate CC
  BY 4.0 components.
- Software, XSLT, fonts, figures and separately noticed assets retain their own
  notices. This is a collection with multiple native rights entries, not a
  flattened blanket license.
- Zenodo record `22059895`, reserved DOI `10.5281/zenodo.22059895`, is the
  preservation destination for this incomplete 8-of-20 boundary. Publication
  and anonymous byte readback are recorded separately after the transaction.

## Next cursor

After the Zenodo preservation transaction and local Git commit, freeze Chapter
9 from the same upstream authority and continue immediately in source order.
The GitHub Chapters 1-8 push and anonymous Pages/raw readback remain queued
unchanged until account write access is restored.
