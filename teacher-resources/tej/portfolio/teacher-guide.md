# TEJ Grade 11 semester portfolio — teacher guide

## Purpose

Assign the portfolio before winter break so students have a working evidence
container before the integrated Linux/Python/circuit project begins. The site is
both a technical product and a documentation routine; it should not become a
separate web-design unit that displaces the circuit work.

## Suggested checkpoints

### Before winter break

- successful local render;
- teacher-approved title and identity language;
- selected Quarto profile and colour palette;
- one draft based on completed course work;
- source-folder and privacy check.

Assess this checkpoint formatively. Correct broken setup before January.

### January project

Require short evidence additions at existing project gates: problem/criteria,
schematic, state model, prediction, first test, fault, revision, conclusion. This
prevents an end-of-project documentation rush and makes troubleshooting visible.

### Final two weeks

Students select their strongest project, improve incomplete evidence, test the
site, and complete a short portfolio tour. Avoid rewarding the number of pages.

## Assessment evidence

Use observations, conversations, source files, rendered pages, demonstration,
and revision history. A non-working final device can still demonstrate strong
achievement when the student designed safely, isolated faults logically,
collected valid evidence, and communicates the remaining limitation.

## Profiles

The starter includes mutually exclusive `core`, `blog`, `skills`, and `full`
profiles. `core` is a suitable minimum. The Learning Log and Skills page should
be enabled only when they contain meaningful evidence. Test profile behaviour
with:

```sh
quarto render --profile core
quarto render --profile full
```

## Privacy and publishing

Public publishing is never required. GitHub Pages is a public publishing path,
not private classroom storage. Review images and repository history as well as
visible text. If credentials or confidential information appear, revoke or
report them through the approved process; unpublishing alone is not remediation.

## Differentiation

Accept the same engineering-story headings in a private document or Markdown
folder when a student cannot use the Quarto CLI. A partner may assist with setup,
but each student needs individually attributable explanation and evidence.

## ZIP integration note

After this branch is merged and validated, rebuild
`site/assets/tej-portfolio/quarto-portfolio-starter.zip` with the repository's
existing computational-resource build pipeline. The branch intentionally does
not refresh the final ZIP.
