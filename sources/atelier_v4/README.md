# ATELİER prototipi v4 — 7 Ekim 2026 planlarının uygulaması

Yayın: https://claude.ai/artifact/88cB2wzHjaRmes3VwRcjiR (özel; paylaşım Artifact'in Share menüsünden yapılır)

Eski Artifact (`WmsLiPPTLdnrjSrdYSXcLM`) bu oturumun hesabından açılamadı (bulunamadı / paylaşılmamış). v4 bu yüzden yeni bir Artifact olarak yayımlandı. Eski bağlantıyı korumak isteniyorsa, sahibinin hesabından o Artifact'e `website/atelier-v4.html` ve `dist/publish.json` dosya listesiyle yeniden yayın yapılır.

## Derleme

```
python3 sources/atelier_v4/shared_media.py          # monogram, yürüyüş kareleri, sertifika, film atlasları
python3 sources/atelier_v4/pmu/pmu_pack.py          # PMU çift dosyaları, ton kartelası, oda
python3 sources/media_ig_20261007/build_media.py --manifest sources/media_ig_20261007/manifest_cilt.json \
        --videos originals/instagram/videos --web website/m/ig --out /tmp/mb   # cilt medyası v2 (çıktı website/m/ig'e kopyalanır)
python3 sources/atelier_v4/build.py --check         # v3 kopyası + 70 doğrulanmış değişiklik -> website/index.html
node sources/atelier_v4/shoot.mjs --all --out /tmp/shots   # 51 rota × 390/1400: JS hatası, taşma, etiket, kırık görsel
```

`build.py` v3 kopyasını değiştirmez. Her değişiklik sayılır ve bulunamayan bir bağlantı noktası derlemeyi durdurur. Çıktılar:
- `website/index.html`: tam belge (yerelde açılır)
- `website/atelier-v4.html`: Artifact'e yayımlanan gövde
- `prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/artifact-v4.html`: anlık görüntü
- `dist/publish.json`: sayfanın kullandığı 193 medya dosyası (sınır 255)

## Durum

| Plan | Durum |
|---|---|
| Lazer epilasyon ailesi | Prototipte 6 görünüm (`#lazer`, `#lazer-fiyat`, `#lazer-erkek`, `#lazer-yuz`, `#lazer-hassas`, `#lazer-bolgesel`); canlı yamayla aynı `render.py` + `lazer.css/js`. Canlı yama `atelier_lazer_20261007/build.py` (`--out`, `--check`, `--apply`, `--rollback`) yazıldı; yapı fikstürlerinde kapılar, uygula, yeniden uygula ve geri al döngüsü ile tıklama testi geçti. Gerçek sayfalarda çalıştırmak sahipte. |
| Kalıcı makyaj “Şölen” | 4 vitrin: `#pmu` (fırça perdesi, üç sanat, kalem filmi, Uyanış, ton kartelası, oda, yol, söz, menü, SSS, final), `#pmu-dudak`, `#pmu-kas` (`/micro`, `/pudra`, `/mix`, `/silme`, `/fiyat`), `#pmu-goz` (`/baby`, `/dipliner`, `/eyeliner`). Menüdeki 11 PMU sayfası vitrinlere bağlı. `kas-cift-3` (yabancı filigran) çıkarıldı; Altın Oran Aynası salonun kına kaşına geçti. |
| Cilt Atlası | Hub + 24 sayfa tek motorla (`#cilt/<sayfa>`, paylaşılan bağlantıda `#cilt.<sayfa>`). D1 ve D2 birlikte: gerçek medya ya da dürüst yer tutucu (oda, cihaz, ürün, tipografik çizim). Prototip notları ve paneldeki “Cilt Atlası sayfası” seçicisi çekim bekleyen sayfaları gösterir (◌ çekimde, ◐ zayıf, ✓ gerçek sonuç). Şüpheli 7 kare ve zayıf montaj kullanılmıyor. |

## Doğrulama (7 Ekim 2026)

- 51 rota × 390 ve 1400 px: JS hatası 0, yatay taşma 0, etiketsiz düğme veya bağlantı 0, kırık görsel 0
- C kademesi (9 rota) ve Gece dünyası (4 rota): 0 hata
- Tarayıcının istediği her medya dosyası yayın listesinde
- Lazer canlı kopyası: 7 sayfa × 2 genişlik. H1, title, meta ve robots aynı; eski H2'ler duruyor; kampanya sayfasında canonical `/laser-signature`; yasaklı ifade 0; WhatsApp bağlantıları bölge ve [W-] kodunu taşıyor

## Sahibe kalanlar

1. Lazer canlı yaması, sunucuda: `./run patches/atelier_lazer_20261007/build.py --out /tmp/atlz --check`, ardından `--apply` (geri almak için `--rollback`). Sonra plan §7.3 kapıları çalıştırılır.
2. Cilt çekimi: `sources/media_ig_20261007/manifest_cilt.json` → `cekim` listesi (P1: leke, dermabrazyon/hydra, hollywood/paris, uzman portresi). Gelen medya manifeste eklenir, `cilt_pages.py`'de sayfanın hero/galeri alanı ona çevrilir, yeniden derlenir (D3).
3. Sahibe sorular: Hollywood ile Paris arasındaki gerçek fark; klasik bakımın adım sırası; hangi başlığın hangi bakımda kullanıldığı; Hydra Elite'in CRM karşılığı; uzman adı ve portre izni; ton adlarının onayı.
4. Sırt (3.500 / 6.500 / 7.000 TL), dudak bakımı (3 seviye) ve ton eşitleme (alan boyu) seçeneklerinin CRM'deki gerçek adları. Prototipte yalnızca fiyatlar ve nötr adlar var.

## Plandan sapmalar

- `lazer-film-kol` üretildi (ham video depoda vardı); erkek sayfasının hero'su planlandığı gibi bu.
- Cilt kadrosundaki fotoğrafların çoğu (#1, #3–#5, #7, #8, #12–#15, #18–#20, #22) depoda yok; yerlerine salon videolarından yazısız kareler kesildi (oda, 8 başlıklı cihaz, ürün, büyüteç, LED). 360p iki video (17991567131670070, 18059851076581437) dışlandı.
- PMU ton kartelası 4 yerine 5 ton (3 makro + 2 dudak fotoğrafı; etiketleri kırpıldı).
- Canlı yamada ayrı `atelier-core.js` yok; ortak parçalar `lazer.js` içinde.
