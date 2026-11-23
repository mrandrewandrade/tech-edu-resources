---
title: "Circuit and Program Fault Cards — Teacher Key"
format:
  html:
    embed-resources: true
    toc: false
    page-layout: full
    css: ../tej/electrical-workbook/print.css
execute: {enabled: false}
---

Prepare only one reversible fault at a time. Record the original configuration
before changing it. Students should state a prediction, work from source toward
return, collect evidence, power off before correction, and then repeat the
functional test.

## 1. Open ground

- **Expected evidence:** load positive may measure near source voltage relative
  to battery negative; both sides of a non-conducting load can also float high
  through the load. A voltage-drop test from load ground to battery negative can
  approach source voltage when the open is downstream and the load is commanded
  on.
- **Safe sequence:** verify source and fuse voltage; measure load-positive to
  battery negative; measure load-ground to battery negative; power off and
  inspect the return connector/conductor.
- **Correction:** restore the intended ground path, then repeat the voltage-drop
  test under load.

## 2. Reversed LED

- **Expected evidence:** LED off; a substantial reverse-polarity voltage may be
  present across it. Exact readings depend on the circuit and meter.
- **Safe sequence:** power off; identify anode/cathode from the part and trusted
  documentation; verify resistor placement; use diode mode only while isolated;
  correct orientation.
- **Correction:** anode toward the resistor/positive side, cathode toward return
  for the stated circuit.

## 3. Wrong resistor decade

- **Expected evidence:** with the same approximate resistor voltage, 10 kΩ gives
  one tenth the current of 1.0 kΩ. Colour code or power-off resistance confirms
  the decade.
- **Safe sequence:** measure resistor voltage; calculate current; power off and
  discharge; isolate one lead if needed; measure resistance; compare with the
  required value and tolerance.
- **Correction:** install the approved value and repeat voltage/current
  calculation.

## 4. Terminal 87 versus 87a

- **Expected evidence:** 30–87a is closed with the coil off; 30–87 closes with
  the coil energized. Case diagrams take precedence over physical position.
- **Safe sequence:** read the relay case/datasheet; identify coil voltage; test
  contact voltage in both states; power off before moving the load lead.
- **Correction:** use 87 for a load that should turn on with coil energization,
  or 87a for the intentional inverse action.

## 5. Missing pull resistor

- **Expected evidence:** released input is undefined or noisy; repeated program
  reads may change without a real switch event. Voltage may wander.
- **Safe sequence:** stop the program; inspect the schematic and configured
  internal pull; confirm 3.3 V compatibility; restart a minimal input monitor.
- **Correction:** enable the documented internal pull or install an approved
  external pull-up/pull-down, then verify defined open and closed voltages.

## 6. Incorrect program pin

- **Expected evidence:** program pin identifier does not map to the wired header
  pin, or `gpioinfo` shows a different line/function. Another pin may change.
- **Safe sequence:** stop the program; compare code, header diagram, pinmux and
  physical wire; use an onboard LED or meter-safe test before reconnecting a
  driver.
- **Correction:** change the code or wiring to the verified mapping, not both at
  once, then repeat the minimal test.

## 7. Program not running

- **Expected evidence:** no matching process, no current log entry, terminal
  returned to the prompt, permission error, missing module, or traceback.
- **Safe sequence:** inspect the terminal's final line; check the exact command
  and working directory; inspect the process list; run the smallest script in
  the foreground.
- **Correction:** address the observed execution error, then confirm the process
  and log before changing hardware.

## 8. Simulated blown fuse

- **Expected evidence:** source voltage upstream; near 0 V downstream relative
  to source negative; near source voltage measured across the open fuse while a
  valid downstream path is commanded on.
- **Safe sequence:** voltage-test both sides relative to the same reference;
  measure across the fuse; power off and isolate; inspect the teacher-prepared
  open link. Do not replace a fuse until the cause of a real operation is known.
- **Correction:** restore the teacher-prepared link only after confirming no
  overload or short is present.
