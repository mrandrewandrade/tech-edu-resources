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
        merged = {
            "consumables": unit.get("consumables", []),
            **defaults,
            **module,
        }
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
</div>
<p>{html.escape(str(module['short_description']))}</p>
<details>
<summary>Materials, deliverables, and notes</summary>

| What is needed | Details |
|:--|:--|
| Equipment | {display_list(module['equipment'])} |
| Software | {display_list(module['software'])} |
| Consumables | {display_list(module.get('consumables'), 'No special consumables')} |
| Student deliverables | {display_list(module['student_deliverables'])} |
| Teacher notes | {html.escape(str(module['implementation_notes']))} |

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
<p>{html.escape(str(unit['short_description']))}</p>

| What is needed | Unit overview |
|:--|:--|
| Equipment | {display_list(unit['equipment'])} |
| Software | {display_list(unit['software'])} |
| Consumables | {display_list(unit.get('consumables'), 'No special consumables')} |
| Student deliverables | {display_list(unit['student_deliverables'])} |
| Teacher notes | {html.escape(str(unit['implementation_notes']))} |

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
description: "The complete TEJ learning pathway in teaching order, with topics, materials, software, consumables, deliverables, and notes."
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

::: {{.callout-note title="How to use this roadmap"}}
Follow the units and modules in order. Each section states what students will learn or do, what equipment, software, and consumables are needed, what students submit, and any useful teacher notes.
:::

The sequence is a planning guide. Adjust individual activities to the available equipment and the students in the class.

## Full progression

{unit_links}

<div data-tej-roadmap>
{unit_markup}
</div>

"""


def main() -> int:
    data = yaml.safe_load(DATA_PATH.read_text(encoding="utf-8"))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        build_page(data).rstrip() + "\n", encoding="utf-8", newline="\n"
    )
    print(f"Generated {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
