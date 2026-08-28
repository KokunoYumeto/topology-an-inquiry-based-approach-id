# Chapter 17 source-completeness QA receipt

Status: **PASS**. The Chapter 17 authority-versus-translation gate completed with zero failures across all eight files.

## Gate identity

- Comparator: `scripts/qa_source_translation.py` — 41,663 bytes; SHA-256 `992640ccb53385deedea2aba4002a8776bfa553a3e8dcfbad68f0b15871d9c84`.
- Authority root: pinned GVSU source commit `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`.
- JSON report: `qa/CHAPTER17_SOURCE_COMPLETE_QA.json` — 28,418 bytes; SHA-256 `f4f8a155e2764e0bd34ef20576af687aaf26b0f52738704f11060c9589f82b5a`.
- Combined translated SHA-256: `e4e9955460ce4af294b6ea0b0e00d9c9766c9d95e460aa1c16b56cf0ddd0bbb1`.
- Inventory: 8 files, 29 `xml:id` values, 36 xrefs, no duplicate IDs, and no missing xref targets. Seven external xrefs are explicitly listed in the JSON report.

## Narrow structural allowances

Only the six approved schema repairs were admitted:

1. `sec_compact_cont.ptx`: paired authority-shell/translated-shell keys `70:theorem` encode the continuous-image theorem hoist from `statement` to `section`. Its preorder index remains 70; all descendants stay in the comparison, and subtree topology/attributes, IDs, and protected mathematics match the authority.
2. `sec_compact_rn.ptx`: authority key `268:theorem` and translated key `293:theorem` encode the description-offset hoist of `thm_closed_compact` from `statement` to `section`. Its description-free preorder index remains 268; all descendants stay in the comparison, and subtree topology/attributes, ID, and protected mathematics match the authority.
3. `sec_compact_app.ptx`: `sec_compact_app.ptx:4:3:7:theorem` reorders the unchanged `thm_max_min` subtree from `introduction` to `section`.
4. `sec_fractals.ptx`: authority shells `54:task`, `55:statement`, `91:task`, and `92:statement` are paired with translated shells `72:activity`, `73:task`, `74:statement`, `109:activity`, `110:task`, `111:statement`, and `112:p`. The section now has three valid activities instead of one invalid shell, while the four primary prompts and all eight chapter tasks remain present. `def_Hausdorff_distance` and the unchanged theorem are section-level; their descendants, IDs, xrefs, and mathematics remain in the comparison.
5. `chap_Compact_topology.ptx:20:1:21:include` restores authority order for comparison while admitting the schema-valid reader order `sec_fractals.ptx`, then `sec_compact_top_exer.ptx`.
6. `sec_compact_top_exer.ptx`: authority shells `346:definition` and `349:statement` are removed while all descendants remain compared; `349:2:346:idx` repositions the unchanged index subtree. Exactly one labeled `Definisi.` paragraph with its `idx` remains in the divisional-exercise introduction.

The first two hoists are parent-only changes with unchanged description-free preorder. Their paired shell allowances make them explicit in the JSON report, while separate parent-path and subtree-identity checks verify the actual relocation. No other structural exception was used.

## Preservation checks

- Protected mathematics matches except for the eight previously approved source repairs recorded by exact key in the JSON report: four in `sec_compact_rn.ptx`, one in `sec_fractals.ptx`, and three in `sec_compact_top_exer.ptx`.
- All nine images have exactly one nonempty description. The descriptions contain 35 inline mathematics nodes; their ordered inventory SHA-256 is `ce0337151d550c6b3224dffca435c0b29fb01423a58af721689f13f7025dae31`.
- All 231 translated reader-text containers are nonempty.
- No source file was changed during this gate.
