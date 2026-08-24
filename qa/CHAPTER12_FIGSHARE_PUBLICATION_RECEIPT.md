# Chapter 12 Figshare maintenance receipt

Checked: 2026-08-24 (Europe/Berlin)

- Target project: <https://figshare.com/projects/Open_and_Share-Alike_Educational_Materials_Translations/280296>
- Target Indonesian collection: <https://doi.org/10.6084/m9.figshare.c.8668413.v1>
- Prepared metadata: `publication/figshare_chapters01_12_metadata.json`
- Byte-preserving release authority: <https://doi.org/10.5281/zenodo.22074449>

The public Figshare API no longer exposes the previously recorded work-level
article `33314751`; its anonymous article endpoint returns HTTP 404. The public
project and collection inventories also do not contain that identifier. An
authenticated owner preflight was therefore required before any possible
creation or update, so that a hidden draft or owner-visible article would not
be duplicated.

The runtime credential was read only in memory from the designated local
credential file and was never printed, logged, copied or committed. The
authenticated account-article endpoint returned HTTP 403 with the exact public-
safe error class `Inactive/disabled account`. No Figshare mutation was accepted
or attempted after that result: no duplicate article was created, no file was
uploaded, no project or collection was modified, and no incompatible license
was substituted.

The prepared zero-file metadata/link payload is advanced truthfully to the
verified 328-page Chapters 1-12 release and the Zenodo version DOI above. Its
CC0 selection applies only to the Figshare metadata and links; it does not
relicense the linked mixed-rights edition. A later retry may create or update
exactly one work-level item only after the account endpoint succeeds and an
owner/public deduplication check proves the target identity.

## Verdict

Figshare maintenance remains operationally blocked by the service's disabled-
account response. GitHub and Zenodo are the current public repositories. This
receipt is a failure-state record, not a publication claim.
