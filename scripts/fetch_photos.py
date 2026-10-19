#!/usr/bin/env python3
"""Fetch and optimize CC BY 4.0 photographs used by AXEN.

The originals are by Baron Maddock, via Wikimedia Commons.
Only resize/transcode (no misleading alteration). Attribution: credits-photos.html
Outputs are checked into git by the Pages workflow on the initial fetch.
"""
from io import BytesIO
from pathlib import Path
import urllib.error
import urllib.request
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "photos"
OUT.mkdir(parents=True, exist_ok=True)

IMAGES = [
    (
        "canon-imagerunner-c7570i.webp",
        "https://upload.wikimedia.org/wikipedia/commons/0/00/Canon_ImageRUNNER_Advance_C7570i_photocopier.jpg",
    ),
    (
        "xerox-altalink-c8045.webp",
        "https://upload.wikimedia.org/wikipedia/commons/4/4e/Xerox_AltaLink_C8045_photocopier.jpg",
    ),
]


def validate(path):
    with Image.open(path) as picture:
        picture.verify()
    with Image.open(path) as picture:
        assert picture.format == "WEBP", f"Unexpected format in {path}"
        assert picture.width >= 750 and picture.height >= 520, f"Insufficient resolution: {path}"


def download_one(filename, url):
    target = OUT / filename
    if target.exists():
        validate(target)
        print(f"PHOTO OK (local): {filename} ({target.stat().st_size} bytes)")
        return
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "AXENWebsite/1.0 (contact: https://github.com/kesurof/axen-web)",
            "Accept": "image/jpeg,image/*;q=0.9",
        },
    )
    with urllib.request.urlopen(request, timeout=40) as reply:
        assert reply.status == 200, f"HTTP {reply.status}: {url}"
        raw = reply.read(7_000_000)
    with Image.open(BytesIO(raw)) as picture:
        assert picture.format == "JPEG", f"Unexpected media from {url}"
        picture = ImageOps.exif_transpose(picture).convert("RGB")
        assert picture.width >= 900 and picture.height >= 700
        picture.thumbnail((1500, 1500), Image.Resampling.LANCZOS)
        picture.save(target, format="WEBP", quality=84, method=6)
    validate(target)
    print(f"PHOTO DOWNLOADED: {filename} ({target.stat().st_size} bytes)")


def main():
    for filename, url in IMAGES:
        download_one(filename, url)
    print("All real brand copier photos available locally.")


if __name__ == "__main__":
    main()
