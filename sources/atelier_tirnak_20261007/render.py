#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TIRNAK ATELYESİ -- markup for the 22 nail pages (plan: plans/claude/20261007-tirnak/README.md).

One source for both targets: build_proto.py puts every page into the prototype as a <template>, and a later
live patch can inline the same HTML into the old pages. Everything a reader or a search engine needs (H1,
texts, menu, questions, media with alt text) is static here; src/tirnak.js only adds the interactions
(film scrub, Renk Atölyesi, kartela, hijyen steps, wall filters, invitation extras).

Facts used and where they come from:
  prices / minutes      data/crm_tirnak.json   (CRM price menu; sync_prices.py refreshes it on the server, the rest: "fiyatı sorun")
  reviews               data/reviews_tirnak.json (Google, verbatim)
  kartela dots          data/kartela.json      (positions + colours measured on the salon's own video frame; label numbers
                                                read from it, shown once "etiket" says which tip a label belongs to; no brand)
  media                 ../media_ig_20261007/manifest_tirnak.json (+ the processed photos in website/m/ig)
  hygiene steps         the salon's own Instagram video 18126120175637645 (owner confirmed the steriliser claim, 2026-10-07)
  maintenance interval  4 weeks for protez tırnak (owner, 2026-10-07)
Shared blocks (hijyen, atelier, kartela, fırça, wall, şekil, versus, final, yol) are written once as includes
(<div data-tz-inc="…">); inline=True expands them for a static page.
"""
from __future__ import annotations

import html
import json
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
WA = "905330390076"
TEL = "+905330390076"
MAPS = "https://www.google.com/maps/search/?api=1&query=Selda+Gen%C3%A7er+Beauty+Center+Konutkent"
M = "m/ig/"  # prototype media root; the live site uses /images/ig/

CRM = json.loads((DATA / "crm_tirnak.json").read_text(encoding="utf-8"))
REVIEWS = json.loads((DATA / "reviews_tirnak.json").read_text(encoding="utf-8"))["reviews"]
_K = json.loads((DATA / "kartela.json").read_text(encoding="utf-8"))
KARTELA, KARTELA_ETIKET = _K["dots"], _K.get("etiket")  # etiket: None | "ust" | "alt"
ROWS = {r["id"]: r for r in CRM["rows"]}
ASK = {r["id"]: r for r in CRM["ask"]}
BAKIM_HAFTA = 4  # protez tırnak maintenance interval (owner)


def fmt_tl(p: int) -> str:
    return f"{p:,}".replace(",", ".") + " TL"


def tl(i: str) -> str:
    """Menu price of one CRM row, e.g. "1.500 TL"; every price on the pages comes through here."""
    return fmt_tl(ROWS[i]["p"])


def dk(i: str) -> int:
    return ROWS[i]["d"]


def page_price(spec) -> str:
    """A page's price chip: a literal, or (row id, suffix); a row that is not in the menu yet asks for the price."""
    if isinstance(spec, str):
        return spec
    i, suffix = spec
    return tl(i) + suffix if i in ROWS else "Fiyatı sorun"

ICON = {
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "down": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg>',
    "zoom": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5M11 8v6M8 11h6"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3 20l1.4-4.2A8.5 8.5 0 1 1 7.6 19L3 20z"/></svg>',
    "tel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    "cam": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/></svg>',
    "replay": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 12a8 8 0 1 0 2.3-5.6M4 4v4h4"/></svg>',
}

# ----------------------------------------------------------------------------------------------- planner data
SHAPES4 = ["Uzun", "Kare", "Oval", "Badem"]
PLANS = {
    "tz-merkez": {"title": "Tırnak randevunuz", "shapes": SHAPES4, "opts": ["oje", "mko", "mjk", "mpk", "art", "manikur", "pedikur"]},
    "tz-oje": {"title": "Kalıcı oje randevunuz", "shapes": SHAPES4, "opts": ["oje", "mko", "mjk"]},
    "tz-protez": {"title": "Protez tırnak randevunuz", "shapes": SHAPES4, "opts": ["mpk", "uzatma", "dolgu", "cikar", "tips", "ayak", "art"]},
    "tz-art": {"title": "Nail art randevunuz", "shapes": SHAPES4, "opts": ["art", "mpk", "oje"]},
    "tz-bakim": {"title": "Manikür ve pedikür randevunuz", "opts": ["mko", "manikur", "pedikur", "mp", "medped", "elayak"]},
}


def plan_opts(fam: str) -> list[dict]:
    out = []
    for i in PLANS[fam]["opts"]:
        if i in ROWS:
            r = ROWS[i]
            out.append({"id": i, "n": r["n"], "p": r["p"], "d": r.get("d"), "b": r.get("b")})
        else:
            a = ASK[i]
            out.append({"id": i, "n": a["n"], "p": None, "d": None, "ps": "Fiyatı sorun", "s": a.get("s", "Fiyat ve süre WhatsApp'ta netleşir"), "ask": True})
    return out


def plans_js() -> dict:
    return {f: {k: v for k, v in dict(p, opts=plan_opts(f)).items()} for f, p in PLANS.items()}


# ----------------------------------------------------------------------------------------------- wall data
# (slug, label, tags, file, w, h). Badge-bearing photos use the -k crops (plan §1b); "Vay" order first.
WALL = [
    ("tirnak-3d", "3D çiçek ve inci", "desenli nude", "tirnak-3d-800.webp", 800, 1056),
    ("tirnak-holo", "Aurora cat-eye", "simli renkli", "tirnak-holo-800.webp", 800, 1067),
    ("v:tirnak-papatya", "3D papatya", "desenli nude", "tirnak-papatya", 720, 1280),
    ("tirnak-mermer", "Altın hatlı kelebek", "desenli", "tirnak-mermer-k.webp", 800, 820),
    ("tirnak-inci", "İnci girdap", "desenli nude", "tirnak-inci-k.webp", 800, 813),
    ("tirnak-mor", "Ametist ve altın", "renkli desenli", "tirnak-mor-k.webp", 800, 813),
    ("v:tirnak-krom", "Krom french", "french simli", "tirnak-krom", 720, 1280),
    ("tirnak-bakir-desen", "Kaplumbağa kabuğu", "desenli", "tirnak-bakir-desen-800.webp", 800, 1067),
    ("tirnak-gumus", "Simli ombre", "simli nude", "tirnak-gumus-800.webp", 800, 1067),
    ("tirnak-sut-beyaz", "Süt beyazı badem", "nude", "tirnak-sut-beyaz-800.webp", 800, 1000),
    ("v:tirnak-babyboomer", "Baby boomer", "nude simli", "tirnak-babyboomer", 720, 960),
    ("tirnak-bordo-french", "Bordo french", "french", "tirnak-bordo-french-800.webp", 800, 800),
    ("tirnak-nude", "Simli nude", "nude simli", "tirnak-nude-k.webp", 1200, 1230),
    ("tirnak-lila-french", "Lila french", "french renkli", "tirnak-lila-french-800.webp", 800, 800),
    ("tirnak-leopar", "Leopar", "desenli", "tirnak-leopar-800.webp", 800, 800),
    ("v:tirnak-lila", "Süt beyazı", "nude", "tirnak-lila", 720, 1280),
    ("tirnak-lacivert-desen", "Lacivert desen", "desenli renkli", "tirnak-lacivert-desen-k.webp", 1200, 1328),
    ("tirnak-kirmizi-desen", "Kırmızı french desen", "french desenli", "tirnak-kirmizi-desen-800.webp", 800, 800),
    ("tirnak-neon", "Neon mor", "renkli", "tirnak-neon-800.webp", 800, 1067),
    ("tirnak-bebek-mavisi", "Bebek mavisi", "renkli", "tirnak-bebek-mavisi-800.webp", 800, 800),
    ("tirnak-badem-bordo", "Bordo badem", "renkli", "tirnak-badem-bordo-k.webp", 1200, 1230),
    ("tirnak-uzun-kirmizi", "Kırmızı uzun", "renkli", "tirnak-uzun-kirmizi-k.webp", 1200, 1230),
    ("tirnak-kirmizi-2", "Parlak kırmızı", "renkli", "tirnak-kirmizi-2-800.webp", 800, 1000),
    ("tirnak-lacivert", "Lacivert", "renkli", "tirnak-lacivert-800.webp", 800, 800),
]
FILTERS = [("", "Tümü"), ("french", "French"), ("nude", "Nude"), ("simli", "Simli"), ("renkli", "Renkli"), ("desenli", "Desenli")]


# ----------------------------------------------------------------------------------------------- pages
EYEBROW = "Konutkent · Çankaya"
SEMT_FROM = {"Çayyolu": "Çayyolu'ndan", "Yaşamkent": "Yaşamkent'ten"}
SEMT_KM = {"Çayyolu": "~2 km", "Yaşamkent": "~3 km"}
SEMT_IN = {"Çayyolu": "Çayyolu'nda", "Yaşamkent": "Yaşamkent'te"}
RATING = '<span class="chip chip-in"><span class="star">★</span> 4,6 · 263 yorum</span>'

FAQ = {
    "sure": ("Ne kadar sürer?", f"Randevu sistemimizdeki süreler: kalıcı oje {dk('oje')} dk; manikür ve jel güçlendirme ile kalıcı oje {dk('mjk')} dk; manikür, protez tırnak ve kalıcı oje {dk('mpk')} dk."),
    "renk": ("Rengi nasıl seçiyorum?", "Salondaki kartelamızdan siz seçersiniz. Sitedeki Renk Atölyesi fikir vermek içindir; ekrandaki ton, ojenin kendisiyle birebir aynı olmayabilir."),
    "model": ("Beğendiğim bir modelin fotoğrafını getirebilir miyim?", "Evet. Fotoğrafı WhatsApp'tan gönderin; uygulanabilirliğini ve fiyatını mesajda birlikte netleştiririz."),
    "hijyen": ("Aletler nasıl temizleniyor?", "Metal aletler önce yıkanır, kurutulur, sterilizasyon cihazımızda tıbbi seviyede sterilize edilir ve kişiye özel pakette bekler. Paketiniz yanınızda açılır."),
    "randevu": ("Randevuyu nasıl alıyorum?", "“Saatimi seç” ile işlemi, günü ve saati seçin. Hazır mesaj WhatsApp'ta açılır; göndermek size kalır, onayı ekibimiz verir."),
    "protez": ("Protez tırnak nasıl uygulanıyor?", f"Önce şekil ve uzunluğu birlikte seçeriz. Tırnaklarınız manikürle hazırlanır, protez uygulanır ve kalıcı oje ile bitirilir. Menüde bu üçü birlikte {dk('mpk')} dk; bakım aralığımız {BAKIM_HAFTA} hafta."),
    "bakim": ("Protez tırnağın bakımı ne zaman?", f"Protez tırnakta bakım aralığımız {BAKIM_HAFTA} hafta. Tırnağınız uzadıkça dipte bir boşluk belirir; bakımda bu boşluk doldurulur. Randevu alırken {BAKIM_HAFTA} hafta sonraki bakımınızı da ayırabilirsiniz. Daha erken bir boşluk fark ederseniz fotoğraf gönderin, birlikte bakalım."),
    "cikar": ("Protezi kendim çıkarabilir miyim?", "Çekip koparmanızı önermeyiz; doğal tırnağa zarar verebilir. Salonda, uygun aletle adım adım alırız."),
    "art": ("Nail art fiyatı nasıl belirleniyor?", "Desene göre değişir. Beğendiğiniz modeli seçip gönderin; fiyatı WhatsApp'ta iletelim."),
    "ask": ("Bu işlemin fiyatını neden göremiyorum?", "Sitede yalnızca randevu sistemimizdeki aktif menüden doğruladığımız fiyatları gösteriyoruz. Bu işlem için güncel fiyatı WhatsApp'ta hemen iletelim."),
    "medikal": ("Medikal pedikür bir tedavi mi?", "Hayır. Bir güzellik merkezi bakımıdır. Tırnak mantarı, açık yara ya da şeker hastalığına bağlı ayak sorunları gibi durumlarda önce doktorunuza danışın."),
    "jel": ("Jel güçlendirme ile protez tırnak farkı ne?", "Jel güçlendirmede kendi tırnağınızın üstüne ince bir jel katmanı uygulanır. Protez tırnakta uzunluk ve şekil eklenir."),
    "uzunluk": ("Uzunluğu nasıl seçiyorum?", "Birlikte seçeriz. Günlük işlerinizi, el yapınızı ve istediğiniz görünümü konuşup uzunluğa ve şekle öyle karar veririz."),
    "konum": ("Salon nerede?", "Konutkent'te, 3028. Cadde 8A No:A1, Çankaya. Salı–Pazar 10.00–20.00 açığız, Pazartesi kapalıyız."),
}

# hero: ("film",) | ("video", slug, alt) | ("photo", file, w, h, alt) | ("atelier",)
PAGES = [
    dict(slug="tirnak", code="merkez", fam="tz-merkez", wave="D1", status="tam", nav="Nail studio",
         h1="Ankara Nail <em>Studio</em>", lede="Kapıdan girdiğiniz an başlar.", price=("oje", "'den"),
         hero=("film",), bar="Tırnak randevum · saatimi seç",
         scenes=["yol", "hijyen", "atelier", "firca", "wall", "soz:all", "versus", "menu:oje,mko,mjk,mpk,art", "faq:sure,renk,hijyen,randevu", "final", "live", "visit"]),
    dict(slug="nail-art-ankara", code="art", fam="tz-art", wave="D1", status="tam", nav="Nail art",
         h1="Ankara <em>Nail Art</em>", lede="Her tırnak küçük bir tablo.", price="Desene göre",
         hero=("video", "tirnak-papatya", "Badem ombre tırnak, 3D papatya nail art; salonumuzda çekildi"), bar="Nail art · saatimi seç",
         scenes=["wall", "firca", "soz:art", "menu:art,mpk,oje", "faq:art,model,randevu", "final", "live", "visit"]),
    dict(slug="kalici-oje", code="oje", fam="tz-oje", wave="D1", status="tam", nav="Kalıcı oje",
         h1="Ankara Kalıcı <em>Oje</em>", lede="Rengi siz seçin, gerisi bizde.", price=("oje", "'den"),
         hero=("atelier",), bar="Kalıcı oje · saatimi seç",
         scenes=["kartela", "firca", "soz:oje", "how:oje", "menu:oje,mko,mjk", "faq:sure,renk,hijyen", "final", "live", "visit"]),
    dict(slug="kalici-oje-fiyatlari", code="ojefiyat", fam="tz-oje", wave="D1", status="tam", nav="Kalıcı oje fiyatları",
         h1="Kalıcı Oje <em>Fiyatları</em>", lede="Randevu sistemimizdeki aktif menüden.", price=("oje", "'den"),
         hero=("video", "tirnak-orkide", "Bordo badem tırnaklar ve beyaz orkide; salonumuzda çekildi"), bar="Kalıcı oje · saatimi seç",
         scenes=["menu:oje,mko,mjk", "dahil", "kartela", "soz:oje", "faq:sure,renk,randevu", "final", "live", "visit"]),
    dict(slug="jel-tirnak", code="jel", fam="tz-oje", opt="mjk", wave="D2", status="ince", nav="Jel tırnak ve jel oje",
         h1="Jel Tırnak ve <em>Jel Oje</em>", lede="Kendi tırnağınızın üstüne ince bir jel katmanı.", price=("mjk", " · manikürle"),
         hero=("photo", "tirnak-lacivert-desen-k.webp", 1200, 1328, "Lacivert desenli jel destekli kalıcı oje"), bar="Jel güçlendirme · saatimi seç",
         scenes=["versus", "firca", "soz:oje", "menu:mjk,oje,mko", "faq:jel,sure,renk", "final", "live", "visit"]),
    dict(slug="tirnak-guclendirme", code="guclendir", fam="tz-oje", opt="mjk", wave="D2", status="cekim", nav="Tırnak güçlendirme",
         h1="Tırnak <em>Güçlendirme</em>", lede="Kendi tırnağınız, ince bir jel katmanıyla.", price=("mjk", " · manikürle"),
         hero=("video", "tirnak-hazirlik", "Eldivenli manikür hazırlığı; salonumuzda çekildi"), bar="Güçlendirme · saatimi seç",
         scenes=["katman", "hijyen", "soz:oje", "menu:mjk,mko", "faq:jel,sure,hijyen", "final", "live", "visit"]),
    dict(slug="protez-tirnak", code="protez", fam="tz-protez", wave="D1", status="tam", nav="Protez tırnak",
         h1="Ankara Protez <em>Tırnak</em>", lede="Hayal ettiğiniz uzunluk ve şekil.", price=("mpk", ""),
         hero=("video", "tirnak-babyboomer", "Baby boomer ombre protez tırnak, altın varak; salonumuzda çekildi"), bar="Protez tırnak · saatimi seç",
         scenes=["sekil", "wall", "hijyen", "soz:protez", "how:protez", "menu:mpk,dolgu,cikar", "faq:protez,bakim,hijyen", "final", "live", "visit"]),
    dict(slug="protez-tirnak-modelleri", code="model", fam="tz-protez", wave="D1", status="tam", nav="Protez tırnak modelleri",
         h1="Protez Tırnak <em>Modelleri</em>", lede="Beğendiğinize dokunun, saatinizi seçin.", price=("mpk", ""),
         hero=("photo", "tirnak-3d-800.webp", 800, 1056, "3D çiçek ve inci detaylı pembe protez tırnak"), bar="Modelim · saatimi seç",
         scenes=["wall", "sekil", "soz:protez", "menu:mpk,art", "faq:model,art,protez", "final", "live", "visit"]),
    dict(slug="protez-tirnak-fiyatlari-ankara", code="pfiyat", fam="tz-protez", wave="D1", status="tam", nav="Protez tırnak fiyatları",
         h1="Protez Tırnak <em>Fiyatları</em> Ankara", lede="Randevu sistemimizdeki aktif menüden.", price=("mpk", ""),
         hero=("photo", "tirnak-gumus-1200.webp", 1200, 1600, "Gümüş simli ombre protez tırnak"), bar="Protez tırnak · saatimi seç",
         scenes=["menu:mpk,dolgu,cikar,tips,art", "belirler", "versus", "soz:protez", "faq:protez,ask,randevu", "final", "live", "visit"]),
    dict(slug="protez-tirnak-randevu", code="prandevu", fam="tz-protez", wave="D1", status="tam", nav="Protez tırnak randevusu",
         h1="Protez Tırnak <em>Randevusu</em>", lede="Üç dokunuşta mesajınız hazır.", price=("mpk", ""),
         hero=("video", "tirnak-lila", "Süt beyazı badem protez tırnak; salonumuzda çekildi"), bar="Saatimi seç",
         scenes=["inline", "soz:protez", "hijyen", "faq:randevu,protez,konum", "final", "visit"]),
    dict(slug="protez-tirnak-bakim-dolgu", code="dolgu", fam="tz-protez", opt="dolgu", wave="D2", status="ince", nav="Protez tırnak bakım ve dolgu",
         h1="Protez Tırnak <em>Bakım ve Dolgu</em>", lede="Dört haftada bir, bakımla tazelenir.", price=("dolgu", ""),
         hero=("video", "tirnak-freze", "Freze ucuyla eski jelin alınması; salonumuzda çekildi"), bar="Bakım · saatimi seç",
         scenes=["saat", "foto:dolgu", "hijyen", "soz:protez", "menu:dolgu,mpk", "faq:bakim,ask,hijyen", "final", "live", "visit"]),
    dict(slug="protez-tirnak-cikartma", code="cikar", fam="tz-protez", opt="cikar", wave="D2", status="ince", nav="Protez tırnak çıkarma",
         h1="Protez Tırnak <em>Çıkarma</em>", lede="Protezinizi özenle, adım adım alırız.", price=("cikar", ""),
         hero=("video", "tirnak-freze", "Freze ucuyla eski jelin alınması; salonumuzda çekildi"), bar="Çıkarma · saatimi seç",
         scenes=["how:cikar", "foto:cikar", "hijyen", "soz:protez", "menu:cikar,mpk", "faq:cikar,ask,hijyen", "final", "live", "visit"]),
    dict(slug="tirnak-uzatma", code="uzatma", fam="tz-protez", opt="uzatma", wave="D1", status="tam", nav="Tırnak uzatma",
         h1="Ankara Tırnak <em>Uzatma</em>", lede="Kısa, orta ya da uzun: seçim sizin.", price=("mpk", " · protezle"),
         hero=("photo", "tirnak-uzun-kirmizi-k.webp", 1200, 1230, "Kırmızı uzun protez tırnak"), bar="Uzunluğum · saatimi seç",
         scenes=["sekil:uzunluk", "wall", "soz:protez", "menu:mpk,uzatma", "faq:uzunluk,protez,bakim", "final", "live", "visit"]),
    dict(slug="yeni-nesil-tips", code="tips", fam="tz-protez", opt="tips", wave="D2", status="cekim", nav="Yeni nesil tips",
         h1="Yeni Nesil <em>Tips</em>", lede="Tırnak uzatmanın bir başka yolu.", price=("tips", ""),
         hero=("video", "tirnak-krom", "Simli krom french badem tırnak; salonumuzda çekildi"), bar="Tips · saatimi seç",
         scenes=["versus", "wall", "soz:protez", "menu:tips,mpk", "faq:ask,uzunluk,randevu", "final", "live", "visit"]),
    dict(slug="ayak-protez-tirnak", code="ayak", fam="tz-protez", opt="ayak", wave="D2", status="cekim", nav="Ayak protez tırnak",
         h1="Ayak Protez <em>Tırnak</em>", lede="Ayaklarınız da aynı özeni hak ediyor.", price=("ayak", ""),
         hero=("photo", "tirnak-hijyen-2.webp", 720, 900, "Yıkanan aletler, salonun logolu havlusunda kuruyor"), bar="Ayak protez · saatimi seç",
         note="Ayak protez tırnak fotoğraflarımız çekim aşamasında; görsel, aletlerimizin hijyen sürecinden.",
         scenes=["hijyen", "foto:ayak", "soz:bakim", "menu:ayak,pedikur", "faq:ask,hijyen,randevu", "final", "live", "visit"]),
    dict(slug="cayyolu-protez-tirnak", code="cayyolu", fam="tz-protez", wave="D1", status="tam", nav="Çayyolu protez tırnak",
         h1="Çayyolu Protez <em>Tırnak</em>", lede="Çayyolu'ndan ~2 km, Konutkent'te.", price=("mpk", ""), semt="Çayyolu",
         hero=("film",), bar="Çayyolu'ndan · saatimi seç",
         scenes=["yerel:Çayyolu", "wall", "soz:protez", "hijyen", "menu:mpk,dolgu,cikar", "faq:konum,protez,randevu", "final", "live", "visit"]),
    dict(slug="yasamkent-protez-tirnak", code="yasamkent", fam="tz-protez", wave="D1", status="tam", nav="Yaşamkent protez tırnak",
         h1="Yaşamkent Protez <em>Tırnak</em>", lede="Yaşamkent'ten ~3 km, Konutkent'te.", price=("mpk", ""), semt="Yaşamkent",
         hero=("film",), bar="Yaşamkent'ten · saatimi seç",
         scenes=["yerel:Yaşamkent", "wall", "soz:protez", "hijyen", "menu:mpk,dolgu,cikar", "faq:konum,protez,randevu", "final", "live", "visit"]),
    dict(slug="manikur-ankara", code="manikur", fam="tz-bakim", opt="mko", wave="D1", status="tam", nav="Manikür",
         h1="Ankara <em>Manikür</em>", lede="Önce hijyen, sonra güzellik.", price=("mko", " · kalıcı ojeyle"),
         hero=("video", "tirnak-hazirlik", "Eldivenli manikür hazırlığı; salonumuzda çekildi"), bar="Manikür · saatimi seç",
         scenes=["hijyen", "atelier", "soz:bakim", "how:manikur", "menu:mko,manikur,mp", "faq:hijyen,renk,randevu", "final", "live", "visit"]),
    dict(slug="pedikur-ankara", code="pedikur", fam="tz-bakim", opt="pedikur", wave="D2", status="cekim", nav="Pedikür",
         h1="Ankara <em>Pedikür</em>", lede="Ayaklarınız için ayrılmış bir saat.", price=("pedikur", ""),
         hero=("photo", "tirnak-hijyen-1.webp", 720, 900, "Metal aletler altın kâsede yıkanıyor"), bar="Pedikür · saatimi seç",
         note="Pedikür fotoğraflarımız çekim aşamasında; görsel, aletlerimizin hijyen sürecinden.",
         scenes=["hijyen", "soz:bakim", "menu:pedikur,mp,medped", "faq:hijyen,ask,randevu", "final", "live", "visit"]),
    dict(slug="medikal-pedikur", code="medped", fam="tz-bakim", opt="medped", wave="D2", status="cekim", nav="Medikal pedikür",
         h1="Medikal <em>Pedikür</em>", lede="Hassas ayaklar için özenli bir bakım.", price=("medped", ""),
         hero=("photo", "tirnak-hijyen-oda.webp", 720, 900, "Salonun sterilizasyon odası"), bar="Medikal pedikür · saatimi seç",
         note="Fotoğraf, salonumuzun sterilizasyon odası. Pedikür fotoğraflarımız çekim aşamasında.",
         scenes=["doktor", "hijyen", "soz:bakim", "menu:medped,pedikur", "faq:medikal,hijyen,ask", "final", "live", "visit"]),
    dict(slug="manikur-pedikur-fiyatlari", code="mpfiyat", fam="tz-bakim", opt="mko", wave="D2", status="tam", nav="Manikür pedikür fiyatları",
         h1="Manikür Pedikür <em>Fiyatları</em>", lede="Randevu sistemimizdeki aktif menüden.", price=("mko", "'den"),
         hero=("photo", "tirnak-hijyen-4.webp", 720, 900, "Kişiye özel kapalı paketteki makas"), bar="Manikür · pedikür · saatimi seç",
         scenes=["menu:mko,manikur,pedikur,mp,medped", "hijyen", "soz:bakim", "faq:ask,hijyen,randevu", "final", "live", "visit"]),
    dict(slug="el-ayak-bakimi", code="elayak", fam="tz-bakim", opt="elayak", wave="D2", status="cekim", nav="El ve ayak bakımı",
         h1="El ve Ayak <em>Bakımı</em>", lede="Eller ve ayaklar için bir ritüel.", price=("elayak", ""),
         hero=("photo", "still-firca-1200.webp", 1200, 1600, "Fırçalar, tırnak bakım ürünleri ve altın tepsi"), bar="El & ayak · saatimi seç",
         note="El ve ayak bakımı fotoğraflarımız çekim aşamasında; görsel, salondaki ürün ve fırçalarımız.",
         scenes=["how:elayak", "hijyen", "soz:bakim", "menu:elayak,mko,mp", "faq:ask,hijyen,randevu", "final", "live", "visit"]),
]
BY_SLUG = {p["slug"]: p for p in PAGES}

STEPS = {
    "oje": [("Renk seçilir", "Kartelamızdan tonunuzu seçersiniz; isterseniz Renk Atölyesi'nde denediğiniz rengi gösterin."),
            ("Tırnaklar hazırlanır", "Şekil verilir, yüzey uygulamaya hazırlanır."),
            ("Kat kat uygulanır", "Renk ince katlarla sürülür ve parlak bir bitişle tamamlanır.")],
    "protez": [("Şekil ve uzunluk", "El yapınıza ve günlük işlerinize göre birlikte seçeriz."),
               ("Hazırlık", "Manikürle tırnaklarınız ve tırnak etleriniz hazırlanır."),
               ("Protez ve renk", "Protez uygulanır, kalıcı oje ya da tasarımla bitirilir.")],
    "cikar": [("Bakarız", "Mevcut protezinize ve doğal tırnağınıza birlikte bakarız."),
              ("Adım adım alırız", "Protez uygun aletle, katman katman inceltilerek alınır."),
              ("Bakım", "Doğal tırnağınız şekillendirilir; isterseniz yeni uygulamayı konuşuruz.")],
    "manikur": [("Hazırlık", "Eldivenli ellerle, kendi paketinden çıkan aletlerle başlarız."),
                ("Şekil ve bakım", "Tırnaklar şekillendirilir, tırnak etleri bakılır."),
                ("Renk", "İsterseniz kalıcı oje ile bitiririz; rengi kartelamızdan siz seçersiniz.")],
    "elayak": [("Temizlik", "Eller ve ayaklar temizlenir, aletler kendi paketinden çıkar."),
               ("Şekil ve bakım", "Tırnaklar şekillendirilir, tırnak etleri bakılır."),
               ("Bitiş", "İsterseniz kalıcı oje ile tamamlarız.")],
}

QUOTES = {  # (reviewer, exact substring of the review) -- asserted against the review text below
    "all": [("Zelal E.", "tüm işlem boyunca hiç acı hissetmedim"), ("Gülseren A.", "protez Tırnak hakkındaki ön yargılarım değişti"), ("Fato P.", "Hem hijyen, hem ilgi, hem de ortaya çıkan tırnaklar efsane!")],
    "protez": [("Öykü A.", "incecik ama sağlam çok güzel bir çalışma yaptı"), ("Merve S.", "hiç burada yapılan kadar uzun kullandığım olmadı"), ("Gülseren A.", "protez Tırnak hakkındaki ön yargılarım değişti")],
    "oje": [("Pelin G.", "o kadar hızlı ve başarılıydı ki hayran kaldım"), ("Itır Ç.", "ortaya çok güzel bir sonuç çıktı"), ("Fato P.", "Ne istediğimi hemen anlayıp harika bir sonuç çıkarıyor.")],
    "art": [("Fato P.", "Hem hijyen, hem ilgi, hem de ortaya çıkan tırnaklar efsane!"), ("Meryem İ.", "Hepsinden oldukça memnun kaldım.")],
    "bakim": [("Büşra o.", "Ankara’da tırnak için aradığım bilinçli ve temiz yeri buldum."), ("Nihal Y.", "Çok temiz bir işletme."), ("Gülbeyaz G.", "hem hijyen kurallarına dikkat edildi")],
}
SOZ_H2 = {"all": "“Tırnaklar efsane.”", "protez": "“İncecik ama sağlam.”", "oje": "“Hayran kaldım.”", "art": "“Tırnaklar efsane.”", "bakim": "“Temiz yeri buldum.”"}
SOZ_TAG = {"all": "", "protez": "protez", "oje": "oje", "art": "art", "bakim": "bakim"}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def wa(msg: str) -> str:
    return f"https://wa.me/{WA}?text={urllib.parse.quote(msg)}"


def lbl(p: dict, place: str) -> str:
    k = f"at-tz-{p['code']}-{place}"
    assert len(k) <= 48 and k.isascii(), k
    return f'data-track-label="{k}"'


def gold(label: str, attrs: str, icon: str = "arrow", cls: str = "") -> str:
    return f'<button class="btn-gold {cls}" {attrs}><span class="lbl">{label}</span>{ICON[icon]}</button>'


def chips(p: dict) -> str:
    price = f'<span class="chip chip-in price" style="animation-delay:.08s">{esc(page_price(p["price"]))}</span>'
    slot = '<span class="chip chip-in" style="animation-delay:.16s" data-slot-chip="tirnak"><span class="dot"></span> <span>Bugün müsait</span></span>'
    return f'<div class="chips">{RATING}{price}{slot}</div>'


def copy_block(p: dict, film: bool = False) -> str:
    eb = (f'<span class="eyebrow">{esc(SEMT_FROM[p["semt"]])} {SEMT_KM[p["semt"]]} · Konutkent</span>' if p.get("semt")
          else f'<span class="eyebrow" data-personal>{EYEBROW}</span>')
    note = f'<p class="hero-note">{esc(p["note"])}</p>' if p.get("note") else ""
    rings = f'<div class="rings" data-tz-rings="{p["fam"]}"></div>'
    if film:
        hint = f'<span class="walk-hint">{ICON["down"]}Kaydırın, içeri girelim</span>'
        return f'{eb}<h1>{p["h1"]}</h1><p class="lede">{esc(p["lede"])}</p>{chips(p)}{rings}{hint}'
    return f'<div class="hero-copy">{eb}<h1>{p["h1"]}</h1><p class="lede">{esc(p["lede"])}</p>{chips(p)}{rings}{note}</div>'


FILM_CAPS = [
    {"n": "01", "t": "Konutkent'te bir kapı.", "s": "Mermer lobi, sıcak ışık."},
    {"n": "02", "t": "Hoş geldiniz.", "s": "Altın monogramın altında, resepsiyonda."},
    {"n": "03", "t": "Masanız hazır.", "s": "Eldivenli eller, tırnak barında."},
    {"n": "04", "t": "Ve sonuç.", "s": "Badem french; salonumuzda çekildi."},
]


def hero(p: dict) -> str:
    kind = p["hero"][0]
    if kind == "film":
        caps = esc(json.dumps(FILM_CAPS, ensure_ascii=False))
        return (f'<div class="walk tz-film" data-tz-film="tirnak-giris" data-frames="48" data-atlases="4" data-stops="0,12,23,35" data-caps="{caps}" style="--n:5">'
                f'<div class="walk-stage lit"><div class="walk-frame">'
                f'<img class="walk-img walk-poster on" src="{M}tirnak-giris-poster.webp" alt="Selda Gençer Beauty Center girişi, Konutkent" width="720" height="1280" fetchpriority="high">'
                f'<canvas class="walk-img walk-film" width="540" height="960" aria-hidden="true"></canvas>'
                f'<canvas class="dust" data-dust></canvas><div class="walk-beam"></div></div>'
                f'<div class="walk-scrim"></div><div class="walk-copy"><div class="walk-hero">{copy_block(p, film=True)}</div>'
                f'<div class="walk-cap"><span class="n"></span><span class="t"></span><span class="s"></span>'
                f'{gold("Bu sonucu istiyorum", "data-tz-plan data-tz-model=" + chr(34) + "Badem french (sitedeki film)" + chr(34) + " " + lbl(p, "film-iste"), cls="tz-cap-cta")}</div></div>'
                f'<ol class="walk-rail" aria-hidden="true"></ol></div></div>')
    if kind == "atelier":
        return f'<div class="hero"><div class="hero-split"><div class="hero-media lit">{inc("atelier")}</div>{copy_block(p)}</div></div>'
    if kind == "video":
        slug, alt = p["hero"][1], p["hero"][2]
        media = (f'<img class="tz-vp" src="{M}{slug}-poster.webp" alt="{esc(alt)}" width="720" height="1280" fetchpriority="high">'
                 f'<video class="auto-vid" muted playsinline loop preload="none" poster="{M}{slug}-poster.webp" data-src="{M}{slug}.mp4" aria-hidden="true"></video>'
                 f'<button class="zoom-btn" data-zoom="{M}{slug}-poster.webp" aria-label="Yakından görün" {lbl(p, "hero-yakindan")}>{ICON["zoom"]}</button>')
        tag = '<span class="tz-tag">Salonumuzda çekildi</span>'
    else:
        f, w, h, alt = p["hero"][1:]
        media = (f'<img src="{M}{f}" alt="{esc(alt)}" width="{w}" height="{h}" fetchpriority="high">'
                 f'<button class="zoom-btn" data-zoom="{M}{f}" aria-label="Yakından görün" {lbl(p, "hero-yakindan")}>{ICON["zoom"]}</button>')
        tag = ""
    return (f'<div class="hero"><div class="hero-split"><div class="hero-media lit"><div class="kb-stage tz-hv">{media}'
            f'<canvas class="dust" data-dust></canvas>{tag}</div></div>{copy_block(p)}</div></div>')


def inc(name: str, arg: str = "") -> str:
    return f'<div data-tz-inc="{name}"' + (f' data-tz-arg="{esc(arg)}"' if arg else "") + "></div>"


# ----------------------------------------------------------------------------------------------- shared blocks
def blk_atelier() -> str:
    shapes = "".join(f'<button data-tz-shape="{k}" aria-pressed="{str(k == "uzun").lower()}">{n}</button>'
                     for k, n in (("uzun", "Uzun"), ("kare", "Kare"), ("oval", "Oval")))
    return (f'<div class="atelier-stage tz-atelier" data-tz-atelier>'
            f'<img class="tz-base" src="{M}tirnak-uzun-kirmizi-1200.webp" alt="Kırmızı uzun protez tırnak, salonumuzda yapıldı" width="1200" height="1500">'
            f'<img class="tz-neutral" src="{M}tirnak-uzun-kirmizi-neutral-1200.webp" alt="" aria-hidden="true" width="1200" height="1500" loading="lazy">'
            f'<div class="tint tz-t0" aria-hidden="true"></div><div class="tint tz-t1" aria-hidden="true"></div><span class="tz-brush" aria-hidden="true"></span>'
            f'<canvas class="dust" data-dust></canvas>'
            f'<div class="ba-toggle" role="group" aria-label="Tırnak şekli">{shapes}</div>'
            f'<div class="palette"><div class="palette-top"><b class="tz-swname">Kiraz Kırmızısı</b><span>Renk Atölyesi · parmağınızla boyayın</span></div>'
            f'<div class="sw-row" role="group" aria-label="Oje rengi"></div></div></div>')


def blk_atelier_sec() -> str:
    return (f'<div class="sec gutter tz-atelier-sec"><div class="two">{blk_atelier()}'
            f'<div class="sec-head tz-side"><span class="eyebrow">Renk Atölyesi</span><h2>Bir renge dokunun, <em>tırnaklara</em> aksın.</h2>'
            f'<p>Gerçek tırnaklar, salonumuzda yapıldı. Rengi seçin ya da parmağınızı fotoğrafın üstünde sürükleyin; yeni ton tırnaklara akar.</p>'
            f'{gold("Bu renkle saatimi seç", "data-tz-plan data-tz-place=atolye")}'
            f'<p class="hero-note">Renk denemesi fotoğraf üzerinde yapılır; salondaki oje ile birebir aynı olmayabilir.</p></div></div></div>')


def kartela_no(d: dict) -> str | None:
    return d.get(f"no_{KARTELA_ETIKET}") if KARTELA_ETIKET else None


def blk_kartela() -> str:
    def dot(d: dict) -> str:
        no = kartela_no(d)
        where = f"{no} numara" if no else f"{d['r']}. sıra"
        return (f'<button class="tz-ks" style="left:{d["x"]}%;top:{d["y"]}%;--c:{d["c"]}" data-n="{esc(d["n"])}" data-r="{d["r"]}"'
                + (f' data-no="{no}"' if no else "") + f' aria-label="{esc(d["n"])}, {where}"></button>')
    nums = any(kartela_no(d) for d in KARTELA)
    dots = "".join(dot(d) for d in KARTELA)
    return (f'<div class="sec dark-band gutter tz-kartela-sec"><div class="golden">'
            f'<div class="tz-kartela" data-tz-kartela><img src="{M}tirnak-kartela.webp" alt="Salondaki jel oje kartelası" width="720" height="1280" loading="lazy">{dots}'
            f'<div class="tz-kpick" aria-live="polite"><i></i><span><b>Bir tona dokunun</b><small>Salondaki kartela</small></span></div></div>'
            f'<div class="sec-head" style="margin:0"><span class="eyebrow">Gerçek kartela</span><h2>Rengi <em>kartelamızdan</em> seçin.</h2>'
            + ('<p>Bu, salondaki jel oje kartelamız. Bir tona dokunun; adını ve kartela numarasını mesajınıza ekleyelim.</p>' if nums else
               '<p>Bu, salondaki jel oje kartelamız. Bir tona dokunun; adını mesajınıza ekleyelim, numarasını salonda karteladan birlikte bulalım.</p>')
            + f'<div class="golden-actions">{gold("Bu tonla saatimi seç", "data-tz-plan data-tz-place=kartela")}</div>'
            + '<p class="hero-note" style="color:#968B76">Ton adları fotoğrafa bakılarak verildi'
            + ('; numaralar karteladaki etiketlerden okundu' if nums else '') + '. Ekrandaki renk ışığa göre değişebilir.</p></div></div></div>')


def blk_firca() -> str:
    caps = esc(json.dumps(["İnce fırça", "Kırmızı çizgi, uçta", "Elde, milim milim"], ensure_ascii=False))
    return (f'<div class="film tz-firca" data-tz-film="tirnak-firca" data-frames="36" data-atlases="3" data-caps="{caps}">'
            f'<div class="film-stage"><div class="film-frame lit">'
            f'<img src="{M}tirnak-firca-poster.webp" alt="İnce fırçayla kırmızı mikro french çizimi, salonumuzda çekildi" width="720" height="1280" loading="lazy">'
            f'<canvas width="540" height="960" aria-hidden="true"></canvas><div class="film-bar"><i></i></div>'
            f'<div class="film-meta"><small>Salonda çekildi · kaydırdıkça çizilir</small><b class="tz-fcap">İnce fırça</b></div></div>'
            f'<div class="film-side"><span class="eyebrow">Fırça darbesi</span><h2 class="display" style="font-size:52px">Kaydırdıkça çizilir.</h2>'
            f'<p class="muted">İnce bir fırça, kırmızı bir çizgi. French uçlar elde, tek tek çizilir.</p>'
            f'{gold("Bu tasarımla saatimi seç", "data-tz-plan data-tz-model=" + chr(34) + "Kırmızı mikro french (sitedeki film)" + chr(34) + " data-tz-place=firca")}</div></div></div>')


def blk_hijyen() -> str:
    steps = [("01", "Yıkama", "Kullanılan her metal alet önce yıkanır.", "tirnak-hijyen-1.webp", "Metal aletler altın kâsede yıkanıyor"),
             ("02", "Kurulama", "Temiz havluda kurutulur.", "tirnak-hijyen-2.webp", "Yıkanan aletler logolu havluda kuruyor"),
             ("03", "Sterilizasyon", "Sterilizasyon cihazımızda tıbbi seviyede sterilize edilir.", "tirnak-hijyen-3.webp", "Aletler sterilizasyon cihazının tepsisinde"),
             ("04", "Kişiye özel paket", "Kapalı pakette bekler; paketiniz yanınızda açılır.", "tirnak-hijyen-4.webp", "Kişiye özel kapalı paketteki makas")]
    imgs = "".join(f'<img class="tz-hij-img{" on" if i == 0 else ""}" src="{M}{f}" alt="{esc(a)}" width="720" height="900" loading="lazy">' for i, (_, _, _, f, a) in enumerate(steps))
    lis = "".join(f'<li class="{"on" if i == 0 else ""}"><span class="n">{n}</span><div><b>{t}</b><p>{s}</p></div></li>' for i, (n, t, s, _, _) in enumerate(steps))
    return (f'<div class="tz-hij" data-tz-hijyen><div class="tz-hij-stage">'
            f'<div class="tz-hij-media lit">{imgs}<span class="tz-tag">Salonumuzun kendi videosundan</span></div>'
            f'<div class="tz-hij-copy"><span class="eyebrow">Hijyen yolculuğu</span><h2>Aletleriniz <em>sizden önce</em> bu yoldan geçer.</h2>'
            f'<ol class="tz-hij-steps">{lis}</ol><div class="tz-hij-bar"><i></i></div></div></div></div>')


def blk_wall() -> str:
    filt = "".join(f'<button data-tz-f="{k}" aria-pressed="{str(not k).lower()}">{n}</button>' for k, n in FILTERS)
    items = []
    for slug, label, tags, f, w, h in WALL:
        if slug.startswith("v:"):
            media = (f'<div class="tz-w-media"><img class="tz-vp" src="{M}{f}-poster.webp" alt="{esc(label)}, salonumuzda çekildi" width="{w}" height="{h}" loading="lazy">'
                     f'<video class="auto-vid" muted playsinline loop preload="none" poster="{M}{f}-poster.webp" data-src="{M}{f}.mp4" aria-hidden="true"></video>'
                     f'<span class="tz-live">Video</span></div>')
        else:
            media = (f'<button class="tz-w-media" data-zoom="{M}{f}" aria-label="{esc(label)}: yakından görün">'
                     f'<img src="{M}{f}" alt="{esc(label)}, salonumuzda yapıldı" width="{w}" height="{h}" loading="lazy"></button>')
        items.append(f'<figure class="tz-w" data-tags="{tags}">{media}<figcaption><span>{esc(label)}</span>'
                     f'<button class="tz-want" data-tz-plan data-tz-model="{esc(label)}" data-tz-place="duvar">Bunu istiyorum</button></figcaption></figure>')
    return (f'<div class="sec gutter tz-wall-sec"><div class="sec-head"><span class="eyebrow">Tasarım duvarı</span>'
            f'<h2>Beğendiğinize <em>dokunun</em>.</h2><p>Hepsi salonumuzda yapıldı, Instagram hesabımızdan. Bir modeli seçin; adını mesajınıza ekleyelim.</p></div>'
            f'<div class="tz-filt" role="group" aria-label="Model süzgeci">{filt}</div><div class="tz-wall">{"".join(items)}</div></div>')


SEKIL = [("oval", "Oval", "Kısa", "tirnak-yuvarlak-kirmizi-1200.webp", "Kırmızı oval tırnak"),
         ("kare", "Kare", "Orta", "tirnak-kare-kirmizi-k.webp", "Kırmızı kare tırnak"),
         ("uzun", "Uzun", "Uzun", "tirnak-uzun-kirmizi-k.webp", "Kırmızı uzun protez tırnak"),
         ("badem", "Badem", "Badem", "tirnak-badem-bordo-k.webp", "Bordo badem protez tırnak")]


def blk_sekil() -> str:
    imgs = "".join(f'<img{" class=" + chr(34) + "on" + chr(34) if k == "uzun" else ""} data-look="{k}" src="{M}{f}" alt="{esc(a)}, salonumuzda yapıldı" loading="lazy">' for k, _, _, f, a in SEKIL)
    btns = "".join(f'<button data-tz-sekil="{k}" data-s="{s}" data-u="{u}" aria-pressed="{str(k == "uzun").lower()}">{s}</button>' for k, s, u, _, _ in SEKIL)
    return (f'<div class="sec gutter tz-sekil-sec"><div class="two"><div class="look-stage wide tz-sekil" data-tz-sekil-stage>{imgs}</div>'
            f'<div class="sec-head tz-side"><span class="eyebrow tz-sekil-eb">Şekil seçici</span><h2 class="tz-sekil-h2">Hangi <em>şekil</em> sizin?</h2>'
            f'<p>Dört gerçek sonuç, dört şekil. Seçtiğiniz şekil randevu mesajınıza eklenir; uzunluğa salonda birlikte karar veririz.</p>'
            f'<div class="tz-seg" role="group" aria-label="Şekil">{btns}</div>'
            f'{gold("Bu şekille saatimi seç", "data-tz-plan data-tz-place=sekil")}</div></div></div>')


def blk_versus() -> str:
    cards = [("kalici-oje", "Kalıcı oje", "Kendi tırnağınıza renk", ["Ekleme yok", f"{dk('oje')} dk", tl("oje") + "'den"]),
             ("tirnak-guclendirme", "Jel güçlendirme", "İnce bir jel katmanı", ["Kendi tırnağınızın üstüne", f"{dk('mjk')} dk · manikürle", tl("mjk")]),
             ("protez-tirnak", "Protez tırnak", "Uzunluk ve şekil", ["Uzunluk eklenir", f"{dk('mpk')} dk · manikür ve ojeyle", tl("mpk")]),
             ("yeni-nesil-tips", "Yeni nesil tips", "Uzatmanın başka yolu", ["Ayrıntıyı birlikte konuşalım"] + ([f"{dk('tips')} dk", tl("tips")] if "tips" in ROWS else ["Süre ve fiyat: WhatsApp'ta", "Fiyatı sorun"]))]
    out = "".join(f'<div class="vs-card"><span class="eyebrow">{e}</span><b>{t}</b><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul>'
                  f'<a class="btn-line" href="#tirnak/{s}" data-go="tirnak/{s}" data-tz-place="karar">Sayfasına git →</a></div>' for s, e, t, li in cards)
    return (f'<div class="sec gutter"><div class="sec-head"><span class="eyebrow">Karar vermek için</span><h2>Oje mi, jel mi, <em>protez</em> mi?</h2>'
            f'<p>Süreler ve fiyatlar randevu sistemimizdeki aktif menüden. Kararsız kalırsanız mesajda birlikte seçeriz.</p></div><div class="versus tz-vs4">{out}</div></div>')


def blk_final() -> str:
    return (f'<div class="sec dark-band gutter tz-final"><div class="golden"><div class="tz-final-media lit">'
            f'<img class="tz-vp" src="{M}tirnak-orkide-poster.webp" alt="Bordo badem tırnaklar ve beyaz orkide, salonumuzda çekildi" loading="lazy">'
            f'<video class="auto-vid" muted playsinline loop preload="none" poster="{M}tirnak-orkide-poster.webp" data-src="{M}tirnak-orkide.mp4" aria-hidden="true"></video></div>'
            f'<div class="sec-head" style="margin:0"><span class="eyebrow">Son söz</span><h2>Sıradaki eller <em>sizinki</em>.</h2>'
            f'<p>Günü ve saati seçin; mesajınız hazır olsun. Onayı ekibimiz WhatsApp\'ta verir.</p>'
            f'<div class="golden-actions">{gold("Saatimi seç", "data-tz-plan data-tz-place=final", cls="shine")}'
            f'<a class="btn-line" data-tz-wa data-tz-place="final-wa" href="{wa("Merhaba, tırnak randevusu almak istiyorum.")}" target="_blank" rel="noopener">{ICON["wa"]}WhatsApp</a>'
            f'<a class="btn-line" href="tel:{TEL}" data-tz-place="final-tel">{ICON["tel"]}Ara</a></div></div></div></div>')


def blk_yol() -> str:
    tiles = [("kalici-oje", "tirnak-lila", "Kalıcı oje", tl("oje") + "'den"),
             ("protez-tirnak", "tirnak-babyboomer", "Protez tırnak", tl("mpk")),
             ("nail-art-ankara", "tirnak-papatya", "Nail art", "Desene göre"),
             ("manikur-ankara", "tirnak-hazirlik", "Manikür ve pedikür", tl("mko") + "'den")]
    out = "".join(f'<a class="tile" href="#tirnak/{s}" data-go="tirnak/{s}" data-tz-place="yol-{s.split("-")[0]}">'
                  f'<img class="tz-vp" src="{M}{v}-poster.webp" alt="" loading="lazy"><video class="auto-vid" muted playsinline loop preload="none" poster="{M}{v}-poster.webp" data-src="{M}{v}.mp4" aria-hidden="true"></video>'
                  f'<span class="tile-tag">Vitrin · canlı</span><span class="tile-txt"><b>{t}</b><span>{pr}</span></span></a>' for s, v, t, pr in tiles)
    return (f'<div class="sec gutter"><div class="sec-head"><span class="eyebrow">Dört kapı</span><h2>Hangi <em>tırnak</em> hikâyesi sizin?</h2>'
            f'<p>Her kartın arkasında salonumuzda çekilmiş bir video var. Dokunun, o hikâyeye geçin.</p></div><div class="tiles tz-yol">{out}</div></div>')


INCLUDES = {"atelier": blk_atelier, "atelier-sec": blk_atelier_sec, "kartela": blk_kartela, "firca": blk_firca, "hijyen": blk_hijyen,
            "wall": blk_wall, "sekil": blk_sekil, "versus": blk_versus, "final": blk_final, "yol": blk_yol}


# ----------------------------------------------------------------------------------------------- per-page blocks
def blk_menu(p: dict, ids: list[str]) -> str:
    rows = []
    for i in ids:
        if i in ROWS:
            r = ROWS[i]
            small = " · ".join(x for x in (r.get("b"), f'{r["d"]} dk' if r.get("d") else None) if x)
            rows.append(f'<div class="mrow"><span class="nm">{esc(r["n"])}<small>{small}</small></span><span class="ld"></span><span class="pr">{fmt_tl(r["p"])}</span></div>')
        else:
            a = ASK[i]
            msg = f"Merhaba, {a['n'].lower()} fiyatını öğrenebilir miyim?"
            rows.append(f'<div class="mrow"><span class="nm">{esc(a["n"])}<small>{esc(a.get("s", "Güncel fiyatı mesajla iletelim"))}</small></span><span class="ld"></span>'
                        f'<a class="pr tz-ask" data-tz-wa data-tz-msg="{esc(msg)}" href="{wa(msg)}" target="_blank" rel="noopener" {lbl(p, "menu-sor")}>Sorun →</a></div>')
    return (f'<div class="sec gutter"><div class="menu-card tz-menu"><span class="eyebrow">Tırnak menüsü</span><h3>Fiyatlar</h3>{"".join(rows)}'
            f'<p class="menu-src">Randevu sistemindeki aktif menüden · {CRM["as_of"][8:10].lstrip("0")} Ekim 2026. Kampanya fiyatları yeni danışanlar içindir; ayrıntıyı mesajda iletelim.</p>'
            f'<div class="tz-menu-cta">{gold("Saatimi seç", "data-tz-plan data-tz-place=menu")}</div></div></div>')


def blk_how(key: str) -> str:
    lis = "".join(f'<li><div><b>{t}</b><p>{s}</p></div></li>' for t, s in STEPS[key])
    title = {"oje": "Üç adımda renk.", "protez": "Üç adım, bir sonuç.", "cikar": "Acele etmeden, adım adım.", "manikur": "Önce hijyen, sonra bakım.", "elayak": "Eller ve ayaklar için."}[key]
    return (f'<div class="sec gutter"><div class="sec-head" style="margin-bottom:16px"><span class="eyebrow">Nasıl geçer</span>'
            f'<h2 style="font-size:40px">{title}</h2></div><ol class="how">{lis}</ol></div>')


def blk_faq(keys: list[str]) -> str:
    out = "".join(f'<details><summary>{esc(FAQ[k][0])}</summary><p>{esc(FAQ[k][1])}</p></details>' for k in keys)
    return f'<div class="sec gutter faq" style="padding-top:0"><div class="sec-head"><span class="eyebrow">Sık sorulanlar</span><h2>Aklınızdakiler</h2></div>{out}</div>'


def blk_soz(tag: str) -> str:
    return (f'<div class="sec gutter tz-soz" style="padding-bottom:28px"><div class="sec-head"><span class="eyebrow">Google yorumlarından</span><h2>{SOZ_H2[tag]}</h2></div>'
            f'<div class="tz-quotes" data-tz-quotes="{tag}"></div></div><div class="reviews" data-tz-rv="{SOZ_TAG[tag]}"></div>'
            f'<p class="rv-note gutter">Google yorumlarından aynen; sonuç kişiye göre değişir. <a href="{MAPS}" target="_blank" rel="noopener" data-tz-place="yorumlar">Tümü Google Haritalar\'da</a>.</p>')


def blk_yerel(p: dict, semt: str) -> str:
    dist, frm = SEMT_KM[semt], SEMT_FROM[semt]
    return (f'<div class="sec gutter"><div class="tz-yerel"><svg viewBox="0 0 400 150" aria-hidden="true">'
            f'<path class="tz-route" d="M30 110 C 120 30, 210 140, 370 50" pathLength="1"/><circle cx="30" cy="110" r="7" class="tz-a"/><circle cx="370" cy="50" r="9" class="tz-b"/>'
            f'<text x="30" y="138" text-anchor="start">{esc(semt)}</text><text x="370" y="28" text-anchor="end">Konutkent</text></svg>'
            f'<div class="sec-head" style="margin:0"><span class="eyebrow">{esc(frm)} {dist}</span><h2>{esc(frm)} <em>birkaç dakika</em>.</h2>'
            f'<p>Salonumuz Konutkent\'te, 3028. Cadde 8A No:A1. {esc(SEMT_IN[semt])} ayrı bir şubemiz yok; {esc(frm)} {dist}. Yol çizgisi temsilidir.</p>'
            f'<div class="golden-actions"><a class="btn-line" href="{MAPS}" target="_blank" rel="noopener" {lbl(p, "yol-tarifi")}>{ICON["pin"]}Yol tarifi</a>'
            f'{gold("Saatimi seç", "data-tz-plan data-tz-place=yerel")}</div></div></div></div>')


def blk_foto(p: dict, kind: str) -> str:
    msg = {"dolgu": "Merhaba, protez tırnağımın fotoğrafını gönderiyorum; bakım zamanı geldi mi?",
           "cikar": "Merhaba, protez tırnaklarımı çıkarmak istiyorum, fotoğrafını gönderiyorum.",
           "ayak": "Merhaba, ayak protez tırnak için bilgi almak istiyorum, fotoğraf gönderiyorum."}[kind]
    return (f'<div class="sec gutter"><div class="invite-teaser"><span class="eyebrow">Önce bir bakalım</span><h3>Fotoğrafınızı gönderin, birlikte bakalım.</h3>'
            f'<p class="muted" style="margin:0">Gün ışığında, filtresiz bir fotoğraf yeterli. Uzmanımız bakıp ne gerektiğini ve fiyatı mesajla iletir.</p>'
            f'<a class="btn-gold shine" data-tz-wa data-tz-msg="{esc(msg)}" href="{wa(msg)}" target="_blank" rel="noopener" {lbl(p, "foto-gonder")}>{ICON["cam"]}<span class="lbl">Fotoğrafımı göndereyim</span></a></div></div>')


def blk_doktor() -> str:
    return ('<div class="sec gutter"><div class="tz-note"><span class="eyebrow">Dürüst bir not</span><h3>Bakım, tedavi değil.</h3>'
            '<p>Medikal pedikür bir güzellik merkezi bakımıdır. Tırnak mantarı, batık tırnakta iltihap, açık yara ya da şeker hastalığına bağlı ayak sorunlarında önce doktorunuza danışın; uygun görürse bakımı birlikte planlarız.</p></div></div>')


def blk_dahil(p: dict) -> str:
    cards = [("Kalıcı oje", f"Renk kartelamızdan siz seçersiniz; {dk('oje')} dk."), ("Manikürle", f"Manikür ve kalıcı oje birlikte; {dk('mko')} dk."),
             ("Jel güçlendirmeyle", f"Manikür, ince jel katmanı ve kalıcı oje; {dk('mjk')} dk."), ("Tasarım eklerseniz", "Nail art desene göre fiyatlanır; mesajla iletelim.")]
    out = "".join(f'<div class="vs-card"><b>{t}</b><p class="muted" style="margin:0;font-size:14px">{s}</p></div>' for t, s in cards)
    return f'<div class="sec gutter" style="padding-top:0"><div class="sec-head"><span class="eyebrow">Ne dahil?</span><h2>Fiyatın <em>içinde</em> ne var?</h2></div><div class="versus tz-vs4">{out}</div></div>'


def blk_belirler(p: dict) -> str:
    cards = [("Uzunluk ve şekil", "Seçtiğiniz uzunluk ve şekil uygulamayı belirler."), ("Tasarım", "Düz renk ya da nail art; desen fiyata eklenir."),
             ("Bakım", f"Bakım ve dolgu {BAKIM_HAFTA} haftada bir, ayrı bir randevudur."), ("Menü", f"Manikür, protez ve kalıcı oje birlikte {tl('mpk')} · {dk('mpk')} dk.")]
    out = "".join(f'<div class="vs-card"><b>{t}</b><p class="muted" style="margin:0;font-size:14px">{s}</p></div>' for t, s in cards)
    return f'<div class="sec gutter" style="padding-top:0"><div class="sec-head"><span class="eyebrow">Fiyatı ne belirler?</span><h2>Dört <em>soru</em>, net bir fiyat.</h2></div><div class="versus tz-vs4">{out}</div></div>'


def blk_katman() -> str:
    layers = [("k-oje", 96, "Kalıcı oje"), ("k-jel", 126, "İnce jel katmanı"), ("k-nail", 156, "Doğal tırnağınız")]
    rows = "".join(f'<g class="k-l {c}"><rect x="150" y="{y}" width="220" height="26" rx="13"/><line x1="140" y1="{y + 13}" x2="40" y2="{y + 13}"/><text x="36" y="{y + 18}" text-anchor="start">{t}</text></g>'
                   for c, y, t in layers)
    return ('<div class="sec dark-band gutter"><div class="golden"><div class="tz-katman" data-tz-katman><svg viewBox="0 0 400 240" aria-hidden="true">'
            f'<rect class="k-skin" x="130" y="186" width="260" height="40" rx="20"/>{rows}</svg></div>'
            '<div class="sec-head" style="margin:0"><span class="eyebrow">Katman katman</span><h2>Kendi tırnağınız, <em>üstünde</em> ince bir jel.</h2>'
            f'<p>Jel güçlendirmede uzunluk eklenmez; doğal tırnağınızın üstüne ince bir jel katmanı ve kalıcı oje uygulanır. Menüde manikürle birlikte {dk("mjk")} dk.</p>'
            '<p class="hero-note" style="color:#968B76">Çizim temsilidir.</p></div></div></div>')


def blk_saat(p: dict) -> str:
    return ('<div class="sec dark-band gutter"><div class="golden"><div class="tz-saat" data-tz-saat><svg viewBox="0 0 400 300" aria-hidden="true">'
            '<path class="s-finger" d="M110 300 L110 128 Q110 36 200 36 Q290 36 290 128 L290 300Z"/>'
            '<path class="s-bed" d="M138 222 Q200 200 262 222 L262 112 Q262 58 200 56 Q138 58 138 112Z"/>'
            '<g class="s-plate"><path class="s-p" d="M140 214 Q200 194 260 214 L260 98 Q260 30 200 24 Q140 30 140 98Z"/>'
            '<path class="s-tip" d="M140 72 Q200 54 260 72 L260 98 Q260 30 200 24 Q140 30 140 72Z"/></g>'
            '<path class="s-cut" d="M132 226 Q200 200 268 226"/>'
            '<text x="330" y="60" text-anchor="middle" class="s-w">0. hafta</text><text x="394" y="88" text-anchor="end" class="s-due">BAKIM ZAMANI</text></svg>'
            f'<label class="tz-range"><span>Haftaları kaydırın</span><input type="range" min="0" max="{BAKIM_HAFTA}" step="1" value="0" aria-label="Hafta"></label></div>'
            f'<div class="sec-head" style="margin:0"><span class="eyebrow">Bakım saati</span><h2>Dipte bir <em>boşluk</em> belirdiyse.</h2>'
            f'<p>Doğal tırnak uzadıkça protez öne doğru ilerler, dipte kendi tırnağınız görünmeye başlar. Bakım aralığımız {BAKIM_HAFTA} hafta; randevunuzu alırken bir sonrakini de ayırabilirsiniz. Daha erken bir boşluk fark ederseniz bir fotoğraf yeterli.</p>'
            f'<div class="golden-actions">{gold("Bakım saatimi seç", "data-tz-plan data-tz-place=saat")}</div>'
            '<p class="hero-note" style="color:#968B76">Çizim temsilidir; uzama hızı kişiden kişiye değişir.</p></div></div></div>')


def blk_inline(p: dict) -> str:
    return ('<div class="sec gutter"><div class="tz-inline" data-tz-inline><span class="eyebrow">Randevu davetiyesi</span>'
            '<h2>Üç dokunuşta <em>hazır</em>.</h2><div class="tz-inline-body"></div></div></div>')


# ----------------------------------------------------------------------------------------------- assemble
def scene(p: dict, s: str) -> str:
    name, _, arg = s.partition(":")
    if name in ("hijyen", "kartela", "firca", "wall", "versus", "final", "yol"):
        return inc(name)
    if name == "atelier":
        return inc("atelier-sec")
    if name == "sekil":
        return inc("sekil", arg)
    if name == "menu":
        return blk_menu(p, arg.split(","))
    if name == "how":
        return blk_how(arg)
    if name == "faq":
        return blk_faq(arg.split(","))
    if name == "soz":
        return blk_soz(arg)
    if name == "yerel":
        return blk_yerel(p, arg)
    if name == "foto":
        return blk_foto(p, arg)
    if name == "live":
        return '<div class="live" data-live="tirnak"></div>'
    if name == "visit":
        return '<div class="sec gutter" data-visit style="padding-top:0"></div>'
    return {"doktor": blk_doktor, "dahil": lambda: blk_dahil(p), "belirler": lambda: blk_belirler(p), "katman": blk_katman,
            "saat": lambda: blk_saat(p), "inline": lambda: blk_inline(p)}[name]()


def page_html(slug: str, inline: bool = False) -> str:
    p = BY_SLUG[slug]
    out = hero(p) + "".join(scene(p, s) for s in p["scenes"])
    if inline:
        for k, fn in INCLUDES.items():
            out = out.replace(f'<div data-tz-inc="{k}"></div>', fn())
    return out


def page_meta() -> dict:
    """What tirnak.js needs per page (no markup): fam, code, bar label, default option, semt, status, nav name."""
    return {p["slug"]: {"fam": p["fam"], "code": p["code"], "bar": p["bar"], "opt": p.get("opt"), "semt": p.get("semt", ""),
                        "status": p["status"], "wave": p["wave"], "nav": p["nav"], "semtFrom": SEMT_FROM.get(p.get("semt", ""), ""), "title": html.unescape(p["h1"].replace("<em>", "").replace("</em>", ""))} for p in PAGES}


def check() -> None:
    for tag, qs in QUOTES.items():
        for name, q in qs:
            rv = [r for r in REVIEWS if r["n"] == name]
            assert rv and q in rv[0]["t"], (tag, name, q)
    assert len(PAGES) == 22 and len(BY_SLUG) == 22


check()
