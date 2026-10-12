from __future__ import annotations

import copy
import json
import unittest

from scripts import course_notes


class CourseNotesManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = course_notes.load_source()
        cls.manifest = course_notes.build_manifest(cls.source)
        cls.lessons = cls.manifest["lessons"]

    def test_active_course_sequences_are_exact(self) -> None:
        routes_by_course: dict[str, list[str]] = {}
        for lesson in self.lessons:
            routes_by_course.setdefault(lesson["course_id"], []).append(lesson["route"])
        design_routes = routes_by_course["design-fabrication"]
        self.assertEqual(len(design_routes), 25)
        self.assertEqual(
            design_routes[0],
            "/commons/design-fabrication/culture-land-based-learning/grandmother-moon-seasons.html",
        )
        self.assertEqual(
            design_routes[-1],
            "/commons/design-fabrication/03-laser-cutting/08-capstone.html",
        )
        self.assertEqual(
            design_routes[10:15],
            [
                "/commons/design-fabrication/logo-design/01-nameplate-text-photopea.html",
                "/commons/design-fabrication/logo-design/rough-sketch-to-svg-photopea.html",
                "/commons/design-fabrication/logo-design/02b-advanced-multilayer-tracing-photopea.html",
                "/commons/design-fabrication/logo-design/03-combine-logo-nameplate.html",
                "/commons/design-fabrication/03-laser-cutting/01-name-logo.html",
            ],
        )
        self.assertEqual(len(routes_by_course["tej"]), 17)
        self.assertEqual(routes_by_course["tej"][0], "/commons/tej3-4/circuits/series-circuits.html")
        self.assertEqual(
            routes_by_course["tej"][-1],
            "/commons/tej3-4/linux-operating-systems/power-and-raspberry-pi-bridge.html",
        )
        self.assertFalse(any("submission" in route for route in routes_by_course["tej"]))

    def test_course_boundaries_stop_cleanly(self) -> None:
        for course_id in ("design-fabrication", "tej"):
            course_lessons = [
                lesson for lesson in self.lessons if lesson["course_id"] == course_id
            ]
            self.assertIsNone(course_lessons[0]["previous_route"])
            self.assertIsNone(course_lessons[-1]["next_route"])
        all_routes = {lesson["route"] for lesson in self.lessons}
        self.assertFalse(any("identity-listening" in route for route in all_routes))
        self.assertFalse(any(route.endswith("/index.html") for route in all_routes))

    def test_cross_course_link_fails_validation(self) -> None:
        broken = copy.deepcopy(self.manifest)
        design_lessons = [
            lesson
            for lesson in broken["lessons"]
            if lesson["course_id"] == "design-fabrication"
        ]
        tej_first = next(
            lesson for lesson in broken["lessons"] if lesson["course_id"] == "tej"
        )
        design_lessons[-1]["next_route"] = tej_first["route"]
        with self.assertRaisesRegex(course_notes.ValidationError, "broken next route"):
            course_notes.validate_manifest(broken)

    def test_generated_manifest_is_current(self) -> None:
        tracked = json.loads(course_notes.OUTPUT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(tracked, self.manifest)
        for path, expected in course_notes.generated_text_outputs(self.source).items():
            self.assertEqual(path.read_text(encoding="utf-8"), expected)

    def test_numbered_slugs_require_an_explicit_legacy_exception(self) -> None:
        broken = copy.deepcopy(self.source)
        lesson = broken["courses"][0]["units"][2]["lessons"][0]
        lesson.pop("legacy_slug", None)
        with self.assertRaisesRegex(course_notes.ValidationError, "Numbered lesson slug"):
            course_notes.build_manifest(broken)


if __name__ == "__main__":
    unittest.main()
