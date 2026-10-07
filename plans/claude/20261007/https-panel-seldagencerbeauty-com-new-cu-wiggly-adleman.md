# ATELİER · FAZ L: Lazer epilasyon ailesi (7 sayfa), prototip + canlı yama (2026-10-07)

## Bağlam

**Sahibin isteği (10-07):** "Lazer epilasyon sayfalarına odaklan. Şu an hayran olunacak kadar iyi değil, çok çok iyi olmalı. Bütün sayfalarını tamamlayalım; fotoğrafları ve videoları Instagram'dan seç."

**Bugünkü durum (ölçüldü):**
- Canlıda 7 lazer sayfası var:
  - /laser-signature (merkez sayfa)
  - /lazer-epilasyon-fiyatlari-ankara
  - /erkek-lazer-epilasyon
  - /yuz-lazer
  - /hassas-cilt-lazer
  - /bolgesel-lazer
  - /laser-signature-kampanya
  - (/epilasyon yalnızca yönlendirme sayfası; dokunulmaz.)
- Sayfalarda 1–5 görsel var: logo, salon fotoğrafı ve "temsili" önce/sonra. Video yok, etkileşim yok.
- Sayfa Sağlığı, 09-09..10-06:

  | Sayfa | Skor | Reklam harcaması |
  |---|---|---|
  | /laser-signature | 49,8 | 5.952 TL |
  | /lazer-epilasyon-fiyatlari-ankara | 54,0 | 4.676 TL |
  | /erkek-lazer-epilasyon | 51,1 | 2.246 TL |

  - Bu 3 sayfadaki reklam maliyetinin %98–100'ü "ortalamanın altında" açılış sayfası etiketli kelimelerde.
  - Hız sorun skoru 23–25.
  - Lazer reklamları 10-01'den beri kapalı; trafiğin çoğu organik.
- Prototip v3'teki lazer vitrini zayıf:
  - durağan bir fotoğraf, bölge çipleri, 4 karelik galeri;
  - "Gıdı" bölgesi eksik;
  - davetiyede örnek (sahte) saatler var.
- **Faz 0 canlıda:** 10-06 20:21'de uygulanmış (`styles.css?v=20261007-faz0`).
- **Fiyat menüsü canlıda:** site `/api/public/price-menu` artık CRM'e proxy ediyor; 292 seçenek doğrulandı.
- `media_ig` canlı yaması henüz uygulanmadı. CRM `site-slots` uç noktası yok.

**Sahip kararları (10-07):**
1. Prototip ve canlı yama birlikte hazırlanacak. Canlıya alma komutunu sahip çalıştırır.
2. Cihaz bilgisi yazılacak: **Lasermach diode, 3 dalga boyu (755 / 808 / 1064 nm), soğutmalı başlık.**
3. Seans aralığı: **yüz 4–6 hafta, vücut 6–8 hafta.** Takvim tarih tahmini gösterecek.
4. "Bitiş garantili paket seçeneği" sayfalarda yer alacak.
   - Uzman adı yazılmayacak.
   - Yorumlardaki yüzdeler ("%70 döküldü" gibi) gösterilmeyecek.
5. Sahibin notu: "Reklamda risk atmadan maksimum öv; çok iyiyiz, kılları döküyoruz." Bu, kanıtlı ve kurallara uygun en güçlü dil demek (aşağıda §6).

**Hedef:**
- 7 lazer sayfası, Ankara'da kimsenin göstermediği kadar etkileyici bir "ışık" deneyimi sunacak.
- Bu deneyim WhatsApp'ta hazır bir bölge, plan ve gün mesajına dönüşecek.
- Önce prototipte (aynı Artifact bağlantısı) görünür; ardından tek komutla canlıya alınır.

## 1. Medya seçimi (Instagram dışa aktarımı, `instagram.db` salt okunur)

Videoların hepsi 720×1280, 9:16. Önizlemeler ve 8'er karelik şeritlerle tek tek incelendi.

| Slug | IG id | Tarih | Ne | Kullanım |
|---|---|---|---|---|
| `lazer-film-jel` (V) | 17891700807595292 | 07-23-2026 | cihaz → jel → yakın pembe ışık → kayış (9,7 sn) | Merkez sayfa hero döngüsü |
| `lazer-film-cene` (V) | 18096951407528888 | 08-29-2026 | çene/gıdı, 3 pembe atış (15,4 sn) | /yuz-lazer hero |
| `lazer-film-bacak` (V) | 18326727661258778 | 07-10-2026 | cihaz → jel → LASERMACH ışığı (10,6 sn) | "Seans nasıl geçer" hikâyesi, /bolgesel-lazer |
| `lazer-film-bacak2` (V) | 17874576207529500 | 07-10-2026 | bacakta ışık (10,6 sn) | film şeridi |
| `lazer-film-kol` (V) | 18101999296585006 | 08-05-2025 | kol uygulaması (12,8 sn) | /erkek-lazer-epilasyon hero |
| `lazer-film-yuz` (V) | 18361016620152430 | 08-05-2025 | koruyucu gözlük + yüz, ışık (6,3 sn) | /hassas-cilt-lazer hero |
| `lazer-koltuk` | 18058141007303868 | 1440×1918 | koltuk altı, LASERMACH ışığı, altın işlemeli havlu | /bolgesel-lazer hero, poster |
| `lazer-yuz-gozluk` | 18122820550555476 | 1164² | gözlüklü yüz, ışık hattı | yüz, hassas, güvenlik |
| `lazer-ekran` | 17977799688010994 | 1448×1931 | cihaz ekranı: Fluence 10 J/cm², 120 ms, Nd:YAG, cilt tonu, 10 °C | Cihaz Paneli, fiyat hero |
| `lazer-uzman` | 17914759008174743 | 1080×1350 | eldivenli uzman, bacak, pembe ışık | hijyen, galeri |
| `lazer-kilif` | 18356001847208677 | 824×1019 | koruyucu kılıflı başlık, koltuk altı | hijyen |
| `lazer-1..5` (mevcut) | 18187662313346224 · 18075151286260581 · 18095832997759812 · 17897285763316977 · 17894600409162953 | — | kol, bacak, cihaz+kol, el, kol | galeri, hikâyeler |

**Elenenler:**
- 18111607790319635 ve 18099937073231260: videoya basılı yazı var.
- Afişler: 18547825357072519 ("22.500 TL"), 18099424985241269, 18148172455519579, 18109202980794778.
- 17956194674966110: 610 px, çözünürlük düşük.
- Mevcut `lazer-epilasyon-*-temsili.webp`: gerçek sonuç değil.

**Gerçek lazer önce/sonra fotoğrafı yok.** Bu yüzden sahte önce/sonra kullanılmayacak. "Vay" etkisi ışıktan, gerçek videolardan ve etkileşimden gelecek.

**Medya üretimi:**
- `patches/media_ig_20261007/manifest.json` dosyasına `fam:"lazer"` öğeleri eklenir. Videolar `trim` ile kırpılır, `crop` ile kadrajlanır.
- `build_media.py` şunları üretir:
  - görseller: 480 / 800 / 1200 webp + avif;
  - videolar: mp4 720p, sessiz, faststart, en fazla 1,5 MB, posterli.

## 2. İmza deneyimler (lazer ailesi için yeni)

Tema "Gece ve Pembe Işık": siyah kadife, gül altını ve cihazın gerçek magenta ışığı. Bu, ATELİER'in Gece yönünün lazer ailesine özel hâli.

| # | Deneyim | Ne görür, ne yapar | Teknik |
|---|---|---|---|
| L1 | **Işık Taraması hero** | Gerçek video sessiz döner. Açılışta pembe-altın bir lazer çizgisi yukarıdan aşağı bir kez süpürür ve H1 harfleri ışık geçtikçe yanar.<br>Çipler: ★ 4,6 · 263 · "Kişiye özel fiyat" · "● Bugün 20.00'ye kadar açık" (gerçek saatler, Pazartesi kapalı).<br>Başparmak bölgesinde [Bölgelerimi seç] ve WhatsApp.<br>Hikâye halkaları: Uygulama · Yüz · Cihaz · Hijyen · Yorumlar · Fiyat. | LCP = AVIF poster. Video `load` olayından sonra gelir (C kademesinde poster). Tarama CSS ile yapılır. |
| L2 | **Vücut Haritası** (merkezî imza) | Zarif altın çizgili silüet: Kadın/Erkek, Ön/Arka.<br>Bir bölgeye dokununca orada pembe bir "atış" halkası patlar, hafif titreşim olur ve bölge listeye eklenir.<br>Başa dokununca yüz yakın planı açılır: dudak üstü, çene, gıdı, boyun; erkekte sakal üstü, kulak, ense.<br>"Yarım / Tüm" inceltmesi var.<br>Hazır seçimler: Tüm vücut 4 bölge · Tepeden tırnağa (erkek: Kemer üstü · Full vücut).<br>Her bölgenin **CRM süresi** ve seçilenlerin toplamı görünür ("Menüdeki süreler toplamı ≈ 75 dk"). | SVG bölge yolları. Süreler `/api/public/price-menu` uç noktasından canlı gelir, derleme anındaki kopya yedek olarak kalır. Erişilebilir liste yedeği var. Bölge listesi CRM'in birebir aynısı ("Gıdı" ve "Popo" dahil). |
| L3 | **Işığın Yolculuğu** (kaydırmalı) | Sabit sahnede bir cilt kesiti: epidermis, dermis ve farklı evrelerde 9 kıl kökü.<br>Kaydırdıkça sırayla:<br>1. Pembe ışık iner.<br>2. Büyüme evresindeki kökler ısınıp söner.<br>3. Dinlenen kökler o seansta etkilenmez.<br>4. Bu yüzden 8 seans aralıklı planlanır.<br>755 / 808 / 1064 nm çipleri, üç ışının ulaştığı derinliği gösterir.<br>"Temsili anlatım" notu. | SVG + kaydırmaya bağlı ilerleme (`animation-timeline`, JS yedeği). C kademesinde durağan son kare ve 4 numaralı açıklama. |
| L4 | **8 Seans Takvimi** | Seçilen bölgelere göre aralık hesaplanır:<br>- yalnız yüz bölgesi seçildiyse 4–6 hafta;<br>- vücut bölgesi varsa 6–8 hafta.<br>Başlangıç seçilir: Bu ay · Gelecek ay · 2 ay sonra. 8 nokta ve ay aralıkları çizilir ("8. seans ≈ Ağu–Eki 2027").<br>Not: "Tahminidir; uzmanınız cilt ve kıl yapınıza göre ayarlar." | Saf JS. Tarih biçimi `Intl` tr-TR. |
| L5 | **Cihaz Paneli** | Cihaz ekranı fotoğrafında 6 nabız atan nokta: Enerji (J/cm²) · Atım süresi (ms) · Cilt tonu · Soğutma 10 °C · Frekans (Hz) · Nd:YAG.<br>Her biri 1–2 cümlelik bir cam kart açar.<br>Altta: "Lasermach diode · 755 / 808 / 1064 nm · soğutmalı başlık". | Noktaların koordinatları fotoğraf üzerinde ölçülür. |
| L6 | **Salonda çekildi** | 4–5 gerçek video yatay şeritte, görünür oldukça oynar (A/B kademesi). Dokununca tam ekran hikâye açılır. | Prototipteki hikâye oynatıcısı (`initAutoVids`, `openStory`). |
| L7 | **Yorum duvarı** | Başlık: "Google'da lazer geçen 31 yorumun 30'u 5 yıldız" (GBP API, 10-07; her derlemede yeniden sayılır).<br>8–10 kelimesi kelimesine yorum: yüzdesiz, "Ad S." ve ay ile.<br>İki satırlık yavaş kayan duvar.<br>Not: "Google yorumlarından aynen; sonuç kişiye göre değişir." | `gbp_cli.py reviews --raw` → `reviews_pick`. `rating_claim` koruması uygulanır. |
| L8 | **Hijyen ve güvenlik** | 4 gerçek fotoğraf kartı: kılıflı başlık · eldiven · koruyucu gözlük · soğutma jeli. Hepsi fotoğrafta görünen şeyler. | — |
| L9 | **Fiyat Menüsü** (fiyat sayfasında tam, diğerlerinde kısa) | Lüks menü düzeni. Sekmeler: Kadın/Erkek × Tek seans / 8 seans paket.<br>Her satır: bölge · süre · "Kişiye özel" · [+ Ekle]. Eklenince yapışkan "Fiyat listem (3)" çubuğu çıkar → WhatsApp.<br>Bitiş garantili kalemlerde **"Bitiş garantili paket seçeneği"** rozeti (CRM'de 4 kalem).<br>"Fiyatı ne belirler?" başlığı altında 4 kart. | Yalnızca CRM adları ve süreleri. Fiyat rakamı yok (sahip kuralı). |
| L10 | **Davetiye** (planlayıcı) | Adımlar: bölgeler → **gün tercihi** (önümüzdeki 7 açık gün, Pazartesi kapalı) → **saat dilimi** (sabah 10–13 / öğle 13–17 / akşam 17–20) → hazır mesaj ve [W-] kodu.<br>Örnek mesaj: "Perşembe akşam uygun mu? Bölgeler: koltuk altı, tüm bacak (kadın). [W-…]".<br>Uydurma saat yok. | Mevcut `renderPlanner`; lazer için `slots:false`. |
| L11 | **Alt sayfa karoları** | Merkez sayfa ile 5 alt sayfa arasında video ve fotoğraf karoları. Dokununca View Transitions geçişi. | — |

**Ayrıca:**
- Hazırlık ve sonrası kartları yalnızca **mevcut sayfalardaki metinlerden** dönüştürülür; yeni tıbbi talimat eklenmez.
- Mevcut SSS ve SEO bölümleri "Detaylı bilgi" altında DOM'da kalır.

## 3. Sayfa sayfa (her sayfanın kendi kimliği; H1, başlık, meta ve canonical korunur)

| Sayfa | Varsayılan | Hero | Öne çıkan |
|---|---|---|---|
| **/laser-signature** (merkez) | Kadın, Ön | L1 + `lazer-film-jel` | L2 → L3 → L4 → L5 → L6 → L7 → L8 → L9 (kısa) → L11 |
| **/lazer-epilasyon-fiyatlari-ankara** | Kadın | L1 + `lazer-ekran` | **L9 tam menü** (ilk bölüm), "Fiyatınızı 3 adımda alın", L2 (kısa), L7 |
| **/erkek-lazer-epilasyon** | **Erkek** silüeti, grafit ve gül altını | `lazer-film-kol` | L2 erkek bölgeleri (sakal üstü, ense, sırt, göğüs, kemer üstü), erkek danışan yorumları, L9 erkek sekmesi, L4 |
| **/yuz-lazer** | Yüz yakın planı açık | `lazer-film-cene` | Yüz haritası hero'nun hemen altında, 4–6 haftalık takvim, gözlük ve güvenlik, mevcut "Akademik kaynaklar" bölümü korunur |
| **/hassas-cilt-lazer** | Kadın | `lazer-film-yuz` | Soğutma 10 °C vurgusu, **cilt tonu seçici** (6 nötr ton → mesaja "cilt tonum: …, cildim hassas" eklenir; sağlık verisi sorulmaz), L5, L8 |
| **/bolgesel-lazer** | Kadın | `lazer-koltuk` | "Sadece ihtiyacınız olan bölge". **15 dakikalık bölgeler** şeridi CRM'den (koltuk altı, dudak üstü, çene, gıdı, boyun, göbek…). Tek dokunuşla hızlı seçim |
| **/laser-signature-kampanya** | merkez sayfayla aynı vitrin | — | Düzeltmeler: NAP "Yaşamkent" → Konutkent, "LazerMech" → Lasermach, canonical → /laser-signature (çift içerik birleşir; sitemap'te zaten yok) |

## 4. Prototip (aynı bağlantı: https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM)

- **Yeni `scratchpad/a3_build.py`:**
  - `atelier/src.html` dosyasını `src.v3.html` olarak bir kez dondurur.
  - LAZER bölümünü merkez sayfa vitriniyle değiştirir ve 5 yeni görünüm ekler: `lazer-fiyat`, `lazer-erkek`, `lazer-yuz`, `lazer-hassas`, `lazer-bolgesel`.
  - Lazer bileşenlerini **canlı yamanın `src/` dosyalarından satır içine alır.** Prototip ile canlı aynı kodu kullanır.
- **Menü ve panel:**
  - Menüdeki 6 lazer sayfası prototip içinde açılır.
  - Prototip panelinin "Sayfa" bölümüne "Lazer ▸" alt seçimi eklenir.
  - Salon karosu merkez sayfaya gider.
  - Prototipteki lazer davetiyesi de gün ve saat dilimi kullanır, örnek saat göstermez.
- **Dosya bütçesi (en fazla 255):** bugün 241 dosya var ve lazer için yaklaşık 23 yeni dosya gerekiyor.
  - `film/salon-giris` (71 kare) ve `film/cilt-led` (59 kare) **tek sprite WebP**'ye paketlenir; `initFilm` sprite'tan çizer. Böylece yaklaşık 128 dosya boşalır.
  - Prototipte her görselin tek boyutu (900w) kullanılır.
- Ardından Version 4 olarak yeniden yayımlanır.

## 5. Canlı yama: `google-adsAI/patches/atelier_lazer_20261007/`

- **Komutlar:**
  - `build.py --out DIR` → kontrol için kopya üretir.
  - `--check` → kapı kontrollerini çalıştırır.
  - `--apply` → sahip çalıştırır.
  - `--rollback` → geri alır.
  - Desen `lp_quality_20261006.py` ile aynı: `LPQ.SITE`, `write_like`, `.gz`.
- **Kaynak dosyalar:**
  - `src/atelier.css`: prototipten ayrıştırılan ortak tokenlar ve bileşenler (nav, menü sayfası, çipler, halkalar, hikâye, lightbox, yorumlar, SSS, butonlar, yapışkan bar).
  - `src/lazer.css`.
  - `src/atelier-core.js` (≤12 KB gz):
    - kademe tespiti;
    - 91 sayfalık menü (sitemap'ten);
    - hikâye ve lightbox;
    - `sig` sayacı;
    - `waHref` (gerçek `SGBVisit.mark()` ile);
    - dinamik çizimden sonra `bindLeadTracking`;
    - açık/kapalı çipi.
  - `src/lazer.js`: L2–L10 adaları; ekrana yaklaşınca ya da ilk dokunuşta yüklenir.
  - `pages.json`: her sayfanın varyantı, hero medyası, varsayılanları, bölüm sırası, yorum süzgeci ve hikâyeleri.
- **Her HTML dosyasında yapılanlar:**
  - **Korunanlar:** `<head>`, title, meta, canonical, robots, consent, gtag, ads-attribution, `script.js`, `ads-tracking.js` ve `sgb-offers.js`.
  - **Head'e eklenenler:** atelier CSS (kritik kısmı satır içinde) ve hero poster preload. Eski salon preload'u kaldırılır.
  - **Değişen gövde:**
    - `<header class="hero…">` yerine L1 gelir; **H1 metni birebir aynı** kalır.
    - Vitrin bölümleri hero'nun hemen arkasına eklenir.
    - Eski bölümlerin hepsi "Detaylı bilgi" altında görünür metin olarak kalır.
    - Eski `lp-sticky-actionbar` yerine ATELİER barı gelir.
  - **İşaretleme:** JSON-LD `image` yeni fotoğrafa geçer ve `sitemap-images.xml` dosyasına lazer görselleri eklenir.
  - **Yedek ve dosyalar:** işaret `<!-- SGB_ATELIER_LAZER 20261007 -->`, yedek `.bak-20261007-atlz`, `.gz` yeniden üretilir.
  - **Dokunulmayanlar:** `styles.css` ve `script.js` → Faz 0 ile sıra çakışması yok.
- **Medya:** `public_html/images/ig/lazer-*`.
  - `media_ig` site yaması (henüz uygulanmadı) bu işareti taşıyan sayfaları atlayacak şekilde ayarlanır.
- **Takip (tagctx kuralı):**
  - Her buton ve bağlantıda `data-track-label="at-<sayfa>-<yer>"` bulunur.
    - Sayfa kodları: `lazer`, `lzfiyat`, `lzerkek`, `lzyuz`, `lzhassas`, `lzbolge`, `lzkamp`.
    - Yer örnekleri: `hero-wa`, `harita-bolge`, `harita-wa`, `takvim-baslangic`, `cihaz-nokta`, `menu-ekle`, `menu-wa`, `davetiye-gun`, `davetiye-wa`, `bar-wa`, `bar-tel`, `alt-sayfa`.
  - WhatsApp ve telefon butonları **gerçek `<a href>`** olur. Böylece contact-ping `b=`, SGB_VISIT tap, Ads dönüşümü ve [W-] kodu ek kod gerekmeden çalışır.
- **Hız bütçesi:**
  - İlk ekran ≤180 KB; LCP ≤2,5 sn (mobil lab).
  - Videolar yalnızca görünürken ve A/B kademesinde yüklenir.
  - Sayfanın tamamı ≤1,5 MB; C kademesinde ≤0,4 MB.

## 6. Dil: "maksimum öv, risk alma"

**Kullanılacak (kanıtlı):**
- "Lazerde yorumlarımız konuşuyor: Google'da lazer geçen 31 yorumun 30'u 5 yıldız."
- "Bitiş garantili paket seçeneği."
- "Lasermach diode · 3 dalga boyu · soğutmalı başlık."
- "8 seanslık plan, aralığı bölgenize göre."
- "Salonumuzda çekildi" (gerçek videolar).
- Kelimesi kelimesine müşteri yorumları, örneğin:
  - "Daha önce bir çok yerde epilasyona gitmiş olmama rağmen hiç sonuç almamıştım. Çok memnunum."
  - "4. seansdan sonra gerek bile duymuyorum…"
  - "neredeyse hiç acı hissetmedim"

  Yorumlarda yüzde ifadesi olmaz.

**Yasak:**
- "kesin sonuç", "%100", "kalıcı" (mutlak anlamda), "acısız" (bizim iddiamız olarak), "en iyi" / "1 numara";
- sahte önce/sonra, sahte kıtlık, geri sayım, popup;
- "garanti" kelimesi, CRM'deki "bitiş garantili paket" adı dışında.

`--check` bu kuralları metin taramasıyla zorlar.

## 7. Doğrulama

1. **Prototip:** `shoot` betiği 6 lazer görünümünü, menüyü ve davetiyeyi 390×844 ve 1400×900'de çeker. Beklenenler:
   - JS hatası 0, yatay taşma 0 (320 / 390 / 430 / 1400);
   - bütün etiketler geçerli;
   - harita → mesajda bölgeler ve [W-] var;
   - takvim tarihleri doğru (yüz 4–6, vücut 6–8 hafta).
2. **Canlı kopya:**
   - `build.py --out DIR` ve `--check` çalışır. `--check` şunları denetler:
     - H1, title, meta, canonical ve robots aynı;
     - eski H2'lerin hepsi duruyor;
     - "Yaşamkent" NAP 0;
     - yasak ifade 0;
     - her `a` ve `button` etiketli.
   - `firstscreen_ovl.mjs` ile 7 sayfanın telefon ve masaüstü ekran görüntüsü alınır.
   - Playwright tıklama testi (ağ kapalı, `/api` 204): her WhatsApp ve telefon CTA'sında 1 contact-ping (doğru `b`), 1 SGB_VISIT tap ve [W-]'li href olmalı.
   - Reddet senaryosunda dönüşüm gitmemeli.
3. **Sahip `--apply` çalıştırdıktan sonra:**
   - `./run tag_ctx.py verify --pages <7 sayfa>`
   - `patches/verify_tags.sh`
   - `adsctx/page_health_check.sh`
   - `curl` ile `.gz`'nin servis edildiğini kontrol
   - `graphify update .`
4. **Ölçüm:** 7. ve 28. günde `ask pages` lazer satırları (öncesi/sonrası, Wilson aralığı).
   - TL artışı iddia edilmez.
   - Lazer reklamları kapalı olduğu için okuma organik ağırlıklı ve gürültülü olacak.

## 8. Sıra ve kim ne yapar

1. Medya: manifest + `build_media.py`.
2. `src/` bileşenleri: L1–L11.
3. `a3_build.py` → prototip Version 4 yayımlanır → sahip telefonda bakar.
4. `atelier_lazer_20261007/build.py --out` + `--check` + ekran görüntüleri ve tıklama testi.
5. Sahip çalıştırır:
   ```
   cd /var/www/seldagencerbeauty.com/google-adsAI && ./run patches/atelier_lazer_20261007/build.py --apply
   ```
   Geri almak için aynı komut `--rollback` ile.
6. Canlı sonrası kapılar (§7.3).
7. Bellek güncellenir:
   - Faz 0 ve fiyat menüsü uygulandı (bellekteki "uygulanmadı" bilgisi eski);
   - FAZ L kararları.

## Ekler: önceki fazların özeti (detayları uygulandı ya da bellekte)

- **ATELİER v3 (10-06 onaylı):** "Mermer, Altın, Işık" dili.
  - Kurallar: ilk saniyede dönüşüm; ziyaretçi seyirci değil, sanatçı; her şov tek bir WhatsApp butonuna bağlanır; şov kademeye göre ölçeklenir (A/B/C) ve asla takılmaz.
  - Kalite kapıları: sahibin telefon onayı, 5 saniye testi, rakiple yan yana, LoAF 0, hız bütçesi, kusursuzluk listesi, tagctx.
- **FAZ M:** Instagram'dan en iyi medya seçildi (`media_ig_20261007/manifest.json`, 88 öğe). Canlı site yaması ayrı onayla.
- **FAZ A2 (prototip v3):**
  - 8 vitrin;
  - 91 sayfalık menü;
  - 185 etiketli buton ve `sig` sayacı;
  - tırnak boyama düzeltmesi (yumuşak mat + nötr plaka).
- **Kalan yol haritası:**
  - Faz C: diğer ailelerin canlı sayfaları.
  - CRM paketi `20261007-site-atelier`: `site-slots`, `site-pulse`, `site_events.sig`, Sayfa Sağlığı ATELİER kartı.
  - Çekim günü.
  - Sahip onayları: bakış eşlemesi, cilt testi, dudak ton adları.
