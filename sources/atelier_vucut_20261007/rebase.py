#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Yayındaki Artifact sürümünden vücut + mobil katmanı eklemelerini geri çıkarıp yeni taban yazar.

Başka oturumlar (tırnak, kaş, lazer, cilt...) aynı Artifact'i sık yayınlıyor; vücut sayfaları bir tabana yama
olarak derlendiği için her yayından önce taban, yayındaki sürüme taşınır:

  1. Artifact'i oku (read, path=index.html) -> YAYINDAKI.html
  2. python3 sources/atelier_vucut_20261007/rebase.py YAYINDAKI.html --rev <yayındaki vücut kodunu üreten commit> \
         --out prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/artifact-taban-<sürüm-id>.html
  3. build.py içindeki BASE'i yeni tabana çevir, derle, test et, yayınla.

--rev, yayındaki vücut kodunu üreten build.py/src sürümüdür (AI_CONTEXT.json → artifact.vucut_build_rev).
Betik o revizyonun build.py'sini geçici bir klasöre açar; eklediği CSS, JS, yamalar, VIEWS kimlikleri ve
loading="lazy" işaretleri tam bir kez bulunmazsa durur. Son adımda yeni taban o revizyonla yeniden derlenir ve
YAYINDAKI.html ile bayt bayt karşılaştırılır; eşit değilse taban yazılmaz.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1].parent
PATHS = ["sources/atelier_vucut_20261007", "sources/atelier_lazer_20261007"]


def load_rev(rev: str, tmp: Path):
    tar = subprocess.run(["git", "-C", str(REPO), "archive", rev, *PATHS], check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(tmp)], input=tar, check=True)
    path = tmp / "sources" / "atelier_vucut_20261007" / "build.py"
    spec = importlib.util.spec_from_file_location("vb_rev", path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(tmp / "sources" / "atelier_lazer_20261007"))
    spec.loader.exec_module(mod)
    return mod


def strip(live: str, b) -> str:
    if "views_patch" not in dir(b):
        raise SystemExit("bu revizyon eski yama düzeninde (artifact-v7 ve öncesi); bu betik 17. sürüm ve sonrası içindir")
    t = live

    def rm(new: str, old: str, what: str) -> None:
        nonlocal t
        n = t.count(new)
        if n != 1:
            raise SystemExit(f"{what}: {n} kez bulundu (1 olmalı)")
        t = t.replace(new, old)

    src = b.HERE / "src"
    css = (src / "vucut.css").read_text(encoding="utf-8")
    if (src / "mobil.css").exists():
        css += (src / "mobil.css").read_text(encoding="utf-8")
    js = (src / "vucut.js").read_text(encoding="utf-8").replace("/*__VB_SVG__*/", b.svg_js())
    rm(css + b.CSS_ANCHOR, b.CSS_ANCHOR, "CSS")
    rm(js + "\n" + b.JS_ANCHOR, b.JS_ANCHOR, "JS")
    for old, new in list(b.PATCHES) + list(getattr(b, "MOBIL_PATCHES", [])):
        rm(new, old, "yama " + old[:60])
    ids = "," + ",".join(f'"{v}"' for v in b.VIEW_IDS) + "];"
    rm(ids, "];", "VIEWS")
    if "lazy_hidden" in dir(b):
        s, e = t.index("<main>"), t.index("</main>")
        t = t[:s] + t[s:e].replace('<img loading="lazy" ', "<img ") + t[e:]
    return t


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("live", type=Path)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    live = a.live.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as d:
        b = load_rev(a.rev, Path(d))
        base = strip(live, b)
        probe = Path(d) / "taban.html"
        probe.write_text(base, encoding="utf-8")
        b.BASE = probe
        again = b.build()
    if again != live:
        raise SystemExit("doğrulama başarısız: yeni taban + " + a.rev + " derlemesi yayındakiyle aynı değil; taban yazılmadı")
    a.out.write_text(base, encoding="utf-8")
    print(f"  taban: {a.out} ({len(base):,} karakter); {a.rev} ile derleme yayındakiyle bayt bayt aynı")
    return 0


if __name__ == "__main__":
    sys.exit(main())
