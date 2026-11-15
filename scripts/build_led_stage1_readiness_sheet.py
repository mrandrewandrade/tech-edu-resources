from pathlib import Path
from shutil import copyfile

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "led-stage1-readiness-sheet.pdf"
SITE_COPY = ROOT / "site" / "assets" / "electronics" / "worksheets" / "led-stage1-readiness-sheet.pdf"
SCHEMATIC = ROOT / "site" / "assets" / "electronics" / "schematics" / "stage1-led-pushbutton.png"

NAVY = HexColor("#162447")
BLUE = HexColor("#1769AA")
PALE = HexColor("#EAF3FA")
GREEN = HexColor("#147D55")
RED = HexColor("#B3261E")
INK = HexColor("#111827")
GREY = HexColor("#5F6B7A")
LINE = HexColor("#B7C4D3")


def text(c, x, y, value, size=11, bold=False, colour=INK):
    c.setFillColor(colour)
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    c.drawString(x, y, value)


def wrapped(c, x, y, value, width, size=10.5, leading=14, colour=INK, bold=False):
    words = value.split()
    line = ""
    rows = []
    font = "Helvetica-Bold" if bold else "Helvetica"
    for word in words:
        trial = f"{line} {word}".strip()
        if stringWidth(trial, font, size) <= width:
            line = trial
        else:
            rows.append(line)
            line = word
    if line:
        rows.append(line)
    c.setFillColor(colour)
    c.setFont(font, size)
    for row in rows:
        c.drawString(x, y, row)
        y -= leading
    return y


def line(c, x1, y, x2, colour=LINE, width=0.8):
    c.setStrokeColor(colour)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)


def checkbox(c, x, y, size=10):
    c.setStrokeColor(NAVY)
    c.setLineWidth(1)
    c.rect(x, y - 2, size, size, fill=0)


def header(c, page, title_value, subtitle):
    c.setFillColor(NAVY)
    c.rect(0, 720, 612, 72, fill=1, stroke=0)
    text(c, 36, 759, title_value, 20, True, white)
    text(c, 36, 738, subtitle, 10.5, False, white)
    text(c, 548, 738, f"{page}/2", 10, True, white)


def footer(c, note):
    line(c, 36, 31, 576)
    text(c, 36, 18, note, 8.5, False, GREY)


def draw_page_one(c):
    header(c, 1, "Stage 1: LED, Resistor, and Pushbutton", "Plan on paper, verify in Tinkercad, then earn READY TO BUILD.")
    text(c, 36, 700, "Name:", 10, True)
    line(c, 76, 698, 285)
    text(c, 315, 700, "Student number:", 10, True)
    line(c, 404, 698, 576)

    c.setFillColor(PALE)
    c.roundRect(36, 646, 540, 38, 7, fill=1, stroke=0)
    text(c, 49, 668, "Thursday: plan", 9.5, True, NAVY)
    text(c, 147, 668, "Friday: Tinkercad", 9.5, True, NAVY)
    text(c, 264, 668, "Sunday 7 PM: due", 9.5, True, NAVY)
    text(c, 378, 668, "Monday: correct", 9.5, True, NAVY)
    text(c, 486, 668, "Then: hardware", 9.5, True, NAVY)
    text(c, 49, 652, "Physical components are issued only after the matching simulation earns 100%.", 9.5, False, NAVY)

    text(c, 36, 625, "1. Read the circuit", 14, True, BLUE)
    c.setStrokeColor(LINE)
    c.roundRect(36, 448, 540, 164, 8, fill=0, stroke=1)
    image = ImageReader(str(SCHEMATIC))
    c.drawImage(image, 54, 462, width=504, height=142, preserveAspectRatio=True, anchor="c", mask="auto")

    text(c, 36, 425, "Required values", 12, True, BLUE)
    values = [
        ("Source", "5.0 V DC"),
        ("Switch", "Normally open pushbutton"),
        ("Resistor", "1.0 kOhm, 1/4 W"),
        ("LED", "Red; anode toward the resistor"),
    ]
    x_positions = [36, 305]
    for index, (label, value) in enumerate(values):
        column = index % 2
        row = index // 2
        x = x_positions[column]
        y = 405 - row * 31
        text(c, x, y, f"{label}:", 10, True)
        text(c, x + 58, y, value, 10)

    text(c, 36, 342, "2. Calculate before simulating", 14, True, BLUE)
    prompts = [
        "A red LED is modelled as 2.0 V. Calculate the resistor voltage:  VR = VS - VLED",
        "Calculate current:  I = VR / R",
        "Calculate resistor power:  PR = I^2 R",
        "Write the KVL check using your answers:  VS = VR + VLED",
    ]
    y = 319
    for number, prompt in enumerate(prompts, 1):
        text(c, 43, y, f"{number}.", 10.5, True)
        y = wrapped(c, 62, y, prompt, 498, 10.2, 13)
        line(c, 62, y - 3, 560, HexColor("#718096"), 0.7)
        y -= 22

    text(c, 36, 173, "3. Draw your Tinkercad wiring plan", 14, True, BLUE)
    text(c, 36, 156, "Use red for +5 V, black for ground, and another colour after the pushbutton.", 9.5, False, GREY)
    c.setStrokeColor(LINE)
    c.roundRect(36, 49, 540, 96, 6, fill=0, stroke=1)
    c.setStrokeColor(HexColor("#D7E0EA"))
    c.setLineWidth(0.35)
    for x in range(54, 576, 18):
        c.line(x, 49, x, 145)
    for y_grid in range(61, 145, 12):
        c.line(36, y_grid, 576, y_grid)
    footer(c, "Grob support: Chapter 9 for KVL and Chapter 27 for LED direction, forward voltage, and current limiting.")


def draw_page_two(c):
    header(c, 2, "Tinkercad Readiness Gate", "A score of 100% unlocks the matching physical circuit.")
    text(c, 36, 697, "Circuit name:", 10, True)
    line(c, 103, 695, 330)
    text(c, 350, 697, "Teacher check date:", 10, True)
    line(c, 452, 695, 576)

    text(c, 36, 666, "Submit", 14, True, BLUE)
    steps = [
        "Direct Tinkercad share URL",
        "One readable screenshot with the simulation running and the button pressed",
        "This completed calculation and readiness sheet",
    ]
    y = 644
    for number, value in enumerate(steps, 1):
        text(c, 43, y, f"{number}.", 10.5, True)
        wrapped(c, 62, y, value, 490, 10.5, 14)
        y -= 20

    text(c, 36, 581, "100% readiness checklist", 14, True, BLUE)
    rows = [
        ("Correct filename and working share URL", "5"),
        ("One complete series path with a normally open pushbutton", "20"),
        ("5.0 V source, 1.0 kOhm resistor, and red LED", "15"),
        ("Correct LED polarity", "10"),
        ("Clear red, black, and switched-wire convention", "10"),
        ("LED off when released and on when pressed", "10"),
        ("KVL calculation with units", "10"),
        ("Current and resistor-power calculations with units", "10"),
        ("Simulated voltage and current evidence", "10"),
    ]
    table_x = 36
    table_top = 559
    row_h = 23
    c.setFillColor(NAVY)
    c.rect(table_x, table_top - row_h, 540, row_h, fill=1, stroke=0)
    text(c, table_x + 12, table_top - 16, "Check", 9.5, True, white)
    text(c, table_x + 50, table_top - 16, "Evidence", 9.5, True, white)
    text(c, table_x + 500, table_top - 16, "Marks", 9.5, True, white)
    y = table_top - row_h
    for index, (label, mark) in enumerate(rows):
        y -= row_h
        if index % 2 == 0:
            c.setFillColor(HexColor("#F5F8FB"))
            c.rect(table_x, y, 540, row_h, fill=1, stroke=0)
        checkbox(c, table_x + 14, y + 7, 9)
        text(c, table_x + 50, y + 7, label, 9.2)
        text(c, table_x + 516, y + 7, mark, 9.5, True)
        c.setStrokeColor(LINE)
        c.rect(table_x, y, 540, row_h, fill=0, stroke=1)
    total_y = y - row_h
    c.setFillColor(PALE)
    c.rect(table_x, total_y, 540, row_h, fill=1, stroke=1)
    text(c, table_x + 50, total_y + 7, "TOTAL - must equal 100 before hardware", 9.8, True, NAVY)
    text(c, table_x + 510, total_y + 7, "/100", 9.8, True, NAVY)

    evidence_y = total_y - 31
    text(c, 36, evidence_y, "Simulation evidence", 13, True, BLUE)
    evidence_y -= 22
    fields = [
        "Tinkercad URL:",
        "VR =                         V        VLED =                         V",
        "I =                         mA      Screenshot filename:",
    ]
    for field in fields:
        text(c, 43, evidence_y, field, 9.8, True if field.endswith(":") else False)
        line(c, 43, evidence_y - 5, 566, HexColor("#718096"), 0.7)
        evidence_y -= 27

    c.setFillColor(HexColor("#FFF4E5"))
    c.roundRect(36, 91, 540, 62, 7, fill=1, stroke=0)
    text(c, 48, 133, "Correction day", 11, True, RED)
    wrapped(c, 48, 117, "If the score is below 100, stay in Tinkercad during the next lab class. Fix one checklist item at a time, retest, and request another check.", 512, 9.5, 12, INK)

    c.setStrokeColor(GREEN)
    c.setLineWidth(1.5)
    c.roundRect(36, 43, 540, 36, 7, fill=0, stroke=1)
    checkbox(c, 49, 55, 12)
    text(c, 69, 57, "READY TO BUILD", 12, True, GREEN)
    text(c, 240, 57, "Teacher initials:", 10, True)
    line(c, 324, 55, 408, GREEN, 0.8)
    text(c, 431, 57, "Date:", 10, True)
    line(c, 462, 55, 560, GREEN, 0.8)
    footer(c, "Physical build: teacher-set 5.0 V supply, current limit 20 mA or less, power-off wiring check required.")


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    SITE_COPY.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=letter)
    c.setTitle("Stage 1 LED Tinkercad Readiness Sheet")
    draw_page_one(c)
    c.showPage()
    draw_page_two(c)
    c.save()
    copyfile(OUTPUT, SITE_COPY)
    print(f"Generated {OUTPUT}")
    print(f"Published copy {SITE_COPY}")


if __name__ == "__main__":
    build()
