#!/usr/bin/env python3
"""Browser smoke checks for the TEJ computational extension and starter site."""

from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args: object) -> None:
        pass


def serve(directory: Path) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietHandler, directory=str(directory))
    )
    Thread(target=server.serve_forever, daemon=True).start()
    return server


def main() -> int:
    site_server = serve(ROOT / "site" / "_site")
    template_server = serve(ROOT / "student-templates" / "quarto-portfolio-starter" / "_site")
    site = f"http://127.0.0.1:{site_server.server_port}"
    template = f"http://127.0.0.1:{template_server.server_port}"
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            local_errors: list[str] = []
            page.on("pageerror", lambda error: local_errors.append(str(error)))
            page.on(
                "response",
                lambda response: local_errors.append(f"{response.status}: {response.url}")
                if response.url.startswith((site, template)) and response.status >= 400
                else None,
            )

            routes = [
                "/tej3-4/electronics-library/components/index.html",
                "/tej3-4/electronics-library/components/schematic-basics.html",
                "/tej3-4/electronics-library/components/resistors.html",
                "/tej3-4/electronics-library/components/capacitors.html",
                "/tej3-4/electronics-library/components/diodes-leds.html",
                "/tej3-4/electronics-library/components/transistors.html",
                "/tej3-4/electronics-library/components/op-amps.html",
                "/tej3-4/circuits/tinkercad-circuits.html",
                "/tej3-4/computational-engineering/index.html",
                "/tej3-4/computational-engineering/jupyter-electronics-lab.html",
                "/tej3-4/computational-engineering/jupyterlite.html",
                "/tej3-4/computational-engineering/local-python-jupyter.html",
                "/tej3-4/computational-engineering/finding-documentation-and-asking-for-help.html",
                "/tej3-4/computational-engineering/kirchhoff-jupyter-assignment.html",
                "/tej3-4/portfolio/index.html",
            ]
            for route in routes:
                response = page.goto(site + route)
                assert response and response.ok, route
                page.wait_for_load_state("networkidle")
                assert page.locator("main").inner_text().strip(), route
                assert page.locator("nav.navbar").count() == 1, route
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"), route
                assert page.evaluate(
                    "[...document.images].every((image) => image.complete && image.naturalWidth > 0)"
                ), f"unloaded image on {route}"

            for href in (
                "/assets/tej-computational/tej-computational-engineering-notebooks.zip",
                "/assets/tej-computational/notebooks/01-engineering-calculator.ipynb",
                "/assets/tej-computational/notebooks/07-rc-op-amp-calculus-bridge.ipynb",
                "/assets/tej-computational/notebooks/08-electronic-components-from-zero.ipynb",
                "/assets/tej-computational/data/circuit-measurements.csv",
                "/assets/tej-portfolio/quarto-portfolio-starter.zip",
            ):
                response = page.request.get(site + href)
                assert response.ok and len(response.body()) > 100, href

            response = page.goto(template + "/projects/index.html")
            assert response and response.ok
            page.wait_for_load_state("networkidle")
            assert page.locator(".quarto-grid-item").count() == 4
            filter_box = page.locator(".quarto-listing-filter input")
            filter_box.click()
            filter_box.press_sequentially("Python")
            page.wait_for_timeout(500)
            visible_items = page.evaluate(
                "window['quarto-listings']['listing-listing'].visibleItems.length"
            )
            assert visible_items == 1, f"expected 1 filtered project, found {visible_items}"
            filter_box.fill("")
            page.locator("#listing-listing-sort").select_option(
                label="Title"
            )
            assert page.locator(".quarto-listing-category .category").count() > 1
            assert page.locator("#quarto-search").count() == 1

            page.set_viewport_size({"width": 390, "height": 844})
            for url in (
                site + "/tej3-4/computational-engineering/jupyterlite.html",
                site + "/tej3-4/computational-engineering/kirchhoff-jupyter-assignment.html",
                site + "/tej3-4/computational-engineering/jupyter-electronics-lab.html",
                site + "/tej3-4/electronics-library/components/schematic-basics.html",
                site + "/tej3-4/electronics-library/components/op-amps.html",
                site + "/tej3-4/portfolio/index.html",
                template + "/projects/index.html",
            ):
                response = page.goto(url)
                assert response and response.ok, url
                page.wait_for_load_state("networkidle")
                overflow = page.evaluate(
                    """() => ({
                      page: document.documentElement.scrollWidth - innerWidth,
                      elements: [...document.querySelectorAll('body *')]
                        .filter((element) => element.getBoundingClientRect().right > innerWidth + 1)
                        .slice(0, 8)
                        .map((element) => ({
                          element: `${element.tagName}.${element.className}`,
                          text: (element.closest('pre')?.innerText || element.innerText || '').slice(0, 180)
                        }))
                    })"""
                )
                assert overflow["page"] <= 1, f"{url}: {overflow}"

            assert not local_errors, local_errors
            browser.close()
    finally:
        for server in (site_server, template_server):
            server.shutdown()
            server.server_close()
    print("TEJ extension browser checks passed: 13 course routes, 6 downloads, responsive template controls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
