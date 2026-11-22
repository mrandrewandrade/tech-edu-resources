# BeagleBone traffic light: software and hardware test matrix

## Pure-Python tests

| ID | Starting state | Input/event | Expected state | Output invariant |
|---|---|---|---|---|
| P01 | startup | initialize | safe/startup state | vehicle green off |
| P02 | vehicle go | no request, timer incomplete | vehicle go | only green on |
| P03 | vehicle go | request, minimum timer complete | vehicle warn | walk off |
| P04 | vehicle warn | timer complete | all stop | green off |
| P05 | all stop | clearance complete | pedestrian go | vehicle red on |
| P06 | pedestrian go | walk timer complete | pedestrian clear | vehicle red on |
| P07 | pedestrian clear | pulse count complete | vehicle go or clearance state | walk off before green |
| P08 | any state | repeated request | documented result | no unsafe combination |
| P09 | any state | stop/exception | safe request/cleanup | outputs not left commanded active |

The actual design may add states, but it must test equivalent safety relationships.

## Keyboard simulator tests

- [ ] Help lists every key and state.
- [ ] Request key is accepted only as documented.
- [ ] Current state and outputs are visible without colour alone.
- [ ] Quit works from every state.
- [ ] Timings can be shortened for testing.
- [ ] Log records state transitions and requests.

## Hardware tests

| ID | Test | Evidence |
|---|---|---|
| H01 | one LED output | resistor calculation, voltage, calculated current |
| H02 | red output alone | correct pin and polarity |
| H03 | yellow output alone | correct pin and polarity |
| H04 | green output alone | correct pin and polarity |
| H05 | button idle | measured voltage and stable software reading |
| H06 | button active | measured voltage and stable software reading |
| H07 | full cycle | video/log plus state/output table |
| H08 | ten requests | no unsafe state; failure count recorded |
| H09 | stop/exception | documented cleanup behaviour |
| H10 | power cycle | known startup output before program begins |

## Troubleshooting order

1. Reproduce the failure in the keyboard simulator.
2. Run pure-state tests.
3. Confirm pin configuration and adapter mapping.
4. Run the relevant one-input or one-output hardware test.
5. Measure voltage.
6. Inspect polarity and breadboard nodes with power removed.
7. Make one change and repeat the same test.

Do not start by swapping the BeagleBone or changing several wires.
