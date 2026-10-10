from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class NotesRefactorTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (SITE / relative).read_text(encoding="utf-8")

    def test_public_navigation_is_small_and_has_no_ai_literacy_unit(self) -> None:
        config = self.read("_quarto.yml")
        self.assertNotIn("AI Literacy", config)
        self.assertNotIn("Language Models & AI", config)
        for path in (
            "tej3-4/circuits/index.qmd",
            "tej3-4/linux-operating-systems/index.qmd",
            "design-fabrication/design-process/index.qmd",
            "design-fabrication/logo-design/index.qmd",
        ):
            self.assertIn(path, config)

    def test_canonical_sidebar_links_do_not_use_numbered_slugs(self) -> None:
        config = self.read("_quarto.yml")
        sidebar = config.split("  sidebar:", 1)[1].split("  page-footer:", 1)[0]
        self.assertNotRegex(sidebar, r"href: (?:tej3-4|design-fabrication)/\d{2}-")

    def test_circuits_page_has_the_requested_topics_and_artifacts(self) -> None:
        circuits = self.read("tej3-4/circuits/index.qmd")
        for text in (
            "Significant figures",
            "Scientific notation",
            "Engineering notation",
            "Metric",
            "Ohm's law",
            "Electrical power",
            "GUESS method",
            "Series circuits",
            "11ooJTlUf7ckOjkTP9eyJr8FyojWuOHV9-IFjZ5IoCeA",
            "1Ux3gAje5iED6vO_gBcF7SbaBJ5TJkV5RqJmkc6XFtDw",
            "1KMKU3e4OkKn40jMy5KeyGHXKcn2IftQcRiNggfYHivc",
            "1CQf3eYAcKw6tf2J7BCa38cskxnGP0T3fjBaxnLKbx-o",
            "1DyGsEwpLrrwSRnyMXN5kze2qRYFoAY2t-P09wnfUS6c",
        ):
            self.assertIn(text, circuits)
        self.assertNotIn("1_pH0LLfqyt0QOZPGVGsXNW0tGNeG2ksXh0ysAUQLF94", circuits)
        self.assertIn("not public yet", circuits)

    def test_logo_page_is_make_first_and_has_all_requested_videos(self) -> None:
        logo = self.read("design-fabrication/logo-design/index.qmd")
        for text in ("Photopea", "GIMP", "Adobe Photoshop"):
            self.assertIn(text, logo)
        for video_id in ("mchoizRTY-s", "t9V6Wp_OnQk", "QmB14oyGWcw", "6dwSRbkSuq8"):
            self.assertIn(video_id, logo)

    def test_design_process_reuses_the_class_deck_and_videos(self) -> None:
        process = self.read("design-fabrication/design-process/index.qmd")
        for text in (
            "Situation",
            "N: Needs",
            "I: Inquiry",
            "C: Create and Communicate",
            "E: Evaluate",
            "1bQBt0WHBp6ca0RWtQHBHKbfqhzXMc4q4uUOJ8hHxvIQ",
            "Vcma79mVAYw",
            "3wRWN3_u17k",
        ):
            self.assertIn(text, process)

    def test_old_linux_urls_are_redirects_to_number_free_pages(self) -> None:
        expectations = {
            "tej3-4/09-linux-operating-systems/index.qmd": "../linux-operating-systems/",
            "tej3-4/09-linux-operating-systems/01-choosing-a-distribution.qmd": "../linux-operating-systems/choosing-a-distribution.html",
            "tej3-4/09-linux-operating-systems/02-install-linux-mint.qmd": "../linux-operating-systems/install-linux-mint.html",
        }
        for path, destination in expectations.items():
            source = self.read(path)
            self.assertIn('http-equiv="refresh"', source)
            self.assertIn(destination, source)


if __name__ == "__main__":
    unittest.main()
