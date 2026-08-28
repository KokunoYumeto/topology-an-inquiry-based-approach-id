# Chapter 16 source checkpoint through quotient spaces

Verified: 2026-08-28 (Europe/Berlin)

Status: **pass**

This bounded checkpoint extends Chapter 16, *Ruang Kuosien*, through the
complete `sec_quotient_space.ptx` section. Four of the seven source files are
now translated in source order. This is a source-only production boundary; the
admitted rendered reader and Zenodo release remain the verified public/open
Chapters 1–15 boundary.

## Authority and translated prefix

- Frozen GVSU commit:
  `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`.
- Complete Chapter 16 authority closure: 7 files / 49,730 raw bytes.
- Ordered basename-plus-NUL authority SHA-256:
  `8d2380b722e111ddb3d2c349ce5eecddd597d6418ca059064e0ac99521354ee3`.
- Newly translated file: `source/sec_quotient_space.ptx`, 15,084 bytes /
  SHA-256
  `484a25fe145d6531bf2982b2ffdc8247b3392487a1d339eed22e2c51c798b1e6`.
- Four-file translated-prefix SHA-256:
  `6a76fb912f902db236698809c2cf4bae58ad1264b26adde8fb66f1894f9f1fe9`.

The translated GVSU source remains conservatively CC BY-NC-SA 3.0. The future
original self-study companion remains separately identified as CC BY 4.0. No
upstream endorsement is claimed. Production provenance is
`OpenAI Codex gpt-5.6-sol, Ultra`.

## Structural and mathematical QA

`qa/CHAPTER16_SOURCE_THROUGH_QUOTIENT_SPACES_QA.json` is 5,199 bytes /
SHA-256
`48e947fe087117341173d927fce69872beb4eddfe695a5fad8bf496bb9ebcc1c`.
It passes with zero failures across the four-file prefix and preserves 10
unique IDs, seven resolving xrefs, 235 protected math nodes, 16 task nodes,
five activities or explorations, and all six image references. The comparator
records exactly one approved mathematical repair and eight additive
accessibility/index elements; there is no hidden attribute, element-order,
code, or other math change.

The approved mathematical repair changes the erroneous first square quotient
from `(x,0) ~ (1-x,0)` to `(x,0) ~ (1-x,1)`, matching the source's frozen
Möbius-identification diagram. The next task's displayed relation is the
standard torus quotient and is now named and indexed as a torus instead of a
Möbius strip. The corrected Möbius construction receives its own index entry.
The source's shorthand lists of generating pairs are explicitly described as
generating equivalence relations, so symmetry and transitive closure are not
silently omitted. These repairs are ledgered as `O003-C190` through
`O003-C192`; the earlier prefix repairs remain `O003-C188` and `O003-C189`.

`qa/CHAPTER16_CUMULATIVE_SCHEMA_PARTIAL_QA.json` is 2,035 bytes / SHA-256
`daf65b2495dbe6fa417f80a3def45a127c44cadcd1ab31d6ce366510297b1451`.
Pinned PreTeXt 1.7.5 RelaxNG validation in the cumulative Chapters 1–15 context
reports zero diagnostics. It remains a mixed translation-state structural
check over the complete Chapter 16 closure, not a claim that the last three
files are translated. The translated section parses as XML, its nonmath prose
has no bounded active-English hit, and the two control JSON files and ledgers
remain parseable with unique IDs.

## Figures and accessibility

All six active diagrams in this section were rendered and inspected before six
faithful Indonesian descriptions were added. The `floor.pdf` derivative is
byte-identical to authority. The five smaller sanitized PDFs for the cylinder,
Klein bottle, Möbius strip, sphere quotient, and torus differ only in container
bytes: Poppler 26.05.0 renderings at 300 dpi have identical dimensions and
ImageMagick absolute-error counts of zero against their frozen authority PDFs.
The complete machine-readable evidence is
`qa/CHAPTER16_QUOTIENT_SPACES_ASSET_QA.json`, 3,643 bytes / SHA-256
`1ba18562816a9a08d595315399ec5988335d36cc8e7d5e7be5560602bddf064f`.
Temporary render files were removed after the evidence was frozen.

Terminology now runs through `O003-T217`, including *pemetaan kuosien*,
*ruang identifikasi*, *fungsi lantai*, *pita Möbius*, *torus*, *botol Klein*,
and *persegi satuan*. The terminology ledger is 23,073 bytes / SHA-256
`510fd1ca1ce0dddd71e0df0cfc8be285ea88da8ff2c373a18b188ef265966fd8`;
the correction ledger is 77,344 bytes / SHA-256
`666712df6db0d40dbba95c64efe9a5b0b5950e59ceda85ce56a31d1cff94df0f`.

## Durable continuation

The exact next file is `source/sec_find_quotient_space.ptx`, followed by the
summary and exercises. Continue in that order, carry the already frozen
inverse-image proof repair, add the remaining image description, and rerun the
fail-closed prefix and cumulative-schema checks before advancing.
