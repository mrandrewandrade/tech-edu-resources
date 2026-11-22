# TEJ3M Semester 1 Finish Plan

## Planning frame

This plan assumes one daily secondary class, a catch-up week from **Monday, November 23 to Friday, November 27, 2026**, winter break from **December 21, 2026 to January 1, 2027**, final regular classes on **January 25–26, 2027**, and semester assessment from **January 27 to February 2, 2027**. Confirm school-specific assemblies, altered timetables, room changes, and assessment details before publishing student deadlines.

The finish is one connected sequence:

> complete current work -> establish voltage and breadboard evidence -> introduce the portfolio -> learn Linux/Python control -> build one approved project -> test, document, and present

The four supported projects are an automatic night light, a Linux/Python alarm, an automotive relay trainer, and a BeagleBone traffic light. A student-designed alternative is acceptable only after its schematic, bill of materials, safety boundary, evidence plan, and fallback are approved.

## Non-negotiable evidence by the end of the semester

Every student submits evidence of:

1. a problem, constraints, and measurable success criteria;
2. an approved schematic or system diagram;
3. a bill of materials with ratings and verified part identities;
4. safe low-voltage construction or an equivalent approved simulation/diagnostic pathway;
5. Linux and Python work, including a tested input/output or hardware-independent simulator;
6. voltage and circuit measurements with units and named test points;
7. KVL/KCL or other suitable circuit reasoning for the chosen topology;
8. at least one recorded fault, diagnostic test, correction, and retest;
9. an individual explanation even when construction is completed in a team; and
10. a portfolio entry that distinguishes predictions, observations, revisions, and conclusions.

## Calendar at a glance

| Dates | Main purpose | Required checkpoint |
|---|---|---|
| Nov. 23–27 | Catch up, diagnose gaps, and establish current standing | Missing-work conference and one verified circuit/meter skill |
| Nov. 30–Dec. 4 | Voltage, breadboards, safe power-up, and KVL | Working LED/pushbutton circuit plus voltage table |
| Dec. 7–11 | KCL, capacitor behaviour, relays, and project demonstrations | Short investigation and ranked project choices |
| Dec. 14–18 | Assign portfolio; Linux/Python launch; project proposal | Portfolio shell plus approved or revision-required proposal |
| Dec. 21–Jan. 1 | Winter break | No new required hardware work |
| Jan. 4–8 | BeagleBone/Linux preflight and staged project start | Tested Python logic and approved unpowered wiring |
| Jan. 11–15 | Build, measure, diagnose, and revise | Mid-build evidence conference |
| Jan. 18–22 | Final two-week finish: testing, documentation, and presentation | Demonstration-ready project and portfolio draft |
| Jan. 25–26 | Contingency, individual demonstrations, portfolio transfer, assessment preparation | Final evidence package |
| Jan. 27–Feb. 2 | Semester assessment | Scheduled assessment evidence |

## Detailed teaching sequence

### November 23–27: catch-up and readiness

**Purpose:** recover unfinished work without beginning another large unit, identify who needs an alternate pathway, and ensure students can use the orange and black meters safely for resistance and DC voltage.

Suggested sequence:

- **Monday:** individual status check; sort work into complete, repairable, and replace-with-equivalent-evidence.
- **Tuesday:** resistance review with power removed; identify resistor values and tolerances; repair documentation gaps.
- **Wednesday:** DC voltage demonstration; COM and V/ohm ports; measure a battery/source and polarity.
- **Thursday:** small-group correction stations; portfolio evidence collection begins with existing work.
- **Friday:** readiness check: each student demonstrates one safe meter setup and submits a realistic completion plan.

Do not allow catch-up to become five unstructured work periods. Use short conferences and daily proof-of-progress entries in the design log.

### November 30–December 4: voltage and breadboards

**Learning focus:** breadboard nodes and rails, schematic-to-breadboard translation, voltage measured in parallel, source voltage, voltage drops, and KVL.

Minimum evidence:

- approved LED/resistor/pushbutton schematic;
- unpowered breadboard inspection;
- measured source, resistor, and LED voltages;
- KVL comparison with a brief explanation of measurement difference;
- current estimated from resistor voltage rather than requiring beginner current-jack use.

Extension: compare two meters at the same test points and discuss resolution, range, sign, and uncertainty.

### December 7–11: choices and circuit reasoning

**Learning focus:** branch current, KCL, capacitor charge/discharge, relay coil versus relay contacts, and why a GPIO cannot power a horn, lamp, motor, or automotive relay coil directly.

Use short demonstrations of all four supported projects. Students complete a project-choice matrix based on interest, difficulty, required parts, and available evidence—not novelty alone.

Minimum checkpoint:

- first and second project choice;
- one-sentence problem statement;
- one measurable success criterion;
- initial component list;
- individual role preference and one skill-development goal.

### December 14–18: portfolio assigned before winter break

**Portfolio checkpoint by December 18:**

- site renders locally or an approved non-public alternative exists;
- student changes teacher-approved display identity, site title, and colours;
- Projects, About, and Privacy sections work;
- optional Blog/Skills sections are intentionally enabled or disabled;
- one existing project entry contains real evidence and useful alt text;
- no student number, private account, schedule, classroom code, serial number, password, token, or identifiable information about another student appears.

**Project checkpoint by December 18:**

- proposal submitted;
- schematic/system diagram labelled;
- BOM and ratings listed;
- Linux/Python plan identified;
- measurements and tests planned;
- project marked **approved**, **revise**, or **alternate pathway**.

No student should be required to purchase parts over the break. The teacher resolves stock, substitutions, groups, and station access before January.

### January 4–8: staged start

**Purpose:** remove platform uncertainty before project pressure increases.

- Confirm board model, Linux image, power supply, login, Python, GPIO interface, and exact safe pins.
- Run hardware-independent Python tests first.
- Demonstrate onboard output, then one resistor-limited external LED.
- Approve unpowered student wiring before energizing.
- Use keyboard simulation or documentation stations while hardware is unavailable.

Friday checkpoint:

- code starts safely and stops safely;
- one input/output behaviour or simulator test passes;
- schematic matches the planned build;
- first predicted voltages are recorded;
- teacher records an observation or short conversation for each student.

### January 11–15: build, test, troubleshoot

This is the first of the final two weeks devoted mainly to testing, documentation, and presentation. New features are allowed only when the minimum project already works or the team has an approved recovery plan.

Required mid-build conference:

1. Student identifies the input, controller, driver/protection, load, and return.
2. Student names the next safe test before connecting power.
3. Student shows one voltage measurement and explains the reference point.
4. Student identifies a fault or mismatch and selects one variable to isolate.
5. Student states what individual evidence they will add to the portfolio.

### January 18–22: prove, document, present

This is the second final week. Freeze major design additions early in the week.

- **Monday:** success-criteria test and remaining-fault triage.
- **Tuesday:** measurement table, code tests, and repeatability check.
- **Wednesday:** final controlled demonstration or equivalent diagnostic walkthrough.
- **Thursday:** portfolio evidence, captions, alt text, citations, and privacy check.
- **Friday:** short presentation/rehearsal, peer question, and individual reflection.

The product need not be perfect. A partly unsuccessful circuit can earn strong achievement when the student provides a safe build, sound reasoning, useful measurements, disciplined troubleshooting, supported revisions, and an honest conclusion.

### January 25–26: contingency and closure

Reserve these days for:

- students absent during demonstrations;
- a second evidence conference where individual contribution is unclear;
- replacement evidence after equipment failure;
- portfolio transfer checklist;
- parts return and inventory reconciliation;
- short assessment preparation.

Do not make January 25–26 the assumed completion window for every group; that removes the only realistic contingency.

## Shortened-course alternatives

### One lost day

- Combine demonstration and project-choice work.
- Use one measured circuit value instead of a full second data set.
- Replace a full-class presentation with a two-minute teacher conference.

### Two or three lost days

- Freeze projects at the minimum viable version: one input, one programmed decision, one protected output.
- Make data logging, second sensors, horns, relays, web interfaces, and enclosures optional.
- Use a supplied schematic that students annotate and verify rather than requiring a complete original schematic.
- Keep the fault/correction record and individual explanation; these are higher-value evidence than cosmetic completion.

### Snow day or widespread absence

Remote-capable work:

- Python state-machine tests with simulated keyboard input;
- portfolio organization and privacy check;
- schematic annotation;
- predicted-voltage table;
- datasheet search using teacher-provided documents;
- troubleshooting decision tree.

Do not require students to take school electronics home.

### Assembly or shortened period

Use a bounded task that can stop cleanly:

- one test-point prediction and measurement;
- one code test;
- one project photograph and caption;
- one design-log update;
- one component/datasheet verification.

Do not begin relay/horn energizing or a new breadboard build when shutdown time is uncertain.

### Equipment failure

Equivalent evidence, in order of preference:

1. repair or substitute the failed component after diagnosis;
2. move to the keyboard/simulated I/O adapter while preserving the same Python logic;
3. analyze a teacher-provided measurement set and explain the expected physical tests;
4. complete a diagnostic walkthrough on a reference circuit;
5. document why available evidence cannot support a stronger conclusion.

Record the equipment limitation separately from the student's achievement.

### Student absence

- Preserve individual code, calculations, and design-log ownership.
- Provide photographs/data from the shared build without representing them as the absent student's direct observation.
- Schedule a short individual conversation or diagnostic task.
- Avoid requiring the team to rebuild a stable project merely to recreate a missed moment.

## Grouping and accountability

Recommended groups contain two students; use three only when equipment is limited. Rotate roles across build sessions:

- **power/safety lead:** controls energizing and shutdown;
- **measurement lead:** predicts, names reference points, and records values;
- **code/test lead:** runs tests and records program state;
- **documentation lead:** captures approved evidence and updates the shared plan.

Roles organize work but do not define marks. Every student must explain the complete system, submit an individual reflection, and provide identifiable evidence of design, code/testing, measurement, troubleshooting, and communication.

## Teacher decisions required before release

- Actual class length and altered-timetable dates.
- Number, model, image, power supply, and verified condition of BeagleBones.
- Available meters, breadboards, relay sockets, transistor/MOSFET drivers, flyback diodes, lamps, buzzers, fuses, and protected supplies.
- Whether a real automotive horn can be used under school noise and safety expectations.
- Approved display-name and publishing rules for portfolios.
- Whether the semester assessment is an exam, interview, practical, portfolio review, or combination.
- Budget ceiling and whether any student-selected parts can be purchased.
