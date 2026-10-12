#!/usr/bin/env python3
"""Validate course-note metadata and generate the continuous lesson manifest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = REPOSITORY_ROOT / "site"
SOURCE_PATH = SITE_ROOT / "data" / "course-notes.json"
OUTPUT_PATH = SITE_ROOT / "assets" / "bs-learn-sequence.json"
SITE_BASE = "/tech-edu-resources"


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
    if data.get("schema_version") != 1:
        raise ValidationError("Course-note source schema_version must be 1")
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
                if route in routes:
                    raise ValidationError(f"Duplicate lesson route: {route}")
                routes.add(route)
                course_records.append(
                    {
                        "course_id": course_id,
                        "course_title": course_title,
                        "lesson_order": raw_lesson["order"],
                        "route": route,
                        "title": require_string(
                            raw_lesson.get("title"), f"Lesson {source} title"
                        ),
                        "track_id": unit_id,
                        "track_order": unit_order,
                        "track_title": unit_title,
                    }
                )

        for index, record in enumerate(course_records):
            previous_record = course_records[index - 1] if index else None
            next_record = course_records[index + 1] if index + 1 < len(course_records) else None
            record["previous_route"] = previous_record["route"] if previous_record else None
            record["next_route"] = next_record["route"] if next_record else None
            record["next_starts_new_track"] = bool(
                next_record and record["track_id"] != next_record["track_id"]
            )
        records.extend(course_records)

    for sequence_index, record in enumerate(records):
        record["sequence_index"] = sequence_index

    manifest: dict[str, object] = {"schema_version": 1, "lessons": records}
    validate_manifest(manifest)
    return manifest


def validate_manifest(manifest: object) -> list[dict[str, object]]:
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise ValidationError("Lesson manifest schema_version must be 1")
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
            previous = course_lessons[index - 1]["route"] if index else None
            following = course_lessons[index + 1]["route"] if index + 1 < len(course_lessons) else None
            if lesson.get("previous_route") != previous:
                raise ValidationError(f"Course {course_id} has a broken previous route")
            if lesson.get("next_route") != following:
                raise ValidationError(f"Course {course_id} has a broken next route")
            expected_boundary = bool(
                following and lesson.get("track_id") != course_lessons[index + 1].get("track_id")
            )
            if lesson.get("next_starts_new_track") is not expected_boundary:
                raise ValidationError(f"Course {course_id} has a broken unit boundary")
    return typed_lessons


def serialized_manifest() -> str:
    return json.dumps(build_manifest(load_source()), ensure_ascii=False, indent=2) + "\n"


def generate() -> None:
    content = serialized_manifest()
    if not OUTPUT_PATH.exists() or OUTPUT_PATH.read_text(encoding="utf-8") != content:
        OUTPUT_PATH.write_text(content, encoding="utf-8", newline="\n")


def validate() -> None:
    expected = serialized_manifest()
    if not OUTPUT_PATH.is_file() or OUTPUT_PATH.read_text(encoding="utf-8") != expected:
        raise ValidationError(
            "Continuous lesson manifest is stale; run python scripts/course_notes.py generate"
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
