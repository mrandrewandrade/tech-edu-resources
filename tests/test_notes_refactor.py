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
        config = self.read("_quarto.yml") + self.read("_course-navigation.yml")
        self.assertNotIn("AI Literacy", config)
        self.assertNotIn("Language Models & AI", config)
        for path in (
            "tej3-4/circuits/**/*.qmd",
            "tej3-4/electronics-library/index.qmd",
            "tej3-4/linux-operating-systems/index.qmd",
            "design-fabrication/design-process/index.qmd",
            "design-fabrication/logo-design/index.qmd",
        ):
            self.assertIn(path, config)

    def test_canonical_sidebar_links_do_not_use_numbered_slugs(self) -> None:
        sidebar = self.read("_course-navigation.yml")
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
            "12rTTMbWPdcCYSY07amSF5Ap3b0m08L5NT6NM4pAba_g",
            "1CQf3eYAcKw6tf2J7BCa38cskxnGP0T3fjBaxnLKbx-o",
            "1_Fiz7KlHHEtBQxfQKmXDNkuWB2RxrWcGWmWvCXh2Iqs",
            "1AIOR80hBtAXB8klvf509k_TjPQGi4dZ3Wlv_1dJtDK4",
            "1qOS16EaUEUCnIGm16eN_7o76OlFKHrzABY3nfJ-v4i8",
            "1DmXKhtsC0AEfR24zmJSCQgU_JLvrGYfIFtn9nOvnmbI",
            "TEJ-Electronics-Quick-Reference.pdf",
            "1RCkfqUT5U0FMKTOJ_ScyiDLmiGF-bCpyo-6y6Pm8ZUo",
        ):
            self.assertIn(text, circuits)
        self.assertIn("answer-key files are not linked publicly", circuits)
        self.assertNotIn("1DyGsEwpLrrwSRnyMXN5kze2qRYFoAY2t-P09wnfUS6c", circuits)

    def test_screen_reader_callout_labels_are_visually_hidden(self) -> None:
        shared_css = self.read("assets/bs-shared.css")
        self.assertIn(".screen-reader-only", shared_css)
        self.assertIn("clip: rect(0, 0, 0, 0)", shared_css)

    def test_student_circuit_pages_exclude_legacy_and_internal_drive_files(self) -> None:
        circuit_sources = [
            SITE / "data" / "course-notes.json",
            *(SITE / "tej3-4" / "circuits").glob("*.qmd"),
            *(SITE / "tej3-4" / "electronics-library").rglob("*.qmd"),
        ]
        published = "\n".join(path.read_text(encoding="utf-8") for path in circuit_sources)
        for private_or_legacy_id in (
            "1KMKU3e4OkKn40jMy5KeyGHXKcn2IftQcRiNggfYHivc",
            "1dGTCgCEVFoxy-M1k4z1qiO31_7Wke69xmd51EnQCGUA",
            "1pKpmcnNJlRVb74YJNFDIcpXS6LeGvjkO1e3KAgAD8JE",
            "1BV2n5NBiJdxmmApagaIntdaDYWowiO4aZiF_VQ3_FHQ",
            "1BxFm8SGSaiEf2NTi_Um7zXlwIjojd0l_hTR0ObwsvGo",
            "1e28pwYXns0sP_EEKAn5sgBCidKrcajucV0sRy3nJxe8",
            "1W3qPw_MyG4iw_SO3Trvovaj_qEZQXwARG_rgWk7OTeQ",
            "1sIm21ehqLgxend99TToo9h7sWII-UbTT8m0at0NM6z8",
            "1Ux3gAje5iED6vO_gBcF7SbaBJ5TJkV5RqJmkc6XFtDw",
            "1blpn_hyzYhFTDt4BcNBgL9C7bqE17oJZ",
            "1JLy3619EgPdDzOVuuR9s3xc9SfCIk911I0xk1CRZicM",
            "1UXOjPUkv4sqgA96DttE2onmgWlp_k5CRAhmTiq2dkAU",
            "1J3Wf2mPp0UHAIjWphWWiRx7wtk9TbDPhLshayqw_pVE",
            "1unYhScz8OdePXy0d2gLM8oRjatb6r2RbNjfSUGRfyVY",
        ):
            self.assertNotIn(private_or_legacy_id, published)

    def test_logo_page_is_make_first_and_has_all_requested_videos(self) -> None:
        logo = self.read("design-fabrication/logo-design/index.qmd")
        for text in ("Photopea", "GIMP", "Adobe Photoshop"):
            self.assertIn(text, logo)
        for video_id in ("mchoizRTY-s", "t9V6Wp_OnQk", "QmB14oyGWcw", "6dwSRbkSuq8"):
            self.assertIn(video_id, logo)

    def test_design_process_reuses_the_class_deck_and_videos(self) -> None:
        process = self.read("design-fabrication/design-process/index.qmd") + self.read(
            "includes/generated/design-fabrication-design-process-toc.md"
        )
        for text in (
            "Understand the Situation",
            "Record User Needs",
            "Necessities and Nice-to-Haves",
            "Rank Priorities",
            "Investigate and Inquire",
            "Create and Communicate",
            "Evaluate and Repeat",
            "Supply Chain and Life Cycle",
            "1bQBt0WHBp6ca0RWtQHBHKbfqhzXMc4q4uUOJ8hHxvIQ",
            "19ObkJz3sYVXwB9VkNUiybXZGZ-ihuGw1FarRj81LtAo",
            "1c-7TbI3IMOicnHsTUSLkGNJ4s1i2OA6d458S2bTZ2ho",
            "1T6f3beZhKXiOxS1ecXt3FHbam2yOqeP1yXrmaLFSbAs",
            "1F_7NWcW4Bzd-PE7BdLssdBxeT-49clS92381QXjW8gw",
            "173eivGi-7of6WWqpPsK81p4Z2Q6_3fIiW5ffjRI6jRQ",
            "1QWY7ss3aY5wHh4ETOcSDGZxgpkrrIXcCYnWlXNv1lxo",
            "1O_j4gcsUT0ELFpgJk3GiyG6B1l5brKPko-6lO8HQPfk",
            "1Sai4_cQGkNudnAsLRYuwec6D-B-U4BqA8CCk0Nyo0CA",
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
