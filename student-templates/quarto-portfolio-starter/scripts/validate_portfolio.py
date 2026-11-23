"""Small source-level checks for the TEJ Quarto portfolio starter."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []

    for name in ("core", "blog", "skills", "full"):
        require(
            (ROOT / f"_quarto-{name}.yml").is_file(),
            f"Missing profile: _quarto-{name}.yml",
            errors,
        )

    core = (ROOT / "_quarto-core.yml").read_text(encoding="utf-8")
    full = (ROOT / "_quarto-full.yml").read_text(encoding="utf-8")
    require("blog/" not in core, "Core profile must not render the blog", errors)
    require("skills.qmd" not in core, "Core profile must not render Skills", errors)
    require("blog/**/*.qmd" in full, "Full profile must render the blog", errors)
    require("skills.qmd" in full, "Full profile must render Skills", errors)

    projects = sorted((ROOT / "projects").glob("*.qmd"))
    require(len(projects) >= 5, "Projects need an index plus four examples", errors)
    for project in projects:
        if project.name == "index.qmd":
            continue
        text = project.read_text(encoding="utf-8")
        require("image-alt:" in text, f"Missing image-alt in {project.name}", errors)
        require(
            "synthetic" in text.lower() or "placeholder" in text.lower(),
            f"Example values are not labelled synthetic in {project.name}",
            errors,
        )

    for required in (
        "_brand.yml",
        "privacy.qmd",
        "skills.qmd",
        "PUBLISHING.md",
        "templates/general-project.qmd",
        "templates/circuit-project.qmd",
        "templates/linux-python-project.qmd",
        "templates/blog-post.qmd",
    ):
        require((ROOT / required).is_file(), f"Missing required file: {required}", errors)

    if errors:
        print("Portfolio validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Portfolio validation passed: {len(projects) - 1} project examples checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
