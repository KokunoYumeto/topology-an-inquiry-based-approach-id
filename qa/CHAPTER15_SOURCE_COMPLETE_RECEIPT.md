# Chapter 15 complete source translation receipt

Verified: 2026-08-26 (Europe/Berlin)

Status: **all seven Chapter 15 source files translated; source closure and the
partial cumulative schema gate pass; the Chapter 15 reader is not yet admitted
because its companion/backend and cumulative HTML/PDF release gates remain
open**.

## Frozen authority and closure

The controlling source is Steven Schlicker's August 2023 GVSU *Topology: An
Inquiry-Based Approach* at commit
`0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
`7df245934eedb7174d5ff8af18afff5a7abdde78`. The complete Chapter 15 authority
closure is seven files / 20,180 raw bytes. Its ordered basename-plus-NUL framed
stream is 20,303 bytes with SHA-256
`65600e4ee8c9ce3b51cb43c13eac92e2a33047b373447008136bf41caae0c13c`.
The Indonesian closure is seven files / 21,685 raw bytes; its corresponding
21,808-byte framed stream has SHA-256
`37de2f5158dff6a266dc79297ebddc216dd053ea5a037e2e08ebab9042afa215`.
The derivative remains conservatively CC BY-NC-SA 3.0; no rights, attribution,
or non-endorsement boundary changed.

| Source-order file | Authority bytes / SHA-256 | Indonesian bytes / SHA-256 |
|---|---:|---:|
| `source/chap_subspaces.ptx` | 900 / `96f6a1b471988d34db2ee46e1a059bcd7993da3a424885f5a9f715eb4b135cb5` | 946 / `f7720031ddf3c35e092d420a9f24ed572e75735a566c4b4c30e7055d88307252` |
| `source/sec_sub.ptx` | 5,067 / `d6041c9caf76d6b57e4da86b92bbc4ad4f1ddca1b045d7fa39aa9829e9fbcdca` | 5,708 / `5cb914d69cb60973a012f1d1e1ae3794b270bd4c3137ee2327b49fe1d2cb6e7a` |
| `source/sec_subspace_top.ptx` | 2,098 / `c12ea1c13ad78e0f7d2bee34b210fa50fe78dcd0c67b906ba0486b76d2a2ab0f` | 2,370 / `91c5519650d091c45195cecaf55fb45da20d07501f4d1fecb2d265fceffba07c` |
| `source/sec_base_sub.ptx` | 1,734 / `e1ac6e81a0366766210f5cdf1b04ca218edbdd4150c24f749e8683fa6962b520` | 1,889 / `66b287d07cc606a59e5385ea3cf010827bac477119bcda8fc28490825eaee48e` |
| `source/sec_open_int_rn.ptx` | 2,843 / `32698a08f57dd3c43ce4a7401f01107726253ad5e65bd23fb46b0b92daf07502` | 3,033 / `905f47e5bd971a82e06de3e8e424a400ff1ca67e71470717f7406408bbe4f302` |
| `source/sec_sub_summ.ptx` | 1,309 / `db2e35d5923fc57aec2ddb8ca848c383f5cbd4f33c2971b8d0037719204aa260` | 1,420 / `18d62774a606bfa2a131129c9551ce4badb7ee76174a4d6612eedf8275840664` |
| `source/sec_sub_exer.ptx` | 6,229 / `ebce70baa33411826a9782a5bf9721bdfe41e0fbd74330326be0292ba890fee5` | 6,319 / `99a0f8f7dbcb02c8367246cb97e05efd157c0faef3c27c8fd765b57c000b0e79` |

The closure preserves 11 XML IDs, four xrefs, 258 protected mathematics nodes,
eight exercises, 27 task nodes, and four activity/exploration containers. Two
task nodes are grouping parents and 25 are atomic learner prompts. Five
exercises carry a direct statement without a child task, so the exact
learner-response denominator is 30 prompts. The two grouping parents remain
explicit backend relations and are not counted again.

## Figure and accessibility surface

Chapter 15 has exactly one active figure, `F_Subspace_open`, and one image
reference, `Subspace_open`. Its 4,240-byte editable SVG is byte-identical to
the pinned SVG and has SHA-256
`9a14e9953375c270f9d03d055865254f5a43aaacbf7469f9e9930fe82fdc59ac`.
The pinned 4,040-byte PDF has SHA-256
`12701b3cd26e1ed909dbe11c3511ba447fbe2fa44dd9b3a164a3551e10c8ac15`;
the existing 2,149-byte sanitized editable PDF has SHA-256
`23ea7c1429c3f58dc63ce98519e021b918052bc3a8cbfc16d72a7c9c7ae3f984`.
The translated figure retains its stable ID, caption, image reference, and
content, and now includes a faithful Indonesian description of the ambient
rectangle `X`, shaded subspace `A`, dashed open set `O`, and the relatively
open intersection `O \cap A`. No other image, interactive, program, remote, or
external-URL surface occurs in this chapter.

## Fail-closed QA

`qa/CHAPTER15_SOURCE_COMPLETE_QA.json` is 6,279 bytes / SHA-256
`c4f20c003f136af40025f21291c454bc25c25e3d50060d577371ab1ded0cde11`,
status `pass`, zero failures. The seven-file comparator passes 464 retained
elements, 258 protected mathematics nodes, 11 IDs, four xrefs, 27 task nodes,
eight exercises, and four activity/exploration containers. The only external
xref, `chap_Closed_sets_topology`, is explicitly allowed and resolves in the
admitted cumulative source. The comparator records exactly the approved
notation repair, description insertion, two complete same-file block moves,
and two invalid ancestor-shell removals; it records no attribute, protected
code, or unapproved mathematics change. Its combined translated SHA-256 is
`37de2f5158dff6a266dc79297ebddc216dd053ea5a037e2e08ebab9042afa215`.

`qa/CHAPTER15_CUMULATIVE_SCHEMA_PARTIAL_QA.json` is 2,001 bytes / SHA-256
`75ec93a358dff4b872f464c01eb9f9a20698968fa1f22b4293aafa55314e4fa0`,
status `pass`, with zero diagnostics. Chapter 15 inserted in memory immediately
after Chapter 14 in the sealed cumulative Chapters 1-14 wrapper produces
41,321 expanded elements and validates under Python 3.12.13, PreTeXt 1.7.5,
lxml 4.9.4, schema SHA-256
`fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0`,
and resource commit `9bce7e55911fb14e3e6e362bfa78bd6431c38597`.

A bounded reader-visible scan of exactly these seven translated files found
zero active English instruction or exposition markers after protected
mathematics was excluded. Its sole approved exception is the unchanged cited
bibliographic title
`Counterexamples in Topology (2nd ed.)`, which occurs exactly once; it is not
translated or treated as active instructional prose.

## Terminology and source corrections

Approved terminology is complete through O003-T203. The Chapter 15 additions
are *subruang*, *topologi subruang*, *terbuka relatif*, *tertutup relatif*,
*topologi relatif*, *topologi terinduksi*, *basis untuk subruang*, *pembatasan
metrik atau fungsi*, and *subhimpunan tak kosong*. The complete terminology
ledger is 21,270 bytes / SHA-256
`01eb146a691688722e18703941c2a27d3d283650aaa32ef99dc1edd451dcb836`.

Verified repairs O003-C182 through O003-C187 are all bound in the current
source. O003-C182 replaces an unstable item-number reference and restores the
chapter's explicit nonempty-subspace scope. O003-C183 corrects the basis
membership from plain `B` to the established `\B`. O003-C184 repairs the
singular/plural agreement in the relatively closed-set summary. O003-C185
moves the complete figure block to a schema-valid section-level position and
adds its description. O003-C186 moves the unchanged formal subspace definition
out of an invalid task-statement nesting. O003-C187 removes only the two
invalid definition/statement ancestor shells in the hereditary-property
exercise while retaining all reader-facing definition content, index text,
mathematics, order, and exercise intent. The complete correction ledger is
74,870 bytes / SHA-256
`1a99e094715799faf8c9d19a688ab66278007e72dfff18c7bb4584bd38007a33`.

## Next gate

This is a complete Chapter 15 source-translation checkpoint, not an admitted
Chapter 15 reader and not completion of the 20-chapter edition. It does not
advance the admitted cumulative HTML/PDF or preservation boundary beyond
Chapters 1-14. The next gate is the separately licensed staged companion for
all 30 prompts, the two grouping relations and bounded mastery surface,
followed by deterministic backend closure, complete cumulative schema and
HTML/PDF builds, accessibility/offline QA, publication into the existing
lineages, and anonymous public-byte readback.
