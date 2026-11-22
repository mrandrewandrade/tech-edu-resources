# BeagleBone traffic light: teacher reference build

This plan separates state-machine verification from physical GPIO work so students can progress when boards are limited or unavailable.

## Hardware inventory gate

For every board, record:

- exact BeagleBone model and revision;
- Linux image, kernel, Python, and GPIO library/tool versions;
- power method and approved supply;
- reserved/default pin functions;
- selected output and input header pins after pin-control verification;
- expansion I/O voltage domain;
- working onboard LED test;
- known defects or quarantined pins.

Do not publish one fixed pin map until the classroom inventory has been checked. The BeagleBone Black documentation identifies expansion I/O as 3.3 V and analogue inputs as a separate 1.8 V maximum domain; this project needs digital GPIO only.

## Software architecture

Require three layers:

1. **State model:** pure Python transition logic with no GPIO import.
2. **Adapter:** keyboard/simulated I/O or BeagleBone GPIO implementation.
3. **Runner:** timing loop, cleanup, logging, and exception handling.

This makes most work testable on an ordinary Linux computer.

## Reference state invariants

- Vehicle green and vehicle red are never on together.
- Pedestrian walk and vehicle green are never on together.
- Startup output is all-stop or another documented safe classroom state.
- A request remains pending until served.
- Repeated presses do not restart an unsafe transition.
- Program stop and caught exceptions request safe outputs before releasing resources.
- Hardware bias makes outputs default off even during boot or disconnected control.

## One-LED hardware gate

1. Select one verified GPIO output.
2. Record the LED type or measured/documented forward voltage.
3. Calculate a conservative resistor from 3.3 V; use the next safe available value.
4. Check resistor power.
5. Build with power removed and receive inspection.
6. Run a short finite output test, not the full state machine.
7. Measure GPIO-high voltage and resistor drop; calculate current.
8. Stop and confirm the output returns to the intended state.

Only then add yellow and green outputs, one at a time.

## Input gate

1. Use a normally open momentary switch.
2. Define idle and active voltages with an approved pull-up or pull-down.
3. Measure both states before connecting the chosen GPIO input if possible through the approved setup.
4. Confirm no external voltage is present while the board is unpowered.
5. Test event handling in a short input script.
6. Add software debouncing and verify rapid/repeated presses.

## Accessible-output choices

Preferred options are a distinct visual flash pattern or a quiet low-current active buzzer through a suitable driver. Never connect an automotive horn. Provide a silent alternative and let students or nearby classmates opt out of sound.

## Timing verification

Use shortened classroom timings. Automated tests should use an injected/fake clock so the suite does not wait in real time. One end-to-end demonstration can use real timings after unit tests pass.

| Case | Required result |
|---|---|
| No request | normal vehicle state persists/loops as designed |
| Request during vehicle go | stored, then served after minimum green |
| Request during warning | does not skip clearance |
| Request during pedestrian state | ignored or stored according to documented rule |
| Repeated/bouncing input | no corrupt or duplicate unsafe transition |
| Program stop | safe output request and resource cleanup |
| Simulated adapter failure | fault logged; outputs move to documented safe state where controllable |

## Reference-build release record

| Check | Result | Date/initials |
|---|---|---|
| Keyboard simulator |  |  |
| Pure state tests |  |  |
| One LED calculation and measurement |  |  |
| Three independent outputs |  |  |
| Button idle/active voltage |  |  |
| Pedestrian cycle |  |  |
| Ten-cycle repeat test |  |  |
| Stop/exception cleanup |  |  |
| Accessible alternative |  |  |

## Diagram requests for the integration stream

1. State diagram showing Startup Safe, Vehicle Go, Vehicle Warn, All Stop, Pedestrian Go, and Pedestrian Clear.
2. Three-LED breadboard schematic with one resistor per LED and a defined button input.
3. System boundary diagram separating pure Python logic, GPIO adapter, and hardware.

Do not assign actual header pins in the generic diagram. Use placeholders tied to the teacher-approved inventory record.

## Reference

BeagleBoard.org, *BeagleBone Black Features and Specification*: <https://docs.beagleboard.org/boards/beaglebone/black/ch04.html>

