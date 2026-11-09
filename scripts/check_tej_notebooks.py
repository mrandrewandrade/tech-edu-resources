#!/usr/bin/env python3
"""Execute every TEJ computational-engineering notebook without rewriting it."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

try:
    import nbformat
    from nbclient import NotebookClient
except ImportError as error:  # pragma: no cover - environment guidance
    raise SystemExit(
        "Install site/assets/tej-computational/requirements-jupyter.txt "
        "in an isolated environment before running this check."
    ) from error


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_ROOT = ROOT / "site" / "assets" / "tej-computational" / "notebooks"


def execute_notebook(path: Path, timeout: int) -> None:
    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    )
    client.execute()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=int, default=120, help="seconds allowed per cell")
    parser.add_argument("--pattern", default="*.ipynb", help="notebook filename glob")
    args = parser.parse_args(argv)
    paths = sorted(NOTEBOOK_ROOT.glob(args.pattern))
    if args.pattern == "*.ipynb" and len(paths) != 12:
        print(f"ERROR: expected 12 notebooks, found {len(paths)}", file=sys.stderr)
        return 1
    if not paths:
        print(f"ERROR: no notebooks matched {args.pattern!r}", file=sys.stderr)
        return 1
    for path in paths:
        execute_notebook(path, args.timeout)
        print(f"PASS {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
