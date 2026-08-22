# Chapters 1-10 cumulative build and QA receipt

Verified: 2026-08-23 (Europe/Berlin)

Boundary: O003/C90 Bahasa Indonesia, complete GVSU Chapters 1-10 through
*Himpunan Tertutup di Ruang Metrik*, together with the separately licensed
original self-study companions for all ten chapters. This is a coherent
incomplete checkpoint of the 20-chapter edition, not a claim that the whole
book or the original O003 completion modules are finished.

## Frozen source and Chapter 10 translation

- Upstream authority remains Steven Schlicker's GVSU *Topology: An
  Inquiry-Based Approach* at commit
  `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
  `7df245934eedb7174d5ff8af18afff5a7abdde78`. The frozen 2,200,204-byte
  archive has SHA-256
  `d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3`.
- Chapter 10 closes exactly over ten source files / 54,463 authority bytes.
  Its raw-concatenated SHA-256 is
  `3551db27ec6801069fe648ac50f782a31321473af794277006aa4c1c209ebcf7`;
  its ordered named-file SHA-256 is
  `36af7661945246c574fe335cfc89acbb3da0ff03888367636ee645e49c88a10b`.
- The translated ten-file chapter totals 58,853 bytes and has ordered
  named-file SHA-256
  `eb900be0f0c1dc8f5f2ec18248612cdc90216eda95105c57387f8fe1868ceb1d`.
  `CHAPTER10_SOURCE_QA.json` is 7,843 bytes / SHA-256
  `fa35e50c7368d7978cc5b987decd745dca326a8df1e52391ea724b7deda4bd9e`;
  it reports status `pass`, no failures, 28 unique IDs, 13 resolving xrefs,
  no missing xref targets and no active Chapter 10 images.
- The cumulative Chapters 1-10 source closure is 66 unique files. Recomputing
  SHA-256 over each ordered filename, one NUL byte and its exact file bytes
  gives
  `b5e333df168a3e13cda4e9b860a707ec9e87700669a6bd6a3aa4796a44025aa8`.
  The cumulative wrapper is 5,872 bytes / SHA-256
  `0429d2322e8c2b3c623a98cede08c2fbcea3b69144b1001e679444c59c916380`.

## Terminology and source-critical repairs

- The Chapter 9 Indonesian field-terminology audit remains controlling.
  Chapter 10 adds the four controlled terms O003-T129 through O003-T132 and
  uses the established forms including `tutupan` and
  `terbuka-tertutup`. The current terminology ledger is 12,779 bytes /
  SHA-256
  `6a7a055dbfe3db7f9542fcb90d5cd714d48a4c812f868ebd50e7dafba7a35510`.
- The source QA admits exactly eight protected-math changes. The cumulative
  correction ledger binds sixteen verified Chapter 10 records, O003-C097
  through O003-C112; it is 42,883 bytes / SHA-256
  `f8521d91d202585583323bcd56a7709804b9036f622057f0ea9bc7620177a03e`.
  Material corrections include using `a_n=1/(n+1)` where `a_1=1` would not
  lie in `(0,1)`, repairing the false printed set identity to
  `A' \cup A^i=A \cup A'`, and correcting point, distance and bound-variable
  notation. Guide 58 uses a direct neighborhood/ball proof rather than a
  circular sequential argument.

## Companion and modular backend

- The Chapter 10 companion covers all 80 assessable source prompts: 43
  exploration/activity or statement-bearing task guides and 37 exercise
  guides. Five statement-less grouping tasks are explicitly excluded from the
  prompt census. Eight additional mastery checks bring the total to 88
  entries.
- Every entry has a statement, staged hint, answer and complete solution:
  exactly 88 of each and 352 bound disclosure surfaces. Chapter 10 introduces
  no companion images and no remote or interactive dependency.
- `CHAPTER10_COMPANION_QA.json` is 172,478 bytes / SHA-256
  `aa96f4236230763c940edb7e55f71d9632ae01bb8fc8f656bc23b76bcb795ff8`
  and reports status `pass` with no failures. The companion wrapper is 1,947
  bytes / SHA-256
  `817dd11edf2aa1c410e336971d9c85673d9ef64030a7ca37e60e2715897f1b72`.
- The stable-ID backend manifest is 288,337 bytes / SHA-256
  `b96b99ab54447ecbeae9b6c6fa965acc47eaf89cb397f8abd09217b3759289ba`.
  It binds all 88 entries, 352 disclosure surfaces, ten unit dependencies,
  four controlled terms and sixteen verified corrections. Its 50,140-byte
  alias table has SHA-256
  `f98766aa368a90a2d6a6af75fa811dde802383014c36a87557348c089ca30b49`.

## Schema and pinned runtime

- The cumulative wrapper passed the official pinned PreTeXt RelaxNG
  validation through
  `pretext devscript source/chapters_01_10_reader.ptx -V`; exit code was zero
  and no diagnostics were emitted.
- The 479-byte validation receipt has SHA-256
  `4c8e4b963fe1009dea8c5d92144162a8530d06fe9e35af89911c2127f054020b`.
  It binds Python 3.12.13, PreTeXt CLI 1.7.5, setuptools 75.8.0, resource
  commit `9bce7e55911fb14e3e6e362bfa78bd6431c38597`, and pinned schema SHA-256
  `fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0`.
  The PDF runtime remains MiKTeX 26.5.

## Deterministic HTML and reader behavior

- Two clean cumulative HTML runs followed by the Indonesian finalizer emitted
  byte-identical 1,394,104-byte file manifests, each with SHA-256
  `399ad3e04e1ef1c31a4092af1948efd2ae982b3d0e1da048c9d763b1b011483e`.
  The canonical tree has 8,501 files, including 8,390 HTML documents, totaling
  21,067,593 bytes. Its canonical tree-manifest SHA-256 is
  `3f816cedb8ff1244a62bc6bca22f70171652c064af8c4b0e7384a9281a4cf91f`;
  the finalizer localized 24,721 nodes or attributes.
- Local HTML QA checked 26,681 links/assets and 37 image references with zero
  failures. Its 919-byte report has SHA-256
  `3f02dd93e44fdd4720389f1a87b9d0b39932c7fd338a4b65137a247a06c485f2`.
- Browser regression covered 1440, 1280, 1024, 768 and 390 CSS-pixel widths.
  The desktop reading measure is centered at 960 px, the intermediate measure
  is 600 px, and mobile content reflows to 318.2222 px. No checked page has
  document-level horizontal overflow or clipping. The pinned commit token on
  the mobile edition note extends into reserved margin space but remains inside
  the viewport.
- Browser interaction on guide 58 and mastery check J.88 proved that the
  statement, hint, answer and solution reveal independently and remain
  readable at desktop and mobile widths. The checked pages use `lang="id-ID"`,
  retain Indonesian navigation chrome, include the exact model-provenance note,
  and emitted no browser-console errors. The 5,261-byte browser receipt has
  SHA-256
  `76d59785583157a4977d901040f4adfab5cda1fd1bcfecf3d747ffee31e2167a`.

## GitHub Pages publication tree

- The bounded `docs/` tree retains deliberate historical entry surfaces and
  earlier PDFs while advancing the primary reader to Chapters 1-10. It has
  8,515 files, including 8,394 HTML documents, totaling 31,108,581 bytes; its
  canonical tree-manifest SHA-256 is
  `e699c2caade96de6a6ad5c62a3a7c2d8ec4fea149b2de9fa1a7d0f4921abdb4e`.
- The detailed 1,396,941-byte file manifest has SHA-256
  `f81f4491dc9bf245702bb2b76349ebcef2a054b70e95975d3252c63f91b27496`.
  The compact 824-byte manifest has SHA-256
  `be9c502c95435cefb7414bc730632a4a4617130ca0387026dc72b3063ff78280`.
  The 1,047-byte Pages-tree QA report has SHA-256
  `0bae5d06c467bc10c0a01c7376c34dc1907b5829f7ee4c2faaab592d1dabedb6`
  and status `pass`; it checked 27,253 links/assets and 37 image references with
  zero failures.
- The primary `docs/` download is byte-identical to the verified PDF build:
  2,146,005 bytes / SHA-256
  `cb1db8bbb88811864f8375eec101826a2ed1db83244ebe6855a91075e1a0101c`.

## Deterministic PDF and visual inspection

- Two clean strict builds used `SOURCE_DATE_EPOCH=1692057600` and the hard
  transcript-error gate. Both emitted the same 2,146,005-byte PDF with SHA-256
  `cb1db8bbb88811864f8375eec101826a2ed1db83244ebe6855a91075e1a0101c`.
  The run receipts are 314 bytes / SHA-256
  `975a4c3b7d239f4f44b11169698f2cee2ae009b8245243db84d2fd93a1ac29ca`
  and 344 bytes / SHA-256
  `05042bff231fd32e6723f871c0fd9183197d7d22fd9834a99568848dfddc4ccc`.
- The PDF has 251 US-Letter pages, no rotation, 25 outline entries and 239
  valid link annotations. Physical pages 1-6 use lowercase Roman labels and
  physical page 7 begins Arabic page 1. The two external lab annotations use
  the portable public HTTPS target; no relative URI remains. The 6,057-byte
  structure receipt has SHA-256
  `6022f2de5180ab6bd8848ab8f4afc49dc573f2dab10423afba6584f20ac9d541`
  and status `pass`.
- Every page was reviewed on sixteen numbered 4-by-4 contact sheets. Physical
  pages 91-102 (Chapter 10), 227-251 (Appendix J and index), and warning or
  long-layout pages 65, 73, 104, 106, 131, 171, 175, 186, 187 and 196 received
  full-page inspection. No clipping, overlap, broken formula, title overflow,
  figure cutoff, transition fault or illegible content was found.
- A 10-pixel edge sweep at 120 dpi found no edge content. The minimum observed
  margins were 115 px left, 82 px right, 79 px top and 77 px bottom. Physical
  page 3 is an intentional blank; sparse pages 102, 103 and 226 arise from
  chapter or appendix boundaries. The maximum non-blocking TeX overfull-box
  warning is 23.83 pt; targeted visual inspection confirms that it does not
  clip. The 3,906-byte visual receipt has SHA-256
  `ee3fff7da66b0ee801f90b8290b6b5bb878e9212a783f096b359a28201bc304f`.

## Rights, provenance, accessibility and open caveats

- The translated GVSU spine remains conservatively CC BY-NC-SA 3.0. The
  independently authored self-study companion remains a separately identified
  CC BY 4.0 component. Figure, software, XSL and font notices remain
  component-specific; the collection is not flattened to one license and no
  endorsement by the source author or institution is claimed.
- `LICENSES.md` is 2,277 bytes / SHA-256
  `408eeec186fd9b34660ea5d6df19df5d0e0da7ae63e8681852ff5eaa7b6fb941`;
  `companion/RIGHTS.md` is 2,181 bytes / SHA-256
  `ef9e9960775b17d187cc655fc73a6f7d76b3d8fe05b9960d3e168ae9fc4fcfe7`.
- The edition note records production assistance exactly as
  `OpenAI Codex gpt-5.6-sol, Ultra` while preserving the source author,
  institution and human-contributor credits.
- HTML remains the primary accessible surface. The PDF is untagged and its
  mathematical fonts have incomplete Unicode extraction maps.
- This boundary contains 10 of 20 source chapters. Chapters 11-20 and the
  separately authored O003 theory-completion modules remain unfinished.
  Whole-edition figure provenance remains a final-release gate, although
  Chapter 10 introduces no active image. Whole-edition offline closure also
  remains open because the cumulative HTML records PreTeXt, Runestone,
  MathJax, font, CDN and rights-host dependencies. These caveats do not block
  the coherent partial checkpoint but must not be hidden by a completeness
  claim.

## Verdict

Chapters 1-10 and their separately licensed self-study companions are admitted
as the current coherent cumulative local reader boundary. Source, protected
mathematics, schema, companion, stable-ID backend, deterministic HTML and PDF,
link/asset, centered responsive reflow, staged disclosures, PDF structure and
all-page visual gates pass. Publication metadata must say truthfully that 10 of
20 GVSU chapters are available. After this boundary is preserved and publicly
read back, production advances to Chapter 11 in source order; the complete
edition remains an active goal.
