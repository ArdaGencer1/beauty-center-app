# Website build status

Son güncelleme: **2026-10-07**

## Ana sürüm

- Repo içinde açılacak ana dosya: `website/index.html`
- Aynı içeriğin Artifact çalışma kopyası:
  `prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/artifact-current.html`
- Korunan geri dönüş tabanı:
  `prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/artifact-v3.html`
- Tekrarlanabilir üretici: repoda `sources/atelier_lazer_20261007/build_artifact.py`,
  sunucuda `patches/atelier_lazer_20261007/build_artifact.py`

`artifact-v3.html` tarihsel anlık görüntüdür; geliştirmeye veya yayınlamaya
`artifact-current.html` / `website/index.html` üzerinden devam edilir.

## Bu birleşimde tamamlananlar

- Artifact v3 tasarımı, işlenmiş Instagram medyası ve gelişmiş lazer motoru tek
  HTML girişinde birleştirildi.
- Lazer sayfasına vücut/yüz bölge seçimi, CRM süreleri, 8 seans anlatımı,
  takvim, cihaz noktaları, gerçek salon videoları, yorumlar, hijyen ve WhatsApp
  randevu davetiyesi bağlandı.
- Başka uzmana ait `kas-cift-3` ile Cilt planında reddedilmiş eski medya görünür
  vitrinden çıkarıldı.
- Arşivde hiç bulunmayan yedi placeholder dosya doğrulanmış salon medyasıyla
  değiştirildi; eksik PNG monogram yerine repo içi `website/m/monogram.svg`
  eklendi.
- HTML başlığı/metadata yapısı düzeltildi.
- Ziyaretçi tarafındaki prototip modu seçicisi kaldırıldı; site yalnızca
  **A / Tam Şölen** sunumunda çalışıyor ve mevcut renk sistemi korunuyor.
- Medya referansı denetimi: **47/47 mevcut, 0 eksik**.
- JavaScript sözdizimi, benzersiz DOM kimlikleri ve deterministik rebuild geçti.
- Playwright: 1440 px masaüstü ve 390 px mobil; **0 yatay taşma, 0 konsol
  hatası, 0 yerel istek hatası**. Lazer seçimi ve planlayıcı etkileşimi geçti.

## Bilerek tamamlanmış sayılmayanlar

- Claude Artifact URL'sine yayınlama ve yayınlanan sürümü geri okuma.
- Canlı `seldagencerbeauty.com` dosyalarını değiştirme / `--apply`.
- PMU “Şölen” arayüzünün planlanan yeni sahneleri ve paket üreticileri.
- Cilt Atlası'nın planlanan 25 ayrı sayfası, medya v2 ve yeni personel çekimleri.

Bu maddeler bitmeden Artifact, PMU veya Cilt Atlası için “tamamlandı” denmez.
Canlı uygulama ayrıca sahip onayı, dry-run ve TagCtx kapılarından geçmelidir.

## Yeniden üretme ve kısa doğrulama

```bash
python3 patches/atelier_lazer_20261007/build_artifact.py
sha256sum website/index.html \
  prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/artifact-current.html
```

İki SHA-256 değeri aynı olmalıdır.
