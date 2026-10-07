# FAZ L+ · Lazer epilasyon: “vay” planı (2026-10-07)

Bu plan, `https-panel-seldagencerbeauty-com-new-cu-wiggly-adleman.md` (FAZ L)
planının **üstüne** gelir; onu değiştirmez. FAZ L'nin kuralları, medya
kararları, dil yasakları (§6) ve doğrulama kapıları (§7) aynen geçerlidir.

Sahibin isteği: “Lazer epilasyon sayfasını daha fazla geliştirelim, gelen
‘vay’ demeli.”

## 0. Bugünkü durum (ölçüldü, 10-07)

`sources/atelier_lazer_20261007/render.py` + `src/lazer.css` + `src/lazer.js`
ile 7 sayfa yerelde derlendi. Merkez sayfa (`hub`) 390×844 ve 1400×900'de
Playwright ile çekildi.

- JS hatası: 0. Yatay taşma: 0. (Yerelde yalnızca beklenen
  `/api/public/price-menu` fetch hatası var; derleme anındaki süre kopyası
  devreye giriyor.)
- Mobil sayfa boyu **10.481 px** (~12,5 ekran); masaüstü 11.397 px.
- L1–L10 bileşenlerinin hepsi çalışıyor. Ancak “vay” etkisini bozan
  sorunlar var:

| # | Bulgu | Yer | Etki |
|---|---|---|---|
| B1 | **Takvim etiketleri üst üste biniyor**: nokta altı ay etiketleri (“Ara–Oca”, “Mar–May”) başlangıç düğmeleriyle ve “8. seans ≈ …” metniyle çakışıyor. | L4, 390 px | Kırık görünür; güveni düşürür. |
| B2 | Merkez sayfa hero'su **durağan fotoğraf** (`lazer-5`). FAZ L planında `lazer-film-jel` videosu vardı. Tarama çizgisi var ama ilk saniyede fark edilmiyor. | L1 | İlk 5 saniyede “vay” yok. |
| B3 | Mobilde kanıt çipleri (3 dalga boyu · 10 °C · 30/31) fotoğrafın en üstünde, logoyla çakışıyor ve okunması zor. Masaüstünde yapışkan WhatsApp barı kanıt çiplerinin üstüne biniyor. | L1 | Kanıt değerini kaybediyor. |
| B4 | “Işığın Yolculuğu” adımları arasında mobilde ~400–500 px'lik boş siyah alanlar var; bölüm toplam ~3 ekran. | L3 | Kaydırma yorucu; sahne boş görünüyor. |
| B5 | Vücut haritası silüeti manken gibi; “DOKUNUN” etiketi kalça hizasında gövdeye biniyor. Haritanın altındaki “Listeden seçmek isterim” bölümü kapalıyken ~150 px boşluk bırakıyor. | L2 | Merkez imza deneyimi sıradan duruyor. |
| B6 | “Salonumuzda çekildi” şeridinde yalnız 2 video var; elde 6 hazır video var. | L6 | Gerçek videoların gücü kullanılmıyor. |
| B7 | Yorum duvarı kartları ekranın solundan kesik başlıyor; büyük “30/31” sayısı durağan. | L7 | Sosyal kanıt sönük. |

Not: Hijyen ve alt sayfa karolarındaki boş kareler tam sayfa çekimdeki
`loading="lazy"` kaynaklıdır; gerçek kaydırmada doluyorlar (doğrulandı).

## 1. “Vay” formülü: 3 an

Ziyaretçi şu üç anda “vay” demeli. Her biri tek bir WhatsApp butonuna
bağlanır.

1. **İlk 2 saniye — Işık açılışı:** Sayfa karanlık açılır, pembe-altın bir
   lazer çizgisi ekranı süpürür. Çizgi geçtikçe gerçek salon videosu ve H1
   harfleri yanar.
2. **İlk dokunuş — Işığı sen yönlendir:** Vücut haritasında dokunduğun
   bölgede bir lazer atışı patlar, bölge pembe yanar ve kişisel planın anında
   oluşur.
3. **İlk karar — Planın hazır:** Seçimlerin; bölge, süre, 8 seans, aralık ve
   tahmini bitiş ayıyla tek bir zarif “Lazer Planım” kartına dönüşür. Tek
   dokunuşla WhatsApp'a gider.

Geri kalan bölümler bu üç anı destekleyen kanıttır: cihaz, gerçek videolar,
yorumlar ve hijyen.

## 2. İşler

### Dalga 1 — Kırıkları düzelt (önce bu; küçük, risksiz)

| İş | Ne yapılır | Dosya |
|---|---|---|
| D1.1 | B1: takvimde başlangıç düğmeleri ayrı satıra alınır; ay etiketleri yalnız 1., 4. ve 8. noktada gösterilir, diğerleri dokununca. 320 / 390 / 430 px'te çakışma 0. | `lazer.css`, `lazer.js` (L4) |
| D1.2 | B3: kanıt çipleri sahnenin altına, cam şerit olarak taşınır. Masaüstünde yapışkan bar hero görünürken gizlenir; hero'dan çıkınca kayarak gelir. | `render.py` (L1), `lazer.css` |
| D1.3 | B5: “DOKUNUN” etiketi silüetin dışına, nabız atan bir el ikonu olarak alınır. Kapalı liste boşluğu kaldırılır. | `lazer.css` |
| D1.4 | B4: adım aralıkları kısaltılır (bölüm ≤ 2 ekran). | `lazer.css` (L3) |

**Durum (10-07): Dalga 1 tamamlandı** (yalnız `sources/atelier_lazer_20261007/`;
Artifact ve canlı site değişmedi).

- Kök neden: `.lz ol` / `.lz button` sıfırlamaları (özgüllük 0-1-1) tek sınıflı
  kuralları eziyordu. Etkilenenler: `.lz-track` (takvim çakışması),
  `.lz-hot` (cihaz noktaları 17 px sağa-aşağı kaymıştı), `.lz-allpages`,
  `.lz-how`. Hepsi `.lz .lz-…` ile düzeltildi.
- Kanıt şeridi fotoğraftan çıkarıldı, CTA'nın altına alındı. Masaüstünde
  yapışkan bar hero'nun yarısı görünürken gizli.
- “Dokunun” ipucu figürün altına alındı. Yolculuk adımları 66→56 svh,
  bölüm iç boşluğu 72→60 px.
- Doğrulama: 7 sayfa × 320/390/430/1400 px'te JS hatası 0, yatay taşma 0,
  takvim metin çakışması 0 (aynı test eski kodda 12–13 çakışma buluyor).
  `data-track-label` ve `href` değişmedi. Mobil sayfa boyu 10.481 → 10.150 px.

### Dalga 2 — “Vay” çekirdeği (3 an)

**W1 · Işık Açılışı (hero)**
- Merkez sayfa hero'su `lazer-film-jel` videosuna geçer. LCP için AVIF/WebP
  poster aynı kalır; video `load` olayından sonra ve yalnız A/B kademesinde
  gelir.
- Açılış koreografisi (toplam ≤ 1,4 sn, yalnız bir kez):
  1. Sahne %85 karanlıkla açılır.
  2. Lazer çizgisi yukarıdan aşağı süpürür; arkasında karanlık açılır.
  3. H1 harfleri çizgi geçtikçe soldan sağa yanar.
  4. CTA'da altın parıltı bir kez geçer.
- Tamamen CSS ile; `prefers-reduced-motion` ve C kademesinde doğrudan son
  kare gösterilir. LoAF 0, CLS 0.

**W2 · Işığı Yönlendir (vücut haritası yenilenir)**
- Silüet yeniden çizilir: manken yerine ince, tek çizgili, zarif bir
  “line-art” figür (kadın ve erkek ayrı). Bölgeler altın konturlu.
- Dokunuş efekti:
  - noktada pembe atış halkası ve kısa parlama;
  - bölge pembe ışıkla dolar;
  - `navigator.vibrate(12)` ile hafif titreşim (destekleyen cihazda).
- Seçim çubuğu canlı sayar: “3 bölge · menüdeki süreler ≈ 45 dk · 8 seans”.
- Yüz yakın planı: başa dokununca figür yumuşakça yüze yakınlaşır
  (View Transition / FLIP).
- Erişilebilir liste yedeği ve CRM bölge adlarıyla birebir eşleşme korunur.

**W3 · Lazer Planım kartı (harita + takvim birleşir)**
- Harita ve takvim tek bir kişisel kart üretir:
  - seçili bölgeler;
  - menüdeki toplam süre;
  - 8 seans; aralık (yalnız yüz → 4–6 hafta, vücut → 6–8 hafta);
  - başlangıç (Bu ay · Gelecek ay · 2 ay sonra) ve “8. seans ≈ Haz–Ağu 2027”;
  - bitiş garantili paket seçeneği olan bölgelerde rozet.
- Görünüm: koyu kadife zemin, altın çerçeve, başlıkta “Lazer Planım ·
  Selda Gençer Beauty Center”. Bir davetiye kartı gibi.
- Tek buton: “Planımı WhatsApp'tan gönder” → hazır mesaj + [W-] kodu.
  İsteğe bağlı ikinci buton: “Gün de seçeyim” (L10 davetiye).
- “Tahminidir; uzmanınız cilt ve kıl yapınıza göre ayarlar.” notu kalır.
- Kart yapışkan barın metnini de günceller: “Planım (3 bölge) → WhatsApp”.

**Durum (10-07): Dalga 2 tamamlandı** (yalnız `sources/atelier_lazer_20261007/`;
Artifact ve canlı site değişmedi).

- W1: `hub` ve `kamp` hero'su `lazer-film-jel` (poster 13,8 KB LCP; video
  `load` sonrası, A/B kademesi). Açılış: koyu perde, 1,3 sn'lik lazer
  taraması perdeyi yukarıdan aşağı kaldırır, H1 0,8 sn'de yanar. C kademesi
  ve azaltılmış harekette perde yok.
- W2: silüet yeniden çizilmedi, **yeniden stillendirildi**: altın kontur,
  saydam gövde, noktalı bölge dikişleri (manken görünümü kalktı). Atış
  efekti: parlama + iki halka + 6 kıvılcım, 12 ms titreşim. Canlı sayaç:
  “2 bölge · menüdeki süreler ≈ 60 dk · 8 seans”. Yüze yakınlaşma geçişi
  (View Transition) yapılmadı; Dalga 3'e kaldı.
- W3: takvim bölümü “Lazer Planım” kartına dönüştü: bölgeler, süre,
  8 seans + aralık, başlangıç, 8. seans tahmini, rozet (yalnız CRM'deki
  4 bitiş garantili paket ve fiyat menüsündeki garantili kalemler),
  “Planı WhatsApp'a gönder” (`plan-wa`) ve “Gün de seçeyim” (`plan-gun`).
  Yapışkan bar seçim varken aynı plan mesajını gönderir (“Planım · N bölge”).
- Örnek mesaj: “Merhaba, lazer epilasyon planım: koltuk altı, tüm bacak
  (kadın). 8 seans, 6–8 hafta arayla; gelecek ay başlamak istiyorum. Fiyat
  ve uygun günleri öğrenebilir miyim? [W-…]”
- `bindLeadTracking` her senkronizasyonda yeniden çağrılmaz (tanımı canlı
  `script.js`'te; tekilleştirme bilinmediği için çift ölçüm riski alınmadı).
- Doğrulama: 7 sayfa × 320/390/430/1400 px, 2 bölge seçiliyken: JS hatası 0,
  yatay taşma 0, plan kartı çakışması 0, kesilen düğme etiketi 0 (≤360 px
  için düğme yazısı küçültüldü), etiketsiz `a`/`button` 0, [W-] taşımayan
  WhatsApp bağlantısı 0. Yalnız yüz seçiminde aralık 4–6 hafta doğrulandı.
- Not: Masaüstü hero'da 720p video yarım ekrana büyütülüyor; hafif yumuşak
  görünür. Yeni çekim kararı (§6.2) bunu çözer.

### Dalga 3 — Kanıt bölümlerini parlat

**W4 · Işığın Yolculuğu, tek sahne**
- Sahne sabitlenir (sticky); adımlar sahnenin üstünde cam kartlar olarak
  akar. Boş alan kalmaz.
- Kökler sırayla ısınır (pembe→turuncu parıltı) ve söner. Dinlenen kökler
  gri kalır.
- 755 / 808 / 1064 nm çiplerine dokununca ışın o derinliğe iner.
- “Temsili anlatım” notu korunur.

**W5 · Cihaz Paneli turu**
- Bölüm görünür olunca 6 nokta sırayla, 1,2 sn arayla kendini anlatır
  (otomatik tur). Ziyaretçi dokununca tur durur.
- Ekran fotoğrafına hafif yakınlaşma (Ken Burns) ve aktif noktanın etrafında
  odak halkası.

**W6 · Salonumuzda çekildi: 5 video, hikâye oynatıcısı**
- Şerit 2 videodan 5 videoya çıkar: jel, çene, bacak, bacak2, yüz. Hepsi
  işlenmiş ve `website/m/ig/` altında hazır.
- Düzeltme (10-07): `lazer-film-kol` manifestte ve `website/m/ig/` altında
  **yok**; FAZ L tablosunda adı geçse de işlenmemiş. 6. video istenirse
  sunucuda `build_media.py` ile üretilir (§6.4).
- Görünen video sessiz oynar; dokununca tam ekran Instagram tarzı hikâye
  açılır (üstte ilerleme çubukları, kaydırarak sonraki video).
- Videolar yalnız görünürken yüklenir; C kademesinde poster.

**W7 · Yorumlar canlansın**
- “30 / 31” bölüm görününce 0'dan sayarak gelir.
- Konu çipleri: Acı · Sonuç · İlgi. Bunlar yalnız kelimesi kelimesine yorum
  metninde geçen sözcüklerle süzer. 12 yorumda sayım: Acı 2, Sonuç 7, İlgi 3,
  Hijyen 1. Kural: bir çip ancak ≥ 2 yorum eşleşirse gösterilir; bu yüzden
  Hijyen çıkarıldı.
- Kartlar ekran kenarından kesik başlamaz; ilk kart hizalı, duvar yavaş
  kayar. Dokununca durur.
- Yüzde ifadesi ve sonuç vaadi yok (FAZ L §6).

### Dalga 4 — İnce işçilik (fark yaratan detaylar)

- Bölüm geçişlerinde ince pembe-altın “ışık çizgisi” ayraçları.
- Masaüstünde koyu bölümlerde imleci izleyen çok hafif pembe ışık halesi
  (yalnız `pointer: fine`, A kademesi).
- Altın CTA'larda parıltı yalnız görünür olduklarında, en fazla bir kez.
- Mobil sayfa boyu hedefi: **≤ 8.500 px** (bugün 10.481 px). Fazla iç
  boşluklar kısalır; hiçbir eski metin silinmez, “Detaylı bilgi” altında
  kalır.

### Alt sayfalara yayılım

Aynı bileşenler her alt sayfanın kendi vurgusuyla çalışır (FAZ L §3):

- `/erkek-lazer-epilasyon`: erkek line-art figürü, grafit ve gül altını.
- `/yuz-lazer`: hero altında doğrudan yüz yakın planı; Plan kartı 4–6 hafta.
- `/hassas-cilt-lazer`: Plan kartına cilt tonu satırı eklenir (sağlık verisi
  sorulmaz).
- `/bolgesel-lazer`: 15 dakikalık bölgeler, tek dokunuşla Plan kartı.
- `/lazer-epilasyon-fiyatlari-ankara`: menüdeki “+ Ekle” ile Plan kartı
  aynı kartı besler.

## 3. Yapılmayacaklar (değişmez)

- Sahte önce/sonra, stok görsel, fiyat rakamı, sonuç garantisi, “acısız”,
  “kalıcı”, “en iyi”, yüzde ifadesi.
- Geri sayım, sahte kıtlık, popup.
- Ses.
- Yeni Artifact. Yayın yalnız
  <https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM> adresine.
- Sahip onayı olmadan canlı `--apply`.

## 4. Sıra (10-07 güncel; ayrıntı §7)

1. ~~Dalga 1~~ ✓ · ~~Dalga 2~~ ✓
2. **Adım A — Artifact v4:** Dalga 1–2'yi aynı URL'de yayınla → sahip
   telefonda bakar.
3. **Adım B — Dalga 3** → Artifact v5.
4. **Adım C — Dalga 4 + alt sayfa kimlikleri** → Artifact v6 → sahibin son
   onayı.
5. **Adım D — Canlı yama:** `build.py --out` + `--check` → sahip `--apply`
   → TagCtx kapıları → 7./28. gün ölçümü.

## 5. Kabul kapıları

FAZ L §7'ye ek olarak:

- **5 saniye testi:** hero'da ilk 5 saniyede ne olduğu (lazer epilasyon,
  Konutkent, gerçek salon, WhatsApp) anlaşılıyor.
- **Üç an testi:** ışık açılışı oynuyor; haritada dokunuş efekti var; Plan
  kartı doğru aralık ve ayları gösteriyor (yüz 4–6, vücut 6–8 hafta).
- Takvim/Plan kartında 320 / 390 / 430 / 1400 px'te metin çakışması 0.
- JS hatası 0, yatay taşma 0, CLS ≤ 0,05, LCP ≤ 2,5 sn (mobil lab).
- İlk ekran ≤ 180 KB; sayfa ≤ 1,5 MB; C kademesinde ≤ 0,4 MB.
- Her yeni buton `data-track-label="at-<sayfa>-<yer>"` taşır. Yeni yerler:
  `plan-wa`, `plan-gun`, `plan-baslangic`, `yorum-konu`, `film-ac`.
  WhatsApp/telefon gerçek `<a href>`.
- Site koduna dokunulduğunda `TAGCTX_RUNBOOK.md`: `audit --record`, `diff`,
  runtime `verify`, `patches/verify_tags.sh`.

## 6. Sahibin kararları

Karara bağlananlar (10-07):

1. Merkez sayfa hero'su: **video (`lazer-film-jel`)**. Uygulandı.
2. Rozet: **yalnız CRM'deki 4 bitiş garantili paket** (ve fiyat menüsündeki
   garantili kalemler). Uygulandı.

Açık olanlar:

3. Yeni çekim (isteğe bağlı, en büyük “vay” kaynağı): 6–8 sn'lik dikey,
   ağır çekim yakın plan “pembe ışık” videosu ve cihaz ekranının temiz bir
   fotoğrafı. Masaüstü hero'daki 720p yumuşaklığını da çözer. Plan bu
   olmadan da çalışır.
4. 6. video (`lazer-film-kol`, IG 18101999296585006): sunucuda işlensin mi?
5. Canlı yama dosyalarına erişim (§7, Adım D0).

## 7. Kalan adımlar — ayrıntılı plan (10-07)

### Ölçülen yeni gerçekler (planı değiştiren)

- **Yayındaki Artifact v3'ten ileride.** Sürüm `1791383911-8f6e`: 291 dosya,
  `index.html` 459 KB. Depodaki `artifact-v3.html` 205 KB. Bölüm bölüm
  karşılaştırma:
  - `lazer`, `kirpik`, `lifting`, `pmu`, `cilt`: v3 ile **birebir aynı**.
  - `tirnak`: 4 KB → 139 KB (Claude içinde büyük geliştirme yapılmış).
  - `salon` ve `kas`: küçük farklar.

  Sonuç: v4 derlemesi **depodaki v3'ten değil, yayındaki sürümden**
  yapılmalı; yoksa tırnak çalışması silinir.
- **Dosya bütçesi sorun değil.** Artifact sınırı sürüm başına 511 dosya,
  yayın başına 255 dosya. Lazer için 24 yeni dosya gerekiyor (≈ 6,4 MB):
  5 video + 5 poster + 14 görsel. Toplam 315 dosya olur. FAZ L §4'teki
  sprite paketleme ve “tek boyut” kısıtı **gereksiz**; iptal.
- Artifact `bindLeadTracking` tanımlamıyor, yalnız varsa çağırıyor. Tanım
  canlı `script.js`'te; tekilleştirme davranışı orada doğrulanmalı (D2).
- Canlı yama araçları (`lp_quality_20261006.py`/`LPQ`, `firstscreen_ovl.mjs`,
  canlı 7 lazer HTML'i, `script.js`) **bu depoda yok**; yalnız sunucuda.

### Adım A — Artifact v4 (Dalga 1–2 telefonda görünsün)

| # | İş | Çıktı / kontrol |
|---|---|---|
| A1 | Yayındaki `index.html`'i depoya anlık görüntü olarak al. `AI_CONTEXT.json` ve `AI_HANDOFF.md` içindeki “son anlık görüntü v3” bilgisini güncelle. | `prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/artifact-1791383911.html` |
| A2 | `sources/atelier_lazer_20261007/a3_build.py` yaz. Girdi: A1 anlık görüntüsü. `<section data-view="lazer">` yerine merkez vitrin. 5 yeni görünüm: `lazer-fiyat`, `lazer-erkek`, `lazer-yuz`, `lazer-hassas`, `lazer-bolgesel` (`kamp` prototipte yok; merkezle aynı). | Diğer 7 bölüm **bayt bayt aynı** kalır (betik bunu doğrular ve farkta durur). |
| A3 | Bileşenler satır içine alınır: `lazer.css` + `lazer.js`. `render.page_html(key, "m/ig/", …)` aynen kullanılır, yani prototip ve canlı aynı kod. `fonts.css` alınmaz; sayfada Google Fonts Cormorant zaten var. | Tek kaynak: `render.py` + `src/`. |
| A4 | Ev sahibi kancaları (`ATLZ.mount(root, host)`): `noFetch:true` (Artifact'te `/api` yok, derleme anı süreleri), `bar` (prototipin kendi barı), `tier` (prototip panelinden kademe), `code` (prototipin W-kodu), `hideProto`. | `window.ATLZ_NOAUTO = true`; görünüm açılınca mount. |
| A5 | Yönlendirme ve menü: 6 lazer görünümü menüden ve `data-go` ile açılır. Salon karosu merkez sayfaya gider. Prototip paneline “Lazer ▸” alt seçimi. Eski lazer planlayıcısı (`lazer:{…regions…}`, “Saat de seçeyim”, örnek saatler) kaldırılır; yerine `ATLZ.plan` (gün + saat dilimi, uydurma saat yok). | Alt sayfa karoları (L11) prototip içinde görünüm değiştirir. |
| A6 | Medya: 24 dosya tek `files` yayınında. | Kırık medya referansı 0. |
| A7 | Yerel doğrulama (Playwright, yayından önce): 6 lazer görünümü + menü + davetiye, 320 / 390 / 430 / 1400 px. Dalga 2 testleri (`check2`), JS hatası 0, taşma 0. Diğer 7 görünüm için önce/sonra ekran görüntüsü karşılaştırması: fark 0. | `scratchpad` çekimleri + özet tablo plana yazılır. |
| A8 | Aynı URL'ye yayın (`label: "v4 lazer"`). Yayın öncesi yayındaki sürüm yeniden okunur; arada değişmişse önce birleştirilir. Yayından sonra geri okunur: boyut + sha + dosya listesi. | Sahibe bağlantı → **telefon onayı**. |

### Adım B — Dalga 3 (kanıt bölümleri) → Artifact v5

Sıra: W6 → W7 → W5 → W4 → yüze yakınlaşma (etkisi en yüksekten).

- **W6:** 5 video (§2 düzeltmesi). Hikâye oynatıcı `openStory` zaten var:
  ilerleme çubukları, kaydırarak sonraki video, görünür olunca sessiz
  oynatma (yalnız A kademesi). Kontrol: aynı anda en fazla 1 video yükleniyor.
- **W7:** sayaçla gelen “30 / 31” (C kademesinde doğrudan son sayı). Konu
  çipleri: Acı · Sonuç · İlgi (`yorum-konu`). İlk kart hizalı. Dokununca duran
  duvar.
- **W5:** otomatik cihaz turu: 6 nokta, 1,2 sn arayla, bir kez. Dokunuşla durur.
  `cihaz-nokta` etiketi korunur. Noktalar Dalga 1'de yerine oturdu; tur
  öncesi 390 ve 1400 px'te nokta–gösterge eşleşmesi tekrar kontrol edilir.
- **W4:** yolculuk tek sahne. Adım kartları sahnenin üstünde cam kartlar
  olarak akar; 755 / 808 / 1064 nm dokunuşu ışını o derinliğe indirir.
  Hedef bölüm boyu ≤ 1,6 ekran.
- **Yüze yakınlaşma** (Dalga 2'den kalan): başa dokununca figür → yüz
  geçişi (View Transition; desteklenmezse mevcut solma).
- Kapı: Dalga 2 testleri + yeni testler (çip süzgeci doğru yorumları
  gösteriyor; tur dokunuşla duruyor; video sayısı) → Artifact v5.

### Adım C — Dalga 4 + alt sayfa kimlikleri → Artifact v6

- Işık çizgisi ayraçları; masaüstü imleç halesi (`pointer: fine`, A
  kademesi); CTA parıltısı görünürken bir kez.
- Mobil sayfa boyu ≤ 8.500 px (bugün 10.150). Önce ölçülür, sonra bölüm bölüm
  kısaltılır; metin silinmez.
- Alt sayfalar (§2 “Alt sayfalara yayılım”): erkek grafit teması; yüzde hero
  altında yüz yakın planı; hassasta cilt tonu Plan kartına satır olarak;
  bölgeselde 15 dk şeridi → Plan kartı; fiyat menüsündeki “+ Ekle” → Plan
  kartı.
- Hız bütçesi ölçümü (Lighthouse mobil lab, yerel): LCP ≤ 2,5 sn, CLS ≤ 0,05,
  ilk ekran ≤ 180 KB, sayfa ≤ 1,5 MB, C kademesi ≤ 0,4 MB.
- Artifact v6 → **sahibin son prototip onayı.** Canlı yama bu onaydan önce
  başlamaz.

### Adım D — Canlı yama (sunucu, sahip onaylı)

| # | İş | Not |
|---|---|---|
| D0 | **Ön koşul, erişim.** Seçenek (a): sahip 7 canlı lazer HTML'ini, `script.js`'i, `lp_quality_20261006.py`'yi ve `ads-tracking.js`'i bu depoya (ya da oturuma) koyar; `build.py` burada yazılıp bu kopyalarla test edilir. Seçenek (b): `build.py` burada yazılır, `--out`/`--check` sunucuda çalıştırılır ve çıktısı geri getirilir. **Öneri: (a)**; test döngüsü burada kapanır. | Kişisel veri ve `.env` gelmez. |
| D1 | `patches/atelier_lazer_20261007/build.py`: `--out DIR`, `--check`, `--apply`, `--rollback`. FAZ L §5'teki her kural: `<head>` korunur, H1 birebir, eski bölümler “Detaylı bilgi” altında, ATELİER barı, JSON-LD görseli, `sitemap-images.xml`, `.bak-20261007-atlz`, `.gz`. | `media_ig` yamasının işaretli sayfaları atlaması da dahil. |
| D2 | `script.js` içinde `bindLeadTracking` tekrar çağrıya dayanıklı mı? Evetse dinamik çizimlerden sonra `relead()` serbest. Hayırsa yalnız ilk mount'ta çağrılır (bugünkü davranış). | Çift ölçüm riski. |
| D3 | `--check`: H1/title/meta/canonical/robots aynı; eski H2'ler duruyor; “Yaşamkent” 0; yasak ifade 0 (§3); her `a`/`button` etiketli; “LazerMech” 0. | Metin taraması. |
| D4 | Tıklama testi (ağ kapalı, `/api` 204): her WhatsApp/telefon CTA'sında 1 contact-ping (doğru `b`), 1 SGB_VISIT tap, [W-]'li href. Reddet senaryosunda dönüşüm yok. 7 sayfanın telefon + masaüstü ilk ekran çekimi. | FAZ L §7.2. |
| D5 | **Sahip çalıştırır:** `./run patches/atelier_lazer_20261007/build.py --apply` (geri alma: `--rollback`). | Onaysız uygulama yok. |
| D6 | Canlı sonrası: `./run tag_ctx.py audit --record` → `diff` (yeni kritik yok) → `verify --pages <7 sayfa>` → `patches/verify_tags.sh <7 sayfa>` → `page_health_check.sh` → `.gz` servis kontrolü. | Bu kapılar geçmeden “bitti” denmez. |
| D7 | 7. ve 28. günde `ask pages` lazer satırları (öncesi/sonrası, Wilson aralığı). TL artışı iddia edilmez; reklamlar kapalı, okuma organik ve gürültülü. | Bellek/handoff güncellenir. |

### Bağımlılıklar

A → (sahip telefon onayı) → B → C → (sahibin son onayı) → D0 → D1–D4 →
D5 (sahip) → D6 → D7. A1 her yayından önce tekrarlanır (yayındaki sürüm
Claude içinde değişmiş olabilir).
