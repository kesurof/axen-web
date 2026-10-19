#!/usr/bin/env python3
"""Validate all AXEN static pages, same-site links, anchors, SVG and CSS before deployment."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re
import xml.etree.ElementTree as ET
import tinycss2

ROOT = Path(__file__).resolve().parents[1]

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.images = []
        self.resources = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a' and 'href' in a: self.links.append(a['href'])
        if tag == 'img': self.images.append(a)
        if tag == 'script' and a.get('src'): self.resources.append(a['src'])
        if tag == 'link' and a.get('href'): self.resources.append(a['href'])

pages = sorted([ROOT / 'index.html', ROOT / 'mentions-legales.html', ROOT / 'confidentialite.html'] +
               list((ROOT / 'solutions').glob('*.html')))
assert len(list((ROOT / 'solutions').glob('*.html'))) == 4, 'Expected four solution pages'
parsed = {}
for file in pages:
    parser = Parser()
    parser.feed(file.read_text(encoding='utf8'))
    assert len(parser.ids) == len(set(parser.ids)), f'{file.name}: duplicate IDs'
    parsed[file.resolve()] = parser

for file, parser in parsed.items():
    for link in parser.links + parser.resources + [img.get('src', '') for img in parser.images]:
        if not link or link.startswith(('mailto:', 'tel:', 'data:', 'https://', 'http://')): continue
        path = urlsplit(link)
        dest = (file.parent / unquote(path.path)).resolve() if path.path else file
        assert dest.is_relative_to(ROOT.resolve()), f'{file.name}: unsafe path {link}'
        assert dest.is_file(), f'{file.name}: missing resource {link}'
        if path.fragment and dest.suffix == '.html':
            assert dest in parsed, f'{file.name}: unregistered destination {link}'
            assert unquote(path.fragment) in parsed[dest].ids, f'{file.name}: broken anchor {link}'
    for img in parser.images:
        assert 'alt' in img, f'{file.name}: missing image alt'
    print('OK', file.relative_to(ROOT), 'links, anchors, images')

home = (ROOT / 'index.html').read_text(encoding='utf8')
assert 'Avec AXEN,' in home and 'faites bonne' in home and 'impression' in home
assert 'contactEmail' in (ROOT / 'site-config.js').read_text(encoding='utf8')
assert 'https://kesurof.github.io/axen-web/' in home
assert not re.search(r'https?://[^"\\s]+(?:\\.js|\\.css)', home), 'External runtime dependency'
for label, slug in (
    ('photocopieurs', 'photocopieurs-multifonctions'),
    ('imprimantes', 'imprimantes-professionnelles'),
    ('numérisation', 'numerisation-documents'),
    ('parc', 'gestion-parc-impression')):
    assert home.count(f'solutions/{slug}.html') == 1, f'Missing card link: {label}'

for svg in ROOT.rglob('*.svg'):
    if 'dist' not in svg.parts:
        ET.parse(svg)
css = tinycss2.parse_stylesheet((ROOT/'styles.css').read_text(encoding='utf8'),
                                skip_whitespace=True, skip_comments=True)
errors = [token for token in css if token.type == 'error']
assert not errors, errors
for page in pages:
    assert '<h1' in page.read_text(encoding='utf8'), f'No H1 in {page}'
print(f'PASS: {len(pages)} HTML pages, complete internal linking, SVG, CSS and configuration')
