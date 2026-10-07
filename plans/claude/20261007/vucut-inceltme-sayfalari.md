# VÜCUT ATÖLYESİ: vücut / incelme kategorisinin 9 sayfası (plan, 2026-10-07)

## Bağlam

Sahibin isteği: Vücut menüsündeki **bütün incelme türleri** için salonun en iyi fotoğraf ve videolarını bulmak, en iyi şekilde editlemek ve sayfaları güncelleme planını çıkarmak. Sayfalar mevcut ATELİER prototipinde (aynı Artifact: https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM) geliştirilecek. Yeni Artifact açılmayacak.

**Bugünkü durum:**
- Prototipte `NAV` içindeki "Vücut" grubunda 9 sayfa var: `bolgesel-incelme`, `slim-tone`, `g5-masaji`, `lenf-drenaj`, `emler`, `heykeltras`, `pasif-jimnastik`, `catlak-protokolu-ince-ton`, `popo-bakimi`.
- Bunların hiçbirinin vitrini (`data-view`) yok. Menüde dokununca canlı sitedeki eski sayfa yeni sekmede açılıyor ("mevcut sayfa ↗").
- Vücut medyası olarak yalnızca salon vitrinindeki "Bölgesel İncelme" kutucuğu var: `bolgesel-cift-sonra-480.webp`. Randevu sihirbazında `bolgesel` seçeneği fiyatsız "Ön görüşme" olarak duruyor.
- Manifestte vücut için **1 kayıt** vardı (`bolgesel-cift`). Bu, 9 sayfa için yetersiz olduğundan handoff protokolünün 7. adımı uygulandı: sınıflandırılmamış **74 ham video** her birinden tek küçük kareyle ön elendi, yalnızca vücut adaylarına ek kare açıldı. Sonuç `sources/media_vucut_20261007/triage_videos.tsv` dosyasında. Sonraki ajan bu 74 videoyu yeniden taramasın.
- Ham **fotoğraflar** depoda yok; yalnızca sunucudaki Instagram kütüphanesinde var. Cilt planı kütüphanede "vücut incelme çiftleri" (çoğul) olduğunu not etmiş. Bunlar sunucuda bulunacak (bkz. 7).
- Bu ortamdan canlı siteye erişilemedi (ağ politikası 403). Canlı vücut sayfalarındaki mevcut görseller denetlenemedi (bkz. 7).

**Geçerli kurallar (önceki planlardan):**
- Yalnızca gerçek salon medyası. Stok görsel, sahte önce/sonra, başka uzmana ait iş yok.
- Fiyat yalnızca CRM'den gelir. Vücut için CRM kalemi doğrulanmadıkça "Ön görüşme" CTA'sı kullanılır, fiyat uydurulmaz.
- Sonuç garantisi, "x cm incelme", "yağ yakar", "selülit yok eder" gibi iddialar yazılmaz. Dil: "görünüm", "sıkılaşmış görünüm", "kişiden kişiye değişir".
- Bir önce/sonra sonucu, sahip hangi bakımla alındığını teyit etmeden belirli bir cihaza ya da hizmete bağlanmaz.
- Yüzü görünen kareler `yuz: true` bayrağıyla işaretlenir.
- Canlı siteye açık sahip onayı olmadan uygulama yapılmaz.

---

## 0. Sahip kararları ve yayın durumu (2026-10-07, ikinci tur)

Sahip planı onayladı ve şunları söyledi:
- **"g5 o makine siyah olan"** → siyah silindir başlıklı cihaz **G5** (`vucut-roller` → `vucut-g5`).
- **"3 vücut em cihaz slim tone"** → EM sandığımız kule cihaz **Slim Tone** (`vucut-em` → `vucut-slimtone-kol`, `vucut-em-cihaz` → `vucut-slimtone-cihaz`; yüz videosu `vucut-slimtone-yuz`).
- **"işlemlerde hem slimtone hem g5 hem lenf drenaj 3 içinde"** → bölgesel incelme programı Slim Tone + G5 + lenf drenajın birlikte kullanılmasıdır; kol/göbek önce-sonrası bu üçlü programın sonucu olarak etiketlenir.
- **"sen oralara orijinal olmayanları koy, en son sunucuya geçireceğiz"** → kendi çekimi olmayan sayfalara temsilî görsel/çizim konur ("Temsilî görsel / Temsilî çizim" etiketiyle); sunucu adımları (540 px, IG başlık araması, canlı) en sona kalır.
- Yüzü kısmen görünen Slim Tone yüz videosu, sahibin 2026-10-06 tarihli genel izniyle ("en iyilerini kullan sıkıntı yok") kullanıldı.

**Yayın:** Aynı Artifact'e **sürüm 5** (`1791382773-9c80`) yayınlandı ve geri okundu (yayınlanan gövde yerel derlemeyle bayt bayt aynı).
Taban, bu sırada başka bir oturumun yayınladığı tırnak sürümüdür (`artifact-v4-tirnak.html`, 22 tırnak sayfası); vücut değişiklikleri onun üstüne birleştirildi, tırnak sayfaları korunarak test edildi.
Kaynak: `sources/atelier_vucut_20261007/` (`build.py`, `src/vucut.css`, `src/vucut.js`); anlık görüntü `prototypes/.../artifact-v5.html`.
Ekran görüntüleri: `plans/claude/20261007/vucut-sayfalar-mobil.jpg`.

| Görünüm | Canlı slug | Kahraman | Durum |
|---|---|---|---|
| `vucut` | bolgesel-incelme | kol+göbek önce/sonra kolajı (altın dikiş) + Bölge Haritası | gerçek medya |
| `slimtone` | slim-tone | Slim Tone kol videosu; cihaz + yüz başlığı ikilisi | gerçek medya |
| `g5` | g5-masaji | G5 bacak videosu | gerçek medya |
| `lenf` | lenf-drenaj | lenf giysileri videosu | gerçek medya (giyili çekim bekliyor) |
| `em` | emler | Slim Tone cihazı | temsilî görsel |
| `heykeltras` | heykeltras | G5 karesi | temsilî görsel |
| `popo` | popo-bakimi | G5 bacak videosu | temsilî görsel |
| `pasif` | pasif-jimnastik | ped yerleşimi çizimi | temsilî çizim |
| `catlak` | catlak-protokolu-ince-ton | ince çizgili silüet | temsilî çizim |

Doğrulama (yerel, Playwright, 390 px ve 1440 px): 9 vücut + salon, kaş, cilt, lazer ve 3 tırnak görünümünde yatay taşma 0, betik hatası 0; harita → WhatsApp metni (bölgeler + `[W-]`), randevu sayfası, menüde 9 vitrin, hikâye, salon kartı → hub, buton sayacı çalışıyor. Kırık referans: vücut dosyalarının 15'i de Artifact'te.

---

## 1. Medya seçimi

### 1a. Kadro (gerçek medya, "randevu aldırır" sırasıyla)

Hepsi işlendi ve `website/m/ig/` altında. Kayıtlar `media_index.json` içinde `fam: "vucut"` ile duruyor. Önizleme: `plans/claude/20261007/vucut-medya-onizleme.jpg`.

| # | slug | IG id | Ne | Rol | Uygulanan edit | Dosyalar |
|---|---|---|---|---|---|---|
| 1 | `vucut-gobek` | 18319579426235256 | Göbek önden, önce → sonra (aynı danışan, 2×2 kolajın alt çeyrekleri) | Bölgesel incelme kahramanı | Yarımlardan **aynı kutu** `[0,660,480,1050]`; ortadaki SG monogramı ve alttaki imza dışarıda kalır; ek renk ayarı yok | `-once-480`, `-sonra-480` (480×390) |
| 2 | `vucut-kol` | 18319579426235256 | Kol arkası, önce → sonra (aynı kolajın üst çeyrekleri) | Bölgesel incelme galerisi; EM teyit edilirse EM | Aynı kutu `[0,0,480,460]`, monogramın üstünde biter | `-once-480`, `-sonra-480` (480×460) |
| 3 | `vucut-g5` | 18127469881839748 | Bacak arkasında **G5** (siyah silindir başlık), yağlı ciltte; tek çekim | G5 kahramanı; temsilî: heykeltraş, popo | 0,3–10,3 sn; `hqdn3d` + `cas` + temel GRADE; 720×1280; poster 5. sn | `.mp4` 1,08 MB, `-poster` |
| 4 | `vucut-slimtone-kol` | 18194252941391360 | Kol arkasında **Slim Tone** başlığı (ekranlı gri aplikatör); arada altın işlemeli havlu | Slim Tone kahramanı, üçlü program kartı | 6,8–15,4 sn (ilk saniyelerdeki cephe çekimi atıldı); CRF 29; poster 9. sn (ekran görünür) | `.mp4` 1,13 MB, `-poster` |
| 5 | `vucut-slimtone-cihaz` | 18194252941391360 | **Slim Tone** cihazı: dokunmatik ekran, düğmeler, iki başlık | Slim Tone "cihazımız"; temsilî: EM | 4,9. sn tek kare; 4:5 kırpım `720:900:0:380` | `-480`, `-720` |
| 6 | `vucut-slimtone-yuz` | 18057972044799856 | Slim Tone başlığı yanak ve çene hattında | Slim tone kahramanı (yüz) | 3–13 sn; 4:5 kırpım `720:900:0:330` → üstteki "SELDA GENÇER BEAUTY / SLIMTONE" yazı katmanı tamamen dışarıda; yüz kısmen (göz yok) → `yuz: true` | `.mp4` 0,97 MB, `-poster` (720×900) |
| 7 | `vucut-lenf` | 18364153699186351 | Lenf drenaj (presoterapi) giysileri uygulama yatağında | Lenf drenaj kahramanı | Salon turundan 22,85–25,85 sn; 4:5 kırpım `720:900:0:90` → gömülü "Lenf Drenaj hizmeti de mevcut" alt yazısı dışarıda | `.mp4` 0,18 MB, `-poster` |
| 8 | `vucut-gobek-yan` | 17976687788747656 | Göbek yandan, önce (üst) → sonra (alt); kaynak 360p durağan kolaj videosu | Bölgesel incelme galerisi (küçük kart) | Bölünmedi: monogram dikişte göbeğin altına biniyor, kırpmak "önce" göbeğini keserdi. Tam kare, büyütülmeden 360 px; monogram ve imza yerinde | `-360` (360×636) |
| 9 | `vucut-cift-tam` | 18319579426235256 | Orijinal 2×2 kolaj, monogram ve imza yerinde | "Orijinal paylaşımı gör" lightbox'ı + IG bağlantısı | İki yarım yeniden yan yana; ek renk ayarı yok | `-480`, `-800`, `-960` |
| 10 | `vucut-cihaz-masa` | 18364153699186351 | Altın tekerlekli sehpada başlıklı bakım cihazı | **Teyitten sonra** slim tone "cihazımız" karesi | 13,9. sn; 4:5 kırpım `720:900:0:60` → alt yazı dışarıda | `-480`, `-720` |

Toplam: 10 kalem, 20 dosya, 3,6 MB.

**Kullanılmayacaklar:**
- `bolgesel-cift` sütun bölmesi (`-once/-sonra-480`): her yarımda kol ve göbek üst üste, monogramın çeyreği köşede kalıyor. Salon kutucuğu dahil yerine `vucut-gobek` / `vucut-kol` geçer.
- `17883457215458159`: LASERMACH başlığı bacakta. Lazer epilasyon, vücut incelme değil. Lazer ailesine aday.
- `18089498999286039`: gümüş eldiven ve mavi başlıkla el bakımı. Vücut sayfası değil.
- `18194252941391360` ilk 2 saniye: salon cephesi (salon ailesinde zaten var).
- Fiyatlı ya da iddialı kampanya afişleri (TSV'de `afis`).

### 1b. Sayfa × medya matrisi

Türler: **hub** = kategori sayfası · **H** = hizmet sayfası.
Durum: **tam** = gerçek süreç ya da sonuç medyası var · **ince** = yalnız ekipman ya da başka bölge · **teyit** = medya var, cihaz adı sahipten bekleniyor · **çekim** = şimdilik dürüst stand-in.

| Sayfa | Tür | Kahraman | İmza sahnesi | Galeri | Durum |
|---|---|---|---|---|---|
| bolgesel-incelme | hub | #1 `vucut-gobek` yan yana | **Bölge Haritası**: silüette bölgeye dokun → o bölgeye uygun bakımlar + WhatsApp mesajına bölge eklenir | #2, #8, #9 (lightbox); süreç: #3, #4 | **tam** |
| emler | H | #4 döngü | **Seans nasıl geçer**: cihaz #5 → havlu ve hazırlık (#4'ün havlu anı) → uygulama #4 | #2 yalnız sahip "EM ile alındı" derse | **tam** (süreç) |
| lenf-drenaj | H | #7 döngü (koyu bant) | "Odamız" + "Nasıl geçer" metin adımları | — | **ince, çekim P1** |
| slim-tone | H | #6 döngü 4:5 | Cihaz kartı #10 (yalnız teyitle) | — | **ince + teyit** (yalnız yüz uygulaması) |
| heykeltras | H | #3 (cihaz heykeltraş ise) | Süreç filmi #3 | — | **teyit** |
| g5-masaji | H | #3 yalnız cihaz G5 ise; değilse salon odası + tipografi | — | — | **teyit / çekim P1** |
| pasif-jimnastik | H | salon odası stand-in + tipografi | Ped yerleşimi SVG'si (çekim gelene kadar) | — | **çekim P1** |
| popo-bakimi | H | #3 yalnız sahip "bu başlık popo bakımında da kullanılıyor" derse; değilse stand-in | — | — | **teyit / çekim P2** |
| catlak-protokolu-ince-ton | H | tipografi + ürün/protokol adımları | — | — | **çekim P2** |

**Not:** #8'deki "önce" karesinde çatlak görünüyor, ama bu bir incelme sonucu. Çatlak sayfasında sonuç olarak **kullanılmaz**.

---

## 2. Edit reçetesi (uygulandı, `sources/media_vucut_20261007/build_vucut.py`)

**Dürüstlük kuralları (uygulandı):**
- Önce ve sonra yarımlarına **aynı kutu, aynı filtre**. "Sonra" ayrıca parlatılmaz, rötuşlanmaz, büyütülmez.
- Yarımlar `build_media.py`'de GRADE almıştı; kırpımda renk ayarı tekrarlanmadı.
- Monogram ve imza: kolajı çeyreklere bölerken dikişteki SG monogramının çeyrekleri kırpım dışında kalır. Bölünemeyen kolajlarda (#8) ve orijinal görünümde (#9) monogram ve imza yerinde durur.
- Videolardaki gömülü yazılar (Slim Tone başlığı, salon turu alt yazısı) **kırpımla** dışarıda bırakıldı, silme ya da boyama yapılmadı.
- Hizalama yok: gövde pozları farklı olduğu için önce/sonra **yan yana kart** olarak sunulur, üst üste kaydırıcıya (`.cmp`) konmaz. Kaydırıcı hizasız pozda yanıltıcı "erime" etkisi verirdi.

**Video:** `hqdn3d=1.5:1.5:6:6` (hafif zamansal gürültü azaltma) + `cas=0.25` (ince keskinlik) + temel GRADE (`eq=contrast=1.03:saturation=1.03:gamma=1.01`, ten rengi kaydırılmaz). 30 fps, H.264 high, sessiz, `+faststart`. Kahraman ≤ 1,2 MB hedefi sağlandı.

**Poster ve tek kare:** WebP q78–80, 480 ve 720 px (kaynağın üstüne çıkılmaz).

**Yeniden üretim:**
```bash
python3 sources/media_vucut_20261007/build_vucut.py              # hepsi
python3 sources/media_vucut_20261007/build_vucut.py --only vucut-g5
python3 scripts/ai_media_lookup.py search "" --family vucut --limit 10
```

**Sunucuda tam çözünürlük (V3):** #1 ve #2 yerelde 480 px'lik yarımlardan üretildi. Sunucuda IG orijinali 1080×1350. Manifestteki `server_once_box` / `server_sonra_box` değerleri `build_media.py`'nin `once_box` / `sonra_box` anahtarlarına aynen girilir → 540 px çıktı. Büyütme yok, 800 px yalnızca kaynak yeterse.

---

## 3. Çekim listesi (personel, telefonla, yarım gün)

**Teknik kurallar (vücut önce/sonrası için):**
- Yerde bant işareti, tripod 2 m mesafede ve bel yüksekliğinde. Önce ve sonra **aynı ışık** (tavan açık, pencere arkada değil), aynı açılar: önden, sol yan 90°, arkadan.
- Aynı siyah iç giyim seti. Rahat duruş, **normal nefes**: karın içe çekilmez, dışarı itilmez. Kollar her çekimde aynı konumda.
- Aynı gün saati (tercihen sabah). Güzellik modu, filtre ve rötuş **kapalı**.
- Önce, son seanstan sonra ve mümkünse 1 ay sonra çekilir.
- Süreç videosu 1080p, 9:16, 10–20 sn tek çekim, yazısız ve müziksiz. Bir çekimde cihaz ekranı görünsün. Personel eldivenli.
- Yüz kadraja girmez (çene altından kesilir). Yüz görünecekse ayrıca izin alınır.
- Her danışandan **web kullanımı için açık yazılı rıza** (KVKK).

**Teslim:** Instagram'a atılan her şey kütüphaneye kendiliğinden düşer. Atılmayanlar `google-adsAI/patches/media_vucut_20261007/drop/` klasörüne konur.

| Öncelik | Sayfa | Çekilecekler |
|---|---|---|
| P1 | g5-masaji | G5 cihazı ve başlıkları yakın plan; basen/bacak uygulaması 15 sn |
| P1 | pasif-jimnastik | Pedlerin göbek ve bacağa yerleşimi; cihaz ekranı; kas kasılması görünen 10 sn |
| P1 | lenf-drenaj | Giysiyle uzanan danışan (yüz yok); cihaz ekranı; bölmelerin sırayla dolduğu 10 sn |
| P1 | slim-tone | Vücut başlığı varsa göbek/bacak uygulaması; cihaz ekranı |
| P1 | bolgesel-incelme | Rızalı yeni önce/sonra seti (kurallara göre, 3 açı); en az biri bel/basen |
| P2 | popo-bakimi | Uygulama klibi; rızalı arkadan önce/sonra |
| P2 | catlak-protokolu-ince-ton | Aynı ışıkta, 30 cm'den çatlak yakın planı önce/sonra; ürün uygulama eli |
| P2 | heykeltras | Teyide göre cihaz ya da el tekniği klibi |
| P3 | b-roll şölen | Vücut odası geniş açı; altın logolu havlu katlama; yağın avuca dökülmesi; cihaz düğmesi ve ekran yakın planı |

---

## 4. Sayfa motoru ve sahneler (prototip)

**Veri yapısı:** Cilt planındaki `CILT_PAGES` ile aynı biçimde tek bir `VUCUT_PAGES` dizisi:
```js
{ id: "emler", nav: "EM vücut bakımı", tur: "H", durum: "tam",
  hero: { slug: "vucut-slimtone-kol", kind: "video" },
  scene: "seans",                       // "harita" | "seans" | "koyu-bant" | "tipografi"
  gallery: ["vucut-kol"],               // yalnız sahip teyidiyle
  cta: { wa: "Merhaba, EM vücut bakımı için ön görüşme almak istiyorum.", plan: "bolgesel" },
  cekim: false }                        // true → proto panelde "çekim bekliyor" rozeti
```

**Yönlendirme:** Sayfa üretildikçe `NAV` "Vücut" grubundaki kaydın 3. elemanı görünüm kimliği olur (`["emler","EM vücut bakımı","emler"]`). Böylece menü canlı siteye değil vitrine gider.

**Yeniden kullanılacak bileşenler:**
- **Bölge Haritası:** Lazer planının L2 "Vücut Haritası" silüeti (`sources/atelier_lazer_20261007/src/lazer.js`, `.lz-part`). Bölge listesi vücut için parametreleşir: kol arkası, göbek, bel/yan, basen, bacak, popo. Seçim → uygun bakım kartları + WhatsApp metnine bölge eklenir. Bölge → bakım eşlemesi sahipten gelir (bkz. 6).
- **Video kutucukları:** Mevcut `.auto-vid` / `.tile-vid` (`data-src` ile tembel yükleme, poster önce).
- **Önce/sonra:** Yeni yan yana kart: iki yarım, altta "ÖNCE · SONRA" etiketi ve "Aynı danışan · sonuç kişiden kişiye değişir" notu. `.cmp` kaydırıcısı kullanılmaz (bkz. 2).
- **CTA:** Mevcut `waHref` + `visitCode()` + `[W-]` izleme. Randevu sihirbazında `bolgesel` seçeneği "Ön görüşme" olarak kalır.

**Salon vitrini:** "Bölgesel İncelme" kutucuğu `bolgesel-cift-sonra-480.webp` yerine `vucut-gobek-sonra-480.webp` yerine G5 videosunu ("Vitrin · canlı") oynatır ve `vucut` vitrinine gider (uygulandı).

**Artifact dosya sınırı:** Vücut en çok 20 dosya ekler. Lazer, PMU ve Cilt ile birlikte toplam 255 sınırı derlemeden önce sayılır.

---

## 5. Dalgalar

| Dalga | İçerik | Yayın |
|---|---|---|
| **V0** (bu çalışma, **tamam**) | Ham video ön elemesi (74), medya v1 (10 kalem / 20 dosya), `build_vucut.py`, `manifest_vucut.json`, `triage_videos.tsv`, `ai_media_lookup.py` vücut desteği, bu plan | Depo |
| **V1** (**tamam**, sürüm 5) | Sayfa motoru + gerçek medyalı 4 sayfa: `bolgesel-incelme` (hub, Bölge Haritası), `emler`, `lenf-drenaj`, `slim-tone`; salon kutucuğu güncellemesi | Aynı Artifact |
| **V2** (**tamam**, sürüm 5; temsilî görsel/çizimle) | Kalan 5 sayfa: teyide göre `heykeltras` / `g5-masaji` / `popo-bakimi` (#3 ile ya da stand-in), `pasif-jimnastik` ve `catlak` dürüst stand-in + "çekim bekliyor" rozeti | Aynı Artifact |
| **V3** | Sunucu adımları (bkz. 7) + çekimler geldikçe yalnız `manifest_vucut.json` güncellenir → yeniden derle → yayınla | Aynı Artifact |
| Canlı | Sahip onayı + dry-run / `--check`; onaysız `--apply` yok | Canlı site |

Önerilen genel sıra: **Lazer → PMU → Cilt Atlası → Vücut**. V1, Lazer'in Vücut Haritası bileşenini kullandığı için Lazer'den sonra gelmeli. Vücut V1 küçük (4 sayfa) olduğundan Cilt D1 ile paralel de yürüyebilir.

---

## 6. Sahibe sorulacaklar

Yanıtlananlar (2026-10-07): 1 (siyah başlık = G5), 3 (sonuç = Slim Tone + G5 + lenf drenaj programı), 6 (genel izin 2026-10-06). Açık kalanlar: 2, 4, 5, 7, 8 ve **EM vücut bakımı Slim Tone ile aynı cihaz mı?**

1. `vucut-roller`'daki siyah silindir başlıklı cihazın adı ne: G5 mi, vakumlu roller mı, heykeltraş mı? Hangi sayfalarda gösterilebilir (G5, heykeltraş, popo)?
2. Sehpadaki cihaz (`vucut-cihaz-masa`) Slim Tone mu? Slim Tone vücutta da uygulanıyor mu?
3. Kol ve göbek önce/sonrası (`18319579426235256`) hangi bakım ya da protokolle alındı? Kaç seans? Sayfada yalnız teyit edilen hizmete bağlanır; seans sayısı yalnız sahip verirse yazılır.
4. Heykeltraş ve pasif jimnastik salonda hangi cihaz ya da yöntemle yapılıyor?
5. CRM'de vücut kalemleri ve fiyatları var mı? Yoksa bütün vücut sayfaları "Ön görüşme" CTA'sıyla kalır.
6. Slim Tone videosunda danışanın yüzü kısmen görünüyor (yanak, dudak; göz yok). Web kullanımı için rıza var mı?
7. Çatlak protokolü "İnce Ton": ürün adı ve adım sırası.
8. Bölge Haritası için bölge → bakım eşlemesi (örn. kol arkası → EM; basen → roller/G5; bacak şişkinliği → lenf drenaj).

---

## 7. Sunucuda yapılacaklar (bu ortamdan erişilemedi)

1. **Kütüphane araması** (görsel açmadan, yalnız başlıklarla):
   ```bash
   cd /var/www/seldagencerbeauty.com/all_api_meta
   for q in "incelme" "bölgesel" "vücut" "g5" "lenf" "drenaj" "presoterapi" "selülit" "slim" "em " "heykeltraş" "pasif jimnastik" "çatlak" "popo" "basen" "sıkılaş"; do
     python3 instagram_context.py --search "$q"
   done
   ```
   Çıkan yeni kimlikler `manifest_vucut.json`'a aday olarak yazılır. En fazla 3–6 görsel açılarak doğrulanır. Özellikle `17976687788747656` kolaj videosunun **görsel sürümü** (aynı gün, 2025-07-30/31 paylaşımları) ve cilt planının andığı diğer "vücut incelme çiftleri" aranır.
2. **Tam çözünürlük:** #1 ve #2 için `build_media.py` manifestine `once_box` / `sonra_box` kayıtları (değerler `manifest_vucut.json`'da) → 540 px yarımlar.
3. **Canlı sayfa denetimi:** 9 canlı vücut sayfasındaki görseller listelenir (tekrar eden, stok, katalog, yanlış alt metin). Bulgular bu planın 8. bölümüne yazılır. Düzeltme ayrı onayla yapılır.

---

## 8. Canlı sitede bulunan hatalar

_(Sunucu denetiminden sonra doldurulacak; bu ortamdan canlı siteye erişim 403.)_

---

## 9. Doğrulama ("tamamlandı" demeden önce)

Handoff'taki ortak kapılar:
- Aynı Artifact URL'sine yayınlandı ve yayınlanan sürüm tekrar okundu.
- Kırık medya referansı 0, tarayıcı konsol hatası 0, mobil yatay taşma 0.
- Mobil ve masaüstü ekran görüntüleri kontrol edildi.
- WhatsApp/telefon CTA ve `[W-]` izleme doğrulandı.
- Artifact dosya sınırı aşılmadı.
- Canlı için dry-run/`--check`; açık onaysız `--apply` yok.

Vücuda özel kapılar:
- Her önce/sonra kartında "aynı danışan" ve "sonuç kişiden kişiye değişir" notu var. Kart, sahip teyidi olmadan bir cihaza ya da hizmete bağlanmamış.
- "Garanti", "x cm", "yağ yakar", "selülit yok eder" gibi ifadeler sayfa metinlerinde yok (`rg -i 'garanti|cm incel|yağ yak|yok eder'`).
- Teyit bekleyen medya (`vucut-cihaz-masa`) yayında değil. Heykeltraş, popo ve EM sayfalarındaki G5/Slim Tone görselleri "Temsilî görsel" etiketli.
- `yuz: true` kayıtlar (`vucut-slimtone`) için rıza notu var.
- Videolar poster önce yüklüyor (`preload="none"` + `data-src`), kahraman ≤ 1,2 MB.
- `python3 scripts/ai_media_lookup.py search "" --family vucut` 10 kayıt döndürüyor; `media_index.json`'daki her `vucut-*` dosyası diskte var.
