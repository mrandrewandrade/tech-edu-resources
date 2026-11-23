# TEJ Linux, Python, and BeagleBone platform

This folder separates project logic from hardware access. The alarm and traffic
controllers, terminal simulation, CSV logger, plots, and tests run without a
BeagleBone. Only `tej_platform/gpio_adapter.py` imports `gpiod`.

## Start without hardware

From this folder:

```sh
python3 -m unittest discover -s tests -v
python3 simulate.py alarm --log alarm-events.csv
python3 simulate.py traffic --log traffic-events.csv
```

At each prompt enter one command. Press `Ctrl+C` or enter `quit` to stop. The
adapter reports that all outputs are inactive when it closes.

## Inspect an onboard LED first

Do not guess an LED device name:

```sh
python3 -m tej_platform.onboard_led --list
python3 -m tej_platform.onboard_led --name TEACHER_APPROVED_NAME
```

If Linux denies permission, stop. Do not add `sudo` or change permissions unless
the teacher has approved the exact change. The program attempts to restore the
LED's previous brightness and kernel trigger.

## Add physical GPIO only after verification

1. Complete the teacher's board and header-pin worksheet.
2. Use `gpiodetect` and `gpioinfo` on the exact board and current image.
3. Copy `gpio-config.example.json` and replace every placeholder.
4. Have the teacher compare the file with the wiring plan while power is off.
5. Run the selected controller with the verified file:

```sh
python3 run_gpio.py alarm --config gpio-config.approved.json
```

The adapter targets the current libgpiod Python 2.x API. It intentionally refuses
an older binding instead of guessing how an old classroom image is configured.

## Interface contract

Project code supplies an `InputSnapshot` to a controller. A controller returns a
`ControllerResult` containing a complete `OutputSnapshot`. An adapter implements:

```text
read_inputs() -> InputSnapshot
write_outputs(OutputSnapshot) -> None
close() -> None
```

Logical input values describe actions, not electrical voltage. For example, an
active-low pressed button becomes `trigger=True`. `close()` must make every
controlled output inactive before releasing resources.

Available logical inputs are `arm`, `disarm`, `trigger`, `silence`, `pedestrian`,
and optional `ambient_value`. Available outputs are `red`, `yellow`, `green`,
`status`, `alarm`, `relay`, and `pedestrian_walk`.

The supplied libgpiod adapter handles digital lines only. An analogue, I2C, or
other sensor needs a separately reviewed adapter that converts its reading into
`ambient_value` while preserving the same interface contract.

Project-page authors should use these exact names. They should not import
`gpiod`, duplicate state machines, or publish an unverified chip/offset mapping.

## Data

`EventLogger` writes a stable CSV schema. Set `data_origin` honestly to values
such as `simulated-terminal`, `synthetic-example`, or `physical-gpio`. The plot
script imports matplotlib only when a graph is requested.
