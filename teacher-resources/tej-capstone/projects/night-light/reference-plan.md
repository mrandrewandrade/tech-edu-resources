# Automatic Night Light — Teacher Reference Plan

This plan supports three evidence-equivalent routes without assuming a particular classroom sensor module.

## Recommended sequence

1. Demonstrate a photoresistor's resistance change with power removed.
2. Build and measure a protected divider without a controller.
3. Calculate LED current limiting and test the output stage separately.
4. Complete the standalone transistor light or move to a verified BeagleBone input.
5. Add threshold hysteresis before logging.
6. Finish with repeated bright/dark trials and portfolio evidence.

## Route decision

| Available input | Recommended use | Main verification |
|---|---|---|
| Bare photoresistor | Standalone divider/transistor or comparator | Actual bright/dark resistance range |
| Comparator module | Digital GPIO input | Output pull-up voltage and output polarity |
| VEML7700 or similar 3.3 V-compatible I²C module | Proficient BeagleBone route | Complete module schematic, pull-ups, detected address |
| Analogue module that may output 5 V | Do not connect directly | Redesign interface or choose another route |
| Direct divider into BeagleBone ADC | Advanced, teacher-approved only | Worst-case voltage with tolerance margin below 1.8 V |

The BeagleBone Black official documentation identifies 3.3 V I/O and 1.8 V maximum analogue inputs. Treat 1.8 V as a destructive boundary, not a design target. Require margin and a multimeter check before connection.

## Inventory confirmation

- [ ] Exact BeagleBone models and Linux images.
- [ ] Light sensor manufacturer and part/module number.
- [ ] Module regulator and I²C pull-up rail.
- [ ] Photoresistor bright/dark resistance range from classroom samples.
- [ ] NPN/MOSFET/comparator part numbers and pinouts.
- [ ] LED colours and conservative forward-voltage assumptions.
- [ ] Breadboard rail continuity.
- [ ] Current-limited 3.3 V/5 V sources.
- [ ] Number and condition of multimeters.

## Reference-build gates

Build one complete reference circuit for each route actually offered.

1. Record source voltage with no load.
2. Measure sensor output in the brightest and darkest planned conditions.
3. Verify every controller input with the controller disconnected.
4. Measure LED-resistor voltage and calculate current.
5. Hold the input around threshold; confirm hysteresis prevents chatter.
6. Disconnect the sensor; record the actual software response.
7. Power-cycle the system and verify the output defaults off.

Do not publish these readings as expected student results. Classroom parts and lighting will differ.

## Suggested checkpoints

| Checkpoint | Student evidence |
|---|---|
| 1. Parts | Exact part numbers and official documents |
| 2. Prediction | Divider/LED calculations and expected sensor direction |
| 3. Sensor | Bright/dark resistance or digital readings |
| 4. Interface | Measured worst-case voltage before board connection |
| 5. Output | Independent LED/driver test |
| 6. Integration | Three repeatable trials and threshold test |
| 7. Portfolio | Fault/revision and conclusion against criteria |

## Frequent misconceptions

- “3.3 V board” does not mean the analogue input accepts 3.3 V.
- A breakout board may have different electrical behaviour than its sensor chip.
- A potentiometer does not automatically limit worst-case voltage.
- A transistor is not a comparator; a simple transistor threshold may be gradual.
- Reversing the photoresistor position reverses the sensor-voltage response.
- A logged value is not automatically calibrated illuminance.

## Available source-backed diagrams

1. Standalone LDR-divider/NPN/LED topology with labelled test points.
2. Comparator route with LM393 open-collector output pulled to 3.3 V.
3. BeagleBone ADC divider boundary diagram showing 1.8 V maximum and pre-connection meter check.
4. Digital I²C sensor route with a warning against hidden 5 V pull-ups.

Editable CircuitTikZ sources plus print PDFs and website SVGs are in `site/assets/tej-capstone/projects/sensor-alarm/diagrams/`.

## Authoritative references

- BeagleBoard.org, [BeagleBone Black overview](https://docs.beagleboard.org/boards/beaglebone/black/ch04.html).
- Vishay, [VEML7700 datasheet](https://www.vishay.com/docs/84286/veml7700.pdf).
- Texas Instruments, [LM393 product information and datasheet](https://www.ti.com/product/LM393).

Verify the current datasheet revision for every issued component.
