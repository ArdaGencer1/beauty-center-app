#!/usr/bin/env python3
"""Kaş sayfası mobil iyileştirmeleri. kasyuz_build.py uygulanmış yayındaki HTML'e uygulanır.

- Hero: telefonda etiketsiz kırpım (<picture>, en çok 699px), 16:10; masaüstü değişmez.
- Beş Perde: telefonda kenardan kenara 1.8:1 kare, sabit çubuğun üstünde ortalı sahne,
  daha kısa kaydırma; adım çubukları dokunulabilir (adıma atlar, 44px dokunma alanı).
- Galeri: kaş kartları etiketsiz kırpımlar, 2:1 oran; kart etiketleri 11px.
- Kapanış: telefonda görsel yüksekliği sınırlı, başlık ilk ekranda.
- SSS (kaş): başlık dokunma alanı 44px.
Kullanım: python3 kasyuz_mobile.py GIRIS.html CIKIS.html
"""
import sys

src, dst = sys.argv[1], sys.argv[2]
h = open(src, encoding="utf-8").read()


def rep(old, new, count=1):
    global h
    n = h.count(old)
    assert n == count, f"{n} != {count}: {old[:90]!r}"
    h = h.replace(old, new)


assert 'id="perde"' in h and "kasyuz-mobile" not in h, "önce kasyuz_build.py; ikinci kez uygulanmaz"

# ---------- CSS ----------
rep("/* ---------- golden mirror ---------- */", """/* ---------- kaş: mobil (kasyuz-mobile) ---------- */
.perde-dots button{flex:1;height:44px;margin:-21px 0;padding:0;border:0;background:none;cursor:pointer;position:relative}
.perde-dots button::before{content:"";position:absolute;left:0;right:0;top:50%;height:2px;margin-top:-1px;border-radius:2px;background:rgba(247,241,228,.2);transition:background .4s var(--ease),box-shadow .4s var(--ease)}
.perde-dots li.on button::before{background:#F4E6BE;box-shadow:0 0 10px rgba(244,230,190,.7)}
.perde-dots li,.perde-dots li.on{background:none;box-shadow:none;display:flex;height:2px}
.perde-shot img{object-position:var(--fx,50%) 50%}
#galKas .gcard.wide{aspect-ratio:2/1}
#galKas .gcard .gl{font-size:11px}
[data-view="kas"] .faq details{padding:6px 0}
[data-view="kas"] .faq summary{min-height:44px;align-items:center}
@media (max-width:699px){
  .hero-kas .cmp{aspect-ratio:16/10}
  .hero-kas .cmp img{object-position:55% 50%}
  .perde{height:calc(var(--n) * 46svh + 100svh)}
  .perde-stage{height:calc(100svh - var(--nav-h) - var(--bar-h));gap:12px;padding-block:8px}
  .perde-frame{width:auto;margin-inline:calc(-1 * var(--gutter));aspect-ratio:1.8;border-radius:0;border-inline:0}
  .perde-dots{width:100%}
  .perde-cap{min-height:8.4em}
  .perde-cap .t{font-size:clamp(28px,8.4vw,36px)}
  .perde-note{font-size:11.5px}
  .perde-final figure{width:min(100%,calc(44svh * .8))}
  html[data-tier="C"] .perde-frame{margin-inline:0}
}

/* ---------- golden mirror ---------- */""")

# ---------- Hero: telefonda etiketsiz kırpım ----------
rep('<img class="cmp-b" src="m/ig/kas-altin-oran-once-1200.webp"',
    '<picture><source media="(max-width:699px)" srcset="m/ig/kas-perde-okuma-800.webp 800w, m/ig/kas-perde-okuma-1200.webp 1200w" sizes="100vw">'
    '<img class="cmp-b" src="m/ig/kas-altin-oran-once-1200.webp"')
rep('alt="Önce: altın oran kaş alımı öncesi" width="1200" height="800" fetchpriority="high">',
    'alt="Önce: altın oran kaş alımı öncesi" width="1200" height="800" fetchpriority="high"></picture>')
rep('<img class="cmp-a" src="m/ig/kas-altin-oran-sonra-1200.webp"',
    '<picture><source media="(max-width:699px)" srcset="m/ig/kas-perde-sonuc-800.webp 800w, m/ig/kas-perde-sonuc-1200.webp 1200w" sizes="100vw">'
    '<img class="cmp-a" src="m/ig/kas-altin-oran-sonra-1200.webp"')
rep('alt="Sonra: altın oranla şekillendirilmiş kaş" width="1200" height="800">',
    'alt="Sonra: altın oranla şekillendirilmiş kaş" width="1200" height="800"></picture>')

# ---------- Beş Perde: kadraj odağı ve dokunulabilir adımlar ----------
for f, fx in [("okuma", "40%"), ("harita", "50%"), ("alim", "50%"), ("sonuc", "62%"), ("gur-once", "50%"), ("gur", "50%")]:
    rep(f'<img src="m/ig/kas-perde-{f}-1200.webp"', f'<img style="--fx:{fx}" src="m/ig/kas-perde-{f}-1200.webp"')
names = ["Okuma", "Haritalama", "Alım", "Sonuç", "Gür kaşlar"]
dots = "".join(
    f'<li{" class=\"on\"" if i == 0 else ""}><button type="button" data-perde-go="{i}" aria-label="{i + 1}. adım: {n}"></button></li>'
    for i, n in enumerate(names)
)
rep('<ol class="perde-dots" aria-hidden="true"><li class="on"></li><li></li><li></li><li></li><li></li></ol>',
    f'<ol class="perde-dots">{dots}</ol>')
rep("""    if(st!==cur && caps[st]){ cur=st; cap.classList.add("out"); setTimeout(function(){ cap.innerHTML=caps[cur]; cap.classList.remove("out"); },140); }
  }
  scrollers.push(update); update();""",
    """    if(st!==cur && caps[st]){ cur=st; cap.classList.add("out"); setTimeout(function(){ cap.innerHTML=caps[cur]; cap.classList.remove("out"); },140); }
  }
  $$("[data-perde-go]",sec).forEach(function(b){ lbl(b,"at-kas-perde-adim"); b.addEventListener("click",function(){
    var st=+b.dataset.perdeGo, k=-1; shots.forEach(function(s,j){ if(+s.dataset.step===st) k=j; });
    var total=sec.offsetHeight-innerHeight, top=sec.getBoundingClientRect().top+scrollY;
    scrollTo({top:Math.round(top+total*Math.min(1,(k+.75)/N)),behavior:S.tier==="A"?"smooth":"auto"}); }); });
  scrollers.push(update); update();""")
rep('var st=+shots[i].dataset.step; dots.forEach(function(d,j){ d.classList.toggle("on",j<=st); });',
    'var st=+shots[i].dataset.step; dots.forEach(function(d,j){ d.classList.toggle("on",j<=st); $("button",d).setAttribute("aria-current",j===st?"step":"false"); });')

# ---------- Galeri: etiketsiz kırpımlar ----------
rep('KAS_PAIRS=[["kas-cift-2","Kaş alımı"],["kas-kina","Altın oran · kına"],["kas-laminasyon","Kaş laminasyonu"]]',
    'KAS_PAIRS=[["kas-perde-gur","Kaş alımı","kas-perde-gur-once"],["kas-perde-alim","Altın oran · kına","kas-perde-harita"],["kas-laminasyon-sonra","Kaş laminasyonu","kas-laminasyon-once"]]')
rep('function initKasGallery(){ var g=$("#galKas"); KAS_PAIRS.forEach(function(p){ card(g,"m/ig/"+p[0]+"-sonra-800.webp","m/ig/"+p[0]+"-once-800.webp",p[1],true); }); }',
    'function initKasGallery(){ var g=$("#galKas"); KAS_PAIRS.forEach(function(p){ card(g,"m/ig/"+p[0]+"-800.webp","m/ig/"+p[2]+"-800.webp",p[1],true); }); }')

open(dst, "w", encoding="utf-8").write(h)
print("ok", len(h))
