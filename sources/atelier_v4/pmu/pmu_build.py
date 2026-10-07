# -*- coding: utf-8 -*-
"""Kalıcı Makyaj "Şölen" -- four PMU vitrines in the ATELIER prototype (plan 2026-10-07).

  pmu        PERDE (brush curtain) · ÜÇ SANAT · ÇİZGİ ÇİZGİ (pen film) · UYANIŞ (5 sweeps) · TON KARTELASI · ODA ·
             YOL · SÖZ · MENÜ (#pmu/fiyat) · SSS · KAPI
  pmu-dudak  brush scene over 5 lip pairs · full kartela · healed-lip macros · price · 3 FAQ
  pmu-kas    sweep slider · TEKNİK LAB (#pmu-kas/micro|pudra|mix) · pen film · gallery · "Eski kalıcı kaşım var"
             (#pmu-kas/silme) · price (#pmu-kas/fiyat)
  pmu-goz    sweep slider (tall halves) · ÇİZGİ STÜDYOSU (#pmu-goz/baby|dip|eyeliner) · real results · FAQ

Media: pmu_pack.py (pairs as one file, kartela sheet, room sheet) + film atlas pmu-kalem (shared_media.py).
Facts: prices from the CRM menu (10-07), kaş silme 3.500 TL / seans; the only PMU Google review (Gülbeyaz G.);
tone names are drafts; no "acısız", no "ömür boyu", no duration promise; rötuş "takipte netleşir".
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
META = json.loads((HERE / "pmu.json").read_text(encoding="utf-8"))

ICON_ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICON_WA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3 20l1.4-4.2A8.5 8.5 0 1 1 7.6 19L3 20z"/></svg>'
ICON_TEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>'
ICON_ZOOM = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5M11 8v6M8 11h6"/></svg>'
KNOB = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 6l-5 6 5 6M15 6l5 6-5 6"/></svg>'
REPLAY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 12a8 8 0 1 0 2.3-5.6M4 4v4h4"/></svg>'

# brush paths (half-image coordinates 0..1) and brush radius (fraction of the shorter side)
BRUSH = {
    "pmu-dudak-a": {"r": .2, "path": [[.70, .33], [.58, .45], [.46, .56], [.33, .67], [.22, .77], [.16, .82]], "alt": "Dudak renklendirme: aynı dudak, önce ve sonra"},
    "dudak-cift-5": {"r": .26, "path": [[.03, .46], [.25, .53], [.48, .62], [.70, .70], [.88, .77]], "alt": "Dudak renklendirme: aynı dudak, önce ve sonra"},
    "pmu-dudak-b": {"r": .22, "path": [[.22, .22], [.32, .38], [.44, .56], [.56, .74], [.64, .86]], "alt": "Dudak renklendirme, önce ve sonra"},
    "pmu-dudak-c": {"r": .2, "path": [[.42, .16], [.42, .46], [.46, .76], [.70, .74], [.72, .44], [.70, .18]], "alt": "Dudak renklendirme, önce ve sonra"},
    "dudak-cift-1": {"r": .3, "path": [[.06, .34], [.5, .3], [.95, .34], [.92, .68], [.5, .74], [.06, .68]], "alt": "Dudak renklendirme, önce ve sonra"},
}
REEL = [  # slug, service, price label, planner opt, ref
    ("pmu-dudak-b", "Dudak renklendirme", "9.000 TL", "dudak", "Uyanış 01 · dudak"),
    ("pmu-kas-cift-a", "Kalıcı kaş", "9.000 TL", "gorusme", "Uyanış 02 · kalıcı kaş"),
    ("pmu-goz-a", "Kalıcı eyeliner", "7.000 TL", "eyeliner", "Uyanış 03 · eyeliner"),
    ("pmu-kas-cift-b", "Kalıcı kaş", "9.000 TL", "gorusme", "Uyanış 04 · kalıcı kaş"),
    ("dudak-cift-1", "Dudak renklendirme", "9.000 TL", "dudak", "Uyanış 05 · dudak"),
]
MENU = [("Dudak ve kaş", [("Dudak renklendirme", "60 dk", "9.000 TL"), ("Microblading (kıl tekniği)", "60 dk", "9.000 TL"),
                          ("Powder brows (pudralama)", "60 dk", "9.000 TL"), ("Mix technique", "60 dk", "9.000 TL")]),
        ("Göz", [("Baby liner", "60 dk", "5.000 TL"), ("Dipliner", "60 dk", "6.000 TL"), ("Eyeliner", "60 dk", "7.000 TL")]),
        ("Kaş silme · yeni", [("Kalıcı kaş silme", "Seans başı · plan kaş görüldükten sonra", "3.500 TL")])]
FAQ = {
    "bolge": ("Hangi bölgelere uygulanıyor?", "Dudak, kaş (kıl tekniği, pudralama ya da ikisi birlikte) ve göz çizgisi (baby liner, dipliner, eyeliner)."),
    "micro": ("Microblading ile pudralama farkı ne?", "Microblading kalemle kıl kıl ince çizgiler çizer; pudralama noktalarla yumuşak, gölge etkisi verir. Mix ikisini birlikte kullanır: başta kıl, gövdede gölge."),
    "liner": ("Baby liner, dipliner ve eyeliner farkı ne?", "Baby liner en yumuşak ve ince seçenektir. Dipliner kirpik dibini doldurur; eyeliner daha belirgindir ve dış köşede uzatılabilir."),
    "kalici": ("Ne kadar kalıcı?", "Kalıcılık cilt tipine, bakıma ve güneşe göre kişiden kişiye değişir; zamanla açılması doğaldır. Tazeleme ihtiyacını uzmanınız kontrolde söyler."),
    "acı": ("Uygulama sırasında ne hissederim?", "Hissedilen kişiden kişiye değişir. Uzmanınız uygulama boyunca sizinle konuşarak ilerler; ara vermek isterseniz verilir."),
    "rotus": ("Rötuş gerekir mi?", "İyileşmeden sonra kontrolde renk ve form birlikte değerlendirilir; rötuş ihtiyacı takipte netleşir."),
    "ton": ("Ton nasıl seçiliyor?", "Dudağınızın ve teninizin kendi rengine bakılarak, ön görüşmede uzmanınızla birlikte seçilir. Kartela adları taslaktır."),
    "silme": ("Eski kalıcı kaşım var, ne yapmalıyım?", "Kaş silme için önce kaşınızı görmemiz gerekir; seans sayısı sabit verilmez. Gün ışığında, filtresiz bir fotoğraf gönderirseniz uzmanımız önden yorumlar."),
    "lens": ("Lens kullanıyorum, göz çizgisi olur mu?", "Uygulama günü lens yerine gözlük tercih etmenizi öneririz. Göz hassasiyetiniz varsa ön görüşmede söyleyin."),
    "kimler": ("Göz çizgisi kimlere uygun?", "Her sabah kalem çekmek istemeyenler, kirpik dibinin daha dolu görünmesini isteyenler için. Uygunluğu ön görüşmede birlikte değerlendiririz."),
}
TECH = {
    "micro": {"n": "Kıl tekniği", "sub": "Microblading", "price": "9.000 TL", "opt": "micro", "photo": "m/ig/pmu-kas-makro-800.webp",
              "p": "Kalem, kaşın yönüne kıl kıl ince çizgiler çizer. Seyrek kaşlarda doğal doluluk için."},
    "pudra": {"n": "Pudralama", "sub": "Powder brows", "price": "9.000 TL", "opt": "powder", "photo": "m/ig/pmu-kas-pudra-800.webp",
              "p": "Noktalarla yumuşak bir gölge; makyajlı ama sade bir kaş görünümü."},
    "mix": {"n": "Mix", "sub": "Mix technique", "price": "9.000 TL", "opt": "mix", "photo": None,
            "p": "Kaş başında kıl tekniği, gövdede pudralama: hem doğal hem dolu."},
}
LINER = {
    "baby": {"n": "Baby liner", "price": "5.000 TL", "opt": "baby", "p": "En ince hat; kirpik dibine yumuşak bir dokunuş."},
    "dip": {"n": "Dipliner", "price": "6.000 TL", "opt": "dipliner", "p": "Kirpik dibini baştan sona doldurur; kirpikler daha gür görünür."},
    "eyeliner": {"n": "Eyeliner", "price": "7.000 TL", "opt": "eyeliner", "p": "Daha belirgin çizgi; dış köşede hafif bir kuyrukla."},
}


def esc(s: str) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def pair_stage(slug: str, cls: str, label: str, intro: bool = True, view: str = "pmu", zoom: str | None = None) -> str:
    p = META["pairs"][slug]
    return (f'<div class="cmp pm-cmp {cls}" data-pm-pair="{slug}" data-intro="{1 if intro else 0}" style="aspect-ratio:{p["w"]}/{p["h"]}">'
            f'<div class="pm-half cmp-b" role="img" aria-label="Önce: {esc(label)}" style="background-image:url({p["file"]})"></div>'
            f'<div class="pm-half pm-son cmp-a" role="img" aria-label="Sonra: {esc(label)}" style="background-image:url({p["file"]})"></div>'
            '<canvas class="dust" data-dust></canvas><div class="cmp-beam"></div><span class="cmp-tag a">Sonra</span><span class="cmp-tag b">Önce</span>'
            f'<button class="cmp-knob" role="slider" aria-label="Önce ve sonra arasında kaydırın" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50" data-track-label="at-{view}-karsilastir">{KNOB}</button>'
            + (f'<button class="zoom-btn" data-pm-zoom="{slug}" aria-label="Sonucu yakından görün" data-track-label="at-{view}-yakindan">{ICON_ZOOM}</button>' if zoom is not False else "")
            + "</div>")


def chips(price: str, slot: str) -> str:
    return (f'<div class="chips"><span class="chip chip-in"><span class="star">★</span> 4,6 · 263 yorum</span>'
            f'<span class="chip chip-in price" style="animation-delay:.08s">{price}</span>'
            f'<span class="chip chip-in" style="animation-delay:.16s" data-slot-chip="{slot}"><span class="dot"></span> <span>Bugün müsait</span></span></div>')


def faq(view: str, keys: list[str]) -> str:
    items = "".join(f'<details><summary data-track-label="at-{view}-sss">{esc(FAQ[k][0])}</summary><p>{esc(FAQ[k][1])}</p></details>' for k in keys)
    return f'<div class="sec gutter faq" style="padding-top:0"><div class="sec-head"><span class="eyebrow">Sık sorulanlar</span><h2>Aklınızdakiler</h2></div>{items}</div>'


def menu(view: str, groups=None, anchor="") -> str:
    groups = groups or MENU
    rows = ""
    for g, items in groups:
        rows += f'<div class="mgroup">{esc(g)}</div>' + "".join(
            f'<div class="mrow"><span class="nm">{esc(n)}<small>{esc(d)}</small></span><span class="ld"></span><span class="pr">{esc(p)}</span></div>' for n, d, p in items)
    return (f'<div class="menu-card pm-menu"{anchor}><span class="eyebrow">Kalıcı makyaj menüsü</span><h3>Fiyatlar</h3>{rows}'
            '<p class="pm-menu-note">Ücret ilk uygulamayı kapsar. Kaş silmede seans sayısı kaş görüldükten sonra planlanır.</p>'
            '<p class="menu-src">Randevu sistemindeki aktif menüden · 7 Ekim 2026</p></div>')


def invite(view: str, title: str, fam: str, steps: str = "1 · İşlem|2 · Gün ve saat|3 · Davetiye → WhatsApp") -> str:
    st = "".join(f"<span>{s}</span>" for s in steps.split("|"))
    return (f'<div class="sec gutter"><div class="invite-teaser"><span class="eyebrow">Randevu davetiyesi</span><h3>{title}</h3>'
            f'<div class="steps-mini">{st}</div><button class="btn-gold shine" data-plan="{fam}" data-track-label="at-{view}-davetiye-ac"><span class="lbl">Davetiyemi hazırla</span>{ICON_ARROW}</button></div></div>')


def film(view: str, fid: str) -> str:
    return f'''<div class="film pm-film" id="{fid}" data-pm-film="pmu-kalem" data-frames="48">
    <div class="film-stage">
      <div class="film-frame lit">
        <img src="m/ig/pmu-kalem-poster.webp" alt="Kalıcı kaş: kalemle kıl kıl çizim, salonumuzda çekildi" width="480" height="854" loading="lazy" class="pm-film-poster">
        <canvas width="480" height="854" aria-hidden="true"></canvas>
        <div class="film-bar"><i></i></div>
        <div class="film-meta"><small data-pm-step-n>01 · Çizim</small><b data-pm-step>Kalem kıl kıl çizer.</b></div>
      </div>
      <div class="film-side pm-film-side">
        <span class="eyebrow">Çizgi çizgi</span>
        <h2 class="display" style="font-size:52px">Kaydırın: kıl kıl çizilir.</h2>
        <p class="muted">Çizim, fazla pigmentin silinmesi ve aynada ilk bakış. Salonumuzda çekilmiş tek bir uygulama.</p>
        <ol class="pm-steps"><li data-k="0" class="on"><b>01</b> Çizim</li><li data-k="1"><b>02</b> Pigment</li><li data-k="2"><b>03</b> Ayna</li></ol>
      </div>
    </div>
  </div>'''


def lipstick(t: dict, i: int, view: str) -> str:
    return (f'<button class="pm-lip" data-tone="{t["id"]}" aria-pressed="{str(i == 0).lower()}" data-track-label="at-{view}-ton" style="--c:{t["c"]}">'
            '<svg viewBox="0 0 40 92" aria-hidden="true"><defs><linearGradient id="pmg-%s-%s" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".35"/><stop offset=".45" stop-color="#fff" stop-opacity=".28"/><stop offset="1" stop-color="#000" stop-opacity=".3"/></linearGradient></defs>'
            '<path d="M11 40 L11 18 Q11 10 20 4 Q29 9 29 18 L29 40Z" fill="var(--c)"/><path d="M11 40 L11 18 Q11 10 20 4 Q29 9 29 18 L29 40Z" fill="url(#pmg-%s-%s)"/>'
            '<rect x="8" y="40" width="24" height="12" rx="1.5" fill="#D9BC78"/><rect x="6" y="52" width="28" height="38" rx="3" fill="#1A1713" stroke="#9C7A35" stroke-width=".8"/>'
            '<rect x="8" y="44" width="24" height="1.4" fill="#F4E6BE" opacity=".7"/></svg>' % (view, t["id"], view, t["id"]) +
            f'<span>{esc(t["n"])}</span></button>')


def kartela(view: str, full: bool) -> str:
    K = META["kartela"]
    t0 = META["tones"][0]
    lips = "".join(lipstick(t, i, view) for i, t in enumerate(META["tones"]))
    return f'''<div class="pm-kartela" data-pm-kartela="{view}">
      <div class="pm-kstage lit" style="background-image:url({K["file"]});background-size:{K["cols"] * 100}% {K["rows"] * 100}%" role="img" aria-label="Gerçek dudak renklendirme sonucu: {esc(t0["n"])} tonu">
        <i class="pm-sheen"></i><span class="pm-kname"><small>Ton · taslak ad</small><b data-pm-kname>{esc(t0["n"])}</b></span>
      </div>
      <div class="pm-kside">
        <div class="pm-lips" role="group" aria-label="Dudak tonu">{lips}</div>
        <p class="hero-note">Ruj başlarının rengi, fotoğraftaki pigmentin ortanca renginden alındı. Ton adları taslaktır; pigment dudağınızın kendi rengine göre ön görüşmede seçilir.</p>
        <div class="pm-row2">
          <a class="btn-gold shine" data-pm-tonewa href="https://wa.me/905330390076" target="_blank" rel="noopener" data-track-label="at-{view}-ton-wa">{ICON_WA}<span class="lbl">Bu ton bana yakışır mı?</span></a>
          {'<button class="btn-line" data-pm-toneplan data-track-label="at-' + view + '-ton-davetiye">Bu tonla saatimi seç</button>' if full else ''}
        </div>
      </div>
    </div>'''


def curtain(view: str, pairs: list[str], h1: str, sub: str, price: str, rings: str) -> str:
    dots = "".join(f'<button class="pm-dot" data-pm-dot="{i}" aria-label="{i + 1}. dönüşüm" aria-pressed="{str(i == 0).lower()}" data-track-label="at-{view}-perde-nokta"></button>' for i in range(len(pairs)))
    first = META["pairs"][pairs[0]]
    return f'''<div class="pm-curtain" data-pm-curtain="{view}" data-pairs="{",".join(pairs)}">
    <div class="pm-cstage" role="group" aria-label="{esc(BRUSH[pairs[0]]["alt"])}">
      <div class="pm-cfallback" style="background-image:url({first["file"]});background-size:200% 100%;background-position:100% 0"></div>
      <canvas class="pm-canvas" aria-hidden="true"></canvas>
      <i class="pm-csweep" aria-hidden="true"></i>
      <canvas class="dust" data-dust></canvas>
      <div class="pm-ctools">
        <span class="pm-hint" data-pm-hint>Parmağınızla boyayın ↔</span>
        <span class="pm-dots">{dots}</span>
        <button class="pm-replay" data-pm-replay aria-label="Yeniden boya" data-track-label="at-{view}-perde-yeniden">{REPLAY}<span>Yeniden</span></button>
      </div>
    </div>
    <div class="pm-ccopy">
      <span class="eyebrow" data-personal>Konutkent · Çankaya</span>
      <h1 class="pm-h1">{h1}</h1>
      <p class="lede pm-sub">{sub}</p>
      {chips(price, rings)}
      <div class="rings" data-rings="{rings}"></div>
      <p class="hero-note pm-honest">Aynı dudağın önce ve sonrası, salonumuzda. İki yarıya aynı renk ayarı uygulandı; sonuç fotoğrafına rötuş yapılmadı.</p>
    </div>
  </div>'''


def h1_letters(text: str) -> str:
    """Letters animate one by one; each word stays unbreakable so a line never splits inside it."""
    out, k = [], 0
    for w in text.split(" "):
        out.append('<span class="pm-w">' + "".join(f'<i style="--k:{k + i}">{c}</i>' for i, c in enumerate(w)) + "</span>")
        k += len(w) + 1
    return " ".join(out)


# --------------------------------------------------------------------------------------------- pages
def page_pmu() -> str:
    v = "pmu"
    arts = [("pmu-dudak", "Dudak", "9.000 TL", "m/ig/pmu-ton-gulpembe-800.webp", "Gerçek dudak renklendirme, yakın çekim", "Renk, form ve parlaklık"),
            ("pmu-kas", "Kaş", "9.000 TL", "m/ig/pmu-kas-makro-800.webp", "Kıl tekniğiyle kalıcı kaş, yakın çekim", "Kıl tekniği · pudra · mix"),
            ("pmu-goz", "Göz", "5.000 TL'den", "m/ig/pmu-goz-a-sonra-795.webp", "Kalıcı göz çizgisi, yakın çekim", "Baby liner · dipliner · eyeliner")]
    cards = "".join(f'<a class="pm-art" href="#{r}" data-go="{r}" data-track-label="at-pmu-git-{r}"><img src="{img}" alt="{esc(alt)}" loading="lazy"><span class="pm-art-t"><small>{esc(sub)}</small><b>{n}</b><em>{p}</em></span></a>'
                    for r, n, p, img, alt, sub in arts)
    reel_items = "".join(
        f'<figure class="pm-ritem" data-i="{i}" data-slug="{s}" style="--ar:{META["pairs"][s]["w"]}/{META["pairs"][s]["h"]}">'
        f'<div class="pm-rframe"><div class="pm-half pm-rb" role="img" aria-label="Önce: {esc(n)}" style="background-image:url({META["pairs"][s]["file"]})"></div>'
        f'<div class="pm-half pm-ra" role="img" aria-label="Sonra: {esc(n)}" style="background-image:url({META["pairs"][s]["file"]})"></div><i class="pm-rbeam"></i>'
        f'<span class="cmp-tag b">Önce</span><span class="cmp-tag a">Sonra</span></div>'
        f'<figcaption><small>0{i + 1} / 0{len(REEL)}</small><b>{esc(n)}</b><span>{esc(p)} · 60 dk</span>'
        f'<button class="btn-line pm-want" data-plan="pmu" data-opt="{o}" data-ref="{esc(ref)}" data-track-label="at-pmu-uyanis-istiyorum">Bunu istiyorum {ICON_ARROW}</button></figcaption></figure>'
        for i, (s, n, p, o, ref) in enumerate(REEL))
    return f'''<section data-view="pmu" hidden>
  {curtain(v, ["pmu-dudak-a", "dudak-cift-5"], '<span class="pm-h1s">Ankara</span> <span class="pm-foil">' + h1_letters("Kalıcı Makyaj") + '</span>', "Bir fırça darbesi. Her sabah hazır.", "5.000 TL'den", "pmu")}

  <div class="sec gutter pm-arts-sec">
    <div class="sec-head"><span class="eyebrow">Üç sanat</span><h2>Dudak, kaş, <em>göz</em>.</h2><p>Her kartın arkasında salonumuzda yapılmış gerçek sonuçlar ve o hizmetin kendi vitrini var.</p></div>
    <div class="pm-arts">{cards}</div>
  </div>

  {film(v, "pmFilm")}

  <div class="pm-reel" id="pmReel" style="--n:{len(REEL)}">
    <div class="pm-rstage dark-band">
      <div class="pm-rhead"><span class="eyebrow">Uyanış</span><h2>Kaydırın, <em>ışık</em> geçsin.</h2></div>
      <div class="pm-ritems">{reel_items}</div>
      <div class="pm-rprog" aria-hidden="true">{"".join("<i></i>" for _ in REEL)}</div>
    </div>
  </div>

  <div class="sec gutter">
    <div class="sec-head"><span class="eyebrow">Ton kartelası</span><h2>Bir ton seçin, <em>gerçeğini</em> görün.</h2><p>Hiçbiri boyama değil: hepsi salonumuzda yapılmış gerçek dudak renklendirmeleri.</p></div>
    {kartela(v, True)}
  </div>

  <div class="sec dark-band gutter pm-oda-sec">
    <div class="pm-oda">
      <div class="pm-oda-figs">
        <figure class="pm-oda-fig" style="background-image:url({META["oda"]["file"]});background-position:0 0;aspect-ratio:{META["oda"]["w"]}/{META["oda"]["h"]}" role="img" aria-label="Kalıcı makyaj istasyonu: pigmentler, kalem ve uçlar tepside"></figure>
        <figure class="pm-oda-fig" style="background-image:url({META["oda"]["file"]});background-position:100% 0;aspect-ratio:{META["oda"]["w"]}/{META["oda"]["h"]}" role="img" aria-label="Uygulama odası: altın lavabo, kadife yatak, logolu havlu"></figure>
      </div>
      <div class="sec-head" style="margin:0"><span class="eyebrow">Oda</span><h2>Her şey <em>hazır</em>, sizi bekliyor.</h2>
        <ul class="pm-lines"><li>Pigmentler, kalem ve uçlar tek tepside.</li><li>Altın lavabo, kadife yatak, logolu havlu.</li><li>Fotoğraflar kalıcı makyaj odamızdan.</li></ul></div>
    </div>
  </div>

  <div class="sec gutter">
    <div class="sec-head"><span class="eyebrow">Yol</span><h2>Dört adım, <em>acele</em> yok.</h2></div>
    <ol class="how pm-way">
      <li><div><b>Ön görüşme</b><p>Yüzünüze ve isteğinize uygun form ve ton birlikte belirlenir.</p></div></li>
      <li><div><b>Çizim ve onay</b><p>Uygulamadan önce çizim yüzünüzde gösterilir; onayınız olmadan başlanmaz.</p></div></li>
      <li><div><b>Uygulama</b><p>Seçtiğiniz bölgeye göre yaklaşık bir saat.</p></div></li>
      <li><div><b>Takip</b><p>İyileşmeden sonra renk ve form kontrolde değerlendirilir; rötuş ihtiyacı takipte netleşir.</p></div></li>
    </ol>
  </div>

  <div class="sec gutter pm-soz" style="padding-top:0">
    <div class="sec-head"><span class="eyebrow">Söz</span><h2>“Beklentimin <em>üstündeydi</em>.”</h2></div>
    <blockquote class="pm-quote"><span class="st" aria-label="5 yıldız">★★★★★</span><p data-pm-quote></p><footer><b>Gülbeyaz G.</b><span>Ağustos 2025 · Google</span></footer></blockquote>
    <p class="rv-note">Google'da kalıcı makyajdan söz eden yorum şimdilik bu kadar; aşağıdakiler salonumuz için yazılanlar.</p>
  </div>
  <div class="sec gutter" style="padding:0 0 4px"><span class="eyebrow gutter" style="display:block;padding:0 var(--gutter)">Salon için yazılanlar · hijyen ve güven</span></div>
  <div class="reviews" data-pm-salon-reviews></div>

  <div class="live" data-live="pmu"></div>

  <div class="sec gutter" id="pmFiyat"><div class="two">
    {menu(v)}
    <div>{faq_inline(v)}</div>
  </div></div>

  <div class="pm-final dark-band">
    <canvas class="dust" data-dust></canvas>
    <span class="eyebrow">Kapı</span>
    <h2 class="pm-final-h">Yarın sabah <em>aynada</em>.</h2>
    <p class="lede">Önce görüşelim, sonra çizelim.</p>
    <div class="pm-final-row">
      <button class="btn-gold shine" data-plan="pmu" data-track-label="at-pmu-final-saat"><span class="lbl">Saatimi seç</span>{ICON_ARROW}</button>
      <a class="btn-line" data-pm-wa="Merhaba, kalıcı makyaj için ön görüşme istiyorum." href="https://wa.me/905330390076" target="_blank" rel="noopener" data-track-label="at-pmu-final-wa">{ICON_WA}WhatsApp</a>
      <a class="btn-line" href="tel:+905330390076" data-track-label="at-pmu-final-tel">{ICON_TEL}Ara</a>
    </div>
  </div>
  <div class="sec gutter" data-visit style="padding-top:0"></div>
</section>'''


def faq_inline(view: str) -> str:
    keys = ["bolge", "micro", "liner", "kalici", "acı", "rotus"]
    items = "".join(f'<details><summary data-track-label="at-{view}-sss">{esc(FAQ[k][0])}</summary><p>{esc(FAQ[k][1])}</p></details>' for k in keys)
    return f'<div class="faq"><div class="sec-head" style="margin-bottom:8px"><span class="eyebrow">Sık sorulanlar</span><h2 style="font-size:40px">Aklınızdakiler</h2></div>{items}</div>'


def page_dudak() -> str:
    v = "pmu-dudak"
    pairs = ["pmu-dudak-a", "pmu-dudak-c", "dudak-cift-5", "pmu-dudak-b", "dudak-cift-1"]
    macros = [("pmu-ton-visne-800", "Vişne · iyileşmiş"), ("pmu-ton-gulkurusu-800", "Gül kurusu · iyileşmiş"), ("pmu-ton-gulpembe-800", "Gül pembe · iyileşmiş"),
              ("dudak-1-800", "Kiremit"), ("dudak-2-800", "Mercan")]
    gal = "".join(f'<button class="gcard pm-macro" data-zoom="m/ig/{s}.webp" aria-label="{esc(n)}: yakından görün" data-track-label="at-pmu-dudak-galeri"><img src="m/ig/{s}.webp" alt="Gerçek dudak renklendirme: {esc(n)}" loading="lazy"><span class="gl"><span>{esc(n)}</span><span>Yakından bak</span></span></button>' for s, n in macros)
    return f'''<section data-view="pmu-dudak" hidden>
  {curtain(v, pairs, 'Kalıcı <span class="pm-foil">' + h1_letters("Dudak Renklendirme") + '</span>', "Kendi dudağınız, bir ton canlı.", "9.000 TL · 60 dk", "pmu-dudak")}
  <div class="sec gutter">
    <div class="sec-head"><span class="eyebrow">Tam kartela</span><h2>Tonunuzu <em>birlikte</em> seçelim.</h2><p>Beş gerçek sonuç; ruj başlarının rengi fotoğraftaki pigmentten.</p></div>
    {kartela(v, True)}
  </div>
  <div class="sec gutter"><div class="sec-head"><span class="eyebrow">İyileşmiş dudaklar</span><h2>Yakından, <em>filtresiz</em>.</h2><p>Dokunun, büyütün. Salonumuzda yapılan gerçek dudak renklendirmeleri.</p></div><div class="gal">{gal}</div></div>
  <div class="live" data-live="pmu"></div>
  {invite(v, "Tonunuzu seçtiniz. Şimdi saatinizi.", "pmu-dudak", "1 · Ton|2 · Gün ve saat|3 · Davetiye → WhatsApp")}
  <div class="sec gutter"><div class="two">
    {menu(v, [("Dudak", [("Dudak renklendirme", "60 dk", "9.000 TL")])])}
    <div>{faq(v, ["ton", "kalici", "rotus"]).replace('class="sec gutter faq" style="padding-top:0"', 'class="faq"')}</div>
  </div></div>
  <div class="sec gutter" data-visit style="padding-top:0"></div>
</section>'''


def tech_svg() -> str:
    # one eyebrow outline; strokes / dots are drawn by JS per technique
    return ('<svg class="pm-brow" viewBox="0 0 400 170" aria-hidden="true"><defs><clipPath id="pmBrowClip"><path id="pmBrowPath" d="M28 118 C40 92 70 74 112 66 C170 54 240 46 300 58 C336 65 362 80 380 104 C352 92 318 86 282 86 C222 86 160 96 112 108 C78 116 52 124 28 118Z"/></clipPath></defs>'
            '<use href="#pmBrowPath" class="pm-brow-out"/><g class="pm-brow-fill" clip-path="url(#pmBrowClip)"></g><path class="pm-brow-edge" d="M28 118 C40 92 70 74 112 66 C170 54 240 46 300 58 C336 65 362 80 380 104 C352 92 318 86 282 86 C222 86 160 96 112 108 C78 116 52 124 28 118Z"/></svg>')


def page_kas() -> str:
    v = "pmu-kas"
    btns = "".join(f'<button data-pm-tech="{k}" aria-pressed="{str(k == "micro").lower()}" data-track-label="at-pmu-kas-teknik">{t["n"]}</button>' for k, t in TECH.items())
    silme_msg = "Merhaba, eski kalıcı kaşım için kaş silme hakkında bilgi almak istiyorum. Gün ışığında, filtresiz fotoğrafımı gönderiyorum."
    return f'''<section data-view="pmu-kas" hidden>
  <div class="hero hero-kas">
    <div class="hero-split">
      <div class="hero-media lit">{pair_stage("pmu-kas-cift-a", "pm-hero-cmp", "kalıcı kaş", True, v)}</div>
      <div class="hero-copy"><span class="eyebrow" data-personal>Konutkent · Çankaya</span><h1>Kalıcı Kaş: <em>Microblading</em>, Pudra, Mix</h1><p class="lede">Kaşınız, her sabah çizilmiş gibi.</p>
        {chips("9.000 TL · 60 dk", "pmu-kas")}<div class="rings" data-rings="pmu-kas"></div><p class="hero-note">Aynı kaşın önce ve sonrası, salonumuzda. Kaydırarak karşılaştırın.</p></div>
    </div>
  </div>
  <div class="sec dark-band gutter" id="pmTech">
    <div class="pm-lab">
      <div class="pm-lab-fig">
        {tech_svg()}
        <figure class="pm-lab-photo"><img data-pm-techphoto src="{TECH["micro"]["photo"]}" alt="Kıl tekniğiyle kalıcı kaş, gerçek sonuç" loading="lazy"><figcaption data-pm-techcap>Gerçek sonuç · kıl tekniği</figcaption></figure>
      </div>
      <div class="sec-head" style="margin:0"><span class="eyebrow">Teknik lab</span><h2>Aynı kaş, <em>üç</em> teknik.</h2>
        <div class="look-row band" role="group" aria-label="Teknik">{btns}</div>
        <div class="pm-tech-card"><b data-pm-techname>{TECH["micro"]["n"]} <small>{TECH["micro"]["sub"]}</small></b><p data-pm-techp>{TECH["micro"]["p"]}</p><span class="pm-tech-price" data-pm-techprice>9.000 TL · 60 dk</span></div>
        <div class="golden-actions"><button class="btn-gold" style="flex:none;padding:0 22px" data-pm-techplan data-track-label="at-pmu-kas-teknik-davetiye"><span class="lbl">Bu teknikle saat seç</span>{ICON_ARROW}</button></div>
        <p class="hero-note" style="color:#968B76">Şema; gerçek sonuç değildir. Tekniği kaş yapınıza göre uzmanınızla birlikte seçersiniz.</p>
      </div>
    </div>
  </div>
  {film(v, "pmFilmKas")}
  <div class="sec gutter">
    <div class="sec-head"><span class="eyebrow">Kalıcı kaş işleri</span><h2>Kaydırın, <em>öncesini</em> görün.</h2><p>Salonumuzda yapılan gerçek kalıcı kaşlar.</p></div>
    <div class="pm-kgal">
      {pair_stage("pmu-kas-cift-b", "pm-gal-cmp", "kalıcı kaş", False, v)}
      <button class="gcard pm-macro" data-zoom="m/ig/pmu-kas-1-800.webp" aria-label="Kalıcı kaş: yakından görün" data-track-label="at-pmu-kas-galeri"><img src="m/ig/pmu-kas-1-800.webp" alt="Kalıcı kaş, gerçek sonuç" loading="lazy"><span class="gl"><span>Kalıcı kaş</span><span>Yakından bak</span></span></button>
      <button class="gcard pm-macro" data-zoom="m/ig/pmu-kas-2-800.webp" aria-label="Microblading: yakından görün" data-track-label="at-pmu-kas-galeri"><img src="m/ig/pmu-kas-2-800.webp" alt="Microblading: çizim ve sonuç" loading="lazy"><span class="gl"><span>Çizim ve sonuç</span><span>Yakından bak</span></span></button>
    </div>
  </div>
  <div class="sec gutter" id="pmSilme">
    <div class="invite-teaser pm-silme">
      <span class="eyebrow">Eski kalıcı kaşım var</span>
      <h3>Önce eskiyi konuşalım.</h3>
      <p class="muted">Kaş silme <b>3.500 TL / seans</b>. Seans sayısı sabit verilmez; plan kaşınız görüldükten sonra yapılır.</p>
      <div class="pm-row2"><a class="btn-gold shine" data-pm-wa="{esc(silme_msg)}" href="https://wa.me/905330390076" target="_blank" rel="noopener" data-track-label="at-pmu-kas-silme-wa">{ICON_WA}<span class="lbl">Fotoğrafımı göndereyim</span></a>
      <button class="btn-line" data-plan="pmu-kas" data-opt="silme" data-track-label="at-pmu-kas-silme-davetiye">Görüşme için saat seç</button></div>
      <p class="hero-note">Gün ışığında, filtresiz bir fotoğraf en doğru yorumu sağlar.</p>
    </div>
  </div>
  <div class="live" data-live="pmu"></div>
  <div class="sec gutter" id="pmKasFiyat"><div class="two">
    {menu(v, [("Kaş", [("Microblading (kıl tekniği)", "60 dk", "9.000 TL"), ("Powder brows (pudralama)", "60 dk", "9.000 TL"), ("Mix technique", "60 dk", "9.000 TL"), ("Kalıcı kaş silme", "Seans başı · plan kaş görüldükten sonra", "3.500 TL")])])}
    <div>{faq(v, ["micro", "silme", "rotus"]).replace('class="sec gutter faq" style="padding-top:0"', 'class="faq"')}</div>
  </div></div>
  <div class="sec gutter" data-visit style="padding-top:0"></div>
</section>'''


def line_svg() -> str:
    p = META["pairs"]["pmu-goz-a"]
    return (f'<div class="pm-studio-fig" style="aspect-ratio:{p["w"]}/{p["h"]}"><div class="pm-half" role="img" aria-label="Göz, uygulamadan önce" style="background-image:url({p["file"]});background-size:200% 100%;background-position:0 0"></div>'
            f'<svg viewBox="0 0 {p["w"]} {p["h"]}" aria-hidden="true"><path class="pm-liner" data-pm-liner d=""/></svg><span class="pm-tag-temsili">Temsili çizim</span></div>')


def page_goz() -> str:
    v = "pmu-goz"
    btns = "".join(f'<button data-pm-liner-pick="{k}" aria-pressed="{str(k == "dip").lower()}" data-track-label="at-pmu-goz-stil">{t["n"]}</button>' for k, t in LINER.items())
    return f'''<section data-view="pmu-goz" hidden>
  <div class="hero">
    <div class="hero-split">
      <div class="hero-media lit pm-goz-media">{pair_stage("pmu-goz-a", "pm-hero-cmp pm-tall", "kalıcı göz çizgisi", True, v)}</div>
      <div class="hero-copy"><span class="eyebrow" data-personal>Konutkent · Çankaya</span><h1>Kalıcı Göz Çizgisi: <em>Eyeliner</em>, Dipliner, Baby Liner</h1><p class="lede">Her sabah çekilmiş bir çizgi.</p>
        {chips("5.000 TL'den", "pmu-goz")}<div class="rings" data-rings="pmu-goz"></div><p class="hero-note">Aynı gözün önce ve sonrası, salonumuzda.</p></div>
    </div>
  </div>
  <div class="sec dark-band gutter" id="pmStudio">
    <div class="pm-studio">
      {line_svg()}
      <div class="sec-head" style="margin:0"><span class="eyebrow">Çizgi stüdyosu</span><h2>Üç çizgi, <em>bir</em> göz.</h2>
        <div class="look-row band" role="group" aria-label="Çizgi stili">{btns}</div>
        <div class="pm-tech-card"><b data-pm-linername>{LINER["dip"]["n"]}</b><p data-pm-linerp>{LINER["dip"]["p"]}</p><span class="pm-tech-price" data-pm-linerprice>{LINER["dip"]["price"]} · 60 dk</span></div>
        <div class="golden-actions"><button class="btn-gold" style="flex:none;padding:0 22px" data-pm-linerplan data-track-label="at-pmu-goz-stil-davetiye"><span class="lbl">Bu çizgiyle saat seç</span>{ICON_ARROW}</button></div>
        <p class="hero-note" style="color:#968B76">Çizgi temsilidir; kalınlık ve uzunluğu göz yapınıza göre uzmanınız belirler.</p>
      </div>
    </div>
  </div>
  <div class="sec gutter"><div class="sec-head"><span class="eyebrow">Gerçek sonuçlar</span><h2>Kaydırın, <em>farkı</em> görün.</h2></div>
    <div class="pm-kgal">{pair_stage("goz-cizgisi-cift", "pm-gal-cmp", "kalıcı göz çizgisi (dipliner)", False, v)}</div></div>
  <div class="live" data-live="pmu"></div>
  {invite(v, "Çizginizi seçtiniz. Şimdi saatinizi.", "pmu-goz", "1 · Çizgi|2 · Gün ve saat|3 · Davetiye → WhatsApp")}
  <div class="sec gutter"><div class="two">
    {menu(v, [("Göz", [("Baby liner", "60 dk", "5.000 TL"), ("Dipliner", "60 dk", "6.000 TL"), ("Eyeliner", "60 dk", "7.000 TL")])])}
    <div>{faq(v, ["liner", "kimler", "lens"]).replace('class="sec gutter faq" style="padding-top:0"', 'class="faq"')}</div>
  </div></div>
  <div class="sec gutter" data-visit style="padding-top:0"></div>
</section>'''


CSS = r"""
/* ---------- v4 · PMU şölen ---------- */
.golden-actions .btn-gold{max-width:100%}.golden-actions .btn-gold .lbl{max-width:none}
.pm-half{position:absolute;inset:0;background-repeat:no-repeat;background-size:200% 100%}
.pm-cmp .cmp-b{background-position:0 0}.pm-cmp .pm-son{background-position:100% 0}
.pm-cmp{border-radius:0;max-height:calc(100svh - var(--nav-h))}
.pm-tall{height:min(86svh,860px);width:auto;max-width:100%;margin:0 auto}
.pm-gal-cmp{border-radius:22px;box-shadow:var(--shadow)}
/* curtain */
.pm-curtain{position:relative;background:var(--velvet);color:#F7F1E4;padding-top:calc(var(--nav-h) + env(safe-area-inset-top,0px))}
.pm-cstage{position:relative;height:calc(100svh - var(--nav-h) - env(safe-area-inset-top,0px));min-height:520px;overflow:hidden;touch-action:pan-y;cursor:crosshair;background:#1a1311}
.pm-cfallback{position:absolute;inset:0;background-repeat:no-repeat;opacity:0}
.pm-canvas{position:absolute;inset:0;width:100%;height:100%}
html[data-tier="C"] .pm-cfallback{opacity:1}html[data-tier="C"] .pm-canvas{display:none}
html[data-tier="C"] .pm-hint,html[data-tier="C"] .pm-replay{display:none}
.pm-csweep{position:absolute;top:-10%;bottom:-10%;left:-60%;width:45%;z-index:3;pointer-events:none;background:linear-gradient(100deg,transparent,rgba(255,236,190,.5),transparent);transform:skewX(-14deg);opacity:0;mix-blend-mode:screen}
.pm-curtain.swept .pm-csweep{animation:hsweep 1.1s var(--ease) both}
.pm-ctools{position:absolute;z-index:6;left:var(--gutter);right:var(--gutter);top:14px;display:flex;align-items:center;gap:10px}
.pm-hint{font:600 10.5px/1 var(--body);letter-spacing:.2em;text-transform:uppercase;color:#F4E6BE;padding:8px 11px;border-radius:999px;background:rgba(14,13,12,.45);border:1px solid rgba(233,215,165,.35);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);transition:opacity .4s}
.pm-curtain.painting .pm-hint{opacity:0}
.pm-dots{display:flex;gap:6px;margin-left:auto}
.pm-dot{width:26px;height:26px;border-radius:50%;border:1px solid rgba(233,215,165,.5);background:rgba(14,13,12,.45);cursor:pointer;padding:0;position:relative}
.pm-dot::after{content:"";position:absolute;inset:8px;border-radius:50%;background:rgba(244,230,190,.45)}
.pm-dot[aria-pressed="true"]::after{background:#F4E6BE;box-shadow:0 0 8px #F4E6BE}
.pm-replay{display:inline-flex;align-items:center;gap:6px;height:32px;padding:0 11px;border-radius:999px;border:1px solid rgba(233,215,165,.5);background:rgba(14,13,12,.45);color:#F7F1E4;font:600 11px/1 var(--body);letter-spacing:.12em;text-transform:uppercase;cursor:pointer}
.pm-replay svg{width:14px;height:14px}
.pm-ccopy{position:relative;z-index:5;display:grid;gap:12px;margin-top:-260px;padding:0 var(--gutter) 34px;background:linear-gradient(180deg,transparent,rgba(14,13,12,.82) 110px,var(--velvet) 200px)}
.pm-ccopy .eyebrow{color:#EBD49A}
.pm-ccopy .chip{background:rgba(20,18,15,.45);color:#F7F1E4;border-color:rgba(233,215,165,.38)}
.pm-ccopy .hero-note{color:#B9AE98}
.pm-ccopy .ring span{color:#C3B8A1}.pm-ccopy .ring img{border-color:var(--velvet)}
.pm-h1{margin:0;font-family:var(--display);font-weight:300;line-height:.9;letter-spacing:-.02em;font-size:clamp(54px,15vw,112px)}
.pm-h1s{display:block;font:600 12px/1 var(--body);letter-spacing:.3em;text-transform:uppercase;color:#EBD49A;margin-bottom:10px}
.pm-w{display:inline-block;white-space:nowrap}
.pm-foil i{font-style:normal;display:inline-block;background:var(--foil);background-size:400% 100%;-webkit-background-clip:text;background-clip:text;color:transparent}
html[data-tier="A"] .pm-curtain .pm-foil i,html[data-tier="B"] .pm-curtain .pm-foil i{opacity:0;transform:translateY(.25em);transition:opacity .5s var(--ease),transform .6s var(--ease);transition-delay:calc(var(--k) * 45ms)}
.pm-curtain.lit-title .pm-foil i{opacity:1!important;transform:none!important}
.pm-sub{color:#EBD49A}
/* arts */
.pm-arts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.pm-art{position:relative;display:block;aspect-ratio:9/16;border-radius:22px;overflow:hidden;background:#2a2320;color:#F7F1E4;text-decoration:none;box-shadow:var(--shadow)}
.pm-art img{width:100%;height:100%;object-fit:cover;transform-origin:50% 60%}
html[data-tier="A"] .pm-art img,html[data-tier="B"] .pm-art img{animation:kb 14s ease-in-out infinite alternate}
.pm-art:nth-child(2) img{animation-delay:-4s}.pm-art:nth-child(3) img{animation-delay:-8s}
.pm-art::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 45%,rgba(14,13,12,.85))}
.pm-art-t{position:absolute;z-index:2;left:10px;right:10px;bottom:12px;display:grid;gap:3px}
.pm-art-t small{font:600 8.5px/1.25 var(--body);letter-spacing:.14em;text-transform:uppercase;color:#EBD49A}
.pm-art-t b{font:400 clamp(24px,7vw,40px)/1 var(--display)}
.pm-art-t em{font:600 12.5px/1 var(--body);font-style:normal;color:#F4E6BE}
/* film */
.pm-film .film-frame{aspect-ratio:480/854}
.pm-steps{list-style:none;margin:6px 0 0;padding:0;display:grid;gap:8px}
.pm-steps li{display:flex;gap:10px;align-items:baseline;font:400 24px/1 var(--display);color:var(--text-3);transition:color .3s}
.pm-steps li b{font:600 11px var(--body);letter-spacing:.2em;color:var(--gold-ink)}
.pm-steps li.on{color:var(--text)}
/* reel (uyanış) */
.pm-reel{height:calc(var(--n) * 85svh + 100svh)}
.pm-rstage{position:sticky;top:calc(var(--nav-h) + env(safe-area-inset-top,0px));height:calc(100svh - var(--nav-h));overflow:hidden;display:grid;grid-template-rows:auto 1fr auto;gap:10px;padding:18px var(--gutter) calc(var(--bar-h) + 18px)}
.pm-rhead h2{font-family:var(--display);font-weight:400;font-size:clamp(32px,8.5vw,52px);line-height:1;margin:6px 0 0}
.pm-ritems{position:relative;min-height:0}
.pm-ritem{position:absolute;inset:0;margin:0;display:grid;grid-template-rows:minmax(0,1fr) auto;gap:12px;opacity:0;transition:opacity .45s var(--ease);pointer-events:none}
.pm-ritem.on{opacity:1;pointer-events:auto}
.pm-rframe{position:relative;justify-self:center;align-self:center;height:100%;max-width:100%;aspect-ratio:var(--ar);border-radius:22px;overflow:hidden;box-shadow:0 30px 80px -30px rgba(0,0,0,.8);border:1px solid rgba(233,215,165,.25);--p:0}
.pm-rb{background-position:0 0}.pm-ra{background-position:100% 0;clip-path:inset(0 calc(100% - var(--p) * 1%) 0 0)}
.pm-rbeam{position:absolute;top:0;bottom:0;left:calc(var(--p) * 1%);width:2px;margin-left:-1px;z-index:4;background:linear-gradient(180deg,#F6EACB,#C9A55C 50%,#F6EACB);box-shadow:0 0 12px 2px rgba(246,234,203,.95),0 0 46px 12px rgba(201,165,92,.5);opacity:calc(var(--p) * (100 - var(--p)) / 900)}
.pm-rframe .cmp-tag{opacity:1}
.pm-ritem figcaption{display:grid;grid-template-columns:1fr auto;gap:2px 12px;align-items:center}
.pm-ritem figcaption small{grid-column:1/-1;font:600 11px/1 var(--body);letter-spacing:.24em;color:#E2C98B}
.pm-ritem figcaption b{font:400 28px/1.05 var(--display)}
.pm-ritem figcaption span{grid-column:1;font-size:13px;color:#C3B8A1}
.pm-want{grid-column:2;grid-row:2/4;height:44px;color:#F3ECDD;font-size:13px}
.pm-rprog{display:flex;gap:6px;justify-content:center}.pm-rprog i{width:26px;height:3px;border-radius:3px;background:rgba(233,215,165,.25)}.pm-rprog i.on{background:#F4E6BE}
html[data-tier="C"] .pm-reel{height:auto}
html[data-tier="C"] .pm-rstage{position:relative;height:auto;top:0}
html[data-tier="C"] .pm-ritems{display:grid;gap:28px}
html[data-tier="C"] .pm-ritem{position:relative;opacity:1;pointer-events:auto}
html[data-tier="C"] .pm-rframe{height:auto;width:100%;max-height:70svh;--p:52}
/* kartela */
.pm-kartela{display:grid;gap:16px}
.pm-kstage{position:relative;aspect-ratio:3/4;max-height:72svh;border-radius:22px;overflow:hidden;background-repeat:no-repeat;box-shadow:var(--shadow);transition:background-position 0s;justify-self:center;width:min(100%,520px)}
.pm-sheen{position:absolute;inset:-10% auto -10% -60%;width:50%;background:linear-gradient(100deg,transparent,rgba(255,244,214,.55),transparent);transform:skewX(-14deg);opacity:0;mix-blend-mode:screen;pointer-events:none}
.pm-kstage.shine .pm-sheen{animation:hsweep 1s var(--ease) both}
.pm-kname{position:absolute;left:14px;bottom:12px;display:grid;gap:2px;color:#FFF8EA;text-shadow:0 1px 12px rgba(0,0,0,.6)}
.pm-kname small{font:600 9.5px/1 var(--body);letter-spacing:.2em;text-transform:uppercase;color:#F4E6BE}
.pm-kname b{font:italic 500 30px/1 var(--display)}
.pm-lips{display:flex;gap:14px;overflow-x:auto;scrollbar-width:none;padding:6px 2px}
.pm-lips::-webkit-scrollbar{display:none}
.pm-lip{flex:none;display:grid;justify-items:center;gap:6px;background:none;border:0;cursor:pointer;padding:6px 4px;border-radius:14px;transition:transform .3s var(--ease)}
.pm-lip svg{width:34px;height:78px;filter:drop-shadow(0 6px 10px rgba(0,0,0,.25));transition:transform .35s var(--ease)}
.pm-lip span{font:500 12px/1.1 var(--body);color:var(--text-2);white-space:nowrap}
.pm-lip[aria-pressed="true"] svg{transform:translateY(-8px) scale(1.08)}
.pm-lip[aria-pressed="true"] span{color:var(--text);font-weight:650}
.pm-row2{display:grid;gap:8px}
.pm-row2 .btn-gold{flex:none;width:100%}
.pm-row2 .btn-line{justify-content:center}
/* oda */
.pm-oda{display:grid;gap:20px}
.pm-oda-figs{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.pm-oda-fig{margin:0;border-radius:20px;background-size:200% 100%;background-repeat:no-repeat;border:1px solid rgba(233,215,165,.25)}
.pm-lines{margin:6px 0 0;padding:0;list-style:none;display:grid;gap:10px}
.pm-lines li{font:400 22px/1.2 var(--display);padding-left:22px;position:relative}
.pm-lines li::before{content:"";position:absolute;left:0;top:.5em;width:10px;height:1px;background:#E2C98B}
/* söz */
.pm-quote{margin:0;padding:24px 20px;border-radius:24px;background:var(--raised);border:1px solid var(--line);box-shadow:var(--shadow);display:grid;gap:12px}
.pm-quote .st{color:var(--gold);letter-spacing:.14em}
.pm-quote p{margin:0;font:400 23px/1.32 var(--display)}
.pm-quote footer{display:flex;justify-content:space-between;font-size:12.5px;color:var(--text-3)}.pm-quote footer b{color:var(--text-2)}
.pm-menu-note{font-size:12.5px;color:var(--text-2);text-align:center;margin:12px 0 0}
/* final */
.pm-final{position:relative;overflow:hidden;min-height:78svh;display:grid;align-content:center;justify-items:center;text-align:center;gap:14px;padding:80px var(--gutter);background:radial-gradient(90% 60% at 50% 40%,rgba(201,165,92,.18),transparent 70%),var(--velvet)}
.pm-final-h{font-family:var(--display);font-weight:300;font-size:clamp(50px,14vw,104px);line-height:.92;margin:0}
.pm-final-row{display:grid;gap:10px;width:min(100%,420px)}
.pm-final-row .btn-gold{flex:none;width:100%}
.pm-final-row .btn-line{justify-content:center;color:#F3ECDD}
/* lab + studio */
.pm-lab,.pm-studio{display:grid;gap:22px}
.pm-lab-fig{display:grid;gap:12px}
.pm-brow{width:100%;height:auto;border-radius:22px;background:radial-gradient(90% 80% at 50% 60%,rgba(201,165,92,.18),transparent 70%),#141210;border:1px solid rgba(233,215,165,.25)}
.pm-brow-out{fill:rgba(247,241,228,.04)}
.pm-brow-edge{fill:none;stroke:rgba(226,201,139,.5);stroke-width:1;stroke-dasharray:3 4}
.pm-hair{fill:none;stroke:#5B3A22;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1;animation:drawl .55s var(--ease) var(--d,0ms) forwards}
.pm-pdot{fill:#8A5A3A;opacity:0;animation:fadein .35s var(--ease) var(--d,0ms) forwards}
html[data-tier="C"] .pm-hair{animation:none;stroke-dashoffset:0}html[data-tier="C"] .pm-pdot{animation:none;opacity:1}
.pm-lab-photo{margin:0;position:relative;border-radius:20px;overflow:hidden;aspect-ratio:16/10;border:1px solid rgba(233,215,165,.25)}
.pm-lab-photo img{width:100%;height:100%;object-fit:cover}
.pm-lab-photo figcaption{position:absolute;left:12px;bottom:10px;color:#F7F1E4;font:500 16px/1.1 var(--display);text-shadow:0 1px 10px rgba(0,0,0,.7)}
.pm-lab-photo.none img{display:none}.pm-lab-photo.none{display:grid;place-items:center;background:#1a1612}.pm-lab-photo.none figcaption{position:static;color:#968B76;font-size:15px;text-align:center;padding:0 20px}
.pm-tech-card{display:grid;gap:6px;padding:16px;border-radius:18px;border:1px solid rgba(233,215,165,.25);background:rgba(255,255,255,.03)}
.pm-tech-card b{font:400 28px/1.05 var(--display)}.pm-tech-card b small{font:600 10.5px var(--body);letter-spacing:.18em;text-transform:uppercase;color:#E2C98B;margin-left:6px}
.pm-tech-card p{margin:0;color:#C3B8A1}.pm-tech-price{font:500 20px/1 var(--display);color:#F4E6BE}
.pm-studio-fig{position:relative;border-radius:22px;overflow:hidden;max-height:74svh;width:min(100%,420px);justify-self:center;border:1px solid rgba(233,215,165,.25)}
.pm-studio-fig svg{position:absolute;inset:0;width:100%;height:100%}
.pm-liner{fill:#14100E;fill-opacity:.88;stroke:#14100E;stroke-width:2;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;transition:none}
.pm-liner.draw{animation:drawl 1.1s var(--ease) forwards, pmFill 1.1s var(--ease) forwards}
@keyframes pmFill{0%,55%{fill-opacity:0}100%{fill-opacity:.88}}
html[data-tier="C"] .pm-liner{stroke-dashoffset:0;animation:none!important;fill-opacity:.88}
.pm-tag-temsili{position:absolute;top:12px;left:12px;font:600 10px/1 var(--body);letter-spacing:.2em;text-transform:uppercase;padding:7px 10px;border-radius:999px;background:rgba(14,13,12,.5);border:1px solid rgba(233,215,165,.4);color:#F7F1E4}
.pm-kgal{display:grid;gap:12px}
.pm-kgal .gcard{width:auto;aspect-ratio:4/5}
.pm-macro img{object-fit:cover}
.pm-silme .muted b{color:var(--text)}
@media (min-width:960px){
  .pm-curtain{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:end}
  .pm-cstage{grid-column:2;grid-row:1;height:calc(100svh - var(--nav-h));width:min(52vw,calc((100svh - var(--nav-h)) * .62));min-height:0}
  .pm-ccopy{grid-column:1;grid-row:1;margin:0;background:none;padding:0 56px 72px;max-width:720px;justify-self:end}
  .pm-arts{gap:18px}.pm-art-t small{font-size:10px}
  .pm-rstage{grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);grid-template-rows:1fr auto;column-gap:48px}
  .pm-rhead{align-self:center}.pm-ritems{grid-row:1/3;grid-column:2}
  .pm-kartela{grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:center;max-width:1000px}
  .pm-oda{grid-template-columns:1.3fr 1fr;align-items:center}
  .pm-lab,.pm-studio{grid-template-columns:1.2fr 1fr;align-items:center;gap:48px}
  .pm-kgal{grid-template-columns:1.4fr 1fr 1fr;align-items:center}
  .pm-tall{height:calc(100svh - var(--nav-h) - 40px)}
  .pm-goz-media{display:grid;place-items:center}
}
"""

JS = r"""
/* ---------- v4 · PMU şölen ---------- */
var PM=__PMDATA__;
var PM_REVIEW="__PMREVIEW__";
function pmPair(slug){ return PM.pairs[slug]; }
function pmImg(src,cb){ var im=new Image(); im.decoding="async"; im.onload=function(){ (im.decode?im.decode():Promise.resolve()).catch(function(){}).then(function(){ cb(im); }); }; im.src=src; return im; }
/* PERDE: canvas brush reveals the sonra half along the lip, then a gold sweep; the visitor can paint too */
function initBrush(box){
  var view=box.dataset.pmCurtain, pairs=box.dataset.pairs.split(","), stage=$(".pm-cstage",box), cv=$(".pm-canvas",box), ctx=cv.getContext("2d"), fb=$(".pm-cfallback",box);
  var mask=document.createElement("canvas"), mx=mask.getContext("2d"), tmp=document.createElement("canvas"), tx=tmp.getContext("2d");
  var cur=0, img=null, W=0, H=0, fit=null, raf=0, painted=0, head=null, mode="auto", dpr=Math.min(2,window.devicePixelRatio||1);
  function size(){ var r=stage.getBoundingClientRect(); W=Math.max(1,Math.round(r.width*dpr)); H=Math.max(1,Math.round(r.height*dpr)); [cv,mask,tmp].forEach(function(c){ c.width=W; c.height=H; }); calc(); }
  function calc(){ if(!img) return; var hw=img.naturalWidth/2, hh=img.naturalHeight, k=Math.max(W/hw,H/hh); var dw=hw*k, dh=hh*k; fit={hw:hw,hh:hh,k:k,ox:(W-dw)/2,oy:(H-dh)/2,dw:dw,dh:dh}; }
  function toC(p){ return [fit.ox+p[0]*fit.dw, fit.oy+p[1]*fit.dh]; }
  function render(){ if(!img||!fit) return; ctx.clearRect(0,0,W,H);
    ctx.drawImage(img,0,0,fit.hw,fit.hh,fit.ox,fit.oy,fit.dw,fit.dh);
    tx.globalCompositeOperation="source-over"; tx.clearRect(0,0,W,H); tx.drawImage(img,fit.hw,0,fit.hw,fit.hh,fit.ox,fit.oy,fit.dw,fit.dh);
    tx.globalCompositeOperation="destination-in"; tx.drawImage(mask,0,0); ctx.drawImage(tmp,0,0);
    if(head){ var g=ctx.createRadialGradient(head[0],head[1],head[2]*.55,head[0],head[1],head[2]*1.05); g.addColorStop(0,"rgba(244,230,190,0)"); g.addColorStop(.7,"rgba(244,224,170,.55)"); g.addColorStop(1,"rgba(201,165,92,0)"); ctx.fillStyle=g; ctx.beginPath(); ctx.arc(head[0],head[1],head[2]*1.05,0,6.283); ctx.fill(); } }
  function stamp(x,y,r){ var g=mx.createRadialGradient(x,y,r*.35,x,y,r); g.addColorStop(0,"rgba(0,0,0,1)"); g.addColorStop(1,"rgba(0,0,0,0)"); mx.fillStyle=g; mx.beginPath(); mx.arc(x,y,r,0,6.283); mx.fill(); }
  function radius(){ var B=PM.brush[pairs[cur]]; return B.r*Math.min(fit.dw,fit.dh)*(fit.dh>fit.dw?1:1); }
  function along(path,t){ var segs=[],L=0; for(var i=1;i<path.length;i++){ var a=toC(path[i-1]),b=toC(path[i]),l=Math.hypot(b[0]-a[0],b[1]-a[1]); segs.push([a,b,l]); L+=l; } var d=t*L; for(var j=0;j<segs.length;j++){ if(d<=segs[j][2]){ var s=segs[j], k=s[2]?d/s[2]:0; return [s[0][0]+(s[1][0]-s[0][0])*k, s[0][1]+(s[1][1]-s[0][1])*k]; } d-=segs[j][2]; } var e=segs[segs.length-1][1]; return e; }
  function auto(){ cancelAnimationFrame(raf); mode="auto"; box.classList.remove("painting","swept"); mx.clearRect(0,0,W,H); render();
    if(S.tier==="C"){ mx.fillRect(0,0,W,H); render(); box.classList.add("lit-title"); return; }
    var B=PM.brush[pairs[cur]], r=radius(), t0=performance.now(), D1=1500, D2=700, lastT=0;
    function f(t){ var k=(t-t0)/D1;
      if(k<=1){ for(var s=lastT;s<=k;s+=.004){ var p=along(B.path,ease(Math.min(1,s))); stamp(p[0],p[1],r); } lastT=k; var hp=along(B.path,ease(Math.min(1,k))); head=[hp[0],hp[1],r*.5]; render(); raf=requestAnimationFrame(f); return; }
      head=null; if(!box.classList.contains("swept")) box.classList.add("swept","lit-title");
      var q=Math.min(1,(t-t0-D1)/D2), x=-.2*W+q*1.4*W; var g=mx.createLinearGradient(x-W*.35,0,x,0); g.addColorStop(0,"rgba(0,0,0,1)"); g.addColorStop(1,"rgba(0,0,0,0)"); mx.fillStyle=g; mx.fillRect(0,0,x,H); render();
      if(q<1) raf=requestAnimationFrame(f); else { mx.fillStyle="#000"; mx.fillRect(0,0,W,H); render(); } }
    raf=requestAnimationFrame(f); }
  function load(i){ cur=i; var P=pmPair(pairs[i]); fb.style.backgroundImage="url("+P.file+")"; stage.setAttribute("aria-label",PM.brush[pairs[i]].alt);
    $$("[data-pm-dot]",box).forEach(function(b){ b.setAttribute("aria-pressed",+b.dataset.pmDot===i); });
    pmImg(P.file,function(im){ if(cur!==i) return; img=im; size(); auto(); }); }
  var down=null;
  stage.addEventListener("pointerdown",function(e){ if(e.target.closest("button")||!fit||S.tier==="C") return; down=[e.clientX,e.clientY]; });
  stage.addEventListener("pointermove",function(e){ if(!down||!fit) return; var dx=e.clientX-down[0], dy=e.clientY-down[1];
    if(mode!=="paint"){ if(Math.abs(dx)<6||Math.abs(dx)<Math.abs(dy)) return; mode="paint"; cancelAnimationFrame(raf); mx.clearRect(0,0,W,H); box.classList.add("painting"); sigHit("at-"+view+"-perde-boya"); }
    var r=stage.getBoundingClientRect(); stamp((e.clientX-r.left)*dpr,(e.clientY-r.top)*dpr,radius()*.8); head=[(e.clientX-r.left)*dpr,(e.clientY-r.top)*dpr,radius()*.4]; render(); });
  function up(){ down=null; head=null; if(mode==="paint") render(); }
  stage.addEventListener("pointerup",up); stage.addEventListener("pointercancel",up); stage.addEventListener("pointerleave",up);
  $("[data-pm-replay]",box).addEventListener("click",function(){ auto(); });
  $$("[data-pm-dot]",box).forEach(function(b){ b.addEventListener("click",function(){ load(+b.dataset.pmDot); }); });
  addEventListener("resize",function(){ if(S.view===view){ size(); if(mode==="auto"){ mx.fillStyle="#000"; mx.fillRect(0,0,W,H); } render(); } });
  var io=new IntersectionObserver(function(es){ if(es[0].isIntersecting && !img){ load(0); } },{threshold:.1}); io.observe(stage);
  box.__replay=auto; }
/* pen film (scroll-scrubbed atlas) */
function initPmFilm(sec){ var cv=$("canvas",sec), ctx=cv.getContext("2d"), bar=$(".film-bar i",sec), poster=$(".pm-film-poster",sec), N=+sec.dataset.frames, FA=atlas(sec.dataset.pmFilm,N,480,854), cur=-1, view=sec.closest("[data-view]").dataset.view;
  var STEPS=[["01 · Çizim","Kalem kıl kıl çizer."],["02 · Pigment","Fazlası silinir, kaş taranır."],["03 · Ayna","Aynada ilk bakış."]];
  cv.style.opacity=0;
  function draw(i){ if(!FA.draw(ctx,i,cv.width,cv.height)) return; cv.style.opacity=1; cur=i; }
  new IntersectionObserver(function(es){ if(es[0].isIntersecting && S.tier!=="C") FA.load(function(){ if(cur<0) draw(0); }); },{rootMargin:"600px"}).observe(sec);
  function update(){ if(S.view!==view||S.tier==="C") return; var r=sec.getBoundingClientRect(), vh=innerHeight; if(r.bottom<0||r.top>vh) return;
    var p=Math.min(1,Math.max(0,-r.top/(r.height-vh))), i=Math.min(N-1,Math.round(p*(N-1))); bar.style.width=(p*100).toFixed(1)+"%"; if(i!==cur) draw(i);
    var k=p<.38?0:(p<.76?1:2); var n=$("[data-pm-step-n]",sec); if(n.textContent!==STEPS[k][0]){ n.textContent=STEPS[k][0]; $("[data-pm-step]",sec).textContent=STEPS[k][1]; $$(".pm-steps li",sec).forEach(function(li){ li.classList.toggle("on",+li.dataset.k===k); }); } }
  scrollers.push(update); }
/* UYANIŞ: scroll moves a gold light across five real before/after pairs */
function initReel(sec){ var items=$$(".pm-ritem",sec), prog=$$(".pm-rprog i",sec), n=items.length, on=-1;
  function update(){ if(S.view!=="pmu"||S.tier==="C") return; var r=sec.getBoundingClientRect(), vh=innerHeight; if(r.bottom<0||r.top>vh) return;
    var p=Math.min(.9999,Math.max(0,-r.top/(r.height-vh))), x=p*n, i=Math.floor(x), t=x-i;
    if(i!==on){ on=i; items.forEach(function(it,k){ it.classList.toggle("on",k===i); }); prog.forEach(function(d,k){ d.classList.toggle("on",k<=i); }); }
    var q=Math.min(1,Math.max(0,(t-.12)/.62)); q=q*q*(3-2*q); $(".pm-rframe",items[i]).style.setProperty("--p",(q*100).toFixed(1)); }
  if(S.tier==="C") items.forEach(function(it){ it.classList.add("on"); });
  scrollers.push(update); update(); }
/* TON KARTELASI */
function initKartela(box){ var view=box.dataset.pmKartela, st=$(".pm-kstage",box), cols=PM.kartela.cols, rows=PM.kartela.rows, user=false;
  function pick(id,byUser){ var t=PM.tones.filter(function(x){ return x.id===id; })[0]; if(!t) return; if(byUser) user=true; S.pmTone=t.n;
    st.style.backgroundPosition=((t.i%cols)/(cols-1)*100)+"% "+(rows>1?(Math.floor(t.i/cols)/(rows-1)*100):0)+"%";
    st.setAttribute("aria-label","Gerçek dudak renklendirme sonucu: "+t.n+" tonu"); $("[data-pm-kname]",box).textContent=t.n;
    st.classList.remove("shine"); void st.offsetWidth; st.classList.add("shine");
    $$(".pm-lip",box).forEach(function(b){ b.setAttribute("aria-pressed",b.dataset.tone===id); });
    var a=$("[data-pm-tonewa]",box); a.href=waHref("Merhaba, kalıcı dudak renklendirme için ton danışmak istiyorum. Ton: "+t.n+" (sitedeki kartela). "+visitCode());
    if(byUser) updateBar(); }
  $$(".pm-lip",box).forEach(function(b){ b.addEventListener("click",function(){ pick(b.dataset.tone,true); }); });
  var pl=$("[data-pm-toneplan]",box); if(pl) pl.addEventListener("click",function(){ openPlanner(view==="pmu"?"pmu-dudak":view,"dudak","Ton: "+(S.pmTone||PM.tones[0].n)); });
  st.addEventListener("click",function(){ openLightbox(PM.kartela.file); });
  pick(PM.tones[0].id);
  if(S.tier!=="C"){ var io=new IntersectionObserver(function(es){ if(!es[0].isIntersecting) return; io.disconnect(); var k=1; setTimeout(function step(){ if(user||S.view!==view) return; pick(PM.tones[k++].id); if(k<3) setTimeout(step,1500); },900); },{threshold:.5}); io.observe(st); } }
/* TEKNİK LAB: one brow outline, redrawn for kıl tekniği / pudra / mix */
function seeded(n){ var s=n; return function(){ s=(s*16807)%2147483647; return (s-1)/2147483646; }; }
function initTechLab(sec){ var g=$(".pm-brow-fill",sec), NS="http://www.w3.org/2000/svg", R;
  function hair(x,y,len,ang,d){ var p=document.createElementNS(NS,"path"), ex=x+Math.cos(ang)*len, ey=y+Math.sin(ang)*len, cx=x+Math.cos(ang+.35)*len*.55, cy=y+Math.sin(ang+.35)*len*.55;
    p.setAttribute("d","M"+x.toFixed(1)+" "+y.toFixed(1)+"Q"+cx.toFixed(1)+" "+cy.toFixed(1)+" "+ex.toFixed(1)+" "+ey.toFixed(1)); p.setAttribute("pathLength","1"); p.setAttribute("class","pm-hair"); p.style.strokeWidth=(1.1+R()*.9)+"px"; p.style.setProperty("--d",d+"ms"); g.appendChild(p); }
  function dot(x,y,r,d,o){ var c=document.createElementNS(NS,"circle"); c.setAttribute("cx",x.toFixed(1)); c.setAttribute("cy",y.toFixed(1)); c.setAttribute("r",r.toFixed(2)); c.setAttribute("class","pm-pdot"); c.style.setProperty("--d",d+"ms"); c.style.fillOpacity=o; g.appendChild(c); }
  function draw(k){ g.innerHTML=""; R=seeded(7);
    var hairs=k==="micro"?1:(k==="mix"?.42:0), dots=k==="pudra"?1:(k==="mix"?1:0);
    if(hairs){ for(var i=0;i<130*hairs;i++){ var t=i/(130*hairs); var x=30+t*(k==="mix"?150:345), base=118-Math.sin(Math.min(1,t*1.1)*2.6)*48*(k==="mix"?1:1); var y=base-R()*30; var ang=-1.25+t*1.05+(R()-.5)*.25; hair(x,y+18,16+R()*14,ang,Math.round(i*9)); } }
    if(dots){ var from=k==="mix"?120:30; for(var j=0;j<1400;j++){ var u=R(), x2=from+u*(380-from), w=R(), y2=60+w*70; var dens=k==="mix"?.25+u*.75:.15+u*.85; if(R()>dens) continue; dot(x2,y2,1.3+R()*1.6,Math.round(200+u*900),(.45+u*.5).toFixed(2)); } } }
  function pick(k,byUser){ var T=PM.tech[k]; if(!T) return; S.pmTech=k; $$("[data-pm-tech]",sec).forEach(function(b){ b.setAttribute("aria-pressed",b.dataset.pmTech===k); });
    $("[data-pm-techname]",sec).innerHTML=T.n+" <small>"+T.sub+"</small>"; $("[data-pm-techp]",sec).textContent=T.p; $("[data-pm-techprice]",sec).textContent=T.price+" · 60 dk";
    var ph=$(".pm-lab-photo",sec), im=$("[data-pm-techphoto]",sec), cap=$("[data-pm-techcap]",sec);
    if(T.photo){ ph.classList.remove("none"); im.src=T.photo; im.alt=T.n+" ile kalıcı kaş, gerçek sonuç"; cap.textContent="Gerçek sonuç · "+T.n.toLocaleLowerCase("tr-TR"); }
    else { ph.classList.add("none"); cap.textContent="Mix için ayrı bir gerçek fotoğrafımız henüz yok; şema yalnızca tekniği anlatır."; }
    draw(k); S.planOpt["pmu-kas"]=T.opt; if(byUser) updateBar(); }
  $$("[data-pm-tech]",sec).forEach(function(b){ b.addEventListener("click",function(){ pick(b.dataset.pmTech,true); }); });
  $("[data-pm-techplan]",sec).addEventListener("click",function(){ var T=PM.tech[S.pmTech||"micro"]; openPlanner("pmu-kas",T.opt,"Teknik: "+T.n); });
  sec.__pick=pick; var io=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ io.disconnect(); pick(S.pmTech||"micro"); } },{threshold:.3}); io.observe(sec); }
/* ÇİZGİ STÜDYOSU: the line is drawn over the real 'önce' eye (temsili) */
function initLineStudio(sec){ var path=$("[data-pm-liner]",sec), L=PM.liner;
  function shape(k){ var up=L.up, pts, w;
    if(k==="baby"){ pts=up.slice(3); w=[2,3,4,5,6]; } else if(k==="dip"){ pts=up; w=[3,5,7,8,9,10,10,9]; } else { pts=up.concat([L.tail]); w=[4,7,10,12,14,16,18,18,1]; }
    var a=[],b=[]; for(var i=0;i<pts.length;i++){ var p=pts[i], q=pts[Math.min(pts.length-1,i+1)], o=pts[Math.max(0,i-1)], dx=q[0]-o[0], dy=q[1]-o[1], l=Math.hypot(dx,dy)||1, nx=-dy/l, ny=dx/l, ww=(w[i]||w[w.length-1])*1.6;
      a.push([p[0]+nx*ww*.2,p[1]+ny*ww*.2]); b.push([p[0]-nx*ww,p[1]-ny*ww]); }
    function sm(P){ var d="M"+P[0][0].toFixed(1)+" "+P[0][1].toFixed(1); for(var i=1;i<P.length;i++){ var m=[(P[i-1][0]+P[i][0])/2,(P[i-1][1]+P[i][1])/2]; d+="Q"+P[i-1][0].toFixed(1)+" "+P[i-1][1].toFixed(1)+" "+m[0].toFixed(1)+" "+m[1].toFixed(1); } return d+"L"+P[P.length-1][0].toFixed(1)+" "+P[P.length-1][1].toFixed(1); }
    return sm(a)+"L"+sm(b.reverse()).slice(1)+"Z"; }
  function pick(k,byUser){ var T=PM.linerStyles[k]; if(!T) return; S.pmLiner=k; $$("[data-pm-liner-pick]",sec).forEach(function(b){ b.setAttribute("aria-pressed",b.dataset.pmLinerPick===k); });
    $("[data-pm-linername]",sec).textContent=T.n; $("[data-pm-linerp]",sec).textContent=T.p; $("[data-pm-linerprice]",sec).textContent=T.price+" · 60 dk";
    path.setAttribute("d",shape(k)); path.setAttribute("pathLength","1"); path.classList.remove("draw"); void path.getBBox; void path.offsetWidth; requestAnimationFrame(function(){ path.classList.add("draw"); });
    S.planOpt["pmu-goz"]=T.opt; if(byUser) updateBar(); }
  $$("[data-pm-liner-pick]",sec).forEach(function(b){ b.addEventListener("click",function(){ pick(b.dataset.pmLinerPick,true); }); });
  $("[data-pm-linerplan]",sec).addEventListener("click",function(){ var T=PM.linerStyles[S.pmLiner||"dip"]; openPlanner("pmu-goz",T.opt,"Çizgi: "+T.n); });
  sec.__pick=pick; var io=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ io.disconnect(); pick(S.pmLiner||"dip"); } },{threshold:.35}); io.observe(sec); }
function initPmPairs(scope){ $$("[data-pm-pair]",scope).forEach(function(el){ initCompare(el,el.dataset.intro==="1"); }); $$("[data-pm-zoom]",scope).forEach(function(b){ b.addEventListener("click",function(e){ e.stopPropagation(); var P=pmPair(b.dataset.pmZoom); openLightbox(P.file); }); }); }
function initPmWa(scope){ $$("[data-pm-wa]",scope).forEach(function(a){ a.href=waHref(a.dataset.pmWa+" "+visitCode()); }); }
function initPmSalonReviews(box){ if(!box||box.dataset.done) return; box.dataset.done=1; var list=REVIEWS.filter(function(r){ return r.f!=="pmu" && /temiz|hijyen|güven|ilgili|özenli|steril/i.test(r.t); }).slice(0,8);
  var tr=document.createElement("div"); tr.className="rv-track"; tr.style.setProperty("--dur",(list.length*9)+"s");
  var html=list.map(function(r){ return '<article class="rv"><span class="st" aria-label="5 yıldız">★★★★★</span><p>'+r.t.replace(/</g,"&lt;")+'</p><footer><b>'+r.n+'</b><span>'+months(r.d)+' · Google</span></footer></article>'; }).join("");
  tr.innerHTML=html+html.replace(/<article class="rv">/g,'<article class="rv" aria-hidden="true">'); box.appendChild(tr); }
function initPmu(v){ var sec=$("main > [data-view='"+v+"']");
  $$("[data-pm-curtain]",sec).forEach(initBrush); $$("[data-pm-film]",sec).forEach(initPmFilm); $$("[data-pm-kartela]",sec).forEach(initKartela);
  initPmPairs(sec); initPmWa(sec);
  if(v==="pmu"){ initReel($("#pmReel")); var q=$("[data-pm-quote]",sec); if(q) q.textContent=PM_REVIEW; initPmSalonReviews($("[data-pm-salon-reviews]",sec)); }
  if(v==="pmu-kas") initTechLab($("#pmTech"));
  if(v==="pmu-goz") initLineStudio($("#pmStudio"));
  $$(".pm-want",sec).forEach(function(b){ b.addEventListener("click",function(e){ e.stopPropagation(); }); }); }
function pmScroll(id){ var t=$(id); if(t) setTimeout(function(){ scrollTo({top:t.getBoundingClientRect().top+scrollY-70,behavior:"instant"}); },80); }
ROUTE_HOOK.pmu=function(p){ if(p==="fiyat") pmScroll("#pmFiyat"); };
ROUTE_HOOK["pmu-kas"]=function(p){ var sec=$("#pmTech"); var map={microblading:"micro",micro:"micro",pudra:"pudra",powder:"pudra",mix:"mix"};
  if(map[p]){ S.pmTech=map[p]; if(sec.__pick) sec.__pick(map[p]); pmScroll("#pmTech"); } else if(p==="silme"){ pmScroll("#pmSilme"); } else if(p==="fiyat"){ pmScroll("#pmKasFiyat"); } };
ROUTE_HOOK["pmu-goz"]=function(p){ var sec=$("#pmStudio"); var map={baby:"baby",babyliner:"baby",dip:"dip",dipliner:"dip",eyeliner:"eyeliner"};
  if(map[p]){ S.pmLiner=map[p]; if(sec.__pick) sec.__pick(map[p]); pmScroll("#pmStudio"); } };
"""

STORIES_ADD = r"""
STORIES["pmu-dudak"]=[{t:"Dudak",th:"m/ig/pmu-dudak-a-sonra-795.webp",fr:[{img:"m/ig/pmu-dudak-a-sonra-795.webp",cap:"Sonra"},{img:"m/ig/pmu-ton-visne-800.webp",cap:"Vişne"},{img:"m/ig/pmu-ton-gulpembe-800.webp",cap:"Gül pembe"}]},{t:"Yorumlar",th:"m/monogram.png",fr:"rv:pmu"},{t:"Fiyat",th:"m/ig/pmu-ton-gulkurusu-800.webp",fr:"price:pmu-dudak"}];
STORIES["pmu-kas"]=[{t:"Kaş",th:"m/ig/pmu-kas-makro-800.webp",fr:[{img:"m/ig/pmu-kas-makro-800.webp",cap:"Kıl tekniği"},{img:"m/ig/pmu-kas-pudra-800.webp",cap:"Pudralama"},{img:"m/ig/pmu-kas-1-800.webp",cap:"Kalıcı kaş"}]},{t:"Kalem",th:"m/ig/pmu-kalem-poster.webp",fr:[{video:"m/ig/pmu-kalem.mp4",poster:"m/ig/pmu-kalem-poster.webp",cap:"Kıl kıl çizim"}]},{t:"Fiyat",th:"m/ig/pmu-kas-2-800.webp",fr:"price:pmu-kas"}];
STORIES["pmu-goz"]=[{t:"Göz",th:"m/ig/pmu-goz-a-sonra-795.webp",fr:[{img:"m/ig/pmu-goz-a-sonra-795.webp",cap:"Sonra"},{img:"m/ig/goz-cizgisi-cift-sonra-800.webp",cap:"Dipliner"}]},{t:"Fiyat",th:"m/ig/goz-cizgisi-cift-sonra-800.webp",fr:"price:pmu-goz"}];
"""

PLANS_ADD = r"""
PLANS.pmu.opts.push({id:"silme",n:"Kalıcı kaş silme",p:3500,d:60,s:"Seans başı · plan kaş görüldükten sonra"});
PLANS["pmu-dudak"]={title:"Dudak renklendirme randevunuz",opts:[{id:"dudak",n:"Dudak renklendirme",p:9000,d:60},{id:"gorusme",n:"Ton için ön görüşme",p:null,d:null,s:"Ton birlikte seçilir"}]};
PLANS["pmu-kas"]={title:"Kalıcı kaş randevunuz",opts:[{id:"micro",n:"Microblading (kıl tekniği)",p:9000,d:60},{id:"powder",n:"Powder brows (pudralama)",p:9000,d:60},{id:"mix",n:"Mix technique",p:9000,d:60},{id:"silme",n:"Kalıcı kaş silme",p:3500,d:60,s:"Seans başı · plan kaş görüldükten sonra"},{id:"gorusme",n:"Kalıcı kaş ön görüşmesi",p:null,d:null,s:"Form ve teknik birlikte seçilir"}]};
PLANS["pmu-goz"]={title:"Kalıcı göz çizgisi randevunuz",opts:[{id:"baby",n:"Baby liner",p:5000,d:60},{id:"dipliner",n:"Dipliner",p:6000,d:60},{id:"eyeliner",n:"Eyeliner",p:7000,d:60}]};
"""


def apply(d) -> None:
    import atelier_build as build
    data = {"pairs": META["pairs"], "tones": META["tones"], "kartela": META["kartela"], "brush": BRUSH,
            "tech": TECH, "linerStyles": LINER,
            "liner": {"up": [[659, 497], [556, 450], [437, 480], [364, 591], [334, 752], [334, 927], [358, 1088], [374, 1167]], "tail": [318, 1300]}}
    review = ("Selda Gençer Beauty Center'da hem kalıcı makyaj hem de kaş ve pedikür hizmeti aldım. İşini bilen, güler yüzlü ve ilgili bir ekip vardı. "
              "Uygulamalar sırasında hem hijyen kurallarına dikkat edildi hem de kendimi çok rahat hissettim. Sonuçlar gerçekten beklentimin üstündeydi! "
              "Herkese gönül rahatlığıyla tavsiye ediyorum. Güzellikte profesyonelliği burada buldum.")
    d.css(CSS)
    d.replace_section("pmu", "\n\n".join([page_pmu(), page_dudak(), page_kas(), page_goz()]))
    js = JS.replace("__PMDATA__", json.dumps(data, ensure_ascii=False)).replace("__PMREVIEW__", review.replace('"', '\\"'))
    d.js_before_boot(js + "\n" + STORIES_ADD.strip())
    # planner: subsets, kaş silme, P.ref in the message; stories for the three sub-vitrines
    d.rep("var P={}; S.planOpt={};", PLANS_ADD.strip() + "\nvar P={}; S.planOpt={};")
    d.rep("function openPlanner(fam,opt){", "function openPlanner(fam,opt,ref){")
    d.rep("slots:sampleSlots(fam),code:P.code||visitCode()};", "slots:sampleSlots(fam),code:P.code||visitCode(),ref:ref||null};")
    d.rep('" uygun mu?"+(colorName?" Renk: "+colorName+(P.shape?", şekil: "+P.shape.toLocaleLowerCase("tr-TR"):"")+".":"")+" "+P.code;',
          '" uygun mu?"+(colorName?" Renk: "+colorName+(P.shape?", şekil: "+P.shape.toLocaleLowerCase("tr-TR"):"")+".":"")+(P.ref?" "+P.ref+".":"")+" "+P.code;')
    d.rep("'<br>Konutkent, 3028. Cd. 8A No:A1 · Çankaya</div></div>';", "(P.ref?'<br>'+P.ref:'')+'<br>Konutkent, 3028. Cd. 8A No:A1 · Çankaya</div></div>';")
    d.rep('    var pl=e.target.closest("[data-plan]"); if(pl){ openPlanner(pl.dataset.plan,pl.dataset.opt); }',
          '    var pl=e.target.closest("[data-plan]"); if(pl){ openPlanner(pl.dataset.plan,pl.dataset.opt,pl.dataset.ref); }')
    # views
    d.rep('  if(v==="pmu"){ initCompare($("#pmuCmp"),true); initCompare($("#gozCmp"),false); initTones(); initPairs("galPmu","pmu"); }',
          '  if(v.indexOf("pmu")===0){ initPmu(v); }')
    d.rep('var BAR={kas:"Kaş için saatimi seç",lifting:"Lifting için saatimi seç",pmu:"Ön görüşme · saatimi seç",cilt:"Cilt bakımı · saatimi seç"};',
          'var BAR={kas:"Kaş için saatimi seç",lifting:"Lifting için saatimi seç",pmu:"Ön görüşme · saatimi seç",cilt:"Cilt bakımı · saatimi seç","pmu-dudak":"Dudak · saatimi seç","pmu-kas":"Kalıcı kaş · saatimi seç","pmu-goz":"Göz çizgisi · saatimi seç"};')
    d.rep('  else l.textContent=BAR[v]||"Randevu · saatimi seç";',
          '  else if(v==="pmu-dudak" && S.pmTone) l.textContent=S.pmTone+" · saatimi seç";\n'
          '  else if(v==="pmu-kas" && S.pmTech) l.textContent=PM.tech[S.pmTech].n+" · saatimi seç";\n'
          '  else if(v==="pmu-goz" && S.pmLiner) l.textContent=PM.linerStyles[S.pmLiner].n+" · saatimi seç";\n'
          '  else l.textContent=BAR[v]||"Randevu · saatimi seç";')
    # live strip label for the sub views
    d.rep('{kas:"kaş",tirnak:"tırnak",kirpik:"ipek kirpik",lifting:"lifting",pmu:"kalıcı makyaj",cilt:"cilt bakımı",lazer:"lazer"}',
          '{kas:"kaş",tirnak:"tırnak",kirpik:"ipek kirpik",lifting:"lifting",pmu:"kalıcı makyaj",cilt:"cilt bakımı",lazer:"lazer","pmu-dudak":"dudak renklendirme","pmu-kas":"kalıcı kaş","pmu-goz":"göz çizgisi"}')
    # stories (pmu) without the removed files; keep frames tall
    d.sub(r' pmu:\[\{t:"Dudak",th:"m/ig/dudak-cift-1-sonra-800\.webp".*?\{t:"Fiyat",th:"m/ig/dudak-2-800\.webp",fr:"price:pmu"\}\],\n',
          ' pmu:[{t:"Dudak",th:"m/ig/pmu-dudak-a-sonra-795.webp",fr:[{img:"m/ig/pmu-dudak-a-sonra-795.webp",cap:"Sonra · dudak renklendirme"},{img:"m/ig/pmu-ton-visne-800.webp",cap:"Vişne"},{img:"m/ig/pmu-ton-gulpembe-800.webp",cap:"Gül pembe"}]},\n'
          '      {t:"Kaş",th:"m/ig/pmu-kas-makro-800.webp",fr:[{img:"m/ig/pmu-kas-makro-800.webp",cap:"Kıl tekniği"},{img:"m/ig/pmu-kas-1-800.webp",cap:"Kalıcı kaş"}]},\n'
          '      {t:"Göz",th:"m/ig/pmu-goz-a-sonra-795.webp",fr:[{img:"m/ig/pmu-goz-a-sonra-795.webp",cap:"Sonra · eyeliner"},{img:"m/ig/goz-cizgisi-cift-sonra-800.webp",cap:"Dipliner"}]},\n'
          '      {t:"Kalem",th:"m/ig/pmu-kalem-poster.webp",fr:[{video:"m/ig/pmu-kalem.mp4",poster:"m/ig/pmu-kalem-poster.webp",cap:"Kıl kıl çizim"}]},\n'
          '      {t:"Yorumlar",th:"m/monogram.png",fr:"rv:pmu"},\n'
          '      {t:"Fiyat",th:"m/ig/pmu-ton-gulkurusu-800.webp",fr:"price:pmu"}],\n')
    # salon tile + mosaic: the PMU tile shows the new hero pair's sonra half
    d.rep('<a class="tile" href="#pmu" data-go="pmu"><img src="m/ig/dudak-1-800.webp"', '<a class="tile" href="#pmu" data-go="pmu"><img src="m/ig/pmu-ton-visne-800.webp"')
    build.nav_map(d, {"kalici-makyaj": "pmu", "dudak-renklendirme": "pmu-dudak", "microblading": "pmu-kas/micro", "powder-brows": "pmu-kas/pudra",
                      "mix-brows": "pmu-kas/mix", "eyeliner": "pmu-goz/eyeliner", "dipliner": "pmu-goz/dipliner", "babyliner": "pmu-goz/baby",
                      "kas-silme": "pmu-kas/silme", "kalici-makyaj-fiyatlari": "pmu/fiyat", "microblading-fiyatlari": "pmu-kas/fiyat"})
    build.proto_views(d, [("pmu-dudak", "▸ dudak"), ("pmu-kas", "▸ kaş"), ("pmu-goz", "▸ göz")], "pmu")
    paths = {p["file"] for p in META["pairs"].values()} | {META["kartela"]["file"], META["oda"]["file"]}
    paths |= {"m/ig/pmu-dudak-a-sonra-795.webp", "m/ig/pmu-ton-visne-800.webp", "m/ig/pmu-ton-gulpembe-800.webp", "m/ig/pmu-ton-gulkurusu-800.webp",
              "m/ig/pmu-kas-makro-800.webp", "m/ig/pmu-kas-pudra-800.webp", "m/ig/pmu-kas-1-800.webp", "m/ig/pmu-kas-2-800.webp",
              "m/ig/pmu-goz-a-sonra-795.webp", "m/ig/goz-cizgisi-cift-sonra-800.webp", "m/ig/pmu-kalem.mp4", "m/ig/pmu-kalem-poster.webp",
              "m/ig/dudak-1-800.webp", "m/ig/dudak-2-800.webp"}
    paths |= {f"m/ig/film/pmu-kalem/a{k}.webp" for k in range(1, 7)}
    d.rep("/* ---------- v4 · PMU şölen ---------- */\nvar PM=", "/*@media " + json.dumps(sorted(paths)) + " @*/\n/* ---------- v4 · PMU şölen ---------- */\nvar PM=")
