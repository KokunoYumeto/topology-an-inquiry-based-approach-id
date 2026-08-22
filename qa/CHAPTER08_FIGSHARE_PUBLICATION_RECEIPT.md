# Chapters 1–8 Figshare publication receipt

Publication boundary: complete verified Bahasa Indonesia reader boundary through
Chapter 8 of 20, including the separately authored self-study companion and the
locale-neutral modular backend. This is a partial edition, not a completion
claim.

Transaction date: 2026-08-22 (Europe/Berlin)

## Rights gate and chosen route

The live Figshare account exposed these seven article licenses:

- CC BY 4.0
- CC0
- MIT
- GPL
- GPL 2.0+
- GPL 3.0+
- Apache 2.0

It did not expose CC BY-NC-SA 3.0, and a Figshare article has one article-level
license field. The verified Zenodo checkpoint is a collection with separate
component rights: the translated GVSU spine is treated conservatively as
CC BY-NC-SA 3.0, while the original companion is CC BY 4.0. Mirroring the six
release files under any single Figshare license would therefore misstate the
rights.

The Figshare item is consequently a **CC0 metadata-and-link record only**. Its
CC0 label applies only to the Figshare metadata. It contains no edition files
and does not relicense the linked work. Zenodo remains the byte-preserving
authority for this checkpoint:

- version record: <https://zenodo.org/records/22059895>
- version DOI: <https://doi.org/10.5281/zenodo.22059895>
- concept DOI: <https://doi.org/10.5281/zenodo.22059894>
- Zenodo byte receipt: `qa/CHAPTER08_ZENODO_PUBLICATION_RECEIPT.md`

## Public Figshare identity

- title: `Topologi: Pendekatan Berbasis Inkuiri`
- article ID: `33314751`
- article version: `1`
- DOI: <https://doi.org/10.6084/m9.figshare.33314751.v1>
- public page:
  <https://figshare.com/articles/online_resource/Topologi_Pendekatan_Berbasis_Inkuiri/33314751>
- item type: `online resource` (the live API's link-resource type)
- license: `CC0`, explicitly scoped in the description to metadata only
- files: `0`
- public authors returned by Figshare: `Kokuno Yumeto`; `Steven Schlicker`
- references: Zenodo version DOI, Zenodo concept DOI, and the official GVSU
  institutional source record
- exact quality/scope label in public prose: Chapters 1–8 of 20; incomplete;
  verified reader, companion, backend, editable PreTeXt source, manifests,
  checksums, and QA available at Zenodo
- non-endorsement and the frozen upstream commit/tree are stated explicitly
- the title and description contain no umbrella-project label or expansion

## Project and collection membership

The article was created directly inside public project `280296`:

- <https://figshare.com/projects/Open_and_Share-Alike_Educational_Materials_Translations/280296>

It was then associated with the existing Indonesian collection `8668413` and
that collection was republished. Concurrent additions had already advanced the
collection; the anonymous readback after this transaction returned current
collection version `7`:

- collection DOI: <https://doi.org/10.6084/m9.figshare.c.8668413.v7>
- requested lineage supplied by the coordinator:
  <https://doi.org/10.6084/m9.figshare.c.8668413.v1>

No competing Zenodo concept was created and no other lane's files or article
metadata were edited.

## Anonymous readback

After publication, requests without an authorization header proved all of the
following:

1. `GET https://api.figshare.com/v2/articles/33314751` returned the exact
   title, article version 1, type `online resource`, license `CC0`, zero files,
   and the Zenodo version DOI among three references.
2. `GET https://api.figshare.com/v2/projects/280296/articles?page_size=1000`
   contained article `33314751` exactly once.
3. `GET https://api.figshare.com/v2/collections/8668413/articles?page_size=1000`
   contained article `33314751` exactly once.
4. `GET https://api.figshare.com/v2/collections/8668413` returned collection
   DOI `10.6084/m9.figshare.c.8668413.v7` and version 7.
5. DOI resolution reached the exact article version page and the exact
   collection version page. The Figshare HTML front end returned HTTP 202 while
   processing the dynamic page; the anonymous public API readbacks above were
   complete and passed.

Because this is deliberately a zero-file metadata record, there are no
Figshare release bytes or file hashes to compare. The six exact release files
and their anonymous byte-for-byte SHA-256 verification remain recorded in the
Zenodo receipt named above.
