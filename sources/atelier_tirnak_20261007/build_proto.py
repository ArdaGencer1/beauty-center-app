#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TIRNAK ATELYESİ -- put the 22 nail pages into the ATELİER prototype (the Claude Artifact's page).

Reads the prototype source (default: the v3 snapshot), applies counted, verified replacements, writes the page.
Only nail code is touched: the tırnak <section>, the nail rows of NAV, SHAPES' kare/oval labels, the old nail-only
functions (initAtelier, initGallery, IG_NAILS, STORIES.tirnak), and the small hooks the nail pages need in shared
code (go() takes "#view/param", the planner prints the tz extras and the 4-week bakım step, the bar asks tz for its label). --check then
confirms that everything outside those spots is byte-for-byte the source.

  python3 sources/atelier_tirnak_20261007/build_proto.py [--src FILE] [--out FILE]

Other families publish to the same Artifact too. When the live version has moved on, build as usual and merge three-way:
the last nail build that went out (--base, kept next to the snapshots) against the live source (--live). Only the nail
edits since --base are carried onto --live; everything the other sessions published stays. A conflict is written to
OUT.conflict for a person to resolve.

  python3 sources/atelier_tirnak_20261007/build_proto.py --base prototypes/.../tirnak-build-vN.html --live live.html
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
import render  # noqa: E402

SRC = REPO / "prototypes" / "claude-artifact" / "WmsLiPPTLdnrjSrdYSXcLM" / "artifact-v3.html"
OUT = REPO / "website" / "index.html"
GROUPS = [("Merkez ve nail art", ["tirnak", "nail-art-ankara"]),
          ("Kalıcı oje", ["kalici-oje", "kalici-oje-fiyatlari", "jel-tirnak", "tirnak-guclendirme"]),
          ("Protez tırnak", ["protez-tirnak", "protez-tirnak-modelleri", "protez-tirnak-fiyatlari-ankara", "protez-tirnak-randevu",
                             "protez-tirnak-bakim-dolgu", "protez-tirnak-cikartma", "tirnak-uzatma", "yeni-nesil-tips", "ayak-protez-tirnak",
                             "cayyolu-protez-tirnak", "yasamkent-protez-tirnak"]),
          ("Manikür ve pedikür", ["manikur-ankara", "pedikur-ankara", "medikal-pedikur", "manikur-pedikur-fiyatlari", "el-ayak-bakimi"])]


class Patch:
    def __init__(self, text: str):
        self.s = text
        self.log: list[str] = []

    def rep(self, old: str, new: str, n: int = 1, what: str = "") -> None:
        c = self.s.count(old)
        if c != n:
            raise SystemExit(f"patch '{what or old[:60]}': expected {n} match(es), found {c}")
        self.s = self.s.replace(old, new)
        self.log.append(what or old[:60])

    def sub(self, pattern: str, new: str, what: str, flags: int = re.S) -> None:
        s2, c = re.subn(pattern, lambda m: new, self.s, flags=flags)
        if c != 1:
            raise SystemExit(f"patch '{what}': expected 1 match, found {c}")
        self.s = s2
        self.log.append(what)


def resolve_linewise(text: str) -> tuple[str, int]:
    """Settle diff3 conflict hunks where the two sides touched different lines: the nail build only edits lines in place,
    so line up base and live inside the hunk and take, per stretch, the side that changed it (live's inserted rows and
    edited rows, our edited nail rows). A stretch both sides changed differently stays a conflict. Returns (text, left)."""
    lines, out, i, left = text.split("\n"), [], 0, 0
    while i < len(lines):
        if not lines[i].startswith("<<<<<<< nail build"):
            out.append(lines[i]); i += 1; continue
        j = lines.index("||||||| base", i); k = lines.index("=======", j); e = lines.index(">>>>>>> live", k)
        ours, base, theirs = lines[i + 1:j], lines[j + 1:k], lines[k + 1:e]
        got = [] if len(ours) == len(base) else None
        for tag, b1, b2, t1, t2 in (difflib.SequenceMatcher(None, base, theirs, autojunk=False).get_opcodes() if got is not None else []):
            if tag == "equal":
                got += ours[b1:b2]
            elif ours[b1:b2] == base[b1:b2] or ours[b1:b2] == theirs[t1:t2]:
                got += theirs[t1:t2]
            else:
                got = None
                break
        if got is None:
            out += lines[i:e + 1]; left += 1
        else:
            out += got
        i = e + 1
    return "\n".join(out), left


def js_json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def section() -> str:
    pages = "\n".join(f'  <template data-tz-page="{p["slug"]}">{render.page_html(p["slug"])}</template>' for p in render.PAGES)
    incs = "\n".join(f'  <template data-tz-inc-tpl="{k}">{fn()}</template>' for k, fn in render.INCLUDES.items())
    return (f'<!-- ===================== TIRNAK ATELYESİ · 22 sayfa (sources/atelier_tirnak_20261007) ===================== -->\n'
            f'<section data-view="tirnak" hidden>\n  <div id="tzMount"></div>\n{pages}\n{incs}\n</section>\n\n')


def proto_row() -> str:
    meta = render.page_meta()
    tag = {"tam": "", "ince": " · ince", "cekim": " · çekim bekliyor"}
    groups = "".join(f'<optgroup label="{g}">' + "".join(f'<option value="{s}">{meta[s]["nav"]}{tag[meta[s]["status"]]}</option>' for s in slugs) + "</optgroup>"
                     for g, slugs in GROUPS)
    return ('  <div class="row"><span>Tırnak sayfası · 22</span><select id="tzSel" class="tz-sel" aria-label="Tırnak sayfası" data-track-label="at-proto-tirnak">'
            f'{groups}</select><p>Tırnak: “çekim bekliyor” sayfalarda gerçek salon görselleriyle dürüst stand-in var. Fiyatı menüde olmayan kalemler '
            '“Fiyatı sorun” olarak WhatsApp\'a gider (sunucuda sync_prices.py ile tamamlanır). Sterilizasyon dili, kişiye özel paket, giriş filmi ve 4 haftalık bakım '
            'sahip onaylı. Kartelada marka yazılmaz; numaralar okundu, etiketin hangi tırnağa ait olduğu netleşince açılır.</p></div>\n')


def build(src: str) -> str:
    P = Patch(src)
    nav_slugs = {s for _, ss in GROUPS for s in ss}
    assert nav_slugs == set(render.BY_SLUG), "GROUPS and PAGES differ"

    css = (HERE / "src" / "tirnak.css").read_text(encoding="utf-8")
    P.rep('}\n</style>\n\n<div class="wrap" lang="tr">', '}\n' + css + '.tz-sel{height:40px;border-radius:12px;border:1px solid var(--line-strong);background:var(--raised);color:var(--text);padding:0 10px;font:14px var(--body);max-width:100%}\n</style>\n\n<div class="wrap" lang="tr">', what="css")
    P.rep('<button data-v="lazer">Lazer</button></div></div>\n', '<button data-v="lazer">Lazer</button></div></div>\n' + proto_row(), what="proto row")
    P.sub(r'<!-- ===================== TIRNAK ===================== -->\n<section data-view="tirnak" hidden>.*?</section>\n\n(?=<!-- ===================== İPEK KİRPİK)',
          section(), "tirnak section")
    # owner does not know whether the kare / oval photos are protez or kalıcı oje: name the shape and colour only
    P.rep('alt:"Kırmızı kare kalıcı oje"}', 'alt:"Kırmızı kare tırnak"}', what="SHAPES kare alt")
    P.rep('alt:"Kırmızı oval kalıcı oje"}', 'alt:"Kırmızı oval tırnak"}', what="SHAPES oval alt")
    P.sub(r'function initAtelier\(\)\{\n.*?\n\}\n(?=\n/\* ---------- gallery ---------- \*/)', '', "drop initAtelier")
    P.sub(r'var IG_NAILS=\[.*?\];\n', '', "drop IG_NAILS", flags=0)
    P.sub(r'function initGallery\(\)\{ var g=\$\("#gal"\);.*?\n', '', "drop initGallery", flags=0)
    # planner: tz price strings, shape label without a colour, tz message and invitation extras
    P.rep('var priceOf=function(x){ return plan.custom?"Kişiye özel":fmtTL(x.p); };',
          'var priceOf=function(x){ return x.ps||(plan.custom?"Kişiye özel":fmtTL(x.p)); }, tz=/^tz-/.test(P.fam);', what="planner priceOf")
    P.rep("'</i> Şekil · renk: '+colorName+'</span>", "'</i> Şekil'+(colorName?' · renk: '+colorName:'')+'</span>", what="planner shape label")
    P.rep('\n  var when=day?(day.full+" · "+P.time):"";\n', '\n  if(tz){ var bk=tzBakim(o,day,stepN); if(bk){ h+=bk; stepN++; } }\n  var when=day?(day.full+" · "+P.time):"";\n', what="planner bakım step")
    P.rep('\n  P.msg=msg;\n', '\n  if(tz) msg=tzMsg(o,day,P.time,plan.shapes?P.shape:null,P.code);\n  P.msg=msg;\n', what="planner tz msg")
    P.rep('lbl($("#sendWa"),"at-"+P.fam+"-davetiye-wa"); relead();',
          'lbl($("#sendWa"),"at-"+P.fam+"-davetiye-wa"); relead(); if(tz) tzBakimBind($("#sheetBody"),renderPlanner,"at-"+P.fam+"-davetiye-bakim");', what="planner bakım bind")
    P.rep("(colorName?' · '+colorName+(P.shape?' · '+P.shape:''):'')+'<br>Konutkent",
          "(colorName?' · '+colorName+(P.shape?' · '+P.shape:''):'')+(tz?tzMeta(plan.shapes?P.shape:null,o):'')+'<br>Konutkent", what="planner tz meta")
    P.rep("'+fmtTL(x.p)+'</b></div>'", "'+(x.ps||fmtTL(x.p))+'</b></div>'", what="priceCard ps")
    P.sub(r' tirnak:\[\{t:"Tasarımlar".*?fr:"price:tirnak"\}\],\n', '', "drop STORIES.tirnak")
    # NAV: every nail page is a vitrine route now
    m = re.search(r'var NAV=(\[.*?\]);\n', P.s)
    nav = json.loads(m.group(1))
    assert json.dumps(nav, ensure_ascii=False) == m.group(1), "NAV does not round-trip"
    grp = [g for g in nav if g[0] == "Tırnak"][0]
    assert {it[0] for it in grp[1]} == nav_slugs, "NAV nail slugs differ from PAGES"
    grp[1] = [[it[0], it[1], "tirnak" if it[0] == "tirnak" else "tirnak/" + it[0]] for it in grp[1]]
    P.rep(m.group(0), "var NAV=" + json.dumps(nav, ensure_ascii=False) + ";\n", what="NAV routes")
    P.rep('function openMenu(){ hideProto(); var cur=S.view;', 'function openMenu(){ hideProto(); var cur=S.view==="tirnak"?tzRoute():S.view;', what="menu here")
    js = (HERE / "src" / "tirnak.js").read_text(encoding="utf-8")
    js = (js.replace("__TZ_PAGES__", js_json(render.page_meta()))
            .replace("__TZ_REVIEWS__", js_json(render.REVIEWS))
            .replace("__TZ_QUOTES__", js_json(render.QUOTES))
            .replace("__TZ_PLANS__", js_json(render.plans_js()))
            .replace("__TZ_BAKIM__", str(render.BAKIM_HAFTA)))
    assert "__TZ_" not in js
    P.rep('\n/* ---------- views ---------- */\n', '\n' + js + '\n/* ---------- views ---------- */\n', what="tz js")
    P.rep('if(v==="tirnak"){ var s=SW.filter(function(x){return x.id===S.color})[0]; l.textContent=(s?s.name:"Rengim")+" · saatimi seç"; }',
          'if(v==="tirnak"){ l.textContent=tzBarLabel(); }', what="bar label")
    P.rep('lbl($("#barCta"),"at-"+v+"-bar-saat"); lbl($("#callBtn"),"at-"+v+"-bar-tel"); }',
          'var bk=v==="tirnak"?tzKey():v; lbl($("#barCta"),"at-"+bk+"-bar-saat"); lbl($("#callBtn"),"at-"+bk+"-bar-tel"); }', what="bar labels")
    P.rep('if(v==="tirnak"){ initAtelier(); initGallery(); }', 'if(v==="tirnak"){ tzBoot(); }', what="initView")
    P.rep('function go(v,noTrans){ if(!document.querySelector("[data-view=\'"+v+"\']")) v="salon";\n'
          '  function apply(){ $$("main > [data-view]").forEach(function(s){ s.hidden=s.dataset.view!==v; }); S.view=v; root.dataset.page=v; window.scrollTo({top:0,behavior:"instant"}); initView(v); updateBar(); markSeg("view",v); onScroll(); }\n'
          '  if(!noTrans && document.startViewTransition && S.tier!=="C") document.startViewTransition(apply); else apply();\n'
          '  try{ history.replaceState(null,"","#"+v); }catch(e){} }',
          'function go(v,noTrans){ var prm="", k=v.indexOf("/"); if(k>0){ prm=v.slice(k+1); v=v.slice(0,k); } if(!document.querySelector("[data-view=\'"+v+"\']")){ v="salon"; prm=""; }\n'
          '  function apply(){ $$("main > [data-view]").forEach(function(s){ s.hidden=s.dataset.view!==v; }); S.view=v; S.route=v+(prm?"/"+prm:""); root.dataset.page=v; window.scrollTo({top:0,behavior:"instant"}); initView(v); if(v==="tirnak") tzShow(prm||"tirnak"); updateBar(); markSeg("view",v); onScroll(); }\n'
          '  if(!noTrans && document.startViewTransition && S.tier!=="C") document.startViewTransition(apply); else apply();\n'
          '  try{ history.replaceState(null,"","#"+v+(prm?"/"+prm:"")); }catch(e){} }', what="go() routes")
    P.rep('go(VIEWS.indexOf(h)>0?h:"salon",true);', 'go(VIEWS.indexOf(h.split("/")[0])>0?h:"salon",true);', what="boot route")
    P.rep('if(VIEWS.indexOf(h)>=0 && h!==S.view) go(h);', 'if(VIEWS.indexOf(h.split("/")[0])>=0 && h!==S.route) go(h);', what="hashchange route")
    P.rep('$("#barCta").addEventListener("click",function(){ openPlanner(S.view,S.planOpt[S.view]); });',
          '$("#barCta").addEventListener("click",function(){ if(S.view==="tirnak"&&TZ.pg) return openPlanner(TZ.pg.fam,TZ.pg.opt||null); openPlanner(S.view,S.planOpt[S.view]); });', what="bar cta")
    print(f"{len(P.log)} patches applied")
    return P.s


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(SRC))
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--base", default="", help="the nail build the live Artifact last received (merge base)")
    ap.add_argument("--live", default="", help="the live Artifact source to merge the new nail edits onto")
    ap.add_argument("--build-out", default="", help="also keep the plain build here (the next --base)")
    a = ap.parse_args()
    src = Path(a.src).read_text(encoding="utf-8")
    out = build(src)
    if a.build_out:
        Path(a.build_out).write_text(out, encoding="utf-8")
    if a.live:
        if not a.base:
            raise SystemExit("--live needs --base")
        with tempfile.TemporaryDirectory() as td:
            ours = Path(td) / "ours.html"
            ours.write_text(out, encoding="utf-8")
            r = subprocess.run(["git", "merge-file", "-p", "--diff3", "-L", "nail build", "-L", "base", "-L", "live", str(ours), a.base, a.live],
                               capture_output=True)
        merged, left = resolve_linewise(r.stdout.decode("utf-8"))
        if r.returncode:
            print(f"{r.returncode - left} conflict(s) settled line by line")
        if left:
            Path(a.out + ".conflict").write_text(merged, encoding="utf-8")
            raise SystemExit(f"{left} conflict(s): resolve {a.out}.conflict by hand (keep both sides' intent), then check it")
        print(f"merged onto {a.live}")
        out = merged
    Path(a.out).write_text(out, encoding="utf-8")
    print(f"{a.out}: {len(out.encode()):,} bytes (source {len(src.encode()):,})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
