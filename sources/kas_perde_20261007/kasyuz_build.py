#!/usr/bin/env python3
"""K1: kaş alımı "Beş Perde" — yayındaki Artifact HTML'ine sayılı değişiklikler."""
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
h = open(src, encoding="utf-8").read()


def rep(old, new, count=1):
    global h
    n = h.count(old)
    assert n == count, f"{n} != {count}: {old[:80]!r}"
    h = h.replace(old, new)


# ---------- CSS ----------
CSS = """/* ---------- kaş: beş perde ---------- */
.perde{position:relative;height:calc(var(--n) * 62svh + 100svh)}
.perde-stage{position:sticky;top:var(--nav-h);height:calc(100svh - var(--nav-h));display:grid;align-content:center;gap:16px;padding-block:18px;max-width:1120px;margin-inline:auto}
.perde-head{display:grid;gap:8px}
.perde-head h2{font-family:var(--display);font-weight:400;font-size:clamp(32px,6.4vw,50px);line-height:1;margin:0;text-wrap:balance}
.perde-head h2 em{font-style:italic;color:#F4E6BE}
.perde-frame{position:relative;width:min(100%,calc(52svh * 1200 / 552));aspect-ratio:1200/552;max-width:100%;border-radius:20px;overflow:hidden;border:1px solid rgba(233,215,165,.25);box-shadow:0 30px 80px -30px rgba(0,0,0,.8);background:#1A1713}
.perde-shot{margin:0}
.perde-frame .perde-shot{position:absolute;inset:0;opacity:0;will-change:opacity,clip-path}
.perde-frame .perde-shot:first-child{opacity:1}
.perde-shot img{width:100%;height:100%;object-fit:cover}
.perde-shot figcaption{display:none}
.perde-tag{position:absolute;left:12px;top:12px;font:600 10.5px/1 var(--body);letter-spacing:.18em;text-transform:uppercase;padding:7px 10px;border-radius:999px;background:rgba(14,13,12,.62);color:#F4E6BE;border:1px solid rgba(233,215,165,.35)}
.perde-seam{position:absolute;top:0;bottom:0;left:0;width:2px;margin-left:-1px;z-index:3;background:linear-gradient(#F6EACB,#C9A55C);box-shadow:0 0 16px rgba(244,230,190,.95);opacity:0;pointer-events:none}
.perde-dots{display:flex;gap:6px;margin:0;padding:0;list-style:none;width:min(100%,calc(52svh * 1200 / 552))}
.perde-dots li{flex:1;height:2px;border-radius:2px;background:rgba(247,241,228,.2);transition:background .4s var(--ease)}
.perde-dots li.on{background:#F4E6BE;box-shadow:0 0 10px rgba(244,230,190,.7)}
.perde-cap{display:grid;gap:6px;min-height:7.6em;align-content:start;transition:opacity .3s var(--ease),transform .3s var(--ease)}
.perde-cap.out{opacity:0;transform:translateY(6px)}
.perde-cap .n,.perde-shot figcaption .n{font:600 11px/1 var(--body);letter-spacing:.22em;text-transform:uppercase;color:#EBD49A}
.perde-cap .t,.perde-shot figcaption .t{font-family:var(--display);font-weight:400;font-size:clamp(28px,6vw,42px);line-height:1;text-wrap:balance}
.perde-cap .s,.perde-shot figcaption .s{color:#E2D8C5;font-size:15px;max-width:56ch;margin:0}
.perde-note{font-size:12px;color:#C3B8A1;margin:0;max-width:70ch}
html[data-tier="C"] .perde{height:auto}
html[data-tier="C"] .perde-stage{position:static;height:auto;gap:22px}
html[data-tier="C"] .perde-frame{width:100%;aspect-ratio:auto;overflow:visible;border:0;box-shadow:none;background:none;border-radius:0;display:grid;gap:26px}
html[data-tier="C"] .perde-frame .perde-shot{position:relative;inset:auto;opacity:1}
html[data-tier="C"] .perde-shot img{height:auto;aspect-ratio:1200/552;border-radius:16px}
html[data-tier="C"] .perde-shot figcaption{display:grid;gap:6px;margin-top:12px}
html[data-tier="C"] .perde-seam,html[data-tier="C"] .perde-dots,html[data-tier="C"] .perde-cap{display:none}
.perde-final{display:grid;gap:22px;align-items:center}
.perde-final figure{margin:0;position:relative;border-radius:22px;overflow:hidden;aspect-ratio:4/5;max-width:380px;border:1px solid rgba(233,215,165,.25);box-shadow:0 30px 80px -30px rgba(0,0,0,.8)}
.perde-final figure img{width:100%;height:100%;object-fit:cover}
.perde-final h2{font-family:var(--display);font-weight:400;font-size:clamp(34px,7vw,52px);line-height:1;margin:0;text-wrap:balance}
.perde-final h2 em{font-style:italic;color:#F4E6BE}
.perde-final .copy{display:grid;gap:14px;min-width:0}
.perde-final .steps-mini{color:#E2D8C5}
@media (min-width:860px){.perde-final{grid-template-columns:minmax(0,380px) minmax(0,1fr);gap:56px}.perde-final .btn-gold{width:auto;max-width:340px;justify-self:start;padding:0 30px}}

/* ---------- golden mirror ---------- */"""
rep("/* ---------- golden mirror ---------- */", CSS)

# Ayna: etiketsiz kırpım (kas-perde-alim = kas-kina sonra, üst %69). SVG y'leri +17 (eski cover ofseti).
rep(".golden-fig{position:relative;border-radius:22px;overflow:hidden;aspect-ratio:800/500;",
    ".golden-fig{position:relative;border-radius:22px;overflow:hidden;aspect-ratio:800/368;")

# ---------- HTML: beş perde ----------
PERDE = [
    # (dosya, mod, adım, etiket, alt, başlık-n, başlık-t, başlık-s)
    ("okuma", "fade", 0, "Önce", "Altın oran kaş alımı öncesi, dağınık kabarık kaş",
     "01 / 05 · Okuma", "Önce bakarız.",
     "Kaşın nerede başladığına, nerede bittiğine ve yüzünüzde nasıl durduğuna birlikte bakarız."),
    ("harita", "fade", 1, "Haritalama", "Kaş çevresinde beyaz çizimle işaretlenmiş alım alanı",
     "02 / 05 · Haritalama", "Çizgiyi belirleriz.",
     "Başlangıç, kavis ve bitiş yüz hatlarınıza göre işaretlenir. Beyaz çizim, alınacak alanı gösterir."),
    ("alim", "sweep", 2, "Sonra · aynı kaş", "Haritalanan kaşın alım sonrası temiz, düzenli hâli",
     "03 / 05 · Alım", "Dağınıklığı toplarız.",
     "İp ve cımbızla yalnız çizginin dışı alınır; dolu duran kısım korunur."),
    ("sonuc", "fade", 3, "Sonra · 01'deki kaş", "Altın oranla şekillendirilmiş kaş, ilk perdedeki danışan",
     "04 / 05 · Sonuç", "Yüzünüze göre.",
     "Altın oran ölçü verir; son şekli yüzünüz belirler."),
    ("gur-once", "fade", 4, "Önce", "Gür ve dağınık kaş, alım öncesi", None, None, None),
    ("gur", "sweep", 4, "Sonra", "Gür kaşın doğal doluluğu korunarak toparlanmış hâli",
     "05 / 05 · Gür kaşlar", "İncelmeden toparlanır.",
     "Gür kaşta da amaç inceltmek değil; dağınık kıllar alınır, doğal doluluk kalır."),
]


def cap_html(n, t, s):
    return f'<span class="n">{n}</span><span class="t">{t}</span><p class="s">{s}</p>'


shots = []
for i, (f, mode, step, tag, alt, n, t, s) in enumerate(PERDE):
    load = 'fetchpriority="low"' if i == 0 else 'loading="lazy"'
    fc = f"<figcaption>{cap_html(n, t, s)}</figcaption>" if n else ""
    shots.append(
        f'        <figure class="perde-shot" data-step="{step}" data-mode="{mode}">'
        f'<img src="m/ig/kas-perde-{f}-1200.webp" srcset="m/ig/kas-perde-{f}-800.webp 800w, m/ig/kas-perde-{f}-1200.webp 1200w" '
        f'sizes="(min-width:1160px) 1120px, 100vw" alt="{alt}" width="1200" height="552" {load} decoding="async">'
        f'<span class="perde-tag">{tag}</span>{fc}</figure>'
    )
first = PERDE[0]
SECTION = f"""
  <div class="perde dark-band gutter" id="perde" style="--n:{len(PERDE)}">
    <div class="perde-stage">
      <div class="perde-head">
        <span class="eyebrow">Bir kaş, beş perde</span>
        <h2>Kaydırın, <em>kaş</em> şekillensin.</h2>
      </div>
      <div class="perde-frame">
{chr(10).join(shots)}
        <span class="perde-seam" aria-hidden="true"></span>
      </div>
      <ol class="perde-dots" aria-hidden="true"><li class="on"></li><li></li><li></li><li></li><li></li></ol>
      <div class="perde-cap" aria-live="polite">{cap_html(*first[5:])}</div>
      <p class="perde-note">Kareler salonumuzda yapılan gerçek işlemlerden; yalnız kırpıldı, rötuş yok. 01 ile 04 aynı danışan, 02 ile 03 aynı danışan.</p>
    </div>
  </div>
"""
rep('        <div class="rings" data-rings="kas"></div>\n      </div>\n    </div>\n  </div>\n',
    '        <div class="rings" data-rings="kas"></div>\n      </div>\n    </div>\n  </div>\n' + SECTION)

# ---------- HTML: Ayna görseli ve SVG ----------
OLD_FIG = """        <img src="m/ig/kas-kina-sonra-800.webp" alt="Altın oran ölçü çizgileriyle kaş, salonumuzda yapıldı" width="800" height="534" loading="lazy">
        <svg viewBox="0 0 800 500" aria-hidden="true">"""
NEW_FIG = """        <img src="m/ig/kas-perde-alim-800.webp" alt="Altın oran ölçü çizgileriyle kaş, salonumuzda yapıldı" width="800" height="368" loading="lazy">
        <svg viewBox="0 0 800 368" aria-hidden="true">"""
rep(OLD_FIG, NEW_FIG)
for a, b in [
    ('d="M830 900 L715 194"', 'd="M830 917 L715 211"'),
    ('d="M830 900 L452 59"', 'd="M830 917 L452 76"'),
    ('d="M830 900 L-17 224"', 'd="M830 917 L-17 241"'),
    ('<circle class="g-ring d1" cx="722" cy="238" r="13"/><circle class="g-ring d2" cx="470" cy="100" r="13"/><circle class="g-ring d3" cx="18" cy="252" r="13"/>',
     '<circle class="g-ring d1" cx="722" cy="255" r="13"/><circle class="g-ring d2" cx="470" cy="117" r="13"/><circle class="g-ring d3" cx="18" cy="269" r="13"/>'),
    ('<circle class="g-dot d1" cx="722" cy="238" r="9"/><circle class="g-dot d2" cx="470" cy="100" r="9"/><circle class="g-dot d3" cx="18" cy="252" r="9"/>',
     '<circle class="g-dot d1" cx="722" cy="255" r="9"/><circle class="g-dot d2" cx="470" cy="117" r="9"/><circle class="g-dot d3" cx="18" cy="269" r="9"/>'),
    ('<text class="g-lbl d1" x="760" y="296" text-anchor="end">BAŞLANGIÇ</text>', '<text class="g-lbl d1" x="760" y="313" text-anchor="end">BAŞLANGIÇ</text>'),
    ('<text class="g-lbl d2" x="494" y="74">KAVİS</text>', '<text class="g-lbl d2" x="494" y="91">KAVİS</text>'),
    ('<text class="g-lbl d3" x="24" y="306">BİTİŞ</text>', '<text class="g-lbl d3" x="24" y="323">BİTİŞ</text>'),
]:
    rep(a, b)
# 1:1,618 yazısı yeni yükseklikte alt kenara
kas_start = h.index('<section data-view="kas"')
kas_end = h.index("</section>", kas_start)
seg = h[kas_start:kas_end]
assert seg.count('<text class="g-ratio" x="24" y="482">') == 1
seg = seg.replace('<text class="g-ratio" x="24" y="482">', '<text class="g-ratio" x="24" y="62">')

# ---------- HTML: kapanış perdesi (kaş davetiye bloğunun yerine) ----------
m = re.search(r'\n  <div class="sec gutter">\n    <div class="invite-teaser">.*?\n    </div>\n  </div>\n', seg, re.S)
assert m and seg.count('class="invite-teaser"') == 1
FINAL = """
  <div class="sec dark-band gutter">
    <div class="perde-final">
      <figure class="lit"><img src="m/ig/kas-profil-4x5-800.webp" alt="Altın oranla şekillendirilmiş kaş, yandan yakın çekim, salonumuzda yapıldı" width="800" height="999" loading="lazy" decoding="async"></figure>
      <div class="copy">
        <span class="eyebrow">Aynada ilk bakış</span>
        <h2>Kaşınız, <em>yüzünüze</em> göre.</h2>
        <p class="s" style="margin:0;color:#E2D8C5;max-width:46ch">30 dakika. İlk deneyimde altın oran kaş alımı 500 TL. Davetiyeniz üç dokunuşta hazır.</p>
        <div class="steps-mini"><span>1 · İşlem</span><span>2 · Gün ve saat</span><span>3 · Davetiye → WhatsApp</span></div>
        <button class="btn-gold shine" data-plan="kas" data-opt="ilk" data-track-label="at-kas-perde-davetiye"><span class="lbl">Saatimi seç</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
      </div>
    </div>
  </div>
"""
seg = seg[: m.start()] + FINAL + seg[m.end():]
h = h[:kas_start] + seg + h[kas_end:]

# ---------- JS ----------
JS = r"""function initPerde(){ var sec=$("#perde"); if(!sec) return;
  var shots=$$(".perde-shot",sec), seam=$(".perde-seam",sec), cap=$(".perde-cap",sec), dots=$$(".perde-dots li",sec), N=shots.length, cur=0, caps={};
  shots.forEach(function(s){ var fc=$("figcaption",s); if(fc) caps[s.dataset.step]=fc.innerHTML; });
  function update(){
    if(S.view!=="kas"||S.tier==="C") return;
    var r=sec.getBoundingClientRect(), vh=innerHeight, total=r.height-vh; if(total<=0||r.bottom<0||r.top>vh) return;
    var p=Math.min(1,Math.max(0,-r.top/total)), x=Math.min(N-1e-4,p*N), i=Math.floor(x), t=x-i, f=i===0?1:Math.min(1,t/.5); f=f*f*(3-2*f);
    shots.forEach(function(s,k){ var sw=s.dataset.mode==="sweep";
      if(k<i){ s.style.opacity=1; s.style.clipPath="none"; }
      else if(k===i){ if(sw){ s.style.opacity=1; s.style.clipPath="inset(0 "+((1-f)*100).toFixed(2)+"% 0 0)"; } else { s.style.opacity=f.toFixed(3); s.style.clipPath="none"; } }
      else { s.style.opacity=0; } });
    var sweeping=shots[i].dataset.mode==="sweep"&&f<1; seam.style.opacity=sweeping?1:0; seam.style.left=(f*100).toFixed(2)+"%";
    var st=+shots[i].dataset.step; dots.forEach(function(d,j){ d.classList.toggle("on",j<=st); });
    if(st!==cur && caps[st]){ cur=st; cap.classList.add("out"); setTimeout(function(){ cap.innerHTML=caps[cur]; cap.classList.remove("out"); },140); }
  }
  scrollers.push(update); update();
}
function initGolden(){"""
rep("function initGolden(){", JS)
rep('if(v==="kas"){ initCompare($("#kasCmp"),true); initGolden(); initKasGallery(); }',
    'if(v==="kas"){ initCompare($("#kasCmp"),true); initPerde(); initGolden(); initKasGallery(); }')

assert "kas-cift-3" not in h
open(dst, "w", encoding="utf-8").write(h)
print("ok", len(h))
