from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "site" / "data" / "tej-curriculum.yml"
PAGE = ROOT / "site" / "tej3-4" / "curriculum" / "index.qmd"


class TejCurriculumTests(unittest.TestCase):
    def test_validation_script(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/validate_tej_curriculum.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Validated 17 units", result.stdout)

    def test_sequence_and_required_topics(self) -> None:
        data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
        self.assertEqual(
            [str(unit["unit_id"]) for unit in data["units"]],
            [str(index) for index in range(17)],
        )
        modules = {
            module["module_id"]: module
            for unit in data["units"]
            for module in unit["modules"]
        }
        self.assertIn("grounded switch", modules["DL03"]["short_description"].lower())
        self.assertIn("binary test order", modules["DL06"]["title"].lower())
        self.assertEqual(modules["CSB01"]["status"], "Published")
        self.assertIn("calculation bridge", modules["CSB01"]["title"].lower())
        self.assertIn("lab shell", modules["CSP01"]["title"].lower())
        self.assertEqual(modules["CSP01"]["status"], "In development")

    def test_public_page_excludes_private_workbook(self) -> None:
        page = PAGE.read_text(encoding="utf-8").lower()
        self.assertNotIn("docs.google.com/spreadsheets", page)
        self.assertNotIn("1jlhg9kwlaaxxwbvpbg9otsc8zrvdactu9ej1p-5dtay", page)
        self.assertIn("data-tej-roadmap-search", page)


if __name__ == "__main__":
    unittest.main()
