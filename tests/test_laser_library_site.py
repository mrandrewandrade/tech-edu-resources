import unittest
from unittest import mock

from scripts import laser_library


class LaserLibrarySiteTests(unittest.TestCase):
    def test_public_catalogue_and_previews_are_complete(self):
        document = laser_library.validate_public()
        self.assertGreaterEqual(document["count"], 150)
        self.assertIn("calibration", document["category_counts"])
        self.assertIn("french-cleat", document["category_counts"])
        self.assertIn("tool-holders", document["category_counts"])

    def test_every_filter_dimension_has_data(self):
        document = laser_library.validate_public()
        assets = document["assets"]
        self.assertTrue({item["shop"] for item in assets} >= {"general", "machine", "auto", "wood", "electronics"})
        self.assertTrue(any("Veccy" in item["editors"] for item in assets))
        self.assertTrue(any(item["fit_type"] != "none" for item in assets))
        self.assertTrue(all(item["units"] == "mm" for item in assets))
        expected_areas = {
            "exploring-technologies", "technological-design", "manufacturing", "construction",
            "transportation", "computer-technology", "communications-technology", "green-industries",
            "hairstyling-aesthetics", "hospitality-tourism", "health-care",
        }
        represented = {area for item in assets for area in item["technology_areas"]}
        self.assertEqual(represented, expected_areas)
        self.assertTrue(all(len(item["technology_areas"]) <= 6 for item in assets))

    def test_duplicate_ids_are_rejected(self):
        document = laser_library.load_catalog(laser_library.PUBLIC_CATALOG)
        duplicate = dict(document)
        duplicate["assets"] = list(document["assets"]) + [document["assets"][0]]
        duplicate["count"] = len(duplicate["assets"])
        with mock.patch.object(laser_library, "load_catalog", return_value=duplicate):
            with self.assertRaisesRegex(laser_library.LaserLibraryError, "Duplicate asset ID"):
                laser_library.validate_public()


if __name__ == "__main__":
    unittest.main()
