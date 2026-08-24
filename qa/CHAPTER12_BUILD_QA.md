# Chapters 1-12 cumulative build and QA receipt

Verified: 2026-08-24 (Europe/Berlin)

Boundary: O003/C90 Bahasa Indonesia, the complete GVSU Chapter 12 boundary
through *Ruang Topologi*, together with its separately licensed original
self-study companion. This is a coherent partial checkpoint (12 of 20 source
chapters), not a claim that the complete GVSU book or the original O003
completion modules are finished.

## Frozen source and Chapter 12 translation

- Upstream authority remains Steven Schlicker's GVSU *Topology: An
  Inquiry-Based Approach* at commit
  `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
  `7df245934eedb7174d5ff8af18afff5a7abdde78`. The official 2,200,204-byte
  archive has SHA-256
  `d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3`.
- Chapter 12 closes over nine translated source files in frozen order. Their
  translated combined SHA-256 is
  `a8d8a40bced406d284d94a6b9549f6b143453fafae4d862a890959b7b980cfdb`.
  `CHAPTER12_SOURCE_QA.json` is 8,016 bytes / SHA-256
  `6839eb6a1dd73aac8c288c3dd8da4abafbba8f8b051847c49fa59895be6f4cdc`;
  status `pass`, 25 IDs, 14 resolving xrefs, no missing targets, and one active
  image. The explicit Chapter 13 forward reference resolves to an Indonesian
  next-boundary page rather than a broken or untranslated target.
- Fifteen boundary repairs are ledgered as O003-C131 through O003-C145. Twelve
  are source-critical repairs and three apply to the companion guides. The
  fail-closed source comparison records the exact protected-math changes and
  the two complete subtree move allowances; no silent prose rewrite is
  admitted. `SOURCE_CORRECTIONS.csv` is 56,197 bytes / SHA-256
  `b0bb730106e3db7fcfcbafd9a9911190aeb293174cf72a62e27f3a865e091563`.

## Terminology and model provenance

The bounded official arXiv search found no qualifying Indonesian topology TeX
package. The permitted fallback therefore uses four frozen Indonesian primary
PDF witnesses whose actual terminology was re-inspected. It supports the
current forms including `ruang topologi`, `basis untuk topologi`, `himpunan
terbuka`, `topologi indiskret`, `topologi diskret`, `lingkungan`, `interior`,
and `hasil kali`; no Chapter 12 term change was justified. The audit is 3,165
bytes / SHA-256
`1edaf330d2b494ad188dd52b47a69dc30e30a2aa73fc1286c17b2fbf3fc8c94a`.
The glossary is 15,274 bytes / SHA-256
`312a904248cc6349ef3d3462ad851af767ea4f7761d7747b373f635f389a52b1`.
The exact model provenance is `OpenAI Codex gpt-5.6-sol, Ultra`; author,
institutional, source, and human-contributor credits remain intact.

## Companion and modular backend

- All 79 independent Chapter 12 source prompt units have original staged
  support: 73 atomic prompts plus six direct prompt carriers. Eight original
  mastery checks add the same four surfaces. The boundary therefore contains
  87 entries with 87 statements, 87 hints, 87 answers or rubrics, and 87
  complete solutions: 348 staged surfaces. Five grouping nodes are mapped
  separately and are not double-counted as prompt units.
- `CHAPTER12_COMPANION_QA.json` is 115,942 bytes / SHA-256
  `ae9ce8ce60539d2a907a51d86394f9ee394ca38f64285faae02c37f4f5115740`.
  Its pre-build `reader_admission_pending` flag is discharged by the
  deterministic reader, docs, and visual evidence in this receipt; the
  companion closure itself is complete.
- The stable-ID backend manifest is 116,133 bytes / SHA-256
  `c80c517b69e87b79e02f799980bc5a48fdef76b1b9b27f9fe6bddf1ee843b21e`.
  The 23,206-byte alias table, 47,950-byte prompt map, and 4,940-byte grouping
  map have SHA-256 values
  `4a8e979717fcc9db27d408980db5e9ec7d222b28aa0823a5cf8483b1095c5c10`,
  `0deb6ece6d5bf8a6152b934843ab65252fc082f7de5419f1acb6df090307a4c5`,
  and `37801610bced290913f8e7e93004b5f4c1d5ecbdda2bb230ee5c60de9059e39e`.
  Original mastery entries carry no false upstream locator.

## Schema and pinned runtime

The 6,770-byte cumulative wrapper has SHA-256
`70916b283254c6810bf4a6dd29f73276835e236fbdb4a0c595c52efd9d841d75`.
Its 139-file local XInclude closure passes the pinned PreTeXt RelaxNG schema
with zero diagnostics. `CHAPTER12_CUMULATIVE_SCHEMA_QA.json` is 6,764 bytes /
SHA-256
`c6355b4974baafb4f376d1c4b99efbf4debea891743ec15e54fe5628f863bd8d`.
The recorded runtime is Python 3.12.13, PreTeXt 1.7.5, setuptools 75.8.0,
resource commit `9bce7e55911fb14e3e6e362bfa78bd6431c38597`, pinned schema SHA-256
`fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0`,
and MiKTeX 26.5.

## Deterministic HTML and live reader behavior

Two clean corrected HTML builds produced byte-identical manifests. The
canonical generated tree has 10,873 files, 10,762 HTML documents, and
27,780,876 bytes; its canonical tree identity is
`2fabac1179b4a079a98ea699ac4a7bc7b041e2e4cd903b08df8a2d1ca9d174aa`.
Each 1,781,758-byte manifest file has SHA-256
`9f7eb1d6526f7b0608d10ebf7c5ca20dfa2a4bf94b5d9a37a369cfbdebf24029`.
`CHAPTER12_HTML_QA.json` is 1,648 bytes / SHA-256
`7facb1fa8bdc11a357db672a5c5925cbe4c041422070fd298e4fc216aef7df6f`,
checking 40,853 local links/assets and 40 image references with zero failures.

Twenty legacy upstream figure PDFs carried absolute author-workstation paths
in their PDF Info fields. The edition working copies now omit Info/XMP
metadata while preserving each page count, box, rotation, and decoded content
stream. Poppler renders at 150 dpi produced byte-identical PNGs before and
after sanitation for all 20 figures. The pinned upstream archive remains the
unaltered source witness, and the release-package gate now inspects metadata
for every standalone and ZIP-contained PDF rather than only the reader PDF.
The 15,384-byte asset receipt has SHA-256
`7133da5332aefb493bc655d36e9cdf863fa7ebe23118ea8f38750b19b5b7bac7`.

Live browser checks covered 1440, 1280, 1024, 768, and 390 CSS-pixel widths.
The main column fills the available reading area, `lang="id-ID"` and localized
chrome remain intact, and no checked page has document-level horizontal
overflow. The corrected neighborhood guide and a mastery check each opened
their statement, hint, answer, and complete solution on a 390-pixel viewport.
The 6,011-byte browser receipt has SHA-256
`8a41225783f80c80238252d8ee3a2d73a3ba8138558e2bdc51732d5101bbe7e0`.

## Deterministic PDF and visual inspection

Two strict clean builds emitted the same 328-page US-Letter PDF: 2,707,451
bytes, SHA-256
`6ce855a593d0a90bc5f8932bc1969f9acede1b348d28aa2b427280f3b060b49a`.
The run receipts have SHA-256 values
`12ef3e92f9c3b984ed85a199b8881e3bfed78bf3f53c23f60a9fb08b4d037da6`
and `d5e26171d2eb1eab0930911d9e04b62282c76eb9c5d46d28f67d0700971c7aef`.
The 7,041-byte structure receipt has SHA-256
`11ae7a6a5e129236cd81221839aa7a3be44a2b7ba8a063694f799c8df01183a6`:
31 outline entries, zero replacement-character titles, zero relative URI
targets, and zero failures.

All 328 pages were freshly rendered at 120 dpi with Poppler `pdftoppm 24.04.0`
and inspected in 28 contact sheets, with full-size review of the sparse divider,
the corrected neighborhood answer, dense basis/interior pages, and mastery
case expressions. Page 3 is the intentional blank verso and page 125 is the
intentional appendix divider. There are zero unexpected blank pages, zero
edge-touching pages, and no clipping, overlap, broken formula, or unreadable
glyph. The 220,959-byte visual receipt has SHA-256
`a53b5007a42c2d36be56d687062898599083517e48f0afc986814be39d1561c0`.
The PDF is not tagged; HTML remains the primary accessible surface.

## GitHub Pages publication tree

The non-destructive `docs/` overlay retains historical reader entry points and
earlier PDFs while adding the complete Chapters 1-12 reader and the primary
328-page PDF. It contains 10,893 files (10,770 HTML), totaling 43,003,678
bytes. The detailed manifest is 1,785,454 bytes / SHA-256
`cb8b3669780fe1a810b55cec6574e5a618cd0e65767e8b3cc5cfdc01d654cf2a`;
the compact manifest is 828 bytes / SHA-256
`bf7c1b0318ba3a2adb3cd119bf8b675a070522265a09196deeb91ad70d1f3ba0`;
the canonical tree identity is
`9eec3dc1fbafba38b0256a8d8e0f96a49e6db48f0f18eb94e4a4ecb0f9f541fa`.
`CHAPTER12_DOCS_QA.json` is 1,110 bytes / SHA-256
`3a699b8afef5583dd93661bf898c93b8ffad217e4b92404beda8e354747ea20f`,
checking 42,105 links/assets and 40 images with zero failures. The primary
download is the verified 328-page PDF above.

## Rights, provenance, and open caveats

The translated GVSU spine remains conservatively CC BY-NC-SA 3.0. The
original self-study companion remains a separate CC BY 4.0 component. Figure,
software, XSL, font, and other notices retain their component-specific rights;
the collection is not flattened to one license, and no endorsement by the
source author or institution is claimed. `LICENSES.md` is 2,277 bytes / SHA-
256 `408eeec186fd9b34660ea5d6df19df5d0e0da7ae63e8681852ff5eaa7b6fb941`;
`companion/RIGHTS.md` is 2,181 bytes / SHA-256
`ef9e9960775b17d187cc655fc73a6f7d76b3d8fe05b9960d3e168ae9fc4fcfe7`.
Remote PreTeXt/Runestone/MathJax/font dependencies remain explicitly recorded;
whole-book offline closure, figure-provenance closure, and PDF tagging remain
final-release gates. Chapters 13-20 and the original C90 completion modules
remain unfinished. The checkpoint must therefore remain labeled partial.

## Verdict

Chapter 12 and its separate self-study companion pass the bounded source,
terminology, schema, backend, deterministic HTML/PDF, live responsive, docs-
tree, and all-page visual gates. This is the next coherent cumulative release
boundary, not completion of the 20-chapter edition. It is ready to push and to
publish as the next version in the existing Zenodo concept.
