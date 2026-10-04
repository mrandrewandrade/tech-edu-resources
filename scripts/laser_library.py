#!/usr/bin/env python3
"""Validate or sync the public laser-library manifest and previews.

SPDX-License-Identifier: AGPL-3.0-only
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOT = ROOT / "site" / "assets" / "laser-library"
PUBLIC_CATALOG = PUBLIC_ROOT / "catalog.json"
REQUIRED = {
    "id", "title", "description", "category", "subcategory", "shop", "tool_family",
    "tags", "technology_areas", "skill_level", "dimensions", "units", "material", "fit_type",
    "kerf_assumptions", "generator", "parameters", "operations", "files", "editors",
    "license", "attribution", "source_reference", "sensitivity", "trademark_status",
    "review_status", "notes",
}


class LaserLibraryError(RuntimeError):
    pass


def load_catalog(path: Path) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LaserLibraryError(f"Cannot read {path}: {exc}") from exc
    assets = document.get("assets")
    if not isinstance(assets, list) or not assets:
        raise LaserLibraryError("Laser catalogue must contain a non-empty assets list")
    if document.get("count") != len(assets):
        raise LaserLibraryError("Laser catalogue count does not match assets list")
    return document


def validate_public() -> dict[str, Any]:
    document = load_catalog(PUBLIC_CATALOG)
    seen: set[str] = set()
    for record in document["assets"]:
        missing = REQUIRED - set(record)
        if missing:
            raise LaserLibraryError(f"{record.get('id', '<unknown>')} is missing {sorted(missing)}")
        if record["id"] in seen:
            raise LaserLibraryError(f"Duplicate asset ID: {record['id']}")
        seen.add(record["id"])
        if record["units"] != "mm":
            raise LaserLibraryError(f"{record['id']} does not use millimetres")
        preview_rel = Path(record["files"]["preview"])
        try:
            preview_suffix = preview_rel.relative_to("generated/previews")
        except ValueError as exc:
            raise LaserLibraryError(f"{record['id']} has an invalid preview path") from exc
        preview = PUBLIC_ROOT / "previews" / preview_suffix
        if not preview.is_file():
            raise LaserLibraryError(f"Missing preview for {record['id']}: {preview}")
    if len(seen) < 150:
        raise LaserLibraryError(f"Expected a meaningful first catalogue; found {len(seen)} assets")
    expected_counts = dict(sorted(Counter(item["category"] for item in document["assets"]).items()))
    if document.get("category_counts") != expected_counts:
        raise LaserLibraryError("Laser category counts are stale")
    recipes = PUBLIC_ROOT / "veccy-recipes.json"
    if not recipes.is_file():
        raise LaserLibraryError("Veccy recipes are missing")
    return document


def sync(source_catalog: Path) -> None:
    source_catalog = source_catalog.resolve()
    document = load_catalog(source_catalog)
    library_root = source_catalog.parents[1]
    source_preview_root = library_root / "generated" / "previews"
    source_recipes = library_root / "veccy" / "recipes.json"
    if not source_preview_root.is_dir() or not source_recipes.is_file():
        raise LaserLibraryError(f"{library_root} is not a generated Technology Commons laser library")
    PUBLIC_ROOT.mkdir(parents=True, exist_ok=True)
    destination_previews = PUBLIC_ROOT / "previews"
    if destination_previews.exists():
        shutil.rmtree(destination_previews)
    shutil.copytree(source_preview_root, destination_previews)
    shutil.copy2(source_catalog, PUBLIC_CATALOG)
    shutil.copy2(source_recipes, PUBLIC_ROOT / "veccy-recipes.json")
    print(f"Synced {document['count']} assets from {source_catalog}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "sync"), nargs="?", default="validate")
    parser.add_argument("source", nargs="?", type=Path, help="source laser/generated/catalog.json for sync")
    args = parser.parse_args()
    try:
        if args.command == "sync":
            if args.source is None:
                parser.error("sync requires a source catalog path")
            sync(args.source)
        document = validate_public()
    except LaserLibraryError as exc:
        print(f"Laser library error: {exc}", file=sys.stderr)
        return 1
    print(f"Validated public laser catalogue: {document['count']} assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
