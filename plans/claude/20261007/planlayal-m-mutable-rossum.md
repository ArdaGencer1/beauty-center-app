# CİLT ATLASI: cilt kategorisinin 25 sayfası, görsel şölen (plan, 2026-10-07)

## Bağlam

Sahip, cilt bakımı kategorisinin **bütün sayfalarının** ATELİER prototipinde (https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM, v3) tamamlanmasını istiyor. Ölçüt: en iyi fotoğraf ve videolar, en iyi edit, en çok randevu, "tam şölen".

**Bugünkü durum:**
- Prototipte cilt için **tek vitrin** var (`cilt-bakimi`). Menüdeki diğer 24 cilt sayfasına dokununca canlı sitedeki eski sayfa yeni sekmede açılıyor.
- Instagram kütüphanesinin 399 öğesi baştan incelendi. Salona ait gerçek cilt medyası **14 sayfaya** yetiyor. **11 sayfada** hiç gerçek medya yok: hollywood, paris ışıltısı, dermabrazyon, antioksidan, dudak bakımı, sıkı görünüm, kararma, sırt, koltuk altı, dirsek ve fiyatlar. Leke ve hassas cilt de çok zayıf.
- Canlı sayfalardaki görseller zayıf:
  - Aynı darsonval fotoğrafı 13 sayfada tekrar ediyor.
  - 7 sayfada hiç içerik görseli yok.
  - Akne sayfasındaki 4 görsel Dermaplus katalog ekran görüntüsü.

**Sahip kararları (10-07):**
1. **Yalnızca gerçek salon medyası** kullanılacak. Prototipteki 7 şüpheli kare çıkıyor (bkz. 1a).
2. Medyası olmayan sayfalar için **personel çekimi yapılacak** (çekim listesi, bkz. 3). Çekim gelene kadar bu sayfalarda salonun gerçek odası, cihazı, LED kubbesi ve ürün kareleri durur. Sahte önce/sonra konmaz.

**Önceki kararlar geçerli:**
- İlk ekranda "…TL'den" fiyat gösterilir.
- Fiyatlar yalnızca CRM'den gelir. 5 seanslık paket, tek seans fiyatının 4,5 katıdır.
- Yüzü görünen kareler kullanılabilir (`yuz: true` bayrağı).
- Fiyat ya da iddia içeren afişler kullanılmaz.
- TL artışı vaat edilmez.

---

## 1. Medya seçimi (işin en önemli kısmı)

### 1a. Prototipten çıkanlar

| slug (IG id) | Neden |
|---|---|
| cilt-yarim-1 (17951646918167938) | Tek fotoğraf ortadan bölünmüş, "önce" yanağında yapay doku, gri stüdyo fonu. **Şu anki cilt kahramanı.** |
| cilt-yarim-2 (17909854857222461) | Tek fotoğraf bölünmüş; burun ve dudak dikişte kesintisiz, bir yarısı rötuşlu |
| cilt-cift-2 (18016986917719157) | 17945921837942670 ile aynı danışan, önce ve sonra **ters**; sonuç da daha zayıf |
| cilt-cift-3 (18086010650107298) | Klinik düzeyde melazma temizliği; büyük olasılıkla stok görsel |
| cilt-cift-4 (17987084615917224) | Yumuşak, büyütülmüş web görseli |
| cilt-cift-5 (18091846780704413) | "Sonra" daha kırmızı, cerrahi bone, yumuşak |
| cilt-islem (18394257022142297) | Stok tarzı köpük maske karesi |
| cilt-video-2 (18084203987184570) | 0,4 saniyede bir kesilen zayıf montaj |

### 1b. Kadro (gerçek medya, "randevu aldırır" sırasıyla)

Yollar `all_api_meta/instagram_library/media/` altında.

| # | IG id | Ne | Rol | Edit reçetesi |
|---|---|---|---|---|
| 1 | 18063357971188976 (1440×1800) | **Gerçek yarım yüz**: iki ayrı fotoğraf, dikişte hafif kayma; mat ve kızarık → aydınlık ve eşit | Hub kahramanı, yüz bakımı, yenileme, ton | 4:5; ışık süpürmesi ve dikiş çizgisi HTML'de; iki yarıya aynı renk ayarı |
| 2 | 18029533706831317 (1350×1687) | Akne, iltihaplı → sakin; farklı kıyafet, gerçek | Akne kahramanı | Üst/alt bölme; alttaki "CİLT BAKIMI" etiketi kırpılır |
| 3 | 17945921837942670 (1080×1350) | Sol/sağ, mat → nemli ışıltı (yeşil sweatshirt "sonra") | Yenileme, ton, hydra sonucu | Sol/sağ bölme → `.cmp` kaydırıcı; yarımlar hizalanır |
| 4 | 17913554493238260 (1350×1688) | Siyah nokta → ışıltı; burun pembe; en keskin kare | Klasik, temizlik | Üst/alt; altyazı: "bakımdan hemen sonra, kızarıklık kısa sürede geçer" |
| 5 | 17884915872588889 (1252×1669) | **Cilt odası**: siyah yatak, altın logolu havlu, Space Oxygen, altın lavabolar | Fiyatlar kahramanı, stand-in | Ken Burns klibi (yavaş yaklaşma), 4:5 ve 9:16 |
| 6 | 18617996404000518 (video, 15,6 sn) | LED kubbe renk döngüsü, yazısız | Hub filmi, LED bölümleri | 0–8 sn kesintisiz döngü; mevcut 59 kare korunur |
| 7 | 17894387157352959 (1448×1931) | Space Oxygen: 8 başlık, LED kubbe, altın halkalı ayna | Dermabrazyon, hydra, ışıltı stand-in'i | "8 başlık" etkileşimli noktaları; 4:5 kırpım |
| 8 | 18133083652567287 (1254²) | Salondaki Dermaplus Premium ürün rafı | Akne, klasik, antioksidan stand-in'i | Kare ve 4:5 |
| 9 | 18025275239906179 (video, 10 sn) | Darsonval: turuncu ışıyan elektrot akneli yanakta | Akne koyu bandı | Tam tek çekim döngü; hafif gürültü azaltma |
| 10 | 18119195767718567 (video, 20,9 sn) | LED kubbe üzerinde elde çekim | Kaydırmalı film (hub, klasik) | 5–17 sn; `vidstab`; 60 kare; poster 10. sn |
| 11 | 17937892356335721 | Şiddetli akne → hafif kızarıklık | Akne galerisi | Üst/alt |
| 12 | 18161360971378712 | Göz çevresi: kaz ayağı ve matlık → daha düz | Göz çevresi kahramanı, anti-aging | Üst/alt |
| 13 | 18093388681773950 | Erkek şakak, arkada salon cihazı | Anti-aging, hub ("erkekler de") | Üst/alt |
| 14 | 18474224356105485 | Burun gözenekleri, aynı seans | Temizlik | Üst/alt |
| 15 | 17981341748700067 | Afişin içinden burun siyah nokta çifti, aynı kırmızı iz | Temizlik "gözenek lupu" | Panel kırpımı: x197–727 ve x731–1262, y410–1252 |
| 16 | 18192437785391754 (video) | Saten yüz germe başlığı kaş ve göz üzerinde | Saten ve sıkı görünüm kahramanı | 1,6–6,6 sn döngü + kaydırma filmi |
| 17 | 18122366353896732 (video) | Büyüteç altında cilt analizi | Cilt analizi kahramanı | 3,2–5,7 sn döngü |
| 18 | 18117918322774135 | Sıcak ışıklı oda köşesi, buhar makinesi, altın tepsi | Hassas cilt, hub atmosfer | 4:5 |
| 19 | 17853340245501601 | Siyah eldivenli eller jelli yüzde kalp yapıyor | Hub "duygu" karesi, yüz bakımı | 4:5 |
| 20 | 18070742126031547 (720×900) | Temizleme köpüğü yakın plan | Klasik zaman çizelgesi adımı | Yalnız 480/720 (büyütme yok) |
| 21 | 18039236768821035 | Ters tam yüz, kızarıklık → daha eşit | Yüz bakımı galerisi | Sol/sağ; 180° döndürme |
| 22 | 18048110567578365 | Olgun cilt, leke ve kırışıklık → nem | Anti-aging (zayıf) | Üst/alt |
| 23 | 18088219433120497 / 18085487912411515 (video) | Komedon çıkarma | Temizlik ve klasik adım klibi | En fazla 2 sn'lik tek parça |

**Kullanılmayacaklar:**
- Fiyat ya da iddia içeren afişler ve yazılı videolar (18125536198504862 hydra başlığı tüm süre yazılı vb.).
- 360p klipler.
- Kalıcı makyaj dudak çiftleri: dudak bakımı ayrı hizmet, etiket yanıltır.
- Lazer koltuk altı karesi.
- Vücut incelme çiftleri.

### 1c. Sayfa × medya matrisi

Türler:
- **H** = kendi CRM kalemi olan hizmet sayfası.
- **İ** = ihtiyaç rehberi. Kendi kalemi yok; gerçek bakımlara yönlendirir ve **fiyatı ödünç gösterilmez**.

Durum değerleri: **tam** = gerçek sonuç kanıtı var · **ince** = zayıf · **çekim** = şimdilik stand-in.

| Sayfa | Tür | Kahraman | İmza sahnesi | Galeri | Durum |
|---|---|---|---|---|---|
| cilt-bakimi | hub | #1 yarım yüz (seçenekler: LED döngüsü #6, oda #5) | Cilt Atlası + test + LED filmi #10 | #3, #2, #4, #13 | tam |
| cilt-bakimi-fiyatlari | hub | #5 oda, Ken Burns | Bakım Menüsü (süre ve ihtiyaç süzgeci, paket hesabı) | — | tam (çekim: geniş oda) |
| klasik-cilt-bakimi | H 2.000/90 | #4 | **90 Dakika** zaman çizelgesi: #17 → #20 → #23 → LED #6 → #4 | #14 | tam |
| cilt-temizligi | H 1.000/30 | #15 | **Gözenek Lupu** (parmakla gezdirilen daire içinde "sonra") | #14, #4 | tam |
| akne-bakimi | H 5.000/120 | #2 | Darsonval koyu bandı #9 | #11 | tam |
| cilt-yenileme | H 6.000/120 + hücresel | #3 kaydırıcı | Bölge seçici (1/2/3 bölge → 3.500/4.000/6.000) | #1, #21 | tam |
| ton-esitleme | H 4.500/5.500/6.500 | #3 / #1 | Alan boyu seçici | — | tam |
| saten-yuz-germe | H 4.500/60 | #16 döngü | Kaydırmalı film #16 | — | tam |
| anti-aging-bakimi | İ | #12 | Yol seçici (saten · hücresel) | #13, #22, #16 | tam |
| goz-cevresi-bakimi | İ | #12 | — | — | ince |
| cilt-analizi | İ (ön görüşme) | #17 döngü | **Yüz Haritası** (bölgeye dokun → ihtiyaç → sayfa önerisi) | — | tam |
| yuz-bakimi | İ | #1 | "Yüzünüz için 4 yol" seçici | #3, #21, #19 | tam |
| leke-bakimi | H 5.500/120 | stand-in #5 + ton kanıtı #3 ("ton eşitleme sonrası" diye etiketli) | — | — | **ince, çekim P1** |
| hollywood-bakimi | H 5.500/120 | stand-in #7 + LED #6 | **Işıltı Düellosu** (Paris ile karşılaştırma kartı) | — | **çekim P1** |
| paris-isiltisi-bakimi | H 4.500/120 | stand-in #7 + LED #6 | Işıltı Düellosu | — | **çekim P1** |
| dermabrazyon | H 6.500/90 | #7 | **8 Başlık** noktaları | — | **çekim P1** |
| hydra-elite | İ | #7 | 8 Başlık | #3 | ince |
| hassas-cilt | İ | #18 | nazik yol (temizlik · LED) | — | ince |
| antioksidan-bakimi | İ | #8 | — | — | **çekim** |
| dudak-bakimi | H 1.000/1.500/2.000 | tipografik + dudak SVG | 3 seviye kartı (3 seanslık paketler) | — | **çekim** |
| cilt-inceltme | İ (saten kopyası) | #16 | saten ve hücresel yönlendirme | — | tam (saten'den) |
| cilt-kararma-bakimi | İ (ton kopyası) | stand-in #8 | AHA protokolü adımları | — | **çekim** |
| sirt-bakimi | H 3.500/6.500/7.000 | stand-in #5 + sırt SVG | Yarım / tam sırt seçici | — | **çekim** |
| koltuk-alti-bakimi | H 4.500/30 | stand-in #5 | — | — | **çekim** |
| dirsek-bakimi | İ | stand-in #5 | — | — | **çekim** |

---

## 2. Edit reçetesi (`build_media.py` v2)

**Dürüstlük kuralları:**
- Önce ve sonra yarımlarına **aynı** filtre zinciri uygulanır. "Sonra" asla ayrıca parlatılmaz, rötuşlanmaz.
- Görsel büyütülmez.
- SG monogramı ve imza kalır.
- Köşedeki "CİLT BAKIMI" etiketi kırpılabiliyorsa kırpılır.

**Yeni manifest anahtarları** (ayrı `manifest_cilt.json` ve `--manifest` bayrağı; mevcut 88 öğenin çıktısı değişmez):

| Anahtar | Ne yapar |
|---|---|
| `crop` | `iw/ih` ifadesi; `webp_set`'e zaten bağlanabiliyor |
| `rotate` | 0/90/180/270 |
| `grade` | Öğe bazında renk ayarı: hafif sıcak "Atelier" tonu (`colortemperature` + `curves`). Çiftin iki yarısına ortak uygulanır |
| `align` | `{dx, dy, s}` ile "sonra" yarımını "önce"ye hizalar; kaydırıcıda yüz kaymaz |
| `denoise` | Telefon videosu için `hqdn3d` |
| `sharpen` | `cas` |
| `stab` | `vidstabdetect` + `vidstabtransform` (elde çekim #10) |
| `loop` | `seamless` ya da `boomerang` (`reverse` + `concat`) |
| `poster_t` | Poster karesinin saniyesi |
| `kenburns` | `zoompan` ile 6 sn'lik 9:16 ve 4:5 klip, 1,5 MB altında |
| `reveal` | `xfade wipeleft` ile önce→sonra hikâye klibi, altın dikiş çizgisiyle |
| `file` | IG dışı kaynak (çekim klasörü) |

**Çıktılar:**
- 480/800/1200 WebP.
- 720p H.264 döngüler: kahraman 1,2 MB altı, diğerleri 0,8 MB altı.
- Film kareleri 540w q60: #10 ve #16, 60'ar kare.
- Posterler.
- `contact_<sayfa>.jpg` iletişim sayfaları (`ffmpeg tile`). Her sayfanın medyası tek bakışta kontrol edilir.

---

## 3. Çekim listesi (personel, telefonla, yarım gün)

**Teknik kurallar:**
- Telefon tutucu sabit bir işarette durur. Önce ve sonra aynı ışık (tavan açık, büyüteç lambası kapalı), aynı mesafe ve aynı açıyla çekilir: önden, sol 45°, sağ 45°.
- Güzellik modu ve filtre **kapalı**. Makyaj yok, saç altın logolu havluyla geride.
- Önce, hemen sonra ve mümkünse 1 hafta sonra çekilir.
- Fotoğraf 4:5 ve en yüksek çözünürlükte. Video 1080p, 9:16, 10–20 sn tek çekim, yazısız ve müziksiz (yazıyı biz ekleriz).
- Her danışandan **web kullanımı için açık rıza** alınır (KVKK).

**Teslim:** Instagram'a atılan her şey kütüphaneye kendiliğinden düşer. Atılmayanlar `google-adsAI/patches/media_cilt_20261007/drop/` klasörüne konur.

| Öncelik | Sayfa | Çekilecekler |
|---|---|---|
| P1 | leke-bakimi (aramada en çok talep alan 2. cilt konusu, ayda ~110) | Leke yakın planı önce/sonra; uygulama klibi |
| P1 | dermabrazyon, hydra-elite | Space Oxygen başlığı çalışırken 10 sn (su ve vakum görünsün); **tanka toplanan kirin** "sonra" karesi |
| P1 | hollywood, paris | Maske ve LED uygulama klibi; yandan ışıkla "ışıltı" sonrası yanak |
| P1 | hepsi | **Cilt uzmanı portresi** (yorumlarda adı geçen Buğlem Hanım, izin alınırsa), cilt odasında |
| P2 | sırt, koltuk altı, dirsek, kararma | Bölge önce/sonra (rızalı); uygulama eli |
| P2 | antioksidan, dudak | Serum ve ampul uygulama yakın planı; dudak maske ve peeling önce/sonra |
| P2 | hassas-cilt | Kırmızı LED altında sakin cilt; nazik uygulama |
| P3 | b-roll şölen | 60 fps yükselen buhar, altın lavaboya dökülen su, havlu katlama, LED kubbe yandan döngü, oda geniş açı (altın saat) |

---

## 4. Sayfa motoru ve sahneler (prototip)

_(Plan ajanının mimari önerisiyle doldurulacak: `CILT_PAGES` veri yapısı, yönlendirme, global kimlik çakışmaları, yeni bileşenler.)_

---

## 5. Dalgalar

| Dalga | İçerik | Yayın |
|---|---|---|
| **D1** | Medya v2 (bölüm 1–2), sayfa motoru, hub yenilemesi + gerçek medyası olan 11 sayfa: fiyatlar, klasik, temizlik, akne, yenileme, ton, saten, anti-aging, göz çevresi, analiz, yüz bakımı | Aynı artifact |
| **D2** | Kalan 13 sayfa, dürüst stand-in ve tipografik/SVG sahnelerle. Proto panelde "çekim bekliyor" rozeti | Aynı artifact |
| **D3** | Çekim gelince yalnızca `manifest_cilt.json` güncellenir, sonra yeniden derlenip yayınlanır | Aynı artifact |

**Sahibe sorulacak içerik bilgileri** (D1'i bekletmez, ilgili sahnede yer tutucu kalır):
1. Hollywood ile Paris arasındaki gerçek fark (ürün ve adım).
2. Klasik bakımın adım sırası.
3. Space Oxygen'in hangi başlığı hangi bakımda kullanılıyor.
4. Hydra Elite CRM'de hangi kaleme denk geliyor.
5. Uzman adı ve portre izni.

---

## 6. Canlı sitede bulunan hatalar (bu planın dışında; ayrı onay ve sahip uygular)

1. `cilt-inceltme.html` ziyaretçiye iç şablon metni gösteriyor ("Landing page kalite sistemi… Google Ads optimizasyonu için izlenir"). WhatsApp ön-mesajı da bozuk.
2. 17 sayfa "standart 8 seans" diyor; CRM'de paketler 5 seans (dudakta 3).
3. Akne sayfasında 4 Dermaplus katalog ekran görüntüsü ve 1 üçüncü taraf ızgara var.
4. 14 sayfanın paylaşım görseli (og:image) tırnak alanı.
5. Kendi kalemi olmayan 10 sayfa başka bakımların fiyatını kendi fiyatıymış gibi gösteriyor. Hydra Elite'in şemasında 4.500 TL var.
6. Sırt sayfasında yüz fotoğrafı, alt metni "sırt".

---

## 7. Doğrulama

_(Plan ajanı çıktısıyla tamamlanacak.)_
