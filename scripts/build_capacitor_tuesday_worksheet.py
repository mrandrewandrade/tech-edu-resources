from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "site" / "assets" / "electronics" / "worksheets" / "capacitors-tuesday-worksheet.pdf"
SCHEMATIC = ROOT / "site" / "assets" / "electronics" / "schematics" / "hands-on-rc-station.png"

NAVY = colors.HexColor("#12202F")
GREEN = colors.HexColor("#147A4D")
BLUE = colors.HexColor("#1498C7")
PALE_BLUE = colors.HexColor("#E6F3FA")
PALE_GREEN = colors.HexColor("#E8F5EE")
GRAY = colors.HexColor("#52606D")
LIGHT = colors.HexColor("#D7E0E8")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))


BODY = ParagraphStyle(
    "body",
    fontName="Arial",
    fontSize=11,
    leading=14,
    textColor=NAVY,
    alignment=TA_LEFT,
)
SMALL = ParagraphStyle(
    "small",
    parent=BODY,
    fontSize=9,
    leading=11,
)
CENTER = ParagraphStyle(
    "center",
    parent=BODY,
    alignment=TA_CENTER,
)


def p(text: str, style: ParagraphStyle = BODY) -> Paragraph:
    return Paragraph(text, style)


def header(c: canvas.Canvas, page: int, subtitle: str) -> None:
    c.setFillColor(GREEN)
    c.setFont("Arial-Bold", 9)
    c.drawString(36, 756, "TEJ COMPUTER ENGINEERING")
    c.setFillColor(NAVY)
    c.setFont("Arial-Bold", 21)
    c.drawString(36, 728, "Capacitor Charging: Predict, Measure, Compare")
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


def line(c: canvas.Canvas, x1: float, x2: float, y: float, label: str = "") -> None:
    if label:
        c.setFillColor(NAVY)
        c.setFont("Arial", 11)
        c.drawString(x1, y + 4, label)
        x1 += pdfmetrics.stringWidth(label, "Arial", 11) + 7
    c.setStrokeColor(colors.HexColor("#7A8793"))
    c.setLineWidth(0.7)
    c.line(x1, y, x2, y)


def draw_page_one(c: canvas.Canvas) -> None:
    header(c, 1, "Complete this page while waiting for the hardware station.")
    c.setFillColor(NAVY)
    c.setFont("Arial", 10)
    c.drawString(36, 681, "Name:")
    c.line(74, 679, 285, 679)
    c.drawString(318, 681, "Group:")
    c.line(360, 679, 470, 679)
    c.drawString(486, 681, "Date:")
    c.line(516, 679, 576, 679)

    y = section(c, 653, 1, "Use one available resistor-capacitor pair")
    c.setFillColor(GRAY)
    c.setFont("Arial", 10)
    c.drawString(36, y, "Your teacher will select the row that matches the available capacitor.")
    data = [
        [p("<b>Capacitor C</b>", CENTER), p("<b>Resistor R</b>", CENTER), p("<b>Expected τ = RC</b>", CENTER)],
        [p("100 µF", CENTER), p("47 kΩ", CENTER), p("4.7 s", CENTER)],
        [p("220 µF", CENTER), p("22 kΩ", CENTER), p("4.84 s", CENTER)],
        [p("470 µF", CENTER), p("10 kΩ", CENTER), p("4.7 s", CENTER)],
        [p("1000 µF", CENTER), p("4.7 kΩ", CENTER), p("4.7 s", CENTER)],
    ]
    table = Table(data, colWidths=[150, 150, 190], rowHeights=[25, 23, 23, 23, 23])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PALE_BLUE),
        ("GRID", (0, 0), (-1, -1), 0.7, LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
    ]))
    table.wrapOn(c, 490, 140)
    table.drawOn(c, 61, 496)

    y = section(c, 478, 2, "Read the circuit before building")
    image = ImageReader(str(SCHEMATIC))
    c.drawImage(image, 72, 315, width=468, height=132, preserveAspectRatio=True, anchor="c", mask="auto")
    c.setFillColor(GRAY)
    c.setFont("Arial", 9)
    c.drawCentredString(306, 304, "The jumper selects +5 V to charge or 0 V to discharge. Current always passes through R.")

    y = section(c, 282, 3, "Complete the simple calculations")
    c.setFillColor(NAVY)
    c.setFont("Arial", 11)
    c.drawString(36, y, "Use the 470 µF capacitor, 10 kΩ resistor, and 5.0 V supply for these calculations.")
    c.setFont("Arial", 12)
    c.drawString(48, y - 30, "a. Convert the resistor:    10 kΩ = 10,000 Ω")
    c.drawString(48, y - 58, "b. Convert the capacitor:  470 µF = 0.000470 F")
    c.drawString(48, y - 88, "c. Time constant:  τ = RC = (10,000 Ω)(0.000470 F) =")
    line(c, 440, 545, y - 91)
    c.drawString(550, y - 88, "s")
    c.drawString(48, y - 118, "d. At one time constant:  Vc ≈ 0.63(5.0 V) =")
    line(c, 375, 505, y - 121)
    c.drawString(512, y - 118, "V")
    c.drawString(48, y - 148, "e. Fully charged:  Q = CV = (470 µF)(5.0 V) =")
    line(c, 390, 505, y - 151)
    c.drawString(512, y - 148, "µC")

    c.setFillColor(PALE_GREEN)
    c.roundRect(36, 42, 540, 37, 6, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.setFont("Arial-Bold", 10)
    c.drawCentredString(306, 63, "Before touching the hardware: predicted Vc near 5 seconds = __________ V")
    c.setFillColor(GRAY)
    c.setFont("Arial", 7.5)
    c.drawString(36, 25, "Adapted for 5 V classroom use from Grob Basic Electronics Experiments, Experiment 22-1: RC Time Constant.")


def draw_page_two(c: canvas.Canvas) -> None:
    header(c, 2, "A small group completes the hardware station, then rotates back to the paper work.")
    y = section(c, 672, 4, "Safety and setup check")
    checks = [
        "Power supply is set to 5.0 V before connecting the breadboard.",
        "Capacitor voltage rating is 10 V or greater.",
        "Capacitor negative stripe is connected to the 0 V rail.",
        "The resistor is in series. The capacitor is never shorted directly.",
        "Multimeter is set to DC volts and connected across the capacitor.",
    ]
    c.setFont("Arial", 10.5)
    c.setFillColor(NAVY)
    for index, text in enumerate(checks, 1):
        yy = y - (index - 1) * 22
        c.rect(42, yy - 9, 10, 10, fill=0, stroke=1)
        c.drawString(61, yy - 8, f"{index}. {text}")

    y = section(c, 524, 5, "Charge, measure, and discharge")
    steps = [
        "Move the jumper to 0 V until the meter reads below 0.10 V.",
        "Move the jumper to +5 V and start the timer at the same moment.",
        "Record the capacitor voltage every five seconds.",
        "After 25 seconds, move the jumper to 0 V and watch the voltage fall.",
    ]
    c.setFont("Arial", 10.5)
    c.setFillColor(NAVY)
    for index, text in enumerate(steps, 1):
        c.drawString(42, y - (index - 1) * 20, f"{index}. {text}")

    data = [
        [p("<b>Time</b>", CENTER), p("<b>Predicted Vc</b>", CENTER), p("<b>Measured Vc</b>", CENTER)],
        [p("0 s", CENTER), p("0.00 V", CENTER), p("", CENTER)],
        [p("5 s", CENTER), p("3.27 V", CENTER), p("", CENTER)],
        [p("10 s", CENTER), p("4.40 V", CENTER), p("", CENTER)],
        [p("15 s", CENTER), p("4.79 V", CENTER), p("", CENTER)],
        [p("20 s", CENTER), p("4.93 V", CENTER), p("", CENTER)],
        [p("25 s", CENTER), p("4.98 V", CENTER), p("", CENTER)],
    ]
    table = Table(data, colWidths=[120, 180, 190], rowHeights=[25, 25, 25, 25, 25, 25, 25])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PALE_BLUE),
        ("GRID", (0, 0), (-1, -1), 0.8, LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
    ]))
    table.wrapOn(c, 490, 200)
    table.drawOn(c, 61, 249)

    y = section(c, 229, 6, "Compare the prediction with the real component")
    c.setFillColor(NAVY)
    c.setFont("Arial", 10.5)
    c.drawString(42, y, "1. At about one time constant, was the measured voltage close to 3.15 V?")
    line(c, 42, 570, y - 20)
    c.drawString(42, y - 46, "2. Did the voltage rise quickly at first and then slow down?")
    line(c, 42, 570, y - 66)
    c.drawString(42, y - 92, "3. One source of difference between the prediction and measurement:")
    line(c, 42, 570, y - 112)

    c.setFillColor(PALE_GREEN)
    c.roundRect(36, 38, 540, 40, 6, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.setFont("Arial-Bold", 10)
    c.drawCentredString(306, 61, "Roles: builder | meter operator | timer | recorder | safety checker")
    c.setFillColor(GRAY)
    c.setFont("Arial", 7.5)
    c.drawString(36, 24, "Use teacher-selected parts. Do not change components or power connections while the supply is on.")


def build() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=letter)
    c.setTitle("Capacitor Charging: Predict, Measure, Compare")
    c.setAuthor("Andrew Andrade - Port Credit Secondary School")
    draw_page_one(c)
    c.showPage()
    draw_page_two(c)
    c.showPage()
    c.save()
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
