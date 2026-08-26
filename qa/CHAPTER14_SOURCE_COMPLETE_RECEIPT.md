# Chapter 14 complete source translation receipt

Verified: 2026-08-26 (Europe/Berlin)

Status: **all eight Chapter 14 source files translated; source closure passes;
the Chapter 14 reader is not yet admitted because its companion/backend and
cumulative HTML/PDF release gates remain open**.

## Frozen authority and closure

The controlling source is Steven Schlicker's August 2023 GVSU *Topology: An
Inquiry-Based Approach* at commit
`0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
`7df245934eedb7174d5ff8af18afff5a7abdde78`. The complete Chapter 14 closure is
eight files / 44,794 raw bytes at ordered basename-plus-NUL SHA-256
`e36457d2a351d3d77a35234c5e39b13ff2dc0163e7099ab17e95ac60294468e5`.
The derivative remains conservatively CC BY-NC-SA 3.0; no rights or
attribution boundary changed.

| Source-order file | Authority bytes / SHA-256 | Indonesian bytes / SHA-256 |
|---|---:|---:|
| `source/chap_continuity_topology.ptx` | 1,122 / `06045aec5703ca1e033d41b030f3ac2330424f311bc6bd8d65b94320569f84c3` | 1,128 / `a58657e0ee50e1155c5e4bda648366db27692210e3b0973b7c1a8736992ea495` |
| `source/sec_cont_top_intro.ptx` | 9,424 / `4adbbaf4266c069669f599ca5d46d8585eccb79089601bde0a1a65f7c15de902` | 9,801 / `867752285d688dbdb1048f0797be04a0e96e7a33b7a28f7cb3d99152ae173857` |
| `source/sec_metric_equiv.ptx` | 4,838 / `dd915f74c61d3ff3c7610b3a0b187c0f250cfe930e62fe8750096f08b8845560` | 5,564 / `34db0fd00a0a3f489f13df56568166eb5297253a5e63328c8e44f50c5f54e6ea` |
| `source/sec_top_equiv.ptx` | 5,287 / `bd3851f4788d8e4bfe0e52efc5843ff802296b0563b87d2f5d81858808268125` | 5,634 / `923c9f8001a0002bee6bccb9dfcff9d04e0a3049f3a23a7acf1743d7ef4b3d9f` |
| `source/sec_relations.ptx` | 3,225 / `f9cd8ea92cae729689c75f48a3af4af3367f4721da519980ab85aa253064f1a8` | 3,791 / `76c082e1ec59a289178b1b72074fc8aeae35bf07569fad972acdb52fdd378ae3` |
| `source/sec_top_invar.ptx` | 1,864 / `0f4cfb2cce3d0440c1beaa4baab5c8e1e53f8800889f49795afb9ac48a600587` | 1,875 / `8c7ed840c32b92735995b0874e53f306ebb5cec691b608fa44464e924f447e92` |
| `source/sec_cont_top_summ.ptx` | 2,064 / `c2b097654aa77dbbcfa4925c220d97b935a515e7faf3cff255d0f372bb316b72` | 2,140 / `8e01cce0f31344b84c7504b540a9c5fe3879b4c3213704aa48975529743fc95a` |
| `source/sec_cont_top_exer.ptx` | 16,970 / `37e57d20d49b097c2aaea3475b4c54328d40dadc876de7aff86d0aff51928fef` | 17,631 / `ecf66963c297000370bc59840e5a4df86d315064cf368a3211086a9fa08e9af` |

The closure preserves 19 XML IDs, 17 xrefs, 13 exercises, 80 task nodes and
the authority's 81 learner-response units (including one direct prompt carrier).
The only active image is the previously described `Equivalence` figure; no new
asset or interactive surface occurs in the final exercise file.

## Fail-closed QA

`qa/CHAPTER14_SOURCE_COMPLETE_QA.json` is 6,902 bytes / SHA-256
`0f98393d44e530a511b1010ee0b5b4b0e5d5d1ec4087cc20a2399fac53b116d4`, status
`pass`, zero failures. The eight-file comparator passes 1,028 elements, 534
protected math nodes, 19 IDs, 17 xrefs, 80 task nodes, 13 exercises, and six
activity/exploration containers. The framed combined translated SHA-256 is
`806d67e9a0b24ca5ba1b2c1a96417c46d43d488649909b27a5eacd3de4328e4b`.
All six intentionally external xrefs are explicitly allowed and resolve in the
frozen cumulative source.

`qa/CHAPTER14_CUMULATIVE_SCHEMA_COMPLETE_QA.json` is 2,193 bytes / SHA-256
`067fb8a1b7d7f30905d146fe4682bd9f8e9075bb3c5c51ecc84b759355e6e5fc`, with
zero diagnostics. The cumulative Chapters 1-14 tree has 37,709 expanded
elements and validates under Python 3.12.13, PreTeXt 1.7.5, lxml 4.9.4,
schema SHA-256 `fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0`,
and resource commit `9bce7e55911fb14e3e6e362bfa78bd6431c38597`.
Narrow `git diff --check` passes and the bounded reader-visible scan found no
English prose outside mathematical notation, identifiers, and approved terms.

## Terminology and source corrections

Approved terminology remains stable through O003-T194, including *titik limit*,
*pembenaman/tertanam*, *topologi titik tertentu*, *topologi titik yang
dikecualikan*, *topologi diskret*, and *topologi komplemen hingga*. The complete
terminology ledger is 20,054 bytes / SHA-256
`51fa85741a48f48bc869b5b5e9ab66933155787619ac6c32872b9a6fda70498e`.

Repairs O003-C175 through O003-C180 correct six unambiguous English grammar
slips (three in the summary and three in the exercise prose) without changing
any protected mathematics, IDs, xrefs, topology lists, or exercise intent. The
complete correction ledger is 71,588 bytes / SHA-256
`1a320ff3a40cade74ac9f44991884d246f843c30b09eb9d50110e5637892d945`.

## Next gate

This source closure remains a working checkpoint and does not advance the
admitted cumulative HTML/PDF or Zenodo boundary beyond Chapters 1-13. Publish
this exact source/QA receipt checkpoint, then close the complete 81-prompt
staged companion and three grouping relations before the cumulative reader,
strict double PDF, accessibility/offline, existing-lineage preservation, and
anonymous public-byte gates.
