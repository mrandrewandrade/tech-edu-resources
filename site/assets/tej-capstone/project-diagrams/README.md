# Output-control project diagrams

These are original, print-first vector drawings made for the Grade 11 TEJ capstone handouts. No textbook scan or web image is embedded.

## Source basis

| Diagram | Technical basis |
|---|---|
| Relay contact states and manual loop | TE Connectivity Micro Relay A/VFMA data sheet: form A/form C arrangements, ISO pin assignment, coil data, and optional integrated suppression |
| Relay GPIO driver | BeagleBoard Black 3.3 V I/O documentation; TI inductive-load clamping guidance; exact parts still require their own data sheets |
| Traffic-light hardware | BeagleBoard Cookbook external-LED tutorial: one series resistor per LED branch and conservative GPIO current |
| Traffic-light state machine | Original classroom logic model derived from the project requirements |
| Capacitor charge/discharge | Panasonic capacitor tutorial: source-side charge state and load-side discharge state |
| Capacitor horn control | Original energy-flow architecture combining the verified relay boundary with capacitor timing |

## References

- TE Connectivity, Micro Relay A/VFMA: <https://www.te.com/content/dam/te-com/documents/automotive/global/ENG_DS_V23074-X0000-A001_0615.pdf>
- BeagleBoard, external LED tutorial: <https://docs.beagleboard.org/books/beaglebone-cookbook/03displays/displays.html>
- BeagleBoard Black documentation and CC BY-SA 4.0 notice: <https://docs.beagleboard.org/boards/beaglebone/black/index.html>
- Panasonic, Basic Knowledge of Capacitors (1): <https://industrial.panasonic.com/ww/ds/ss/technical/b2>
- Texas Instruments, switching inductive loads: <https://www.ti.com/document-viewer/lit/html/SLVAF04/GUID-6EC58385-6811-4984-B5CF-9CD8D8E7D24E>

## Quality-control rules used

- large sans-serif labels;
- black lines on white for grayscale printing;
- no colour-only meaning;
- no crossed conductors;
- arrows only where state-flow direction is unambiguous;
- control and load power kept in separate panels;
- text alternatives supplied where diagrams appear in Quarto;
- generic diagrams never override the exact case marking, socket map, data sheet, GPIO inventory, or measured part values.

Grob's or another commercial textbook may be added as a reading reference when the exact edition and page are supplied. Its artwork should not be copied into this repository without permission.
