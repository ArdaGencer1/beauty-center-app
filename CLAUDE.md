# CLAUDE.md — Selda Gençer Beauty · Website Studio

Bu dosya, depoda çalışacak sonraki AI oturumları içindir. 7 Ekim 2026 oturumunda yapılan hatalar ve çözümleri aşağıda. Aynılarını tekrarlama.

## Önce bunları bil

- **Aktif Artifact:** https://claude.ai/artifact/88cB2wzHjaRmes3VwRcjiR (v4). Eski `WmsLiPPTLdnrjSrdYSXcLM` bu hesaptan açılamıyor; `read` "not found" döner, tekrar deneme. Başka bir sohbetten güncellerken v4 URL'sini `url` olarak ver; vermezsen yeni bir Artifact açılır.
- **Yayımlanan dosya `website/atelier-v4.html`'dir, `website/index.html` değil.** v3 kopyası Artifact iskeletini (`<!doctype html>…<body>`) içeriyor; `build.py` bunu soyup `atelier-v4.html`'e yazar. Tam belgeyi yayımlarsan iskelet iç içe girer.
- **Akış:** `sources/atelier_v4/build.py --check` → `node sources/atelier_v4/shoot.mjs --all --out /tmp/shots` → yayın (`files` = `sources/atelier_v4/dist/publish.json`, `root` = `website`). Ayrıntılar: `sources/atelier_v4/README.md`.
- **Canlı site bu ortamdan erişilemez.** `seldagencerbeauty.com` proxy tarafından engelli (403); `/api/public/price-menu` de çekilemez. Canlı sayfaları indirme. Lazer yaması `tests/make_fixtures.py` ile üretilen yapı fikstürlerinde test edilir; gerçek `--apply` işini sahip sunucuda yapar. "Canlıda doğrulandı" deme.
- **`instagram.db` ve ham fotoğraf arşivi depoda yok.** Yalnızca `originals/instagram/videos/` (100 video) ve işlenmiş `website/m/ig/` var. Plandaki bir IG fotoğrafı yoksa uydurma; salon videolarından yazısız kare kes (`build_media.py` kind `still`).

## Kod hataları ve çözümleri

1. **Modül adı çakışması.** `mod_lazer.py`, `atelier_lazer_20261007/`'yi `sys.path`'e ekliyor. O klasörde de `build.py` var; `import build` yanlış dosyayı aldı. Derleyici yardımcılarını **`import atelier_build as build`** ile al (`build.py` kendini bu adla kaydeder).
2. **İç içe `<section>`.** Lazer işaretlemesinde `<section class="lz-sec">` var. `Doc.section()` / `replace_section()` ilk `</section>`'ı bulur; lazer görünümlerinde kullanma, boyut ölçerken de yanılma.
3. **Aynı id'ler.** Altı lazer sayfası tek belgede duruyor; `id="lz-harita"` gibi id'ler çakışıyordu. `mod_lazer.suffix_ids()` her id'ye `--<anahtar>` ekler. Yeni çok sayfalı modülde de aynısını yap.
4. **JS sırası.** `PLANS` planlayıcı bölümünde, `STORIES` dosyanın sonuna yakın tanımlı. `STORIES[...]` eklemeleri **`d.js_before_boot()`** ile gider; `PLANS` öncesine koyarsan `undefined` hatası alırsın.
5. **Çalışma anında kurulan medya yolları.** `"m/ig/"+slug+"-800.webp"` gibi yollar statik taramada görünmez; yayın listesi eksik kalır. Modülde `/*@media ["m/ig/..."] @*/` bloğuyla kaydet. v3'ün dizileri için `build.py: v3_dynamic()` var. Yayından önce `shoot.mjs`'in yazdığı `requested.json` ile `publish.json`'u karşılaştır; fark sıfır olmalı.
6. **v3'te olmayan dosyalar.** `m/monogram.png`, `m/walk-06..10.webp`, `m/cert-*.webp` depoda yoktu; `shared_media.py` salon videolarından üretiyor. `build.py --check` eksik dosyayı yakalar, atlama.
7. **Dosya sınırı.** Bir yayın en fazla 255 dosya alır. Film kareleri tek tek değil, 3×3 atlas (`a1.webp…`) olarak yayımlanır; okuyucu `atlas()` fonksiyonu.

## CSS ve düzen hataları

8. **Siyah ya da boş hero.** `aspect-ratio:auto!important` ile `margin:0 auto` grid içinde birleşince kutunun genişliği 0 oldu. Dikey karşılaştırmalarda satır içi `aspect-ratio` kalsın; `height` ver, `width:auto` bırak. `background-size:200% 100%` (tek dosyada önce|sonra) ancak kutu oranını koruyorsa düzgün görünür; yoksa görüntü gerilir.
9. **Yatay taşma.** İçinde yatay kayan satır olan grid çocuğuna `min-width:0` ver; kapsayıcıya da `grid-template-columns:minmax(0,1fr)`.
10. **Kelime ortasından kırılan başlık.** Harf harf animasyonda her harf `inline-block` olunca satır kelimenin içinden kırıldı. Her kelimeyi `white-space:nowrap` bir span'a sar (`pmu_build.h1_letters`).
11. **Altın düğme etiketi `…` ile kesiliyor** (v3'ten gelen sorun). `.golden-actions .btn-gold .lbl{max-width:none}`; etiketleri de kısa tut.
12. **C kademesi (statik).** Animasyonu kapatırken o animasyonun ipucunu ve düğmesini de gizle (örneğin "Parmağınızla boyayın").

## Medya hataları

13. **360p videolar.** 17991567131670070 ve 18059851076581437 360p; plan 360p'yi dışlar. Kullanmadan önce `ffprobe` ile çözünürlüğe bak.
14. **IG id yazım hatası.** Bir id plan notunda yanlış yazılmıştı (…165831; doğrusu …155831). Dosyayı `*_<id>.mp4` glob'uyla bul; bulamazsan id'den şüphelen.
15. **Basılı yazılar.** Birçok videoda altyazı, "ÖNCESİ/SONRASI" ya da fiyat afişi var. Kare seçmeden önce ızgaraya bak (`contact_sheets`); kırpma kutusunu yazının üstünde bitir.
16. **Görsel etiketleri.** "CİLT BAKIMI", "DUDAK RENKLENDİRME" ve "ALTIN ORAN KAŞ" hapları var. Kırpılabiliyorsa önce ve sonra yarısına **aynı** kutuyu uygula. Renk ayarı da iki yarıya aynı olmalı; rötuş yapılmaz.
17. **Yabancı filigran.** `kas-cift-3` (IG 18516297502030856) yabancı filigranlı; asla kullanma.
18. **Dudak tonu rengi.** Ortanca renk ilk denemede ten ve gölge piksellerini topladı. Maske sıkı olmalı (`r > 1.6g`, `r > 1.4b`, doygunluk yüksek); sonucu gözle kontrol et.
19. **ffmpeg döngüsü.** `while read` içinde ffmpeg stdin'i tüketip döngüyü bozdu. `-nostdin` kullan ya da Python ile yaz.

## Test ve araç hataları

20. **Playwright içe aktarma.** ESM, `NODE_PATH`'i görmez. `createRequire` kullan, bulamazsa `npm root -g` yolundan yükle (`shoot.mjs`'de hazır).
21. **Fontta yanlış alarm.** Testte Google Fonts isteği bilerek engelleniyor; `net::ERR_FAILED` hatasını hata sayma.
22. **Fikstür viewport'u.** `<meta name=viewport>` yoksa mobil genişlik 980 görünür. Fikstürde bulunmalı.
23. **Otomatik denetim yanıt vermezse** (Bash "classifier gave no verdict"): dosyayı Write aracıyla yaz, komutu sonra tekrar dene. Bu sırada Bash gerektirmeyen işe geç.

## İçerik kuralları (sahip kararları)

24. **Yasak ifadeler:** "kesin sonuç", "%100", mutlak anlamda "kalıcı", bizim iddiamız olarak "acısız", "en iyi", sahte önce/sonra, sahte kıtlık, geri sayım. "Garanti" yalnızca CRM adı olan "bitiş garantili paket" içinde geçebilir. Kelimesi kelimesine Google yorumları müşterinin sözüdür; lazer `--check` yorum kartlarını taramaz, kendi metnimiz ise taranır.
25. **Fiyat ve ad yalnızca CRM'den.** Ad bilinmiyorsa uydurma: sırt (3 seçenek), dudak bakımı (3 seviye) ve ton eşitleme (alan boyu) için CRM adları sahipten bekleniyor. Lazerde fiyat yazılmaz.
26. **Paket hesabı:** 5 seans = tek seansın 4,5 katı. Bu "beş seans, dört buçuk seans fiyatına" demektir; "bir seans hediye" demek yanlış.
27. **Rehber (İ) sayfalar fiyat ödünç almaz.** İlgili bakımın fiyatı, o bakımın adıyla gösterilir.
28. **Uzman adı yazılmaz** (lazer). Yorumlardaki yüzde ifadeleri gösterilmez.
29. **Gerçek sonucu olmayan sayfalar** "Prototip notu · sonuç fotoğrafı çekimde" taşır. Çekim listesi `sources/media_ig_20261007/manifest_cilt.json` → `cekim`.

## Yayın ve Artifact kuralları

30. **Derin bağlantı.** Artifact bağlantısından `location.hash`'e yalnızca düz token ulaşır; `/` ulaşmaz. Paylaşılan bağlantıda `#cilt.akne-bakimi` biçimini kullan; sayfa içinde `#cilt/akne-bakimi` de çalışır.
31. **Çubuk etiketi.** `bar` alanına kodda " · saatimi seç" eklenir; alanın kendisine yazma, yoksa iki kez görünür.
32. **Yayın öncesi kontrol:** `build.py --check` (0 eksik dosya, ≤255 dosya) ve `shoot.mjs --all` (`SUMMARY failing=0`). Ekran görüntülerine gerçekten bak: siyah kutu, kırık başlık, gerilmiş görsel. Bunlar otomatik kontrolden geçebiliyor.
