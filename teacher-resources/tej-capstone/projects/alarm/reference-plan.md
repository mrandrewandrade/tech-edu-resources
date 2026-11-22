# Linux Alarm — Teacher Reference Plan

## Core architecture

The student system uses a protected switch input, Linux/Python state machine, resistor-limited status LED, and low-current audible output through a suitable interface. The minimum successful artifact is not an automotive security system; it is a controlled classroom model with inspectable states and evidence.

## Recommended build order

1. Test state transitions with keyboard or simulated inputs.
2. Build the switch and pull resistor; measure open/closed voltage without the board.
3. Read and print the input; keep outputs disconnected.
4. Test the LED/resistor independently.
5. Test the buzzer driver independently with the approved low-voltage supply.
6. Integrate core states and event logging.
7. Test safe startup, intentional exit, error cleanup, and sensor disconnect.
8. Add a relay-controlled lamp only after the core is complete.
9. Demonstrate the shared horn last, under direct supervision.

## Hardware confirmation

- [ ] Exact BeagleBone model, Linux image, Python version, and GPIO method.
- [ ] Available safe GPIO pins and default boot states.
- [ ] Door/pushbutton contact action and reliable terminals.
- [ ] Pull-resistor values.
- [ ] LED colour, resistor value, and current calculation.
- [ ] Buzzer type: active/passive, voltage, current, polarity.
- [ ] Driver part number, pinout, drive requirement, and power rating.
- [ ] Relay coil voltage/current and suppression.
- [ ] Contact rating, lamp rating, fuse, and external supply.
- [ ] Horn rated voltage and measured/label current requirement.

## Shared automotive-horn station

Use a relay socket, fused 12 V source, clearly labelled emergency disconnect, short pulse duration, and visual warning. Position the horn to reduce startling sound exposure. Offer a silent lamp equivalent. Students request horn operation through the controller, but the teacher retains load-power control.

Do not use a capacitor as the horn's energy source. A capacitor can time/filter the control signal; the fused supply provides load energy.

## Software review questions

1. What state is established before the first input read?
2. Can the state machine be tested without GPIO?
3. Are delays non-blocking enough to allow disarm/silence requests?
4. Does one physical press create one logical event?
5. Does each transition create exactly one log entry?
6. What happens when input is missing or implausible?
7. How are outputs switched off on normal exit and error?

## Suggested prepared faults

- open switch return/ground;
- wrong active-low interpretation;
- missing pull resistor in an unpowered prepared model;
- reversed LED;
- wrong transistor pinout shown on a paper diagram;
- contact wired to 87a instead of 87;
- open fuse on the lamp trainer;
- log directory not writable in the software simulator.

Never create a deliberate short or apply an overvoltage.

## Requested diagrams for the shared diagram workstream

1. Active-low door input with external 3.3 V pull-up.
2. LED and buzzer-driver output stages with test points.
3. BeagleBone-to-transistor-to-relay coil with flyback diode.
4. Separate fused contact-side lamp/horn circuit with 30/87 terminals.
5. State diagram for DISARMED, ARMING, ARMED, ALARM, and SILENCED.

## References

- BeagleBoard.org, [BeagleBone Black overview](https://docs.beagleboard.org/boards/beaglebone/black/ch04.html).
- BeagleBoard.org, [BeagleBone Black connector reference](https://docs.beagleboard.org/boards/beaglebone/black/ch07.html).
- Python Software Foundation, [`csv`](https://docs.python.org/3/library/csv.html) and [`logging`](https://docs.python.org/3/library/logging.html).

Use the current manufacturer documents for the exact buzzer, driver, relay, lamp, horn, and supply.
