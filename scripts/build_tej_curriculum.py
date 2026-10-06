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

ROADMAP_WHY = {
    "0": "Safe, documented work is the foundation for every build, investigation, and engineering decision.",
    "1": "Units, scale, estimation, and calculator fluency make technical results understandable and trustworthy.",
    "2": "These quantities explain how electrical systems transfer energy and why components behave as they do.",
    "3": "Circuit analysis turns schematics into predictions that can be checked by simulation and measurement.",
    "4": "Readable schematics, careful construction, and correct measurement make troubleshooting possible.",
    "5": "Component knowledge lets students select, connect, protect, and test useful electronic circuits.",
    "6": "Stable inputs and Boolean logic connect physical switches and sensors to dependable digital decisions.",
    "7": "Fabrication turns a tested design into a durable, repeatable physical product.",
    "8": "Computer hardware work connects electrical principles to real systems, maintenance, repair, and reuse.",
    "9": "Operating-system knowledge gives students control over files, software, permissions, and system behaviour.",
    "10": "Programming turns a process or calculation into a repeatable tool that can handle inputs and errors.",
    "11": "Physical computing joins code, sensors, outputs, timing, and electrical protection in one system.",
    "12": "Networking explains how devices communicate and how small services are operated safely.",
    "13": "Data science helps students turn measurements into evidence while recognizing uncertainty and bias.",
    "14": "Understanding language models helps students use, test, and evaluate artificial intelligence responsibly.",
    "15": "A culminating project combines design, construction, programming, testing, revision, and communication.",
    "16": "Control systems show how sensing, decisions, and feedback produce safe, useful machine behaviour.",
}

ROADMAP_OUTCOMES = {
    "0": "Work safely, document decisions, cite sources, and keep a usable design record.",
    "1": "Convert technical quantities, use engineering notation, estimate results, and present calculations clearly.",
    "2": "Explain and calculate voltage, current, resistance, power, energy, opens, shorts, and source behaviour.",
    "3": "Solve and verify series, parallel, and mixed circuits and diagnose common faults.",
    "4": "Build from a schematic, measure safely, compare predicted and measured values, and locate wiring errors.",
    "5": "Design and test sensor, timing, switching, power-supply, and actuator-interface circuits.",
    "6": "Build stable switch inputs, complete truth tables, analyze logic, and create a small digital system.",
    "7": "Prepare a manufacturable design and produce a soldered, printed, laser-cut, or machined result.",
    "8": "Identify, assemble, commission, benchmark, troubleshoot, upgrade, and document a computer.",
    "9": "Install and use Linux, manage files and permissions, run commands, and complete basic administration.",
    "10": "Write, test, debug, and document programs that calculate, model, process data, or control a task.",
    "11": "Create a protected sensor-and-actuator system using a microcontroller or single-board computer.",
    "12": "Configure and diagnose a small network or classroom service using defensive administration practices.",
    "13": "Clean, visualize, model, and evaluate a non-personal dataset and explain the limits of the result.",
    "14": "Build or evaluate a small grounded artificial-intelligence application with documented tests and limits.",
    "15": "Deliver a working or simulated technology project supported by evidence, revision, and a technical explanation.",
    "16": "Model or build a feedback-controlled system with safe states, interlocks, and measured response.",
}


def as_list(value: Any) -> list[str]:
    if value in (None, "", []):
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


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


def render_unit(unit: dict[str, Any]) -> str:
    unit_id = str(unit["unit_id"])
    validate_record(unit, f"unit {unit_id}")
    modules = effective_modules(unit)
    subsections: list[str] = []
    for module in modules:
        title = str(module["title"])
        route = str(module.get("public_notes_route", ""))
        if route.endswith(".qmd"):
            subsections.append(link_or_text(title, route))
        else:
            subsections.append(html.escape(title))
    subsection_markup = "; ".join(subsections)
    why = ROADMAP_WHY[unit_id]
    outcome = ROADMAP_OUTCOMES[unit_id]
    return f"""
## {html.escape(unit_id)}. {html.escape(str(unit['title']))} {{#unit-{unit_id.replace('.', '-')}}}

| What students learn | Why it matters |
|:--|:--|
| {html.escape(str(unit['short_description']))} | {html.escape(why)} |

**Subsections:** {subsection_markup}

**Coming out of this section, students can:** {html.escape(outcome)}
""".strip()


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
    return f"""---
title: "TEJ Curriculum Roadmap"
description: "A concise guide to the TEJ learning pathway, major topics, and practical outcomes."
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

Use this page as a course map. Follow the sections in order, then use the TEJ sidebar to open lessons, reference notes, worksheets, labs, projects, and optional enhancements. Detailed implementation planning belongs in the teacher guide rather than on this public roadmap.

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
