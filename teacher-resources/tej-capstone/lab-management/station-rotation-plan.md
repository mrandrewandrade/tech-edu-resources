# TEJ Capstone Lab Station Plan

## Purpose

Keep every student doing relevant work while BeagleBones, meters, protected supplies, and relay hardware are limited. Stations produce evidence that transfers directly into the design log and portfolio.

## Team model

- Plan for **12 teams of 2** in a class of 24.
- Label teams A–L and place two teams at each station.
- If groups of 3–4 are necessary, preserve individual code, measurement, diagnostic, and explanation evidence.
- A station is not “finished” when the device works; it is finished when the required evidence is recorded and the station is reset.

## Six stations

### S1 — Linux/Python simulator

**Equipment:** Linux computers or approved environment; hardware-independent project code; test instructions.

**Evidence:** safe startup state, one normal test, one boundary/timing test, one error/fix or log entry.

**No controller required.** This is the primary fallback when boards are unavailable.

### S2 — Breadboard and power-off inspection

**Equipment:** breadboards, components, printed schematic, continuity reference if assigned.

**Evidence:** node map, polarity/pinout checks, current-limiting/protection parts, teacher power-off approval.

**Power remains disconnected** until approval.

### S3 — Voltage measurement

**Equipment:** known-safe low-voltage reference circuit, working meters, test-point sheet.

**Evidence:** prediction, named test points, meter mode/range/jacks, source/load/control voltage, KVL/KCL or other suitable check.

Resistance/continuity work occurs only with power removed and stored energy discharged.

### S4 — Relay and lamp trainer

**Equipment:** fused 12 V relay/lamp station, manual switch, verified relay socket, protected driver demonstration where assigned.

**Evidence:** trace 85/86 coil and 30/87/87a contact paths, predict contact state, measure control and load voltages, diagnose one inserted open/poor-ground fault.

Teacher controls first energizing. No horn at this station.

### S5 — Shared horn/control demonstration

**Equipment:** teacher-controlled fused horn/lamp demonstration, quiet buzzer equivalent, relay/driver, physical barrier or marked control area.

**Evidence:** explain why GPIO cannot power the horn, identify the driver/flyback/fuse, compare quiet and horn load behaviour, calculate/interpret current or power from teacher-provided evidence.

Use a lamp/quiet buzzer whenever sound would create a barrier or distraction. Horn activation is brief and announced.

### S6 — Portfolio and documentation

**Equipment:** portfolio source, design log, approved photos/data, privacy checklist.

**Evidence:** one complete section with caption/alt text/units/citation, working link or local render, individual reflection update.

This station is also suitable for students temporarily unable to access physical equipment, but it must document actual technical reasoning rather than decorative site work.

## Three-day rotation for 12 teams

Each cell lists the station used by the team pair.

| Team pair | Day 1, R1 | Day 1, R2 | Day 2, R3 | Day 2, R4 | Day 3, R5 | Day 3, R6 |
|---|---:|---:|---:|---:|---:|---:|
| A–B | S1 | S2 | S3 | S4 | S5 | S6 |
| C–D | S2 | S3 | S4 | S5 | S6 | S1 |
| E–F | S3 | S4 | S5 | S6 | S1 | S2 |
| G–H | S4 | S5 | S6 | S1 | S2 | S3 |
| I–J | S5 | S6 | S1 | S2 | S3 | S4 |
| K–L | S6 | S1 | S2 | S3 | S4 | S5 |

If six complete stations cannot operate simultaneously, use two cohorts:

- Cohort 1 completes S1–S3 while Cohort 2 completes S4–S6.
- Swap cohorts the next class.
- Keep S5 teacher-scheduled rather than open-access.

## Suggested 75-minute period

| Time | Action |
|---:|---|
| 0–8 min | Entry, station assignment, safety/goal briefing |
| 8–33 min | Rotation A: predict, perform, record |
| 33–37 min | Power down, count parts, transition |
| 37–62 min | Rotation B: predict, perform, record |
| 62–71 min | Reset, design-log update, evidence upload/save |
| 71–75 min | Teacher check and dismissal by reset station |

For a shortened class, run one 30-minute rotation plus documentation. Do not compress the power-down/reset step.

## Sign-out and access

Record:

- team and student names;
- station/bin/controller/meter identifier;
- starting condition and missing/damaged parts;
- teacher approval state;
- return condition;
- damaged/consumed/missing items;
- student and teacher initials where required.

High-current stations, controllers, meters, and specialized sensors remain assigned to a numbered station. Do not allow unrecorded parts to migrate between teams.

## Absence recovery

An absent student does not need the team to repeat a safe successful build solely for reenactment.

Use one or more of:

- keyboard simulator test and explanation;
- reference circuit voltage/diagnostic task;
- team data clearly identified as shared evidence;
- individual schematic trace;
- five-minute teacher conference;
- portfolio explanation of a team fault/revision;
- scheduled January 25–26 demonstration.

The returning student still provides individual evidence for the intended learning.

## Equipment failure

1. Label the item **do not use** and remove it from circulation.
2. Record the symptom and last known safe condition.
3. Move the team to S1 or S6 rather than waiting.
4. Substitute a known-good part only after recording the diagnostic reason.
5. Keep equipment failure separate from the student’s achievement record.

## Teacher preparation decisions

- Actual number of working BeagleBones and safe power supplies.
- Number and type of meters; whether any current function will be used.
- Number of relay/lamp trainers that can be supervised.
- School requirements for horn noise, eye/hearing access, and electrical work.
- Room layout, emergency shutoff, and sight lines.
- Which station evidence will be assessed versus formative.
