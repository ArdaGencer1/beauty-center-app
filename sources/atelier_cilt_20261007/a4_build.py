#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CİLT ATLASI · Artifact v4 derleyicisi.

Girdi:  prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/artifact-v3.html (yayındaki sürümle aynı) +
        src/cilt.css + src/cilt_pages.js + src/cilt.js
Çıktı:  website/index.html (yerel önizleme, medya website/m/) ve artifact-v4.html (depo anlık görüntüsü).

Her yama tam olarak bir kez eşleşmek zorundadır; eşleşmezse derleme durur.  Taban hep v3 olduğu için betik
istenildiği kadar yeniden çalıştırılabilir.

Kullanım:  python3 sources/atelier_cilt_20261007/a4_build.py [--check]
           python3 sources/atelier_cilt_20261007/a4_build.py --refresh <yayındaki-sürüm.html>   (cilt zaten yayındaysa)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ART = REPO / "prototypes" / "claude-artifact" / "WmsLiPPTLdnrjSrdYSXcLM"
BASE = ART / "artifact-v5.html"  # yayındaki sürüm 1791385473-59b6 (v3 + vücut + lazer ailesi + tırnak kartela, başka oturumlar)
OUT_ART = ART / "artifact-v7.html"
OUT_WEB = REPO / "website" / "index.html"
MEDIA = REPO / "website"

HUB_HERO = (
    '<div class="half-stage" id="halfStage" style="view-transition-name:media-cilt">'
    '<video class="auto-vid" muted playsinline loop preload="none" poster="m/ig/cilt-led-dongu-poster.webp" '
    'data-src="m/ig/cilt-led-dongu.mp4" aria-label="LED ışık terapisi, salonumuzda çekildi"></video>'
    '<span class="ca-film-tag"><i></i>Salonumuzda çekildi</span></div>'
)

ATLAS = (
    '\n  <div class="sec gutter" style="padding-top:0"><div class="sec-head"><span class="eyebrow">Cilt Atlası · 24 sayfa</span>'
    '<h2>Derdinizi seçin, <em>hikâyesini</em> okuyun.</h2><p>Her bakımın kendi sayfası: nasıl geçtiği, salonumuzda çekilmiş '
    'videoları ve fiyatı.</p></div><div class="ca-atlas" id="ciltAtlas"></div></div>'
    '\n  <div class="sec gutter" id="ciltHubStory"></div>\n'
)

STORIES_CILT = (
    ' cilt:[{t:"Önce / Sonra",th:"m/ig/yuz-cift-1-sonra-480.webp",fr:[{img:"m/ig/yuz-cift-1-once-480.webp",cap:"Önce"},'
    '{img:"m/ig/yuz-cift-1-sonra-480.webp",cap:"Sonra · yüz bakımı"},{img:"m/ig/akne-cift-1-once-800.webp",cap:"Önce"},'
    '{img:"m/ig/akne-cift-1-sonra-800.webp",cap:"Sonra · akne bakımı"}]},\n'
    '      {t:"Seans",th:"m/ig/cilt-analiz-poster.webp",fr:[{video:"m/ig/cilt-analiz.mp4",poster:"m/ig/cilt-analiz-poster.webp",cap:"Önce bakarız"},'
    '{video:"m/ig/cilt-kopuk.mp4",poster:"m/ig/cilt-kopuk-poster.webp",cap:"Arındırma"},'
    '{video:"m/ig/cilt-masaj.mp4",poster:"m/ig/cilt-masaj-poster.webp",cap:"Masaj"},'
    '{video:"m/ig/cilt-led-dongu.mp4",poster:"m/ig/cilt-led-dongu-poster.webp",cap:"LED ile kapanış"}]},\n'
    '      {t:"Akne",th:"m/ig/cilt-darsonval-poster.webp",fr:[{video:"m/ig/cilt-darsonval.mp4",poster:"m/ig/cilt-darsonval-poster.webp",cap:"Darsonval"},'
    '{img:"m/ig/akne-cift-2-once-800.webp",cap:"Önce"},{img:"m/ig/akne-cift-2-sonra-800.webp",cap:"Sonra"}]},\n'
    '      {t:"Saten",th:"m/ig/cilt-saten-poster.webp",fr:[{video:"m/ig/cilt-saten.mp4",poster:"m/ig/cilt-saten-poster.webp",cap:"Saten yüz germe"},'
    '{video:"m/ig/cilt-saten-yakin.mp4",poster:"m/ig/cilt-saten-yakin-poster.webp",cap:"Göz çevresi"}]},\n'
    '      {t:"Yorumlar",th:"m/monogram.png",fr:"rv:cilt"},\n'
    '      {t:"Fiyat",th:"m/ig/cilt-led-dongu-poster.webp",fr:"price:cilt"}],'
)

QUIZ_LINK = ("(CA_OPT2SLUG[o.id]?'<button class=\"btn-line\" style=\"justify-content:center;margin-top:8px\" data-go=\"cilt/'"
             "+CA_OPT2SLUG[o.id]+'\" data-track-label=\"at-cilt-test-sayfa\">'+o.n+' sayfası →</button>':'')+")

PROTO_NOTE = (" <b>Cilt Atlası:</b> 24 cilt alt sayfası prototipte açılır (<code>#cilt/…</code>); yalnızca salonun gerçek "
              "medyası. Personel çekimi bekleyen sayfalar: leke, hollywood, paris, dermabrazyon, hydra elite, hassas cilt, "
              "antioksidan, dudak, kararma, sırt, koltuk altı, dirsek, anti aging, göz çevresi. Yeni 5 menü kalemi (ton, saten, "
              "dudak, sırt, koltuk altı) ile alan/bölge fiyatları planın CRM matrisinden alındı; canlıya almadan önce CRM'den "
              "yeniden doğrulanmalı.")


def sub1(html: str, old: str, new: str, label: str) -> str:
    n = html.count(old)
    if n != 1:
        sys.exit(f"yama '{label}': {n} eşleşme (1 bekleniyordu)")
    return html.replace(old, new)


def build() -> str:
    h = BASE.read_text(encoding="utf-8")
    css = (HERE / "src" / "cilt.css").read_text(encoding="utf-8")
    js = (HERE / "src" / "cilt_pages.js").read_text(encoding="utf-8") + (HERE / "src" / "cilt.js").read_text(encoding="utf-8")

    # Yayın servisi sayfayı kendi belge iskeletiyle sarar; geri okunan taban bu iskeleti içerir.  Çift iskelet
    # olmasın diye sökülür (ilk satır <!doctype…<body>, son satır </body></html>).
    if h.startswith("<!doctype html><html><head><meta charset=utf8>"):
        first, rest = h.split("\n", 1)
        if not first.rstrip().endswith("<body>"):
            sys.exit("iskelet: ilk satır beklenen biçimde değil")
        h = rest.rstrip("\n")
        if not h.endswith("</body></html>"):
            sys.exit("iskelet: son satır beklenen biçimde değil")
        h = h[: -len("</body></html>")].rstrip("\n") + "\n"
    if "<!doctype" in h.lower():
        sys.exit("iskelet: ikinci <!doctype> kaldı")
    m0 = re.match(r"<title>[^<]*</title>\n", h)
    if not m0:
        sys.exit("yama 'css': sayfa <title> ile başlamıyor")
    h = h[: m0.end()] + f'<style id="cilt-atlas">\n{css}</style>\n' + h[m0.end():]

    # --- hub: kahraman (çıkarılan yarım yüz karesi yerine gerçek LED döngüsü)
    m = re.search(r'<div class="half-stage" id="halfStage".*?</button>\s*</div>', h, re.S)
    if not m or h.count('id="halfStage"') != 1:
        sys.exit("yama 'hub-hero': bulunamadı")
    h = h[:m.start()] + HUB_HERO + h[m.end():]
    h = sub1(h, '<p class="hero-note">Aynı yüzün iki yarısı: solda bakımdan önce, sağda sonra. Fotoğraf salonumuzda çekildi.</p>',
             '<p class="hero-note">LED ışık terapisi, salonumuzda çekildi. Aşağıda 24 sayfalık Cilt Atlası ve gerçek önce/sonra kareleri.</p>',
             "hub-note")

    # --- hub sarmalayıcı + alt sayfa kabı
    start = h.index('<section data-view="cilt" hidden>')
    end = h.index("</section>", start)
    h = h[:start] + '<section data-view="cilt" hidden>\n<div id="ciltHub">' + h[start + len('<section data-view="cilt" hidden>'):end] + \
        '</div>\n<div id="ciltPage" hidden></div>\n' + h[end:]

    # --- hub: atlas + seans hikâyesi (testten hemen sonra)
    h = sub1(h, '<div id="quizBody"></div>\n    </div>\n  </div>\n', '<div id="quizBody"></div>\n    </div>\n  </div>\n' + ATLAS, "atlas")

    # --- hub: LED bandı LED kubbe klibine geçer (kahraman artık LED döngüsü)
    h = sub1(h, 'poster="m/ig/cilt-led-poster.webp" data-src="m/ig/cilt-led.mp4" aria-label="LED ışık terapisi, salonumuzda çekildi"',
             'poster="m/ig/cilt-kubbe-poster.webp" data-src="m/ig/cilt-kubbe.mp4" aria-label="LED kubbe altında cilt bakımı, salonumuzda çekildi"',
             "led-band")
    h = sub1(h, '<p>Yeşil, kırmızı, mor ve mavi: cilt bakımlarımızda kullandığımız LED ışık terapisi, salonumuzda çekildi.</p>\n        <div class="golden-actions"><button class="btn-line" data-story="cilt" data-story-i="1">',
             '<p>Bakımlarımızın son adımı: LED kubbe altında birkaç dakika. Salonumuzda, elde çekildi.</p>\n        <div class="golden-actions"><button class="btn-line" data-story="cilt" data-story-i="1">',
             "led-band-text")
    h = sub1(h, "<summary>Paket var mı?</summary><p>Ana bakımların 5 seanslık paketleri var; fiyatları ön görüşmede iletiyoruz.</p>",
             "<summary>Paket var mı?</summary><p>Ana bakımların 5 seanslık paketleri var; paket fiyatı tek seans fiyatının 4,5 katıdır. "
             "Hepsini <a href=\"#cilt/cilt-bakimi-fiyatlari\" data-go=\"cilt/cilt-bakimi-fiyatlari\">fiyatlar sayfasında</a> görebilirsiniz.</p>",
             "faq-paket")

    # --- veri: çıkarılan kareler (plan 10-07, §1a) galeriden, hikâyelerden ve mozaikten çıkar
    h = sub1(h, ' cilt:[["akne-cift-1","Akne bakımı","pair"],["akne-cift-2","Akne bakımı","pair"],["cilt-cift-1","Cilt bakımı","pair480"],["cilt-cift-3","Leke bakımı","pair480"],["cilt-cift-4","Nem ve parlaklık","pair480"],["cilt-cift-5","Kızarıklık bakımı","pair480"],["cilt-yarim-2","Yarım yüz","one"],["cilt-islem","Maske uygulaması","one"]],',
             ' cilt:[["yuz-cift-1","Yüz bakımı","pair480"],["akne-cift-1","Akne bakımı","pair"],["akne-cift-2","Akne bakımı","pair"]],', "gal")
    m = re.search(r' cilt:\[\{t:"Yarım yüz".*?fr:"price:cilt"\}\],', h, re.S)
    if not m:
        sys.exit("yama 'stories': bulunamadı")
    h = h[:m.start()] + STORIES_CILT + h[m.end():]
    h = sub1(h, '["cilt-yarim-1","Cilt bakımı, önce ve sonra"]', '["akne-cift-1-sonra","Akne bakımı sonrası"]', "mosaic")

    # --- yönlendirme: tabanın genel "görünüm/parametre" yolu kullanılır (go → S.route, boot, hashchange hazır)
    h = sub1(h, 'if(v==="tirnak") tzShow(prm||"tirnak");',
             'if(v==="tirnak") tzShow(prm||"tirnak"); if(v==="cilt") ciltRoute(CP[prm]?prm:null);', "go-cilt")
    h = sub1(h, '$$("[data-go]",sec).forEach(function(b){ lbl(b,"at-"+v+"-git-"+b.dataset.go); });',
             '$$("[data-go]",sec).forEach(function(b){ lbl(b,("at-"+v+"-git-"+b.dataset.go.replace(/[^a-z0-9_-]/g,"-")).slice(0,48)); });',
             "autolabel")
    h = sub1(h, 'var cur=S.view==="tirnak"?tzRoute():S.view;', 'var cur=S.view==="tirnak"?tzRoute():(S.view==="cilt"?caRoute():S.view);', "menu")
    h = sub1(h, 'if(v==="cilt"){ initHalf(); initQuiz();', 'if(v==="cilt"){ initHalf(); initQuiz(); caInitHub();', "init")
    h = sub1(h, "'<button class=\"q-back\" data-qagain", QUIZ_LINK + "'<button class=\"q-back\" data-qagain", "quiz-link")
    h = sub1(h, "yeniden doğrulandı.", "yeniden doğrulandı." + PROTO_NOTE, "proto-note")

    h = put_mobile(h)

    # --- motor (IIFE içinde, boot'tan hemen önce: $, S, PLANS, NAV, REVIEWS, card, scrollers erişilebilir)
    h = sub1(h, "\nboot();\n})();", "\n" + js + "\nboot();\n})();", "engine")
    return h


JS_START = "/* ---------- CİLT ATLASI · içerik (24 alt sayfa) ----------"
JS_END = "/* ---------- /CİLT ATLASI ---------- */"


def strip_wrapper(h: str) -> str:
    """Yayın servisinin eklediği <!doctype…<body> … </body></html> iskeletini (bir ya da daha fazla kat) söker."""
    w = "<!doctype html><html><head><meta charset=utf8>"
    while h.startswith(w):
        first, h = h.split("\n", 1)
        if not first.rstrip().endswith("<body>"):
            sys.exit("iskelet: ilk satır beklenen biçimde değil")
        h = h.rstrip("\n")
        if not h.endswith("</body></html>"):
            sys.exit("iskelet: son satır beklenen biçimde değil")
        h = h[: -len("</body></html>")].rstrip("\n") + "\n"
    if "<!doctype" in h.lower():
        sys.exit("iskelet: içeride <!doctype> kaldı")
    return h


def put_mobile(h: str) -> str:
    """Ortak mobil düzen bloğu (<style id="mobil-duzen">): yoksa cilt stilinin hemen ardına eklenir, varsa yenilenir.
    Sayfanın tüm stillerinden sonra gelmesi için </style> zincirinin sonuna değil, ilk <script>'ten önceye konur."""
    css = (HERE / "src" / "mobil.css").read_text(encoding="utf-8")
    o = '<style id="mobil-duzen">\n'
    if o in h:
        i = h.index(o) + len(o)
        j = h.index("</style>", i)
        return h[:i] + css + h[j:]
    k = h.index("<script")
    return h[:k] + o + css + "</style>\n" + h[k:]


def refresh(base: Path) -> str:
    """Cilt Atlası zaten yayında: yayındaki sürümü al, yalnız cilt stilini ve cilt kod bloğunu kaynaktan yenile."""
    h = strip_wrapper(base.read_text(encoding="utf-8"))
    css = (HERE / "src" / "cilt.css").read_text(encoding="utf-8")
    js = (HERE / "src" / "cilt_pages.js").read_text(encoding="utf-8") + (HERE / "src" / "cilt.js").read_text(encoding="utf-8")
    o = '<style id="cilt-atlas">\n'
    i = h.index(o) + len(o)
    j = h.index("</style>", i)
    h = h[:i] + css + h[j:]
    h = put_mobile(h)
    if h.count(JS_START) != 1:
        sys.exit("yenileme: cilt kod bloğu başlangıcı 1 kez bulunmalı")
    i = h.index(JS_START)
    if JS_END in h:
        j = h.index(JS_END) + len(JS_END) + 1
    else:  # ilk yayın (sürüm 12) bitiş işaretsizdi: blok hubStory satırıyla biter
        m = re.compile(r"^function hubStory\(\)\{.*\n", re.M).search(h, i)
        if not m:
            sys.exit("yenileme: cilt kod bloğunun sonu bulunamadı")
        j = m.end()
    return h[:i] + js + h[j:]


def check(h: str) -> int:
    """Kırık medya referansı ve dışlanan kare kontrolü."""
    refs = set(re.findall(r'm/(?:ig/)?[A-Za-z0-9_./-]+\.(?:webp|mp4|png|jpg)', h))
    # JS içinde parça parça kurulan yollar: CM ve GAL kayıtlarından türet
    for slug, s in re.findall(r'pair:"([a-z0-9-]+)",s:(\d+)', h):
        refs |= {f"m/ig/{slug}-once-{s}.webp", f"m/ig/{slug}-sonra-{s}.webp"}
    for v in re.findall(r'\{img:"([a-z0-9-]+)"', h):
        refs |= {f"m/ig/{v}-480.webp", f"m/ig/{v}-720.webp"}
    for v in re.findall(r'\{v:"([a-z0-9-]+)"', h):
        refs |= {f"m/ig/{v}.mp4", f"m/ig/{v}-poster.webp"}
    extra = {l.strip() for l in (HERE / "data" / "artifact_published_extra.txt").read_text().splitlines() if l.strip() and not l.startswith("#")}
    missing = sorted(r for r in refs if not (MEDIA / r).exists() and r not in extra and "/f\"+" not in r)
    banned = [b for b in ("cilt-yarim-1", "cilt-yarim-2", "cilt-cift-2", "cilt-cift-3", "cilt-cift-4", "cilt-cift-5", "cilt-islem", "cilt-video-2")
              if b in h]
    print(f"medya referansı: {len(refs)}  eksik: {len(missing)}  dışlanan kare: {len(banned)}")
    for r in missing:
        print("  EKSİK", r)
    for b in banned:
        print("  DIŞLANAN", b)
    return 1 if (missing or banned) else 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="yalnızca derle ve denetle, dosya yazma")
    ap.add_argument("--refresh", metavar="YAYINDAKI.html", help="Cilt Atlası'nı içeren yayındaki sürümde yalnız cilt bloklarını yenile")
    a = ap.parse_args()
    h = refresh(Path(a.refresh)) if a.refresh else build()
    rc = check(h)
    if a.check:
        sys.exit(rc)
    OUT_WEB.write_text(h, encoding="utf-8")
    OUT_ART.write_text(h, encoding="utf-8")
    print(f"yazıldı: {OUT_WEB.relative_to(REPO)} ve {OUT_ART.relative_to(REPO)} ({len(h.encode()):,} bayt)")
    sys.exit(rc)


if __name__ == "__main__":
    main()
