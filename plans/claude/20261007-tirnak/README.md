# TIRNAK ATELYESİ: tırnak ailesinin 22 sayfası, kaydırmalı hikâye (plan, 2026-10-07)

## Bağlam

**Sahibin isteği (10-07):** "Eski sayfaları yeni stile geçir. En kaliteli fotoğraf ve videoları seç. Kusursuz olsun; giren şaşırsın. Storytelling ve scroll tarzında olsun. Her sayfada gelen kişi randevu almak istesin." Ardından kapsam netleşti: **yalnızca tırnak sayfaları.**

**Kapsam dışı (dokunulmaz):**
- `plans/claude/20261007/` altındaki lazer, kalıcı makyaj ve Cilt Atlası planları.
- Prototipteki diğer vitrinler: salon, kaş, kirpik, lifting, kalıcı makyaj, cilt, lazer.

**Çalışma yeri:** Eski sunucudaki `/var/www/seldagencerbeauty.com/google-adsAI/` yapısı artık bu depoda:

| Sunucudaki yer | Bu depodaki karşılığı |
|---|---|
| `google-adsAI/patches/media_ig_20261007/out/` | `website/m/ig/` |
| `google-adsAI/patches/media_ig_20261007/{build_media.py, manifest.json}` | `sources/media_ig_20261007/` |
| `all_api_meta/instagram_exports/20261006-191757Z/media` (videolar) | `originals/instagram/videos/` (100 video) |
| Instagram fotoğraf orijinalleri, `instagram.db` | **depoda yok** (bkz. §1d) |
| Artifact kaynağı | `website/index.html` (= `prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/artifact-v3.html`) |

**Hedef Artifact:** https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM. Aynı Artifact güncellenir, yenisi açılmaz. 10-07'de okundu: canlı sürüm depodaki v3 ile aynı (205.394 bayt, 241 dosya).

**Bugünkü durum (ölçüldü):**
- Menüde 22 tırnak sayfası var. Prototipte bunlardan yalnız `nail-art-ankara` bir vitrine bağlı (`tirnak`). Kalan 21 sayfa "mevcut sayfa ↗" diye canlı sitedeki eski sayfaya gidiyor.
- Bugünkü `tirnak` vitrininde şunlar var:
  - Renk Atölyesi: 3 şekil × 8 renk, gerçek fotoğraf üzerinde ton eşleme.
  - 12 kartlık galeri, yorumlar, 4 satırlık menü.
  - **Hiç video yok** (yalnızca hikâye halkalarında). Kaydırmalı sahne de yok.
- Canlı site bu ortamdan erişilemiyor (proxy 403). Eski sayfaların H1, title, meta ve SSS metinleri sunucuda alınacak (§6.1).

**Bu incelemede bulunan hatalar (bu iş kapsamında düzeltilecek):**
1. **`tirnak-video-1` posteri bozuk.** Poster 0,8. saniyeden alınmış; o kare neredeyse bembeyaz bir geçiş karesi. Video 0–1,5 ve 11,5–12,9 saniyelerde de bu beyaz silmeyle açılıp kapanıyor.
2. **`tirnak-video-3`'e Instagram'ın ses ikonu gömülü.** İkon videonun tamamında sol altta duruyor (y≈1030–1130 px; bkz. `kanit/tam-kare-kontrol.jpg`). Hikâyede bugün olduğu gibi gösteriliyor.
3. **`tirnak-kare-kirmizi` yanlış etiketli.** Alt metni "Kırmızı kalıcı oje" diyor, oysa fotoğrafın üzerinde altın "PROTEZ TIRNAK" rozeti var. Renk Atölyesi bu kareyi "kare kalıcı oje" olarak sunuyor.
4. **Rozetler ve imza.** 7 fotoğrafta altın "PROTEZ TIRNAK" rozeti ile imza var, 1 fotoğrafta "JEL DESTEKLİ KALICI OJE" rozeti var. Sahnede ve tam ekranda dağınık duruyorlar.
5. **Çözünürlüğü düşük kareler büyük kullanılıyor.** 10 fotoğrafın kaynağı yalnız ~1080 px (çıktısı en fazla 800w). Bunlar tam ekran ya da hero olarak kullanılmamalı.
6. **Pedikür ve ayak için gerçek medya yok.** Ne işlenmiş kütüphanede ne de 100 ham videoda var.

---

## 1. Medya seçimi (işin en önemli kısmı)

Yöntem:
- 22 işlenmiş tırnak fotoğrafı ve 5 still (ürün/alet) karesi, en büyük boyutlarında tek tek incelendi (`kanit/fotograflar-*.jpg`).
- 100 ham videodan başka ailelere atanmamış 77'sinin ikişer karesine bakıldı. Tırnakla ilgili **21 aday** çıktı.
- Her adaydan 8 kare alındı (`kanit/videolar-1…5.jpg`; her sayfada beşer video, V21 son sayfada tek başına).
- Kullanılacak saniyeler tek tek okundu. Kritik kareler tam çözünürlükte cetvelle kontrol edildi.

### 1a. Videolar: seçilenler

Dosyalar: `originals/instagram/videos/*_<IG id>.mp4`. Hepsi 720×1280, 9:16.

| Slug (yeni) | V | IG id · tarih | Ne görünüyor | Kullanılacak aralık ve edit | Rol |
|---|---|---|---|---|---|
| `tirnak-film-giris` | V16 | 18187785991403175 · 08-13 | Krem takımlı kadın mermer lobiden SG logolu resepsiyona yürüyor → tırnak barında eldivenli uzman törpülüyor → badem french makro | **0,0–3,4 sn** (giriş + işlem, yazısız) ve **5,2–6,0 sn** (sonuç). 3,6 sn'den sonra "Selda Gençer'de" yazısı, 6,2 sn'den sonra "Premium Protez Tırnak" yazısı gömülü olduğu için kesilir. 60 kare film. | **Merkez sayfa açılışı: "Kapıdan tırnağa"** (T1). `yuz`: profil görünüyor, sahip onayı gerekiyor. |
| `tirnak-film-kartela` | V15 | 18118642289477894 · 08-13 (24 fps) | Bahçe yolu → frezeyle kırmızı oje çıkarma → **salonun gerçek, numaralı jel oje kartelası** → fırça → kare french | 1,4–2,0 (freze), **2,2–3,1 (kartela)**, 3,4–4,2 (fırça), **5,2–6,6 (sonuç)**. 0–1,0 (ilgisiz yol) ile 6,7 sn sonrası (sonradan eklenmiş yıldız efekti) kesilir. | Gerçek Kartela (T3), kalıcı oje açılışı. |
| `tirnak-film-firca` | V13 | 18374798185224149 · 08-07 | İnce fırçayla kırmızı mikro-french, altın kap, ızgaralı masa | **5,4–10,0 sn.** 1,5–2,6 sn'deki Instagram gönderi kartı ve 4,2–4,8 sn'deki bulanık geçiş kesilir. 48 kare film. | Fırça Darbesi (T4), nail art ve jel. |
| `tirnak-film-hijyen` | V11 | 18126120175637645 · 06-23 | Aletler yıkanıyor → kutu → altın lavabo → sterilizasyon cihazı → kişiye özel poşet | **Üstteki gömülü yazı bandı kırpılır:** 720×900 (4:5), y 380–1280. Yazıların yerine HTML'de onaylı dil kullanılır (§5). Adımlar: 3,6–6,0 · 8,4 · 10,9–13,3 · 15,7–18,1. | **Hijyen Yolculuğu** (T5): manikür, pedikür, medikal pedikür, el-ayak. |
| `tirnak-film-freze` | V17 | 18124896217778836 · 08-16 | Freze ucuyla eski jel alınıyor; siyah eldiven, toz, makro | 0,3–8,0 sn, yazı yok. | Protez çıkarma ile bakım ve dolgu açılışı. |
| `tirnak-film-hazirlik` | V05 | 18346810036246415 · 04-21 (43,9 sn) | Eldivenli manikür hazırlığı: freze, kütikül aleti | 17,5–21,5 · 26,5–31,0 · 40,5–43,5 sn | Manikür açılışı, tırnak güçlendirme. |
| `tirnak-film-orkide` | V19 | 18089498999286039 · 08-23 (42,6 sn) | Uygulama → **bordo badem tırnaklar ve beyaz orkide** | **38,5–42,6 sn** (final), 23,5–29,5 sn (uygulama; uzmanın yüzü kısmen görünüyor) | **Final perdesi** (T12), fiyat sayfaları. |
| `tirnak-film-krom` | V20 | 18226291744323491 · 08-26 | Simli krom french, badem, koyu fon | 5,5–12,0 sn. 0–2,5 sn'deki kolaj kesilir. | Yeni nesil tips, modeller. |
| `tirnak-film-babyboomer` | V04 | 18096499007018487 · 04-14 (bugünkü `tirnak-video-3`) | Baby boomer ombre, altın varak, bokeh | 0,3–9,8 sn. **720×960 üst kırpımla ses ikonu tamamen çıkar** (ikon y≈1030–1130). | Protez tırnak açılışı. |
| `tirnak-film-papatya` | V02 | 17898568689257024 · 2025-08-07 (bugünkü `tirnak-video-1`) | Badem ombre, 3D papatya, siyah eldiven | **1,6–11,0 sn; poster 5,6 sn.** Beyaz silme geçişleri kesilir. | Nail art reel. |
| `tirnak-film-lila` | V10 | 18213037222332820 · 06-13 (bugünkü `tirnak-video-2`) | Lila simli badem → süt beyazı badem | İkiye bölünür: 0,2–3,2 ve 5,0–8,6 sn | Modeller reel. |
| `tirnak-hijyen-oda` (still) | V12 | 18187340608376469 · 06-23 | Sterilizasyon odası, geniş açı | **Yalnız 4,4–6,4 sn** (yazısız) → poster ya da still. Videonun geri kalanında korku dili kullanan yazılar var ("…en çok korkmanız gereken…"). Kullanılmaz. | Fiyat ve pedikür sayfalarında arka plan. |

**Yedekler** (yalnız küçük kart):
- V01 18172308562331022: kare french, 3,0–6,8 sn. El titrek. 8 sn'den sonra beyaz çerçeve, 10,5 sn'den sonra logo kartı var.
- V09 17971149837066309: nude badem, koyu, 2,6–6,0 sn.
- V14 17930306856379485: kırmızı french ve nokta deseni, 5,0–9,2 sn. Bit hızı ~430 kbps, düşük.

**Elenenler:**
- **Fiyat yazısı gömülü:** V06 18011957690713082, V07 18100751945014092, V08 18180626833402501 ve 18125591554728667. Hepsinde "700₺" var; bu eski kampanya CRM'deki fiyatla çelişiyor.
- **Ekran yazısı gömülü:** V18 18099335882258707 (ortada "wow / perfect / love") ve V21 18189264124407162 (baştan sona başlık ve DM yazısı).
- **Kalite düşük:** V03 18056711009453399 (bulanık), 18094209241532965 (360p), 18125319967457903 (360×450).

### 1b. Fotoğraflar (`website/m/ig/`)

**Kadro A: kaynak ≥1338 px, tam ekran ve sahnede kullanılabilir.**
- `uzun-kirmizi`, `kare-kirmizi`, `badem-bordo`, `yuvarlak-kirmizi`: bu dördünün Renk Atölyesi maskesi var.
- `gumus` (1448×1931), `bakir-desen` (1440×1920), `lila-french` (1440²), `leopar` (1440²), `sut-beyaz`, `nude`, `kirmizi-2`, `lacivert-desen`.

**Kadro B: kaynak ~1080 px, yalnız kart ve galeride kullanılır (en fazla 1080w):**
`3d`, `holo`, `inci`, `mor`, `mermer`, `neon`, `bebek-mavisi`, `bordo-french`, `kirmizi-desen`, `lacivert`.

**"Vay" sırası** (Tasarım Duvarı'nda ilk görünenler):
1. `3d`: inci ve 3D çiçekli pembe stiletto
2. `holo`: aurora cat-eye
3. `mermer`: altın hatlı kelebek
4. `inci`: inci girdap
5. `mor`: ametist ve altın çatlak
6. `bakir-desen`: kaplumbağa kabuğu
7. `gumus`: simli ombre
8. `sut-beyaz`: süt beyazı badem
9. `bordo-french`

**Edit reçetesi** (`sources/media_ig_20261007/manifest_tirnak.json`, `--manifest` bayrağıyla; mevcut 88 öğenin çıktısı değişmez):

| Anahtar | Uygulama |
|---|---|
| `crop` | Rozetli 8 karede alttaki ~%16'lık rozet bandı kırpılır, 4:5 korunur. Ortadaki SG monogramı kalır. |
| `grade` | Yalnız pozlama, beyaz dengesi ve hafif `cas` keskinleştirme. **Oje rengi değiştirilmez**, sonuç rötuşlanmaz. |
| `sizes` | Kadro A'ya 1440w eklenir (desktop hero). Görsel hiçbir zaman büyütülmez. WebP + AVIF. |
| `trim`, `crop`, `poster_t`, `film`, `atlas` | Videolar §1a'daki aralıklarla kesilir. Döngüler 720p, sessiz, faststart. Sınırlar: hero ≤1,2 MB, diğerleri ≤0,8 MB. |
| `neutral` | `badem-bordo` için "nötr" katman üretilir. Mask var, neutral yok. Bu üretilince Renk Atölyesi'ne **4. şekil "Badem"** eklenir (davetiyede zaten "Badem" seçeneği var). |
| `label` | `kare-kirmizi` alt metni "Kırmızı kare protez tırnak" olur. Kesin tür IG altyazısıyla doğrulanır (§7, soru 7). |

**Kanıt (zorunlu):** Her öğe için `kanit/` altında temas sayfası üretilir. Bakılacaklar: yazı, fiyat ya da IG arayüz ikonu kalmamış mı; rozet temizlenmiş mi; iki yarıya aynı ayar uygulanmış mı; poster karesi temiz mi.

### 1c. Çekim listesi (gerçek medya olmayan sayfalar için; personel çeker, yarım gün)

**Kurallar:**
- Fotoğraf 4:5, en yüksek çözünürlük, filtre ve güzellik modu kapalı.
- Video 1080p, 9:16, 10–20 sn tek çekim, **yazısız ve müziksiz**.
- Önce ve sonra aynı ışıkta ve aynı açıdan çekilir.
- Her danışandan web kullanımı için KVKK rızası alınır.

| Öncelik | Sayfa | Çekilecekler |
|---|---|---|
| P1 | Kalıcı oje (Gerçek Kartela) | **Kartela, 4K, yukarıdan, gün ışığında**; her numara okunur olmalı. Etkileşim gerçek numaralarla çalışır. |
| P1 | Pedikür, medikal pedikür, ayak protez | Altın lavabolu ayak banyosu, pedikür koltuğu, steril poşetin ayak işleminde açılışı, sonuç (yüz yok) |
| P1 | Protez çıkarma, bakım ve dolgu | Aynı açıdan önce/sonra: uzama payı → dolgu; protez → doğal tırnak |
| P2 | Güçlendirme, uzatma, yeni nesil tips | Kırılgan doğal tırnak → jel; tips takılış klibi |
| P3 | Şölen b-roll | Tırnak barı geniş açı (akşam ışığı), LED lamba ışığı, fırça rafı, simli toz (60 fps) |

### 1d. Fotoğraf kütüphanesinin geri kalanı (önkoşul)

Instagram'daki tırnak paylaşımlarının yalnız 22'si işlenmiş. Videolardan, işlenmemiş başka iyi kareler olduğu anlaşılıyor (lila çiçekli, kırmızı tabut, simli ombre). Fotoğraf orijinalleri ve `instagram.db` depoda yok.

D1'i bekletmeden, iki yoldan biri seçilir:
- (a) Sunucuda aşağıdaki arama çalıştırılır. Seçilen orijinaller `originals/instagram/images/` altına konur, `instagram.db` salt okunur olarak eklenir.
  ```
  summary.json → delta.tsv → instagram_context.py --search "protez tırnak" | "kalıcı oje" | "nail art" | "manikür" | "pedikür" | "french" | "jel"
  ```
- (b) `build_media.py --manifest manifest_tirnak.json` sunucuda çalıştırılır ve çıktısı commit edilir.

`media.json` kullanılmaz.

---

## 2. Hikâye omurgası: her sayfa bir kaydırmalı film

**ATELİER v3 kuralları geçerli:**
- İlk saniyede dönüşüm.
- Ziyaretçi seyirci değil, sanatçı.
- Her şov tek bir WhatsApp butonuna bağlanır.
- Şov kademeye göre ölçeklenir (A/B/C) ve asla takılmaz.

**Tırnak hikâyesinin yedi perdesi:**

> Kapıdan girersiniz → elleriniz hazırlanır → renginizi seçersiniz → fırça değer → sonuç → başkalarının sözü → saatiniz.

Her perde, o perdede seçtiğiniz şeyi taşıyan bir CTA ile biter. Örnek: "Kiraz · badem · saatimi seç".

**Merkez sayfanın kaydırma senaryosu (storyboard):**

| Kaydırma | Görüntü | Metin ve etkileşim |
|---|---|---|
| 0 (100svh) | `tirnak-film-giris` ilk kare. Siyah kadife çerçeve, altın ışık süpürmesi | H1 yaldızla belirir. Çipler: ★ 4,6 · 263 · "1.000 TL'den" · "● Şu an açık". Başparmak bölgesinde [Saatimi seç] |
| %0–35 | Kadın lobiden resepsiyona yürür (kaydırmaya bağlı kareler) | "01 · Konutkent'te bir kapı" |
| %35–60 | Tırnak barı, törpü | "02 · Masanız hazır" |
| %60–100 | Altın ışık süpürmesi → badem french makro | "03 · Bir saat sonra" → [Bu sonucu istiyorum] |
| Perde 2 | Hijyen Yolculuğu (yapışkan, 4 adım) | Adım başlıkları + hijyen yorumlarından birebir alıntı |
| Perde 3 | Renk Atölyesi v2 + Gerçek Kartela | Parmakla boyama; seçim alt çubuğa yazılır |
| Perde 4 | Fırça Darbesi filmi | "Çizgi → renk → parlaklık" |
| Perde 5 | Tasarım Duvarı | Video kartlar görününce oynar. Her kartta "Bunu istiyorum" |
| Perde 6 | Söz duvarı | Kelimesi kelimesine Google yorumları |
| Perde 7 | Karar kartları + menü | Oje · güçlendirme · protez · tips |
| Final | `tirnak-film-orkide` döngüsü | "Sıradaki eller sizinki." [Saatimi seç] · WhatsApp · telefon |

---

## 3. İmza deneyimler (tırnak ailesi için yeni)

| # | Deneyim | Ne görür, ne yapar | Teknik |
|---|---|---|---|
| T1 | **Kapıdan Tırnağa** (açılış filmi) | Yukarıdaki storyboard. Kademe C'de poster ve üç satırlık metin gösterilir. | 60 kare WebP atlas. Mevcut `initWalk` deseniyle, ama atlastan çizer. LCP = AVIF poster ≤180 KB. |
| T2 | **Renk Atölyesi v2** | Mevcut ton eşleme korunur. Eklenenler:<br>- 4. şekil **Badem**.<br>- **"Parmağınla boya"**: sahnede yatay sürükleme rengi yumuşak bir fırça maskesiyle boyar. Dikey hareket sayfayı kaydırır (`touch-action:pan-y`).<br>- "↺ Yeniden" düğmesi. | Canvas ile açığa çıkarma maskesi. Mevcut `SW`, `SHAPES` ve SVG filtreleri yeniden kullanılır. |
| T3 | **Gerçek Kartela** | Kartela karesi üzerinde numaralı nabız noktaları (031–036, 046, 057, 643, 644, 653…). Dokununca renk yakınlaşır ve "Bu renk: 033" görünür. Seçim alt çubuğa ve WhatsApp mesajına girer.<br>Not: "Numaralar salondaki kartelanın videosundan okunmuştur; stok değişebilir." | Koordinatlar karede ölçülür. 4K çekim (P1) gelince yalnız görsel ve koordinatlar değişir. |
| T4 | **Fırça Darbesi** | Kaydırdıkça mikro-french çizilir: "Çizgi → Renk → Parlaklık". | 48 kare atlas. Kaydırmaya bağlı (`animation-timeline`, JS yedeği). |
| T5 | **Hijyen Yolculuğu** | Yapışkan sahnede 4 adım: Yıkama → Kurulama → Sterilizasyon cihazı → Kişiye özel paket. Yanında hijyen yorumlarından birebir alıntı. | Kırpılmış (4:5) film kareleri. Kademe C'de 4 kart alt alta. |
| T6 | **Tasarım Duvarı v2** | Vay sırasıyla masonry. Video kartlar görününce oynar (A/B kademesi). Basılı tutunca yakınlaşır.<br>Her kartta **"Bunu istiyorum"** düğmesi davetiyeyi `ref` ile açar: "Model: Holografik (sitedeki fotoğraf)". | Mevcut `card()` ve `openLightbox` genişletilir. |
| T7 | **Şekil ve Uzunluk** | 4 gerçek fotoğraf (oval → kare → uzun → badem) arasında kaydırıcı. Seçim davetiyedeki şekil adımını doldurur. | Mevcut `SHAPES`. |
| T8 | **Karar kartları** | Kalıcı oje · jel güçlendirme · protez · yeni nesil tips. Her birinde süre, fiyat (CRM) ve "kime uygun" (yalnız mevcut sayfa metinlerinden). | Mevcut `.versus` 4'lüye genişletilir. |
| T9 | **Bakım Saati** (bakım ve dolgu) | SVG tırnak, hafta kaydırıcısıyla uzar ve uzama payı görünür ("temsili").<br>[Fotoğrafımı göndereyim] düğmesi hazır WhatsApp mesajı açar: "Mevcut tırnağımın fotoğrafını gönderiyorum, bakım zamanı geldi mi?" | Saf SVG. Aralık bilgisi sahip onayıyla girer (§7, soru 8). |
| T10 | **Söz duvarı** | 9 tırnak yorumu ile manikür, pedikür ve protezden bahseden 3 salon yorumu, kelimesi kelimesine.<br>Öne çıkan ifadeler:<br>- "hiç acı hissetmedim"<br>- "protez tırnak hakkındaki ön yargılarım değişti"<br>- "incecik ama sağlam"<br>- "hiçbir atma vs. sorun yaşamadım"<br>- "Çok temiz bir yer öncelikle" | Kaynak `data/reviews_tirnak.json` (GBP). Not: "Google yorumlarından aynen." |
| T11 | **Davetiye v2** | Adımlar: işlem → şekil → renk no / model → gün → saat → WhatsApp.<br>Örnek mesaj: "Merhaba, manikür + protez tırnak + kalıcı oje için Perşembe 14:30 uygun mu? Şekil: badem, renk: 033, model: Holografik. [W-…]" | Mevcut `renderPlanner`. Yeni `ref` ve `colorNo` alanları eklenir. |
| T12 | **Final perde** | Orkide döngüsü, "Sıradaki eller sizinki.", altın [Saatimi seç], WhatsApp ve telefon. | `auto-vid` deseni. |

---

## 4. Sayfa sayfa (22 sayfa; her sayfanın kendi kimliği)

**Mimari:**
- Tek bir **`TIRNAK_PAGES`** veri tablosu kullanılır. Her sayfa için: `slug`, `aile`, H1, lede, hero, sahne sırası, plan seçenekleri, alt çubuk etiketi, SSS ve yorum süzgeci.
- Tek bir sayfa motoru çizer. Rota `#tirnak/<slug>` olur.
- Menüdeki 22 kaydın hepsi bu rotaya bağlanır; "mevcut sayfa ↗" kalmaz.
- Aileler: **merkez · oje · protez · art · bakım.**

| # | Sayfa | Aile / tür | Açılış | İmza sahne(ler) | Alt çubuk | Medya |
|---|---|---|---|---|---|---|
| 1 | `tirnak` (Nail studio) | merkez | T1 `tirnak-film-giris` | **Hizmet Yolu** (4 canlı video karosu → alt sayfalar), T5, T2, T6, T10 | "Tırnak randevum · saatimi seç" | tam |
| 2 | `nail-art-ankara` | art | `3d` + `tirnak-film-papatya` | T6 (vay sırası), T4, T11 | "Model: {seçilen} · saatimi seç" | tam |
| 3 | `kalici-oje` | oje | T2 Renk Atölyesi (ilk ekranda) | T3 Gerçek Kartela, T4, T10 | "{Renk} · {şekil} · saatimi seç" | tam |
| 4 | `kalici-oje-fiyatlari` | oje · fiyat | `tirnak-film-orkide` | **Menü ilk bölümde**, "Ne dahil?" kartları, T3 (kısa) | "{kalem} · saatimi seç" | tam |
| 5 | `jel-tirnak` | oje | `tirnak-film-firca` | T8 (jel · oje · protez), `lacivert-desen` | "Jel · saatimi seç" | ince |
| 6 | `tirnak-guclendirme` | oje | `lacivert-desen` (rozet kırpılmış) | Katman çizimi (SVG: doğal tırnak + jel katmanı, "temsili"), `tirnak-film-hazirlik` | "Güçlendirme · saatimi seç" | çekim P2 |
| 7 | `protez-tirnak` | protez | `tirnak-film-babyboomer` | T7, T6 (protez süzgeçli), T10 ("incecik ama sağlam") | "{Şekil} protez · saatimi seç" | tam |
| 8 | `protez-tirnak-modelleri` | protez | Tasarım Duvarı açılışı | Model süzgeci: French · Nude · Simli · Renkli · Desenli. Her kartta "Bunu istiyorum" | "Model: … · saatimi seç" | tam |
| 9 | `protez-tirnak-fiyatlari-ankara` | protez · fiyat | `gumus` | Menü ilk bölümde, "Fiyatı ne belirler?" (uzunluk · tasarım · bakım), T8 | "{kalem} · saatimi seç" | tam |
| 10 | `protez-tirnak-randevu` | protez · randevu | **Davetiye sayfada açık** (sheet değil, satır içi) | 3 adım, bugün/yarın çipleri, T10 (kısa) | "Saatimi seç" | tam |
| 11 | `protez-tirnak-bakim-dolgu` | protez | `tirnak-film-freze` | T9 Bakım Saati, fotoğraf gönder | "Bakım · fotoğrafımı göndereyim" | ince (çekim P1) |
| 12 | `protez-tirnak-cikartma` | protez | `tirnak-film-freze` | "Doğal tırnağı koruyarak" 3 adım (yalnız mevcut sayfa metninden), fotoğraf gönder | "Çıkarma · saatimi seç" | ince (çekim P1) |
| 13 | `tirnak-uzatma` | protez | `uzun-kirmizi` | T7 uzunluk (kısa / orta / uzun: `yuvarlak` → `kare` → `uzun`) | "{Uzunluk} · saatimi seç" | tam (tür IG'den doğrulanacak) |
| 14 | `yeni-nesil-tips` | protez | `tirnak-film-krom` | T8 (tips ve klasik protez; fark sahipten) | "Tips · saatimi seç" | çekim P2 |
| 15 | `ayak-protez-tirnak` | protez | Dürüst stand-in: `tirnak-film-hijyen` + `still-firca` | T5 | "Ayak · saatimi seç" | çekim P1 |
| 16 | `cayyolu-protez-tirnak` | protez · yerel | T1 + "Çayyolu'ndan ~2 km · Konutkent" | Yol çizgisi (SVG, temsili), park ve ulaşım, T6 (kısa) | "Çayyolu'ndan · saatimi seç" | tam |
| 17 | `yasamkent-protez-tirnak` | protez · yerel | T1 + "Yaşamkent'ten ~3 km · Konutkent" | Aynı | "Yaşamkent'ten · saatimi seç" | tam |
| 18 | `manikur-ankara` | bakım | `tirnak-film-hazirlik` | T5 Hijyen Yolculuğu, T2 (kısa) | "Manikür · saatimi seç" | tam |
| 19 | `pedikur-ankara` | bakım | Stand-in: `tirnak-film-hijyen` (altın lavabo karesi) | T5, pedikür yorumları | "Pedikür · saatimi seç" | çekim P1 |
| 20 | `medikal-pedikur` | bakım | Stand-in: `tirnak-hijyen-oda` | T5 ve dürüst bir "Ne zaman doktora?" kutusu. Yalnız bakım dili kullanılır (§5). | "Medikal pedikür · saatimi seç" | çekim P1 |
| 21 | `manikur-pedikur-fiyatlari` | bakım · fiyat | `tirnak-hijyen-oda` | Menü ilk bölümde, T5 (kısa) | "{kalem} · saatimi seç" | tam (fiyat CRM'den) |
| 22 | `el-ayak-bakimi` | bakım | `still-firca` + T5 | El ve ayak ritüeli adımları | "El & ayak · saatimi seç" | çekim P2 |

**Yerel sayfalar (16, 17):** Salonun adresi Konutkent'tir. "Çayyolu'nda/Yaşamkent'te salon" yazılmaz; yalnız mesafe ve yol tarifi verilir (`DIST`). Mevcut semt kişiselleştirmesi (`data-personal`) bu sayfalarda varsayılan olarak açılır.

**Stand-in ilkesi:** Gerçek medyası olmayan sayfalarda salonun gerçek odası, hijyen filmi ve aletleri gösterilir. Sahte önce/sonra konmaz. Proto panelinde "çekim bekliyor" rozeti görünür.

---

## 5. Randevu düzenekleri ve dil

**Her sayfada:**
1. İlk ekranda fiyat çipi ("…TL'den", CRM) ve başparmak bölgesinde CTA.
2. Ziyaretçinin seçimi (renk, şekil, model, uzunluk) **alt çubuğa yazılır**. Seçen kişi "kendi tırnağını" rezerve ediyormuş gibi hisseder.
3. Her perde CTA ile biter; sayfa final perdeyle kapanır.
4. WhatsApp mesajı seçimleri ve `[W-…]` kodunu taşır. Ekip, müşterinin ne istediğini ilk mesajda bilir.
5. Boş saat çipi prototipte "(örnek)" etiketiyle kalır. CRM'de `site-slots` gelince gerçek saat gösterilir. Uydurma saat yoktur.
6. Takip etiketleri: `data-track-label="at-tz-<sayfa>-<yer>"` (ASCII, en fazla 48 karakter).
   - Sayfa kodları: `merkez`, `art`, `oje`, `ojefiyat`, `jel`, `guclendir`, `protez`, `model`, `pfiyat`, `prandevu`, `dolgu`, `cikar`, `uzatma`, `tips`, `ayak`, `cayyolu`, `yasamkent`, `manikur`, `pedikur`, `medped`, `mpfiyat`, `elayak`.
   - Yer örnekleri: `hero-wa`, `kartela-no`, `boya`, `sekil`, `model-iste`, `foto-gonder`, `davetiye-wa`, `bar-saat`, `bar-tel`, `final-wa`.
   - WhatsApp ve telefon gerçek `<a href>` olarak kalır. Böylece contact-ping, SGB_VISIT ve Ads dönüşümü ek kod gerekmeden çalışır.

**Fiyatlar:**
- Fiyatlar yalnız CRM'den alınır (`/api/public/price-menu`). Derleme anında `sources/atelier_tirnak_20261007/data/crm_tirnak.json` dosyasına dondurulur.
- Prototipte CRM'den (10-06) alınmış 4 kalem; derlemede yeniden doğrulanır:

  | Kalem | Fiyat |
  |---|---|
  | Kalıcı oje | 1.000 TL |
  | Manikür + kalıcı oje | 1.100 TL |
  | Manikür + jel güçlendirme + kalıcı oje | 1.300 TL |
  | Manikür + protez + kalıcı oje | 1.500 TL |

  Nail art "kişiye özel".
- Pedikür, medikal pedikür, bakım-dolgu, çıkarma, tips ve ayak protez kalemleri CRM'den çekilene kadar "menüde" yer tutucusuyla kalır. **Instagram'daki "700₺" kampanyası kullanılmaz.**

**Kullanılacak dil (kanıtlı):**
- "Salonumuzda çekildi."
- Kelimesi kelimesine Google yorumları.
- "Kişiye özel paket, yanınızda açılır" (sahip onayıyla; §7).
- "Rengi kartelamızdan siz seçersiniz."

**Yasak:**
- "%100 hijyen", "tıbbi seviyede" (cihaz belgesi yoksa), "en iyi" / "1 numara", "kırılmaz", "hiç kalkmaz", "acısız" (kendi iddiamız olarak).
- Sahte önce/sonra; sahte kıtlık, geri sayım, popup.
- Rakibi kötüleyen ya da korku dili (V12'deki yazı tonu).
- Medikal pedikürde tedavi iddiası ("mantar tedavisi" vb.).

Derleme kontrolü (`--check`) bu kuralları metin taramasıyla zorlar.

---

## 6. Uygulama

### 6.1 Önkoşullar (D1'i bekletmez, ilgili sahne yer tutucuyla başlar)
- Canlı sitedeki 22 sayfanın H1, title, meta, canonical ve SSS metinlerinin anlık görüntüsü sunucuda alınır ve `sources/atelier_tirnak_20261007/data/live_pages.json` dosyasına konur. Prototip H1'leri bunlarla aynı tutulur.
- Ek veriler: `crm_tirnak.json`, `reviews_tirnak.json` (`gbp_cli.py reviews --raw`; "tırnak geçen X yorumun Y'si 5 yıldız" sayısı **yalnız** bu çıktıdan hesaplanır).
- §1d fotoğraf kütüphanesi.

### 6.2 Kod (`sources/atelier_tirnak_20261007/`, lazer klasörünün deseniyle)
- `render.py`: `TIRNAK_PAGES` → statik işaretleme. H1, poster ve metinler HTML'de olur; JS yalnız etkileşim ekler.
- `src/tirnak.css`, `src/tirnak.js`: T1–T12.
- **Ad çakışmasını önlemek için** tüm yeni fonksiyonlar `tz` önekiyle adlandırılır (`tzInitFilm`, `tzKartela`, `tzWall`…). Kalıcı makyaj planında `initKartela` ve `initFilmAtlas`, cilt planında `CILT_PAGES` var.
- `go()` rotasına `#görünüm/parametre` çözümü kalıcı makyaj planında da var. Hangisi önce uygulanırsa diğeri onu yeniden kullanır; iki kez yazılmaz.
- `build_proto.py`: `website/index.html` dosyasında **yalnız şunları** değiştirir:
  - `<section data-view="tirnak">` bloğu;
  - NAV'daki 22 tırnak kaydı;
  - `VIEWS`, `PLANS.tirnak*`, `STORIES.tirnak*`, `BAR`;
  - `initView` kancası, `autoLabel`;
  - proto paneline "Tırnak ▸" alt seçimi.

  Bunun dışındaki her bayt aynı kalmalı. Derleme sonunda, tırnak blokları dışında kalan kısım eski dosyayla karşılaştırılır.

### 6.3 Artifact yayını
- Önce `Artifact read` ile güncel sürüm okunur. Başka bir plan araya yayın yaptıysa onun üzerine kurulur.
- Yayın aynı URL'e yapılır. `files` ile yalnız yeni ve değişen tırnak dosyaları gönderilir. Değiştirilen eski dosyalara `null` verilir (`tirnak-video-1/3` ve posterleri).
- **Dosya sınırı düzeltmesi:** Önceki planlar sınırı toplam 255 dosya varsaydı. Araç sınırı **yayın başına 255, sürüm başına 511 dosya**. Tırnak için ~35 yeni dosya bekleniyor:
  - film atlasları ~10,
  - döngü videoları ve posterleri ~18,
  - kartela, kırpılmış fotoğraflar ve neutral ~7.

  Tek yayında sığar. Gerekirse iki yayına bölünür.
- Yayından sonra `prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/` altına yeni bir anlık görüntü (`artifact-v4-tirnak.html`) eklenir ve `website/index.html` eşitlenir.

### 6.4 Canlı sayfalara taşıma (prototip sahip onayı aldıktan sonra)
Lazer yamasının deseni kullanılır: `build.py --out / --check / --apply / --rollback`.
- **Korunanlar:** `<head>`, H1, title, meta, canonical, robots, JSON-LD, consent, gtag, `ads-tracking.js`.
- **Taşınanlar:** Eski bölümler "Detaylı bilgi" altında DOM'da kalır.
- İşaret `<!-- SGB_ATELIER_TIRNAK 20261007 -->`, yedek `.bak-20261007-attz`.
- Medya `public_html/images/ig/tirnak-*` altına gider.
- `--apply` komutunu sahip çalıştırır.

---

## 7. Sahibe sorulacaklar (D1'i bekletmez)

1. V16'daki kadın (salona giriş sahnesi) kim? Web'de kullanılmasına izin var mı?
2. Sterilizasyon cihazının adı ve türü nedir? Videoda "tıbbi seviyede" yazıyor; belge yoksa bu ifade kullanılmaz.
3. "Kişiye özel paket, yanınızda açılır" her manikür ve pedikürde geçerli mi?
4. Kartela numaraları ve oje markası sayfada yazılabilir mi?
5. CRM'deki tırnak kalemlerinin tam listesi: pedikür, medikal pedikür, çıkarma, bakım-dolgu, tips, ayak protez, uzatma, güçlendirme; her birinin süresi ve fiyatı.
6. Uzman adları sayfada yazılsın mı? Yorumlarda Ceren, Pelin, Melisa, Zelal ve Tamay geçiyor; yorumlar her durumda kelimesi kelimesine kalır.
7. `kare-kirmizi` ve `yuvarlak-kirmizi` protez tırnak mı, kalıcı oje mi? (IG altyazısından.)
8. Protez bakım aralığı ne söylenebilir? (T9 için; söylenemezse yalnız "fotoğrafını gönder" kalır.)
9. Yeni nesil tips ile klasik protez arasındaki gerçek fark nedir?

---

## 8. Doğrulama

1. **Medya:** `kanit/` temas sayfalarının hepsine bakılır. Yazı, fiyat ve IG ikonu 0; rozet temiz; poster karesi temiz; renk değiştirilmemiş olmalı.
2. **Ekran görüntüleri:** Playwright (`/opt/pw-browsers/chromium`) ile 22 rota çekilir:
   - 390×844 ve 1440×900; Mermer ve Gece; kademe A ve C.
   - T1'in %0 / %40 / %80 hâlleri, boyama öncesi ve sonrası, kartela dokunuşu, davetiye ve WhatsApp metninin açılmış hâli.
3. **Otomatik kontroller:**
   - JS hatası 0; yatay taşma 0 (320 / 390 / 430 / 1440).
   - Kırık `m/` referansı 0.
   - Her rotada H1 tekil ve canlı sayfanınkiyle aynı.
   - Her `a` ve `button` etiketli.
   - Her WhatsApp href'inde sayfaya özel mesaj ve `[W-]` var.
   - Yasak ifade 0.
   - Yayındaki dosya sayısı ≤255; sürümdeki toplam ≤511.
4. **Dokunulmazlık:** Tırnak blokları dışında `website/index.html` farkı 0 bayt. Diğer 7 vitrin için duman testi: açılıyor ve konsol temiz.
5. **Hız bütçesi:**
   - İlk ekran ≤180 KB; LCP ≤2,5 sn (mobil lab).
   - Sayfa toplamı ≤1,5 MB (A kademesi), ≤0,4 MB (C kademesi).
   - Videolar yalnız görünürken yüklenir.
6. **5 saniye testi:** İlk ekranda gerçek bir tırnak sonucu, fiyat çipi ve CTA birlikte görünmeli.
7. **Yayın sonrası:** `Artifact read` ile canlı sürüm ve dosya sayısı doğrulanır.

---

## 9. Dalgalar

| Dalga | İçerik | Yayın |
|---|---|---|
| **D1** | Medya v2 (§1a–1b; videolar depoda hazır), sayfa motoru, merkez + 4 aile vitrini, gerçek medyası tam olan 12 sayfa: 1, 2, 3, 4, 7, 8, 9, 10, 13, 16, 17, 18 | Aynı Artifact |
| **D2** | Kalan 10 sayfa (5, 6, 11, 12, 14, 15, 19, 20, 21, 22). Dürüst stand-in, SVG sahneler, "çekim bekliyor" rozeti | Aynı Artifact |
| **D3** | Çekim ve §1d fotoğrafları gelince yalnız `manifest_tirnak.json` güncellenir, yeniden derlenip yayınlanır | Aynı Artifact |
| **Canlı** | §6.4, sahip onayından sonra | Sahip `--apply` çalıştırır |

**Kanıt dosyaları:** `kanit/fotograflar-1.jpg`, `kanit/fotograflar-2.jpg` (22 fotoğraf + 3 video posteri + 5 still), `kanit/videolar-1…5.jpg` (21 aday video, her biri 8 kare, saniyeleriyle), `kanit/tam-kare-kontrol.jpg` (V16, V15, V04 ve V13'ün tam karesi; ses ikonu ölçüsü).

---

## 10. Uygulama durumu (2026-10-07, Artifact sürüm 4)

D1 ve D2 birlikte yayınlandı. 22 sayfanın hepsi prototipte `#tirnak/<slug>` rotasıyla açılıyor.
- 13 sayfa gerçek medyayla tam.
- 3 sayfada medya ince (`jel-tirnak`, `protez-tirnak-bakim-dolgu`, `protez-tirnak-cikartma`).
- 6 sayfa "çekim bekliyor" rozetiyle stand-in kullanıyor: `tirnak-guclendirme`, `yeni-nesil-tips`, `ayak-protez-tirnak`, `pedikur-ankara`, `medikal-pedikur`, `el-ayak-bakimi`.

Yayın 1791382406-9153: 278 dosya. 43 dosya eklendi, 6 dosya kaldırıldı (`tirnak-video-1/2/3` ve posterleri). Anlık görüntü: `prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/artifact-v4-tirnak.html`.

**Kod:** `sources/atelier_tirnak_20261007/`
- `render.py`
- `src/tirnak.css`
- `src/tirnak.js`
- `build_proto.py` (23 yama)
- `data/`

**Medya:** `sources/media_ig_20261007/build_tirnak.py` ve `manifest_tirnak.json`.

**Plandan sapmalar:**
- **Badem, Renk Atölyesi'nde yok.** `badem-bordo` maskesi çapraz duran tırnaklarda kompaktlık testini geçemiyor (doluluk 0,33 < 0,42). Parlak kenarlarda bordo şeritler kalıyor. Atölye şimdilik Uzun / Kare / Oval ile çalışıyor; davetiyede "Badem" seçeneği duruyor. Badem için elle çizilmiş bir maske gerekiyor. O gelince yalnız `TZ_LREF` ve `SHAPES` güncellenir.
- **Kartelada numara yerine ton adı var.** Numaralar videodan güvenle okunamıyor ve sahibin onayı gerekiyor (§7-4). 22 nokta ton adıyla çalışıyor ("Mercan", "Gül Kurusu"…). 4K kartela çekimi (P1) gelince `data/kartela.json` güncellenir.
- **Film kare sayıları:** `tirnak-giris` 48 kare / 4 atlas (plan 60), aralıklar 0,1–3,2 ve 5,2–6,4 sn. `tirnak-firca` 36 kare / 3 atlas, aralık 5,2–9,8 sn.
- **H1'ler canlı sayfalarla henüz eşitlenmedi.** `live_pages.json` (§6.1) sunucudan alınmadı. Canlıya taşımadan (§6.4) önce yapılmalı.
- **Doğrulama:** Test Chromium'u H.264 oynatamıyor. Bu yüzden videolar poster yedeğiyle (`.tz-vp`) doğrulandı. Gerçek tarayıcıda oynatma ayrıca bakılmalı.

**Kapsam dışı bulgu:** Kaş vitrini hâlâ `kas-cift-3` çiftini kullanıyor. Bu görselde yabancı filigran var.
