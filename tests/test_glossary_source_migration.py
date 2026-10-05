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
        implementation = inspect.getsource(source.build_production_source)
        self.assertIn("load_contract_json", implementation)
        self.assertIn("build_imported_public_entries", implementation)
        self.assertNotIn("parse_markdown", implementation)
        self.assertNotIn("glossary_old", implementation)

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

    def test_design_fabrication_expansion_entries_are_all_sourced(self) -> None:
        expansion = {
            slug: entry
            for slug, entry in self.entries.items()
            if entry["added"] == "2026-10-04"
        }
        self.assertGreaterEqual(len(expansion), 170)
        missing = [slug for slug, entry in expansion.items() if not entry["references"]]
        self.assertEqual(missing, [])

    def test_curriculum_aliases_resolve_to_expected_canonicals(self) -> None:
        owners = {
            source.normalize_lookup(alias): slug
            for slug, entry in self.entries.items()
            for alias in entry["aliases"]
        }
        expected = {
            "AI": "artificial-intelligence",
            "CAD": "computer-aided-design",
            "JPG": "jpeg",
            "SVG": "scalable-vector-graphics",
            "UI": "user-interface",
            "UX": "user-experience",
            "STEP": "step-file",
        }
        for alias, slug in expected.items():
            self.assertEqual(owners[source.normalize_lookup(alias)], slug)

    def test_reference_numbers_preserve_existing_sequence(self) -> None:
        references = learn_glossary.BIBLIOGRAPHY_REFERENCES
        self.assertEqual(references["grob2016"]["number"], "1")
        self.assertEqual(references["opencircuits2023"]["number"], "2")
        self.assertEqual(references["ngss2013"]["number"], "3")
        self.assertEqual(references["troteclaserparameters"]["number"], "26")


if __name__ == "__main__":
    unittest.main()
