# Renk Atölyesi v3 ve tırnak filmleri — adım günlüğü (2026-10-07)

Artifact: <https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM> — **Sürüm 18**
(`1791390454-c30c`). Yayından sonra geri okundu; `index.html` ve yeni medya
yerel test kopyasıyla bayt bayt aynı.

Canlı site (seldagencerbeauty.com) **değiştirilmedi**.

## İstek

1. İlk ekran görüntüsündeki çiçekli (orkide) tırnak fotoğrafı düşük kaliteli;
   “Baby boomer” kalitesinde olanlarla değiştirilsin.
2. Renk Atölyesi'nin animasyon hatlarına (tırnak kenarları, fırça çizgisi)
   detaylıca bakılsın.
3. Mobil uyum en üst düzeye çıkarılsın.
4. Her adım TagCtx ile izlenebilir olsun.

## Bulgular (değişiklikten önce)

| # | Gözlem | Kök neden |
|---|---|---|
| 1 | Orkide klibi bulanık ve sarı tonlu | Canlıdaki dosya 5,5 sn, **425 kbps** (kaynak 2,1 Mbps). Kaynağın kendisi de yumuşak ve sıcak ışıklı (`18089498999286039`, 42,6 sn'lik uygulama videosunun son kısmı). Yeniden kodlamak yetmez. |
| 2 | Lila/nude/gül renklerinde tırnak çevresinde açık renkli çerçeve | v2 maskesi tırnağın birkaç px dışına taşıyor; boya katmanı fotoğrafın kendi parlaklığını yeniden renklendiriyor. O banttaki ten, koyu kırmızı tırnaktan parlak olduğu için açık renge dönüşüyor. |
| 3 | Arkadaki bulanık eldeki tırnaklar sert kenarlı lekeler, içlerinde pembe dikdörtgenler | Maske kenarı fotoğrafın odağını izlemiyor; bulanık tırnaktaki yansımalar maskede delik bırakıyor. |
| 4 | Sürüklerken bütün fotoğraf maviye boyanıyor (3. ekran görüntüsü) | Tarayıcı fotoğrafları **seçiyor** (seçim vurgusu). `<img>`ler maviye dönüyor, boya katmanları dönmüyor. Ctrl+A / çift tık / sürükleme ile birebir yeniden üretildi. |
| 5 | Fırça geçişi bulanık | Süpürme kenarı %12 genişliğinde yumuşak rampa (telefonda ~42 px); altın çizgi rampanın ortasında. |
| 6 | Şekil değişiminde ani sıçrama | Taban fotoğraf 180 ms karartılıp anında değiştiriliyor; boyalıyken nötr plaka ve boya katmanı hiç solmadan değişiyor. Hızlı tıklamada yarış durumu var. |
| 7 | Telefonda palet taşması | 8 renk × 36 px + boşluk 390 px'e sığmıyor (siyah kesik); uzun renk adında başlık iki satıra kırılıyor; şekil düğmeleri ~25 px yüksek. |

## Medya kararı (kısa liste: 6 poster + 1 video, kural sınırı içinde)

Eşleştirme görsel açmadan yapıldı: canlı posterler/videolar ile
`originals/instagram/videos/` kareleri karşılaştırıldı (gri ölçek, korelasyon).

| Slug | Instagram ID | Eşleşme | Karar | Gerekçe |
|---|---|---|---|---|
| `tirnak-orkide` | `18089498999286039` | 0,999 | **Çıkarıldı** | Kaynak yumuşak/sarı, canlı dosya 425 kbps. |
| `tirnak-babyboomer` | repo orijinallerinde yok | en iyi 0,38 | Kapanış bandı + kalıcı oje hikâyesi | Kullanıcının referans kalitesi; kaynak ID sunucudaki dışa aktarımda doğrulanmalı. |
| `tirnak-lila` (süt beyazı) | `18213037222332820` | 1,000 | Kalıcı oje fiyatları kahramanı | Temiz ışık, net kenar. Alt metin olduğu gibi: “Süt beyazı badem protez tırnak”. |
| `tirnak-krom` | `18226291744323491` | 1,000 | Kapanış bandı yedeği | Protez sayfasının kahramanı zaten baby boomer olduğu için orada krom french. |

Yeni medya eklenmedi; yayındaki dosyalar kullanıldı. Orkide dosyaları ve v2
maskeler artık hiçbir yerde referans almadığı için yayından kaldırıldı (eski
sürümlerde duruyor).

## Adımlar

Her adım `sources/atelier_tirnak_20261007/patch_renk_atolyesi_v3.py` içinde
birebir metin değişimi olarak durur ve beklenen sayıda eşleşmezse betik durur.
Bu sayede başka bir oturumun araya giren yayını (02bc) üzerine aynı yama
güvenle yeniden uygulandı.

| Adım | Ne değişti |
|---|---|
| A1 | Kalıcı oje fiyatları kahramanı: orkide → süt beyazı. |
| A2 | Kapanış bandı şablonu: orkide → baby boomer. |
| A3 | Kalıcı oje hikâyesi “Video”: orkide karesi → baby boomer. |
| A4–A5 | `tzFinalPick()`: kapanış bandı sayfada zaten oynayan filmi tekrarlamaz; üçü de kullanılıyorsa en azından kahramanın filmini seçmez (protez → krom french, diğer 21 sayfa → baby boomer). |
| B1 | `SHAPES`: v3 maske (`-mask-v3.png`, önbellek sorunu olmasın diye yeni ad) + gölge plakası (`-shade-1200.webp`). |
| B2 | `TZ_LREF` yeni maskelerin altında yeniden ölçüldü: uzun .236, kare .214, oval .349 (eski: .233/.217/.348). |
| B3 | Boya katmanı fotoğraf yerine gölge plakasını boyar → açık renklerde hale yok. |
| C1 | Süpürme kenarı %12 → %5; altın çizgi kenarın tam üstünde ve parmağın altında (`x*1.06% - 2.5%`). |
| C2 | Islak parıltı katmanı: kenarın hemen arkasında, yalnızca tırnak maskesinin içinde, `screen` %30. |
| C3 | Dar ekranda ipucu “Parmağınızla boyayın”a kısalır. |
| D1–D2 | `wetMask()` ve `ghost()`: ekrandaki görüntü tek katmana dondurulup 420 ms'de söner → şekil değişimi çapraz geçiş. Düşük güç (tier C) ve azaltılmış hareket tercihinde atlanır. |
| D3 | `setShape`: dört dosya (foto, nötr, gölge, maske) birlikte çözülür; eski tıklama sonrakini ezemez. |
| D4 | Fotoğraflar sürüklenemez; ıslak katman maskesi başlangıçta kurulur. |
| D5 | Fareyle basışta varsayılan davranış (seçim/sürükleme) engellenir; dikey kaydırma (dy > dx) boyamaya dönüşmez. |
| E1 | CSS: `user-select:none`, dokunma vurgusu yok; palet 8 eşit sütun (`@supports aspect-ratio`), tek satır başlık, dokunmatikte 36 px şekil düğmeleri. |

Maske/gölge üretimi: `sources/atelier_tirnak_20261007/refine_nail_masks.py`
(numpy + Pillow). Renkli yönlendirmeli filtre (r=5, eps=2e-3), v2 maskenin en
fazla 3 px dışı, ≤%0,2 kare boyutundaki kapalı yansımalar doldurulur, kenar
bandında ton `[0,85·iç, iç]` aralığına kıstırılır. Çıktılar yayınlanan v2
dosyalarından bayt bayt yeniden üretilebiliyor.

## TagCtx

### Bu ortamda çalışmayanlar (sunucu gerekiyor)

Bu bulut oturumunda `/var/www/seldagencerbeauty.com`, `public_html`, Google Ads
`.env` ve önbellekli envanter yok:

- `./run tag_ctx.py audit --offline` → `data/tag/inventory-latest.json` yok.
- `surface` → `public_html` yok, 0 sayfa.
- `tests/site*.test.js` (4 dosya) → `/var/www/.../ads-tracking.js` okunamıyor.
- `tests/test_tagctx_core.py` → **4/4 geçti**.

Canlı siteye dokunulmadığı için `audit --record`, `diff`, `verify` ve
`patches/verify_tags.sh` bu iş için çalıştırılmadı. Bu değişiklik canlı siteye
taşınırsa sunucuda TAGCTX_RUNBOOK.md'deki dört komut zorunludur.

### Artifact ölçüm kapısı (`tagtools/artifact_probe.mjs`)

Artifact'te gtag/GTM yok; ölçüm `data-track-label`, `data-tz-place`,
`wa.me`/`tel:` bağlantıları ve WhatsApp mesajındaki `[W-XXXXXX]` kodudur.
Prob her rota/ekran için bunları kaydeder, Google/Meta ölçüm isteklerini
kaydedip **iptal eder**, ayrıca konsol/sayfa hatası, kırık medya ve yatay
taşmayı ölçer.

Önce = canlı `1791389678-02bc`, sonra = aynı sürüm + v3 yaması (yerel kopya):

| Çalıştırma | Rota | Sonuç |
|---|---|---|
| 22 tırnak sayfası, 360 px | 22 | yeni hata yok |
| 6 tırnak sayfası, 320 px | 6 | yeni hata yok |
| 6 tırnak sayfası, 414 px | 6 | yeni hata yok |
| 6 tırnak sayfası, 1366 px | 6 | yeni hata yok |
| 10 diğer görünüm, 360 px | 10 | yeni hata yok |
| 10 diğer görünüm, 1366 px | 10 | yeni hata yok |

Sonra durumunun toplamı (60 çalıştırma): **0 hata, 0 kırık medya, 0 yatay
taşma, 0 ölçüm isteği**; bütün etiketler ve CTA bağlantıları aynı.
`[W-]` kodu 60'ın 56'sında var; eksik 4'ü `lazer` ve `lazer-fiyat` (360 ve
1366) ve **değişiklikten önce de** yoktu: lazer planlayıcısı bölge seçilmeden
WhatsApp bağlantısı üretmiyor.

Ham çıktılar: `sources/atelier_tirnak_20261007/tagctx/gate.txt` ve
`once-*/sonra-*.json.gz`.

## Görsel kontrol

`sources/atelier_tirnak_20261007/shots/`:

1. `1-kenarlar-mobil.jpg` — lila ve nude, önce/sonra (390 px).
2. `2-firca-kenari.jpg` — sürükleme anında kenar ve parıltı (1366 px).
3. `3-secim-ve-gecis.jpg` — seçim mavisi (önce) / yok (sonra); şekil değişiminde 170. ms.
4. `4-orkide-yerine.jpg` — kalıcı oje fiyatları kahramanı ve kapanış bandı.
5. `5-palet-mobil.jpg` — 390 px'te palet.

## Açık kalanlar

- Baby boomer kaynağının Instagram ID'si repodaki 100 orijinal arasında yok;
  sunucudaki dışa aktarımda doğrulanmalı.
- Arkadaki bulanık elin bir tırnağında kenara açılan yansıma hâlâ hafif
  pembe kalıyor (kapalı olmadığı için doldurulmadı). Gerekirse elle bir
  `fills` kutusu eklenebilir.
- Oval şekil fotoğrafı (`tirnak-yuvarlak-kirmizi`) aslında uzun köşeli
  tırnaklar gösteriyor; daha uygun bir oval kırmızı fotoğraf seçilebilir.
