#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ATELIER · FAZ L -- the laser family's markup, written once for both targets.

build.py (live site, media under /images/ig/) and the prototype's a3_build.py (artifact, media under m/ig/)
both call page_html() / page_data(); src/lazer.css + src/lazer.js enhance the markup. Everything a search
engine or a slow phone needs (H1, hero poster, region names, texts) is static HTML here; JS only adds the
interactions (map, journey, calendar, hotspots, reels, invitation).

Facts used and where they come from:
  regions, minutes, sessions  data/crm_laser.json  (live CRM price menu, prices deliberately not stored)
  reviews + 31/30 count       data/reviews_laser.json (GBP API, verbatim)
  device                      owner 10-07: Lasermach diode, 755 / 808 / 1064 nm, cooled tip (10 °C on the
                              device screen in the salon's own photo)
  session interval            owner 10-07: face 4-6 weeks, body 6-8 weeks; packages are 8 sessions (CRM)
  'bitiş garantili paket'     CRM package names (owner 10-07: may be shown)
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
WA = "905330390076"
PHONE_TEL = "+905330390076"
PHONE_TXT = "0533 039 00 76"
MAPS = "https://www.google.com/maps/search/?api=1&query=Selda+Gen%C3%A7er+Beauty+Center+Konutkent"

ICON = {
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.6.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 2.9 2.9 0 0 0-.9 2.2 5.1 5.1 0 0 0 1.1 2.7 11.6 11.6 0 0 0 4.4 3.9c1.7.7 2.3.7 3.1.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .2-1.2c-.1-.1-.3-.2-.5-.3z"/></svg>',
    "tel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "down": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="3"/><path d="M8 3v4M16 3v4M3.5 10h17"/></svg>',
    "play": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>',
    "back": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>',
}

# --------------------------------------------------------------------------------------------- regions
# id -> (display name, CRM SEANS option, zone).  zone: face | front | back | both | pkg
REGIONS = {
    "kadin": [
        ("dudak-ustu", "Dudak üstü", "DUDAK ÜSTÜ", "face"),
        ("cene", "Çene", "ÇENE", "face"),
        ("gidi", "Gıdı", "GIDI", "face"),
        ("tum-yuz", "Tüm yüz", "TÜM YÜZ", "face"),
        ("boyun", "Boyun", "BOYUN", "front"),
        ("koltuk", "Koltuk altı", "KOLTUK ALTI", "front"),
        ("gogus", "Göğüs", "GÖĞÜS", "front"),
        ("gobek", "Göbek", "GÖBEK", "front"),
        ("genital", "Genital", "GENİTAL", "front"),
        ("tum-kol", "Tüm kol", "TÜM KOL", "both"),
        ("yarim-kol", "Yarım kol", "YARIM KOL", "both"),
        ("tum-bacak", "Tüm bacak", "TÜM BACAK", "both"),
        ("yarim-bacak", "Yarım bacak", "YARIM BACAK", "both"),
        ("omuz", "Omuz", "OMUZ", "back"),
        ("sirt", "Sırt", "SIRT", "back"),
        ("bel", "Bel", "BEL", "back"),
        ("popo", "Popo", "POPO", "back"),
        ("tum-vucut-4", "Tüm vücut 4 bölge", "TÜM VÜCUT 4 BÖLGE", "pkg"),
        ("tepeden", "Tepeden tırnağa", "TEPEDEN TIRNAĞA", "pkg"),
    ],
    "erkek": [
        ("sakal-ustu", "Sakal üstü", "SAKAL ÜSTÜ", "face"),
        ("kulak", "Kulak", "KULAK", "face"),
        ("tum-yuz", "Tüm yüz", "TÜM YÜZ", "face"),
        ("boyun", "Boyun", "BOYUN", "front"),
        ("koltuk", "Koltuk altı", "KOLTUK ALTI", "front"),
        ("gogus", "Göğüs", "GÖĞÜS", "front"),
        ("gobek", "Göbek", "GÖBEK", "front"),
        ("genital", "Genital", "GENİTAL", "front"),
        ("tum-kol", "Tüm kol", "TÜM KOL", "both"),
        ("yarim-kol", "Yarım kol", "YARIM KOL", "both"),
        ("tum-bacak", "Tüm bacak", "TÜM BACAK", "both"),
        ("yarim-bacak", "Yarım bacak", "YARIM BACAK", "both"),
        ("ense", "Ense", "ENSE", "back"),
        ("omuz", "Omuz", "OMUZ", "back"),
        ("sirt", "Sırt", "SIRT", "back"),
        ("bel", "Bel", "BEL", "back"),
        ("kemer-ustu", "Kemer üstü", "KEMER ÜSTÜ", "pkg"),
        ("full-vucut", "Full vücut", "FULL VÜCUT", "pkg"),
    ],
}
SERVICE = {"kadin": "KADIN LAZER EPİLASYON", "erkek": "ERKEK LAZER EPİLASYON"}
# packages that light the whole figure / the upper body (kemer üstü = above the belt)
PKG_PARTS = {
    "tepeden": "all", "full-vucut": "all",
    "kemer-ustu": ["boyun", "ense", "gogus", "gobek", "koltuk", "omuz", "sirt", "bel", "ust-kol", "alt-kol"],
    "tum-vucut-4": [],
}
FACE_IDS = {"dudak-ustu", "cene", "gidi", "tum-yuz", "sakal-ustu", "kulak"}


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def tr_sentence(s: str) -> str:
    """'KOLTUK ALTI PAKET' -> 'Koltuk altı paket' (Turkish casing)."""
    low = s.replace("I", "ı").replace("İ", "i").lower()
    low = re.sub(r"\s+", " ", low).strip()
    if not low:
        return low
    first = {"i": "İ", "ı": "I"}.get(low[0], low[0].upper())
    return first + low[1:]


def load(name: str):
    return json.loads((HERE / "data" / name).read_text(encoding="utf-8"))


def crm_minutes() -> dict:
    """{'kadin': {'KOLTUK ALTI': (15, 15)}, ...} single-session minutes (min, max) from the CRM snapshot."""
    rows = load("crm_laser.json")["rows"]
    out = {"kadin": {}, "erkek": {}}
    for r in rows:
        g = "kadin" if r["service"].startswith("KADIN") else "erkek"
        if not r["service"].endswith("SEANS"):
            continue
        m = r.get("min") or 0
        lo, hi = out[g].get(r["name"], (m, m))
        out[g][r["name"]] = (min(lo, m), max(hi, m))
    return out


def region_list(g: str) -> list[dict]:
    mins = crm_minutes()[g]
    res = []
    for rid, name, crm, zone in REGIONS[g]:
        lo, hi = mins.get(crm, (None, None))
        res.append({"id": rid, "n": name, "crm": crm, "z": zone, "m": lo, "mx": hi})
    return res


def menu_rows(g: str) -> list[dict]:
    """Every active CRM laser row for one gender: single sessions and packages, names + minutes + sessions."""
    rows = load("crm_laser.json")["rows"]
    seans, paket = [], []
    seen = set()
    ids = {crm: rid for rid, _n, crm, _z in REGIONS[g]}
    for r in rows:
        if not r["service"].startswith(SERVICE[g]):
            continue
        is_pkg = r["service"].endswith("PAKET")
        name = r["name"]
        base = re.sub(r"\s*PAKET$", "", name).strip()
        key = (is_pkg, base, r.get("sessions"), r.get("min"))
        if key in seen:
            continue
        seen.add(key)
        garanti = "BİTİŞ GARANTİLİ" in name
        clean = re.sub(r"\s*\(?BİTİŞ GARANTİLİ\)?\s*", " ", base).strip()
        rid = ids.get(clean) if not (garanti or is_pkg) else None
        item = {"n": tr_sentence(clean), "m": r.get("min"), "s": r.get("sessions") or 1, "g": garanti, "id": rid}
        (paket if is_pkg else seans).append(item)
    # merge duplicate single-session rows that differ only by minutes (erkek genital 31 / 46)
    merged = {}
    for it in seans:
        k = it["n"]
        if k in merged:
            a = merged[k]
            a["m"], a["mx"] = min(a["m"], it["m"]), max(a.get("mx", a["m"]), it["m"])
        else:
            merged[k] = dict(it, mx=it["m"])
    seans = list(merged.values())
    paket = [p for p in paket if p["s"] and p["s"] > 1]
    return [{"t": "Tek seans", "rows": seans}, {"t": "Paket", "rows": paket}]


# --------------------------------------------------------------------------------------------- figure
def smooth(pts, t: float = 1.0) -> str:
    n = len(pts)
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(n):
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 6, p1[1] + (p2[1] - p0[1]) * t / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 6, p2[1] - (p3[1] - p1[1]) * t / 6)
        d += f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d + "Z"


def mirror(pts):
    return [(240 - x, y) for x, y in reversed(pts)]


def centroid(pts):
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


# Left-side shapes (x < 120); bilateral parts are mirrored.  viewBox 0 0 240 500.
SHAPES = {
    "kadin": {
        "neck": [(111, 66), (129, 66), (131, 92), (109, 92)],
        "chest": [(109, 90), (131, 90), (150, 96), (161, 106), (159, 128), (155, 152), (140, 162), (120, 164), (100, 162), (85, 152), (81, 128), (79, 106), (90, 96)],
        "belly": [(100, 160), (120, 163), (140, 160), (153, 172), (148, 197), (152, 218), (120, 224), (88, 218), (92, 197), (87, 172)],
        "groin": [(92, 219), (120, 226), (148, 219), (141, 238), (128, 253), (120, 257), (112, 253), (99, 238)],
        "thigh": [(88, 214), (99, 233), (113, 253), (118, 263), (116, 302), (112, 342), (104, 354), (93, 354), (87, 322), (82, 282), (82, 240)],
        "shin": [(92, 348), (112, 348), (113, 380), (109, 430), (105, 468), (96, 470), (92, 430), (88, 380)],
        "foot": [(95, 466), (107, 466), (110, 488), (100, 493), (91, 489)],
        "uarm": [(80, 101), (70, 105), (62, 120), (58, 148), (57, 180), (65, 185), (73, 182), (77, 152), (81, 126)],
        "farm": [(57, 180), (72, 180), (69, 216), (63, 250), (57, 262), (51, 262), (49, 240), (51, 212)],
        "hand": [(50, 258), (59, 258), (63, 281), (57, 293), (49, 289), (47, 275)],
        "pit": [(82, 112), (88, 116), (88, 134), (83, 140), (79, 128)],
        # back
        "shoulder": [(79, 104), (90, 96), (109, 91), (109, 106), (92, 112), (81, 120)],
        "upback": [(90, 112), (109, 106), (131, 106), (150, 112), (159, 124), (156, 152), (150, 174), (120, 178), (90, 174), (84, 152), (81, 124)],
        "lowback": [(90, 176), (120, 180), (150, 176), (148, 200), (151, 214), (120, 220), (89, 214), (92, 200)],
        "butt": [(89, 216), (120, 222), (120, 262), (108, 270), (94, 264), (84, 246), (84, 228)],
        "head": (120, 44, 23, 29),
    },
    "erkek": {
        "neck": [(109, 66), (131, 66), (134, 92), (106, 92)],
        "chest": [(106, 90), (134, 90), (154, 94), (171, 103), (169, 126), (163, 154), (145, 164), (120, 166), (95, 164), (77, 154), (71, 126), (69, 103), (86, 94)],
        "belly": [(95, 162), (120, 165), (145, 162), (151, 176), (148, 200), (150, 219), (120, 225), (90, 219), (92, 200), (89, 176)],
        "groin": [(92, 221), (120, 227), (148, 221), (141, 239), (128, 253), (120, 257), (112, 253), (99, 239)],
        "thigh": [(89, 216), (99, 235), (113, 253), (118, 263), (116, 302), (112, 342), (104, 354), (93, 354), (88, 322), (85, 282), (86, 240)],
        "shin": [(92, 348), (112, 348), (113, 380), (110, 430), (106, 468), (96, 470), (92, 430), (88, 380)],
        "foot": [(95, 466), (107, 466), (111, 488), (100, 493), (90, 489)],
        "uarm": [(71, 100), (60, 105), (52, 121), (48, 149), (48, 181), (56, 186), (64, 183), (68, 152), (72, 127)],
        "farm": [(48, 181), (63, 181), (60, 217), (56, 250), (50, 262), (44, 262), (42, 240), (43, 212)],
        "hand": [(43, 258), (52, 258), (56, 281), (50, 293), (42, 289), (40, 275)],
        "pit": [(73, 112), (80, 116), (80, 134), (75, 140), (71, 128)],
        "shoulder": [(70, 102), (86, 94), (106, 91), (106, 106), (88, 113), (73, 121)],
        "upback": [(88, 113), (106, 106), (134, 106), (152, 113), (167, 124), (163, 154), (152, 176), (120, 180), (88, 176), (77, 154), (73, 124)],
        "lowback": [(89, 178), (120, 182), (151, 178), (148, 202), (150, 216), (120, 222), (90, 216), (92, 202)],
        "butt": [(90, 218), (120, 224), (120, 262), (108, 270), (95, 264), (86, 246), (86, 228)],
        "head": (120, 44, 24, 30),
    },
}
# part -> region id, per side; bilateral parts appear twice.  None = shape only (not selectable)
PARTS = {
    "on": [("neck", "boyun", False), ("chest", "gogus", False), ("belly", "gobek", False), ("groin", "genital", False),
           ("thigh", "ust-bacak", True), ("shin", "alt-bacak", True), ("foot", None, True), ("uarm", "ust-kol", True),
           ("farm", "alt-kol", True), ("hand", None, True), ("pit", "koltuk", True)],
    "arka": [("neck", "ense", False), ("upback", "sirt", False), ("lowback", "bel", False), ("shoulder", "omuz", True),
             ("butt", "popo", True), ("thigh", "ust-bacak", True), ("shin", "alt-bacak", True), ("foot", None, True),
             ("uarm", "ust-kol", True), ("farm", "alt-kol", True), ("hand", None, True)],
}
PART_NAME = {"boyun": "Boyun", "gogus": "Göğüs", "gobek": "Göbek", "genital": "Genital", "ust-bacak": "Bacak (üst)",
             "alt-bacak": "Bacak (diz altı)", "ust-kol": "Kol (üst)", "alt-kol": "Kol (dirsek altı)", "koltuk": "Koltuk altı",
             "ense": "Ense", "sirt": "Sırt", "bel": "Bel", "omuz": "Omuz", "popo": "Popo"}


HAIR = {
    "kadin": {"on": "M95,44 C92,20 104,10 120,10 C136,10 148,20 145,44 C143,30 134,22 120,22 C106,22 97,30 95,44Z",
              "arka": "M96,50 C93,22 104,12 120,12 C136,12 147,22 144,50 C140,64 132,72 120,73 C108,72 100,64 96,50Z",
              "bun": (120, 9, 9)},
    "erkek": {"on": "M96,40 C95,22 106,13 120,13 C134,13 145,22 144,40 C140,28 132,24 120,24 C108,24 100,28 96,40Z",
              "arka": "M96,48 C94,24 105,14 120,14 C135,14 146,24 144,48 C140,58 132,62 120,62 C108,62 100,58 96,48Z",
              "bun": None},
}


def body_svg(g: str, side: str, code: str) -> str:
    sh = SHAPES[g]
    have = {r["id"] for r in region_list(g)}
    uid = f"{code}-{g}-{side}"
    base, hits = [], []
    cx, cy, rx, ry = sh["head"]
    if side == "on":
        hits.append(f'<ellipse class="lz-part lz-head" data-part="yuz" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" tabindex="0" role="button" '
                    f'aria-label="Yüz bölgeleri" data-track-label="at-{code}-harita-yuz"/>')
    else:
        base.append(f'<ellipse class="lz-shape" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/>')
    hair = HAIR[g]
    base.append(f'<path class="lz-hair" d="{hair[side]}"/>')
    if hair["bun"]:
        bx, by, br = hair["bun"]
        base.append(f'<circle class="lz-hair" cx="{bx}" cy="{by}" r="{br}"/>')
    for name, part, bilateral in PARTS[side]:
        pts = sh[name]
        shapes = [pts, mirror(pts)] if bilateral else [pts]
        region_ok = part is not None and (part in have or part in ("ust-kol", "alt-kol", "ust-bacak", "alt-bacak"))
        for p in shapes:
            d = smooth(p)
            if not region_ok:
                base.append(f'<path class="lz-shape" d="{d}"/>')
                continue
            lab = PART_NAME.get(part, part)
            hits.append(f'<path class="lz-part" data-part="{part}" d="{d}" tabindex="0" role="button" aria-label="{esc(lab)}" '
                        f'data-track-label="at-{code}-harita-bolge"/>')
    label = "ön" if side == "on" else "arka"
    defs = (f'<defs><linearGradient id="lzSkin-{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2A1D22"/>'
            f'<stop offset=".45" stop-color="#3A2A30"/><stop offset="1" stop-color="#261A1F"/></linearGradient>'
            f'<filter id="lzRim-{uid}" x="-12%" y="-6%" width="124%" height="112%">'
            '<feMorphology in="SourceAlpha" operator="dilate" radius="1.2" result="d"/>'
            '<feComposite in="d" in2="SourceAlpha" operator="out" result="edge"/>'
            '<feFlood flood-color="#EBCB9E" flood-opacity=".8"/><feComposite in2="edge" operator="in" result="rim"/>'
            '<feGaussianBlur in="rim" stdDeviation="2.2" result="glow"/>'
            '<feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/><feMergeNode in="rim"/></feMerge></filter></defs>')
    # shapes are drawn first (non-selectable), parts after them so a tap always reaches a region
    return (f'<svg class="lz-body" data-g="{g}" data-side="{side}" viewBox="30 0 180 500" role="group" '
            f'aria-label="Vücut haritası, {label} görünüm" style="--lz-skin:url(#lzSkin-{uid})">{defs}'
            f'<g class="lz-sil" filter="url(#lzRim-{uid})"><g class="lz-base">{"".join(base)}</g><g class="lz-parts">{"".join(hits)}</g></g>'
            '<g class="lz-fx"></g></svg>')


def face_svg(g: str, code: str) -> str:
    oval = smooth([(100, 22), (140, 30), (161, 60), (165, 100), (159, 140), (145, 172), (123, 194), (100, 201), (77, 194),
                   (55, 172), (41, 140), (35, 100), (39, 60), (60, 30)])
    zones = []
    if g == "kadin":
        zones += [("dudak-ustu", smooth([(80, 137), (100, 141), (120, 137), (126, 147), (100, 150), (74, 147)]), "Dudak üstü"),
                  ("cene", smooth([(80, 172), (100, 177), (120, 172), (128, 184), (100, 200), (72, 184)]), "Çene"),
                  ("gidi", smooth([(64, 190), (100, 207), (136, 190), (134, 214), (100, 228), (66, 214)]), "Gıdı")]
    else:
        zones += [("sakal-ustu", smooth([(44, 112), (68, 116), (78, 136), (60, 146), (44, 132)]), "Sakal üstü"),
                  ("sakal-ustu", smooth(mirror_face([(44, 112), (68, 116), (78, 136), (60, 146), (44, 132)])), "Sakal üstü"),
                  ("kulak", "M34,86 C22,86 20,120 32,124 C38,124 38,90 34,86Z", "Kulak"),
                  ("kulak", "M166,86 C178,86 180,120 168,124 C162,124 162,90 166,86Z", "Kulak")]
    feat = ('<path class="lz-feat" d="M64,90 C72,84 84,84 92,90 M108,90 C116,84 128,84 136,90"/>'
            '<path class="lz-feat" d="M66,96 C74,101 84,101 90,97 M110,97 C116,101 126,101 134,96"/>'
            '<path class="lz-feat" d="M100,100 C98,112 95,120 93,126 C97,129 103,129 107,126"/>'
            '<path class="lz-feat lz-lips" d="M84,156 C92,151 97,153 100,155 C103,153 108,151 116,156 C108,165 92,165 84,156Z"/>')
    if g == "erkek":
        feat += '<path class="lz-feat" d="M56,150 C64,176 84,192 100,194 C116,192 136,176 144,150" stroke-dasharray="2 4"/>'
    neck = smooth([(76, 206), (124, 206), (128, 240), (72, 240)])
    parts = "".join(
        f'<path class="lz-part" data-part="{rid}" d="{d}" tabindex="0" role="button" aria-label="{esc(n)}" data-track-label="at-{code}-harita-yuz-bolge"/>'
        for rid, d, n in zones)
    return (f'<svg class="lz-facesvg" viewBox="20 14 160 230" role="group" aria-label="Yüz bölgeleri">'
            f'<path class="lz-shape" d="{neck}"/><path class="lz-shape lz-faceoval" d="{oval}"/>'
            f'<g class="lz-feats">{feat}</g><g class="lz-parts">{parts}</g><g class="lz-fx"></g></svg>')


def mirror_face(pts):
    return [(200 - x, y) for x, y in reversed(pts)]


# --------------------------------------------------------------------------------------------- journey
def journey_svg(code: str = "lz") -> str:
    xs = [20 + i * 35 for i in range(9)]
    phases = ["A", "T", "A", "C", "A", "A", "T", "A", "C"]
    out = []
    for i, (x, ph) in enumerate(zip(xs, phases)):
        bulb_y = {"A": 196, "C": 150, "T": 118}[ph]
        top = {"A": 34, "C": 40, "T": 54}[ph]
        sheath = f"M{x - 6:.1f},70 C{x - 7:.1f},{bulb_y - 30} {x - 8:.1f},{bulb_y - 10} {x - 9:.1f},{bulb_y + 4} M{x + 6:.1f},70 C{x + 7:.1f},{bulb_y - 30} {x + 8:.1f},{bulb_y - 10} {x + 9:.1f},{bulb_y + 4}"
        bulb = (f'<ellipse class="lz-bulb" cx="{x:.1f}" cy="{bulb_y}" rx="{9 if ph == "A" else 7}" ry="{11 if ph == "A" else 8}"/>' if ph != "T"
                else f'<circle class="lz-club" cx="{x:.1f}" cy="{bulb_y}" r="5"/>')
        out.append(f'<g class="lz-fol" data-ph="{ph}" data-i="{i}"><path class="lz-sheath" d="{sheath}"/>'
                   f'<path class="lz-shaft" d="M{x:.1f},{bulb_y - 6} C{x - 1:.1f},{(bulb_y + 70) / 2} {x + 2:.1f},80 {x + (3 if i % 2 else -3):.1f},{top}"/>{bulb}</g>')
    fat = "".join(f'<circle class="lz-fat" cx="{18 + (i * 47) % 340}" cy="{258 + (i * 29) % 56}" r="{13 + (i * 7) % 9}"/>' for i in range(16))
    beams = "".join(
        f'<rect class="lz-beam lz-b{wl}" x="116" y="30" width="104" height="{d}" rx="20" fill="url(#lzBeam-{code})"/>'
        for wl, d in (("755", 120), ("808", 180), ("1064", 270)))
    return ('<svg class="lz-jsvg" viewBox="0 0 360 330" aria-hidden="true">'
            f'<defs><linearGradient id="lzDerm-{code}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7B3F45"/><stop offset="1" stop-color="#3F2027"/></linearGradient>'
            f'<linearGradient id="lzBeam-{code}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE6F3" stop-opacity=".95"/><stop offset=".25" stop-color="#FF5FB0" stop-opacity=".75"/>'
            '<stop offset="1" stop-color="#C2187A" stop-opacity="0"/></linearGradient>'
            f'<filter id="lzBlur-{code}" x="-30%" y="-10%" width="160%" height="120%"><feGaussianBlur stdDeviation="6"/></filter></defs>'
            '<rect class="lz-sub" x="0" y="230" width="360" height="100"/>' + fat +
            f'<rect x="0" y="84" width="360" height="148" fill="url(#lzDerm-{code})"/>'
            '<rect class="lz-epi" x="0" y="68" width="360" height="17"/>'
            '<text class="lz-jlab" x="352" y="80" text-anchor="end">epidermis</text>'
            '<text class="lz-jlab" x="352" y="224" text-anchor="end">dermis</text>'
            + "".join(out) +
            f'<g class="lz-beams" filter="url(#lzBlur-{code})">{beams}</g>'
            '<g class="lz-hp"><rect x="126" y="0" width="84" height="30" rx="8"/><rect class="lz-win" x="138" y="24" width="60" height="8" rx="3"/></g>'
            '<g class="lz-tags"><g class="lz-tag lz-tag-a"><line x1="90" y1="196" x2="90" y2="300"/><text x="90" y="314" text-anchor="middle">büyüme evresi</text></g>'
            '<g class="lz-tag lz-tag-t"><line x1="55" y1="118" x2="55" y2="300"/><text x="55" y="314" text-anchor="middle">dinlenme evresi</text></g></g>'
            '</svg>')


# --------------------------------------------------------------------------------------------- pages
PAGES = {
    "hub": {"slug": "laser-signature", "code": "lazer", "g": "kadin", "hero": ("video", "lazer-film-jel", "lazer-5"), "focal": "64% 58%",
            "lede": "Lasermach, 3 dalga boyu, soğutmalı başlık. Bölgenizi seçin, planı birlikte yapalım.",
            "order": ["map", "journey", "cal", "device", "reels", "reviews", "hygiene", "price", "family", "visit"]},
    "kamp": {"slug": "laser-signature-kampanya", "code": "lzkamp", "g": "kadin", "hero": ("video", "lazer-film-jel", "lazer-5"), "focal": "64% 58%",
             "lede": "Lasermach, 3 dalga boyu, soğutmalı başlık. Bölgenizi seçin, planı birlikte yapalım.",
             "order": ["map", "journey", "cal", "device", "reels", "reviews", "hygiene", "price", "family", "visit"]},
    "fiyat": {"slug": "lazer-epilasyon-fiyatlari-ankara", "code": "lzfiyat", "g": "kadin", "hero": ("img", "lazer-ekran", None), "focal": "42% 32%",
              "lede": "Fiyat; bölgenize, seans sayısına ve pakete göre belirlenir. Bölgeleri seçin, size özel fiyat WhatsApp'ta.",
              "cta": ("Bölge menüsünü aç", "#lz-menu"),
              "order": ["menu", "factors", "map", "reviews", "cal", "device", "reels", "family", "visit"]},
    "erkek": {"slug": "erkek-lazer-epilasyon", "code": "lzerkek", "g": "erkek", "hero": ("video", "lazer-film-kol", None), "focal": "50% 40%",
              "lede": "Sakal hattından sırta; erkek bölgeleri, kişiye özel plan.",
              "order": ["map", "reviews", "cal", "journey", "device", "reels", "price", "hygiene", "family", "visit"]},
    "yuz": {"slug": "yuz-lazer", "code": "lzyuz", "g": "kadin", "face": True, "hero": ("video", "lazer-film-cene", None),
            "lede": "Dudak üstü, çene, gıdı: yüzde ince ayar, koruyucu gözlükle.",
            "order": ["map", "cal", "hygiene", "journey", "device", "reels", "reviews", "price", "family", "visit"]},
    "hassas": {"slug": "hassas-cilt-lazer", "code": "lzhassas", "g": "kadin", "tone": True, "hero": ("video", "lazer-film-yuz", "lazer-yuz-gozluk"), "focal": "45% 55%",
               "lede": "Soğutmalı başlık ve cilt tonunuza göre ayar. Önce cildinizi tanıyoruz.",
               "order": ["tone", "device", "map", "journey", "hygiene", "cal", "reviews", "reels", "price", "family", "visit"]},
    "bolge": {"slug": "bolgesel-lazer", "code": "lzbolge", "g": "kadin", "quick": True, "hero": ("img", "lazer-koltuk", None), "focal": "58% 62%",
              "lede": "Yalnızca ihtiyacınız olan bölge. Koltuk altı tek seansta 15 dakika.",
              "order": ["quick", "map", "cal", "reels", "reviews", "journey", "device", "price", "family", "visit"]},
}
FAMILY = [("hub", "Lazer epilasyon", "lazer-film-jel-poster.webp", "Merkez sayfa"),
          ("fiyat", "Fiyatlar ve bölge menüsü", "lazer-ekran-800.webp", "Tüm bölgeler, süreleriyle"),
          ("erkek", "Erkek lazer", "lazer-film-kol-poster.webp", "Sakal üstünden sırta"),
          ("yuz", "Yüz lazer", "lazer-film-cene-poster.webp", "Dudak üstü, çene, gıdı"),
          ("hassas", "Hassas cilt", "lazer-film-yuz-poster.webp", "Soğutmalı başlık"),
          ("bolge", "Bölgesel lazer", "lazer-koltuk-800.webp", "Tek bölge, kısa seans")]
def alt_of(sl):
    return {"lazer-5": "Lasermach başlığıyla kol bölgesine lazer epilasyon, salonumuzda",
            "lazer-2": "Bacak bölgesine lazer epilasyon, salonumuzda",
            "lazer-yuz-gozluk": "Koruyucu gözlükle yüz bölgesine lazer epilasyon, salonumuzda"}.get(sl, "Lazer epilasyon, salonumuzda")


HERO_MEDIA = {
    "lazer-film-jel": "Lasermach başlığının pembe ışığı jel üzerinde, salonumuzda çekildi",
    "lazer-film-cene": "Çene ve gıdı bölgesinde lazer epilasyon, salonumuzda çekildi",
    "lazer-film-bacak": "Bacakta lazer epilasyon uygulaması, salonumuzda çekildi",
    "lazer-film-yuz": "Koruyucu gözlükle yüz bölgesinde lazer epilasyon, salonumuzda çekildi",
    "lazer-film-kol": "Kol bölgesinde lazer epilasyon, salonumuzda çekildi",
    "lazer-ekran": "Lasermach lazer cihazının ekranı: enerji, atım süresi, cilt tonu ve başlık sıcaklığı",
    "lazer-koltuk": "Koltuk altına Lasermach başlığıyla lazer epilasyon, salonumuzda",
}
HOTSPOTS = [
    ("enerji", 28.3, 29.0, "Enerji · J/cm²", "Atış başına verilen enerji. Uzmanınız cilt tonunuza ve kıl yapınıza göre ayarlar."),
    ("atim", 46.6, 29.8, "Atım süresi · ms", "Işığın ne kadar sürede verileceği. Ekrandaki “Nd:YAG” ibaresi 1064 nm dalga boyunun seçili olduğunu gösterir."),
    ("frekans", 63.5, 34.2, "Frekans · Hz", "Saniyedeki atış sayısı. Geniş bölgelerde başlık kayarak ilerler."),
    ("ton", 40.0, 39.1, "Cilt tonu", "Uygulamadan önce cilt tonunuz cihazda seçilir; başlangıç ayarı buna göre yapılır."),
    ("sicaklik", 66.6, 38.6, "Soğutma · 10 °C", "Başlık soğutmalı çalışır; bu fotoğrafta ekrandaki başlık sıcaklığı 10 °C."),
    ("baslik", 90.0, 83.0, "Başlık", "Lasermach diode başlığı: tek başlıkta 3 dalga boyu, 755 · 808 · 1064 nm."),
]
JOURNEY = [
    ("Işık yalnızca pigmenti arar.", "Lazer ışığı cildin üst katmanını geçer ve kıl kökündeki koyu pigmente (melanin) ulaşır."),
    ("Büyüme evresindeki kök ısınır.", "Işığı emen kök ısınır ve zayıflar. Etki en çok büyüme evresindeki köklerde olur."),
    ("Dinlenen kökler sırasını bekler.", "Her kök aynı anda büyüme evresinde değildir; dinlenenler o seansta etkilenmez."),
    ("Bu yüzden seanslar aralıklı.", "Sıradaki kökler büyüme evresine geçtikçe bir sonraki seansta yakalanır. Paketlerimiz 8 seans; aralığı bölgenize göre planlanır."),
]
WAVES = [("755", "755 nm", "Yüzeye yakın kökler; ince ve açık renkli kıllar."),
         ("808", "808 nm", "Orta derinlik; çoğu bölge için dengeli."),
         ("1064", "1064 nm", "Derin kökler; koyu ten tonlarında tercih edilir.")]
HYGIENE = [("lazer-kilif-800.webp", "Kılıflı başlık", "Başlık koruyucu kılıf içinde."),
           ("lazer-uzman-800.webp", "Eldivenli uygulama", "Uzmanımız eldivenle çalışır."),
           ("lazer-yuz-gozluk-800.webp", "Koruyucu gözlük", "Yüz bölgesinde gözler kapatılır."),
           ("lazer-film-bacak2-poster.webp", "Soğutucu jel", "Işık, jel katmanının üzerinden verilir.")]
REELS = [("lazer-film-jel", "Jel, ışık, kayış"), ("lazer-film-cene", "Çene ve gıdı"), ("lazer-film-kol", "Kol"),
         ("lazer-film-bacak", "Bacak"), ("lazer-film-yuz", "Yüz, gözlükle"), ("lazer-film-bacak2", "Diz altı")]
TONES = [("1", "#F3DCCB", "Çok açık"), ("2", "#E9C6A7", "Açık"), ("3", "#D6A57E", "Buğday"),
         ("4", "#B57E55", "Esmer"), ("5", "#8A5634", "Koyu esmer"), ("6", "#5A3622", "Koyu")]
FACTORS = [("Bölge", "Koltuk altı 15 dakika, tüm bacak 45 dakika; bölge büyüdükçe süre ve fiyat değişir."),
           ("Seans", "Tek seans ya da 8 seanslık paket; aralığı bölgenize göre planlanır."),
           ("Paket", "Tepeden tırnağa ve tüm vücut seçeneklerinde bitiş garantili paket de var."),
           ("Cilt ve kıl", "Cilt tonunuz ve kıl yapınız ilk görüşmede değerlendirilir.")]


def fmt_min(r) -> str:
    if r.get("m") is None:
        return ""
    if r.get("mx") and r["mx"] != r["m"]:
        return f'{r["m"]}–{r["mx"]} dk'
    return f'{r["m"]} dk'


def split_h1(h1: str) -> tuple[str, str]:
    """Big line + small line with big + " " + small == h1 (text unchanged for search engines)."""
    h1 = re.sub(r"\s+", " ", h1).strip()
    i = h1.find(": ")
    if 8 < i < 60:
        return h1[:i + 1], h1[i + 2:]
    for sep in (" için ", " ve "):
        i = h1.find(sep)
        if 8 < i < 60:
            return h1[:i], h1[i + 1:]
    return h1, ""


def sec_head(eyebrow, title, p=""):
    return (f'<div class="lz-head"><span class="lz-over">{eyebrow}</span><h2>{title}</h2>'
            + (f"<p>{p}</p>" if p else "") + "</div>")


def wa_link(code, place, msg, cls="lz-btn-gold", label="", icon=True, extra=""):
    href = f"https://wa.me/{WA}?text=" + _q(msg)
    return (f'<a class="{cls}" href="{esc(href)}" target="_blank" rel="noopener" data-track-label="at-{code}-{place}" data-lz-wa="{place}"{extra}>'
            + (ICON["wa"] if icon else "") + (f'<span class="lz-lbl">{label}</span>' if label else "") + "</a>")


def _q(s: str) -> str:
    from urllib.parse import quote
    return quote(s, safe="")


HERO_IMG: dict = {}


def page_html(key: str, media: str, h1: str, link) -> str:
    """The vitrine markup for one laser page.  media = '/images/ig/' or 'm/ig/'; link(page_key) -> href."""
    P = PAGES[key]
    code, g = P["code"], P["g"]
    rev = load("reviews_laser.json")
    st = rev["stats"]
    big, small = split_h1(h1)
    kind, slug, still = P["hero"]
    SIZES = {"lazer-5": (1200, 1500, True), "lazer-2": (1200, 1599, True), "lazer-yuz-gozluk": (800, 800, False),
             "lazer-ekran": (1200, 1600, True), "lazer-koltuk": (1200, 1599, True)}
    def still_img(sl, cls):
        w, hh, big = SIZES[sl]
        srcset = f'{media}{sl}-480.webp 480w, {media}{sl}-800.webp 800w' + (f', {media}{sl}-1200.webp 1200w' if big else "")
        return (f'<img class="{cls}" style="object-position:{P.get("focal", "50% 50%")}" src="{media}{sl}-800.webp" srcset="{srcset}" sizes="(min-width:960px) 50vw, 100vw" '
                f'alt="{esc(HERO_MEDIA.get(sl, alt_of(sl)))}" width="{w}" height="{hh}" fetchpriority="high" decoding="async">')
    if kind == "video":
        poster = f"{media}{slug}-poster.webp"
        first = still_img(still, "lz-poster lz-kb") if still else (
            f'<img class="lz-poster" src="{poster}" alt="{esc(HERO_MEDIA[slug])}" width="720" height="1280" fetchpriority="high" decoding="async">')
        stage = first + f'<video class="lz-hero-vid" muted playsinline loop preload="none" data-src="{media}{slug}.mp4" aria-hidden="true"></video>'
        hero_img = f"{media}{still}-800.webp" if still else poster
    else:
        stage = still_img(slug, "lz-poster lz-kb")
        hero_img = f"{media}{slug}-800.webp"
    HERO_IMG[key] = hero_img
    cta_txt, cta_href = P.get("cta", ("Bölgelerimi seç", "#lz-harita"))
    hello = "Merhaba, lazer epilasyon hakkında bilgi almak istiyorum."
    hero_wa = wa_link(code, "hero-wa", hello, "lz-btn-round", "", True, ' aria-label="WhatsApp’tan yazın"')
    h1b = f' <span class="lz-h1b">{esc(small)}</span>' if small else ""
    h = []
    h.append(f'<div class="lz" data-lz-page="{key}" data-lz-code="{code}" data-lz-g="{g}" data-lz-media="{media}">')
    # ---------------------------------------------------------------- L1 hero
    h.append(f'''<header class="lz-hero" id="lz-ust">
  <div class="lz-stage">{stage}<div class="lz-scan" aria-hidden="true"></div><div class="lz-glow" aria-hidden="true"></div><div class="lz-scrim" aria-hidden="true"></div>
    <div class="lz-proof" aria-label="Kısa bilgiler"><span><b>3</b> dalga boyu<small>755·808·1064 nm</small></span><span><b>10 °C</b> başlık<small>soğutmalı</small></span><span><b>{st["five"]}/{st["mentions"]}</b> lazer yorumu<small>Google · 5 yıldız</small></span></div>
  </div>
  <div class="lz-copy">
    <span class="lz-over">Konutkent · Çankaya · Lasermach diode</span>
    <h1 class="lz-h1"><span class="lz-h1a">{esc(big)}</span>{h1b}</h1>
    <div class="lz-chips"><span class="lz-chip"><b class="lz-star">★</b> 4,6 · 263 yorum</span><span class="lz-chip">Kişiye özel fiyat</span><span class="lz-chip" data-lz-open><i class="lz-dot"></i>Salı–Pazar 10.00–20.00</span></div>
    <div class="lz-cta-row"><a class="lz-btn-gold lz-shine" href="{cta_href}" data-lz-scroll data-track-label="at-{code}-hero-bolge"><span class="lz-lbl">{cta_txt}</span>{ICON["down"]}</a>{hero_wa}</div>
    <p class="lz-lede">{P["lede"]}</p>
    <div class="lz-rings" data-lz-rings></div>
    <p class="lz-fine">Videolar ve fotoğraflar salonumuzda çekildi.</p>
  </div>
</header>''')
    sections = {
        "map": lambda: map_section(P, code, g),
        "journey": lambda: journey_section(code),
        "cal": lambda: cal_section(code),
        "device": lambda: device_section(code, media),
        "reels": lambda: reels_section(code, media),
        "reviews": lambda: reviews_section(code, rev, P),
        "hygiene": lambda: hygiene_section(code, media),
        "price": lambda: price_card(code, link),
        "menu": lambda: menu_section(code),
        "factors": lambda: factors_section(),
        "family": lambda: family_section(key, code, media, link),
        "visit": lambda: visit_section(code),
        "tone": lambda: tone_section(code),
        "quick": lambda: quick_section(code),
    }
    for s in P["order"]:
        h.append(sections[s]())
    h.append("</div>")
    return "\n".join(h)


def map_section(P, code, g):
    face_first = P.get("face")
    regs = region_list(g)
    chips_body = "".join(
        f'<button type="button" data-rg="{r["id"]}" aria-pressed="false" data-track-label="at-{code}-liste-bolge"><span>{esc(r["n"])}</span><small>{fmt_min(r)}</small></button>'
        for r in regs if r["z"] != "pkg")
    pkgs = "".join(
        f'<button type="button" class="lz-pkg" data-rg="{r["id"]}" aria-pressed="false" data-track-label="at-{code}-harita-paket"><b>{esc(r["n"])}</b><small>{fmt_min(r)}{" · bitiş garantili seçenek" if r["id"] in ("tepeden", "tum-vucut-4", "full-vucut", "kemer-ustu") else ""}</small></button>'
        for r in regs if r["z"] == "pkg")
    figs = "".join(body_svg(gg, side, code) for gg in ("kadin", "erkek") for side in ("on", "arka"))
    faces = "".join(face_svg(gg, code).replace('class="lz-facesvg"', f'class="lz-facesvg" data-g="{gg}"') for gg in ("kadin", "erkek"))
    return f'''<section class="lz-sec lz-map" id="lz-harita" aria-labelledby="lz-harita-h">
  {sec_head("Vücut haritası", 'Işığı nereye <em>yönlendirelim</em>?', "Bölgeye dokunun, ışık orada yansın. Süreler randevu sistemimizdeki menüden.").replace("<h2>", '<h2 id="lz-harita-h">')}
  <div class="lz-map-ui" data-face="{'1' if face_first else '0'}">
    <div class="lz-toggles">
      <div class="lz-seg" role="group" aria-label="Kimin için"><button type="button" data-lz-gender="kadin" aria-pressed="{str(g == 'kadin').lower()}" data-track-label="at-{code}-harita-cinsiyet">Kadın</button><button type="button" data-lz-gender="erkek" aria-pressed="{str(g == 'erkek').lower()}" data-track-label="at-{code}-harita-cinsiyet">Erkek</button></div>
      <div class="lz-seg" role="group" aria-label="Görünüm"><button type="button" data-lz-side="on" aria-pressed="true" data-track-label="at-{code}-harita-yon">Ön</button><button type="button" data-lz-side="arka" aria-pressed="false" data-track-label="at-{code}-harita-yon">Arka</button><button type="button" data-lz-side="yuz" aria-pressed="false" data-track-label="at-{code}-harita-yon">Yüz</button></div>
    </div>
    <div class="lz-map-grid">
      <div class="lz-figure" data-view="on">{figs}{faces}<span class="lz-fig-hint">Dokunun</span></div>
      <div class="lz-picked" aria-live="polite">
        <span class="lz-over">Seçtikleriniz</span>
        <ul class="lz-plist" data-lz-plist><li class="lz-empty">Henüz bölge yok. Haritada bir bölgeye dokunun.</li></ul>
        <div class="lz-total" data-lz-total></div>
        <div class="lz-pkgs">{pkgs}</div>
      </div>
    </div>
    <div class="lz-actions">
      {wa_link(code, "harita-wa", "Merhaba, lazer epilasyon için fiyat ve plan almak istiyorum.", "lz-btn-gold lz-shine", "WhatsApp'tan fiyat sor")}
      <button type="button" class="lz-btn-line" data-lz-plan data-track-label="at-{code}-davetiye-ac">{ICON["cal"]}<span>Gün de seçeyim</span></button>
    </div>
    <p class="lz-fine">Mesaj hazır; göndermek size kalır. Fiyatı bölgelerinize göre WhatsApp'tan iletiyoruz.</p>
    <details class="lz-list"><summary data-track-label="at-{code}-liste-ac">Listeden seçmek isterim</summary><div class="lz-rgchips" data-lz-rgchips>{chips_body}</div></details>
  </div>
</section>'''


def journey_section(code):
    steps = "".join(f'<li class="lz-jstep" data-step="{i + 1}"><div class="lz-jtxt" data-step="{i + 1}"><span class="lz-jn">0{i + 1}</span><b>{t}</b><p>{p}</p></div></li>' for i, (t, p) in enumerate(JOURNEY))
    waves = "".join(f'<button type="button" data-wl="{w}" aria-pressed="{str(w == "808").lower()}" data-track-label="at-{code}-yolculuk-dalga"><b>{n}</b><small>{d}</small></button>' for w, n, d in WAVES)
    return f'''<section class="lz-sec lz-journey" id="lz-yolculuk">
  {sec_head("Işığın yolculuğu", "Neden <em>8 seans</em>?", "Kaydırdıkça ışığın cildinizde ne yaptığını görün.")}
  <div class="lz-jwrap">
    <div class="lz-jfig" data-step="0" data-wl="808">{journey_svg(code)}<div class="lz-sess" aria-hidden="true"><span>Seans</span><b data-lz-sess>1</b><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
    <ol class="lz-jsteps">{steps}</ol>
  </div>
  <div class="lz-waves" role="group" aria-label="Dalga boyları">{waves}</div>
  <p class="lz-fine">Temsili anlatım. Seans sayısı ve aralığı cilt ve kıl yapınıza göre uzmanınızca planlanır; sonuç kişiye göre değişir.</p>
</section>'''


def cal_section(code):
    return f'''<section class="lz-sec lz-calsec" id="lz-takvim">
  {sec_head("Seans takvimi", "8 seanslık <em>yolculuğunuz</em>", "Seçtiğiniz bölgelere göre tahmini takvim. Yüz bölgelerinde 4–6, vücutta 6–8 hafta arayla.")}
  <div class="lz-cal" data-lz-cal>
    <div class="lz-seg lz-start" role="group" aria-label="Başlangıç"><button type="button" data-start="0" aria-pressed="true" data-track-label="at-{code}-takvim-baslangic">Bu ay</button><button type="button" data-start="1" aria-pressed="false" data-track-label="at-{code}-takvim-baslangic">Gelecek ay</button><button type="button" data-start="2" aria-pressed="false" data-track-label="at-{code}-takvim-baslangic">2 ay sonra</button></div>
    <ol class="lz-track" data-lz-track></ol>
    <p class="lz-calsum" data-lz-calsum>8 seans, vücut bölgelerinde 6–8 hafta arayla.</p>
    <p class="lz-fine">Tahminidir; uzmanınız cilt ve kıl yapınıza göre ayarlar.</p>
  </div>
</section>'''


def device_section(code, media):
    dots = "".join(f'<button type="button" class="lz-hot" data-hot="{k}" style="left:{x}%;top:{y}%" aria-label="{esc(t)}" aria-pressed="{str(i == 0).lower()}" data-track-label="at-{code}-cihaz-nokta"><i></i></button>'
                   for i, (k, x, y, t, _d) in enumerate(HOTSPOTS))
    cards = "".join(f'<div class="lz-hotcard" data-hotcard="{k}"{"" if i == 0 else " hidden"}><b>{t}</b><p>{d}</p></div>' for i, (k, _x, _y, t, d) in enumerate(HOTSPOTS))
    return f'''<section class="lz-sec lz-device" id="lz-cihaz">
  {sec_head("Cihazımız", "Lasermach: <em>3 dalga boyu</em>, tek başlık", "Ekrandaki noktalara dokunun; uzmanınızın neyi ayarladığını görün.")}
  <div class="lz-dev-grid">
    <figure class="lz-devfig"><img src="{media}lazer-ekran-800.webp" srcset="{media}lazer-ekran-480.webp 480w, {media}lazer-ekran-800.webp 800w, {media}lazer-ekran-1200.webp 1200w" sizes="(min-width:960px) 520px, 92vw" alt="{esc(HERO_MEDIA['lazer-ekran'])}" width="1200" height="1600" loading="lazy" decoding="async">{dots}</figure>
    <div class="lz-dev-side">
      <div class="lz-hotcards">{cards}</div>
      <div class="lz-spec"><span>Lasermach diode</span><span>755 nm</span><span>808 nm</span><span>1064 nm</span><span>Soğutmalı başlık</span></div>
    </div>
  </div>
</section>'''


def reels_section(code, media):
    items = "".join(
        f'<button type="button" class="lz-reel" data-reel="{s}" data-track-label="at-{code}-film-ac" aria-label="{esc(c)}: videoyu açın">'
        f'<video muted playsinline loop preload="none" poster="{media}{s}-poster.webp" data-src="{media}{s}.mp4" aria-hidden="true"></video>'
        f'<span class="lz-reel-t"><i>{ICON["play"]}</i>{esc(c)}</span></button>' for s, c in REELS)
    return f'''<section class="lz-sec lz-reels" id="lz-film">
  {sec_head("Salonumuzda çekildi", "Işığı <em>iş başında</em> görün", "Gerçek uygulamalar, Instagram hesabımızdan. Dokunun, tam ekran izleyin.")}
  <div class="lz-reelrow">{items}</div>
</section>'''


def reviews_section(code, rev, P):
    st = rev["stats"]
    items = rev["items"]
    if P["g"] == "erkek":
        items = sorted(items, key=lambda r: 0 if r.get("g") == "m" else 1)
    cards = "".join(f'<article class="lz-rv"><span class="lz-stars" aria-label="5 yıldız">★★★★★</span><p>{esc(r["t"])}</p><footer><b>{esc(r["n"])}</b><span>{month_tr(r["d"])} · Google</span></footer></article>' for r in items)
    return f'''<section class="lz-sec lz-reviews" id="lz-yorumlar">
  <div class="lz-rvstat"><span class="lz-over">Lazerde yorumlarımız konuşuyor</span><div class="lz-big"><b>{st["five"]}</b><span>/ {st["mentions"]}</span></div><p>Google'da lazer geçen {st["mentions"]} yorumun {st["five"]}'u 5 yıldız.</p></div>
  <div class="lz-rvrow" data-lz-rv><div class="lz-rvtrack">{cards}</div></div>
  <p class="lz-fine">Google yorumlarından aynen alıntı; “…” kısaltmayı gösterir. Sonuç kişiye göre değişir. <a href="{MAPS}" target="_blank" rel="noopener" data-track-label="at-{code}-yorumlar-google">Tüm yorumlar ↗</a></p>
</section>'''


def month_tr(d):
    y, m = d.split("-")
    return ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"][int(m) - 1] + " " + y


def hygiene_section(code, media):
    cards = "".join(f'<button type="button" class="lz-hy" data-zoom="{media}{f}" data-track-label="at-{code}-hijyen">'
                    f'<img src="{media}{f}" alt="{esc(t)}" loading="lazy" decoding="async"><span><b>{t}</b><small>{d}</small></span></button>'
                    for f, t, d in HYGIENE)
    return f'''<section class="lz-sec lz-hygiene" id="lz-hijyen">
  {sec_head("Hijyen ve güvenlik", "Detaylar <em>görünür</em>.", "Hepsi salonumuzdaki gerçek uygulamalardan.")}
  <div class="lz-hygrid">{cards}</div>
</section>'''


def price_card(code, link):
    return f'''<section class="lz-sec lz-pricecard" id="lz-fiyat">
  <div class="lz-card lz-foil">
    <span class="lz-over">Fiyat</span>
    <h3>Kişiye özel fiyat</h3>
    <p>Fiyat; bölgeye, seans sayısına ve pakete göre değişir. Tek seans ve 8 seanslık paket seçenekleri var; <b>bitiş garantili paket</b> seçeneğimiz de var.</p>
    <div class="lz-actions">
      {wa_link(code, "fiyat-wa", "Merhaba, lazer epilasyon için fiyat almak istiyorum.", "lz-btn-gold", "Fiyatımı WhatsApp'tan iste")}
      <a class="lz-btn-line" href="{link('fiyat')}#lz-menu" data-track-label="at-{code}-fiyat-menu"><span>Bölge menüsünün tamamı</span>{ICON["arrow"]}</a>
    </div>
  </div>
</section>'''


def menu_section(code):
    def rows_html(g):
        out = []
        for grp in menu_rows(g):
            out.append(f'<div class="lz-mgroup" data-mg="{"seans" if grp["t"] == "Tek seans" else "paket"}">')
            for r in grp["rows"]:
                sess = f'{r["s"]} seans' if r["s"] > 1 else "Tek seans"
                key = r["id"] or ("pkg:" + r["n"] + (" bitiş garantili" if r["g"] else "") + (f" {r['s']} seans paket" if r["s"] > 1 else ""))
                badge = '<em class="lz-badge">Bitiş garantili</em>' if r["g"] else ""
                out.append(f'<div class="lz-mrow"><span class="lz-mnm">{esc(r["n"])}{badge}<small>{sess} · {fmt_min(r)}</small></span><span class="lz-mld"></span>'
                           f'<span class="lz-mpr">Kişiye özel</span><button type="button" class="lz-madd" data-rg="{esc(key)}" aria-pressed="false" aria-label="{esc(r["n"])}: listeme ekle" data-track-label="at-{code}-menu-ekle">+</button></div>')
            out.append("</div>")
        return "".join(out)
    return f'''<section class="lz-sec lz-menu" id="lz-menu">
  {sec_head("Bölge menüsü", "Her bölge, <em>süresiyle</em>", "Randevu sistemimizdeki aktif menü. Fiyat kişiye özel; seçtiklerinizi tek mesajla sorun.")}
  <div class="lz-card">
    <div class="lz-toggles"><div class="lz-seg" role="group" aria-label="Kimin için"><button type="button" data-lz-gender="kadin" aria-pressed="true" data-track-label="at-{code}-menu-cinsiyet">Kadın</button><button type="button" data-lz-gender="erkek" aria-pressed="false" data-track-label="at-{code}-menu-cinsiyet">Erkek</button></div>
    <div class="lz-seg" role="group" aria-label="Seans"><button type="button" data-lz-mg="seans" aria-pressed="true" data-track-label="at-{code}-menu-tur">Tek seans</button><button type="button" data-lz-mg="paket" aria-pressed="false" data-track-label="at-{code}-menu-tur">Paketler</button></div></div>
    <div class="lz-mbody" data-g="kadin">{rows_html("kadin")}</div>
    <div class="lz-mbody" data-g="erkek" hidden>{rows_html("erkek")}</div>
    <p class="lz-menu-src">Bölge adları, süreler ve seans sayıları randevu sistemimizdeki aktif menüden; fiyat bölgelerinize göre WhatsApp'tan iletilir.</p>
  </div>
  <div class="lz-mybar" data-lz-mybar hidden><span data-lz-mycount>Fiyat listem</span>{wa_link(code, "menu-wa", "Merhaba, lazer epilasyon için fiyat almak istiyorum.", "lz-btn-gold", "WhatsApp'tan sor")}</div>
</section>'''


def factors_section():
    cards = "".join(f'<li><b>{t}</b><p>{p}</p></li>' for t, p in FACTORS)
    return f'''<section class="lz-sec lz-factors">
  {sec_head("Fiyatı ne belirler?", "Dört <em>etken</em>")}
  <ol class="lz-fgrid">{cards}</ol>
</section>'''


def tone_section(code):
    tones = "".join(f'<button type="button" class="lz-tone" data-tone="{k}" style="--c:{c}" aria-pressed="false" data-track-label="at-{code}-ton"><i></i><span>{n}</span></button>' for k, c, n in TONES)
    return f'''<section class="lz-sec lz-tonesec" id="lz-ton">
  {sec_head("Nazik başlangıç", "Cildinizi <em>önce tanıyalım</em>", "Cilt tonunuzu seçin; mesajınıza eklensin, uzmanınız ilk ayarı buna göre planlasın.")}
  <div class="lz-card">
    <div class="lz-tones" role="group" aria-label="Cilt tonu">{tones}</div>
    <label class="lz-check"><input type="checkbox" data-lz-sens data-track-label="at-{code}-hassas-isaret"><span>Cildim hassas, ön görüşmede konuşmak istiyorum</span></label>
    <ol class="lz-how"><li><b>Ön değerlendirme</b><p>Cilt tonunuz, kıl yapınız ve hassasiyetiniz konuşulur.</p></li><li><b>Soğutmalı başlık</b><p>Uygulama 10 °C'ye ayarlanabilen soğutmalı başlıkla yapılır.</p></li><li><b>Takip</b><p>Cildinizin yanıtına göre sonraki seans planlanır.</p></li></ol>
    <div class="lz-actions">{wa_link(code, "ton-wa", "Merhaba, hassas cildim için lazer epilasyon ön görüşmesi istiyorum.", "lz-btn-gold lz-shine", "Ön görüşme iste")}</div>
  </div>
</section>'''


def quick_section(code):
    regs = [r for r in region_list("kadin") if r["m"] == 15 and r["z"] != "pkg"]
    chips = "".join(f'<button type="button" class="lz-qchip" data-rg="{r["id"]}" aria-pressed="false" data-track-label="at-{code}-hizli-bolge"><b>{esc(r["n"])}</b><small>15 dk</small></button>' for r in regs)
    return f'''<section class="lz-sec lz-quick" id="lz-hizli">
  {sec_head("15 dakikalık bölgeler", "Tek bölge, <em>kısa seans</em>", "Randevu sistemimizde tek seansı 15 dakika olan kadın bölgeleri. Dokunun, listenize eklensin; erkek bölgeleri haritada.")}
  <div class="lz-qrow">{chips}</div>
</section>'''


def family_section(key, code, media, link):
    tiles = "".join(
        f'<a class="lz-tile" href="{link(k)}" data-track-label="at-{code}-alt-sayfa"><img src="{media}{img}" alt="" loading="lazy" decoding="async"><span><b>{esc(t)}</b><small>{esc(s)}</small></span></a>'
        for k, t, img, s in FAMILY if k != key and not (key == "kamp" and k == "hub"))
    return f'''<section class="lz-sec lz-family" id="lz-sayfalar">
  {sec_head("Lazer sayfalarımız", "Size en yakın <em>plan</em>")}
  <div class="lz-tiles">{tiles}</div>
  <button type="button" class="lz-btn-line lz-allpages" data-lz-menu data-track-label="at-{code}-tum-sayfalar"><span>Tüm sayfalar ve hizmetler</span>{ICON["arrow"]}</button>
</section>'''


def visit_section(code):
    return f'''<section class="lz-sec lz-visit" id="lz-kapi">
  <div class="lz-card lz-visitcard">
    <span class="lz-over">Kapı</span>
    <h3>Konutkent'te, sizi bekliyoruz.</h3>
    <address>Konutkent, 3028. Cd. 8A No:A1<br>06810 Çankaya / Ankara</address>
    <div class="lz-hours"><b>Salı – Pazar</b><span>10.00 – 20.00</span><b>Pazartesi</b><span>Kapalı</span></div>
    <div class="lz-actions lz-row2">
      <a class="lz-btn-line" href="{MAPS}" target="_blank" rel="noopener" data-track-label="at-{code}-yol-tarifi">{ICON["pin"]}<span>Yol tarifi</span></a>
      <a class="lz-btn-line" href="tel:{PHONE_TEL}" data-track-label="at-{code}-kapi-tel">{ICON["tel"]}<span>{PHONE_TXT}</span></a>
    </div>
  </div>
</section>'''


def page_data(key: str, media: str, nav: bool) -> dict:
    """JSON the script reads (regions with CRM minutes, presets, stories, review cards, optional site menu)."""
    rev = load("reviews_laser.json")
    P = PAGES[key]
    regs = {g: region_list(g) for g in ("kadin", "erkek")}
    stories = [
        {"t": "Uygulama", "th": f"{media}lazer-film-jel-poster.webp", "fr": [{"video": f"{media}lazer-film-jel.mp4", "poster": f"{media}lazer-film-jel-poster.webp", "cap": "Jel, ışık, kayış"}, {"video": f"{media}lazer-film-bacak.mp4", "poster": f"{media}lazer-film-bacak-poster.webp", "cap": "Bacakta uygulama"}]},
        {"t": "Yüz", "th": f"{media}lazer-film-cene-poster.webp", "fr": [{"video": f"{media}lazer-film-cene.mp4", "poster": f"{media}lazer-film-cene-poster.webp", "cap": "Çene ve gıdı"}, {"video": f"{media}lazer-film-yuz.mp4", "poster": f"{media}lazer-film-yuz-poster.webp", "cap": "Koruyucu gözlükle"}]},
        {"t": "Cihaz", "th": f"{media}lazer-ekran-480.webp", "fr": [{"img": f"{media}lazer-ekran-1200.webp", "cap": "Lasermach · 3 dalga boyu"}, {"img": f"{media}lazer-5-1200.webp", "cap": "Başlığın ışığı"}]},
        {"t": "Hijyen", "th": f"{media}lazer-kilif-480.webp", "fr": [{"img": f"{media}lazer-kilif-800.webp", "cap": "Kılıflı başlık"}, {"img": f"{media}lazer-uzman-800.webp", "cap": "Eldivenli uygulama"}, {"img": f"{media}lazer-yuz-gozluk-800.webp", "cap": "Koruyucu gözlük"}]},
        {"t": "Yorumlar", "th": f"{media}lazer-koltuk-480.webp", "fr": [{"rv": r} for r in rev["items"][:3]]},
        {"t": "Fiyat", "th": f"{media}lazer-uzman-480.webp", "fr": [{"price": True}]},
    ]
    d = {"page": key, "code": P["code"], "g": P["g"], "media": media, "wa": WA, "regions": regs,
         "pkgParts": PKG_PARTS, "face": sorted(FACE_IDS), "stories": stories, "stats": rev["stats"]}
    if nav:
        d["nav"] = load("nav.json")
    return d


if __name__ == "__main__":
    import sys
    key = sys.argv[1] if len(sys.argv) > 1 else "hub"
    print(page_html(key, "/images/ig/", "Ankara Lazer Epilasyon: Konutkent ve Çayyolu Yakınında Bölge Planı", lambda k: "/" + PAGES[k]["slug"])[:2000])
