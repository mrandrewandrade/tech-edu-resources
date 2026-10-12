#!/usr/bin/env python3
"""Validate course-note metadata and generate the continuous lesson manifest."""

from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = REPOSITORY_ROOT / "site"
SOURCE_PATH = SITE_ROOT / "data" / "course-notes.json"
OUTPUT_PATH = SITE_ROOT / "assets" / "bs-learn-sequence.json"
NAVIGATION_PATH = SITE_ROOT / "_course-navigation.yml"
HUB_OUTPUT_DIR = SITE_ROOT / "includes" / "generated"
RENDERED_ROOT = SITE_ROOT / "_site"
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
        for field in (
            "course_title",
            "course_hub",
            "sidebar_id",
            "source",
            "title",
            "summary",
            "use",
            "track_id",
            "track_title",
            "track_summary",
            "track_use",
        ):
            require_string(lesson.get(field), f"Lesson {field}")
        for field in ("lesson_order", "track_order", "sequence_index"):
            if not isinstance(lesson.get(field), int) or int(lesson[field]) < 0:
                raise ValidationError(f"Lesson {field} must be a non-negative integer")
        resources = lesson.get("resources")
        if not isinstance(resources, list):
            raise ValidationError("Lesson resources must be a list")
        track_hub = lesson.get("track_hub")
        if track_hub is not None and not isinstance(track_hub, str):
            raise ValidationError("Lesson track_hub must be a string or null")
        for route_field in ("previous_route", "next_route"):
            route_value = lesson.get(route_field)
            if route_value is not None and not isinstance(route_value, str):
                raise ValidationError(f"Lesson {route_field} must be a string or null")
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
        for resource in raw_course.get("course_resources", []):
            assert isinstance(resource, dict)
            lines.extend(
                [
                    f"        - text: {_yaml_string(resource['title'])}",
                    f"          href: {_yaml_string(resource['source'])}",
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


def _attribute_json(values: list[str]) -> str:
    return html.escape(json.dumps(values, ensure_ascii=False), quote=True)


def _relative_public_href(source: str, hub_source: str) -> str:
    relative = posixpath.relpath(source, posixpath.dirname(hub_source))
    return str(Path(relative).with_suffix(".html")).replace("\\", "/")


def _catalogue_lessons(raw_unit: dict[str, object]) -> list[dict[str, object]]:
    lessons = raw_unit.get("lessons", [])
    assert isinstance(lessons, list)
    return [
        lesson
        for lesson in lessons
        if isinstance(lesson, dict)
        and lesson.get("status", "published") in {"published", "planned"}
    ]


def build_hub_fragment(
    raw_course: dict[str, object],
    hub_source: str,
    selected_unit: str | None = None,
) -> str:
    course_id = str(raw_course["id"])
    units = raw_course.get("units", [])
    assert isinstance(units, list)
    selected_units = [
        raw_unit
        for raw_unit in units
        if isinstance(raw_unit, dict)
        and (selected_unit is None or raw_unit.get("id") == selected_unit)
    ]
    total_lessons = sum(len(_catalogue_lessons(raw_unit)) for raw_unit in selected_units)
    filter_id = f"{course_id}-{selected_unit or 'all'}-lesson-search"
    lines = [
        "<!-- Generated by scripts/course_notes.py; do not edit. -->",
        "```{=html}",
        '<details class="bs-learn-filter-panel" data-bs-learn-filters>',
        '  <summary class="bs-learn-filters-summary" aria-label="Search and filter lessons">Search and filter lessons</summary>',
        '  <div class="bs-learn-filter-body">',
        '    <div class="bs-learn-search-group">',
        f'      <label for="{html.escape(filter_id, quote=True)}">Search lessons</label>',
        f'      <input id="{html.escape(filter_id, quote=True)}" type="search" autocomplete="off" spellcheck="false" placeholder="Search by title, topic, or purpose" data-bs-learn-search>',
        "    </div>",
    ]
    if len(selected_units) > 1:
        lines.extend(
            [
                '    <details class="bs-learn-filter-disclosure">',
                "      <summary>Filter by module</summary>",
                '      <div class="bs-learn-filter-options" role="group" aria-label="Filter by module">',
            ]
        )
        for raw_unit in selected_units:
            unit_id = str(raw_unit["id"])
            count = len(_catalogue_lessons(raw_unit))
            lines.append(
                f'        <button type="button" class="bs-learn-filter bs-learn-filter--track" '
                f'data-bs-filter-track="{html.escape(unit_id, quote=True)}" aria-pressed="false">'
                f'{html.escape(str(raw_unit["title"]))}<span class="bs-learn-filter-count">×{count}</span></button>'
            )
        lines.extend(["      </div>", "    </details>"])
    lines.extend(
        [
            '    <div class="bs-learn-filter-footer">',
            f'      <p class="bs-learn-result-count" data-bs-learn-result-count aria-live="polite">Showing {total_lessons} lessons.</p>',
            '      <button type="button" class="bs-learn-clear" data-bs-learn-clear hidden>Clear filters</button>',
            "    </div>",
            "  </div>",
            "</details>",
            '<div class="bs-learn-section-actions" role="group" aria-label="Lesson modules">',
            '  <button type="button" data-bs-learn-collapse-all>Collapse all</button>',
            '  <button type="button" data-bs-learn-expand-all>Expand all</button>',
            "</div>",
            '<div class="bs-learn-catalogue" data-bs-learn-list>',
        ]
    )
    for raw_unit in selected_units:
        unit_id = str(raw_unit["id"])
        lessons = _catalogue_lessons(raw_unit)
        count = len(lessons)
        unit_hub = raw_unit.get("hub")
        if unit_hub:
            relative_hub = _relative_public_href(str(unit_hub), hub_source)
            heading = (
                f'<a href="{html.escape(relative_hub, quote=True)}">'
                f'{html.escape(str(raw_unit["title"]))}</a>'
            )
        else:
            heading = f'<span class="bs-learn-track-lessons-label">{html.escape(str(raw_unit["title"]))}</span>'
        lines.extend(
            [
                f'<details class="bs-learn-catalogue-section" data-bs-learn-group data-bs-track-id="{html.escape(unit_id, quote=True)}" data-bs-total-lessons="{count}" open>',
                '  <summary class="bs-learn-catalogue-section-heading">',
                f'    <span class="bs-learn-track-heading">{heading}<span data-bs-learn-group-count>{count} {"lesson" if count == 1 else "lessons"}</span></span>',
                "  </summary>",
                '  <div class="bs-learn-catalogue-section-items">',
            ]
        )
        for lesson in lessons:
            status = lesson.get("status", "published")
            title = str(lesson["title"])
            if status == "published":
                relative_source = _relative_public_href(str(lesson["source"]), hub_source)
                title_markup = f'<a class="bs-learn-catalogue-link" href="{html.escape(relative_source, quote=True)}">{html.escape(title)}</a>'
            else:
                title_markup = f'<span class="bs-learn-catalogue-link">{html.escape(title)} <em>(planned)</em></span>'
            search_primary = _attribute_json([title, str(raw_unit["title"])])
            search_body = _attribute_json(
                [str(lesson["summary"]), str(lesson["use"])]
                + [
                    str(resource.get("label", ""))
                    for resource in lesson.get("resources", [])
                    if isinstance(resource, dict)
                ]
            )
            lines.extend(
                [
                    f'    <article class="bs-learn-catalogue-item" data-bs-learn-item data-bs-track="{html.escape(unit_id, quote=True)}" data-bs-difficulties="[]" data-bs-terms="[]" data-bs-search-primary="{search_primary}" data-bs-search-body="{search_body}">',
                    '      <details class="bs-learn-catalogue-description">',
                    f'        <summary aria-label="Show description for {html.escape(title, quote=True)}"><span class="bs-learn-catalogue-title-row">{title_markup}<span class="bs-learn-description-arrow" aria-hidden="true">▾</span></span></summary>',
                    f'        <p>{html.escape(str(lesson["summary"]))}</p>',
                    f'        <p>{html.escape(str(lesson["use"]))}</p>',
                ]
            )
            badges = _resource_badges(lesson.get("resources", []))
            if badges:
                lines.append(f'        <p class="ter-resource-badges">{badges}</p>')
            lines.extend(["      </details>", "    </article>"])
        lines.extend(["  </div>", "</details>"])
    lines.extend(
        [
            "</div>",
            '<p class="bs-learn-empty" data-bs-learn-empty hidden>No lessons match these filters.</p>',
            "```",
        ]
    )
    if selected_unit is None:
        resources = raw_course.get("course_resources", [])
        assert isinstance(resources, list)
        if resources:
            lines.extend(["", "## Highlighted tools", "", '<ul class="bs-learn-highlighted-tools">'])
            for resource in resources:
                assert isinstance(resource, dict)
                relative_source = _relative_public_href(str(resource["source"]), hub_source)
                lines.append(
                    f'  <li><a href="{html.escape(relative_source, quote=True)}">{html.escape(str(resource["title"]))}</a></li>'
                )
            lines.append("</ul>")
    return "\n".join(lines).rstrip() + "\n"


def generated_text_outputs(data: dict[str, object]) -> dict[Path, str]:
    outputs = {NAVIGATION_PATH: build_navigation(data)}
    courses = data["courses"]
    assert isinstance(courses, list)
    for raw_course in courses:
        assert isinstance(raw_course, dict)
        course_id = str(raw_course["id"])
        course_hub = str(raw_course["hub"])
        outputs[HUB_OUTPUT_DIR / f"{course_id}-toc.md"] = build_hub_fragment(
            raw_course, course_hub
        )
        units = raw_course.get("units", [])
        assert isinstance(units, list)
        for raw_unit in units:
            assert isinstance(raw_unit, dict)
            unit_hub = str(raw_unit.get("hub") or course_hub)
            outputs[HUB_OUTPUT_DIR / f"{course_id}-{raw_unit['id']}-toc.md"] = build_hub_fragment(
                raw_course,
                unit_hub,
                str(raw_unit["id"]),
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


class _RenderedHubParser(HTMLParser):
    def __init__(self, source: str) -> None:
        super().__init__()
        self.source = source
        self.catalogue_links: set[str] = set()
        self.sidebar_links: set[str] = set()
        self.qmd_links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attributes = dict(attrs)
        href = attributes.get("href") or ""
        parsed_href = urlsplit(href)
        if (
            not parsed_href.scheme
            and not parsed_href.netloc
            and parsed_href.path.lower().endswith(".qmd")
        ):
            self.qmd_links.append(href)
        classes = set((attributes.get("class") or "").split())
        route = _rendered_link_target(self.source, href)
        if route is None:
            return
        if "bs-learn-catalogue-link" in classes:
            self.catalogue_links.add(route)
        if "sidebar-link" in classes:
            self.sidebar_links.add(route)


def _rendered_source(source: str) -> str:
    return Path(source).with_suffix(".html").as_posix()


def _rendered_link_target(source: str, href: str) -> str | None:
    url = urlsplit(href)
    if url.scheme or url.netloc or not url.path:
        return None
    path = unquote(url.path).replace("\\", "/")
    for site_base in (SITE_BASE, "/tech-edu-resources"):
        if path == site_base:
            path = "/"
            break
        if path.startswith(site_base + "/"):
            path = path[len(site_base) :]
            break
    if path.startswith("/"):
        resolved = posixpath.normpath(path).lstrip("/")
    else:
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), path))
    if resolved.endswith("/"):
        resolved += "index.html"
    return resolved


def validate_rendered(rendered_root: Path = RENDERED_ROOT) -> None:
    if not rendered_root.is_dir():
        raise ValidationError(f"Rendered site does not exist: {rendered_root}")
    data = load_source()
    problems: list[str] = []
    all_html = sorted(rendered_root.rglob("*.html"))
    for path in all_html:
        source = path.relative_to(rendered_root).as_posix()
        parser = _RenderedHubParser(source)
        parser.feed(path.read_text(encoding="utf-8"))
        for href in parser.qmd_links:
            problems.append(f"Public .qmd link in {source}: {href}")

    courses = data["courses"]
    assert isinstance(courses, list)
    for raw_course in courses:
        assert isinstance(raw_course, dict)
        hub_source = _rendered_source(str(raw_course["hub"]))
        hub_path = rendered_root / hub_source
        if not hub_path.is_file():
            problems.append(f"Missing rendered course hub: {hub_source}")
            continue
        parser = _RenderedHubParser(hub_source)
        parser.feed(hub_path.read_text(encoding="utf-8"))
        units = raw_course.get("units", [])
        assert isinstance(units, list)
        for raw_unit in units:
            assert isinstance(raw_unit, dict)
            for lesson in _published_lessons(raw_unit):
                target = _rendered_source(str(lesson["source"]))
                if not (rendered_root / target).is_file():
                    problems.append(f"Published lesson was not rendered: {target}")
                if target not in parser.catalogue_links:
                    problems.append(f"Published lesson missing from course hub: {target}")
                if target not in parser.sidebar_links:
                    problems.append(f"Published lesson missing from course sidebar: {target}")
    if problems:
        raise ValidationError("Rendered course-note validation failed:\n- " + "\n- ".join(problems))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=("generate", "validate", "validate-rendered"),
        nargs="?",
        default="generate",
    )
    args = parser.parse_args(argv)
    try:
        if args.command == "generate":
            generate()
        elif args.command == "validate":
            validate()
        else:
            validate_rendered()
    except (OSError, json.JSONDecodeError, ValidationError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Course-note manifest {args.command} passed: {OUTPUT_PATH.relative_to(REPOSITORY_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
