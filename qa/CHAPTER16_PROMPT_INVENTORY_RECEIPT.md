# Chapter 16 deterministic occurrence-aware prompt-inventory receipt

Verified: 2026-08-28 (Europe/Berlin)

Status: **complete source-prompt occurrence inventory, canonical support map,
grouping backend, and explicit duplicate aliases; staged companion support is
not asserted by this receipt**.

The inventory is derived only from the immutable seven-file Chapter 16
authority closure at GVSU commit
`0c2d8f614ef87aa00de373f3418146c2f1d13bb9`. The generator's path-aware
ordered authority contract has SHA-256
`c778bea11f8afb5c389e0f6d7b1b68f95b5cad2c61a9b41665bc00cdd0dbc285`.
The separately frozen raw chapter-closure identity remains 49,730 bytes at
ordered framed SHA-256
`8d2380b722e111ddb3d2c349ce5eecddd597d6418ca059064e0ac99521354ee3`.

## Exact occurrence and support census

- 54 physical learner-prompt occurrences: 50 atomic leaf tasks, three direct
  statements in taskless exercises, and one direct body in taskless activity
  `act_quotient_er`;
- 52 canonical source-support entries: 18 non-exercise and 34 exercise
  entries;
- three grouping-only task nodes with seven child relations, all resolving;
- two and only two explicit occurrence aliases: occurrence 51 to occurrence
  49 and occurrence 52 to occurrence 50;
- no generic text deduplication: the aliases are hard-coded to the exact
  frozen file/XPath pairs, and all 54 physical locators remain represented;
- canonical prompt-mapping SHA-256
  `ba2157997333466c011f7fee16a72763cb1791174296276bbe56b464a47d608b`;
- occurrence prompt-mapping SHA-256
  `cc8fc0cf2757c652edba7b060bd724a224eba830a9e80a7ca75298c0035ad923`.

Stable companion IDs are assigned in source order as
`o003-c90-ch16-guide-01` through `-18`, followed by four exercise batches of
10, 10, 10, and 4 entries. Each occurrence records its authority file,
one-based line, exact XPath, carrier kind, nearest real XML ID, canonicalized
subtree hash, locale-neutral source anchor, canonical occurrence, and grouping
parent where applicable.

## Deterministic outputs

| Path | Bytes | SHA-256 |
|---|---:|---|
| `scripts/build_chapter16_prompt_inventory.py` | 57,515 | `2bdf2424a7f47926b394508cf11c68233b1ffa55b52bad45edb3a72349906ca2` |
| `backend/chapter_16_prompt_inventory.json` | 145,530 | `ad56dc8745c84b5bad9e9c8824bb528577a66aaa9671500a21a1d8dac2896d89` |
| `backend/chapter_16_source_prompt_map.csv` | 32,059 | `8e4f45db5b73921f2e12ea3d48e11e3af3092b2567a74383d4176f824762ed01` |
| `backend/chapter_16_grouping_nodes.json` | 3,013 | `668d2c9d382aa1aec39d2aef05adac09c5da75e358194bade432ee9924993505` |
| `backend/chapter_16_occurrence_entry_aliases.csv` | 2,587 | `66d5e44c91a977c126439b4a38c7fc091a03634d37387eb9383b19979e269e36` |

Two consecutive `write/check` cycles reproduced all four backend outputs
byte-for-byte. A fresh independent `--check` run also passed with the identities
above. The bounded generator reads only the seven declared frozen authority
files and performs no broad repository or workspace scan.

## Next gate

Author and validate the separately licensed CC BY 4.0 staged support for all
52 canonical source entries, retain the two occurrence aliases and three
grouping relations, add eight bounded mastery entries, and require exactly 60
canonical companion entries with 240 statement/hint/answer-or-rubric/solution
surfaces. This inventory does not itself admit a cumulative Chapters 1–16
reader or change the public Zenodo reader boundary.
