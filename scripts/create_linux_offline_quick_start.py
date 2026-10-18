from __future__ import annotations

from pathlib import Path

from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import black, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "site" / "assets" / "linux" / "TEJ-Linux-Offline-Kit-Quick-Start.pdf"
PAGE_URL = (
    "https://andrewandrade.ca/tech-edu-resources/"
    "tej3-4/linux-operating-systems/offline-kit/"
)

LEFT = 48
RIGHT = 564
CONTENT_WIDTH = RIGHT - LEFT


def register_fonts() -> None:
    windows_fonts = Path("C:/Windows/Fonts")
    regular = windows_fonts / "arial.ttf"
    bold = windows_fonts / "arialbd.ttf"
    if regular.is_file() and bold.is_file():
        pdfmetrics.registerFont(TTFont("TCArial", str(regular)))
        pdfmetrics.registerFont(TTFont("TCArial-Bold", str(bold)))
        return
    pdfmetrics.registerFont(TTFont("TCArial", "LiberationSans-Regular.ttf"))
    pdfmetrics.registerFont(TTFont("TCArial-Bold", "LiberationSans-Bold.ttf"))


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
    size: float = 12,
    leading: float = 16,
) -> float:
    pdf.setFillColor(black)
    pdf.setFont(font, size)
    for line in wrap(text, font, size, width):
        pdf.drawString(x, y, line)
        y -= leading
    return y


def draw_header(pdf: canvas.Canvas, page_number: int) -> float:
    _, page_height = letter
    pdf.setFillColor(black)
    pdf.setFont("TCArial-Bold", 22)
    pdf.drawString(LEFT, page_height - 54, "TEJ Linux Offline Kit")
    pdf.setFont("TCArial-Bold", 14)
    pdf.drawString(LEFT, page_height - 77, "Printable Quick Start")
    pdf.setLineWidth(1.5)
    pdf.line(LEFT, page_height - 91, RIGHT, page_height - 91)
    pdf.setFont("TCArial", 9)
    pdf.drawRightString(RIGHT, page_height - 74, f"Page {page_number} of 2")
    return page_height - 120


def section_heading(pdf: canvas.Canvas, number: int, title: str, y: float) -> float:
    pdf.setFillColor(black)
    pdf.setFont("TCArial-Bold", 16)
    pdf.drawString(LEFT, y, f"{number}. {title}")
    pdf.setLineWidth(1)
    pdf.line(LEFT, y - 7, RIGHT, y - 7)
    return y - 30


def draw_bullet(pdf: canvas.Canvas, text: str, y: float) -> float:
    pdf.setFillColor(black)
    pdf.circle(LEFT + 4, y + 4, 2, stroke=0, fill=1)
    return draw_wrapped(pdf, text, LEFT + 18, y, CONTENT_WIDTH - 18)


def draw_command_step(
    pdf: canvas.Canvas,
    number: int,
    command: str,
    explanation: str,
    y: float,
) -> float:
    box_height = 72
    pdf.setStrokeColor(black)
    pdf.setFillColor(white)
    pdf.setLineWidth(1.25)
    pdf.rect(LEFT, y - box_height, CONTENT_WIDTH, box_height, stroke=1, fill=1)

    pdf.setFillColor(black)
    pdf.setFont("TCArial-Bold", 13)
    pdf.drawString(LEFT + 14, y - 23, f"Step {number}")
    pdf.setFont("Courier-Bold", 14)
    pdf.drawString(LEFT + 92, y - 23, command)
    pdf.setFont("TCArial-Bold", 11.5)
    pdf.drawRightString(RIGHT - 14, y - 23, "then press Enter")
    draw_wrapped(
        pdf,
        explanation,
        LEFT + 92,
        y - 48,
        CONTENT_WIDTH - 112,
        size=11,
        leading=14,
    )
    return y - box_height - 12


def draw_command_reference(
    pdf: canvas.Canvas,
    command: str,
    explanation: str,
    y: float,
) -> float:
    box_height = 40
    pdf.setStrokeColor(black)
    pdf.setFillColor(white)
    pdf.setLineWidth(1)
    pdf.rect(LEFT, y - box_height, CONTENT_WIDTH, box_height, stroke=1, fill=1)
    pdf.setFillColor(black)
    pdf.setFont("Courier-Bold", 13)
    pdf.drawString(LEFT + 14, y - 25, command)
    pdf.setFont("TCArial", 11)
    pdf.drawString(LEFT + 165, y - 25, explanation)
    return y - box_height - 5


def draw_footer(pdf: canvas.Canvas, page_number: int) -> None:
    pdf.setStrokeColor(black)
    pdf.setLineWidth(0.75)
    pdf.line(LEFT, 50, RIGHT, 50)
    pdf.setFillColor(black)
    pdf.setFont("TCArial", 7.5)
    pdf.drawString(
        LEFT,
        38,
        "CC BY-SA 4.0 | Andrew Andrade | andrewandrade.ca | Source: github.com/mrandrewandrade",
    )
    pdf.drawString(
        LEFT,
        27,
        "Please share, modify and redistribute. Keep the licence, original source, and add your name and links.",
    )
    pdf.setFont("TCArial-Bold", 8)
    pdf.drawRightString(RIGHT, 38, f"Page {page_number} of 2")


def build() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter)
    pdf.setTitle("TEJ Linux Offline Kit - Printable Quick Start")
    pdf.setAuthor("Andrew Andrade, Technology Commons")
    pdf.setSubject("Offline-first student quick start for Terminal Quest and Bashcrawl")

    y = draw_header(pdf, 1)
    y = section_heading(pdf, 1, "Get the kit", y)

    qr_size = 82
    qr_x = RIGHT - qr_size
    qr_y = y - 88
    qr = QrCodeWidget(PAGE_URL)
    qr.barWidth = qr_size
    qr.barHeight = qr_size
    drawing = Drawing(qr_size, qr_size)
    drawing.add(qr)
    drawing.drawOn(pdf, qr_x, qr_y)
    pdf.linkURL(PAGE_URL, (qr_x, qr_y, qr_x + qr_size, qr_y + qr_size), relative=0)

    bullet_width = CONTENT_WIDTH - qr_size - 24
    pdf.setFillColor(black)
    pdf.circle(LEFT + 4, y + 4, 2, stroke=0, fill=1)
    y = draw_wrapped(
        pdf,
        "No Internet: copy TEJ-Linux-Offline-Kit.zip from the class USB drive to Downloads.",
        LEFT + 18,
        y,
        bullet_width - 18,
    )
    y -= 7
    pdf.circle(LEFT + 4, y + 4, 2, stroke=0, fill=1)
    y = draw_wrapped(
        pdf,
        "Internet available: scan the code or use the website to download the same ZIP file.",
        LEFT + 18,
        y,
        bullet_width - 18,
    )
    y -= 7
    pdf.circle(LEFT + 4, y + 4, 2, stroke=0, fill=1)
    y = draw_wrapped(
        pdf,
        "Extract the ZIP. Keep every file and folder together.",
        LEFT + 18,
        y,
        bullet_width - 18,
    )
    y = min(y - 24, qr_y - 25)
    link_y = y
    display_url = (
        "andrewandrade.ca/tech-edu-resources/tej3-4/"
        "linux-operating-systems/offline-kit/"
    )
    y = draw_wrapped(
        pdf,
        display_url,
        LEFT,
        y,
        CONTENT_WIDTH,
        font="TCArial-Bold",
        size=9.5,
        leading=12,
    )
    link_width = pdfmetrics.stringWidth(display_url, "TCArial-Bold", 9.5)
    pdf.setLineWidth(0.75)
    pdf.line(LEFT, link_y - 2, LEFT + link_width, link_y - 2)
    pdf.linkURL(
        PAGE_URL,
        (LEFT, link_y - 4, LEFT + link_width, link_y + 10),
        relative=0,
    )
    y -= 14

    y = section_heading(pdf, 2, "Open the instructions", y)
    y = draw_bullet(pdf, "Open the extracted TEJ-Linux-Offline-Kit folder.", y)
    y -= 8
    y = draw_bullet(
        pdf,
        "Double-click START-HERE.html. It opens in your browser without Internet.",
        y,
    )
    y -= 8
    y = draw_bullet(
        pdf,
        "Choose Computer Detective or Bashcrawl. Open the ODT in LibreOffice, or use the PDF and matching TXT answer sheet.",
        y,
    )
    y -= 18

    y = section_heading(pdf, 3, "Prepare Bashcrawl", y)
    y = draw_bullet(
        pdf,
        "Copy the complete bashcrawl folder from the extracted kit.",
        y,
    )
    y -= 8
    y = draw_bullet(
        pdf,
        "Open Home in the Files app. Create a folder named Games. Paste bashcrawl inside Games.",
        y,
    )
    y -= 8
    y = draw_bullet(
        pdf,
        "Open Terminal in Linux Mint by pressing Ctrl + Alt + T. This works in the installed system and in the live USB session.",
        y,
    )
    y -= 18
    pdf.setLineWidth(1.25)
    pdf.rect(LEFT, y - 75, CONTENT_WIDTH, 75, stroke=1, fill=0)
    draw_wrapped(
        pdf,
        "Using another device?",
        LEFT + 14,
        y - 23,
        CONTENT_WIDTH - 28,
        font="TCArial-Bold",
        size=12.5,
        leading=15,
    )
    draw_wrapped(
        pdf,
        "The website has setup instructions for Windows, Mac, Chromebook, Linux, Android, and iPhone. A phone is slower and more difficult than a computer, but it is possible.",
        LEFT + 14,
        y - 45,
        CONTENT_WIDTH - 28,
        size=11,
        leading=14,
    )
    draw_footer(pdf, 1)
    pdf.showPage()

    y = draw_header(pdf, 2)
    y = section_heading(pdf, 4, "Start Bashcrawl", y)
    y = draw_wrapped(
        pdf,
        "Complete each step separately. Type only the command shown, then press Enter. Wait for it to finish before moving to the next step. Do not type the $ prompt symbol.",
        LEFT,
        y,
        CONTENT_WIDTH,
        font="TCArial-Bold",
        size=12.5,
        leading=17,
    )
    y -= 11
    y = draw_command_step(
        pdf,
        1,
        "cd ~/Games/bashcrawl/entrance",
        "Go to the Bashcrawl entrance folder.",
        y,
    )
    y = draw_command_step(
        pdf,
        2,
        "cat scroll",
        "Read the instructions in the entrance room.",
        y,
    )

    y = section_heading(pdf, 5, "Commands you will use while playing", y - 1)
    y = draw_wrapped(
        pdf,
        "Type one command, press Enter, read the result, and then decide what to do next.",
        LEFT,
        y,
        CONTENT_WIDTH,
        font="TCArial-Bold",
        size=11.5,
        leading=15,
    )
    y -= 9
    y = draw_command_reference(pdf, "ls", "List what is in the current room.", y)
    y = draw_command_reference(pdf, "pwd", "Show the folder you are currently in.", y)
    y = draw_command_reference(pdf, "cat scroll", "Read the scroll in the current room.", y)
    y = draw_command_reference(pdf, "cd cellar", "Example: enter a room named cellar.", y)
    y = draw_command_reference(pdf, "cd ..", "Go back one folder or room.", y)
    y = draw_command_reference(pdf, "ls -a", "List everything, including hidden items.", y)

    y -= 10
    draw_wrapped(
        pdf,
        "Important: cellar is only an example. Replace cellar with the room name that you see after running ls. Complete the answer sheet, save your screenshots, and submit your work when Internet is available.",
        LEFT,
        y,
        CONTENT_WIDTH,
        font="TCArial-Bold",
        size=11,
        leading=14,
    )
    draw_footer(pdf, 2)
    pdf.showPage()
    pdf.save()
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    build()
