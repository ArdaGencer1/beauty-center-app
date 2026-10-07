#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ATELIER · FAZ L -- build the prototype Artifact with the laser family.

Input is the *published* Artifact's index.html (saved under prototypes/claude-artifact/...), never the old v3
snapshot: the published page carries work done inside Claude (the nail family) that the snapshot lacks.

What it does, and nothing else:
  * replaces <section data-view="lazer"> with six laser views rendered by render.page_html() -- the very
    markup the live patch uses (hub -> "lazer", fiyat -> "lazer-fiyat", erkek, yuz, hassas, bolgesel);
  * inlines src/lazer.css and src/lazer.js (fonts.css is not needed: the page loads Cormorant itself);
  * wires the views into the prototype: VIEWS, initView (ATLZ.mount with host hooks), the bottom bar, the
    "Lazer" menu group, the prototype panel and the tier switch;
  * drops the old laser planner path (region chips, sample hours) for laser views.
Every other <section data-view> must come out byte-identical; the build stops if one does not.

  python3 a3_build.py --base prototypes/.../artifact-1791383911.html --out DIR
Prints the media files the page references that are not yet published (pass them as `files` on publish).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))
import render as R  # noqa: E402

MEDIA = "m/ig/"
VIEW = {"hub": "lazer", "fiyat": "lazer-fiyat", "erkek": "lazer-erkek", "yuz": "lazer-yuz",
        "hassas": "lazer-hassas", "bolge": "lazer-bolgesel"}
NAV_SLUG = {"lazer-epilasyon-fiyatlari-ankara": "lazer-fiyat", "erkek-lazer-epilasyon": "lazer-erkek",
            "bolgesel-lazer": "lazer-bolgesel", "yuz-lazer": "lazer-yuz", "hassas-cilt-lazer": "lazer-hassas"}
# Prototype headings.  The live patch keeps each page's real H1 verbatim; these only stand in for it here.
H1 = {"hub": "Ankara Lazer Epilasyon: Konutkent ve Çayyolu Yakınında Bölge Planı",
      "fiyat": "Ankara Lazer Epilasyon Fiyatları: Bölge Bölge Kişiye Özel",
      "erkek": "Erkek Lazer Epilasyon: Sakal Hattından Sırta",
      "yuz": "Yüz Lazer Epilasyon: Dudak Üstü, Çene, Gıdı",
      "hassas": "Hassas Ciltte Lazer Epilasyon: Soğutmalı Başlık",
      "bolge": "Bölgesel Lazer Epilasyon: Yalnızca İhtiyacınız Olan Bölge"}
MARK = "<!-- ATELIER FAZ L · lazer ailesi (a3_build.py) -->"


def sections(html: str) -> dict:
    out = {}
    for m in re.finditer(r'<section data-view="([a-z-]+)"', html):
        end = html.index("</section>", m.start())
        out[m.group(1)] = html[m.start():end + len("</section>")]
    return out


def rep(s: str, old: str, new: str, n: int = 1) -> str:
    c = s.count(old)
    if c != n:
        raise SystemExit(f"a3_build: expected {n}x, found {c}x: {old[:90]!r}")
    return s.replace(old, new)


def laser_views() -> str:
    link = lambda k: "#" + VIEW[k]  # noqa: E731  -- hash routing; the page's hashchange handler calls go()
    out = [MARK]
    for k, v in VIEW.items():
        body = R.page_html(k, MEDIA, H1[k], link)
        out.append(f'<section data-view="{v}" hidden>\n{body}\n</section>')
    return "\n".join(out)


def laser_data() -> str:
    pages = {k: R.page_data(k, MEDIA, False) for k in VIEW}
    keys = set.intersection(*(set(d) for d in pages.values()))
    shared = {k: pages["hub"][k] for k in sorted(keys) if all(d[k] == pages["hub"][k] for d in pages.values())}
    own = {p: {k: v for k, v in d.items() if k not in shared} for p, d in pages.items()}
    js = json.dumps({"shared": shared, "own": own}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return ("<script>window.ATLZ_NOAUTO=true;(function(){var D=" + js +
            ",o={};for(var k in D.own){var x={},s;for(s in D.shared)x[s]=D.shared[s];for(s in D.own[k])x[s]=D.own[k][s];o[k]=x;}"
            "window.ATLZ_DATA=o;})();</script>")


# host wiring inside the prototype's own script -------------------------------------------------------------
LZ_HOST = r'''
/* ---------- ATELIER FAZ L: lazer ailesi (render.py + src/lazer.js, canlıyla aynı kod) ---------- */
var LZV={"lazer":"hub","lazer-fiyat":"fiyat","lazer-erkek":"erkek","lazer-yuz":"yuz","lazer-hassas":"hassas","lazer-bolgesel":"bolge"};
function lzRoot(v){ return $("main > [data-view='"+v+"'] .lz"); }
function lzMount(v){ var r=lzRoot(v); if(!r||!window.ATLZ) return null;
  return window.ATLZ.mount(r,{data:window.ATLZ_DATA[LZV[v]],noFetch:true,tier:function(){ return S.tier; },code:visitCode,hideProto:hideProto,menu:openMenu,
    bar:function(t){ if(S.view===v) $("#barLbl").textContent=t; }}); }
'''


def wire(html: str) -> str:
    # views
    html = rep(html, 'var VIEWS=["salon","kas","tirnak","kirpik","lifting","pmu","cilt","lazer",',
               'var VIEWS=["salon","kas","tirnak","kirpik","lifting","pmu","cilt","lazer","lazer-fiyat","lazer-erkek","lazer-yuz","lazer-hassas","lazer-bolgesel",')
    html = rep(html, '  if(v==="lazer"){ initRegions(); initPairs("galLazer","lazer"); }',
               '  if(LZV[v]) lzMount(v);')
    html = rep(html, '/* ---------- views ---------- */', LZ_HOST + '\n/* ---------- views ---------- */')
    # bottom bar: label from the laser page, tap opens its invitation (day + time band; no sample hours)
    html = rep(html, '''  else if(v==="lazer") l.textContent=LZ.sel.length?LZ.sel.length+" bölge · saatimi seç":"Bölgelerim · saatimi seç";''',
               '''  else if(LZV[v]){ var lr=lzRoot(v); l.textContent=(lr&&window.ATLZ?window.ATLZ.barText(lr):"Bölgelerim · günümü seç"); }''')
    html = rep(html, '''  var bk=v==="tirnak"?tzKey():v;''',
               '''  var bk=v==="tirnak"?tzKey():(LZV[v]?({hub:"lazer",fiyat:"lzfiyat",erkek:"lzerkek",yuz:"lzyuz",hassas:"lzhassas",bolge:"lzbolge"})[LZV[v]]:v);''')
    html = rep(html, '''$("#barCta").addEventListener("click",function(){ if(S.view==="tirnak"&&TZ.pg) return openPlanner(TZ.pg.fam,TZ.pg.opt||null);''',
               '''$("#barCta").addEventListener("click",function(){ if(LZV[S.view]&&window.ATLZ) return window.ATLZ.plan(lzRoot(S.view)); if(S.view==="tirnak"&&TZ.pg) return openPlanner(TZ.pg.fam,TZ.pg.opt||null);''')
    # any leftover [data-plan="lazer"] elsewhere opens the laser invitation, not the old sample-hours planner
    html = rep(html, '''    var pl=e.target.closest("[data-plan]"); if(pl){ openPlanner(pl.dataset.plan,pl.dataset.opt); }''',
               '''    var pl=e.target.closest("[data-plan]"); if(pl){ if(pl.dataset.plan==="lazer"&&window.ATLZ){ go("lazer"); window.ATLZ.plan(lzRoot("lazer")); } else openPlanner(pl.dataset.plan,pl.dataset.opt); }''')
    # tier switch in the panel reaches the laser views too
    html = rep(html, '''if(k==="tier"){ S.tierPick=v; setTier(v==="auto"?detectTier():v);''',
               '''if(k==="tier"){ S.tierPick=v; setTier(v==="auto"?detectTier():v); $$(".lz[data-lz-tier]").forEach(function(r){ r.setAttribute("data-lz-tier",S.tier); });''')
    # menu: the five laser pages become vitrines
    for slug, v in NAV_SLUG.items():
        html, n = re.subn(r'\["%s", "([^"]+)"\]' % re.escape(slug), lambda m, v=v, slug=slug: f'["{slug}", "{m.group(1)}", "{v}"]', html, count=1)
        if n != 1:
            raise SystemExit(f"a3_build: NAV entry {slug} not found")
    # prototype panel: a laser page picker next to the nail one
    html = rep(html, '''(function(){ var sel=$("#tzSel"); if(sel) sel.addEventListener("change",function(){ hideProto(); go(sel.value==="tirnak"?"tirnak":"tirnak/"+sel.value); }); })();''',
               '''(function(){ var sel=$("#tzSel"); if(sel) sel.addEventListener("change",function(){ hideProto(); go(sel.value==="tirnak"?"tirnak":"tirnak/"+sel.value); }); })();
(function(){ var sel=$("#lzSel"); if(sel) sel.addEventListener("change",function(){ hideProto(); go(sel.value); }); })();''')
    opts = "".join(f'<option value="{v}">{n}</option>' for v, n in
                   [("lazer", "Lazer epilasyon (merkez)"), ("lazer-fiyat", "Fiyatlar ve bölge menüsü"), ("lazer-erkek", "Erkek lazer"),
                    ("lazer-yuz", "Yüz lazer"), ("lazer-hassas", "Hassas cilt"), ("lazer-bolgesel", "Bölgesel lazer")])
    i = html.index('<div class="row"><span>Tırnak sayfası')
    html = html[:i] + (f'<div class="row"><span>Lazer sayfası · 6</span><select id="lzSel" class="tz-sel" aria-label="Lazer sayfası" '
                       f'data-track-label="at-proto-lazer">{opts}</select></div>\n  ') + html[i:]
    return html


def build(base: str) -> str:
    html = base
    before = sections(html)
    if "lazer" not in before or "lazer-fiyat" in before:
        raise SystemExit("a3_build: base must be a published page with the old single laser view")
    html = rep(html, before["lazer"], laser_views())
    # styles after the page's last head stylesheet; scripts before the page script
    css = (HERE / "src/lazer.css").read_text()
    html = rep(html, '<header class="nav">', '<style id="lz-css">\n' + css + '\n</style>\n<header class="nav">')
    js = (HERE / "src/lazer.js").read_text()
    html = rep(html, "<script>\n(function(){\n\"use strict\";", laser_data() + "\n<script>\n" + js + "\n</script>\n<script>\n(function(){\n\"use strict\";")
    html = wire(html)
    after = sections(html)
    for v, s in before.items():
        if v != "lazer" and after.get(v) != s:
            raise SystemExit(f"a3_build: section {v!r} changed -- refusing")
    missing = [v for v in VIEW.values() if v not in after]
    if missing:
        raise SystemExit(f"a3_build: views missing: {missing}")
    return html


def media_refs(html: str) -> list[str]:
    return sorted(set(re.findall(r'm/ig/([A-Za-z0-9_.-]+\.(?:webp|mp4|avif|png|jpg))', html)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="published Artifact index.html")
    ap.add_argument("--out", required=True, help="output directory (index.html is written there)")
    ap.add_argument("--published", help="file listing the published paths, one per line (default: media the base page references)")
    a = ap.parse_args()
    html = build(Path(a.base).read_text())
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(html)
    refs = media_refs(html)
    base_refs = media_refs(Path(a.base).read_text())
    pub = set(Path(a.published).read_text().split()) if a.published else {"m/ig/" + r for r in base_refs}
    new = [r for r in refs if "m/ig/" + r not in pub and r.startswith("lazer")]
    lost = [r for r in refs if not (REPO / "website/m/ig" / r).exists() and "m/ig/" + r not in pub]
    print(json.dumps({"bytes": len(html.encode()), "media_refs": len(refs), "upload": new, "unresolved": lost}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
