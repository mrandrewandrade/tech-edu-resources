# Capacitor and sound: calculation and answer notes

These notes support teacher checking. Substitute the actual approved values.

## Energy

$$E=\frac{1}{2}CV^2$$

For 4700 µF at 5.0 V:

$$E=\frac{1}{2}(0.0047)(25)=0.05875\ \text{J}\approx0.059\ \text{J}.$$

For the same capacitance at 10 V, ideal stored energy is four times larger because energy depends on voltage squared. This does not authorize charging a part to 10 V; the source, rating, load, and classroom plan still govern.

## Initial RC charging current

For an initially uncharged ideal capacitor in series with $R$:

$$I(0^+)\approx\frac{V_S}{R}.$$

Check resistor power at the start:

$$P_R(0^+)\approx\frac{V_S^2}{R}.$$

The current and resistor power then fall as the capacitor charges.

## Time constant

$$\tau=RC$$

For an ideal charge toward $V_S$:

$$V_C(t)=V_S\left(1-e^{-t/RC}\right).$$

For an ideal discharge from $V_0$ through one equivalent resistance:

$$V_C(t)=V_0e^{-t/RC}.$$

An LED or active buzzer is not a simple resistor. Treat the exponential as a model whose limitations must be stated.

## Current from measured voltage change

Using two nearby samples:

$$I_C\approx C\frac{V_{C,2}-V_{C,1}}{t_2-t_1}.$$

The sign depends on the chosen current direction. Require the student to draw that direction.

## Constant-current sizing estimate

$$C\approx\frac{I\Delta t}{\Delta V}.$$

Example: 5 A, 0.10 s, 4 V permitted drop:

$$C\approx0.125\ \text{F}=125{,}000\ \mu\text{F}.$$

At the same current and voltage drop, one full second would require approximately 1.25 F. Real requirements are higher or different because horn current is not constant, ESR creates an immediate drop, and the horn has a minimum operating voltage.

## KVL checks

Charge loop:

$$V_S-V_R-V_C=0.$$

Discharge loop with LED:

$$V_C-V_R-V_{LED}=0.$$

## KCL check

At a capacitor node feeding several branches, define current leaving the capacitor as positive:

$$I_C=I_{LED}+I_{buzzer}+I_{bleeder}.$$

If a branch is absent, its current is zero. If the source remains connected during the selected switch state, include source current with a consistent sign.

## Common marking errors

- µF not converted to farads;
- using capacitor voltage rating as its normal operating voltage;
- omitting the square on voltage in stored energy;
- mixing milliseconds and seconds;
- applying $P=VI$ with values from different times;
- treating a horn, LED, or buzzer as a constant resistor without saying it is a first model;
- KVL loop that jumps between disconnected switch states;
- KCL currents drawn without directions.
