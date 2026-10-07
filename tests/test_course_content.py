from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class CourseContentTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (SITE / relative).read_text(encoding="utf-8")

    def test_course_homes_are_useful_and_searchable(self) -> None:
        design = self.read("design-fabrication/index.qmd")
        tej = self.read("tej3-4/index.qmd")
        self.assertIn("General Design & Fabrication", design)
        self.assertIn("N.I.C.E. Design Process", design)
        self.assertIn("Laser Cutting &amp; 2D Fabrication", design)
        self.assertIn("3D Modelling + 3D Printing", design)
        self.assertIn("**Work in progress.**", tej)
        self.assertIn("data-bs-learn-search", tej)
        self.assertIn("data-bs-learn-list", tej)
        self.assertIn(
            "0. [Course Orientation, Safety, Design Process, and Documentation]", tej
        )
        self.assertIn(
            "1. [Number Systems, Measurement, Units, and Calculator Skills]", tej
        )
        self.assertIn("## Curriculum Roadmap", tej)
        self.assertIn("[Open the complete curriculum roadmap](curriculum/index.qmd)", tej)

    def test_retired_lessons_are_compatibility_only(self) -> None:
        config = self.read("_quarto.yml")
        self.assertNotIn("Identity, Listening & Communication", config)
        self.assertNotIn("00-getting-to-know-you/index.qmd", config)
        for relative in ("tej3-4/00-getting-to-know-you/01-identity-listening-communication.qmd",):
            content = self.read(relative)
            self.assertIn("search: false", content)
            self.assertNotIn("ter-notes-lesson", content)

    def test_expectation_pages_are_intentionally_minimal(self) -> None:
        expected = "Refer to the current course outline for course expectations."
        self.assertIn(expected, self.read("tej3-4/00-expectations/index.qmd"))

    def test_tas_class_material_uses_real_links_only(self) -> None:
        needs = self.read("design-fabrication/01-nice-design-process/01-needs-necessities.qmd")
        inquiry = self.read("design-fabrication/01-nice-design-process/02-investigate-inquire.qmd")
        self.assertIn("1E7Io8pd1ZfymHki94Jnn5-1JUzcM5wrODzr5hTEjoa8", needs)
        self.assertIn("1TX9yMuScKH04QcF0TBzkMZTycqwOfSDpK0wZtJ-EbJQ", needs)
        self.assertIn("1FoN2vg_Tmm2QAUfiJSqPqeSmV7y_m5Brknn0JXxKv0s", inquiry)
        self.assertNotIn("Inquiry Worksheet](http", inquiry)

    def test_significant_figures_links_slides_and_actual_assignment(self) -> None:
        lesson = self.read("tej3-4/01-number-systems/01-significant-figures.qmd")
        self.assertIn("Day 6 slides: Significant figures", lesson)
        self.assertIn("Day 7 slides: Significant figures review and number systems", lesson)
        self.assertIn("Presentation 1: Significant Figures", lesson)
        self.assertIn("Presentation 2: Significant Figures", lesson)
        self.assertNotIn("Significant Figures practice 1", lesson)
        self.assertNotIn("Significant Figures practice 2", lesson)
        self.assertIn("Assignment: Number Systems practice problems", lesson)
        self.assertIn("1eDQR4YRVu6Ny7Ud5PC6YKqn-lvc6FZof", lesson)

    def test_significant_figures_has_brief_calculation_examples(self) -> None:
        lesson = self.read("tej3-4/01-number-systems/01-significant-figures.qmd")
        self.assertIn("### Adding and subtracting", lesson)
        self.assertIn("16.3 + 17.14 = 33.44 → 33.4", lesson)
        self.assertIn("### Multiplying and dividing", lesson)
        self.assertIn("6.23 × 1.23 = 7.6629 → 7.66", lesson)
        self.assertIn("round once, at the end", lesson)

    def test_reference_links_load_hover_titles_and_reader_panel(self) -> None:
        config = self.read("_quarto.yml")
        scripts = self.read("includes/bs-scripts.html")
        helper = self.read("assets/bs-reference-titles.js")
        self.assertIn("assets/bs-reference-titles.js", config)
        self.assertIn('"bs-reference-titles.js"', scripts)
        self.assertIn('"ref-grob2016": "Grob\'s Basic Electronics"', helper)
        self.assertIn('link.title = title', helper)
        self.assertIn('className = "bs-reference-panel"', helper)
        self.assertIn('fetch(key, { credentials: "same-origin" })', helper)
        self.assertIn('event.preventDefault()', helper)
        self.assertIn('Cited here as ', helper)

    def test_engineering_preparation_track_uses_plain_language_and_linked_references(self) -> None:
        track = self.read("tej3-4/engineering-preparation-track/index.qmd")
        self.assertIn('title: "Engineering Preparation Track"', track)
        self.assertNotIn('title: "Waterloo Engineering Track"', track)
        self.assertIn("## Full progression", track)
        self.assertEqual(track.count("**Learning goal:**"), 15)
        self.assertEqual(track.count("**Why it matters:**"), 15)
        self.assertEqual(track.count("**Subsections:**"), 15)
        self.assertEqual(track.count("**Subsections:**\n\n1."), 15)
        self.assertNotIn("| What students learn | Why it matters |", track)
        self.assertNotIn('collapse="true" title="Why it matters"', track)
        self.assertIn("[0. Engineering design and communication](#chapter-0-engineering-design-and-communication)", track)
        self.assertIn("[14. Engineering design project](#chapter-12-engineering-design-project)", track)
        self.assertEqual(track.count("**Coming out of this chapter, students can:**"), 15)
        self.assertNotIn("<summary>What is needed</summary>", track)
        self.assertEqual(track.count("**Suggested work:**"), 14)
        self.assertEqual(track.count("**Reference:**") + track.count("**References:**"), 13)
        self.assertNotIn("| Equipment |", track)
        self.assertNotIn("| Consumables |", track)
        self.assertNotIn("| Teacher note |", track)
        self.assertIn("Ohm's law and electrical power", track)
        self.assertIn("Series, parallel, and series-parallel circuits", track)
        self.assertIn("Kirchhoff's laws and systems of equations", track)
        self.assertIn("equivalent resistance, source current, branch current, voltage drops, and power", track)
        self.assertIn("Material and energy balances", track)
        self.assertIn("Sensors, measurement, calibration, and uncertainty", track)
        self.assertIn("Curve fitting, regression, and machine learning", track)
        self.assertIn("Number systems and digital representation", track)
        self.assertIn("Signed integers and two's complement", track)
        self.assertIn("training and test data, baselines, prediction error", track)
        self.assertIn("Kirchhoff's current law at nodes", track)
        self.assertIn("[[1]](../../references.qmd#ref-grob2016)", track)
        self.assertIn("[[27]](../../references.qmd#ref-cengel2008)", track)
        self.assertNotIn("KCL", track)
        self.assertNotIn("KVL", track)
        self.assertNotIn("WET-A", track)

        redirect = self.read("tej3-4/waterloo-engineering-track/index.qmd")
        self.assertIn("../engineering-preparation-track/", redirect)

        config = self.read("_quarto.yml")
        self.assertIn('section: "Engineering Preparation Track"', config)
        self.assertIn("index.qmd#chapter-8-curve-fitting-regression-and-machine-learning", config)
        self.assertIn("index.qmd#chapter-10-number-systems-and-digital-representation", config)
        self.assertIn("index.qmd#chapter-12-engineering-design-project", config)

    def test_tej_pages_inherit_the_learn_sidebar_layout(self) -> None:
        metadata_files = [SITE / "tej3-4" / "_metadata.yml"]
        metadata_files.extend((SITE / "tej3-4").glob("**/_metadata.yml"))
        for metadata_path in metadata_files:
            content = metadata_path.read_text(encoding="utf-8")
            if "body-classes:" in content:
                self.assertIn(
                    "bs-learn-article",
                    content,
                    f"{metadata_path.relative_to(SITE)} overrides the Learn layout",
                )

        root_metadata = self.read("tej3-4/_metadata.yml")
        self.assertIn('body-classes: "bs-learn-article"', root_metadata)

    def test_curriculum_roadmap_is_a_concise_public_course_map(self) -> None:
        roadmap = self.read("tej3-4/curriculum/index.qmd")
        self.assertEqual(roadmap.count("| What students learn | Why it matters |"), 17)
        self.assertEqual(roadmap.count("**Subsections:**"), 17)
        self.assertEqual(roadmap.count("**Coming out of this section, students can:**"), 17)
        self.assertIn("Use the sidebar for lessons", roadmap)
        self.assertNotIn("| Consumables |", roadmap)
        self.assertNotIn("| Teacher notes |", roadmap)
        self.assertNotIn("| Estimated time |", roadmap)
        self.assertNotIn("| Student handout |", roadmap)
        self.assertNotIn("| Copyright or permissions |", roadmap)
        self.assertNotIn("data-tej-roadmap-status", roadmap)


if __name__ == "__main__":
    unittest.main()
