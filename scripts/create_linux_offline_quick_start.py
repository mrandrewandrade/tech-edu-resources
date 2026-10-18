from __future__ import annotations

from pathlib import Path

from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "site" / "assets" / "linux" / "TEJ-Linux-Offline-Kit-Quick-Start.pdf"
HANDS_LOGO = (
    ROOT
    / "site"
    / "assets"
    / "branding"
    / "emblem"
    / "technology-commons-hands.png"
)
PAGE_URL = (
    "https://andrewandrade.ca/tech-edu-resources/"
    "tej3-4/linux-operating-systems/offline-kit/"
)

INK = HexColor("#111820")
NAVY = HexColor("#123A63")
MID_GREY = HexColor("#4F5963")
RULE = HexColor("#636C74")
LIGHT_FILL = HexColor("#F1F2F3")


def register_fonts() -> None:
    windows_fonts = Path("C:/Windows/Fonts")
    regular = windows_fonts / "arial.ttf"
    bold = windows_fonts / "arialbd.ttf"
    italic = windows_fonts / "ariali.ttf"
    if regular.is_file() and bold.is_file():
        pdfmetrics.registerFont(TTFont("TCArial", str(regular)))
        pdfmetrics.registerFont(TTFont("TCArial-Bold", str(bold)))
        pdfmetrics.registerFont(
            TTFont("TCArial-Italic", str(italic if italic.is_file() else regular))
        )
        return
    # Arial-compatible fallback for non-Windows rebuilds.
    pdfmetrics.registerFont(TTFont("TCArial", "LiberationSans-Regular.ttf"))
    pdfmetrics.registerFont(TTFont("TCArial-Bold", "LiberationSans-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("TCArial-Italic", "LiberationSans-Italic.ttf"))


def wrap(text: str, font: str, size: float, width: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if pdfmetrics.stringWidth(candidate, font, size) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(
    pdf: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    *,
    font: str = "TCArial",
    size: float = 10.5,
    leading: float = 13,
    color=INK,
) -> float:
    pdf.setFillColor(color)
    pdf.setFont(font, size)
    for line in wrap(text, font, size, width):
        pdf.drawString(x, y, line)
        y -= leading
    return y


def section_heading(pdf: canvas.Canvas, number: int, title: str, y: float) -> float:
    pdf.setFillColor(NAVY)
    pdf.setFont("TCArial-Bold", 12)
    pdf.drawString(43, y, f"{number}. {title}")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(0.75)
    pdf.line(43, y - 6, 569, y - 6)
    return y - 22


def draw_bullet(pdf: canvas.Canvas, text: str, x: float, y: float, width: float) -> float:
    pdf.setFillColor(INK)
    pdf.circle(x + 2.5, y + 3, 1.5, stroke=0, fill=1)
    return draw_wrapped(pdf, text, x + 12, y, width - 12, size=10.5, leading=13)


def draw_code(pdf: canvas.Canvas, code: str, x: float, y: float, width: float) -> float:
    pdf.setFillColor(LIGHT_FILL)
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(0.65)
    pdf.rect(x, y - 19, width, 27, stroke=1, fill=1)
    pdf.setFillColor(black)
    pdf.setFont("Courier-Bold", 10)
    pdf.drawString(x + 9, y - 10, code)
    return y - 33


def build() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter)
    page_width, page_height = letter
    pdf.setTitle("TEJ Linux Offline Kit - Printable Quick Start")
    pdf.setAuthor("Andrew Andrade, Technology Commons")
    pdf.setSubject("Offline-first student quick start for Terminal Quest and Bashcrawl")

    # Compact identity block from the Technology Commons printable template.
    logo_size = 58
    pdf.drawImage(
        ImageReader(str(HANDS_LOGO)),
        43,
        page_height - 43 - logo_size,
        width=logo_size,
        height=logo_size,
        preserveAspectRatio=True,
        mask="auto",
    )
    title_x = 115
    pdf.setFillColor(INK)
    pdf.setFont("TCArial-Bold", 24)
    pdf.drawString(title_x, page_height - 61, "TEJ Linux Offline Kit")
    pdf.setFont("TCArial-Bold", 13)
    pdf.drawString(title_x, page_height - 82, "Printable Quick Start")
    pdf.setFont("TCArial-Bold", 8.5)
    pdf.setFillColor(MID_GREY)
    pdf.drawString(title_x, page_height - 98, "Technology Commons | Port Credit Secondary School")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1)
    pdf.line(43, page_height - 111, 569, page_height - 111)

    y = page_height - 132
    y = section_heading(pdf, 1, "Get the kit", y)

    qr_size = 61
    qr_x = 508
    qr_y = y - 67
    pdf.setFillColor(white)
    pdf.rect(qr_x - 3, qr_y - 3, qr_size + 6, qr_size + 6, stroke=0, fill=1)
    qr = QrCodeWidget(PAGE_URL)
    qr.barWidth = qr_size
    qr.barHeight = qr_size
    drawing = Drawing(qr_size, qr_size)
    drawing.add(qr)
    drawing.drawOn(pdf, qr_x, qr_y)

    text_width = 450
    y = draw_bullet(pdf, "No Internet: copy TEJ-Linux-Offline-Kit.zip from the class USB drive to Downloads.", 43, y, text_width)
    y -= 2
    y = draw_bullet(pdf, "Internet available: scan the code or open the address below and download the same ZIP.", 43, y, text_width)
    y -= 2
    y = draw_bullet(pdf, "Double-click the ZIP, choose Extract, and keep the complete extracted folder together.", 43, y, text_width)
    pdf.setFont("TCArial-Bold", 8.5)
    pdf.setFillColor(MID_GREY)
    pdf.drawString(qr_x - 8, qr_y - 13, "Linux Offline Kit")
    pdf.setFont("TCArial", 8.3)
    pdf.drawString(43, y - 2, "andrewandrade.ca/tech-edu-resources/tej3-4/linux-operating-systems/offline-kit/")
    y = min(y - 25, qr_y - 27)

    y = section_heading(pdf, 2, "Open the local instructions", y)
    y = draw_bullet(pdf, "Open the extracted TEJ-Linux-Offline-Kit folder.", 43, y, 526)
    y -= 2
    y = draw_bullet(pdf, "Double-click START-HERE.html. It opens locally in a browser and does not need Internet.", 43, y, 526)
    y -= 2
    y = draw_bullet(pdf, "Choose 3.1 Computer Detective or 3.2 Bashcrawl. Open the ODT in LibreOffice, or use the PDF and matching TXT answer sheet.", 43, y, 526)
    y -= 2
    y = draw_wrapped(
        pdf,
        "This sheet focuses on Linux Mint and the class USB. Use the website for Windows, Mac, Chromebook, or phone instructions. A phone is slower and more difficult than a computer.",
        43,
        y,
        526,
        size=9.2,
        leading=11,
        color=MID_GREY,
    )
    y -= 9

    y = section_heading(pdf, 3, "Prepare Bashcrawl", y)
    y = draw_wrapped(
        pdf,
        "In the extracted kit, copy the complete bashcrawl folder. In Files, open Home, create a folder named Games, and paste bashcrawl inside it. Hidden rooms are part of the game, so copy the whole folder.",
        43,
        y,
        526,
        size=10.5,
        leading=13,
    )
    y -= 3
    y = draw_bullet(pdf, "Open Terminal with Ctrl + Alt + T in Linux Mint, including the live USB session.", 43, y, 526)
    y -= 4
    draw_code(pdf, "cd ~/Games/bashcrawl/entrance", 43, y, 253)
    y = draw_code(pdf, "cat scroll", 316, y, 253)
    y -= 3

    y = section_heading(pdf, 4, "Play and record your work", y)
    y = draw_wrapped(pdf, "Run one command at a time. Do not type the $ prompt symbol.", 43, y, 526, font="TCArial-Bold", size=10.5, leading=13, color=NAVY)
    y -= 5
    draw_code(pdf, "ls        pwd        cat scroll", 43, y, 253)
    y = draw_code(pdf, "cd roomname        cd ..        ls -a", 316, y, 253)
    y -= 3
    y = draw_bullet(pdf, "Read each clue, explore, and complete the answer sheet. A wrong turn is part of the problem solving.", 43, y, 526)
    y -= 2
    y = draw_bullet(pdf, "Save the completed ODT, DOCX, or TXT file with your name in the filename.", 43, y, 526)
    y -= 2
    y = draw_bullet(pdf, "Save readable screenshots in the document or beside the TXT answer sheet.", 43, y, 526)
    y -= 2
    draw_bullet(pdf, "Copy your work back to the USB if needed. Upload it to Google Classroom when Internet returns. Never record passwords, tokens, or Wi-Fi credentials.", 43, y, 526)

    # Required footer wording from the printable handout guide.
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(0.65)
    pdf.line(43, 47, 569, 47)
    pdf.setFillColor(MID_GREY)
    pdf.setFont("TCArial", 6.5)
    pdf.drawString(43, 37, "CC BY-SA 4.0 · Created by Andrew Andrade · andrewandrade.ca · Source: github.com/mrandrewandrade")
    pdf.drawString(43, 28, "Please share, modify and redistribute. If you change this file, do not remove:")
    pdf.drawString(43, 19, "CC BY-SA 4.0. Original Source: andrewandrade.ca and add your own name + links. Sharing is caring!")
    pdf.setFont("TCArial-Bold", 7)
    pdf.drawRightString(569, 37, "Page 1 of 1")

    pdf.showPage()
    pdf.save()
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    build()
