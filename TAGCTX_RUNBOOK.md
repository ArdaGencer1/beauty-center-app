# TagCtx ölçüm koruma sistemi

Son canlı doğrulama: **2026-10-07 16:29 Europe/Istanbul**

TagCtx, web sitesinin gerçekten gönderdiği ölçüm sinyallerini Google Ads
envanteri, GTM container'ları, Consent Mode sırası, nginx'in servis ettiği
`.gz` dosyaları ve canlı tarayıcı davranışıyla çapraz doğrular. Salt okunurdur;
siteyi veya reklam hesabını değiştirmez.

## Ajanlar için zorunlu kural

`website/`, canlı `public_html`, HTML/JS, CTA, form, WhatsApp/telefon bağlantısı,
Consent Mode, GTM veya dönüşüm koduna dokunan her işten sonra TagCtx çalıştırılır.
TagCtx geçmeden “ölçüm bozulmadı” veya “iş tamamlandı” denmez.

## Kaynak haritası

- CLI: `tag_ctx.py`
- Statik site taraması: `adsai/tag_surface.py`
- Google Ads dönüşüm envanteri: `adsai/tag_account.py`
- Site × hesap çapraz denetimi: `adsai/tag_audit.py`
- Canlı endpoint kontrolü: `adsai/tag_endpoints.py`
- GTM web/server container okuması: `adsai/tag_gtm.py`
- Playwright canlı doğrulaması: `adsai/tag_runtime.py`
- Geçmiş/diff kaydı: `adsai/tag_store.py`
- Sağlık entegrasyonu: `adsai/tag_doctor.py`
- Deploy kapısı: `patches/verify_tags.sh`
- Tarayıcı probu: `tagtools/tag_probe.mjs`
- Claude slash-skill: `.claude/skills/tagctx/SKILL.md`

## İlk kurulum

Python:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-tagctx.txt
```

Playwright Chromium ikili dosyaları Git'e konmaz. Yaklaşık 658 MB'tır ve
yeniden kurulabilir:

```bash
npm ci --prefix tagtools
cd tagtools
PLAYWRIGHT_BROWSERS_PATH="$PWD/browsers" npx playwright install chromium
```

`.env` ve GTM service-account JSON dosyaları Git'e konmaz. Çevrimiçi Google Ads
envanteri için mevcut sunucu `.env` değerleri, GTM için yalnız dosya yolunu
taşıyan `ADSAI_GTM_KEY` kullanılır.

## Günlük kullanım

```bash
# En önemli çapraz denetim
./run tag_ctx.py audit

# Canlı deploy kapısı: ölçüm hitlerini Google'a ulaştırmadan yakalar
./run tag_ctx.py verify

# Bütün sayfalar
./run tag_ctx.py sweep

# Statik yüzey, eksik sayfalar, endpoint ve GTM
./run tag_ctx.py surface
./run tag_ctx.py coverage
./run tag_ctx.py endpoints
./run tag_ctx.py gtm
```

Makine çıktısı için her komuta `--json`; Google Ads API olmadan son önbelleği
kullanmak için uygun komutlara `--offline` eklenebilir.

## Deploy kapısı

Sunucuda, site değişikliğinden sonra:

```bash
./run tag_ctx.py audit --record
./run tag_ctx.py diff
./run tag_ctx.py verify --pages index.html,degisen-sayfa.html
patches/verify_tags.sh index.html,degisen-sayfa.html
```

`verify_tags.sh`, eski ve bilinen açıkları yeni deploy hatası saymaz. Önce audit
kaydeder, sonra yalnız yeni açılmış kritik bulguları `diff` ile yakalar; canlı
tarayıcı doğrulamasını ise mutlak kapı olarak uygular.

## Güvenlik ve yanlış pozitifleri önleme

- `ads-tracking.js` üzerinde normal `grep` kullanma. Dosyada ham kontrol
  baytları vardır; byte okuyup `errors="replace"` ile çözmek gerekir.
- `public_html` bir release symlink'idir; çözülmüş hedef okunur.
- nginx `gzip_static` açıksa `.gz` ikizi gerçek kullanıcıya gider. Düz dosya ve
  açılmış `.gz` baytları aynı olmalıdır.
- Hesap tarafındaki “enabled/primary” durumu tek başına etiketin çalıştığını
  kanıtlamaz. Statik site + GTM + gerçek tarayıcı birlikte kontrol edilir.
- Runtime probu Google ölçüm isteklerini kaydeder ve iptal eder. `--live-hits`
  kullanılmaz; aksi halde test trafiği gerçek dönüşüm sinyaline dönüşür.
- Yazma yapan attribution/contact endpointleri varsayılan olarak yoklanmaz.
  `--probe-writes` ancak bunun veri yazacağı açıkça kabul edildiğinde kullanılır.
- Dönüşüm aksiyonu, goal, etiket veya GTM değişikliği ayrı ve açık insan onayı
  gerektirir; TagCtx'in kendisi böyle bir değişiklik yapmaz.

## 2026-10-07 doğrulanmış başlangıç çizgisi

- Runtime örneği: **5/5 temiz**.
- Tarayıcı konsol hatası: **0**.
- Ana Ads destination `AW-11538067972`: beş sayfanın tamamında görüldü.
- Statik/hesap audit: **2 kritik, 3 uyarı, 1 bilgi**. Bunlar yeni repo
  paketlemesinden önce de vardı; güncel gerçek için her zaman audit yeniden
  çalıştırılır.
- Bilinen iki kritik kimlik:
  `dead_primary::7766869428` ve
  `unreachable_endpoint::seldagencerbeauty.com/api/meta-conversions`.

Makine-okunur başlangıç çizgisi `tagctx-baseline.json` dosyasındadır.

## GitHub canlı monitörü

`.github/workflows/tagctx-live.yml`, tracking/site kaynakları ana dala geldiğinde,
elle çalıştırıldığında ve günlük zamanlamada canlı 5 sayfalık runtime kontrolü
yapar. Bu kontrol deploy öncesi sunucu kapısının yerine geçmez; deploy sonrası
erken uyarı katmanıdır.
