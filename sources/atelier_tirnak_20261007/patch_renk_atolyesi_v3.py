#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Renk Atölyesi v3 + nail film swap -- an exact, step-by-step patch of the live Artifact page.

Every step is a literal replacement that must match the expected number of times, so a step that no
longer fits the page stops the run instead of half-applying. Steps print as they apply; the step log
(plans/claude/20261007/renk-atolyesi-v3-adimlar.md) explains each one.

  python3 -I patch_renk_atolyesi_v3.py IN.html OUT.html

Media this patch expects next to the page (refine_nail_masks.py writes the first two):
  m/ig/tirnak-{uzun,kare,yuvarlak}-kirmizi-mask-v3.png
  m/ig/tirnak-{uzun,kare,yuvarlak}-kirmizi-shade-1200.webp
  m/ig/tirnak-{babyboomer,krom,lila}{.mp4,-poster.webp}   (already published)
After it, m/ig/tirnak-orkide{.mp4,-poster.webp} and the v2 *-mask.png are no longer referenced.
"""
from __future__ import annotations

import sys

STEPS: list[tuple[str, str, str, int]] = []


def step(name: str, old: str, new: str, count: int = 1) -> None:
    STEPS.append((name, old, new, count))


# ---------------------------------------------------------------- A. orkide -> sharper nail films
# A1/A2 are scoped to one template each (see SCOPED below); A3 is the kalıcı oje story reel.
step("A3 hikâye (tz-oje): orkide karesi -> baby boomer",
     '{video:"m/ig/tirnak-orkide.mp4",poster:"m/ig/tirnak-orkide-poster.webp",cap:"Bordo"}',
     '{video:"m/ig/tirnak-babyboomer.mp4",poster:"m/ig/tirnak-babyboomer-poster.webp",cap:"Baby boomer"}')

step("A4 kapanış bandı: sayfada zaten oynayan filmi tekrar etme (tzFinalPick çağrısı)",
     'el.parentNode.replaceChild(f,el); });\n  TZ.page=slug;',
     'el.parentNode.replaceChild(f,el); });\n  tzFinalPick(mount);\n  TZ.page=slug;')

step("A5 tzFinalPick tanımı",
     '/* ---------- T2: Renk Atölyesi v2',
     '/* closing band: the sharpest nail film the page is not already playing (hero, wall, route tiles) */\n'
     'var TZ_FINAL=[["babyboomer","Baby boomer ombre protez tırnak, altın varak; salonumuzda çekildi"],'
     '["krom","Simli krom french badem tırnak; salonumuzda çekildi"],'
     '["lila","Süt beyazı badem protez tırnak; salonumuzda çekildi"]];\n'
     'function tzFinalPick(mount){ var box=$(".tz-final-media",mount); if(!box) return;\n'
     '  var used=$$("video[data-src]",mount).filter(function(v){ return !box.contains(v); }).map(function(v){ return v.dataset.src; });\n'
     '  var hv=$(".hero video[data-src]",mount), hs=hv&&hv.dataset.src, vs=function(x){ return "m/ig/tirnak-"+x[0]+".mp4"; };\n'
     '  // unused on this page first; when the page plays all three, at least not the hero\'s film again\n'
     '  var f=TZ_FINAL.filter(function(x){ return used.indexOf(vs(x))<0; })[0]||TZ_FINAL.filter(function(x){ return vs(x)!==hs; })[0]||TZ_FINAL[0],\n'
     '      im=$("img",box), vd=$("video",box), po="m/ig/tirnak-"+f[0]+"-poster.webp";\n'
     '  if(im){ im.src=po; im.alt=f[1]; } if(vd){ vd.poster=po; vd.dataset.src=vs(f); } }\n\n'
     '/* ---------- T2: Renk Atölyesi v2')

# ---------------------------------------------------------------- B. v3 mattes + shade plates
for shape in ("uzun", "kare", "yuvarlak"):
    step(f"B1 SHAPES.{shape}: v3 maske + gölge katmanı",
         f'mask:"m/ig/tirnak-{shape}-kirmizi-mask.png",',
         f'mask:"m/ig/tirnak-{shape}-kirmizi-mask-v3.png",shade:"m/ig/tirnak-{shape}-kirmizi-shade-1200.webp",')

step("B2 TZ_LREF: v3 maskelerin altındaki ortalama tırnak parlaklığı",
     'var TZ_LREF={uzun:.233,kare:.217,oval:.348}',
     'var TZ_LREF={uzun:.236,kare:.214,oval:.349}')

step("B3 boya katmanı fotoğrafın yerine gölge plakasını boyar (açık renklerde hale yok)",
     't.style.backgroundImage="url("+sh.img+")";',
     't.style.backgroundImage="url("+(sh.shade||sh.img)+")";')

# ---------------------------------------------------------------- C. the sweep: crisp wet edge
step("C1 süpürme kenarı: %12 bulanık rampa -> %5 net fırça kenarı",
     'var TZ_SWEEP="linear-gradient(90deg,#000 calc(var(--x) * 1.12% - 12%),transparent calc(var(--x) * 1.12%))";',
     'var TZ_SWEEP="linear-gradient(90deg,#000 calc(var(--x) * 1.06% - 5%),transparent calc(var(--x) * 1.06%))";')

step("C2 şablonlar: ıslak parıltı katmanı (yalnızca tırnakların üstünde)",
     '<span class="tz-brush" aria-hidden="true"></span>',
     '<span class="tz-wet" aria-hidden="true"></span><span class="tz-brush" aria-hidden="true"></span>', 2)

step("C3 şablonlar: dar ekranda kısalabilen ipucu",
     '<span>Renk Atölyesi · parmağınızla boyayın</span>',
     '<span><i>Renk Atölyesi · </i>parmağınızla boyayın</span>', 2)

# ---------------------------------------------------------------- D. tzAtelier: wet layer, cross-fade, drag
step("D1 tzAtelier: ıslak katman referansı",
     'row=$(".sw-row",st), name=$(".tz-swname",st);\n  var shape=TZ_LREF[S.shape]?S.shape:"uzun",',
     'row=$(".sw-row",st), name=$(".tz-swname",st), wet=$(".tz-wet",st), swap=0;\n  var shape=TZ_LREF[S.shape]?S.shape:"uzun",')

step("D2 tzAtelier: wetMask + ghost (şekil değişiminde çapraz geçiş)",
     '  function orig(){ return TZ_ORIG[shape]; }\n',
     '  function orig(){ return TZ_ORIG[shape]; }\n'
     '  function wetMask(){ if(!wet) return; var mi="url("+SHAPES[shape].mask+")"; wet.style.webkitMaskImage=wet.style.maskImage=mi; }\n'
     '  /* freeze what is on screen into one layer above the photos, so a shape change cross-fades instead of blinking */\n'
     '  function ghost(){ if(S.tier==="C") return null; var g=document.createElement("div"); g.className="tz-ghost"; g.setAttribute("aria-hidden","true");\n'
     '    [base,neu].concat(T).forEach(function(el){ var o=+getComputedStyle(el).opacity; if(o<.01) return; var c=el.cloneNode(false); c.removeAttribute("loading"); c.style.transition="none"; c.style.opacity=o; g.appendChild(c); });\n'
     '    st.insertBefore(g,$(".ba-toggle",st)); return g; }\n')

step("D3 setShape: dört dosya birlikte çözülür, yarış yok, çapraz geçiş",
     '''  function setShape(k){ if(k===shape) return; var sh=SHAPES[k]; shape=k; S.shape=k; $$("[data-tz-shape]",st).forEach(function(x){ x.setAttribute("aria-pressed",x.dataset.tzShape===k); });
    var im=new Image(); im.src=sh.img; stop();
    (im.decode?im.decode():Promise.resolve()).catch(function(){}).then(function(){ base.style.opacity=0; TZ.timers.push(setTimeout(function(){
      base.src=sh.img; base.alt=sh.alt; neu.src=sh.neutral; T.forEach(function(t){ t.classList.remove("on"); }); st.classList.remove("painted","sweeping"); neuSweep(false); cur=null; front=0;
      var c=TZ.color&&TZ.colorTouched?TZ.color:orig(); if(c!==orig()) paint(c,false); else { label(c); cur=c; } base.style.opacity=1; updateBar(); },180)); }); }''',
     '''  function setShape(k){ if(k===shape) return; var sh=SHAPES[k], my=++swap; $$("[data-tz-shape]",st).forEach(function(x){ x.setAttribute("aria-pressed",x.dataset.tzShape===k); });
    stop(); Promise.all([sh.img,sh.neutral,sh.shade,sh.mask].filter(Boolean).map(function(u){ var i=new Image(); i.src=u; return i.decode?i.decode().catch(function(){}):Promise.resolve(); })).then(function(){
      if(my!==swap||!st.isConnected) return; var g=ghost(); shape=k; S.shape=k;
      base.src=sh.img; base.alt=sh.alt; neu.src=sh.neutral; T.forEach(function(t){ t.classList.remove("on"); }); st.classList.remove("painted","sweeping"); neuSweep(false); cur=null; front=0; wetMask();
      var c=TZ.color&&TZ.colorTouched?TZ.color:orig(); if(c!==orig()) paint(c,false); else { label(c); cur=c; } updateBar();
      if(g) requestAnimationFrame(function(){ requestAnimationFrame(function(){ g.style.opacity=0; TZ.timers.push(setTimeout(function(){ g.remove(); },460)); }); }); }); }''')

step("D4 başlangıç: fotoğraflar sürüklenmez, ıslak katman maskesi",
     '  if(shape!=="uzun"){ var sh0=SHAPES[shape]; base.src=sh0.img; base.alt=sh0.alt; neu.src=sh0.neutral; }\n',
     '  if(shape!=="uzun"){ var sh0=SHAPES[shape]; base.src=sh0.img; base.alt=sh0.alt; neu.src=sh0.neutral; }\n'
     '  [base,neu].forEach(function(i){ i.draggable=false; }); wetMask();\n')

step("D5 sürükleme: fare seçimi/sürüklemesi engellenir, dikey kaydırma boyamaya dönmez",
     '''  st.addEventListener("pointerdown",function(e){ if(e.target.closest(".palette,.ba-toggle,.zoom-btn,button")) return; drag={x0:e.clientX,id:e.pointerId,on:false}; });
  st.addEventListener("pointermove",function(e){ if(!drag||e.pointerId!==drag.id) return; var r=st.getBoundingClientRect();
    if(!drag.on){ if(Math.abs(e.clientX-drag.x0)<10) return; drag.on=true;''',
     '''  st.addEventListener("pointerdown",function(e){ if(e.target.closest(".palette,.ba-toggle,.zoom-btn,button")) return; if(e.pointerType==="mouse"){ if(e.button) return; e.preventDefault(); } drag={x0:e.clientX,y0:e.clientY,id:e.pointerId,on:false}; });
  st.addEventListener("pointermove",function(e){ if(!drag||e.pointerId!==drag.id) return; var r=st.getBoundingClientRect();
    if(!drag.on){ var dx=Math.abs(e.clientX-drag.x0), dy=Math.abs(e.clientY-drag.y0); if(dy>dx&&dy>8){ drag=null; return; } if(dx<10) return; drag.on=true;''')

# ---------------------------------------------------------------- E. CSS
step("E1 CSS: Renk Atölyesi v3 (seçim mavisi yok, net fırça, ıslak parıltı, telefon paleti)",
     '.tz-side .btn-gold{flex:none;justify-self:start;padding:0 24px}',
     '''.tz-side .btn-gold{flex:none;justify-self:start;padding:0 24px}
/* T2 Renk Atölyesi v3 (2026-10-07) */
.tz-atelier{-webkit-user-select:none;user-select:none;-webkit-touch-callout:none;-webkit-tap-highlight-color:transparent}
.tz-atelier img{-webkit-user-drag:none;pointer-events:none}
.tz-atelier .tz-brush{left:calc(var(--x) * 1.06% - 2.5%);box-shadow:0 0 8px 1px rgba(246,234,203,.85),0 0 30px 7px rgba(201,165,92,.32)}
.tz-wet{position:absolute;inset:0;z-index:4;pointer-events:none;opacity:0;transition:opacity .35s var(--ease);mix-blend-mode:screen;
  background:linear-gradient(90deg,transparent calc(var(--x) * 1.06% - 13%),rgba(255,246,222,.3) calc(var(--x) * 1.06% - 2.5%),transparent calc(var(--x) * 1.06% + .5%));
  -webkit-mask-size:cover;mask-size:cover;-webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat}
.tz-atelier.sweeping .tz-wet{opacity:1}
.tz-ghost{position:absolute;inset:0;z-index:5;pointer-events:none;transition:opacity .42s var(--ease)}
.tz-ghost>*{position:absolute;inset:0;width:100%;height:100%}
.tz-atelier .palette-top{gap:12px;align-items:center;min-width:0}
.tz-atelier .palette-top b{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.tz-atelier .palette-top span{flex:none;text-align:right}
.tz-atelier .palette-top span i{font-style:normal}
@supports (aspect-ratio:1){
  .tz-atelier .sw-row{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:6px;overflow:visible;padding:4px 3px}
  .tz-atelier .sw{width:100%;height:auto;aspect-ratio:1;max-width:42px;justify-self:center}
}
@media (max-width:520px){.tz-atelier .palette-top span i{display:none}.tz-atelier .palette-top b{font-size:20px}}
@media (pointer:coarse){.tz-atelier .ba-toggle button{min-height:36px;padding:9px 12px}}
@media (prefers-reduced-motion:reduce){.tz-wet{display:none}.tz-ghost{transition:none}}''')

# A1/A2: one template each, so the same file name elsewhere is never touched by accident
SCOPED = [
    ("A1 kalıcı oje fiyatları kahramanı: orkide -> süt beyazı (lila)",
     '<template data-tz-page="kalici-oje-fiyatlari">',
     [("tirnak-orkide", "tirnak-lila", 4),
      ("Bordo badem tırnaklar ve beyaz orkide; salonumuzda çekildi",
       "Süt beyazı badem protez tırnak; salonumuzda çekildi", 1)]),
    ("A2 kapanış bandı şablonu: orkide -> baby boomer",
     '<template data-tz-inc-tpl="final">',
     [("tirnak-orkide", "tirnak-babyboomer", 3),
      ("Bordo badem tırnaklar ve beyaz orkide, salonumuzda çekildi",
       "Baby boomer ombre protez tırnak, altın varak; salonumuzda çekildi", 1)]),
]


def main() -> None:
    src, dst = sys.argv[1], sys.argv[2]
    html = open(src, encoding="utf-8").read()
    for name, start, subs in SCOPED:
        i = html.find(start)
        j = html.find("</template>", i)
        assert i >= 0 and j > i, f"{name}: template not found"
        seg = html[i:j]
        for old, new, n in subs:
            got = seg.count(old)
            assert got == n, f"{name}: {old!r} x{got}, expected {n}"
            seg = seg.replace(old, new)
        html = html[:i] + seg + html[j:]
        print(f"ok  {name}")
    for name, old, new, n in STEPS:
        got = html.count(old)
        assert got == n, f"{name}: found x{got}, expected {n}"
        html = html.replace(old, new)
        print(f"ok  {name}")
    assert "tirnak-orkide" not in html, "orkide still referenced"
    assert "-kirmizi-mask.png" not in html, "a v2 mask is still referenced"
    open(dst, "w", encoding="utf-8").write(html)
    print(f"wrote {dst} ({len(html.encode()):,} bytes)")


if __name__ == "__main__":
    main()
