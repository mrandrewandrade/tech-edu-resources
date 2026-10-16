from __future__ import annotations

import copy
import json
import posixpath
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
        self.assertEqual(len(design_routes), 29)
        self.assertEqual(
            design_routes[0],
            "/commons/design-fabrication/culture-land-based-learning/grandmother-moon-seasons.html",
        )
        self.assertEqual(
            design_routes[-1],
            "/commons/design-fabrication/advanced-making/stamp-faux-enamel-jewellery.html",
        )
        self.assertEqual(
            design_routes[9:14],
            [
                "/commons/design-fabrication/logo-design/01-nameplate-text-photopea.html",
                "/commons/design-fabrication/logo-design/rough-sketch-to-svg-photopea.html",
                "/commons/design-fabrication/logo-design/02b-advanced-multilayer-tracing-photopea.html",
                "/commons/design-fabrication/logo-design/03-combine-logo-nameplate.html",
                "/commons/design-fabrication/03-laser-cutting/01-name-logo.html",
            ],
        )
        self.assertEqual(
            design_routes[18:25],
            [
                "/commons/design-fabrication/03-laser-cutting/02-make-it-stand.html",
                "/commons/design-fabrication/03-laser-cutting/03-measure-place.html",
                "/commons/design-fabrication/03-laser-cutting/04-material-fit-calibration.html",
                "/commons/design-fabrication/03-laser-cutting/05-assemblies-hybrid-fabrication.html",
                "/commons/design-fabrication/03-laser-cutting/assembly-adhesives-finishing.html",
                "/commons/design-fabrication/03-laser-cutting/07-wall-bench-module.html",
                "/commons/design-fabrication/03-laser-cutting/08-capstone.html",
            ],
        )
        self.assertEqual(
            design_routes[25:29],
            [
                "/commons/design-fabrication/cad-parametric-modeling/introduction-to-cad.html",
                "/commons/design-fabrication/cad-parametric-modeling/phone-holder-design.html",
                "/commons/design-fabrication/hand-tools/phone-holder.html",
                "/commons/design-fabrication/advanced-making/stamp-faux-enamel-jewellery.html",
            ],
        )
        self.assertEqual(len(routes_by_course["tej"]), 17)
        self.assertEqual(routes_by_course["tej"][0], "/commons/tej3-4/circuits/parallel-circuits.html")
        self.assertEqual(routes_by_course["tej"][1], "/commons/tej3-4/circuits/series-circuits.html")
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

    def test_generated_hubs_use_the_interactive_catalogue(self) -> None:
        outputs = course_notes.generated_text_outputs(self.source)
        design = outputs[course_notes.HUB_OUTPUT_DIR / "design-fabrication-toc.md"]
        self.assertIn('data-bs-learn-filters', design)
        self.assertIn('data-bs-learn-collapse-all', design)
        self.assertIn('data-bs-learn-expand-all', design)
        self.assertIn('data-bs-learn-search', design)
        self.assertIn('aria-label="Show description for Understand the Situation &amp; Opportunity"', design)
        self.assertIn('data-bs-learn-result-count aria-live="polite"', design)
        self.assertIn("A clear situation and opportunity keep the team focused on a meaningful improvement.", design)
        self.assertNotIn("Why it matters:", design)
        self.assertNotIn("## Project path and tools", design)
        catalogue = design[design.index('<div class="bs-learn-catalogue"'):]
        self.assertLess(catalogue.index("Culture and Land-Based Learning"), catalogue.index("S.O. N.I.C.E. Design Process"))
        self.assertLess(catalogue.index("S.O. N.I.C.E. Design Process"), catalogue.index("Logo Design in Photopea"))
        self.assertLess(catalogue.index("Logo Design in Photopea"), catalogue.index("Accessible Design"))
        self.assertLess(catalogue.index("Accessible Design"), catalogue.index("Laser Cutting and Fabrication Tools"))
        self.assertLess(catalogue.index("Laser Cutting and Fabrication Tools"), catalogue.index("Laser-Cut Assembly, Adhesives &amp; Finishing"))
        self.assertLess(catalogue.index("Laser-Cut Assembly, Adhesives &amp; Finishing"), catalogue.index("CNC Machining"))
        self.assertLess(catalogue.index("CNC Machining"), catalogue.index("3D Printing"))
        self.assertLess(catalogue.index("3D Printing"), catalogue.index("Introduction to CAD &amp; 3D Parametric Modeling"))
        self.assertLess(catalogue.index("Introduction to CAD &amp; 3D Parametric Modeling"), catalogue.index("Phone Holder Design"))
        self.assertLess(catalogue.index("Phone Holder Design"), catalogue.index("Introduction to Tools, Machines &amp; Phone Holder Building"))
        self.assertLess(catalogue.index("Introduction to Tools, Machines &amp; Phone Holder Building"), catalogue.index("Advanced Making: Stamp or Faux-Enamel Jewellery"))
        self.assertLess(catalogue.index("Advanced Making: Stamp or Faux-Enamel Jewellery"), catalogue.index("## Highlighted tools"))
        self.assertIn('href="tools/index.html">CAD Tools</a>', design)

    def test_hubs_and_sidebar_number_sections_without_changing_titles_or_routes(self) -> None:
        outputs = course_notes.generated_text_outputs(self.source)
        design = outputs[course_notes.HUB_OUTPUT_DIR / "design-fabrication-toc.md"]
        logo = outputs[
            course_notes.HUB_OUTPUT_DIR / "design-fabrication-logo-design-toc.md"
        ]
        navigation = outputs[course_notes.NAVIGATION_PATH]

        self.assertIn(">2. S.O. N.I.C.E. Design Process</a>", design)
        self.assertIn(">1. Understand the Situation &amp; Opportunity</a>", design)
        self.assertIn(">3. Logo Design in Photopea</a>", logo)
        self.assertIn(">1. Build the Nameplate Text</a>", logo)
        self.assertIn('section: "3. Logo Design in Photopea"', navigation)
        self.assertIn('text: "1. Build the Nameplate Text"', navigation)
        self.assertIn('section: "CAD Tools"', navigation)
        self.assertIn('href: "design-fabrication/tools/index.qmd"', navigation)
        self.assertLess(
            navigation.index('section: "CAD Tools"'),
            navigation.index('text: "Laser-Cutting Files and Resources"'),
        )

        logo_unit = self.source["courses"][0]["units"][2]
        self.assertEqual(logo_unit["title"], "Logo Design in Photopea")
        self.assertEqual(
            logo_unit["lessons"][0]["source"],
            "design-fabrication/logo-design/01-nameplate-text-photopea.qmd",
        )

    def test_every_published_lesson_is_in_its_hub_and_sidebar(self) -> None:
        outputs = course_notes.generated_text_outputs(self.source)
        navigation = outputs[course_notes.NAVIGATION_PATH]
        for course in self.source["courses"]:
            hub = outputs[course_notes.HUB_OUTPUT_DIR / f"{course['id']}-toc.md"]
            for unit in course["units"]:
                for lesson in unit["lessons"]:
                    if lesson.get("status", "published") != "published":
                        continue
                    relative_source = course_notes._relative_public_href(
                        lesson["source"], course["hub"]
                    )
                    self.assertIn(f'href="{relative_source}"', hub)
                    self.assertIn(f'href: "{lesson["source"]}"', navigation)

    def test_restricted_resources_are_labels_not_links(self) -> None:
        outputs = course_notes.generated_text_outputs(self.source)
        electronics = outputs[
            course_notes.HUB_OUTPUT_DIR / "tej-circuits-electronics-toc.md"
        ]
        self.assertIn(
            '<span class="ter-resource-badge is-restricted">Teacher Answers, restricted</span>',
            electronics,
        )
        self.assertNotIn('href="Teacher Answers"', electronics)

    def test_manifest_rejects_incomplete_schema_two_records(self) -> None:
        broken = copy.deepcopy(self.manifest)
        broken["lessons"][0].pop("track_summary")
        with self.assertRaisesRegex(course_notes.ValidationError, "track_summary"):
            course_notes.validate_manifest(broken)

    def test_nice_page_uses_the_canonical_cycle_image_once(self) -> None:
        source = (
            course_notes.SITE_ROOT / "design-fabrication" / "design-process" / "index.qmd"
        ).read_text(encoding="utf-8")
        self.assertEqual(source.count("nice-process-cycle.png"), 1)
        self.assertIn("#fig-nice-process", source)
        self.assertNotIn("lighthouse-garden.png", source)
        image = course_notes.SITE_ROOT / "assets" / "nice-design-process" / "nice-process-cycle.png"
        self.assertTrue(image.is_file())
        self.assertGreater(image.stat().st_size, 1_000_000)

    def test_all_published_laser_lessons_are_rendered(self) -> None:
        quarto = (course_notes.SITE_ROOT / "_quarto.yml").read_text(encoding="utf-8")
        self.assertIn('"design-fabrication/03-laser-cutting/**/*.qmd"', quarto)
        self.assertNotIn('"design-fabrication/03-laser-cutting/01-name-logo.qmd"', quarto)

    def test_numbered_slugs_require_an_explicit_legacy_exception(self) -> None:
        broken = copy.deepcopy(self.source)
        lesson = broken["courses"][0]["units"][2]["lessons"][0]
        lesson.pop("legacy_slug", None)
        with self.assertRaisesRegex(course_notes.ValidationError, "Numbered lesson slug"):
            course_notes.build_manifest(broken)


if __name__ == "__main__":
    unittest.main()
