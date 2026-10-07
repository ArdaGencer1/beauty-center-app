#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Renk Atölyesi v3 -- refine the red-nail mattes and add a shade plate per shape.

The v2 mattes (build_media.py nail_mask) grow a few pixels past the nail and let redness decide the alpha
there. On a light polish (lila, nude, gül) that band shows as a pale outline: the tint layer recolours
the photo's own luminance, and the skin in the band is brighter than the dark red nail, so it maps to a
brighter shade of the new colour. Out-of-focus nails get a hard edge the blurry photo does not have.

Two outputs per shape fix both:

  <slug>-mask.png        the v2 matte refined with a colour guided filter (He et al.) on the photo: the
                         alpha edge follows the photo's own edge, sharp where the nail is sharp and soft
                         where it is out of focus; kept inside a small grow of the v2 matte so it never
                         reaches skin the v2 matte did not.
  <slug>-shade-1200.webp the luminance the tint recolours. Inside the nail it is the photo; in the edge
                         band it is never brighter than the nail just inside it (push-pull fill), so a
                         part-nail part-skin pixel takes the nail's tone and no pale ring is left.

It also prints the mean nail luminance under each new matte (TZ_LREF in the page script).

  python3 -I refine_nail_masks.py --src DIR --out DIR [uzun kare yuvarlak]

DIR holds tirnak-<shape>-kirmizi-1200.webp and the v2 tirnak-<shape>-kirmizi-mask.png. Only numpy and
Pillow are needed.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

LUMA = np.array([0.2126, 0.7152, 0.0722], np.float32)  # feColorMatrix saturate(0) weights


def box(a: np.ndarray, r: int) -> np.ndarray:
    """Mean over a (2r+1)^2 window, edges clamped (cumulative sums, any trailing dims)."""
    p = np.pad(a, [(r + 1, r), (r + 1, r)] + [(0, 0)] * (a.ndim - 2), mode="edge").astype(np.float64)
    c = p.cumsum(0).cumsum(1)
    k = 2 * r + 1
    s = c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]
    return (s / (k * k)).astype(np.float32)


def guided(img: np.ndarray, p: np.ndarray, r: int, eps: float) -> np.ndarray:
    """Colour guided filter: img HxWx3 in 0..1, p HxW in 0..1."""
    mi = box(img, r)
    mp = box(p, r)
    cov = box(img * p[..., None], r) - mi * mp[..., None]
    var = np.empty(p.shape + (3, 3), np.float32)
    for i in range(3):
        for j in range(i, 3):
            v = box(img[..., i] * img[..., j], r) - mi[..., i] * mi[..., j]
            var[..., i, j] = var[..., j, i] = v
    var += eps * np.eye(3, dtype=np.float32)
    a = np.linalg.solve(var, cov[..., None])[..., 0]
    b = mp - (a * mi).sum(-1)
    return (box(a, r) * img).sum(-1) + box(b, r)


def morph(m: np.ndarray, px: int, grow: bool) -> np.ndarray:
    im = Image.fromarray((m * 255).astype(np.uint8))
    f = ImageFilter.MaxFilter if grow else ImageFilter.MinFilter
    for _ in range(px):
        im = im.filter(f(3))
    return np.asarray(im, np.float32) / 255


def push_pull(val: np.ndarray, known: np.ndarray) -> np.ndarray:
    """Fill unknown pixels from the known ones around them (coarse-to-fine weighted average)."""
    levels = []
    v, w = val * known, known.astype(np.float32)
    while min(v.shape) > 8:
        levels.append((v, w))
        h, wd = v.shape
        size = (max(1, wd // 2), max(1, h // 2))
        v = np.asarray(Image.fromarray(v).resize(size, Image.BOX), np.float32)
        w = np.asarray(Image.fromarray(w).resize(size, Image.BOX), np.float32)
    est = v / np.maximum(w, 1e-6)
    for v, w in reversed(levels):
        up = np.asarray(Image.fromarray(est).resize((v.shape[1], v.shape[0]), Image.BILINEAR), np.float32)
        a = np.clip(w * 4, 0, 1)
        est = a * (v / np.maximum(w, 1e-6)) + (1 - a) * up
    return est


def small_holes(solid: np.ndarray, max_px: int) -> np.ndarray:
    """Pixels of the not-solid regions that the border cannot reach and that are smaller than max_px."""
    h, w = solid.shape
    # flood the free area from a 1 px frame; what stays unflooded is enclosed
    im = Image.fromarray(np.pad(np.where(solid, 0, 255), 1, constant_values=255).astype(np.uint8))
    ImageDraw.floodfill(im, (0, 0), 128)
    enclosed = np.asarray(im)[1:-1, 1:-1] == 255
    seen = np.zeros_like(enclosed)
    out = np.zeros_like(enclosed)
    for y0, x0 in zip(*np.nonzero(enclosed)):
        if seen[y0, x0]:
            continue
        stack, px = [(y0, x0)], []
        seen[y0, x0] = True
        while stack:
            y, x = stack.pop()
            px.append((y, x))
            for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                if 0 <= yy < h and 0 <= xx < w and enclosed[yy, xx] and not seen[yy, xx]:
                    seen[yy, xx] = True
                    stack.append((yy, xx))
        if len(px) <= max_px:
            ys, xs = zip(*px)
            out[ys, xs] = True
    return out


def refine(src: Path, out: Path, shape: str) -> float:
    slug = f"tirnak-{shape}-kirmizi"
    img = np.asarray(Image.open(src / f"{slug}-1200.webp").convert("RGB"), np.float32) / 255
    m0 = np.asarray(Image.open(src / f"{slug}-mask.png"))[..., 3].astype(np.float32) / 255
    # alpha follows the photo's edges; r=5 px at 1200 w is ~1.6 css px on a phone
    q = np.clip(guided(img, m0, 5, 2e-3), 0, 1)
    # never further out than 3 px past the v2 matte, never less than its solid core
    gate = morph((m0 > 0.03).astype(np.float32), 3, True)
    core = morph((m0 > 0.97).astype(np.float32), 2, False)
    q = np.maximum(np.minimum(q, gate), core)
    # reflections inside a nail (pale patches the redness test left out, mostly on out-of-focus nails)
    holes = small_holes(q > 0.5, int(q.size * 0.002))
    q[holes] = 1
    q[q < 0.03] = 0
    q[q > 0.97] = 1
    # the same 1 px blur the v2 matte had, so the edge is anti-aliased at any zoom
    qa = np.asarray(Image.fromarray((q * 255).round().astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)))
    rgba = np.dstack([np.full(qa.shape + (3,), 255, np.uint8), qa])
    Image.fromarray(rgba, "RGBA").save(out / f"{slug}-mask.png", optimize=True)

    L = img @ LUMA
    inside = q > 0.9
    fill = push_pull(L, inside.astype(np.float32))
    band = (qa > 0) & ~inside
    shade = L.copy()
    # edge band: the nail's own tone, at most a little darker (a natural sidewall), never brighter (skin)
    shade[band] = np.clip(L[band], 0.85 * fill[band], fill[band])
    # outside the matte nothing shows; a flat tone keeps the file small
    shade[qa == 0] = float(L[inside].mean())
    Image.fromarray((shade * 255).round().clip(0, 255).astype(np.uint8), "L").save(
        out / f"{slug}-shade-1200.webp", quality=88, method=6)
    lref = float(L[q > 0.9].mean())
    print(f"{shape}: core {inside.mean():.3f} of frame, band {band.mean():.4f}, holes {holes.sum()} px, LREF {lref:.3f}")
    return lref


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("shapes", nargs="*", default=["uzun", "kare", "yuvarlak"])
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    for s in a.shapes:
        refine(a.src, a.out, s)


if __name__ == "__main__":
    main()
