# Claude başlangıç talimatı

Web sitesi, Artifact, fotoğraf veya video işi yapmadan önce kökteki
`AI_HANDOFF.md` dosyasını; otomatik işleme gerekiyorsa `AI_CONTEXT.json`
dosyasını oku.

- Aynı Artifact'i geliştir: <https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM>
- Yeni Artifact oluşturma.
- Medyayı topluca açma. Önce `scripts/ai_media_lookup.py` ile manifest/index
  içinden en fazla 3–6 görsel veya 1–3 video kısa listele.
- Instagram için `instagram.db` kullan; `media.json` kullanma.
- Planların “hazır” ve “kalan” durumu `AI_CONTEXT.json` içindedir.
- Canlı siteye açık sahip onayı olmadan uygulama yapma.

Başlangıç:

```bash
python3 scripts/ai_media_lookup.py summary
python3 scripts/ai_media_lookup.py search lazer --family lazer --limit 6
```
