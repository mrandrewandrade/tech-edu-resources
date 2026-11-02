import json
from pathlib import Path
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "site" / "assets"
NOTEBOOKS = ASSETS / "tej-computational" / "notebooks"


class TejComputationalResourceTests(unittest.TestCase):
    def test_eight_real_notebooks_have_required_learning_structure(self) -> None:
        paths = sorted(NOTEBOOKS.glob("*.ipynb"))
        self.assertEqual(len(paths), 8)
        required = (
            "Learning goal",
            "Why it matters",
            "Prior knowledge",
            "Working demonstration",
            "challenge",
            "Hint",
            "Common errors",
            "Reflection",
            "assert",
        )
        for path in paths:
            notebook = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(notebook["nbformat"], 4)
            text = "".join("".join(cell.get("source", [])) for cell in notebook["cells"])
            for phrase in required:
                self.assertIn(phrase.lower(), text.lower(), f"{phrase} missing from {path.name}")
            self.assertTrue(any(cell.get("cell_type") == "code" for cell in notebook["cells"]))

    def test_downloads_and_dataset_exist(self) -> None:
        dataset = ASSETS / "tej-computational" / "data" / "circuit-measurements.csv"
        self.assertIn("measured_current_mA", dataset.read_text(encoding="utf-8"))
        for archive_path in (
            ASSETS / "tej-computational" / "tej-computational-engineering-notebooks.zip",
            ASSETS / "tej-portfolio" / "quarto-portfolio-starter.zip",
        ):
            self.assertTrue(zipfile.is_zipfile(archive_path), archive_path)
            with zipfile.ZipFile(archive_path) as archive:
                self.assertGreater(len(archive.namelist()), 5)

    def test_template_uses_native_search_listing_and_accessible_images(self) -> None:
        template = ROOT / "student-templates" / "quarto-portfolio-starter"
        config = (template / "_quarto.yml").read_text(encoding="utf-8")
        listing = (template / "projects" / "index.qmd").read_text(encoding="utf-8")
        self.assertIn("search:", config)
        self.assertIn("type: grid", listing)
        self.assertIn("sort-ui:", listing)
        self.assertIn("filter-ui:", listing)
        self.assertIn("categories: true", listing)
        for project in (template / "projects").glob("*.qmd"):
            if project.name != "index.qmd":
                self.assertIn("image-alt:", project.read_text(encoding="utf-8"), project.name)


if __name__ == "__main__":
    unittest.main()
