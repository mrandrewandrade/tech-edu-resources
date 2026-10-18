from __future__ import annotations

from pathlib import Path

from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "site" / "assets" / "linux" / "TEJ-Linux-Offline-Kit-Quick-Start.pdf"
PAGE_URL = (
    "https://andrewandrade.ca/tech-edu-resources/"
    "tej3-4/linux-operating-systems/offline-kit/"
)

NAVY = HexColor("#163A5F")
BLUE = HexColor("#2468A2")
PALE_BLUE = HexColor("#EAF3FA")
PALE_GREY = HexColor("#F4F6F8")
MID_GREY = HexColor("#52616B")
TEXT = HexColor("#17212B")
GREEN = HexColor("#246B4A")


def wrapped_lines(text: str, font: str, size: float, width: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if stringWidth(candidate, font, size) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_text(
    pdf: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    *,
    font: str = "Helvetica",
    size: float = 9.3,
    leading: float = 12,
    color=TEXT,
) -> float:
    pdf.setFont(font, size)
    pdf.setFillColor(color)
    for line in wrapped_lines(text, font, size, width):
        pdf.drawString(x, y, line)
        y -= leading
    return y


def draw_bullets(
    pdf: canvas.Canvas,
    items: list[tuple[str, str]],
    x: float,
    y: float,
    width: float,
    *,
    size: float = 9.1,
    leading: float = 11.5,
) -> float:
    for label, body in items:
        pdf.setFillColor(BLUE)
        pdf.circle(x + 3, y + 3, 1.7, stroke=0, fill=1)
        label_width = stringWidth(label, "Helvetica-Bold", size)
        pdf.setFillColor(TEXT)
        pdf.setFont("Helvetica-Bold", size)
        pdf.drawString(x + 12, y, label)
        remainder_width = max(20, width - 12 - label_width)
        first_lines = wrapped_lines(body, "Helvetica", size, remainder_width)
        if first_lines:
            pdf.setFont("Helvetica", size)
            pdf.drawString(x + 12 + label_width, y, first_lines[0])
            y -= leading
            for line in first_lines[1:]:
                pdf.drawString(x + 12, y, line)
                y -= leading
        else:
            y -= leading
        y -= 2
    return y


def draw_box(
    pdf: canvas.Canvas,
    x: float,
    y_top: float,
    width: float,
    height: float,
    title: str,
    *,
    fill=white,
    title_color=NAVY,
) -> tuple[float, float, float]:
    y_bottom = y_top - height
    pdf.setFillColor(fill)
    pdf.setStrokeColor(HexColor("#CAD5DE"))
    pdf.roundRect(x, y_bottom, width, height, 8, stroke=1, fill=1)
    pdf.setFillColor(title_color)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x + 14, y_top - 22, title)
    return x + 14, y_top - 40, width - 28


def draw_code(pdf: canvas.Canvas, code: str, x: float, y: float, width: float) -> float:
    pdf.setFillColor(HexColor("#15202B"))
    pdf.roundRect(x, y - 17, width, 24, 4, stroke=0, fill=1)
    pdf.setFillColor(white)
    pdf.setFont("Courier-Bold", 9)
    pdf.drawString(x + 10, y - 8, code)
    return y - 31


def build() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter)
    page_width, page_height = letter
    pdf.setTitle("TEJ Linux Offline Kit - Printable Quick Start")
    pdf.setAuthor("Technology Commons")
    pdf.setSubject("One-page student instructions for the TEJ Linux Offline Kit")

    margin = 34
    content_width = page_width - 2 * margin

    # Header
    pdf.setFillColor(NAVY)
    pdf.rect(0, page_height - 102, page_width, 102, stroke=0, fill=1)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(margin, page_height - 42, "TEJ Linux Offline Kit")
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawString(margin, page_height - 64, "Printable Quick Start")
    pdf.setFont("Helvetica", 8.2)
    pdf.drawString(margin, page_height - 84, PAGE_URL)

    qr = QrCodeWidget(PAGE_URL)
    qr.barWidth = 66
    qr.barHeight = 66
    pdf.setFillColor(white)
    pdf.roundRect(page_width - margin - 73, page_height - 87, 72, 72, 4, stroke=0, fill=1)
    drawing = Drawing(66, 66)
    drawing.add(qr)
    drawing.drawOn(pdf, page_width - margin - 70, page_height - 84)

    # Primary instruction banner
    banner_top = page_height - 116
    pdf.setFillColor(PALE_BLUE)
    pdf.setStrokeColor(BLUE)
    pdf.roundRect(margin, banner_top - 58, content_width, 58, 8, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(margin + 14, banner_top - 20, "Download or copy the folder, extract the ZIP, then open START-HERE.html.")
    draw_text(
        pdf,
        "Keep the whole folder together. Hidden folders are part of Bashcrawl.",
        margin + 14,
        banner_top - 40,
        content_width - 28,
        size=9.2,
        color=MID_GREY,
    )

    gap = 12
    col_width = (content_width - gap) / 2
    row_top = banner_top - 72

    # Formats
    x, y, w = draw_box(pdf, margin, row_top, col_width, 156, "1. Choose an editable file")
    draw_bullets(
        pdf,
        [
            ("ODT: ", "best choice for LibreOffice Writer."),
            ("DOCX: ", "works in Microsoft Word and LibreOffice."),
            ("TXT: ", "use the answer sheet if no office program is installed."),
            ("PDF: ", "read or print it; do not use it as the editable submission."),
        ],
        x,
        y,
        w,
    )

    # Activities
    x2, y2, w2 = draw_box(
        pdf,
        margin + col_width + gap,
        row_top,
        col_width,
        156,
        "2. Pick an activity",
    )
    draw_bullets(
        pdf,
        [
            ("Terminal Quest: ", "inspect the computer and practise terminal commands."),
            ("Bashcrawl: ", "learn navigation by playing the included terminal game."),
            ("Xfce Appearance: ", "inspect and run the script, then explain your changes."),
        ],
        x2,
        y2,
        w2,
    )

    # Offline setup and commands
    commands_top = row_top - 168
    x3, y3, w3 = draw_box(pdf, margin, commands_top, content_width, 184, "3. Work offline")
    left_w = 258
    y_left = draw_text(
        pdf,
        "Linux Mint and Mac terminal activities work without Internet. WSL, Termux, and iSH only work offline if they were installed earlier.",
        x3,
        y3,
        left_w,
        size=9.2,
        leading=12,
    )
    y_left -= 5
    pdf.setFont("Helvetica-Bold", 9.2)
    pdf.setFillColor(GREEN)
    pdf.drawString(x3, y_left, "Check for LibreOffice Writer")
    y_left = draw_code(pdf, "libreoffice --version", x3, y_left - 10, left_w)
    draw_text(
        pdf,
        "If it is missing, use the TXT answer sheet. Do not install unknown software from the USB drive.",
        x3,
        y_left,
        left_w,
        size=8.8,
        leading=11,
        color=MID_GREY,
    )

    divider_x = x3 + left_w + 14
    pdf.setStrokeColor(HexColor("#D7E0E7"))
    pdf.line(divider_x, commands_top - 166, divider_x, commands_top - 42)
    right_x = divider_x + 16
    right_w = w3 - left_w - 30
    pdf.setFillColor(GREEN)
    pdf.setFont("Helvetica-Bold", 9.2)
    pdf.drawString(right_x, y3, "Start Bashcrawl")
    y_right = draw_text(
        pdf,
        "Use the file manager to copy the complete bashcrawl folder into Home > Games. Then run:",
        right_x,
        y3 - 18,
        right_w,
        size=9.1,
        leading=12,
    )
    y_right -= 4
    y_right = draw_code(pdf, "cd ~/Games/bashcrawl/entrance", right_x, y_right, right_w)
    draw_code(pdf, "cat scroll", right_x, y_right, right_w)

    # Submission
    submit_top = commands_top - 196
    x4, y4, w4 = draw_box(
        pdf,
        margin,
        submit_top,
        content_width,
        114,
        "4. Save now and submit when Internet returns",
        fill=PALE_GREY,
    )
    draw_bullets(
        pdf,
        [
            ("Name the file clearly: ", "include your name and the assignment title."),
            ("Keep evidence: ", "insert screenshots in the document or save them beside the TXT file."),
            ("Upload later: ", "submit the completed ODT, DOCX, or TXT file to Google Classroom."),
            ("Protect your privacy: ", "never record passwords, tokens, Wi-Fi credentials, or student numbers."),
        ],
        x4,
        y4,
        w4,
        size=8.8,
        leading=10.5,
    )

    # Footer
    pdf.setStrokeColor(HexColor("#CAD5DE"))
    pdf.line(margin, 31, page_width - margin, 31)
    pdf.setFillColor(MID_GREY)
    pdf.setFont("Helvetica", 7.6)
    pdf.drawString(margin, 19, "Technology Commons | CC BY-SA 4.0 | Print this page or scan the QR code for the download.")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 7.6)
    pdf.drawRightString(page_width - margin, 19, "TEJ Linux Offline Kit")

    pdf.showPage()
    pdf.save()
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    build()
