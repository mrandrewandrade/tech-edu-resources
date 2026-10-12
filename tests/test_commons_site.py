import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import check_site, commons_glossary


class CommonsChecks(unittest.TestCase):
    def test_detects_missing_asset_and_fragment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'index.html').write_text('<a href="#missing">Link</a><img src="absent.png">', encoding='utf-8')
            _, errors = check_site.check(root)
            self.assertTrue(any('Missing fragment: index.html: #missing' in error for error in errors))
            self.assertTrue(any('Missing target: index.html: absent.png' in error for error in errors))

    def test_detects_public_qmd_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'index.html').write_text('<a href="lesson.qmd">Lesson</a>', encoding='utf-8')
            (root / 'lesson.qmd').write_text('source', encoding='utf-8')
            _, errors = check_site.check(root)
            self.assertTrue(any('Public .qmd link: index.html: lesson.qmd' in error for error in errors))

    def test_glossary_rejects_stale_presentation_with_matching_count(self):
        with mock.patch.object(commons_glossary.learn_glossary, 'build_entries_html', return_value='stale'):
            with self.assertRaisesRegex(commons_glossary.learn_glossary.ValidationError, 'Stale glossary presentation'):
                commons_glossary.validate_current_presentation()
