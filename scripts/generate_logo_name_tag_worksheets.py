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
LOGO_EXAMPLE = OUT / "landscape-to-logo-example.png"
PHOTOPEA_SCREENSHOTS = ROOT / "site" / "assets" / "personal-logo-photopea"
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
    for i, line in enumerate(wrap_lines(c, "Start with your own paper drawing. Photograph or scan it, then circle only the shapes you might reuse. Do not trace every detail.", "SourceSans", 10.5, 526)):
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
    c.drawString(55, 96, "Next: compare your sketch with the worked example on page 2.")
    c.setFont("SourceSans", 9)
    c.drawString(55, 82, "Then use the separate Photopea step-by-step guide to build your selected idea.")
    draw_footer(c, 1)
    c.showPage()

    draw_print_header(c, "WORKED EXAMPLE", "What a strong simplification looks like")
    c.setFillColor(TEXT)
    c.setFont("SourceSans", 10.5)
    c.drawString(43, 672, "Study the changes from the starting idea to the final mark. Use the same tests on your own design.")
    if LOGO_EXAMPLE.is_file():
        c.drawImage(str(LOGO_EXAMPLE), 43, 492, width=526, height=149, preserveAspectRatio=True, anchor="c")

    analyses = [
        ("1. Keep the meaning", "The sun, mountain, and river still communicate the original landscape idea."),
        ("2. Reduce the parts", "The image is rebuilt with one circle, one triangle, and one strong curve."),
        ("3. Test in black", "The silhouette remains clear without colour. That makes engraving possible."),
        ("4. Remove tiny details", "Wide gaps and bold shapes remain readable when the logo is only 25 mm wide."),
        ("5. Use limited colour", "Three colours separate the forms without making the mark complicated."),
        ("6. Keep it editable", "Each part stays on its own named layer so size, spacing, and colour can change."),
    ]
    positions = [(43, 402), (310, 402), (43, 314), (310, 314), (43, 226), (310, 226)]
    for (title, body), (x, y) in zip(analyses, positions):
        c.setStrokeColor(RULE)
        c.setFillColor(white)
        c.roundRect(x, y, 259, 76, 5, stroke=1, fill=1)
        c.setFillColor(NAVY)
        c.setFont("SourceSansBold", 10.5)
        c.drawString(x + 10, y + 57, title)
        c.setFillColor(TEXT)
        c.setFont("SourceSans", 9.3)
        for line_number, line in enumerate(wrap_lines(c, body, "SourceSans", 9.3, 239)):
            c.drawString(x + 10, y + 40 - line_number * 11, line)

    c.setFillColor(LIGHT)
    c.roundRect(43, 77, 526, 126, 5, stroke=0, fill=1)
    c.setFillColor(TEXT)
    c.setFont("SourceSansBold", 11)
    c.drawString(55, 181, "Analyze your selected sketch")
    c.setFont("SourceSans", 9.7)
    c.drawString(55, 162, "Which two or three shapes carry the meaning?  ______________________________________")
    c.drawString(55, 139, "What detail can you remove?  __________________________________________________")
    c.drawString(55, 116, "Will it still work in black at 25 mm?  ____________________________________________")
    c.setFont("SourceSansBold", 9.7)
    c.drawString(55, 91, "Next: open the separate Photopea Step-by-Step Guide and build the mark.")
    draw_footer(c, 2)
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


def build_photopea_guide():
    output = OUT / "personal-logo-photopea-guide.pdf"
    c = canvas.Canvas(str(output), pagesize=letter)
    pages = [
        ("1. Create a square file", "Choose File > New. Name the file PERSONAL LOGO. Set Width to 1000 px, Height to 1000 px, and Background to Transparent. Select Create.", "Checkpoint: a square checkerboard canvas is visible."),
        ("2. Place the selected sketch", "Choose File > Open & Place. Select a clear photo or scan of the sketch chosen on the worksheet. Resize it to fill most of the square without stretching it.", "Checkpoint: the sketch appears on its own layer."),
        ("3. Make a safe reference layer", "In Layers, double-click the sketch layer name and type REFERENCE. Set Opacity to 30%, then select the lock icon. Never draw on this layer.", "Checkpoint: the sketch is faint and locked."),
        ("4. Rebuild with clean shapes", "Select New Layer and name each part. Press U for circles and rectangles. Press P for a custom shape. Set Fill to black and Stroke to none. Close every Pen-tool path.", "Checkpoint: SUN, MOUNTAIN, and RIVER are separate named layers."),
        ("5. Run the black and size tests", "Hide REFERENCE by selecting its eye icon. Zoom out until the mark is about 25 mm wide on screen. Remove details that disappear, close up, or become confusing.", "Checkpoint: the logo still reads as one strong black mark."),
        ("6. Add colour and export", "Use two or three colours only after the black version works. Save the editable PSD. Choose File > Export As > SVG for the scale-free master and PNG for the transparent name-tag copy.", "Checkpoint: PSD, SVG, and transparent PNG are saved."),
    ]
    for page_number, (title, instruction, checkpoint) in enumerate(pages, start=1):
        draw_print_header(c, "PHOTOPEA GUIDE", title)
        screenshot = PHOTOPEA_SCREENSHOTS / f"{page_number:02d}-photopea-personal-logo.jpg"
        if screenshot.is_file():
            c.drawImage(str(screenshot), 43, 320, width=526, height=329, preserveAspectRatio=True, anchor="c")
        c.setFillColor(TEXT)
        c.setFont("SourceSansBold", 12)
        c.drawString(43, 288, "Do this")
        c.setFont("SourceSans", 10.5)
        y = 270
        for line in wrap_lines(c, instruction, "SourceSans", 10.5, 526):
            c.drawString(43, y, line)
            y -= 14
        c.setFillColor(LIGHT)
        c.roundRect(43, 104, 526, 70, 5, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.setFont("SourceSansBold", 11)
        c.drawString(55, 146, "STOP AND CHECK")
        c.setFillColor(TEXT)
        c.setFont("SourceSans", 10.5)
        for index, line in enumerate(wrap_lines(c, checkpoint, "SourceSans", 10.5, 500)):
            c.drawString(55, 126 - index * 14, line)
        draw_footer(c, page_number, "Photopea Guide")
        c.showPage()
    c.save()


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    build_logo_worksheet()
    build_name_tag_prototype()
    build_photopea_guide()
