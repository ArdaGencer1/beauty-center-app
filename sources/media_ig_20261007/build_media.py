#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ M (plan 0b) -- build web media from the salon's own Instagram library.

Reads manifest.json (the hand-picked items) and instagram_library/instagram.db (read-only, authoritative
for asset paths), and writes web-ready files under OUT/images/ig/:

  <slug>-{480,800,1200}.webp            single images (only sizes the source can fill)
  <slug>-once-*.webp / <slug>-sonra-*.webp   pairs split from collages (split h / v / h3)
  <slug>.mp4 + <slug>-poster.webp       videos: H.264 <= 720x1280, no audio, faststart
  film/<slug>/fNN.webp                  scroll-scrub frames for items with "film": N
  <slug>-mask.png                       red-nail alpha mask for items with "mask": true
  media_index.json                      what was built: files, sizes, alt, flags (the site patch reads it)

Item keys added for the PMU vitrines (2026-10-07; all optional, older items build exactly as before):
  file            a local source (site jpeg) instead of an Instagram `id`
  crop            [x0,y0,x1,y1] source pixels kept for a single image (cuts label pills and signatures)
  once_box        [x0,y0,x1,y1] source pixels of each half; overrides `split` (collages whose seam is
  sonra_box       not at the middle)
  delogo          [[x,y,w,h], ...] source pixels interpolated away before cropping (monogram on plain skin)
  align           {"once": [[x,y],[x,y]], "sonra": [[x,y],[x,y]]}: two untreated landmarks per half, in
                  source pixels; the sonra half is warped (scale, rotation, shift) onto the once half
  pair_crop       [x0,y0,x1,y1] in once-half pixels, cut from both halves after alignment
  grade           "pmu" for the PMU grade; a pair's halves always get the same grade
  vignette        true: a soft vignette (single images only, never on a before/after half)
  sizes, film_w   output widths; film frame width

Nothing under public_html is touched; the site patch copies OUT into place.

  ./run patches/media_ig_20261007/build_media.py [--out DIR] [--avif] [--only slug,slug]
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import tempfile
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path("/var/www/seldagencerbeauty.com")
LIB = ROOT / "all_api_meta" / "instagram_library"
GRADE = "eq=contrast=1.03:saturation=1.03:gamma=1.01"
# PMU: a touch more contrast and micro-contrast; no hue shift, so pigment colour stays as photographed
GRADES = {"pmu": "eq=contrast=1.05:saturation=1.02:gamma=0.985,unsharp=5:5:0.45:5:5:0"}
SIZES = (480, 800, 1200)


def run(*args: str) -> str:
    return subprocess.run(list(args), capture_output=True, text=True, check=True).stdout


def probe(path: Path) -> tuple[int, int, float]:
    out = run("ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
              "stream=width,height:format=duration", "-of", "csv=p=0", str(path)).split()
    w, h = (int(x) for x in out[0].split(",")[:2])
    dur = float(out[1]) if len(out) > 1 and out[1] not in ("N/A", "") else 0.0
    return w, h, dur


def asset(db: sqlite3.Connection, mid: str, kind: str, item: int | None) -> Path:
    if kind == "video":
        row = db.execute("select path from assets where owner_id=? and media_type='VIDEO' order by path limit 1",
                         (mid,)).fetchone()
    else:
        rows = db.execute("select path from assets where owner_id=? and media_type='IMAGE' and kind!='thumbnail' "
                          "order by path", (mid,)).fetchall()
        row = rows[(item or 1) - 1] if rows else None
    if not row:
        raise SystemExit(f"asset not found: {mid}")
    p = Path(row[0])
    return p if p.is_absolute() else LIB / p


def webp_set(src: Path, crop: str | None, base: Path, avif: bool) -> dict:
    """Write base-{size}.webp for the sizes the (cropped) source can fill; return {size: name}."""
    w, h, _ = probe(src)
    if crop:
        cw, ch = (int(eval(x, {}, {"iw": w, "ih": h})) for x in crop.split(":")[:2])
    else:
        cw, ch = w, h
    return webp_chain(src, f"crop={crop}" if crop else "", cw, ch, base, avif)


def webp_chain(src: Path, chain: str, cw: int, ch: int, base: Path, avif: bool, grade: str = GRADE,
               sizes: tuple = SIZES) -> dict:
    """webp_set for an arbitrary pre-scale filter chain whose output is cw x ch."""
    out = {}
    for s in sizes:
        if s > cw and out:
            break
        tw = min(s, cw)
        vf = (f"{chain}," if chain else "") + f"scale={tw}:-2:flags=lanczos,{grade}"
        name = f"{base.name}-{s}.webp"
        run("ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-vf", vf, "-c:v", "libwebp",
            "-quality", "78" if s < 1200 else "74", str(base.parent / name))
        if avif:
            run("ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-vf", vf, "-c:v", "libaom-av1",
                "-still-picture", "1", "-crf", "33", "-cpu-used", "6", str(base.parent / f"{base.name}-{s}.avif"))
        out[s] = name
    return {"files": out, "w": cw, "h": ch}


def box_crop(b: list) -> str:
    x0, y0, x1, y1 = (int(round(v)) for v in b)
    return f"crop={x1 - x0}:{y1 - y0}:{x0}:{y0}"


def delogo_chain(boxes: list | None) -> list[str]:
    return [f"delogo=x={x}:y={y}:w={w}:h={h}" for x, y, w, h in boxes or []]


def pair_halves(it: dict, w: int, h: int, outdir: Path, src: Path, avif: bool) -> tuple[dict, dict]:
    """Before/after halves from explicit boxes, optionally warped onto each other and cut to one window.

    The warp is a similarity transform fitted to two untreated landmarks per half (nose, eye corners),
    applied with ffmpeg `perspective` (exact for affine maps). Both halves get the same crop and grade.
    """
    sp = it.get("split")
    ob, sb = it.get("once_box"), it.get("sonra_box")
    if not ob:
        ob, sb = ([0, 0, w, h // 2], [0, h // 2, w, h]) if sp == "h" else ([0, 0, w // 2, h], [w // 2, 0, w, h])
    W, H = ob[2] - ob[0], ob[3] - ob[1]
    sw, sh = sb[2] - sb[0], sb[3] - sb[1]
    pre = delogo_chain(it.get("delogo"))
    grade = GRADES.get(it.get("grade"), GRADE)
    sizes = tuple(it.get("sizes", SIZES))
    once_chain = pre + [box_crop(ob)]
    sonra_chain = pre + [box_crop(sb)]
    al = it.get("align")
    if al:
        a1, a2 = (complex(x - ob[0], y - ob[1]) for x, y in al["once"])
        b1, b2 = (complex(x - sb[0], y - sb[1]) for x, y in al["sonra"])
        k = (a2 - a1) / (b2 - b1)

        def inv(z: complex) -> complex:  # once-half point -> sonra-half point
            return b1 + (z - a1) / k
        # perspective keeps the frame size: pad the sonra half to cover the once frame, warp, then cut W x H
        Wp, Hp = max(W, sw), max(H, sh)
        corners = [inv(complex(0, 0)), inv(complex(Wp, 0)), inv(complex(0, Hp)), inv(complex(Wp, Hp))]
        if (sw, sh) != (Wp, Hp):
            sonra_chain.append(f"pad={Wp}:{Hp}:0:0")
        args = ":".join(f"x{i}={c.real:.2f}:y{i}={c.imag:.2f}" for i, c in enumerate(corners))
        sonra_chain.append(f"perspective={args}:interpolation=cubic:sense=source")
        if (Wp, Hp) != (W, H):
            sonra_chain.append(f"crop={W}:{H}:0:0")
        print(f"    align scale={abs(k):.3f} rot={__import__('math').degrees(__import__('cmath').phase(k)):.2f}deg")
    elif (sw, sh) != (W, H):
        raise SystemExit(f"{it['slug']}: halves differ ({W}x{H} vs {sw}x{sh}); give align or equal boxes")
    pc = it.get("pair_crop")
    if pc:
        once_chain.append(box_crop(pc))
        sonra_chain.append(box_crop(pc))
        W, H = pc[2] - pc[0], pc[3] - pc[1]
    once = webp_chain(src, ",".join(once_chain), W, H, outdir / f"{it['slug']}-once", avif, grade, sizes)
    sonra = webp_chain(src, ",".join(sonra_chain), W, H, outdir / f"{it['slug']}-sonra", avif, grade, sizes)
    return once, sonra


def fill_holes(m: bytearray, w: int, h: int, max_area: int | None = None) -> bytearray:
    """Set the enclosed background regions of a 0/non-0 mask (only those up to max_area pixels, if given)."""
    n = w * h
    seen = bytearray(n)
    out = bytearray(m)
    for start in range(n):
        if m[start] or seen[start]:
            continue
        q, px, border = deque([start]), [start], False
        seen[start] = 1
        while q:
            j = q.popleft()
            x, y = j % w, j // w
            if x == 0 or y == 0 or x == w - 1 or y == h - 1:
                border = True
            for k in ((j - 1) if x > 0 else -1, (j + 1) if x < w - 1 else -1, j - w, j + w):
                if 0 <= k < n and not m[k] and not seen[k]:
                    seen[k] = 1
                    q.append(k)
                    px.append(k)
        if not border and (max_area is None or len(px) <= max_area):
            for j in px:
                out[j] = 1
    return out


def nail_mask(src_webp: Path, dst_png: Path, tmp: Path, rmin: int = 55, cuts: list | None = None,
              sat: float = 0.58, area: float = 0.0008, grow: int = 4, keeps: list | None = None,
              lo: float | None = None, fills: list | None = None, hi: float | None = None,
              box_sat: float | None = None, softs: list | None = None) -> None:
    """Red/bordo nails -> white alpha matte.

    Seeds are saturated-red components shaped like nail plates (r-max(g,b) > sat*r), highlights filled in.
    The seed interior (2 px in) is fully painted; in a `grow` px band around it the alpha follows redness
    (lo..sat), so the nail's own soft edge is painted and the skin beside it is not. A hard shrunk edge
    left a red rim on dark colours, a hard grown edge a pale halo on light ones. lo/hi are the skin's and the
    nail's own redness: a pixel that is part nail, part skin has a redness linear in that share.
    """
    w, h, _ = probe(src_webp)
    n = w * h
    lo = sat - 0.22 if lo is None else lo
    hi = sat if hi is None else hi
    span = max(hi - lo, 0.05)
    box_sat = (sat + lo) / 2 if box_sat is None else box_sat
    raw = tmp / "m0.rgb"
    run("ffmpeg", "-loglevel", "error", "-y", "-i", str(src_webp), "-f", "rawvideo", "-pix_fmt", "rgb24", str(raw))
    d = raw.read_bytes()
    fg = bytearray(n)
    soft = bytearray(n)
    # inside hand-placed keep/fill boxes the seed threshold drops halfway to `lo` (shaded and out-of-focus nails)
    boxes = [(int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)) for x0, y0, x1, y1 in (keeps or []) + (fills or [])]
    for i in range(n):
        r = d[3 * i]
        if r <= 20:
            continue
        g, b = d[3 * i + 1], d[3 * i + 2]
        q = (r - (g if g > b else b)) / r
        if q > sat and r > rmin:
            fg[i] = 1
        elif boxes and q > box_sat and r > rmin:
            x, y = i % w, i // w
            if any(x0 <= x < x1 and y0 <= y < y1 for x0, y0, x1, y1 in boxes):
                fg[i] = 1
        if q > lo:
            soft[i] = 255 if q >= lo + span else int((q - lo) / span * 255)
    # hand-placed cuts (fractions x0,y0,x1,y1) for clothing or skin that reads as red
    for x0, y0, x1, y1 in cuts or []:
        for y in range(int(y0 * h), int(y1 * h)):
            for x in range(int(x0 * w), int(x1 * w)):
                fg[y * w + x] = 0
                soft[y * w + x] = 0
    seen = bytearray(n)
    keep = bytearray(n)
    for i in range(n):
        if fg[i] and not seen[i]:
            q, px = deque([i]), [i]
            seen[i] = 1
            while q:
                j = q.popleft()
                x = j % w
                for k in ((j - 1) if x > 0 else -1, (j + 1) if x < w - 1 else -1, j - w, j + w):
                    if 0 <= k < n and fg[k] and not seen[k]:
                        seen[k] = 1
                        q.append(k)
                        px.append(k)
            # nails can run off the side of the frame, but blobs touching the top edge are clothing/background
            edge = any(j // w == 0 for j in px)
            # nails are compact plates; reddish skin creases and shadows are thin slivers
            xs = [j % w for j in px]
            ys = [j // w for j in px]
            bw, bh = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
            compact = min(bw, bh) >= 0.025 * w and len(px) / (bw * bh) >= 0.42
            # hand-placed boxes: `keeps` are nails that fail the shape rules (out of focus, merged with a
            # neighbour); `fills` are side-view nails, a red rim around a pale reflection
            cx, cy = (min(xs) + bw / 2) / w, (min(ys) + bh / 2) / h
            kept = any(x0 <= cx <= x1 and y0 <= cy <= y1 for x0, y0, x1, y1 in keeps or [])
            forced = any(x0 <= cx <= x1 and y0 <= cy <= y1 for x0, y0, x1, y1 in fills or [])
            if os.environ.get("MASK_DEBUG") and len(px) > 200:
                print(f"    comp c=({cx:.3f},{cy:.3f}) box=({min(xs)/w:.3f},{min(ys)/h:.3f},{max(xs)/w:.3f},{max(ys)/h:.3f})"
                      f" px={len(px)} fill={len(px)/(bw*bh):.2f} edge={edge} compact={compact}"
                      f" -> {'FILL' if forced else 'KEEP' if kept or (len(px) > n * area and not edge and compact) else '-'}")
            if kept:
                for j in px:
                    keep[j] = 1
            elif forced:
                # fill each row between the rim's outer pixels so the reflection inside is coloured too
                rows: dict[int, list[int]] = {}
                for j in px:
                    rows.setdefault(j // w, []).append(j % w)
                for y, row in rows.items():
                    for x in range(min(row), max(row) + 1):
                        keep[y * w + x] = 1
            elif len(px) > n * area and not edge and compact:
                for j in px:
                    keep[j] = 1
    # highlights inside a nail plate: fill every hole of the seeds
    keep = fill_holes(keep, w, h)
    (tmp / "keep.gray").write_bytes(bytes(255 if v else 0 for v in keep))
    gray = ["-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{w}x{h}"]

    def morph(src: str, dst: str, ops: list[str]) -> bytes:
        run("ffmpeg", "-loglevel", "error", "-y", *gray, "-i", str(tmp / src), "-vf", ",".join(ops), *gray[:4],
            str(tmp / dst))
        return (tmp / dst).read_bytes()

    # gate = seeds grown `grow` px; slits the growth closes (a side-view nail's rim) are filled too, but not
    # the skin between neighbouring nails
    gate = fill_holes(bytearray(morph("keep.gray", "gate0.gray", ["dilation"] * grow)), w, h, int(n * 0.0003))
    gate = bytearray(255 if v else 0 for v in gate)
    (tmp / "gate.gray").write_bytes(bytes(gate))
    core = morph("gate.gray", "core.gray", ["erosion"] * (grow + 2))
    # ease the edge band up (1-(1-a)^2): what is left of the original there is red, so lean towards paint
    ease = bytes(255 - (255 - v) * (255 - v) // 255 for v in range(256))
    m2 = bytearray(min(gate[i], max(core[i], ease[soft[i]])) for i in range(n))
    # `softs` boxes hold out-of-focus nails: their own redness is the matte, no filled core (it would paint
    # the blurred skin between them as one pale cloud)
    for x0, y0, x1, y1 in softs or []:
        for y in range(int(y0 * h), int(y1 * h)):
            for i in range(y * w + int(x0 * w), y * w + int(x1 * w)):
                m2[i] = min(gate[i], soft[i])
    (tmp / "m2.gray").write_bytes(bytes(m2))
    # neutral plate: the same photo with the polish's red taken out around the nails. Shown under a recolour,
    # so the part of an edge pixel the paint leaves shows skin, not a red ring. Skin chroma = median g/r, b/r
    # of the unpainted ring around the nails.
    gs, bs = [], []
    for i in range(0, n, 3):
        if gate[i] and not soft[i] and d[3 * i] > 60:
            gs.append(d[3 * i + 1] / d[3 * i])
            bs.append(d[3 * i + 2] / d[3 * i])
    gs.sort()
    bs.sort()
    kg, kb = (gs[len(gs) // 2], bs[len(bs) // 2]) if gs else (0.68, 0.52)
    # within ~10 px of the nails, move g and b towards skin chroma by how far short of skin the pixel's
    # chroma falls: polish red (and its blur) goes, skin, highlights and shading stay
    kmax = max(kg, kb)
    wide = morph("keep.gray", "wide.gray", ["dilation"] * (grow + 6))
    plate = bytearray(d)
    for i in range(n):
        if wide[i]:
            r, g, b = d[3 * i], d[3 * i + 1], d[3 * i + 2]
            if r and max(g, b) < r * kmax:
                t = min(1.0, 1.6 * (1 - max(g, b) / (r * kmax)))
                plate[3 * i + 1] = min(255, int(g + (r * kg - g) * t)) if r * kg > g else g
                plate[3 * i + 2] = min(255, int(b + (r * kb - b) * t)) if r * kb > b else b
    (tmp / "plate.rgb").write_bytes(bytes(plate))
    neutral = dst_png.with_name(dst_png.name.replace("-mask.png", "-neutral-1200.webp"))
    run("ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-i",
        str(tmp / "plate.rgb"), "-c:v", "libwebp", "-quality", "74", str(neutral))
    print(f"    skin chroma g/r={kg:.2f} b/r={kb:.2f} -> {neutral.name}")
    run("ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{w}x{h}", "-i",
        str(tmp / "m2.gray"), "-vf", "gblur=sigma=1.0", str(tmp / "m2.png"))
    run("ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"color=c=white:s={w}x{h}", "-i",
        str(tmp / "m2.png"), "-filter_complex", "[0][1]alphamerge,format=rgba", "-frames:v", "1", str(dst_png))


def video(src: Path, it: dict, outdir: Path) -> dict:
    w, h, dur = probe(src)
    t0, t1 = it.get("trim", [0, dur])
    t1 = min(t1, dur)
    scale = "scale=-2:1280" if h >= w else "scale=1280:-2"
    if max(w, h) <= 1280:
        scale = "scale=trunc(iw/2)*2:trunc(ih/2)*2"
    mp4 = outdir / f"{it['slug']}.mp4"
    run("ffmpeg", "-loglevel", "error", "-y", "-ss", str(t0), "-to", str(t1), "-i", str(src), "-vf",
        f"{scale},fps=30,{GRADE}", "-c:v", "libx264", "-preset", "slow", "-crf", "27", "-pix_fmt", "yuv420p",
        "-profile:v", "high", "-an", "-movflags", "+faststart", str(mp4))
    poster = outdir / f"{it['slug']}-poster.webp"
    pt = it.get("poster_t", t0 + min(0.4, (t1 - t0) / 3))
    run("ffmpeg", "-loglevel", "error", "-y", "-ss", str(pt), "-i", str(src),
        "-frames:v", "1", "-vf", f"scale=720:-2,{GRADE}", "-c:v", "libwebp", "-quality", "74", str(poster))
    res = {"mp4": mp4.name, "poster": poster.name, "w": w, "h": h, "dur": round(t1 - t0, 2),
           "bytes": mp4.stat().st_size}
    n = it.get("film")
    if n:
        fd = outdir / "film" / it["slug"]
        fd.mkdir(parents=True, exist_ok=True)
        fw = it.get("film_w") or (540 if h >= w else 960)
        run("ffmpeg", "-loglevel", "error", "-y", "-ss", str(t0), "-to", str(t1), "-i", str(src), "-vf",
            f"fps={n}/{max(0.1, t1 - t0):.3f},scale={fw}:-2,{GRADES.get(it.get('grade'), GRADE)}", "-frames:v", str(n), "-c:v", "libwebp",
            "-quality", "60", str(fd / "f%02d.webp"))
        res["film"] = {"dir": f"film/{it['slug']}", "frames": len(list(fd.glob('f*.webp')))}
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "out")
    ap.add_argument("--avif", action="store_true")
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    man = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    only = {s for s in args.only.split(",") if s}
    outdir = args.out / "images" / "ig"
    outdir.mkdir(parents=True, exist_ok=True)
    idx_path = outdir / "media_index.json"
    index = json.loads(idx_path.read_text(encoding="utf-8")) if idx_path.exists() else {}
    db = sqlite3.connect(f"file:{LIB / 'instagram.db'}?mode=ro", uri=True)
    for it in man["items"]:
        if only and it["slug"] not in only:
            continue
        if it.get("file"):
            src = Path(it["file"]) if Path(it["file"]).is_absolute() else ROOT / it["file"]
            perm = None
        else:
            src = asset(db, it["id"], it["kind"], it.get("item"))
            perm = db.execute("select permalink, timestamp from media where id=?", (it["id"],)).fetchone()
        rec = {k: it[k] for k in ("fam", "kind", "alt") if k in it}
        rec.update({"id": it.get("id") or it["file"], "permalink": perm[0] if perm else None,
                    "date": (perm[1] or "")[:10] if perm else None, "yuz": bool(it.get("yuz"))})
        new_keys = {"file", "crop", "once_box", "delogo", "align", "pair_crop", "grade", "vignette", "sizes"}
        if it["kind"] == "video":
            rec.update(video(src, it, outdir))
        elif new_keys & it.keys():
            w, h, _ = probe(src)
            if it.get("split") or it.get("once_box"):
                rec["once"], rec["sonra"] = pair_halves(it, w, h, outdir, src, args.avif)
            else:
                chain = delogo_chain(it.get("delogo")) + ([box_crop(it["crop"])] if it.get("crop") else [])
                cw, ch = (it["crop"][2] - it["crop"][0], it["crop"][3] - it["crop"][1]) if it.get("crop") else (w, h)
                grade = GRADES.get(it.get("grade"), GRADE) + (",vignette=angle=PI/9" if it.get("vignette") else "")
                rec["full"] = webp_chain(src, ",".join(chain), cw, ch, outdir / it["slug"], args.avif, grade,
                                         tuple(it.get("sizes", SIZES)))
        else:
            sp = it.get("split")
            if sp == "h":
                rec["once"] = webp_set(src, "iw:ih/2:0:0", outdir / f"{it['slug']}-once", args.avif)
                rec["sonra"] = webp_set(src, "iw:ih/2:0:ih/2", outdir / f"{it['slug']}-sonra", args.avif)
            elif sp == "v":
                rec["once"] = webp_set(src, "iw/2:ih:0:0", outdir / f"{it['slug']}-once", args.avif)
                rec["sonra"] = webp_set(src, "iw/2:ih:iw/2:0", outdir / f"{it['slug']}-sonra", args.avif)
            elif sp == "h3":
                rec["once"] = webp_set(src, "iw:ih/3:0:0", outdir / f"{it['slug']}-once", args.avif)
                rec["sonra"] = webp_set(src, "iw:ih/3:0:2*ih/3", outdir / f"{it['slug']}-sonra", args.avif)
                rec["full"] = webp_set(src, None, outdir / it["slug"], args.avif)
            else:
                rec["full"] = webp_set(src, None, outdir / it["slug"], args.avif)
            if it.get("mask"):
                with tempfile.TemporaryDirectory() as tmp:
                    big = outdir / rec["full"]["files"][max(rec["full"]["files"])]
                    nail_mask(big, outdir / f"{it['slug']}-mask.png", Path(tmp), it.get("mask_rmin", 55), it.get("mask_cut"),
                              it.get("mask_sat", 0.58), it.get("mask_area", 0.0008), it.get("mask_grow", 4),
                              it.get("mask_keep"), it.get("mask_lo"), it.get("mask_fill"), it.get("mask_hi"),
                              it.get("mask_box_sat"), it.get("mask_soft"))
                rec["mask"] = f"{it['slug']}-mask.png"
        rec["split"] = it.get("split")
        index[it["slug"]] = rec
        print(f"  {it['slug']:<26} {it['kind']:<5} {it.get('split') or ''}")
        idx_path.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  {len(index)} kayit -> {idx_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
