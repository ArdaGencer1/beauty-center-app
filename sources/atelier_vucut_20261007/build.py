#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ATELİER · Vücut ailesi -- yayındaki Artifact'e 9 vücut sayfasını ekler; kaş sayfasındaki dışlanmış fotoğrafı çıkarır (Artifact 7. sürüm).

Girdi : prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/artifact-v6-tirnak-taban.html
        (yayındaki 6. sürüm 1791383614-b96f'den vücut eklemeleri çıkarılmış hâli: v3 + başka bir oturumun 22 tırnak
        sayfası ve T13 bakım randevusu. artifact-v4-tirnak.html (1791382406-9153) ile farkı yalnızca o oturumun
        tırnak değişiklikleridir; KAS_PATCHES olmadan derlenen çıktı 1791383614-b96f ile birebir aynıdır.)
Çıktı : website/index.html                   açılabilir site (tam belge)
        prototypes/.../artifact-v7.html      yayınlanan 7. sürümün depodaki anlık görüntüsü (v5 = kaş düzeltmesinden önceki kendi yayınımız)
        --publish DIR                        Artifact'e yüklenecek gövde (yayın iskeleti çıkarılmış)

Yaptıkları:
  * src/vucut.css stil bloğunun sonuna, src/vucut.js boot bölümünden önce IIFE içine eklenir;
  * vücut haritası (ön/arka) ve iki temsilî çizim, lazer ailesinin kadın silüetinden (render.SHAPES) üretilir;
  * küçük yamalar: NAV "Vücut" grubu vitrinlere bağlanır, VIEWS, prototip paneli, salon kartı, canlı şerit
    etiketi, hikâyede `fit`, boot'ta buildVucut(), initView'da initVucut();
  * her yama tam bir kez eşleşmek zorundadır; m/ig referanslarının hepsi diskte olmalıdır (--check).

  python3 sources/atelier_vucut_20261007/build.py [--check] [--publish DIR]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SNAP = REPO / "prototypes" / "claude-artifact" / "WmsLiPPTLdnrjSrdYSXcLM"
BASE = SNAP / "artifact-v6-tirnak-taban.html"
SITE = REPO / "website"
sys.path.insert(0, str(REPO / "sources" / "atelier_lazer_20261007"))
import render as LZ  # noqa: E402  (yalnızca SHAPES / HAIR / smooth / mirror kullanılır)

SH = LZ.SHAPES["kadin"]
REG_NAME = {"kol": "Kol arkası", "gobek": "Göbek", "bel": "Bel ve yanlar", "popo": "Popo", "bacak": "Bacak ve basen"}
# (şekil, bölge, iki taraflı mı); bölge None = yalnızca silüet
# Bölgeler sırayla çizilir; kenarları örtüşen göbek ve popo en sonda durur ki dokunuş bacağa değil onlara gitsin.
PARTS = {
    "on": [("neck", None, False), ("chest", None, False), ("groin", None, False), ("foot", None, True),
           ("farm", None, True), ("hand", None, True), ("thigh", "bacak", True), ("shin", "bacak", True),
           ("uarm", "kol", True), ("belly", "gobek", False)],
    "arka": [("neck", None, False), ("upback", None, False), ("shoulder", None, True), ("foot", None, True),
             ("farm", None, True), ("hand", None, True), ("thigh", "bacak", True), ("shin", "bacak", True),
             ("uarm", "kol", True), ("lowback", "bel", False), ("butt", "popo", True)],
}


def head(side: str, cls: str) -> list[str]:
    cx, cy, rx, ry = SH["head"]
    hair = LZ.HAIR["kadin"]
    out = [f'<ellipse class="{cls}" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/>', f'<path class="{cls}" d="{hair[side]}"/>']
    if hair["bun"]:
        bx, by, br = hair["bun"]
        out.append(f'<circle class="{cls}" cx="{bx}" cy="{by}" r="{br}"/>')
    return out


def map_svg(side: str) -> str:
    base, hits = head(side, "vb-shape"), []
    for name, part, both in PARTS[side]:
        for pts in ([SH[name], LZ.mirror(SH[name])] if both else [SH[name]]):
            d = LZ.smooth(pts)
            if part is None:
                base.append(f'<path class="vb-shape" d="{d}"/>')
            else:
                hits.append(f'<path class="vb-part" data-part="{part}" d="{d}" tabindex="0" role="button" aria-pressed="false" '
                            f'aria-label="{REG_NAME[part]}" data-track-label="at-vucut-harita-bolge"/>')
    label = "ön" if side == "on" else "arka"
    return (f'<svg viewBox="30 0 180 500" role="group" aria-label="Vücut haritası, {label} görünüm">'
            f'<g>{"".join(base)}</g><g>{"".join(hits)}</g></svg>')


def silhouette() -> str:
    parts = head("on", "")
    for name, _, both in PARTS["on"]:
        for pts in ([SH[name], LZ.mirror(SH[name])] if both else [SH[name]]):
            parts.append(f'<path d="{LZ.smooth(pts)}"/>')
    return '<g class="sil">' + "".join(p.replace(' class=""', "") for p in parts) + "</g>"


def art_pasif() -> str:
    pads = [(98, 178, 17, 26), (125, 178, 17, 26), (88, 262, 17, 32), (135, 262, 17, 32)]
    g = "".join(f'<rect class="pad" x="{x}" y="{y}" width="{w}" height="{h}" rx="4"/>' for x, y, w, h in pads)
    rings = "".join(f'<circle class="pulse d{1 + i % 3}" cx="{x + w / 2:.1f}" cy="{y + h / 2:.1f}" r="11"/>'
                    for i, (x, y, w, h) in enumerate(pads))
    return f'<svg viewBox="30 0 180 500" aria-hidden="true">{silhouette()}<g>{g}{rings}</g></svg>'


def art_catlak() -> str:
    lines = []
    for i in range(7):  # sol kalça ve bel yanı: ince, kısa kavisler; sağ taraf aynalanır
        x, y = 87 + (i % 2) * 3, 196 + i * 8
        for sx in (x, 240 - x):
            k = 1 if sx < 120 else -1
            lines.append(f'<path class="line" d="M{sx:.1f},{y} q{4 * k},{3} {7 * k},{9}"/>')
    return f'<svg viewBox="30 0 180 500" aria-hidden="true">{silhouette()}<g>{"".join(lines)}</g></svg>'


def svg_js() -> str:
    data = {"on": map_svg("on"), "arka": map_svg("arka"), "pasif": art_pasif(), "catlak": art_catlak()}
    return "var VB_SVG=" + json.dumps(data, ensure_ascii=False) + ";"


VUCUT_NAV_OLD = ('["Vücut", [["bolgesel-incelme", "Bölgesel incelme"], ["slim-tone", "Slim tone"], ["g5-masaji", "G5 masajı"], '
                 '["lenf-drenaj", "Lenf drenaj"], ["emler", "EM vücut bakımı"], ["heykeltras", "Heykeltraş"], ["pasif-jimnastik", "Pasif jimnastik"], '
                 '["catlak-protokolu-ince-ton", "Çatlak görünümü bakımı"], ["popo-bakimi", "Popo bakımı"]]]')
VUCUT_NAV_NEW = ('["Vücut", [["bolgesel-incelme", "Bölgesel incelme", "vucut"], ["slim-tone", "Slim tone", "slimtone"], ["g5-masaji", "G5 masajı", "g5"], '
                 '["lenf-drenaj", "Lenf drenaj", "lenf"], ["emler", "EM vücut bakımı", "em"], ["heykeltras", "Heykeltraş", "heykeltras"], '
                 '["pasif-jimnastik", "Pasif jimnastik", "pasif"], ["catlak-protokolu-ince-ton", "Çatlak görünümü bakımı", "catlak"], ["popo-bakimi", "Popo bakımı", "popo"]]]')
VIEW_IDS = ["vucut", "slimtone", "g5", "lenf", "em", "heykeltras", "pasif", "catlak", "popo"]

PATCHES = [
    # menü: dokuz vücut sayfası vitrine gider
    (VUCUT_NAV_OLD, VUCUT_NAV_NEW),
    ('"Vücut":"incelme selulit zayiflama"', '"Vücut":"incelme selulit zayiflama slimtone g5 lenf drenaj em heykeltras pasif jimnastik catlak popo"'),
    # hash yönlendirme
    ('var VIEWS=["salon","kas","tirnak","kirpik","lifting","pmu","cilt","lazer"];',
     'var VIEWS=["salon","kas","tirnak","kirpik","lifting","pmu","cilt","lazer",' + ",".join(f'"{v}"' for v in VIEW_IDS) + '];'),
    # prototip paneli
    ('<button data-v="lazer">Lazer</button></div></div>',
     '<button data-v="lazer">Lazer</button><button data-v="vucut">Vücut</button></div></div>'),
    ("Fiyatlar 7 Ekim 2026'da canlı CRM'den yeniden doğrulandı.</p>",
     "Fiyatlar 7 Ekim 2026'da canlı CRM'den yeniden doğrulandı. Vücut: bölgesel incelme, Slim Tone, G5 ve lenf drenaj gerçek salon medyasıyla; "
     "EM, heykeltraş ve popo temsilî görselle, pasif jimnastik ve çatlak temsilî çizimle (çekim bekliyor). Vücut fiyatları ön görüşmede.</p>"),
    # salon: Bölgesel İncelme kartı vitrine gider ve canlı oynar
    ('<button class="tile" data-plan="salon" data-opt="bolgesel"><img src="m/ig/bolgesel-cift-sonra-480.webp" alt="Bölgesel incelme sonrası" loading="lazy" width="480" height="1200"><span class="tile-txt"><b>Bölgesel İncelme</b><span>Kişiye özel paket</span></span></button>',
     '<a class="tile" href="#vucut" data-go="vucut"><video class="tile-vid" muted playsinline loop preload="none" poster="m/ig/vucut-g5-poster.webp" data-src="m/ig/vucut-g5.mp4" aria-label="G5 masajı, salonumuzda çekildi"></video><span class="tile-tag">Vitrin · canlı</span><span class="tile-txt"><b>Bölgesel İncelme</b><span>Slim Tone · G5 · Lenf drenaj</span></span></a>'),
    # canlı şerit etiketi
    ('cilt:"cilt bakımı",lazer:"lazer"}[fam]||fam)', 'cilt:"cilt bakımı",lazer:"lazer"}[fam]||(VUCUT_BY[fam]?"vücut bakımı":fam))'),
    # hikâye: kolaj kareleri kırpılmadan
    ('else if(f.img){ m=document.createElement("img"); m.src=f.img; m.alt=f.cap||""; }',
     'else if(f.img){ m=document.createElement("img"); m.src=f.img; m.alt=f.cap||""; if(f.fit) m.style.objectFit=f.fit; }'),
    # görünüm başlatma ve boot
    ('  if(v==="lazer"){ initRegions(); initPairs("galLazer","lazer"); }\n',
     '  if(v==="lazer"){ initRegions(); initPairs("galLazer","lazer"); }\n  if(VUCUT_BY[v]) initVucut(v);\n'),
    ("function boot(){\n  S.world=", "function boot(){\n  buildVucut();\n  S.world="),
]
# Kaş sayfası (sahip onayı 2026-10-07): manifestin "başka uzmana ait" diye dışladığı kas-cift-3 (IG 18516297502030856)
# Altın Oran Aynası'ndan ve galeriden çıkar. Aynanın yerine salonun kendi "altın oran · kına" sonucu gelir; kaşın yönü aynı
# (baş sağda, kuyruk solda), ölçü noktaları bu fotoğrafın 800x500 kapak kırpımına göre yeniden konumlandı.
KAS_PATCHES = [
    ('<img src="m/ig/kas-cift-3-sonra-800.webp" alt="Altın oran ölçü çizgileriyle kaş" width="800" height="500" loading="lazy">',
     '<img src="m/ig/kas-kina-sonra-800.webp" alt="Altın oran ölçü çizgileriyle kaş, salonumuzda yapıldı" width="800" height="534" loading="lazy">'),
    ('<path class="g-line" pathLength="1" d="M830 900 L602 209"/>', '<path class="g-line" pathLength="1" d="M830 900 L715 194"/>'),
    ('<path class="g-line" pathLength="1" d="M830 900 L300 50"/>', '<path class="g-line" pathLength="1" d="M830 900 L452 59"/>'),
    ('<path class="g-line" pathLength="1" d="M830 900 L-5 188"/>', '<path class="g-line" pathLength="1" d="M830 900 L-17 224"/>'),
    ('<circle class="g-ring d1" cx="615" cy="248" r="13"/><circle class="g-ring d2" cx="330" cy="98" r="13"/><circle class="g-ring d3" cx="42" cy="228" r="13"/>',
     '<circle class="g-ring d1" cx="722" cy="238" r="13"/><circle class="g-ring d2" cx="470" cy="100" r="13"/><circle class="g-ring d3" cx="18" cy="252" r="13"/>'),
    ('<circle class="g-dot d1" cx="615" cy="248" r="9"/><circle class="g-dot d2" cx="330" cy="98" r="9"/><circle class="g-dot d3" cx="42" cy="228" r="9"/>',
     '<circle class="g-dot d1" cx="722" cy="238" r="9"/><circle class="g-dot d2" cx="470" cy="100" r="9"/><circle class="g-dot d3" cx="18" cy="252" r="9"/>'),
    ('<text class="g-lbl d1" x="640" y="214" text-anchor="end">BAŞLANGIÇ</text>', '<text class="g-lbl d1" x="760" y="296" text-anchor="end">BAŞLANGIÇ</text>'),
    ('<text class="g-lbl d2" x="352" y="70">KAVİS</text>', '<text class="g-lbl d2" x="494" y="74">KAVİS</text>'),
    ('<text class="g-lbl d3" x="30" y="300">BİTİŞ</text>', '<text class="g-lbl d3" x="24" y="306">BİTİŞ</text>'),
    ('var KAS_PAIRS=[["kas-cift-2","Kaş alımı"],["kas-cift-3","Kaş tasarımı"],["kas-kina","Altın oran · kına"],["kas-laminasyon","Kaş laminasyonu"]];',
     'var KAS_PAIRS=[["kas-cift-2","Kaş alımı"],["kas-kina","Altın oran · kına"],["kas-laminasyon","Kaş laminasyonu"]];'),
]
CSS_ANCHOR = '</style>\n\n<div class="wrap" lang="tr">'
JS_ANCHOR = "/* ---------- boot ---------- */"


def build() -> str:
    html = BASE.read_text(encoding="utf-8")
    for old, new in PATCHES + KAS_PATCHES:
        n = html.count(old)
        if n != 1:
            raise SystemExit(f"yama {n} kez eşleşti (1 olmalı): {old[:80]}")
        html = html.replace(old, new)
    css = (HERE / "src" / "vucut.css").read_text(encoding="utf-8")
    js = (HERE / "src" / "vucut.js").read_text(encoding="utf-8").replace("/*__VB_SVG__*/", svg_js())
    for anchor in (CSS_ANCHOR, JS_ANCHOR):
        if html.count(anchor) != 1:
            raise SystemExit(f"çapa bulunamadı: {anchor}")
    html = html.replace(CSS_ANCHOR, css + CSS_ANCHOR)
    html = html.replace(JS_ANCHOR, js + "\n" + JS_ANCHOR)
    return html


def check(html: str) -> list[str]:
    refs = set(re.findall(r'm/(?:ig/)?[A-Za-z0-9_./-]+\.(?:webp|mp4|png)', html))
    # JS'te VM+"..." ile kurulan yollar
    refs |= {"m/ig/" + r for r in re.findall(r'VM\+"([a-z0-9-]+\.(?:webp|mp4))"', html)}
    return sorted(r for r in refs if "film/" not in r and not (SITE / r).is_file())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="yalnızca derle ve referansları denetle; yazma")
    ap.add_argument("--publish", type=Path, help="Artifact gövdesini (iskeletsiz) bu klasöre index.html olarak yaz")
    a = ap.parse_args()
    html = build()
    before = set(check(BASE.read_text(encoding="utf-8")))
    missing = [r for r in check(html) if r not in before]
    if missing:
        raise SystemExit("eksik medya: " + ", ".join(missing))
    print(f"  {len(html):,} bayt, yeni eksik medya 0"
          + (f" (tabandan kalan, depoda olmayan: {', '.join(sorted(before))})" if before else ""))
    if a.check:
        return 0
    (SITE / "index.html").write_text(html, encoding="utf-8")
    (SNAP / "artifact-v7.html").write_text(html, encoding="utf-8")
    print(f"  -> {SITE / 'index.html'}\n  -> {SNAP / 'artifact-v7.html'}")
    if a.publish:
        head_end = html.index("</head><body>\n") + len("</head><body>\n")
        body = html[head_end:].rstrip()
        if body.endswith("</body></html>"):
            body = body[: -len("</body></html>")].rstrip() + "\n"
        a.publish.mkdir(parents=True, exist_ok=True)
        (a.publish / "index.html").write_text(body, encoding="utf-8")
        print(f"  -> {a.publish / 'index.html'} (yayın gövdesi)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
