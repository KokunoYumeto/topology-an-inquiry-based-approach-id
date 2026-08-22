# Chapters 1-5 reader - admitted build and QA receipt

Date: 2026-08-22 (Europe/Berlin)
Lane: O003/C90, id-ID
Boundary: Chapters 1-5, *Himpunan*, *Fungsi*, *Ruang Metrik*, *Penerapan
Ruang Metrik*, and *Batas Bawah Terbesar*, plus separately licensed
self-study companions

## Result

This cumulative Chapter 5 boundary is admitted for continued edition
production and public preservation. It supersedes the Chapters 1-4 reader as
the current public boundary without claiming that the complete 20-chapter
edition or the original O003 completion modules are finished.

## Source and companion

- Exact cumulative manifest: `qa/CHAPTER05_SOURCE_MANIFEST.json`, 16,115
  bytes, SHA-256
  `46971569bd005290aea45d840da8a331f754268b4d08e0e4b0b36daa8cf0b2e7`.
- Chapter 5 ordered five-file translated-source SHA-256:
  `cc6b2f4ada1f5a567dbd52721ba0bb640f0bee032676956676fde4d171286047`.
- Cumulative 31-file translated-source SHA-256:
  `816eba4aba3beaf2496d94c98922de7b29b05ce96e51930f2f9242ad15216fe2`.
- Chapter 5 source QA passed for 14 IDs, ten resolving xrefs, one
  exploration, two activities, 50 task nodes and 13 exercises. Protected
  mathematics, source order, attributes and IDs agree except for the explicit
  deterministic corrections O003-C044 through O003-C056 and their approved
  topology/markup allowances. The five upstream theorem blocks that were
  invalid inside exercise paragraphs remain intact, in source order, in one
  schema-valid exercises-level introduction; exercise and task order is
  unchanged.
- Source QA: `qa/CHAPTER05_SOURCE_QA.json`, 8,221 bytes, SHA-256
  `432316b45d76d034d9f91558ecd15b4adbb093f0ecc5c71d46678905a216ccb3`.
- Original Chapter 5 companion wrapper: 1,731 bytes, SHA-256
  `ffe13fb15a8a24204d4806c174598b6f05ec1865df7784ffe5963abe3baf3eb2`.
  Its five fragments contain 48 keyed source-prompt guides and six mastery
  checks, with 54 each of staged hints, answers and complete solutions and 222
  unique IDs.
- Companion QA: `qa/CHAPTER05_COMPANION_QA.json`, 14,006 bytes, SHA-256
  `7d3d6cf25fc646162cfcb9d95053cedecc5dad31b623bea25f2fdc337a7f1c92`.
- Backend manifest: `backend/chapter_05_companion_manifest.json`, 80,449
  bytes, SHA-256
  `bb88d9de6b1a13820d6824c0227f27504364d7e6e35ee54b08d5bc622111ca99`;
  stable entry-alias map: 11,399 bytes, SHA-256
  `b43f0a3f2244d44c953446c630b6be73f29e984a59e6bb352e367053a5b1ccbf`.
- The cumulative wrapper and all repaired source/companion components validate
  against the pinned PreTeXt 1.7.5 RelaxNG schema.

## HTML

- Runtime: Python 3.12.13, PreTeXt 1.7.5 and setuptools 75.8.0.
- Two clean builds at `SOURCE_DATE_EPOCH=1692057600` produced identical
  finalized manifests and QA reports.
- Canonical tree SHA-256:
  `5d58d5258c8655e32e47535f3585cb5b631b347ed3794d9729bd7aa30462323d`.
- Manifest file: 564,427 bytes, SHA-256
  `d29d773d4064563191457c9ae36aed97eb1eaab8b1040937361fa1a85245bd0a`.
- Closure: 3,469 files, 3,358 HTML files, 9,432,612 bytes.
- Automated QA checked 10,290 links/assets and 145 images with no failures,
  duplicate IDs, missing local targets/fragments, generated-English denylist
  hits, missing image alternatives, privacy hits or credential patterns.
- Responsive browser QA passed at 1280 x 900 and 390 x 844. With the desktop
  TOC visible, the reading column is 960 px and centered inside the available
  main pane; hiding the TOC keeps it centered. Mobile reflows to 318.22 px
  without horizontal overflow, and the drawer opens and closes without
  widening the page.
- The Chapter 5 page and staged companion disclose the Indonesian
  `Petunjuk`, `Jawaban` and `Solusi` correctly. The duplicate inner hint labels
  found during final QA were removed. Browser console errors: zero. Six
  warnings across three page loads are repetitions of two known MathJax
  component-version notices.
- Browser QA: `qa/CHAPTER05_BROWSER_QA.json`, 4,314 bytes, SHA-256
  `5874a5b0963b1e0e524a42effc160143b89d6569e90277ee6e222b397557e74e`.
- Current caveat: this bounded reader still references remote PreTeXt,
  Runestone, MathJax, font, CSS and JavaScript hosts. Whole-edition offline
  closure remains a release gate and is not falsely claimed here.

## PDF

- Runtime: MiKTeX 26.5 with XeLaTeX. The strict wrapper cleans the target and
  rejects hidden TeX failures even when the PreTeXt CLI reports success.
- Two clean strict fixed-epoch builds produced identical bytes.
- Artifact: `output/chapters01-05-pdf/chapters_01_05_reader.pdf`.
- 601,566 bytes; 108 US Letter pages; PDF 1.7; SHA-256
  `db4d7d2e39837f43595719ddc371a05052eb7c12849f8d49421e10ad5b7f8126`.
- Unencrypted, no JavaScript, not tagged. HTML remains the primary accessible
  surface.
- All 108 pages were rendered at 100 dpi and inspected through seven contact
  sheets. Pages 49, 50, 53, 89, 93-96, 101 and 107 were also inspected
  full-size, including the Chapter 5 appendix transition, staged disclosures,
  long equations and final mastery page. No clipping, overlap, missing glyph,
  broken equation, page-transition, header/footer or margin defect remains.
- The final TeX pass has no fatal, undefined-reference or LaTeX-warning
  diagnostics. One nonblocking underfull box and the same three inherited
  overfull diagnostics from Chapters 1 and 4 remain; their final pixels are
  contained and readable. Chapter 5 adds no overfull diagnostic after its two
  long equations were reflowed.
- PDF visual QA: `qa/CHAPTER05_PDF_VISUAL_QA.json`, 6,988 bytes, SHA-256
  `08c2f7c641cc43d11e583900ad1c6b82dc057f5884cdee45faeee76435c1fae8`.

## Rights and release scope

- The translated GVSU spine is handled conservatively as CC BY-NC-SA 3.0.
- Independently authored companions are separately CC BY 4.0.
- The edition is a collection with per-component rights and explicit
  non-endorsement; it has no flattened blanket license.
- Publication must identify this truthfully as a Chapters 1-5 boundary and
  retain the prior Chapters 1-2, Chapters 1-3 and Chapters 1-4 PDFs as
  historical artifacts.

## Next cursor

After publication and anonymous byte readback, freeze the exact Chapter 6
authority closure and continue immediately in source order with its natural
id-ID translation, original staged self-study companion and modular backend.

## Publication

The GitHub commit, Pages deployment, public reader inventory and anonymous
byte-for-byte readback are recorded in `qa/CHAPTER05_PUBLICATION_RECEIPT.md`
after the transaction completes.
