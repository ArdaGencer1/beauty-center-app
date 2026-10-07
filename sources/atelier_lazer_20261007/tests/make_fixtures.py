#!/usr/bin/env python3
"""Synthetic stand-ins for the 7 live laser pages (structure only: head facts, hero header with the H1, sections
with H2s, lp-sticky-actionbar, JSON-LD, the three scripts).  The real pages live on the server; build.py --check
runs the same gates there.  These fixtures exist so the transform and the apply/rollback cycle are tested here."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import render
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
H1 = {"hub": "Ankara Lazer Epilasyon: Konutkent ve Çayyolu Yakınında Bölge Planı", "kamp": "Laser Signature Kampanya: Konutkent Lazer Epilasyon",
      "fiyat": "Lazer Epilasyon Fiyatları Ankara", "erkek": "Erkek Lazer Epilasyon Ankara", "yuz": "Yüz Lazer Epilasyon Ankara",
      "hassas": "Hassas Cilt İçin Lazer Epilasyon", "bolge": "Bölgesel Lazer Epilasyon Ankara"}
for key, P in render.PAGES.items():
    slug = P["slug"]
    nap = "Yaşamkent, Ankara" if key == "kamp" else "Konutkent, Çankaya / Ankara"
    dev = "LazerMech" if key == "kamp" else "Lasermach"
    ld = {"@context": "https://schema.org", "@type": "BeautySalon", "name": "Selda Gençer Beauty Center", "image": "https://seldagencerbeauty.com/images/salon-1.jpg", "address": nap}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "Kaç seans gerekir?", "acceptedAnswer": {"@type": "Answer", "text": "Bölgeye göre değişir."}}]}
    html = f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{H1[key]} | Selda Gençer</title>
<meta name="description" content="{slug} açıklaması"><link rel="canonical" href="https://seldagencerbeauty.com/{slug}"><meta name="robots" content="index,follow">
<link rel="preload" as="image" href="/images/salon-hero.webp"><link rel="stylesheet" href="/styles.css?v=20261007-faz0">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script><script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>
<script>/* consent */</script><script async src="https://www.googletagmanager.com/gtag/js?id=G-X"></script></head>
<body><nav class="top-nav"><a href="/">Selda Gençer</a></nav>
<header class="hero hero--laser"><div class="hero__media"><img src="/images/lazer-epilasyon-1-temsili.webp" alt=""></div>
<div class="hero__copy"><h1>{H1[key]}</h1><p>{dev} diode lazer ile {nap}.</p><a class="btn" href="https://wa.me/905330390076">WhatsApp</a></div></header>
<main><section class="lp"><h2>Lazer epilasyon nasıl çalışır?</h2><p>Metin.</p></section>
<section class="lp"><h2>Sık sorulan sorular</h2><details><summary>Kaç seans?</summary><p>Bölgeye göre.</p></details></section>
<section class="lp"><h2>Adres ve ulaşım</h2><p>{nap}</p></section></main>
<div class="lp-sticky-actionbar"><a href="tel:+905330390076">Ara</a><a href="https://wa.me/905330390076">WhatsApp</a></div>
<footer>© Selda Gençer</footer><script src="/script.js?v=20261007-faz0"></script><script src="/ads-tracking.js"></script><script src="/sgb-offers.js"></script></body></html>'''
    (out / f"{slug}.html").write_text(html, encoding="utf-8")
(out / "sitemap-images.xml").write_text('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"></urlset>', encoding="utf-8")
print("fixtures ->", out)
