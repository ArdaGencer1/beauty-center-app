# KAŞ VE YÜZ "Hikâye": 5 sayfa, storytelling scroll (plan, 2026-10-07)

**Durum:** sahip planı onayladı (2026-10-07). Sahip kararları bölüm 7'de.

## Bağlam

Sahip, menüdeki **Kaş ve yüz** ailesinin bütün sayfalarının ATELİER
prototipinde (https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM) tamamlanmasını
istiyor. Ölçüt: kaydırdıkça anlatılan bir hikâye (storytelling scroll), en kaliteli
fotoğraf ve videolar, en iyi edit.

Kapsam, `NAV` içindeki "Kaş ve yüz" grubudur:

| Sayfa (NAV slug) | Bugün prototipte |
|---|---|
| `kas-alimi` | `kas` vitrini var (slider, Altın Oran Aynası, galeri, canlı slot, davetiye) |
| `kas-laminasyonu` | Vitrin yok, "mevcut sayfa ↗" ile dışarı gidiyor |
| `yuz-alimi` | Vitrin yok |
| `cene-alimi` | Vitrin yok |
| `dudakustu-alimi` | Vitrin yok |

**Bilinen fiyatlar** (prototipteki `PLANS.kas` ve menüden; CRM ile yeniden doğrulanacak):

| Hizmet | Fiyat | Süre |
|---|---|---|
| İlk deneyim · altın oran kaş alımı | 500 TL | 30 dk |
| Kaş alımı | 600 TL | 30 dk |
| Altın oran kaş alımı | 800 TL | 30 dk |
| Kaş laminasyonu | 2.500 TL | 60 dk |
| Yüz alımı, çene alımı, dudak üstü alımı, kına | **bilinmiyor** | — |

Bilinmeyen fiyatlar yalnız CRM'den (`panel…/api/public/price-menu`) okunur. Bu
konteynerden uç nokta 403 verdi; fiyatlar sunucuda okunacak. Okunana kadar sahnede
fiyat yerine "Fiyat menüde" bağlantısı durur; fiyat uydurulmaz.

**Yorumlar.** Prototipte `f:"kas"` etiketli 7 Google yorumu var; çoğu "Ebru Nur
Hanım"ı ve "altın oran"ı anıyor. Bunlar müşterinin yazdığı gibi kullanılır;
uzman adı ayrıca öne çıkarılmaz, portre kullanılmaz (sahip: gerek yok). Yüz alımı için
ayrı yorum yoksa olmayan yorum varmış gibi gösterilmez.

---

## 0. Acil düzeltme (bu planın ilk işi)

Prototip v3'te **başka uzmana ait fotoğraf hâlâ yayında**:

- `kas` vitrinindeki Altın Oran Aynası `m/ig/kas-cift-3-sonra-800.webp` kullanıyor.
- `KAS_PAIRS` listesinde `kas-cift-3` duruyor.

`kas-cift-3` (IG 18516297502030856) manifestte "TALITA …STRO" filigranı nedeniyle
dışlanmış durumda. PMU planı da bunu çıkarmayı söylüyor ama henüz uygulanmadı.
Yayındaki Artifact önce `Artifact read` ile okunur; hâlâ oradaysa:

- Altın Oran Aynası tabanı `kas-kina` "sonra" yarısına geçer (bkz. 1a), SVG
  noktaları yeni görsele göre yeniden ölçülür.
- `KAS_PAIRS` → `kas-cift-2`, `kas-altin-oran`, `kas-kina`, `kas-laminasyon`.
- `kas-cift-3-*` dosyaları yayında `null` ile kaldırılır.

---

## 1. Medya seçimi

### 1a. Görsel olarak doğrulanan kısa liste (6 öğe, 2026-10-07)

Manifest ve `media_index.json` ile ön elendi; yalnız bu 6 öğe açıldı.

| slug (IG id) | Kaynak | Ne görünüyor | Karar ve rol | Edit |
|---|---|---|---|---|
| `kas-altin-oran` (17969532135076932) | 1448×965 yarımlar | 3/4 açı, kapalı göz; dağınık kabarık kaş → keskin, yukarı taranmış kaş. **Setin en zarif karesi.** | **Kahraman** (`kas-alimi`, masaüstü) ve "Sonuç" perdesi | "Önce" altında komşu panelden ince şerit var → ortak kırpım. "ALTIN ORAN KAŞ" hapı ve imza "sonra"da göz köşesinde → iki yarıya aynı `crop` (üst ~%70). Kirpik kesimi kanıt sayfasında kontrol edilir. |
| `kas-cift-2` (18092748737430504) | 2048×1365 yarımlar | Gür, dağınık kaş + beyaz haritalama macunu → temiz, şekilli kaş. **En güçlü dönüşüm.** | Uyanış dönüşümü 01 ve hikâyenin "Okuma" perdesi | İki yarı farklı ölçekte → `align` (göz kapağı kıvrımı + burun kökü; işlem görmeyen noktalar). Alt şerit ve etiket için ortak kırpım (üst ~%68). Altyazı dürüst: "Haritalama sonrası, alım öncesi". |
| `kas-kina` (18196341943375941) | 1448×965 yarımlar | Sol yarı gerçek "önce" değil, **beyaz macunla haritalama anı**; sağ yarı kınalı, düz, önden temiz sonuç. | Hikâyenin "Haritalama" ve "Alım" perdeleri; sağ yarı **Altın Oran Aynası'nın yeni tabanı** | Etiket için ortak kırpım (üst ~%68). Aynı seans, aynı danışan olduğundan perde geçişinde süpürme ile birleştirilebilir. |
| `kas-profil` (17879042364617421) | dikey, 800×1066 çıktı | Yatakta uzanan danışan, kapalı göz, yandan; altın oran kaş. Keskin, sıcak ışık. | **Mobil kahraman** (4:5) ve **Final perde** | Alttaki "ALTIN ORAN KAŞ" hapı ve imza kırpılır (yaklaşık x %15–100, y %5–82 → 4:5). Kaşın üstündeki SG monogramı **kalır** (kıl üstünde silme = sonucu değiştirmek). |
| `kas-laminasyon` (18088049695997551) | **1080×540**, yumuşak | Aşağı dönük ince kıllar → yukarı taranmış, kahverengi, laminasyonlu kaş. "Önce" üstten kesik. | `kas-laminasyonu` galerisinde ikinci kanıt | Büyütme yok: en fazla 800w. Hafif `unsharp`, ortak renk ayarı. |
| `kas-3-adim` (18040684901410337) | 1335×555 bantlar | Önce · laminasyon uygulaması · sonuç, aynı danışan, 3 bant. 3. bantta kaşın üst sınırında soluk "@refreshed…" yazısı var; **sahip: başka bir yer değil, edit hatası → kullanılacak.** | **`kas-laminasyonu` Tarama perdelerinin gerçek fotoğrafları** (3 bant = 3 perde) | Yazı yalnız harf biçimli maskeyle ve yalnız cilt piksellerinde temizlenir (inpaint); kıllara dokunulmaz. Kutu `delogo` denendi: kılları bulandırdı, kullanılmaz. Kanıt temiz değilse yalnız 1. ve 2. bant kullanılır, sonuç `kas-laminasyon`dan gelir. |

**Açılmadan bırakılanlar (kural sınırı):**

- `kas-yakin` (18037699223717361): PMU planı aynı IG id'yi `pmu-kas-pudra` olarak
  kullanıyor. Pudralama (kalıcı makyaj) ise kaş alımı sayfasında **sonuç gibi
  gösterilemez**. Sahip netleştirene kadar yalnız PMU'da kalır.
- 17986864907913512: PMU'dan "laminasyon ve lifting, PMU değil" diye dışlanmıştı.
  **Sahip: güzelse kullanılsın.** Depoda yok; sunucuda 1 kez açılıp doğrulanır.
  Güzelse `kas-laminasyonu` kahramanı olur ve manifeste `kas-lam-lifting` olarak
  eklenir (PMU dışlaması geçerli kalır).

### 1b. Video: kaş ailesinde seçilmiş video yok

Manifestte kaş ve yüz alımı için video yok. Yerel `originals/instagram/videos/`
altında manifestte kullanılmayan **84 ham video** var: 61 tanesi 720×1280, 19
tanesi 360p (elenir). Altyazı bilgisi depoda yok; bu yüzden toplu açma yerine
sunucuda metin araması yapılır:

```bash
python3 /var/www/seldagencerbeauty.com/all_api_meta/instagram_context.py --search "kaş alımı"
# aynı komut: "altın oran", "laminasyon", "kına", "yüz alımı", "ip ile", "iple",
#             "cımbız", "bıyık", "dudak üstü", "çene"
```

Sonuçlar yalnız 720p+ yerel ham videolarla kesiştirilir. Her sayfa için **en fazla
3 video** kısa listelenir; her birinin yalnız posteri ve 3 karesi açılır.

Aranan anlar (varsa kaydırmaya bağlı film olur, yoksa çekim listesine gider):

| Sahne | Kullanım |
|---|---|
| İp/kalemle kaş haritalama | `kas-alimi` "Ölçüm" perdesi filmi |
| Cımbız veya iple alım yakın plan | "Alım" perdesi |
| Kına sürme ve silme | "Kına" bandı |
| Laminasyonda kılların fırçayla yukarı taranması | `kas-laminasyonu` "Tarama" filmi |
| İple yüz alımı ve cımbızla ince düzeltme | Yüz alımı ailesinin kahramanı |

Seçilen her video için mevcut `build_media.py` alanları kullanılır: `trim`,
`poster_t`, `yuz`. Film için 36 kare, 540×960, 4×3 atlas (PMU planındaki
`initFilmAtlas` deseni).

### 1c. Sayfa × medya matrisi

Durum değerleri: **tam** = gerçek sonuç kanıtı var · **ince** = zayıf · **çekim** = şimdilik dürüst stand-in.

| Sayfa | Kahraman | İmza sahnesi | Kanıt / galeri | Durum |
|---|---|---|---|---|
| `kas-alimi` (merkez) | `kas-altin-oran` slider (masaüstü), `kas-profil` (mobil 4:5) | **Bir Kaş, Beş Perde** (kaydırmalı hikâye) + Altın Oran Aynası (`kas-kina` sonra) | `kas-cift-2`, `kas-altin-oran`, `kas-kina` | tam |
| `kas-laminasyonu` | 17986864907913512 (güzelse), yoksa `kas-3-adim` 3. bant | **Tarama**: `kas-3-adim`'in 3 gerçek bandı + SVG fırça izi + "Hangisi bana göre?" | `kas-laminasyon` | tam (videosu çekim P1) |
| `yuz-alimi` | Altın çizgi SVG yüz portresi + `still-altin` (17880458079585542) | **Yüz Haritası** (bölgeye dokun → ip ve cımbız, süre, CRM fiyatı, sayfa) | — | çekim P1 |
| `cene-alimi` | Aynı motor, çene seçili | Yüz Haritası + **"Kalıcı çözüm?" köprüsü** → `yuz-lazer` (`lazer-film-cene`, "Yüz lazer epilasyon · salonumuzda çekildi" etiketli) | — | çekim P1 |
| `dudakustu-alimi` | Aynı motor, dudak üstü seçili | Yüz Haritası + "Kaç dakika?" zaman çizgisi (CRM süresi) + lazer köprüsü | — | çekim P1 |

**Dürüstlük:** lazer videoları yalnız lazer köprü kartında ve "lazer" etiketiyle
görünür; yüz alımının sonucu gibi sunulmaz. Yüz alımı sayfalarında önce/sonra
yoksa önce/sonra alanı açılmaz.

---

## 2. Edit reçetesi

PMU planının `build_media.py` eklerini (`file`, `crop`, `align`, `grade`,
`delogo`) aynen kullanır. PMU fazı bunları henüz yazmadıysa bu faz yazar, PMU
yeniden kullanır; ikisi ayrı ayrı yazmaz.

- **`grade:"kas"`**: nötr-sıcak; `eq` kontrast 1.04, doygunluk 1.02, gama .99;
  hafif `unsharp`. Bir çiftin iki yarısına **birebir aynı** uygulanır.
- **Yasak:** yalnız "sonra"yı parlatmak, cilt pürüzsüzleştirmek, kılları
  koyulaştırmak veya doldurmak, kaş üstündeki monogramı silmek, büyütmek.
- **Serbest:** ortak kırpım, iki noktalı hizalama, pozlama ve beyaz dengesi,
  etiket hapı ve imzanın kırpılması (kıl üstünde değilse).
- **Çıktılar:**
  - Artifact için çiftler tek dosya: `*-pair.webp` (önce|sonra yan yana), 1200w; laminasyon 800w.
    Canlı site ayrı 480/800/1200 yarımları kullanmaya devam eder.
  - `kas-profil-4x5` 480/800/1200.
  - Hikâye klibi (`reveal`, `xfade wipeleft` + altın dikiş): `kas-cift-2` ve
    `kas-altin-oran` için 9:16 ve 16:9, 6 sn, 1 MB altı. Sitede kullanılmasa bile
    Reels ve reklam için hazır olur.
- **Kanıt (zorunlu):** scratchpad'de `kasyuz/proof/` altında her çift için
  önce | sonra | %50 karışım sayfası. Hepsine bakılır: yabancı filigran (iris ve
  köşeler 2× yakın), etiket temizliği, ortak renk ayarı, hizalama, kirpik kesimi.
  Hizası tutmayan çift süpürme yerine yan yana gösterilir.

---

## 3. Sayfalar ve hikâye sahneleri

**Ortak görünüm:** sahne bölümleri siyah kadife ve altın; bilgi bölümleri
Mermer/Gece anahtarına uyar. Var olan `.dark-band`, `.foil-text`, `initDust`,
`initCompare`, `initGolden`, `initQuiz`, `tween`, `card()`, `openLightbox`,
`STORIES`, `rings` yeniden kullanılır.

**Yeni ortak bileşen `initScrolly`:** sabit (sticky) sahne + kaydırma ilerlemesi
(`--p` 0–1). Her perde bir görsel durum, bir başlık ve bir satırdan oluşur.
Destek varsa CSS `animation-timeline: view()`, yoksa `IntersectionObserver` +
`requestAnimationFrame`. Kademe C ve `prefers-reduced-motion` için perdeler alt
alta duran statik kartlara döner.

### `kas` → `kas-alimi`: "Bir Kaş, Beş Perde"

1. **PERDE (100svh).** Masaüstünde `kas-altin-oran`, mobilde `kas-profil` yavaş
   yakınlaşmayla açılır. Harf harf "Ankara Kaş Alımı", alt başlık "Yüzünüze göre,
   altın oranla." Çipler: ★ 4,6 · 263 yorum | 500 TL'den | Bugün müsait. Hikâye halkaları.
2. **BİR KAŞ, BEŞ PERDE** (`initScrolly`, 5 adım, her adımda "01/05"):
   1. *Okuma* — `kas-cift-2` önce: "Önce yüzünüzü okuruz."
   2. *Ölçüm* — Altın Oran Aynası çizgileri kaydırmayla çizilir (`kas-kina` sonra
      tabanı, 1 : 1,618). "Başlangıç, kavis, bitiş."
   3. *Haritalama* — `kas-kina` sol yarı (beyaz macun): "Çizginin dışını belirleriz."
   4. *Alım* — aynı karede kaydırmaya bağlı altın süpürme: macunlu kare → temiz kare.
   5. *Sonuç* — `kas-altin-oran` sonra, sinematik: "Doğal doluluk korunur."
   Sonda CTA: "Benim yüzüme göre ölçün" (`data-plan="kas" data-opt="altin"`).
3. **UYANIŞ.** 3 dönüşüm (`kas-cift-2`, `kas-altin-oran`, `kas-kina`), her biri
   kaydırmayla ilerleyen süpürme; hizmet adı, fiyat ve "Bunu istiyorum →"
   (`P.ref` = "Uyanış 02 · altın oran").
4. **KINA BANDI.** `kas-kina` sonra yakın plan; CRM'de kına kalemi varsa seçenek
   çipi olarak eklenir, yoksa yalnız anlatım.
5. **SÖZ.** 7 kaş yorumu, müşterinin yazdığı gibi; ek isim vurgusu ve portre yok.
6. **YOL HARİTASI kartları.** "Kaşlarım seyrek" → `pmu-kas` (microblading);
   "Kıllarım dağınık" → `kas-laminasyonu`; "Yüzümde ince tüy" → `yuz-alimi`.
7. **MENÜ (`#kas/fiyat`)** ve **SSS** (canlı sayfanın JSON-LD SSS'sinden kısaltılmış).
8. **FİNAL PERDE.** `kas-profil` üzerinde "Aynada ilk bakış." Altın "Saatimi seç",
   WhatsApp, telefon.

### `kas-lam` → `kas-laminasyonu`: "Tarama"

1. PERDE: laminasyon çifti, girişte otomatik süpürme.
2. **TARAMA** (`initComb`): ~120 SVG kıl dağınık durur; kaydırdıkça fırça geçer,
   kıllar yukarı taranır ve sabitlenir. Üç adım: kaldırma → sabitleme → besleme
   (adım metni canlı sayfadan). Her adımın arkasında `kas-3-adim`'in gerçek bandı
   durur; SVG yalnız fırça izini çizer ve "temsili çizim" etiketi taşır.
3. **HANGİSİ BANA GÖRE?** `initQuiz` ile 3 soru → kaş alımı · laminasyon ·
   microblading önerisi; her sonuç kendi sayfasına ve fiyatına gider. Tıbbi soru yok.
4. Kanıt, SÖZ (laminasyon yorumu yoksa "Salon için yazılanlar" etiketi), SSS, final perde.
5. Kirpik lifting (1.500 TL) yalnız çapraz bağlantı; "aynı seansta" gibi bir söz
   CRM veya sahip onayı olmadan yazılmaz.

### `yuz` → `yuz-alimi`, `cene-alimi`, `dudakustu-alimi`: "Yüz Haritası"

Tek vitrin, parametreli: `#yuz`, `#yuz/cene`, `#yuz/dudakustu`. H1, başlık ve
canonical her sayfanın kendisininkidir.

1. PERDE: kaydırdıkça altın çizgiyle kendini çizen SVG yüz portresi (fotoğraf
   gerekmez, sahte sonuç riski yok). Başlık sayfaya göre değişir.
2. **YÜZ HARİTASI** (`initFaceMap`): bölgeler alın, kaş arası, yanak, favori,
   dudak üstü, çene, boyun. Dokununca: yöntem (**ip ile ve cımbızla**; sahip
   onayı), süre ve fiyat (CRM), "Bu bölgeyi seç" → davetiyeye eklenir. Birden çok bölge
   seçilebilir; toplam yalnız CRM'de paket varsa gösterilir.
3. **ÜÇ PERDE** (`initScrolly`): *Hazırlık* → *Uygulama* → *Sonrası* (yatıştırma;
   iddia yok). Video gelene kadar `still-altin` ve `still-firca` (18107668510813428) stand-in.
4. **KALICI ÇÖZÜM?** köprüsü: `lazer-film-cene` döngüsü, "Yüz lazer epilasyon ·
   salonumuzda çekildi" etiketi → `yuz-lazer`.
5. SSS ve final perde.

### Gezinme ve randevu

- `VIEWS` + `kas-lam`, `yuz`. `go()` `#görünüm/parametre` biçimini çözer (PMU
  planıyla ortak; tek kez yazılır).
- `NAV` eşlemesi: `kas-alimi`→`kas`, `kas-laminasyonu`→`kas-lam`,
  `yuz-alimi`→`yuz`, `cene-alimi`→`yuz/cene`, `dudakustu-alimi`→`yuz/dudakustu`.
- `PLANS.kas` + laminasyon seçeneği; yeni `PLANS.yuz` (bölgeler, CRM fiyatlarıyla).
- Alt çubuk etiketi seçilen teknik veya bölgeyi gösterir ("Dudak üstü · saatimi seç").
- WhatsApp mesajına `P.ref` ("Referans: Perde 05 · altın oran", "Bölge: çene").
- Yeni düğmelerde `data-track-label="at-kas…"` / `"at-yuz…"` (ASCII, en çok 48).

---

## 4. Çekim listesi (personel, telefonla)

Teknik kurallar Cilt Atlası planıyla aynı: sabit telefon tutucu, aynı ışık ve açı,
güzellik modu ve filtre kapalı, 4:5 fotoğraf, 1080p 9:16 video, 10–20 sn tek
çekim, yazısız ve müziksiz, **her danışandan web için açık rıza (KVKK)**.

| Öncelik | Sayfa | Çekilecekler |
|---|---|---|
| P1 | kas-alimi | Haritalama ipi/kalemle ölçüm (5–10 sn), cımbız alım makro, kına sürme ve silme, aynada ilk bakış (yüz çevirme, 3 sn) |
| P1 | kas-laminasyonu | Kılların fırçayla yukarı taranma anı (makro, yandan ışık); önce/sonra aynı ışıkta 3 açı |
| P1 | yuz-alimi | İple alım yakın planı (eller + ip; yüz kısmi) ve cımbızla ince düzeltme makrosu |
| P2 | cene, dudak üstü | Yalnız uygulama anı (eller, ürün); hassas bölge için önce/sonra istenmez |
| P3 | b-roll | Altın cımbız ve fırçalar still-life, ayna önü ışık |

Teslim: Instagram'a atılanlar kütüphaneye düşer; atılmayanlar
`google-adsAI/patches/media_kas_20261007/drop/`.

---

## 5. Kod uygulaması (prototip)

- **Önce:** yayındaki Artifact `Artifact read` ile okunur. v3 anlık görüntüsünden
  yeniyse yeni sürüm taban alınır. `artifact-design` skill'i yüklenir.
- **Çalışma klasörü:** `scratchpad/kasyuz/` (`index.html`, `m/`, `proof/`).
- **`kasyuz_build.py`** (`a2_build.py`/`pmu_build.py` deseni, sayılı ve doğrulanmış `rep()`):
  - `data-view="kas"` bölümü baştan yazılır; `kas-lam` ve `yuz` bölümleri eklenir.
  - CSS bloğu `/* Kaş ve yüz hikâye */`: masaüstü, kademe C, reduced-motion.
  - JS: `initScrolly`, `initSweep` (`initCompare` tabanlı, kaydırmaya bağlı),
    `initComb`, `initFaceMap`, `initGolden` yeni koordinatlar, rota çözümü,
    `PLANS`, `STORIES.kas*`, `NAV` eşlemesi, `initView` kancaları.
  - `KAS_PAIRS` güncellenir; `kas-cift-3` hiçbir yerde kalmaz (derlemede `grep` ile 0 doğrulanır).
- **Dosya bütçesi (sınır 255):** v3'te 241 dosya; PMU planı ~249 bekliyor. Bu faz
  net en çok +6 dosya:
  - Eklenir: 4 `*-pair.webp`, `kas-profil-4x5` (tek boyut), varsa 1 film atlası.
  - Kaldırılır (`null`): `kas-cift-3-*`, ayrı `kas-*-once/sonra-*` dosyaları (çift dosyasına geçenler; başka yerde kullanılmadığı doğrulanır).
  - Derleme sonunda dosya sayısı hesaplanır; 255'i aşarsa yayın yapılmaz.
- **Yayın:** `Artifact publish`, aynı `url`; `capabilities` gönderilmez.

**Sıra bağımlılığı.** `AI_CONTEXT.json` sırası Lazer → PMU → Cilt. Bu faz PMU ile
yönlendirici, `build_media.py` ekleri ve dosya bütçesini paylaşır. Öneri: 0. bölümdeki
acil düzeltme hemen; geri kalanı PMU'nun ortak altyapısından sonra (ya da ortak
altyapıyı bu faz yazar, PMU kullanır).

---

## 6. Doğrulama

1. **Medya:** `kasyuz/proof/*` sayfalarının hepsi; `media_index.json` kayıtları;
   `kas-cift-3` ve `kas-3-adim` referansı 0.
2. **Ekran görüntüleri** (`shoot2.mjs` deseni, Playwright): iPhone 13 ve 1440
   masaüstü; Mermer ve Gece; kademe A ve C. Beş perdenin 5 kaydırma noktası,
   Uyanış 3 nokta, Tarama 3 durum, Yüz Haritası 3 bölge seçimi, `#yuz/cene` ve
   `#kas/fiyat` derin bağlantıları, davetiye ve WhatsApp metni.
3. **Otomatik:** yatay taşma 0, konsol hatası 0, dosya sayısı ≤255, kırık `m/`
   referansı 0, reduced-motion'da perdelerin statik açılması.
4. **CTA ve ölçüm:** WhatsApp/telefon CTA ve `[W-]` kodu; `data-track-label` kuralı.
   Canlı siteye geçilecekse `TAGCTX_RUNBOOK.md`: `audit --record`, `diff`,
   runtime `verify`, `patches/verify_tags.sh` geçmeden "tamam" denmez. Canlı
   `--apply` yalnız açık sahip onayıyla.
5. **Yayın sonrası:** `Artifact read` ile sürüm ve dosya sayısı.

---

## 7. Sahip kararları (2026-10-07) ve açık soru

| # | Konu | Karar |
|---|---|---|
| 1 | `kas-3-adim` yazısı | Dışlanmaz. Yazı başka bir yerin adı değil, edit hatası. Cilt üzerindeki harfler maskeyle temizlenir (bkz. 1a). |
| 2 | `kas-yakin` doğal kaş mı, pudralama mı? | **Açık.** Cevap gelene kadar yalnız PMU'da kalır. |
| 3 | Yüz, çene, dudak üstü yöntemi | **İp ile ve cımbızla.** Ağda yazılmaz. |
| 4 | 17986864907913512 (laminasyon + lifting) | Güzelse kullanılır; sunucuda doğrulanır. |
| 5 | Uzman adı ve portresi | Gerek yok. Portre çekilmez, ad öne çıkarılmaz. |

Hâlâ CRM'den okunacak: yüz, çene ve dudak üstü alımı fiyat ve süreleri; kına ayrı kalem mi?

## 9. Uygulama durumu (2026-10-07)

- **K0 — tamam.** Yayındaki Artifact'te `kas-cift-3` zaten başka bir oturumca
  kaldırılmıştı (Ayna `kas-kina` kullanıyordu, `KAS_PAIRS` 3 kart).
- **K1 — ilk kısım yayında, Artifact sürüm 13** (`1791386645-72f7`):
  - "Bir Kaş, Beş Perde" kaydırmalı bölümü (`#perde`, `initPerde`): 6 kare, 5 adım,
    aynı danışan geçişlerinde altın dikişli süpürme, kademe C ve reduced-motion'da
    alt alta statik kartlar.
  - Altın Oran Aynası: etiketsiz `kas-perde-alim-800` ile; SVG noktaları +17 px
    kaydırıldı, "1 : 1,618" sol üste alındı.
  - Kaş davetiye bloğu yerine "Aynada ilk bakış" kapanışı (`kas-profil-4x5`,
    `data-plan="kas" data-opt="ilk"`, `at-kas-perde-davetiye`).
  - Görseller: `sources/kas_perde_20261007/kas_perde.py` (işlenmiş 1200w yarımlardan,
    ortak kırpım ve renk ayarı). HTML değişiklikleri:
    `sources/kas_perde_20261007/kasyuz_build.py` (sayılı `rep()`; yayındaki HTML'e uygulanır).
  - Doğrulama: Playwright 390 ve 1440 genişlik; konsol hatası 0, yatay taşma 0,
    kaş medyası eksik 0; reduced-motion'da statik görünüm.
- **Mobil — yayında, Artifact sürüm 15** (`1791387535-eead`,
  `sources/kas_perde_20261007/kasyuz_mobile.py`, `kasyuz_build.py`'den sonra uygulanır):
  - Hero telefonda (≤699px) etiketsiz kırpım, 16:10; masaüstü hero değişmedi.
  - Beş Perde telefonda kenardan kenara 1.8:1, sahne sabit randevu çubuğunun üstünde,
    kaydırma ~%25 kısa; adım çubukları dokunulabilir (adıma atlar, 44px).
  - Galeri kaş kartları etiketsiz kırpımlar, 2:1; kart yazısı 11px.
  - Kapanış görseli telefonda en çok 44svh; başlık ilk ekranda.
  - Kaş SSS başlıkları 44px dokunma alanı.
  - Doğrulama: 360×740 ve 390×844; konsol hatası 0, yatay taşma 0, 40px altı dokunma alanı 0.
- **K1 kalan:** Uyanış ayrı bölüm olarak yapılmadı (dönüşümler Beş Perde ve mevcut
  galeride); kına bandı CRM'de kına kalemi netleşince.
- **K2, K3:** başlanmadı.
- **Not:** Artifact'e aynı anda başka oturum (lazer) da yayın yapıyor; her yayından
  önce en yeni sürüm okunup `kasyuz_build.py` onun üstüne uygulanmalı.

## 8. Dalgalar

| Dalga | İçerik | Yayın |
|---|---|---|
| **K0** | `kas-cift-3` acil çıkarma, Altın Oran Aynası yeni taban | Aynı Artifact |
| **K1** | Medya v2 (4 çift + `kas-profil`), `initScrolly`, `kas-alimi` "Beş Perde" tam sayfa | Aynı Artifact |
| **K2** | `kas-laminasyonu` + Yüz Haritası motoru ile 3 yüz sayfası (SVG ve dürüst stand-in), proto panelde "çekim bekliyor" rozeti | Aynı Artifact |
| **K3** | Sunucu IG araması ve çekimlerden gelen video/fotoğraflarla stand-in'lerin değişimi; yalnız manifest güncellenir, yeniden derlenir | Aynı Artifact |
