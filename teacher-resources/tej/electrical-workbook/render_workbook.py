"""Render printable workbook HTML/PDF variants and visual QA contact sheets."""

from __future__ import annotations

import asyncio
import json
import shutil
import subprocess
from pathlib import Path

from playwright.async_api import async_playwright
from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BUILD = HERE / ".build"
QA = BUILD / "qa"
RENDERED = HERE / "rendered"

SOURCES = {
    "automotive-relay-investigation": ROOT
    / "site/assets/electronics/worksheets/automotive-relay-kvl-kcl.qmd",
    "automotive-relay-answer-key": HERE / "automotive-relay-kvl-kcl-answer-key.qmd",
    "capacitor-sound-investigation": ROOT
    / "site/assets/electronics/worksheets/capacitor-sound-investigation.qmd",
    "capacitor-sound-answer-key": HERE / "capacitor-sound-answer-key.qmd",
    "fault-cards": ROOT / "site/assets/tej-capstone/fault-cards.qmd",
    "fault-card-key": ROOT / "teacher-resources/tej-capstone/fault-card-key.md",
}

SUPPORT = [
    ROOT / "site/assets/electronics/schematics/automotive-relay-kvl-kcl.svg",
    ROOT / "site/assets/electronics/schematics/automotive-relay-meter-placement.svg",
    ROOT / "site/assets/electronics/schematics/automotive-relay-poor-ground.svg",
    ROOT / "site/assets/electronics/schematics/automotive-capacitor-sound-control.svg",
    HERE / "print.css",
]


def run(*args: str, cwd: Path | None = None) -> None:
    print(f"Running: {' '.join(args)}", flush=True)
    subprocess.run(args, cwd=cwd, check=True)


def stage_sources() -> dict[str, Path]:
    if BUILD.exists():
        resolved = BUILD.resolve()
        if HERE.resolve() not in resolved.parents:
            raise RuntimeError(f"Refusing to remove unexpected build path: {resolved}")
        shutil.rmtree(BUILD)
    QA.mkdir(parents=True)
    RENDERED.mkdir(parents=True, exist_ok=True)

    staged: dict[str, Path] = {}
    for name, source in SOURCES.items():
        relative = source.relative_to(ROOT)
        target = BUILD / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        staged[name] = target

    for source in SUPPORT:
        relative = source.relative_to(ROOT)
        target = BUILD / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    return staged


def render_html(staged: dict[str, Path]) -> dict[str, Path]:
    html_files: dict[str, Path] = {}
    for name, source in staged.items():
        run("quarto", "render", source.name, "--to", "html", cwd=source.parent)
        output = source.with_suffix(".html")
        if not output.exists():
            raise RuntimeError(f"Quarto did not create {output}")
        html_files[name] = output
    return html_files


async def render_pdfs(html_files: dict[str, Path]) -> dict[str, dict[str, Path]]:
    chrome = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    if not chrome.exists():
        raise RuntimeError(f"Chrome not found at {chrome}")

    outputs: dict[str, dict[str, Path]] = {}
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            executable_path=str(chrome), headless=True, args=["--allow-file-access-from-files"]
        )
        page = await browser.new_page()
        for name, html in html_files.items():
            await page.goto(html.as_uri(), wait_until="networkidle")
            await page.emulate_media(media="print")
            outputs[name] = {}
            for paper, pdf_format, prefer_css in (
                ("letter", "Letter", True),
                ("a4", "A4", False),
            ):
                colour_pdf = QA / f"{name}-{paper}-color.pdf"
                await page.pdf(
                    path=str(colour_pdf),
                    format=pdf_format,
                    print_background=True,
                    prefer_css_page_size=prefer_css,
                    margin={"top": "10mm", "right": "10mm", "bottom": "10mm", "left": "10mm"},
                )
                grey_pdf = QA / f"{name}-{paper}-grayscale.pdf"
                run(
                    "gswin64c",
                    "-q",
                    "-dNOPAUSE",
                    "-dBATCH",
                    "-sDEVICE=pdfwrite",
                    "-sColorConversionStrategy=Gray",
                    "-dProcessColorModel=/DeviceGray",
                    f"-sOutputFile={grey_pdf}",
                    str(colour_pdf),
                )
                outputs[name][f"{paper}-color"] = colour_pdf
                outputs[name][f"{paper}-grayscale"] = grey_pdf

            shutil.copy2(outputs[name]["letter-color"], RENDERED / f"{name}.pdf")
        await browser.close()
    return outputs


def make_contact_sheets(outputs: dict[str, dict[str, Path]]) -> dict[str, int]:
    pages: dict[str, int] = {}
    by_variant: dict[str, list[Path]] = {
        "letter-color": [],
        "letter-grayscale": [],
        "a4-color": [],
        "a4-grayscale": [],
    }
    for name, variants in outputs.items():
        for variant, pdf in variants.items():
            count = len(PdfReader(str(pdf)).pages)
            pages[f"{name}:{variant}"] = count
            prefix = QA / f"page-{variant}-{name}"
            for stale in QA.glob(f"{prefix.name}-*.png"):
                stale.unlink()
            run("pdftoppm", "-png", "-r", "105", str(pdf), str(prefix))
            page_images = sorted(QA.glob(f"{prefix.name}-*.png"))
            by_variant[variant].extend(page_images)

    for variant, images in by_variant.items():
        if not images:
            continue
        run(
            "magick",
            "montage",
            *(str(image) for image in images),
            "-thumbnail",
            "360x480",
            "-tile",
            "4x",
            "-geometry",
            "+12+12",
            "-background",
            "#d8dde0",
            str(QA / f"contact-{variant}.png"),
        )

    (QA / "page-counts.json").write_text(json.dumps(pages, indent=2), encoding="utf-8")
    return pages


async def main() -> None:
    print("Staging workbook sources...", flush=True)
    staged = stage_sources()
    print("Rendering standalone HTML...", flush=True)
    html = render_html(staged)
    print("Printing colour and grayscale variants...", flush=True)
    outputs = await render_pdfs(html)
    print("Creating QA contact sheets...", flush=True)
    pages = make_contact_sheets(outputs)
    canonical_pages = sum(
        count for key, count in pages.items() if key.endswith(":letter-color")
    )
    print(f"Rendered {len(SOURCES)} printable documents ({canonical_pages} canonical pages).", flush=True)
    print(f"PDFs: {RENDERED}", flush=True)
    print(f"QA contact sheets: {QA}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
