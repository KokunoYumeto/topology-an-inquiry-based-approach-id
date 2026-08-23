# Chapters 1-11 cumulative build and QA receipt

Verified: 2026-08-23 (Europe/Berlin)

Boundary: O003/C90 Bahasa Indonesia, the complete GVSU Chapter 11 boundary
through *Subruang dan Hasil Kali Ruang Metrik*, together with its separately
licensed original self-study companion. This is a coherent partial checkpoint
(11 of 20 source chapters), not a claim that the complete GVSU book or the
original O003 completion modules are finished.

## Frozen source and Chapter 11 translation

- Upstream authority remains Steven Schlicker's GVSU *Topology: An Inquiry-
  Based Approach* at commit
  `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
  `7df245934eedb7174d5ff8af18afff5a7abdde78`. The official 2,200,204-byte
  archive has SHA-256
  `d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3`.
- Chapter 11 closes over six translated source files in frozen order. The
  authority ordered SHA-256 is
  `b36b91c1d1826cef631953a9c8fd05a00aa09ae051b5782ff21e0185b7119d90`;
  the raw concatenated authority SHA-256 is
  `a285e2001e841097c5e1a9f6b53be1304b7982ae8e0e81844d966e4051c4c12e`.
  The translated six-file combined SHA-256 is
  `a976ffaace169f98e4294630f428a63925e4be472af5344ee3239e94932d1572`.
- The source QA is 8,469 bytes / SHA-256
  `f2f474655051af7aeb41d568bf211ad41f9e5f9ef2382cfeb42665cca9fc2890`;
  status `pass`, 14 IDs, 11 resolving xrefs, no missing targets, no active
  images or interactive surfaces, and 15 approved deterministic mathematical
  repairs. Those repairs are recorded in the correction ledger and do not
  silently alter upstream prose.

## Terminology and source-critical repairs

The Chapter 11 terminology audit records a bounded official-arXiv search with
no qualifying Indonesian topology TeX package. The fallback witnesses are
actual Indonesian primary PDFs, not claimed arXiv evidence: Oki Neswan
(`636b5110a6ac6fece61f75bb4a3c04206734b4806e5335df21c096b8cbe9fdee`), UT
PEMA4427 (`3271d0016f0386079f53202021b0f717b1c87103d469edcb4a3c5f755474fcbc`),
Badrulfalah–Joebaedi–Irianingsih
(`aa75607bde2d568e8e8c5a748ac34e043a5c1f2d95591e2f2de2a8c78787582b`), and
Saputro–Hariyanto–Sumanto
(`a8d61c1c9e090a9cad5294aa8f01733fbcb22d7495f2096f6b55e84cf523539d`).
The resulting house terms include `subruang`, `ruang metrik`, `hasil kali`,
`topologi hasil kali`, `ruang Hilbert`, `norma`, and `kekontinuan`; five
`ketaksamaan` occurrences were normalized to `pertidaksamaan` and eight
reader-visible `produk` uses were recast as `hasil kali`. The exact model
provenance is recorded as `OpenAI Codex gpt-5.6-sol, Ultra`; author,
institutional, source, and human-contributor credits remain intact.

## Companion and modular backend

- The separately identified Chapter 11 companion covers all 35 source prompt
  units (16 activity/task guides and 19 exercise guides) plus eight mastery
  checks: 43 entries total. Every entry has a statement, staged hint,
  answer/rubric, and complete solution: 43 of each, 172 disclosure surfaces.
  There are no companion images, remote dependencies, or interactive surfaces.
- `CHAPTER11_COMPANION_QA.json` is 82,847 bytes / SHA-256
  `4f8760a0be71ebd2db7245fe608646a9df29a7c109b7a716b19b45375519b4d1` and
  reports `pass`. The wrapper is 1,961 bytes / SHA-256
  `86d1777ddf08ceb26fe5da1663b36e357b9f3921b3722dc032de30622cd5fa01`.
- The stable-ID backend manifest is 145,686 bytes / SHA-256
  `466bd6e935e11d4af90a9dbeb862f2258d7b08889689be61ba309ebcf4489a60`;
  its alias table is 24,116 bytes / SHA-256
  `af3011c27feeac668b468d404fa0e682df5a84beac93620612c8fbab6d246d0e`.
  It binds the 43 entries, their four staged surfaces, source locators,
  terminology, corrections, rights, and translation state.

## Schema and pinned runtime

The cumulative wrapper and Chapter 11 XInclude closure pass the pinned
PreTeXt RelaxNG validation. `CHAPTER11_SCHEMA_QA.json` is 5,645 bytes / SHA-
256 `5b32b1e60c50c5a7f904be504ab3c642b5a7bf7cb5351f38b90b77732e4542a7`;
the closure contains 115 local files. The recorded runtime is Python 3.12.13,
PreTeXt 1.7.5, setuptools 75.8.0, resource commit
`9bce7e55911fb14e3e6e362bfa78bd6431c38597`, pinned schema SHA-256
`fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0`, and
MiKTeX 26.5.

## Deterministic HTML and reader behavior

Two clean cumulative HTML builds produced identical file identities. The
canonical generated tree has 9,241 files, 9,130 HTML documents, and 23,134,486
bytes; its canonical manifest identity is
`f6a2fa9042171b20ee6f33b15f94ef76f614cfa1ab9ff1e5d01478c9a2934578` (the
1,515,547-byte manifest file has SHA-256
`b4f95d3251852add63850b7e9c7919ba58c3abda63101846f129a1fd9d51f9e2`).
`CHAPTER11_HTML_QA.json` is 1,099 bytes / SHA-256
`6062be72ec405965653930c2e8b309d8285940825d69ecb39f2a3ee3f8016046`,
checking 30,824 links/assets and 37 image references with zero failures.

Responsive browser measurements cover 1440, 1280, 1024, 768, and 390 CSS
pixels: the desktop measure is centered at 960 px, the intermediate measure is
600 px, and mobile content reflows to 318.2222 px with no document-level
horizontal overflow. Indonesian chrome and `lang="id-ID"` are retained. The
5,079-byte browser receipt has SHA-256
`23d3d3dd1e3ac59b26a288efbba964733c80bf3c7e589e06a07387dcef82935f`.
The receipt states the limited reconnect caveat explicitly: no unperformed
post-reconnect public interaction is claimed; current-tree static QA covers
all required surfaces.

## Deterministic PDF and visual inspection

Two strict builds emitted the same 276-page US-Letter PDF:
2,322,239 bytes, SHA-256
`a00ad9c4ea949edc7b90c18534386cea23efd6093b47bc57bae8da387c8ee034`.
The final raster review rendered all 276 pages at 120 dpi with Poppler
`pdftoppm 24.04.0`; full-size checks included the corrected Chapter 11 math
pages and found no clipping, overlap, broken formula, or edge-touching content.
The PDF structure and visual receipts are respectively 6,391 bytes / SHA-256
`5953de247d367aa566055933f708492ef85a659f513791b29a528ada48eeeed9` and
186,312 bytes / SHA-256
`d45fdc241c4a37aa8b6fdbbe3bbbca55ca6f1adbcfa6985dcb87faa1b0aea7be`.
The PDF is not tagged; HTML remains the primary accessible surface.

## GitHub Pages publication tree

The manifest-driven `docs/` overlay retained all historical Chapter 1-10
entry surfaces and added only the Chapter 1-11 reader HTML and primary PDF.
It contains 9,258 files (9,136 HTML), totaling 35,571,726 bytes. The detailed
manifest is 1,518,923 bytes / SHA-256
`868782f1a111fbf1fa64c2c7c6937d45bb849b340aaf8dd26f394229bac57435`; the
compact manifest is 824 bytes / SHA-256
`78092064e793b058c8ea9695662a2c5145a41ac2e38cad8d250bf687d640f1a3`; the
tree identity is
`87d15fc3d3b8c4a056d05c4bfe961c8ab4476a8b5f54a8d64c8009e8d3cb1f73`.
`CHAPTER11_DOCS_QA.json` is 1,052 bytes / SHA-256
`3320db96f48a3c02ed713fd9edae48dc59cdea7ee23d76fc452654b4e00d84fb`,
checking 31,724 links/assets and 37 images with zero failures. The primary
download is the verified 276-page PDF above.

## Rights, provenance and open caveats

The translated GVSU spine remains conservatively CC BY-NC-SA 3.0. The
original self-study companion remains a separate CC BY 4.0 component. Figure,
software, XSL, font, and other notices retain their component-specific rights;
the collection is not flattened to one license, and no endorsement by the
source author or institution is claimed. `LICENSES.md` is 2,277 bytes / SHA-
256 `408eeec186fd9b34660ea5d6df19df5d0e0da7ae63e8681852ff5eaa7b6fb941`;
`companion/RIGHTS.md` is 2,181 bytes / SHA-256
`ef9e9960775b17d187cc655fc73a6f7d76b3d8fe05b9960d3e168ae9fc4fcfe7`.
Remote PreTeXt/Runestone/MathJax/font dependencies remain recorded, whole-book
figure provenance and offline closure remain final-release gates, and Chapters
12-20 plus the original C90 completion modules remain unfinished. The
checkpoint therefore must be labeled partial/finishing.

## Verdict

Chapter 11 and its separate self-study companion pass the bounded source,
terminology, schema, backend, deterministic HTML/PDF, responsive, docs-tree,
and all-page visual gates. This is the next coherent cumulative release
boundary, not completion of the 20-chapter edition. It is ready to push and to
publish as the next version in the existing Zenodo concept while maintaining
the existing Figshare metadata/link record.
