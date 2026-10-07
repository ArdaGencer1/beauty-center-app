#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CİLT ATLASI · medya v2 (depo içi kaynaklarla).

Girdi:   originals/instagram/videos/<tarih>_<IG id>.mp4  ve  website/m/ig/ altındaki işlenmiş kareler.
Çıktı:   website/m/ig/<slug>.mp4, <slug>-poster.webp, film/<slug>.webp (sprite), <slug>-once/-sonra-480.webp
         + data/cilt_media.json (slug -> kaynak, kesim, karar) + website/m/ig/media_index.json içine kayıt.

Dürüstlük kuralları (plan 10-07, §2):
  * Önce ve sonra yarımlarına aynı işlem uygulanır; "sonra" ayrıca parlatılmaz, rötuşlanmaz.
  * Hiçbir görsel büyütülmez.  Videolara tek, hafif ve ortak "atelier" renk ayarı uygulanır.
  * Kesimler sahne sınırlarına göre (ffmpeg scene > 0.3) seçildi; her klip tek bir gerçek çekimdir.

Kullanım:  python3 sources/atelier_cilt_20261007/build_cilt_media.py [--only slug,slug] [--dry]
"""
from __future__ import annotations

import argparse
import glob
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SRC_VID = REPO / "originals" / "instagram" / "videos"
OUT = REPO / "website" / "m" / "ig"
INDEX = OUT / "media_index.json"
LOG = HERE / "data" / "cilt_media.json"

# Hafif sıcak ton; tüm kliplerde aynı.  Kontrast/doygunluk çok küçük tutuldu.
GRADE = "colortemperature=temperature=6100:mix=0.6,eq=contrast=1.03:saturation=1.04"

VIDEOS = [
    # slug, IG id, başlangıç, bitiş, poster sn (klip içi), ek filtre, hedef KB, alt, kaynak notu
    dict(slug="cilt-led-dongu", id="18617996404000518", ss=0.55, to=8.40, poster=5.0, extra="", kb=1200,
         alt="LED ışık terapisi: yüz maskesinde yeşil, kırmızı, mor ve mavi ışık", note="#6, 0,53 ve 8,4 sn kesimleri arası"),
    dict(slug="cilt-kubbe", id="18119195767718567", ss=5.0, to=17.0, poster=5.0, extra="stab", kb=1000,
         alt="LED kubbe altında cilt bakımı", note="#10 elde çekim; vidstab ile sabitlendi"),
    dict(slug="cilt-saten", id="18192437785391754", ss=1.70, to=6.50, poster=1.6, extra="", kb=900,
         alt="Saten yüz germe başlığı yanak ve şakakta", note="#16 tek çekim (1,63–6,57 sn)"),
    dict(slug="cilt-saten-yakin", id="18192437785391754", ss=6.62, to=13.20, poster=0.6, extra="", kb=900,
         alt="Saten yüz germe başlığı alın ve göz çevresinde, yakın plan", note="#16 son iki çekim"),
    dict(slug="cilt-analiz", id="18122366353896732", ss=3.20, to=6.65, poster=0.9, extra="", kb=700,
         alt="Büyüteçli lamba altında cilt analizi", note="#17 lamba + büyüteç çekimleri"),
    dict(slug="cilt-masaj", id="18122366353896732", ss=0.0, to=2.15, poster=0.8, extra="", kb=500,
         alt="Uzman eldivenli ellerle yüze masaj yapıyor", note="#17 ilk çekim"),
    dict(slug="cilt-kopuk", id="18122366353896732", ss=2.24, to=3.12, poster=0.4, extra="boomerang", kb=400,
         alt="Temizleme süngeri ve köpük, yakın plan", note="#17 ikinci çekim; ileri-geri döngü"),
    dict(slug="cilt-komedon", id="18122366353896732", ss=6.74, to=8.64, poster=0.9, extra="", kb=500,
         alt="Steril uçla siyah nokta temizliği, yakın plan", note="#17 son çekim; en fazla 2 sn kuralı"),
    dict(slug="cilt-darsonval", id="18025275239906179", ss=0.0, to=10.08, poster=3.0, extra="dn", kb=1000,
         alt="Darsonval elektrodu akneli yanakta turuncu ışıkla", note="#9 tek çekim; hafif gürültü azaltma"),
]

# Kaydırma filmi: tek dosyalık sprite (Artifact dosya bütçesi için 48 ayrı kare yerine 1 dosya).
FILMS = [
    dict(slug="cilt-saten-film", id="18192437785391754", ss=1.70, to=13.20, n=48, cols=8, w=360, h=640,
         note="#16 kaydırmalı film; siyah geçiş (0,7–1,6 sn) dışarıda"),
]

# Fotoğraf çiftleri: aynı döndürme/kırpma iki yarıma birden.
PAIRS = [
    dict(slug="yuz-cift-1", src="cilt-cift-1", id="18039236768821035", rotate=180, crop=(30, 196, 450, 1110),
         alt="Yüz bakımı öncesi ve sonrası: kızarıklık ve ton farkı, tam yüz",
         note="#21; IG paylaşımı ters çekilmiş, 180° döndürüldü; ters kalan etiket iki yarımdan eşit kırpıldı"),
]


def run(cmd: list[str], dry: bool) -> None:
    print(" ".join(cmd) if len(" ".join(cmd)) < 400 else " ".join(cmd)[:400] + " …")
    if not dry:
        subprocess.run(cmd, check=True)


def src_for(ig_id: str) -> Path:
    m = glob.glob(str(SRC_VID / f"*_{ig_id}.mp4"))
    if not m:
        sys.exit(f"kaynak video yok: {ig_id}")
    return Path(m[0])


def probe(p: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height:format=duration,size", "-of", "json", str(p)],
                       capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    return dict(w=j["streams"][0]["width"], h=j["streams"][0]["height"],
                dur=round(float(j["format"]["duration"]), 2), bytes=int(j["format"]["size"]))


def build_video(v: dict, dry: bool, tmp: Path) -> dict:
    src = src_for(v["id"])
    out = OUT / f"{v['slug']}.mp4"
    dur = v["to"] - v["ss"]
    chain = [GRADE]
    if v["extra"] == "dn":
        chain.insert(0, "hqdn3d=2:2:4:4")
    if v["extra"] == "stab":
        trf = tmp / f"{v['slug']}.trf"
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(v["ss"]), "-t", f"{dur:.2f}", "-i", str(src),
             "-vf", f"vidstabdetect=shakiness=6:accuracy=15:result={trf}", "-f", "null", "-"], dry)
        chain.insert(0, f"vidstabtransform=input={trf}:smoothing=24:zoom=3,unsharp=5:5:0.6:3:3:0.3")
    vf = ",".join(chain) + ",scale=720:-2,format=yuv420p"
    if v["extra"] == "boomerang":
        fc = f"[0:v]{','.join(chain)},scale=720:-2,format=yuv420p,split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1[o]"
        args = ["-filter_complex", fc, "-map", "[o]"]
    else:
        args = ["-vf", vf]
    # Hedef boyuta bit hızıyla yaklaş (2 geçiş yerine sabit üst sınır).
    total = dur * (2 if v["extra"] == "boomerang" else 1)
    kbps = int(v["kb"] * 8 / total * 0.92)
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(v["ss"]), "-t", f"{dur:.2f}", "-i", str(src), *args,
         "-an", "-c:v", "libx264", "-preset", "slow", "-profile:v", "high", "-crf", "23",
         "-maxrate", f"{kbps}k", "-bufsize", f"{kbps * 2}k", "-movflags", "+faststart", str(out)], dry)
    poster = OUT / f"{v['slug']}-poster.webp"
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(v["poster"]), "-i", str(out), "-frames:v", "1",
         "-c:v", "libwebp", "-quality", "72", str(poster)], dry)
    info = probe(out) if not dry else {}
    return dict(kind="video", fam="cilt", id=v["id"], alt=v["alt"], mp4=out.name, poster=poster.name,
                trim=[v["ss"], v["to"]], note=v["note"], **info)


def build_film(f: dict, dry: bool) -> dict:
    src = src_for(f["id"])
    dur = f["to"] - f["ss"]
    rows = -(-f["n"] // f["cols"])
    out = OUT / "film" / f"{f['slug']}.webp"
    out.parent.mkdir(parents=True, exist_ok=True)
    vf = (f"{GRADE},fps={f['n']}/{dur:.3f},scale={f['w']}:{f['h']}:force_original_aspect_ratio=increase,"
          f"crop={f['w']}:{f['h']},tile={f['cols']}x{rows}")
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(f["ss"]), "-t", f"{dur:.3f}", "-i", str(src), "-vf", vf,
         "-frames:v", "1", "-c:v", "libwebp", "-quality", "58", str(out)], dry)
    return dict(kind="film", fam="cilt", id=f["id"], sprite=f"film/{out.name}", frames=f["n"], cols=f["cols"],
                fw=f["w"], fh=f["h"], trim=[f["ss"], f["to"]], note=f["note"],
                bytes=(out.stat().st_size if not dry else None))


def build_pair(p: dict, dry: bool) -> dict:
    from PIL import Image
    files = {}
    for side in ("once", "sonra"):
        src = OUT / f"{p['src']}-{side}-480.webp"
        out = OUT / f"{p['slug']}-{side}-480.webp"
        if not dry:
            im = Image.open(src).convert("RGB")
            if p["rotate"]:
                im = im.rotate(p["rotate"], expand=True)
            im = im.crop(p["crop"])
            im.save(out, "WEBP", quality=84, method=6)
        files[side] = out.name
        print(f"{src.name} -> {out.name} rotate={p['rotate']} crop={p['crop']}")
    w, h = p["crop"][2] - p["crop"][0], p["crop"][3] - p["crop"][1]
    return dict(kind="image", fam="cilt", id=p["id"], alt=p["alt"], split="v", yuz=True,
                once={"files": {"480": files["once"]}, "w": w, "h": h},
                sonra={"files": {"480": files["sonra"]}, "w": w, "h": h}, note=p["note"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    only = set(filter(None, a.only.split(",")))
    tmp = HERE / ".tmp"
    tmp.mkdir(exist_ok=True)
    log = json.loads(LOG.read_text()) if LOG.exists() else {}
    for v in VIDEOS:
        if not only or v["slug"] in only:
            log[v["slug"]] = build_video(v, a.dry, tmp)
    for f in FILMS:
        if not only or f["slug"] in only:
            log[f["slug"]] = build_film(f, a.dry)
    for p in PAIRS:
        if not only or p["slug"] in only:
            log[p["slug"]] = build_pair(p, a.dry)
    if a.dry:
        return
    LOG.write_text(json.dumps(log, ensure_ascii=False, indent=1) + "\n")
    idx = json.loads(INDEX.read_text())
    for slug, rec in log.items():
        if rec["kind"] == "film":
            continue
        idx[slug] = {k: rec[k] for k in rec if k not in ("note", "trim")}
        if rec["kind"] == "video":
            idx[slug].update(w=rec.get("w"), h=rec.get("h"), dur=rec.get("dur"), split=None, yuz=False)
    INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=1) + "\n")
    for p in tmp.glob("*.trf"):
        p.unlink()
    tmp.rmdir()
    print("ok:", len(log), "kayıt")


if __name__ == "__main__":
    main()
