from __future__ import annotations

import copy
import inspect
import json
import unittest

from scripts import glossary_source as source
from scripts import learn_glossary


class CanonicalGlossaryJsonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.entries = source.load_contract_json()
        cls.serialized, cls.report = source.build_production_source()
        cls.data = json.loads(cls.serialized)

    def test_curated_json_and_import_directory_are_production_inputs(self) -> None:
        self.assertEqual(
            source.GLOSSARY_SOURCE_PATH,
            learn_glossary.REPOSITORY_ROOT / "glossary" / "glossary.json",
        )
        self.assertEqual(
            source.GLOSSARY_IMPORT_DIR,
            learn_glossary.REPOSITORY_ROOT / "glossary" / "imports",
        )
        self.assertEqual(
            source.TEJ_GLOSSARY_SOURCE_PATH,
            learn_glossary.REPOSITORY_ROOT / "glossary" / "tej-curriculum.json",
        )
        implementation = inspect.getsource(source.build_production_source)
        self.assertIn("load_contract_json", implementation)
        self.assertIn("build_imported_public_entries", implementation)
        self.assertNotIn("parse_markdown", implementation)
        self.assertNotIn("glossary_old", implementation)

    def test_tej_terms_have_public_references_and_grounded_switch_alias(self) -> None:
        tej_entries = source.load_tej_curriculum_entries()
        self.assertGreaterEqual(len(tej_entries), 170)
        for slug, entry in tej_entries.items():
            self.assertEqual(len(entry["references"]), 1, slug)
            reference = entry["references"][0]
            self.assertEqual(reference["type"], "website", slug)
            self.assertTrue(reference["title"], slug)
            self.assertTrue(reference["url"].startswith("https://"), slug)
        self.assertIn(
            "Grounded Switch",
            tej_entries["pull-up-resistor"]["aliases"],
        )

    def test_only_published_entries_are_projected(self) -> None:
        self.assertEqual(self.report["curated_entries"], len(self.entries))
        self.assertGreater(self.report["imported_entries"], 500)
        self.assertEqual(
            self.report["canonical_entries"],
            len(self.data["entries"]),
        )
        self.assertEqual(
            self.report["published_entries"],
            len(self.data["entries"]),
        )
        self.assertLessEqual(
            set(self.entries),
            {entry["slug"] for entry in self.data["entries"]},
        )

    def test_imported_terms_keep_grob_provenance_only(self) -> None:
        curated_slugs = set(self.entries)
        imported = [
            entry for entry in self.data["entries"] if entry["slug"] not in curated_slugs
        ]
        self.assertTrue(imported)
        for entry in imported:
            self.assertEqual(entry["references"][0]["key"], "grob2016")
        for entry in self.data["entries"]:
            if entry["slug"] in curated_slugs:
                self.assertFalse(
                    any(reference.get("key") == "grob2016" for reference in entry["references"])
                )

    def test_contract_fields_map_without_rewriting_authoritative_json(self) -> None:
        source_entry = self.entries["nice-design-process"]
        generated = {
            entry["slug"]: entry for entry in self.data["entries"]
        }["nice-design-process"]
        self.assertEqual(generated["term"], source_entry["term"])
        self.assertEqual(generated["short_definition"], source_entry["short_definition"])
        self.assertEqual(generated["definition"], source_entry["long_definition"])
        self.assertEqual(generated["categories"], source_entry["categories"])
        self.assertEqual(generated["learning_tracks"], source_entry["tracks"])
        self.assertEqual(generated["date_added"], source_entry["added"])

    def test_related_terms_resolve_to_published_canonicals(self) -> None:
        published = set(self.entries)
        for slug, entry in self.entries.items():
            self.assertLessEqual(set(entry["related_terms"]), published, slug)
        self.assertEqual(self.report["unresolved_related_terms"], 0)

    def test_basic_unit_aliases_are_preserved(self) -> None:
        self.assertIn("amps", self.entries["ampere"]["aliases"])
        self.assertIn("volts", self.entries["volt"]["aliases"])
        self.assertIn("m/s", self.entries["metres-per-second"]["aliases"])
        self.assertIn("m/s²", self.entries["metres-per-second-squared"]["aliases"])
        self.assertIn("N.I.C.E.", self.entries["nice-design-process"]["aliases"])

    def test_duplicate_raw_json_keys_fail_before_normal_parsing(self) -> None:
        with self.assertRaisesRegex(source.ValidationError, "Duplicate raw JSON key"):
            json.loads(
                '{"one":{"term":"One"},"one":{"term":"Other"}}',
                object_pairs_hook=source._reject_duplicate_keys,
            )

    def test_alias_collision_and_broken_inline_target_fail(self) -> None:
        collision = copy.deepcopy(self.entries)
        collision["ampere"]["aliases"] = ["Voltage"]
        with self.assertRaisesRegex(source.ValidationError, "conflicts with a canonical"):
            source.validate_contract_entries(collision)

        broken = copy.deepcopy(self.entries)
        broken["nice-design-process"]["inline_terms"] = {
            "design cycle": "not-published"
        }
        with self.assertRaisesRegex(source.ValidationError, "broken inline target"):
            source.validate_contract_entries(broken)

    def test_generation_is_deterministic(self) -> None:
        first, _ = source.build_production_source()
        second, _ = source.build_production_source()
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
