# Selda Gençer Beauty — Website Studio

Web sitesi, Claude Artifact prototipi, geliştirme planları, medya kütüphanesi ve ölçüm koruma sistemi için ortak çalışma deposu.

## AI ajanları: önce buradan başla

- İnsan/ajan handoff: [AI_HANDOFF.md](AI_HANDOFF.md)
- Makine-okunur durum: [AI_CONTEXT.json](AI_CONTEXT.json)
- Claude başlangıcı: [CLAUDE.md](CLAUDE.md)
- Codex/diğer ajan kuralları: [AGENTS.md](AGENTS.md)
- Medyayı açmadan sorgulama: `python3 scripts/ai_media_lookup.py summary`
- Ölçüm koruma sistemi: [TAGCTX_RUNBOOK.md](TAGCTX_RUNBOOK.md)
- Claude slash-skill: [/.claude/skills/tagctx/SKILL.md](.claude/skills/tagctx/SKILL.md)

Ajanlar 548 işlenmiş dosyayı veya 100 ham videoyu topluca incelememeli. Önce
manifest ve medya indeksinden en fazla 3–6 görsel ya da 1–3 video kısa listelemeli.

HTML/JS, CTA, form, Consent Mode, GTM veya dönüşüm kodu değişirse TagCtx deploy
kapısı zorunludur. `audit --record`, `diff`, runtime `verify` ve
`patches/verify_tags.sh` geçmeden ölçümün korunduğu söylenmez.

## Yapı

- `website/index.html` — geliştirilebilir ve tarayıcıda açılabilir ATELİER prototipi
- `website/m/ig/` — web için seçilmiş/işlenmiş 548 fotoğraf, video, poster ve film karesi
- `originals/instagram/videos/` — Instagram dışa aktarımından 100 ham video
- `sources/media_ig_20261007/` — medya üretim betiği ve manifest
- `sources/atelier_lazer_20261007/` — lazer sayfaları prototip kaynakları
- `plans/claude/20261007/` — lazer, kalıcı makyaj ve Cilt Atlası planları
- `prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/` — Artifact HTML anlık görüntüsü
- `tag_ctx.py`, `adsai/tag_*.py`, `tagtools/` — TagCtx ölçüm denetimi
- `patches/verify_tags.sh` — deploy sonrası ölçüm kapısı
- `.github/workflows/tagctx-live.yml` — günlük ve push sonrası canlı runtime monitörü

## Aktif Artifact

https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM

Yeni bir Artifact oluşturmak yerine bu Artifact geliştirilmeye devam edilir.

## Kaynak notları

Ana Instagram veri kaynağı sunucudaki `instagram.db` dosyasıdır; `media.json` kullanılmaz. Veritabanı, gizli yapılandırmalar ve ham fotoğraf arşivinin tamamı GitHub deposuna eklenmemiştir. Web için işlenmiş medya ile ham videolar depodadır.

TagCtx anahtar veya tarayıcı ikilisi içermez. `.env`, GTM service-account JSON'u,
`tagtools/node_modules/` ve `tagtools/browsers/` Git'e konmaz.

İlk aktarım yerel kaynak commit’i: `5f3ec85`.
AI handoff commit’i: `932b3a8`.
TagCtx kaynak commit’i: `fbfada5`.
