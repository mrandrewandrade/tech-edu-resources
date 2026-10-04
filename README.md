# Technological Education Resources

Open educator-first resources supporting the Ontario Technological Education curriculum, including reusable presentations, teaching materials, General Design & Fabrication curriculum, TEJ notes, and current TAS and TEJ class slides.

Live site: https://andrewandrade.ca/tech-edu-resources/

## Build and check

Install Quarto, Python 3.11+, Node.js, and the Python requirements.

```sh
python -m pip install -r requirements.txt
quarto render site
python scripts/check_commons.py --rendered
```

For editing:

```sh
quarto preview site
```

The rendered output is `site/_site`. Do not edit generated output directly.

## Current public structure

- `site/slides/tas.qmd`: chronological TAS class slides.
- `site/slides/tej.qmd`: chronological TEJ class slides.
- `site/design-fabrication/`: reusable General Design & Fabrication curriculum covering the N.I.C.E. design process, digital design, laser cutting, 3D printing, and planned fabrication methods.
- `site/tas2/`: compatibility redirects and retired TAS course scaffolding; reusable curriculum is canonical under `site/design-fabrication/`.
- `site/tej3-4/`: intentionally unfinished TEJ collaborative notes.
- `site/teacher-slides/`: General Slides, searchable reusable presentations.
- `site/teaching-materials/`: General Materials, searchable assignments, worksheets, and worked examples.
- `site/teaching-materials/laser-cutting/`: manifest-driven laser fabrication catalogue synced from `mrandrewandrade/assets`.
- `site/lore/`: stories, reflections, investigations, and design-process examples.
- `site/about.qmd`: project purpose, attribution, influences, Port Credit history, and TER visual identity.
- `site/assets/`: site styling, scripts, images, icons, branding, and the canonical published teaching PDFs/DOCX files under `site/assets/materials/`.
- `glossary/glossary.json`: retained glossary source used by internal tooling.

## Design principle

The current course notes are intentionally incomplete. They should record classroom learning as it happens rather than pretend the future sequence is already known.

A guiding idea is **Kinoo'amaadawaad Megwaa Doodamawaad**, translated by Paul Cormier as “they are learning with each other while they are doing.”

## Attribution and licensing

Original educational content uses CC BY-SA 4.0. Original project code and executable materials use AGPL-3.0-only.

When adapting educational resources, keep the work under **CC BY-SA 4.0**, identify changes, and preserve attribution to **andrewandrade.ca** and **github.com/mrandrewandrade**. Add your own name, website, repository, or links so later versions can credit your contribution too. **Sharing is caring.**

Legacy and third-party attribution is retained in `THIRD_PARTY_NOTICES.md` and the repository licence files.

## Laser library snapshot

The canonical generators, fabrication SVGs, metadata, validation and download bundle live in the sibling `mrandrewandrade/assets` repository. This repository commits the public catalogue manifest and lightweight preview snapshot used by the searchable teaching page. To refresh it from a local assets checkout:

```sh
python scripts/laser_library.py sync ../assets/laser/generated/catalog.json
python scripts/laser_library.py validate
```

The ordinary site pre-render validates the snapshot so missing previews, duplicate IDs and stale category counts fail the build.

See `LICENSE.md`, `LICENSES/`, `THIRD_PARTY_NOTICES.md`, and `site/licensing.qmd`.
