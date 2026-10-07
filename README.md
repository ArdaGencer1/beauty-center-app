# Selda Gençer Beauty — Website Studio

Web sitesi, Claude Artifact prototipi, geliştirme planları ve medya kütüphanesi için ortak çalışma deposu.

## AI ajanları: önce buradan başla

- İnsan/ajan handoff: [AI_HANDOFF.md](AI_HANDOFF.md)
- Makine-okunur durum: [AI_CONTEXT.json](AI_CONTEXT.json)
- Claude başlangıcı: [CLAUDE.md](CLAUDE.md)
- Codex/diğer ajan kuralları: [AGENTS.md](AGENTS.md)
- Medyayı açmadan sorgulama: `python3 scripts/ai_media_lookup.py summary`

Ajanlar 568 işlenmiş dosyayı veya 100 ham videoyu topluca incelememeli. Önce
manifest ve medya indeksinden en fazla 3–6 görsel ya da 1–3 video kısa listelemeli.

## Yapı

- `website/index.html` — geliştirilebilir ve tarayıcıda açılabilir ATELİER prototipi
- `website/m/ig/` — web için seçilmiş/işlenmiş 568 fotoğraf, video, poster ve film karesi
- `originals/instagram/videos/` — Instagram dışa aktarımından 100 ham video
- `sources/media_ig_20261007/` — medya üretim betiği ve manifest
- `sources/atelier_lazer_20261007/` — lazer sayfaları prototip kaynakları
- `sources/media_vucut_20261007/` — vücut/incelme medya manifesti, üretim betiği ve ham video ön elemesi
- `sources/atelier_vucut_20261007/` — 9 vücut sayfasının Artifact derleyicisi
- `plans/claude/20261007/` — lazer, kalıcı makyaj, Cilt Atlası ve Vücut planları
- `prototypes/claude-artifact/WmsLiPPTLdnrjSrdYSXcLM/` — Artifact HTML anlık görüntüleri (güncel: `artifact-v5.html`)

## Aktif Artifact

https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM

Yeni bir Artifact oluşturmak yerine bu Artifact geliştirilmeye devam edilir.

## Kaynak notları

Ana Instagram veri kaynağı sunucudaki `instagram.db` dosyasıdır; `media.json` kullanılmaz. Veritabanı, gizli yapılandırmalar ve ham fotoğraf arşivinin tamamı GitHub deposuna eklenmemiştir. Web için işlenmiş medya ile ham videolar depodadır.

İlk aktarım yerel kaynak commit’i: `5f3ec85`.
