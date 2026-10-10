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
        self.assertIn('title: "Design & Fabrication"', design)
        self.assertIn("N.I.C.E. Design Process", design)
        self.assertIn("Logo Design", design)
        self.assertIn("Tool Organizer Project", design)
        self.assertIn("Fabrication Plate Builder", design)
        self.assertIn('title="Work in progress"', tej)
        self.assertIn("## Available units", tej)
        self.assertIn("[Open Circuits](circuits/index.qmd)", tej)
        self.assertIn("[Open the Engineering Preparation Track]", tej)

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
        self.assertIn("## Circuit sequence", track)
        self.assertEqual(track.count("**I will be able to**"), 19)
        self.assertEqual(track.count("**This is useful because I can**"), 19)
        self.assertEqual(track.count("**Used in college or university:**"), 19)
        self.assertNotIn("| What students learn | Why it matters |", track)
        self.assertNotIn("<summary>What is needed</summary>", track)
        self.assertNotIn("| Equipment |", track)
        self.assertNotIn("| Consumables |", track)
        self.assertNotIn("| Teacher note |", track)
        self.assertIn("Ohm's law and power", track)
        self.assertIn("Series circuits", track)
        self.assertIn("Parallel circuits", track)
        self.assertIn("Series-parallel circuits", track)
        self.assertIn("Kirchhoff's laws", track)
        self.assertIn("Linear algebra for circuits", track)
        self.assertIn("Material and energy balances", track)
        self.assertIn("Sensors and measurement", track)
        self.assertIn("Curve fitting, regression, and machine learning", track)
        self.assertIn("Number systems and digital representation", track)
        self.assertIn("Sensor, logic, and actuator project", track)
        sequence = [
            "## Engineering calculations", "## Ohm's law and power",
            "## Series circuits", "## Parallel circuits",
            "## Series-parallel circuits", "## Kirchhoff's laws",
            "## Linear algebra for circuits", "## Equivalent circuits and optimization",
            "## Material and energy balances", "## Transient systems",
            "## Boolean logic, algorithms, and state machines",
            "## Number systems and digital representation",
            "## Sensors and measurement", "## Motors and electromechanical systems",
            "## Sensor, logic, and actuator project",
            "## Curve fitting, regression, and machine learning",
            "## Operational amplifiers and calculus", "## Feedback and control",
            "## Engineering design project",
        ]
        positions = [track.index(heading) for heading in sequence]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("analog-to-digital converter", track)
        self.assertIn("pulse-width modulation", track)
        self.assertIn("pull-up and pull-down switch inputs", track)
        self.assertIn("Kirchhoff's current law at a node", track)
        self.assertIn("Series Circuits lesson package", track)
        self.assertIn("Series-Parallel Circuits lesson package", track)
        self.assertIn("[[1]](../../references.qmd#ref-grob2016)", track)
        self.assertIn("[[27]](../../references.qmd#ref-cengel2008)", track)
        self.assertIn("## Ontario course collaboration opportunities", track)
        self.assertIn("They do not mean that one course replaces", track)
        for course in ("TEJ3M", "TEJ4M", "SPH3U", "SCH4U", "SBI4U"):
            self.assertIn(course, track)
        self.assertIn("the electronics are the instrument, not a substitute for the biology", track)
        self.assertIn("2009teched1112curr.pdf", track)
        self.assertIn("secondary-science/courses/sph3u/strands", track)
        self.assertIn("secondary-science/courses/sch4u/strands", track)
        self.assertIn("secondary-science/courses/sbi4u/strands", track)

        redirect = self.read("tej3-4/waterloo-engineering-track/index.qmd")
        self.assertIn("../engineering-preparation-track/", redirect)

        config = self.read("_quarto.yml")
        self.assertIn('text: "Engineering Preparation Track"', config)
        self.assertIn("tej3-4/engineering-preparation-track/index.qmd", config)

    def test_equations_are_copyable_numbered_mathjax_and_have_diagrams(self) -> None:
        config = self.read("_quarto.yml")
        scripts = self.read("includes/bs-scripts.html")
        helper = self.read("assets/tej-equations-v1.js")
        styles = self.read("assets/tej-equations-v2.css")
        self.assertIn("assets/tej-equations-v1.js", config)
        self.assertIn("assets/tej-equations-v2.css", config)
        self.assertIn('"tej-equations-v1.js"', scripts)
        self.assertIn("terEquationSources", scripts)
        self.assertIn("Copy equation", helper)
        self.assertIn("Copy LaTeX", helper)
        self.assertIn("ClipboardItem", helper)
        self.assertIn('document.execCommand("copy")', helper)
        self.assertIn("mjx-assistive-mml", helper)
        self.assertNotIn('mjx-container[jax="CHTML"]', styles)
        self.assertIn(".ter-figure-anchor", styles)

        chapters = [
            "tej3-4/circuits/index.qmd",
            "tej3-4/circuits/series-circuits.qmd",
            "tej3-4/circuits/parallel-circuits.qmd",
            "tej3-4/circuits/series-parallel-circuits.qmd",
            "tej3-4/circuits/kirchhoffs-laws.qmd",
            "tej3-4/circuits/linear-algebra-circuits.qmd",
        ]
        for relative in chapters:
            source = self.read(relative)
            self.assertEqual(source.count("$$") // 2, source.count("{#eq-"), relative)

        examples = {
            "tej3-4/circuits/series-circuits.qmd": ("In a car", "In a robot", "fig-series-rule"),
            "tej3-4/circuits/parallel-circuits.qmd": ("A car", "A robot", "fig-parallel-rule"),
            "tej3-4/circuits/series-parallel-circuits.qmd": ("A car", "A robot", "fig-series-parallel-comparison"),
            "tej3-4/circuits/kirchhoffs-laws.qmd": ("In a car", "In a robot", "fig-kirchhoff-node-loop"),
            "tej3-4/circuits/linear-algebra-circuits.qmd": ("car wiring", "robotics engineer", "Used in college or university"),
        }
        for relative, required in examples.items():
            source = self.read(relative)
            self.assertIn("**Used in college or university:**", source)
            self.assertIn("**Where you see it:**", source)
            for phrase in required:
                self.assertIn(phrase, source)

        mixed = self.read("tej3-4/circuits/series-parallel-circuits.qmd")
        self.assertIn('id="fig-series-parallel-example"', mixed)
        self.assertEqual(mixed.count('class="ter-figure-anchor"'), 2)

        comparison = self.read("assets/electronics/schematics/series-parallel-comparison.svg")
        self.assertIn('viewBox="0 0 470 125"', comparison)
        self.assertNotIn('x="62.299" y="17.075"', comparison)
        self.assertNotIn('x="283.401" y="17.075"', comparison)
        self.assertIn('x="94" y="88.3"', comparison)
        self.assertIn('x="330" y="88.3"', comparison)

        for relative in (
            "assets/electronics/schematics/series-rule-reference.svg",
            "assets/electronics/schematics/parallel-rule-reference.svg",
            "assets/electronics/schematics/series-parallel-comparison.svg",
            "assets/electronics/schematics/kirchhoff-node-loop-reference.svg",
            "assets/electronics/schematics/series-parallel-example.png",
        ):
            self.assertTrue((SITE / relative).is_file(), relative)

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
        config = self.read("_quarto.yml")
        self.assertIn('"tej3-4/curriculum/**/*.qmd"', config)
        self.assertEqual(roadmap.count("| What students learn | Why it matters |"), 17)
        self.assertEqual(roadmap.count("**Subsections:**"), 17)
        self.assertEqual(roadmap.count("**Coming out of this section, students can:**"), 17)
        self.assertIn("Use the sidebar for lessons", roadmap)
        self.assertIn("Engineering Preparation Track collaboration map", roadmap)
        self.assertNotIn("| Consumables |", roadmap)
        self.assertNotIn("| Teacher notes |", roadmap)
        self.assertNotIn("| Estimated time |", roadmap)
        self.assertNotIn("| Student handout |", roadmap)
        self.assertNotIn("| Copyright or permissions |", roadmap)
        self.assertNotIn("data-tej-roadmap-status", roadmap)


if __name__ == "__main__":
    unittest.main()
