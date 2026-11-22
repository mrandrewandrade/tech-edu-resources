# Automatic Night Light — Readiness Checklist

## Before parts are issued

- [ ] Student chose minimum, proficient, or extension scope.
- [ ] Success criteria name bright/dark test conditions and response.
- [ ] Exact sensor/module documentation is attached.
- [ ] Sensor direction is predicted.
- [ ] LED resistor/current/power calculation is complete.
- [ ] Driver/comparator pinout is verified.
- [ ] Controller input maximum is recorded.
- [ ] Schematic separates source, sensor, controller, driver, load, and return.

## Before controller connection

- [ ] Sensor is powered from the approved rail.
- [ ] Bright and dark outputs have been measured.
- [ ] I²C pull-ups are not connected to 5 V.
- [ ] Direct ADC route remains conservatively below 1.8 V in every tested condition.
- [ ] Student can point to the input test point and reference ground.
- [ ] Board pin and Linux GPIO/I²C configuration are verified.

## Before integration

- [ ] Sensor/input works alone.
- [ ] LED/driver works alone.
- [ ] Output defaults off.
- [ ] Threshold and hysteresis are documented.
- [ ] Teacher performed a power-off inspection.

## Completion

- [ ] Three bright-to-dark and dark-to-bright trials.
- [ ] Boundary/chatter test.
- [ ] Sensor-disconnect fault test.
- [ ] Voltage/current table complete.
- [ ] One evidence-based revision.
- [ ] Portfolio evidence and source attribution complete.
