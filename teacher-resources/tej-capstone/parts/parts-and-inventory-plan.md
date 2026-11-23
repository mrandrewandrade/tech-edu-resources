# TEJ Capstone Parts and Inventory Plan

## Planning assumptions

- Class size: **24 students**.
- Preferred build teams: **12 teams of 2**.
- Practical alternative with limited controllers: **6 groups of 4**, with individual evidence requirements.
- Automotive relay/horn work is preferably a **shared station**, not 12 complete kits.
- Price bands are rough Canadian classroom-planning bands, not current vendor quotations.
- **This plan does not authorize or place any order.** Reconcile stock, test samples, verify exact part documentation, then request purchasing approval through the normal process.

## Priority definitions

- **Must-have:** required for the minimum project or safe operation.
- **Useful:** improves reliability, access, troubleshooting, or reuse.
- **Extension:** adds capability only after minimum evidence is complete.

## Common equipment pool

| Item | Priority | Preferred availability for 24 students | Minimum workable pool | Spare/condition rule | Planning band |
|---|---|---:|---:|---|---:|
| BeagleBone with verified power supply and image | Must-have for hardware pathway | 12 | 4–6 rotating | One tested spare if available | Existing stock; replacement often $80+ each |
| Solderless breadboard | Must-have | 15 | 12 | 3 spare/repair units | $5–$15 each |
| Male-male jumpers | Must-have | 300+ | 200 | Sort by usable condition | $15–$35 class pack |
| Digital multimeter with intact probes | Must-have | 12 | 6 rotating | Test fuse, leads, and battery | Existing stock; $20–$80 each |
| Protected low-voltage breadboard source | Must-have | 12 | 6 rotating | Verify voltage/current limiting | Existing stock; varies |
| USB/network/console cables appropriate to boards | Must-have | 15 | 12 | Label by type; test data capability | $5–$15 each |
| Insulated test leads/alligator adapters | Useful | 24 pairs | 12 pairs | Remove damaged leads | $20–$60 class set |
| Component trays and labelled team bins | Useful | 12 | 6 | One return/check card per bin | $3–$10 each |
| Quiet active buzzer test load | Useful | 15 | 6 | Confirm voltage and current | $1–$5 each |
| Automotive horn | Extension/shared demo | 1 | 1 | Teacher-controlled; quiet alternative required | $20–$50 |

Do not assume a “5 V” header is a safe logic input. Confirm exact board signals, power state, and pin mapping before assigning student connections.

## Project 1: automatic night light

The safest base path is an LDR/resistor/transistor light independent of the BeagleBone. The controller extension requires a verified digital sensor/comparator output or a correctly limited analogue path within the exact board’s ADC range.

| Part | Priority | Per team | 12 teams | Recommended spare | Class target | Planning band/team |
|---|---|---:|---:|---:|---:|---:|
| Breadboard and jumpers | Must-have | 1 set | 12 | 3 | 15 | Common pool |
| Photoresistor/LDR | Must-have | 1 | 12 | 3 | 15 | <$2 |
| Fixed resistor assortment including likely divider values | Must-have | 3 | 36 | 12 | 48 | <$2 |
| LED | Must-have | 1 | 12 | 6 | 18 | <$1 |
| LED current-limiting resistor | Must-have | 1 | 12 | 6 | 18 | <$1 |
| NPN transistor or verified logic-level MOSFET | Must-have for switched load | 1 | 12 | 3 | 15 | $1–$4 |
| Base/gate resistor and pull resistor | Must-have | 2 | 24 | 8 | 32 | <$1 |
| Digital light sensor or comparator module | Useful controller path | 1 | 12 | 2 | 14 | $3–$12 |
| Quiet buzzer or small approved lamp | Extension | 1 | 12 | 3 | 15 | $2–$8 |

**Approximate new-parts band:** $5–$15 per team excluding controller, breadboard, meter, and reusable leads.

**Verify before issue:** sensor supply/output voltage; LDR range; transistor/MOSFET pinout and drive; LED forward voltage/current; ADC maximum if used; module pull-ups; load current.

## Project 2: Linux/Python alarm

| Part | Priority | Per team | 12 teams | Recommended spare | Class target | Planning band/team |
|---|---|---:|---:|---:|---:|---:|
| Breadboard and jumpers | Must-have | 1 set | 12 | 3 | 15 | Common pool |
| Normally open pushbutton/door switch | Must-have | 2 | 24 | 6 | 30 | $1–$5 |
| Red/green status LEDs | Must-have | 2 | 24 | 6 | 30 | <$2 |
| LED current-limiting resistors | Must-have | 2 | 24 | 8 | 32 | <$1 |
| Input pull resistor(s), if external | Must-have when required | 2 | 24 | 8 | 32 | <$1 |
| Low-current active buzzer matched to supply | Must-have physical pathway | 1 | 12 | 3 | 15 | $2–$6 |
| Transistor/MOSFET driver parts | Useful for buzzer/load | 1 set | 12 | 3 | 15 | $2–$6 |
| Second approved sensor | Extension | 1 | 12 | 2 | 14 | $3–$15 |
| Relay/lamp interface | Extension/shared | 0–1 | Prefer stations | 1 station spare | 4–5 sets | See relay plan |

**Approximate new-parts band:** $6–$18 per team excluding controller and common equipment.

**Verify before issue:** buzzer active/passive type, voltage/current, polarity; switch contact arrangement; GPIO pull configuration; transistor/MOSFET pinout; external sensor logic level.

## Project 3: automotive relay trainer

### Full-team quantities (only if 12 trainers are intentionally desired)

| Part | Priority | Per team | 12 teams | Spare | Class target |
|---|---|---:|---:|---:|---:|
| 12 V SPDT automotive relay | Must-have | 1 | 12 | 2 | 14 |
| Matching relay socket/pigtail | Must-have | 1 | 12 | 2 | 14 |
| Fused 12 V protected source connection | Must-have | 1 | 12 | 2 | 14 |
| Fuse holder and approved fuse | Must-have | 1 | 12 | 3 holders/12 fuses | 15 holders + fuse stock |
| 12 V indicator lamp or protected equivalent | Must-have | 1 | 12 | 3 | 15 |
| Manual control switch | Must-have | 1 | 12 | 3 | 15 |
| Flyback diode | Must-have for electronic coil control | 1 | 12 | 6 | 18 |
| NPN transistor or logic-level MOSFET | Must-have for GPIO control | 1 | 12 | 3 | 15 |
| Base/gate and pull resistors | Must-have | 2 | 24 | 8 | 32 |
| Terminal blocks/insulated leads | Must-have | 1 set | 12 | 3 | 15 sets |
| Automotive horn | Extension | 0 | 0 | — | 1 shared |

### Recommended shared-station quantities

Build **four relay/lamp stations plus one tested spare**. This supports two teams per station across rotations without purchasing 12 automotive sets.

| Item | Four active stations | Spare | Total target |
|---|---:|---:|---:|
| Relay and matching socket | 4 | 1 | 5 |
| Fused source connection | 4 | 1 | 5 |
| Indicator lamp | 4 | 1 | 5 |
| Manual switch | 4 | 2 | 6 |
| Driver/protection component set | 4 | 2 | 6 |
| Insulated terminal/lead set | 4 | 1 | 5 |
| Horn demonstration station | 1 | 0 | 1 |

**Approximate new-parts band:** $20–$45 per complete relay/lamp trainer; $100–$225 for five reusable stations, excluding protected supplies and meters. A horn station can add $25–$75 depending on enclosure, switch, fuse, leads, and source already available.

**Verify before issue:** actual relay case diagram; coil voltage/resistance/current; suppression already inside relay or socket; contact current/voltage; 30/85/86/87/87a mapping; socket wire colours; lamp/horn steady and inrush current; fuse and conductor ratings; supply current capacity; transistor/MOSFET safe load and drive.

## Project 4: BeagleBone traffic light

| Part | Priority | Per team | 12 teams | Recommended spare | Class target | Planning band/team |
|---|---|---:|---:|---:|---:|---:|
| Breadboard and jumpers | Must-have | 1 set | 12 | 3 | 15 | Common pool |
| Red LED | Must-have | 1 | 12 | 3 | 15 | <$1 |
| Yellow LED | Must-have | 1 | 12 | 3 | 15 | <$1 |
| Green LED | Must-have | 1 | 12 | 3 | 15 | <$1 |
| Current-limiting resistors | Must-have | 3 | 36 | 12 | 48 | <$2 |
| Pedestrian pushbutton | Must-have | 1 | 12 | 3 | 15 | $1–$3 |
| Pull resistor(s), if external | Must-have when required | 1–2 | 24 | 8 | 32 | <$1 |
| Quiet active buzzer | Useful/accessibility | 1 | 12 | 3 | 15 | $2–$6 |
| Diffuser/model housing | Extension | 1 set | 12 | — | Student-designed | $0–$10 |

**Approximate new-parts band:** $4–$12 per team excluding controller/common equipment.

**Verify before issue:** LED polarity/forward voltage, current target and GPIO current boundary, input pull configuration, buzzer type/current, exact safe GPIO pins.

## Universal consumables and spares

| Item | Starting target | Reorder/repair trigger |
|---|---:|---|
| 220–1,000 ohm LED resistors | 100 mixed/labelled | Fewer than 48 verified |
| 1 k–100 k divider/pull resistors | 150 mixed/labelled | Any planned value below 20 verified |
| General LEDs | 75 | Fewer than 45 verified |
| Pushbuttons/switches | 40 | Fewer than 30 verified |
| Small-signal transistors/MOSFETs | 25 | Fewer than 15 verified |
| Flyback diodes | 25 | Fewer than 18 verified |
| Jumper wires | 300+ | Fewer than 200 undamaged |
| Correct fuses for trainer | At least 3 complete changes/station | Fewer than one full class reset |

Keep rejected/damaged components physically separated from usable stock. A “mystery parts” bin is not suitable for a time-limited capstone unless component identification is itself the assigned investigation.

## Must-have, useful, and extension summary

### Must-have before January project launch

- verified controllers/power supplies or a dependable simulator fallback;
- breadboards, jumpers, resistors, LEDs, switches, buzzers;
- working voltage-capable meters;
- protected low-voltage sources;
- transistor/MOSFET driver components for non-LED loads;
- fuses, insulated connections, and relay sockets for relay stations;
- labelled bins and an inventory/sign-out process.

### Useful

- spare imaged microSD cards where appropriate;
- colour-coded test leads;
- known-good reference components;
- quiet buzzers and protected lamp loads;
- printed pin maps/datasheets for the exact parts;
- reference builds that remain teacher-controlled.

### Extensions only

- extra sensors;
- enclosures;
- additional relays;
- automotive horn;
- displays/network features;
- op-amp/comparator path;
- student-specific purchased parts.

## Inventory reconciliation procedure

1. Count physical stock; do not copy expected quantities into the actual column.
2. Test a sample from each lot and every high-value controller/meter.
3. Record exact part numbers and package/pinout variants.
4. Mark usable, repair/test required, and reject quantities separately.
5. Allocate parts first to the minimum viable versions.
6. Create shared stations for expensive/high-current parts.
7. Determine only then whether a purchase request is necessary.
8. Reconcile issued/returned/damaged/consumed quantities after demonstrations.

The companion `inventory-reconciliation.csv` is intentionally blank and can be copied for pre-project and post-project counts.
