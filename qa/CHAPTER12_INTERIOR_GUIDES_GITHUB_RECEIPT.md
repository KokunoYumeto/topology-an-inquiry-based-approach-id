# Chapter 12 interior-guide checkpoint — GitHub readback

- Lane: O003/C90, Bahasa Indonesia, Chapter 12 (*Ruang Topologi*)
- Status: partial, not an admitted reader boundary
- Content commit: `adc1e054`
- Repository: https://github.com/KokunoYumeto/topology-an-inquiry-based-approach-id
- Readback: unauthenticated HTTPS raw reads at the immutable commit; every
  listed file returned HTTP 200 and exact local bytes.
- Exact model provenance: `OpenAI Codex gpt-5.6-sol, Ultra`. Source-author,
  institutional, and human-contributor credits remain unchanged.

## Public files

| Path | Bytes | SHA-256 |
|---|---:|---|
| `source/sec_interior_set_top.ptx` | 7,236 | `5ca0fa8b701495b67d519621430e2cd4eb53bcfcff409639228e970586e851f8` |
| `companion/chapter_12_source_guides_f.ptx` | 15,112 | `428317e5d74981441740499418d311abb986c6e971782f6b00fd8214639531f0` |
| `companion/chapter_12_topological_spaces_self_study.ptx` | 1,347 | `712e61acf02fbebd8346762d9182b19621ca0c59f0140ea3b18ca35b5a2690e3` |
| `backend/chapter_12_companion_manifest.partial.json` | 13,756 | `91803e531f003e10c88a79c1ec6362baeefc4624621c379e739cd3854b79080c` |
| `backend/chapter_12_entry_aliases.partial.csv` | 6,174 | `8af026f52029380d1b1cd6b29182c7e4a83f495523e8efa847c2584ad6911d9a` |
| `qa/CHAPTER12_COMPANION_PARTIAL_QA.json` | 13,520 | `d31db380aba614c0e2e2c65efceaae62ebc608451166901cc9ce8e99fb43a997` |
| `qa/CHAPTER12_COMPANION_WRAPPER_SCHEMA_QA.json` | 1,120 | `1741eeba6a496ba9a7fe1831470a244adcb45665dc3ca153fec24615f60648bc` |
| `qa/CHAPTER12_INTERIOR_GUIDE_SCHEMA_QA.json` | 792 | `9d3894cb4aa786d90bf5cd38608797e6301a6a74aa65b2ea5e9ab7545d930262` |
| `qa/CHAPTER12_SOURCE_QA.json` | 6,778 | `6919e508cd81df33f1a9226f2409d7ac88620cfdba69cccbf86ea3ab901f2df0` |
| `qa/CHAPTER12_SOURCE_TRANSLATION_RECEIPT.md` | 2,399 | `821e177a88fd19d9c078beffef9f94280580c2230263577917dce9f198711798` |

## Scope and gates

- The separately licensed companion now covers 31 of 78 Chapter 12 prompt
  units (31 atomic units; 47 pending) with 124 staged
  statement/hint/answer/solution surfaces. Five grouping tasks, mastery checks,
  the complete backend, and the cumulative HTML/PDF reader remain pending.
- `chapter_12_source_guides_f.ptx` covers the four interior examples and the two
  maximal-open-subset proof tasks in source order (local stable IDs 26–31).
- The six-file XInclude wrapper and standalone guide pass pinned PreTeXt 1.7.5,
  Python 3.12.13, and RelaxNG validation with zero diagnostics. Schema SHA-256:
  `fb9632a81f16d94068e463df4efcaf0c7ffa9e20555abde9aea2f1dc52888ca0`;
  resource commit: `9bce7e55911fb14e3e6e362bfa78bd6431c38597`.
- Source QA passes at translated combined SHA-256
  `a773f83e8f119e5fc62a7b56e1107bc1489f6fd4e14652d126f0276e346884f0`.
  Corrections C139–C140 repair two upstream uses of `d` where an arbitrary
  topological space is intended; all seven source-critical repairs are listed
  in `00_control/SOURCE_CORRECTIONS.csv`.
- The GVSU derivative remains conservatively CC BY-NC-SA 3.0; the original
  companion remains a separate CC BY 4.0 component. No blanket license or
  endorsement claim is made.

Anonymous public-byte readback passed for every file in this receipt.
