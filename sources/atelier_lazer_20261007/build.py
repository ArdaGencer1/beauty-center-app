#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ATELIER · FAZ L live patch -- the 7 laser pages of seldagencerbeauty.com.

  build.py --out DIR            write patched copies of the 7 pages (+ assets) into DIR; the site is not touched
  build.py --out DIR --check    ... and run the gates on them (exit 1 on any failure)
  build.py --apply              owner only: back up, patch in place, gzip, copy media/assets (refuses if a gate fails)
  build.py --rollback           restore every page from its .bak-20261007-atlz backup, remove the copied assets
  --site DIR                    public_html (default /var/www/seldagencerbeauty.com/public_html)

What changes in each page (everything else stays byte for byte):
  head   + lazer.css / fonts (critical part inline), hero poster preload; the old hero image preload goes
  body   <header class="hero…"> -> the ATELIER laser vitrine (render.py); the H1 text is the page's own, unchanged
         old sections stay, as visible text, under "Detaylı bilgi"; lp-sticky-actionbar -> the laser bar (lazer.js)
         JSON-LD "image" -> the new hero photo
  kampanya page: NAP "Yaşamkent" -> "Konutkent", "LazerMech" -> "Lasermach", canonical -> /laser-signature
Marker <!-- SGB_ATELIER_LAZER 20261007 -->; a page that already carries it is rebuilt from its backup, never patched twice.
Not touched: styles.css, script.js (Faz 0), ads-tracking.js, sgb-offers.js, consent, gtag.
"""
from __future__ import annotations

import argparse
import gzip
import html as H
import json
import os
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import render  # noqa: E402

MARK = "<!-- SGB_ATELIER_LAZER 20261007 -->"
BAK = ".bak-20261007-atlz"
VER = "20261007-atlz"
SITE = Path("/var/www/seldagencerbeauty.com/public_html")
MEDIA_SRC = HERE.parents[1] / "website/m/ig"          # repo copy of the built media (same files as images/ig)
PAGES = {k: v["slug"] for k, v in render.PAGES.items()}  # key -> slug (7 pages)
FORBIDDEN = [r"kesin sonuç", r"%\s?100", r"\b100\s?%", r"acısız", r"en iyi", r"1 numara", r"bir numara", r"kalıcı\s+(?:çözüm|sonuç|olarak)",
             r"son\s+\d+\s+(?:kişi|yer|gün)", r"geri sayım"]
GARANTI_OK = re.compile(r"bitiş garantili", re.I)


def page_file(site: Path, slug: str) -> Path:
    for cand in (site / f"{slug}.html", site / slug / "index.html"):
        if cand.exists():
            return cand
    raise SystemExit(f"page not found for /{slug} under {site}")


# ------------------------------------------------------------------------------------------------- html helpers
def span(doc: str, start: int) -> tuple[int, int]:
    """[start, end) of the element whose start tag begins at `start` (same-name nesting counted)."""
    m = re.match(r"<([a-zA-Z][\w-]*)", doc[start:])
    tag = m.group(1).lower()
    depth, i = 0, start
    pat = re.compile(rf"<(/?){tag}\b[^>]*?(/?)>", re.I)
    for t in pat.finditer(doc, start):
        if t.group(1):
            depth -= 1
        elif not t.group(2):
            depth += 1
        if depth == 0:
            return start, t.end()
        i = t.end()
    raise ValueError(f"unclosed <{tag}> at {start}")


def text(s: str) -> str:
    s = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", H.unescape(s)).strip()


def head_facts(doc: str) -> dict:
    def one(pat):
        m = re.search(pat, doc, re.I | re.S)
        return re.sub(r"\s+", " ", m.group(1)).strip() if m else None
    h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", doc, re.I | re.S)
    return {
        "title": one(r"<title>(.*?)</title>"),
        "description": one(r'<meta\s+name="description"\s+content="([^"]*)"'),
        "canonical": one(r'<link\s+rel="canonical"\s+href="([^"]*)"'),
        "robots": one(r'<meta\s+name="robots"\s+content="([^"]*)"'),
        "h1": text(h1.group(1)) if h1 else None,
        "h1_count": len(re.findall(r"<h1\b", doc, re.I)),
        "h2": [text(x) for x in re.findall(r"<h2\b[^>]*>(.*?)</h2>", doc, re.I | re.S)],
    }


# ------------------------------------------------------------------------------------------------- transform
def critical_css() -> str:
    css = (HERE / "src/lazer.css").read_text(encoding="utf-8")
    keep = []
    for block in re.findall(r"[^{}]+\{[^{}]*\}", css.split("/* ---------- L2 map")[0]):
        keep.append(block.strip())
    return re.sub(r"\s+", " ", " ".join(keep))


def transform(doc: str, key: str) -> str:
    if MARK in doc:
        raise ValueError("already patched (marker present); rebuild from the backup")
    P = render.PAGES[key]
    facts = head_facts(doc)
    if not facts["h1"]:
        raise ValueError("no <h1>")
    out = doc
    if key == "kamp":
        out = out.replace("Yaşamkent", "Konutkent").replace("LazerMech", "Lasermach").replace("Lazermech", "Lasermach")
        out = re.sub(r'(<link\s+rel="canonical"\s+href=")[^"]*(")', r"\1https://seldagencerbeauty.com/laser-signature\2", out, count=1, flags=re.I)
    vit = render.page_html(key, "/images/ig/", facts["h1"], lambda k: "/" + render.PAGES[k]["slug"])
    data = render.page_data(key, "/images/ig/", True)
    data_tag = '<script type="application/json" id="lz-data">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>"
    # body: the hero header (holding the H1) becomes the vitrine; the old H1 is demoted so the page keeps one H1
    m = re.search(r'<header\b[^>]*class="[^"]*\bhero\b[^"]*"[^>]*>', out, re.I)
    if m:
        a, b = span(out, m.start())
        old_hero = out[a:b]
    else:
        h1m = re.search(r"<h1\b", out, re.I)
        a, b = span(out, h1m.start())
        old_hero = out[a:b]
    rest_old = re.sub(r"<h1\b([^>]*)>(.*?)</h1>", r'<p class="lz-oldh1"\1>\2</p>', old_hero, flags=re.I | re.S)
    out = out[:a] + MARK + "\n" + vit + "\n" + data_tag + out[b:]
    # old content -> "Detaylı bilgi" (visible text, kept in DOM for search engines)
    mm = re.search(r"<main\b[^>]*>", out, re.I)
    if mm:
        ma, mb = span(out, mm.start())
        inner_start = mm.end()
        inner_end = mb - len("</main>")
        body = out[inner_start:inner_end]
        i = body.find(MARK)
        if i >= 0:  # vitrine sits inside <main>: wrap only what follows it
            j = body.index('<script type="application/json" id="lz-data">', i)
            j = body.index("</script>", j) + len("</script>")
            head_part, tail = body[:j], body[j:]
        else:
            head_part, tail = "", body
        more = ('<details class="lz-more" id="detayli-bilgi"><summary data-track-label="at-' + P["code"] + '-detayli-bilgi">Detaylı bilgi</summary>'
                '<div class="lz-more-body">' + rest_old + tail + "</div></details>")
        out = out[:inner_start] + head_part + more + out[inner_end:]
    # old sticky action bar -> lazer.js bar
    sb = re.search(r'<(div|nav|aside)\b[^>]*class="[^"]*\blp-sticky-actionbar\b[^"]*"[^>]*>', out, re.I)
    if sb:
        a, b = span(out, sb.start())
        out = out[:a] + out[b:]
    # head: drop the old hero/salon image preload, add poster preload + css + fonts + script
    out = re.sub(r'\s*<link\s+rel="preload"\s+as="image"\s+href="[^"]*(?:salon|hero)[^"]*"[^>]*>', "", out, flags=re.I)
    hero = render.HERO_IMG[key]
    fonts = (HERE / "src/fonts.css").read_text(encoding="utf-8").strip()
    head_add = ("\n" + MARK + f'\n<link rel="preload" as="image" href="{hero}" fetchpriority="high">'
                f"\n<style id=\"lz-critical\">{fonts}{critical_css()}</style>"
                f'\n<link rel="stylesheet" href="/assets/atelier/lazer.css?v={VER}" media="print" onload="this.media=\'all\'">'
                f'<noscript><link rel="stylesheet" href="/assets/atelier/lazer.css?v={VER}"></noscript>'
                f'\n<script src="/assets/atelier/lazer.js?v={VER}" defer></script>\n')
    out = re.sub(r"</head>", head_add + "</head>", out, count=1, flags=re.I)
    # JSON-LD image -> new hero photo
    def ld(mo):
        try:
            obj = json.loads(mo.group(2))
        except Exception:
            return mo.group(0)
        def fix(o):
            if isinstance(o, dict):
                if "image" in o and o.get("@type") not in ("ImageObject",):
                    o["image"] = "https://seldagencerbeauty.com" + hero
                for v in o.values():
                    fix(v)
            elif isinstance(o, list):
                for v in o:
                    fix(v)
        fix(obj)
        return mo.group(1) + json.dumps(obj, ensure_ascii=False) + mo.group(3)
    out = re.sub(r'(<script\s+type="application/ld\+json"[^>]*>)(.*?)(</script>)', ld, out, flags=re.S | re.I)
    return out


# ------------------------------------------------------------------------------------------------- gates
def vitrine_part(doc: str) -> str:
    i = doc.find('<div class="lz" data-lz-page=')
    j = doc.find('id="lz-data"', i)
    return doc[i:j] if i >= 0 else ""


def gates(key: str, before: str, after: str) -> list[str]:
    fail = []
    A, B = head_facts(before), head_facts(after)
    for k in ("title", "description", "robots"):
        if A[k] != B[k]:
            fail.append(f"{k} changed: {A[k]!r} -> {B[k]!r}")
    if key == "kamp":
        if B["canonical"] != "https://seldagencerbeauty.com/laser-signature":
            fail.append(f"kampanya canonical not merged: {B['canonical']}")
    elif A["canonical"] != B["canonical"]:
        fail.append(f"canonical changed: {A['canonical']} -> {B['canonical']}")
    if A["h1"] != B["h1"] or B["h1_count"] != 1:
        fail.append(f"H1 changed or not unique: {A['h1']!r} -> {B['h1']!r} (x{B['h1_count']})")
    miss = [h for h in A["h2"] if h not in B["h2"] and h not in text(after)]
    if miss:
        fail.append(f"old H2 missing: {miss}")
    if "yaşamkent" in text(after).lower() and key == "kamp":
        fail.append("Yaşamkent NAP still present")
    vit = vitrine_part(after)
    # verbatim Google reviews are the customers' own words (plan §6); the rules apply to our copy
    vt = text(re.sub(r'<article class="lz-rv".*?</article>', " ", vit, flags=re.S)).lower()
    for pat in FORBIDDEN:
        if re.search(pat, vt, re.I):
            fail.append(f"forbidden phrase /{pat}/ in vitrine")
    if re.search(r"garanti", GARANTI_OK.sub("", vt)):
        fail.append("'garanti' outside 'bitiş garantili'")
    for tag in re.findall(r"<(?:a|button)\b[^>]*>", vit):
        if "data-track-label=" not in tag:
            fail.append(f"unlabeled control: {tag[:90]}")
            break
    labels = re.findall(r'data-track-label="([^"]+)"', vit)
    bad = [x for x in labels if not re.fullmatch(r"at-[a-z0-9-]{1,45}", x)]
    if bad:
        fail.append(f"bad track labels: {bad[:4]}")
    for s in ("script.js", "ads-tracking.js", "sgb-offers.js"):
        if s in before and s not in after:
            fail.append(f"{s} lost")
    if after.count(MARK) != 2:
        fail.append("marker count != 2")
    for blob in re.findall(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>', after, re.S):
        try:
            json.loads(blob)
        except Exception as e:
            fail.append(f"JSON-LD invalid: {e}")
    srcs = set(re.findall(r'/images/ig/([\w.-]+)', after))
    gone = [s for s in srcs if not (MEDIA_SRC / s).exists()]
    if gone:
        fail.append(f"media missing from build: {gone[:5]}")
    kb = len(vit.encode()) // 1024
    if kb > 260:
        fail.append(f"vitrine markup {kb} KB > 260 KB")
    return fail


# ------------------------------------------------------------------------------------------------- io
def write_like(dst: Path, data: str, like: Path | None) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + ".tmp-atlz")
    tmp.write_text(data, encoding="utf-8")
    if like and like.exists():
        st = like.stat()
        os.chmod(tmp, st.st_mode & 0o7777)
        try:
            os.chown(tmp, st.st_uid, st.st_gid)
        except PermissionError:
            pass
    os.replace(tmp, dst)
    with open(dst, "rb") as f, gzip.open(str(dst) + ".gz", "wb", compresslevel=9) as g:
        shutil.copyfileobj(f, g)


def media_files(docs: list[str]) -> set[str]:
    out = set()
    for d in docs:
        out |= set(re.findall(r'/images/ig/([\w.-]+)', d))
    return out


def assets(dst_root: Path, docs: list[str], like: Path | None) -> list[Path]:
    made = []
    a = dst_root / "assets/atelier"
    a.mkdir(parents=True, exist_ok=True)
    for name in ("lazer.css", "lazer.js"):
        write_like(a / name, (HERE / "src" / name).read_text(encoding="utf-8"), like)
        made += [a / name, a / (name + ".gz")]
    f = dst_root / "fonts"
    f.mkdir(parents=True, exist_ok=True)
    for w in (HERE / "fonts").glob("*.woff2"):
        if not (f / w.name).exists():
            shutil.copy2(w, f / w.name)
            made.append(f / w.name)
    ig = dst_root / "images/ig"
    ig.mkdir(parents=True, exist_ok=True)
    for name in sorted(media_files(docs)):
        if not (ig / name).exists() or (ig / name).stat().st_size != (MEDIA_SRC / name).stat().st_size:
            shutil.copy2(MEDIA_SRC / name, ig / name)
            made.append(ig / name)
    return made


def sitemap_images(site: Path, docs: dict[str, str]) -> str | None:
    sm = site / "sitemap-images.xml"
    if not sm.exists():
        return None
    xml = sm.read_text(encoding="utf-8")
    if MARK in xml:
        return None
    add = []
    for key, d in docs.items():
        if key == "kamp":
            continue
        loc = f"https://seldagencerbeauty.com/{render.PAGES[key]['slug']}"
        imgs = sorted(set(re.findall(r'/images/ig/(lazer-[\w-]+-(?:800|1200)\.webp|lazer-film-[\w]+-poster\.webp)', d)))[:8]
        add.append(f"<url><loc>{loc}</loc>" + "".join(f"<image:image><image:loc>https://seldagencerbeauty.com/images/ig/{i}</image:loc></image:image>" for i in imgs) + "</url>")
    return xml.replace("</urlset>", MARK + "\n" + "\n".join(add) + "\n</urlset>")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", type=Path, default=SITE)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--rollback", action="store_true")
    a = ap.parse_args()
    site = a.site
    if a.rollback:
        n = 0
        for key, slug in PAGES.items():
            p = page_file(site, slug)
            b = p.with_name(p.name + BAK)
            if b.exists():
                shutil.copy2(b, p)
                with open(p, "rb") as f, gzip.open(str(p) + ".gz", "wb", compresslevel=9) as g:
                    shutil.copyfileobj(f, g)
                n += 1
        sb = site / ("sitemap-images.xml" + BAK)
        if sb.exists():
            shutil.copy2(sb, site / "sitemap-images.xml")
        for x in ("lazer.css", "lazer.js"):
            for suf in ("", ".gz"):
                q = site / "assets/atelier" / (x + suf)
                if q.exists():
                    q.unlink()
        print(f"rollback: {n} pages restored from {BAK}; media under images/ig left in place (harmless, unreferenced)")
        return 0
    before, after = {}, {}
    for key, slug in PAGES.items():
        p = page_file(site, slug)
        b = p.with_name(p.name + BAK)
        src = b.read_text(encoding="utf-8") if (b.exists() and MARK in p.read_text(encoding="utf-8")) else p.read_text(encoding="utf-8")
        before[key] = src
        after[key] = transform(src, key)
    failed = False
    if a.check or a.apply:
        for key in PAGES:
            f = gates(key, before[key], after[key])
            print(f"{'OK ' if not f else 'FAIL'} /{PAGES[key]:<36} {len(after[key].encode()) // 1024:>4} KB")
            for x in f:
                print("     -", x)
            failed |= bool(f)
    if a.out:
        for key, slug in PAGES.items():
            p = page_file(site, slug)
            write_like(a.out / p.relative_to(site), after[key], None)
        assets(a.out, list(after.values()), None)
        sm = sitemap_images(site, after)
        if sm:
            write_like(a.out / "sitemap-images.xml", sm, None)
        print(f"out: {a.out} ({len(PAGES)} pages, {len(media_files(list(after.values())))} media files)")
    if a.apply:
        if failed:
            print("apply refused: a gate failed")
            return 1
        for key, slug in PAGES.items():
            p = page_file(site, slug)
            b = p.with_name(p.name + BAK)
            if not b.exists():
                shutil.copy2(p, b)
            write_like(p, after[key], p)
        made = assets(site, list(after.values()), page_file(site, PAGES["hub"]))
        sm = sitemap_images(site, after)
        if sm:
            smp = site / "sitemap-images.xml"
            if not (site / ("sitemap-images.xml" + BAK)).exists():
                shutil.copy2(smp, site / ("sitemap-images.xml" + BAK))
            write_like(smp, sm, smp)
        print(f"applied: {len(PAGES)} pages, {len(made)} asset/media files; rollback: build.py --rollback")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
