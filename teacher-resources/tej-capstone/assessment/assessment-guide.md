# TEJ Capstone Assessment Guide

## Purpose

Use a body of evidence to determine what each student knows and can do in design, electronics, Linux/Python, testing, troubleshooting, revision, and technical communication. The final device is one source of evidence, not the sole source and not a proxy for individual achievement.

## Evidence model

Collect evidence through:

- **observations:** meter setup, power-off inspection, safe energizing, terminal use, coding/testing habits, troubleshooting process, team participation;
- **conversations:** design approval, mid-build conference, transfer questions, final explanation, response to unexpected evidence; and
- **products:** schematic, BOM, calculations, code/tests, measurement table, design log, demonstration, portfolio, and reflection.

Triangulation is useful because a polished team product can conceal individual gaps, while an untidy or partly unsuccessful product can conceal strong understanding.

## Suggested checkpoint sequence

| Checkpoint | Timing | Evidence | Status/action |
|---|---|---|---|
| Readiness/catch-up conference | Nov. 23–27 | Existing work, meter demonstration, completion plan | Ready / repair / alternate evidence |
| Portfolio shell | By Dec. 18 | Local render or approved alternative, privacy check, one project draft | Complete / revise |
| Project approval | By Dec. 18 | Problem, schematic, BOM, ratings, tests, fallback | Approved / revise / supported fallback |
| Platform/code check | Jan. 4–8 | Linux/Python environment, safe startup, hardware-independent or GPIO test | Ready to build / continue simulator |
| Mid-build conference | Jan. 11–15 | Individual explanation, voltage evidence, fault hypothesis | Continue / narrow scope / targeted evidence |
| Demonstration and portfolio | Jan. 18–26 | Controlled demo or diagnostic walkthrough, final evidence, reflection | Final body of evidence |

## Criteria and evidence sources

| Criterion | Useful observation | Useful conversation | Useful product |
|---|---|---|---|
| Design and schematic | Student checks topology before wiring | Explains source, control, protection, driver, load, return | Approved diagram, criteria, BOM |
| Safe construction | Power-off checks and controlled energizing | Explains current limiting, fusing, GPIO boundary | Approval sheet, inspection record |
| Linux/Python | Uses terminal, runs tests, stops program safely | Explains program states and error evidence | Source code, test output, log |
| Measurements/reasoning | Selects meter setup and named reference points | Interprets sign, range, KVL/KCL or other model | Prediction and measurement table |
| Troubleshooting | Isolates one variable and retests | Explains what a result rules in/out | Fault/correction record |
| Revision/judgement | Freezes scope and chooses informative tests | Explains trade-off and limitation | Before/evidence/after comparison |
| Communication/portfolio | Selects useful, privacy-safe evidence | Answers audience questions | Rendered portfolio, captions, citations |
| Individual accountability | Performs assigned and shared tasks | Explains complete system and own contribution | Individual log, code/test entries, reflection |

## Achievement-chart relationship

Use professional judgement rather than mechanically averaging eight numbers.

- **Knowledge/Understanding:** circuit concepts, component roles/ratings, Linux/Python concepts.
- **Thinking:** problem definition, test planning, troubleshooting, interpretation, revision.
- **Communication:** schematic conventions, tables/units, explanations, portfolio organization, citations.
- **Application:** safe construction, meter use, code execution, interface implementation, transfer to a new fault or question.

The student rubric’s eight criteria deliberately supply evidence across these four categories. If a locally required category weighting applies, use it when recording the final task result; do not change the performance descriptions merely to produce a desired arithmetic total.

## Individual accountability in team projects

Use teams for access to limited equipment, not as a single assessment identity.

Require each student to:

1. own identifiable design-log/code/test entries;
2. take a turn in safety/power, measurement, code/test, and documentation roles where practical;
3. explain the entire input-control-driver-load-return system;
4. complete at least one voltage/circuit-reasoning check;
5. explain one fault and what the evidence ruled in/out;
6. answer one transfer question individually; and
7. submit an individual reflection/portfolio attribution.

When individual understanding is unclear, schedule a five-minute conference or diagnostic task. Do not infer equal achievement from a shared demonstration.

## When the circuit is partly unsuccessful

Do not reduce achievement automatically because the final load does not operate. Determine whether the student provides valid evidence such as:

- an approved and substantially correct schematic;
- safe staged construction and inspection;
- realistic predictions with units and ratings;
- valid voltage measurements at named points;
- passing hardware-independent Python tests;
- a fault tree or logical diagnostic sequence;
- a test that isolates the failed interface/component;
- a controlled substitution or simulator comparison;
- an evidence-based revision;
- a precise explanation of what remains unknown; and
- a defensible next test.

Likewise, do not assign high achievement merely because a team’s device works once. Ask the student to explain and reproduce the evidence.

## Equipment failure versus student learning

Record equipment limitations separately. If a BeagleBone, meter, relay, supply, or component fails:

1. preserve the diagnosis as evidence;
2. substitute equipment if available;
3. continue Python tests with a hardware-independent adapter;
4. use teacher-provided measurements/reference hardware for interpretation;
5. use a diagnostic walkthrough if physical construction time is no longer reasonable.

The alternate evidence must address the same intended learning, not become unrelated make-work.

## Late, absent, and interrupted work

- Use the design log to identify evidence completed before the interruption.
- Let an absent student use approved team photographs/data, clearly identifying which observations were made by others.
- Collect individual explanation and analysis after return.
- Use January 25–26 for missed demonstrations or conversations.
- Reduce the feature set before extending a deadline into assessment days.

## Recommended evidence record

For every criterion, record:

- date;
- evidence source (observation, conversation, product);
- concise description of demonstrated learning;
- provisional level or feedback;
- next required evidence where needed.

Avoid comments such as “participated” or “worked well.” Record observable technical evidence: “named COM as the voltage reference, selected V DC, predicted 3.2 V across R1, measured 3.18 V, and explained the difference.”

## Teacher decisions before use

- Local achievement-chart/category weighting.
- Role of this task in the final course grade.
- Format of semester assessment from January 27–February 2.
- Whether portfolios are public, private, or locally rendered.
- Approved accommodations and alternate formats.
- Whether a real automotive horn is permitted and under what noise controls.
