# KİRPİK · "Bir bakışın hikâyesi": kirpik sayfalarını storytelling scroll ile bitirme (plan, 2026-10-07)

## Bağlam

Sahip, kirpik sayfalarının tamamlanmasını istiyor. Sayfalar kaydırdıkça anlatılan bir hikâye (storytelling scroll) olacak. En kaliteli fotoğraf ve videolar, en iyi düzenlemeleriyle kullanılacak.

- Hedef artifact (güncellenecek, yenisi açılmayacak): https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM
- Depodaki taban: `prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/artifact-v3.html`. Uygulamadan önce `Artifact read` ile canlı sürüm okunur. Lazer ya da PMU planı v3'ten sonra yayınlandıysa onun üstüne kurulur.
- Sitemap'teki kirpik ailesi 5 sayfadır (`NAV` → "Kirpik"):

| Canlı sayfa | Prototipte bugün | Bu planda |
|---|---|---|
| `ipek-kirpik` | `kirpik` vitrini (Bakış Stüdyosu, göz haritası, galeri) | Merkez hikâye sayfası olur |
| `kirpik-lifting` | `lifting` vitrini (slider, kıvrım çizimi, karşılaştırma) | Kendi hikâyesine dönüşür |
| `klasik-ipek-kirpik` | "mevcut sayfa ↗" (dışarı gider) | Yeni vitrin: `kirpik-klasik` |
| `mega-volume-ipek-kirpik` | "mevcut sayfa ↗" | Yeni vitrin: `kirpik-mega` |
| `ipek-kirpik-fiyatlari` | "mevcut sayfa ↗" | `#kirpik/fiyat` derin bağlantısı ve fiyat gezgini |

Bugünkü durumun eksikleri:
- Kirpik ailesinde **hiç video yok**. Manifestte 12 görsel var, 16 seçili videonun hiçbiri kirpik değil.
- `kirpik-makro-3`, ailenin en büyük ve en etkileyici makrosu (1440², mega volüm, uygulama anı). Hiçbir yerde kullanılmıyor.
- `ipek-kirpik-1…6`'nın altında "İPEK KİRPİK" altın etiket bandı ve imza duruyor.
- `ipek-kirpik-cift` slider'da kayıyor (aşağıda, 1b).
- Lifting'in tek gerçek görseli düşük çözünürlüklü.

## 1. Medya

### 1a. İnceleme yöntemi (yapıldı, tekrarlanmasın)

1. `ai_media_lookup.py` ve `media_index.json` ile 12 kirpik ve 2 still kaydı görsel açmadan listelendi.
2. 16 görüntü yarısı için piksel ölçümü yapıldı: merkez kenar varyansı (keskinlik), ortalama ve std (pozlama/kontrast), uç kırpılma yüzdesi.
3. Altın etiket bandının satırları renkle tespit edildi.
4. Yalnız 6 görsel göz ile doğrulandı: `kirpik-makro-3`, `ipek-kirpik-cift` (önce ve sonra), `ipek-kirpik-5`, `lifting-cift` (sonra), `ipek-kirpik-1`.

| slug | kaynak | merkez keskinlik | not |
|---|---|---:|---|
| kirpik-makro-1 | 1080² | 1670 | Keskin makro, temiz |
| ipek-kirpik-cift · sonra | 1350×843 | 1513 | Keskin. Etiket bandı y≈0.67–0.84, alt kirpiğin sağ yarısının üstünde |
| kirpik-makro-3 | 1440² | 1288 | **Ailenin en iyisi.** Mega volüm, göz altı bandıyla uygulama anı. Logo yazısı sağ üstte, havlu zemin üzerinde |
| ipek-kirpik-5 | 1350×1687 | 977 | Wispy bakış, kaşla birlikte çok iyi kompozisyon. Etiket ve imza y≥0.85 |
| still-kirpik | 1254² | 954 | Tepsiler ve cımbızlar (süreç sahnesi için) |
| lifting-cift · sonra | 1080×540 | 894 | Yumuşak, en çok 800 px. Büyütülmez |
| ipek-kirpik-cift · önce | 1350×843 | 880 | **Hata:** alt ~%12'de başka bir karenin şeridi var (split kesiti yanlış). Kadraj "sonra"dan daha yakın |
| kirpik-makro-2 | 1080² | 732 | Volüm yakın plan |
| kirpik-makro-4 | 1350×1688 | 601 | v3 galerisinde "Kahverengi ipek kirpik" yazıyor ama manifest alt'ı "Kirpik, yakın çekim". **Renk iddiası IG açıklamasından doğrulanmadan yazılmaz** |
| ipek-kirpik-3 / 4 / 1 / 6 / 2 | 1350×1687 | 385–207 | Tam göz ve kaş portreleri. Düşük skor alan yüzeyinden geliyor, bulanıklıktan değil. `ipek-kirpik-1` göz ile doğrulandı: net |

Etiket bandı ölçümü: `ipek-kirpik-1…5` için bant y≈0.85–0.92, imza y≈0.93–0.99. `ipek-kirpik-6` farklı sonuç verdi; kanıt sayfasında ayrıca bakılacak.

### 1b. Kadro (sayfa × medya)

| Sahne | Medya | Kullanım |
|---|---|---|
| Merkez · Perde | `kirpik-makro-3` | Kaydırmayla makrodan geri çekilme (scale 2.2 → 1) |
| Merkez · Önce | `ipek-kirpik-cift` önce (düzeltilmiş) | Sabit sahne |
| Merkez · Tel tel | **V1 video** (bulunursa), yoksa `still-kirpik` → `kirpik-makro-3` → `kirpik-makro-1` | Kaydırmaya bağlı film ya da 3 karelik sekans |
| Merkez · Uyanış | `ipek-kirpik-cift` (hizalı çift) | Işık süpürmesiyle önce→sonra. Hizalama tutmazsa yan yana diptik |
| Merkez · Üç bakış | `ipek-kirpik-4` / `-1` / `-3` (etiketsiz) | Bakış Stüdyosu, kaydırmayla adım adım |
| Merkez · Bakım | `still-urun` | Bakım randevusu bölümü |
| Klasik · Kahraman | `ipek-kirpik-4` (doğal), `ipek-kirpik-2`, `ipek-kirpik-6` | Doğal bakış hikâyesi |
| Klasik · Wispy | `ipek-kirpik-5` | Kaşla birlikte tam kompozisyon |
| Mega · Kahraman | `kirpik-makro-3` | Yelpaze açılışı |
| Mega · Yakın | `kirpik-makro-2` → `ipek-kirpik-3` (yoğun, tam göz) | Makrodan bakışa geçiş |
| Lifting · Kahraman | Kıvrım SVG'si (kaydırmaya bağlı), ardından `lifting-cift` | Gerçek sonuç çerçeveli "polaroid" olarak, tam ekran değil (düşük çözünürlük gizlenmez, büyütülmez) |
| Lifting · Aday | IG `17986864907913512` | PMU'dan "laminasyon + lifting" diye dışlanmıştı. Lifting yarısı temiz ve yeterli çözünürlükteyse `lifting-cift-2` olur |

### 1c. Videolar (sunucuda, `instagram.db` ile; `media.json` kullanılmaz)

Depoda video açıklaması yok. Bu yüzden 84 seçilmemiş videonun hiçbiri körlemesine açılmayacak.

```bash
python3 /var/www/seldagencerbeauty.com/all_api_meta/instagram_context.py --search "ipek kirpik"
python3 /var/www/seldagencerbeauty.com/all_api_meta/instagram_context.py --search "kirpik lifting"
python3 /var/www/seldagencerbeauty.com/all_api_meta/instagram_context.py --search "volüm"
```

- **Seçim ölçütü:** ≥720p, ≥8 sn kesintisiz işlem, salonun kendi işi, ekranda müzik ya da metin olmadan anlaşılır.
- **En çok 3 video** kısa listelenir. Her birinden yalnız 3 kare (%15, %50, %85) çıkarılıp bakılır.
- **Aranan hikâye anları:**
  - V1 "tel tel": cımbızla izolasyon ve uygulama, yukarıdan.
  - V2 "uyanış": göz açılış anı.
  - V3 lifting: kıvrım ya da tarama.
- Bulunamayan an, 3. bölümdeki çekim listesine gider. Bulunamazsa video varmış gibi yapılmaz; sahne fotoğraf sekansıyla kurulur.
- Sonuç, slug + IG ID + karar + gerekçe ile bu plana yazılır.

## 2. Edit reçetesi (`build_media.py`, ayrı `manifest_kirpik.json` + `--manifest`)

**Dürüstlük kuralları (PMU ve Cilt ile aynı):**
- Önce ve sonra yarılarına birebir aynı renk zinciri uygulanır.
- Yalnız "sonra"ya rötuş, cilt pürüzsüzleştirme ya da kirpik "çoğaltma" yapılmaz.
- Görsel büyütülmez.
- SG monogramı ve göz üstündeki monogram kalır. Kirpik ya da göz üstündeki hiçbir şey silinmez.
- Serbest olanlar: kırpma, hizalama, pozlama, beyaz dengesi, hafif keskinleştirme. Etiket ve imza yalnız kırpılarak temizlenir. `delogo` yalnız düz havlu ya da ten zemininde kullanılabilir.

| slug | İşlem |
|---|---|
| `ipek-kirpik-1…6` | `crop` alt sınırı y=0.84 (bant ve imza dışarıda). 4:5 pencere, göz merkezli: genişlik ≈1106, yükseklik ≈1383. Aynı dosya adlarıyla yerinde üretilir, HTML'deki `width`/`height` güncellenir. `-6` kanıtta ayrıca kontrol edilir |
| `ipek-kirpik-cift` | "Önce" yarısında alt şerit kırpılır (y≤0.88). `align` iki noktalı yapılır (iris merkezi ve iç göz köşesi). "Sonra"da bant kırpılır (y≤0.66). Uyanış sahnesi üst kirpik hattını anlatır; alt kirpik feda edilir. Çıktı tek dosya: `ipek-kirpik-cift-pair.webp` |
| `kirpik-makro-3` | Logo yazısı kirpik üstünde değil, havlu üstünde. Kırpma `[0,0.2,0.8,1.0]` (1152²) **veya** havluda `delogo`. Kanıtta ikisi karşılaştırılır. Ayrıca 9:16 mobil perde kesiti üretilir |
| `kirpik-makro-1/2/4` | Yalnız `grade:"kirpik"` |
| `lifting-cift` | Değişmez (800 sınırı). Aday `lifting-cift-2` aynı reçeteyle işlenir |
| Videolar | `trim` 6–10 sn, `stab` (elde çekimse), `denoise` (`hqdn3d`), `sharpen` (`cas`), `grade:"kirpik"`. Çıktılar: 720p H.264 döngü (<1 MB), poster ve kaydırma filmi için atlas (36 kare, 540×960, 4×3 → 3 dosya) |

`grade:"kirpik"`:
- `eq`: kontrast 1.04, doygunluk 1.00, gama 0.98.
- `unsharp`: yalnız luma, 5:5:0.6. Kirpik telini ayırır, cildi büyütmez.
- Hafif sıcak "Atelier" tonu, Cilt planındaki `colortemperature` değeriyle aynı.
- Çift yarılarına ortak uygulanır.

**Kanıt (zorunlu).** Her çift için scratchpad'de `kirpik/proof/` altında önce | sonra | %50 karışım sayfası üretilir. Her kırpmanın da önce/sonra kesiti üretilir. Hepsine tek tek bakılır. Kontrol listesi:
- Etiket kaldı mı?
- Monogram yerinde mi?
- Hizalama tutuyor mu?
- İki yarı aynı tonda mı?

**Artifact dosya bütçesi (sınır 255).** Gerçek sayı uygulama başında `Artifact list scope:"files"` ile okunur. PMU planı yaklaşık 249'a çıkarabilir.
- Kırpmalar aynı adla üretilir: +0 dosya.
- Çift dosyaları birleşir: `ipek-kirpik-cift-{once,sonra}-{480,800,1200}` 6 dosya → 1 dosya, yani −5.
- Video atlasları ve posteri: +4 ile +5.
- Lifting adayı: +1.
- Net etki yaklaşık 0 ile +1. Taşarsa kullanılmayan 480 varyantları `null` ile kaldırılır; önce başka yerde kullanılmadıkları doğrulanır.

## 3. Çekim listesi (personel, telefonla; bulunamayan anlar için)

**Teknik kurallar:**
- Güzellik modu ve filtre kapalı.
- Önce ve sonra aynı ışıkta, aynı mesafeden, aynı açıdan, sabit tutucuyla çekilir.
- Fotoğraf 4:5, en yüksek çözünürlük. Video 1080p 9:16, 10–20 sn tek çekim, yazısız ve müziksiz.
- Etiket bandı ve imza **eklenmez**; yazıyı web ekler.
- Her danışandan web kullanımı için açık rıza alınır (KVKK).

| Öncelik | Ne | Neden |
|---|---|---|
| P1 | Lifting önce/sonra, aynı açı 4:5 | Tek lifting görseli 1080×540 ve yumuşak |
| P1 | "Uyanış": uygulama bitince gözün ilk açılışı, 9:16, 5 sn | Merkez hikâyenin doruk anı |
| P1 | Tel tel uygulama, makro, yukarıdan, 15 sn | Kaydırma filmi |
| P2 | Kahverengi ipek kirpik makro | Menüde var, doğrulanmış fotoğrafı yok |
| P2 | Bakım randevusu (köpük ve tarama) | Bakım bölümü |
| P3 | B-roll: tepsiden tel alma (60 fps), yelpaze açılışı makro | Mega sahnesi |

Teslim yeri: IG'ye atılanlar kütüphaneye düşer, atılmayanlar `patches/media_kirpik_20261007/drop/` klasörüne konur.

## 4. Storytelling scroll motoru

Hepsi tek bir veri güdümlü motorla kurulur: `initStory(root)` ve sayfa başına `KIRPIK_STORY[view]` dizisi.

**Sahne yapısı:**
- Her bölüm `.st-ch` içinde bir `.st-stage` (`position:sticky; top:var(--top)`) ve 2–4 `.st-step` metin kartı taşır.
- Bölüm yüksekliği adım sayısının 100svh katıdır; mobilde en çok 300svh.

**İlerleme:**
- Tek, pasif, rAF ile kısılmış bir scroll dinleyicisi her görünür bölüm için `p∈[0,1]` hesaplar ve `--p` CSS değişkenine yazar.
- Adım değişimleri `IntersectionObserver` ile yakalanır.
- `animation-timeline: view()` destekleyen tarayıcıda yalnız CSS ile ilerletme yapılır; diğerlerinde JS'e düşülür.

**Bileşenler:**
- `zoomOut` (perde).
- `sweep`: önce→sonra ışık süpürmesi; var olan `initCompare`/`cmp-beam` yeniden kullanılır.
- `filmAtlas`: PMU planındaki `initFilmAtlas`. PMU önce yapıldıysa ondan alınır, yapılmadıysa burada kurulur ve PMU onu kullanır.
- `svgDraw`: var olan `eyeLashes` ve `curlLashes` çizimleri `p`'ye bağlanır.
- `lookSteps`: Bakış Stüdyosu adımları.

**Erişilebilirlik ve performans:**
- Kaydırma kaçırılmaz: snap kilidi ve wheel yakalama yok.
- Her sayfada "Hikâyeyi atla → Fiyatlar" bağlantısı var.
- Alt CTA çubuğu hep görünür.
- `prefers-reduced-motion` ve Kademe C: bölümler sabit, alt alta figür ve altyazı olur. Film yerine poster ve tek karşılaştırma gösterilir.
- Görseller `loading=lazy`. Yalnız perde görseli `fetchpriority=high` alır.
- Video ve atlas yalnız bölüme yaklaşınca (1 ekran önce) yüklenir.
- Mobilde LCP öğesi perde görselidir.

## 5. Sayfalar

**Ortak:**
- Sahne bölümleri siyah kadife ve altın. Bilgi bölümleri Mermer/Gece anahtarına uyar.
- Var olan `.dark-band`, `initDust`, `STORIES`, `rings`, `card()`, `openLightbox`, `PLANS` ve `REVIEWS` yeniden kullanılır.
- Metinler yalnız canlı sayfaların JSON-LD SSS'lerinden ve v3'teki onaylı metinlerden kısaltılır. Sunucuda `instagram_context.py` ile kirpik açıklamaları da okunur.
- **Yazılmayacaklar:** kalıcılık ya da dayanma süresi garantisi, "doğal kirpiğe zarar vermez" gibi sağlık iddiası, "ücretsiz görüşme".

### `kirpik` (ipek-kirpik) · merkez hikâye "Bir bakışın hikâyesi"

1. **PERDE (100svh).** `kirpik-makro-3` aşırı yakın başlar; kaydırdıkça geri çekilir ve "Tel tel." yazısı belirir.
   - Ardından H1 "Ankara İpek Kirpik" ve "Bakışınız, tek seansta." gelir.
   - Çipler: ★ 4,6 · 263 yorum (salon geneli, v3'teki gibi) | 1.200 TL'den | Bugün müsait (örnek).
   - Hikâye halkaları burada.
2. **ÖNCE.** "Her şey kendi kirpiğinizle başlar." Düzeltilmiş önce karesi sabit sahnede durur. Adımlar: göz yapısı, kirpik gücü, istenen etki (v3 "Bakış seçilir" metni).
3. **HARİTA.** Göz haritası SVG'si kaydırmayla iç köşeden dış köşeye çizilir; mm etiketleri belirir. Bakış düğmeleri kalır. "Uzunluklar örnektir" notu durur.
4. **TEL TEL.** V1 filmi kaydırmayla oynar, yoksa 3 karelik sekans (tepsi → uygulama → makro) gösterilir. Altyazı: "Gözleriniz kapalı, rahat bir koltukta uzanırsınız." CTA: "Bu bakışla saatimi seç".
5. **UYANIŞ.** Hizalı çiftte kaydırmaya bağlı altın ışık süpürmesi önceden sonraya geçer. Sonda "Basılı tutun, öncesini görün" etkileşimi var. "Bunu istiyorum →" düğmesi davetiyeyi `Referans: Uyanış · ipek kirpik` ile açar.
6. **ÜÇ BAKIŞ.** Bakış Stüdyosu sabit sahnede durur; kaydırdıkça Doğal → Dolgun → Yoğun geçer. Her birinde en yakın menü kalemi ve fiyatı görünür. Dokunarak seçim de çalışır.
7. **YOĞUNLUĞUNU SEÇ.** Üç kart: Klasik → `kirpik-klasik`, Orta volüm → merkezde kalır, Mega → `kirpik-mega`. Altta "Lifting mi, ipek kirpik mi?" bağlantısı.
8. **SÖZ.** Gerçek kirpik yorumları: Elanur İ. (2025-09, "hem özenli hem doğal") ve Derin Nehir A. (2025-08). Altta Meryem İ.'nin salon yorumundan "ipek kirpik" satırı. Daha fazla kirpik yorumu varmış gibi yapılmaz.
9. **MENÜ (`#kirpik/fiyat`).** v3'teki CRM menüsü (7 Ekim 2026), "Yeni danışan · kampanya" ve "Standart" grupları. Üstünde **fiyat gezgini**: bakış (klasik / orta / mega) × renk (siyah / kahverengi) × danışan (yeni / standart) → menüdeki tek kalem. Hesaplama değil, seçim; uydurma ara fiyat yok.
10. **BAKIM.** `still-urun`; "İpek kirpik bakım · 90 dk · 1.200 TL"; v3 SSS metni ("ne zaman geleceğinizi uzmanınız söyler").
11. **SSS ve FİNAL PERDE.** Tam ekran kadife kapanış, `kirpik-makro-1` üzerinde. Altın "Saatimi seç", WhatsApp ve telefon.

### `kirpik-klasik` (klasik-ipek-kirpik) · "Az, ama tam yerinde"

- **Perde:** etiketsiz `ipek-kirpik-4`, yavaş Ken Burns.
- **Teknik şema (SVG, "temsili şema, gerçek sonuç değil" etiketiyle).** Klasik ve volüm farkı, yalnız canlı sayfanın anlattığı kadarıyla.
- **Doğal galeri:** `ipek-kirpik-2`, `-4`, `-6`, `-5` (wispy, kaşla).
- **Fiyat:** Klasik volüm 1.200 TL (yeni danışan), Kahverengi klasik volüm 1.400 TL, Klasik ipek kirpik 1.700 TL (standart) · 120 dk.
- 3 soruluk SSS. Davetiye "Klasik" seçili açılır.

### `kirpik-mega` (mega-volume-ipek-kirpik) · "Yelpaze"

- **Perde:** `kirpik-makro-3`. Kaydırdıkça SVG yelpaze açılır ("temsili"), ardından gerçek makro gelir.
- **Makrodan bakışa:** `kirpik-makro-2` → `ipek-kirpik-3` (yoğun, tam göz).
- **Fiyat:** Mega volüm 1.700 TL (yeni danışan); kahverengi ve standart satırlar v3 menüsünden birebir alınır (standart: 150 dk, 2.200 TL).
- "Mega bana ağır gelir mi?" bölümü Orta volüme yönlendirir. Yalnız seçenek gösterilir, öneri iddiası yok.

### `lifting` (kirpik-lifting) · "Düz kirpik, yukarı bakar"

1. **Perde:** kıvrım SVG'si kaydırmaya bağlanır (ÖNCE → SONRA etiketi). Ardından gerçek `lifting-cift` polaroid çerçevede, süpürme ile gösterilir. Aday onaylanırsa `lifting-cift-2` 1/2 noktasıyla eklenir.
2. **Üç adım** (Bakarız → Kaldırırız → Sabitleriz). Sabit sahne; V3 varsa film, yoksa SVG.
3. **Karar:** var olan "Lifting mi, ipek kirpik mi?" kartları.
4. **Söz:** Zehra İ. (2026-07, "1 kere kirpik lifting").
5. **Menü:** Kirpik lifting 1.500 TL · 60 dk, Kaş laminasyonu 2.500 TL. Ardından SSS ve final perde.

### Gezinme ve ölçüm

- **`VIEWS`:** `kirpik-klasik` ve `kirpik-mega` eklenir.
- **`go()`:** `#görünüm/parametre` biçimini çözer. Bu, PMU planıyla ortak; hangisi önce yapılırsa o kurar.
- **`NAV` eşlemesi:**
  - `ipek-kirpik` → `kirpik`
  - `kirpik-lifting` → `lifting`
  - `klasik-ipek-kirpik` → `kirpik-klasik`
  - `mega-volume-ipek-kirpik` → `kirpik-mega`
  - `ipek-kirpik-fiyatlari` → `kirpik/fiyat`
- **Diğer bağlar:**
  - Ana sayfa kutuları ve prototip panelindeki "Sayfa" seçicisi güncellenir.
  - `STORIES.kirpik` listesine video halkası eklenir (video varsa).
  - `PLANS.kirpik` için klasik, orta, mega ve kahverengi alt seçenekleri eklenir.
- **WhatsApp mesajı:** `P.ref` ile "Bakış: Dolgun", "Renk: Kahverengi" ya da "Referans: Uyanış" eklenir.
- **Sayaç etiketleri:** yeni düğmelere `data-track-label="at-kirpik-…"` ya da `at-lifting-…` verilir (ASCII, en çok 48 karakter); `[W-]` kodu korunur.

## 6. Kod uygulaması

- **Çalışma klasörü:** `scratchpad/kirpik/`.
  - `index.html`: canlı Artifact'in okunmuş kopyası.
  - `kirpik_build.py`: `a2_build.py` ve `pmu_build.py` deseniyle, sayılı ve doğrulanmış `rep()` değişimleri. Kapsamı:
    - `kirpik` ve `lifting` `<section>`'larını yeniden yazar, iki yeni `<section>` ekler.
    - `/* KİRPİK hikâye */` CSS bloğunu ekler; masaüstü, Kademe C ve reduced-motion kuralları dahil.
    - JS: `initStory`, `KIRPIK_STORY`, `initPriceFinder`, rota, `NAV`, `PLANS` ve `STORIES` bağları.
  - `kirpik_pack.py`: çift ve atlas paketleme.
- **Yazmadan önce:** `artifact-design` skill'i yüklenir; kirpik ve lifting bölümlerinin bütün JS bağımlılıkları (`initLook`, `initEyemap`, `initCurl`, `GAL.kirpik`) okunur.
- **Yayın:** `Artifact publish`, `url` ile aynı artifact'e yapılır. `files` yeni dosyaları ekler, kaldırılanlara `null` verilir. `capabilities` gönderilmez.
- **Canlı site:** ayrı yama klasörü `patches/atelier_kirpik_20261007/build.py` (önce `--check`). **Açık sahip onayı olmadan `--apply` yapılmaz.**

## 7. Doğrulama

1. **Medya:** `kirpik/proof/*` sayfalarının hepsine bakılır (etiket, monogram, hizalama, aynı ton). `media_index.json` kayıtları kontrol edilir.
2. **Ekran görüntüleri** (Playwright, iPhone 13 ve 1440 masaüstü; Mermer ve Gece; Kademe A ve C):
   - Her bölümün 0 / 0,5 / 1 ilerleme hâli.
   - Uyanış süpürmesi.
   - Film.
   - Bakış Stüdyosu'nun 3 adımı.
   - Fiyat gezgininin 4 bileşimi.
   - Dört vitrin.
   - Davetiye ve WhatsApp metni.
   - `#kirpik/fiyat` derin bağlantısı.
3. **Otomatik kontroller:**
   - Yatay taşma 0.
   - Konsol hatası 0.
   - Dosya sayısı en çok 255.
   - Kırık `m/` referansı 0.
   - Etiket kuralı geçiyor.
   - Reduced-motion'da içerik tam görünüyor.
   - Kaydırma 60 fps'e yakın (Performance paneli, orta mobil profil).
4. **Duman testi:** salon, kaş, PMU ve lazer açılıyor mu?
5. **Yayın sonrası:** `Artifact read` ile sürüm ve dosya sayısı doğrulanır.
6. **Canlıya geçilirse:** `TAGCTX_RUNBOOK.md` uygulanır (`audit --record`, `diff`, runtime `verify`, `patches/verify_tags.sh`).

## 8. Dalgalar

| Dalga | İş | Bitti sayılır |
|---|---|---|
| K0 | Sunucuda `instagram.db` aramaları; ≤3 video ve `17986864907913512` kararı; bu plana yazılır | Video kararı kayıtlı |
| K1 | `manifest_kirpik.json`, edit reçetesi, kanıt sayfaları | Kanıtlar gözle onaylı |
| K2 | `initStory` motoru ve `kirpik` merkez sayfası | Mobil ve masaüstü ekran görüntüleri temiz |
| K3 | `kirpik-klasik`, `kirpik-mega`, `#kirpik/fiyat`, `lifting` | Dört vitrin ve derin bağlantılar çalışıyor |
| K4 | Doğrulama ve aynı Artifact'e yayın, okuma | Bitiş kapılarının hepsi geçti |
| K5 | Canlı yama `--check`, ardından **sahip onayıyla** `--apply` ve TagCtx | TagCtx temiz |
| Paralel | Çekim listesi P1 | Yeni medya K1 hattından geçip yer tutucunun yerine geçer |

## 9. Sahibin kararı gerekenler

1. Kirpik, önerilen sıraya (Lazer → PMU → Cilt) göre nereye girecek? Öneri: K0–K1 hemen başlar (medya, düşük risk). K2–K4, PMU yayınından sonra aynı Artifact sürümünün üstüne kurulur; böylece çakışma olmaz.
2. `kirpik-makro-4` gerçekten kahverengi ipek kirpik mi? IG açıklamasıyla doğrulanmadan galeri etiketi "Yakın çekim" olur.
3. P1 çekim günü ve KVKK rıza metni.
