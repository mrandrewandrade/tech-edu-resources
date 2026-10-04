from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CURRICULUM = SITE / "design-fabrication"


class DesignFabricationTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (SITE / relative).read_text(encoding="utf-8")

    def test_canonical_curriculum_structure_exists(self) -> None:
        required = [
            "index.qmd",
            "01-nice-design-process/index.qmd",
            "02-digital-design/index.qmd",
            "03-laser-cutting/index.qmd",
            "04-3d-printing/index.qmd",
            "05-cnc-digital-machining/index.qmd",
            "06-textiles-soft-goods/index.qmd",
            "07-other-fabrication/index.qmd",
            "applications/index.qmd",
            "applications/exploring-technologies/index.qmd",
            "applications/technological-design/index.qmd",
            "applications/manufacturing/index.qmd",
            "applications/construction/index.qmd",
            "applications/transportation/index.qmd",
            "applications/computer-technology/index.qmd",
            "applications/communications-technology/index.qmd",
            "applications/green-industries/index.qmd",
            "applications/hairstyling-aesthetics/index.qmd",
            "applications/hospitality-tourism/index.qmd",
            "applications/health-care/index.qmd",
        ]
        for relative in required:
            self.assertTrue((CURRICULUM / relative).is_file(), relative)

    def test_navigation_is_educator_first(self) -> None:
        config = self.read("_quarto.yml")
        educator = config.index("text: Educator Resources")
        classes = config.index("text: Classes")
        self.assertLess(educator, classes)
        ordered = ["General Slides", "General Materials", "General Design & Fabrication", "TEJ Notes"]
        positions = [config.index(item, educator) for item in ordered]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn('title: "TAS Notes"', config)

    def test_homepage_prioritizes_reusable_resources(self) -> None:
        home = self.read("index.qmd")
        self.assertLess(home.index("Educator resources"), home.index("Current class slides"))
        self.assertLess(home.index("General Slides"), home.index("General Materials"))
        self.assertIn("design-fabrication/index.qmd", home)

    def test_laser_curriculum_has_all_eight_projects(self) -> None:
        laser = self.read("design-fabrication/03-laser-cutting/index.qmd")
        for name in (
            "Name + Logo",
            "Make It Stand",
            "Measure + Place",
            "Material Fit + Calibration",
            "Assemblies + Hybrid Fabrication",
            "Tool Holder",
            "Wall + Bench Tool Module",
            "Design &amp; Fabrication Capstone",
        ):
            self.assertIn(name, laser)

    def test_curriculum_relevance_is_varied_and_compact(self) -> None:
        pages = list(CURRICULUM.rglob("*.qmd"))
        relevance_pages = [p for p in pages if "ter-curriculum-relevance" in p.read_text(encoding="utf-8")]
        self.assertGreaterEqual(len(relevance_pages), 20)
        main = (CURRICULUM / "index.qmd").read_text(encoding="utf-8")
        for code in ("TIJ1O", "TDJ", "TMJ", "TGJ", "TEJ", "TCJ", "THJ", "TTJ"):
            self.assertIn(code, main)

    def test_application_layer_is_cross_process_and_substantial(self) -> None:
        landing = self.read("design-fabrication/applications/index.qmd")
        self.assertIn("The fabrication method is transferable", landing)
        for code in ("TIJ1O", "TDJ2O", "TMJ2O", "TCJ2O", "TTJ2O", "TEJ2O", "TGJ2O", "THJ2O", "TXJ2O", "TFJ2O", "TPJ2O"):
            self.assertIn(code, landing)
        pages = list((CURRICULUM / "applications").glob("*/index.qmd"))
        self.assertEqual(len(pages), 11)
        for page in pages:
            content = page.read_text(encoding="utf-8")
            self.assertGreaterEqual(content.count("ter-project-card"), 3, page)
            for field in ("<dt>Process", "<dt>Skills", "<dt>Material", "<dt>Structural", "<dt>Safety", "<dt>Library", "<dt>Lesson", "<dt>Extension"):
                self.assertIn(field, content, (page, field))

    def test_sensitive_application_pages_state_boundaries(self) -> None:
        hair = self.read("design-fabrication/applications/hairstyling-aesthetics/index.qmd").lower()
        hospitality = self.read("design-fabrication/applications/hospitality-tourism/index.qmd").lower()
        health = self.read("design-fabrication/applications/health-care/index.qmd").lower()
        self.assertIn("heat-safe", hair)
        self.assertIn("food-contact", hospitality)
        self.assertIn("not medical devices", health)

    def test_course_code_queries_have_specific_pages(self) -> None:
        expectations = {
            "TDJ2O laser cutting": "design-fabrication/03-laser-cutting/index.qmd",
            "TMJ2O 3d printing": "design-fabrication/04-3d-printing/index.qmd",
            "TTJ tool holder": "design-fabrication/03-laser-cutting/06-tool-holder.qmd",
            "TGJ logo": "design-fabrication/02-digital-design/03-logos-lettermarks.qmd",
            "Ontario curriculum design process": "design-fabrication/01-nice-design-process/index.qmd",
        }
        for query, relative in expectations.items():
            words = re.findall(r"[a-z0-9]+", query.lower())
            content = self.read(relative).lower()
            self.assertTrue(all(word in content for word in words), (query, relative))

    def test_old_tas_route_is_redirect_only(self) -> None:
        old = self.read("tas2/index.qmd")
        self.assertIn("http-equiv=\"refresh\"", old)
        self.assertIn("rel=\"canonical\"", old)
        self.assertIn("design-fabrication", old)
        self.assertNotIn("TAS Notes", old)

    def test_library_and_curriculum_cross_link(self) -> None:
        library = self.read("teaching-materials/laser-cutting/index.qmd")
        curriculum = self.read("design-fabrication/03-laser-cutting/index.qmd")
        self.assertIn("design-fabrication/03-laser-cutting", library)
        self.assertIn("teaching-materials/laser-cutting", curriculum)

    def test_first_laser_projects_toolkit_is_complete(self) -> None:
        toolkit = self.read("design-fabrication/03-laser-cutting/resources/index.qmd")
        for label in ("Basic Geometry", "Hole", "Slot", "Structure", "Wall + Mounting", "Organizer"):
            self.assertIn(label, toolkit)
        for relative in (
            "design-fabrication/03-laser-cutting/resources/fabrication-planning-worksheet.qmd",
            "design-fabrication/03-laser-cutting/resources/paper-to-inkscape.qmd",
            "design-fabrication/03-laser-cutting/resources/pill-bottle-organizer.qmd",
            "design-fabrication/03-laser-cutting/resources/active-sequence-slides.qmd",
        ):
            self.assertTrue((SITE / relative).is_file(), relative)

        first_project = self.read("design-fabrication/03-laser-cutting/01-name-logo.qmd")
        self.assertIn("pre-cut", first_project)
        self.assertIn("Photopea", first_project)
        self.assertIn("export", first_project.lower())
        self.assertIn("PNG", first_project)

        organizer = self.read("design-fabrication/03-laser-cutting/resources/pill-bottle-organizer.qmd")
        for design in ("Simple shelf", "Dowel-supported", "Reinforced wall", "Removable wall / bench"):
            self.assertIn(design, organizer)
        self.assertIn("unverified", organizer)

    def test_public_classroom_kit_has_palettes_and_reference_assemblies(self) -> None:
        kit = SITE / "assets" / "laser-library" / "classroom-kit"
        self.assertTrue((kit / "manifest.json").is_file())
        self.assertEqual(len(list((kit / "palettes").glob("*.svg"))), 6)
        assembly = __import__("json").loads((kit / "pill-bottle" / "assemblies.json").read_text(encoding="utf-8"))
        self.assertEqual(len(assembly["designs"]), 4)


if __name__ == "__main__":
    unittest.main()
