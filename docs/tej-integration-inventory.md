# TEJ integration inventory

Last updated: 2026-11-22

This file tracks the consolidated TEJ website work before the later website-wide
cleanup. The integration branch is `codex/tej-integrated-site`. Source branches
remain intact so individual packages can still be inspected or recovered.

## Integrated packages

| Package | Source branch | Source tip at integration | Current purpose |
|---|---|---:|---|
| Circuit labs and electrical workbook | `codex/circuit-labs-focus` | `1e3a198` | Active circuit-lab planning, printable investigations, relay trainer, capacitor/sound work, and fault cards |
| Sensor and alarm projects | `codex/sensor-alarm-projects` | `649fcb2` | Night-light, alarm, protected input/output, sensor, and student-choice pathways |
| Semester course package | `codex/semester-course-package` | `8ee0dc1` | Assessment, inventory, lab-management, inclusion, and capstone planning resources |
| BeagleBone platform | `codex/beaglebone-platform` | `bec09f1` | Later Linux/Python/GPIO progression, simulations, tests, and documentation |
| Student portfolio system | `codex/semester-portfolio` | `01dadfe` | Later culminating portfolio assignment and configurable Quarto starter |
| Learning-world map | `codex/learning-world-map` | `adcebf3` | Separate game-like navigation area for later site-overhaul work |

The previously separate output/control work is already contained in
`codex/circuit-labs-focus` and was not merged a second time.

## Current instructional priority

1. Inventory the actual classroom components.
2. Select one or two low-voltage circuits that can be made reliable.
3. Prototype before mounting anything to a wooden trainer board.
4. Add labelled connectors, test points, fault switches, and a matching
   schematic only after the circuit works consistently.
5. Introduce Raspberry Pi or BeagleBone control after the analog circuit and
   output driver are understood.

## Hardware facts still requiring confirmation

- 555 timer quantity and exact part markings
- active buzzer versus passive piezo quantity, voltage, and current
- capacitor values, voltage ratings, polarity, and condition
- resistor and potentiometer values
- transistor and MOSFET part numbers and verified pinouts
- diode part numbers and orientation
- automotive relay coil voltage, terminal map, and built-in suppression
- lamp and horn voltage/current ratings
- available 5 V and current-limited 12 V supplies
- Raspberry Pi and BeagleBone models
- multimeter models and whether the clamp measures DC current
- mini-oscilloscope model and safe input limits

## Provisional lab decision

- If a 555 and passive piezo are available, pilot an adjustable RC oscillator
  in which resistance and capacitance change the audible frequency.
- If the buzzers are active, use RC timing to change beep duration or cadence,
  not pitch.
- If no suitable timer is available, use the existing low-voltage capacitor
  charge/discharge investigation with an LED or verified active buzzer.
- Use a fused 12 V lamp as the first relay load. The horn remains an optional,
  brief, teacher-controlled demonstration.

## Deferred cleanup

The packages intentionally retain some overlapping diagrams and explanations.
After the mounted labs are chosen from the real inventory, the website overhaul
can remove duplication, establish canonical pages, simplify navigation, and
archive unused alternatives.
