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

**W6 · Salonumuzda çekildi: 6 video, hikâye oynatıcısı**
- Şerit 2 videodan 6 videoya çıkar: jel, çene, bacak, bacak2, kol, yüz.
  Hepsi FAZ L'de seçilmiş, işlenmiş ve `website/m/ig/` altında hazır.
- Görünen video sessiz oynar; dokununca tam ekran Instagram tarzı hikâye
  açılır (üstte ilerleme çubukları, kaydırarak sonraki video).
- Videolar yalnız görünürken yüklenir; C kademesinde poster.

**W7 · Yorumlar canlansın**
- “30 / 31” bölüm görününce 0'dan sayarak gelir.
- Konu çipleri: Acı · Sonuç · İlgi · Hijyen. Bunlar yalnız kelimesi
  kelimesine yorum metninde geçen sözcüklerle süzer.
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

## 4. Sıra

1. Dalga 1 düzeltmeleri → yerel çekimle doğrula.
2. Dalga 2 (W1–W3) → yerel çekim → **sahibe telefonda gösterilir.**
3. Dalga 3–4.
4. FAZ L §4: `a3_build.py` ile Artifact v4 derlenir ve aynı URL'ye yayınlanır;
   yayınlanan sürüm geri okunur.
5. FAZ L §5: canlı yama `build.py --out` + `--check`.
6. Sahip `--apply` çalıştırır; ardından TagCtx kapıları.

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

## 6. Sahibin kararı gereken konular

1. Merkez sayfa hero'su: **video (`lazer-film-jel`) önerilir**; fotoğrafta
   kalmak da mümkün.
2. Yeni çekim (isteğe bağlı, en büyük “vay” kaynağı): 6–8 sn'lik dikey,
   ağır çekim yakın plan “pembe ışık” videosu ve cihaz ekranının temiz bir
   fotoğrafı. Çekim günü planına eklenebilir; plan bu olmadan da çalışır.
3. Plan kartında “bitiş garantili paket seçeneği” rozeti hangi bölgelerde
   görünsün? CRM'deki 4 kalemle sınırlı tutulması önerilir.
