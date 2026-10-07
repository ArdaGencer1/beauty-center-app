# AI handoff — web sitesi, Artifact ve medya

Son doğrulama: **2026-10-07**

Bu dosyayı web sitesi, Claude Artifact veya Instagram medyası üzerinde çalışmaya
başlamadan önce oku. Amaç, her yeni ajanın yüzlerce fotoğrafı ve videoyu yeniden
inceleyerek token harcamasını önlemektir.

## Değiştirilemez çalışma kuralları

- Mevcut Claude Artifact geliştirilecek; yeni Artifact oluşturulmayacak:
  <https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM>
- Depodaki son kaynak anlık görüntüsü **Artifact v17**'dir (`artifact-v17.html`, Artifact sürüm id `1791389678-02bc`, yayındakiyle bayt bayt aynı). İçeriği: tırnak, kaş "beş perde", 5 lazer alt sayfası, Cilt Atlası ve "mobil düzen" oturumlarının işleri (sürüm 8–16) + 9 vücut sayfası + ortak mobil katmanı. Tabanı `artifact-taban-1791388726-c3e0.html`. Aynı Artifact'i birden çok oturum sık yayınlıyor: yayından hemen önce yayındaki sürümü okuyun. v3 yalnızca tarihçe için durur. Artifact üzerinde bu
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
| İşlenmiş medya | `website/m/ig/` | 568 dosya (20'si `vucut-*`); topluca açma. |
| Medya indeksi | `website/m/ig/media_index.json` | 121 slug (10'u `fam: "vucut"`); dosya, poster, boyut, süre, Instagram ID ve permalink bilgisi. İlk bakılacak medya kaynağı. |
| Seçim manifesti | `sources/media_ig_20261007/manifest.json` | 111 seçilmiş kayıt ve açık dışlama nedenleri. |
| Medya üreticisi | `sources/media_ig_20261007/build_media.py` | Crop, hizalama, poster, video ve varyant üretim kuralları. |
| Vücut medyası | `sources/media_vucut_20261007/` | `manifest_vucut.json` (10 kalem), `build_vucut.py` (depodaki ham videolardan üretir), `triage_videos.tsv` (74 sınıflandırılmamış ham videonun ön elemesi; bu videolar yeniden taranmaz). |
| Ham videolar | `originals/instagram/videos/` | 100 video; yalnızca seçilen Instagram ID/slug için aç. |
| Lazer kaynakları | `sources/atelier_lazer_20261007/` | `render.py`, `src/lazer.css`, `src/lazer.js` ve doğrulanmış veri. |
| Artifact anlık görüntüsü | `prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/artifact-v17.html` | Yayındaki sürüm 17. Tabanı `artifact-taban-1791388726-c3e0.html` (sürüm 16'dan vücut eklemeleri çıkarılmış hâli); eski: `artifact-v7.html`, `artifact-v5.html`, `artifact-v6-tirnak-taban.html`, `artifact-v4-tirnak.html`, ilk sürüm `artifact-v3.html`. |
| Vücut sayfaları + mobil katmanı | `sources/atelier_vucut_20261007/` | `build.py` (tabana yama + `src/vucut.css` + `src/vucut.js` + `src/mobil.css` + `lazy_hidden()`, `--check`, `--publish DIR`). Başka oturum yeni sürüm yayınlarsa: yayındakini oku (`index.html`), `rebase.py YAYINDAKI.html --rev $(git log -1 --format=%h -- sources/atelier_vucut_20261007) --out .../artifact-taban-<id>.html` ile yeni taban yaz (betik, o revizyonla yeniden derlemenin yayındakiyle bayt bayt aynı olduğunu doğrular), `BASE`'i çevir, derle, test et, yayınla. |
| Güncel planlar | `plans/claude/20261007/` | Lazer, PMU, Cilt Atlası ve Vücut planları. |

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

Ana manifestte toplam **111** kayıt, vücut ek manifestinde **10** kayıt vardır
(`ai_media_lookup.py` ikisini birlikte okur):

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
| Vücut (ek manifest `manifest_vucut.json`) | 10 |

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

### 4. Vücut atölyesi — 9 sayfa Artifact'te (sürüm 17), sunucu adımları bekliyor

Plan: `plans/claude/20261007/vucut-inceltme-sayfalari.md`
(önizleme: `plans/claude/20261007/vucut-medya-onizleme.jpg`)

Hazır olanlar: 74 ham videonun ön elemesi (`triage_videos.tsv`); 10 işlenmiş
vücut kalemi / 20 dosya (`vucut-g5`, `vucut-slimtone-kol`,
`vucut-slimtone-cihaz`, `vucut-slimtone-yuz`, `vucut-lenf`, `vucut-kol`,
`vucut-gobek`, `vucut-cift-tam`, `vucut-gobek-yan`, `vucut-cihaz-masa`); `build_vucut.py`;
9 sayfalık sayfa-medya matrisi, çekim listesi ve dalga planı.

Sahip kararları (2026-10-07): siyah başlık = G5; kule cihaz = Slim Tone;
bölgesel incelme = Slim Tone + G5 + lenf drenaj programı; medyası olmayan
sayfalara temsilî görsel/çizim, sunucu en son. V1 ve V2 aynı Artifact'te
yayında (sürüm 5'ten beri; güncel sürüm 17). Mobil denetim ve düzeltmeler planın 10. bölümünde.

Kalanlar: açık sahip soruları (EM = Slim Tone mu, sehpadaki cihaz, heykeltraş,
pasif jimnastik, CRM fiyatları, çatlak protokolü). Sahip 2026-10-07'de "tam
bilmiyorum" dedi: bu sayfalar teyide kadar temsilî görsel/çizimle kalır; cevap
salon kayıtlarından veya personelden alınmalı. Sunucuda IG başlık araması,
540 px tam çözünürlük ve canlı sayfa denetimi; çekimler; canlı için dry-run ve
sahip onayı.

### 5. Ortak mobil katmanı — bütün sayfalar (sürüm 17)

Kaynak: `sources/atelier_vucut_20261007/src/mobil.css`, `build.py` (`MOBIL_PATCHES`, `lazy_hidden()`).
Ayrıntı ve ölçümler: `plans/claude/20261007/vucut-inceltme-sayfalari.md` §10. Başka bir oturumun
`<style id="mobil-duzen">` bloğu (yön, çentik, kahraman yüksekliği) ayrıdır ve onunla uyumludur.

- Gizli görünümlerdeki görseller `loading="lazy"` alır (salon ve tırnak hariç). İlk yüklemede inen veri
  vücutta 767 → 207 KB, salonda 1,65 → 1,09 MB oldu. **Yeni görünüm ekleyen oturumlar:** ana görsele
  `fetchpriority="high"` tek başına yetmez, gizli görünümde her sayfa açılışında iner; `loading="lazy"`
  ekleyin (görünüm açılınca hemen iner) ya da derlemeyi bu katmanla yapın.
- SSS satırının tamamı dokunulabilir (`.faq summary` iç boşluğu); görünüm aynı.
- Galeri "basılı tutun" iPhone'da resim menüsünü açmaz (`-webkit-touch-callout:none`).
- Menüde bulunulan grubun kısayolu işaretli; kısayollar ve lazer "Kadın / Erkek" dokunmatikte ≥ 38 px.
- Alt çubuk yazısı 320 px'te sığar (dar ekranda boşluk ve yazı küçülür). Yeni çubuk metni ≤ 29 karakter olsun.
- Öneri (lazer oturumu): 6 lazer sayfası aynı ~39 KB'lık vücut haritası SVG'sini ayrı ayrı gömüyor
  (~230 KB HTML); tek kopyadan JS ile çoğaltmak telefonda sayfayı belirgin hafifletir.
- Yeni bir kahraman sahne sınıfı eklenirse "mobil düzen"in dikey/yatay `height:100%` kuralına da eklenmeli
  (vücut `.vb-stage`/`.vb-split` için `src/vucut.css` içinde eklendi; eklenmezse 320 px'te ve yatayda taşar).

Önerilen geliştirme sırası: **Lazer → PMU → Cilt Atlası → Vücut**.

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

Vücut planında verilen kararlar:

- `bolgesel-cift` sütun bölmesi yerine `vucut-gobek` / `vucut-kol` çeyrek
  kırpımları kullanılır (2×2 kolaj; sütunlarda monogram çeyreği kalıyordu).
- `17883457215458159`: LASERMACH bacak videosu; lazer, vücut incelme değil.
- `18089498999286039`: el bakımı (gümüş eldiven); vücut değil.
- `vucut-cihaz-masa` sahip teyidi olmadan yayınlanmaz. Önce/sonra sonucu yalnızca
  Slim Tone + G5 + lenf drenaj programının sonucu olarak etiketlenir.
- Artifact dosya sınırı: bir yayında en çok 255 dosya, bir sürümde 511. Dosya sayısı
  başka oturumların medyasıyla artıyor (`Artifact list scope=files`); güncellemede yalnızca
  yeni/değişen dosyaları gönderin.
- Kaş sayfası artık `kas-cift-3` kullanmıyor (manifest bunu başka uzmana ait diye
  dışlamıştı, `18516297502030856`). Sahip onayıyla (2026-10-07) sürüm 7'de çıkarıldı;
  iki `kas-cift-3` dosyası Artifact'ten silindi. Kaş oturumu Altın Oran aynasını
  sonra kendi `kas-perde-alim-800.webp` fotoğrafına geçirdi ("beş perde" bölümü);
  `kas-cift-3` geri gelmedi. Canlı sitede bu fotoğrafın kullanılıp kullanılmadığı
  sunucudaki sayfa denetiminde kontrol edilmeli; değişiklik canlıya yalnızca sahip
  onayıyla uygulanır.

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
