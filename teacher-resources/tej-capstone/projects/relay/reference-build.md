# Automotive relay trainer: teacher reference build

This file is a preparation and verification plan, not a claim that the classroom hardware has been tested. Record the actual results before releasing parts.

## Intended reference system

- protected, current-limited 12 V DC source;
- branch fuse selected for the reference wiring and lamp load;
- plug-in automotive relay in a matching socket;
- manual control switch for the first build;
- 12 V lamp as the normal load;
- optional transistor/MOSFET driver after the manual circuit works;
- automotive horn only at a separate teacher-controlled demonstration station.

## Datasheet gate

Complete one row for every relay type in stock.

| Check | Recorded evidence |
|---|---|
| Manufacturer and exact part number |  |
| Manufacturer datasheet URL/file |  |
| Nominal coil voltage |  |
| Coil resistance or current and tolerance |  |
| Operating/release voltage when specified |  |
| Contact form: NO/form A or changeover/form C |  |
| Terminal assignment shown on case |  |
| Contact rating for 12 V DC load category |  |
| Internal diode, resistor, or no suppression |  |
| Required 85/86 polarity |  |
| Socket manufacturer/part and wire map |  |

Do not generalize one relay's suppression or pin orientation to another. If the case diagram and datasheet disagree, quarantine the part.

## Reference-build sequence

1. With all sources disconnected, map the socket conductors to terminal numbers.
2. Measure and record released-state continuity: 30–87, 30–87a, and coil terminals.
3. Set the 12 V source current limit conservatively for the coil-only test.
4. Energize the coil manually. Confirm mechanical operation and energized continuity.
5. Disconnect power. Add the fused lamp branch through 30 and 87.
6. Increase the source limit only to the documented amount needed for the verified lamp and coil.
7. Measure source, coil, 30, 87, lamp, and return voltages in both states.
8. Run the circuit for the planned class interval. Check socket, conductors, fuse holder, relay, and lamp connections for unexpected heating.
9. Add the driver stage only after the manual build and part calculations are documented.
10. Repeat safe-state, voltage-drop, and thermal checks with the driver.

## Driver-stage decisions

Record rather than assume:

- measured/documented coil current including tolerance;
- transistor or MOSFET voltage, current, safe-operating-area, and power margin;
- exact pinout;
- GPIO high/low compatibility;
- base/gate resistor calculation;
- whether a gate/source or base/emitter bias resistor is required;
- flyback diode current/voltage rating and orientation;
- whether internal relay suppression already exists;
- whether grounds are shared or galvanically isolated;
- behaviour during boot, program exit, exception, and BeagleBone power loss.

The BeagleBone output must never carry coil current. Load current must never flow in the breadboard or GPIO ground path.

## Current measurement plan

Prefer voltage evidence and calculation for the student sequence. If a clamp is used, verify that it measures DC and has adequate resolution for the chosen conductor/current. Enclose only one conductor. Direct series measurement requires a fused meter, correct jack/range, and a teacher-controlled procedure. Do not place a current-configured meter across the source.

## Horn demonstration gate

- Verify horn rated voltage and measure/document current with the intended supply.
- Select fuse, holder, conductors, switch/relay contacts, and connectors for that current and surge.
- Mount the horn securely and keep it away from ears.
- Establish a maximum pulse time and a quiet alternative.
- Use a separate physical enable switch or removable fuse.
- Do not let student software create an unlimited continuous horn command.

## Release record

| Item | Result | Date/initials |
|---|---|---|
| Coil-only test |  |  |
| Released/energized continuity |  |  |
| Lamp voltage/current estimate |  |  |
| Fuse/wire/socket thermal check |  |  |
| Driver default-off behaviour |  |  |
| Flyback protection verified |  |  |
| Program stop/exception test |  |  |
| Horn station test, if used |  |  |

## Diagram requests for the integration stream

1. Manual two-loop relay schematic with 30/85/86/87/87a and six voltage test points.
2. BeagleBone low-side driver schematic with transistor/MOSFET, bias resistor, coil supply, flyback diode, and separated contact circuit.
3. Released-versus-energized contact inset showing 30–87a and 30–87.

Each should use large terminal labels, avoid conductor crossings, distinguish control and load current, and remain clear in grayscale.

## Authoritative references to retain

- BeagleBoard.org, *BeagleBone Black Features and Specification*: <https://docs.beagleboard.org/boards/beaglebone/black/ch04.html>
- TE Connectivity, example Micro ISO relay data sheet: <https://www.te.com/content/dam/te-com/documents/automotive/global/ENG_DS_V23074-X0000-A001_0615.pdf>

The TE sheet is an example of the information to verify. Use the actual classroom relay's manufacturer sheet for final approval.

