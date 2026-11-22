# Electrical workbook QA report

Date: 2026-11-22
Branch: `codex/electrical-diagrams-workbook`

## Rendered page count

| Printable document | Letter | A4 |
|---|---:|---:|
| Automotive relay investigation | 8 | 8 |
| Automotive relay answer key | 5 | 5 |
| Capacitor-sound investigation | 6 | 6 |
| Capacitor-sound answer key | 3 | 3 |
| Fault cards | 4 | 4 |
| Fault-card teacher key | 2 | 2 |
| **Total** | **28** | **28** |

Each document was rendered in Letter colour, Letter grayscale, A4 colour, and
A4 grayscale. That produced 112 inspected page instances. The committed PDFs in
`rendered/` are the Letter colour masters.

## Visual inspection

Final result: **PASS**

- [x] All page edges and SVG viewBoxes have clear margins; no text, symbols, or
      ground marks are clipped.
- [x] No blank trailing pages remain.
- [x] Automotive lamp circles are aligned and separated.
- [x] Horn loads use bounded two-terminal load symbols; sound-effect curves do
      not cross electrical conductors.
- [x] Current arrows sit on the intended branch and point in conventional-current
      direction.
- [x] Meter placement shows the voltmeter in parallel and the DC clamp around
      one conductor. The prohibited current-mode connection is visibly crossed
      out.
- [x] Junctions use filled dots; test points use outlined purple circles; a
      crossing without a dot is not used as a junction.
- [x] Terminals 30, 85, 86, 87, and 87a remain legible at normal print size.
- [x] The polarized capacitor has its positive plate marked; the LED symbol has
      light arrows and a labelled polarity-sensitive branch.
- [x] Colour meaning is repeated through line style, labels, and arrow patterns,
      so grayscale copies remain usable.
- [x] Student text is 11.5 pt, captions are 10.5 pt, and the source note is 9 pt.
- [x] Letter and A4 contact sheets show no table, answer-box, or card clipping.
- [x] The standalone BeagleBone diagram was inspected in colour and grayscale;
      the control, coil-current, load-current, mechanical-link, and isolation
      notes remain distinguishable.

Corrections made during QA included separating overlapping lamp symbols,
replacing ambiguous horn artwork with two-terminal load boxes, adding LED light
arrows, moving capacitor polarity closer to the positive plate, increasing
bottom margin around ground symbols, and deleting stale raster pages before
contact-sheet regeneration.

## Electrical and answer-key checks

`calculation_checks.py` passes independently of the prose key.

| Check | Result |
|---|---:|
| 21 W lamp at 12 V | 1.750 A |
| State-B horn current | 4.750 A |
| State-B horn power | 57.0 W |
| State-B total battery current, including coil | 6.65 A |
| State-B total battery power | 79.8 W |
| Poor-ground current | 1.527 A |
| Poor-ground lamp voltage | 10.47 V |
| Poor-ground lamp power | 16.0 W |
| 1000 µF at 5 V | 0.0125 J |
| Ideal 12 mA buzzer estimate, 5 V to 3 V | 0.167 s |
| Horn capacitance estimate | 0.3125 F = 312,500 µF |
| Estimated energy at 12 V | 22.5 J |

The student prompts and teacher keys agree on both relay states, KVL signs, the
State-B KCL node, meter placement, the poor-ground diagnosis, and the capacitor
model limitations.

## Ratings that remain assumptions

- 80.0 ohm classroom relay-coil model.
- Two 21.0 W lamps at a nominal 12.0 V.
- State-B measured current of 6.50 A.
- Horn model of 5.0 A for the capacitor estimate.
- 1.00 ohm poor-ground fault.
- 330 ohm charging resistor, 1.0 kohm LED resistor, and 1000 µF capacitor.
- The actual fuse sizes, conductor size, relay contact rating, suppression type,
  coil resistance, MOSFET/transistor, diode, lamp, horn, and supply ratings.

Actual classroom parts must be checked against their markings and data sheets.
See `SOURCES.md` for the published references and the adaptation record.
