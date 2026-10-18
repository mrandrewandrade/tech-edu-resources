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


if __name__ == "__main__":
    unittest.main()
