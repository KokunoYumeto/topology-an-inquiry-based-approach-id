# Chapter 13 source translation receipt

Verified: 2026-08-25 (Europe/Berlin)

## Boundary

This receipt covers the complete nine-file source closure of Chapter 13,
*Himpunan Tertutup dalam Ruang Topologi*. It is a source-production checkpoint,
not an admitted reader release: the 76-prompt self-study companion, stable-ID
backend, cumulative HTML/PDF build, publication, and anonymous readback still
follow.

Authority is Steven Schlicker's August 2023 GVSU *Topology: An Inquiry-Based
Approach* at commit `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`, tree
`7df245934eedb7174d5ff8af18afff5a7abdde78`. The frozen authority closure is
9 files / 61,337 bytes at ordered basename-plus-NUL SHA-256
`9ca7295746f9916cea625420370e0ee1f09d28c4d6c940b03f22d75251235313`.

## Translated files

| Order | File | Bytes | SHA-256 |
|---:|---|---:|---|
| 1 | `repo/source/chap_Closed_sets_topology.ptx` | 2,148 | `44a59dab0a8411c39f100b081651d4e287a2369627d54d1deceb458086114c4d` |
| 2 | `repo/source/sec_closed_sets_top_intro.ptx` | 4,049 | `81a783cad1430e39fbbfed4dd601661acacbb69b833ce230de8b4d4ca5b0084b` |
| 3 | `repo/source/sec_union_inter_closed.ptx` | 3,760 | `e9ef4c2372e590174f29c79df90d6f906128cecbe55d1c184f98fe5c3672de71` |
| 4 | `repo/source/sec_limit_points.ptx` | 7,737 | `e66d2f03a8fc9f08b300b4beef5f34904e8c357f67508b8c4bb15f26c0450d07` |
| 5 | `repo/source/sec_top_closure.ptx` | 4,336 | `fb0005a38e4188ef75ea200bb8ce4b56333820c40965645a9611d88b0da5b0af` |
| 6 | `repo/source/sec_set_boundary.ptx` | 2,879 | `34bc5f2f4fe11ded3170153e584f8227c29fd8f9ff52290288eb5bdd4aec6049` |
| 7 | `repo/source/sec_separation_ax.ptx` | 13,982 | `745bf02dfb66a8f1fbbc0703cf6b11bcd1ed0d2ad567c5b64d4dd47d0641f9d7` |
| 8 | `repo/source/sec_closed_sets_top_summ.ptx` | 4,667 | `051a4372cff499464c2ae67be8eecd67829bdb5baeafb2083e34b9cf73a0125a` |
| 9 | `repo/source/sec_closed_sets_top_exer.ptx` | 22,788 | `d4ae3e0d376a0baaccf788748d5ffc2320ec6a292e6ac7f100b072e65d9cb06b` |

The QA script's ordered translated identity is SHA-256
`9b8a851c97b6f9a0b3ca82a991a6a535ff08eac32dee6a51f3ef0f859eea5b65`.

## Fail-closed checks

`repo/qa/CHAPTER13_SOURCE_QA.json` is 8,343 bytes / SHA-256
`a329cfa487fa51f932308c06bc67a37ed118f31663acccddb9313d8e88619889`.
It passes with zero failures and proves:

- all nine files parse as XML;
- the translated closure retains 23 XML IDs, 20 exercises, 77 task nodes,
  779 math nodes, and no image or interactive dependency;
- all 25 translated xrefs resolve against the explicit chapter plus eight
  admitted external targets;
- element, attribute, ID, and protected-math order is identical except for one
  approved repair that converts a printed raw ID to a resolving `xref` and 13
  specifically approved protected-math corrections;
- translated TeX `text` payloads change only reader-visible language;
- the 76-prompt denominator is unchanged: 70 leaf task prompts plus six direct
  prompt carriers, with seven grouping task nodes retained separately.

A bounded reader-visible-text scan found no unintended active English. The
retained `clopen` explanation and the official English Niemytzki-paper title
are deliberate terminology/bibliographic data.

## Corrections and terminology

Source repairs O003-C146 through O003-C160 are recorded in
`00_control/SOURCE_CORRECTIONS.csv` (62,833 bytes / SHA-256
`7db6a08b254a326a75d82e715bf7e0432c20d59ebe67ee9f367aacfedd304e5c`).
They repair only deterministic notation, variable, cross-reference,
quantifier, geometric-description, and definition defects; no new theorem or
hypothesis is silently introduced.

Terminology is frozen through O003-T166 in `00_control/TERMINOLOGY.csv`
(17,009 bytes / SHA-256
`67ffe90c191d7cfe1222ec85e0efadae460847751a5989aa2c6b8d172d4ede40`).
`00_control/CHAPTER13_TERMINOLOGY_AUDIT.md` is 2,634 bytes / SHA-256
`6cc5c1acebbcf1be3e7fe68c6a783f04bdf84f5ff1b48e7c178e4778f53d74c3`
and records the bounded failed arXiv search, official Indonesian academic PDF
fallback, decisions, and the normalization to `aksioma separasi` and `ruang
reguler`. Repository and reader metadata retain the explicit production model
identity `OpenAI Codex gpt-5.6-sol, Ultra` without displacing source authorship.

## Next action

Generate the exact 76-row prompt map and seven grouping relationships, author
all staged statement/hint/answer/solution support plus eight original mastery
checks, build the deterministic five-file backend transaction, then integrate
the cumulative Chapters 1–13 reader for pinned-schema, HTML/PDF, link,
responsive, accessibility, structure, visual, publication, and anonymous
readback gates.
