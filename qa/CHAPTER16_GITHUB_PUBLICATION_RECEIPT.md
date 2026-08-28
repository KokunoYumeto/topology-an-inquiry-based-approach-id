# Chapter 16 GitHub publication and anonymous readback receipt

Verified: 2026-08-28T19:30:47+02:00

Status: **pass**

The verified cumulative Chapters 1–16 Indonesian reader was committed and
pushed to the existing edition lineage; no replacement repository or branch
was created.

- Repository: `https://github.com/KokunoYumeto/topology-an-inquiry-based-approach-id`
- Branch: `main`
- Publication commit: `5f8ad7cd9d42a504b9f530ff2c856fda872d1bac`
- Commit subject: `Publish verified Indonesian Chapters 1-16 reader`
- Anonymous `git ls-remote` returned that exact commit for `refs/heads/main`.

## Commit-pinned anonymous byte readback

- `README.md`: 5,788 bytes / SHA-256
  `5718ea9b56bf162a663b7f318ae643a1c18c5881c28751e5591dc148542fc34e`.
- `qa/CHAPTER16_SOURCE_MANIFEST.json`: 190,811 bytes / SHA-256
  `2d326ce1fd48751b0dc115931d7ca4e2778e957a6864171b67d51e87ee69bdde`.

Both unauthenticated commit-pinned raw responses were HTTP 200 and byte-equal
to the local committed files.

## GitHub Pages anonymous byte readback

| Public path | Bytes | SHA-256 |
|---|---:|---|
| `index.html` | 1,001 | `9d01b78e7f97c60a9e3f895cba060be93dfccc97549622c559cd18b1c788353d` |
| `o003-c90-chapters-01-16-reader.html` | 54,853 | `ec09800d516c41a64e70ab04c948eb5a6f6587b49678c6022828fb382254f95a` |
| `chap_quotients.html` | 55,519 | `d60c2bc0e1e6eaad42fe3518b46a8994650dcae43f6e75ecde3ac2722a2ee54b` |
| `sec_quotients_exer.html` | 87,881 | `7f07bec43b40dcf18122aa81d7dcbfd01bc62070c2776b0637eb7bd5ca749134` |
| `o003-c90-ch16-companion.html` | 57,376 | `dabf4b107dd1775b5e191735839f5a88100640eb9dc1a940a03caaad384ddb52` |
| `o003-c90-ch16-mastery.html` | 94,857 | `352b46976e82f809c5d157a0f2566c37ed53e5a4f9ae741e40942a53e2346253` |
| `external/o003-readable-layout.css` | 2,678 | `6464e036ba324c14c37c763cebf648d55eb354357d2befe5819938691c8caae4` |
| `downloads/topologi-pendekatan-berbasis-inkuiri-bab-01-16-id.pdf` | 3,810,136 | `0a240d7416b6730e8e69c7485524fb5309a1153ec4b07e97dd4db080e76a1fd7` |
| retained `o003-c90-chapters-01-15-reader.html` | 52,187 | `83d07eb2a093e2e251583215b6124cd759c3ff12108ba3e536510d3aa332b1ab` |
| retained Chapters 1–15 PDF | 3,453,492 | `b62c1a6ff498cce11312fcb412ee74f47a8893a3363395414eb8f526dbf0456e` |

Every cache-busted Pages response was HTTP 200 and byte-equal to its committed
`docs/` file. The retained Chapter 15 reader and PDF prove that the
non-destructive overlay preserved the preceding public boundary. No credential
material is present in this receipt.
