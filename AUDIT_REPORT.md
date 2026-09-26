# Wilton Dental Website Audit

**Audit date:** 26 September 2026  
**Prepared for:** Wilton Dental Practice prototype pitch  
**Scope:** Current public website, redesigned prototype in this repository, deployment readiness, conversion UX, accessibility, SEO, performance, and launch risks.

## Executive summary

The redesigned prototype is **pitch-ready but not yet production-ready**. It is a substantial improvement over the current public website in visual credibility, content hierarchy, mobile presentation, clinician visibility, and appointment-flow clarity. The prototype also has a clean browser console, valid landmark structure, labelled form controls, visible keyboard focus, and reduced-motion support.

The remaining work is primarily operational rather than aesthetic. Before launch, the appointment journey must connect to a real destination, phone and WhatsApp routes should be restored, local-business structured data and social metadata should be added, the two large PNG assets should be optimized, and the modal should receive a complete keyboard focus cycle.

| Area | Status | Summary |
|---|---|---|
| Visual design | Strong | Distinctive, premium and responsive; suitable for a client presentation. |
| Content clarity | Strong | Services, clinician, process and location are easy to understand. |
| Conversion | Needs work | Clear CTAs, but the form intentionally sends no data and phone/WhatsApp are absent. |
| Accessibility | Good foundation | Semantic structure, labels, focus styles and reduced motion pass; modal focus handling needs completion. |
| SEO | Needs work | Title, description and heading structure exist; canonical, social metadata and schema are missing. |
| Performance | Needs work | Lightweight HTML and hero WebP, but two PNG assets total about 3.8 MB. |
| Deployment | Ready | Repository-level Vercel configuration correctly publishes `dist/`. |

## 1. Current public website baseline

The live website was reviewed on 26 September 2026 at [wiltondental.co.uk](https://wiltondental.co.uk/).

### Verified issues

1. **Unfinished clinician biographies reduce trust.** Five visible staff profiles still contain raw Lorem Ipsum copy. This is especially damaging on a healthcare website, where clinician identity and credentials influence patient confidence.
2. **Several service descriptions contain avoidable copy errors.** Examples visible on the homepage include “Meal-free with no mercury,” “ROOT CANAL TREAT,” “Loose the nerve, not the tooth,” and inconsistent capitalization. These weaken clinical credibility.
3. **The service architecture is fragmented.** Important services appear as a long undifferentiated list, while the main navigation exposes only a small subset of the offer.
4. **The primary conversion journey is unclear.** Contact links and a form exist, but there is no strongly guided consultation path explaining what happens next.
5. **The visual system feels template-led.** Inconsistent imagery, spacing and content density make the practice feel less established than its actual service range suggests.

### Existing strengths worth preserving

- Central Victoria/Westminster location.
- NHS, independent and private positioning.
- Evening and weekend availability.
- Dental finance messaging.
- Broad service range including implants, oral surgery, orthodontics, hygiene and sedation.
- Published telephone and WhatsApp contact routes on the [contact page](https://wiltondental.co.uk/contact/).

## 2. Redesigned prototype assessment

### What now works well

- **Clear proposition:** the opening message immediately communicates modern, human-centred central London dentistry.
- **Stronger visual credibility:** the editorial typography, treatment cards, motion system and 3D dental artwork give the practice a memorable premium identity.
- **Better clinician presentation:** Dr Wale Towolawi’s portrait is clear on desktop and mobile, with credentials and role presented beside it.
- **Improved information hierarchy:** treatments, technology, clinician, care journey and location each have a distinct section.
- **Consistent conversion cues:** consultation buttons are repeated at appropriate decision points without overwhelming the page.
- **Responsive behaviour:** the design was visually checked at desktop and 390 × 844 mobile dimensions. The navigation, portrait, 3D section and booking modal remain legible.
- **Motion safety:** `prefers-reduced-motion` is respected, disabling decorative animation and transitions for users who request it.
- **Clean runtime:** browser testing found no console errors or warnings and all local images loaded successfully.

## 3. Accessibility audit

### Confirmed passes

- One descriptive `<h1>` followed by a logical `<h2>`/`<h3>` hierarchy.
- `<header>`, `<nav>`, `<main>` and `<footer>` landmarks are present.
- All three content images have meaningful alternative text.
- Every booking input, select and textarea has a programmatic label.
- Required fields are marked with native `required` attributes.
- Global `:focus-visible` styling is present.
- The modal has `role="dialog"`, `aria-modal="true"` and an accessible title.
- Escape closes the booking modal.
- Reduced-motion preferences are supported.

### Remaining accessibility work

| Priority | Finding | Recommendation |
|---|---|---|
| P1 | Keyboard focus is not trapped inside the open modal. | Add a focus trap, keep Tab/Shift+Tab within the dialog, and return focus to the CTA that opened it. |
| P1 | No automated colour-contrast measurement has been completed. | Run axe and Lighthouse against the deployed production URL and correct any WCAG AA failures. |
| P2 | Several non-form buttons inherit the default `type="submit"`. | Add `type="button"` to navigation and modal-launch buttons for safer reuse. |
| P2 | The combined “Phone or email” field uses `autocomplete="email"`. | Split phone and email, or remove the misleading autocomplete value and validate the accepted formats clearly. |

## 4. Conversion and content audit

### Highest-impact launch blockers

1. **The appointment form is demonstrative only.** Submission is prevented in JavaScript and displays a success state without sending the request. This is appropriate for a pitch prototype but must never be presented as a live booking channel.
2. **No click-to-call or WhatsApp action is present.** These are already published by the practice and should be visible in the header, mobile navigation and final contact section.
3. **Treatment cards are not linked to deeper information.** Production should provide dedicated, indexable pages for implants, braces, oral surgery, hygiene, cosmetic dentistry and sedation.
4. **Trust evidence is still thin.** Add verified registration details, genuine testimonials/review links, finance terms, accepted-patient status, clinician biographies and authentic practice photography.
5. **The prototype copy needs stakeholder verification.** Claims about services, opening availability, NHS intake, qualifications and finance must be approved by the practice before publication.

### Recommended appointment flow

1. Patient selects a treatment or general consultation.
2. Patient chooses a contact preference and suitable time window.
3. Submission reaches the practice CRM, booking platform or monitored inbox.
4. Patient receives a clear acknowledgement containing expected response time and urgent-care guidance.
5. Analytics records the CTA source and successful submission without capturing sensitive free-text content.

## 5. SEO and local discovery

### Confirmed foundation

- Descriptive page title: `Wilton Dental Practice | Victoria, London`.
- Relevant meta description covering location and priority services.
- One visible H1 and coherent supporting headings.
- Address and geographic area appear prominently in page copy.
- Human-readable anchor links and clean Vercel URLs.

### Missing production elements

| Priority | Missing element | Recommendation |
|---|---|---|
| P1 | Canonical URL | Add the final production-domain canonical tag. |
| P1 | Local business structured data | Add validated `Dentist`/`LocalBusiness` JSON-LD with approved name, address, telephone, URL, hours and map/profile references. |
| P1 | Dedicated service pages | Create unique pages for the principal treatments and connect them through internal links. |
| P1 | Robots and sitemap files | Add `robots.txt` and `sitemap.xml` after final routes are confirmed. |
| P2 | Open Graph and social-card metadata | Add `og:title`, `og:description`, `og:image`, Twitter card metadata and a purpose-built sharing image. |
| P2 | Local trust signals | Link the verified Google Business Profile, professional registrations and authoritative review sources. |

## 6. Performance audit

The page HTML is approximately 49 KB and the existing practice hero image is an efficient 55 KB WebP. The two presentation-quality PNGs are the main performance risk:

- `dr-wale-enhanced.png`: approximately **2.00 MB**.
- `tooth-sculpture.png`: approximately **1.78 MB**.

### Recommendations

1. Convert both PNG assets to appropriately sized AVIF/WebP derivatives, retaining PNG only where transparency quality requires it.
2. Provide responsive `srcset` sizes so mobile devices do not download desktop-scale artwork.
3. Lazy-load below-the-fold clinician and sculpture images and set `decoding="async"`.
4. Preload only the true largest-contentful image and avoid preloading decorative content.
5. Add long-lived immutable caching for hashed production assets; the current Vercel configuration already supplies long-lived caching for `/assets/`.
6. Run Lighthouse and Core Web Vitals measurement on the final Vercel production URL. No synthetic score is claimed in this report because the audited build is currently running locally.

## 7. Privacy, security and operational readiness

- The current form explicitly states that no details are sent; this is correct for the prototype.
- Before enabling submission, define the data recipient, retention policy, access controls and deletion process.
- Avoid inviting unnecessary health information in an unstructured textarea until the practice has completed an appropriate privacy review.
- Add an accessible privacy notice link beside the form and explain how follow-up will occur.
- Add spam protection that does not create a disproportionate accessibility barrier.
- Configure production error monitoring and confirm that failed enquiries are visible to staff.

## 8. Deployment audit

The repository now includes a root `vercel.json` with `outputDirectory` set to `dist`. The configured output exists and contains `index.html` and all referenced assets. This resolves the repository-layout mismatch that previously prevented Vercel from identifying the publishable site.

Recommended Vercel project settings:

- Root Directory: repository root.
- Framework Preset: Other.
- Build Command: none required for the current static prototype.
- Output Directory: controlled by `vercel.json` as `dist`.
- Production branch: `main`.

Reference: [Vercel project configuration](https://vercel.com/docs/project-configuration/vercel-json) and [configuring a build](https://vercel.com/docs/builds/configure-a-build).

## 9. Prioritized roadmap

### P0 — before any live patient traffic

- Connect and end-to-end test the appointment form.
- Add phone and WhatsApp alternatives.
- Verify every clinical, availability, NHS and finance claim with the practice.
- Publish privacy information and establish an enquiry-handling process.

### P1 — before public launch

- Compress and responsively serve the two large PNG assets.
- Complete modal keyboard focus handling.
- Add canonical, JSON-LD, sitemap, robots and social metadata.
- Add real clinician/team content and verified trust evidence.
- Create core treatment landing pages.
- Run Lighthouse, axe and cross-browser testing on the production URL.

### P2 — first optimization cycle

- Connect privacy-safe conversion analytics.
- A/B test CTA wording and contact-route prominence.
- Add review/testimonial modules backed by verifiable sources.
- Build an emergency-care route and location-specific search content.
- Review real search, booking and call data after 30–60 days.

## Final assessment

The prototype successfully demonstrates the value of a redesign: it is clearer, more distinctive and more trustworthy than the current public site. Its strongest sales story is not animation alone; it is the combination of improved clinician visibility, a calmer care journey, more deliberate service presentation and a much stronger first impression.

With the P0 and P1 work completed, this design can move from an excellent pitch prototype to a credible, measurable and operationally safe production website.

