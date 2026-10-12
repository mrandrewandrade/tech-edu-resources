#!/usr/bin/env python3
"""Validate course-note metadata and generate the continuous lesson manifest."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = REPOSITORY_ROOT / "site"
SOURCE_PATH = SITE_ROOT / "data" / "course-notes.json"
OUTPUT_PATH = SITE_ROOT / "assets" / "bs-learn-sequence.json"
NAVIGATION_PATH = SITE_ROOT / "_course-navigation.yml"
HUB_OUTPUT_DIR = SITE_ROOT / "includes" / "generated"
SITE_BASE = "/commons"


class ValidationError(RuntimeError):
    """Raised when course-note metadata or generated output is invalid."""


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def require_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label} must be a non-empty string")
    return value.strip()


def lesson_route(source: str) -> str:
    path = Path(source)
    if path.suffix != ".qmd" or path.is_absolute() or ".." in path.parts:
        raise ValidationError(f"Invalid lesson source: {source!r}")
    return f"{SITE_BASE}/{path.with_suffix('.html').as_posix()}"


def load_source(path: Path = SOURCE_PATH) -> dict[str, object]:
    data = read_json(path)
    if not isinstance(data, dict) or set(data) != {"schema_version", "courses"}:
        raise ValidationError("Course-note source must contain schema_version and courses")
    if data.get("schema_version") != 2:
        raise ValidationError("Course-note source schema_version must be 2")
    courses = data.get("courses")
    if not isinstance(courses, list) or not courses:
        raise ValidationError("Course-note source requires at least one course")
    return data


def build_manifest(data: dict[str, object]) -> dict[str, object]:
    raw_courses = data["courses"]
    assert isinstance(raw_courses, list)
    records: list[dict[str, object]] = []
    course_ids: set[str] = set()
    routes: set[str] = set()

    for course_index, raw_course in enumerate(raw_courses):
        if not isinstance(raw_course, dict):
            raise ValidationError(f"Course {course_index} must be an object")
        course_id = require_string(raw_course.get("id"), f"Course {course_index} id")
        course_title = require_string(
            raw_course.get("title"), f"Course {course_id} title"
        )
        course_hub = require_string(raw_course.get("hub"), f"Course {course_id} hub")
        course_hub_path = SITE_ROOT / course_hub
        if not course_hub_path.is_file():
            raise ValidationError(f"Course hub does not exist: {course_hub}")
        course_hub_route = lesson_route(course_hub)
        sidebar_id = require_string(
            raw_course.get("sidebar_id"), f"Course {course_id} sidebar_id"
        )
        if course_id in course_ids:
            raise ValidationError(f"Duplicate course id: {course_id}")
        course_ids.add(course_id)
        units = raw_course.get("units")
        if not isinstance(units, list) or not units:
            raise ValidationError(f"Course {course_id} requires units")

        course_records: list[dict[str, object]] = []
        unit_ids: set[str] = set()
        for unit_index, raw_unit in enumerate(units):
            if not isinstance(raw_unit, dict):
                raise ValidationError(f"Course {course_id} unit {unit_index} must be an object")
            unit_id = require_string(raw_unit.get("id"), f"Course {course_id} unit id")
            unit_title = require_string(
                raw_unit.get("title"), f"Course {course_id} unit {unit_id} title"
            )
            unit_order = raw_unit.get("order")
            if not isinstance(unit_order, int) or unit_order < 0:
                raise ValidationError(f"Unit {unit_id} order must be a non-negative integer")
            if unit_id in unit_ids:
                raise ValidationError(f"Duplicate unit id in {course_id}: {unit_id}")
            unit_ids.add(unit_id)
            unit_summary = require_string(
                raw_unit.get("summary"), f"Unit {unit_id} summary"
            )
            unit_use = require_string(raw_unit.get("use"), f"Unit {unit_id} use")
            unit_hub = raw_unit.get("hub")
            if unit_hub is not None:
                unit_hub = require_string(unit_hub, f"Unit {unit_id} hub")
            lessons = raw_unit.get("lessons")
            if not isinstance(lessons, list):
                raise ValidationError(f"Unit {unit_id} lessons must be a list")
            expected_orders = list(range(1, len(lessons) + 1))
            actual_orders = [
                lesson.get("order") if isinstance(lesson, dict) else None
                for lesson in lessons
            ]
            if actual_orders != expected_orders:
                raise ValidationError(f"Unit {unit_id} lesson orders must be contiguous from 1")

            for raw_lesson in lessons:
                assert isinstance(raw_lesson, dict)
                status = require_string(
                    raw_lesson.get("status", "published"),
                    f"Unit {unit_id} lesson status",
                )
                if status not in {"published", "planned", "restricted"}:
                    raise ValidationError(f"Lesson status is invalid in {unit_id}: {status}")
                if status != "published":
                    continue
                source = require_string(
                    raw_lesson.get("source"), f"Unit {unit_id} lesson source"
                )
                source_path = SITE_ROOT / source
                if not source_path.is_file():
                    raise ValidationError(f"Lesson source does not exist: {source}")
                source_text = source_path.read_text(encoding="utf-8")
                if "ter-notes-lesson" not in source_text:
                    raise ValidationError(f"Lesson source lacks lesson body class: {source}")
                route = lesson_route(source)
                slug = Path(source).stem
                if re.match(r"^\d+(?:[-_]|$)", slug) and not raw_lesson.get(
                    "legacy_slug", False
                ):
                    raise ValidationError(
                        f"Numbered lesson slug requires an explicit legacy_slug exception: {source}"
                    )
                if route in routes:
                    raise ValidationError(f"Duplicate lesson route: {route}")
                routes.add(route)
                course_records.append(
                    {
                        "course_id": course_id,
                        "course_title": course_title,
                        "course_hub": course_hub_route,
                        "sidebar_id": sidebar_id,
                        "lesson_order": raw_lesson["order"],
                        "route": route,
                        "source": source,
                        "title": require_string(
                            raw_lesson.get("title"), f"Lesson {source} title"
                        ),
                        "summary": require_string(
                            raw_lesson.get("summary"), f"Lesson {source} summary"
                        ),
                        "use": require_string(
                            raw_lesson.get("use"), f"Lesson {source} use"
                        ),
                        "resources": raw_lesson.get("resources", []),
                        "track_id": unit_id,
                        "track_order": unit_order,
                        "track_title": unit_title,
                        "track_hub": unit_hub,
                        "track_summary": unit_summary,
                        "track_use": unit_use,
                    }
                )

        for index, record in enumerate(course_records):
            previous_record = course_records[index - 1] if index else None
            next_record = course_records[index + 1] if index + 1 < len(course_records) else None
            if next_record and record["track_id"] != next_record["track_id"]:
                next_record = None
            record["previous_route"] = previous_record["route"] if previous_record else None
            if previous_record and record["track_id"] != previous_record["track_id"]:
                record["previous_route"] = None
            record["next_route"] = next_record["route"] if next_record else None
            record["next_starts_new_track"] = False
        records.extend(course_records)

    for sequence_index, record in enumerate(records):
        record["sequence_index"] = sequence_index

    manifest: dict[str, object] = {"schema_version": 2, "lessons": records}
    validate_manifest(manifest)
    return manifest


def validate_manifest(manifest: object) -> list[dict[str, object]]:
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 2:
        raise ValidationError("Lesson manifest schema_version must be 2")
    lessons = manifest.get("lessons")
    if not isinstance(lessons, list) or not lessons:
        raise ValidationError("Lesson manifest requires lessons")
    if any(not isinstance(lesson, dict) for lesson in lessons):
        raise ValidationError("Every lesson manifest record must be an object")
    typed_lessons = lessons  # type: ignore[assignment]
    routes = [require_string(lesson.get("route"), "Lesson route") for lesson in typed_lessons]
    if len(routes) != len(set(routes)):
        raise ValidationError("Lesson manifest routes must be unique")
    if [lesson.get("sequence_index") for lesson in typed_lessons] != list(range(len(typed_lessons))):
        raise ValidationError("Lesson manifest indexes must be contiguous")

    by_course: dict[str, list[dict[str, object]]] = {}
    course_order: list[str] = []
    for lesson in typed_lessons:
        course_id = require_string(lesson.get("course_id"), "Lesson course_id")
        if course_id not in by_course:
            by_course[course_id] = []
            course_order.append(course_id)
        by_course[course_id].append(lesson)
        if not str(lesson["route"]).startswith(f"{SITE_BASE}/"):
            raise ValidationError("Lesson route does not preserve the site base path")

    flattened = [lesson for course_id in course_order for lesson in by_course[course_id]]
    if flattened != typed_lessons:
        raise ValidationError("Each course must occupy one contiguous manifest block")

    for course_id, course_lessons in by_course.items():
        for index, lesson in enumerate(course_lessons):
            previous_record = course_lessons[index - 1] if index else None
            following_record = course_lessons[index + 1] if index + 1 < len(course_lessons) else None
            previous = (
                previous_record["route"]
                if previous_record and previous_record.get("track_id") == lesson.get("track_id")
                else None
            )
            following = (
                following_record["route"]
                if following_record and following_record.get("track_id") == lesson.get("track_id")
                else None
            )
            if lesson.get("previous_route") != previous:
                raise ValidationError(f"Course {course_id} has a broken previous route")
            if lesson.get("next_route") != following:
                raise ValidationError(f"Course {course_id} has a broken next route")
            if lesson.get("next_starts_new_track") is not False:
                raise ValidationError(f"Course {course_id} has a broken unit boundary")
    return typed_lessons


def _yaml_string(value: object) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def _published_lessons(raw_unit: dict[str, object]) -> list[dict[str, object]]:
    lessons = raw_unit.get("lessons", [])
    assert isinstance(lessons, list)
    return [
        lesson
        for lesson in lessons
        if isinstance(lesson, dict) and lesson.get("status", "published") == "published"
    ]


def build_navigation(data: dict[str, object]) -> str:
    lines = ["# Generated by scripts/course_notes.py; do not edit.", "website:", "  sidebar:"]
    courses = data["courses"]
    assert isinstance(courses, list)
    for raw_course in courses:
        assert isinstance(raw_course, dict)
        lines.extend(
            [
                f"    - id: {_yaml_string(raw_course['sidebar_id'])}",
                f"      title: {_yaml_string(raw_course['title'])}",
                "      style: docked",
                "      collapse-level: 2",
                "      contents:",
                f"        - text: {_yaml_string(raw_course['title'] + ' Home')}",
                f"          href: {_yaml_string(raw_course['hub'])}",
            ]
        )
        for extra in raw_course.get("sidebar_links", []):
            assert isinstance(extra, dict)
            lines.extend(
                [
                    f"        - text: {_yaml_string(extra['title'])}",
                    f"          href: {_yaml_string(extra['source'])}",
                ]
            )
        units = raw_course.get("units", [])
        assert isinstance(units, list)
        for raw_unit in units:
            assert isinstance(raw_unit, dict)
            lessons = _published_lessons(raw_unit)
            if not lessons:
                continue
            hub = raw_unit.get("hub")
            if hub:
                lines.append(f"        - section: {_yaml_string(raw_unit['title'])}")
                lines.append(f"          href: {_yaml_string(hub)}")
            else:
                lines.append(f"        - section: {_yaml_string(raw_unit['title'])}")
            lines.append("          contents:")
            for lesson in lessons:
                lines.extend(
                    [
                        f"            - text: {_yaml_string(lesson['title'])}",
                        f"              href: {_yaml_string(lesson['source'])}",
                    ]
                )
    lines.extend(
        [
            "    - id: tas2",
            "      title: \"General Design & Fabrication\"",
            "      style: docked",
            "      contents:",
            "        - href: design-fabrication/index.qmd",
            "          text: \"Open the reusable curriculum\"",
        ]
    )
    return "\n".join(lines) + "\n"


def _resource_badges(resources: object) -> str:
    if not isinstance(resources, list):
        raise ValidationError("Lesson resources must be a list")
    badges: list[str] = []
    for resource in resources:
        if not isinstance(resource, dict):
            raise ValidationError("Lesson resource must be an object")
        label = require_string(resource.get("label"), "Resource label")
        if resource.get("restricted"):
            badges.append(f"<span class=\"ter-resource-badge is-restricted\">{html.escape(label)}, restricted</span>")
        else:
            url = require_string(resource.get("url"), f"Resource {label} URL")
            badges.append(
                f"<a class=\"ter-resource-badge\" href=\"{html.escape(url, quote=True)}\">{html.escape(label)}</a>"
            )
    return " ".join(badges)


def build_hub_fragment(raw_course: dict[str, object], selected_unit: str | None = None) -> str:
    lines = ["<!-- Generated by scripts/course_notes.py; do not edit. -->"]
    units = raw_course.get("units", [])
    assert isinstance(units, list)
    for raw_unit in units:
        assert isinstance(raw_unit, dict)
        if selected_unit and raw_unit.get("id") != selected_unit:
            continue
        lines.extend(
            [
                f"## {raw_unit['title']}",
                "",
                str(raw_unit["summary"]),
                "",
                str(raw_unit["use"]),
                "",
            ]
        )
        lessons = raw_unit.get("lessons", [])
        assert isinstance(lessons, list)
        for lesson in lessons:
            assert isinstance(lesson, dict)
            status = lesson.get("status", "published")
            title = str(lesson["title"])
            if status == "published":
                title_text = f"[{title}]({lesson_route(str(lesson['source']))})"
            elif status == "planned":
                title_text = f"{title} *(planned)*"
            else:
                continue
            lines.extend(
                [
                    f"### {title_text}",
                    "",
                    str(lesson["summary"]),
                    "",
                    str(lesson["use"]),
                    "",
                ]
            )
            badges = _resource_badges(lesson.get("resources", []))
            if badges:
                lines.extend([f"<p class=\"ter-resource-badges\">{badges}</p>", ""])
    return "\n".join(lines).rstrip() + "\n"


def generated_text_outputs(data: dict[str, object]) -> dict[Path, str]:
    outputs = {NAVIGATION_PATH: build_navigation(data)}
    courses = data["courses"]
    assert isinstance(courses, list)
    for raw_course in courses:
        assert isinstance(raw_course, dict)
        course_id = str(raw_course["id"])
        outputs[HUB_OUTPUT_DIR / f"{course_id}-toc.md"] = build_hub_fragment(raw_course)
        units = raw_course.get("units", [])
        assert isinstance(units, list)
        for raw_unit in units:
            assert isinstance(raw_unit, dict)
            outputs[HUB_OUTPUT_DIR / f"{course_id}-{raw_unit['id']}-toc.md"] = build_hub_fragment(
                raw_course, str(raw_unit["id"])
            )
    return outputs


def serialized_manifest() -> str:
    return json.dumps(build_manifest(load_source()), ensure_ascii=False, indent=2) + "\n"


def generate() -> None:
    content = serialized_manifest()
    if not OUTPUT_PATH.exists() or OUTPUT_PATH.read_text(encoding="utf-8") != content:
        OUTPUT_PATH.write_text(content, encoding="utf-8", newline="\n")
    data = load_source()
    for path, generated in generated_text_outputs(data).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_text(encoding="utf-8") != generated:
            path.write_text(generated, encoding="utf-8", newline="\n")


def validate() -> None:
    expected = serialized_manifest()
    if not OUTPUT_PATH.is_file() or OUTPUT_PATH.read_text(encoding="utf-8") != expected:
        raise ValidationError(
            "Continuous lesson manifest is stale; run python scripts/course_notes.py generate"
        )
    for path, generated in generated_text_outputs(load_source()).items():
        if not path.is_file() or path.read_text(encoding="utf-8") != generated:
            raise ValidationError(
                f"Generated course navigation is stale: {path.relative_to(REPOSITORY_ROOT)}"
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("generate", "validate"), nargs="?", default="generate")
    args = parser.parse_args(argv)
    try:
        generate() if args.command == "generate" else validate()
    except (OSError, json.JSONDecodeError, ValidationError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Course-note manifest {args.command} passed: {OUTPUT_PATH.relative_to(REPOSITORY_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
