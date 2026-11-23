# Student-Designed Project — Approval Guide

## Approval principle

Approve the smallest version that produces meaningful Linux/Python, circuit, measurement, and troubleshooting evidence. A novel idea does not justify an unsafe interface or an unfinishable scope.

## Gate 1: problem and scope

- Is the result observable and testable?
- Can the minimum version be completed with current class time?
- Are four to six success criteria measurable?
- Does the project contain a real input decision and output response?
- Is the extension clearly separated from the minimum?

## Gate 2: availability and budget

- Are core parts physically in stock or reserved?
- Are substitutes electrically compatible?
- Is shipping excluded from the critical path?
- Is there a classroom-stock fallback?
- Has no purchase been made before approval?

## Gate 3: electrical compatibility

Reject or return for revision when:

- the exact part/module is unknown;
- GPIO/ADC voltage is unspecified;
- a 5 V output or pull-up might reach 3.3 V GPIO;
- a high-current/inductive load lacks a driver and protection;
- source current limiting/fusing is absent;
- grounds or isolation are unexplained;
- a package drawing is used as a pinout without documentation.

## Gate 4: evidence plan

The proposal must name:

- calculations and assumptions;
- test points and expected voltages;
- software-only test;
- input-only test;
- output/driver-only test;
- boundary and prepared-fault test;
- safe power-up/shutdown test;
- exact portfolio evidence.

## Scope decision

| Decision | Meaning |
|---|---|
| Revise | Missing evidence or unsafe/unbounded design |
| Approved for documentation | Research, calculations, and simulation only |
| Approved for unpowered build | Placement/wiring may begin; no source connected |
| Approved for staged power-up | Only the named subsystem may be energized |
| Approved for integration | Minimum subsystems have passed separately |

Record conditions directly on the proposal. Approval for one gate does not imply approval for the next.

## Suggested limits

- Use protected extra-low voltage.
- Keep one controller and one primary sensor in the minimum scope.
- Use low-current LED/buzzer outputs before relay/motor loads.
- Require a working simulator/keyboard mode when hardware is scarce.
- Treat cloud services, cameras, microphones, real security data, and public network exposure as out of scope unless separately reviewed.
