#!/usr/bin/env python3
"""Validate canonical TEJ curriculum metadata and its generated public page."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import yaml

from build_tej_curriculum import (
    ALLOWED_ACCESS,
    ALLOWED_PATHWAYS,
    ALLOWED_STATUSES,
    DATA_PATH,
    OUTPUT_PATH,
    effective_modules,
    validate_record,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
PRIVATE_MARKERS = {
    "docs.google.com/spreadsheets",
    "student quest tracker!",
    "leaderboard!",
    "1jlhg9kwlaaxxwbvpbg9otsc8zrvdactu9ej1p-5dtay",
}
OFFICIAL_HOSTS = {
    "www.edu.gov.on.ca",
    "www.allaboutcircuits.com",
    "www.casio.com",
    "www.statlearning.com",
    "developers.google.com",
    "karpathy.ai",
}


def main() -> int:
    data = yaml.safe_load(DATA_PATH.read_text(encoding="utf-8"))
    assert data["statuses"] == [
        "Published",
        "Pilot",
        "In development",
        "Planned",
        "Bonus",
        "Restricted source",
    ]
    assert set(data["access_levels"]) == ALLOWED_ACCESS

    units = data["units"]
    assert [str(unit["unit_id"]) for unit in units] == [str(i) for i in range(17)]

    source_ids = {str(source["source_id"]) for source in data["sources"]}
    module_ids: list[str] = []
    public_routes: list[str] = []
    for unit in units:
        validate_record(unit, f"unit {unit['unit_id']}")
        assert unit["status"] in ALLOWED_STATUSES
        assert str(unit["pathway"]).lower() in ALLOWED_PATHWAYS
        records = effective_modules(unit)
        assert records, f"unit {unit['unit_id']} has no modules"
        for record in records:
            module_id = str(record["module_id"])
            module_ids.append(module_id)
            referenced = set(record.get("source_references", []))
            assert referenced <= source_ids, f"{module_id} has unknown sources: {referenced - source_ids}"
            route = str(record["public_notes_route"])
            if route.endswith(".qmd"):
                public_routes.append(route)

    assert len(module_ids) == len(set(module_ids)), "module IDs must be unique"
    assert len(module_ids) >= 150, "roadmap unexpectedly lost modules"

    for route in public_routes:
        candidate = REPO_ROOT / "site" / route.removeprefix("site/")
        assert candidate.exists(), f"public route does not exist: {route}"

    for source in data["sources"]:
        url = str(source.get("url", ""))
        access = str(source["access_level"])
        if access == "Classroom restricted":
            assert not url, f"restricted source exposes a URL: {source['source_id']}"
        elif url:
            assert urlparse(url).hostname in OFFICIAL_HOSTS, f"unreviewed source host: {url}"

    combined = DATA_PATH.read_text(encoding="utf-8") + OUTPUT_PATH.read_text(encoding="utf-8")
    lowered = combined.lower()
    assert "\u2014" not in combined, "em dash found in public roadmap sources"
    for marker in PRIVATE_MARKERS:
        assert marker not in lowered, f"private marker found: {marker}"

    assert "data-tej-roadmap-search" in combined
    assert "data-tej-roadmap-status" in combined
    assert "data-tej-roadmap-pathway" in combined
    assert "data-tej-roadmap-access" in combined
    print(
        f"Validated {len(units)} units, {len(module_ids)} modules, "
        f"{len(data['sources'])} sources, and {len(public_routes)} public routes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
