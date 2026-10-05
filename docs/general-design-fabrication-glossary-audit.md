# General Design & Fabrication glossary audit

Audit date: 2026-10-04

## Scope and result

The audit compared vocabulary taught across `site/design-fabrication/` with the canonical entries in `glossary/glossary.json`. It reviewed 189 candidate concepts from the active curriculum and project resources.

- 174 new canonical entries were added.
- 2 existing entries were reused and improved with sources: `engineering-design-process` and `nice-design-process`.
- 13 candidates were intentionally not made separate canonical entries.
- 71 aliases were added to the new entries.
- 24 authoritative sources were added to the central IEEE-numbered reference system.

## Added term families

| Family | New canonical entries |
|---|---:|
| Design Process | 18 |
| AI & Digital Literacy | 20 |
| Digital Design & Media | 30 |
| Web & UI/UX | 16 |
| CAD & Technical Drawing | 28 |
| 3D Printing | 19 |
| Fabrication & Manufacturing | 43 |
| **Total** | **174** |

## Candidates not added as separate entries

Onshape, Blender, Pencil2D, Inkscape, and Photopea remain searchable through relevant technical definitions instead of becoming brand-only glossary entries. Alpha channel, tween/interpolation, mesh normal, G-code, load path, pin, 2D animation, and 3D animation were not explicit enough in the current lessons to justify separate entries. They can be reconsidered when a lesson directly teaches the distinction.

## Taxonomy changes

The existing `Design Process` category was retained. Six coherent categories were added:

- AI & Digital Literacy
- Digital Design & Media
- Web & UI/UX
- CAD & Technical Drawing
- Fabrication & Manufacturing
- 3D Printing

Existing electrical, measurement, notation, and legacy glossary categories remain unchanged.

## Integration decisions

Broad lesson relationships use `terms`. Only selected first-use concepts use `highlighted-terms`, preventing dense or repetitive inline highlighting. The General Design & Fabrication directory enables the existing inline-glossary filter so highlighted vocabulary opens the shared canonical definitions.

Every entry added by this expansion has at least one `references` item. Tests enforce source coverage, reference-key resolution, stable reference numbers, alias ownership, related-term resolution, deterministic generation, and curriculum metadata resolution.
