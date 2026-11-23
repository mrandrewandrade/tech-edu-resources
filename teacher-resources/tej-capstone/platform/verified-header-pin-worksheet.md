# Verified BeagleBone header-pin worksheet

Complete one worksheet for every distinct combination of board model/revision and
Linux image. A visually similar board is not evidence that its mapping is the
same. Keep this teacher record with the reference build.

## Identification

| Field | Verified value | Evidence |
|---|---|---|
| Asset ID |  | Physical label kept private |
| Board model |  | Printed board text and device-tree model |
| Printed revision |  | Physical inspection |
| Linux image/release |  | `/etc/os-release` and class image record |
| Kernel |  | `uname -r` |
| libgpiod CLI version |  | `gpiodetect --version` |
| Python gpiod version/API |  | preflight `gpio.txt` |
| Approved power source |  | Adapter label, polarity, condition, measured value if required |

## One row per proposed signal

| Project signal | Header label | Header pin | Default/pinmux function | Voltage domain | `/dev/gpiochipN` | Line name or offset | `gpioinfo` direction/use evidence | External circuit and resistor | Teacher test result |
|---|---|---:|---|---|---|---|---|---|---|
| Example role only: status LED |  |  |  |  |  |  |  |  |  |
| Example role only: trigger button |  |  |  |  |  |  |  |  |  |

Do not copy the example roles into a student configuration until every cell in
the corresponding row has been verified. Confirm the line remains available
after reboot and is not claimed by HDMI, eMMC, a cape, or another kernel driver.

## Power-off wiring gate

- [ ] Exact board and image match this worksheet.
- [ ] All GPIO signals are in the documented logic domain.
- [ ] No 5 V signal reaches a 3.3 V GPIO.
- [ ] No analogue input can exceed the exact board's ADC maximum.
- [ ] The board is powered before an external circuit can drive any I/O.
- [ ] LED current is limited by a calculated resistor.
- [ ] Button input has a verified internal or external bias.
- [ ] Relay, lamp, horn, motor, and other loads use an approved driver and supply.
- [ ] Output-safe state and program shutdown have been tested without the load.
- [ ] The approved JSON configuration matches this worksheet exactly.
