# Capstone Conference Prompts

Use a small selection, not every question. Ask follow-ups that require the student to point to evidence.

## Proposal and schematic

- What exactly must the system do to count as successful?
- Trace the path from source to protection, control, load, and return.
- Which line is a signal and which path carries load current?
- Which rating or pinout did you have to verify from a datasheet?
- What would you remove first if time or parts became limited?

## Linux and Python

- What command or evidence confirms the environment you are using?
- What state is the program in immediately after startup, and why is that safe?
- Show one test that does not require the physical hardware.
- What input causes a state change? Where is that represented in code?
- What error or failed test gave you the most useful information?

## Measurements and reasoning

- Name both points used for this voltage measurement.
- What do you predict before connecting the meter?
- Which KVL loop or KCL node are you checking?
- Is the sign/value reasonable? What would an open circuit or poor ground show here?
- How could the meter reading be correct but your conclusion still be wrong?

## Troubleshooting

- What is the symptom, and what should happen instead?
- What are your two most likely hypotheses?
- Which one safe test distinguishes them?
- What did the result rule in or out?
- Did your correction solve the original symptom when retested?

## Revision and scope

- What changed because of evidence rather than preference?
- What trade-off did you accept?
- What feature should you stop adding now?
- What limitation remains in the demonstration?
- What is the next most informative test?

## Individual contribution

- Show a design-log, code, calculation, test, or documentation entry you own.
- Explain a section completed by your teammate.
- If you worked alone tomorrow, what step could you perform independently?
- Which safety decision is everyone on the team responsible for?

## Transfer questions

- If the supply voltage fell, which observations would change first?
- If the ground opened, what voltage might appear at the load side?
- If the relay clicks but the lamp stays off, which circuit do you test first?
- If the input changes in Linux but the output does not, where is the boundary between software and hardware?
- If the hardware is unavailable, what equivalent evidence can still test the program logic?
