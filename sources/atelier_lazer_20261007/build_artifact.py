#!/usr/bin/env python3
"""Build the canonical Atelier site while preserving Artifact v3 for rollback."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATCH = Path(__file__).resolve().parent
ARTIFACT_DIR = ROOT / "prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM"
SOURCE = ARTIFACT_DIR / "artifact-v3.html"
CURRENT = ARTIFACT_DIR / "artifact-current.html"
WEBSITE = ROOT / "website/index.html"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    sys.path.insert(0, str(PATCH))
    import render  # noqa: PLC0415

    html = SOURCE.read_text(encoding="utf-8")

    # Artifact v3 closed <head> before its title and font links. Keep all metadata
    # in a valid head and add a useful description for the canonical repo page.
    bootstrap_end = "</style></head><body>\n<title>Selda Gençer Atelier</title>\n"
    head_end = (
        "</style>\n<title>Selda Gençer Beauty Center · Atelier</title>\n"
        '<meta name="description" content="Konutkent Çankaya’da kaş, tırnak, kirpik, kalıcı makyaj, cilt bakımı ve lazer epilasyon.">\n'
        '<meta name="theme-color" content="#0B0909">\n'
    )
    html = replace_once(html, bootstrap_end, head_end, "document head")
    html = html.replace("<html><head>", '<html lang="tr"><head>', 1)

    # Later review decisions override the legacy manifest selections.
    html = html.replace("m/ig/kas-cift-3-sonra-800.webp", "m/ig/kas-profil-800.webp")
    html = html.replace(
        '["kas-cift-2","Kaş alımı"],["kas-cift-3","Kaş tasarımı"],',
        '["kas-cift-2","Kaş alımı"],',
    )
    html = html.replace("m/ig/cilt-yarim-1-1200.webp", "m/ig/cilt-led-poster.webp")
    html = html.replace(
        "Cilt bakımı: yüzün sol yarısı bakım öncesi, sağ yarısı bakım sonrası",
        "LED ışık terapisi, salonumuzda çekildi",
    )
    html = html.replace(
        '["cilt-yarim-1","Cilt bakımı, önce ve sonra"]',
        '["cilt-led","LED ışık terapisi"]',
    )
    old_gallery = (
        'cilt:[["akne-cift-1","Akne bakımı","pair"],["akne-cift-2","Akne bakımı","pair"],'
        '["cilt-cift-1","Cilt bakımı","pair480"],["cilt-cift-3","Leke bakımı","pair480"],'
        '["cilt-cift-4","Nem ve parlaklık","pair480"],["cilt-cift-5","Kızarıklık bakımı","pair480"],'
        '["cilt-yarim-2","Yarım yüz","one"],["cilt-islem","Maske uygulaması","one"]],'
    )
    new_gallery = (
        'cilt:[["akne-cift-1","Akne bakımı","pair"],["akne-cift-2","Akne bakımı","pair"],'
        '["cilt-cift-1","Cilt bakımı","pair480"]],'
    )
    html = replace_once(html, old_gallery, new_gallery, "Cilt gallery")
    old_stories = (
        'cilt:[{t:"Yarım yüz",th:"m/ig/cilt-yarim-1-800.webp",fr:[{img:"m/ig/cilt-led-poster.webp",cap:"Solda önce, sağda sonra"},{img:"m/ig/cilt-yarim-2-800.webp",cap:"Bakım sonrası ışıltı"}]},\n'
        '      {t:"LED",th:"m/ig/cilt-led-poster.webp",fr:[{video:"m/ig/cilt-led.mp4",poster:"m/ig/cilt-led-poster.webp",cap:"LED ışık terapisi"},{video:"m/ig/cilt-video-3.mp4",poster:"m/ig/cilt-video-3-poster.webp",cap:"LED kubbe"}]},\n'
        '      {t:"Akne",th:"m/ig/akne-cift-1-sonra-800.webp",fr:[{img:"m/ig/akne-cift-1-once-800.webp",cap:"Önce"},{img:"m/ig/akne-cift-1-sonra-800.webp",cap:"Sonra"}]},\n'
        '      {t:"Yorumlar",th:"m/monogram.png",fr:"rv:cilt"},\n'
        '      {t:"Fiyat",th:"m/ig/cilt-yarim-2-800.webp",fr:"price:cilt"}],'
    )
    new_stories = (
        'cilt:[{t:"LED",th:"m/ig/cilt-led-poster.webp",fr:[{video:"m/ig/cilt-led.mp4",poster:"m/ig/cilt-led-poster.webp",cap:"LED ışık terapisi"},{video:"m/ig/cilt-video-3.mp4",poster:"m/ig/cilt-video-3-poster.webp",cap:"LED kubbe"}]},\n'
        '      {t:"Akne",th:"m/ig/akne-cift-1-sonra-800.webp",fr:[{img:"m/ig/akne-cift-1-once-800.webp",cap:"Önce"},{img:"m/ig/akne-cift-1-sonra-800.webp",cap:"Sonra"}]},\n'
        '      {t:"Yorumlar",th:"m/monogram.svg",fr:"rv:cilt"},\n'
        '      {t:"Fiyat",th:"m/ig/cilt-led-poster.webp",fr:"price:cilt"}],'
    )
    html = replace_once(html, old_stories, new_stories, "Cilt stories")
    html = html.replace("m/monogram.png", "m/monogram.svg")

    # Artifact-only placeholder files were never archived. Point those frames to
    # the verified salon media set so the canonical page has no dead assets.
    salon_replacements = {
        "m/walk-06.webp": "m/ig/salon-merdiven-800.webp",
        "m/walk-07.webp": "m/ig/salon-lobi-2-800.webp",
        "m/walk-08.webp": "m/ig/salon-giris-poster.webp",
        "m/walk-09.webp": "m/ig/salon-lobi-800.webp",
        "m/walk-10.webp": "m/ig/salon-resepsiyon-800.webp",
        "m/cert-wall.webp": "m/ig/salon-lobi-2-800.webp",
        "m/cert-trophy.webp": "m/ig/salon-resepsiyon-800.webp",
        "Salondaki sertifika duvarı": "Salonumuzun iç mekânı",
        "Sertifika duvarı": "Salonumuz",
        "Altın kalp ödülü": "Salon resepsiyonu",
        "Ödül": "Resepsiyon",
    }
    for old, new in salon_replacements.items():
        html = html.replace(old, new)

    laser_html = render.page_html(
        "hub",
        "m/ig/",
        "Ankara Lazer Epilasyon: Konutkent ve Çayyolu Yakınında Bölge Planı",
        lambda key: "https://seldagencerbeauty.com/" + render.PAGES[key]["slug"],
    )
    laser_data = json.dumps(
        render.page_data("hub", "m/ig/", False),
        ensure_ascii=False,
        separators=(",", ":"),
    ).replace("</", "<\\/")
    new_laser = (
        '<!-- ===================== LAZER EPİLASYON · GELİŞMİŞ BİRLEŞİK SÜRÜM ===================== -->\n'
        '<section data-view="lazer" hidden>\n'
        f"{laser_html}\n"
        f'<script id="lz-data" type="application/json">{laser_data}</script>\n'
        "</section>"
    )
    laser_pattern = re.compile(
        r"<!-- ===================== LAZER EPİLASYON ===================== -->\s*"
        r'<section data-view="lazer" hidden>.*?</section>\s*</main>',
        re.DOTALL,
    )
    html, count = laser_pattern.subn(new_laser + "\n</main>", html, count=1)
    if count != 1:
        raise RuntimeError(f"laser section: expected one match, found {count}")

    css = (PATCH / "src/lazer.css").read_text(encoding="utf-8")
    css_marker = '</style>\n\n<div class="wrap" lang="tr">'
    html = replace_once(
        html,
        css_marker,
        "\n/* BEGIN GENERATED ADVANCED LASER CSS */\n"
        + css
        + '\n/* END GENERATED ADVANCED LASER CSS */\n</style>\n</head><body>\n\n<div class="wrap" lang="tr">',
        "laser CSS insertion",
    )

    html = replace_once(
        html,
        'if(v==="lazer"){ initRegions(); initPairs("galLazer","lazer"); }',
        'if(v==="lazer"){ /* Advanced laser mounts after shared boot. */ }',
        "legacy laser initializer",
    )
    old_bar = '$("#barCta").addEventListener("click",function(){ openPlanner(S.view,S.planOpt[S.view]); });'
    new_bar = (
        '$("#barCta").addEventListener("click",function(){ '
        'var lr=document.querySelector(".lz[data-lz-page]"); '
        'if(S.view==="lazer"&&lr&&window.ATLZ){ window.ATLZ.plan(lr); } '
        'else openPlanner(S.view,S.planOpt[S.view]); });'
    )
    html = replace_once(html, old_bar, new_bar, "bottom bar handler")

    laser_js = (PATCH / "src/lazer.js").read_text(encoding="utf-8")
    adapter = r'''
/* BEGIN GENERATED ADVANCED LASER JS */
window.ATLZ_NOAUTO=true;
'''+ laser_js + r'''
(function mountMergedLaser(){
  function mount(){
    var r=document.querySelector(".lz[data-lz-page]");
    if(!r||!window.ATLZ) return;
    window.ATLZ.mount(r,{
      data:JSON.parse(document.getElementById("lz-data").textContent),
      noFetch:true,
      menu:function(){var b=document.getElementById("menuBtn");if(b)b.click();},
      bar:function(label){var el=document.getElementById("barLbl");if(el&&document.documentElement.dataset.page==="lazer")el.textContent=label;}
    });
  }
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",mount);
  else mount();
})();
/* END GENERATED ADVANCED LASER JS */
'''
    html = replace_once(
        html,
        "\n</script>\n\n</body></html>",
        adapter + "\n</script>\n\n</body></html>",
        "laser JS insertion",
    )

    WEBSITE.parent.mkdir(parents=True, exist_ok=True)
    CURRENT.write_text(html, encoding="utf-8")
    WEBSITE.write_text(html, encoding="utf-8")
    print(f"wrote {CURRENT.relative_to(ROOT)} ({CURRENT.stat().st_size} bytes)")
    print(f"wrote {WEBSITE.relative_to(ROOT)} ({WEBSITE.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
