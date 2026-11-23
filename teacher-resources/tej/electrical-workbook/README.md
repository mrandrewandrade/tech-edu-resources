# Electrical diagrams and printable investigation package

This folder contains teacher keys, calculation checks, print styling, rendered
PDFs, and the visual QA record for the automotive relay, capacitor-sound, and
fault-card investigations.

Student sources live in `site/assets/electronics/worksheets/`. Canonical SVG
diagrams live in `site/assets/electronics/schematics/`. Do not edit the rendered
PDFs directly.

See [SOURCES.md](SOURCES.md) for the textbook/manufacturer references and the
adaptation record. All SVGs and questions in this package are original. The
sources were used to check conventions and limits, not as artwork to trace.

The automotive calculations deliberately use an ideal steady-state model. The
21 W incandescent lamps are treated as rated 12 V loads. Only the poor-ground
calculation converts the rated lamp to a fixed hot resistance, and the student
page states that assumption. Real cold-filament current, relay contact drop,
horn current, coil resistance, and supply voltage must be measured from the
actual classroom parts before a physical build.

The capacitor student circuit uses only protected 5 V. The automotive horn is a
teacher-only extension powered by a separately fused supply. Its capacitor
question is an engineering estimate, not a physical instruction to connect a
large capacitor directly across a horn.
