# Chapter 14 deterministic prompt-inventory receipt

Verified: 2026-08-26 (Europe/Berlin)

Status: **complete source-prompt inventory and grouping backend; staged
companion entries remain to be authored**.

The inventory is derived only from the immutable Chapter 14 authority closure
at GVSU commit `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`. Its eight declared files have
the generator's framed ordered SHA-256
`73a2623e77c3b26b588dd441dcf77609c6cb07d1cc40a2605c46b6e9caaf1084`.

## Exact census

- 81 learner-response units: 25 non-exercise and 56 exercise prompts;
- 77 atomic leaf tasks and four taskless exercises with direct statements;
- three grouping-only task nodes, retained separately with all child-entry
  relations resolving;
- stable companion entry IDs `o003-c90-ch14-guide-01` through `-25` and
  `o003-c90-ch14-exer-a-01` through `o003-c90-ch14-exer-f-06`;
- canonical prompt-mapping SHA-256
  `ee610085d17009e74afd6776ecb62838a764fb77bc419a53ee4a9e5c17960ab7`.

Every entry records its authority file, one-based source line, carrier type,
nearest real XML ID, exact XPath, canonical subtree hash, synthetic
locale-neutral anchor, parent grouping anchor where applicable, and current
support status. The three grouping records retain the two nested activities in
the introduction and the nested composition exercise.

## Deterministic outputs

| Path | Bytes | SHA-256 |
|---|---:|---|
| `scripts/build_chapter14_prompt_inventory.py` | 34,969 | `c18cf54cbb1c28d37a028db8f53065c1a2aa9036007dfafa66d68394bdd8c762` |
| `backend/chapter_14_prompt_inventory.json` | 96,231 | `47821c780d73e6164ca512356c2c545f82468b168308a85283bf0efa06c04399` |
| `backend/chapter_14_source_prompt_map.csv` | 47,375 | `7d166f2f6888cbc102fba025986b5d362d20a49f69a25fc4ea525699ce6e9445` |
| `backend/chapter_14_grouping_nodes.json` | 2,984 | `d3204860900770fa814007b4e4db8e859caa0a5a479bbb54a00d56cd239d7e13` |

An immediate second run with `--check` regenerated all three outputs in memory
and required exact existing bytes; it passed with the identities above. The
script is bounded to the eight frozen Chapter 14 files and performs no broad
repository or workspace scan.

## Next gate

Author one staged statement, hint, answer or assessment rubric, and complete
solution for each of the 81 mapped prompts, preserve the three grouping
relations, add bounded original mastery checks, and then seal the five coupled
backend artifacts and PreTeXt schema receipts deterministically. This
inventory does not itself admit or publish a Chapters 1-14 reader.
