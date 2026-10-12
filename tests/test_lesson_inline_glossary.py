from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "learn_glossary.py"
SPEC = importlib.util.spec_from_file_location("learn_glossary_iteration03", MODULE_PATH)
assert SPEC and SPEC.loader
learn_glossary = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(learn_glossary)

PANDOC = Path(r"C:\Program Files\Quarto\bin\tools\pandoc.exe")
FILTER = (
    ROOT
    / "site"
    / "_extensions"
    / "bs-inline-glossary"
    / "bs-inline-glossary.lua"
)
LOOKUP = ROOT / "site" / "assets" / "bs-glossary-lookup.json"
FIXTURES = ROOT / "tests" / "fixtures" / "iteration03"


class LessonInlineGlossaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not PANDOC.exists():
            raise unittest.SkipTest(f"Bundled Pandoc not found at {PANDOC}")
        data = json.loads(learn_glossary.PUBLIC_DATA_PATH.read_text(encoding="utf-8"))
        cls.entries = learn_glossary.validate_public_data(data)

    def render(
        self,
        source: str,
        *,
        lookup_path: Path = LOOKUP,
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["BS_GLOSSARY_LOOKUP"] = str(lookup_path)
        return subprocess.run(
            [
                str(PANDOC),
                "--from",
                "markdown",
                "--to",
                "html",
                "--lua-filter",
                str(FILTER),
            ],
            cwd=ROOT,
            env=environment,
            input=source,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

    def highlighted_source(self) -> str:
        return (FIXTURES / "highlighted-lesson.qmd").read_text(encoding="utf-8")

    def control_source(self) -> str:
        return (FIXTURES / "control-lesson.qmd").read_text(encoding="utf-8")

    def test_highlighted_fixture_uses_only_first_safe_canonical_occurrences(self) -> None:
        result = self.render(self.highlighted_source())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count('class="bs-inline-glossary"'), 2)
        self.assertIn('data-bs-glossary-slug="voltage">voltage</a>', result.stdout)
        self.assertIn(
            'data-bs-glossary-slug="current">current</a>',
            result.stdout,
        )
        self.assertIn('href="https://andrewandrade.ca/tech-edu-resources/glossary/#voltage"', result.stdout)
        self.assertIn('href="https://andrewandrade.ca/tech-edu-resources/glossary/#current"', result.stdout)
        self.assertIn(
            "Voltage appears again, and Current appears again",
            result.stdout,
        )

    def test_excluded_contexts_and_visible_wording_remain_unchanged(self) -> None:
        result = self.render(self.highlighted_source())
        self.assertEqual(result.returncode, 0, result.stderr)
        heading = result.stdout.split("</h1>", 1)[0]
        self.assertNotIn("bs-inline-glossary", heading)
        self.assertIn('href="https://example.com/voltage"', result.stdout)
        self.assertIn("<code>current in inline code</code>", result.stdout)
        self.assertIn("Voltage and Electric Current in a fenced code block.", result.stdout)
        self.assertIn('class="math inline"', result.stdout)
        self.assertRegex(
            result.stdout,
            r'class="fixture-raw">Voltage and Electric Current in raw\s+HTML\.</span>',
        )
        self.assertIn('alt="Voltage and Electric Current in a caption."', result.stdout)
        self.assertNotIn("data-bs-glossary-summary", result.stdout)
        self.assertNotIn("short_definition=", result.stdout)

    def test_control_lesson_has_no_inline_markup(self) -> None:
        result = self.render(self.control_source())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("bs-inline-glossary", result.stdout)
        self.assertIn("Voltage and Electric Current appear in ordinary prose", result.stdout)

    def test_broad_terms_still_drive_all_backlinks(self) -> None:
        lesson = {
            "relative_path": "fixture.qmd",
            "categories": ["Beginner"],
            "tags": ["Checker Play"],
            "terms": ["voltage", "resistance", "current", "ampere"],
            "highlighted_terms": ["voltage", "current"],
            "title": "Fixture",
        }
        related = learn_glossary.validate_lessons([lesson], self.entries)
        self.assertEqual(
            set(related),
            {"voltage", "resistance", "current", "ampere"},
        )
        self.assertEqual(
            lesson["terms"],
            ["voltage", "resistance", "current", "ampere"],
        )
        self.assertEqual(
            lesson["highlighted_terms"],
            ["voltage", "current"],
        )

    def test_absent_and_empty_highlighted_metadata_disable_highlighting(self) -> None:
        self.assertEqual(
            learn_glossary.highlighted_terms_from_metadata({}, "Fixture"),
            [],
        )
        self.assertEqual(
            learn_glossary.highlighted_terms_from_metadata(
                {"highlighted-terms": []},
                "Fixture",
            ),
            [],
        )

    def test_highlighted_metadata_must_be_a_list(self) -> None:
        with self.assertRaisesRegex(
            learn_glossary.ValidationError,
            "must be a YAML list",
        ):
            learn_glossary.highlighted_terms_from_metadata(
                {"highlighted-terms": "ace"},
                "Fixture",
            )

    def test_duplicate_normalized_values_fail(self) -> None:
        with self.assertRaisesRegex(
            learn_glossary.ValidationError,
            "duplicate normalized",
        ):
            learn_glossary.highlighted_terms_from_metadata(
                {"highlighted-terms": ["ace", "Ace"]},
                "Fixture",
            )

    def test_malformed_multi_word_slug_fails(self) -> None:
        with self.assertRaisesRegex(
            learn_glossary.ValidationError,
            "malformed",
        ):
            learn_glossary.highlighted_terms_from_metadata(
                {"highlighted-terms": ["active builder"]},
                "Fixture",
            )

    def test_unknown_alias_and_missing_broad_term_fail(self) -> None:
        base = {
            "relative_path": "fixture.qmd",
            "categories": ["Beginner"],
            "tags": ["Checker Play"],
            "terms": ["voltage"],
            "title": "Fixture",
        }
        cases = (
            (
                {**base, "highlighted_terms": ["not-a-term"]},
                "unknown term slug",
            ),
            (
                {
                    **base,
                    "terms": ["current"],
                    "highlighted_terms": ["electric-current"],
                },
                "uses alias slug",
            ),
            (
                {**base, "highlighted_terms": ["current"]},
                "missing from terms",
            ),
        )
        for lesson, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(
                    learn_glossary.ValidationError,
                    message,
                ):
                    learn_glossary.validate_lessons([lesson], self.entries)

    def test_longest_valid_phrase_wins_without_partial_word_matches(self) -> None:
        source = """---
terms: [one-point, point]
highlighted-terms: [point, one-point]
---

Checkpoint is not a match. One Point comes first; point comes second.
"""
        result = self.render(
            source,
            lookup_path=FIXTURES / "longest-phrase-lookup.json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('>point</a> is not', result.stdout)
        first = result.stdout.index('data-bs-glossary-slug="one-point"')
        second = result.stdout.index('data-bs-glossary-slug="point"')
        self.assertLess(first, second)

    def test_canonical_phrase_wins_over_an_ambiguous_alias(self) -> None:
        source = """---
terms: [anchor, holding-point]
highlighted-terms: [anchor, holding-point]
---

Anchor and Holding Point.
"""
        result = self.render(
            source,
            lookup_path=FIXTURES / "ambiguous-phrase-lookup.json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('data-bs-glossary-slug="anchor">Anchor</a>', result.stdout)
        self.assertRegex(
            result.stdout,
            r'data-bs-glossary-slug="holding-point">Holding\s+Point</a>',
        )

    def test_existing_link_is_not_nested_and_missing_safe_match_warns(self) -> None:
        source = """---
terms: [voltage]
highlighted-terms: [voltage]
---

[Voltage](https://example.com/voltage)
"""
        result = self.render(source)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("<a "), 1)
        self.assertNotIn("bs-inline-glossary", result.stdout)
        self.assertIn("no safe prose occurrence for voltage", result.stderr)

    def test_rendering_is_byte_deterministic_and_metadata_order_independent(self) -> None:
        first = self.render(self.highlighted_source())
        second_source = self.highlighted_source().replace(
            "  - voltage\n  - current\n",
            "  - current\n  - voltage\n",
        )
        second = self.render(second_source)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first.stdout.encode("utf-8"), second.stdout.encode("utf-8"))

    def test_generated_lookup_always_has_canonical_short_definitions(self) -> None:
        data = json.loads(LOOKUP.read_text(encoding="utf-8"))
        by_slug = {entry["slug"]: entry for entry in data["entries"]}
        for slug in ("voltage", "resistance", "current", "ampere"):
            self.assertIsInstance(by_slug[slug]["short_definition"], str)
            self.assertTrue(by_slug[slug]["short_definition"])
        self.assertEqual(
            by_slug["current"]["aliases"],
            ["Electric Current", "I"],
        )
        self.assertEqual(
            by_slug["current"]["alias_slugs"],
            ["electric-current", "i"],
        )

    def test_client_hover_focus_and_slug_only_contract(self) -> None:
        javascript = (ROOT / "site" / "assets" / "bs-learn.js").read_text(
            encoding="utf-8"
        )
        glossary_html = (
            ROOT / "site" / "glossary" / "_entries.html"
        ).read_text(encoding="utf-8")
        self.assertIn("function canonicalShortDefinition(entries, slug)", javascript)
        self.assertIn("entry.short_definition", javascript)
        self.assertIn(
            '".bs-inline-glossary[data-bs-glossary-slug]"',
            javascript,
        )
        self.assertIn('link.addEventListener("mouseenter"', javascript)
        self.assertIn('link.addEventListener("focus"', javascript)
        self.assertIn('link.addEventListener("blur"', javascript)
        self.assertIn('link.addEventListener("click"', javascript)
        self.assertIn("Click for full definition", javascript)
        self.assertIn('"bs:open-glossary-term"', javascript)
        self.assertIn("renderLookupResult(result, entry", javascript)
        self.assertIn("link.dataset.bsGlossarySlug", javascript)
        self.assertIn("inlineGlossaryTooltipPosition", javascript)
        self.assertIn('window.addEventListener("resize"', javascript)
        self.assertIn('window.addEventListener("scroll"', javascript)
        self.assertNotIn("dataset.bsGlossarySummary", javascript)
        self.assertIn(
            'class="bs-inline-glossary"',
            glossary_html,
        )
        self.assertNotIn(
            'data-bs-glossary-slug="ampere" '
            'data-bs-definition-link="ampere">Ampere</a>',
            glossary_html,
        )
        self.assertIn(
            'data-bs-glossary-slug="current" '
            'data-bs-definition-link="current">current</a>',
            glossary_html,
        )




    def test_real_research_article_uses_the_same_highlight_contract(self) -> None:
        articles = learn_glossary.discover_research_articles()
        if not articles:
            self.skipTest("No research articles are part of the current public build")
        selected = next(
            article
            for article in articles
            if article["relative_path"]
            == "research/sage-vs-gnu-additional-details.qmd"
        )
        self.assertEqual(selected["highlighted_terms"], [])
        self.assertIn("equity", selected["terms"])
        related = learn_glossary.validate_research_articles(
            articles,
            self.entries,
        )
        self.assertNotIn("equity", related)

        result = self.render(selected["path"].read_text(encoding="utf-8"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('data-bs-glossary-slug="equity"', result.stdout)

    def test_research_highlighted_term_must_be_canonical_and_in_terms(self) -> None:
        base = {
            "relative_path": "research/fixture.qmd",
            "terms": ["current"],
            "highlighted_terms": ["electric-current"],
            "title": "Fixture",
        }
        with self.assertRaisesRegex(
            learn_glossary.ValidationError,
            "uses alias slug",
        ):
            learn_glossary.validate_research_articles([base], self.entries)
        base["highlighted_terms"] = ["voltage"]
        with self.assertRaisesRegex(
            learn_glossary.ValidationError,
            "missing from terms",
        ):
            learn_glossary.validate_research_articles([base], self.entries)


if __name__ == "__main__":
    unittest.main()
