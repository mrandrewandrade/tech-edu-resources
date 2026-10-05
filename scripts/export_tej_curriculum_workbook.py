from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = REPO_ROOT / "site" / "data" / "tej-curriculum.yml"


def text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    return str(value)


def load() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    data = yaml.safe_load(DATA_PATH.read_text(encoding="utf-8"))
    modules: list[dict[str, Any]] = []
    for unit in data["units"]:
        defaults = dict(unit.get("module_defaults", {}))
        for module in unit.get("modules", []):
            merged = {**defaults, **module}
            merged["unit_id"] = text(unit["unit_id"])
            merged["unit_title"] = text(unit["title"])
            modules.append(merged)
    return data, modules


RECORD_HEADERS = [
    "Unit ID",
    "Module ID",
    "Title",
    "Short description",
    "Status",
    "Pathway",
    "Prerequisites",
    "Estimated time",
    "Simulation requirement",
    "Physical-lab requirement",
    "Equipment",
    "Software",
    "Safety level",
    "Student deliverables",
    "Assessment evidence",
    "Public Notes route",
    "Student handout",
    "Teacher guide",
    "Slides",
    "Source references",
    "Access level",
    "Copyright or permissions note",
    "Implementation notes",
]


def module_row(module: dict[str, Any]) -> list[str]:
    return [
        text(module["unit_id"]),
        text(module["module_id"]),
        text(module["title"]),
        text(module["short_description"]),
        text(module["status"]),
        text(module["pathway"]),
        text(module["prerequisites"]),
        text(module["estimated_time"]),
        text(module["simulation_requirement"]),
        text(module["physical_lab_requirement"]),
        text(module["equipment"]),
        text(module["software"]),
        text(module["safety_level"]),
        text(module["student_deliverables"]),
        text(module["assessment_evidence"]),
        text(module["public_notes_route"]),
        text(module["student_handout"]),
        text(module["teacher_guide"]),
        text(module["slides"]),
        text(module["source_references"]),
        text(module["access_level"]),
        text(module["copyright_permissions_note"]),
        text(module["implementation_notes"]),
    ]


def unit_row(unit: dict[str, Any]) -> list[str]:
    synthetic = {**unit, "module_id": "UNIT"}
    return module_row(synthetic)


def table(title: str, note: str, headers: list[str], rows: list[list[str]]) -> list[list[str]]:
    return [[title], [note], [], headers, *rows]


def main() -> int:
    data, modules = load()
    units = data["units"]
    by_unit: dict[str, list[dict[str, Any]]] = {}
    for module in modules:
        by_unit.setdefault(module["unit_id"], []).append(module)

    hardware_prefixes = ("H", "BB", "DL", "FAB", "MC", "DC", "EL")
    hardware = [module for module in modules if text(module["module_id"]).startswith(hardware_prefixes)]

    tabs = {
        "Roadmap": table(
            "TEJ Curriculum Roadmap",
            "Curriculum-only sequence. Public statuses distinguish Published, Pilot, In development, Planned, Bonus, and Restricted source material. The public site is generated from site/data/tej-curriculum.yml and does not link this workbook.",
            RECORD_HEADERS,
            [unit_row(unit) for unit in units],
        ),
        "Hardware Modules": table(
            "TEJ Hardware and Fabrication Modules",
            "Hardware, circuit, digital-input, fabrication, and physical-computing scope aligned to the public curriculum sequence.",
            RECORD_HEADERS,
            [module_row(module) for module in hardware],
        ),
        "Programming": table(
            "Programming Fundamentals",
            "Python is the accessible general-purpose pathway. C and C++ support embedded work. Scope is planned until classroom packages are verified.",
            RECORD_HEADERS,
            [module_row(module) for module in by_unit.get("10", [])],
        ),
        "Linux": table(
            "Linux and Operating Systems",
            "Full planned pathway from operating-system concepts and desktop use to safe command-line administration.",
            RECORD_HEADERS,
            [module_row(module) for module in by_unit.get("9", [])],
        ),
        "Systems": table(
            "Networking and Systems Administration",
            "Planned defensive administration pathway. School network, privacy, and least-privilege rules apply.",
            RECORD_HEADERS,
            [module_row(module) for module in by_unit.get("12", [])],
        ),
        "Projects": table(
            "Culminating Projects",
            "Two major stages: a circuits and digital-logic project, then a final integrated technology project with teacher-approved pathways and budgets.",
            RECORD_HEADERS,
            [module_row(module) for module in by_unit.get("15", [])],
        ),
        "Site Index": table(
            "TEJ Public Site Index",
            "Public landing routes and honest implementation status. No teacher workbook, student tracker, or leaderboard link belongs on the public site.",
            ["Unit ID", "Landing page", "Purpose", "Status", "Access", "Implementation notes"],
            [
                [
                    text(unit["unit_id"]),
                    text(unit["public_notes_route"]),
                    text(unit["short_description"]),
                    text(unit["status"]),
                    text(unit["access_level"]),
                    text(unit["implementation_notes"]),
                ]
                for unit in units
            ],
        ),
        "Sources": table(
            "Curriculum Source Register",
            "Public pages use original summaries, original diagrams, official links, and properly licensed assets. Restricted classroom sources are not redistributed.",
            ["Source ID", "Source", "Use", "Public URL", "Access", "Copyright or permissions note"],
            [
                [
                    text(source["source_id"]),
                    text(source["title"]),
                    text(source["use"]),
                    text(source["url"]),
                    text(source["access_level"]),
                    text(source["copyright_permissions_note"]),
                ]
                for source in data["sources"]
            ],
        ),
    }

    quest_records = {
        text(module["module_id"]): {
            "unit_id": text(module["unit_id"]),
            "unit_title": text(module["unit_title"]),
            "title": text(module["title"]),
            "pathway": text(module["pathway"]),
            "status": text(module["status"]),
            "public_notes_route": text(module["public_notes_route"]),
            "access_level": text(module["access_level"]),
        }
        for module in modules
    }

    print(json.dumps({"tabs": tabs, "quest_records": quest_records}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
