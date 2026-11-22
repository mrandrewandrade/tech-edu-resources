# GPIO compatibility notes

The student platform targets the current libgpiod Python 2.x API using
`LineSettings`, `request_lines`, `LineRequest.get_value`, and
`LineRequest.set_value`. The hardware adapter refuses a binding that lacks that
API. This is intentional: silently translating an old example could control a
different line or leave an output active.

Older classroom images may use libgpiod 1.x, an older `gpiod` Python binding,
deprecated sysfs GPIO, or a board-specific library such as Adafruit_BBIO. Treat
that as an image-management decision:

1. record the exact existing image and package versions;
2. decide whether to update the teacher reference image;
3. repeat the pin and safe-state verification after any update;
4. if an older image must remain, implement and test a separate adapter that
   preserves the same `read_inputs`, `write_outputs`, and `close` contract;
5. do not mix two GPIO APIs in student project code.

No compatibility note can substitute for the exact board's voltage-domain,
pinmux, connector, and power-sequencing documentation.
