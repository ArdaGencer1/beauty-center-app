# AI handoff — web sitesi, Artifact ve medya

Son doğrulama: **2026-10-07**

Bu dosyayı web sitesi, Claude Artifact veya Instagram medyası üzerinde çalışmaya
başlamadan önce oku. Amaç, her yeni ajanın yüzlerce fotoğrafı ve videoyu yeniden
inceleyerek token harcamasını önlemektir.

## Değiştirilemez çalışma kuralları

- Mevcut Claude Artifact geliştirilecek; yeni Artifact oluşturulmayacak:
  <https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM>
- Depodaki son kaynak anlık görüntüsü **Artifact v3**'tür. Artifact üzerinde bu
  anlık görüntüden sonra yalnızca Claude içinde yapılmış değişiklikler depoda
  olmayabilir; sürümü doğrulamadan “tam eşleşiyor” deme.
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
| Artifact anlık görüntüsü | `prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/artifact-v3.html` | Mevcut Artifact'in depodaki v3 tabanı. |
| Güncel planlar | `plans/claude/20261007/` | Lazer, PMU ve Cilt Atlası planları. |

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

### 3. Cilt Atlası — planlandı, uygulama büyük ölçüde bekliyor

Plan: `plans/claude/20261007/planlayal-m-mutable-rossum.md`

Hazır olanlar: medya araştırması, sayfa-medya matrisi, edit reçetesi, çekim
listesi ve dalga planı; manifestte 13 cilt kaydı.

Kalanlar: medya v2, sayfa motoru, 25 sayfanın D1–D3 dalgaları, yeni personel
çekimleri, yer tutucuların gerçek medyayla değişimi ve doğrulama bölümü.

### 4. Kirpik ailesi storytelling scroll — planlandı, medya incelendi

Plan: `plans/claude/20261007/kirpik-storytelling-scroll.md`

Hazır olanlar: 5 sayfalık hikâye haritası; 13 kirpik görselinin ölçümü ve 6'sının
görsel doğrulaması; crop/delogo/grade reçetesi; video arama protokolü.

Kalanlar: sunucuda `instagram.db` ile kirpik videosu araması (en fazla 3),
`17986864907913512` kontrolü, manifest + `build_media.py`, story motoru, 3 yeni
görünüm, lifting yeniden yazımı, Artifact v5 (Lazer v4 sonrası), doğrulama.

Önerilen geliştirme sırası: **Lazer → PMU → Cilt Atlası**; kirpik dosya bütçesi
nedeniyle Lazer v4'ten sonra gelir.

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

Kirpik görsel incelemesi (10-07):

- `ipek-kirpik-1..6` ve `ipek-kirpik-cift` Instagram şablonunda “İPEK KİRPİK”
  hapı ve imza yazısı taşıyor; manifestte crop yok. `ipek-kirpik-*` için üst
  1:1 kırpma hapı siler; `ipek-kirpik-cift` sonrasında hap irisin üstünde,
  silinmez.
- `kirpik-makro-2` (`17885561247405556`): ailenin en yumuşak karesi; sahnede
  kullanılmaz.
- `ipek-kirpik-5` (`17917970235180938`): alt metin “Hacimli” yanlış; doğal
  klasik görünüm.
- `17986864907913512` PMU'dan elendi ama lifting sayfası için aday.

Manifest eski kayıtları hâlâ içerebilir. Cilt geliştirmesinde planın son kararı
manifestteki eski varlıktan üstündür. Lazer için gerçek “önce/sonra” yoktur;
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
