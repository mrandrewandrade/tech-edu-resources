from pathlib import Path

import schemdraw
import schemdraw.elements as elm


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "site" / "assets" / "electronics" / "schematics" / "stage1-led-pushbutton.svg"


def build() -> None:
    drawing = schemdraw.Drawing(show=False, file=str(OUTPUT))
    drawing.config(unit=3.2, fontsize=12, color="#0E1733", lw=2.0)

    drawing += elm.SourceV().up().label("VS = 5.0 V", loc="right")
    drawing += elm.Switch().right().length(2.5).label("Pushbutton S1", loc="top")
    drawing += elm.Resistor().right().length(3.2).label("R1 = 1.0 kΩ", loc="top")
    drawing += elm.LED().down().length(3.0).label("D1 red LED", loc="right")
    drawing += elm.Line().left().tox(0)
    drawing += elm.Ground()

    drawing.save(str(OUTPUT), transparent=False)
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    build()
