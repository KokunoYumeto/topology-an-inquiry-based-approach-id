# Chapter 14 source-checkpoint GitHub receipt

Published and anonymously verified: 2026-08-26 (Europe/Berlin)

Status: source-only checkpoint covering the translated Chapter 14 wrapper and
complete introductory section. It does not advance the admitted cumulative
HTML/PDF or Zenodo reader beyond Chapters 1-13.

## Public identity

- Repository: https://github.com/KokunoYumeto/topology-an-inquiry-based-approach-id
- Content commit: `0d10a2c38bf190498d87d180d37df0fa372203cb`
- Branch: `main`

The checkpoint was pushed into the existing edition repository. No competing
repository, release lineage, or DOI concept was created.

## Anonymous commit-pinned readback

The public branch head first resolved to the content commit. Each scoped file
was then downloaded from an unauthenticated commit-pinned raw URL with HTTP
200 and reproduced the local byte count and SHA-256 exactly:

| File | Bytes | SHA-256 |
|---|---:|---|
| `source/chap_continuity_topology.ptx` | 1,128 | `a58657e0ee50e1155c5e4bda648366db27692210e3b0973b7c1a8736992ea495` |
| `source/sec_cont_top_intro.ptx` | 9,801 | `867752285d688dbdb1048f0797be04a0e96e7a33b7a28f7cb3d99152ae173857` |
| `scripts/validate_chapter14_partial_schema.py` | 5,319 | `641052913d9ec4384ae6e5113453a3c6ac0bbefe31060d161c3454581ecefc6d` |
| `qa/CHAPTER14_SOURCE_PARTIAL_QA.json` | 2,579 | `357e7d04f6d98a9b30b068b0a218783921998982a217c80a48ffaef136e060e5` |
| `qa/CHAPTER14_CUMULATIVE_SCHEMA_PARTIAL_QA.json` | 2,193 | `eca808850ec8b41707eb4f1bab5111725032d30e4bc8f7cdf1701402af087a21` |
| `qa/CHAPTER14_SOURCE_PARTIAL_RECEIPT.md` | 4,828 | `6bfc867ecf4dcdd6f96b8401e0fe4f81e7e3ec65c7bb52df0f42f667711a3282` |

## Verdict

The bounded Chapter 14 source checkpoint is public and byte-identical to the
validated local files. Translation resumes with `source/sec_metric_equiv.ptx`.
Chapter 14 remains incomplete and is not represented as a reader release.
