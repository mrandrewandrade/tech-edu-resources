#!/usr/bin/env python3
"""Exercise the rendered Commons site in Chromium and save review screenshots."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '.tools' / 'review'

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT / 'site/_site')))
    Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    pages = [
        'index.html',
        'design-fabrication/index.html',
        'design-fabrication/03-laser-cutting/index.html',
        'design-fabrication/04-3d-printing/index.html',
        'tej3-4/index.html',
        'slides/2026-27-tas-2-sem-1.html',
        'slides/2026-27-tej-3-sem-1.html',
        'teacher-slides/index.html',
        'teaching-materials/index.html',
        'glossary/index.html',
        'about.html',
        'lore/index.html',
        'lore/remembering-the-port-credit-boys.html',
    ]
    errors = []
    failed_external = set()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={'width': 1440, 'height': 1000})
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('response', lambda response: errors.append(f'{response.status}: {response.url}') if response.url.startswith(base) and response.status >= 400 else None)
            page.on('requestfailed', lambda request: failed_external.add(request.url) if not request.url.startswith(base) else errors.append(f'Request failed: {request.url}'))
            for route in pages:
                assert page.goto(base + '/' + route).ok, route
                page.locator('img').evaluate_all('async (images) => { for (const image of images) image.loading = "eager"; await Promise.all(images.map(image => image.decode().catch(() => null))); }')
                page.wait_for_load_state('networkidle')
                assert page.locator('nav.navbar').count() == 1, f'Navbar: {route}'
                nav = page.locator('#navbarCollapse a.nav-link').all_text_contents()
                assert len(nav) == len(set(nav)), f'Duplicate navigation: {route}'
                assert page.locator('main').inner_text().strip(), f'Empty main: {route}'
                assert page.evaluate('getComputedStyle(document.body).fontFamily').find('Source') >= 0, f'CSS: {route}'
                broken = page.locator('img').evaluate_all('(images) => images.filter(i => i.src.startsWith(location.origin) && (!i.complete || !i.naturalWidth)).map(i => i.src)')
                assert not broken, broken
                if route.startswith('lore/') and route != 'lore/index.html':
                    themes = page.locator('.commons-lore-taxonomy')
                    assert themes.is_visible(), f'Lore themes: {route}'
                    tools = page.locator('.bs-site-tools')
                    assert tools.bounding_box()['y'] >= themes.bounding_box()['y'] + themes.bounding_box()['height'], f'Overlapping Lore tools: {route}'
                page.screenshot(path=str(OUTPUT / (route.replace('/', '-') + '.png')))

            page.goto(base + '/lore/index.html')
            design_filter = page.locator('[data-bs-filter-category="Design"]')
            if design_filter.is_enabled():
                design_filter.click()
                assert page.locator('[data-bs-research-item]:visible').count() >= 1
                page.locator('[data-bs-clear-filters]').click()
            assert page.locator('[data-bs-research-item]:visible').count() >= 1

            page.goto(base + '/glossary/index.html')
            page.locator('#bs-glossary-search').fill('Zero-power resistance')
            page.wait_for_timeout(250)
            assert page.locator('[data-bs-glossary-entry]:visible').count() == 1

            page.goto(base + '/tej3-4/01-number-systems/01-significant-figures.html')
            page.wait_for_load_state('networkidle')
            toc = page.locator('#quarto-margin-sidebar #TOC')
            assert toc.is_visible(), 'TEJ lesson TOC is not visible'
            assert 'Core idea' in toc.inner_text()
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            page.wait_for_timeout(1200)
            assert toc.is_visible(), 'TEJ lesson TOC disappeared while scrolling'
            assert not page.locator('#quarto-margin-sidebar').evaluate(
                '(element) => element.classList.contains("bs-refined-right-rail-scroll-collapsed")'
            ), 'TEJ lesson TOC auto-collapsed while scrolling'
            assert page.locator('.bs-learn-scroll-lesson-marker').count() >= 2, (
                'TEJ continuous notes did not load the next lesson'
            )
            page.screenshot(path=str(OUTPUT / 'tej-continuous-toc.png'))

            page.goto(base + '/design-fabrication/01-nice-design-process/01-needs-necessities.html')
            page.wait_for_load_state('networkidle')
            assert page.locator('#quarto-margin-sidebar #TOC').is_visible(), (
                'Design & Fabrication lesson TOC is not visible'
            )
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            page.wait_for_timeout(1200)
            assert page.locator('.bs-learn-scroll-lesson-marker').count() >= 2, (
                'Design & Fabrication continuous notes did not load the next lesson'
            )

            page.set_viewport_size({'width': 390, 'height': 844})
            for route in ['index.html', 'design-fabrication/index.html', 'design-fabrication/03-laser-cutting/index.html', 'tej3-4/index.html']:
                page.goto(base + '/' + route)
                page.wait_for_load_state('networkidle')
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), f'Horizontal overflow: {route}'
                page.screenshot(path=str(OUTPUT / ('mobile-' + route.replace('/', '-') + '.png')))
            page.goto(base + '/index.html')
            page.locator('.navbar-toggler').click()
            page.locator('#navbarCollapse').wait_for(state='visible')
            page.get_by_role('link', name='Educator Resources').click()
            page.locator('#navbarCollapse').get_by_role(
                'link', name='General Design & Fabrication', exact=True
            ).click()
            page.wait_for_url('**/design-fabrication/**')
            assert not errors, errors
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    result = {'desktop_pages': len(pages), 'mobile_pages': 4, 'local_errors': errors, 'external_request_failures': sorted(failed_external)}
    (OUTPUT / 'browser-results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
