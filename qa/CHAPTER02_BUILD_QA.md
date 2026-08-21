# Chapters 1-2 reader - admitted build and QA receipt

Date: 2026-08-21 (Europe/Berlin)  
Lane: O003/C90, id-ID  
Boundary: Chapters 1-2, Himpunan and Fungsi, plus separately licensed
self-study companions

## Result

This cumulative Chapter 2 boundary is admitted for continued edition
production. It supersedes the standalone Chapter 1 hashes after a
terminology-only normalization and the companion-rights clarification. The
complete 20-chapter edition is still in progress.

## Source and companion

- Exact cumulative manifest:
  \`qa/CHAPTER02_SOURCE_MANIFEST.json\`, 8,143 bytes, SHA-256
  \`200de99d0ebd951161d7ddc864c782b54bf19f478dcd8fd0e116e0512abc4faf\`.
- Current Chapter 1 source combined SHA-256:
  \`a4378df30a25d675ac4261d8aa0266a8368bf99d9a405632cc00c8506127bbf3\`.
- Chapter 2 source combined SHA-256:
  \`c739fef4fcebcf02e370fcd7579cca150d4f24f0c08c8ec07f14b6f0bf900fb8\`.
- Cumulative 16-file source SHA-256:
  \`4dfd872589a5750ae677568aac4386e31f0dfa2b8fd2aae05643d2bd7732d882\`.
- Chapter 2 source QA passed for 8 files, 31 IDs, 16 xrefs, 8
  explorations/activities, 17 exercises, and 60 tasks. Protected mathematics,
  topology, attributes, IDs, and xrefs agree except for the explicitly
  ledgered deterministic repairs C004-C017.
- The original Chapter 2 companion is 61,897 bytes, SHA-256
  \`19c68038c862b5634b004fbd57ace01c57c6282583efd9f4b30778bbdcbd1c25\`.
  An independent audit passed all 8 activity checkpoints, all 17
  source-exercise guides, all 8 mastery checks, all 33 hints, answers, and
  complete solutions, 137 unique IDs, and 10 resolving source xrefs.
- Backend manifest:
  \`backend/chapter_02_companion_manifest.json\`, SHA-256
  \`e88a73523489b3637c5ea0b51b12c95d1c513e24c29c89d942f5b7a6e56f7b9b\`.

## HTML

- Runtime: Python 3.12.13, PreTeXt 1.7.5, setuptools 75.8.0.
- Two clean builds at \`SOURCE_DATE_EPOCH=1692057600\` produced identical
  finalized manifests.
- Canonical tree SHA-256:
  \`96675e619de6b630d441a31184017a9dfb5ce6e78b01072d010053b547791863\`.
- Manifest file SHA-256:
  \`d40b377f057db4ba2f85759806db54a88045bdab686aee2806977f56392635fb\`.
- Closure: 1,635 files, 1,524 HTML files, 5,331,142 bytes.
- Automated QA checked 4,151 links/assets and 76 images with no failures,
  duplicate IDs, missing local targets/fragments, generated-English denylist
  hits, missing image alternatives, privacy hits, or credential patterns.
- Responsive browser QA passed at 1280 x 900 and 390 x 844 with zero
  horizontal overflow. The desktop reading column is 784 px centered between
  the 240 px TOC and the matching right margin; the mobile reading column is
  318.22 px with the sidebar hidden.
- Indonesian navigation labels were widened so \`Sebelumnya\`, \`Naik\`, and
  \`Berikutnya\` have equal client and scroll widths. A Chapter 2
  \`Petunjuk\` knowl opened and exposed Indonesian content.
- Browser console: zero errors; only the known MathJax component-version
  warnings.
- Current caveat: this bounded reader still references remote PreTeXt,
  Runestone, MathJax, font, CSS, and JavaScript hosts. Whole-edition offline
  closure remains a release gate and is not falsely claimed here.

## PDF

- Runtime: MiKTeX 26.5 with XeLaTeX; strict wrapper rejects TeX errors even
  when the PreTeXt CLI reports success.
- Two strict builds at the fixed epoch produced identical bytes.
- Artifact:
  \`output/chapters01-02-pdf/chapters_01_02_reader.pdf\`.
- 289,219 bytes; 51 Letter pages; PDF 1.7; SHA-256
  \`e95490eb7c7bdf2670ac9985342dd70e4e80ff2b64db18cbb283dccdf2d2f98c\`.
- Unencrypted, no JavaScript, not tagged. HTML remains the primary accessible
  surface.
- All 51 pages were rendered at 120 dpi and inspected through five contact
  sheets; dense source pages, both companion transitions, long solutions,
  final exercise pages, and the index were also inspected at full size.
  No clipping, overlap, missing glyph, broken mathematics, or bad pagination
  remains.
- The final internal LaTeX pass has one accepted 6.48035 pt overfull box in a
  Chapter 1 answer. Visual inspection confirms that it does not clip. First
  internal passes request reruns; final references and outlines resolve.

## Rights and release scope

- The translated GVSU spine is handled conservatively as CC BY-NC-SA 3.0.
- The independently authored companions are separately CC BY 4.0.
- The edition is a collection with per-component rights and explicit
  non-endorsement; it is not distributed under a flattened blanket license.
- The public boundary is truthful about being Chapters 1-2 of an unfinished
  complete edition. Publication and anonymous byte readback are recorded below
  once the transaction completes.

## Next cursor

Continue in source order with Chapter 3, Metric Spaces. Do not pause the
production lane merely because this bounded reader is publishable.

## Publication

- Public repository:
  https://github.com/KokunoYumeto/topology-an-inquiry-based-approach-id
- Initial content commit:
  `3b5b091846b8ba9aa1ba1dc927bb54db100fcd9e`.
- Public reader:
  https://kokunoyumeto.github.io/topology-an-inquiry-based-approach-id/
- Public PDF:
  https://kokunoyumeto.github.io/topology-an-inquiry-based-approach-id/downloads/topologi-pendekatan-berbasis-inkuiri-bab-01-02-id.pdf
- GitHub Pages build for the content commit reached `built`.
- Anonymous raw and Pages reads returned exact index SHA-256
  `e1335dfb6ae5f07dc263923a080b8d3d940bd6c542b17ad49302b9f65efd4f37`
  and exact PDF SHA-256
  `e95490eb7c7bdf2670ac9985342dd70e4e80ff2b64db18cbb283dccdf2d2f98c`.
- Full transaction evidence:
  `qa/CHAPTER02_PUBLICATION_RECEIPT.md`.
