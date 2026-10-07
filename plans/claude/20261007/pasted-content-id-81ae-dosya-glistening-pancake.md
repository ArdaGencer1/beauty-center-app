# Kalıcı Makyaj "Şölen": ATELİER prototipinde PMU sayfalarını bitirme

## Context
Sahip, kalıcı makyaj (PMU) bölümünün çarpıcı olmasını istiyor: sayfaya giren şaşırsın ve randevu alsın. En iyi fotoğraflar en iyi şekilde düzenlenip kullanılacak. Şimdilik diğer vitrinlere dokunulmayacak. İkinci mesajda "kalıcı makyaj sayfalarını tam bitir" dendi. Bu nedenle sitemap'teki 11 PMU sayfasının hepsi bir vitrine bağlanacak.

Bugünkü PMU vitrini düz kalıyor:
- 1 dudak slider'ı, ton seçici, göz ve kaş ikilisi, galeri.
- Fotoğraflarda IG filigranı ve "KALICI MAKYAJ" etiketleri duruyor.
- Menüdeki 10 PMU alt sayfası prototipte hâlâ "mevcut sayfa ↗" diye dışarı gidiyor.

Hedef artifact (güncellenecek, yenisi açılmayacak): https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM. Kaynak dosyası: `tool-results/artifact-f11cc523-1791364926-c6e9.html` (1778 satır).

## Bulgular ve doğruluk kuralları
- **Yabancı fotoğraf.** IG 18516297502030856 (prototipteki `kas-cift-3`) gözde "TALITA …STRO" filigranı taşıyor. Sahip yanlışlıkla konduğunu söyledi.
  - Kaş galerisinden (`KAS_PAIRS`) ve `manifest.json`'dan çıkarılacak.
  - PMU'da kullanılmayacak.
- **Site fotoğrafları salonun işi (sahip onayladı).** `public_html/images/kalici-makyaj-1…10.jpeg` setinde filigransız, en temiz çiftler var: dudak 2/3/1, eyeliner 10 ve makrolar 4/5/6/7/9.
- **Kullanılmayacaklar:**
  - `kalici-makyaj-dudak-20260407.png` (1024×1536). Kalici-makyaj-7'nin AI ile pürüzsüzleştirilmiş hâli.
  - 18104556860143186 (MAST kalem afişi). Stok görünümlü.
  - 17986864907913512. Laminasyon ya da lifting, PMU değil.
  - 18284646271254855. 360p.
- **Fiyatlar** CRM'den okundu (`panel…/api/public/price-menu`, 10-07):

  | Hizmet | Fiyat |
  |---|---|
  | Baby liner | 5.000 TL |
  | Dipliner | 6.000 TL |
  | Eyeliner | 7.000 TL |
  | Dudak | 9.000 TL |
  | Microblading | 9.000 TL |
  | Powder | 9.000 TL |
  | Mix | 9.000 TL |
  | **Kaş silme (yeni)** | **3.500 TL** |

  Hepsi 60 dk. Canlı sayfa kaş silme için "sabit seans sayısı verilmez" diyor. Bu yüzden şöyle yazılacak: "3.500 TL / seans · plan kaş görüldükten sonra".
- **Yorumlar.** 263 Google yorumunda kalıcı makyajdan söz eden yalnız 1 tane var (Gülbeyaz G., 2025-08).
  - O yorum öne çıkarılır.
  - Diğer yorumlar "Salon için yazılanlar" etiketiyle hijyen ve güven odaklı gösterilir. Daha fazla PMU yorumu varmış gibi yapılmaz.
- **SSS metinleri** yalnız canlı PMU sayfalarının JSON-LD SSS'lerinden kısaltılır. Bu metinler "acısız" ya da "ömür boyu" sözü vermiyor, rötuşu "takipte netleşir" diye anlatıyor.
- **Hiç yazılmayacaklar:** "ücretsiz görüşme" ve süre garantisi.
- **Taslak etiketi gerekenler:** ton adları taslak (sahip onaylayacak). Boş saatler "(örnek)" olarak kalır.
- **Düzenleme kuralı (önce/sonra dürüstlüğü):**
  - Bir çiftin iki yarısına aynı renk ayarı uygulanır.
  - Pigment tonu değiştirilmez.
  - Yalnız "sonra" yarısına rötuş ya da cilt pürüzsüzleştirme yapılmaz.
  - Kırpma, hizalama, pozlama ve beyaz dengesi, hafif keskinleştirme, etiket ve imza temizliği serbest.

## 1. Fotoğrafları seçme ve düzenleme
**Değişecek dosyalar:** `google-adsAI/patches/media_ig_20261007/build_media.py` ve `manifest.json`. Canlı Faz C de aynı hattı kullanacak.

**`build_media.py`'ye eklenecekler (geriye uyumlu):**
- `file`: IG `id` yerine yerel kaynak. Site jpeg'leri için.
- `crop`: kaynaktan oran olarak `[x0,y0,x1,y1]` kesit. Etiket ve imza kırpmak için.
- `delogo`: düz cilt üstündeki ortadaki monogram ya da etiket için kutular. ffmpeg `delogo` kullanılır. Yalnız kanıt temiz çıkarsa uygulanır.
- `align`: iki noktalı yer işaretleri (`once:[[x,y],[x,y]]`, `sonra:[…]`). Burun ve ağız köşesi gibi işlem görmemiş noktalardan benzerlik dönüşümü hesaplanır (ölçek, dönme, kaydırma). İki yarı aynı W×H'de çıkar.
- `grade:"pmu"`: `eq` (kontrast 1.05, doygunluk 1.03, gama .98) ve `unsharp`. Tek fotoğraflarda hafif `vignette` de eklenir. Çiftin iki yarısına birebir aynı uygulanır.
- `film` ile `atlas` (aşağıda).
- Var olan `GRADE` ve `webp_set` yeniden kullanılır.

**Yeni manifest kalemleri:**

| Grup | Kalemler |
|---|---|
| Dudak çiftleri | `pmu-dudak-a` (site-2, v, hizalı) · `pmu-dudak-b` (site-3, h) · `pmu-dudak-c` (site-1, v). `dudak-cift-5` için hizalama, `dudak-cift-4` için imza kırpma eklenir. |
| Dudak makroları | `pmu-ton-parlak` (site-4) · `pmu-ton-visne` (site-5) · `pmu-ton-gul` (site-7) · `pmu-ton-ahududu` (site-9). Site-6 isteğe bağlı. |
| Göz | `pmu-goz-a` (site-10, v) |
| Kaş | `pmu-kas-cift-a` (IG 17981935718764019, h, delogo) · `pmu-kas-cift-b` (IG 18091579450867776, h, delogo) · `pmu-kas-makro` (IG 18046411448587830; etiket ve imza kırpılır) · `pmu-kas-pudra` (IG 18037699223717361, imza kırpılır) |
| Oda | `pmu-oda-istasyon` (IG 18604797226029445) ve `pmu-oda-yatak` (IG 17869181736564248). Afişlerin sağ tarafındaki gerçek oda fotoğrafından yazısız kesit alınır. |
| Film | `pmu-kalem`: IG 17971549406932390, kalemle kıl kıl kaş çizimi (720×1280, 14.8 sn). Önce 3 kare bakılır. İlerleme görünüyorsa kaydırmaya bağlı film olur, görünmüyorsa sessiz döngü video olur. |

**Kanıt (zorunlu).** Scratchpad'de `pmu/proof/` altında her çift için üç sütunlu bir sayfa üretilir: önce | sonra | %50 karışım. Hepsine tek tek bakılır.
- Yabancı filigran var mı diye kontrol: göz parıltıları ve köşeler 2× yakınlaştırılarak bakılır.
- Etiket temizlendi mi?
- İki yarıya aynı renk ayarı uygulandı mı?
- Hizalama tutuyor mu?
- Hizası tutmayan çift "fırça" efektine girmez, ışık süpürmesiyle gösterilir.

**Artifact dosya bütçesi.** Artifact'in sınırı 255 dosya, şu an 241 dosya var. Paketlemeyi scratchpad'deki `pmu/pmu_pack.py` yapar; canlı site ayrı dosyaları kullanır.
- Her çift tek dosya olur (`*-pair.webp`, önce|sonra yan yana).
- Ton makroları 2×2 tek sayfaya girer.
- Oda kesitleri tek sayfaya girer.
- Film 3 atlasa paketlenir (36 kare, 540×960, 4×3).
- Her makronun dudak bölgesinden medyan renk alınır ve ton yuvarlağı rengi yapılır.

Dosya hesabı:
- Yeni dosya: yaklaşık 15.
- Kaldırılacak dosyalar (`null`): `dudak-cift-3-*` (aynı danışan), `kas-cift-3-*`, `dudak-cift-2-sonra-1200`, `dudak-cift-4-sonra-1200`, `dudak-2-1200`. Hepsinin başka yerde kullanılmadığı doğrulanacak.
- Sonuç yaklaşık 249 dosya, sınırın altında.

## 2. Sayfalar (dört vitrin)
`pmu` merkez sayfa olur, yanında üç alt vitrin açılır.

**Ortak görünüm:**
- Sahne bölümleri her zaman siyah kadife ve altın.
- Bilgi bölümleri Mermer/Gece anahtarına uyar.
- Var olan `.dark-band`, `.foil-text`, `initDust`, `initCompare`, `tween`, `card()`, `openLightbox`, `STORIES` ve `rings` yapıları yeniden kullanılır.

### `pmu`: Kalıcı Makyaj (merkez, "şölen")
1. **PERDE (100svh açılış).** Sayfa tam ekran canvas'ta, `pmu-dudak-a`'nın dik "önce" yarısıyla açılır.
   - Altın kenarlı yumuşak bir fırça dudak hattı boyunca kendiliğinden geçer ve "sonra"yı boyar. Ardından altın ışık süpürmesi açılışı tamamlar. Toplam süre yaklaşık 2,4 sn.
   - Sonra harf harf beliren yaldızlı "Kalıcı Makyaj" başlığı ve "Bir fırça darbesi. Her sabah hazır." alt başlığı gelir.
   - Bilgi çipleri: ★ 4,6 · 263 yorum | 5.000 TL'den | Bugün 14:30 müsait. Hikâye halkaları da burada.
   - Ziyaretçi "Parmağınızla boyayın ↔" ipucuyla kendisi de boyayabilir. `touch-action:pan-y` sayesinde yatay hareket boyar, dikey hareket sayfayı kaydırır.
   - "↺ Yeniden" düğmesi ve 1/2 noktaları (`pmu-dudak-a`, `dudak-cift-5`) var.
2. **ÜÇ SANAT.** Üç dik kart, yavaş yakınlaşan canlı görsellerle:
   - Dudak · 9.000 TL
   - Kaş · 9.000 TL
   - Göz · 5.000 TL'den

   Her kart kendi alt vitrinine götürür.
3. **ÇİZGİ ÇİZGİ.** `pmu-kalem` filmi kaydırdıkça oynar: "Kaydırın: kıl kıl çizilir." Bölümler: Ölçüm → Çizim → Pigment. Var olan `initFilm` genelleştirilerek atlas okur hâle getirilir.
4. **UYANIŞ.** Sabit sahnede 5 dönüşüm; her biri kaydırmayla ilerleyen altın ışık süpürmesiyle önceden sonraya geçer.
   - Sıra: `pmu-dudak-b`, `pmu-kas-cift-a`, `pmu-goz-a`, `pmu-kas-cift-b`, `dudak-cift-1`.
   - Her dönüşümde "01/05", hizmet adı ve fiyat görünür.
   - "Bunu istiyorum →" düğmesi davetiyeyi o hizmet seçili ve referanslı açar.
   - Kademe C'de bunlar alt alta duran sabit karşılaştırmalara döner.
5. **TON KARTELASI.** Mevcut ton seçicinin yerine geçer.
   - Parlak makrolar arasında geçişte bir parıltı süpürmesi oynar.
   - Rujlar, fotoğraftan alınan gerçek renkte SVG ruj başları olarak gösterilir.
   - "Bu ton bana yakışır mı?" düğmesi WhatsApp mesajına "Ton: …" ekler.
   - Ton adları "taslak" etiketiyle kalır.
6. **ODA.** Gerçek PMU istasyonu ve yatak fotoğrafları gösterilir. Yanındaki üç kısa satır yalnız salonun kendi IG'de yazdıklarından alınır.
7. **YOL.** Dört adım: ön görüşme → çizim ve onay → uygulama → takip. Rötuş ve fiyat dili canlı SSS'den alınır.
8. **SÖZ.** Öne çıkan tek PMU yorumu, altında "Salon için yazılanlar" kayan şeridi.
9. **MENÜ (`#fiyat`).** 8 kalem; kaş silme eklenir. Altında şu not yer alır: "Ücret ilk uygulamayı kapsar".
10. **SSS.** 6 soru: bölgeler, micro ve pudra farkı, liner farkları, kalıcılık, acı, rötuş.
11. **KAPI ve FİNAL PERDE.** Tam ekran kadife kapanış: "Yarın sabah aynada." Altın "Saatimi seç" düğmesi, WhatsApp ve telefon.

### `pmu-dudak` (dudak-renklendirme)
- Açılışta aynı fırça sahnesi var. 5 dudak çifti gezilebilir: a, b, c, `dudak-cift-5`, `dudak-cift-1`.
- Tam ton kartelası.
- "İyileşmiş dudaklar" makro galerisi.
- Fiyat 9.000 TL · 60 dk.
- 3 soruluk SSS.

### `pmu-kas` (microblading, powder-brows, mix-brows, kas-silme, microblading-fiyatlari)
- Açılışta `pmu-kas-cift-a` slider'ı, girişte otomatik süpürmeyle.
- **TEKNİK LAB.** Bir SVG kaş şeması üç teknik arasında yeniden çizilir; her birinde fiyat 9.000 TL. Altta "şema, gerçek sonuç değil" notu durur.

  | Teknik | Şema | Gerçek fotoğraf |
  |---|---|---|
  | Kıl tekniği | kıl çizgileri | `pmu-kas-makro` |
  | Pudralama | noktalı gölge | `pmu-kas-pudra` |
  | Mix | çizgi ve gölge birlikte | yalnız şema |

- Kalem filmi burada da kullanılır.
- Galeri: `pmu-kas-cift-b`, `pmu-kas-1`, `pmu-kas-2`.
- **"Eski kalıcı kaşım var" bloğu.** Kaş silme 3.500 TL / seans. "Gün ışığında, filtresiz fotoğrafınızı gönderin" mesajı hazır yazılmış bir WhatsApp bağlantısıyla gelir.
- SSS.

### `pmu-goz` (eyeliner, dipliner, babyliner)
- Açılışta `pmu-goz-a` slider'ı (dik yarılar).
- **ÇİZGİ STÜDYOSU.** "Önce" göz fotoğrafının üstünde SVG çizgi animasyonla çizilir. Üstünde "temsili çizim" etiketi durur.

  | Stil | Fiyat |
  |---|---|
  | Baby liner (ince) | 5.000 TL |
  | Dipliner (kirpik dibi) | 6.000 TL |
  | Eyeliner (kuyruklu) | 7.000 TL |

- Gerçek sonuçlar: `pmu-goz-a`, `goz-cizgisi-cift`.
- SSS: fark, kimler için, öncesinde lens ve hassasiyet bilgisi.

### Gezinme
- `VIEWS` listesine `pmu-dudak`, `pmu-kas`, `pmu-goz` eklenir.
- `go()` artık `#görünüm/parametre` biçimini çözer (örnek: `#pmu-kas/pudra`, `#pmu-goz/dipliner`, `#pmu/fiyat`).
- `NAV` içindeki 11 PMU kaydı vitrinlere bağlanır:
  - kalici-makyaj → pmu
  - dudak-renklendirme → pmu-dudak
  - microblading / powder-brows / mix-brows → pmu-kas, ilgili teknik seçili
  - kas-silme → pmu-kas/silme
  - eyeliner / dipliner / babyliner → pmu-goz, ilgili stil seçili
  - kalici-makyaj-fiyatlari → pmu/fiyat
  - microblading-fiyatlari → pmu-kas/fiyat
- Prototip panelindeki "Sayfa" seçicisine 3 düğme eklenir.

## 3. Randevuya iten düzenekler
- **Alt çubuk etiketleri:**
  - Dudak vitrininde seçilen ton: "Gül · saatimi seç".
  - Kaş vitrininde seçilen teknik.
  - Göz vitrininde seçilen stil.
  - Bu, `updateBar` ve `BAR` üzerinden yapılır.
- **Davetiye seçenekleri.** `PLANS["pmu-dudak"|"pmu-kas"|"pmu-goz"]` alt kümeleri eklenir. `pmu` planına kaş silme girer.
- **WhatsApp mesajı.** `P.ref` ile "Referans: Uyanış 03 · kalıcı kaş", "Ton: Vişne" ya da "Teknik: Pudralama" eklenir. Ekip, müşterinin tam olarak ne istediğini bilir.
- Her "vay" bölümü bir CTA ile biter; sayfa final perdeyle kapanır.
- Fiyat ilk ekranda: "5.000 TL'den".
- **Sayaç etiketleri.** Tüm yeni düğmelere `data-track-label="at-pmu…"` verilir (ASCII, en çok 48 karakter). `autoLabel` genişletilir.

## 4. Kod uygulaması
- **Çalışma klasörü:** `scratchpad/pmu/`.
  - `index.html`: kaynak dosyanın kopyası.
  - `m/`: önceki `atelier/m` ve yeni medya.
  - `pmu_build.py`: `a2_build.py` deseniyle, sayılı ve doğrulanmış `rep()` değişimleri yapar. Şunları ekler ya da değiştirir:
    - PMU `<section>` bölümünü baştan yazar, üç yeni `<section>` ekler.
    - `/* PMU şölen */` CSS bloğu; masaüstü, kademe C ve reduced-motion kuralları dahil.
    - JS: `initBrush`, `initFilmAtlas`, `initReel`, `initKartela` (`initTones` yerine), `initTechLab`, `initLineStudio`, rota çözümü, `PLANS`, `STORIES.pmu*`, `NAV` eşlemesi, `initView` kancaları.
    - `KAS_PAIRS` listesinden `kas-cift-3` çıkarılır.
- **Yazmadan önce:** `artifact-design` skill'i yüklenir ve artifact kaynağının okunmamış satırları (1-559, 735-1019, 1066-1169) okunur.
- **Yayın:** `Artifact publish`, `url` ile aynı artifact'e yapılır. `files` yeni dosyaları ekler, kaldırılanlara `null` verilir. `capabilities` gönderilmez.
- **Kod değişikliğinden sonra:** `graphify update .`

## 5. Doğrulama
1. **Medya:** `pmu/proof/*` sayfalarının hepsine bakılır (filigran, etiket, aynı renk ayarı, hizalama). `media_index.json` kayıtları kontrol edilir.
2. **Ekran görüntüleri.** `shoot2.mjs` deseniyle (Playwright, yerel yönlendirme) alınır: iPhone 13 ve 1440 masaüstü; Mermer ve Gece; kademe A ve C. Çekilecekler:
   - Açılışın 0 / 1,2 / 2,6 sn hâli ve elle boyama.
   - Uyanış'ta 3 kaydırma noktası.
   - Film.
   - Kartela tıklaması.
   - Teknik Lab'in 3 durumu.
   - Çizgi Stüdyosu'nun 3 durumu.
   - Üç alt vitrin.
   - Davetiye sayfaları ve WhatsApp metninin açılmış hâli.
   - Menü derin bağlantıları (`#pmu-kas/pudra`).
3. **Otomatik kontroller:**
   - Yatay taşma 0.
   - Konsol hatası 0.
   - Dosya sayısı en çok 255.
   - Kırık `m/` referansı 0 (HTML ve JS'deki tüm yollar dosya listesiyle karşılaştırılır).
   - Etiket kuralı geçiyor.
4. **Duman testi:** salon ve kaş açılıyor mu? Kaş galerisi 3 kart mı?
5. **Yayın sonrası:** `Artifact read` ile canlı sürüm ve dosya sayısı doğrulanır.

## 6. Hafıza
`vitrin-landing-plan-20261006` güncellenecek. Eklenecekler:
- PMU vitrinleri.
- Site fotoğraflarının sahip onaylı olduğu.
- `kas-cift-3` yabancı filigranı ve çıkarıldığı.
- AI ile düzenlenmiş PNG'nin hariç tutulduğu.
- CRM'deki kaş silme fiyatı 3.500 TL.
