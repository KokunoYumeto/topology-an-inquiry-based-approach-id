# Chapter 16 complete source translation receipt

Verified: 2026-08-28 (Europe/Berlin)

Status: **all seven Chapter 16 source files translated; source, accessibility,
and partial cumulative schema gates pass. The Chapter 16 reader is not yet
admitted because its staged companion/backend and cumulative HTML/PDF release
gates remain open.**

## Frozen authority and translated closure

The controlling source is Steven Schlicker's August 2023 GVSU *Topology: An
Inquiry-Based Approach* at commit
`0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
`7df245934eedb7174d5ff8af18afff5a7abdde78`. The complete Chapter 16 authority
closure is seven files / 49,730 raw bytes. Its ordered basename-plus-NUL framed
stream is 49,885 bytes with SHA-256
`8d2380b722e111ddb3d2c349ce5eecddd597d6418ca059064e0ac99521354ee3`.
The Indonesian closure is seven files / 58,310 raw bytes; its corresponding
58,465-byte framed stream has SHA-256
`158afadc3f4ec7be7cae2542381975cb006617ff666bac145acdc205026d4ee6`.

| Source-order file | Authority bytes / SHA-256 | Indonesian bytes / SHA-256 |
|---|---:|---:|
| `source/chap_quotients.ptx` | 775 / `ee5691b2f8c3cc814667a10ddd43f35deeb9113e96ee1e2195834bdf6e608e85` | 800 / `7520b13b2127e1b1126bc22565faac35a6aa186a90c06fa78df09a79dfe62041` |
| `source/sec_quotients.ptx` | 2,075 / `678707a977d59b27527acc0d898d0ae61c928142b44b20d9e9f0c37ba417e6ec` | 2,268 / `322b51175ef5c16b05a35b4e9242f34c8dabaf6c66b92234ae2f41527b680792` |
| `source/sec_quotient_top.ptx` | 2,292 / `9809eda0a49c11c7cdd8062b81ee688610f6e37703cec3811aceb0358afc48ee` | 2,494 / `8d7c8cdab02b6ba253062977a2d7b0ac2dfbc872efab277ce81653bed0aecf6e` |
| `source/sec_quotient_space.ptx` | 12,553 / `e45f4f570a00afed781a7e650042cd8fe4f8beac434dfb9b3ed086281c90d8a3` | 15,090 / `6e0877ee00afde4785318c95d4a2b1eb0889e2bd7985e10295278c10ca5626a8` |
| `source/sec_find_quotient_space.ptx` | 11,826 / `7e3cd80c993a1c0618214c31d7fb8819a05c1432e23c384f0b5e3cd20711ca36` | 13,431 / `c0acf007662d0d18c6bc1f7ddf6b2723451025405b132c082e2181dd2e991adf` |
| `source/sec_quotients_summ.ptx` | 864 / `afdbaabe16ba200b6d96c3ee96e79b33acdb034703441e57a52b3007163d03bd` | 898 / `e92700cff300a31f6db49a5c17cb4accb25d449ece00657515b4bb0fe911f71b` |
| `source/sec_quotients_exer.ptx` | 19,345 / `684303f457655696d841c7b0378599d9729ad5edf6666691d4d9907bbaebbda0` | 23,329 / `19d725f1ace752875c2c353b627054e103d47ebe6154f818e2aadd3610376225` |

The GVSU derivative remains conservatively CC BY-NC-SA 3.0. The original
self-study companion remains separately identified as CC BY 4.0. No upstream
endorsement is claimed. Production provenance is
`OpenAI Codex gpt-5.6-sol, Ultra`.

## Exact learner and support denominator

The closure preserves 53 task nodes: three grouping parents and 50 leaf
tasks. Four taskless containers carry a direct prompt: three exercise
statements and the body of activity `act_quotient_er`. The exact physical
learner-response denominator is therefore 54 occurrences. The final
true/false exercise contains two exact duplicated prompt pairs inherited
verbatim from the frozen source. All four repeated occurrences remain present
to preserve source topology; the two later copies must be explicit aliases of
their respective first copies in the stable-ID backend. Thus the backend has
54 occurrence rows and 52 canonical source-support entries, before mastery
work. The chapter also contains 13 exercises, two upstream hints, no upstream
answers, and no upstream solutions.

## Fail-closed source QA

`qa/CHAPTER16_SOURCE_COMPLETE_QA.json` is 12,403 bytes / SHA-256
`52afa5f8b4919d6a14f21d105210c0b57a1249ede5c18923b7aae822adcea5bd`,
status `pass`, with zero failures. The comparator accounts for 1,106 complete
translated elements, 667 protected mathematics nodes, 21 unique XML IDs, 25
xrefs, 53 task nodes, 13 exercises, and 16 image occurrences. The only two
chapter-external xrefs are explicitly consumed and resolve in the admitted
cumulative source. Excluding 18 approved additive accessibility/index
insertions, element order, attributes, identifiers, exercise topology, and
protected code match the frozen authority exactly.

Sixteen protected-math changes are individually allowlisted and ledger-backed:
the four previously verified quotient-space repairs and twelve exercise-file
changes needed to state three relations precisely and repair duplicated tau,
circle-quotient, and real-projective-plane notation. No unapproved mathematics
or code changed. A protected-surface-aware scan over exactly the seven files
found zero active English instruction or exposition markers. Independent
current-byte review confirms natural id-ID, all 13 exercises, all 34
exercise-file task nodes, and the deliberate duplicate retention.

## Accessibility and schema

All 16 image occurrences now have a faithful Indonesian description. The nine
exercise-file descriptions were based on direct inspection of the exact
projective-plane SVG/PDF assets and distinguish the hemisphere, disk, square,
Möbius-strip, cut, rearrangement, and final disk models. Image references,
figure IDs, captions, order, and assets remain unchanged.

`qa/CHAPTER16_CUMULATIVE_SCHEMA_PARTIAL_QA.json` is 2,035 bytes / SHA-256
`2152771370ec09b27f1f43219b5275c1d069e4883f47ba8b6829859ce79aaec2`,
status `pass`, with zero diagnostics. Chapter 16 inserted in memory after the
sealed Chapters 1-15 wrapper produces 44,231 expanded elements and validates
under Python 3.12.13, PreTeXt 1.7.5, lxml 4.9.4, schema SHA-256
`fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0`,
and resource commit `9bce7e55911fb14e3e6e362bfa78bd6431c38597`.

## Terminology and source corrections

Terminology is complete through `O003-T240`. The 240-row ledger is 26,042
bytes / SHA-256
`95201b440aff0be934d0f08637ecbf0e9050a4bb14239f9fc1d44115e50dead1`.
Chapter 16 additions cover quotient constructions, projective-plane models,
surface classification, and retractions with consistent Indonesian terms.

Verified Chapter 16 repairs are ledgered as `O003-C188` through `O003-C208`.
The complete 207-row correction ledger is 84,773 bytes / SHA-256
`08d69141e9edc2a10d25f2b821f65ff60cc748e75fc942c8ede194af04e7bb11`.
The final exercise repairs make the empty-subspace collapse valid, close two
under-specified equivalence relations, correct projective-incidence and
closed-surface-classification claims, normalize three notation defects, and
record the inherited duplicate prompts without deleting or fabricating work.

## Next gate

This is the complete Chapter 16 source-translation boundary, not yet the
admitted cumulative reader. The next gate is the separately licensed staged
companion for all 54 physical prompt occurrences through 52 canonical source
support entries, the three grouping relations, both exact duplicate-pair
aliases, and eight bounded mastery entries: 60 canonical companion entries and
240 staged statement/hint/answer-or-rubric/solution surfaces. After the backend
reproduces deterministically, build the cumulative Chapters 1-16 HTML and PDF
twice, run link/responsive/accessibility/structure/all-page visual QA, publish
to the existing GitHub and Zenodo lineages, and read every public byte back
anonymously.
