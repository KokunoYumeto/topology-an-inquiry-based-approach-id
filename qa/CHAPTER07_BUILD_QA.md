# Chapters 1-7 reader - admitted build and QA receipt

Date: 2026-08-22 (Europe/Berlin)  
Lane: O003/C90, id-ID  
Boundary: Chapters 1-7 through *Bola Terbuka dan Lingkungan pada Ruang
Metrik*, plus separately licensed self-study companions and the original
epsilon-delta lab

## Result

This cumulative Chapter 7 boundary is admitted for continued edition
production and public preservation. It supersedes Chapters 1-6 as the current
local release boundary without claiming that the complete 20-chapter edition
or the original O003 completion modules are finished.

## Source, corrections, companion, and backend

- Exact cumulative manifest: `qa/CHAPTER07_SOURCE_MANIFEST.json`, 36,095
  bytes, SHA-256
  `4771f640ee8d1c2ed57e8a528dcfead233fab05e5067b7853c3dceb59feffe71`.
- Chapter 7 authority is the six-file, 29,354-byte closure at frozen GVSU
  commit `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`; its ordered raw-byte
  SHA-256 is
  `dae2379760505e1725c51af0d8f7a6471ee648084d51ef9a3877777b30334c95`.
- Chapter 7 translated-source SHA-256 is
  `a749530fc95cbc4dc834e337039346b8756908c68eee4658e267c320769a9211`.
  The cumulative 43-file translated-source SHA-256 is
  `563d08458f3ce9457870e4865f49c5df433be77b768db2edc0a62039ff08b23e`.
- Source QA passed for all six files, 14 IDs, 11 resolving xrefs, four
  exploration/activity containers, 34 task containers after the recorded
  malformed-shell split, 11 exercise containers, and 40 actual learner
  prompts. Protected source order, IDs, attributes, and mathematics agree
  except for the seven explicit O003-C066 through O003-C072 corrections and
  their narrow recorded markup allowances. Both active figures have faithful
  Indonesian descriptions. Source QA: `qa/CHAPTER07_SOURCE_QA.json`, 5,315
  bytes, SHA-256
  `c201a0b9527670af514105c760a57b1daca963a10361816c3e575056921f7f9f`.
- The original Chapter 7 companion has keyed staged support for all 40 source
  prompts and six mastery checks. All 46 entries have exactly one statement,
  hint, answer, and complete solution. Independent mathematical review checked
  the 24 end-exercise solutions, including graph shortest-path thresholds,
  strict open-ball inequalities, inverse images, and finite-intersection
  quantifiers. Companion QA: `qa/CHAPTER07_COMPANION_QA.json`, 95,590 bytes,
  SHA-256
  `4cd1a5f624147c960c8599a2523bb3114f07af7caf75eb107208efe631a247ed`.
- Backend manifest: `backend/chapter_07_companion_manifest.json`, 154,945
  bytes, SHA-256
  `899e106d8a8e94d786ec44e9a313cf3968fde14585c7e1591afda5dc514abcdb`;
  stable entry-alias map: 25,464 bytes, SHA-256
  `082cdcee30f3c42a9a85d4b83d0d527b43f90a11c944d95a5152af71b149123d`.
- The cumulative wrapper and all included source and companion components pass
  the pinned PreTeXt 1.7.5 RelaxNG validation.

## HTML

- Runtime: Python 3.12.13, PreTeXt 1.7.5, setuptools 75.8.0.
- Two clean fixed-epoch builds produced identical finalized manifests. The
  canonical tree SHA-256 is
  `7ce7e3a6869794d7573c50bfd2d9c4abe1c20ab0150f813c10a9659a4ad08ae8`.
- Canonical manifest: 835,730 bytes, SHA-256
  `9c3e3cf8e0ff0eec1ea263bac4f3586efcba95544818827fbb66bc95b1831cf8`.
  Closure: 5,093 files, 4,982 HTML documents, 13,161,675 bytes.
- Automated QA checked 13,625 local links, fragments, knowls and assets and
  200 images with no failures. All 4,982 documents have `lang=id-ID` and
  localized chrome; both Chapter 7 image assets and descriptions resolve.
- Responsive browser QA passed at 1280 x 900 and 390 x 844. The desktop
  reading column is 960 px and centered in the available main pane. The mobile
  reading column reflows to 318.22 px without horizontal overflow; the 240 px
  contents drawer opens correctly. A source-guide entry and its hint opened
  independently, with `Petunjuk`, `Jawaban`, and `Solusi` controls present.
  Browser QA records the served origin, capture times, in-app browser identity,
  exact desktop/mobile measurements, zero console errors, and three retained
  hashed screenshots: `qa/CHAPTER07_BROWSER_QA.json`, 3,692 bytes, SHA-256
  `3cd0c8e8720d486b5ac45485b22daffc22745fe531fc2d376340e51481cfd2f6`.
- Current caveat: the bounded reader still references nine remote runtime host
  families from PreTeXt, Runestone, MathJax, fonts, CSS, JavaScript, and
  license links. Complete-edition offline closure remains open and is not
  claimed.

## PDF

- Runtime: MiKTeX 26.5 with XeLaTeX. The strict wrapper cleans the target,
  rejects hidden TeX failures, and deterministically normalizes and reopens
  the embedded PDF page-label tree.
- Two clean fixed-epoch strict builds produced identical bytes.
- Artifact: `output/chapters01-07-pdf/chapters_01_07_reader.pdf`.
- 1,357,233 bytes; 156 US Letter pages; PDF 1.7; SHA-256
  `b6ab4ee95e91b96e4605574c1703107484d49b8698c8a6070c4cc88a44209ebc`.
- Unencrypted, no JavaScript or forms, and not tagged. HTML remains the primary
  accessible surface. Metadata retains the Indonesian title and fixed source
  date.
- Embedded viewer labels agree with print: physical pages 1-7 are `i` through
  `vi`, then `1`; Chapter 7 on physical page 65 is label `59`; Appendix G on
  physical page 141 is `135`; and the index on physical page 156 is `150`.
  Four top-level outline entries, seven chapter children under the main part,
  and all 177 annotations survive normalization. Both epsilon-delta lab
  annotations are rewritten exactly from the HTML-relative path to the
  canonical public HTTPS target; no relative PDF URI remains, and the exact
  target is present in the staged Pages tree.
- All 156 pages were rendered at 100 dpi and inspected through eight contact
  sheets. Thirteen Chapter 7, figure, sparse-tail, Appendix G, mastery, and
  index pages were also inspected full-size. The URI-repaired PDF was rendered
  again; all 156 page PNGs are pixel-identical to the pre-repair render. The
  retained render manifest is 29,116 bytes / SHA-256
  `3f389ac448c92c50e3b3895c11c04027d61738e7f733dba2329803b53acb402c`;
  the eight-sheet manifest is 1,938 bytes / SHA-256
  `c4c85d160964850053ee616ada776ab978583ec0231db42640d7b16e3e1f7643`.
  No clipping, overlap, missing glyph, broken equation, transition,
  header/footer, margin, or page-label defect remains.
- The final TeX pass has no fatal, undefined-reference, missing-glyph, or LaTeX
  warning. Two Chapter 7 box diagnostics and four inherited diagnostics are
  visually contained. Both run receipts were captured immediately with their
  build-log identities. PDF visual QA: `qa/CHAPTER07_PDF_VISUAL_QA.json`, 8,387
  bytes, SHA-256
  `c0ec5216f48b5a8dc4d25839b9693eca3dc8a04b93f155b1951704f4317deef6`.

## Rights and release scope

- The translated GVSU spine is handled conservatively as CC BY-NC-SA 3.0.
- Independently authored companions and the epsilon-delta lab are separate CC
  BY 4.0 components.
- The edition is a collection with per-component rights and explicit
  non-endorsement; it has no flattened blanket license.
- Release must identify this truthfully as a Chapters 1-7 boundary and retain
  the Chapters 1-2 through Chapters 1-6 PDFs as historical artifacts.

## Next cursor

Freeze Chapter 8, *Open Sets in Metric Spaces*, at the same upstream commit and
continue immediately in source order with its natural id-ID translation,
original staged self-study companion, and modular backend.

## Publication

The GitHub content commit, Pages deployment, public reader inventory, and
anonymous byte-for-byte readback belong in
`qa/CHAPTER07_PUBLICATION_RECEIPT.md` only after the transaction succeeds. A
rejected push is not publication and must instead remain in the durable lane
controls.
