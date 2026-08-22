# Chapters 1-9 cumulative build and QA receipt

Verified: 2026-08-22 (Europe/Berlin)

Boundary: O003/C90 Bahasa Indonesia, complete GVSU Chapters 1-9 through
*Barisan di Ruang Metrik*, together with the separately licensed original
self-study companions for all nine chapters. This is a coherent incomplete
checkpoint of the 20-chapter edition, not a claim that the whole book or the
original O003 completion modules are finished.

## Frozen source and Chapter 9 translation

- Upstream authority remains GVSU commit
  `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
  `7df245934eedb7174d5ff8af18afff5a7abdde78`.
- Chapter 9 closes exactly over five source files / 34,075 authority bytes,
  with raw ordered SHA-256
  `c6d2935beda94460617eeba29cf6bd181fd7d061bbd11ed6b8471b91d614cce9`.
- The complete translated five-file chapter has ordered SHA-256
  `16508d2363ba205c28b5187b7909d577a1fd482c49414ca7d05572ca77125c73`.
  `CHAPTER09_SOURCE_QA.json` is 5,719 bytes / SHA-256
  `95218a80b9b8ca1bf1e2ba90e42b2e15e4aa91231ef636abd2b887c48cad7aa3`
  and reports zero failures, 11 unique IDs and 12 resolving xrefs.
- The cumulative Chapters 1-9 source closure is 56 files. Its deterministic
  named-file SHA-256 is
  `583966ac3c2f46208b1423db42e46ce6ed51cc039790fcde758916ccb7626a63`.
- `CHAPTER09_SOURCE_MANIFEST.json` is 60,728 bytes / SHA-256
  `a731db7e0a89f68a638208055997f5f51a167dd2a552f7ff69d3a3208527480d`.
  It fails closed over the exact cumulative source, companion, rights, assets,
  corrections, backend, HTML, browser and PDF identities and has status
  `pass` with no pending evidence.

## Indonesian terminology audit

- A bounded official arXiv search found no Indonesian point-set-topology
  source package under the exact phrases `ruang metrik`, `ruang topologi`,
  or `himpunan terbuka`; the permitted PDF fallback was therefore used.
- The primary witness is Oki Neswan's 2019 FMIPA-ITB teaching deck
  *Dari Barisan Bilangan ke Barisan Fungsi* (723,813 bytes; SHA-256
  `636b5110a6ac6fece61f75bb4a3c04206734b4806e5335df21c096b8cbe9fdee`),
  corroborated by Universitas Terbuka's PEMA4427 topology overview
  (96,422 bytes; SHA-256
  `3271d0016f0386079f53202021b0f717b1c87103d469edcb4a3c5f755474fcbc`).
- The actual PDF bodies support the edition forms `ruang topologi`,
  `tutupan`, `kekontinuan`, `pertidaksamaan segitiga`, and `unsur`.
  The controlled glossary was updated, the justified refinements were
  propagated through Chapters 1-9, and stale variants were checked away.
- `00_control/CHAPTER09_TERMINOLOGY_AUDIT.md` is 5,307 bytes / SHA-256
  `9ece56964e47cb36dc0528aa3899e2d90a860de3d6b58ab1f92ad0a370ff8036`;
  the cumulative manifest explicitly records every inherited source and
  companion identity changed by this audit.

## Companion and modular backend

- The Chapter 9 companion covers all 44 source prompts: 16 exploration or
  activity-task guides and 28 exercise-prompt guides. Six additional mastery
  checks bring the total to 50 entries.
- Every entry has a statement, staged hint, answer and complete solution.
  `CHAPTER09_COMPANION_QA.json` is 97,611 bytes / SHA-256
  `4e8712c1dea303278bc293e64907d7e96029e1bfe1258f33898ce70b3638b2bf`
  and reports zero failures and one described Chapter 9 image.
- The stable-ID backend is 166,775 bytes / SHA-256
  `11902b466090d7218c093e1b420c63970679604ab4a46483fda4a228187feccd`.
  Its 26,671-byte alias table has SHA-256
  `31d6115571a035d775d581f48a4e90a09a9d34fb8df45b0083ad93326e6464ab`.
  It binds all 50 entries and all 200 disclosure surfaces, the image, source
  locators, component rights and 15 verified Chapter 9 corrections.
- O003-C094 records the source-critical subspace-convergence correction;
  O003-C096 repairs the proposed-limit notation. O003-C095 is no longer
  pending: the cumulative wrapper passed the pinned PreTeXt 1.7.5 RelaxNG
  validation after the unchanged summary list became a sibling of its
  introductory paragraph; the pinned validation exited successfully.

## Deterministic HTML and reader behavior

- Two clean, fixed-epoch HTML builds followed by the idempotent Indonesian
  finalizer produced identical 7,038-file manifests. The tree contains 6,927
  HTML documents and 17,715,029 bytes; its canonical manifest SHA-256 is
  `e8df11b6f24433ec04fb62d232927363f6e37eb872a79e7f019b49593b7514cc`.
- The canonical file manifest is 1,153,907 bytes / SHA-256
  `7840b39e1ebf4e90adab72ce3082389d609137c25c1f0d770a67a4dc37ebfac4`.
  Local QA checked 21,251 links/assets and 37 image references with zero
  failures; its 846-byte report has SHA-256
  `662f26cac6564f87f413a46fb1e692a5671b00a24f27944fc774ef6e28496af6`.
- Browser regression at 1280 and 390 CSS-pixel widths found no document-level
  horizontal overflow. The desktop reading measure is centered at 960 px;
  mobile content reflows to 318.2222 px. The cumulative wrapper, affected
  source pages, prior point-set guides, and Chapter 8-9 exercise guides remain
  readable after the terminology changes.
- Browser interaction opened a source guide, exercise guide and mastery check
  and proved independent staged hint, answer and solution disclosures. The
  3,583-byte browser receipt has SHA-256
  `9eeb3c7b9598ebdfd208b647ec6d7227f7890a7bdafe20b30d799b73acaedbbe`.

## GitHub Pages publication tree

- The bounded `docs/` tree retains the historical Chapter 1-8 entry surfaces
  and PDFs while advancing the primary reader to the corrected Chapters 1-9
  boundary. It contains 7,049 files, including 6,929 HTML documents, totaling
  25,541,658 bytes; its canonical manifest SHA-256 is
  `0d4b1bfefda757ee6bdfa52fe067d373f4de5f1959bfc1951f4a6d6b006cb888`.
- The detailed 1,156,217-byte file manifest has SHA-256
  `adf93b69f2b4b2dfe34faf8c24202e527aa248c6eeec89401d51dfb878567cd0`.
  The compact 353-byte identity manifest has SHA-256
  `153fcd182104f4a5fdb2dcd0d7ded2bbe7eae82f6bb46b67a7bf6786b79036a1`.
- The 834-byte Pages-tree QA report has SHA-256
  `c3872beda84c793f6b2f22ceddc981f63b61dc81f894fc926c208305578b3a7c`
  and status `pass`. It checked 21,527 links/assets and 37 image references,
  required the cumulative reader, Chapter 9 source and companion entry points,
  mastery surface and current PDF, and found zero failures.

## Deterministic PDF and visual inspection

- Two clean strict XeLaTeX builds used `SOURCE_DATE_EPOCH=1692057600` and the
  transcript error gate. Both emitted exactly 1,866,925 bytes with SHA-256
  `554f6c699e73951f2eddcc32b80ceb656448a2f85eb945a88fc507dab6033621`.
  The two deterministic receipts are 314 bytes / SHA-256
  `fa5acac5a2b48eaf8abe0ae474e4f98554338b4df651bc8ebda83c5e567fd1e6`
  and 349 bytes / SHA-256
  `d8f68d80adefcc71eccdbb3ff41d74427df5e678863219e5ca4b64b4713eff90`.
- The PDF has 215 US-Letter pages, no rotation and 23 outline entries. Physical
  pages 1-6 use lowercase Roman page labels and physical page 7 begins Arabic
  page 1. All 218 link annotations are valid; the two interactive-lab links
  use the portable public HTTPS target and no relative URI remains.
- The 5,689-byte structure report has SHA-256
  `a5667e67b85202f052f87d8d7407070ceef881892bcca6281df134649148b1bc`
  and status `pass`.
- All 215 pages were inspected through all-page contact sheets; physical
  pages 82-90 (Chapter 9), the terminology-changed companion pages 127,
  138-140, 178-180, 196, 198 and 208, and long titles on pages 65, 73, 174
  and 196 received full-page inspection. No clipping, overlap, broken
  glyph box, illegible formula, title overflow, figure cutoff or faulty
  transition was found. A 10-pixel edge sweep at 120 dpi found no edge content.
  The minimum observed content margin was 77 pixels. The 1,259-byte visual
  receipt has SHA-256
  `a8f8cca1ccb047fd0a2e23e4e0286f58d5c353c054c3483858afc31eb17283a1`.
- Non-blocking TeX box warnings include inherited long headings and a 2.83 pt
  Chapter 9 line; targeted visual inspection proves that they do not clip.
  Sparse pages 90, 98, 109 and 142 arise from clean chapter/appendix breaks.

## Runtime, rights and open caveats

- Pinned runtime: Python 3.12.13, PreTeXt 1.7.5, setuptools 75.8.0 and
  MiKTeX 26.5. The wrapper targets are `chapters01-09-html` and
  `chapters01-09-pdf`.
- The translated GVSU spine remains conservatively CC BY-NC-SA 3.0. The
  independently authored self-study companion remains a separately identified
  CC BY 4.0 component. Figure/software notices remain component-specific; no
  endorsement is claimed and the collection is not flattened to one license.
- HTML remains the primary accessible surface. The PDF is untagged and its
  mathematical fonts have incomplete Unicode extraction maps. Complete-edition
  offline closure also remains open: the current bounded HTML still references
  documented PreTeXt, Runestone, MathJax, font, CDN and rights hosts.

## Verdict

Chapters 1-9 and their separately licensed self-study companions are admitted
as the current coherent cumulative reader boundary. Source, schema, companion,
backend, deterministic HTML/PDF, link/asset, responsive/reflow, staged
disclosure, PDF structure and all-page visual gates pass. Publication must say
truthfully that 9 of 20 GVSU chapters are available; production advances next
to Chapter 10 in source order after this boundary is preserved and anonymously
read back.
