#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ATELIER prototype v4 -- one build for the three 2026-10-07 plans.

  v3 snapshot (frozen)  prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/artifact-v3.html
        |  rep(): counted, verified string edits (a missing anchor stops the build)
        |  shared   -- film atlases, walk stills, monogram, golden mirror, routing (#view/param), menu
        |  lazer    -- FAZ L: 6 views, markup from atelier_lazer_20261007/render.py + src/lazer.css/js
        |  pmu      -- Kalıcı Makyaj "Şölen": pmu, pmu-dudak, pmu-kas, pmu-goz (pmu/pmu_build.py)
        |  cilt     -- Cilt Atlası: hub + 24 pages on one page engine (cilt/cilt_build.py)
        v
  website/index.html  (+ prototypes/.../artifact-v4.html copy, dist/publish.json = every m/ file the page uses)

Usage: build.py [--check]     --check also fails on a broken m/ reference or a file budget overflow.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SRC = REPO / "prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/artifact-v3.html"
OUT = REPO / "website/index.html"
SNAP = REPO / "prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/artifact-v4.html"
SITE = REPO / "website"
BUDGET = 255          # files per artifact publish (page + supporting files)


class Doc:
    def __init__(self, text: str):
        self.t = text
        self.n = 0

    def rep(self, old: str, new: str, count: int = 1) -> None:
        k = self.t.count(old)
        if k != count:
            raise SystemExit(f"rep #{self.n + 1}: expected {count} x {old[:90]!r}, found {k}")
        self.t = self.t.replace(old, new)
        self.n += 1

    def sub(self, pat: str, new, count: int = 1, flags: int = re.S) -> None:
        t, k = re.subn(pat, new, self.t, flags=flags)
        if k != count:
            raise SystemExit(f"sub #{self.n + 1}: expected {count} x /{pat[:90]}/, found {k}")
        self.t = t
        self.n += 1

    def section(self, view: str) -> tuple[int, int]:
        a = self.t.index(f'<section data-view="{view}"')
        b = self.t.index("</section>", a) + len("</section>")
        return a, b

    def replace_section(self, view: str, new: str) -> None:
        a, b = self.section(view)
        self.t = self.t[:a] + new + self.t[b:]
        self.n += 1

    def css(self, block: str) -> None:
        self.rep("\n</style>\n\n<div class=\"wrap\"", "\n" + block.strip() + "\n</style>\n\n<div class=\"wrap\"")

    def js_before_boot(self, block: str) -> None:
        self.rep("\n/* ---------- boot ---------- */", "\n" + block.strip() + "\n\n/* ---------- boot ---------- */")


# ---------------------------------------------------------------------------------------------------- shared
ATLAS_JS = r"""
/* ---------- v4: film atlases (3x3 frames per sheet; one request instead of nine) ---------- */
function atlas(set,n,fw,fh,per){ per=per||9; var sheets=[], A={n:n,ready:false};
  A.load=function(cb){ if(A.started) return; A.started=true; var order=[]; for(var k=0;k*per<n;k++) order.push(k);
    (function next(){ var k=order.shift(); if(k===undefined) return; var im=new Image(); im.decoding="async"; im.src="m/ig/film/"+set+"/a"+(k+1)+".webp";
      im.onload=function(){ (im.decode?im.decode():Promise.resolve()).catch(function(){}).then(function(){ sheets[k]=im; A.ready=true; if(cb) cb(k); next(); }); }; im.onerror=next; })(); };
  A.near=function(i){ i=Math.max(0,Math.min(n-1,i)); var k=Math.floor(i/per);
    if(!sheets[k]){ var found=-1; for(var d=1;d<=Math.ceil(n/per);d++){ if(sheets[k-d]){ found=k-d; i=found*per+per-1; break; } if(sheets[k+d]){ found=k+d; i=found*per; break; } } if(found<0) return null; k=found; }
    var j=i-k*per; return {img:sheets[k],x:(j%3)*fw,y:Math.floor(j/3)*fh,w:fw,h:fh}; };
  A.draw=function(ctx,i,cw,ch){ var f=A.near(i); if(!f) return false; var s=Math.max(cw/f.w,ch/f.h), w=f.w*s, h=f.h*s; ctx.drawImage(f.img,f.x,f.y,f.w,f.h,(cw-w)/2,(ch-h)/2,w,h); return true; };
  return A; }
"""

ROUTE_JS = r"""
/* ---------- v4: routes  #view  or  #view/param  (e.g. #pmu-kas/pudra, #cilt/akne-bakimi, #lazer-fiyat/menu) ---------- */
var ROUTE_HOOK={}, ROUTE_ALIAS=[];
function parseRoute(h){ h=String(h||"").replace(/^#/,""); if(h.indexOf("/")<0 && h.indexOf(".")>0) h=h.replace(".","/"); var i=h.indexOf("/"); return {v:i<0?h:h.slice(0,i),p:i<0?"":decodeURIComponent(h.slice(i+1))}; }
function routeTo(r){ for(var i=0;i<ROUTE_ALIAS.length;i++){ var x=ROUTE_ALIAS[i](r); if(x) return x; } return {sec:r.v,p:r.p,route:r.v+(r.p?"/"+r.p:"")}; }
"""


def shared(d: Doc) -> None:
    # missing v3 files are now real media (shared_media.py); certificate figure captions stay
    d.rep('<img class="walk-img walk-ph" data-src="m/walk-06.webp" alt="Altın korkuluklu merdiven" width="720" height="960">',
          '<img class="walk-img walk-ph" data-src="m/walk-06.webp" alt="Altın korkuluklu merdiven ve bekleme salonu" width="720" height="960">')
    d.rep('<img class="walk-img walk-ph" data-src="m/walk-08.webp" alt="Uygulama odasının kapısı açılıyor" width="720" height="960">',
          '<img class="walk-img walk-ph" data-src="m/walk-08.webp" alt="Uygulama odası" width="720" height="960">')
    d.rep('<img class="walk-img walk-ph" data-src="m/walk-09.webp" alt="Halka ışıklı uygulama odası" width="720" height="960">',
          '<img class="walk-img walk-ph" data-src="m/walk-09.webp" alt="Büyüteç lambalı cilt bakım odası" width="720" height="960">')
    d.rep('<img class="walk-img walk-ph" data-src="m/walk-10.webp" alt="Halka ışık altında uygulama" width="720" height="960">',
          '<img class="walk-img walk-ph" data-src="m/walk-10.webp" alt="Işık altında uygulama" width="720" height="960">')
    d.rep('{n:"07",t:"Kapınız.",s:"Sizin için hazırlanan oda."},\n  {n:"08",t:"Halka ışık altında.",s:"Her detay milim milim görünür."},',
          '{n:"07",t:"Odanız.",s:"Sizin için hazırlanan oda."},\n  {n:"08",t:"Işık altında.",s:"Her detay milim milim görünür."},')
    # film frames -> atlases (salon walk: salon-giris; LED film: cilt-led)
    d.rep('  function fsrc(i){ return "m/ig/film/salon-giris/f"+String(i+1).padStart(2,"0")+".webp"; }\n', '  var FA=atlas("salon-giris",NF,540,960);\n')
    d.sub(r'  function loadFilm\(\)\{ if\(S\.tier==="C"\) return; var step=.*?next\(\); next\(\); next\(\); \}\n',
          '  function loadFilm(){ if(S.tier==="C") return; FA.load(function(){ if(curF<0) onScroll(); }); }\n')
    d.rep('  function nearest(i){ if(frames[i]) return frames[i]; for(var d=1;d<NF;d++){ if(frames[i-d]) return frames[i-d]; if(frames[i+d]) return frames[i+d]; } return null; }\n'
          '  function drawF(i){ var im=nearest(i); if(!im) return false; if(!cw) size(); var k=Math.max(cw/im.naturalWidth,ch/im.naturalHeight), w=im.naturalWidth*k, h=im.naturalHeight*k; ctx.drawImage(im,(cw-w)/2,(ch-h)/2,w,h); return true; }',
          '  function drawF(i){ if(!cw) size(); return FA.draw(ctx,i,cw,ch); }')
    d.rep('  function src(i){ return "m/ig/film/cilt-led/f"+String(i+1).padStart(2,"0")+".webp"; }\n', '  var FA=atlas("cilt-led",N,540,960);\n')
    d.sub(r'  function load\(\)\{ if\(loading\|\|S\.tier==="C"\) return; loading=true;.*?next\(\); next\(\); next\(\); \}\n',
          '  function load(){ if(loading||S.tier==="C") return; loading=true; FA.load(function(){ if(cur<0) draw(0); }); }\n')
    d.rep('  function nearest(i){ if(frames[i]) return frames[i]; for(var d=1;d<N;d++){ if(frames[i-d]) return frames[i-d]; if(frames[i+d]) return frames[i+d]; } return null; }\n'
          '  function draw(i){ var im=nearest(i); if(!im) return; ctx.drawImage(im,0,0,cv.width,cv.height); cv.style.opacity=1; cur=i; }',
          '  function draw(i){ if(!FA.draw(ctx,i,cv.width,cv.height)) return; cv.style.opacity=1; cur=i; }')
    d.rep("/* ---------- WALK ---------- */", ATLAS_JS.strip() + "\n\n/* ---------- WALK ---------- */")

    # golden mirror: kas-cift-3 carried a foreign watermark (owner 10-07) -> salon's own kına kaş, points re-measured
    d.rep('<img src="m/ig/kas-cift-3-sonra-800.webp" alt="Altın oran ölçü çizgileriyle kaş" width="800" height="500" loading="lazy">',
          '<img src="m/ig/kas-kina-sonra-800.webp" alt="Altın oran ölçü çizgileriyle kaş" width="800" height="534" loading="lazy">')
    d.rep('<path class="g-line" pathLength="1" d="M830 900 L602 209"/>\n          <path class="g-line" pathLength="1" d="M830 900 L300 50"/>\n          <path class="g-line" pathLength="1" d="M830 900 L-5 188"/>',
          '<path class="g-line" pathLength="1" d="M830 900 L690 168"/>\n          <path class="g-line" pathLength="1" d="M830 900 L450 64"/>\n          <path class="g-line" pathLength="1" d="M830 900 L-5 232"/>')
    d.rep('<circle class="g-ring d1" cx="615" cy="248" r="13"/><circle class="g-ring d2" cx="330" cy="98" r="13"/><circle class="g-ring d3" cx="42" cy="228" r="13"/>\n          <circle class="g-dot d1" cx="615" cy="248" r="9"/><circle class="g-dot d2" cx="330" cy="98" r="9"/><circle class="g-dot d3" cx="42" cy="228" r="9"/>\n          <text class="g-lbl d1" x="640" y="214" text-anchor="end">BAŞLANGIÇ</text>\n          <text class="g-lbl d2" x="352" y="70">KAVİS</text>\n          <text class="g-lbl d3" x="30" y="300">BİTİŞ</text>',
          '<circle class="g-ring d1" cx="700" cy="196" r="13"/><circle class="g-ring d2" cx="478" cy="104" r="13"/><circle class="g-ring d3" cx="30" cy="262" r="13"/>\n          <circle class="g-dot d1" cx="700" cy="196" r="9"/><circle class="g-dot d2" cx="478" cy="104" r="9"/><circle class="g-dot d3" cx="30" cy="262" r="9"/>\n          <text class="g-lbl d1" x="760" y="262" text-anchor="end">BAŞLANGIÇ</text>\n          <text class="g-lbl d2" x="500" y="66">KAVİS</text>\n          <text class="g-lbl d3" x="18" y="320">BİTİŞ</text>')
    d.rep('var KAS_PAIRS=[["kas-cift-2","Kaş alımı"],["kas-cift-3","Kaş tasarımı"],["kas-kina","Altın oran · kına"],["kas-laminasyon","Kaş laminasyonu"]];',
          'var KAS_PAIRS=[["kas-cift-2","Kaş alımı"],["kas-kina","Altın oran · kına"],["kas-laminasyon","Kaş laminasyonu"]];')
    d.rep('var MOSAIC=[["kirpik-makro-3","Mega volüm ipek kirpik"],["dudak-cift-1-sonra","Dudak renklendirme"],["tirnak-holo","Holografik nail art"],["kas-profil","Altın oran kaş"],["cilt-yarim-1","Cilt bakımı, önce ve sonra"],',
          'var MOSAIC=[["kirpik-makro-3","Mega volüm ipek kirpik"],["dudak-cift-1-sonra","Dudak renklendirme"],["tirnak-holo","Holografik nail art"],["kas-profil","Altın oran kaş"],["akne-a-sonra","Akne bakımı sonrası"],')

    # routing: #view/param, aliases, per-view hooks
    d.rep("/* ---------- views ---------- */", ROUTE_JS.strip() + "\n\n/* ---------- views ---------- */")
    d.rep('function go(v,noTrans){ if(!document.querySelector("[data-view=\'"+v+"\']")) v="salon";\n'
          '  function apply(){ $$("main > [data-view]").forEach(function(s){ s.hidden=s.dataset.view!==v; }); S.view=v; root.dataset.page=v; window.scrollTo({top:0,behavior:"instant"}); initView(v); updateBar(); markSeg("view",v); onScroll(); }\n'
          '  if(!noTrans && document.startViewTransition && S.tier!=="C") document.startViewTransition(apply); else apply();\n'
          '  try{ history.replaceState(null,"","#"+v); }catch(e){} }',
          'function go(route,noTrans){ var R=routeTo(parseRoute(route)), v=R.sec; if(!document.querySelector("main > [data-view=\'"+v+"\']")){ v="salon"; R={sec:v,p:"",route:"salon"}; }\n'
          '  var same=v===S.view;\n'
          '  function apply(){ $$("main > [data-view]").forEach(function(s){ s.hidden=s.dataset.view!==v; }); S.view=v; S.param=R.p; S.route=R.route; root.dataset.page=v; window.scrollTo({top:0,behavior:"instant"}); initView(v); if(ROUTE_HOOK[v]) ROUTE_HOOK[v](R.p); updateBar(); markSeg("view",R.route.split("/")[0]==="cilt"?"cilt":v); onScroll(); }\n'
          '  if(!noTrans && !same && document.startViewTransition && S.tier!=="C") document.startViewTransition(apply); else apply();\n'
          '  try{ history.replaceState(null,"","#"+R.route); }catch(e){} }')
    d.rep('  var h=(location.hash||"").replace("#",""); go(VIEWS.indexOf(h)>0?h:"salon",true); autoLabel();',
          '  var h=(location.hash||"").replace("#",""); go(h||"salon",true); autoLabel();')
    d.rep('  addEventListener("hashchange",function(){ var h=(location.hash||"").replace("#",""); if(VIEWS.indexOf(h)>=0 && h!==S.view) go(h); });',
          '  addEventListener("hashchange",function(){ var h=(location.hash||"").replace("#",""); if(h && h!==S.route) go(h); });')
    # menu: a page that has a vitrine opens it (route may carry a parameter), "here" compares routes
    d.rep("function openMenu(){ hideProto(); var cur=S.view;", "function openMenu(){ hideProto(); var cur=S.route||S.view;")
    d.rep('(it[2]===cur?\'Buradasınız\':\'Vitrin\')', '(it[2]===cur?\'Buradasınız\':(VITRIN_TAG[it[2]]||\'Vitrin\'))')
    d.rep("var NAVN=NAV.reduce(", "var VITRIN_TAG={};\nvar NAVN=NAV.reduce(")
    # monogram file: same name, now a real keyed PNG (shared_media.py); stories ring thumbnails keep it


def nav_map(d: Doc, mapping: dict[str, str], tags: dict[str, str] | None = None) -> None:
    """Point NAV entries (slug -> route) at vitrines.  NAV is one JSON-ish line in the v3 script."""
    a = d.t.index("var NAV=")
    b = d.t.index(";\n", a)
    nav = json.loads(d.t[a + len("var NAV="):b])
    hit = set()
    for _g, items in nav:
        for it in items:
            if it[0] in mapping:
                route = mapping[it[0]]
                if len(it) == 2:
                    it.append(route)
                else:
                    it[2] = route
                hit.add(it[0])
    miss = set(mapping) - hit
    if miss:
        raise SystemExit(f"nav_map: slugs not in NAV: {sorted(miss)}")
    d.t = d.t[:a] + "var NAV=" + json.dumps(nav, ensure_ascii=False) + d.t[b:]
    if tags:
        d.rep("var VITRIN_TAG={};", "var VITRIN_TAG={};\nObject.assign(VITRIN_TAG," + json.dumps(tags, ensure_ascii=False) + ");")
    d.n += 1


def proto_views(d: Doc, buttons: list[tuple[str, str]], after: str) -> None:
    btn = "".join(f'<button data-v="{v}">{t}</button>' for v, t in buttons)
    a = d.t.index('<div class="seg" data-ctl="view">')
    b = d.t.index("</div>", a)
    seg = d.t[a:b]
    k = seg.index(f'data-v="{after}"')
    end = seg.index("</button>", k) + len("</button>")
    seg = seg[:end] + btn + seg[end:]
    d.t = d.t[:a] + seg + d.t[b:]
    d.n += 1


def views_list(d: Doc, add: list[str]) -> None:
    d.rep('var VIEWS=["salon","kas","tirnak","kirpik","lifting","pmu","cilt","lazer"];',
          'var VIEWS=["salon","kas","tirnak","kirpik","lifting","pmu","cilt","lazer"' + "".join(f',"{v}"' for v in add) + "];")


# ---------------------------------------------------------------------------------------------------- checks
def media_refs(html: str) -> set[str]:
    refs = set(re.findall(r'(m/[A-Za-z0-9_./-]+\.(?:webp|png|mp4|jpg|avif|svg|json))', html))
    return refs


def dynamic_refs(html: str) -> set[str]:
    """Paths the scripts build at run time; modules register them in a JSON comment block."""
    out = set()
    for blob in re.findall(r"/\*@media (.*?) @\*/", html, re.S):
        out.update(json.loads(blob))
    return out


def v3_dynamic(html: str) -> set[str]:
    """Paths the v3 script builds from slug lists (galleries, mosaic, nails, walk/film atlases) that are still live."""
    out = set()
    a = html.index("var GAL={kirpik:")
    b = html.index("]],", a)
    for s, k in re.findall(r'\["([a-z0-9-]+)","[^"]*","(pair|pair480|one)"\]', html[a:b]):
        out |= {f"m/ig/{s}-sonra-800.webp", f"m/ig/{s}-once-800.webp"} if k == "pair" else {f"m/ig/{s}-800.webp"}
    a = html.index("var KAS_PAIRS=")
    for s in re.findall(r'\["([a-z0-9-]+)",', html[a:html.index(";", a)]):
        out |= {f"m/ig/{s}-sonra-800.webp", f"m/ig/{s}-once-800.webp"}
    for name in ("var IG_NAILS=", "var MOSAIC="):
        a = html.index(name)
        for s in re.findall(r'\["([a-z0-9-]+)",', html[a:html.index(";", a)]):
            out.add(f"m/ig/{s}-800.webp")
    for st, n in (("salon-giris", 8), ("cilt-led", 7)):
        out |= {f"m/ig/film/{st}/a{k}.webp" for k in range(1, n + 1)}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    sys.path.insert(0, str(HERE))
    sys.modules["atelier_build"] = sys.modules[__name__]   # modules reach the helpers by this name
    d = Doc(SRC.read_text(encoding="utf-8"))
    shared(d)
    import mod_lazer
    mod_lazer.apply(d)
    try:
        sys.path.insert(0, str(HERE / "pmu"))
        import pmu_build
        pmu_build.apply(d)
    except ModuleNotFoundError as e:
        if e.name != "pmu_build":
            raise
        print("pmu: module not present yet, skipped")
    try:
        sys.path.insert(0, str(HERE / "cilt"))
        import cilt_build
        cilt_build.apply(d)
    except ModuleNotFoundError as e:
        if e.name != "cilt_build":
            raise
        print("cilt: module not present yet, skipped")
    # the viewer's theme picks the opening world when nothing is stored (data-theme first, then the OS setting)
    d.rep('  S.world=store("world")||"mermer";',
          '  S.world=store("world")||(root.getAttribute("data-theme")==="dark"||(root.getAttribute("data-theme")!=="light"&&matchMedia("(prefers-color-scheme: dark)").matches)?"gece":"mermer");')
    d.rep("<title>Selda Gençer Atelier</title>", "<title>Selda Gençer Atelier</title>\n<!-- ATELIER prototype v4 · 2026-10-07 · lazer + kalıcı makyaj + cilt atlası -->")
    html = d.t
    OUT.write_text(html, encoding="utf-8")
    SNAP.write_text(html, encoding="utf-8")
    # the artifact publish wraps the page in its own skeleton: publish the authored part only
    body = html.split("<body>", 1)[1] if html.startswith("<!doctype html>") else html
    body = body.rsplit("</body></html>", 1)[0]
    (REPO / "sources/atelier_v4/dist").mkdir(exist_ok=True)
    (REPO / "website/atelier-v4.html").write_text(body.lstrip("\n"), encoding="utf-8")
    refs = sorted(media_refs(html) | dynamic_refs(html) | v3_dynamic(html))
    missing = [r for r in refs if not (SITE / r).exists()]
    dist = REPO / "sources/atelier_v4/dist"
    dist.mkdir(exist_ok=True)
    (dist / "publish.json").write_text(json.dumps({"files": refs}, ensure_ascii=False, indent=1), encoding="utf-8")
    size = sum((SITE / r).stat().st_size for r in refs if (SITE / r).exists())
    print(f"edits: {d.n} · html {len(html.encode()) // 1024} KB · media files {len(refs)} ({size / 1e6:.1f} MB) · missing {len(missing)}")
    for m in missing:
        print("  MISSING", m)
    if a.check and (missing or len(refs) + 1 > BUDGET):
        raise SystemExit(f"check failed: missing={len(missing)} files={len(refs) + 1}/{BUDGET}")


if __name__ == "__main__":
    main()
