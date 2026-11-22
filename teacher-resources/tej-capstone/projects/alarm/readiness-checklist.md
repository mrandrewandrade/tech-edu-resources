# Linux Alarm — Readiness Checklist

## Software first

- [ ] States and events are named.
- [ ] Transition table is complete.
- [ ] Logic can run with simulated or keyboard input.
- [ ] Arming delay and output patterns are configurable.
- [ ] Event log contains no private/security information.
- [ ] Cleanup requests every output off.

## Input

- [ ] Exact input pin and mode verified.
- [ ] External pull-up/pull-down and switch action documented.
- [ ] Open/closed node voltages measured before connection.
- [ ] Active-low/active-high interpretation verified.
- [ ] Bounce response tested.

## Outputs

- [ ] LED resistor calculation complete.
- [ ] Buzzer voltage/current and driver requirements verified.
- [ ] Relay coil is not connected directly to GPIO.
- [ ] Flyback diode orientation checked.
- [ ] Lamp/horn supply is separate and fused.
- [ ] Core loads work independently.

## Integration and completion

- [ ] Starts DISARMED or another explicitly approved safe state.
- [ ] Three complete arm/trigger/silence/reset trials pass.
- [ ] Log matches observed transitions.
- [ ] Input-disconnect response tested.
- [ ] `Ctrl+C`, normal exit, and prepared error leave outputs off.
- [ ] Fault diagnosis and revision recorded.
- [ ] Portfolio evidence complete.
