#!/usr/bin/env python3
"""Build the printable Bring Your Brand to Life student handout."""

from __future__ import annotations

from pathlib import Path

from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "site" / "assets" / "animate-your-logo" / "animate-your-logo-handout.pdf"
LESSON_URL = "https://andrewandrade.ca/tech-edu-resources/design-fabrication/02-digital-design/animate-your-logo.html"

NAVY = colors.HexColor("#16324f")
GREEN = colors.HexColor("#216147")
COPPER = colors.HexColor("#a45a2a")
INK = colors.HexColor("#172033")
PALE = colors.HexColor("#eef4f1")
GRID = colors.HexColor("#a9b8c5")


def paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def make_qr_code(url: str, size: float = 1.05 * inch) -> Drawing:
    widget = QrCodeWidget(url)
    bounds = widget.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    drawing = Drawing(size, size, transform=[size / width, 0, 0, size / height, 0, 0])
    drawing.add(widget)
    return drawing


def decorate_page(canvas, doc) -> None:
    canvas.saveState()
    width, height = letter
    canvas.setStrokeColor(GREEN)
    canvas.setLineWidth(2)
    canvas.line(0.55 * inch, height - 0.42 * inch, width - 0.55 * inch, height - 0.42 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#52606d"))
    canvas.drawString(0.55 * inch, 0.38 * inch, "TAS · Bring Your Brand to Life")
    canvas.drawRightString(width - 0.55 * inch, 0.38 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.58 * inch,
        bottomMargin=0.6 * inch,
        title="Bring Your Brand to Life: Animate Your Logo",
        author="Tech Ed Resources",
        subject="Four-day TAS logo animation assignment",
    )

    sample = getSampleStyleSheet()
    title = ParagraphStyle(
        "Title",
        parent=sample["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=25,
        textColor=NAVY,
        alignment=TA_LEFT,
        spaceAfter=8,
    )
    subtitle = ParagraphStyle(
        "Subtitle",
        parent=sample["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=14,
        textColor=GREEN,
        spaceAfter=10,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=sample["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13.5,
        leading=16,
        textColor=NAVY,
        spaceBefore=8,
        spaceAfter=5,
    )
    body = ParagraphStyle(
        "Body",
        parent=sample["BodyText"],
        fontName="Helvetica",
        fontSize=9.6,
        leading=12.2,
        textColor=INK,
        spaceAfter=4,
    )
    small = ParagraphStyle(
        "Small",
        parent=body,
        fontSize=8.3,
        leading=10.2,
        spaceAfter=2,
    )
    tiny = ParagraphStyle(
        "Tiny",
        parent=body,
        fontSize=7.2,
        leading=8.8,
        spaceAfter=0,
    )
    white = ParagraphStyle(
        "White",
        parent=body,
        fontName="Helvetica-Bold",
        textColor=colors.white,
        alignment=TA_CENTER,
    )

    story = [
        paragraph("Bring Your Brand to Life", title),
        paragraph("Animate the logo you already designed · Four class periods · Due at the end of Day 4", subtitle),
    ]

    brief = Table(
        [[paragraph("<b>Do not design a new logo.</b> Make a 5–8 second animated intro from your existing logo. Give it a clear beginning, middle, and ending. Your motion should match your brand.", body)]],
        colWidths=[7.35 * inch],
    )
    brief.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("BOX", (0, 0), (-1, -1), 1, GREEN),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.extend([brief, Spacer(1, 5), paragraph("Choose one direction", h2)])

    directions = Table(
        [
            [paragraph("<b>Gaming / creator</b><br/>Energetic, bold, punchy", small), paragraph("<b>Personal brand</b><br/>Clear, confident, authentic", small), paragraph("<b>Product / fashion / business</b><br/>Polished, deliberate, professional", small)],
        ],
        colWidths=[2.45 * inch] * 3,
    )
    directions.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.8, GRID),
        ("INNERGRID", (0, 0), (-1, -1), 0.6, GRID),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.extend([directions, paragraph("Your four days", h2)])

    schedule_data = [
        [paragraph("DAY", white), paragraph("MAKE", white), paragraph("END-OF-DAY CHECKPOINT", white)],
        [paragraph("1", body), paragraph("Learn the editor. Try three motion presets. Choose the direction and emotion.", small), paragraph("A rough motion test plays.", small)],
        [paragraph("2", body), paragraph("Build a complete 5–8 second draft with a beginning, middle, and ending.", small), paragraph("Version 1 is exported.", small)],
        [paragraph("3", body), paragraph("Improve timing, legibility, and at least one weak moment after feedback.", small), paragraph("Version 2 is visibly better.", small)],
        [paragraph("4", body), paragraph("Peer test, fix, export, reopen the file, and submit through Classroom.", small), paragraph("All files and the design sentence are submitted.", small)],
    ]
    schedule = Table(schedule_data, colWidths=[0.5 * inch, 4.25 * inch, 2.6 * inch], repeatRows=1)
    schedule.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.6, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#f8fafc")),
        ("BACKGROUND", (0, 4), (-1, 4), colors.HexColor("#f8fafc")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.extend([schedule, paragraph("Final checklist", h2)])

    checklist_items = [
        "[ ] 5–8 seconds long",
        "[ ] Uses my existing logo",
        "[ ] At least two intentional changes (move, scale, rotate, fade, or reveal)",
        "[ ] Timing makes some moments faster or slower on purpose",
        "[ ] Clear beginning, middle, and ending",
        "[ ] Motion matches my chosen brand emotion",
        "[ ] One visible improvement after testing",
        "[ ] Final export was reopened and checked",
    ]
    checks = Table(
        [[paragraph(checklist_items[i], small), paragraph(checklist_items[i + 1], small)] for i in range(0, len(checklist_items), 2)],
        colWidths=[3.65 * inch, 3.65 * inch],
    )
    checks.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.extend([checks, PageBreak(), paragraph("Assessment rubric", title)])

    rubric_data = [
        [paragraph("CRITERION", white), paragraph("BEGINNING", white), paragraph("MEETING", white), paragraph("STRONGER WORK", white)],
        [paragraph("<b>Movement and timing are intentional</b><br/>30%", small), paragraph("Motion is missing, random, or rushed.", tiny), paragraph("Two or more controlled changes create a clear 5–8 second sequence.", tiny), paragraph("Varied timing creates emphasis, a readable hold, and a confident rhythm.", tiny)],
        [paragraph("<b>Animation communicates the brand or emotion</b><br/>30%", small), paragraph("The logo is difficult to read or the motion does not fit the feeling.", tiny), paragraph("The logo stays readable and the motion supports the named emotion.", tiny), paragraph("Restraint, hierarchy, and polish strengthen the brand message.", tiny)],
        [paragraph("<b>Testing, feedback, and improvement</b><br/>25%", small), paragraph("Feedback or a visible improvement is missing.", tiny), paragraph("A peer test leads to one meaningful change.", tiny), paragraph("The improvement solves a named communication or timing problem.", tiny)],
        [paragraph("<b>Finished and submitted correctly</b><br/>15%", small), paragraph("Required files, reopen check, or sentence are missing.", tiny), paragraph("The final plays and the accepted files and sentence are included.", tiny), paragraph("The final package is complete, organized, and easy to verify.", tiny)],
    ]
    rubric = Table(rubric_data, colWidths=[1.22 * inch, 2.03 * inch, 2.03 * inch, 2.03 * inch], repeatRows=1)
    rubric.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.6, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 1), (0, -1), PALE),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.extend([rubric, paragraph("Submit through Google Classroom", h2)])

    submit = Table(
        [[paragraph("<b>1.</b> <font name='Courier'>studentnumber-lastname-logo-animation.mp4</font> <b>or</b> <font name='Courier'>.gif</font><br/><b>2.</b> Editable project: <font name='Courier'>.smooth</font> or <font name='Courier'>.psd</font> when supported<br/><b>3.</b> One sentence: <i>My most important design choice was ___ because ___.</i>", body)]],
        colWidths=[7.35 * inch],
    )
    submit.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fff7ed")),
        ("BOX", (0, 0), (-1, -1), 1, COPPER),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.extend([submit, paragraph("Quick help", h2)])

    help_table = Table(
        [
            [paragraph("<b>Too fast?</b><br/>Spread the timeline points apart and add a short hold.", small), paragraph("<b>Feels boring?</b><br/>Change timing first. Add one purposeful reveal, not many effects.", small)],
            [paragraph("<b>Logo is blurry?</b><br/>Use the largest clean PNG, SVG, or layered PSD available.", small), paragraph("<b>Export is still?</b><br/>Export MP4 or GIF, then reopen the exported file to test it.", small)],
        ],
        colWidths=[3.65 * inch, 3.65 * inch],
    )
    help_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.6, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(help_table)

    qr = make_qr_code(LESSON_URL)
    link = paragraph(f"<b>Full tutorial, starter, example, and progressive hints</b><br/><link href='{LESSON_URL}' color='#216147'>{LESSON_URL}</link>", small)
    qr_box = Table([[qr, link]], colWidths=[1.2 * inch, 6.1 * inch])
    qr_box.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(KeepTogether([qr_box]))

    doc.build(story, onFirstPage=decorate_page, onLaterPages=decorate_page)
    print(f"Built {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
