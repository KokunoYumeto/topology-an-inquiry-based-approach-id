# Chapters 1-12 cumulative build and QA receipt

Verified: 2026-08-25 (Europe/Berlin)

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
  `0783fc2b8c6cb123225496c5171b20c9297f0a9c13b1ac9a99c99fcf7dee61fc`.
  `CHAPTER12_SOURCE_QA.json` is 8,274 bytes / SHA-256
  `a4bb46a5f8a2b043b59324b888fec1f16441b31cbcd4ad3fa21ff0354facd89a`;
  status `pass`, 25 IDs, 14 resolving xrefs, no missing targets, and one active
  image. The retained forward reference to Product Topology is visibly labeled
  Bab 20 and resolves to a localized unnumbered *Kolofon*. That page identifies
  source-order Chapter 13 as *Himpunan Tertutup dalam Ruang Topologi* rather
  than misnumbering Product Topology as Chapter 13.
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
and `hasil kali`; the corrected terminology pass also standardizes
`ketaksamaan`, `produk`, `elemen`, and the set-theoretic use of `irisan`, while
retaining the genuinely geometric use of `perpotongan`. The audit is 4,525
bytes / SHA-256
`732b03e504a8f6ffed52112d8306a6d084dba588c7e8da0ad0c79b2e1325064e`.
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
- `CHAPTER12_COMPANION_QA.json` is 115,941 bytes / SHA-256
  `666d1938373c180a524a58be6d2ed37172ddf29be6ea025a2b076479d73d1f50`.
  Its pre-build `reader_admission_pending` flag is discharged by the
  deterministic reader, docs, and visual evidence in this receipt; the
  companion closure itself is complete.
- The stable-ID backend manifest is 116,133 bytes / SHA-256
  `a3879dc648a8e870751ad57cf6691e37a5be543999c10f0ebb103324d9e43a77`.
  The 23,206-byte alias table, 47,950-byte prompt map, and 4,940-byte grouping
  map have SHA-256 values
  `4a8e979717fcc9db27d408980db5e9ec7d222b28aa0823a5cf8483b1095c5c10`,
  `0deb6ece6d5bf8a6152b934843ab65252fc082f7de5419f1acb6df090307a4c5`,
  and `37801610bced290913f8e7e93004b5f4c1d5ecbdda2bb230ee5c60de9059e39e`.
  Original mastery entries carry no false upstream locator.

## Schema and pinned runtime

The 6,944-byte cumulative wrapper has SHA-256
`1b0b4b77887c016aa88ac3ec9b779796e539d95974382e12b0668477ebe6fc61`.
Its 139-file local XInclude closure passes the pinned PreTeXt RelaxNG schema
with zero diagnostics. `CHAPTER12_CUMULATIVE_SCHEMA_QA.json` is 6,764 bytes /
SHA-256
`f758da7bd8195b1c2d13d8279e874ef1f6013d2f31b4f0a8b1051b515f7f7bcd`.
The recorded runtime is Python 3.12.13, PreTeXt 1.7.5, setuptools 75.8.0,
resource commit `9bce7e55911fb14e3e6e362bfa78bd6431c38597`, pinned schema SHA-256
`fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0`,
and MiKTeX 26.5.

## Deterministic HTML and live reader behavior

Two clean corrected HTML builds produced byte-identical canonical manifests.
The canonical generated tree has 10,873 files, 10,762 HTML documents, and
27,769,203 bytes; its canonical tree identity is
`ef6819b209faab95f8f74ea80a632a4b50a4e3616e96036de4dc053e093cb0a3`.
The canonical manifest is 1,781,955 bytes / SHA-256
`44144e15e4b4c57ce2d731877bb4252a8cf5d778b23210ba4236698b7e3c957d`;
the labeled run-one and run-two manifests are 1,781,961 bytes with SHA-256
`1a7e42747308ef2128fd8f52bc5506b51c7c1595c93bb89d3128826f89ba57fe`
and `2d6f4475d6fa20ed3e717395d81d73fe26527cd06e5d3e9d43b5c46a3b4c1c43`.
`CHAPTER12_HTML_QA.json` is 1,648 bytes / SHA-256
`e67557af727811212b18a88e695f1349823cf7c70fd572bdb16dd1ca10244f17`,
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
The byte-preserving upstream archive itself is retained locally and bound by
its official commit, tree, byte count, and SHA-256. It is intentionally omitted
from the public source ZIP because those same 20 original PDF metadata
dictionaries retain the legacy paths; the archive is not silently rewritten
or falsely represented as privacy-clean.

Live browser checks covered 1440, 1280, 1024, 768, and 390 CSS-pixel widths.
The main column fills the available reading area, `lang="id-ID"` and localized
chrome remain intact, and no checked page has document-level horizontal
overflow. The corrected neighborhood guide and a mastery check each opened
their statement, hint, answer, and complete solution on a 390-pixel viewport.
The 5,449-byte browser receipt has SHA-256
`3fd947d783ef6bd6a6ea06db3b21655ce76818913d9145bf43fbab9798150d9e`.

## Deterministic PDF and visual inspection

Two strict clean builds emitted the same 328-page US-Letter PDF: 2,707,175
bytes, SHA-256
`2cb491eb69ebf24e829a1877417023b79b619c887dd43e94afe8b57e369bdcdd`.
The run receipts have SHA-256 values
`47b2246bfdc43a1463fd40382e6b43e82c062098ec80b4d4b243f20c85b6f7de`
and `f5ff089bf245f3212cc44a1d9c7380c06c3eef582165ec37926d3a0d96e01c93`.
Their strict build logs are 121,738 bytes each, with SHA-256
`d741c61970ac5fbb857fd039d211679665930c2675a2aafcd094f9b196eaec1c`
and `2a40e0d2dd2976d46051cd9848324b2c3f6e855ee4fdbbc529448ecb70200f91`.
The 6,891-byte structure receipt has SHA-256
`ab5d74b881faa049c9054e3b08a6e4f644c7ea84679ff368f92e00fc5f9bc35a`:
30 outline entries, 298 link annotations, zero replacement-character titles,
zero relative URI targets, and zero failures.

All 328 pages were freshly rendered at 120 dpi with Poppler `pdftoppm 24.04.0`
and inspected in 28 contact sheets, with direct review of the corrected dense
exercise page and final *Kolofon*. Page 3 is the intentional blank verso and
page 124 is the sparse appendix heading. There are zero unexpected blank pages, zero
edge-touching pages, and no clipping, overlap, broken formula, or unreadable
glyph. The 220,965-byte visual receipt has SHA-256
`357aa0579548e9395a781737799e948896a2533345f2c95d1482c00be53cf5c2`.
The PDF is not tagged; HTML remains the primary accessible surface.

## GitHub Pages publication tree

The non-destructive `docs/` overlay retains historical reader entry points and
earlier PDFs while adding the complete Chapters 1-12 reader and the primary
328-page PDF. It contains 10,893 files (10,770 HTML), totaling 42,991,729
bytes. The detailed manifest is 1,785,668 bytes / SHA-256
`35ad2e38da37fed38ba9aebdbe42e49712c0105513ea38bdcbee967785b40041`;
the compact manifest is 828 bytes / SHA-256
`a11c17c1cd269b5b1b20f3fb5719ba8d4acef3a413832ca14c1781324318633a`;
the canonical tree identity is
`7d0f24e03fb7373f87dfe6b472fecface5f30918c11bd225403cbb63607739b0`.
`CHAPTER12_DOCS_QA.json` is 1,016 bytes / SHA-256
`884daa1b0a393113d11c61b6759c497f3fd0b26377a4fd0ba9c97228f5516c7d`,
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
