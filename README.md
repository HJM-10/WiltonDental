# Wilton Dental website

A source-backed, multi-page redesign retaining the original logo and authentic practice/team imagery.

## Build and preview

```powershell
python scripts/build.py
python -m http.server 4173 --directory dist
```

Open http://localhost:4173/. The build uses Python's standard library. Generated output in `dist` works without a build step on Vercel.

## Structure

- `src/content.py`: treatment and team content.
- `scripts/build.py`: shared templates, 29 pages (28 content pages and a not-found design) and four legacy redirects.
- `src/site.css`: branding, responsive layouts and motion.
- `src/site.js`: navigation, filtering, care-journey progress and imaging explorer.
- `src/tooth-viewer.js`: GLB rendering, controls, lifecycle and fallback.
- `scripts/build_tooth.py`: original illustrative mesh; requires NumPy and Pillow.
- `docs/sources/`: dated source snapshots and asset provenance.
- `docs/verification.json`: latest browser verification results.
- `audit/src/build-documentation.py`: A4 report generator; requires ReportLab, Pillow and Windows fonts.

## Verification

Run `node scripts/verify.cjs` with the local server running. The script uses the bundled Playwright runtime and installed Chrome. Change its two runtime paths when using another machine.

Checks cover generated routes, links/assets, four responsive widths, axe accessibility rules, menu, filters, contact context, map, 3D controls, reduced motion, data saving, failed-model fallback and JavaScript-disabled reading. No enquiry is sent.

## Current scope

- 13 treatment pages plus directory and imaging page.
- All six published team members with individual profiles.
- Practice, care options, fees, contact and website information pages.
- Original logo, locally hosted typography and source photography.
- Animated 3D opening, motion pause, keyboard controls, OPG/CBCT explorer and card/scroll effects.
- The four-stage care journey and the practice's original Google Maps embed on the homepage and contact page.

There is no booking backend. Contact links open the relevant application and do not promise a booking. The site is intentionally noindex: current fees, NHS intake, biographies, registration details, service arrangements and practice policies require approval before public launch.

## Deployment and rollback

The existing GitHub/Vercel structure is preserved. `vercel.json` serves `dist`, maps four old public routes and avoids immutable caching of unversioned assets. Changes pushed to `main` use the existing repository deployment configuration; replacing the live practice website still requires practice approval. The ignored `.openai` registration is historical.

Baseline repository revision: `62fc513`. Starting files were also copied to `tmp/baseline`.

## Documentation

- `output/pdf/Wilton-Dental-Project-Report.pdf`: current audit and implementation report.
- `docs/IMPLEMENTATION_PLAN.md`: scope and acceptance sequence.
- `docs/routes.json`: generated route inventory.

The previous audit and logo concepts are historical artifacts, superseded by the new report and original-logo direction.
