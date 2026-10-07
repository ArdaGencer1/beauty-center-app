#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TIRNAK ATELYESİ -- nail media v2 for the 22 nail pages (plan: plans/claude/20261007-tirnak/README.md).

Reads manifest_tirnak.json and writes into website/m/ig/ (the prototype's media folder, = OUT/images/ig/ on
the live site). Raw videos come from originals/instagram/videos/<date>_<IG id>.mp4; photos are the already
processed webp files (their Instagram originals are not in this repository).

  atlas    <slug>-atlas-<k>.webp (4x3 frames each, frame i in atlas i % n) + <slug>-poster.webp
  loop     <slug>.mp4 (H.264, no audio, faststart) + <slug>-poster.webp
  still    <slug>.webp (one video frame, optional crop)
  photo    <slug>.webp (a crop of a processed photo; colour untouched, never upscaled)

Nothing is graded: polish colour stays as photographed. Every range in the manifest was checked frame by frame.

  python3 sources/media_ig_20261007/build_tirnak.py [--only slug,slug] [--proof DIR]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
VIDEOS = REPO / "originals" / "instagram" / "videos"
OUT = REPO / "website" / "m" / "ig"
X264 = ["-c:v", "libx264", "-preset", "slow", "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an"]


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def source(vid: str) -> Path:
    hits = sorted(VIDEOS.glob(f"*_{vid}.mp4"))
    if not hits:
        raise SystemExit(f"raw video {vid} not found under {VIDEOS}")
    return hits[0]


def frame(src: Path, t: float, dst: Path, vf: str | None = None) -> None:
    run("ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", str(src), "-frames:v", "1",
        *(["-vf", vf] if vf else []), str(dst))


def crop_vf(c: list | None) -> str | None:
    if not c:
        return None
    x0, y0, x1, y1 = c
    return f"crop={x1 - x0}:{y1 - y0}:{x0}:{y0}"


def webp(src: Path, dst: Path, q: int) -> int:
    Image.open(src).convert("RGB").save(dst, "WEBP", quality=q, method=6)
    return dst.stat().st_size


def atlas(it: dict, tmp: Path) -> list[str]:
    src = source(it["id"])
    n, na, fw, fh = it["frames"], it["atlases"], it["fw"], it["fh"]
    segs = it["segments"]
    total = sum(b - a for a, b in segs)
    times = []
    for i in range(n):
        t = total * (i + 0.5) / n
        for a, b in segs:
            if t <= b - a:
                times.append(a + t)
                break
            t -= b - a
    cells = []
    for i, t in enumerate(times):
        p = tmp / f"{it['slug']}_{i:03d}.png"
        frame(src, t, p, f"scale={fw}:{fh}:flags=lanczos")
        cells.append(Image.open(p).convert("RGB"))
    per = -(-n // na)
    cols = 4
    rows = -(-per // cols)
    files = []
    for k in range(na):
        sheet = Image.new("RGB", (cols * fw, rows * fh))
        for j, i in enumerate(range(k, n, na)):
            sheet.paste(cells[i], ((j % cols) * fw, (j // cols) * fh))
        dst = OUT / f"{it['slug']}-atlas-{k}.webp"
        sheet.save(dst, "WEBP", quality=it.get("q", 62), method=6)
        files.append(dst.name)
    p = tmp / f"{it['slug']}_poster.png"
    frame(src, it["poster_t"], p, "scale=720:-2:flags=lanczos")
    webp(p, OUT / f"{it['slug']}-poster.webp", 78)
    files.append(f"{it['slug']}-poster.webp")
    return files


def loop(it: dict, tmp: Path) -> list[str]:
    src = source(it["id"])
    vf = ",".join(x for x in [crop_vf(it.get("crop")), "scale=720:-2:flags=lanczos", "fps=30", "format=yuv420p"] if x)
    dst = OUT / f"{it['slug']}.mp4"
    limit = it.get("max_mb", 0.8) * 1_000_000
    for crf in (23, 25, 27, 29):
        if "segments" in it:
            parts = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[s{i}];" for i, (a, b) in enumerate(it["segments"]))
            cat = "".join(f"[s{i}]" for i in range(len(it["segments"])))
            run("ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-filter_complex",
                f"{parts}{cat}concat=n={len(it['segments'])}:v=1:a=0,{vf}[v]", "-map", "[v]",
                *X264, "-crf", str(crf), str(dst))
        else:
            a, b = it["trim"]
            run("ffmpeg", "-loglevel", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", str(src),
                "-vf", vf, *X264, "-crf", str(crf), str(dst))
        if dst.stat().st_size <= limit:
            break
    p = tmp / f"{it['slug']}_poster.png"
    frame(src, it["poster_t"], p, ",".join(x for x in [crop_vf(it.get("crop")), "scale=720:-2:flags=lanczos"] if x))
    webp(p, OUT / f"{it['slug']}-poster.webp", 80)
    print(f"    {dst.name}: {dst.stat().st_size / 1e6:.2f} MB (crf {crf})")
    return [dst.name, f"{it['slug']}-poster.webp"]


def still(it: dict, tmp: Path) -> list[str]:
    p = tmp / f"{it['slug']}.png"
    frame(source(it["id"]), it["t"], p, crop_vf(it.get("crop")))
    webp(p, OUT / f"{it['slug']}.webp", it.get("q", 84))
    return [f"{it['slug']}.webp"]


def photo(it: dict) -> list[str]:
    im = Image.open(OUT / it["file"]).convert("RGB")
    w, h = im.size
    x0, y0, x1, y1 = it["keep"]
    im = im.crop((round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h)))
    dst = OUT / f"{it['slug']}.webp"
    im.save(dst, "WEBP", quality=88, method=6)
    return [dst.name]


def proof(files: list[str], dst: Path) -> None:
    """One contact sheet of everything built: posters, stills, photos, the first atlas of each film."""
    thumbs = []
    for f in files:
        if f.endswith(".mp4"):
            continue
        im = Image.open(OUT / f).convert("RGB")
        im.thumbnail((300, 400))
        thumbs.append(im)
    cols = 8
    rows = -(-len(thumbs) // cols)
    sheet = Image.new("RGB", (cols * 304, rows * 404), (20, 20, 20))
    for i, im in enumerate(thumbs):
        sheet.paste(im, ((i % cols) * 304, (i // cols) * 404))
    sheet.save(dst, quality=78)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--proof", default="")
    args = ap.parse_args()
    only = {s for s in args.only.split(",") if s}
    items = json.loads((HERE / "manifest_tirnak.json").read_text(encoding="utf-8"))["items"]
    built = []
    with tempfile.TemporaryDirectory() as td:
        for it in items:
            if only and it["slug"] not in only:
                continue
            tmp = Path(td) / it["slug"]
            tmp.mkdir()
            kind = it["kind"]
            print(f"  {kind:7} {it['slug']}")
            files = {"atlas": lambda: atlas(it, tmp), "loop": lambda: loop(it, tmp), "still": lambda: still(it, tmp),
                     "photo": lambda: photo(it)}[kind]()
            built += files
    total = sum((OUT / f).stat().st_size for f in built)
    print(f"{len(built)} files, {total / 1e6:.1f} MB")
    if args.proof:
        proof(built, Path(args.proof))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
