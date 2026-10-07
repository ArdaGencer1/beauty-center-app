# CİLT ATLASI v5: 24 sayfa, hikâye anlatımı (uygulama + güncelleme planı, 2026-10-07)

Ana plan: `planlayal-m-mutable-rossum.md` (Cilt Atlası). Bu dosya o planın **uygulanan kısmını**, bu
oturumda verilen medya kararlarını ve kalan işleri tutar. Ana planın 4. ve 7. bölümleri burada tamamlandı.

## Bağlam

Sahibin isteği: "Cilt bakımı sayfalarını maksimum storytelling tarzında, en iyi fotoğraflar, en iyi
videolar ve edit ile geliştir ve güncelleme planı yap."

Başlangıç durumu:
- Prototipte cilt için tek vitrin (`#cilt`) vardı. Menüdeki diğer 24 cilt sayfası canlı sitedeki eski
  sayfaya dışarı bağlanıyordu.
- Vitrinin kahramanı `cilt-yarim-1` idi; sahibin 10-07 kararıyla çıkarılması gereken bir kare. Galeride de
  çıkarılacak 6 kare daha duruyordu (`cilt-cift-3/4/5`, `cilt-yarim-2`, `cilt-islem`; `cilt-cift-1` ters).
- Çalışma sırasında Artifact başka bir oturumda **vücut ailesiyle** güncellendi (sürüm
  `1791383911-8f6e`). Bu sürüm depoya `artifact-v4.html` olarak alındı; cilt işi onun üzerine kuruldu.

## 1. Yapılanlar (depoda, test edildi)

| Parça | Yol |
|---|---|
| Medya üreticisi (ffmpeg/PIL, tekrar çalıştırılabilir) | `sources/atelier_cilt_20261007/build_cilt_media.py` |
| Medya kararları ve kesimler | `sources/atelier_cilt_20261007/data/cilt_media.json` (+ `website/m/ig/media_index.json` kayıtları) |
| İçerik: 24 sayfa, 5 perdelik hikâye | `sources/atelier_cilt_20261007/src/cilt_pages.js` |
| Sayfa motoru | `sources/atelier_cilt_20261007/src/cilt.js` |
| Stil (`ca-` öneki) | `sources/atelier_cilt_20261007/src/cilt.css` |
| Artifact derleyicisi (taban: v4; her yama tam 1 eşleşme) | `sources/atelier_cilt_20261007/a4_build.py` |
| Tarayıcı doğrulaması | `sources/atelier_cilt_20261007/shoot_cilt.cjs` |
| Çıktı | `website/index.html` = `prototypes/.../artifact-v6.html` (yayındaki sürüm 12) |

### Hikâye yapısı (her alt sayfa)

1. **Kahraman**: salonda çekilmiş döngü video, "Salonumuzda çekildi" etiketi, fiyat çipi (CRM), iki CTA
   (davetiye + WhatsApp).
2. **Hikâye**: yapışkan sahne + 3–5 perde (Aynada → Önce bakarız → Koltukta → Sonra). Kaydırdıkça sahnedeki
   video perdeye göre değişir; yalnızca görünen video oynar.
3. **İmza sahnesi** (sayfaya göre): 90 dakika adım adım (klasik), kaydırmalı film (saten, sıkı görünüm),
   yüz haritası (cilt analizi), bakım menüsü + süre süzgeci + paket hesabı (fiyatlar), ışıltı düellosu
   (Hollywood ↔ Paris), alan/bölge seçici (yenileme, ton, sırt), darsonval koyu bandı (akne).
4. **Kanıt**: yalnızca gerçek önce/sonra çiftleri (basılı tut). Kanıtı olmayan hizmet sayfasında dürüst not:
   "henüz yayınlamadık; sahte görsel kullanmıyoruz".
5. Gerçek Google yorumu (birebir), fiyat kartı (H) ya da bakım yönlendirmesi (İ), SSS, "Sizin hikâyeniz" CTA'sı.

Yönlendirme: `#cilt/<slug>`; tabanın genel `görünüm/parametre` yolu kullanılır. Menüdeki 24 cilt sayfası
artık prototipte açılır. Hub'a **Cilt Atlası** ızgarası (6 ihtiyaç grubu) ve "Bir bakımın içinden" hikâyesi
eklendi; test sonucundan bakımın sayfasına bağlantı verilir.

Ölçüm: her buton `data-track-label="at-<kod>-<yer>"` (ör. `at-cakne-hero-saat`); WhatsApp bağlantıları gerçek
`<a href>`, mesajda `[W-XXXXXX]` kodu (`visitCode()`), render sonrası `relead()`. Mevcut `autoLabel`'daki
`/` içeren geçersiz `at-…-git-…` etiketleri (tırnak alt sayfaları dahil) güvenli karaktere çevrildi.

## 2. Medya kararları (bu oturum)

Kaynak: `originals/instagram/videos/` + `website/m/ig/`. Görsel inceleme sınırına uyuldu (3 video şeridi,
1 poster karesi, 1 çift karesi).

| slug | IG id | Karar | Gerekçe / edit |
|---|---|---|---|
| `cilt-led-dongu` | 18617996404000518 | Hub kahramanı | 0,55–8,4 sn sahne kesimleri arası; poster 5. sn (kırmızı ışık) |
| `cilt-kubbe` | 18119195767718567 | LED bandı, kubbe perdeleri | 5–17 sn; `vidstab` ile sabitlendi |
| `cilt-saten` | 18192437785391754 | Saten kahramanı | 1,7–6,5 sn tek çekim. **Planın 1,6–6,6 önerisi düzeltildi**: 0,7–1,6 sn siyah geçiş |
| `cilt-saten-yakin` | 18192437785391754 | Göz çevresi, anti-aging | 6,62–13,2 sn (alın + göz); poster 0,6 sn |
| `cilt-saten-film` | 18192437785391754 | Kaydırmalı film | 48 kare tek sprite (2880×3840, 431 KB). Artifact dosya bütçesi için 48 ayrı kare yerine 1 dosya |
| `cilt-analiz` | 18122366353896732 | Cilt analizi kahramanı, Adım 1 | 3,2–6,65 sn (lamba + büyüteç) |
| `cilt-masaj` | 18122366353896732 | Adım 4 | 0–2,15 sn |
| `cilt-kopuk` | 18122366353896732 | Adım 2, temizlik kahramanı | 2,24–3,12 sn ileri-geri döngü |
| `cilt-komedon` | 18122366353896732 | Adım 3 | 6,74–8,64 sn (≤2 sn kuralı) |
| `cilt-darsonval` | 18025275239906179 | Akne kahramanı + koyu bant | Tam tek çekim; `hqdn3d` |
| `yuz-cift-1` | 18039236768821035 | Hub kanıtı, yüz/yenileme/ton/temizlik | Eski `cilt-cift-1`: 180° döndürüldü, ters kalan etiket iki yarımdan eşit kırpıldı. Kaynak yalnız 480 px (büyütülmedi) |
| `akne-cift-1`, `akne-cift-2` | 17937892356335721, 18029533706831317 | Akne kanıtı | Değiştirilmedi. "CİLT BAKIMI" etiketi yüzü kesmeden kırpılamıyor, yerinde kaldı |

Hepsine aynı hafif sıcak ton (`colortemperature 6100 / mix 0.6`, kontrast 1,03, doygunluk 1,04). Önce ve sonra
yarımlarına ayrı işlem yok. Yeni videoların toplamı ~7,4 MB, her biri 1,2 MB altında.

**Konu dışı stand-in düzeltmesi:** `salon-tur` posteri tırnak barını gösteriyor; cilt sayfalarından çıkarıldı.
Sırt, koltuk altı ve dirsek sayfalarında monogramlı tipografik kahraman kullanılıyor.

Artifact'ten kaldırılacak 14 dosya (artık hiçbir yerden referans verilmiyor): `cilt-yarim-1-{800,1200}`,
`cilt-yarim-2-800`, `cilt-islem-800`, `cilt-cift-{1,3,4,5}-{once,sonra}-480`, `cilt-video-3{.mp4,-poster}`.

## 3. Doğrulama (yapıldı)

```bash
python3 sources/atelier_cilt_20261007/a4_build.py            # 136 referans · eksik 0 · dışlanan 0
python3 -m http.server 8766 -d <önizleme>                    # website/ + yayındaki diğer oturum medyası
BASE=http://127.0.0.1:8766/index.html NODE_PATH=$(npm root -g) \
  node sources/atelier_cilt_20261007/shoot_cilt.cjs <çıktı>  # 50/50
```

- 25 yol × (390×844, 1280×800): konsol hatası 0, başarısız istek 0, yatay taşma 0, WhatsApp bağlantılarının
  hepsinde `[W-]`, geçersiz etiket 0, hikâye sahnesi = aktif perde.
- Tıklama akışı: atlas kartı → sayfa; menü → saten sayfası (24 iç bağlantı); kahraman CTA → davetiye doğru
  bakımla ve `[W-]` ile; geri → hub; yüz haritası (yanak → akne/ton/hassas); film tuvali çiziliyor.
- Gerileme: 18 görünüm (tırnak alt sayfası ve 9 vücut sayfası dahil) temiz.
- **Yapılamayan:** TagCtx `audit --record / diff / verify` ve `patches/verify_tags.sh`. Bunlar sunucudaki
  `public_html` ile Google Ads envanterini istiyor; bu bulut ortamında ikisi de yok. Canlı site değişmedi.

## 4. Güncelleme planı (kalanlar, sırayla)

| # | İş | Kim / koşul | Çıktı |
|---|---|---|---|
| G0 | ~~Artifact'e yayın~~ **Yapıldı** | Sahip onayıyla | Sürüm 12 (`1791386588-7eb6`): 21 dosya eklendi, 14 dosya kaldırıldı (322 dosya). Geri okundu: tek iskelet, içerik birebir. Yayın sırasında lazer ve tırnak oturumları da yayın yaptı; değişiklikleri korundu |
| G1 | CRM doğrulaması | Sahip / CRM | Yeni 5 kalem (ton, saten, dudak, sırt, koltuk altı) ve yenileme bölge fiyatları (3.500/4.000/6.000) ile ton alan fiyatları (4.500/5.500/6.500) planın CRM matrisinden alındı; canlı CRM'den yeniden doğrula. Sırt 3 fiyatının (3.500/6.500/7.000) yarım/tam eşleşmesi |
| G2 | Sunucudaki fotoğraflar (D1 tamamlama) | Sunucu oturumu | Planın kadrosundaki şu kareler yalnızca sunucuda: #1 gerçek yarım yüz 18063357971188976 (hub kahramanı olmalı), #3 17945921837942670 (kaydırıcı), #4 17913554493238260, #5 cilt odası 17884915872588889 (fiyatlar ve vücut stand-in'i), #7 Space Oxygen 17894387157352959 (dermabrazyon, hydra), #8 Dermaplus rafı 18133083652567287, #12 göz çevresi 18161360971378712, #13 erkek şakak 18093388681773950, #14/#15 burun gözenek, #18 oda köşesi, #19 kalp karesi, #20 köpük, #22 olgun cilt. `build_media.py` + manifest ile işle, `website/m/ig/`'ye koy, `CM`'ye ekle, sayfalarda `hero`/`proof`/perde medyasını değiştir |
| G3 | Personel çekimi (D3) | Salon; çekim listesi ana plan §3 | P1: leke, dermabrazyon/hydra (Space Oxygen), hollywood/paris, uzman portresi. P2: sırt, koltuk altı, dirsek, kararma, antioksidan, dudak, hassas. Rıza (KVKK). Gelince yalnızca `CM` + sayfa `hero/proof` alanı değişir, `shoot:true` kaldırılır |
| G4 | Sahibe sorular | Sahip | Hollywood ↔ Paris gerçek farkı (düello metni), klasik bakım adım sırası (şu an genel 5 adım), Space Oxygen başlık eşleşmesi, Hydra Elite'in CRM kalemi, uzman adı ve portre izni |
| G5 | Canlı siteye taşıma | Sahip onayı + `--check` | `render.py` benzeri statik HTML (SEO için H1/metin sunucuda), canlı slug'lar; ana plan §6'daki canlı hatalar (cilt-inceltme şablon metni, "8 seans", Dermaplus ekran görüntüleri, og:image, ödünç fiyatlar, sırt sayfasındaki yüz) |
| G6 | TagCtx kapısı | Sunucu | `./run tag_ctx.py audit --record`, `diff`, `verify --pages <cilt sayfaları>`, `patches/verify_tags.sh` |

Önerilen sıra: **G1 → G2 → G4 → G3 → G5 → G6** (G0 tamamlandı).

## 5. Yayın notu

- `a4_build.py` cilt yamalarını cilt öncesi bir tabana uygular. Yayındaki sürüm artık Cilt Atlası'nı içerdiği için sonraki cilt değişiklikleri doğrudan `src/` dosyalarından ve yayındaki sürüm üzerinde yapılmalı (yamalar ikinci kez uygulanamaz, derleyici bunu 0/2 eşleşme hatasıyla durdurur).
- Geri okunan sayfa yayın iskeletini içerir; yayından önce sökülür (bkz. `AI_HANDOFF.md`).

## 6. Güncelleme turu 2 (2026-10-07, Artifact sürüm 16 `1791388726-c3e0`)

**G1 · CRM doğrulaması: yapılamadı (ağ).** Bu bulut ortamının ağ politikası `seldagencerbeauty.com`'u
(ve `/api/public/price-menu`'yu) engelliyor. Diğer dallarda da cilt CRM verisi yok; `claude/happy-babbage-hz55k8`
dalındaki cilt sayfaları aynı rakamları kullanıyor (bağımsız doğrulama değil). Kalan: sunucuda
`/api/public/price-menu`'dan ton, saten, dudak, sırt, koltuk altı ve bölge/alan fiyatlarını oku.

**G2 · Gerçek medya: kısmen yapıldı.** `instagram.com` ve sunucu arşivi bu ortamdan erişilemez. Ancak
`claude/happy-babbage-hz55k8` dalında başka bir oturumun sunucu arşivinden ürettiği cilt medyası vardı; kısa liste
görsel olarak doğrulandı ve 9 öğe alındı:

| slug | IG id | Kullanım |
|---|---|---|
| `cilt-hydra` (video) | 18406447750155831 | Dermabrazyon ve Hydra kahramanı |
| `cilt-maske` (video) | 18106634948074733 | Hollywood ve antioksidan kahramanı |
| `cilt-led-kubbe` (video) | 18106634948074733 | Paris kahramanı |
| `cilt-sunger` (video) | 18455967805112572 | Fiyatlar kahramanı (altın lavabo) |
| `cilt-cihaz` | 18014729837423154 | Dermabrazyon/Hydra "Cihaz" perdesi |
| `cilt-uygulama` | 18406447750155831 | Dermabrazyon/Hydra "Koltukta" perdesi |
| `cilt-hazirlik` | 18106634948074733 | Hollywood/Paris maske hazırlığı |
| `cilt-urun` | 18406447750155831 | Antioksidan "Ürün" perdesi |
| `cilt-lamba` | 18455967805112572 | Analiz ve yüz bakımı "Erkekler de" perdesi |

Dışlanan: `cilt-kirmizi-led` (çok karanlık). Cihazın hangi bakımda kullanıldığı sahibe sorulacak; metinler bu
yüzden "çok başlıklı cihazımız, başlığı uzman seçer" diyor. Sunucuda kalanlar (hâlâ eksik): #1 gerçek yarım yüz,
#3, #4, #5 cilt odası, #12, #13, #14/#15, #18, #19, #22.

**G3 · Sahip soruları: sahipten yanıt bekliyor** (Hollywood ↔ Paris farkı, klasik adım sırası, cihaz başlıkları,
Hydra Elite CRM kalemi, uzman adı/portre izni).

**Mobil uyum ve yön (oryantasyon) düzeltmeleri** (`src/mobil.css` → `<style id="mobil-duzen">`, tüm görünümler):
- Yatay telefon (≤560 px yükseklik): kahraman iki sütun, medya ekran yüksekliğinde; H1 ilk ekranda (önce 700–1300 px
  aşağıdaydı: cilt, kaş, kirpik, lifting, kalıcı makyaj, tırnak alt sayfaları, vücut, lazer). Alt çubuk sağda küçük hap.
- Dikey tablet ve 320 px telefon: kahraman yüksekliği `min(125vw, 58svh, 100svh − 300px)`; genişlik tam kalır.
- Çentik: yatayda `env(safe-area-inset-*)` ile sol/sağ boşluk.
- Cilt: yatayda hikâye ve film iki sütun / tam yükseklik; dikey tablette atlas 3 sütun; "← Cilt Atlası" dokunma alanı 44 px.
- Doğrulama: `mobil_audit.cjs` 10 ekran × 10 cilt yolu 100/100; 13 diğer görünümde yatay ve dikey temiz; döndürme testi
  (dikey ↔ yatay, sayfa ortasında) taşma yok, sahne-perde eşleşmesi korunuyor; `shoot_cilt.cjs` 50/50; 23 görünüm duman testi temiz.
- Diğer oturumlara bildirilen küçük dokunma hedefleri: lazer bölge düğmeleri 29 px, tırnak `tz-ask` 14 px, salon 15 px bağlantılar.

**Derleme:** Cilt artık yayında olduğu için `a4_build.py --refresh <yayındaki.html>` kullanılır: yalnız
`#cilt-atlas` stili, `#mobil-duzen` stili ve `/* CİLT ATLASI … /CİLT ATLASI */` kod bloğu yenilenir.
