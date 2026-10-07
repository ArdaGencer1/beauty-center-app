#!/usr/bin/env python3
"""Kalıcı Makyaj "Şölen" -- pack the PMU media for the artifact (the live site keeps the separate files).

  m/ig/pmu/<slug>-pair.webp   önce | sonra side by side in ONE file (both halves already share crop and grade;
                              packing only places them next to each other, nothing is re-graded)
  m/ig/pmu/kartela.webp       the tone macros on one 3x2 sheet (600x800 cells)
  m/ig/pmu/oda.webp           the two PMU room crops side by side
  sources/atelier_v4/pmu/pmu.json   sizes + the median lip colour of every tone (for the lipstick bullets)

Usage: pmu_pack.py   (reads website/m/ig, writes website/m/ig/pmu and pmu.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
IG = HERE.parents[2] / "website/m/ig"
OUT = IG / "pmu"

PAIRS = {  # slug: half size used
    "pmu-dudak-a": "795", "pmu-dudak-b": "800", "pmu-dudak-c": "480", "dudak-cift-5": "480", "dudak-cift-1": "800",
    "pmu-kas-cift-a": "800", "pmu-kas-cift-b": "800", "pmu-goz-a": "795", "goz-cizgisi-cift": "800",
}
TONES = [  # id, draft name (owner approves), source, source box (cuts the "DUDAK RENKLENDİRME" pill + signature)
    ("gulpembe", "Gül pembe", "pmu-ton-gulpembe-1200.webp", None),
    ("visne", "Vişne", "pmu-ton-visne-1200.webp", None),
    ("gulkurusu", "Gül kurusu", "pmu-ton-gulkurusu-1200.webp", None),
    ("kiremit", "Kiremit", "dudak-1-1200.webp", (0, 0, 1200, 1120)),
    ("mercan", "Mercan", "dudak-2-1200.webp", (0, 0, 1200, 1120)),
]
CELL = (600, 800)


def cover(im: Image.Image, size: tuple[int, int], focus=(0.5, 0.5)) -> Image.Image:
    w, h = size
    k = max(w / im.width, h / im.height)
    r = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    x = int((r.width - w) * focus[0])
    y = int((r.height - h) * focus[1])
    return r.crop((x, y, x + w, y + h))


def lip_colour(im: Image.Image) -> str:
    """Median of the saturated red pixels (the pigment), ignoring skin, teeth and highlights."""
    a = np.asarray(im.convert("RGB").resize((300, 400))).astype(float)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(axis=2), a.min(axis=2)
    sat = (mx - mn) / np.maximum(mx, 1)
    m = (r > g * 1.6) & (r > b * 1.4) & (sat > .38) & (mx > 110) & (mx < 240)
    if m.sum() < 200:
        m = r > g * 1.2
    med = np.median(a[m], axis=0)
    return "#%02X%02X%02X" % tuple(int(v) for v in med)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = {"pairs": {}, "tones": [], "kartela": {"cell": CELL, "cols": 3}, "oda": {}}
    for slug, size in PAIRS.items():
        a = Image.open(IG / f"{slug}-once-{size}.webp").convert("RGB")
        b = Image.open(IG / f"{slug}-sonra-{size}.webp").convert("RGB")
        if b.size != a.size:
            b = b.resize(a.size, Image.LANCZOS)
        sheet = Image.new("RGB", (a.width * 2, a.height))
        sheet.paste(a, (0, 0))
        sheet.paste(b, (a.width, 0))
        sheet.save(OUT / f"{slug}-pair.webp", quality=80, method=6)
        meta["pairs"][slug] = {"w": a.width, "h": a.height, "file": f"m/ig/pmu/{slug}-pair.webp"}
    cols = 3
    rows = (len(TONES) + cols - 1) // cols
    kart = Image.new("RGB", (CELL[0] * cols, CELL[1] * rows), (14, 13, 12))
    for i, (tid, name, src, box) in enumerate(TONES):
        im = Image.open(IG / src).convert("RGB")
        if box:
            im = im.crop(box)
        kart.paste(cover(im, CELL), ((i % cols) * CELL[0], (i // cols) * CELL[1]))
        meta["tones"].append({"id": tid, "n": name, "c": lip_colour(im), "i": i})
    kart.save(OUT / "kartela.webp", quality=80, method=6)
    meta["kartela"]["file"] = "m/ig/pmu/kartela.webp"
    meta["kartela"]["rows"] = rows
    oa = Image.open(IG / "pmu-oda-istasyon-680.webp").convert("RGB")
    ob = Image.open(IG / "pmu-oda-yatak-680.webp").convert("RGB")
    ob = ob.resize(oa.size, Image.LANCZOS) if ob.size != oa.size else ob
    oda = Image.new("RGB", (oa.width * 2, oa.height))
    oda.paste(oa, (0, 0))
    oda.paste(ob, (oa.width, 0))
    oda.save(OUT / "oda.webp", quality=80, method=6)
    meta["oda"] = {"file": "m/ig/pmu/oda.webp", "w": oa.width, "h": oa.height}
    (HERE / "pmu.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: (len(v) if isinstance(v, (dict, list)) else v) for k, v in meta.items()}), [t["c"] for t in meta["tones"]])


if __name__ == "__main__":
    main()
