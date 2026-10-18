from __future__ import annotations

import unittest
from pathlib import Path
from zipfile import ZipFile, is_zipfile


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
KIT_SOURCE = ROOT / "offline-kits" / "linux"
KIT_ZIP = SITE / "assets" / "linux" / "TEJ-Linux-Offline-Kit.zip"
QUICK_START = SITE / "assets" / "linux" / "TEJ-Linux-Offline-Kit-Quick-Start.pdf"


class LinuxOfflineKitTests(unittest.TestCase):
    def test_public_page_and_explore_lesson_link_the_kit(self) -> None:
        page = SITE / "tej3-4" / "linux-operating-systems" / "offline-kit" / "index.qmd"
        explore = SITE / "tej3-4" / "linux-operating-systems" / "explore-linux.qmd"
        self.assertIn("TEJ-Linux-Offline-Kit.zip", page.read_text(encoding="utf-8"))
        self.assertIn(
            "TEJ-Linux-Offline-Kit-Quick-Start.pdf",
            page.read_text(encoding="utf-8"),
        )
        self.assertIn("Linux Offline Kit", explore.read_text(encoding="utf-8"))
        self.assertTrue(QUICK_START.read_bytes().startswith(b"%PDF-"))
        self.assertGreater(QUICK_START.stat().st_size, 5_000)

    def test_editable_assignments_and_fallbacks_are_present(self) -> None:
        for stem in (
            "Terminal-Quest",
            "Linux-Mint-Xfce-Appearance",
            "Bashcrawl-Terminal-Adventure",
        ):
            for suffix in ("docx", "odt", "pdf"):
                path = KIT_SOURCE / "assignments" / f"{stem}.{suffix}"
                self.assertTrue(path.is_file(), path)
                self.assertGreater(path.stat().st_size, 10_000, path)
            self.assertTrue((KIT_SOURCE / "answers" / f"{stem}-Answers.txt").is_file())

        for suffix in ("docx", "odt"):
            for path in (KIT_SOURCE / "assignments").glob(f"*.{suffix}"):
                self.assertTrue(is_zipfile(path), path)
        for path in (KIT_SOURCE / "assignments").glob("*.pdf"):
            self.assertTrue(path.read_bytes().startswith(b"%PDF-"), path)

    def test_zip_contains_bashcrawl_hidden_rooms_and_licence(self) -> None:
        self.assertTrue(KIT_ZIP.is_file())
        with ZipFile(KIT_ZIP) as archive:
            names = set(archive.namelist())
        prefix = "TEJ-Linux-Offline-Kit/"
        self.assertIn(prefix + "START-HERE.html", names)
        self.assertIn(prefix + "PRINTABLE-QUICK-START.pdf", names)
        self.assertIn(prefix + "tej-xfce-style.sh", names)
        self.assertIn(prefix + "bashcrawl/LICENSE", names)
        self.assertTrue(any("/bashcrawl/entrance/.chapel/" in name for name in names))
        self.assertFalse(any("/.git/" in name for name in names))
        self.assertFalse(any("answer key" in name.lower() for name in names))

    def test_phone_support_and_difficulty_warning_are_consistent(self) -> None:
        warning = "slower and more difficult"
        text_sources = (
            SITE / "tej3-4" / "linux-operating-systems" / "index.qmd",
            SITE / "tej3-4" / "linux-operating-systems" / "explore-linux.qmd",
            SITE / "tej3-4" / "linux-operating-systems" / "offline-kit" / "index.qmd",
            KIT_SOURCE / "README.txt",
            KIT_SOURCE / "START-HERE.html",
            ROOT / "scripts" / "create_linux_offline_quick_start.py",
        )
        for path in text_sources:
            self.assertIn(warning, path.read_text(encoding="utf-8"), path)

        assignment_xml = (
            ("Terminal-Quest.docx", "word/document.xml"),
            ("Terminal-Quest.odt", "content.xml"),
            ("Bashcrawl-Terminal-Adventure.docx", "word/document.xml"),
            ("Bashcrawl-Terminal-Adventure.odt", "content.xml"),
        )
        for filename, xml_name in assignment_xml:
            path = KIT_SOURCE / "assignments" / filename
            with ZipFile(path) as archive:
                content = archive.read(xml_name).decode("utf-8")
            self.assertIn(warning, content, path)


if __name__ == "__main__":
    unittest.main()
