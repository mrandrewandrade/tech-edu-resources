from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site" / "assets" / "learning-map" / "learning-map.yml"
JSON_OUTPUT = ROOT / "site" / "assets" / "learning-map" / "learning-map.json"
GRAPH_OUTPUT = ROOT / "site" / "assets" / "learning-map" / "learning-graph.json"
SEQUENCE_OUTPUT = ROOT / "site" / "assets" / "bs-learn-sequence.json"
JS = ROOT / "site" / "assets" / "learning-map" / "learning-map.js"


class LearningMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = yaml.safe_load(SOURCE.read_text(encoding="utf-8"))
        cls.nodes = cls.source["nodes"]
        cls.by_id = {node["id"]: node for node in cls.nodes}

    def test_builder_succeeds_and_generated_json_matches(self):
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build_learning_map.py")], check=True, cwd=ROOT)
        generated = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
        self.assertEqual(generated, self.source)

    def test_map_has_both_courses_and_central_hub(self):
        self.assertIn("commons-hub", self.by_id)
        self.assertGreaterEqual(sum(node["world"] == "tej" for node in self.nodes), 10)
        self.assertGreaterEqual(sum(node["world"] == "tas" for node in self.nodes), 10)

    def test_connections_are_known_and_reciprocal(self):
        for node in self.nodes:
            for neighbour in node["neighbours"]:
                self.assertIn(neighbour, self.by_id, f"{node['id']} has an unknown neighbour")
                self.assertIn(node["id"], self.by_id[neighbour]["neighbours"], f"{node['id']} <-> {neighbour} is not reciprocal")

    def test_internal_lesson_targets_exist(self):
        for node in self.nodes:
            href = node["href"]
            self.assertTrue(href.startswith("../"), f"{node['id']} does not have a relative href")
            relative = href.removeprefix("../")
            html_target = ROOT / "site" / relative
            candidates = [html_target.with_suffix(".qmd"), html_target.with_suffix(".md")]
            if html_target.name == "index.html":
                candidates.append(html_target.parent / "index.qmd")
            self.assertTrue(any(path.exists() for path in candidates), f"{node['id']} target missing: {href}")

    def test_references_are_https_and_videos_do_not_autoplay(self):
        for node in self.nodes:
            if "reference" in node:
                self.assertTrue(node["reference"]["url"].startswith("https://"))
        script = JS.read_text(encoding="utf-8").lower()
        self.assertNotIn("autoplay", script)


class LearningGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build_learning_graph.py")], check=True, cwd=ROOT)
        cls.graph = json.loads(GRAPH_OUTPUT.read_text(encoding="utf-8"))
        cls.sequence = json.loads(SEQUENCE_OUTPUT.read_text(encoding="utf-8"))
        cls.by_id = {node["id"]: node for node in cls.graph["nodes"]}

    def test_graph_contains_every_sequenced_lesson(self):
        lessons = [node for node in self.graph["nodes"] if node["kind"] == "lesson"]
        tracks = [node for node in self.graph["nodes"] if node["kind"] == "track"]
        self.assertEqual(len(lessons), len(self.sequence["lessons"]))
        self.assertEqual(len(tracks), 15)
        self.assertEqual(sum(node["kind"] == "course" for node in self.graph["nodes"]), 2)
        self.assertIn("commons-hub", self.by_id)

    def test_graph_edges_are_typed_unique_and_known(self):
        valid_types = {"contains", "sequence", "related"}
        keys = set()
        for edge in self.graph["edges"]:
            self.assertIn(edge["type"], valid_types)
            self.assertIn(edge["from"], self.by_id)
            self.assertIn(edge["to"], self.by_id)
            key = (edge["from"], edge["to"], edge["type"])
            self.assertNotIn(key, keys)
            keys.add(key)

    def test_graph_uses_sequence_and_page_links(self):
        edge_types = [edge["type"] for edge in self.graph["edges"]]
        self.assertGreaterEqual(edge_types.count("sequence"), 60)
        self.assertGreaterEqual(edge_types.count("related"), 20)

    def test_all_strands_have_accessible_labels_and_colours(self):
        strand_ids = {strand["id"] for strand in self.graph["strands"]}
        for strand in self.graph["strands"]:
            self.assertTrue(strand["label"])
            self.assertRegex(strand["colour"], r"^#[0-9a-fA-F]{6}$")
            self.assertRegex(strand["soft"], r"^#[0-9a-fA-F]{6}$")
        for node in self.graph["nodes"]:
            self.assertTrue(set(node["strands"]).issubset(strand_ids))


if __name__ == "__main__":
    unittest.main()
