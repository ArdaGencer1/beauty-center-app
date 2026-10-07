#!/usr/bin/env python3
"""ATELIER v4 -- shared media the v3 snapshot referenced but the repo never had, plus film atlases.

  m/monogram.png            SG monogram keyed out of the salon's own end card (IG 18172308562331022 @11.3 s)
  m/walk-06..10.webp        salon walk stills (IG 18364153699186351, 17877211629689213, 17971549406932390)
  m/cert-wall.webp          certificate wall, m/cert-trophy.webp the gold heart award (IG 17877211629689213 @2.2 s)
  m/ig/film/<set>/a<k>.webp 3x3 frame atlases (9 frames per sheet) so the artifact stays under its file budget;
                            the per-frame files stay for the live site.

Usage: shared_media.py [--repo DIR]   (idempotent; reads originals/instagram/videos)
"""
from __future__ import annotations

import argparse
import glob
import io
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]

WALK = {  # name: (ig id, second, crop box on the 720x1280 frame)
    "walk-06": ("18364153699186351", 2.8, (0, 100, 720, 1060)),   # gold-railed staircase
    "walk-07": ("17877211629689213", 4.4, (0, 160, 720, 1120)),   # marble corridor
    "walk-08": ("18364153699186351", 10.2, (0, 20, 720, 980)),    # treatment room (subtitle below the crop)
    "walk-09": ("18364153699186351", 28.7, (0, 20, 720, 980)),    # skin-care room with magnifier lamp
    "walk-10": ("17971549406932390", 4.6, (0, 160, 720, 1120)),   # application under the lamp
}
ATLAS = {"salon-giris": 9, "cilt-led": 9, "salon-cephe": 9, "pmu-kalem": 9, "cilt-film": 9, "saten-film": 9}


def video(vid: str) -> str:
    return glob.glob(str(ROOT / f"originals/instagram/videos/*_{vid}.mp4"))[0]


def frame(vid: str, t: float) -> Image.Image:
    p = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(t), "-i", video(vid), "-frames:v", "1",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(p)).convert("RGB")


def grade(im: Image.Image) -> Image.Image:
    """The media pipeline's light 'atelier' grade: a touch of contrast and warmth, nothing local."""
    a = np.asarray(im).astype(np.float32) / 255
    a = np.clip((a - .5) * 1.04 + .5, 0, 1) ** .98
    a[..., 0] = np.clip(a[..., 0] * 1.015, 0, 1)
    a[..., 2] = np.clip(a[..., 2] * .985, 0, 1)
    return Image.fromarray((a * 255 + .5).astype(np.uint8))


def monogram(out: Path) -> None:
    a = np.asarray(frame("18172308562331022", 11.3)).astype(float)
    c = a[409:875, 126:593]
    lum = c.max(axis=2)
    alpha = np.clip((lum - 28) / (130 - 28), 0, 1)
    t = np.clip((lum - 60) / 180, 0, 1)[..., None]
    rgb = np.array([150, 114, 46.]) * (1 - t) + np.array([214, 181, 108.]) * t
    Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8), "RGBA").resize((160, 160), Image.LANCZOS).save(out / "monogram.png", optimize=True)


def stills(out: Path) -> None:
    for name, (vid, t, box) in WALK.items():
        grade(frame(vid, t).crop(box)).save(out / f"{name}.webp", quality=80, method=6)
    cert = grade(frame("17877211629689213", 2.2))
    cert.crop((0, 200, 720, 1160)).save(out / "cert-wall.webp", quality=80, method=6)
    cert.crop((230, 880, 500, 1240)).save(out / "cert-trophy.webp", quality=82, method=6)


def atlases(film: Path) -> None:
    for name, per in ATLAS.items():
        d = film / name
        frames = sorted(d.glob("f*.webp"))
        if not frames:
            continue
        for old in d.glob("a*.webp"):
            old.unlink()
        w, h = Image.open(frames[0]).size
        cols = 3
        for k in range(0, len(frames), per):
            chunk = frames[k:k + per]
            rows = (len(chunk) + cols - 1) // cols
            sheet = Image.new("RGB", (w * cols, h * rows))
            for i, f in enumerate(chunk):
                sheet.paste(Image.open(f).convert("RGB"), ((i % cols) * w, (i // cols) * h))
            sheet.save(d / f"a{k // per + 1}.webp", quality=72, method=6)
        print(f"{name}: {len(frames)} frames -> {(len(frames) + per - 1) // per} atlases ({w}x{h})")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(ROOT))
    ap.add_argument("--only", choices=["stills", "atlas"], default=None)
    a = ap.parse_args()
    m = Path(a.repo) / "website" / "m"
    if a.only != "atlas":
        monogram(m)
        stills(m)
    if a.only != "stills":
        atlases(m / "ig" / "film")


if __name__ == "__main__":
    main()
