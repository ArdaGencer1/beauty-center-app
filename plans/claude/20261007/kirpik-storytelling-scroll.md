# ATELİER · FAZ K: Kirpik ailesi (5 sayfa), storytelling scroll (2026-10-07)

## Bağlam

**İstek (10-07):** "Kirpik sayfalarını tamamla; storytelling scroll tarzında, en
kaliteli fotoğrafları ve videoları seç, en iyi editleriyle oluşturma planı yap."

**Bugünkü durum (depoda ölçüldü, Artifact v3 = `website/index.html`):**

- Menüde Kirpik ailesi 5 sayfa: `ipek-kirpik` (görünüm `kirpik`),
  `kirpik-lifting` (görünüm `lifting`), `klasik-ipek-kirpik`,
  `mega-volume-ipek-kirpik`, `ipek-kirpik-fiyatlari`. **Son üçünün prototipte
  görünümü yok.**
- `kirpik` görünümü: Bakış Stüdyosu hero (3 fotoğraf çapraz geçiş), Göz haritası
  SVG, galeri, davetiye, yorumlar, menü, SSS. Sayfa bloklar hâlinde; kaydırmaya
  bağlı bir anlatı yok.
- `lifting` görünümü: önce/sonra kaydırıcısı, kıvrım SVG'si, Lifting mi ipek
  kirpik mi kartları.
- **Kirpik videosu yok.** Manifestteki 12 kirpik kaydının hepsi görsel.
- Hero ve galerideki `ipek-kirpik-*` fotoğraflarında Instagram şablonundan kalan
  **"İPEK KİRPİK" etiket hapı ve "Selda Gençer" imza yazısı görünüyor.** Bu
  kayıtların manifestte `crop` alanı yok.
- Fiyatlar (CRM aktif menü, 7 Ekim 2026, v3'e yazılı): Klasik volüm 1.200 TL,
  Kahverengi klasik 1.400, Orta volüm 1.450, Kahverengi orta 1.650, Mega volüm
  1.700, Kahverengi mega 1.900 (yeni danışan); standart Klasik 1.700, Volüm
  1.950, Mega volüm 2.200 (150 dk); Bakım 1.200 (90 dk); Lifting 1.500 (60 dk);
  Kaş laminasyonu 2.500. **Derleme anında `/api/public/price-menu`'den yeniden
  okunur; plan rakamı kaynak değildir.**

**Hedef:** Her kirpik sayfası, kaydırdıkça ilerleyen tek bir hikâye: "kendi
kirpiğiniz → harita → tel tel → bakışınız → sizin saatiniz". Her bölüm gerçek
salon fotoğrafı veya videosuyla anlatılır, sonunda WhatsApp davetiyesine bağlanır.

## 1. Medya seçimi

### 1a. Görseller: ölçüm + görsel doğrulama (10-07)

Protokol: 13 kirpik görselinin tümü metadatadan ölçüldü (keskinlik = merkez
%60'ta kenar varyansı, 800w). Yalnızca en iyi 6 aday gözle açıldı.

| Slug | IG id | Kaynak | Keskinlik | Göz kontrolü | Karar |
|---|---|---|---:|---|---|
| `kirpik-makro-3` | 17918048469017834 | 1440² | 3034 | Uygulama anı: göz bantlı, mega volüm yelpazeleri, havlu zemin. Sağ üstte imza yazısı, bantta monogram. | **A · "Tel tel" bölümü + mega volüm hero** |
| `ipek-kirpik-cift` | 18054018488742876 | 1350×843 ×2 | 2993 / 1842 | Sonra kesin ve parlak. "İPEK KİRPİK" hapı irisin ve alt kirpiklerin üstünden geçiyor; kırpmayla çıkmaz. | **A · Dönüşüm bölümü**, hap için bkz. §2 |
| `ipek-kirpik-5` | 17917970235180938 | 1350×1687 | 2389 | Doğal, seyrek wispy klasik; kaş ile birlikte. Altta hap + imza. **Alt metni yanlış ("Hacimli").** | **A · Klasik sayfa hero**, alt: "Doğal klasik ipek kirpik" |
| `ipek-kirpik-3` | 17883162954668298 | 1350×1687 | 1213 | Kaş + yoğun wispy dış köşe, en "bakış" duygusu veren kare. Altta hap + imza. | **A · Ana sayfa hero** |
| `kirpik-makro-1` | 17986019318762562 | 1080² | 1735 | Kahverengi göz, yan açı makro, yelpaze dokusu çok güzel. Monogram iriste, imza altta. 1200w yok. | **B · Doku/yelpaze bölümü (≤800w)** |
| `lifting-cift` | 18383965606199591 | 1080×540 ×2 | 978 / 782 | Kıvrım net okunuyor, ama yumuşak ve düşük çözünürlüklü. 1200w yok. | **B · Lifting dönüşüm (≤800w, tam ekran değil)** |
| `ipek-kirpik-4` | 18027151178746074 | 1350×1687 | 1123 | v3 hero'su (Doğal). Açılmadı; aynı şablon, hap varsayılır. | A · Bakış Stüdyosu "Doğal" |
| `ipek-kirpik-1` | 18107383999958512 | 1350×1687 | 911 | v3 hero'su (Dolgun). Açılmadı. | A · Bakış Stüdyosu "Dolgun" |
| `kirpik-makro-4` | 18027584354550038 | 1350×1688 | 1573 | Açılmadı; düşük kontrast (36,7). | B · Kahverengi seçenek kartı |
| `ipek-kirpik-2` | 18126043255725501 | 1350×1687 | 773 | Açılmadı. | C · Klasik sayfa galerisi |
| `ipek-kirpik-6` | 18103810502001285 | 1350×1687 | 796 | Açılmadı; yan açı. | C · Galeri |
| `kirpik-makro-2` | 17885561247405556 | 1080² | **682** | Açılmadı; ailenin en yumuşağı. | **D · Kullanma** (yalnızca galeri küçük boyut, gerekirse) |
| `still-kirpik` | 18593472577053386 | 1254² | 1613 | Tepsiler ve cımbızlar (still ailesi). | A · "Atölye" bölümü |

A = sahne/hero · B = destek bölümü · C = galeri · D = dışarıda.

**Ek aday (sunucuda kontrol edilecek):** `17986864907913512` (PMU'dan "brow
lamination and lash lift" diye elenmişti). Kirpik lifting sayfası için doğru
yerde olabilir. Çözünürlük yeterliyse lifting hero'su olarak
`lifting-cift`'in yerini alır.

### 1b. Videolar: sunucuda aranacak (görsel açmadan önce)

Depodaki 100 ham videonun 84'ü indekste yok. Dosyalarda başlık/açıklama
metaverisi yok, bu yüzden kirpik videosunu yalnızca sunucuda
`instagram.db` ile eşleştirebiliriz. Toplu açma yok.

1. Sunucuda arama:
   `instagram_context.py --search "kirpik"`, `"ipek kirpik"`, `"lifting"`,
   `"volüm"`, `"lash"`. Yalnızca `media_type=VIDEO/REELS` ID'leri alınır.
2. Çıkan ID'ler aşağıdaki havuzla kesiştirilir. **360p dosyalar (360×640,
   360×450) otomatik elenir.** Kalan aday havuzu: 720×1280 olanlar, özellikle
   kirpik fotoğraflarının paylaşıldığı **2026-06-02 … 2026-07-19** aralığı
   (yaklaşık 25 video). Örnek: `18088219433120497`, `18125591554728667`,
   `18011957690713082`, `18100751945014092`, `18180626833402501` (06-13),
   `18106595869806319`, `18093406391262864` (06-19), `18126120175637645`,
   `18187340608376469` (06-23), `18380338273207488`, `18002751545949371` (06-24),
   `18085487912411515` (07-07).
3. Kesişimden **en fazla 3 video**, tek tek ön izleme + 8 karelik şeritle
   doğrulanır. Hedef roller:
   - **V1 "Açılış"** (hero döngüsü): göz açılır, sonuç görünür. 4–6 sn.
   - **V2 "Tel tel"** (süreç): cımbızla izolasyon, yelpaze yerleştirme. 6–8 sn.
   - **V3 "Kıvrım"** (lifting): lifting pedi, kıvrım. 5–7 sn.
4. Elenme kuralları: videoya basılı yazı veya fiyat, başka uzmanın filigranı,
   720p altı, titrek el veya odak kaçması, müşteri yüzü (yuz:true ise sahip
   kararı 10-06 geçerli; yine de göz yakın planı tercih edilir).
5. **Uygun video çıkmazsa sahte video üretilmez.** Durağan fotoğraflara
   sadece CSS ile yavaş zoom/pan verilir (bkz. §3) ve sahibe 3 kısa çekimlik
   bir çekim listesi verilir (§1c).

### 1c. Çekim listesi (video çıkmazsa ya da yetersizse)

Telefon, 4K/30, dikey, ring light yerine pencere ışığı + beyaz reflektör.
Her çekim 10–15 sn, sabit tripod, makro mod.

1. **Göz açılışı:** uygulama bitti, bant alınır, göz yavaşça açılır (yan 3/4 açı).
2. **Tel tel:** cımbız + ipek kirpik yakın plan, tek yelpaze yerleşimi (yüz yok).
3. **Lifting kıvrımı:** silikon ped üzerinde kirpikler, sonra göz açılışı.
4. **Tepsi:** ipek kirpik tepsileri ve cımbızlar üzerinde yavaş kaydırma (atölye).

## 2. Edit reçetesi (`build_media.py` manifest alanlarıyla)

**İlke:** Sonuç alanı (kirpik, iris, kapak) piksel düzeyinde değiştirilmez.
Yumuşatma, AI ile büyütme veya rötuş yok. Edit = kadraj + logo temizliği (yalnızca
düz zeminde) + tutarlı renk.

| Slug | `crop` (kaynak px, ölçülerek kesinleşir) | `delogo` | Not |
|---|---|---|---|
| `ipek-kirpik-3` | `[0,0,1350,1350]` → 1:1, kaş + göz | — | Hap ve imza alt %20'de, kırpmayla gider. Ayrıca 4:5 mobil varyant: `[135,0,1215,1350]`. |
| `ipek-kirpik-5` | `[0,0,1350,1350]` | — | Aynı şablon. |
| `ipek-kirpik-4`, `-1`, `-2`, `-6` | `[0,0,1350,1350]` (açıp hap yerini doğrula) | — | Bakış Stüdyosu kareleri aynı kadrajda olmalı; göz merkezi hizalanır. |
| `kirpik-makro-3` | — | sağ üst imza (≈`[810,150,490,140]`), bant monogramı (≈`[680,830,160,230]`) | İkisi de düz havlu/bant zemininde. |
| `kirpik-makro-1` | `[0,0,1080,930]` | — | İmza alt şeritte. İristeki monogram **kalır** (iris sonuç alanı). |
| `ipek-kirpik-cift` | mevcut `split:h` + `pair_crop` | — | "Sonra" yarısındaki hap iris üstünde; silinmez. Arayüzde aynı konuma buzlu "Sonra · ipek kirpik" etiketi oturur. **Önce sunucuda karusel çocukları kontrol edilir:** haplı olmayan bir kare varsa o kullanılır. |
| `lifting-cift` | mevcut `split:h` | — | En fazla 800w. Tam ekran yerine ortalanmış 4:2 bant. |
| `still-kirpik` | — | — | Olduğu gibi. |

**Renk (`grade`):** Kirpik ailesi için tek ton: beyaz dengesi hafif sıcak
(+150 K), siyahlar 6/255'e kaldırılır (kirpik detayının boğulmaması için),
doygunluk −5. `ipek-kirpik-*` setinin pozlama ortalaması 129–159 arasında;
hedef 140±6. `vignette` yalnızca hero'larda, %12.

**Boyutlar:** 480 / 800 / 1200 webp + avif (1200 yalnızca kaynak yetiyorsa;
`makro-1`, `makro-2`, `lifting-cift` en fazla 800). Prototipte tek boyut (900w,
ya da kaynak daha küçükse 800w).

**Videolar:** `trim` 4–8 sn; `crop` 9:16 (mobil) + 4:5 masaüstü varyantı;
sessiz, H.264 720p, faststart, ≤1,5 MB; poster = en keskin kare (Laplace
varyansı en yüksek kare otomatik seçilir). Yavaşlatma ve yapay hareket yok.

**Alt metin düzeltmeleri:** `ipek-kirpik-5` → "Doğal klasik ipek kirpik";
`kirpik-makro-4` gözle doğrulandıktan sonra "kahverengi" ifadesi korunur ya da
düzeltilir.

## 3. Storytelling scroll motoru (ailenin ortak bileşeni)

**Yapı:** `<section class="story">` içinde yapışkan bir medya sahnesi
(`position: sticky`) ve sahnenin üstünden akan metin "adımları". Her adım
görünür olduğunda sahne değişir: çapraz geçiş, yakınlaşma, perde açılışı,
SVG çizimi.

| Parça | Davranış | Teknik |
|---|---|---|
| K-Sahne | Yapışkan medya (fotoğraf/video/SVG katmanları) | `position: sticky; height: 100svh`; katmanlar `opacity`/`transform` |
| K-Adım | Metin kartı; sahnedeki geçişi tetikler | `IntersectionObserver` (eşik 0,55) → `data-step` |
| K-İlerleme | Sahnede ilerlemeye bağlı zoom/pan, perde | `animation-timeline: view()`; desteklenmeyen tarayıcıda JS `scroll` + rAF yedeği |
| K-Perde | Önce → sonra kaydırmaya bağlı açılış | `clip-path: inset()` kaydırma oranına bağlı; basılı tutma ve kaydırıcı yedeği korunur |
| K-Çizim | Göz haritası / yelpaze / kıvrım SVG'si kaydırdıkça çizilir | `stroke-dashoffset` ilerlemeye bağlı; mevcut `drawEye` ve kıvrım kodu yeniden kullanılır |
| K-Film | Video yalnızca görünürken oynar | mevcut `initAutoVids`; C kademesinde poster |

**Mobil:** Sahne tam ekran, metin kartları altta buzlu cam; başparmak bölgesinde
sabit [Bakışımı seç] + WhatsApp. **Masaüstü:** sahne sağda %55, adımlar solda.

**Erişilebilirlik ve performans:**
- `prefers-reduced-motion` ve C kademesi: animasyon yok, bölümler sıradan
  dikey sırayla görünür; her adımın son karesi gösterilir.
- LCP = hero AVIF (fetchpriority=high); diğer tüm sahne medyası `loading=lazy`,
  videolar `load` olayından sonra.
- Metin DOM'da sıralı durur; ekran okuyucu ve SEO için hikâye düz okunur.
- Yatay taşma 0; `100svh` kullanılır (iOS adres çubuğu).

## 4. Sayfa sayfa hikâyeler

H1, başlık, meta ve canonical canlı sayfalardan korunur.

### 4.1 `/ipek-kirpik` (merkez, görünüm `kirpik`)

| # | Bölüm | Sahne medyası | Metin (özet) |
|---|---|---|---|
| 0 | **Açılış** | V1 döngüsü; yoksa `ipek-kirpik-3` (1:1) yavaş zoom 1,00→1,06 | H1 "Ankara İpek Kirpik" · "Bakışınız, tek seansta." · ★ 4,6 · 263 · 1.200 TL'den · Bugün müsait |
| 1 | **Kendi kirpiğiniz** | `ipek-kirpik-cift` *önce* yarısı | "Her şey kendi kirpiğinizle başlar: uzunluğu, gücü, yönü." |
| 2 | **Harita** | Göz haritası SVG kaydırdıkça iç köşeden dış köşeye çizilir | Mevcut "Her kirpik yerini bilir" metni; "uzunluklar örnektir" notu |
| 3 | **Tel tel** | V2 ya da `kirpik-makro-3` (bantlı uygulama), yakınlaşma 1,0→1,25 | "Gözleriniz kapalı, rahat bir koltukta uzanırsınız." (v3'teki metin) |
| 4 | **Yelpaze** | `kirpik-makro-1` (yan açı doku) | Klasik / volüm / mega volüm farkı; alt sayfalara iki karo |
| 5 | **Dönüşüm** | K-Perde: `ipek-kirpik-cift` önce → sonra | "Salonumuzda yapılan gerçek ipek kirpik; Instagram hesabımızdan." |
| 6 | **Bakışınızı seçin** | Bakış Stüdyosu (Doğal `-4` / Dolgun `-1` / Yoğun `-3`, aynı 1:1 kadraj) | Bakış → menüdeki en yakın hizmet ve fiyat (CRM'den) → [Bu bakışla saatimi seç] |
| 7 | **Atölye** | `still-kirpik` | "Tepsiler, cımbızlar ve tek kullanımlık bantlar." (yalnızca fotoğrafta görüneni söyler) |
| — | Davetiye · Yorumlar · Menü · Nasıl geçer · SSS · Ziyaret | mevcut bileşenler | değişmez |

### 4.2 `/klasik-ipek-kirpik` (yeni görünüm `kirpik-klasik`)

Kimlik: "doğal, hafif, maskarasız". Açık tonlu sahne.

| # | Bölüm | Medya | Metin |
|---|---|---|---|
| 0 | Açılış | `ipek-kirpik-5` (1:1) | H1 canlı sayfadan; "Klasik volüm 1.200 TL'den · 120 dk" |
| 1 | Klasik ne demek? | K-Çizim: tek doğal kirpiğe tek ipek kirpik eşleşmesi SVG'si (temsili) | "Her doğal kirpiğinize bir ipek kirpik." |
| 2 | Doğal bakış | `ipek-kirpik-4` → `ipek-kirpik-2` çapraz geçiş | "Yoğunluğu siz seçersiniz." |
| 3 | Siyah mı kahverengi mi? | `kirpik-makro-4` + iki ton çipi | Kahverengi klasik 1.400 TL (CRM) |
| 4 | Klasik mi volüm mü? | iki kart → mega volüm sayfasına bağlantı | — |
| — | Davetiye (varsayılan `klasik`) · klasik yorumları · kısa menü · SSS | | |

### 4.3 `/mega-volume-ipek-kirpik` (yeni görünüm `kirpik-mega`)

Kimlik: "yoğun, dramatik". Koyu "Gece" sahnesi, altın vurgular.

| # | Bölüm | Medya | Metin |
|---|---|---|---|
| 0 | Açılış | V2 ya da `kirpik-makro-3`; koyu zemin | H1 canlı sayfadan; "Mega volüm 1.700 TL'den" |
| 1 | Yelpaze | K-Çizim: bir doğal kirpiğe birden fazla ince ipek kirpikten açılan yelpaze SVG'si (temsili, sayı verilmez) | "İnce ipek kirpiklerden yelpazeler." |
| 2 | Yoğunluk | `kirpik-makro-1` yakınlaşma | — |
| 3 | Sonuç | `ipek-kirpik-3` → `ipek-kirpik-1` | — |
| 4 | Orta mı mega mı? | Orta volüm 1.450 · Mega 1.700 · kahverengi seçenekleri (CRM) | — |
| — | Davetiye (varsayılan `mega`) · yorumlar · SSS | | |

### 4.4 `/ipek-kirpik-fiyatlari` (yeni görünüm `kirpik-fiyat`)

Fiyat önce gelir; hikâye kısadır ve fiyat kararına hizmet eder.

| # | Bölüm | Medya | Metin |
|---|---|---|---|
| 0 | Açılış | `ipek-kirpik-cift` sonra (hap üstünde buzlu etiket) | H1 canlı sayfadan |
| 1 | **Tam menü** (ilk ekran) | Lüks menü: Yeni danışan / Standart sekmeleri, Siyah / Kahverengi | Tüm satırlar CRM'den, "Randevu sistemindeki aktif menüden · tarih" |
| 2 | Fiyatı ne belirler? | 3 bakış küçük resmi (Doğal / Dolgun / Yoğun) → ilgili satır vurgulanır | Yoğunluk, renk, süre. Yeni madde uydurulmaz. |
| 3 | Bakım | `still-kirpik` | Bakım 1.200 TL · 90 dk; "zamanını uzmanınız söyler" |
| — | Davetiye · SSS | | |

### 4.5 `/kirpik-lifting` (görünüm `lifting`, yeniden yazılır)

| # | Bölüm | Medya | Metin |
|---|---|---|---|
| 0 | Açılış | V3 ya da `17986864907913512` (uygunsa) ya da `lifting-cift` sonra (800w, ortalanmış bant) | H1 "Ankara Kirpik Lifting" · 1.500 TL · 60 dk |
| 1 | Düz kirpik | `lifting-cift` önce | "Kendi kirpiğiniz, olduğu gibi." |
| 2 | Kaldırırız | K-Çizim: mevcut kıvrım SVG'si kaydırdıkça kökten kalkar | v3'teki 3 adım metni |
| 3 | Kıvrım | K-Perde: önce → sonra | "Maskarasız belirgin bir bakış." |
| 4 | Lifting mi ipek kirpik mi? | mevcut versus kartları | — |
| — | Davetiye · yorumlar · menü (lifting + kaş laminasyonu) · SSS | | |

## 5. Dil kuralları

- Yalnızca fotoğrafta/videoda görünen ve CRM'de yazan bilgi. Kirpik sayısı,
  kalıcılık süresi (hafta), "zarar vermez", "alerji yapmaz" gibi doğrulanmamış
  iddia yok.
- Sonuç garantisi yok; "sonuç kişiye göre değişir" notu dönüşüm bölümlerinde.
- SVG anlatımlarında "temsili anlatım" notu.
- Uzman adı yazılmaz (lazer kararıyla tutarlı).

## 6. Prototip (aynı bağlantı: https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM)

- Lazer planındaki `a3_build.py` hattı kullanılır; kirpik için ayrı
  `src/kirpik.css` + `src/kirpik.js` (story motoru + 3 yeni görünüm). Prototip ve
  canlı yama aynı kaynağı satır içine alır.
- `VIEWS` dizisine `kirpik-klasik`, `kirpik-mega`, `kirpik-fiyat` eklenir; `NAV`
  satırlarına üçüncü eleman (görünüm adı) yazılır, menüden prototip içinde açılır.
- Prototip panelinin "Sayfa" bölümüne "Kirpik ▸" alt seçimi.
- **Dosya bütçesi (≤255):** v3'te 241 dosya; lazer ≈ +23, sprite paketlemesiyle
  ≈ −128. Kirpik ≈ +16 (10 görsel tek boyut + en fazla 3 video + 3 poster).
  Lazer v4 sprite paketlemesi yapılmadan kirpik eklenirse sınır aşılır, bu
  yüzden **sıra: Lazer v4 yayını → Kirpik (v5).**
- Yayın sonrası Artifact tekrar okunur ve sürüm doğrulanır.

## 7. Canlı yama (sahip onayından sonra)

`patches/atelier_kirpik_YYYYMMDD/` → `build.py --check` (dry-run) → ekran
görüntüleri → sahip onayı → `--apply`. Canlı sayfaların H1/başlık/meta/
canonical'ı ve mevcut SSS/SEO metinleri "Detaylı bilgi" altında DOM'da korunur.

## 8. Doğrulama (bitti demeden önce)

- Medya: kırık referans 0; her sahnenin 480/800 (ve varsa 1200) dosyası mevcut;
  hiçbir karede "İPEK KİRPİK" hapı ya da kırpılmış yarım imza kalmadı (6 hero
  karesi gözle kontrol).
- Tarayıcı: konsol hatası 0; mobil (390×844) ve masaüstü (1440×900) ekran
  görüntüleri her bölüm için; yatay taşma 0; `prefers-reduced-motion` ve C
  kademesi görüntüsü.
- Performans: LCP öğesi hero AVIF; hero dışı video `load` öncesi indirilmiyor.
- CTA: her sayfada davetiye → WhatsApp mesajı doğru hizmet/varsayılanla, `[W-]`
  kodu ile; telefon bağlantısı.
- TagCtx: `audit --record`, `diff` (yeni kritik yok), `verify --pages` (5 kirpik
  sayfası), `patches/verify_tags.sh`.
- Artifact aynı URL'ye yayınlandı, geri okundu, dosya sayısı ≤255.

## 9. Sıra

| Adım | İş | Kim |
|---|---|---|
| K0 | Sunucuda video araması (§1b) + `17986864907913512` ve karusel kontrolü | Ajan (sunucu erişimi) |
| K1 | En fazla 3 video ve ek görselin gözle doğrulanması; kararların bu plana yazılması | Ajan |
| K2 | Manifest güncellemesi (crop/delogo/grade/alt) + `build_media.py` | Ajan |
| K3 | `kirpik.css/js` story motoru + `ipek-kirpik` merkez sayfa | Ajan |
| K4 | Klasik, mega, fiyat görünümleri + lifting yeniden yazımı | Ajan |
| K5 | Artifact v5 yayını (Lazer v4 sonrasında) + doğrulama (§8) | Ajan |
| K6 | Canlı yama `--check` → sahip onayı → `--apply` | Sahip |
| (K1b) | Video çıkmazsa §1c çekim listesi | Sahip / salon |
