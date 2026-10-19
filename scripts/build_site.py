#!/usr/bin/env python3
"""Build a clean and self-contained AXEN static website for GitHub Pages."""
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET
import cairosvg

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir()
for name in ('index.html', 'mentions-legales.html', 'confidentialite.html', 'styles.css', 'script.js', 'site-config.js',
             'manifest.webmanifest', 'robots.txt', 'sitemap.xml', 'credits-photos.html', '.nojekyll'):
    shutil.copy2(ROOT / name, DIST / name)
shutil.copytree(ROOT / 'assets', DIST / 'assets')
for photo in ('canon-imagerunner-c7570i.webp', 'xerox-altalink-c8045.webp'):
    path = DIST / 'assets' / 'photos' / photo
    assert path.is_file() and path.stat().st_size > 10_000, f'Photo missing or invalid: {path}'
shutil.copytree(ROOT / 'solutions', DIST / 'solutions')
for svg in DIST.rglob('*.svg'):
    ET.parse(svg)
icon = DIST / 'assets/brand/symbol-on-navy.svg'
logo_og = DIST / 'assets/brand/og-image.svg'
assert icon.exists() and logo_og.exists()
cairosvg.svg2png(url=str(icon), write_to=str(DIST/'assets/brand/favicon-180.png'), output_width=180, output_height=180)
cairosvg.svg2png(url=str(logo_og), write_to=str(DIST/'assets/brand/og-image.png'), output_width=1200, output_height=630)
print('AXEN: static website assembled into dist/, including favicon and Open Graph PNG.')
