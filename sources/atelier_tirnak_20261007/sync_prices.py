#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TIRNAK ATELYESİ -- refresh data/crm_tirnak.json from the CRM price menu (/api/public/price-menu).

Run it where the site is reachable (the server); a Claude container's network policy may not allow the host.

  python3 sources/atelier_tirnak_20261007/sync_prices.py                    # dry run: what would change
  python3 sources/atelier_tirnak_20261007/sync_prices.py --write            # update data/crm_tirnak.json
  python3 sources/atelier_tirnak_20261007/sync_prices.py --file menu.json   # a saved copy of the endpoint

The menu's JSON shape is not pinned here: every object that carries a name and a price is an option, and the names of
the objects above it (service, category) are its context. Each page id has a rule on that text. An id gets a price only
when exactly one option matches it (or several with the same price and minutes); everything else stays "fiyatı sorun"
and is printed for a person to decide. Prices are never guessed. Then rebuild: build_proto.py picks the rows up
everywhere (menus, planner, price chips, FAQ minutes, comparison cards).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import ssl
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CRM_FILE = HERE / "data" / "crm_tirnak.json"
URL = "https://seldagencerbeauty.com/api/public/price-menu"

NAME_KEYS = ("name", "title", "ad", "label", "optionName", "serviceName")
PRICE_KEYS = ("price", "fiyat", "amount", "unitPrice", "priceTl")
CAMPAIGN_KEYS = ("campaignPrice", "discountedPrice", "salePrice", "kampanyaFiyat")
MIN_KEYS = ("duration", "durationMinutes", "durationMin", "minutes", "min", "sure", "süre")
CTX_KEYS = ("service", "category", "kategori", "group")  # context only, never an option name
NAIL = ("tırnak", "oje", "manikür", "pedikür", "nail", "tips", "protez", "el ve ayak", "el ayak")

# id -> all of / one of / none of (substrings of the normalised "context + name" text)
RULES = {
    "oje": dict(all=["kalıcı oje"], none=["manikür", "pedikür", "protez", "jel", "ayak", "çıkar"]),
    "mko": dict(all=["manikür", "kalıcı oje"], none=["jel", "protez", "pedikür"]),
    "mjk": dict(all=["manikür", "jel", "kalıcı oje"], none=["protez", "pedikür"]),
    "mpk": dict(all=["manikür", "protez", "kalıcı oje"], none=["ayak", "pedikür", "bakım", "dolgu", "çıkar"]),
    "art": dict(any=["nail art", "nailart"]),
    "manikur": dict(all=["manikür"], none=["oje", "pedikür", "jel", "protez"]),
    "pedikur": dict(all=["pedikür"], none=["manikür", "medikal", "oje", "protez"]),
    "mp": dict(all=["manikür", "pedikür"], none=["oje", "protez", "medikal"]),
    "medped": dict(all=["medikal pedikür"], none=["manikür"]),
    "elayak": dict(any=["el ve ayak", "el ayak"]),
    "uzatma": dict(all=["uzatma"], none=["kirpik", "protez"]),
    "dolgu": dict(all=["protez"], any=["bakım", "dolgu"], none=["ayak", "çıkar"]),
    "cikar": dict(all=["protez"], any=["çıkarma", "çıkartma", "çıkarım", "sökme"]),
    "tips": dict(all=["tips"]),
    "ayak": dict(all=["ayak", "protez"]),
}
CORE = ("oje", "mko", "mjk", "mpk")  # the page texts quote their minutes: these must keep a duration


def norm(s: str) -> str:
    """Turkish lower case, punctuation out, and ı folded into i so "NAIL ART" and "KALICI" match either spelling."""
    s = s.replace("I", "ı").replace("İ", "i").lower()
    return " ".join(re.sub(r"[^0-9a-zçğıöşü]+", " ", s).split()).replace("ı", "i")


def num(v) -> int | None:
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, (int, float)):
        return int(round(v)) if v > 0 else None
    if isinstance(v, str):
        t = re.sub(r"[^\d.,]", "", v)
        if not t:
            return None
        t = re.sub(r"[.,]\d{1,2}$", "", t) if re.search(r"[.,]\d{1,2}$", t) and len(t) > 3 else t
        t = t.replace(".", "").replace(",", "")
        return int(t) if t.isdigit() and int(t) > 0 else None
    return None


def text_of(d: dict) -> str | None:
    for k in NAME_KEYS:
        if isinstance(d.get(k), str) and d[k].strip():
            return d[k].strip()
    return None


def num_of(d: dict, keys: tuple[str, ...]) -> int | None:
    for k in keys:
        v = num(d.get(k))
        if v is not None:
            return v
    return None


def options(node, ctx: list[str]):
    if isinstance(node, list):
        for v in node:
            yield from options(v, ctx)
    elif isinstance(node, dict):
        name = text_of(node)
        own = [node[k].strip() for k in CTX_KEYS if isinstance(node.get(k), str) and node[k].strip() and node[k].strip() != name]
        price, camp = num_of(node, PRICE_KEYS), num_of(node, CAMPAIGN_KEYS)
        if name and (price or camp):
            yield {"ctx": " / ".join(ctx + own), "name": name, "p": camp or price, "list": price, "campaign": bool(camp and camp != price),
                   "d": num_of(node, MIN_KEYS)}
        sub = ctx + own + ([name] if name else [])
        for v in node.values():
            if isinstance(v, (dict, list)):
                yield from options(v, sub)


def label(o: dict) -> str:
    return " / ".join(x for x in (o["ctx"], o["name"]) if x)


def matches(rule: dict, text: str) -> bool:
    has = lambda t: norm(t) in text  # noqa: E731
    return (all(has(t) for t in rule.get("all", [])) and (not rule.get("any") or any(has(t) for t in rule["any"]))
            and not any(has(t) for t in rule.get("none", [])))


def load(a) -> dict:
    if a.file:
        try:
            return json.loads(Path(a.file).read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            raise SystemExit(f"could not read {a.file}: {e}")
    req = urllib.request.Request(a.url, headers={"Accept": "application/json", "User-Agent": "sgb-sync-prices/1"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=ssl.create_default_context()) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001 -- one clear line instead of a traceback
        raise SystemExit(f"could not read {a.url}: {e}\n(run this on the server, or save the endpoint and pass --file)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default=URL)
    ap.add_argument("--file", default="")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    menu = load(a)
    crm = json.loads(CRM_FILE.read_text(encoding="utf-8"))
    old_rows = {r["id"]: r for r in crm["rows"]}
    names = {r["id"]: r["n"] for r in crm["rows"] + crm["ask"]}
    extra = {r["id"]: {k: v for k, v in r.items() if k in ("s",)} for r in crm["ask"]}

    opts = [o for o in options(menu, []) if any(norm(w) in norm(o["ctx"] + " " + o["name"]) for w in NAIL)]
    print(f"{len(opts)} nail options in the menu")
    rows, ask, used, notes = [], [], set(), []
    for i in names:
        # the option's own name first; its category only when the name alone says too little ("BAKIM" under "PROTEZ TIRNAK")
        hit = [o for o in opts if matches(RULES[i], norm(o["name"]))] or [o for o in opts if matches(RULES[i], norm(o["ctx"] + " " + o["name"]))]
        same = {(o["p"], o["d"]) for o in hit}
        if len(same) == 1 and not (i in CORE and hit[0]["d"] is None):
            o = hit[0]
            used.update(id(x) for x in hit)
            prev = old_rows.get(i, {})
            b = "Kampanya" if o["campaign"] else (prev.get("b") if prev.get("p") == o["p"] else None)
            rows.append({k: v for k, v in {"id": i, "n": names[i], "p": o["p"], "d": o["d"], "b": b, "crm": label(o)}.items() if v is not None})
            was = f'{prev["p"]} TL / {prev.get("d")} dk' if prev else "fiyatı sorun"
            print(f'  {i:8} {was:>18} -> {o["p"]} TL / {o["d"]} dk   [{rows[-1]["crm"]}]')
        else:
            found = "; ".join(f'{label(o)} = {o["p"]} TL, {o["d"]} dk' for o in hit) or "no match"
            if i in old_rows:
                rows.append(old_rows[i])
                notes.append(f"{i}: kept {old_rows[i]['p']} TL from the file; the menu gives {found}")
            else:
                ask.append({"id": i, "n": names[i], **extra.get(i, {})})
                if hit:
                    notes.append(f"{i}: left as 'fiyatı sorun'; the menu gives {found}")
    for n in notes:
        print("  ! " + n)
    left = [o for o in opts if id(o) not in used]
    if left:
        print(f"  nail options no page uses ({len(left)}):")
        for o in left:
            print(f'    {label(o)}: {o["p"]} TL, {o["d"]} dk')
    if not a.write:
        print("dry run; --write updates " + str(CRM_FILE.relative_to(HERE.parents[1])))
        return 0
    order = list(names)
    crm.update({"_doc": "Nail rows of the CRM price menu (/api/public/price-menu), written by sync_prices.py. Ids without a single clear "
                        "match stay in 'ask' and show 'fiyatı sorun'.",
                "as_of": dt.date.today().isoformat(), "rows": sorted(rows, key=lambda r: order.index(r["id"])), "ask": ask})
    if isinstance(menu, dict) and menu.get("version"):
        crm["version"] = menu["version"]
    CRM_FILE.write_text(json.dumps(crm, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {CRM_FILE.name}: {len(rows)} priced, {len(ask)} ask")
    return 0


if __name__ == "__main__":
    sys.exit(main())
