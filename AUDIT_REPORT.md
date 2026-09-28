# Wilton Dental project audit

The baseline audit is the professional A4 report at `output/pdf/Wilton-Dental-Project-Report.pdf`. The September 28 visual update is documented here, in `docs/ARTWORK.md` and in the current browser verification results; the baseline PDF predates that update.

It supersedes the original single-page prototype assessment and includes source evidence, visual comparisons, architecture, content coverage, animation/3D decisions, verification results, technical handover and launch requirements.

## Verified implementation

- 28 content pages plus a not-found page, and four legacy route aliases.
- 13 dedicated treatment pages and a separate imaging page.
- All six published team members and individual profiles.
- Original logo, practice/team photography and diagnostic scan examples retained; ten generated treatment illustrations added.
- Original glossy tooth restored with automatic decorative motion; viewer and pause/resume controls removed. Image explorer and scroll/card effects retained.
- Mobile navigation, hero, treatment cards, imaging dimensions, location and footer spacing reworked; patient journey displayed in animated cards.
- Restored four-stage care journey, working contact destinations and the original Google Maps embed on the homepage and contact page.
- Zero recorded axe rule violations or horizontal overflow findings across the tested routes and widths in the final local run.

Evidence: `docs/verification.json`, `docs/routes.json`, `docs/sources/` and `audit/screenshots/rebuild/`.

## Remaining launch requirements

Practice approval of clinical copy, staff roles/biographies and registration details, availability, fees, finance terms, source-image rights, contact destinations, privacy and complaints information. There is no booking backend. Repository delivery uses the existing GitHub/Vercel configuration; a production browser/device/accessibility review and indexing configuration are still required before replacing the live practice website.

This is a local redesign preview, not a certification of compliance or readiness to replace the live clinical website.
