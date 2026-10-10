#!/usr/bin/env python3
"""Check local links, fragments, images, scripts and CSS in the rendered TER site."""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


class Document(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[tuple[str, str]] = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        for key in ('href', 'src', 'poster'):
            if attrs.get(key):
                self.links.append((tag, attrs[key]))
        if attrs.get('srcset') and not attrs['srcset'].startswith('data:'):
            self.links.extend((tag, item.strip().split()[0]) for item in attrs['srcset'].split(',') if item.strip())


def check(root: Path) -> tuple[int, list[str]]:
    root = root.resolve()
    documents = {path: Document(path.read_text(encoding='utf-8')) for path in root.rglob('*.html')}
    problems = []
    count = 0

    def inspect(source: Path, tag: str, href: str):
        nonlocal count
        url = urlsplit(href)
        if url.scheme or url.netloc or href.startswith('#/'):
            return
        count += 1
        path_text = unquote(url.path)
        for site_base in ('/commons', '/tech-edu-resources'):
            if path_text == site_base:
                path_text = '/'
                break
            if path_text.startswith(site_base + '/'):
                path_text = path_text[len(site_base):]
                break
        target = (root / path_text.lstrip('/') if path_text.startswith('/')
                  else source.parent / path_text) if path_text else source
        target = target.resolve()
        if target.is_dir():
            target /= 'index.html'
        label = f'{source.relative_to(root)}: {href}'
        if not target.is_relative_to(root) or not target.is_file():
            problems.append('Missing target: ' + label)
        elif tag == 'a' and url.fragment and target in documents:
            if unquote(url.fragment) not in documents[target].ids:
                problems.append('Missing fragment: ' + label)

    for path, document in documents.items():
        for tag, href in document.links:
            inspect(path, tag, href)
    for path in root.rglob('*.css'):
        for match in re.finditer(r'url\(\s*[\'"]?([^\)\'"\s]+)', path.read_text(encoding='utf-8')):
            if not match[1].startswith('#'):
                inspect(path, 'css', match[1])
    for required in ['index.html', 'design-fabrication/index.html',
                     'design-fabrication/design-process/index.html',
                     'design-fabrication/logo-design/index.html',
                     'design-fabrication/laser-cutting/tool-organizer.html',
                     'tej3-4/index.html',
                     'tej3-4/circuits/index.html',
                     'tej3-4/engineering-preparation-track/index.html',
                     'slides/index.html', 'teacher-slides/index.html',
                     'teaching-materials/index.html',
                     'lore/index.html']:
        if not (root / required).is_file():
            problems.append('Missing main page: ' + required)
    for path in root.rglob('*.webp'):
        content = path.read_bytes()
        if content[:4] != b'RIFF' or content[8:12] != b'WEBP' or int.from_bytes(content[4:8], 'little') + 8 != len(content):
            problems.append('Invalid or truncated WebP: ' + str(path.relative_to(root)))
    return count, sorted(set(problems))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', nargs='?', type=Path, default=Path('site/_site'))
    args = parser.parse_args()
    count, problems = check(args.output)
    for problem in problems:
        print(problem)
    print(f'Checked {count} local references; {len(problems)} failures.')
    raise SystemExit(bool(problems))
