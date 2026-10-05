from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    """Run one required build step from the repository root."""
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def main() -> int:
    print("Generating the TEJ curriculum roadmap.")
    run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "build_tej_curriculum.py"),
        ]
    )
    print("Generating Technology Commons glossary.")
    run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "commons_glossary.py"),
            "generate",
        ]
    )
    print("Generating continuous course-note navigation.")
    run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "course_notes.py"),
            "generate",
        ]
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
