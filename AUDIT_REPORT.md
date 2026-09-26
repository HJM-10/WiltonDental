# Wilton Dental project audit

The current audit is the professional A4 report at `output/pdf/Wilton-Dental-Project-Report.pdf`.

It supersedes the original single-page prototype assessment and includes source evidence, visual comparisons, architecture, content coverage, animation/3D decisions, verification results, technical handover and launch requirements.

## Verified implementation

- 28 content pages plus a not-found page, and four legacy route aliases.
- 13 dedicated treatment pages and a separate imaging page.
- All six published team members and individual profiles.
- Original logo and source images retained.
- Animated 3D opening, image explorer, scroll/card effects and motion controls.
- Restored four-stage care journey, working contact destinations and the original Google Maps embed on the homepage and contact page.
- Zero recorded axe rule violations or horizontal overflow findings across the tested routes and widths in the final local run.

Evidence: `docs/verification.json`, `docs/routes.json`, `docs/sources/` and `audit/screenshots/rebuild/`.

## Remaining launch requirements

Practice approval of clinical copy, staff roles/biographies and registration details, availability, fees, finance terms, source-image rights, contact destinations, privacy and complaints information. There is no booking backend. Repository delivery uses the existing GitHub/Vercel configuration; a production browser/device/accessibility review and indexing configuration are still required before replacing the live practice website.

This is a local redesign preview, not a certification of compliance or readiness to replace the live clinical website.
