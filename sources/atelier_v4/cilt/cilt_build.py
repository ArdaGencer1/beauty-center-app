# -*- coding: utf-8 -*-
"""Cilt Atlası in the ATELIER prototype: the hub (#cilt) + 24 pages (#cilt/<slug>) on one page engine.

Wave D1 + D2 together: every page has a real-media hero or an honest stand-in (room, device, product, typographic SVG);
pages without own result photos say so in a prototype note and are listed with their shoot item.  D3 = add shoot
media to sources/media_ig_20261007/manifest_cilt.json, rebuild media, point the page's hero/gallery at it, rebuild.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image

import cilt_pages as C

HERE = Path(__file__).resolve().parent
IG = HERE.parents[2] / "website/m/ig"

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
KNOB = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 6l-5 6 5 6M15 6l5 6-5 6"/></svg>'


def tl(p: int) -> str:
    return f"{p:,}".replace(",", ".") + " TL"


def esc(s: str) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def pair_dims() -> dict:
    out = {}
    for slug, size in (("akne-a", 1200), ("akne-b", 1200), ("akne-a", 800), ("akne-b", 800), ("cilt-ters", 480)):
        w, h = Image.open(IG / f"{slug}-once-{size}.webp").size
        out[f"{slug}@{size}"] = [w, h]
    return out


def pair_html(slug: str, size: int, label: str, view: str, intro: bool, cls: str = "") -> str:
    w, h = Image.open(IG / f"{slug}-once-{size}.webp").size
    return (f'<div class="cmp cl-cmp {cls}" data-cl-pair data-intro="{1 if intro else 0}" style="aspect-ratio:{w}/{h}">'
            f'<img class="cmp-b" src="m/ig/{slug}-once-{size}.webp" alt="Önce: {esc(label)}" width="{w}" height="{h}">'
            f'<img class="cmp-a" src="m/ig/{slug}-sonra-{size}.webp" alt="Sonra: {esc(label)}" width="{w}" height="{h}">'
            '<canvas class="dust" data-dust></canvas><div class="cmp-beam"></div><span class="cmp-tag a">Sonra</span><span class="cmp-tag b">Önce</span>'
            f'<button class="cmp-knob" role="slider" aria-label="Önce ve sonra arasında kaydırın" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50" data-track-label="at-{view}-karsilastir">{KNOB}</button></div>')


def atlas_html() -> str:
    out = []
    for g, slugs in C.GROUPS:
        tiles = []
        for s in slugs:
            p = C.P[s]
            if p["type"] == "H":
                o = C.MENU[p["opt"]]
                price = (C.FROM[p["opt"]].split(" · ")[0].split("–")[0] + " TL'den") if p["opt"] in C.FROM else tl(o[1])
            elif p["type"] == "hub":
                price = "Tüm menü"
            else:
                price = "Rehber"
            st = {"tam": "", "ince": '<i class="cl-st ince" title="Gerçek sonuç kanıtı zayıf">◐</i>', "cekim": '<i class="cl-st cekim" title="Gerçek sonuç fotoğrafı çekimde">◌</i>'}[p["status"]]
            tiles.append(f'<a class="cl-tile" href="#cilt/{s}" data-track-label="at-cilt-atlas-sayfa"><img src="{C.THUMB[s]}" alt="" loading="lazy"><span><b>{esc(p["t"])}</b><small>{price}</small></span>{st}</a>')
        out.append(f'<div class="cl-grp"><h3>{esc(g)}</h3><div class="cl-tiles">{"".join(tiles)}</div></div>')
    return "".join(out)


def menu_card(view: str, packages: bool = True) -> str:
    rows = ""
    for g, ids in C.MENU_GROUPS:
        rows += f'<div class="mgroup">{esc(g)}</div>'
        for i in ids:
            n, p, m = C.MENU[i]
            sub = C.FROM.get(i, f"{m} dk" if m else "")
            pr = tl(p) + ("'den" if i in C.FROM else "")
            pk = f' · 5 seans {tl(int(p * 4.5))}' if (packages and i in C.PACKAGE) else ""
            rows += f'<div class="mrow"><span class="nm">{esc(n)}<small>{esc(sub)}{pk}</small></span><span class="ld"></span><span class="pr">{pr}</span></div>'
    return (f'<div class="menu-card"><span class="eyebrow">Cilt bakımı menüsü</span><h3>Fiyatlar</h3>{rows}'
            '<p class="menu-src">Randevu sistemindeki aktif menüden · 7 Ekim 2026 · 5 seanslık paket tek seansın 4,5 katı</p></div>')


def hub() -> str:
    v = "cilt"
    return f'''<section data-view="cilt" hidden>
  <div class="hero">
    <div class="hero-split">
      <div class="hero-media lit cl-hero-media">{pair_html("cilt-ters", 480, "cilt bakımı, kızarıklık ve matlık", v, True, "cl-tall")}</div>
      <div class="hero-copy"><span class="eyebrow" data-personal>Konutkent · Çankaya</span><h1>Ankara Cilt <em>Bakımı</em></h1><p class="lede">Cildiniz ne istiyor? Birlikte bakalım.</p>
        <div class="chips"><span class="chip chip-in"><span class="star">★</span> 4,6 · 263 yorum</span><span class="chip chip-in price" style="animation-delay:.08s">1.000 TL'den</span><span class="chip chip-in" style="animation-delay:.16s" data-slot-chip="cilt"><span class="dot"></span> <span>Bugün müsait</span></span></div>
        <div class="rings" data-rings="cilt"></div>
        <p class="hero-note">Aynı yüz, bakımdan önce ve sonra; salonumuzda çekildi. İki yarıya aynı renk ayarı uygulandı, rötuş yok.</p></div>
    </div>
  </div>

  <div class="sec gutter" id="ciltAtlas">
    <div class="sec-head"><span class="eyebrow">Cilt Atlası</span><h2>Yirmi beş sayfa, <em>bir</em> harita.</h2><p>İhtiyacınızı bulun; her sayfada o bakımın gerçek adımları, süresi ve fiyatı var.</p></div>
    <div class="cl-atlas">{atlas_html()}</div>
    <p class="hero-note cl-legend"><i class="cl-st ince">◐</i> gerçek sonuç fotoğrafı az · <i class="cl-st cekim">◌</i> sonuç fotoğrafı çekimde; şimdilik salonumuzun odası, cihazı ve ürünleri</p>
  </div>

  <div class="sec gutter">
    <div class="quiz" id="quiz">
      <div class="quiz-top"><span class="eyebrow">Cildin ne istiyor?</span><span class="quiz-dots" id="quizDots"><i></i><i></i><i></i></span></div>
      <div id="quizBody"></div>
    </div>
  </div>

  <div class="film cl-film" data-cl-film="cilt-film" data-n="54" data-steps='[["01 · Kubbe","LED kubbe yüzün üzerinde."],["02 · Renk","Işık rengi bakıma göre seçilir."],["03 · Sakinlik","Gözler kapalı, birkaç dakika."]]'>
    <div class="film-stage">
      <div class="film-frame lit">
        <img src="m/ig/cilt-film-poster.webp" alt="LED kubbe yüzün üzerinde, salonumuzda çekildi" width="540" height="960" loading="lazy" class="cl-film-poster">
        <canvas width="540" height="960" aria-hidden="true"></canvas>
        <div class="film-bar"><i></i></div>
        <div class="film-meta"><small data-cl-step-n>01 · Kubbe</small><b data-cl-step>LED kubbe yüzün üzerinde.</b></div>
      </div>
      <div class="film-side"><span class="eyebrow">LED ışık</span><h2 class="display" style="font-size:52px">Kaydırdıkça ışık iner.</h2><p class="muted">Bakımlarımızın son adımı; elde, salonumuzda çekildi.</p></div>
    </div>
  </div>

  <div class="sec gutter">
    <div class="sec-head"><span class="eyebrow">Gerçek sonuçlar</span><h2>Kaydırın, <em>farkı</em> görün.</h2><p>Salonumuzda yapılan bakımlar. İki yarıya aynı renk ayarı uygulandı; etiketler kırpıldı, yüzlere dokunulmadı.</p></div>
    <div class="cl-results">
      <figure>{pair_html("akne-a", 1200, "akne bakımı", v, False)}<figcaption>Akne bakımı · iltihaplı görünümden daha sakin bir cilde</figcaption></figure>
      <figure>{pair_html("akne-b", 1200, "akne bakımı", v, False)}<figcaption>Akne bakımı · yoğun sivilceden hafif kızarıklığa</figcaption></figure>
    </div>
    <a class="cl-men" href="#cilt/klasik-cilt-bakimi" data-track-label="at-cilt-erkek-klasik"><img src="m/ig/cilt-lamba-720.webp" alt="Erkek danışan büyüteç lambası altında bakıma hazırlanıyor" loading="lazy"><span><small>Erkekler de</small><b>Klasik cilt bakımı</b><em>2.000 TL · 90 dk</em></span></a>
  </div>

  <div class="live" data-live="cilt"></div>
  <div class="sec gutter"><div class="invite-teaser"><span class="eyebrow">Randevu davetiyesi</span><h3>Cildiniz için bir saat ayırın.</h3><div class="steps-mini"><span>1 · Bakım</span><span>2 · Gün ve saat</span><span>3 · Davetiye → WhatsApp</span></div><button class="btn-gold shine" data-plan="cilt"><span class="lbl">Davetiyemi hazırla</span>{ARROW}</button></div></div>
  <div class="sec gutter" style="padding-top:0"><div class="sec-head"><span class="eyebrow">Cilt bakımı için yazılanlar</span><h2>“Tertemiz çıktım.”</h2></div></div><div class="reviews" data-reviews="cilt"></div>
  <div class="sec gutter" id="ciltFiyat"><div class="two">
    {menu_card(v)}
    <div><div class="sec-head" style="margin-bottom:16px"><span class="eyebrow">Nasıl geçer</span><h2 style="font-size:40px">Önce bakarız, sonra bakım.</h2></div><ol class="how"><li><div><b>Cildinize bakarız</b><p>Cilt tipiniz, hassasiyetiniz ve şikâyetiniz birlikte değerlendirilir.</p></div></li><li><div><b>Bakımı seçeriz</b><p>Temizlikten ana bakımlara, ihtiyacınıza uygun olan önerilir.</p></div></li><li><div><b>Uygularız</b><p>Seçilen bakıma göre 30 dakikadan iki saate kadar.</p></div></li></ol></div>
  </div></div>
  <div class="sec gutter faq" style="padding-top:0"><div class="sec-head"><span class="eyebrow">Sık sorulanlar</span><h2>Aklınızdakiler</h2></div><details><summary>Hangi bakım bana uygun?</summary><p>Yukarıdaki üç soruluk test bir ön öneri verir. Kesin bakımı uzmanımız cildinize bakarak belirler.</p></details><details><summary>İlk kez yaptıracağım, nereden başlamalıyım?</summary><p>Çoğu danışanımız klasik cilt bakımıyla başlar (90 dk). Kısa bir zamanınız varsa cilt temizliği 30 dakika sürer.</p></details><details><summary>Paket var mı?</summary><p>Ana bakımların 5 seanslık paketleri var; paket, tek seans fiyatının 4,5 katıdır.</p></details></div>
  <div class="sec gutter" data-visit style="padding-top:0"></div>
</section>

<section data-view="cilt-sayfa" hidden>
  <div id="ciltPage"></div>
  <div class="live" data-live="cilt"></div>
  <div class="sec gutter"><div class="invite-teaser"><span class="eyebrow">Randevu davetiyesi</span><h3 data-cl-invite>Cildiniz için bir saat ayırın.</h3><div class="steps-mini"><span>1 · Bakım</span><span>2 · Gün ve saat</span><span>3 · Davetiye → WhatsApp</span></div><button class="btn-gold shine" data-cl-plan data-track-label="at-cilt-sayfa-davetiye"><span class="lbl">Davetiyemi hazırla</span>{ARROW}</button></div></div>
  <div class="sec gutter" style="padding-top:0"><div class="sec-head"><span class="eyebrow">Cilt bakımı için yazılanlar</span><h2>“Tertemiz çıktım.”</h2></div></div><div class="reviews" data-reviews="cilt"></div>
  <div class="sec gutter" data-cl-around></div>
  <div class="sec gutter" data-visit style="padding-top:0"></div>
</section>'''


CSS = r"""
/* ---------- v4 · Cilt Atlası ---------- */
.cl-tall{height:min(82svh,820px);width:auto;max-width:100%;margin:0 auto;justify-self:center}
.cl-hero-media{display:grid;align-content:center}
.cl-atlas{display:grid;gap:22px;grid-template-columns:minmax(0,1fr)}
.cl-grp{min-width:0}
.cl-grp h3{margin:0 0 10px;font:400 26px/1 var(--display)}
.cl-tiles{display:flex;gap:10px;overflow-x:auto;scrollbar-width:none;padding:2px 2px 6px;margin-inline:calc(var(--gutter) * -1);padding-inline:var(--gutter);scroll-snap-type:x proximity}
.cl-tiles::-webkit-scrollbar{display:none}
.cl-tile{position:relative;flex:none;width:148px;border-radius:18px;overflow:hidden;background:var(--velvet);color:#F7F1E4;text-decoration:none;aspect-ratio:3/4;scroll-snap-align:start;box-shadow:var(--shadow)}
.cl-tile img{width:100%;height:100%;object-fit:cover;transition:transform 1s var(--ease)}
.cl-tile:hover img{transform:scale(1.06)}
.cl-tile::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 40%,rgba(14,13,12,.88))}
.cl-tile span{position:absolute;z-index:2;left:10px;right:10px;bottom:10px;display:grid;gap:3px}
.cl-tile b{font:400 20px/1.02 var(--display)}
.cl-tile small{font:600 11px/1.2 var(--body);color:#EBD49A}
.cl-st{position:absolute;z-index:3;top:8px;right:8px;width:22px;height:22px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-size:12px;background:rgba(14,13,12,.55);border:1px dashed rgba(233,215,165,.6);color:#F4E6BE}
.cl-legend .cl-st{position:static;display:inline-grid;vertical-align:middle;background:var(--velvet)}
.cl-results{display:grid;gap:18px}
.cl-results figure{margin:0;display:grid;gap:8px}
.cl-results .cmp{border-radius:20px;box-shadow:var(--shadow)}
.cl-results figcaption{font-size:13px;color:var(--text-2)}
.cl-men{margin-top:18px;display:grid;grid-template-columns:110px 1fr;gap:14px;align-items:center;padding:10px;border-radius:20px;border:1px solid var(--line);background:var(--raised);text-decoration:none;color:var(--text)}
.cl-men img{width:110px;height:137px;border-radius:14px;object-fit:cover}
.cl-men span{display:grid;gap:4px}.cl-men small{font:600 10px/1 var(--body);letter-spacing:.2em;text-transform:uppercase;color:var(--gold-ink)}
.cl-men b{font:400 26px/1 var(--display)}.cl-men em{font-style:normal;font-size:13px;color:var(--text-2)}
.cl-film .film-frame{aspect-ratio:540/960}
/* page */
.cl-hero{padding-top:calc(var(--nav-h) + env(safe-area-inset-top,0px))}
.cl-hmedia{position:relative;overflow:hidden;background:#1a1612;aspect-ratio:4/5;max-height:calc(100svh - var(--nav-h) - 40px);width:100%}
.cl-hmedia video,.cl-hmedia>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.cl-hmedia.wide{aspect-ratio:auto;max-height:none;background:none}
.cl-hmedia.wide .cmp{position:relative}
.cl-hmedia.tall{aspect-ratio:auto;display:grid;max-height:none;background:none}
.cl-hmedia.tall .cmp{position:relative;inset:auto}
.cl-kb{transform-origin:55% 45%}
html[data-tier="A"] .cl-kb,html[data-tier="B"] .cl-kb{animation:kb 16s ease-in-out infinite alternate}
.cl-type{position:absolute;inset:0;display:grid;place-items:center;background:radial-gradient(70% 55% at 50% 45%,rgba(201,165,92,.22),transparent 70%),var(--velvet)}
.cl-type svg{width:72%;max-width:420px;height:auto;overflow:visible}
.cl-type .ln{fill:none;stroke:url(#clGold);stroke-width:2.2;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1;animation:drawl 2.4s var(--ease) .3s forwards;filter:drop-shadow(0 0 6px rgba(244,230,190,.6))}
html[data-tier="C"] .cl-type .ln{animation:none;stroke-dashoffset:0}
.cl-badges{display:flex;flex-wrap:wrap;gap:6px}
.proto-note{display:inline-flex;align-items:center;gap:6px;font:600 10.5px/1.3 var(--body);letter-spacing:.06em;color:var(--gold-ink);padding:6px 10px;border-radius:12px;border:1px dashed var(--line-strong);background:transparent}
.cl-kicker{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.cl-kicker .eyebrow{margin-right:4px}
.cl-scene{display:grid;gap:18px}
.cl-tl{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;margin-inline:calc(var(--gutter) * -1);padding:4px var(--gutter) 10px;counter-reset:t}
.cl-tl::-webkit-scrollbar{display:none}
.cl-step{flex:none;width:min(64vw,250px);scroll-snap-align:start;display:grid;gap:10px;margin:0}
.cl-step .m{position:relative;aspect-ratio:9/14;border-radius:20px;overflow:hidden;background:#1a1612;box-shadow:var(--shadow)}
.cl-step .m video,.cl-step .m img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.cl-step .m::before{counter-increment:t;content:counter(t,decimal-leading-zero);position:absolute;z-index:2;top:10px;left:10px;font:600 11px/1 var(--body);letter-spacing:.2em;color:#F4E6BE;padding:6px 8px;border-radius:999px;background:rgba(14,13,12,.45);border:1px solid rgba(233,215,165,.4)}
.cl-step b{font:400 24px/1.05 var(--display)}
.cl-step p{margin:0;font-size:14px;color:var(--text-2)}
.cl-total{font:italic 500 22px/1.2 var(--display);color:var(--gold-ink)}
.cl-band{display:grid;gap:22px;align-items:center}
.cl-band .led-frame{justify-self:center}
.cl-pick{display:grid;gap:14px;border-radius:26px;padding:22px 18px;background:var(--raised);border:1px solid var(--line);box-shadow:var(--shadow)}
.cl-opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(96px,1fr));gap:8px}
.cl-opts button{display:grid;gap:4px;justify-items:center;padding:14px 8px;border-radius:16px;border:1px solid var(--line-strong);background:var(--ground);cursor:pointer;font:500 14px/1.1 var(--body)}
.cl-opts button b{font:500 22px/1 var(--display)}
.cl-opts button[aria-pressed="true"]{border-color:var(--gold);box-shadow:0 0 0 1px var(--gold),0 10px 30px -14px rgba(156,122,53,.6)}
.cl-sum{font:italic 500 22px/1.2 var(--display);color:var(--gold-ink)}
.cl-pick .btn-gold{flex:none;width:100%}
.cl-paths{display:grid;gap:10px}
.cl-path{display:grid;grid-template-columns:92px 1fr auto;gap:14px;align-items:center;padding:10px;border-radius:18px;border:1px solid var(--line);background:var(--raised);text-decoration:none;color:var(--text)}
.cl-path img{width:92px;height:92px;border-radius:12px;object-fit:cover}
.cl-path span{display:grid;gap:3px}.cl-path small{font:600 10px/1.2 var(--body);letter-spacing:.16em;text-transform:uppercase;color:var(--gold-ink)}
.cl-path b{font:400 23px/1.05 var(--display)}.cl-path em{font-style:normal;font-size:13px;color:var(--text-2)}
.cl-path svg{width:18px;height:18px;color:var(--gold-ink)}
.cl-face{display:grid;gap:16px}
.cl-face svg{width:min(100%,340px);justify-self:center;height:auto}
.cl-zone{fill:rgba(201,165,92,.08);stroke:rgba(201,165,92,.55);stroke-width:1.2;stroke-dasharray:3 3;cursor:pointer;transition:fill .3s}
.cl-zone:hover{fill:rgba(201,165,92,.2)}
.cl-zone[aria-pressed="true"]{fill:rgba(244,230,190,.45);stroke:#C9A55C;stroke-dasharray:none}
.cl-faceout{fill:none;stroke:var(--line-strong);stroke-width:1.4}
.cl-zl{font:600 10px var(--body);letter-spacing:.14em;fill:var(--gold-ink);pointer-events:none;text-transform:uppercase}
.cl-faceres{display:grid;gap:10px;padding:18px;border-radius:22px;border:1px solid var(--line);background:var(--raised)}
.cl-faceres b{font:400 26px/1.05 var(--display)}
.cl-duel{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.cl-dcard{display:grid;gap:8px;align-content:start;padding:18px 14px;border-radius:22px;border:1px solid var(--line);background:var(--raised);text-decoration:none;color:var(--text)}
.cl-dcard.on{border-color:var(--gold);box-shadow:0 0 0 1px rgba(201,165,92,.4),var(--shadow)}
.cl-dcard b{font:400 26px/1.02 var(--display)}
.cl-dcard dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:4px 10px;font-size:13.5px}
.cl-dcard dt{color:var(--text-3)}.cl-dcard dd{margin:0}
.cl-heads{position:relative;border-radius:22px;overflow:hidden;aspect-ratio:4/5;max-height:76svh;justify-self:center;width:min(100%,520px);box-shadow:var(--shadow)}
.cl-heads img{width:100%;height:100%;object-fit:cover}
.cl-hot{position:absolute;width:34px;height:34px;margin:-17px 0 0 -17px;border-radius:50%;border:0;background:transparent;cursor:pointer;padding:0}
.cl-hot i{position:absolute;inset:9px;border-radius:50%;background:#F4E6BE;box-shadow:0 0 0 3px rgba(201,165,92,.55),0 0 14px rgba(244,230,190,.9)}
.cl-hot i::after{content:"";position:absolute;inset:-9px;border-radius:50%;border:1.5px solid #F4E6BE;animation:pulse 2.2s var(--ease) infinite}
.cl-hot[aria-pressed="true"] i{background:#C9A55C}
.cl-hotcard{padding:16px;border-radius:18px;border:1px solid var(--line);background:var(--raised);display:grid;gap:4px}
.cl-hotcard b{font:400 24px/1.05 var(--display)}.cl-hotcard p{margin:0;color:var(--text-2);font-size:14px}
.cl-pkg{display:grid;gap:12px;padding:20px 18px;border-radius:24px;border:1px solid var(--line);background:var(--raised);box-shadow:var(--shadow)}
.cl-pkg select{height:46px;border-radius:14px;border:1px solid var(--line-strong);background:var(--ground);color:var(--text);font:500 15px var(--body);padding:0 12px}
.cl-pkgrow{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;text-align:center}
.cl-pkgrow div{padding:12px 6px;border-radius:14px;border:1px solid var(--line)}
.cl-pkgrow b{display:block;font:500 22px/1 var(--display)}.cl-pkgrow small{font-size:11.5px;color:var(--text-3)}
.cl-filter{display:flex;gap:6px;flex-wrap:wrap}
.cl-filter button{height:36px;padding:0 12px;border-radius:999px;border:1px solid var(--line-strong);background:transparent;cursor:pointer;font:500 13px var(--body)}
.cl-filter button[aria-pressed="true"]{background:var(--text);color:var(--ground);border-color:var(--text)}
.cl-menu .mrow[hidden]{display:none}
.cl-gal{display:grid;gap:14px}
.cl-gal figure{margin:0;display:grid;gap:6px}.cl-gal figcaption{font-size:13px;color:var(--text-2)}
.cl-gal .cmp,.cl-gal video,.cl-gal img{border-radius:20px;width:100%;display:block;box-shadow:var(--shadow)}
.cl-gal video,.cl-gal img{aspect-ratio:4/5;object-fit:cover}
.cl-around{display:flex;gap:8px;flex-wrap:wrap}
.cl-around a{height:40px;padding:0 14px;border-radius:999px;border:1px solid var(--line-strong);display:inline-flex;align-items:center;text-decoration:none;font:500 13.5px var(--body);color:var(--text)}
.cl-around a.here{background:var(--text);color:var(--ground)}
@media (min-width:960px){
  .cl-tiles{flex-wrap:wrap;overflow:visible;margin:0;padding:0}
  .cl-tile{width:180px}
  .cl-results{grid-template-columns:1fr 1fr}
  .cl-hero .hero-split{min-height:calc(100svh - var(--nav-h))}
  .cl-hmedia{height:calc(100svh - var(--nav-h));max-height:none;aspect-ratio:auto}
  .cl-hmedia.wide{height:auto;align-self:center;padding:0 0 0 48px}
  .cl-hmedia.tall{height:calc(100svh - var(--nav-h))}
  .cl-hmedia.tall .cmp{height:calc(100svh - var(--nav-h) - 40px);justify-self:center;align-self:center}
  .cl-band{grid-template-columns:auto 1fr;gap:48px}
  .cl-face,.cl-scene.two-col{grid-template-columns:1fr 1fr;align-items:center}
  .cl-gal{grid-template-columns:repeat(2,1fr)}
  .cl-step{width:230px}
  .cl-paths{grid-template-columns:repeat(2,1fr)}
}
"""

JS = r"""
/* ---------- v4 · Cilt Atlası: page engine ---------- */
var CILT=__CILT__;
var CL_ICON={arrow:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',knob:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 6l-5 6 5 6M15 6l5 6-5 6"/></svg>'};
function clEsc(s){ return String(s).replace(/[&<>"]/g,function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); }
function clTL(p){ return p.toLocaleString("tr-TR")+" TL"; }
function clLbl(slug,place){ return "at-cilt-"+slug.replace(/-bakimi$/,"").replace(/[^a-z0-9-]/g,"").slice(0,24)+"-"+place; }
function clVideo(slug,alt,cls){ return '<video class="auto-vid '+(cls||"")+'" muted playsinline loop preload="none" poster="m/ig/'+slug+'-poster.webp" data-src="m/ig/'+slug+'.mp4" aria-label="'+clEsc(alt||CILT.alt[slug]||"Salonumuzda çekildi")+'"></video>'; }
function clPair(slug,size,label,s,intro,cls){ var d=CILT.dims[slug+"@"+size]; return '<div class="cmp cl-cmp '+(cls||"")+'" data-cl-pair data-intro="'+(intro?1:0)+'" style="aspect-ratio:'+d[0]+'/'+d[1]+'"><img class="cmp-b" src="m/ig/'+slug+'-once-'+size+'.webp" alt="Önce: '+clEsc(label)+'" width="'+d[0]+'" height="'+d[1]+'"><img class="cmp-a" src="m/ig/'+slug+'-sonra-'+size+'.webp" alt="Sonra: '+clEsc(label)+'" width="'+d[0]+'" height="'+d[1]+'"><canvas class="dust" data-dust></canvas><div class="cmp-beam"></div><span class="cmp-tag a">Sonra</span><span class="cmp-tag b">Önce</span><button class="cmp-knob" role="slider" aria-label="Önce ve sonra arasında kaydırın" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50" data-track-label="'+clLbl(s,"karsilastir")+'">'+CL_ICON.knob+'</button></div>'; }
function clMedia(m,s,alt){ if(m.video) return clVideo(m.video,alt); if(m.img) return '<img src="'+m.img+'" alt="'+clEsc(alt||m.alt||"")+'" loading="lazy">'; return ""; }
function clPrice(pg){ if(pg.type!=="H") return null; var o=CILT.menu[pg.opt]; return {from:!!CILT.from[pg.opt],p:o[1],m:o[2],range:CILT.from[pg.opt]||null}; }
function clTypeSvg(k){
  var G='<defs><linearGradient id="clGold" x1="0" x2="1"><stop offset="0" stop-color="#9C7A35"/><stop offset=".5" stop-color="#F6EACB"/><stop offset="1" stop-color="#C9A55C"/></linearGradient></defs>';
  if(k==="dudak") return '<svg viewBox="0 0 300 140" aria-hidden="true">'+G+'<path class="ln" pathLength="1" d="M20 70 C60 30 110 22 150 48 C190 22 240 30 280 70 C240 112 190 128 150 128 C110 128 60 112 20 70Z"/><path class="ln" pathLength="1" d="M20 70 C80 82 120 80 150 76 C180 80 220 82 280 70" style="animation-delay:.9s"/></svg>';
  if(k==="sirt") return '<svg viewBox="0 0 240 300" aria-hidden="true">'+G+'<path class="ln" pathLength="1" d="M120 20 C104 20 98 34 100 48 C70 56 46 66 34 92 C26 120 34 190 46 280 M120 20 C136 20 142 34 140 48 C170 56 194 66 206 92 C214 120 206 190 194 280"/><path class="ln" pathLength="1" d="M120 60 L120 270" style="animation-delay:.8s;stroke-dasharray:1"/><path class="ln" pathLength="1" d="M60 120 C90 132 150 132 180 120" style="animation-delay:1.2s"/></svg>';
  return '<svg viewBox="0 0 300 160" aria-hidden="true">'+G+'<path class="ln" pathLength="1" d="M20 90 Q150 0 280 90 Q150 160 20 90Z"/><circle class="ln" pathLength="1" cx="150" cy="86" r="32" style="animation-delay:.8s"/><path class="ln" pathLength="1" d="M40 60 Q150 -6 262 54" style="animation-delay:1.3s"/></svg>'; }
function clHero(s,pg){ var h=pg.hero, cls="", inner="";
  if(h.pair){ cls=h.size===480?" tall":" wide"; inner=clPair(h.pair,h.size,pg.t,s,true,h.size===480?"cl-tall":""); }
  else if(h.video){ inner=clVideo(h.video); }
  else if(h.img){ inner='<img class="cl-kb" src="'+h.img+'" alt="'+clEsc(h.alt||pg.t)+'" fetchpriority="high">'; }
  else if(h.type){ inner='<div class="cl-type" role="img" aria-label="'+clEsc(pg.t)+' (temsili çizim)">'+clTypeSvg(h.type)+'<canvas class="dust" data-dust></canvas></div>'; }
  var pr=clPrice(pg), chip=pr?(pr.range?pr.range.split(" · ")[0].split("–")[0]+" TL'den":clTL(pr.p)+(pr.m?" · "+pr.m+" dk":"")):(pg.type==="hub"?pg.chip:"Önce ön görüşme");
  var badge=pg.status==="cekim"?'<span class="proto-note">Prototip notu · sonuç fotoğrafı çekimde: '+clEsc(pg.cekim||"")+'</span>':(pg.status==="ince"?'<span class="proto-note">Prototip notu · gerçek sonuç kanıtı zayıf'+(pg.cekim?": "+clEsc(pg.cekim):"")+'</span>':"");
  var kind=pg.type==="H"?"Hizmet":(pg.type==="İ"?"Rehber":"Menü");
  return '<div class="hero cl-hero"><div class="hero-split"><div class="hero-media lit cl-hmedia'+cls+'">'+inner+'</div><div class="hero-copy">'+
    '<div class="cl-kicker"><span class="eyebrow">Cilt Atlası · '+kind+'</span></div><h1>'+pg.h1+'</h1><p class="lede">'+clEsc(pg.lede)+'</p>'+
    '<div class="chips"><span class="chip chip-in"><span class="star">★</span> 4,6 · 263 yorum</span><span class="chip chip-in price" style="animation-delay:.08s">'+chip+'</span><span class="chip chip-in" style="animation-delay:.16s" data-cl-slot><span class="dot"></span> <span>Bugün müsait</span></span></div>'+
    '<div class="rings" data-cl-rings></div>'+(badge?'<div class="cl-badges">'+badge+'</div>':'')+
    (h.pair?'<p class="hero-note">'+clEsc(pg.pairnote||"Aynı yüz, bakımdan önce ve sonra; salonumuzda çekildi.")+'</p>':(h.type?'<p class="hero-note">Temsili çizim. Bu sayfanın gerçek sonuç fotoğrafları çekimde.</p>':'<p class="hero-note">'+(h.video?"Video salonumuzda çekildi.":"Fotoğraf salonumuzdan.")+'</p>'))+
    '</div></div></div>'; }
function clHead(e,h,p){ return '<div class="sec-head"><span class="eyebrow">'+e+'</span><h2>'+h+'</h2>'+(p?'<p>'+p+'</p>':'')+'</div>'; }
function clPathCard(s,why,from){ var pg=CILT.pages[s], pr=clPrice(pg); return '<a class="cl-path" href="#cilt/'+s+'" data-track-label="'+clLbl(from,"yol")+'"><img src="'+CILT.thumb[s]+'" alt="" loading="lazy"><span><small>'+clEsc(why)+'</small><b>'+clEsc(pg.t)+'</b><em>'+(pr?(pr.range||clTL(pr.p)+(pr.m?" · "+pr.m+" dk":"")):"Rehber sayfa")+'</em></span>'+CL_ICON.arrow+'</a>'; }
var CL_FACE=[["alin","Alın",'M70 40 C100 22 160 22 190 40 L190 78 L70 78Z',"Matlık, ince çizgi görünümü",["saten-yuz-germe","cilt-yenileme"]],
  ["goz","Göz çevresi",'M64 86 L120 86 L120 112 L64 112Z M140 86 L196 86 L196 112 L140 112Z',"Yorgun görünüm",["goz-cevresi-bakimi","saten-yuz-germe"]],
  ["burun","Burun",'M116 112 L144 112 L150 160 L110 160Z',"Siyah nokta, gözenek",["cilt-temizligi","klasik-cilt-bakimi"]],
  ["yanak","Yanaklar",'M56 118 L106 118 L104 176 L64 170Z M154 118 L204 118 L196 170 L156 176Z',"Kızarıklık, ton farkı, sivilce",["ton-esitleme","akne-bakimi","hassas-cilt"]],
  ["dudak","Dudak",'M106 178 L154 178 L150 198 L110 198Z',"Kuruluk, pürüz",["dudak-bakimi"]],
  ["cene","Çene",'M84 204 L176 204 C166 236 150 250 130 252 C110 250 94 236 84 204Z',"Sivilce görünümü",["akne-bakimi","klasik-cilt-bakimi"]]];
function clScene(s,pg){ var h="";
  if(pg.scene==="timeline"){ var tot=pg.opt?CILT.menu[pg.opt][2]:null;
    h='<div class="sec gutter">'+clHead("Adım adım",(tot?tot+" dakika, ":"")+"<em>"+pg.timeline.length+"</em> adım.","Hepsi salonumuzda çekilmiş gerçek uygulamalar. Kaydırın.")+
      '<div class="cl-tl">'+pg.timeline.map(function(t){ return '<figure class="cl-step"><div class="m">'+clMedia(t[2],s,t[0])+'</div><b>'+clEsc(t[0])+'</b><p>'+clEsc(t[1])+'</p></figure>'; }).join("")+'</div>'+
      (pg.note?'<p class="hero-note">'+clEsc(pg.note)+'</p>':'')+'</div>'; }
  else if(pg.scene==="band"){ var b=pg.band; h='<div class="sec dark-band gutter"><div class="cl-band"><div class="led-frame lit">'+clVideo(b.video)+'</div><div class="sec-head" style="margin:0"><span class="eyebrow">'+b.eyebrow+'</span><h2>'+b.h+'</h2><p>'+clEsc(b.p)+'</p><div class="golden-actions"><button class="btn-gold" style="flex:none;padding:0 22px" data-cl-plan data-track-label="'+clLbl(s,"bant-davetiye")+'"><span class="lbl">Bu bakım için saat seç</span>'+CL_ICON.arrow+'</button></div></div></div></div>'; }
  else if(pg.scene==="picker"){ var k=pg.picker; h='<div class="sec gutter"><div class="cl-pick" data-cl-picker>'+clHead(k.eyebrow,k.h,clEsc(k.p))+
      '<div class="cl-opts" role="group" aria-label="'+clEsc(k.eyebrow)+'">'+k.opts.map(function(o,i){ return '<button data-cl-opt="'+o[0]+'" data-p="'+o[2]+'" data-n="'+clEsc(o[1])+'" aria-pressed="'+(i===0)+'" data-track-label="'+clLbl(s,"secim")+'"><span>'+clEsc(o[1])+'</span><b>'+clTL(o[2])+(k.from?"'den":"")+'</b></button>'; }).join("")+'</div>'+
      '<div class="cl-sum" data-cl-sum></div><button class="btn-gold shine" data-cl-pickplan data-track-label="'+clLbl(s,"secim-davetiye")+'"><span class="lbl">Bu seçenekle saat seç</span>'+CL_ICON.arrow+'</button></div></div>'; }
  else if(pg.scene==="film"){ var f=pg.film; h='<div class="film cl-film" data-cl-film="'+f.set+'" data-n="'+f.n+'" data-steps=\''+JSON.stringify(f.steps).replace(/'/g,"&#39;")+'\'><div class="film-stage"><div class="film-frame lit"><img src="m/ig/'+(pg.hero.video||"cilt-saten")+'-poster.webp" alt="" class="cl-film-poster" loading="lazy"><canvas width="540" height="960" aria-hidden="true"></canvas><div class="film-bar"><i></i></div><div class="film-meta"><small data-cl-step-n>'+f.steps[0][0]+'</small><b data-cl-step>'+f.steps[0][1]+'</b></div></div><div class="film-side"><span class="eyebrow">Kaydırmalı film</span><h2 class="display" style="font-size:52px">Başlığı izleyin.</h2><p class="muted">Tek bir uygulama, salonumuzda çekildi.</p></div></div></div>'; }
  else if(pg.scene==="paths"){ h='<div class="sec gutter">'+clHead("Size uygun yol",pg.type==="İ"?"Bu ihtiyaç için <em>gerçek</em> bakımlar.":"Benzer <em>bakımlar</em>.",pg.type==="İ"?"Bu sayfanın kendi menü kalemi yok; fiyatlar ilgili bakımın kendi fiyatıdır.":"")+'<div class="cl-paths">'+pg.paths.map(function(p){ return clPathCard(p[0],p[1],s); }).join("")+'</div></div>'; }
  else if(pg.scene==="facemap"){ h='<div class="sec gutter"><div class="cl-face">'+
      '<svg viewBox="0 0 260 280" role="group" aria-label="Yüz haritası"><path class="cl-faceout" d="M130 14 C190 14 214 64 214 120 C214 196 178 262 130 266 C82 262 46 196 46 120 C46 64 70 14 130 14Z"/>'+
      CL_FACE.map(function(z){ return '<path class="cl-zone" d="'+z[2]+'" data-cl-zone="'+z[0]+'" tabindex="0" role="button" aria-pressed="false" aria-label="'+z[1]+'" data-track-label="'+clLbl(s,"yuz-bolge")+'"/>'; }).join("")+
      '<text class="cl-zl" x="130" y="62" text-anchor="middle">Alın</text><text class="cl-zl" x="130" y="140" text-anchor="middle">Burun</text><text class="cl-zl" x="130" y="232" text-anchor="middle">Çene</text></svg>'+
      '<div>'+clHead("Yüz haritası","Bölgeye <em>dokunun</em>.","Hangi bölge sizi rahatsız ediyorsa ona dokunun; uygun sayfayı önerelim.")+'<div class="cl-faceres" data-cl-faceres><b>Bir bölge seçin</b><p class="muted" style="margin:0">Analiz randevusunda bu bölgeye birlikte bakarız.</p></div></div></div></div>'; }
  else if(pg.scene==="duel"){ var A=["hollywood-bakimi","paris-isiltisi-bakimi"]; h='<div class="sec gutter">'+clHead("Işıltı düellosu","Hollywood mu, <em>Paris</em> mi?","İkisi de iki saatlik ana bakım. Farkı içerik ve adımlarda; ön görüşmede uzmanımız anlatır.")+
      '<div class="cl-duel">'+A.map(function(x){ var p=CILT.pages[x], o=CILT.menu[p.opt]; return '<a class="cl-dcard'+(x===s?" on":"")+'" href="#cilt/'+x+'" data-track-label="'+clLbl(s,"duello")+'"><span class="eyebrow">'+(x===s?"Bu sayfa":"Karşılaştır")+'</span><b>'+clEsc(p.t)+'</b><dl><dt>Süre</dt><dd>'+o[2]+' dk</dd><dt>Tek seans</dt><dd>'+clTL(o[1])+'</dd><dt>5 seans</dt><dd>'+clTL(o[1]*4.5)+'</dd></dl></a>'; }).join("")+'</div>'+
      '<p class="hero-note"><span class="proto-note">Prototip notu · içerik farkı sahibine soruldu</span></p></div>'; }
  else if(pg.scene==="heads"){ var HS=[["kubbe",40,12,"LED kubbe","Bakımın sonunda yüzün üzerine iner."],["baslik",46,36,"8 uygulama başlığı","Başlıklar cildinize göre seçilir; uzmanınız seansta gösterir."],["ekran",50,66,"Dokunmatik ekran","Süre ve ayar buradan seçilir."],["hazne",78,95,"Ürün hazneleri","Renkli etiketli hazneler; içerikleri bakıma göre değişir."]];
    h='<div class="sec gutter"><div class="cl-scene two-col"><div class="cl-heads"><img src="m/ig/cilt-cihaz-720.webp" alt="Salonumuzdaki 8 başlıklı cilt bakım cihazı" loading="lazy">'+HS.map(function(x,i){ return '<button class="cl-hot" style="left:'+x[1]+'%;top:'+x[2]+'%" data-cl-hot="'+i+'" aria-label="'+x[3]+'" aria-pressed="'+(i===1)+'" data-track-label="'+clLbl(s,"cihaz-nokta")+'"><i></i></button>'; }).join("")+'</div>'+
      '<div>'+clHead("Cihazımız","Noktalara <em>dokunun</em>.","Fotoğraf salonumuzdaki cihazdan.")+'<div class="cl-hotcard" data-cl-hotcard><b>'+HS[1][3]+'</b><p>'+HS[1][4]+'</p></div>'+(pg.paths?'<div class="cl-paths" style="margin-top:14px">'+pg.paths.map(function(p){ return clPathCard(p[0],p[1],s); }).join("")+'</div>':'')+'</div></div></div>'; window.__clHS=HS; }
  else if(pg.scene==="proof"){ var pf=pg.proof; h='<div class="sec gutter">'+clHead("Dürüst kanıt","Ton farkına <em>gerçek</em> bir örnek.","Leke bakımının kendi önce/sonra fotoğrafı çekimde. Bu fotoğraf ton eşitleme sonrası; öyle etiketledik.")+'<figure class="cl-proof" style="margin:0;display:grid;gap:8px;justify-items:center">'+clPair(pf.pair,pf.size,pf.label,s,false,"cl-tall")+'<figcaption class="hero-note">'+clEsc(pf.label)+'</figcaption></figure></div>'; }
  else if(pg.scene==="menu"){ var opts=Object.keys(CILT.menu).filter(function(k){ return CILT.pkg.indexOf(k)>=0; });
    h='<div class="sec gutter"><div class="two"><div class="cl-menu">'+clHead("Bakım menüsü","Süreye ya da <em>ihtiyaca</em> göre.","")+
      '<div class="cl-filter" role="group" aria-label="Süre">'+[["","Tümü"],["30","30 dk"],["60","60 dk"],["90","90 dk"],["120","120 dk"]].map(function(f,i){ return '<button data-cl-min="'+f[0]+'" aria-pressed="'+(i===0)+'" data-track-label="'+clLbl(s,"filtre")+'">'+f[1]+'</button>'; }).join("")+'</div>'+
      '<div class="menu-card" style="margin-top:12px" data-cl-menucard>'+CILT.menuHtml+'</div></div>'+
      '<div class="cl-pkg">'+clHead("Paket hesabı","Beş seans, <em>dört buçuk</em> fiyatına.","Ana bakımlarda 5 seanslık paket, tek seans fiyatının 4,5 katıdır.")+
      '<select data-cl-pkg aria-label="Ana bakım" data-track-label="'+clLbl(s,"paket-sec")+'">'+opts.map(function(k){ return '<option value="'+k+'">'+CILT.menu[k][0]+'</option>'; }).join("")+'</select>'+
      '<div class="cl-pkgrow"><div><b data-cl-p1></b><small>tek seans</small></div><div><b data-cl-p5></b><small>5 seans paket</small></div><div><b data-cl-pe></b><small>seans başına</small></div></div>'+
      '<button class="btn-gold shine" data-cl-pkgplan data-track-label="'+clLbl(s,"paket-davetiye")+'"><span class="lbl">Bu bakım için saat seç</span>'+CL_ICON.arrow+'</button></div></div></div>'; }
  return h; }
function clGallery(s,pg){ if(!pg.gallery.length) return ""; return '<div class="sec gutter">'+clHead("Salonumuzda","Gerçek <em>uygulamalar</em>.","")+'<div class="cl-gal">'+pg.gallery.map(function(g){
    if(g[0]==="pair") return '<figure>'+clPair(g[1],1200,g[2],s,false)+'<figcaption>'+clEsc(g[2])+'</figcaption></figure>';
    if(g[0]==="video") return '<figure>'+clVideo(g[1],g[2])+'<figcaption>'+clEsc(g[2])+'</figcaption></figure>';
    return '<figure><img src="'+g[1]+'" alt="'+clEsc(g[2])+'" loading="lazy"><figcaption>'+clEsc(g[2])+'</figcaption></figure>'; }).join("")+'</div></div>'; }
function clHow(s,pg){ var how=CILT.how[pg.type==="H"?"H":"İ"], pr=clPrice(pg);
  var price=pr?'<div class="menu-card"><span class="eyebrow">'+clEsc(pg.t)+'</span><h3>Fiyat</h3>'+(pr.range?'<div class="mrow"><span class="nm">'+clEsc(CILT.menu[pg.opt][0])+'<small>'+clEsc(pr.range)+'</small></span><span class="ld"></span><span class="pr">'+clTL(pr.p)+"'den</span></div>":'<div class="mrow"><span class="nm">Tek seans<small>'+(pr.m?pr.m+" dk":"")+'</small></span><span class="ld"></span><span class="pr">'+clTL(pr.p)+'</span></div>'+(CILT.pkg.indexOf(pg.opt)>=0?'<div class="mrow"><span class="nm">5 seans paket<small>tek seansın 4,5 katı</small></span><span class="ld"></span><span class="pr">'+clTL(pr.p*4.5)+'</span></div>':''))+'<p class="menu-src">Randevu sistemindeki aktif menüden · 7 Ekim 2026</p></div>':
    '<div class="menu-card"><span class="eyebrow">'+clEsc(pg.t)+'</span><h3>Fiyat</h3><p class="muted" style="text-align:center;margin:0">Bu bir rehber sayfa; kendi menü kalemi yok. Uygun bakımı ön görüşmede seçeriz, fiyat o bakımın fiyatıdır.</p><p class="menu-src"><a href="#cilt/cilt-bakimi-fiyatlari" data-track-label="'+clLbl(s,"fiyatlar")+'">Tüm cilt menüsü →</a></p></div>';
  var faq=pg.faq.length?'<div class="faq" style="margin-top:22px">'+pg.faq.map(function(q){ return '<details><summary data-track-label="'+clLbl(s,"sss")+'">'+clEsc(q[0])+'</summary><p>'+clEsc(q[1])+'</p></details>'; }).join("")+'</div>':"";
  return '<div class="sec gutter"><div class="two">'+price+'<div><div class="sec-head" style="margin-bottom:16px"><span class="eyebrow">Nasıl geçer</span><h2 style="font-size:40px">Üç adım.</h2></div><ol class="how">'+how.map(function(x){ return '<li><div><b>'+clEsc(x[0])+'</b><p>'+clEsc(x[1])+'</p></div></li>'; }).join("")+'</ol>'+faq+'</div></div></div>'; }
function clAround(s){ var g=CILT.groups.filter(function(x){ return x[1].indexOf(s)>=0; })[0]; if(!g) return "";
  return clHead("Cilt Atlası · "+g[0],"Yakın <em>sayfalar</em>.","")+'<div class="cl-around">'+g[1].map(function(x){ return '<a href="#cilt/'+x+'" class="'+(x===s?"here":"")+'" data-track-label="'+clLbl(s,"atlas")+'">'+clEsc(CILT.pages[x].t)+'</a>'; }).join("")+'<a href="#cilt/atlas" data-track-label="'+clLbl(s,"atlas-tumu")+'">Tüm atlas →</a></div>'; }
function clRings(box){ STORIES.cilt.forEach(function(st,i){ var b=document.createElement("button"); b.className="ring"; b.innerHTML='<i><img src="'+st.th+'" alt="" loading="lazy"></i><span>'+st.t+'</span>'; lbl(b,"at-cilt-hikaye"); b.addEventListener("click",function(){ openStory("cilt",i); }); box.appendChild(b); }); }
function clFilm(sec){ var cv=$("canvas",sec), ctx=cv.getContext("2d"), bar=$(".film-bar i",sec), N=+sec.dataset.n, FA=atlas(sec.dataset.clFilm,N,540,960), cur=-1, view=sec.closest("[data-view]").dataset.view, steps=JSON.parse(sec.dataset.steps), route=S.route;
  cv.style.opacity=0; function draw(i){ if(!FA.draw(ctx,i,cv.width,cv.height)) return; cv.style.opacity=1; cur=i; }
  new IntersectionObserver(function(es){ if(es[0].isIntersecting && S.tier!=="C") FA.load(function(){ if(cur<0) draw(0); }); },{rootMargin:"600px"}).observe(sec);
  function update(){ if(!sec.isConnected||S.view!==view||S.tier==="C") return; var r=sec.getBoundingClientRect(), vh=innerHeight; if(r.bottom<0||r.top>vh) return;
    var p=Math.min(1,Math.max(0,-r.top/(r.height-vh))), i=Math.min(N-1,Math.round(p*(N-1))); bar.style.width=(p*100).toFixed(1)+"%"; if(i!==cur) draw(i);
    var k=Math.min(steps.length-1,Math.floor(p*steps.length)); var n=$("[data-cl-step-n]",sec); if(n.textContent!==steps[k][0]){ n.textContent=steps[k][0]; $("[data-cl-step]",sec).textContent=steps[k][1]; } }
  scrollers.push(update); }
function clBind(root,s,pg){
  $$("[data-cl-pair]",root).forEach(function(el){ initCompare(el,el.dataset.intro==="1"); });
  initAutoVids(root); $$("[data-dust]",root).forEach(initDust); $$("[data-cl-film]",root).forEach(clFilm);
  var rb=$("[data-cl-rings]",root); if(rb) clRings(rb);
  var sc=$("[data-cl-slot]",root); if(sc){ var sl=sampleSlots("cilt")[0]; $("span:last-child",sc).textContent=sl?(sl.label+" "+sl.times[0]+" müsait"):"Saat için yazın"; }
  $$("[data-cl-plan]",root).forEach(function(b){ b.addEventListener("click",function(){ openPlanner("cilt",pg.opt||null,pg.opt?null:"Sayfa: "+pg.t); }); });
  var pk=$("[data-cl-picker]",root); if(pk){ function sum(){ var on=$("[data-cl-opt][aria-pressed='true']",pk); $("[data-cl-sum]",pk).textContent=on.dataset.n+" · "+clTL(+on.dataset.p)+(pg.picker.from?"'den":""); }
    $$("[data-cl-opt]",pk).forEach(function(b){ b.addEventListener("click",function(){ $$("[data-cl-opt]",pk).forEach(function(x){ x.setAttribute("aria-pressed",x===b); }); sum(); }); }); sum();
    $("[data-cl-pickplan]",pk).addEventListener("click",function(){ var on=$("[data-cl-opt][aria-pressed='true']",pk); openPlanner("cilt",pg.opt,pg.picker.ref+": "+on.dataset.n); }); }
  $$("[data-cl-zone]",root).forEach(function(z){ function pick(){ $$("[data-cl-zone]",root).forEach(function(x){ x.setAttribute("aria-pressed",x===z); }); var Z=CL_FACE.filter(function(x){ return x[0]===z.dataset.clZone; })[0];
      var msg="Merhaba, cilt analizi için randevu istiyorum. İlgilendiğim bölge: "+Z[1].toLocaleLowerCase("tr-TR")+" ("+Z[3].toLocaleLowerCase("tr-TR")+"). "+visitCode();
      $("[data-cl-faceres]",root).innerHTML='<span class="eyebrow">'+Z[1]+'</span><b>'+Z[3]+'</b><div class="cl-paths">'+Z[4].map(function(x){ return clPathCard(x,"Önerilen sayfa",s); }).join("")+'</div><a class="btn-gold shine" href="'+waHref(msg)+'" target="_blank" rel="noopener" data-track-label="'+clLbl(s,"yuz-wa")+'"><span class="lbl">Bu bölge için analiz iste</span></a>'; relead(); }
    z.addEventListener("click",pick); z.addEventListener("keydown",function(e){ if(e.key==="Enter"||e.key===" "){ e.preventDefault(); pick(); } }); });
  $$("[data-cl-hot]",root).forEach(function(b){ b.addEventListener("click",function(){ var x=window.__clHS[+b.dataset.clHot]; $$("[data-cl-hot]",root).forEach(function(y){ y.setAttribute("aria-pressed",y===b); }); $("[data-cl-hotcard]",root).innerHTML="<b>"+x[3]+"</b><p>"+x[4]+"</p>"; }); });
  var sel=$("[data-cl-pkg]",root); if(sel){ function calc(){ var o=CILT.menu[sel.value]; $("[data-cl-p1]",root).textContent=clTL(o[1]); $("[data-cl-p5]",root).textContent=clTL(o[1]*4.5); $("[data-cl-pe]",root).textContent=clTL(o[1]*.9); }
    sel.addEventListener("change",calc); calc(); $("[data-cl-pkgplan]",root).addEventListener("click",function(){ openPlanner("cilt",sel.value,"5 seans paket"); });
    $$("[data-cl-min]",root).forEach(function(b){ b.addEventListener("click",function(){ $$("[data-cl-min]",root).forEach(function(x){ x.setAttribute("aria-pressed",x===b); }); var m=b.dataset.clMin;
      $$("[data-cl-menucard] .mrow",root).forEach(function(r){ r.hidden=!!m && r.dataset.min!==m; }); }); }); }
  relead(); }
function renderCiltPage(s){ var pg=CILT.pages[s], box=$("#ciltPage"); if(!pg){ go("cilt"); return; }
  if(box.dataset.slug===s) return; box.dataset.slug=s;
  box.innerHTML=clHero(s,pg)+clScene(s,pg)+clGallery(s,pg)+clHow(s,pg);
  var sec=$("main > [data-view='cilt-sayfa']"); $("[data-cl-around]",sec).innerHTML=clAround(s);
  $("[data-cl-invite]",sec).textContent=pg.type==="H"?pg.t+" için bir saat ayırın.":"Önce bir görüşme; doğru bakım oradan.";
  var ip=$("[data-cl-plan]",sec); ip.onclick=function(){ openPlanner("cilt",pg.opt||null,pg.opt?null:"Sayfa: "+pg.t); };
  S.planOpt.cilt=pg.opt||S.planOpt.cilt; S.clPage=s; document.title=pg.t+" · Selda Gençer Atelier";
  clBind(box,s,pg); $$("[data-cl-around] a",sec).forEach(function(a){ a.addEventListener("click",function(){}); }); updateBar(); }
ROUTE_ALIAS.push(function(r){ if(r.v==="cilt" && r.p && CILT.pages[r.p]) return {sec:"cilt-sayfa",p:r.p,route:"cilt/"+r.p}; if(r.v==="cilt" && r.p==="atlas") return {sec:"cilt",p:"atlas",route:"cilt/atlas"}; return null; });
ROUTE_HOOK["cilt-sayfa"]=function(p){ renderCiltPage(p); };
ROUTE_HOOK.cilt=function(p){ document.title="Selda Gençer Atelier"; if(p==="atlas"){ var t=$("#ciltAtlas"); if(t) setTimeout(function(){ scrollTo({top:t.getBoundingClientRect().top+scrollY-70,behavior:"instant"}); },80); } };
"""

STORIES_CILT = r''' cilt:[{t:"Önce / Sonra",th:"m/ig/cilt-ters-sonra-480.webp",fr:[{img:"m/ig/cilt-ters-once-480.webp",cap:"Önce"},{img:"m/ig/cilt-ters-sonra-480.webp",cap:"Sonra"}]},
      {t:"LED",th:"m/ig/cilt-led-poster.webp",fr:[{video:"m/ig/cilt-led.mp4",poster:"m/ig/cilt-led-poster.webp",cap:"LED ışık terapisi"},{video:"m/ig/cilt-led-kubbe.mp4",poster:"m/ig/cilt-led-kubbe-poster.webp",cap:"LED kubbe"}]},
      {t:"Akne",th:"m/ig/akne-a-sonra-800.webp",fr:[{video:"m/ig/cilt-darsonval.mp4",poster:"m/ig/cilt-darsonval-poster.webp",cap:"Darsonval"},{img:"m/ig/cilt-ters-sonra-480.webp",cap:"Bakım sonrası"}]},
      {t:"Oda",th:"m/walk-09.webp",fr:[{img:"m/walk-09.webp",cap:"Cilt bakım odamız"},{img:"m/ig/cilt-cihaz-720.webp",cap:"8 başlıklı cihaz"},{video:"m/ig/cilt-sunger.mp4",poster:"m/ig/cilt-sunger-poster.webp",cap:"Altın lavabo"}]},
      {t:"Yorumlar",th:"m/monogram.png",fr:"rv:cilt"},
      {t:"Fiyat",th:"m/ig/cilt-hazirlik-720.webp",fr:"price:cilt"}],
'''


def apply(d) -> None:
    import atelier_build as build
    pages = {}
    for s, p in C.P.items():
        q = dict(p)
        pages[s] = q
    rows = ""
    for g, ids in C.MENU_GROUPS:
        rows += f'<div class="mgroup">{esc(g)}</div>'
        for i in ids:
            n, p, m = C.MENU[i]
            sub = C.FROM.get(i, f"{m} dk" if m else "")
            pr = tl(p) + ("'den" if i in C.FROM else "")
            pk = f" · 5 seans {tl(int(p * 4.5))}" if i in C.PACKAGE else ""
            rows += f'<div class="mrow" data-min="{m or ""}"><span class="nm">{esc(n)}<small>{esc(sub)}{pk}</small></span><span class="ld"></span><span class="pr">{pr}</span></div>'
    rows += '<p class="menu-src">Randevu sistemindeki aktif menüden · 7 Ekim 2026</p>'
    alt = {
        "cilt-led-kubbe": "LED kubbe altında renk döngüsü, salonumuzda çekildi", "cilt-komedon": "Detaylı temizlik, salonumuzda çekildi",
        "cilt-saten": "Saten yüz germe başlığı, salonumuzda çekildi", "cilt-analiz": "Büyüteç altında cilt analizi, salonumuzda çekildi",
        "cilt-hydra": "Başlıkla uygulama, salonumuzda çekildi", "cilt-darsonval": "Darsonval uygulaması akneli yanakta, salonumuzda çekildi",
        "cilt-sunger": "Altın lavabo ve temizleme süngerleri, salonumuzda çekildi", "cilt-maske": "Maskenin hazırlanıp sürülmesi, salonumuzda çekildi",
    }
    data = {"pages": pages, "menu": C.MENU, "from": C.FROM, "pkg": sorted(C.PACKAGE), "groups": C.GROUPS, "thumb": C.THUMB, "how": C.HOW,
            "dims": pair_dims(), "menuHtml": rows, "alt": alt}
    d.css(CSS)
    d.replace_section("cilt", hub())
    d.js_before_boot(JS.replace("__CILT__", json.dumps(data, ensure_ascii=False)))
    d.rep('  if(v==="cilt"){ initHalf(); initQuiz(); initAutoVids($("main > [data-view=\'cilt\']")); initPairs("galCilt","cilt"); }',
          '  if(v==="cilt"){ initQuiz(); initAutoVids($("main > [data-view=\'cilt\']")); $$("main > [data-view=\'cilt\'] [data-cl-pair]").forEach(function(el){ initCompare(el,el.dataset.intro==="1"); }); $$("main > [data-view=\'cilt\'] [data-cl-film]").forEach(clFilm); }')
    # bar + planner on cilt pages
    d.rep('  $("#barCta").addEventListener("click",function(){ if(S.view.indexOf("lazer")===0) return lzPlan(S.view); openPlanner(S.view,S.planOpt[S.view]); });',
          '  $("#barCta").addEventListener("click",function(){ if(S.view.indexOf("lazer")===0) return lzPlan(S.view); if(S.view==="cilt-sayfa") return openPlanner("cilt",S.planOpt.cilt); openPlanner(S.view,S.planOpt[S.view]); });')
    d.rep('  else if(v==="cilt" && S.planOpt && S.planOpt.cilt) l.textContent=PLANS.cilt.opts.filter(function(x){return x.id===S.planOpt.cilt})[0].n+" · saatimi seç";',
          '  else if(v==="cilt-sayfa" && S.clPage){ var cp=CILT.pages[S.clPage]; l.textContent=(cp.bar||(cp.type==="H"?cp.t:"Ön görüşme"))+" · saatimi seç"; }\n'
          '  else if(v==="cilt" && S.planOpt && S.planOpt.cilt) l.textContent=PLANS.cilt.opts.filter(function(x){return x.id===S.planOpt.cilt})[0].n+" · saatimi seç";')
    d.rep(' cilt:{title:"Cilt bakımı randevunuz",opts:[{id:"temizlik",n:"Cilt temizliği",p:1000,d:30},',
          ' cilt:{title:"Cilt bakımı randevunuz",opts:[{id:"gorusme",n:"Cilt bakımı ön görüşmesi",p:null,d:null,s:"Cildinize bakıp bakımı birlikte seçeriz"},{id:"temizlik",n:"Cilt temizliği",p:1000,d:30},')
    d.rep('{id:"derma",n:"Dermabrazyon yüz bakımı",p:6500,d:90}]},',
          '{id:"derma",n:"Dermabrazyon yüz bakımı",p:6500,d:90},{id:"saten",n:"Saten yüz germe",p:4500,d:60},{id:"ton",n:"Ton eşitleme",p:4500,d:null,s:"Alan boyuna göre 4.500–6.500 TL"},{id:"dudak",n:"Dudak bakımı",p:1000,d:null,s:"3 seanslık paketler"},{id:"sirt",n:"Sırt bakımı",p:3500,d:null,s:"Üç seçenek, 3.500–7.000 TL"},{id:"koltuk",n:"Koltuk altı bakımı",p:4500,d:30}]},')
    # quiz result -> the page of the suggested treatment
    d.rep("    '<button class=\"q-back\" data-qagain data-track-label=\"at-cilt-test-yeniden\">↺ Testi yeniden yap</button></div>';",
          "    (Q2PAGE[o.id]?'<a class=\"btn-line\" style=\"justify-content:center;margin-top:8px\" href=\"#cilt/'+Q2PAGE[o.id]+'\" data-track-label=\"at-cilt-test-sayfa\">'+o.n+' sayfası →</a>':'')+\n"
          "    '<button class=\"q-back\" data-qagain data-track-label=\"at-cilt-test-yeniden\">↺ Testi yeniden yap</button></div>';")
    d.rep("function initQuiz(){ renderQuiz(0); }",
          'var Q2PAGE={temizlik:"cilt-temizligi",mini:"cilt-bakimi-fiyatlari",klasik:"klasik-cilt-bakimi",paris:"paris-isiltisi-bakimi",akne:"akne-bakimi",hollywood:"hollywood-bakimi",leke:"leke-bakimi",yenileme:"cilt-yenileme",derma:"dermabrazyon"};\nfunction initQuiz(){ renderQuiz(0); }')
    d.sub(r' cilt:\[\{t:"Yarım yüz",th:"m/ig/cilt-yarim-1-800\.webp".*?\{t:"Fiyat",th:"m/ig/cilt-yarim-2-800\.webp",fr:"price:cilt"\}\],\n', STORIES_CILT.replace("\\", "\\\\"))
    # menu: every cilt page opens its vitrine
    mapping = {"cilt-bakimi": "cilt"}
    mapping.update({s: f"cilt/{s}" for s in C.P})
    build.nav_map(d, mapping)
    # proto panel: a page picker with status marks
    opts = "".join(f'<option value="cilt/{s}">{"◌ " if p["status"] == "cekim" else ("◐ " if p["status"] == "ince" else "✓ ")}{esc(p["t"])}</option>' for s, p in C.P.items())
    d.rep('  <div class="row"><span>Sanat yönü</span>',
          '  <div class="row"><span>Cilt Atlası sayfası (✓ gerçek sonuç · ◐ zayıf · ◌ çekimde)</span><select id="clPick" style="height:38px;border-radius:12px;border:1px solid var(--line-strong);background:var(--raised);color:var(--text);font:14px var(--body);padding:0 8px"><option value="cilt">Cilt (hub)</option>' + opts + '</select></div>\n  <div class="row"><span>Sanat yönü</span>')
    d.rep('  $("#callBtn").addEventListener("click",openCall);', '  $("#callBtn").addEventListener("click",openCall);\n  $("#clPick").addEventListener("change",function(){ go(this.value); });')
    paths = set()
    for s, p in C.P.items():
        h = p["hero"]
        if "video" in h:
            paths |= {f"m/ig/{h['video']}.mp4", f"m/ig/{h['video']}-poster.webp"}
        if "img" in h:
            paths.add(h["img"])
        if "pair" in h:
            paths |= {f"m/ig/{h['pair']}-once-{h['size']}.webp", f"m/ig/{h['pair']}-sonra-{h['size']}.webp"}
        for t in p.get("timeline", []):
            m = t[2]
            if "video" in m:
                paths |= {f"m/ig/{m['video']}.mp4", f"m/ig/{m['video']}-poster.webp"}
            else:
                paths.add(m["img"])
        if p.get("band"):
            paths |= {f"m/ig/{p['band']['video']}.mp4", f"m/ig/{p['band']['video']}-poster.webp"}
        for g in p["gallery"]:
            if g[0] == "pair":
                paths |= {f"m/ig/{g[1]}-once-1200.webp", f"m/ig/{g[1]}-sonra-1200.webp"}
            elif g[0] == "video":
                paths |= {f"m/ig/{g[1]}.mp4", f"m/ig/{g[1]}-poster.webp"}
            else:
                paths.add(g[1])
        if p.get("proof"):
            paths |= {f"m/ig/{p['proof']['pair']}-once-480.webp", f"m/ig/{p['proof']['pair']}-sonra-480.webp"}
        if p.get("film"):
            paths |= {f"m/ig/film/{p['film']['set']}/a{k}.webp" for k in range(1, (p["film"]["n"] + 8) // 9 + 1)}
    paths |= set(C.THUMB.values()) | {"m/ig/cilt-cihaz-720.webp"} | {f"m/ig/film/cilt-film/a{k}.webp" for k in range(1, 7)}
    paths |= set(re.findall(r'm/[\w./-]+\.(?:webp|mp4|png)', STORIES_CILT))
    d.rep("/* ---------- v4 · Cilt Atlası: page engine ---------- */", "/*@media " + json.dumps(sorted(paths)) + " @*/\n/* ---------- v4 · Cilt Atlası: page engine ---------- */")
