from pathlib import Path

from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site" / "assets" / "name-tag-photopea"
FONT = ROOT / "site" / "assets" / "fonts" / "SourceSans3-VariableFont_wght.ttf"
BOLD_FONT = ROOT / "site" / "assets" / "fonts" / "SourceSans3-Bold.ttf"
NAVY = HexColor("#0b2e4f")
LIGHT = HexColor("#e9f0f5")
MID = HexColor("#98aabb")

pdfmetrics.registerFont(TTFont("SourceSans", str(FONT)))
pdfmetrics.registerFont(TTFont("SourceSansBold", str(BOLD_FONT)))


def draw_header(c, title, subtitle, page_width):
    c.setFillColor(NAVY)
    c.rect(0, 720, page_width, 72, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFont("SourceSansBold", 24)
    c.drawString(42, 754, title)
    c.setFont("SourceSans", 10)
    c.drawString(42, 736, subtitle)


def build_logo_worksheet():
    output = OUT / "personal-logo-worksheet.pdf"
    c = canvas.Canvas(str(output), pagesize=letter)
    width, height = letter
    draw_header(c, "PERSONAL LOGO: IDEA TO SVG", "Turn a hand-drawn or AI-made inspiration image into your own simple Photopea logo.", width)

    c.setFillColor(NAVY)
    c.setFont("SourceSansBold", 12)
    c.drawString(42, 694, "1  START WITH INSPIRATION, THEN SIMPLIFY")
    c.setFont("SourceSans", 9)
    c.drawString(42, 679, "Do not trace every detail. Pick two or three useful shapes and rebuild them in your own way.")

    panel_x = [42, 177, 312, 447]
    panel_titles = ["STARTING IDEA", "PICK 3 SHAPES", "PHOTOPEA", "YOUR MARK"]
    panel_notes = ["drawing or AI image", "circle · triangle · curve", "test in black", "add 2–3 colours"]
    for x, title, note in zip(panel_x, panel_titles, panel_notes):
        c.setFillColor(LIGHT)
        c.roundRect(x, 525, 123, 136, 7, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.setFont("SourceSansBold", 8)
        c.drawCentredString(x + 61.5, 642, title)
        c.setFont("SourceSans", 7)
        c.drawCentredString(x + 61.5, 630, note)

    # Starting landscape sketch.
    c.setStrokeColor(HexColor("#687985"))
    c.setLineWidth(2.5)
    p = c.beginPath()
    p.moveTo(53, 555)
    p.lineTo(83, 608)
    p.lineTo(103, 577)
    p.lineTo(127, 612)
    p.lineTo(154, 555)
    c.drawPath(p)
    c.circle(137, 612, 9, stroke=1, fill=0)
    p = c.beginPath()
    p.moveTo(55, 546)
    p.curveTo(88, 530, 120, 532, 153, 546)
    c.drawPath(p)

    # Three extracted shapes.
    c.setFillColor(HexColor("#f1b434"))
    c.circle(205, 591, 15, stroke=0, fill=1)
    c.setFillColor(HexColor("#2d6a4f"))
    p = c.beginPath()
    p.moveTo(226, 550)
    p.lineTo(255, 608)
    p.lineTo(286, 550)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.setStrokeColor(HexColor("#247ba0"))
    c.setLineWidth(7)
    p = c.beginPath()
    p.moveTo(194, 543)
    p.curveTo(225, 528, 257, 529, 290, 544)
    c.drawPath(p)

    # Black Photopea silhouette.
    c.setFillColor(black)
    c.circle(350, 591, 14, stroke=0, fill=1)
    p = c.beginPath()
    p.moveTo(347, 548)
    p.lineTo(380, 611)
    p.lineTo(416, 548)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.setStrokeColor(black)
    c.setLineWidth(7)
    p = c.beginPath()
    p.moveTo(331, 541)
    p.curveTo(361, 528, 390, 529, 422, 543)
    c.drawPath(p)

    # Finished colour mark.
    c.setFillColor(HexColor("#f8f4e8"))
    c.setStrokeColor(NAVY)
    c.setLineWidth(2)
    c.circle(508, 575, 41, stroke=1, fill=1)
    c.setFillColor(HexColor("#f1b434"))
    c.circle(492, 590, 11, stroke=0, fill=1)
    c.setFillColor(HexColor("#2d6a4f"))
    p = c.beginPath()
    p.moveTo(480, 552)
    p.lineTo(510, 605)
    p.lineTo(542, 552)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.setStrokeColor(HexColor("#247ba0"))
    c.setLineWidth(6)
    p = c.beginPath()
    p.moveTo(476, 548)
    p.curveTo(500, 536, 526, 537, 544, 548)
    c.drawPath(p)

    c.setFillColor(NAVY)
    c.setFont("SourceSansBold", 12)
    c.drawString(42, 497, "2  SKETCH THREE DIFFERENT SIMPLE MARKS")
    labels = ["A  INITIALS", "B  LANDSCAPE SHAPES", "C  INITIALS + ONE SHAPE"]
    x_positions = [42, 229, 416]
    for x, label in zip(x_positions, labels):
        c.setFillColor(LIGHT)
        c.roundRect(x, 319, 154, 160, 8, stroke=0, fill=1)
        c.setStrokeColor(MID)
        c.setDash(4, 3)
        c.roundRect(x + 10, 342, 134, 104, 6, stroke=1, fill=0)
        c.setDash()
        c.setFillColor(NAVY)
        c.setFont("SourceSans", 8)
        c.drawCentredString(x + 77, 461, label)
        c.setFont("SourceSans", 7)
        c.drawCentredString(x + 77, 327, "quick sketch — use few shapes")

    c.setFillColor(NAVY)
    c.setFont("SourceSansBold", 12)
    c.drawString(42, 292, "3  BUILD IN PHOTOPEA")
    c.setFont("SourceSans", 9)
    c.drawString(42, 275, "1000 × 1000 px · transparent background · place reference · lower opacity · lock layer")
    c.drawString(42, 260, "Rebuild with Shape, Pen and Type tools. Hide the reference. Test the new silhouette in black.")

    c.setFont("SourceSansBold", 12)
    c.drawString(42, 230, "4  ADD SIMPLE COLOUR")
    c.setFont("SourceSans", 9)
    c.drawString(42, 213, "Use one main colour, one supporting colour and an optional accent. Keep a black version for engraving.")
    swatches = [HexColor("#2d6a4f"), HexColor("#247ba0"), HexColor("#f1b434")]
    for i, colour in enumerate(swatches):
        c.setFillColor(colour)
        c.circle(470 + i * 34, 218, 11, stroke=0, fill=1)

    c.setFillColor(NAVY)
    c.setFont("SourceSansBold", 12)
    c.drawString(42, 180, "5  TEST + SAVE")
    c.setFont("SourceSans", 9)
    checks = [
        "[ ] clear at 25 mm wide",
        "[ ] works in solid black",
        "[ ] works white on dark",
        "[ ] colour has strong contrast",
        "[ ] no tiny gaps or thin lines",
        "[ ] saved as PSD, SVG and PNG",
    ]
    for i, item in enumerate(checks):
        c.drawString(54 + (i % 2) * 270, 157 - (i // 2) * 19, item)

    c.setFillColor(LIGHT)
    c.roundRect(42, 58, 528, 42, 8, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.setFont("SourceSansBold", 9)
    c.drawString(56, 83, "FLOW: inspiration → choose shapes → sketch → rebuild → colour → test → export")
    c.setFont("SourceSans", 8)
    c.drawString(56, 68, "Your final mark should be simpler and more original than the starting image.")
    c.save()


def build_name_tag_prototype():
    output = OUT / "name-tag-paper-prototype.pdf"
    page = landscape(letter)
    c = canvas.Canvas(str(output), pagesize=page)
    width, height = page
    inch = 72

    c.setFillColor(black)
    c.setFont("SourceSans", 8)
    c.drawString(18, height - 13, "PRINT AT ACTUAL SIZE / 100%. Cut on solid lines. One letter sheet makes two 11 x 4 inch prototypes.")

    strips = [(4.25 * inch, 8.25 * inch), (0.25 * inch, 4.25 * inch)]
    for index, (bottom, top) in enumerate(strips, start=1):
        c.setStrokeColor(black)
        c.setLineWidth(0.8)
        c.line(0, bottom, width, bottom)
        c.line(0, top, width, top)

        safe = 0.25 * inch
        c.setStrokeColor(MID)
        c.setDash(5, 4)
        c.rect(safe, bottom + safe, width - 2 * safe, 4 * inch - 2 * safe, stroke=1, fill=0)
        centre_y = bottom + 2 * inch
        c.setStrokeColor(HexColor("#8fc4d8"))
        c.setDash(3, 4)
        c.line(safe, centre_y, width - safe, centre_y)
        c.setDash()

        c.setFillColor(NAVY)
        c.setFont("SourceSans", 9)
        c.drawString(22, top - 18, f"PROTOTYPE {index}: sketch logo + name on one horizontal centreline")
        c.setFillColor(HexColor("#778899"))
        c.setFont("SourceSans", 7)
        c.drawRightString(width - 22, bottom + 8, "dashed box = 0.25 inch safe margin")

    c.setStrokeColor(black)
    c.setLineWidth(2)
    c.line(22, 21, 94, 21)
    c.setFont("SourceSans", 7)
    c.setFillColor(black)
    c.drawString(22, 9, "1 inch check line")
    c.save()


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    build_logo_worksheet()
    build_name_tag_prototype()
