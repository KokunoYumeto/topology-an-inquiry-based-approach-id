# Chapter 16 source checkpoint through identifying quotient spaces

Verified: 2026-08-28 (Europe/Berlin)

Status: **pass**

This bounded checkpoint extends Chapter 16, *Ruang Kuosien*, through the
complete `sec_find_quotient_space.ptx` section. Five of the seven source files
are translated contiguously in upstream order. This is a source-only
checkpoint; the admitted rendered reader and current Zenodo version remain the
public/open Chapters 1-15 boundary.

## Authority and translated prefix

- Frozen GVSU commit:
  `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`.
- Complete Chapter 16 authority closure: 7 files / 49,730 raw bytes.
- Ordered basename-plus-NUL authority SHA-256:
  `8d2380b722e111ddb3d2c349ce5eecddd597d6418ca059064e0ac99521354ee3`.
- Newly translated file: `source/sec_find_quotient_space.ptx`, 13,431 bytes /
  SHA-256
  `c0acf007662d0d18c6bc1f7ddf6b2723451025405b132c082e2181dd2e991adf`.
- Five-file translated-prefix SHA-256:
  `d59ddaaa07ae4aa5c84b683c58d505b2a771beef1111f6a3e5e964b3d7263e69`.

The translated GVSU component remains conservatively CC BY-NC-SA 3.0. The
future original self-study companion remains separately identified as CC BY
4.0. No upstream endorsement is claimed. Production provenance is
`OpenAI Codex gpt-5.6-sol, Ultra`.

## Structural, language, and mathematical QA

`qa/CHAPTER16_SOURCE_THROUGH_IDENTIFYING_QUOTIENT_SPACES_QA.json` is 6,802
bytes / SHA-256
`307ad95e4f3706e293f5530fe67151bee297511c9a20719a375a9e23fb4a2391`.
The pinned Python 3.12.13 comparator passes with zero failures across the
five-file prefix. It preserves 669 elements after the nine explicitly
additive accessibility/index insertions, 437 protected math nodes, 15 unique
IDs, 16 xrefs, and 19 task nodes. The one prefix-external xref,
`ex_sim_p_relation`, resolves in the frozen Chapter 16 exercise file and in
the cumulative source; the allowance is consumed exactly once. A bounded
active-English scan of the new reader-facing source has zero hits.

The new file preserves its complete element order, IDs, xrefs, task topology,
and 202 protected math nodes. It has exactly one additive accessibility
description and exactly three approved math changes:

1. `S_1` is corrected to the defined circle notation `S^1`.
2. The invalid equality between subsets of different ambient spaces is
   replaced by
   `f^{-1}(O)=p^{-1}(\overline f^{-1}(O))`, followed by the quotient-topology
   criterion in `X/~`.
3. Lifted intervals for `f(t)=(cos(2 pi t),sin(2 pi t))` are translated by
   integers, `(A+k,B+k)`, rather than by `2 pi k`.

Two prose-only repairs make the quotient representative statement precise and
restrict the open-map proof to subintervals of length less than one. These five
repairs are ledgered as `O003-C193` through `O003-C197`. An independent
sentence-by-sentence mathematical and id-ID review found no omission,
unintended addition, terminology defect, or remaining semantic error.

## Schema and accessibility

`qa/CHAPTER16_CUMULATIVE_SCHEMA_PARTIAL_QA.json` is 2,035 bytes / SHA-256
`a44be02d55c3245bbf4ba52517097c53df70462140ee1abd0f0f5f86e03a1e64`.
Pinned PreTeXt 1.7.5 RelaxNG validation in the cumulative Chapters 1-15
context reports zero diagnostics over 44,222 expanded elements. This remains
a mixed-translation-state structural check over the complete Chapter 16
closure; it does not claim the final two source files are translated.

The `S_1_basis` SVG was rendered and inspected. Its new Indonesian description
faithfully identifies the unit circle, open disk, and highlighted open arc.
The active SVG is 24,754 bytes / SHA-256
`e2df196fef35a98580588a25eec28c277c2d12f70a78902458d1d5e435951a64`;
the paired PDF is 5,692 bytes / SHA-256
`b91ea229bb0b7622c3f27342b8a2b410e19974c3e4810e974a0bc4bd3ebde367`.
Both identities match the frozen authority audit.

Terminology now runs through `O003-T222`, adding *proyeksi kuosien kanonis*,
*terdefinisi dengan baik*, *menghormati relasi ekuivalensi*, *busur terbuka*,
and *himpunan terbuka basis*. The terminology ledger is 23,728 bytes /
SHA-256
`d676579ac6a8614c2d15a16d96555f0d6ed3fc8f6194027b0ff9102993538dd3`;
the correction ledger is 79,621 bytes / SHA-256
`6a858f7938ed1a4cfadcc3641c8638d133cadd93c342bc113b7ac346f21e8da2`.

## Durable continuation

The exact next file is `source/sec_quotients_summ.ptx`, followed by
`source/sec_quotients_exer.ptx`. Translate in that order, repair the summary's
misclassification of `p` as a topology, rerun the complete-prefix and
cumulative-schema checks, then close the 53-prompt companion/backend.
