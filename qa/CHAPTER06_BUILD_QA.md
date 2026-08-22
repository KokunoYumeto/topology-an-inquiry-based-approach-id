# Chapters 1-6 reader - admitted build and QA receipt

Date: 2026-08-22 (Europe/Berlin)
Lane: O003/C90, id-ID
Boundary: Chapters 1-6 through *Fungsi Kontinu di Ruang Metrik*, plus
separately licensed self-study companions and the original epsilon-delta lab

## Result

This cumulative Chapter 6 boundary is admitted for continued edition
production and public preservation. It supersedes Chapters 1-5 as the current
reader boundary without claiming that the complete 20-chapter edition or the
original O003 completion modules are finished.

## Source, corrections, and companion

- Exact cumulative manifest: `qa/CHAPTER06_SOURCE_MANIFEST.json`, 32,105
  bytes, SHA-256
  `f6e8b1c1f331c7bb8c895ee082cd25db08c349bc60ad381b2842a4b7f9f10e44`.
- Chapter 6 authority is the six-file, 33,845-byte closure at frozen GVSU
  commit `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`; its ordered authority
  SHA-256 is
  `6872eac9f833addfc84b711f5d1509ec00116db884ca509dc73f8f2763bd581a`.
- Chapter 6 translated-source SHA-256:
  `c59c311c2017cde74375e6866bbe84d96203b21d2244ca6694aaafac5fa7027f`.
  The cumulative 37-file translated-source SHA-256 is
  `7e39e95d3a276468a707f3dfc050fd75fe695a6187317ea5fec20da9c805083c`.
- Source QA passed for all six files, 13 IDs, nine resolving xrefs, two focus
  questions, one exploration, three activities, 39 real learner prompts, 14
  exercise containers, two described figures, and both local-lab links.
  Protected source order, IDs, attributes, and mathematics agree except for
  the explicit O003-C057 through O003-C065 corrections and their narrow
  recorded markup allowances. Source QA: `qa/CHAPTER06_SOURCE_QA.json`, 6,865
  bytes, SHA-256
  `1718330ae81f98b81c7d49b15df246f64c4af5b8438150a0c05dabf28f0bad45`.
- The original Chapter 6 companion has 39 source-prompt guides and six mastery
  checks. All 45 entries have exactly one statement, staged hint, answer, and
  complete solution. Companion QA: `qa/CHAPTER06_COMPANION_QA.json`, 83,051
  bytes, SHA-256
  `4460a8ae879c41a22eb0e874e373029a9caae1a24fd0a46aa1f6d45065378703`.
- Backend manifest: `backend/chapter_06_companion_manifest.json`, 153,969
  bytes, SHA-256
  `7053ce880a2105db4e6daee1525b7cf2ede424998cbdbd954f2d9449873517fb`;
  stable entry-alias map: 22,994 bytes, SHA-256
  `9f52fbb27b9ebfa61645ae8a0e46f8d92c71442cc903df6f9d1b3b87a9837fb3`.
- The independently authored `f(x)=x sin(x)` epsilon-delta lab is
  dependency-free, keyboard-operable, responsive, sample-count transparent,
  and locally integrated where the frozen source depended on an unarchived
  GeoGebra object. Source identity: 21,114 bytes, SHA-256
  `e5e9c94004b66d7862a51d94d15361ac5b2069657016eff5a76290c22478e07a`.
- The cumulative wrapper and repaired source/companion components validate
  against the pinned PreTeXt 1.7.5 RelaxNG schema.

## HTML

- Runtime: Python 3.12.13, PreTeXt 1.7.5 and setuptools 75.8.0.
- Two clean fixed-epoch builds produced byte-identical finalized run manifests
  with SHA-256
  `0497fd4bfc4e0a5691d0be4f99f8cc80f21ad0090beb5f4db24e1ec9288eef3b`.
- Canonical tree SHA-256:
  `f11eab132e28379fdb8c32625c4fd0bb9119d455cfc8cbda2e1728e38e220f00`.
- Canonical manifest: 704,431 bytes, SHA-256
  `3227cd9d3cfc89d389e73dc51a976011dcee92a64adc0d5eec63242a39c6c375`.
  Closure: 4,313 files, 4,202 HTML files, 11,321,611 bytes.
- Automated QA checked 13,195 links/assets and 171 images with no failures.
  All 4,202 documents have `lang=id-ID` and localized chrome; both Chapter 6
  lab links and all four paired continuity image assets resolve. The finalizer
  is idempotent.
- Responsive browser QA passed at 1280 x 900 and 390 x 844. The desktop reading
  column is 960 px and centered inside the available main pane with or without
  the 240 px table of contents; mobile reflows to 318.22 px without horizontal
  overflow, and its drawer opens and closes correctly.
- Chapter 6 figures have distinct Indonesian descriptions. The companion
  disclosures open independently with `Petunjuk`, `Jawaban`, and `Solusi`.
  The lab passed and failed the intended numerical presets, tightened delta
  correctly, displayed 2,001 sample points and its limitation, and produced no
  browser-console error or warning. Browser QA:
  `qa/CHAPTER06_BROWSER_QA.json`, 3,614 bytes, SHA-256
  `36e0635a22126d9a907efa6e35cd0fe80a8396ffc707c9a4f655bb7f7708ec5b`.
- Current caveat: the bounded reader still references nine remote runtime host
  families from PreTeXt, Runestone, MathJax, fonts, CSS, JavaScript, and license
  links. Complete-edition offline closure remains open and is not claimed.

## PDF

- Runtime: MiKTeX 26.5 with XeLaTeX. The strict wrapper cleans the target,
  rejects hidden TeX failures, and deterministically normalizes and reopens the
  embedded PDF page-label tree.
- Two clean fixed-epoch strict builds produced identical bytes.
- Artifact: `output/chapters01-06-pdf/chapters_01_06_reader.pdf`.
- 1,102,652 bytes; 133 US Letter pages; PDF 1.7; SHA-256
  `5085c7d8f29d97c993b663288856f34683c2a6a1c5e19f8620befb3e08c61eaf`.
- Unencrypted, no JavaScript or forms, and not tagged. HTML remains the primary
  accessible surface. Metadata retains the Indonesian title, LaTeX creator,
  MiKTeX producer, and fixed source date.
- Embedded viewer labels now agree with print: physical pages 1-7 are
  `i, ii, iii, iv, v, vi, 1`; Chapter 6 on physical page 56 is label 50;
  Appendix F on physical page 117 is label 111; and the index on physical page
  133 is label 127. Seven top-level outline entries, 161 annotations, and two
  local-lab URI links survive the metadata normalization.
- All 133 pages were rendered at 100 dpi and inspected through seven contact
  sheets. Twenty-two transition, figure, equation, lab-link, sparse-tail,
  Appendix F, mastery, and index pages were also inspected full-size. No
  clipping, overlap, missing glyph, broken equation, transition, header/footer,
  margin, or page-label defect remains.
- A fresh render of the final normalized PDF matches all 133 inspected page
  PNG hashes and all seven contact-sheet hashes from the pre-normalization
  artifact, proving the catalog correction did not alter visible content.
- The final TeX pass has no fatal, undefined-reference, missing-glyph, or LaTeX
  warning. One inherited underfull and three inherited overfull diagnostics
  remain visually contained. Chapter 6 adds none.
- PDF visual QA: `qa/CHAPTER06_PDF_VISUAL_QA.json`, 8,756 bytes, SHA-256
  `2badd4b9f89cb0b13cc10d061d419eb0ab528e1344a1ebd643f97ae2cb8679b3`.

## Rights and release scope

- The translated GVSU spine is handled conservatively as CC BY-NC-SA 3.0.
- Independently authored companions and the epsilon-delta lab are separate
  CC BY 4.0 components.
- The edition is a collection with per-component rights and explicit
  non-endorsement; it has no flattened blanket license.
- Publication must identify this truthfully as a Chapters 1-6 boundary and
  retain the Chapters 1-2 through Chapters 1-5 PDFs as historical artifacts.

## Next cursor

After publication and anonymous byte readback, freeze the exact Chapter 7
authority closure and continue immediately in source order with its natural
id-ID translation, original staged self-study companion, and modular backend.

## Publication

The GitHub content commit, Pages deployment, public reader inventory, and
anonymous byte-for-byte readback are recorded in
`qa/CHAPTER06_PUBLICATION_RECEIPT.md` after the transaction completes.
