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
LIGHT_RULE = HexColor("#B9C0C6")
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


def draw_platform_table(pdf: canvas.Canvas, y_top: float) -> float:
    x = 43
    total_width = 526
    platform_width = 105
    instruction_width = total_width - platform_width
    rows = [
        (
            "Windows",
            "Open Start and search for WSL or Ubuntu. If it is missing, ask the computer owner before using wsl --install as an administrator. Setup needs Internet and may require a restart.",
        ),
        (
            "Mac",
            "Press Command + Space, type Terminal, then press Return. No installation is needed.",
        ),
        (
            "Chromebook",
            "On a personal or owner account: Settings > About ChromeOS > Developers > Linux development environment > Set up. Setup needs Internet once. A school-managed Chromebook may block this feature.",
        ),
        (
            "Linux Mint or Ubuntu",
            "Press Ctrl + Alt + T, or open Terminal from the application menu.",
        ),
        (
            "Phone or tablet",
            "Android: use Termux from F-Droid. iPhone or iPad: use iSH Shell. A phone is slower and more difficult to use, but it works. A Bluetooth keyboard helps.",
        ),
    ]

    body_font = "TCArial"
    body_size = 9.4
    leading = 11.2
    row_specs: list[tuple[str, list[str], float]] = []
    for label, instruction in rows:
        lines = wrap(instruction, body_font, body_size, instruction_width - 16)
        height = max(30, len(lines) * leading + 12)
        row_specs.append((label, lines, height))

    header_height = 25
    table_height = header_height + sum(item[2] for item in row_specs)
    y_bottom = y_top - table_height

    pdf.setFillColor(white)
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(0.65)
    pdf.rect(x, y_bottom, total_width, table_height, stroke=1, fill=1)
    pdf.setFillColor(LIGHT_FILL)
    pdf.rect(x, y_top - header_height, total_width, header_height, stroke=0, fill=1)
    pdf.setStrokeColor(RULE)
    pdf.line(x, y_top - header_height, x + total_width, y_top - header_height)
    pdf.line(x + platform_width, y_bottom, x + platform_width, y_top)

    pdf.setFillColor(INK)
    pdf.setFont("TCArial-Bold", 9.5)
    pdf.drawString(x + 8, y_top - 17, "Computer")
    pdf.drawString(x + platform_width + 8, y_top - 17, "How to open the terminal at home")

    y = y_top - header_height
    for index, (label, lines, height) in enumerate(row_specs):
        row_bottom = y - height
        if index < len(row_specs) - 1:
            pdf.setStrokeColor(LIGHT_RULE)
            pdf.line(x, row_bottom, x + total_width, row_bottom)
        pdf.setFillColor(INK)
        pdf.setFont("TCArial-Bold", 9.4)
        label_lines = wrap(label, "TCArial-Bold", 9.4, platform_width - 16)
        label_y = y - 14
        for line in label_lines:
            pdf.drawString(x + 8, label_y, line)
            label_y -= leading
        pdf.setFont(body_font, body_size)
        body_y = y - 14
        for line in lines:
            pdf.drawString(x + platform_width + 8, body_y, line)
            body_y -= leading
        y = row_bottom

    return y_bottom


def build() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter)
    page_width, page_height = letter
    pdf.setTitle("TEJ Linux Offline Kit - Printable Quick Start")
    pdf.setAuthor("Andrew Andrade, Technology Commons")
    pdf.setSubject("Printable student quick start for Terminal Quest and Bashcrawl")

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
    y = section_heading(pdf, 1, "Get the files", y)

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
    y = draw_bullet(pdf, "Download the TEJ Linux Offline Kit or copy it from the class USB drive.", 43, y, text_width)
    y -= 2
    y = draw_bullet(pdf, "Extract the ZIP. Keep the complete folder together, including hidden files.", 43, y, text_width)
    y -= 2
    y = draw_bullet(pdf, "Open START-HERE.html inside the extracted folder.", 43, y, text_width)
    pdf.setFont("TCArial-Bold", 8.5)
    pdf.setFillColor(MID_GREY)
    pdf.drawString(qr_x - 8, qr_y - 13, "Linux Offline Kit")
    pdf.setFont("TCArial", 8.3)
    pdf.drawString(43, y - 2, "andrewandrade.ca/tech-edu-resources/tej3-4/linux-operating-systems/offline-kit/")
    y = min(y - 25, qr_y - 27)

    y = section_heading(pdf, 2, "Open the correct terminal", y)
    y = draw_platform_table(pdf, y + 2) - 9
    y = draw_wrapped(
        pdf,
        "Waiting for a classroom computer or Internet connection? Use your phone to begin or continue instead of doing nothing.",
        43,
        y,
        526,
        font="TCArial-Bold",
        size=9.2,
        leading=11,
        color=NAVY,
    )
    y -= 5

    y = section_heading(pdf, 3, "Choose the work and file format", y)
    y = draw_wrapped(
        pdf,
        "Terminal Quest inspects the computer and records commands. Bashcrawl teaches navigation through a terminal game. Use ODT in LibreOffice, DOCX in Word or LibreOffice, or TXT if no office program is installed. PDF is for reading or printing.",
        43,
        y,
        526,
        size=10.5,
        leading=13,
    )
    y -= 9

    y = section_heading(pdf, 4, "Start Bashcrawl", y)
    y = draw_wrapped(
        pdf,
        "Copy the complete bashcrawl folder into Home > Games. On a Chromebook, move it into Linux files first. Then run one command at a time:",
        43,
        y,
        526,
        size=10.5,
        leading=13,
    )
    y -= 3
    draw_code(pdf, "cd ~/Games/bashcrawl/entrance", 43, y, 253)
    y = draw_code(pdf, "cat scroll", 316, y, 253)
    y -= 3

    y = section_heading(pdf, 5, "Save now and submit later", y)
    y = draw_bullet(pdf, "Save the completed ODT, DOCX, or TXT file locally with your name in the filename.", 43, y, 526)
    y -= 2
    y = draw_bullet(pdf, "Insert readable screenshots, or save them beside the TXT answer sheet.", 43, y, 526)
    y -= 2
    draw_bullet(pdf, "Upload the completed work to Google Classroom when Internet access returns. Never record passwords, tokens, Wi-Fi credentials, or student numbers.", 43, y, 526)

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
