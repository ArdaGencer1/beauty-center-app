# AI handoff — web sitesi, Artifact ve medya

Son doğrulama: **2026-10-07** (Cilt Atlası v5 eklendi)

Bu dosyayı web sitesi, Claude Artifact veya Instagram medyası üzerinde çalışmaya
başlamadan önce oku. Amaç, her yeni ajanın yüzlerce fotoğrafı ve videoyu yeniden
inceleyerek token harcamasını önlemektir.

## Değiştirilemez çalışma kuralları

- Mevcut Claude Artifact geliştirilecek; yeni Artifact oluşturulmayacak:
  <https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM>
- Yayındaki sürüm **Artifact v6** = Artifact sürüm 12, `1791386588-7eb6`
  (v3 + vücut + lazer + tırnak kartela, başka oturumlar + Cilt Atlası). Depoda
  `artifact-v6.html` = `website/index.html` (yayın iskeleti olmadan). Artifact'e
  aynı anda birden çok oturum yayın yapıyor: yayından hemen önce yeniden oku ve
  değişiklikleri o sürümün üzerine birleştir.
- Yayın servisi sayfayı kendi `<!doctype…><body>` iskeletiyle sarar ve geri
  okumada bu iskelet döner. Geri okunan dosyayı olduğu gibi yayınlama: önce
  iskeleti sök (ilk satır ve son `</body></html>`), yoksa iskelet ikilenir.
- Fotoğrafları veya videoları topluca açma, yeniden analiz etme ya da contact
  sheet üretme. Önce manifest ve medya indeksinden ele, sonra yalnızca kısa
  listeyi görsel olarak doğrula.
- Instagram ana veri kaynağı `instagram.db`'dir. **`media.json` kullanma.**
- Gerçek olmayan önce/sonra, stok görsel, başka uzmana ait iş, fiyat uydurma,
  sonuç garantisi veya doğrulanmamış iddia ekleme.
- `.env`, erişim anahtarı, kişisel veri veya `instagram.db` Git'e konmaz.
- HTML/JS, CTA, form, WhatsApp/telefon bağlantısı, Consent Mode, GTM veya
  dönüşüm koduna dokunan her işten sonra `TAGCTX_RUNBOOK.md` izlenir ve
  `patches/verify_tags.sh` geçmeden ölçümün korunduğu söylenmez.

## Kaynak haritası

### GitHub teslim deposundaki yollar

| İçerik | Yol | Not |
|---|---|---|
| Açılabilir site | `website/index.html` | İşlenmiş medyayı `website/m/ig/` altından kullanır. |
| İşlenmiş medya | `website/m/ig/` | 548 dosya; topluca açma. |
| Medya indeksi | `website/m/ig/media_index.json` | 111 slug; dosya, poster, boyut, süre, Instagram ID ve permalink bilgisi. İlk bakılacak medya kaynağı. |
| Seçim manifesti | `sources/media_ig_20261007/manifest.json` | 111 seçilmiş kayıt ve açık dışlama nedenleri. |
| Medya üreticisi | `sources/media_ig_20261007/build_media.py` | Crop, hizalama, poster, video ve varyant üretim kuralları. |
| Ham videolar | `originals/instagram/videos/` | 100 video; yalnızca seçilen Instagram ID/slug için aç. |
| Lazer kaynakları | `sources/atelier_lazer_20261007/` | `render.py`, `src/lazer.css`, `src/lazer.js` ve doğrulanmış veri. |
| Artifact anlık görüntüleri | `prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/artifact-v{3,4,5,6}.html` | v4/v5 = başka oturumların ara sürümleri; v6 = yayındaki sürüm (Cilt Atlası dahil). |
| Cilt Atlası kaynakları | `sources/atelier_cilt_20261007/` | `build_cilt_media.py`, `a4_build.py`, `shoot_cilt.cjs`, `src/`, `data/cilt_media.json`. |
| Güncel planlar | `plans/claude/20261007/` | Lazer, PMU, Cilt Atlası ve Cilt Atlası v5 uygulama/güncelleme planı. |

### Sunucudaki asıl yollar

- Proje: `/var/www/seldagencerbeauty.com/google-adsAI/`
- İşlenmiş medya: `patches/media_ig_20261007/out/`
- Medya indeksi:
  `patches/media_ig_20261007/out/images/ig/media_index.json`
- Manifest ve üretici: `patches/media_ig_20261007/manifest.json` ve
  `patches/media_ig_20261007/build_media.py`
- Instagram orijinalleri:
  `/var/www/seldagencerbeauty.com/all_api_meta/instagram_exports/20261006-191757Z/media/`
- Instagram arama kaynakları:
  `/var/www/seldagencerbeauty.com/all_api_meta/instagram_library/ai/summary.json`
  → `delta.tsv` → `instagram_context.py --search "hizmet"`
- Ana Instagram veritabanı:
  `/var/www/seldagencerbeauty.com/all_api_meta/instagram.db`

## Token tasarruflu medya inceleme protokolü

1. İstenen hizmeti ve sayfayı belirle.
2. Önce `manifest.json` içinde `fam`, `slug`, `id`, `kind` ve `alt` alanlarıyla
   filtrele. Görsel açma.
3. Adayların teknik bilgisini `media_index.json` içinden oku. Video için önce
   poster, süre, boyut ve permalink bilgisine bak.
4. Plan dosyasındaki daha önce verilmiş medya kararlarını ve dışlamaları uygula.
5. En fazla **3–6 görsel** veya **1–3 video** kısa listele; yalnızca bunları
   görsel olarak açıp doğrula.
6. Yeni inceleme sonucunu slug + Instagram ID + karar + kısa gerekçeyle bu
   handoff'a veya ilgili plana yaz. Sonraki ajan aynı işi tekrarlamasın.
7. Yalnızca mevcut indeks/plan kararı yetersizse daha geniş tarama yap; nedenini
   çalışma notunda belirt.

Hızlı, görselsiz sorgu örnekleri:

```bash
python3 scripts/ai_media_lookup.py summary
python3 scripts/ai_media_lookup.py search lazer --family lazer --limit 6
python3 scripts/ai_media_lookup.py show lazer-film-jel
rg -n '"fam": "lazer"|"slug": "lazer-' sources/media_ig_20261007/manifest.json
rg -n 'pmu|dudak|kas|goz' sources/media_ig_20261007/manifest.json
python3 /var/www/seldagencerbeauty.com/all_api_meta/instagram_context.py --search "hizmet"
```

Makine-okunur yollar, plan durumları, sabit kurallar ve bitiş kapıları ayrıca
`AI_CONTEXT.json` içinde tutulur. Ajanlar uzun belgeyi tekrar tekrar ayrıştırmak
yerine önce bu dosyayı kullanabilir.

## Mevcut seçilmiş medya özeti

Manifestte toplam **111** kayıt vardır:

| Aile | Kayıt |
|---|---:|
| Tırnak | 25 |
| Kalıcı makyaj (PMU) | 24 |
| Lazer | 15 |
| Cilt | 13 |
| Kirpik | 12 |
| Salon | 9 |
| Kaş | 7 |
| Still-life | 5 |
| Bölgesel incelme | 1 |

Bu sayı “sayfa tamamlandı” anlamına gelmez; yalnızca medya seçimi/işleme
envanteridir.

## Planların gerçek durumu

### 1. Lazer epilasyon ailesi — ileri aşamada, yarım

Plan:
`plans/claude/20261007/https-panel-seldagencerbeauty-com-new-cu-wiggly-adleman.md`

Hazır olanlar: 15 lazer medya kaydı; `render.py`; `src/lazer.css`;
`src/lazer.js`; CRM, navigasyon ve yorum veri dosyaları.

Kalanlar: plandaki `a3_build.py`/Artifact v4 derlemesi ve aynı Artifact'e yayın;
canlı yama `build.py`; tam sayfa paketi; ekran görüntüleri, `--check`, mobil/
masaüstü ve CTA testleri; sahip onayından sonra canlı `--apply`.

### 2. Kalıcı Makyaj “Şölen” — medya ileri, arayüz yarım

Plan:
`plans/claude/20261007/pasted-content-id-81ae-dosya-glistening-pancake.md`

Hazır olanlar: 24 PMU manifest kaydı ve bunlardan üretilmiş varyantlar.

Kalanlar: `pmu_build.py`, `pmu_pack.py`, yeni vitrin/sahneler, `shoot2.mjs`,
Artifact yayını ve plandaki doğrulamalar.

### 3. Cilt Atlası — 24 sayfa yayında (Artifact sürüm 12)

Plan: `plans/claude/20261007/planlayal-m-mutable-rossum.md`; uygulama ve
güncelleme planı: `plans/claude/20261007/cilt-atlasi-hikaye-v5.md`.

Hazır olanlar: 11 yeni cilt medyası (9 video, 1 kaydırma filmi sprite'ı, 1
döndürülmüş önce/sonra çifti); sayfa motoru; 24 alt sayfa (`#cilt/<slug>`) ve
hub'da atlas; çıkarılan kareler kaldırıldı; tarayıcı doğrulaması 50/50.

Kalanlar: yeni CRM kalemlerinin doğrulanması,
yalnız sunucuda duran kadro fotoğrafları (#1, #3, #5, #7…), personel çekimleri,
canlıya taşıma ve TagCtx kapısı. Ayrıntı ve sıra v5 planında (G0–G6).

Önerilen geliştirme sırası: **Lazer → PMU → Cilt Atlası**.

## Bilinen dışlamalar ve doğruluk kararları

Manifestte açıkça dışlanan PMU/kaş içerikleri:

- `18516297502030856`: başka uzmana ait filigranlı iş.
- `kalici-makyaj-dudak-20260407.png`: AI ile fazla yumuşatılmış kopya; gerçek
  sonuç olarak kullanılmaz.
- `18104556860143186`: stok görünümlü kalem posteri.
- `17986864907913512`: brow lamination/lash lift; PMU değil.
- `18284646271254855`: 360p microblading videosu.

Cilt planında çıkarılması kararlaştırılan eski seçimler:

- `cilt-yarim-1` (`17951646918167938`)
- `cilt-yarim-2` (`17909854857222461`)
- `cilt-cift-2` (`18016986917719157`)
- `cilt-cift-3` (`18086010650107298`)
- `cilt-cift-4` (`17987084615917224`)
- `cilt-cift-5` (`18091846780704413`)
- `cilt-islem` (`18394257022142297`)
- `cilt-video-2` (`18084203987184570`)

Manifest eski kayıtları hâlâ içerebilir. Cilt geliştirmesinde planın son kararı
manifestteki eski varlıktan üstündür.

Cilt v5'te verilen ek kararlar (ayrıntı: `cilt-atlasi-hikaye-v5.md` §2):

- `cilt-cift-1` (`18039236768821035`) → `yuz-cift-1`: 180° döndürüldü, ters
  etiket iki yarımdan eşit kırpıldı; gerçek ve güçlü tam yüz kanıtı.
- `18192437785391754` saten videosunda 0,7–1,6 sn siyah geçiş var; döngü 1,7
  sn'den başlar (planın 1,6–6,6 önerisi düzeltildi).
- `salon-tur` posteri tırnak barını gösterir; cilt sayfalarında kullanılmaz. Lazer için gerçek “önce/sonra” yoktur;
gerçek işlem videoları ve dürüst süreç anlatımı kullanılır.

## “Tamamlandı” demeden önce zorunlu kapılar

- Aynı Artifact URL'sine yayınlandı ve yayınlanan sürüm tekrar okundu.
- Kırık medya referansı: 0.
- Tarayıcı konsol hatası: 0.
- Mobil yatay taşma: 0.
- İlgili planın mobil ve masaüstü ekran görüntüleri kontrol edildi.
- WhatsApp/telefon CTA ve `[W-]` izleme davranışı doğrulandı.
- Artifact dosya sınırı aşılmadı; PMU planındaki bilinen sınır 255 dosyadır.
- Canlı site için önce dry-run/`--check`; açık sahip onayı olmadan `--apply` yok.
- Site/tracking değiştiyse TagCtx `audit --record`, `diff` ve runtime `verify`
  geçti; yeni kritik ölçüm bulgusu yok.

## Repo aktarım notu

Bu handoff önce sunucudaki kaynak depoda üretilmiştir. GitHub'da dosyaların
bulunduğu teslim deposuna da kök dosya olarak eklenmelidir. Hedef özel depo
`ardagencerz01-rgb/beautyapp` ise bağlı GitHub hesabının bu depoya erişimi
doğrulanmadan “aktarıldı” denmemelidir.
