# Teacher BeagleBone preflight

This process prepares evidence; it does not certify unseen hardware. Perform the
physical inspections and measurements locally before any student connects a
breadboard.

## 1. Quarantine and identify

Assign an internal asset ID. Record the printed model and revision, board
condition, connector damage, debris, corrosion, and any attached cape. Do not
publish serial numbers or school asset labels.

## 2. Check power before connecting it

Read the adapter label. Confirm the required voltage, polarity, connector, and
adequate current rating against documentation for that exact board. Inspect the
cable and strain relief. Do not assume a physically fitting adapter is correct.

## 3. Boot without student circuits

Remove unapproved header wiring. Boot the board and confirm its power and status
indicators. Run the evidence script from a normal user account:

```sh
bash collect-beaglebone-evidence.sh
```

Keep the generated folder private. Transfer approved facts into `inventory.csv`.

## 4. Review software evidence

Check the device-tree model, OS release, kernel, storage, Python, `gpiodetect`,
`gpioinfo`, Python `gpiod`, network-interface state, and Linux LED names. Resolve
missing or inconsistent tooling on the teacher reference board before cloning an
image or releasing boards.

## 5. Verify pins rather than remembering them

Complete `verified-header-pin-worksheet.md`. Use the official connector table,
the current image's pinmux information, and `gpioinfo`. Record the gpiochip and
line name/offset actually reported. Recheck after reboot.

## 6. Test in increasing-risk order

1. Run hardware-independent unit tests.
2. Inspect an onboard LED device.
3. Test one resistor-limited external LED with no load driver attached.
4. Test one biased pushbutton input.
5. Test the driver input with the high-current supply disconnected.
6. Only then test an approved load with protection and current limiting.

## 7. Confirm safe shutdown

Stop Python with `Ctrl+C` and verify controlled outputs become inactive. Shut
Linux down using its normal shutdown command or the documented momentary power
button action. Wait until activity ends before removing power. Do not treat
pulling the cable as a normal shutdown method.

## 8. Freeze the classroom reference

Record the approved image, packages, pin worksheet, JSON configuration, wiring
diagram, reference test result, and date. Student instructions must point to this
record rather than an Internet pinout chosen by appearance.

## Authoritative references

- [BeagleBone Black overview and voltage domains](https://docs.beagleboard.org/boards/beaglebone/black/ch04.html)
- [BeagleBone Black expansion connectors and warnings](https://docs.beagleboard.org/boards/beaglebone/black/ch07.html)
- [BeagleBone Black power button and orderly shutdown](https://docs.beagleboard.org/boards/beaglebone/black/ch05.html)
- [BeagleBoard GPIO mapping with `gpioinfo`](https://docs.beagleboard.org/books/beaglebone-cookbook/02sensors/sensors.html#mapping-header-numbers-to-gpio-numbers)
- [libgpiod 2.x Python API](https://libgpiod.readthedocs.io/en/v2.3/python_api.html)
