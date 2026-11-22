"""Validate the learning-world manifest and build browser/print artifacts."""

from __future__ import annotations

import html
import json
from pathlib import Path
import sys

try:
    import yaml
except ImportError as exc:  # pragma: no cover - clear failure for local editors
    raise SystemExit("PyYAML is required: python -m pip install pyyaml") from exc


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site" / "assets" / "learning-map" / "learning-map.yml"
JSON_OUTPUT = ROOT / "site" / "assets" / "learning-map" / "learning-map.json"
SVG_OUTPUT = ROOT / "site" / "assets" / "learning-map" / "learning-worlds-print.svg"
FALLBACK_OUTPUT = ROOT / "site" / "includes" / "generated" / "learning-map-noscript.html"

VALID_WORLDS = {"hub", "tej", "tas"}
VALID_TYPES = {"hub", "portal", "lesson", "project", "safety", "portfolio", "help"}
VALID_STATUS = {"required", "optional"}


def load_manifest() -> dict:
    data = yaml.safe_load(SOURCE.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("nodes"), list):
        raise ValueError("Manifest must contain a nodes list")
    return data


def validate(data: dict) -> None:
    errors: list[str] = []
    nodes = data["nodes"]
    ids = [node.get("id") for node in nodes]
    if len(ids) != len(set(ids)):
        errors.append("Node ids must be unique")
    id_set = set(ids)

    required = {
        "id", "title", "world", "region", "type", "status", "x", "y",
        "href", "summary", "do", "look_for", "neighbours",
    }
    for node in nodes:
        node_id = node.get("id", "<missing id>")
        missing = sorted(required - set(node))
        if missing:
            errors.append(f"{node_id}: missing {', '.join(missing)}")
            continue
        if node["world"] not in VALID_WORLDS:
            errors.append(f"{node_id}: invalid world {node['world']}")
        if node["type"] not in VALID_TYPES:
            errors.append(f"{node_id}: invalid type {node['type']}")
        if node["status"] not in VALID_STATUS:
            errors.append(f"{node_id}: invalid status {node['status']}")
        if not (0 <= node["x"] <= 100 and 0 <= node["y"] <= 100):
            errors.append(f"{node_id}: coordinates must be between 0 and 100")
        if not str(node["href"]).startswith("../"):
            errors.append(f"{node_id}: href must be a site-relative ../ link")
        for neighbour in node["neighbours"]:
            if neighbour not in id_set:
                errors.append(f"{node_id}: unknown neighbour {neighbour}")

    by_id = {node["id"]: node for node in nodes if "id" in node}
    for node in nodes:
        for neighbour in node.get("neighbours", []):
            if node["id"] not in by_id.get(neighbour, {}).get("neighbours", []):
                errors.append(f"{node['id']} -> {neighbour}: connection is not reciprocal")

    if "commons-hub" not in id_set:
        errors.append("A commons-hub start node is required")
    if errors:
        raise ValueError("Learning map validation failed:\n- " + "\n- ".join(errors))


def write_json(data: dict) -> None:
    JSON_OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_fallback(data: dict) -> None:
    groups = (("hub", "Central Hub"), ("tej", "Circuit and Computing Realms"), ("tas", "Fabrication Frontier"))
    out = [
        '<noscript><section class="learning-map-noscript" aria-labelledby="no-js-map-title">',
        '<h2 id="no-js-map-title">Learning Worlds lesson list</h2>',
        '<p>The interactive map needs JavaScript. Every destination is still available below.</p>',
    ]
    for world, label in groups:
        out.append(f"<h3>{html.escape(label)}</h3><ul>")
        for node in data["nodes"]:
            if node["world"] != world:
                continue
            out.append(
                '<li><a href="{href}">{title}</a> — {summary}</li>'.format(
                    href=html.escape(node["href"], quote=True),
                    title=html.escape(node["title"]),
                    summary=html.escape(node["summary"]),
                )
            )
        out.append("</ul>")
    out.append("</section></noscript>\n")
    FALLBACK_OUTPUT.write_text("\n".join(out), encoding="utf-8")


def svg_label(title: str) -> list[str]:
    words = title.split()
    if len(title) <= 20 or len(words) < 2:
        return [title]
    split = max(1, len(words) // 2)
    return [" ".join(words[:split]), " ".join(words[split:])]


def write_svg(data: dict) -> None:
    by_id = {node["id"]: node for node in data["nodes"]}
    palette = {"hub": "#f6c453", "tej": "#6ed6e8", "tas": "#f39b65"}
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000" role="img" aria-labelledby="title desc">',
        '<title id="title">Technology Commons Learning Worlds map</title>',
        '<desc id="desc">A printable route map connecting the central hub, TEJ circuit and computing regions, and TAS fabrication regions.</desc>',
        '<rect width="1600" height="1000" fill="#f8f5ea"/>',
        '<path d="M0 0H720V1000H0Z" fill="#e7f6f8"/><path d="M880 0H1600V1000H880Z" fill="#fff0e7"/>',
        '<text x="38" y="54" font-family="system-ui,sans-serif" font-size="34" font-weight="800" fill="#0d4f63">CIRCUIT + COMPUTING REALMS</text>',
        '<text x="1562" y="54" text-anchor="end" font-family="system-ui,sans-serif" font-size="34" font-weight="800" fill="#7a3518">FABRICATION FRONTIER</text>',
        '<g stroke="#52616b" stroke-width="5" stroke-linecap="round" opacity=".72" fill="none">',
    ]
    seen: set[tuple[str, str]] = set()
    map_y = lambda value: 80 + value * 8.0
    for node in data["nodes"]:
        for neighbour_id in node["neighbours"]:
            edge = tuple(sorted((node["id"], neighbour_id)))
            if edge in seen:
                continue
            seen.add(edge)
            neighbour = by_id[neighbour_id]
            out.append(
                f'<line x1="{node["x"] * 16:.0f}" y1="{map_y(node["y"]):.0f}" '
                f'x2="{neighbour["x"] * 16:.0f}" y2="{map_y(neighbour["y"]):.0f}"/>'
            )
    out.append("</g>")
    for node in data["nodes"]:
        x, y = node["x"] * 16, map_y(node["y"])
        radius = 37 if node["type"] in {"hub", "portal"} else 27
        out.append(
            f'<g><circle cx="{x:.0f}" cy="{y:.0f}" r="{radius}" fill="{palette[node["world"]]}" '
            'stroke="#152832" stroke-width="5"/>'
        )
        mark = {"safety": "!", "project": "◆", "portfolio": "★", "portal": "↗", "help": "?", "hub": "●"}.get(node["type"], "•")
        out.append(
            f'<text x="{x:.0f}" y="{y + 10:.0f}" text-anchor="middle" font-family="system-ui,sans-serif" '
            f'font-size="28" font-weight="900" fill="#152832">{html.escape(mark)}</text>'
        )
        label_y = y + radius + 23
        for index, line in enumerate(svg_label(node["title"])):
            out.append(
                f'<text x="{x:.0f}" y="{label_y + index * 18:.0f}" text-anchor="middle" '
                'font-family="system-ui,sans-serif" font-size="15" font-weight="750" fill="#152832">'
                f'{html.escape(line)}</text>'
            )
        out.append("</g>")
    out.extend([
        '<g transform="translate(38 940)" font-family="system-ui,sans-serif" font-size="18" fill="#152832">',
        '<text font-weight="800">Legend:</text><text x="88">● hub</text><text x="180">↗ portal</text>',
        '<text x="300">! safety</text><text x="405">◆ project</text><text x="520">★ portfolio</text>',
        '<text x="650">A visited stop records exploration, not mastery.</text></g>',
        '</svg>\n',
    ])
    SVG_OUTPUT.write_text("\n".join(out), encoding="utf-8")


def main() -> int:
    data = load_manifest()
    validate(data)
    write_json(data)
    write_fallback(data)
    write_svg(data)
    print(f"Built learning map: {len(data['nodes'])} nodes")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
