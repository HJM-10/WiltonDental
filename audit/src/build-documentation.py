"""A4 project audit and implementation report. Evidence is read from verification.json."""
from pathlib import Path
import json, sys
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from content import TREATMENTS,TEAM
OUT=ROOT/'output/pdf/Wilton-Dental-Project-Report.pdf';OUT.parent.mkdir(parents=True,exist_ok=True)
QA=json.loads((ROOT/'docs/verification.json').read_text())
NAVY=colors.HexColor('#143b59');BLUE=colors.HexColor('#066789');MUTED=colors.HexColor('#526777');PALE=colors.HexColor('#edf4f8');LINE=colors.HexColor('#d5e2e9')
for name,file in [('Body','arial.ttf'),('Body-Bold','arialbd.ttf'),('Display','georgia.ttf')]:pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Body-Bold',italic='Body',boldItalic='Body-Bold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyCopy',fontName='Body',fontSize=10,leading=15,textColor=NAVY,spaceAfter=10))
styles.add(ParagraphStyle(name='SmallCopy',fontName='Body',fontSize=8,leading=11.5,textColor=MUTED,spaceAfter=8))
styles.add(ParagraphStyle(name='SectionTitle',fontName='Display',fontSize=23,leading=29,textColor=NAVY,spaceAfter=20))
styles.add(ParagraphStyle(name='Subhead',fontName='Body-Bold',fontSize=11,leading=16,textColor=BLUE,spaceBefore=12,spaceAfter=8,keepWithNext=True))
styles.add(ParagraphStyle(name='Kicker',fontName='Body-Bold',fontSize=8,leading=12,textColor=BLUE,spaceAfter=13))
styles.add(ParagraphStyle(name='Cell',fontName='Body',fontSize=8,leading=11,textColor=NAVY,spaceAfter=0))
styles.add(ParagraphStyle(name='HeadCell',fontName='Body-Bold',fontSize=8,leading=11,textColor=colors.white,spaceAfter=0))
styles.add(ParagraphStyle(name='Cover',fontName='Display',fontSize=33,leading=41,textColor=NAVY,spaceAfter=22))
W,H=A4;M=48;CW=W-M*2
story=[]
def p(text,style='BodyCopy'):return Paragraph(text,styles[style])
def add(text,style='BodyCopy'):story.append(p(text,style))
def heading(num,title):
    if story:story.append(PageBreak())
    add(f'WILTON DENTAL / PROJECT DOCUMENTATION / {num:02d}','Kicker');add(title,'SectionTitle')
def sub(title):add(title,'Subhead')
def table(headers,rows,widths,compact=False):
    data=[[p(escape(h),'HeadCell') for h in headers]]+[[p(str(x),'Cell') for x in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9),('LINEBELOW',(0,1),(-1,-1),.45,LINE),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE])]))
    if compact:t.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    story.append(t);story.append(Spacer(1,12))
def figure(file,caption,width=CW,maxheight=350):
    f=ROOT/file;im=PILImage.open(f);w,h=im.size;scale=min(width/w,maxheight/h)
    story.append(KeepTogether([Image(str(f),width=w*scale,height=h*scale,hAlign='LEFT'),Spacer(1,7),p(caption,'SmallCopy')]))
def page(c,doc):
    c.setTitle('Wilton Dental - Website Audit and Project Documentation');c.setAuthor('Wilton Dental project team')
    if doc.page>1:
        c.setFont('Body',8);c.setFillColor(MUTED);c.drawString(M,H-30,'WILTON DENTAL  |  WEBSITE AUDIT & IMPLEMENTATION')
        c.setStrokeColor(LINE);c.setLineWidth(.5);c.line(M,36,W-M,36);c.drawString(M,23,'26 September 2026  /  Version 2.1');c.drawRightString(W-M,23,str(doc.page))

story.append(Image(str(ROOT/'dist/assets/wilton-original-logo.png'),width=69,height=63,hAlign='LEFT'));story.append(Spacer(1,24))
add('PROJECT RECORD / VERSION 2.1 / 26 SEPTEMBER 2026','Kicker')
add('Wilton Dental<br/>Website audit &amp;<br/>project documentation','Cover')
add('A source-backed record of the multi-page redevelopment, visual and interaction design, quality checks and requirements for public launch.')
figure('audit/screenshots/rebuild/home-desktop.png','Redesigned homepage. Local implementation captured on 26 September 2026.',maxheight=280)
story.append(Spacer(1,16))
table(['Prepared for','Document purpose'],[['Project collaborators','Internal review, design decisions, implementation handover and launch planning.']],[145,CW-145])
add('Status: functional local redesign preview. Public launch remains subject to practice content approval and operational checks.','SmallCopy')

heading(1,'Contents & document control')
contents=[('1','Contents & document control','2'),('2','Executive assessment & methodology','3'),('3','Baseline findings','4'),('4','Information architecture','5'),('5','Brand & visual comparison','6'),('6','Treatment & team completeness','7'),('7','Patient journeys & contact','8'),('8','Motion & 3D experience','9'),('9','Verification results','10'),('10','Technical handover & performance','11'),('11','Launch requirements & ownership','12'),('12','Sources & asset provenance','13'),('13','Route inventory','14')]
table(['Section','Title','Page'],contents,[47,CW-87,40])
sub('Document control')
add('This report supersedes the earlier audit that described the single-page prototype as pitch-ready. That assessment was too broad: it did not establish content completeness, reliable appointment handling or sufficient evidence for the visual claims.')
add('The current document separates verified implementation behaviour from unresolved practice information. It is a conventional project report, with findings, evidence, technical records and launch responsibilities.')
add('Evidence files: docs/sources/*.json, docs/sources/assets.json, docs/routes.json, docs/verification.json and audit/screenshots/rebuild/.','SmallCopy')

heading(2,'Executive assessment & methodology')
sub('Assessment')
add('The project has been rebuilt from a single promotional page into a navigable static website with 28 content pages and a dedicated not-found page. It retains Wilton Dental’s existing logo and brings back the service breadth, published staff identities and contact pathways that were missing from the earlier prototype.')
add('The design combines a stronger blue visual identity, editorial typography, a visible interactive tooth and purposeful page transitions. A source-image explorer lets visitors switch between panoramic and CBCT examples. Text remains available without animation or JavaScript, and reduced-motion preferences use a static tooth image.')
sub('What is complete')
add('Dedicated pages cover all 13 named dental, skin and wellbeing treatments identified in the reviewed sources, plus imaging. The site includes a six-person team directory and individual profiles, care and fee information, practice information, contact routes and a directly embedded practice map. A repeatable build and browser verification script accompany the output.')
sub('What is not a launch approval')
add('The website is a review preview, not a replacement for clinical or operational sign-off. Five source biographies remain incomplete; registration information, current availability, fees, finance terms, service arrangements, privacy and complaints information require approval. There is no booking backend and no claim that an appointment has been submitted or reserved.')
sub('Method')
add('Public practice pages were reviewed and saved on 26 September 2026. Their names, roles, images, contact details and service listings informed the inventory. The earlier repository revision 62fc513 provides the prototype baseline. Browser checks cover the generated routes, local assets, accessibility rules, responsive widths, navigation and interactive states. Selected screenshots were inspected visually.')
add('Limitations: automated checks do not certify WCAG compliance. Testing here used Chrome on the local server; Safari, Firefox, real touch devices, assistive technology and a public production environment need separate validation. Contact destinations were inspected but no message, call or patient enquiry was sent.','SmallCopy')

heading(3,'Baseline findings')
table(['ID / priority','Observed issue','Impact and response'],[
('B01 / High','The earlier prototype contained one page and six unlinked service cards.','Patients could not explore the complete service offer. Dedicated, linked pages now provide a consistent information structure.'),
('B02 / High','The original logo was replaced by a letter W mark.','Brand continuity was lost. The original practice logo is now used in the header and favicon.'),
('B03 / High','Only one clinician appeared in the earlier prototype.','The team was underrepresented. All six published members have directory entries and profiles.'),
('B04 / High','The prototype form presented a success state without sending data.','Visitors could mistakenly believe an enquiry had reached the practice. The rebuild uses direct contact channels with explicit appointment-confirmation wording.'),
('B05 / Medium','User-reported clipped moving headings and low-contrast photograph overlays.','The rebuild removes horizontal text translation and uses stable text layouts with readable foreground/background combinations.'),
('B06 / Medium','The live site contains placeholder text in five biographies.','Those paragraphs are not reproduced. Profiles use published identity information and short, general role context.'),
('B07 / Medium','The live pages publish seasonal offers and different contact details on the implant page.','The contact page landline and WhatsApp are the primary routes; no seasonal offer is promoted as an evergreen fee.'),
('B08 / Medium','The first rebuild was too visually restrained in user review.','The revised homepage introduces prominent 3D, richer blue surfaces, staged entrances and an interactive imaging example.'),
],[75,190,CW-265])
add('Priorities describe impact on this project, not a regulatory determination. Public-site evidence is preserved under docs/sources; user-reported defects are distinguished from independently measured findings.','SmallCopy')

heading(4,'Information architecture')
add('Shared navigation leads to genuine URLs, not unrelated anchors or a generic booking modal. The homepage introduces key pathways, while detailed pages preserve readable treatment and team information.')
table(['Area','Pages','Purpose'],[
('Home','1','Visual introduction, treatment pathways, the team, imaging examples and contact entry.'),
('Our practice','1','Practice overview, visit preparation and access enquiry guidance.'),
('Treatments','14','Directory plus 13 individual dental, skin and wellbeing treatment pages.'),
('Our team','7','Full directory plus six individual profiles.'),
('Imaging','1','OPG and CBCT information, referral enquiries and the tooth visualisation.'),
('NHS & private care','1','Explain listed pathways and prompt confirmation of availability.'),
('Fees & finance','1','Explain estimates and questions to ask without inventing a price list.'),
('Contact','1','Landline, email, WhatsApp, address, map and urgent-care information.'),
('Website information','1','Preview privacy behaviour and outstanding launch information.'),
('Not found','1','A recovery page with working navigation.'),
],[120,45,CW-165])
sub('Page conventions')
add('Each generated page has a unique title and description, one primary heading, a main content landmark and consistent footer links. Inner pages include breadcrumbs. Treatment pages combine a real source image, an overview, expected stages, one common question, related care and a contact route that preserves the selected treatment in the URL.')
sub('Preview indexing')
add('The current output intentionally uses noindex and a disallowing robots file. A verified production hostname, canonical metadata and sitemap belong in the launch pass after practice approval; the preview should not compete with the live practice site.')

heading(5,'Brand & visual comparison')
add('The original blue-and-silver identity is retained. The redesign extends it through deep navy, a restrained cyan accent, pale blue surfaces and locally hosted typography. It avoids the previous neon-green accent and keeps the real logo intact.')
figure('audit/screenshots/current-home-hero.png','Figure 1. Existing public homepage, captured earlier on the same project date. Use docs/sources/home.json for the source-content record.',maxheight=225)
figure('audit/screenshots/rebuild/home-desktop.png','Figure 2. Revised homepage: a clearer visual hierarchy and a prominent interactive tooth. This screenshot represents the local build.',maxheight=225)
add('The comparison demonstrates layout and hierarchy, not a measured increase in conversion. Real practice imagery remains available in the opening practice link and on the practice page. No synthetic staff photographs are used.','SmallCopy')

heading(6,'Treatment & team completeness')
sub('Treatment inventory')
add('Every named service found in the reviewed practice pages has a destination: white fillings, dental implants, invisible braces, root canal treatment, dental hygiene, wisdom-tooth care, conscious sedation, smile makeovers, teeth whitening, facial aesthetics, stress therapy, microdermabrasion and microneedling. OPG and CBCT imaging have their own page.')
add('Treatment imagery is retained from the practice sources. Where a source has no dedicated picture, a related source illustration is reused and described as illustrative. The wording avoids guaranteed results and directs individual suitability, risk and cost questions to a consultation.')
table(['Published team member','Role shown in rebuild','Content status'],[(t['name'],t['role'],'Published biography and qualifications retained in summary.' if i==0 else 'Name, role and photo retained; personal biography awaiting practice input.') for i,t in enumerate(TEAM)],[130,140,CW-270])
sub('Specific discrepancies to resolve')
add('Tinu Oloyede’s source heading says Dental Nurse while its image alternative text says Trainee Dental Nurse. The rebuild uses the neutral label Dental nursing team until the practice confirms the current title. Namitha Shibu is presented with the source’s Dr title and Dental therapist role; current professional titles and registration details require practice verification.')

heading(7,'Patient journeys & contact')
sub('Treatment enquiry')
add('Directory → treatment page → contact page → chosen contact channel. The treatment selection is carried to the contact page as a short context message. It is never represented as a submitted enquiry. A caller or sender must agree an appointment with the practice.')
sub('Find the practice')
add('The homepage and contact page display the exact Google Maps embed URL used by the practice website, together with the postal address and direct directions link. The map loads automatically near the viewport. No extra activation button is required. Contact details include the published landline, WhatsApp and practice email.')
table(['Channel','Published destination'],[('Landline','020 7834 6361'),('WhatsApp','+44 7378 776626'),('Email','info@wiltondental.co.uk'),('Location','63a Wilton Road, Victoria, London SW1V 1DE')],[95,CW-95])
figure('audit/screenshots/rebuild/map-desktop.png','Figure 3. The homepage visibly embeds the same practice map used by the original website.',maxheight=235)
add('Loading the map connects the visitor’s browser to Google; the website information page explains this behaviour. Direct contact links depend on the visitor’s configured applications. No enquiry was sent during verification.','SmallCopy')

heading(8,'Motion & 3D experience')
table(['Experience','Purpose','Control / fallback'],[
('Staged headline entrance','Establish hierarchy in the opening view.','Short one-time transform/opacity animation; reduced-motion override.'),
('Orbital motion and tooth rotation','Make the opening visually distinctive.','Pause motion and Pause rotation controls; reduced-motion and data-saving fallbacks.'),
('Scroll entrances','Introduce card groups and sections.','Intersection-based, one-time animations; content is visible without JavaScript.'),
('Card hover and focus','Signal that cards lead to detail pages.','Small elevation and image scaling; visible keyboard focus remains independent.'),
('OPG / CBCT explorer','Let visitors compare two published imaging examples.','Native buttons update the image, description and pressed state.'),
('Reading progress','Indicate progress through the document.','A lightweight scroll indicator and an underline on the care statement.'),
('Four-stage care journey','Restore the preferred conversation, assessment, choice and support narrative.','Numbered vertical timeline with scroll progress; all text remains visible and reduced motion is supported.'),
],[115,165,CW-280])
sub('Tooth implementation')
model=(ROOT/'dist/assets/tooth.glb').stat().st_size
add(f'The original stylised mesh is a local glTF binary ({model:,} bytes; approximately {model/1024:.0f} KiB), with 12,352 vertices and 24,192 triangles. It uses an untextured porcelain material, so no large model textures are downloaded. It is visual artwork, not a patient scan or a clinically accurate anatomy model.')
add('Three.js r180 modules are locally hosted. Loading begins as the viewer approaches the viewport. Rotation uses a capped render interval and stops when the viewer is offscreen or the document is hidden. Pixel density is capped at 1.5. Pointer dragging and keyboard-operable buttons provide control; a reset returns the view to its starting orientation.')
add('Reduced motion, data-saving mode and a failed model request retain the static illustration. WebGL context loss also returns to the fallback. The existing fallback artwork differs from the interactive mesh; a matched render can replace it in a later asset-refinement pass.','SmallCopy')

heading(9,'Verification results')
violations=sum(len(p['a11y']) for p in QA['pages']);overflows=sum(len(p['overflow']) for p in QA['pages'])
table(['Check','Recorded result'],[
('Generated route coverage',f'{len(QA["pages"])} routes loaded with HTTP 200 in the local server, including the not-found design route.'),
('Document structure','One h1 per checked route; no Lorem Ipsum in rendered content.'),
('Responsive widths',f'1440, 768, 390 and 320 CSS pixels; {overflows} horizontal-overflow findings.'),
('Automated accessibility',f'axe-core 4.10.3, WCAG 2 A/AA and 2.1 AA tags; {violations} recorded rule violations.'),
('Local links and assets','Generated internal destinations exist; referenced local images and scripts are fetched by the verification script.'),
('JavaScript errors',f'{len(QA["errors"])} errors recorded in the verification run.'),
],[165,CW-165])
sub('Interaction checks')
for check in QA['interactionChecks']:add('• '+escape(check),'SmallCopy')
sub('Interpretation')
add('These results describe the recorded local build and test conditions. A clean automated result is not a declaration of accessibility conformance. Keyboard use, reading order, real-device performance and assistive-technology testing need a dedicated production review.')
add('Reproduce: run scripts/build.py, start the local static server on port 4173 and run scripts/verify.cjs. Full per-page findings are stored in docs/verification.json. Screenshot evidence is under audit/screenshots/rebuild/.','SmallCopy')

heading(10,'Technical handover & performance')
table(['Location','Responsibility'],[
('src/content.py','Treatment data, team identities, source-backed profile copy and related-care links.'),
('scripts/build.py','Shared templates, page assembly and the route manifest.'),
('src/site.css','Responsive visual system, brand tokens, animation and print styles.'),
('src/site.js','Navigation, filtering, journey progress, imaging explorer and viewer loading.'),
('src/tooth-viewer.js','Rendering, controls, pause/resume, lifecycle handling and fallback.'),
('scripts/build_tooth.py','Reproducible original tooth mesh and static-poster optimisation.'),
('dist/','Generated, self-contained static website output, including local images, fonts and 3D dependencies.'),
('docs/ and audit/','Sources, verification records, screenshots and report builder.'),
],[155,CW-155])
sub('Build and serve')
add('<b>Build:</b> python scripts/build.py<br/><b>Preview:</b> python -m http.server 4173 --directory dist<br/><b>Browser checks:</b> node scripts/verify.cjs')
sub('Performance decisions')
add('The site serves ordinary HTML for every route. The core interface has no client framework. Images and fonts are local, images below the opening view load lazily, and 3D modules are not requested by pages without a viewer. The Google map uses native lazy loading. No performance score or Core Web Vitals claim is made without a production measurement.')
add('The font files currently prioritise typographic fidelity over minimum transfer size. A further WOFF2 subset pass, immutable content-hashed assets and field measurements are sensible deployment improvements. The three.js distribution retains its MIT licence; fonts retain their SIL Open Font licences.')
sub('Rollback')
add('The prior prototype is preserved in repository history at 62fc513; the starting homepage and report were also copied into tmp/baseline. The main workflow writes generated pages without changing the Git remote or publishing to the public practice domain.')

heading(11,'Launch requirements & ownership')
add('The following items must be resolved before treating this as the practice’s public operational website. They are not hidden behind a successful visual or automated check.')
table(['Priority','Requirement','Owner'],[
('High','Approve every service page for clinical accuracy, scope, risks and wording.','Practice clinical lead'),
('High','Confirm all six staff identities, roles, qualifications, registration details, photos and biographies. Resolve the Tinu role discrepancy.','Practice manager / clinical lead'),
('High','Confirm current NHS intake, appointment times, accessibility arrangements, prices, finance provider and finance terms.','Practice manager'),
('High','Approve contact destinations; resolve the separate implant-page mobile/email details and external aesthetics-provider arrangement.','Practice manager'),
('High','Provide the final privacy notice, complaints procedure and applicable practice/regulatory information.','Practice owner / adviser'),
('High','Confirm publication rights for source images and any identifiable people shown.','Practice owner'),
('Medium','Run keyboard, screen-reader, Safari/Firefox and real-device checks against the intended production environment.','Delivery team'),
('Medium','Connect a booking platform only if a real workflow, consent wording and confirmation behaviour are agreed.','Practice manager / developer'),
('Medium','Approve deployment; configure production hostname, canonical URLs, sitemap, redirects and indexing.','Site owner / developer'),
('Medium','Measure page performance after deployment and monitor broken links, errors and enquiry routes.','Delivery team'),
],[53,335,CW-388])
add('Suggested acceptance: the practice signs off content and contact routes; the delivery team records final accessibility, browser and deployment checks; the site owner approves publication. The current deliverable remains a reviewable local implementation until that process is complete.','SmallCopy')

heading(12,'Sources & asset provenance')
add('Practice content and original imagery were retrieved on 26 September 2026. The source register records what was available at that time; it is not an independent verification of registration or clinical claims.')
sources=[
('S01','Practice homepage','https://wiltondental.co.uk/','Service inventory, team names/roles and source images.'),
('S02','Contact','https://wiltondental.co.uk/contact/','Address, landline and WhatsApp.'),
('S03','Dr Wale Towolawi','https://wiltondental.co.uk/dr-wale-towolawi/','Published biography, qualifications and GDC number.'),
('S04','Whitening','https://wiltondental.co.uk/whitening/','Named whitening options and seasonal pricing evidence.'),
('S05','Imaging','https://wiltondental.co.uk/imaging/','OPG, CBCT, imaging assets and practice email.'),
('S06','Implants','https://wiltondental.co.uk/implants/','Implant offer limitations and alternate contact details.'),
('S07','Skin services','https://wiltondental.co.uk/microdermabrasion/','Microdermabrasion, microneedling and email.'),
]
for id,title,url,note in sources:add(f'<b>{id} - {title}.</b> <link href="{url}" color="#066789">{url}</link><br/>{note}','SmallCopy')
sub('Patient-information references')
for title,url in [('NHS dental treatments','https://www.nhs.uk/live-well/healthy-teeth-and-gums/dental-treatments/'),('NHS root canal treatment','https://www.nhs.uk/tests-and-treatments/root-canal-treatment/'),('NHS teeth whitening','https://www.nhs.uk/tests-and-treatments/teeth-whitening/'),('Guy’s and St Thomas’ dental implants','https://www.guysandstthomas.nhs.uk/health-information/dental-implants'),('Guy’s and St Thomas’ sedation options','https://www.guysandstthomas.nhs.uk/health-information/sedation-options-dental-treatment')]:add(f'<b>{escape(title)}</b><br/><link href="{url}" color="#066789">{url}</link>','SmallCopy')
sub('Asset record')
add('docs/sources/assets.json maps downloaded practice images to their original URLs. The original logo is unmodified. Team photographs use the public source files rather than generated likenesses. The new tooth mesh is original procedural artwork; the fallback sculpture is retained from the earlier project. Image publication rights remain a practice approval item.','SmallCopy')

heading(13,'Route inventory')
routes=json.loads((ROOT/'docs/routes.json').read_text())
table(['Page','Route'],[(escape(r['title']),r['path']) for r in routes],[210,CW-210],compact=True)

doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=M,leftMargin=M,topMargin=54,bottomMargin=51,title='Wilton Dental - Website Audit and Project Documentation',author='Wilton Dental project team')
doc.build(story,onFirstPage=page,onLaterPages=page)
print(OUT)
