from pathlib import Path

import schemdraw
import schemdraw.elements as elm


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "site" / "assets" / "electronics" / "schematics" / "hands-on-led-rc-fade.svg"


def build() -> None:
    drawing = schemdraw.Drawing(show=False, file=str(OUTPUT))
    drawing.config(unit=3.2, fontsize=11, color="#0E1733", lw=2.0)

    drawing += elm.SourceV().up().label("VS = 5.0 V", loc="left")
    drawing += elm.Switch().right().length(2.2).label("S1", loc="top")
    drawing += elm.Resistor().right().length(3.2).label("RC = 330 Ω", loc="top")
    drawing += elm.Dot().label("Node A", loc="bottom")

    drawing.push()
    drawing += elm.Capacitor2().down().length(3.6).label("C = 1000 to 4700 µF", loc="left").label("VC", loc="right")
    drawing += elm.Ground()
    drawing.pop()

    drawing += elm.Line().right(3.4)
    drawing.push()
    drawing += elm.Resistor().down().length(2.2).label("RLED = 1.0 kΩ", loc="right")
    drawing += elm.LED().down().length(2.2).label("D1 red\nILED ↓", loc="right")
    drawing += elm.Ground()
    drawing.pop()

    drawing += elm.Line().right(3.4)
    drawing += elm.Resistor().down().length(3.6).label("RB = 10 kΩ\nIB ↓", loc="right")
    drawing += elm.Ground()

    drawing.save(str(OUTPUT), transparent=False)
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    build()
