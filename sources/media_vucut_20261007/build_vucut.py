#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vücut / incelme ailesi -- web medyasını salonun kendi Instagram medyasından üretir.

manifest_vucut.json'daki elle seçilmiş kalemleri okur ve OUT altına yazar (varsayılan website/m/ig):

  <slug>.mp4 + <slug>-poster.webp        video: trim, isteğe bağlı 4:5 kırpım (gömülü yazıyı dışarıda bırakır),
                                         hafif gürültü azaltma + ince keskinlik, H.264 <= 720 px, sessiz, faststart
  <slug>-{480,720}.webp                  still: videodan tek kare (kırpılmış)
  <slug>-once-480.webp / -sonra-480.webp pair: önce/sonra yarımlarından AYNI kutu, AYNI filtre
  <slug>-{480,800,960}.webp              join: iki yarım yeniden yan yana (orijinal kolaj; monogram ve imza yerinde)
  <slug>-360.webp                        frame: kolaj videosundan tam kare (büyütülmez)
  media_index.json                       mevcut indekse fam "vucut" kayıtları eklenir/güncellenir

Kaynak sırası: depodaki originals/instagram/videos/*_<id>.mp4, yoksa sunucudaki instagram_library (salt okunur).
pair/join yerelde website/m/ig/bolgesel-cift-{once,sonra}-480.webp yarımlarını kullanır (zaten GRADE almış;
tekrar renk ayarı yapılmaz). Sunucuda tam çözünürlük için aynı kutular server_once_box/server_sonra_box olarak
manifestte durur; build_media.py'nin once_box/sonra_box anahtarlarıyla 540 px üretilir.

Dürüstlük: önce ve sonra yarımı asla ayrı parlatılmaz; görsel büyütülmez; sahte önce/sonra üretilmez.

  python3 sources/media_vucut_20261007/build_vucut.py [--out DIR] [--only slug,slug]
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
RAW_VIDEOS = REPO / "originals" / "instagram" / "videos"
LIB = Path("/var/www/seldagencerbeauty.com/all_api_meta/instagram_library")
# build_media.py ile aynı temel renk ayarı; ten rengi kaydırılmaz
GRADE = "eq=contrast=1.03:saturation=1.03:gamma=1.01"
# telefon videosu: hafif zamansal gürültü azaltma + ince uyarlamalı keskinlik
CLEAN = "hqdn3d=1.5:1.5:6:6,cas=0.25"


def run(*args: str) -> str:
    return subprocess.run(list(args), capture_output=True, text=True, check=True).stdout


def ff(*args: str) -> None:
    run("ffmpeg", "-loglevel", "error", "-y", *args)


def probe(path: Path) -> tuple[int, int, float]:
    out = run("ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
              "stream=width,height:format=duration", "-of", "csv=p=0", str(path)).split()
    w, h = (int(x) for x in out[0].split(",")[:2])
    return w, h, float(out[1]) if len(out) > 1 and out[1] not in ("N/A", "") else 0.0


def video_source(mid: str) -> Path:
    hits = sorted(RAW_VIDEOS.glob(f"*_{mid}.mp4"))
    if hits:
        return hits[0]
    db_path = LIB / "instagram.db"
    if db_path.is_file():
        db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        row = db.execute("select path from assets where owner_id=? and media_type='VIDEO' order by path limit 1",
                         (mid,)).fetchone()
        if row:
            p = Path(row[0])
            return p if p.is_absolute() else LIB / p
    raise SystemExit(f"video bulunamadı: {mid}")


def chain(*parts: str | None) -> str:
    return ",".join(p for p in parts if p)


def webp(src: Path, vf: str, dst: Path, quality: int, ss: float | None = None) -> None:
    pre = ["-ss", f"{ss:.3f}"] if ss is not None else []
    ff(*pre, "-i", str(src), "-frames:v", "1", "-vf", vf, "-c:v", "libwebp", "-quality", str(quality), str(dst))


def crop_size(crop: str | None, w: int, h: int) -> tuple[int, int]:
    if not crop:
        return w, h
    cw, ch = crop.split(":")[:2]
    return int(cw), int(ch)


def build_video(it: dict, out: Path) -> dict:
    src = video_source(it["id"])
    w, h, dur = probe(src)
    t0, t1 = it.get("trim", [0, dur])
    t1 = min(t1, dur)
    crop = f"crop={it['crop']}" if it.get("crop") else None
    cw, ch = crop_size(it.get("crop"), w, h)
    scale = None if max(cw, ch) <= 1280 else ("scale=-2:1280" if ch >= cw else "scale=1280:-2")
    mp4 = out / f"{it['slug']}.mp4"
    ff("-ss", f"{t0:.3f}", "-to", f"{t1:.3f}", "-i", str(src), "-vf",
       chain(crop, scale, "fps=30", CLEAN, GRADE, "format=yuv420p"),
       "-c:v", "libx264", "-preset", "slow", "-crf", str(it.get("crf", 26)), "-profile:v", "high", "-an",
       "-movflags", "+faststart", str(mp4))
    poster = out / f"{it['slug']}-poster.webp"
    webp(src, chain(crop, "scale=720:-2:flags=lanczos", "hqdn3d=1:1:0:0", GRADE), poster, 80,
         it.get("poster_t", t0 + min(0.4, (t1 - t0) / 3)))
    return {"mp4": mp4.name, "poster": poster.name, "w": cw, "h": ch, "dur": round(t1 - t0, 2),
            "bytes": mp4.stat().st_size}


def build_still(it: dict, out: Path) -> dict:
    src = video_source(it["id"])
    w, h, _ = probe(src)
    crop = f"crop={it['crop']}" if it.get("crop") else None
    cw, ch = crop_size(it.get("crop"), w, h)
    files = {}
    for s in (480, 720):
        if s > cw:
            break
        name = f"{it['slug']}-{s}.webp"
        webp(src, chain(crop, f"scale={s}:-2:flags=lanczos", "hqdn3d=1:1:0:0", "cas=0.2", GRADE), out / name,
             80 if s < 720 else 78, it["t"])
        files[s] = name
    return {"full": {"files": files, "w": cw, "h": ch}}


def build_pair(it: dict, out: Path) -> dict:
    x0, y0, x1, y1 = it["box"]
    vf = f"crop={x1 - x0}:{y1 - y0}:{x0}:{y0}"
    res = {}
    for half in ("once", "sonra"):
        src = out / it[f"src_{half}"]
        name = f"{it['slug']}-{half}-480.webp"
        # yarımlar build_media.py'de GRADE almıştı: yalnızca kırpılır, renk ayarı tekrarlanmaz
        webp(src, vf, out / name, 88)
        res[half] = {"files": {480: name}, "w": x1 - x0, "h": y1 - y0}
    return res


def build_join(it: dict, out: Path) -> dict:
    once, sonra = out / it["src_once"], out / it["src_sonra"]
    w, h, _ = probe(once)
    files = {}
    for s in (480, 800, 2 * w):
        name = f"{it['slug']}-{s}.webp"
        ff("-i", str(once), "-i", str(sonra), "-filter_complex",
           f"[0][1]hstack=2,scale={s}:-2:flags=lanczos", "-frames:v", "1", "-c:v", "libwebp",
           "-quality", "84", str(out / name))
        files[s] = name
    return {"full": {"files": files, "w": 2 * w, "h": h}}


def build_frame(it: dict, out: Path) -> dict:
    src = video_source(it["id"])
    w, h, _ = probe(src)
    cw, ch = crop_size(it.get("crop"), w, h)
    name = f"{it['slug']}-{cw}.webp"
    webp(src, chain(f"crop={it['crop']}" if it.get("crop") else None, GRADE), out / name, 88, it.get("t", 0))
    return {"full": {"files": {cw: name}, "w": cw, "h": ch}}


BUILDERS = {"video": build_video, "still": build_still, "pair": build_pair, "join": build_join,
            "frame": build_frame}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=REPO / "website" / "m" / "ig")
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    man = json.loads((HERE / "manifest_vucut.json").read_text(encoding="utf-8"))
    only = {s for s in args.only.split(",") if s}
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    idx_path = out / "media_index.json"
    index = json.loads(idx_path.read_text(encoding="utf-8")) if idx_path.exists() else {}
    for it in man["items"]:
        if only and it["slug"] not in only:
            continue
        rec = {"fam": "vucut", "kind": "video" if it["kind"] == "video" else "image", "alt": it["alt"],
               "id": it["id"], "permalink": index.get(it["slug"], {}).get("permalink"),
               "date": index.get(it["slug"], {}).get("date"), "yuz": bool(it.get("yuz"))}
        if it["id"] == "18319579426235256" and "bolgesel-cift" in index:
            rec["permalink"], rec["date"] = index["bolgesel-cift"]["permalink"], index["bolgesel-cift"]["date"]
        elif not rec["date"] and it["kind"] in ("video", "still", "frame"):
            # depodaki ham video adı paylaşım zamanıyla başlar: 2026-08-27T...Z_<id>.mp4
            rec["date"] = video_source(it["id"]).name[:10]
        rec.update(BUILDERS[it["kind"]](it, out))
        rec["split"] = "v" if it["kind"] == "pair" else None
        index[it["slug"]] = rec
        print(f"  {it['slug']:<20} {it['kind']}")
    idx_path.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  {len(index)} kayit -> {idx_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
