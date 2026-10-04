#!/usr/bin/env python3
"""Check the rendered TEJ electronics pathways at desktop and mobile widths."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / ".tools" / "review" / "tej-electronics"
ROUTES = [
    "tej3-4/index.html",
    "tej3-4/03-digital-logic-inputs/index.html",
    "tej3-4/03-digital-logic-inputs/02-switches-floating-inputs.html",
    "tej3-4/03-digital-logic-inputs/03-pull-down-inputs.html",
    "tej3-4/03-digital-logic-inputs/04-pull-up-active-low.html",
    "tej3-4/03-digital-logic-inputs/05-debounce-protection.html",
    "tej3-4/03-digital-logic-inputs/06-circuits-culminating-project.html",
    "tej3-4/04-microcontrollers/index.html",
    "tej3-4/05-control-systems/index.html",
    "tej3-4/05-control-systems/c06-pid.html",
    "tej3-4/05-control-systems/c10-cnc.html",
    "tej3-4/05-control-systems/c11-culminating-project.html",
    "tej3-4/electronics-library/index.html",
]
SCREENSHOT_ROUTES = {
    "tej3-4/index.html",
    "tej3-4/03-digital-logic-inputs/04-pull-up-active-low.html",
    "tej3-4/05-control-systems/index.html",
    "tej3-4/05-control-systems/c06-pid.html",
}


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    handler = partial(QuietHandler, directory=str(ROOT / "site" / "_site"))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    errors = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page()
            page.on(
                "response",
                lambda response: errors.append(f"{response.status}: {response.url}")
                if response.url.startswith(base) and response.status >= 400
                else None,
            )
            page.on("pageerror", lambda error: errors.append(str(error)))
            for label, viewport in (
                ("desktop", {"width": 1440, "height": 1000}),
                ("mobile", {"width": 390, "height": 844}),
            ):
                page.set_viewport_size(viewport)
                for route in ROUTES:
                    response = page.goto(f"{base}/{route}")
                    assert response and response.ok, route
                    page.wait_for_load_state("networkidle")
                    assert page.locator("main").inner_text().strip(), f"Empty main: {route}"
                    assert page.evaluate(
                        "document.documentElement.scrollWidth <= innerWidth + 1"
                    ), f"Horizontal overflow at {label}: {route}"
                    broken = page.locator("img").evaluate_all(
                        """(images) => images
                        .filter((image) => image.src.startsWith(location.origin)
                            && (!image.complete || !image.naturalWidth))
                        .map((image) => image.src)"""
                    )
                    assert not broken, f"Broken images at {route}: {broken}"
                    if route in SCREENSHOT_ROUTES:
                        name = route.replace("/", "-").replace(".html", "")
                        page.screenshot(
                            path=str(OUTPUT / f"{label}-{name}.png"), full_page=True
                        )
            assert not errors, errors
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    print(f"Checked {len(ROUTES)} routes at desktop and mobile widths; 0 failures.")


if __name__ == "__main__":
    main()
