"""Build the expandable Learning Worlds graph from canonical course content.

The course manifest owns the linear teaching sequence.  Internal links between
lesson pages add the cross-connections that turn those sequences into a web.
The generated JSON is browser data only; it is never the source of truth.
"""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import sys
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError as exc:  # pragma: no cover - clear failure for local editors
    raise SystemExit("PyYAML is required: python -m pip install pyyaml") from exc


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
SEQUENCE = SITE / "assets" / "bs-learn-sequence.json"
OUTPUT = SITE / "assets" / "learning-map" / "learning-graph.json"
SCRIPT_OUTPUT = SITE / "assets" / "learning-map" / "learning-graph-data.js"

STRANDS = {
    "circuits": {"label": "Circuits & Electronics", "colour": "#1677a6", "soft": "#d9f2ff"},
    "programming": {"label": "Programming & Data", "colour": "#6f42c1", "soft": "#eee5ff"},
    "linux": {"label": "Linux & Tools", "colour": "#4557b8", "soft": "#e4e8ff"},
    "systems": {"label": "Computer Systems & Networks", "colour": "#087f8c", "soft": "#d9f5f2"},
    "portfolio": {"label": "Portfolio & Evidence", "colour": "#2d7d52", "soft": "#ddf4e6"},
    "design-process": {"label": "Design Process", "colour": "#a86700", "soft": "#fff0c7"},
    "visual-design": {"label": "Visual Communication", "colour": "#b2387a", "soft": "#f9e1ee"},
    "fabrication": {"label": "Fabrication", "colour": "#b84c22", "soft": "#ffe5d8"},
    "culture": {"label": "Culture & Place", "colour": "#62751f", "soft": "#edf4d2"},
}

TRACK_STRANDS = {
    "circuits-electronics": "circuits",
    "programming-interfacing": "programming",
    "linux-operating-systems": "linux",
    "computer-systems": "systems",
    "networking": "systems",
    "portfolio": "portfolio",
    "design-process": "design-process",
    "accessible-design": "visual-design",
    "emotions-visual-communication": "visual-design",
    "logo-animation": "visual-design",
    "logo-design": "visual-design",
    "fabrication-tools": "fabrication",
    "phone-holder-project": "fabrication",
    "advanced-making": "fabrication",
    "culture-land": "culture",
}

TERM_STRANDS = {
    "circuits": {
        "circuit", "voltage", "current", "resistance", "resistor", "capacitor",
        "diode", "transistor", "operational-amplifier", "kirchhoff-law",
    },
    "programming": {"python", "programming", "numpy", "jupyter-notebook", "data-logging"},
    "linux": {"linux", "terminal", "git", "ssh", "file-path", "permission"},
    "systems": {"computer", "ethernet", "network", "router", "switch", "wi-fi", "usb"},
    "portfolio": {"portfolio", "evidence", "reflection", "documentation"},
    "design-process": {"need", "requirement", "constraint", "criterion", "prototype", "iteration"},
    "visual-design": {
        "logo", "typography", "animation", "raster-image", "vector-graphic",
        "contrast", "visual-hierarchy", "user-interface",
    },
    "fabrication": {
        "fabrication", "laser-cutting", "laser-cutter", "kerf", "joint", "assembly",
        "fastener", "computer-aided-design", "three-d-printing", "slicer",
    },
    "culture": {"land", "culture", "season", "community"},
}

MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HTML_LINK = re.compile(r"\bhref\s*=\s*['\"]([^'\"]+)['\"]", re.IGNORECASE)


def stable_id(kind: str, *parts: str) -> str:
    value = "-".join(parts).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return f"{kind}-{value}"


def page_href(source: str) -> str:
    return "../" + str(PurePosixPath(source).with_suffix(".html"))


def read_front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    data = yaml.safe_load(text[4:end]) or {}
    return data if isinstance(data, dict) else {}


def strands_for(lesson: dict) -> list[str]:
    primary = TRACK_STRANDS[lesson["track_id"]]
    source_path = SITE / lesson["source"]
    metadata = read_front_matter(source_path) if source_path.exists() else {}
    raw_terms = metadata.get("terms", [])
    terms = {str(term).strip().lower() for term in raw_terms} if isinstance(raw_terms, list) else set()
    strands = [primary]
    for strand, keywords in TERM_STRANDS.items():
        if strand != primary and terms.intersection(keywords):
            strands.append(strand)
        if len(strands) == 3:
            break
    return strands


def candidate_links(source: Path) -> list[str]:
    text = source.read_text(encoding="utf-8")
    links = [match.group(1).strip().split(maxsplit=1)[0] for match in MARKDOWN_LINK.finditer(text)]
    links.extend(match.group(1).strip() for match in HTML_LINK.finditer(text))
    return links


def resolve_internal_source(source: str, raw_target: str) -> str | None:
    target = unquote(raw_target.strip())
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    path = parsed.path
    if path.startswith("/commons/"):
        path = path.removeprefix("/commons/")
    elif path.startswith("/"):
        return None
    else:
        path = str(PurePosixPath(source).parent / path)
    normalized = posixpath.normpath(path)
    while normalized.startswith("../"):
        normalized = normalized[3:]
    if normalized.endswith(".html"):
        normalized = normalized[:-5] + ".qmd"
    elif normalized.endswith("/"):
        normalized += "index.qmd"
    return normalized


def build_graph() -> dict:
    manifest = json.loads(SEQUENCE.read_text(encoding="utf-8"))
    lessons = manifest.get("lessons", [])
    if not lessons:
        raise ValueError("Course sequence does not contain lessons")

    nodes: list[dict] = [
        {
            "id": "commons-hub",
            "kind": "hub",
            "title": "Technology Commons",
            "summary": "Begin here, choose a world, and expand only the routes you want to explore.",
            "href": "../index.html",
            "course": None,
            "track": None,
            "strands": [],
            "order": 0,
        }
    ]
    edges: list[dict] = []
    course_ids: dict[str, str] = {}
    track_ids: dict[tuple[str, str], str] = {}
    source_ids: dict[str, str] = {}
    route_ids: dict[str, str] = {}

    courses: dict[str, dict] = {}
    tracks: dict[tuple[str, str], dict] = {}
    for lesson in lessons:
        courses.setdefault(lesson["course_id"], lesson)
        tracks.setdefault((lesson["course_id"], lesson["track_id"]), lesson)

    for course_order, (course_id, lesson) in enumerate(courses.items(), start=1):
        node_id = stable_id("course", course_id)
        course_ids[course_id] = node_id
        course_strands = sorted({TRACK_STRANDS[item["track_id"]] for item in lessons if item["course_id"] == course_id})
        nodes.append(
            {
                "id": node_id,
                "kind": "course",
                "title": lesson["course_title"],
                "summary": "Choose a strand to see its lessons and connected ideas.",
                "href": ".." + lesson["course_hub"].removeprefix("/commons"),
                "course": course_id,
                "track": None,
                "strands": course_strands,
                "order": course_order,
            }
        )
        edges.append({"from": "commons-hub", "to": node_id, "type": "contains"})

    for (course_id, track_id), lesson in sorted(tracks.items(), key=lambda item: (item[1]["course_id"], item[1]["track_order"])):
        node_id = stable_id("track", course_id, track_id)
        track_ids[(course_id, track_id)] = node_id
        hub = lesson.get("track_hub") or lesson["source"]
        nodes.append(
            {
                "id": node_id,
                "kind": "track",
                "title": lesson["track_title"],
                "summary": lesson.get("track_summary") or lesson.get("track_use") or "Open this learning strand.",
                "href": page_href(hub),
                "course": course_id,
                "track": track_id,
                "strands": [TRACK_STRANDS[track_id]],
                "order": lesson["track_order"],
            }
        )
        edges.append({"from": course_ids[course_id], "to": node_id, "type": "contains"})

    for lesson in lessons:
        node_id = stable_id("lesson", lesson["source"])
        source_ids[lesson["source"]] = node_id
        route_ids[lesson["route"]] = node_id
        nodes.append(
            {
                "id": node_id,
                "kind": "lesson",
                "title": lesson["title"],
                "summary": lesson["summary"],
                "href": page_href(lesson["source"]),
                "source": lesson["source"],
                "course": lesson["course_id"],
                "track": lesson["track_id"],
                "strands": strands_for(lesson),
                "order": lesson["lesson_order"],
                "sequence_index": lesson["sequence_index"],
            }
        )
        edges.append(
            {
                "from": track_ids[(lesson["course_id"], lesson["track_id"])],
                "to": node_id,
                "type": "contains",
            }
        )

    seen_edges = {(edge["from"], edge["to"], edge["type"]) for edge in edges}

    def add_edge(from_id: str, to_id: str, edge_type: str) -> None:
        if from_id == to_id:
            return
        key = (from_id, to_id, edge_type)
        reverse = (to_id, from_id, edge_type)
        if key in seen_edges or (edge_type == "related" and reverse in seen_edges):
            return
        seen_edges.add(key)
        edges.append({"from": from_id, "to": to_id, "type": edge_type})

    for lesson in lessons:
        current_id = source_ids[lesson["source"]]
        next_route = lesson.get("next_route")
        if next_route and next_route in route_ids:
            add_edge(current_id, route_ids[next_route], "sequence")

        source_path = SITE / lesson["source"]
        if not source_path.exists():
            continue
        for raw_target in candidate_links(source_path):
            target_source = resolve_internal_source(lesson["source"], raw_target)
            if target_source in source_ids:
                add_edge(current_id, source_ids[target_source], "related")

    node_ids = {node["id"] for node in nodes}
    for edge in edges:
        if edge["from"] not in node_ids or edge["to"] not in node_ids:
            raise ValueError(f"Unknown graph edge endpoint: {edge}")

    return {
        "version": 1,
        "title": "Technology Commons Learning Web",
        "subtitle": "Expand a route, follow a quest path, or discover where ideas connect.",
        "storage_key": "technology-commons-learning-web-v1",
        "strands": [{"id": strand_id, **values} for strand_id, values in STRANDS.items()],
        "nodes": nodes,
        "edges": edges,
    }


def main() -> int:
    graph = build_graph()
    serialized = json.dumps(graph, ensure_ascii=False, indent=2)
    OUTPUT.write_text(serialized + "\n", encoding="utf-8")
    SCRIPT_OUTPUT.write_text(
        "window.TECHNOLOGY_COMMONS_LEARNING_GRAPH = " + serialized + ";\n",
        encoding="utf-8",
    )
    counts = {kind: sum(node["kind"] == kind for node in graph["nodes"]) for kind in ("hub", "course", "track", "lesson")}
    print(f"Built learning graph: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges ({counts})")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
