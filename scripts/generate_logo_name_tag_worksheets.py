from pathlib import Path

from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site" / "assets" / "name-tag-photopea"
FONT = ROOT / "site" / "assets" / "fonts" / "SourceSans3-VariableFont_wght.ttf"
BOLD_FONT = ROOT / "site" / "assets" / "fonts" / "SourceSans3-Bold.ttf"
NAVY = HexColor("#0b2e4f")
LIGHT = HexColor("#e9f0f5")
MID = HexColor("#98aabb")
TEXT = HexColor("#171717")
RULE = HexColor("#5f6368")
HEADER_LOGO = OUT / "downloads" / "source-files" / "technology-commons-transparent.png"
HEADER_LOGO_IMAGE = None
if HEADER_LOGO.is_file():
    HEADER_LOGO_IMAGE = Image.open(HEADER_LOGO).convert("RGBA")
    HEADER_LOGO_IMAGE.load()

pdfmetrics.registerFont(TTFont("SourceSans", str(FONT)))
pdfmetrics.registerFont(TTFont("SourceSansBold", str(BOLD_FONT)))


def draw_print_header(c, title, subtitle):
    if HEADER_LOGO_IMAGE is not None:
        c.drawImage(ImageReader(HEADER_LOGO_IMAGE.copy()), 43, 742, 34, 34, preserveAspectRatio=True, mask="auto")
    else:
        c.setStrokeColor(NAVY)
        c.circle(60, 759, 16, stroke=1, fill=0)
        c.setFont("SourceSansBold", 10)
        c.setFillColor(NAVY)
        c.drawCentredString(60, 755, "TC")
    c.setFillColor(TEXT)
    c.setFont("SourceSansBold", 24)
    c.drawString(86, 757, title)
    c.setFont("SourceSansBold", 12)
    c.drawString(86, 740, subtitle)
    c.setFont("SourceSansBold", 8.5)
    c.drawString(43, 721, "Technology Commons | Port Credit Secondary School")
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.line(43, 714, 569, 714)
    c.setFont("SourceSansBold", 10.5)
    c.drawString(43, 697, "Student Number: ____________________________    Date: ____________________")


def draw_footer(c, page_number, short_title="Idea to SVG"):
    c.setStrokeColor(RULE)
    c.setLineWidth(0.45)
    c.line(43, 45, 569, 45)
    c.setFillColor(TEXT)
    c.setFont("SourceSansBold", 6.5)
    c.drawString(43, 34, "CC BY-SA 4.0 · Created by Andrew Andrade · andrewandrade.ca · Source: github.com/mrandrewandrade")
    c.setFont("SourceSans", 6.5)
    c.drawString(43, 24, "Please share, modify and redistribute. Keep the original source and add your own name and links.")
    c.drawRightString(569, 24, f"{short_title}  |  {page_number}")


def wrap_lines(c, text, font_name, font_size, width):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if c.stringWidth(candidate, font_name, font_size) <= width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_step(c, number, title, text, y):
    c.setFillColor(white)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.roundRect(43, y - 62, 526, 67, 5, stroke=1, fill=1)
    c.setFillColor(NAVY)
    c.circle(62, y - 13, 12, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFont("SourceSansBold", 11)
    c.drawCentredString(62, y - 17, str(number))
    c.setFillColor(TEXT)
    c.setFont("SourceSansBold", 11)
    c.drawString(82, y - 11, title)
    c.setFont("SourceSans", 10.5)
    for line_number, line in enumerate(wrap_lines(c, text, "SourceSans", 10.5, 468)):
        c.drawString(82, y - 27 - line_number * 13, line)


def build_logo_worksheet():
    output = OUT / "personal-logo-worksheet.pdf"
    c = canvas.Canvas(str(output), pagesize=letter)
    draw_print_header(c, "PERSONAL LOGO", "Idea to SVG: sketch first, then rebuild in Photopea")

    c.setFillColor(TEXT)
    c.setFont("SourceSansBold", 12)
    c.drawString(43, 670, "1. Find two or three useful shapes")
    c.setFont("SourceSans", 10.5)
    for i, line in enumerate(wrap_lines(c, "Start with your own drawing or an approved AI-made image. Circle only the shapes you might reuse. Do not trace every detail.", "SourceSans", 10.5, 526)):
        c.drawString(43, 653 - i * 13, line)
    c.setStrokeColor(RULE)
    c.roundRect(43, 501, 526, 116, 5, stroke=1, fill=0)
    c.setFont("SourceSansBold", 10.5)
    c.drawString(55, 599, "Paste, sketch, or describe the inspiration here. Circle two or three shapes.")

    c.setFont("SourceSansBold", 12)
    c.drawString(43, 478, "2. Sketch three different simple marks")
    labels = ["A. Initials", "B. Shapes", "C. Initials + one shape"]
    for x, label in zip((43, 222, 401), labels):
        c.setFont("SourceSansBold", 10.5)
        c.drawString(x, 457, label)
        c.setStrokeColor(RULE)
        c.roundRect(x, 291, 168, 153, 5, stroke=1, fill=0)

    c.setFont("SourceSansBold", 12)
    c.drawString(43, 266, "3. Choose one")
    c.setFont("SourceSans", 10.5)
    c.drawString(43, 249, "Circle:   A   B   C      Why is this the clearest idea?")
    c.setStrokeColor(RULE)
    c.line(43, 222, 569, 222)
    c.line(43, 199, 569, 199)

    c.setFont("SourceSansBold", 12)
    c.drawString(43, 173, "4. Plan the build")
    c.setFont("SourceSans", 10.5)
    c.drawString(43, 155, "List the layers you need:  ______________________________________________")
    c.drawString(43, 134, "Examples: SUN, MOUNTAIN, RIVER, INITIALS. Start with black shapes.")
    c.setFillColor(LIGHT)
    c.roundRect(43, 75, 526, 42, 5, stroke=0, fill=1)
    c.setFillColor(TEXT)
    c.setFont("SourceSansBold", 10.5)
    c.drawString(55, 96, "Next: open Photopea and follow pages 2 and 3. Bring this page with you.")
    c.setFont("SourceSans", 9)
    c.drawString(55, 82, "The finished mark should be simpler and more original than the starting image.")
    draw_footer(c, 1)
    c.showPage()

    draw_print_header(c, "PHOTOPEA STEPS", "Build the selected sketch: setup and first shapes")
    c.setFont("SourceSans", 10.5)
    c.setFillColor(TEXT)
    c.drawString(43, 672, "Complete each step in order. Keep the sketch beside you.")
    steps_page_2 = [
        (1, "Create the file", "Open Photopea. Select File > New. Set Width and Height to 1000 px. Choose Transparent, then Create."),
        (2, "Place the sketch", "Select File > Open & Place. Choose a clear photo or scan of the sketch you circled on page 1."),
        (3, "Set the reference", "In Layers, rename the placed image REFERENCE. Set Opacity to 30%. Select the lock icon."),
        (4, "Make the first layer", "Select New Layer. Name it for the part you will draw, such as SUN, MOUNTAIN, or INITIALS."),
        (5, "Draw basic shapes", "Press U. Choose a Shape tool. Set Fill to black and Stroke to none. Drag to draw the first shape."),
        (6, "Draw custom shapes", "Press P for the Pen tool. Click for straight corners. Click and drag only when you need a curve. Close the path."),
    ]
    for row, step in enumerate(steps_page_2):
        draw_step(c, *step, 646 - row * 86)
    draw_footer(c, 2)
    c.showPage()

    draw_print_header(c, "PHOTOPEA STEPS", "Finish, test, and export the logo")
    steps_page_3 = [
        (7, "Add initials", "Press T. Choose a bold, readable sans-serif font. Keep the text editable while you test the idea."),
        (8, "Arrange the parts", "Press V. Select a layer, then use Ctrl+T to move, resize, or rotate it. Hold Shift to keep proportions."),
        (9, "Protect your options", "Duplicate a layer before changing it. Keep one idea per clearly named layer or group."),
        (10, "Run the black test", "Hide REFERENCE by selecting its eye icon. The logo should still read clearly as one black silhouette."),
        (11, "Add simple colour", "Use two or three colours at most. Keep strong contrast. Save a solid black version for engraving."),
        (12, "Save and export", "Save the editable PSD. Select File > Export As > SVG. Export a transparent PNG for the name tag."),
    ]
    for row, step in enumerate(steps_page_3):
        draw_step(c, *step, 664 - row * 80)

    c.setFillColor(LIGHT)
    c.roundRect(43, 76, 526, 78, 5, stroke=0, fill=1)
    c.setFillColor(TEXT)
    c.setFont("SourceSansBold", 11)
    c.drawString(55, 135, "Final check")
    c.setFont("SourceSans", 10.5)
    checks = ["[ ] clear at 25 mm", "[ ] works in black", "[ ] no tiny gaps", "[ ] PSD + SVG + PNG saved"]
    for index, check in enumerate(checks):
        c.drawString(55 + (index % 2) * 250, 115 - (index // 2) * 22, check)
    draw_footer(c, 3)
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
