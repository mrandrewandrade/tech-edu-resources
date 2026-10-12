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

ROADMAP_TITLES = {
    "0": "Orientation, Safety, and Design",
    "1": "Numbers, Units, and Calculator Skills",
    "2": "Electrical Fundamentals",
    "3": "DC Circuit Analysis",
    "4": "Building, Schematics, and Measurement",
    "5": "Components and Applied Circuits",
    "6": "Digital Logic and Inputs",
    "7": "Fabrication and PCBs",
    "8": "Computer Systems",
    "9": "Linux, Operating Systems and Basic Networking",
    "10": "Programming",
    "11": "Microcontrollers",
    "12": "Networking and Administration",
    "13": "Data Science and Machine Learning",
    "14": "Language Models and Applied AI",
    "15": "Culminating Projects",
    "16": "Control Systems and CNC",
}

ROADMAP_SUBSECTIONS = {
    "0": "Safety; design process; documentation; privacy and attribution",
    "1": "Number systems; units; significant figures; engineering notation; calculator workflow",
    "2": "Charge; voltage; current; resistance; sources and loads; AC and DC",
    "3": "Ohm's law; series circuits; parallel circuits; mixed networks; Kirchhoff's laws; linear systems; work, energy, power, and efficiency; dividers; troubleshooting",
    "4": "Breadboards; schematics; simulation; multimeter use; measurement uncertainty",
    "5": "Sensors; batteries; capacitors; diodes; transistors; timers; motors and relays",
    "6": "Logic levels; pull-ups and pull-downs; debouncing; logic gates; truth tables; state",
    "7": "Soldering; connectors; PCB design; manufacturing files; enclosures and fabrication",
    "8": "Components; power; assembly; startup; Linux installation; upgrades and troubleshooting",
    "9": "Desktop use; files and permissions; command line; software; basic networking; services; backup and recovery",
    "10": "Algorithms; variables; conditions; loops; functions; files; testing and debugging",
    "11": "Inputs and outputs; sensors; timing; communication; actuators; state machines; data logging",
    "12": "Addresses; protocols; diagnostics; secure remote access; services; users and backups",
    "13": "Data preparation; visualization; regression; classification; model evaluation; responsible use",
    "14": "Tokens; prediction; small models; prompting; grounding; evaluation; responsible use",
    "15": "Requirements; design; build or simulation; testing; revision; technical communication",
    "16": "Open and closed loop control; hysteresis; proportional control; PID; interlocks; motion and CNC",
}

ROADMAP_LEARNING = {
    "0": "Work safely, follow a design process, and document decisions and sources.",
    "1": "Use number systems, units, engineering notation, estimates, and a scientific calculator.",
    "2": "Explain and calculate charge, voltage, current, resistance, sources, and loads.",
    "3": "Analyze direct-current networks, solve their equations, and connect electrical energy to useful work.",
    "4": "Build readable circuits and compare calculated, simulated, and measured results.",
    "5": "Select and apply common components in useful low-voltage circuits.",
    "6": "Create stable digital inputs and analyze combinational and sequential logic.",
    "7": "Turn a tested prototype into a durable fabricated or manufactured result.",
    "8": "Assemble, commission, maintain, upgrade, and troubleshoot computer hardware.",
    "9": "Use and administer a Linux system safely from the desktop and command line.",
    "10": "Write, test, debug, and document programs for calculations, data, and control.",
    "11": "Connect code to protected sensors, inputs, outputs, communication, and actuators.",
    "12": "Explain networks and operate small classroom services using defensive practices.",
    "13": "Prepare, visualize, model, and evaluate non-personal data responsibly.",
    "14": "Explain, use, ground, and evaluate small language-model applications responsibly.",
    "15": "Plan, build or simulate, test, revise, and explain an integrated technology project.",
    "16": "Model or build systems that use sensing, decisions, feedback, and safe states.",
}

ROADMAP_WHY = {
    "0": "Safe, documented work is the foundation for every build, investigation, and engineering decision.",
    "1": "Units, scale, estimation, and calculator fluency make technical results understandable and trustworthy.",
    "2": "These quantities explain how sources, conductors, and loads behave in a complete circuit.",
    "3": "Circuit analysis predicts electrical behaviour; an energy-conversion lab shows what that behaviour accomplishes in a real device.",
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
    "2": "Explain and calculate charge, voltage, current, resistance, opens, shorts, and source behaviour.",
    "3": "Solve and verify series, parallel, and mixed networks, use linear equations, and compare electrical energy with mechanical work.",
    "4": "Build from a schematic, measure safely, compare predicted and measured values, and locate wiring errors.",
    "5": "Design and test sensor, timing, switching, power-supply, and actuator-interface circuits.",
    "6": "Build stable switch inputs, complete truth tables, analyze logic, and create a small digital system.",
    "7": "Prepare a manufacturable design and produce a soldered, printed, laser-cut, or machined result.",
    "8": "Identify, assemble, commission, benchmark, troubleshoot, upgrade, and document a computer.",
    "9": "Install and use Linux, manage files and permissions, run commands, check basic network settings and connectivity, and complete basic administration.",
    "10": "Write, test, debug, and document programs that calculate, model, process data, or control a task.",
    "11": "Create a protected sensor-and-actuator system using a microcontroller or single-board computer.",
    "12": "Configure and diagnose a small network or classroom service using defensive administration practices.",
    "13": "Clean, visualize, model, and evaluate a non-personal dataset and explain the limits of the result.",
    "14": "Build or evaluate a small grounded artificial-intelligence application with documented tests and limits.",
    "15": "Deliver a working or simulated technology project supported by evidence, revision, and a technical explanation.",
    "16": "Model or build a feedback-controlled system with safe states, interlocks, and measured response.",
}

ROADMAP_COLLABORATION = {
    "3": (
        "**Collaboration:** The [Engineering Preparation Track collaboration map]"
        "(../engineering-preparation-track/index.qmd#ontario-course-collaboration-opportunities) "
        "connects this work with TEJ3M/TEJ4M, SPH3U physics, SCH4U chemistry, and SBI4U biology."
    ),
}


# The YAML remains the detailed teacher/development source.  The public map is
# deliberately short: students see broad areas and useful destinations, not
# implementation fields, status labels, or module IDs.
PUBLIC_CURRICULUM_MAP = [
    ("Foundations and measurement", "Read measurements, use units, estimate, and write very large or small values clearly.", "../01-number-systems/index.qmd", "Open Foundations"),
    ("Basic electricity", "Build a working model of charge, voltage, current, resistance, power, energy, opens, and shorts.", "../02-basic-electronics/index.qmd", "Open Basic Electricity"),
    ("DC circuits", "Calculate and check series, parallel, mixed, and Kirchhoff circuit networks.", "../circuits/index.qmd", "Open Circuit Analysis"),
    ("Measurement and circuit building", "Move from a schematic to a simulation or breadboard, then compare predictions with measurements.", "../electronics-library/index.qmd#labs-and-assignments", "Find labs and activities"),
    ("Electronic components", "Explore resistors, switches, diodes, capacitors, transistors, sensors, motors, relays, and useful circuits.", "../electronics-library/index.qmd#components-and-applied-circuits", "Browse component resources"),
    ("Digital logic", "Use binary states, stable inputs, gates, truth tables, and simple digital decisions.", "../03-digital-logic-inputs/index.qmd", "Open Digital Logic"),
    ("Fabrication and PCB workflow", "Turn tested designs into physical parts, soldered circuits, boards, or enclosures.", "../../design-fabrication/index.qmd", "Open Design & Fabrication"),
    ("Computer systems", "Identify parts, understand power, start a computer, install an operating system, upgrade it, and test it.", "../computer-systems/index.qmd", "Open Computer Systems"),
    ("Linux, operating systems and networking", "Install Linux, use the desktop and terminal, inspect hardware, and diagnose connections.", "../linux-operating-systems/index.qmd", "Open Linux & Operating Systems"),
    ("Programming", "Turn a process into clear steps, code, tests, and useful output.", "../engineering-preparation-track/index.qmd#boolean-logic-algorithms-and-state-machines", "Explore programming in the engineering track"),
    ("Microcontrollers", "Connect code to protected inputs, sensors, outputs, timing, communication, and actuators.", "../04-microcontrollers/index.qmd", "Open Physical Computing"),
    ("Systems administration and networks", "Work with addresses, services, users, permissions, remote access, and troubleshooting.", "../linux-operating-systems/networking-diagnosis.qmd", "Open Networking Diagnosis"),
    ("Data and machine learning", "Collect useful data, graph it, test models, and explain what the evidence can and cannot show.", "../engineering-preparation-track/index.qmd#curve-fitting-regression-and-machine-learning", "Open the data and modelling track"),
    ("Applied AI", "Explore small, testable uses of artificial intelligence while checking sources, privacy, limits, and results.", "../engineering-preparation-track/index.qmd#curve-fitting-regression-and-machine-learning", "Start with data and model evaluation"),
    ("Projects and culminating work", "Combine design, building, code, measurement, testing, revision, and communication in a useful project.", "../electronics-library/projects/index.qmd", "Explore projects"),
]


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
    subsection_markup = ROADMAP_SUBSECTIONS[unit_id]
    why = ROADMAP_WHY[unit_id]
    outcome = ROADMAP_OUTCOMES[unit_id]
    collaboration = ROADMAP_COLLABORATION.get(unit_id, "")
    if collaboration:
        collaboration = f"\n\n{collaboration}"
    return f"""
## {html.escape(unit_id)}. {html.escape(ROADMAP_TITLES[unit_id])} {{#unit-{unit_id.replace('.', '-')}}}

| What students learn | Why it matters |
|:--|:--|
| {html.escape(ROADMAP_LEARNING[unit_id])} | {html.escape(why)} |

**Subsections:** {html.escape(subsection_markup)}

**Coming out of this section, students can:** {html.escape(outcome)}{collaboration}
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

    cards = []
    for number, (title, description, route, link_text) in enumerate(PUBLIC_CURRICULUM_MAP, start=1):
        cards.append(
            "\n".join(
                (
                    '::: {.ter-path-card}',
                    f"### {number}. {html.escape(title)}",
                    "",
                    html.escape(description),
                    "",
                    f"[{html.escape(link_text)}]({route})",
                    ":::",
                )
            )
        )
    card_markup = "\n\n".join(cards)
    return f"""---
title: "Computer Engineering Curriculum Map"
description: "The major areas of computer engineering in a useful learning order."
categories: [TEJ, curriculum roadmap, electronics, fabrication, computer systems, Linux, programming, microcontrollers, networking, machine learning, artificial intelligence]
sidebar: tej
page-layout: full
toc: false
body-classes: "ter-design-fabrication bs-title-eyebrow"
execute: {{enabled: false}}
---

This map shows the major areas of Computer Engineering and one sensible order for learning them. It is a map, not a checklist. Your class may move between areas as projects and equipment become available.

## Learning map

::: {{.ter-path-grid}}
{card_markup}
:::

## Optional tracks

- [Engineering Preparation Track](../engineering-preparation-track/index.qmd)
- [Linux & Systems pathway](../linux-operating-systems/index.qmd)
- [Advanced Circuit Analysis](../circuits/index.qmd)
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
