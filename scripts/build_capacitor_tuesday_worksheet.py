from pathlib import Path
import math

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "site" / "assets" / "electronics" / "worksheets" / "capacitors-tuesday-worksheet.pdf"

NAVY = colors.HexColor("#12202F")
GREEN = colors.HexColor("#147A4D")
BLUE = colors.HexColor("#1498C7")
RED = colors.HexColor("#D43A32")
PALE_BLUE = colors.HexColor("#E6F3FA")
PALE_GREEN = colors.HexColor("#E8F5EE")
GRAY = colors.HexColor("#52606D")
LIGHT = colors.HexColor("#D7E0E8")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))


BODY = ParagraphStyle(
    "body", fontName="Arial", fontSize=10.5, leading=13, textColor=NAVY, alignment=TA_LEFT
)
CENTER = ParagraphStyle("center", parent=BODY, alignment=TA_CENTER)


def p(text: str, style: ParagraphStyle = BODY) -> Paragraph:
    return Paragraph(text, style)


def header(c: canvas.Canvas, page: int, subtitle: str) -> None:
    c.setFillColor(GREEN)
    c.setFont("Arial-Bold", 9)
    c.drawString(36, 756, "TEJ COMPUTER ENGINEERING")
    c.setFillColor(NAVY)
    c.setFont("Arial-Bold", 20)
    c.drawString(36, 728, "Capacitor Charge and Discharge")
    c.setFillColor(GRAY)
    c.setFont("Arial", 10)
    c.drawString(36, 710, subtitle)
    c.setFont("Arial-Bold", 9)
    c.drawRightString(576, 756, f"PAGE {page} OF 2")
    c.setStrokeColor(BLUE)
    c.setLineWidth(3)
    c.line(36, 699, 150, 699)


def section(c: canvas.Canvas, y: float, number: int, title: str) -> float:
    c.setFillColor(GREEN)
    c.roundRect(36, y - 19, 24, 24, 5, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Arial-Bold", 12)
    c.drawCentredString(48, y - 12, str(number))
    c.setFillColor(NAVY)
    c.setFont("Arial-Bold", 15)
    c.drawString(70, y - 13, title)
    return y - 31


def answer_line(c: canvas.Canvas, y: float, x1: float = 56, x2: float = 570) -> None:
    c.setStrokeColor(colors.HexColor("#7A8793"))
    c.setLineWidth(0.7)
    c.line(x1, y, x2, y)


def draw_axes(c: canvas.Canvas, x: float, y: float, w: float, h: float, blank: bool) -> None:
    c.setStrokeColor(LIGHT)
    c.setLineWidth(0.5)
    for index in range(6):
        xx = x + index * w / 5
        c.line(xx, y, xx, y + h)
        yy = y + index * h / 5
        c.line(x, yy, x + w, yy)

    c.setStrokeColor(NAVY)
    c.setLineWidth(1.3)
    c.line(x, y, x + w, y)
    c.line(x, y, x, y + h)
    c.setFillColor(NAVY)
    c.setFont("Arial", 8.5)
    for index, value in enumerate([0, 5, 10, 15, 20, 25]):
        xx = x + index * w / 5
        c.drawCentredString(xx, y - 13, str(value))
    for index, value in enumerate([0, 1, 2, 3, 4, 5]):
        yy = y + index * h / 5
        c.drawRightString(x - 7, yy - 3, str(value))
    c.setFont("Arial-Bold", 9)
    c.drawCentredString(x + w / 2, y - 28, "Time (s)")
    c.saveState()
    c.translate(x - 34, y + h / 2)
    c.rotate(90)
    c.drawCentredString(0, 0, "Capacitor voltage (V)")
    c.restoreState()

    if blank:
        return

    points = [index * 0.25 for index in range(101)]
    charge = [5 * (1 - math.exp(-time / 5)) for time in points]
    discharge = [5 * math.exp(-time / 5) for time in points]

    def plot(values: list[float], colour: colors.Color) -> None:
        path = c.beginPath()
        for index, (time, voltage) in enumerate(zip(points, values)):
            xx = x + time / 25 * w
            yy = y + voltage / 5 * h
            if index == 0:
                path.moveTo(xx, yy)
            else:
                path.lineTo(xx, yy)
        c.setStrokeColor(colour)
        c.setLineWidth(2.8)
        c.drawPath(path)

    plot(charge, BLUE)
    plot(discharge, RED)
    c.setFont("Arial-Bold", 9)
    c.setFillColor(BLUE)
    c.drawString(x + w - 87, y + h - 18, "CHARGING")
    c.setFillColor(RED)
    c.drawString(x + w - 100, y + 22, "DISCHARGING")


def draw_page_one(c: canvas.Canvas) -> None:
    header(c, 1, "Connect Monday's capacitor lesson to a graph that changes over time.")
    c.setFillColor(NAVY)
    c.setFont("Arial", 10)
    c.drawString(36, 681, "Name:")
    c.line(74, 679, 285, 679)
    c.drawString(318, 681, "Group:")
    c.line(360, 679, 470, 679)
    c.drawString(486, 681, "Date:")
    c.line(516, 679, 576, 679)

    y = section(c, 653, 1, "Connect to Monday")
    facts = [
        "A capacitor stores separated charge and energy.",
        "A polarized capacitor must be connected in the correct direction.",
        "The voltage rating must be greater than the circuit voltage.",
        "A resistor controls how quickly the capacitor charges or discharges.",
    ]
    c.setFillColor(PALE_GREEN)
    c.roundRect(36, 534, 540, 86, 7, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Arial", 10.5)
    for index, text in enumerate(facts, 1):
        c.drawString(52, 602 - (index - 1) * 19, f"{index}. {text}")

    y = section(c, 513, 2, "Read the two curves")
    draw_axes(c, 82, 268, 460, 200, blank=False)
    c.setFillColor(GRAY)
    c.setFont("Arial", 9)
    c.drawCentredString(312, 230, "Grob-style charging and discharging curves for a 5 V circuit")

    y = section(c, 211, 3, "Explain what the graph shows")
    c.setFillColor(NAVY)
    c.setFont("Arial", 10.5)
    questions = [
        "1. Charging starts near ______ V and moves toward ______ V.",
        "2. Discharging starts near ______ V and moves toward ______ V.",
        "3. The voltage changes fastest at the  beginning  /  end. Circle one.",
        "4. Why does the resistor belong in the charging and discharging path?",
    ]
    for index, text in enumerate(questions):
        yy = y - index * 31
        c.drawString(42, yy, text)
        if index == 3:
            answer_line(c, yy - 18, 42, 570)

    c.setFillColor(GRAY)
    c.setFont("Arial", 7.5)
    c.drawString(36, 25, "Adapted from the qualitative method in Grob Basic Electronics Experiments, Experiment 22-1: RC Time Constant.")


def draw_page_two(c: canvas.Canvas) -> None:
    header(c, 2, "Plot the data while small groups rotate through the component-sorting table.")
    y = section(c, 672, 4, "Plot the provided data")
    data = [
        [p("<b>Time</b>", CENTER), p("<b>Charging</b>", CENTER), p("<b>Discharging</b>", CENTER)],
        [p("0 s", CENTER), p("0.0 V", CENTER), p("5.0 V", CENTER)],
        [p("5 s", CENTER), p("3.2 V", CENTER), p("1.8 V", CENTER)],
        [p("10 s", CENTER), p("4.3 V", CENTER), p("0.7 V", CENTER)],
        [p("15 s", CENTER), p("4.8 V", CENTER), p("0.2 V", CENTER)],
        [p("20 s", CENTER), p("4.9 V", CENTER), p("0.1 V", CENTER)],
        [p("25 s", CENTER), p("5.0 V", CENTER), p("0.0 V", CENTER)],
    ]
    table = Table(data, colWidths=[110, 185, 195], rowHeights=[24] + [22] * 6)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PALE_BLUE),
        ("GRID", (0, 0), (-1, -1), 0.7, LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
    ]))
    table.wrapOn(c, 490, 170)
    table.drawOn(c, 61, 483)

    c.setFillColor(NAVY)
    c.setFont("Arial", 9.5)
    c.drawString(61, 468, "Use blue for charging and red for discharging. Connect the points with smooth curves.")
    draw_axes(c, 82, 250, 460, 190, blank=True)

    y = section(c, 219, 5, "Use the graph, not an equation")
    c.setFillColor(NAVY)
    c.setFont("Arial", 10.2)
    c.drawString(42, y, "1. At 5 seconds, which curve has the larger voltage?")
    answer_line(c, y - 17, 42, 570)
    c.drawString(42, y - 39, "2. For the same capacitor, Q = CV. As voltage rises, stored charge:")
    c.drawString(66, y - 57, "increases  /  decreases  /  stays the same. Circle one.")

    c.setFillColor(PALE_GREEN)
    c.roundRect(36, 47, 540, 71, 7, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.setFont("Arial-Bold", 10.5)
    c.drawString(50, 100, "When your group is called to the sorting table:")
    c.setFillColor(NAVY)
    c.setFont("Arial", 9.5)
    c.drawString(50, 82, "1. Decode and meter-check two resistors.  2. Read two capacitor values and ratings.")
    c.drawString(50, 66, "3. Identify polarized parts.  4. Put uncertain parts in CHECK WITH TEACHER.")

    c.setFillColor(GRAY)
    c.setFont("Arial", 7.5)
    c.drawString(36, 25, "No powered capacitor circuit is required for this activity. Use resistance mode only on disconnected resistors.")


def build() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=letter)
    c.setTitle("Capacitor Charge and Discharge")
    c.setAuthor("Andrew Andrade - Port Credit Secondary School")
    draw_page_one(c)
    c.showPage()
    draw_page_two(c)
    c.showPage()
    c.save()
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
