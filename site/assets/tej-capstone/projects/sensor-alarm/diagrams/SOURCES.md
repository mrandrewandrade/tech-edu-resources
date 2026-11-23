# Sensor and alarm diagram sources

These figures are original classroom drawings. They reproduce circuit relationships and safety limits, not the layout or artwork of any textbook or tutorial.

## Primary technical references

- BeagleBoard.org, [BeagleBone Black overview](https://docs.beagleboard.org/boards/beaglebone/black/ch04.html): 3.3 V expansion I/O and 1.8 V maximum analogue inputs.
- BeagleBoard.org, [BeagleBone Black connectors](https://docs.beagleboard.org/boards/beaglebone/black/ch07.html): connector cautions, 3.3 V logic warning, and pin-multiplexing context.
- BeagleBoard.org, [BeagleBone Cookbook sensor examples](https://docs.beagleboard.org/books/beaglebone-cookbook/02sensors/sensors.html): divider/ADC teaching context.
- Vishay, [VEML7700 ambient-light sensor datasheet](https://www.vishay.com/docs/84286/veml7700.pdf): digital sensor supply and I2C application information.
- Texas Instruments, [LM393 comparator datasheet](https://www.ti.com/product/LM393): comparator input constraints and open-collector output behaviour.
- onsemi, [2N3903/2N3904 datasheet](https://www.onsemi.com/pub/Collateral/2N3903-D.PDF): NPN switching characteristics and device limits.
- Texas Instruments, [Driving inductive loads](https://www.ti.com/document-viewer/lit/html/SLVAF04): relay-coil switching and freewheel-path context.

## Diagram-specific notes

- `night-light-standalone` is a first transistor model. Actual threshold depends on sensor range, transistor loading, base resistor, temperature, and component variation.
- `night-light-safe-input-options` shows three alternative architectures. It is not permission to combine them or use an undocumented breakout board.
- `beaglebone-adc-divider-check` deliberately omits universal resistor values. The teacher must check source impedance, tolerance, and the actual board documentation.
- `alarm-door-input` uses an external pull-up for a visible, inspectable classroom circuit. Exact resistor values and pins remain teacher-approved.
- `alarm-output-drivers` separates the direct, resistor-limited LED path from a transistor-driven buzzer path. The exact buzzer type determines whether flyback protection is required.
- `alarm-relay-driver` is a topology, not a parts list. The MOSFET, diode, relay, fuse, supply, lamp, horn, and grounding plan require actual ratings.
- `alarm-state-machine` documents software behaviour and does not replace electrical safety.

Grob and other textbooks may be consulted for general circuit-analysis instruction, but their diagrams are not copied into these assets.
