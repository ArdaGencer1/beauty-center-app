# -*- coding: utf-8 -*-
"""FAZ L in the prototype: the laser family as six views, from the same code the live patch ships.

render.py writes the markup (media under m/ig/), src/lazer.css + src/lazer.js are inlined verbatim, and the
prototype hosts each page through ATLZ.mount(root, host): its own action bar, menu, [W-] code and tier.
Ids inside the laser markup get a per-page suffix so six pages can share one document.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

LZ = Path(__file__).resolve().parents[1] / "atelier_lazer_20261007"
sys.path.insert(0, str(LZ))
import render  # noqa: E402

# view -> (render key, H1 used in the prototype; the live patch keeps each page's own H1)
VIEWS = {
    "lazer": ("hub", "Ankara Lazer Epilasyon: Konutkent ve Çayyolu Yakınında Bölge Planı"),
    "lazer-fiyat": ("fiyat", "Lazer Epilasyon Fiyatları Ankara: Bölge Bölge Kişiye Özel Plan"),
    "lazer-erkek": ("erkek", "Erkek Lazer Epilasyon Ankara: Sakal Üstünden Sırta"),
    "lazer-yuz": ("yuz", "Yüz Lazer Epilasyon: Dudak Üstü, Çene ve Gıdı"),
    "lazer-hassas": ("hassas", "Hassas Ciltte Lazer Epilasyon: Soğutmalı Başlık, Nazik Başlangıç"),
    "lazer-bolgesel": ("bolge", "Bölgesel Lazer Epilasyon: Yalnızca İhtiyacınız Olan Bölge"),
}
KEY2VIEW = {k: v for v, (k, _h) in VIEWS.items()}
KEY2VIEW["kamp"] = "lazer"

PROTO_CSS = """
/* ---------- v4 · FAZ L host: laser pages inside the prototype ---------- */
:root{--top-nav-offset:calc(var(--nav-h) + env(safe-area-inset-top,0px))}
section[data-view^="lazer"]{background:#0B0909}
section[data-view^="lazer"] .lz{padding-top:var(--top-nav-offset)}
section[data-view^="lazer"] .lz-visit{padding-bottom:calc(var(--bar-h) + 30px)}
html[data-page^="lazer"] footer.site{background:#0B0909;color:#9C8B84}
html[data-page^="lazer"] .bar{background:rgba(14,9,11,.7);border-color:rgba(255,211,234,.18)}
html[data-page^="lazer"] .bar .btn-round{background:rgba(26,19,22,.9);color:#F6EEE8;border-color:rgba(255,211,234,.3)}
"""

HOST_JS = r"""
/* ---------- v4 · FAZ L host ---------- */
var LZV={};
function lzRoot(v){ return $("main > [data-view='"+v+"'] .lz"); }
function lzMount(v){ var r=lzRoot(v); if(!r||!window.ATLZ) return null; if(r.__lz) return r.__lz;
  var key=r.getAttribute("data-lz-page");
  return window.ATLZ.mount(r,{data:window.ATLZ_DATA[key],tier:function(){ return S.tier; },noFetch:true,
    bar:function(t){ LZV[v]=t; if(S.view===v){ $("#barLbl").textContent=t; } },
    code:visitCode, menu:openMenu, hideProto:hideProto}); }
function lzPlan(v){ v=v&&lzRoot(v)?v:(S.view.indexOf("lazer")===0?S.view:"lazer"); if(S.view!==v) go(v); lzMount(v); var r=lzRoot(v); if(window.ATLZ&&r) window.ATLZ.plan(r); }
""" + "var LZ_VIEWS=" + json.dumps(list(VIEWS)) + r""";
LZ_VIEWS.forEach(function(v){ ROUTE_HOOK[v]=function(p){ lzMount(v);
  if(p){ var id={menu:"lz-menu",harita:"lz-harita",takvim:"lz-takvim",cihaz:"lz-cihaz",yorumlar:"lz-yorumlar"}[p]; var t=id&&$("#"+id+"--"+$("main > [data-view='"+v+"'] .lz").getAttribute("data-lz-page"));
    if(t) setTimeout(function(){ var top=t.getBoundingClientRect().top+scrollY-70; scrollTo({top:top,behavior:"instant"}); },60); } }; });
"""


def suffix_ids(html: str, key: str) -> str:
    """id="lz-x" -> id="lz-x--key" (and every in-page reference to it)."""
    ids = set(re.findall(r'id="(lz-[\w-]+)"', html))
    for i in sorted(ids, key=len, reverse=True):
        new = f"{i}--{key}"
        html = html.replace(f'id="{i}"', f'id="{new}"').replace(f'href="#{i}"', f'href="#{new}"').replace(f'aria-labelledby="{i}"', f'aria-labelledby="{new}"')
    return html


def link(k: str) -> str:
    return "#" + KEY2VIEW.get(k, "lazer")


def page(view: str) -> str:
    key, h1 = VIEWS[view]
    html = render.page_html(key, "m/ig/", h1, link)
    html = html.replace(f'href="{link("fiyat")}#lz-menu"', 'href="#lazer-fiyat/menu"')
    html = suffix_ids(html, key)
    return f'<section data-view="{view}" hidden>\n{html}\n</section>'


def apply(d) -> None:
    css = (LZ / "src/lazer.css").read_text(encoding="utf-8")
    js = (LZ / "src/lazer.js").read_text(encoding="utf-8")
    data = {VIEWS[v][0]: render.page_data(VIEWS[v][0], "m/ig/", False) for v in VIEWS}
    d.css("/* ---------- FAZ L · src/lazer.css (verbatim) ---------- */\n" + css + PROTO_CSS)
    # replace the v3 laser vitrine with the hub, add five more views after it
    pages = "\n\n".join(page(v) for v in VIEWS)
    d.replace_section("lazer", "<!-- ===================== LAZER (FAZ L · 6 sayfa) ===================== -->\n" + pages)
    # laser script + data before the prototype script; mounted lazily by the host (no auto mount)
    d.rep("<script>\n(function(){", "<script>window.ATLZ_NOAUTO=true;window.ATLZ_DATA=" + json.dumps(data, ensure_ascii=False) +
          ";</script>\n<script>\n" + js + "\n</script>\n<script>\n(function(){", 1)
    d.js_before_boot(HOST_JS)
    # bar + planner + story CTA on laser views go to the laser invitation (days + day parts, no sample times)
    d.rep('  $("#barCta").addEventListener("click",function(){ openPlanner(S.view,S.planOpt[S.view]); });',
          '  $("#barCta").addEventListener("click",function(){ if(S.view.indexOf("lazer")===0) return lzPlan(S.view); openPlanner(S.view,S.planOpt[S.view]); });')
    d.rep("function openPlanner(fam,opt){ hideProto(); closeStory();",
          "function openPlanner(fam,opt){ if(fam==='lazer'){ closeStory(); closeSheet(); return lzPlan(); } hideProto(); closeStory();")
    d.rep('  else if(v==="lazer") l.textContent=LZ.sel.length?LZ.sel.length+" bölge · saatimi seç":"Bölgelerim · saatimi seç";',
          '  else if(v.indexOf("lazer")===0) l.textContent=LZV[v]||"Bölgelerim · günümü seç";')
    d.rep('  if(v==="lazer"){ initRegions(); initPairs("galLazer","lazer"); }', '  if(v.indexOf("lazer")===0){ lzMount(v); }')
    # menu entries -> laser views
    import atelier_build as build
    build.nav_map(d, {"laser-signature": "lazer", "lazer-epilasyon-fiyatlari-ankara": "lazer-fiyat", "erkek-lazer-epilasyon": "lazer-erkek",
                      "bolgesel-lazer": "lazer-bolgesel", "yuz-lazer": "lazer-yuz", "hassas-cilt-lazer": "lazer-hassas"})
    build.proto_views(d, [("lazer-fiyat", "Lazer ▸ fiyat"), ("lazer-erkek", "▸ erkek"), ("lazer-yuz", "▸ yüz"),
                          ("lazer-hassas", "▸ hassas"), ("lazer-bolgesel", "▸ bölgesel")], "lazer")
    # every image/video path the laser data and script build at run time
    paths = set(re.findall(r'm/ig/[\w./-]+', json.dumps(data)))
    d.rep("/* ---------- v4 · FAZ L host ---------- */", "/*@media " + json.dumps(sorted(paths)) + " @*/\n/* ---------- v4 · FAZ L host ---------- */")
