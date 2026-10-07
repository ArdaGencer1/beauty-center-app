# SALON: Salon grubunun 8 sayfası, storytelling scroll (plan, 2026-10-07)

## Bağlam

Sahip, menüdeki **Salon** grubunun bütün sayfalarının ATELİER prototipinde
(https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM) storytelling scroll
tarzında tamamlanmasını istiyor. Ölçüt: en kaliteli fotoğraf ve videolar, en
iyi edit.

**Salon grubu (menüde 8 kayıt):**

| Menü adı | Canlı slug | Prototipte bugün |
|---|---|---|
| Ana sayfa | `/` | `salon` görünümü var (walk filmi, kartlar, mozaik, yorumlar, belgeler) |
| Güzellik merkezi | `guzellik-merkezi` | yok, canlı sayfa yeni sekmede açılıyor |
| Tüm hizmetler | `hizmetler` | yok |
| Fiyat listesi | `price-menu` | yok |
| Özel gün makyajı | `ozel-gun-makyaji` | yok |
| İletişim | `iletisim` | yok |
| Konum ve yol tarifi | `konum` | yok |
| KVKK | `kvkk` | yok |

**Canlı Artifact, depodaki anlık görüntünün çok ilerisinde.**

- Yayınlanan sürüm `1791387535-eead`: 335 dosya, `index.html` 1.117.539 bayt.
- Depodaki `artifact-v3.html`: 205.395 bayt.
- Canlıda olup v3'te olmayanlar: 6 lazer görünümü, 9 vücut görünümü
  (`VUCUT_PAGES`), tırnak sayfa motoru (`TZ_PAGES`), cilt perdeleri ve sprite
  film (`caFilm`), tırnak hijyen kareleri.
- **Sonuç:** salon işi v3'ten değil, canlı sürümden başlar (bkz. D0).

**Medya envanteri dar.** Manifestte 9 salon ve 5 still kaydı var; 8 sayfa için
yetmez. Bu yüzden görsel açmadan geniş tarama yapıldı (bkz. 0). Görsel
doğrulama kural sınırında kaldı: 6 görsel ve 3 video.

**Geçerli kurallar:**
- Yalnızca gerçek salon medyası. Stok, üretilmiş ya da kaynağı belirsiz kare
  "salonumuz" diye gösterilmez.
- Fiyatlar yalnızca CRM'den (`PLANS`) gelir. Uydurma fiyat, süre ya da vaat yok.
- Yeni Artifact yok; her dalga aynı URL'ye yayınlanır.
- Canlı siteye sahip onayı olmadan `--apply` yok.
- CTA, WhatsApp ya da telefon bağlantısı değiştiği için TagCtx kapısı zorunlu.

---

## 0. Bu incelemede doğrulanan bulgular

Ölçümler görsel açmadan yapıldı: ffprobe, `scdet` sahne kesmeleri, Laplace
netliği, kırpılmış ışık yüzdesi, R−B sıcaklığı ve çok ölçekli NCC eşleme.

1. **Ana sayfadaki 7 karenin kaynağı kanıtlanamadı:** `m/walk-06…10.webp`,
   `m/cert-wall.webp`, `m/cert-trophy.webp`.
   - Hiçbirinin IG kimliği yok. Hepsi 720×960.
   - 100 ham videoya karşı en yüksek eşleşme 0,59.
   - 4 salon videosuna karşı en yüksek 0,49.
   - 124 işlenmiş fotoğrafa karşı en yüksek 0,69.
   - Gerçek bir kırpımda 0,8'in üstü beklenir.
   - **Karar:** sunucuda `instagram.db` kütüphanesindeki 392 öğeye karşı
     algısal hash kontrolü yapılır. Eşleşmeyen kare kaldırılır (D0 kapısı).
2. **`salon-cephe` (17877211629689213, 2026-08-21) canlıda hiç kullanılmıyor,
   ama salonun en değerli kaynağı.**
   - 5 ayrı çekim: cephe tabelası, monogramlı resepsiyon, **gerçek sertifika
     duvarı ve altın kalp ödülü**, lobi, ağaçlı koridor.
   - Sertifika çekimi, kaynağı belirsiz `cert-*` karelerinin yerini alır.
3. **`salon-giris` filminin son 1,5 saniyesi bozuk.**
   - 10,0–11,54 sn arası netlik 36; diğer bölümlerde 560–1330.
   - Film karelerinden f60–f71 6–11 KB (karanlık ya da bulanık).
   - Ana sayfa walk'ında kaydırmanın yaklaşık %47–56'sında görünüyor.
   - **Karar:** film 0–10,0 sn olarak yeniden üretilir.
4. **`still-altin` ve `still-kutu` üretilmiş ya da stok görünümlü.**
   - Kusursuz ışık huzmeleri, render tipografi ("SELDA GENÇER BEAUTY CENTER"
     defter), pürüzsüz kabartma kutu.
   - Kanıt olarak kullanılmaz; sahibe sorulur.
   - Aynı soru `still-firca`, `still-kirpik` ve `still-urun` için de geçerli.
     `still-firca` canlıda kullanılıyor.
5. **Açılış yılı doğrulanmalı.**
   - Video 2024-04-02'de paylaşılmış.
   - İlk karedeki afiş: "12 MAYIS · GÜLBEN ERGEN'İN AÇILIŞ TÖRENİ HATIRASI".
   - 2 Nisan 2024'te yayımlanan video 12 Mayıs'taki bir töreni gösteriyorsa
     tören en geç 2023'tür.
   - Canlıdaki "2024 · Açılışımız" etiketi doğrulanana kadar yıl yazılmaz.
6. **`salon-tur` (18014729837423154, 2024-07-05) yalnızca parça parça
   kullanılabilir.**
   - 800 kbps, 0,5 sn'lik hızlı montaj.
   - Bazı çekimlerde pencerelerin %18–27'si patlak.
   - İç mekân 2024'ten bu yana değişmiş olabilir; sahibe sorulur.
7. **Lobi fotoğraflarında tanınabilir danışanlar var.**
   - `salon-lobi`, `salon-lobi-2`, `salon-merdiven`, `salon-resepsiyon`
     (`yuz: true`).
   - Sahibin "yüz sorun değil" onayı sonuç fotoğrafları içindi; bekleme
     salonundaki danışanlar ayrı konu.
   - Varsayılan: yüzü kadraj dışında bırakan kırpım. Sahip izin verirse tam kare.
8. **Ham videolarda başka lobi veya resepsiyon B-roll'u yok.**
   - Salon karelerine benzerlikte en yüksek 0,77; eşik 0,80.
   - Eksikler çekim listesine gider (bkz. 5).
9. **Dosya sınırı yanlış biliniyor.**
   - 255, tek yayındaki sınır. Bir sürüm 511 dosyaya kadar tutabilir.
   - Canlıda bugün 335 dosya var.
10. **v3 anlık görüntüsünde düzeltilmiş eski hatalar duruyor.**
    - Dışlanan `kas-cift-3` (başka uzmanın filigranlı işi) ve
      `cilt-yarim-1` mozaiği v3'te hâlâ var; canlıda temizlenmiş.
    - Depodaki anlık görüntü yenilenmeli.
11. **Yönlendirme çakışması.** Ana sayfadaki `<div id="hizmetler">` ile yeni
    bir `hizmetler` görünümü hash yönlendirmesinde çakışır. Bölümün kimliği
    `hizmet-kartlari` olur.

---

## 1. Hikâye kurgusu: 8 sayfa, tek ziyaret

Her sayfa bir ziyaretin farklı anını anlatır, aynı medya aynı rolü iki kez
oynamaz.

| Sayfa | Anlatılan an | Ton | Kahraman |
|---|---|---|---|
| Ana sayfa | "Kapıdan içeri" kısa tanıtım | sinematik, 9 durak | S1 giriş filmi |
| Güzellik merkezi | **Bir ziyaretin tamamı** (amiral sayfa) | 12 perde | S2 cephe → S3 resepsiyon |
| Konum | "Kapımıza kadar" yolculuk | harita → bina → kapı | S2 cephe tabelası |
| İletişim | "Size en hızlı yol" | kısa, 3 perde | S3 monogramlı resepsiyon |
| Tüm hizmetler | Hizmet atlası | kategori bölümleri | aile kahramanları (mevcut) |
| Fiyat listesi | Menü | önce işlev | S8 resepsiyon, yavaş Ken Burns |
| Özel gün makyajı | Hazırlık sabahı | medya bulunursa | **arama ya da çekim bekliyor** |
| KVKK | Metin | tipografik, efektsiz | monogram |

---

## 2. Medya kadrosu (seçim ve edit reçetesi)

Kaynak yollar:
- Videolar: `originals/instagram/videos/<tarih>_<id>.mp4`.
- Fotoğraflar: sunucuda `all_api_meta/instagram_library/media/`.

Ölçüm sütunları: **netlik** = Laplace varyansı (800 px ya da 180 px, kendi
içinde karşılaştırılır) · **kırp%** = 250 üstü piksel oranı · **R−B** =
sıcaklık.

### 2a. Kadro

| # | Kaynak (slug · IG id) | Çekim / zaman | Ne | Ölçüm | Rol | Durum |
|---|---|---|---|---|---|---|
| S1 | salon-giris · 17877053286496908 | **0,0–10,0 sn**, tek kesintisiz çekim | Cephe → kırmızı halı → cam kapı → resepsiyon | netlik 560–1330; son 1,5 sn 36; R−B −10,6 (soğuk) | Ana sayfa walk, Konum perde III | doğrulandı, kırpılacak |
| S2 | salon-cephe · 17877211629689213 | çekim 1: 0,0–1,0 sn (en net 0,3) | Cephe ve tabela | 2234; kırp 1,9 | Konum kahramanı, GM perde I | doğrulandı |
| S3 | 〃 | çekim 2: 1,0–2,0 (1,3) | Monogramlı resepsiyon duvarı | 1964 | İletişim kahramanı, GM perde III | doğrulandı |
| S4 | 〃 | çekim 3: 2,0–2,93 (2,1) | **Sertifika duvarı ve altın kalp ödülü** | 1144 (orta) | `cert-*` yerine; GM perde IX | doğrulandı |
| S5 | 〃 | çekim 4: 2,93–3,87 (3,1) | Lobi, kadife koltuk, bar tabureleri | 1919 | GM perde IV | doğrulandı |
| S6 | 〃 | çekim 5: 3,87–4,71 (3,9) | Ağaçlı salıncak, mermer koridor | **3560** | Walk "Sessiz koridor", GM perde V | doğrulandı |
| S7 | salon-merdiven · 18081951466894957 | 1440×1464 | Altın çıtalı merdiven, koltuklar, arkada resepsiyon | 911; gürültü 2,97 | **En güçlü kompozisyon:** walk "Bir kat yukarı", GM perde V | doğrulandı; yüz kırpımı |
| S8 | salon-resepsiyon · 17915368251233815 | 1440² | Kasetli tavan, resepsiyon bankosu, cam cephe | 1073 | Fiyat listesi kahramanı, İletişim | doğrulandı; yüz kırpımı |
| S9 | salon-lobi-2 · 18083680814252903 | 1440² | Cam cepheli bekleme salonu, bar | 672; koyu %10,6 | GM perde IV (ikinci kare) | doğrulandı; gölge açma |
| S10 | salon-lobi · 18206708032335644 | 1440² | Merdiven önü lobi, **ön planda tanınır danışanlar** | 558 | Yalnızca sahip izin verirse | koşullu |
| S11 | salon-tur · 18014729837423154 | 1,03–2,07 (1,7) · 6,52–7,55 (7,3) · 7,55–8,24 (7,6) · 24,59–25,62 (24,8) | Pedikür koltukları, tırnak masaları, tırnak barı geniş, salıncak | 2368 / 1426 / 2526 / 1551; kırp ≤1,7 | GM perde VI "Tırnak barı", walk durak 07 | 2024: güncellik sorulacak |
| S12 | acilis · 18032788969913973 | 0–1,67 · 3,27–4,77 (4,4) · 6,2–7,8 (7,3) · 16,2–17,2 (16,6) · 20–30,67 (21,9) | Afiş, cephe, varış, kurdele, kalabalık | 1800–3041 | GM perde XI "Açılış", mevcut hikâye | **yıl kapısı** |
| S13 | acilis-foto · 18045137929722800 | 1080² | Açılış günü | 2581 | Açılış kartı (mevcut) | yıl kapısı |

**Başka ailelerden, canlıda zaten yayında ve kendi planlarında doğrulanmış
salon kareleri:**
- Hijyen: `tirnak-hijyen-1…4` (yıkama → kurutma → sterilizasyon → kişiye
  özel paket) ve `tirnak-hijyen-oda`.
- Cilt odası: `cilt-kubbe.mp4` ve `cilt-led-dongu.mp4`.
- Lazer: `lazer-koltuk`, `lazer-uzman`.
- Vücut: `vucut-slimtone-cihaz`.
- Tırnak: `tirnak-kartela`.

**Kullanılmayacaklar ve kapıdakiler:**

| Varlık | Karar | Gerekçe |
|---|---|---|
| still-altin · 17880458079585542 | kanıt olarak kullanılmaz | Üretilmiş ya da stok görünüm, render tipografi |
| still-kutu · 18104790091800124 | kanıt olarak kullanılmaz | Aynı |
| still-firca, still-kirpik, still-urun | sahibe sorulur | 1254 ve 1179 piksellik standart dışı boyutlar, aynı seri |
| m/walk-06…10, m/cert-wall, m/cert-trophy | D0 hash kapısı; eşleşmezse kaldırılır | Hiçbir kaynağa izlenemedi (bkz. 0.1) |
| salon-tur 18,31–19,07 · 20,14–20,83 · 22,97–24,59 sn | kullanılmaz | Kırpılmış ışık %18–27 |
| salon-tur 0,55–1,03 · 8,76–12,38 · 19,07–20,14 sn | kullanılmaz | Netlik 74–287 |

### 2b. Edit reçetesi: "Salon" tonu

**Dürüstlük kuralları:**
- Nesne silme, gökyüzü değiştirme, insan ya da dekor ekleme yok.
- SG filigranı ve monogram kalır.
- Görsel büyütülmez: video kareleri en fazla 720w, fotoğraflar en fazla 1200w.
- Danışan yüzü yalnızca kırpımla kadraj dışına alınır. Kişi silinmez.

**Ton birliği.** Bugün videolar soğuk (S1 R−B −10,6; açılış −17,1),
fotoğraflar sıcak (+3…+13).

- Hepsi tek hedefe çekilir: **R−B +6…+12, ortalama parlaklık 120–150**.
- Başlangıç zinciri:
  `colortemperature=temperature=5600:mix=0.5,eq=contrast=1.04:saturation=1.03:gamma=0.99,curves=master='0/0 0.75/0.74 1/0.95'`.
- Değerler varlık başına ayarlanır. Hedef, bu incelemede kullanılan ölçüm
  betiğiyle otomatik kontrol edilir.
- `curves` omzu, cam cephe ve pencere ışığını korur (salon-tur dersi).

**Mimari fotoğraflar (S7–S10):**
- `lenscorrection` ile geniş açı bükümü hafifletilir.
- `perspective` ile dikeyler (kapı, kolon, cam kasa) ±0,5° içinde düzeltilir.
- Kırpımlar: 4:5 (1152×1440 → 1200w) ve 9:16 (810×1440 → 720w).
- S9'a gölge açma (`curves` alt uç 0/0.03).
- S7'de gürültü 2,97: `hqdn3d=1.5:1.5:3:3`, sonra `cas=0.35`.

**Video çekimlerinden film (S1–S6, S11):**
- Her çekim kendi başına bir kaydırma filmidir: 1 sn'lik kamera hareketi,
  sticky bir perde boyunca kaydırmayla oynatılır. Kaydırdıkça kamera ilerler.
- Kesme olan yerde film bölünür. Montaj kesmesi kaydırmanın ortasına
  düşmez (salon-cephe ve salon-tur montaj).
- 540w kareler, tek **sprite WebP** (sütun 6, q60), çekim başına en fazla
  ~700 KB. B kademesinde kareler yarıya iner.
- S1: 0–10,0 sn, 60 kare, hafif `vidstabdetect`/`vidstabtransform` (ilk 2
  sn hareket 35).
- Her çekime en net karesinden poster (yukarıdaki "en net" zamanları):
  480w ve 720w, 4:5 ve 9:16.
- Açılış (S12) film yapılmaz. Hikâye klibi olarak kalır: 0–9 sn yerine
  yukarıdaki 5 çekimden 8 sn'lik kurgu, sesiz ve yazısız.

**Ken Burns (S8):** `zoompan` ile 6 sn'lik yavaş yaklaşma, 4:5 ve 9:16,
1 MB altı. Fiyat listesi kahramanı.

### 2c. Üretim

- `build_media.py` için ayrı `manifest_salon.json` ve `--manifest` bayrağı
  (cilt planındaki öneriyle aynı). Mevcut 111 kaydın çıktısı değişmez.
- Yeni anahtarlar:
  - `shots`: `[[t0, t1, ad, en_net_t], ...]`
  - `sprite`: `{cols, w, q}`
  - `grade: "salon"`
  - `persp`
  - `face_crop`: yüzü dışarıda bırakan kutu
  - `kenburns`
- Çıktı adları:
  - `film/salon-giris.webp` (sprite)
  - `film/salon-cephe-s1…s5.webp`
  - `film/salon-tur-s1…s4.webp`
  - `salon-cephe-s{n}-{480,720}.webp`
  - `salon-merdiven-4x5-{800,1200}.webp`, `salon-resepsiyon-kb.mp4` vb.
- Her çıktı için `provenance.json`: dosya → IG id, permalink, zaman aralığı,
  zincir. Kaynağı olmayan dosya yayına girmez (bkz. 7).

---

## 3. Sayfa motoru (prototip)

- **`SALON_PAGES`** veri yapısı, `VUCUT_PAGES` desenindedir. Her sayfa için:
  - `id`, `nav`, `h1`, `lede`
  - `acts`: `[{k, kind: film|still|loop|kb|type, src, cap, h, p, quote}]`
  - `cta`, `trackPrefix`
- **Tek `initSalonStory(view)`**, canlıdaki parçaların genelleştirilmesidir:
  - cilt perdelerindeki sticky katmanlar, Roma rakamlı sayaç ve
    IntersectionObserver (`rootMargin -45%`);
  - `caFilm` sprite kaydırması `spriteFilm(sec, src, n, cols, fw, fh)` olarak
    ortaklaşır. Walk ve film de bu fonksiyonu kullanır.
- **Görünüm adları:** `gm`, `tum-hizmetler`, `fiyat`, `ozel-gun`,
  `iletisim`, `konum`, `kvkk`.
  - `NAV`'daki Salon kayıtlarına üçüncü eleman eklenir; prototip içinde açılır.
  - Prototip panelinin "Sayfa" bölümüne "Salon ▸" alt seçimi eklenir.
  - `VIEWS` listesi genişler.
- **Tek NAP kaynağı:** adres, saat ve telefon bugün en az 4 yerde elle yazılı
  (visit bloğu, SSS, arama sayfası, semt sayfaları). Tek `NAP` nesnesine alınır.
- **Kademeler:**
  - A: tam film.
  - B: yarı kare.
  - C ve `prefers-reduced-motion`: film yok; en net posterler ve metin okunur
    kalır.
- **Ölçüm:** `data-track-label="at-<görünüm>-<öğe>"`. WhatsApp yalnızca
  `waHref(... visitCode())` ile. Yeni form ya da uç nokta yok.

---

## 4. Sayfa sayfa

### 4.1 Ana sayfa (`salon`): revizyon

- **Walk:**
  - S1 filmi 0–10 sn sprite olur. Durak sınırları yeniden hesaplanır
    (bugün 13/36/54. kare).
  - Kaynağı belirsiz `walk-06…10` yerine doğrulanmış kareler, durak
    metinleri gerçeğe göre:

| Durak | Metin | Kare |
|---|---|---|
| 05 | Bir kat yukarı. | S7 |
| 06 | Sessiz koridor. | S6 |
| 07 | Tırnak barı. | S11 (7,6 sn) |
| 08 | Bakım odası. | cilt-kubbe posteri |
| 09 | Ve başlıyoruz. | S3 ve CTA |

  - "Halka ışık altında" durağı, gerçek karesi bulunana kadar çıkar.
- **Belgeler:** `cert-wall`/`cert-trophy` yerine S4 posteri ve mini filmi
  ("Duvarımızda asılı" metni artık gerçek kareyle).
- **Açılış kartı:** yıl, doğrulanana kadar yazılmaz ("Açılış günümüz").
- **Bölüm kimliği:** `id="hizmetler"` → `hizmet-kartlari`.
- **Yeni bağlantı:** "Salonu baştan sona gezin →" ile `gm`'ye geçilir.

### 4.2 Güzellik merkezi (`gm`): amiral hikâye, 12 perde

Masaüstünde medya solda sticky, metin sağda akar. Mobilde medya tam ekran,
metin kartları perdenin üstünden geçer. Sağ kenarda ilerleme rayı ve
"IV / XII" sayacı bulunur.

| Perde | Başlık yönü | Medya | Metin dayanağı |
|---|---|---|---|
| I | Konutkent, 3028. Cadde | S2 film | NAP |
| II | Kırmızı halı | S1 film (8–10 sn bölümü) | — |
| III | Hoş geldiniz | S3 film | Yorumdaki karşılama ("Melek Hanım … karşılama", Gaye H.); isim yalnız onayla |
| IV | Siz beklerken | S5 film + S9 | "Mekânın güzelliği ve ferahlığı" (Itır Ç.); ikram yalnız onayla (S. Y. yorumu) |
| V | Bir kat yukarı | S7 → S6 | — |
| VI | Tırnak barı | S11 dört çekim | Tırnak vitrinine bağlantı |
| VII | Bakım odaları | cilt-kubbe döngüsü, lazer-koltuk, slimtone-cihaz | Her biri kendi vitrinine |
| VIII | Hijyen, adım adım | tirnak-hijyen-1→2→3→4, oda | Alt metinlerdeki gerçek adımlar; hijyen yorumları (Nihal Y., Büşra o., Elanur İ.) |
| IX | Duvarımızda asılı | S4 film | Belge adları yalnız okunabiliyorsa ve sahip onaylarsa |
| X | Ekibimiz | tipografik, portreler çekim P1 | Yalnız roller; isim ve portre onayla |
| XI | Açılış | S12 kurgusu → mevcut hikâye | Yıl kapısı |
| XII | Sıra sizde | S3 posteri + planlayıcı + ziyaret bloğu | `PLANS.salon` |

### 4.3 Konum ve yol tarifi (`konum`): "Kapımıza kadar"

1. **Harita:** mevcut ziyaret haritası ve tırnak semt sayfalarındaki altın
   yol çizgisi bileşeni ("Yol çizgisi temsilidir").
   - Semt mesafeleri mevcut veriden: Bağlıca ~1,5 km, Çayyolu ~2 km,
     Koru ~2 km, Yaşamkent ~3 km, Ümitköy ~4 km, Alacaatlı ~4 km.
   - Ziyaretçinin semti bilinirse (`data-personal`) önce o gösterilir.
2. **Bina:** S2 cephe filmi. İkinci kare olarak S12 4,4 sn karesi (yüzsüz
   cephe ve tabela).
3. **Kapı:** S1 filmi tam boy. **Bu filmin asıl yeri burası.**
4. **Resepsiyon ve CTA:** "Yol tarifi" (Google Haritalar), "Ara", "WhatsApp'tan
   konum isteyin".
- Otopark, bina girişi ve toplu taşıma bilgisi **sahipten gelene kadar
  yazılmaz**.
- `konum.html` TagCtx runtime listesinde; canlı yamada özellikle doğrulanır.

### 4.4 İletişim (`iletisim`): "Size en hızlı yol", 3 perde

| Perde | İçerik | Medya |
|---|---|---|
| I | WhatsApp: ön dolu mesaj ve ziyaret kodu | S3 |
| II | Telefon ve kopyala | S8 |
| III | Gelin: NAP, saatler, harita bağlantısı | S2 posteri |

- Yanıt süresi gibi doğrulanmamış vaat yok.
- Saatler `NAP`'tan: Salı–Pazar 10.00–20.00, Pazartesi kapalı.
- Açık/kapalı çipi mevcut.

### 4.5 Tüm hizmetler (`tum-hizmetler`): hizmet atlası

- Üstte sticky kategori şeridi: 8 aile.
- Her aile bir bölüm:
  - Ailenin canlıdaki kahramanı (yeni medya yok): kas-profil,
    tirnak-uzun-kirmizi, kirpik-makro-1, lifting-cift-sonra, dudak-1,
    cilt-led döngüsü, lazer-5, vucut-g5.
  - "…TL'den" yalnızca `PLANS`'tan; kişiye özel olanlarda "Kişiye özel".
  - `NAV`'daki bütün alt sayfalar çip olarak: vitrini olanlar prototipte,
    olmayanlar canlı sayfada açılır.
- Kahraman geçişleri mevcut `view-transition-name: media-*` ile.
- Arama, mevcut `fold()` ve `NAV_SYN` ile.

### 4.6 Fiyat listesi (`fiyat`): önce işlev

- Kahraman: S8 Ken Burns (kısa, 40vh).
- Sticky sekmeler, arama, aile bölümleri.
- Satırlar `PLANS`'tan:
  - ad, fiyat, süre, CRM'deki "Kampanya" rozeti;
  - `null` fiyat → "Fiyatı sorun" ya da "Kişiye özel".
- Her bölüm başında tek satırlık gerçek medya şeridi (aile posterleri).
- CTA: satıra dokun → planlayıcı o seçenekle açılır.
- Uydurma "son güncelleme" tarihi yok; CRM tarihi varsa o yazılır.
- `price-menu.html` TagCtx runtime listesinde.

### 4.7 Özel gün makyajı (`ozel-gun`): medya kapısı

Manifestte, canlı Artifact'te ve `PLANS`'ta özel gün makyajı **yok**.

- **D0 araması (sunucu):**
  `instagram_context.py --search` ile: "makyaj", "gelin", "nişan", "söz",
  "kına", "özel gün", "mezuniyet".
- **3 ve üstü gerçek iş bulunursa:** "Hazırlık sabahı" hikâyesi: karşılama
  → kaş/kirpik hazırlığı → makyaj → son dokunuş.
- **Bulunmazsa:** D3'e kalır. Hizmet aktifse çekim listesi P1'e girer.
- O zamana kadar sayfa prototipte açılmaz; menü canlı sayfaya gitmeye devam
  eder.
- Başka hizmetin sonucu "özel gün makyajı" diye gösterilmez.

### 4.8 KVKK (`kvkk`): tipografik

- Metin canlı `kvkk` sayfasından **birebir** alınır; yeniden yazılmaz.
- Sticky içindekiler, okunur satır boyu, efekt yok, medya yok (yalnız
  monogram).
- Metinde değişiklik ancak sahip ve hukuk onayıyla yapılır.

---

## 5. Çekim listesi (personel, telefonla, yarım gün)

**Teknik kurallar:**
- Kaydırma filmi için **tek kesintisiz çekim**, montaj yok. Bugünkü
  salon-cephe ve salon-tur montaj olduğu için perdeler 1 saniyelik
  parçalara bölünüyor.
- 1080p, 30 fps, 9:16. Gimbal ya da yavaş yürüyüş.
- Pozlama pencereye kilitli; salon-tur'daki %27 patlak ışık tekrarlanmaz.
- Işıklar açık; güzellik modu, filtre, müzik ve yazı kapalı.
- Kadrajdaki herkesten web kullanımı için açık rıza (KVKK).

| Öncelik | Sayfa / perde | Çekilecek |
|---|---|---|
| P1 | Konum | Caddeden bina girişine ve kapıya tek çekim, 15 sn; otopark ve giriş yolu |
| P1 | GM III, İletişim | Resepsiyon: içeriden kapı açılışı ve karşılama, 8 sn |
| P1 | GM V | Merdivenden yukarı tek çekim yürüyüş, 12 sn (walk'ın kayıp halkası) |
| P1 | GM VII | Her uygulama odası için yatay pan, 10 sn: cilt, kaş/kirpik, lazer, tırnak, vücut |
| P1 | GM X | Ekip portreleri, rızalı, kendi istasyonlarında |
| P2 | GM IV | İkram servisi, 6 sn (sahip onaylarsa) |
| P2 | Ana sayfa, Konum | Akşam cephesi, tabela ışıkları yanık |
| P2 | Özel gün | Hizmet aktifse: hazırlık sabahı, rızalı, önce ve sonra aynı ışıkta |
| P3 | Şölen B-roll | Sertifika duvarında yavaş kayma; altın detaylar makro |

**Teslim:** Instagram'a atılan her şey kütüphaneye kendiliğinden düşer.
Atılmayanlar `google-adsAI/patches/media_salon_20261007/drop/` klasörüne konur.

---

## 6. Dalgalar

| Dalga | İçerik | Yayın |
|---|---|---|
| **D0** | Depodaki anlık görüntüyü canlı `1791387535-eead` ile yenile. walk/cert/still hash kapısı. Özel gün araması. Sahip soruları (bkz. 9) | — |
| **D1** | Medya v2 (bölüm 2), sprite paketleme (salon-giris, cilt-led), `initSalonStory`. Ana sayfa revizyonu, **Güzellik merkezi**, **Konum**, **İletişim** | Aynı Artifact |
| **D2** | **Tüm hizmetler**, **Fiyat listesi**, **KVKK** | Aynı Artifact |
| **D3** | Özel gün makyajı (arama ya da çekim sonucu). Çekimlerle stand-in'lerin değişimi; yalnızca `manifest_salon.json` güncellenip yeniden derlenir | Aynı Artifact |
| Canlı | Lazer planındaki `build.py --check/--apply` deseniyle salon yaması. **Sahip onayı ve TagCtx kapısı olmadan uygulanmaz** | canlı site |

**Önerilen sıra:** D0 hemen. Ana sayfadaki kaynağı belirsiz kareler bir
"sabit kural" ihlali olabilir; bu, diğer planlardan bağımsız olarak önce
kapanmalı.

---

## 7. Dosya ve boyut bütçesi

- **Bugün:** 335 dosya. Tek yayında en fazla 255 dosya, sürümde en fazla 511.
- **Boşalan:** salon-giris (71 kare) ve cilt-led (59 kare) sprite'a
  paketlenir; 130 dosya → 2 dosya, **−128**.
- **Eklenen** (yaklaşık 34 dosya):
  - salon-cephe: 5 sprite ve 10 poster;
  - salon-tur: 4 sprite ve 4 poster;
  - S7–S9: 6 kırpım;
  - S8 Ken Burns: 2 dosya;
  - açılış kurgusu: 2 dosya;
  - `provenance.json`.
- **Sonuç:** yaklaşık 241 dosya. Her güncelleme yalnızca değişen dosyaları
  gönderir.
- **Boyut:** her sprite en fazla ~700 KB; sayfa başına ilk yük (LCP posteri)
  en fazla 200 KB. Filmler ekrana 800 px kala yüklenir.

---

## 8. Doğrulama

**Medya:**
- Her yayın dosyasının `provenance.json` karşılığı var. Kaynaksız dosya: 0.
- Ölçüm betiği hedefleri: R−B +6…+12; parlaklık 120–150; kırp% < 2.
  Netlik, kaynak çekimin medyanının altına düşmez.
- Büyütme yok: çıktı genişliği kaynak genişliğini aşmaz.
- Lobi kırpımlarında tanınır yüz yok (sahip izni yoksa).
- Kırık medya referansı: 0.
  - Bugün depodaki v3'te 9 eksik var.
  - Canlıda 170 sabit referansın hepsi yayında. JS'te üretilen yollar
    Playwright ağ kaydıyla kontrol edilir.

**Prototip** (Playwright, 390×844 ve 1440×900):
- 8 sayfanın her biri için kaydırmanın %0/25/50/75/100'ünde ekran görüntüsü.
  Perde geçişlerinde montaj kesmesi görünmez.
- Konsol hatası 0; yatay taşma 0; CLS için bütün `img`/`video` boyutları
  tanımlı.
- C kademesi ve `prefers-reduced-motion`: bütün metin ve CTA'lar eksiksiz.
- Menüdeki Salon kayıtları prototip görünümlerini açar; `#hizmetler`
  çakışması yok.
- Her WhatsApp ve telefon bağlantısında `data-track-label` var; `waHref` ziyaret
  kodunu taşır.
- Aynı Artifact URL'sine yayınlanır, okunarak geri doğrulanır, dosya sayısı
  kontrol edilir.

**Canlı yama** (yalnızca sahip onayından sonra):
- `./run tag_ctx.py audit --record`
- `./run tag_ctx.py diff`
- `./run tag_ctx.py verify --pages index.html guzellik-merkezi.html konum.html iletisim.html hizmetler.html price-menu.html kvkk.html`
- `patches/verify_tags.sh` aynı sayfalarla.
- Yeni kritik bulgu yok. Bugün bilinen 2 kritik (`dead_primary`,
  `meta-conversions`) bu işten bağımsız.

---

## 9. Sahibe sorulacaklar

D0'da sorulur. D1, cevap gelmeyen yerde yer tutucuyla ilerler.

1. Açılış töreninin gerçek tarihi (afişte "12 Mayıs"; video 2 Nisan 2024'te
   paylaşılmış).
2. `still-altin`, `still-kutu`, `still-firca`, `still-kirpik`, `still-urun`
   gerçek çekim mi, tasarım veya yapay üretim mi?
3. `walk-06…10`, `cert-wall`, `cert-trophy` nereden geldi?
4. Lobi fotoğraflarındaki danışanlar: tam kare kullanılabilir mi, yoksa kırpım mı?
5. Ekip: hangi isimler ve portreler sitede kullanılabilir?
6. Özel gün makyajı aktif bir hizmet mi; CRM kalemi ve fiyatı ne; örnek iş var mı?
7. Otopark, bina adı ve girişi, toplu taşıma bilgisi.
8. Salon-tur (2024) iç mekânı hâlâ aynı mı?
9. "İkram" ya da "kahveniz hazır" ifadesi kullanılabilir mi? Yorumda dayanağı
   var ama hizmet vaadine dönüşür.
