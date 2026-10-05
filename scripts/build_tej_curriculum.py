from __future__ import annotations

import html
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = REPO_ROOT / "site" / "data" / "tej-curriculum.yml"
OUTPUT_PATH = REPO_ROOT / "site" / "tej3-4" / "curriculum" / "index.qmd"

REQUIRED_RECORD_FIELDS = {
    "short_description",
    "status",
    "pathway",
    "prerequisites",
    "estimated_time",
    "simulation_requirement",
    "physical_lab_requirement",
    "equipment",
    "software",
    "safety_level",
    "student_deliverables",
    "assessment_evidence",
    "public_notes_route",
    "student_handout",
    "teacher_guide",
    "slides",
    "source_references",
    "access_level",
    "copyright_permissions_note",
    "implementation_notes",
}

ALLOWED_STATUSES = {
    "Published",
    "Pilot",
    "In development",
    "Planned",
    "Bonus",
    "Restricted source",
}
ALLOWED_ACCESS = {
    "Public",
    "Teacher only",
    "Classroom restricted",
    "External official source",
}
ALLOWED_PATHWAYS = {"core", "extension", "side quest", "bonus"}


def as_list(value: Any) -> list[str]:
    if value in (None, "", []):
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def display_list(value: Any, empty: str = "None") -> str:
    items = as_list(value)
    return ", ".join(html.escape(item) for item in items) if items else empty


def validate_record(record: dict[str, Any], identity: str) -> None:
    missing = sorted(REQUIRED_RECORD_FIELDS - set(record))
    if missing:
        raise ValueError(f"{identity} is missing required fields: {', '.join(missing)}")
    if record["status"] not in ALLOWED_STATUSES:
        raise ValueError(f"{identity} has invalid status: {record['status']}")
    if record["access_level"] not in ALLOWED_ACCESS:
        raise ValueError(f"{identity} has invalid access level: {record['access_level']}")
    if str(record["pathway"]).lower() not in ALLOWED_PATHWAYS:
        raise ValueError(f"{identity} has invalid pathway: {record['pathway']}")


def link_or_text(label: str, value: Any) -> str:
    text = str(value or "Not yet available")
    if text.startswith("http://") or text.startswith("https://"):
        return f"[{html.escape(label)}]({text})"
    if text.endswith(".qmd"):
        route = "../" + text.removeprefix("tej3-4/") if text.startswith("tej3-4/") else "../../" + text
        return f"[{html.escape(label)}]({route})"
    return f"**{html.escape(label)}:** {html.escape(text)}"


def effective_modules(unit: dict[str, Any]) -> list[dict[str, Any]]:
    defaults = dict(unit.get("module_defaults", {}))
    result: list[dict[str, Any]] = []
    for module in unit.get("modules", []):
        merged = {**defaults, **module}
        merged["unit_id"] = str(unit["unit_id"])
        validate_record(merged, f"module {merged.get('module_id', '<unknown>')}")
        result.append(merged)
    return result


def render_module(module: dict[str, Any]) -> str:
    status_slug = str(module["status"]).lower().replace(" ", "-")
    pathway_slug = str(module["pathway"]).lower().replace(" ", "-")
    access_slug = str(module["access_level"]).lower().replace(" ", "-")
    search_terms = " ".join(
        [
            str(module["module_id"]),
            str(module["title"]),
            str(module["short_description"]),
            *as_list(module["equipment"]),
            *as_list(module["software"]),
        ]
    )
    notes = str(module["public_notes_route"] or "Not yet available")
    if notes.endswith(".qmd"):
        notes_markup = link_or_text("Public notes", notes)
    else:
        notes_markup = f"**Public notes:** {html.escape(notes)}"
    return f"""
<article class="tej-roadmap-module" data-tej-roadmap-module data-status="{status_slug}" data-pathway="{pathway_slug}" data-access="{access_slug}" data-search="{html.escape(search_terms, quote=True)}">
<div class="tej-roadmap-module-heading">
<h3>{html.escape(str(module['module_id']))}: {html.escape(str(module['title']))}</h3>
<div><span class="tej-badge status-{status_slug}">{html.escape(str(module['status']))}</span> <span class="tej-badge">{html.escape(str(module['pathway']).title())}</span> <span class="tej-badge">{html.escape(str(module['access_level']))}</span></div>
</div>
<p>{html.escape(str(module['short_description']))}</p>
<details>
<summary>Requirements, evidence, and implementation notes</summary>

| Field | Roadmap record |
|:--|:--|
| Prerequisites | {display_list(module['prerequisites'])} |
| Estimated time | {html.escape(str(module['estimated_time']))} |
| Simulation | {html.escape(str(module['simulation_requirement']))} |
| Physical lab | {html.escape(str(module['physical_lab_requirement']))} |
| Equipment | {display_list(module['equipment'])} |
| Software | {display_list(module['software'])} |
| Safety level | {html.escape(str(module['safety_level']))} |
| Student deliverables | {display_list(module['student_deliverables'])} |
| Assessment evidence | {display_list(module['assessment_evidence'])} |
| Student handout | {html.escape(str(module['student_handout']))} |
| Teacher guide | {html.escape(str(module['teacher_guide']))} |
| Slides | {html.escape(str(module['slides']))} |
| Source references | {display_list(module['source_references'])} |
| Copyright or permissions | {html.escape(str(module['copyright_permissions_note']))} |
| Implementation notes | {html.escape(str(module['implementation_notes']))} |

{notes_markup}
</details>
</article>
""".strip()


def render_unit(unit: dict[str, Any]) -> str:
    unit_id = str(unit["unit_id"])
    validate_record(unit, f"unit {unit_id}")
    modules = effective_modules(unit)
    module_markup = "\n\n".join(render_module(module) for module in modules)
    return f"""
## {html.escape(unit_id)}. {html.escape(str(unit['title']))} {{#unit-{unit_id.replace('.', '-')}}}

<div class="tej-roadmap-unit-summary">
<p><span class="tej-badge status-{str(unit['status']).lower().replace(' ', '-')}">{html.escape(str(unit['status']))}</span> <span class="tej-badge">{html.escape(str(unit['pathway']).title())}</span> <span class="tej-badge">{html.escape(str(unit['access_level']))}</span></p>
<p>{html.escape(str(unit['short_description']))}</p>

| Unit field | Roadmap record |
|:--|:--|
| Prerequisites | {display_list(unit['prerequisites'])} |
| Estimated time | {html.escape(str(unit['estimated_time']))} |
| Simulation | {html.escape(str(unit['simulation_requirement']))} |
| Physical lab | {html.escape(str(unit['physical_lab_requirement']))} |
| Equipment | {display_list(unit['equipment'])} |
| Software | {display_list(unit['software'])} |
| Safety level | {html.escape(str(unit['safety_level']))} |
| Student deliverables | {display_list(unit['student_deliverables'])} |
| Assessment evidence | {display_list(unit['assessment_evidence'])} |
| Student handout | {html.escape(str(unit['student_handout']))} |
| Teacher guide | {html.escape(str(unit['teacher_guide']))} |
| Slides | {html.escape(str(unit['slides']))} |
| Source references | {display_list(unit['source_references'])} |
| Copyright or permissions | {html.escape(str(unit['copyright_permissions_note']))} |
| Implementation notes | {html.escape(str(unit['implementation_notes']))} |

{link_or_text('Public notes', unit['public_notes_route'])}
</div>

<div class="tej-roadmap-module-grid">
{module_markup}
</div>
""".strip()


def render_sources(sources: list[dict[str, Any]]) -> str:
    rows = []
    for source in sources:
        access = html.escape(str(source["access_level"]))
        url = str(source.get("url", ""))
        title = html.escape(str(source["title"]))
        title_markup = f"[{title}]({url})" if url.startswith("http") else title
        rows.append(
            f"| {html.escape(str(source['source_id']))} | {title_markup} | {html.escape(str(source['use']))} | {access} | {html.escape(str(source['copyright_permissions_note']))} |"
        )
    return "\n".join(rows)


def build_page(data: dict[str, Any]) -> str:
    units = data.get("units", [])
    if not units:
        raise ValueError("Curriculum metadata contains no units")
    unit_ids = [str(unit["unit_id"]) for unit in units]
    if len(unit_ids) != len(set(unit_ids)):
        raise ValueError("Curriculum unit IDs must be unique")
    module_ids: list[str] = []
    for unit in units:
        validate_record(unit, f"unit {unit.get('unit_id', '<unknown>')}")
        module_ids.extend(str(module["module_id"]) for module in effective_modules(unit))
    if len(module_ids) != len(set(module_ids)):
        raise ValueError("Curriculum module IDs must be unique")

    unit_links = "\n".join(
        f"- [{html.escape(str(unit['unit_id']))}. {html.escape(str(unit['title']))}](#unit-{str(unit['unit_id']).replace('.', '-')})"
        for unit in units
    )
    unit_markup = "\n\n".join(render_unit(unit) for unit in units)
    source_rows = render_sources(data.get("sources", []))
    return f"""---
title: "TEJ Curriculum Roadmap"
description: "The complete TEJ learning pathway with honest Published, Pilot, In development, Planned, Bonus, and Restricted source labels."
categories: [TEJ, curriculum roadmap, electronics, fabrication, computer systems, Linux, programming, microcontrollers, networking, machine learning, artificial intelligence]
sidebar: tej
page-layout: full
toc: true
toc-depth: 2
execute: {{enabled: false}}
format:
  html:
    include-after-body:
      - ../../includes/tej-curriculum-script.html
---

::: {{.callout-note title="In Development"}}
This is a working plan for the complete TEJ learning pathway. It will take time to make every module publicly available while classroom resources, citations, permissions, diagrams, accessibility, handouts, and source files are cleaned up. **Published** modules are ready to use. **Pilot** modules are being tested. **Planned** modules show the intended sequence.
:::

This page is generated from [`site/data/tej-curriculum.yml`](https://github.com/mrandrewandrade/tech-edu-resources/blob/codex/tej-electronics-library/site/data/tej-curriculum.yml). It contains curriculum-only information. It does not expose the teacher planning workbook, student numbers, aliases, scores, private notes, restricted Drive links, or teacher-only tracking tools.

## Status and access

- **Published:** a public classroom resource is available and ready to use.
- **Pilot:** a resource is being tested and may change.
- **In development:** active authoring or verification is underway.
- **Planned:** the module belongs in the intended sequence, but its classroom package is not complete.
- **Bonus:** optional enrichment or a specialized pathway.
- **Restricted source:** a source may be available through the teacher but is not redistributed publicly.

Access is recorded as **Public**, **Teacher only**, **Classroom restricted**, or **External official source**. A public roadmap record does not make a restricted source public.

<div class="tej-roadmap-filter-row" data-tej-roadmap-filters aria-label="Filter the TEJ curriculum roadmap">
  <label>Search <input type="search" data-tej-roadmap-search placeholder="Try soldering, Linux, Python, GPIO, machine learning, or CNC"></label>
  <label>Status <select data-tej-roadmap-status><option value="all">All statuses</option><option value="published">Published</option><option value="pilot">Pilot</option><option value="in-development">In development</option><option value="planned">Planned</option><option value="bonus">Bonus</option><option value="restricted-source">Restricted source</option></select></label>
  <label>Pathway <select data-tej-roadmap-pathway><option value="all">All pathways</option><option value="core">Core</option><option value="extension">Extension</option><option value="side-quest">Side quest</option><option value="bonus">Bonus</option></select></label>
  <label>Access <select data-tej-roadmap-access><option value="all">All access levels</option><option value="public">Public</option><option value="teacher-only">Teacher only</option><option value="classroom-restricted">Classroom restricted</option><option value="external-official-source">External official source</option></select></label>
</div>

<p class="tej-roadmap-result-count" data-tej-roadmap-count aria-live="polite"></p>

## Full progression

{unit_links}

<div data-tej-roadmap>
{unit_markup}
</div>

<p class="tej-roadmap-empty" data-tej-roadmap-empty hidden>No curriculum modules match these filters.</p>

## Source register

The roadmap uses original summaries and links to official or appropriately licensed sources. Copyrighted textbooks, teacher copies, source scans, and materials not cleared for redistribution remain outside the public repository.

<div class="tej-roadmap-table-scroll">

| Source ID | Source | Roadmap use | Access | Copyright or permissions note |
|:--|:--|:--|:--|:--|
{source_rows}

</div>

## Remaining implementation backlog

Planned records still need lesson pages, verified citations, original diagrams, accessible handouts, teacher guides, slides, equipment checks, permissions review, and classroom testing. The status field must be updated only when that evidence exists.
"""


def main() -> int:
    data = yaml.safe_load(DATA_PATH.read_text(encoding="utf-8"))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(build_page(data), encoding="utf-8", newline="\n")
    print(f"Generated {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
