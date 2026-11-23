# Sources and adaptation record

The diagrams and questions in this package are original classroom adaptations.
They were not traced from a textbook, tutorial, data sheet, or the photographed
relay problem. Published sources were used to verify conventions, component
limits, and the teaching sequence.

## Textbook sequence

- M. E. Schultz, *Grob's Basic Electronics*, 12th ed., McGraw-Hill Education,
  2016: Chapter 9 for KVL/KCL language and Chapter 22 for capacitor charging,
  discharging, and time-dependent relationships. Chapter 27 supports LED
  polarity and current limiting. The workbook uses new circuits, values,
  wording, questions, and artwork.

## Manufacturer and board documentation

- [TE Connectivity, Micro Relay A/VFMA data sheet](https://www.te.com/content/dam/te-com/documents/automotive/global/ENG_DS_V23074-X0000-A001_0615.pdf):
  used to check that Micro ISO products may be form A or form C, that contact
  ratings depend on load and temperature, and that suppression may be a resistor
  or diode. The classroom relay model is generic; its case diagram and data
  sheet must be checked before wiring.
- [TE Connectivity 9-1904105-7 product page](https://www.te.com/en/product-9-1904105-7.html):
  used as one current manufacturer example of a 12 V, form-C automotive relay.
  It is not a required purchase or a claim that every five-pin relay is wired
  identically.
- [BeagleBoard.org, BeagleBone Black expansion connectors](https://docs.beagleboard.org/boards/beaglebone/black/ch07.html):
  used for the 3.3 V header warning and the instruction to verify pin mux and
  software configuration. The diagram intentionally says `verified GPIO`
  instead of prescribing one pin.
- [BeagleBoard.org Cookbook, Motors](https://docs.beagleboard.org/books/beaglebone-cookbook/04motors/motors.html):
  used to verify the teaching pattern of a GPIO controlling an external
  transistor rather than powering an inductive load directly.
- [Texas Instruments, *Using DRV to Drive Solenoids*, SLVAE59A](https://www.ti.com/lit/an/slvae59a/slvae59a.pdf):
  used to verify the low-side MOSFET arrangement and the freewheeling-diode
  path. TI shows the diode cathode toward the positive supply and anode toward
  the switched low side.

## Deliberate modelling choices

- The 80.0 ohm relay coil, 21.0 W lamps, 6.50 A branch measurement, 5.0 A horn
  estimate, and 1.00 ohm poor-ground fault are original exercise values, not
  copied equipment ratings.
- The five-pin relay symbol uses the common classroom designations 85/86 for
  the coil, 30 for common, 87 for normally open, and 87a for normally closed.
  Students must verify the diagram printed on the actual relay. Coil polarity
  matters when an internal diode is fitted.
- Fuse, conductor, transistor/MOSFET, diode, relay-contact, lamp, horn, and
  supply ratings remain part-specific. The diagrams identify the verification
  point rather than inventing a universal rating.
- The capacitor-to-horn calculation is an energy estimate. It is not an
  instruction to connect a large capacitor directly to a horn.
