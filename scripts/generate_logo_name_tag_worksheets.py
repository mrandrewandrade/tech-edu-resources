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
    draw_header(c, "PERSONAL LOGO: INITIALS TO SVG", "Sketch three different ideas. Choose the clearest shape, not the fanciest one.", width)

    c.setFillColor(NAVY)
    c.setFont("SourceSans", 13)
    c.drawString(42, 690, "1  Write your initials:")
    c.setStrokeColor(NAVY)
    c.line(182, 687, 330, 687)
    c.drawString(352, 690, "Three words it should feel like:")
    c.line(535, 687, 570, 687)

    labels = ["A  CLEAR LETTERS", "B  OVERLAP / INTERLOCK", "C  SYMBOL / NEGATIVE SPACE"]
    x_positions = [42, 229, 416]
    for x, label in zip(x_positions, labels):
        c.setFillColor(LIGHT)
        c.roundRect(x, 420, 154, 238, 8, stroke=0, fill=1)
        c.setStrokeColor(MID)
        c.setDash(4, 3)
        c.roundRect(x + 10, 444, 134, 178, 6, stroke=1, fill=0)
        c.setDash()
        c.setFillColor(NAVY)
        c.setFont("SourceSans", 9)
        c.drawCentredString(x + 77, 632, label)
        c.setFont("SourceSans", 8)
        c.drawCentredString(x + 77, 429, "quick pencil sketch")

    c.setFillColor(NAVY)
    c.setFont("SourceSans", 13)
    c.drawString(42, 390, "2  Circle one idea. Rebuild it in Photopea with black shapes first.")

    tests = ["SMALL", "SOLID BLACK", "WHITE ON DARK", "GRAYSCALE"]
    box_w = 123
    for i, label in enumerate(tests):
        x = 42 + i * 136
        c.setStrokeColor(MID)
        c.setFillColor(NAVY if label == "WHITE ON DARK" else white)
        c.roundRect(x, 245, box_w, 112, 6, stroke=1, fill=1)
        c.setFillColor(white if label == "WHITE ON DARK" else NAVY)
        c.setFont("SourceSans", 9)
        c.drawCentredString(x + box_w / 2, 332, label)
        c.setFont("SourceSans", 30)
        c.drawCentredString(x + box_w / 2, 278, "AA")

    c.setFillColor(NAVY)
    c.setFont("SourceSans", 13)
    c.drawString(42, 214, "3  Final check")
    c.setFont("SourceSans", 10)
    checks = [
        "[ ] recognizable at small size",
        "[ ] strong in one colour",
        "[ ] no tiny gaps or hairline strokes",
        "[ ] saved as PSD and SVG",
    ]
    for i, item in enumerate(checks):
        c.drawString(54 + (i % 2) * 270, 188 - (i // 2) * 24, item)

    c.setFillColor(LIGHT)
    c.roundRect(42, 70, 528, 62, 8, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.setFont("SourceSans", 11)
    c.drawString(56, 107, "PHOTOPEA: 1000 x 1000 px, transparent background")
    c.setFont("SourceSans", 9)
    c.drawString(56, 88, "Type + shapes: keep an editable text copy, convert the working copy to a shape, then export SVG.")
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
