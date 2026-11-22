# Capacitor and sound: teacher reference demonstration

The classroom sequence uses a low-current LED or active buzzer. The automotive horn is a separate analysis and optional teacher demonstration.

## Student reference circuit gate

Record the actual part information:

| Item | Required record |
|---|---|
| Source | voltage, current limit, polarity |
| Capacitor | capacitance, tolerance if known, voltage rating, polarity, condition |
| Charging resistor | resistance, power rating, calculated initial current |
| Bleeder/discharge resistor | resistance, power rating, predicted discharge interval |
| LED branch | LED type/polarity, series resistor, predicted current |
| Buzzer branch, if used | exact part, active/passive, voltage range, current, polarity |
| Switch | contact form and approved charge/discharge topology |

Build and test one reference circuit. Confirm that the student measurement interval is long enough to observe but short enough for class. Measure capacitor voltage before and after the nominal interval. Replace values rather than improvising unsafe parallel capacitors.

## Buzzer identification

An active buzzer makes a tone from a suitable DC supply. A passive piezo or magnetic transducer requires a changing waveform. Appearance is not proof. Test only within the documented voltage/current range and label the classroom stock.

## Demonstration sequence

1. Show the uncharged capacitor and verify near-zero voltage.
2. Identify polarity and rating.
3. Charge through the resistor while showing $V_S=V_R+V_C$.
4. Disconnect the source using the switch, not by pulling live breadboard wires.
5. Observe the small load and record $V_C(t)$.
6. Verify the bleeder path and final voltage.
7. Compare a second capacitance or resistance while holding other factors constant.
8. Complete the horn calculation before showing the separate relay-controlled station.

## Horn station boundary

The capacitor must not be placed directly across the horn as the student experiment. If a horn demonstration is used:

- the horn uses a separately fused 12 V source and appropriate wiring;
- the capacitor affects a transistor/comparator/timer control signal;
- the control stage operates a verified relay;
- the relay contacts carry horn current;
- the relay coil has verified flyback suppression;
- a hardware enable limits when the horn can operate;
- sound duration and location are controlled;
- a lamp or silent indicator is available instead.

## Example scale calculation

For a first estimate with approximately constant current,

$$
C\approx\frac{I\Delta t}{\Delta V}.
$$

At 5 A for 0.10 s with an allowed 4 V drop, the ideal estimate is 0.125 F or 125,000 µF. Record the actual horn current and permitted voltage range before using the calculation. Discuss ESR, wiring loss, surge, and the horn's nonlinear behaviour.

## Release record

| Check | Result | Date/initials |
|---|---|---|
| Capacitor values/ratings verified |  |  |
| Initial charging current safe |  |  |
| Bleeder discharges reliably |  |  |
| LED/buzzer branch within rating |  |  |
| Charge KVL evidence |  |  |
| Discharge timing suitable |  |  |
| Horn estimate reviewed |  |  |
| Relay-control demo safe, if used |  |  |

## Included diagrams

- [Separate charge and discharge switch states](../../../../site/assets/tej-capstone/project-diagrams/capacitor-charge-discharge.svg)
- [Capacitor timing with separately powered horn or lamp](../../../../site/assets/tej-capstone/project-diagrams/capacitor-horn-control.svg)

The diagrams use distinct source boundaries, large polarity marks, no crossed conductors, and separate low-energy and high-current paths. Students still create their own measured voltage-time graph and mark one time constant from their selected parts.

