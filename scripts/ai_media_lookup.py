#!/usr/bin/env python3
"""Compact, non-visual lookup for the curated Instagram media catalog.

This tool intentionally reads metadata only. It helps AI agents shortlist media
without opening hundreds of images or videos.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_CANDIDATES = (
    ROOT / "sources/media_ig_20261007/manifest.json",
    ROOT / "patches/media_ig_20261007/manifest.json",
)
INDEX_CANDIDATES = (
    ROOT / "website/m/ig/media_index.json",
    ROOT / "patches/media_ig_20261007/out/images/ig/media_index.json",
)


def existing(candidates: tuple[Path, ...], label: str) -> Path:
    for path in candidates:
        if path.is_file():
            return path
    checked = ", ".join(str(path) for path in candidates)
    raise SystemExit(f"{label} bulunamadı. Bakılan yollar: {checked}")


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def catalog() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest = load_json(existing(MANIFEST_CANDIDATES, "manifest"))
    media_index = load_json(existing(INDEX_CANDIDATES, "media index"))
    return manifest.get("items", []), media_index


def slim(item: dict[str, Any], media_index: dict[str, Any]) -> dict[str, Any]:
    indexed = media_index.get(item.get("slug", ""), {})
    return {
        "slug": item.get("slug"),
        "id": item.get("id"),
        "fam": item.get("fam"),
        "kind": item.get("kind"),
        "alt": item.get("alt"),
        "date": indexed.get("date"),
        "duration": indexed.get("dur"),
        "width": indexed.get("w"),
        "height": indexed.get("h"),
        "poster": indexed.get("poster"),
        "video": indexed.get("mp4"),
        "permalink": indexed.get("permalink"),
    }


def emit(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def command_summary(_: argparse.Namespace) -> None:
    items, _ = catalog()
    families: dict[str, int] = {}
    kinds: dict[str, int] = {}
    for item in items:
        family = str(item.get("fam", "unknown"))
        kind = str(item.get("kind", "unknown"))
        families[family] = families.get(family, 0) + 1
        kinds[kind] = kinds.get(kind, 0) + 1
    emit({"total": len(items), "families": families, "kinds": kinds})


def command_search(args: argparse.Namespace) -> None:
    items, media_index = catalog()
    query = args.query.casefold().strip()
    found = []
    for item in items:
        if args.family and item.get("fam") != args.family:
            continue
        if args.kind and item.get("kind") != args.kind:
            continue
        haystack = " ".join(
            str(item.get(field, "")) for field in ("slug", "id", "fam", "kind", "alt")
        ).casefold()
        if query and query not in haystack:
            continue
        found.append(slim(item, media_index))
        if len(found) >= args.limit:
            break
    emit({"count": len(found), "limit": args.limit, "items": found})


def command_show(args: argparse.Namespace) -> None:
    items, media_index = catalog()
    for item in items:
        if args.slug_or_id in (item.get("slug"), str(item.get("id"))):
            emit({"manifest": item, "index": media_index.get(item.get("slug", ""))})
            return
    raise SystemExit(f"Kayıt bulunamadı: {args.slug_or_id}")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description="Medya açmadan seçilmiş Instagram kataloğunu sorgula."
    )
    commands = root.add_subparsers(dest="command", required=True)

    summary = commands.add_parser("summary", help="Aile ve tür sayılarını göster.")
    summary.set_defaults(func=command_summary)

    search = commands.add_parser("search", help="Slug, ID veya açıklamada ara.")
    search.add_argument("query", nargs="?", default="")
    search.add_argument("--family", help="Örn. lazer, pmu, cilt")
    search.add_argument("--kind", help="Örn. image veya video")
    search.add_argument("--limit", type=int, default=6)
    search.set_defaults(func=command_search)

    show = commands.add_parser("show", help="Tek slug veya Instagram ID ayrıntısı.")
    show.add_argument("slug_or_id")
    show.set_defaults(func=command_show)
    return root


def main() -> None:
    args = parser().parse_args()
    if getattr(args, "limit", 1) < 1:
        raise SystemExit("--limit en az 1 olmalı")
    args.func(args)


if __name__ == "__main__":
    main()
