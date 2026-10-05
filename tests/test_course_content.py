from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class CourseContentTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (SITE / relative).read_text(encoding="utf-8")

    def test_course_homes_are_lean_and_searchable(self) -> None:
        tas = self.read("tas2/index.qmd")
        tej = self.read("tej3-4/index.qmd")
        for content in (tas, tej):
            self.assertIn("**Work in progress.**", content)
            self.assertIn("data-bs-learn-search", content)
            self.assertIn("data-bs-learn-list", content)
            self.assertNotIn("Identity, Listening & Communication", content)
        self.assertIn("0. [Expectations]", tas)
        self.assertIn("1. [N.I.C.E. Design Process]", tas)
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
        for relative in (
            "tas2/00-getting-to-know-you/01-identity-listening-communication.qmd",
            "tej3-4/00-getting-to-know-you/01-identity-listening-communication.qmd",
        ):
            content = self.read(relative)
            self.assertIn("search: false", content)
            self.assertNotIn("ter-notes-lesson", content)

    def test_expectation_pages_are_intentionally_minimal(self) -> None:
        expected = "Refer to the current course outline for course expectations."
        self.assertIn(expected, self.read("tas2/00-expectations/index.qmd"))
        self.assertIn(expected, self.read("tej3-4/00-expectations/index.qmd"))

    def test_tas_class_material_uses_real_links_only(self) -> None:
        needs = self.read("tas2/01-nice-design-process/01-needs-necessities.qmd")
        inquiry = self.read("tas2/01-nice-design-process/02-investigate-inquire.qmd")
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


if __name__ == "__main__":
    unittest.main()
