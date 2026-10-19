#!/usr/bin/env python3
"""Basic CI checks: local paths, anchors, asset validity, site meta and no external dependencies."""
from pathlib import Path
from html.parser import HTMLParser
import re
import xml.etree.ElementTree as ET
import tinycss2

ROOT=Path(__file__).resolve().parents[1]
class Parser(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.links=[];self.images=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if tag=='img':self.images.append(a)

for filename in ('index.html','mentions-legales.html','confidentialite.html'):
    p=Parser();p.feed((ROOT/filename).read_text(encoding='utf8'))
    assert len(p.ids)==len(set(p.ids)),f'{filename}: duplicate anchors'
    for link in p.links:
        if link.startswith('#'):assert link[1:] in p.ids,f'{filename}: broken anchor {link}'
        if link.startswith('./'):assert (ROOT/link[2:]).exists(),f'{filename}: broken local link {link}'
    for image in p.images:
        assert 'alt' in image, f'{filename}: alt text missing'
        src=image.get('src','')
        if src.startswith('./'):assert (ROOT/src[2:]).exists(),f'{filename}: image missing {src}'
    print('OK',filename,'anchors and images')
for item in ROOT.rglob('*.svg'):
    if 'dist' not in item.parts:ET.parse(item)
errors=[token for token in tinycss2.parse_stylesheet((ROOT/'styles.css').read_text(),skip_whitespace=True,skip_comments=True) if token.type=='error']
assert not errors,errors
homepage=(ROOT/'index.html').read_text()
assert 'Avec AXEN,' in homepage and 'faites bonne' in homepage and 'impression' in homepage
assert 'contactEmail' in (ROOT/'site-config.js').read_text()
assert 'https://kesurof.github.io/axen-web/' in homepage
assert not re.search(r'https?://[^"\s]+(?:\.js|\.css)',homepage), 'External runtime dependencies'
print('PASS: links, HTML structure, SVG XML, CSS, web config and project subpath.')
