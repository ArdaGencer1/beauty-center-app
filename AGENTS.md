# AI agent başlangıç talimatı

Her web sitesi, Artifact, fotoğraf veya video işinden önce:

1. `AI_HANDOFF.md` dosyasını oku.
2. Makine-okunur yollar ve plan durumları için `AI_CONTEXT.json` kullan.
3. Medyayı topluca açma. Önce `scripts/ai_media_lookup.py` ile en fazla 3–6 görsel veya 1–3 video kısa listele.
4. Mevcut Artifact'i geliştir: https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM
5. Yeni Artifact oluşturma.
6. Instagram için `instagram.db` kullan; `media.json` kullanma.
7. Bitiş kapılarının tamamı geçmeden planı “tamamlandı” sayma.
8. Açık sahip onayı olmadan canlı siteye uygulama yapma.

Başlangıç komutları:

```bash
python3 scripts/ai_media_lookup.py summary
python3 scripts/ai_media_lookup.py search lazer --family lazer --limit 6
python3 scripts/ai_media_lookup.py show lazer-film-jel
```
