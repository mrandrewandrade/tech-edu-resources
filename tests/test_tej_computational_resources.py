import json
from pathlib import Path
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "site" / "assets"
NOTEBOOKS = ASSETS / "tej-computational" / "notebooks"


class TejComputationalResourceTests(unittest.TestCase):
    def test_local_jupyter_page_keeps_route_navigation(self) -> None:
        lesson = (
            ROOT
            / "site"
            / "tej3-4"
            / "computational-engineering"
            / "local-python-jupyter.qmd"
        ).read_text(encoding="utf-8")
        for phrase in (
            "toc: true",
            'toc-title: "On this page"',
            "## Choose your route",
            "## Route A: Windows with WSL",
            "## Route B: macOS",
            "## Route C: Linux",
            "## Route D: native Windows PowerShell",
            "## Route E: Google Colab",
            "https://colab.research.google.com/",
            "not the recommended course route",
        ):
            self.assertIn(phrase, lesson)

    def test_eleven_real_notebooks_have_required_learning_structure(self) -> None:
        paths = sorted(NOTEBOOKS.glob("*.ipynb"))
        self.assertEqual(len(paths), 11)
        required = (
            "Learning goal",
            "Why it matters",
            "Prior knowledge",
            "challenge",
            "Hint",
            "Common errors",
            "assert",
        )
        for path in paths:
            notebook = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(notebook["nbformat"], 4)
            text = "".join("".join(cell.get("source", [])) for cell in notebook["cells"])
            for phrase in required:
                self.assertIn(phrase.lower(), text.lower(), f"{phrase} missing from {path.name}")
            self.assertNotIn("## reflection", text.lower(), path.name)
            self.assertNotIn("finish this sentence", text.lower(), path.name)
            self.assertIn("help improve this lesson", text.lower(), path.name)
            if path.name != "00-python-first-steps.ipynb":
                self.assertIn("working demonstration", text.lower(), path.name)
            self.assertTrue(any(cell.get("cell_type") == "code" for cell in notebook["cells"]))

        first_steps = json.loads((NOTEBOOKS / "00-python-first-steps.ipynb").read_text(encoding="utf-8"))
        first_steps_text = "".join("".join(cell.get("source", [])) for cell in first_steps["cells"])
        for phrase in (
            "No previous Python",
            "Shift+Enter",
            "## Videos",
            "kqtD5dpn9C8",
            "Four basic types",
            "variable",
            "Keep several values together",
            "list",
            "Make a NumPy array",
            "NumPy array stores numbers in order",
            "np.array",
            "change only the middle number",
            "TASK 1 through TASK 6",
            "studentnumber-lastname-python-first-steps.ipynb",
        ):
            self.assertIn(phrase.lower(), first_steps_text.lower())
        for phrase in (
            "Reflection",
            "prediction",
            "My three answers",
            "Finish this sentence",
            "written answer",
            "Markdown prompt",
        ):
            self.assertNotIn(phrase.lower(), first_steps_text.lower())

        foundations = json.loads((NOTEBOOKS / "01-engineering-calculator.ipynb").read_text(encoding="utf-8"))
        foundations_text = "".join("".join(cell.get("source", [])) for cell in foundations["cells"])
        for phrase in (
            "NumPy arrays",
            "calculate_current_mA",
            "Boolean filter",
            "help(np.round)",
            "Command detective routine",
            "Read the **final line**",
            "Every numbered `TODO`",
            "studentnumber-lastname-jupyter-foundations.ipynb",
            "coding assignment",
            "matplotlib",
        ):
            self.assertIn(phrase.lower(), foundations_text.lower())

        bridge = json.loads((NOTEBOOKS / "03a-two-loop-to-matrix-bridge.ipynb").read_text(encoding="utf-8"))
        bridge_text = "".join("".join(cell.get("source", [])) for cell in bridge["cells"])
        for phrase in ("I_3=I_1-I_2", "numpy.linalg.solve", "sympy", "exact fractions", "residual"):
            self.assertIn(phrase.lower(), bridge_text.lower())

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

        notebook_archive = ASSETS / "tej-computational" / "tej-computational-engineering-notebooks.zip"
        with zipfile.ZipFile(notebook_archive) as archive:
            self.assertIn(
                "tej-computational-engineering/notebooks/00-python-first-steps.ipynb",
                archive.namelist(),
            )
            readme = archive.read("tej-computational-engineering/README.txt").decode("utf-8")
            self.assertIn("eleven notebooks", readme)
            self.assertIn(
                "tej-computational-engineering/notebooks/09-midterm-three-current-circuit.ipynb",
                archive.namelist(),
            )

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
