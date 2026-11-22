# Electronics Diagram Standard Operating Procedure

Use this procedure for every student-facing circuit, wiring diagram, test-point
diagram, and printable electronics investigation. A diagram is not ready because
it is electrically plausible; it is ready only when a learner can trace it,
measure it, and print it without guessing.

## 1. Establish the electrical story

Arrange the main energy or signal flow from left to right:

1. **source**;
2. **protection**;
3. **control**;
4. **load**;
5. **return**.

Keep a separate control circuit physically separate from its load circuit. For a
relay, place the coil and driver in a control region and the contacts and load in
a load region. Do not imply an electrical connection between the two regions.

Show conventional current direction when it supports the task. An arrow must sit
on the conductor it describes and point from the positive source, through the
load, toward the return. Label it with a unique symbol such as `I_COIL` or
`I_LAMP`; do not use an unlabeled decorative arrow.

## 2. Draw conductors and nodes

- Use horizontal and vertical conductors. Use a diagonal only when it is part of
  a standard symbol, such as a switch contact.
- Route conductors around labels, symbols, and callouts.
- Prefer a longer route over a crossed route.
- If conductors must cross without connecting, use a clear bridge or a visible
  gap. Never rely on a barely visible intersection.
- Mark every connected branch with a filled junction dot at least twice the
  conductor width.
- Do not place a junction dot on a simple bend.
- Keep terminal spacing consistent. Do not join a conductor to the side of a
  symbol when the symbol has a defined terminal.
- Give every complete circuit an obvious return path.

## 3. Use symbols and terminal names consistently

- Use standard schematic symbols rather than pictures of components.
- Add reference designators: `F1`, `S1`, `K1`, `L1`, `H1`, `Q1`, `D1`, `R1`,
  and `C1`.
- Put a component value or rating beside the reference designator when the task
  uses it.
- Mark polarity for batteries, electrolytic capacitors, diodes, LEDs, and DC
  supplies.
- For an automotive five-pin SPDT relay, identify terminals individually:
  `85` and `86` for the coil, `30` for common, `87` for normally open, and
  `87a` for normally closed. Confirm the actual relay case diagram; terminal
  position is not guaranteed by its physical shape.
- Show a flyback diode across a DC coil with its cathode at the positive side and
  anode at the switched low side.

## 4. Place labels and leader lines exactly

- A leader line ends at the symbol, terminal, node, or conductor being named.
- Stop the leader just short of the target; do not run through it.
- Do not use one leader to identify two objects.
- Keep text horizontal.
- Keep labels outside symbols and away from conductor intersections.
- Use a short name on the diagram and a longer explanation in the caption or
  legend.
- Test-point labels use a consistent sequence such as `TP1`, `TP2`, and `TP3`.

## 5. Show measurement connections truthfully

- Draw a voltmeter in parallel between the two named test points.
- Draw an ammeter in series only when the circuit is deliberately opened for it.
- For high-current classroom demonstrations, prefer a DC clamp around one
  conductor. Do not draw the clamp around both supply and return conductors.
- Distinguish a labelled current arrow from a physical ammeter.
- Never suggest moving a meter lead to a current jack while the probes remain
  across a source.
- State the meter mode and range when the activity depends on them.
- Do not show resistance or continuity measurements on an energized circuit.

## 6. Use colour as a second cue, never the only cue

Recommended roles:

| Role | Colour cue | Required non-colour cue |
|---|---|---|
| protected positive / load current | red | solid line and `+` or current label |
| return / ground | dark grey or black | ground symbol and `0 V` label |
| logic or control signal | blue | dashed line or `GPIO` label |
| timing or sensed node | purple | node name and test-point label |
| warning or fault | amber | warning symbol, hatch, or explicit text |

Use dark colours that retain contrast on white paper. Print a grayscale copy and
confirm that line style, symbol, and text still carry the meaning.

## 7. Design for normal print size

- Student body text: at least 11 pt.
- Diagram labels: target 12–14 pt when placed at final page width; never below
  10 pt.
- Major headings: at least 18 pt.
- Conductor width: at least 1.5 pt at final size.
- Junction dots: at least 3.5 pt diameter at final size.
- Keep at least 12 mm clear margin on Letter and A4 pages.
- Avoid putting essential detail within 8 mm of an SVG viewBox edge.
- Use a viewBox that tightly contains the art plus intentional margins. Do not
  clip arrowheads, text descenders, shadows, or symbols.
- Size figures by the page, not by a browser screenshot. A diagram that works
  only when zoomed is not a printable diagram.

## 8. Write useful SVG accessibility information

Each standalone SVG must include:

- a unique `<title>` describing the circuit or comparison;
- a `<desc>` that states the source, control, load, return, switch or relay
  state, and the important measurement relationship;
- `role="img"` and `aria-labelledby` pointing to the title and description.

The surrounding lesson or worksheet must also provide concise alt text. Alt text
should explain what the learner must trace or compare, not list every pixel.

## 9. Perform electrical review

Trace with a finger or cursor:

1. every source-to-return path in each switch state;
2. every branch node used for KCL;
3. every loop used for KVL;
4. each protection device and its protected conductor;
5. each component polarity;
6. each relay terminal and contact state;
7. each meter connection;
8. each stated current, voltage, resistance, and power value.

Calculate the answer key independently from the diagram. If the answer requires
an unstated ideal-wire, ideal-contact, fixed-resistance, or steady-state
assumption, put that assumption on the student page.

## 10. Perform visual and print review

Render, then inspect every page at 100%:

- colour on screen;
- grayscale on screen;
- colour on Letter paper or a Letter PDF page;
- grayscale on A4 paper or an A4 PDF page.

Inspect the diagram itself at its final page width. Check headings, footers,
tables, equations, page breaks, whitespace, and answer areas as well as the art.

## Final pass/fail checklist

A single **Fail** keeps the diagram out of release.

| Check | Pass | Fail |
|---|:---:|:---:|
| Source, protection, control, load, and return are identifiable | ☐ | ☐ |
| Every intended path is complete in the stated operating state | ☐ | ☐ |
| No unintended connection is created by a crossing | ☐ | ☐ |
| Junction dots occur only at connected branches | ☐ | ☐ |
| No conductor, arrow, or leader runs through text | ☐ | ☐ |
| Every leader points to exactly the named object | ☐ | ☐ |
| Symbols, terminal numbers, polarity, and reference designators are correct | ☐ | ☐ |
| Current arrows and voltage polarities match the answer key | ☐ | ☐ |
| Voltmeters are parallel and physical current meters are series or clamped correctly | ☐ | ☐ |
| Colour meanings remain clear in grayscale | ☐ | ☐ |
| Labels remain readable at normal print size | ☐ | ☐ |
| SVG title, description, viewBox, margins, and arrowheads are intact | ☐ | ☐ |
| Letter and A4 renders have no clipping or accidental blank pages | ☐ | ☐ |
| Calculations and stated assumptions agree with the released diagram | ☐ | ☐ |
