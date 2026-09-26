from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, Color, white, black
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "audit"
SHOTS = AUDIT / "screenshots"
LOGOS = ROOT / "brand" / "logo-concepts" / "previews"
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)
PDF_PATH = OUT / "Wilton-Dental-Website-Audit.pdf"

W, H = landscape(A4)

NAVY = HexColor("#061F2D")
NAVY_2 = HexColor("#0B3446")
INK = HexColor("#102D3A")
CREAM = HexColor("#F4F7F3")
PAPER = HexColor("#FBFCF9")
MINT = HexColor("#81EAD8")
LIME = HexColor("#D7875F")
GREY = HexColor("#6F7E83")
LINE = HexColor("#D7E0DC")
SOFT = HexColor("#E9F5F1")
PINK = HexColor("#F4D9E6")

pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("ArialBold", "C:/Windows/Fonts/arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Georgia", "C:/Windows/Fonts/georgia.ttf"))
pdfmetrics.registerFont(TTFont("GeorgiaItalic", "C:/Windows/Fonts/georgiai.ttf"))

styles = {
    "body": ParagraphStyle("body", fontName="Arial", fontSize=10, leading=14, textColor=INK),
    "body_light": ParagraphStyle("body_light", fontName="Arial", fontSize=10, leading=14, textColor=HexColor("#D3E0E3")),
    "small": ParagraphStyle("small", fontName="Arial", fontSize=8, leading=11, textColor=GREY),
    "small_light": ParagraphStyle("small_light", fontName="Arial", fontSize=8, leading=11, textColor=HexColor("#B7C8CD")),
    "caption": ParagraphStyle("caption", fontName="ArialBold", fontSize=8, leading=10, textColor=INK),
    "center": ParagraphStyle("center", fontName="Arial", fontSize=9, leading=12, alignment=TA_CENTER, textColor=INK),
}


def ptop(c, text, x, top, width, style="body", height=500):
    p = Paragraph(text, styles[style])
    _, ph = p.wrap(width, height)
    p.drawOn(c, x, top - ph)
    return top - ph


def draw_cover_image(c, path, x, y, w, h, radius=0, darken=0):
    image = Image.open(path)
    iw, ih = image.size
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    dx, dy = x + (w - dw) / 2, y + (h - dh) / 2
    c.saveState()
    clip = c.beginPath()
    if radius:
        clip.roundRect(x, y, w, h, radius)
    else:
        clip.rect(x, y, w, h)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(ImageReader(image), dx, dy, dw, dh, preserveAspectRatio=True, mask="auto")
    if darken:
        c.setFillColor(Color(0.02, 0.12, 0.17, alpha=darken))
        c.rect(x, y, w, h, stroke=0, fill=1)
    c.restoreState()


def draw_contain_image(c, path, x, y, w, h, radius=0, bg=CREAM):
    image = Image.open(path)
    iw, ih = image.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    dx, dy = x + (w - dw) / 2, y + (h - dh) / 2
    c.saveState()
    clip = c.beginPath()
    if radius:
        clip.roundRect(x, y, w, h, radius)
    else:
        clip.rect(x, y, w, h)
    c.clipPath(clip, stroke=0, fill=0)
    c.setFillColor(bg); c.rect(x,y,w,h,stroke=0,fill=1)
    c.drawImage(ImageReader(image), dx, dy, dw, dh, preserveAspectRatio=True, mask="auto")
    c.restoreState()


def header(c, kicker, title, page, dark=False):
    color = white if dark else INK
    sub = MINT if dark else GREY
    c.setFillColor(sub)
    c.setFont("ArialBold", 7.5)
    c.drawString(36, H - 34, kicker.upper())
    c.setFillColor(color)
    c.setFont("Georgia", 24)
    c.drawString(36, H - 62, title)
    c.setFillColor(sub)
    c.setFont("Arial", 7)
    c.drawRightString(W - 36, H - 34, f"WILTON DENTAL  /  {page:02d}")


def footer(c, source="Visual audit • 26 September 2026", dark=False):
    c.setFillColor(HexColor("#A9BBC0") if dark else GREY)
    c.setFont("Arial", 6.8)
    c.drawString(36, 20, source)


def pill(c, text, x, y, bg=LIME, fg=NAVY, w=None):
    c.setFont("ArialBold", 7.5)
    if w is None:
        w = pdfmetrics.stringWidth(text.upper(), "ArialBold", 7.5) + 24
    c.setFillColor(bg)
    c.roundRect(x, y, w, 22, 11, stroke=0, fill=1)
    c.setFillColor(fg)
    c.drawCentredString(x + w / 2, y + 7.2, text.upper())
    return w


def number_marker(c, n, x, y, color=LIME):
    c.setFillColor(color)
    c.circle(x, y, 10, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.setFont("ArialBold", 8)
    c.drawCentredString(x, y - 2.7, str(n))


def bullet_list(c, items, x, top, width, dark=False, gap=11, size=9):
    style = ParagraphStyle(
        "bullet_light" if dark else "bullet",
        fontName="Arial",
        fontSize=size,
        leading=size + 4,
        textColor=HexColor("#D4E1E4") if dark else INK,
    )
    y = top
    for item in items:
        c.setFillColor(LIME if dark else NAVY)
        c.circle(x + 4, y - 6, 2.6, stroke=0, fill=1)
        p = Paragraph(item, style)
        _, ph = p.wrap(width - 18, 100)
        p.drawOn(c, x + 16, y - ph)
        y -= ph + gap
    return y


def score_bar(c, label, old, new, x, y, width=220):
    c.setFillColor(INK)
    c.setFont("ArialBold", 8)
    c.drawString(x, y + 7, label)
    track_x = x + 82
    track_w = width - 82
    c.setFillColor(LINE)
    c.roundRect(track_x, y, track_w, 8, 4, stroke=0, fill=1)
    c.setFillColor(HexColor("#AEBABC"))
    c.roundRect(track_x, y, track_w * old / 5, 8, 4, stroke=0, fill=1)
    c.setFillColor(LIME)
    c.roundRect(track_x, y, track_w * new / 5, 8, 4, stroke=0, fill=1)
    c.setFillColor(GREY)
    c.setFont("Arial", 6.5)
    c.drawRightString(x + width + 25, y + 1.5, f"{old} → {new}")


def page_one(c):
    c.setFillColor(NAVY); c.rect(0,0,W,H,stroke=0,fill=1)
    draw_cover_image(c, SHOTS / "prototype-precision.png", 495, 0, W - 495, H, darken=0.2)
    c.setFillColor(LIME)
    c.roundRect(46, H - 82, 46, 46, 13, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.setFont("ArialBold", 21)
    c.drawCentredString(69, H - 67, "W")
    c.setFillColor(white)
    c.setFont("ArialBold", 8)
    c.drawString(104, H - 53, "WILTON DENTAL PRACTICE")
    c.setFillColor(MINT)
    c.setFont("Arial", 7)
    c.drawString(104, H - 68, "WEBSITE EXPERIENCE AUDIT")
    c.setFillColor(white)
    c.setFont("Georgia", 36)
    c.drawString(48, 292, "From functional website")
    c.setFont("GeorgiaItalic", 36)
    c.drawString(48, 248, "to confident digital")
    c.drawString(48, 204, "front door.")
    c.setFillColor(HexColor("#C8D6D8"))
    c.setFont("Arial", 11)
    c.drawString(50, 157, "A visual review of trust, clarity, conversion and launch readiness")
    pill(c, "Client-facing audit", 50, 106, LIME, NAVY)
    c.setFillColor(white)
    c.setFont("Arial", 8)
    c.drawString(50, 80, "26 SEPTEMBER 2026")


def page_two(c):
    c.setFillColor(CREAM); c.rect(0, 0, W, H, stroke=0, fill=1)
    header(c, "Executive view", "The redesign changes the perceived quality of the practice", 2)
    c.setFillColor(NAVY)
    c.setFont("Georgia", 29)
    c.drawString(36, H - 112, "Pitch-ready today.")
    c.setFont("GeorgiaItalic", 25)
    c.drawString(36, H - 143, "Production-ready after")
    c.drawString(36, H - 173, "focused operational work.")
    ptop(c, "The redesigned concept is a significant step up in visual trust, information hierarchy, mobile presentation and clinician visibility. The remaining gaps are not design problems; they are launch integrations, verified content, technical SEO and performance optimization.", 38, H - 202, 430)
    c.setFillColor(NAVY); c.roundRect(515, H - 228, 280, 150, 24, stroke=0, fill=1)
    c.setFillColor(LIME); c.setFont("ArialBold", 8); c.drawString(540, H - 110, "THE CORE OPPORTUNITY")
    c.setFillColor(white); c.setFont("Georgia", 22); c.drawString(540, H - 144, "Make confidence visible")
    ptop(c, "The practice already offers broad care, specialist experience and flexible access. The new design finally presents those strengths with the clarity and polish patients expect.", 540, H - 165, 220, "body_light")
    c.setFillColor(INK); c.setFont("ArialBold", 8); c.drawString(38, 275, "HEURISTIC EXPERIENCE SCORE  /  5 POINT SCALE")
    scores = [("Brand clarity",2,5),("Patient trust",1,4),("Content hierarchy",2,5),("Conversion path",2,3),("Mobile experience",2,4),("Accessibility",2,4)]
    for idx, row in enumerate(scores):
        col = idx % 2; r = idx // 2
        score_bar(c, *row, 38 + col * 380, 235 - r * 50, 300)
    c.setFillColor(GREY); c.setFont("Arial", 7); c.drawString(38, 55, "Scores are expert heuristic ratings based on the audited screens and code, not automated Lighthouse results.")
    footer(c)


def page_three(c):
    c.setFillColor(PAPER); c.rect(0,0,W,H,stroke=0,fill=1)
    header(c, "Current public site", "A credible practice presented through an inconsistent template", 3)
    draw_cover_image(c, SHOTS / "current-home-hero.png", 36, 105, 485, 390, 18)
    number_marker(c, 1, 480, 455); number_marker(c, 2, 495, 130)
    pill(c, "Current experience", 48, 463, NAVY, white)
    c.setFillColor(NAVY); c.setFont("Georgia", 20); c.drawString(550, 458, "The first impression")
    c.drawString(550, 432, "is clinical,")
    c.setFont("GeorgiaItalic", 20); c.drawString(550, 404, "but not distinctive.")
    bullet_list(c, [
        "Navigation is visually crowded and lacks a clear primary patient journey.",
        "The hero establishes location and dentistry, but does not explain why this practice should be trusted or chosen.",
        "Finance dominates the lower hero while booking and contact actions compete for attention.",
        "Typography, spacing and imagery feel assembled from different systems rather than one intentional brand.",
    ], 550, 360, 240)
    c.setFillColor(NAVY); c.setFont("ArialBold", 8); c.drawString(550, 145, "BUSINESS EFFECT")
    ptop(c, "Patients may perceive a gap between the practice's clinical capability and the quality of its digital experience. In healthcare, that gap can become a trust and enquiry-conversion problem.", 550, 128, 238)
    footer(c, "Source capture: wiltondental.co.uk • 26 September 2026")


def page_four(c):
    c.setFillColor(CREAM); c.rect(0,0,W,H,stroke=0,fill=1)
    header(c, "Credibility audit", "Visible unfinished content creates avoidable doubt", 4)
    draw_cover_image(c, SHOTS / "current-team.png", 36, 140, 520, 350, 18)
    for n, x, y in [(1,115,455),(2,430,455),(3,505,250)]: number_marker(c,n,x,y)
    c.setFillColor(NAVY); c.setFont("Georgia", 22); c.drawString(585, 455, "What patients can see")
    items = [
        ("01", "Copy errors", "Service wording includes 'Meal-free with no mercury', 'ROOT CANAL TREAT' and 'Loose the nerve, not the tooth.'"),
        ("02", "Mixed visual quality", "Photography style, crop, lighting and treatment imagery vary widely across the same grid."),
        ("03", "Placeholder biographies", "Five team profiles display raw Lorem Ipsum, directly undermining clinician and staff credibility."),
    ]
    top = 410
    for num, title, body in items:
        c.setFillColor(LIME); c.setFont("ArialBold", 8); c.drawString(585, top, num)
        c.setFillColor(INK); c.setFont("ArialBold", 11); c.drawString(615, top, title)
        ptop(c, body, 615, top - 10, 175, "small")
        top -= 95
    c.setFillColor(NAVY); c.roundRect(36, 55, 756, 54, 16, stroke=0, fill=1)
    c.setFillColor(white); c.setFont("GeorgiaItalic", 14); c.drawString(58, 78, "Trust-sensitive pages cannot look unfinished. Every biography and service claim must feel deliberate.")
    footer(c, "Source capture: wiltondental.co.uk • 26 September 2026")


def page_five(c):
    c.setFillColor(NAVY); c.rect(0,0,W,H,stroke=0,fill=1)
    header(c, "Redesign direction", "A calmer, clearer and more memorable first impression", 5, dark=True)
    draw_cover_image(c, SHOTS / "prototype-home-hero.png", 36, 105, 756, 385, 20)
    for n,x,y in [(1,175,400),(2,660,430),(3,690,155)]: number_marker(c,n,x,y)
    labels = [
        ("01", "Human proposition", "Emotion-led headline balanced with specific clinical scope."),
        ("02", "Credible visual focus", "Authentic practice imagery, intentional cropping and supporting proof points."),
        ("03", "Clear conversion", "One primary consultation action, supported by exploration rather than competition."),
    ]
    for idx,(num,title,body) in enumerate(labels):
        x = 38 + idx*255
        c.setFillColor(LIME); c.setFont("ArialBold",8); c.drawString(x,80,num)
        c.setFillColor(white); c.setFont("ArialBold",10); c.drawString(x+26,80,title)
        ptop(c,body,x+26,70,205,"small_light")
    footer(c, dark=True)


def page_six(c):
    c.setFillColor(PAPER); c.rect(0,0,W,H,stroke=0,fill=1)
    header(c, "Before and after", "The redesign turns information into a guided decision", 6)
    draw_cover_image(c, SHOTS / "current-home-hero.png", 36, 190, 362, 285, 16)
    draw_cover_image(c, SHOTS / "prototype-home-hero.png", 444, 190, 348, 285, 16)
    pill(c, "Before", 50, 442, HexColor("#DDE3E2"), INK)
    pill(c, "After", 458, 442, LIME, NAVY)
    c.setFillColor(INK); c.setFont("ArialBold",9); c.drawCentredString(217,160,"TEMPLATE-LED PRESENTATION")
    c.drawCentredString(618,160,"PATIENT-LED EXPERIENCE")
    left = "Crowded navigation • generic hierarchy • inconsistent brand signals • weak path to action"
    right = "Distinct proposition • focused proof • modern visual system • deliberate consultation journey"
    ptop(c,left,60,145,315,"center"); ptop(c,right,460,145,315,"center")
    c.setFillColor(NAVY); c.setFont("GeorgiaItalic",18); c.drawCentredString(W/2,73,"The new design makes the practice feel as considered as the care it promises.")
    footer(c)


def page_seven(c):
    c.setFillColor(SOFT); c.rect(0,0,W,H,stroke=0,fill=1)
    header(c, "Clinician trust", "Move the person patients choose to the centre of the story", 7)
    draw_cover_image(c, SHOTS / "current-team.png", 36, 165, 350, 305, 18)
    draw_cover_image(c, SHOTS / "prototype-doctor.png", 420, 165, 372, 305, 18)
    pill(c, "Current", 50, 438, white, INK)
    pill(c, "Redesign", 434, 438, LIME, NAVY)
    c.setFillColor(INK); c.setFont("ArialBold",9); c.drawString(38,135,"FROM A CROWDED TEAM GRID")
    ptop(c,"Small portraits, mixed crops and unfinished biographies ask patients to work too hard to understand who is responsible for their care.",38,120,325,"small")
    c.setFont("ArialBold",9); c.drawString(422,135,"TO A CLEAR CLINICIAN MOMENT")
    ptop(c,"A confident portrait, visible credentials, concise experience statement and supporting proof create immediate reassurance.",422,120,340,"small")
    footer(c)


def page_eight(c):
    c.setFillColor(PAPER); c.rect(0,0,W,H,stroke=0,fill=1)
    header(c, "Experience system", "Service clarity supported by a signature visual moment", 8)
    draw_cover_image(c, SHOTS / "prototype-treatments.png", 36, 288, 756, 200, 18)
    draw_cover_image(c, SHOTS / "prototype-precision.png", 36, 60, 470, 200, 18)
    c.setFillColor(NAVY); c.roundRect(532,60,260,200,18,stroke=0,fill=1)
    c.setFillColor(LIME); c.setFont("ArialBold",8); c.drawString(558,225,"WHY THIS ADDS VALUE")
    c.setFillColor(white); c.setFont("Georgia",18); c.drawString(558,197,"Memorable,")
    c.setFont("GeorgiaItalic",18); c.drawString(558,174,"not ornamental")
    bullet_list(c,[
        "Treatment cards group the offer into understandable patient needs.",
        "The 3D tooth creates a recognisable visual signature for digital outreach and presentations.",
        "Motion reinforces precision while reduced-motion support keeps the experience inclusive.",
    ],554,145,215,dark=True,gap=7,size=8)
    footer(c)


def page_colour(c):
    c.setFillColor(CREAM); c.rect(0,0,W,H,stroke=0,fill=1)
    header(c, "Colour direction", "Replace neon energy with warmer confidence", 9)
    c.setFillColor(NAVY); c.setFont("Georgia",24); c.drawString(36,455,"The lime accent is energetic,")
    c.setFont("GeorgiaItalic",24); c.drawString(36,423,"but it reads more tech than care.")
    ptop(c,"The deep navy is worth keeping: it gives the site authority and makes the photography feel crisp. The accent should become warmer, quieter and more human. These three directions preserve contrast without falling back into the usual blue-and-green dental palette.",38,395,330)
    options = [
        ("01", "Warm copper", "#D7875F", HexColor("#D7875F"), "Recommended", "Human, crafted and premium. It softens the navy while remaining distinctive and works well across general, cosmetic and specialist care."),
        ("02", "Soft coral", "#FF765F", HexColor("#FF765F"), "Expressive", "Contemporary and welcoming with more personality. Best if the practice wants a slightly bolder cosmetic and lifestyle feel."),
        ("03", "Champagne gold", "#D7B66F", HexColor("#D7B66F"), "Established", "Quietly premium and assured. Especially strong for implants and specialist positioning, though it needs careful contrast treatment."),
    ]
    for idx,(num,name,hexv,color,badge,desc) in enumerate(options):
        x=395+idx*137
        c.setFillColor(color); c.roundRect(x,220,118,240,22,stroke=0,fill=1)
        c.setFillColor(NAVY if idx != 2 else HexColor("#4B1823")); c.setFont("ArialBold",8); c.drawString(x+15,430,num)
        c.setFont("Georgia",16); c.drawString(x+15,398,name)
        c.setFont("ArialBold",7); c.drawString(x+15,376,hexv)
        c.setFillColor(Color(1,1,1,alpha=.7)); c.roundRect(x+14,337,90,22,11,stroke=0,fill=1)
        c.setFillColor(NAVY); c.setFont("ArialBold",6.5); c.drawCentredString(x+59,344,badge.upper())
        body_style = ParagraphStyle(f"swatch{idx}",fontName="Arial",fontSize=7.5,leading=10,textColor=NAVY)
        p=Paragraph(desc,body_style); _,ph=p.wrap(88,120); p.drawOn(c,x+15,315-ph)
    c.setFillColor(NAVY); c.roundRect(38,72,754,110,20,stroke=0,fill=1)
    c.setFillColor(LIME); c.setFont("ArialBold",8); c.drawString(62,151,"DESIGN RECOMMENDATION")
    c.setFillColor(white); c.setFont("Georgia",18); c.drawString(62,122,"Keep navy as the anchor. Replace lime with warm copper.")
    ptop(c,"The mint can remain as a restrained supporting wash, but copper should carry buttons, highlights, orbit details and the primary logo accent.",62,105,650,"small_light")
    footer(c)


def page_logos(c):
    c.setFillColor(PAPER); c.rect(0,0,W,H,stroke=0,fill=1)
    header(c, "Identity exploration", "Three logo directions beyond the generic dental palette", 10)
    concepts = [
        ("01  WILTON RIBBON", "A continuous W and smile mark. Friendly, ownable and the strongest all-round direction.", LOGOS / "concept-01-wilton-ribbon.png", HexColor("#D7875F")),
        ("02  PORCELAIN BLOOM", "A sculptural tooth and smile form with more cosmetic energy and a bolder personality.", LOGOS / "concept-02-porcelain-bloom.png", HexColor("#FF765F")),
        ("03  VICTORIA ORBIT", "A refined evolution of the original sweeping W, recast as a premium London-practice seal.", LOGOS / "concept-03-victoria-orbit.png", HexColor("#D7B66F")),
    ]
    y_positions=[355,218,81]
    for idx,(title,desc,path,color) in enumerate(concepts):
        y=y_positions[idx]
        c.setFillColor(white); c.roundRect(36,y,500,116,16,stroke=0,fill=1)
        draw_cover_image(c,path,48,y+10,476,96,10)
        c.setFillColor(color); c.roundRect(558,y,234,116,16,stroke=0,fill=1)
        c.setFillColor(NAVY if idx < 2 else HexColor("#4B1823")); c.setFont("ArialBold",8); c.drawString(577,y+87,title)
        body_style=ParagraphStyle(f"logo{idx}",fontName="Arial",fontSize=8.5,leading=12,textColor=NAVY)
        p=Paragraph(desc,body_style); _,ph=p.wrap(195,70); p.drawOn(c,577,y+70-ph)
        if idx==0:
            c.setFillColor(white); c.roundRect(577,y+15,116,21,10,stroke=0,fill=1)
            c.setFillColor(NAVY); c.setFont("ArialBold",6.5); c.drawCentredString(635,y+22,"RECOMMENDED")
    footer(c,"Editable SVG concepts included with this audit")


def page_nine(c):
    c.setFillColor(NAVY); c.rect(0,0,W,H,stroke=0,fill=1)
    header(c, "Responsive design", "The visual impact survives the smaller screen", 11, dark=True)
    draw_contain_image(c, SHOTS / "prototype-mobile-hero.png", 65, 70, 235, 420, 24, NAVY_2)
    draw_contain_image(c, SHOTS / "prototype-mobile-doctor.png", 335, 70, 235, 420, 24, SOFT)
    c.setFillColor(white); c.setFont("Georgia",24); c.drawString(610,430,"Mobile is not")
    c.setFont("GeorgiaItalic",24); c.drawString(610,399,"an afterthought.")
    bullet_list(c,[
        "Readable type hierarchy without flattening the brand personality.",
        "Touch-friendly navigation and full-width actions.",
        "The clinician portrait remains clear and uncropped.",
        "Decorative motion and depth adapt to the available space.",
    ],606,350,180,dark=True,gap=9,size=8.5)
    pill(c,"Checked at 390 × 844",610,98,LIME,NAVY,w=155)
    footer(c,dark=True)


def page_ten(c):
    c.setFillColor(CREAM); c.rect(0,0,W,H,stroke=0,fill=1)
    header(c, "Production audit", "Strong foundation with a short, explicit launch list", 12)
    cols = [
        (36, "What passes", LIME, ["One clear H1 and logical heading hierarchy", "Header, nav, main and footer landmarks", "Meaningful alternative text on all content images", "Labelled form fields and native required states", "Visible keyboard focus and reduced-motion support", "No browser console errors or missing local assets"]),
        (296, "What must be finished", MINT, ["Connect the appointment form to a monitored destination", "Restore click-to-call and WhatsApp contact routes", "Trap and restore keyboard focus in the modal", "Compress the two large PNG assets and add responsive sources", "Add canonical, schema, social metadata, robots and sitemap", "Verify every clinical, NHS, finance and availability claim"]),
        (556, "What creates growth", PINK, ["Dedicated treatment landing pages", "Verified reviews and professional registrations", "Google Business Profile and local search alignment", "Privacy-safe conversion analytics", "Emergency-care and location-led content", "Post-launch testing using real calls and booking data"]),
    ]
    for x,title,color,items in cols:
        c.setFillColor(color); c.roundRect(x,115,235,355,20,stroke=0,fill=1)
        c.setFillColor(NAVY); c.setFont("Georgia",18); c.drawString(x+20,435,title)
        bullet_list(c,items,x+18,400,200,dark=False,gap=8,size=8.2)
    c.setFillColor(GREY); c.setFont("Arial",7); c.drawString(38,75,"Note: automated Lighthouse and Core Web Vitals scores should be captured only after the final production URL is deployed.")
    footer(c)


def page_eleven(c):
    c.setFillColor(PAPER); c.rect(0,0,W,H,stroke=0,fill=1)
    header(c, "Roadmap", "A practical route from prototype to patient-ready website", 13)
    phases = [
        ("P0", "Before live traffic", LIME, ["Connect and test appointment delivery", "Add phone and WhatsApp", "Approve all clinical and availability claims", "Publish privacy information"]),
        ("P1", "Before public launch", MINT, ["Optimize responsive imagery", "Complete modal accessibility", "Add technical SEO foundation", "Publish authentic team and trust content", "Test production across browsers"]),
        ("P2", "First optimization cycle", PINK, ["Connect privacy-safe analytics", "Test CTA language and placement", "Add verified review modules", "Build emergency and local-search routes", "Review 30–60 days of enquiry data"]),
    ]
    for i,(code,title,color,items) in enumerate(phases):
        x=38+i*258
        c.setFillColor(color); c.circle(x+24,430,24,stroke=0,fill=1)
        c.setFillColor(NAVY); c.setFont("ArialBold",11); c.drawCentredString(x+24,426,code)
        c.setFont("Georgia",18); c.drawString(x,382,title)
        c.setStrokeColor(LINE); c.setLineWidth(1); c.line(x,360,x+215,360)
        bullet_list(c,items,x,335,215,gap=12,size=9)
    c.setFillColor(NAVY); c.roundRect(38,58,754,62,18,stroke=0,fill=1)
    quote_style=ParagraphStyle("roadmap_quote",fontName="GeorgiaItalic",fontSize=14,leading=18,textColor=white)
    q=Paragraph("The design is already doing the persuasive work. The next investment should make it operational, findable and measurable.",quote_style)
    _,qh=q.wrap(700,48); q.drawOn(c,60,84-qh/2)
    footer(c)


def page_twelve(c):
    draw_cover_image(c, SHOTS / "prototype-precision.png", 0,0,W,H,darken=0.68)
    c.setFillColor(LIME); c.setFont("ArialBold",8); c.drawString(50,H-70,"FINAL ASSESSMENT")
    c.setFillColor(white); c.setFont("Georgia",37); c.drawString(50,H-125,"The prototype proves the opportunity.")
    c.setFont("GeorgiaItalic",37); c.drawString(50,H-169,"Now make the promise real.")
    ptop(c,"The redesigned experience is clearer, more distinctive and more trustworthy than the current public site. Its strongest sales story is not animation alone; it is the way visual craft, clinician visibility and a calmer patient journey work together.",52,H-205,500,"body_light")
    c.setFillColor(LIME); c.roundRect(52,145,310,92,18,stroke=0,fill=1)
    c.setFillColor(NAVY); c.setFont("ArialBold",8); c.drawString(72,212,"RECOMMENDED NEXT MOVE")
    c.setFont("Georgia",14); c.drawString(72,183,"Present the prototype with this audit,")
    c.setFont("GeorgiaItalic",14); c.drawString(72,161,"then scope the P0 and P1 launch work.")
    c.setFillColor(white); c.setFont("ArialBold",7.2); c.drawString(52,100,"SOURCES")
    c.setFont("Arial",7); c.setFillColor(HexColor("#BDD0D4"))
    sources=["wiltondental.co.uk  •  live public website captured 26 September 2026","Local redesign prototype  •  localhost build at commit 60f03c6","Vercel deployment documentation  •  vercel.com/docs"]
    for idx,s in enumerate(sources): c.drawString(52,84-idx*13,s)
    footer(c,dark=True)


def build():
    c = canvas.Canvas(str(PDF_PATH), pagesize=(W,H), pageCompression=1)
    c.setTitle("Wilton Dental Website Experience Audit")
    c.setAuthor("Website redesign audit")
    for fn in [page_one,page_two,page_three,page_four,page_five,page_six,page_seven,page_eight,page_colour,page_logos,page_nine,page_ten,page_eleven,page_twelve]:
        fn(c)
        c.showPage()
    c.save()
    print(PDF_PATH)


if __name__ == "__main__":
    build()
