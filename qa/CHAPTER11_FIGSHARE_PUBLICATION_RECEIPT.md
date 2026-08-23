# Chapter 11 Figshare maintenance receipt

Checked: 2026-08-23 (Europe/Berlin)

Target project: https://figshare.com/projects/Open_and_Share-Alike_Educational_Materials_Translations/280296
Target Indonesian collection: https://doi.org/10.6084/m9.figshare.c.8668413.v1
Prepared metadata: `publication/figshare_chapters01_11_metadata.json`

The public Figshare API currently reports project `280296` with zero articles
and collection `8668413` with zero articles. The previously recorded article
identifier `33314751` returns `EntityNotFound: ArticleVersion` from the public
API and has no public version list. I therefore did not create a duplicate or
claim a publication that cannot be read back.

The runtime credential was read from the designated local credential file only
in memory. Both authenticated schemes supported by the endpoint returned HTTP
403 `InactiveAccount`; no upload or metadata mutation was accepted. The local
metadata is nevertheless advanced to the published Zenodo DOI
`https://doi.org/10.5281/zenodo.22070455`, accurately labels the 276-page
11-of-20 boundary, and preserves the CC0-metadata/link-only rule without
substituting a false license. A later authorized retry can create one public
work-level item under the named project and collection once the Figshare
account is reactivated; until then, Zenodo is the authoritative public release
and this receipt is the complete truthful Figshare state.
