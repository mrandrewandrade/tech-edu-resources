"""Build the cumulative Circuits + Python life checkpoint and teacher key."""

from pathlib import Path
import subprocess

import schemdraw
import schemdraw.elements as elm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"
TEMP_DIR = ROOT / "tmp" / "pdfs"
LOGO = ROOT / "site" / "assets" / "branding" / "emblem" / "technology-commons-hands.png"

STUDENT_PDF = OUTPUT_DIR / "life-checkpoint-circuits-python-next-semester.pdf"
KEY_PDF = OUTPUT_DIR / "life-checkpoint-circuits-python-next-semester-answer-key.pdf"
FULL_SCHEMATIC = TEMP_DIR / "checkpoint-two-loop.png"
LOOP1_SCHEMATIC = TEMP_DIR / "checkpoint-loop-1.png"
LOOP2_SCHEMATIC = TEMP_DIR / "checkpoint-loop-2.png"
SERIES_SCHEMATIC = TEMP_DIR / "checkpoint-series.png"

INK = colors.black
WHITE = colors.white

FOOTER_LINE_1 = (
    "CC BY-SA 4.0 · Created by Andrew Andrade · andrewandrade.ca · "
    "Source: github.com/mrandrewandrade"
)
FOOTER_LINE_2 = "Please share, modify and redistribute. If you change this file, do not remove:"
FOOTER_LINE_3 = (
    "CC BY-SA 4.0. Original Source: andrewandrade.ca and add your own name + links. "
    "Sharing is caring!"
)


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", "C:/Windows/Fonts/arialbd.ttf"))
    pdfmetrics.registerFont(TTFont("Consolas", "C:/Windows/Fonts/consola.ttf"))


def styles():
    sample = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=sample["Title"],
            fontName="Arial-Bold",
            fontSize=22,
            leading=24,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=1,
        ),
        "key_title": ParagraphStyle(
            "KeyTitle",
            parent=sample["Title"],
            fontName="Arial-Bold",
            fontSize=18.5,
            leading=21,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=1,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=sample["Normal"],
            fontName="Arial-Bold",
            fontSize=11,
            leading=14,
            textColor=INK,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=sample["Heading2"],
            fontName="Arial-Bold",
            fontSize=15,
            leading=18,
            textColor=INK,
            spaceBefore=4,
            spaceAfter=3,
        ),
        "question": ParagraphStyle(
            "Question",
            parent=sample["BodyText"],
            fontName="Arial-Bold",
            fontSize=11.5,
            leading=14,
            textColor=INK,
            spaceBefore=2,
            spaceAfter=2,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=sample["BodyText"],
            fontName="Arial",
            fontSize=11,
            leading=14,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=3,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=sample["BodyText"],
            fontName="Arial",
            fontSize=9.5,
            leading=12,
            textColor=INK,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=sample["Code"],
            fontName="Consolas",
            fontSize=10.5,
            leading=14,
            textColor=INK,
            leftIndent=3,
        ),
        "kcl_question": ParagraphStyle(
            "KCLQuestion",
            parent=sample["Heading3"],
            fontName="Arial-Bold",
            fontSize=14,
            leading=17,
            textColor=INK,
            spaceBefore=2,
            spaceAfter=4,
        ),
        "kcl_code": ParagraphStyle(
            "KCLCode",
            parent=sample["Code"],
            fontName="Consolas",
            fontSize=14,
            leading=19,
            textColor=INK,
            leftIndent=5,
        ),
    }


def save_drawing(drawing, name: str) -> Path:
    svg = TEMP_DIR / f"{name}.svg"
    png = TEMP_DIR / f"{name}.png"
    drawing.save(str(svg), transparent=False)
    subprocess.run(
        ["magick", "-background", "white", "-density", "400", str(svg), str(png)],
        check=True,
    )
    return png


def make_schematics() -> None:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    # Complete two-loop network. Every label has its own whitespace zone.
    d = schemdraw.Drawing(show=False)
    d.config(unit=3.0, fontsize=15, lw=2.1, color="black")
    d += elm.SourceV().up()
    d += elm.Resistor().right()
    top_mid = d.here
    d += elm.Dot().at(top_mid)
    d += elm.Resistor().right()
    d += elm.SourceV().down()
    d += elm.Line().left().length(3.0)
    bottom_mid = d.here
    d += elm.Dot().at(bottom_mid)
    d += elm.Line().left().length(3.0)
    d += elm.Resistor().at(top_mid).down().to(bottom_mid)

    d += elm.Label().at((-1.25, 1.50)).label("VS1\n12 V")
    d += elm.Label().at((7.25, 1.50)).label("VS2\n5 V")
    d += elm.Label().at((1.50, 3.42)).label("R1 = 5 kΩ")
    d += elm.Label().at((4.50, 3.42)).label("R2 = 7 kΩ")
    d += elm.Label().at((4.15, 1.45)).label("R3\n2 kΩ")
    d += elm.Arrow().at((0.90, 3.95)).right().length(1.05)
    d += elm.Label().at((1.43, 4.24)).label("I1")
    d += elm.Arrow().at((4.00, 3.95)).right().length(1.05)
    d += elm.Label().at((4.53, 4.24)).label("I2")
    d += elm.Arrow().at((2.64, 2.60)).down().length(0.90)
    d += elm.Label().at((2.18, 2.44)).label("I3")
    save_drawing(d, "checkpoint-two-loop")

    # Isolated left loop for the teacher key.
    d = schemdraw.Drawing(show=False)
    d.config(unit=3.0, fontsize=13, lw=2.1, color="black")
    d += elm.SourceV().up()
    d += elm.Resistor().at((0, 3)).right()
    d += elm.Resistor().down()
    d += elm.Line().left()
    d += elm.Label().at((-1.20, 1.50)).label("VS1\n12 V")
    d += elm.Label().at((1.50, 3.58)).label("R1\n5 kΩ")
    d += elm.Label().at((4.15, 1.50)).label("R3\n2 kΩ")
    d += elm.Arrow().at((0.75, 4.22)).right().length(1.00)
    d += elm.Label().at((1.25, 4.48)).label("I1")
    d += elm.Arrow().at((3.55, 2.45)).down().length(0.85)
    d += elm.Label().at((3.88, 2.35)).label("I3")
    save_drawing(d, "checkpoint-loop-1")

    # Isolated right loop for the teacher key.
    d = schemdraw.Drawing(show=False)
    d.config(unit=3.0, fontsize=13, lw=2.1, color="black")
    d += elm.Resistor().at((0, 3)).right()
    d += elm.SourceV().down()
    d += elm.Line().left()
    d += elm.Resistor().up()
    d += elm.Label().at((1.50, 3.58)).label("R2\n7 kΩ")
    d += elm.Label().at((4.15, 1.50)).label("VS2\n5 V")
    d += elm.Label().at((-1.15, 1.50)).label("R3\n2 kΩ")
    d += elm.Arrow().at((0.75, 4.22)).right().length(1.00)
    d += elm.Label().at((1.25, 4.48)).label("I2")
    d += elm.Arrow().at((-0.55, 2.45)).down().length(0.85)
    d += elm.Label().at((-0.88, 2.35)).label("I3")
    save_drawing(d, "checkpoint-loop-2")

    # Simple series circuit expected in the schematic-drawing task.
    d = schemdraw.Drawing(show=False)
    d.config(unit=2.6, fontsize=15, lw=2.1, color="black")
    d += elm.SourceV().up()
    d += elm.Switch().right()
    d += elm.Resistor().right()
    d += elm.Line().down()
    d += elm.Line().left().length(5.2)
    d += elm.Label().at((-1.20, 1.30)).label("VS\n9 V")
    d += elm.Label().at((1.30, 3.20)).label("S1")
    d += elm.Label().at((3.90, 3.38)).label("R1\n1 kΩ")
    d += elm.Arrow().at((3.35, 4.02)).right().length(1.00)
    d += elm.Label().at((3.85, 4.30)).label("I")
    save_drawing(d, "checkpoint-series")


def header(st, teacher=False):
    title = "Life Checkpoint: Circuits + Python"
    if teacher:
        title += " - Teacher Key"
    title_style = st["key_title"] if teacher else st["title"]
    subtitle = (
        "The only test is life. And this is life."
        if not teacher
        else "Mark each step independently. Continue after an incorrect earlier answer."
    )
    text = Table(
        [[Paragraph(title, title_style)], [Paragraph(subtitle, st["subtitle"])]],
        colWidths=[5.82 * inch],
    )
    text.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    table = Table(
        [[Image(str(LOGO), width=0.64 * inch, height=0.64 * inch), text]],
        colWidths=[0.76 * inch, 5.82 * inch],
    )
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return table


def identity_table():
    table = Table(
        [["Name:", "", "Date:", ""], ["Class:", "", "Core mark:", " / 44"]],
        colWidths=[0.55 * inch, 2.45 * inch, 0.85 * inch, 2.35 * inch],
        rowHeights=[0.31 * inch, 0.31 * inch],
    )
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10.5),
        ("LINEBELOW", (1, 0), (1, -1), 0.9, INK),
        ("LINEBELOW", (3, 0), (3, -1), 0.9, INK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return table


def box(content, st, width=6.48 * inch, padding=7, style="body"):
    flowable = content if not isinstance(content, str) else Paragraph(content, st[style])
    table = Table([[flowable]], colWidths=[width])
    table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1.0, INK),
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("LEFTPADDING", (0, 0), (-1, -1), padding),
        ("RIGHTPADDING", (0, 0), (-1, -1), padding),
        ("TOPPADDING", (0, 0), (-1, -1), padding),
        ("BOTTOMPADDING", (0, 0), (-1, -1), padding),
    ]))
    return table


def code_box(lines, st, width=6.35 * inch):
    rows = [[Paragraph(line.replace(" ", "&nbsp;"), st["code"])] for line in lines]
    table = Table(rows, colWidths=[width])
    table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1.0, INK),
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def kcl_response_box(st):
    lines = [
        "I1 = ______________ + ______________",
        "I3 = ______________ - ______________",
    ]
    rows = [[Paragraph(line.replace(" ", "&nbsp;"), st["kcl_code"])] for line in lines]
    table = Table(rows, colWidths=[6.35 * inch], rowHeights=[0.52 * inch, 0.52 * inch])
    table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1.0, INK),
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return table


def blank_box(width, height, label, st):
    table = Table(
        [[Paragraph(label, st["question"])], [""]],
        colWidths=[width],
        rowHeights=[0.33 * inch, height - 0.33 * inch],
    )
    table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1.0, INK),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, INK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def answer_lines(rows=1, width=6.35 * inch, row_height=0.28 * inch):
    table = Table([[""] for _ in range(rows)], colWidths=[width], rowHeights=[row_height] * rows)
    table.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.8, INK)]))
    return table


def mark_note(text, st):
    return Paragraph(f"<b>Marking:</b> {text}", st["small"])


def matrix_table(answers=False):
    values = [["7", "-2", "12"], ["-2", "9", "5"]] if answers else [["", "", ""], ["", "", ""]]
    rows = [
        ["Equation", "I1 coefficient", "I2 coefficient", "Right side"],
        ["Loop 1", *values[0]],
        ["Loop 2", *values[1]],
    ]
    table = Table(
        rows,
        colWidths=[1.05 * inch, 1.72 * inch, 1.72 * inch, 1.40 * inch],
        rowHeights=[0.31 * inch, 0.37 * inch, 0.37 * inch],
    )
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 1), (-1, -1), "Consolas"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("GRID", (0, 0), (-1, -1), 0.8, INK),
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return table


def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(INK)
    canvas.setFillColor(INK)
    canvas.setLineWidth(0.7)
    canvas.line(0.72 * inch, 0.62 * inch, 7.78 * inch, 0.62 * inch)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(0.72 * inch, 0.68 * inch, "Life Checkpoint | Circuits + Python")
    canvas.drawRightString(7.78 * inch, 0.68 * inch, f"Page {doc.page}")
    canvas.setFont("Helvetica", 7.1)
    canvas.drawCentredString(4.25 * inch, 0.49 * inch, FOOTER_LINE_1)
    canvas.setFont("Helvetica", 6.7)
    canvas.drawCentredString(4.25 * inch, 0.37 * inch, FOOTER_LINE_2)
    canvas.drawCentredString(4.25 * inch, 0.26 * inch, FOOTER_LINE_3)
    canvas.restoreState()


def build_student(st):
    story = [
        header(st),
        Spacer(1, 5),
        identity_table(),
        Spacer(1, 6),
        box(
            "No calculator is needed; the numbers are chosen to give clean answers. Work one line at a time. "
            "If one section stops you, continue to the next. If it all checks, you may pop off like you won "
            "the last stock in Smash Bros. Keep the controller on the desk.",
            st,
        ),
        Spacer(1, 6),
        Paragraph("A. Ohm's law and power (8 marks)", st["section"]),
        Paragraph(
            "A 12 V test supply is connected across a 2.0 kΩ resistor. Show the formula, substitution, answer, and unit.",
            st["body"],
        ),
        code_box([
            "2.0 kΩ = __________ Ω",
            "I = V / R = __________ / __________ = __________ A = __________ mA",
            "P = V x I = __________ x __________ = __________ W = __________ mW",
        ], st),
        Spacer(1, 5),
        Paragraph(
            "The resistor rating must be at least twice the calculated power. Circle one: &nbsp; 1/8 W &nbsp;&nbsp; 1/4 W",
            st["question"],
        ),
        Spacer(1, 6),
        Paragraph("B. Draw a simple schematic (4 marks)", st["section"]),
        Paragraph(
            "Draw one series loop containing a 9 V source, a closed switch S1, and resistor R1 = 1 kΩ. "
            "Use schematic symbols, label every part, show source polarity, and add one conventional-current arrow.",
            st["body"],
        ),
        blank_box(6.45 * inch, 3.50 * inch, "Your schematic", st),
        Spacer(1, 5),
        Paragraph("Page 1 mark: ____ / 12", st["question"]),
        PageBreak(),

        header(st),
        Spacer(1, 5),
        Paragraph("C. Read and redraw the two-loop circuit (8 marks)", st["section"]),
        Paragraph(
            "A controller test fixture uses two isolated supplies. Read the complete schematic, then redraw each loop by itself. "
            "Do not copy components that are not part of that loop.",
            st["body"],
        ),
        Image(str(FULL_SCHEMATIC), width=6.55 * inch, height=3.00 * inch),
        Table(
            [[
                blank_box(3.12 * inch, 3.00 * inch, "1. Loop 1 only (3 marks)", st),
                blank_box(3.12 * inch, 3.00 * inch, "2. Loop 2 only (3 marks)", st),
            ]],
            colWidths=[3.17 * inch, 3.17 * inch],
            style=TableStyle([
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]),
        ),
        Spacer(1, 7),
        Paragraph("3. Write KCL at the top centre node (2 marks)", st["kcl_question"]),
        kcl_response_box(st),
        Spacer(1, 8),
        Paragraph("Page 2 mark: ____ / 8", st["question"]),
        PageBreak(),

        header(st),
        Spacer(1, 5),
        Paragraph("D. KVL, standard form, and solution (12 marks)", st["section"]),
        Paragraph("1. Loop 1 (4 marks)", st["question"]),
        code_box([
            "+12 - ______ I1 - ______ I3 = 0",
            "+12 - 5I1 - 2( __________________ ) = 0",
            "Standard form: ______ I1 + ______ I2 = ______",
        ], st),
        Spacer(1, 5),
        Paragraph("2. Loop 2 (4 marks)", st["question"]),
        code_box([
            "+5 - ______ I2 + ______ I3 = 0",
            "+5 - 7I2 + 2( __________________ ) = 0",
            "Standard form: ______ I1 + ______ I2 = ______",
        ], st),
        Spacer(1, 5),
        box(
            "<b>RESTART POINT:</b> If an earlier line stopped you, use 7I1 - 2I2 = 12 and -2I1 + 9I2 = 5 below.",
            st,
        ),
        Spacer(1, 5),
        Paragraph("3. Solve and check (4 marks)", st["question"]),
        code_box([
            "I1 = __________________ mA    I2 = __________________ mA",
            "I3 = I1 - I2 = __________________ mA",
            "One KCL or KVL check: __________________________________________",
        ], st),
        Spacer(1, 6),
        Paragraph("E. Matrix bridge (4 separate marks)", st["section"]),
        Paragraph("Use variable order [I1, I2]. Copy one standard-form equation into each row.", st["body"]),
        matrix_table(answers=False),
        Spacer(1, 4),
        code_box([
            "[ ____  ____ ] [ I1 ]   [ ____ ]",
            "[ ____  ____ ] [ I2 ] = [ ____ ]",
        ], st),
        Spacer(1, 5),
        Paragraph("Core page mark: ____ / 12 &nbsp;&nbsp;&nbsp; Matrix evidence: ____ / 4", st["question"]),
        PageBreak(),

        header(st),
        Spacer(1, 5),
        Paragraph("F. Python and NumPy (12 marks)", st["section"]),
        Paragraph("1. Complete the Ohm's-law program (4 marks)", st["question"]),
        Paragraph("Use the variable names already provided. Fill only the blanks.", st["body"]),
        code_box([
            "voltage_V = 12",
            "resistance_ohm = 2000",
            "current_A = __________ / __________",
            "power_W = __________ * __________",
            "print(current_A)",
            "print(power_W)",
        ], st),
        Spacer(1, 4),
        Paragraph("Write the two printed numbers: __________________________________________", st["body"]),
        Spacer(1, 7),
        Paragraph("2. Complete the NumPy array code (4 marks)", st["question"]),
        code_box([
            "import numpy as np",
            "voltages_V = np.__________([2, 4, 6, 8])",
            "resistance_ohm = 2000",
            "currents_mA = voltages_V / __________ * 1000",
            "print(currents_mA)",
        ], st),
        Spacer(1, 4),
        Paragraph("Write the printed array: ______________________________________________", st["body"]),
        Spacer(1, 7),
        Paragraph("3. Repair the type error (4 marks)", st["question"]),
        Paragraph("Circle the line that causes the error. Rewrite only that line, then write the output.", st["body"]),
        code_box([
            "voltage_V = 12",
            "resistance_ohm = \"2000\"",
            "current_A = voltage_V / resistance_ohm",
            "print(current_A)",
        ], st),
        Spacer(1, 5),
        Paragraph("Corrected line: ______________________________________________________", st["body"]),
        Paragraph("Printed output: ______________________________________________________", st["body"]),
        Spacer(1, 8),
        box(
            "<b>MARK RECORD:</b> Circuits ___/32 &nbsp;&nbsp; Python ___/12 &nbsp;&nbsp; Core ___/44 &nbsp;&nbsp; Matrix ___/4",
            st,
        ),
    ]

    doc = SimpleDocTemplate(
        str(STUDENT_PDF),
        pagesize=letter,
        rightMargin=0.72 * inch,
        leftMargin=0.72 * inch,
        topMargin=0.42 * inch,
        bottomMargin=0.82 * inch,
        title="Life Checkpoint: Circuits + Python",
        author="Andrew Andrade",
    )
    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)


def build_key(st):
    story = [
        header(st, teacher=True),
        Spacer(1, 6),
        box(
            "<b>MARKING RULE:</b> Award marks for correct evidence in each box even when an earlier answer is wrong. "
            "Accept equivalent current directions and signed equations when the student's work is internally consistent.",
            st,
        ),
        Spacer(1, 6),
        Paragraph("A. Ohm's law and power (8 marks)", st["section"]),
        code_box([
            "2.0 kΩ = 2000 Ω",
            "I = V / R = 12 / 2000 = 0.006 A = 6 mA",
            "P = V x I = 12 x 0.006 = 0.072 W = 72 mW",
            "Twice the power is 0.144 W, so choose 1/4 W.",
        ], st),
        Spacer(1, 4),
        mark_note("1 conversion, 1 formula, 2 current, 1 power formula, 2 power, 1 rating.", st),
        Spacer(1, 7),
        Paragraph("B. Draw a simple schematic (4 marks)", st["section"]),
        Image(str(SERIES_SCHEMATIC), width=5.65 * inch, height=2.30 * inch),
        mark_note("1 complete loop, 1 correct symbols, 1 values/polarity, 1 current arrow. Equivalent clean layouts earn full marks.", st),
        Spacer(1, 8),
        box("<b>PAGE 1 TOTAL:</b> 12 marks", st),
        PageBreak(),

        header(st, teacher=True),
        Spacer(1, 5),
        Paragraph("C. Read and redraw the two-loop circuit (8 marks)", st["section"]),
        Image(str(FULL_SCHEMATIC), width=6.30 * inch, height=2.75 * inch),
        Table(
            [[
                box(Image(str(LOOP1_SCHEMATIC), width=2.70 * inch, height=1.90 * inch), st, width=3.05 * inch, padding=4),
                box(Image(str(LOOP2_SCHEMATIC), width=2.70 * inch, height=1.90 * inch), st, width=3.05 * inch, padding=4),
            ], [
                Paragraph("<b>Loop 1:</b> VS1, R1, R3 (3)", st["small"]),
                Paragraph("<b>Loop 2:</b> R3, R2, VS2 (3)", st["small"]),
            ]],
            colWidths=[3.17 * inch, 3.17 * inch],
            style=TableStyle([
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]),
        ),
        Spacer(1, 6),
        Paragraph("KCL at the centre node (2 marks)", st["question"]),
        code_box(["I1 = I2 + I3", "I3 = I1 - I2"], st),
        Spacer(1, 4),
        mark_note("Continue marking the equations even if one isolated-loop drawing is incomplete.", st),
        Spacer(1, 8),
        box("<b>PAGE 2 TOTAL:</b> 8 marks", st),
        PageBreak(),

        header(st, teacher=True),
        Spacer(1, 5),
        Paragraph("D. KVL, standard form, and solution (12 marks)", st["section"]),
        Paragraph("1. Loop 1 (4 marks)", st["question"]),
        code_box([
            "+12 - 5I1 - 2I3 = 0",
            "+12 - 5I1 - 2(I1 - I2) = 0",
            "+12 - 7I1 + 2I2 = 0",
            "7I1 - 2I2 = 12",
        ], st),
        Spacer(1, 4),
        Paragraph("2. Loop 2 (4 marks)", st["question"]),
        code_box([
            "+5 - 7I2 + 2I3 = 0",
            "+5 - 7I2 + 2(I1 - I2) = 0",
            "+5 + 2I1 - 9I2 = 0",
            "-2I1 + 9I2 = 5",
        ], st),
        Spacer(1, 4),
        Paragraph("3. Solve and check (4 marks)", st["question"]),
        code_box([
            "I1 = 2 mA",
            "I2 = 1 mA",
            "I3 = 1 mA",
            "KCL: 2 mA = 1 mA + 1 mA",
        ], st),
        Spacer(1, 5),
        Paragraph("E. Matrix bridge (4 separate marks)", st["section"]),
        matrix_table(answers=True),
        Spacer(1, 4),
        code_box([
            "[  7  -2 ] [ I1 ]   [ 12 ]",
            "[ -2   9 ] [ I2 ] = [  5 ]",
        ], st),
        Spacer(1, 4),
        mark_note("Record matrix evidence separately if matrix form has not yet been independently assessed.", st),
        PageBreak(),

        header(st, teacher=True),
        Spacer(1, 5),
        Paragraph("F. Python and NumPy (12 marks)", st["section"]),
        Paragraph("1. Ohm's-law program (4 marks)", st["question"]),
        code_box([
            "voltage_V = 12",
            "resistance_ohm = 2000",
            "current_A = voltage_V / resistance_ohm",
            "power_W = voltage_V * current_A",
            "print(current_A)     # 0.006",
            "print(power_W)       # 0.072",
        ], st),
        Spacer(1, 4),
        mark_note("1 mark per correct variable in the two formulas; accept equivalent numeric expressions.", st),
        Spacer(1, 8),
        Paragraph("2. NumPy array (4 marks)", st["question"]),
        code_box([
            "import numpy as np",
            "voltages_V = np.array([2, 4, 6, 8])",
            "resistance_ohm = 2000",
            "currents_mA = voltages_V / resistance_ohm * 1000",
            "print(currents_mA)   # [1.0 2.0 3.0 4.0]",
        ], st),
        Spacer(1, 4),
        mark_note("1 array constructor, 1 resistance variable, 1 calculation, 1 output.", st),
        Spacer(1, 8),
        Paragraph("3. Repair the type error (4 marks)", st["question"]),
        code_box([
            "resistance_ohm = 2000",
            "current_A = voltage_V / resistance_ohm",
            "print(current_A)     # 0.006",
        ], st),
        Spacer(1, 4),
        mark_note("1 identifies quoted number, 2 corrected assignment syntax, 1 correct output.", st),
        Spacer(1, 10),
        box(
            "<b>MARK RECORD:</b> Circuits ___/32 &nbsp;&nbsp; Python ___/12 &nbsp;&nbsp; Core ___/44 &nbsp;&nbsp; Matrix ___/4",
            st,
        ),
    ]

    doc = SimpleDocTemplate(
        str(KEY_PDF),
        pagesize=letter,
        rightMargin=0.72 * inch,
        leftMargin=0.72 * inch,
        topMargin=0.42 * inch,
        bottomMargin=0.82 * inch,
        title="Life Checkpoint: Circuits + Python - Teacher Key",
        author="Andrew Andrade",
    )
    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    register_fonts()
    make_schematics()
    st = styles()
    build_student(st)
    build_key(st)
    print(STUDENT_PDF)
    print(KEY_PDF)


if __name__ == "__main__":
    main()
