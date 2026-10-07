"""Drive a real browser and turn what it sees into findings.

Static analysis proves a tag is reachable. Only a browser proves it fires, and
some defects have no other detector at all: a second Ads destination attached
to the Google tag outside every container shows up in nothing but the live
`tids=` parameter.

This is also the deploy gate. The regression that took this site's lead
tracking down for five hours was visible in the first second of a page load;
nothing was looking.

Nothing reaches Google -- `tag_probe.mjs` records every measurement request and
aborts it.
"""
from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from adsai import config

TOOLS_DIR = config.ROOT_DIR / "tagtools"
PROBE = TOOLS_DIR / "tag_probe.mjs"
BROWSERS = TOOLS_DIR / "browsers"
SITE_ORIGIN = "https://seldagencerbeauty.com"

# The destination every ad landing page must end up configuring.
ADS_DESTINATION = "AW-11538067972"

# A deploy gate cannot afford 124 pages. These cover the shapes that differ:
# the home page, a service landing page, a location page, an offer page and the
# price menu, which is the one page built differently from the rest.
DEFAULT_SAMPLE = (
    "index.html",
    "protez-tirnak.html",
    "erkek-lazer-epilasyon.html",
    "konum.html",
    "price-menu.html",
)


class ProbeFailed(RuntimeError):
    pass


@dataclass
class PageResult:
    page: str
    ok: bool
    page_errors: list[str]
    gtag_configured: bool
    ads_destination_seen: bool
    hit_counts: dict
    detail: str

    def to_dict(self) -> dict:
        return {
            "page": self.page,
            "ok": self.ok,
            "page_errors": self.page_errors,
            "gtag_configured": self.gtag_configured,
            "ads_destination_seen": self.ads_destination_seen,
            "hit_counts": self.hit_counts,
            "detail": self.detail,
        }


def probe(url: str, consent: str = "granted", scenario: str = "load",
          timeout: int = 90) -> dict:
    if not PROBE.exists():
        raise ProbeFailed(f"prober yok: {PROBE}")
    env = {**os.environ, "PLAYWRIGHT_BROWSERS_PATH": str(BROWSERS)}
    result = subprocess.run(
        ["node", str(PROBE), "--url", url, "--consent", consent,
         "--scenario", scenario],
        cwd=str(TOOLS_DIR), env=env, capture_output=True, text=True, timeout=timeout,
    )
    if result.returncode != 0:
        raise ProbeFailed(f"prober cikis {result.returncode}: {result.stderr[:300]}")
    try:
        return json.loads(result.stdout[result.stdout.index("{"):])
    except (ValueError, json.JSONDecodeError) as exc:
        raise ProbeFailed(f"prober ciktisi okunamadi: {exc}") from exc


def check_page(page: str, consent: str = "granted") -> PageResult:
    """One page, load scenario, judged against what an ad landing page must do."""
    url = page if page.startswith("http") else f"{SITE_ORIGIN}/{page.lstrip('/')}"
    data = probe(url, consent=consent, scenario="load")

    page_errors = data.get("page_errors", [])
    state = data.get("page_state") or {}
    gtag_ok = bool(state.get("gtag_is_function"))
    hits = data.get("hit_counts", {})
    ads_seen = any(k.startswith(ADS_DESTINATION) for k in hits)

    problems = []
    if page_errors:
        problems.append(f"sayfa hatasi: {'; '.join(page_errors[:3])}")
    if not gtag_ok:
        problems.append("window.gtag fonksiyon degil")
    if not ads_seen:
        problems.append(f"{ADS_DESTINATION} icin hic hit gitmedi")

    return PageResult(
        page=page,
        ok=not problems,
        page_errors=page_errors,
        gtag_configured=gtag_ok,
        ads_destination_seen=ads_seen,
        hit_counts=hits,
        detail="; ".join(problems) if problems else "temiz",
    )


def verify(pages: list[str] | None = None, consent: str = "granted") -> dict:
    """The deploy gate. Non-zero exit when a page stops measuring."""
    targets = pages or list(DEFAULT_SAMPLE)
    results: list[PageResult] = []
    for page in targets:
        try:
            results.append(check_page(page, consent=consent))
        except (ProbeFailed, subprocess.TimeoutExpired) as exc:
            results.append(
                PageResult(page, False, [], False, False, {},
                           f"yoklanamadi: {type(exc).__name__}: {exc}")
            )
    failed = [r for r in results if not r.ok]
    return {
        "as_of": config.now_iso(),
        "consent": consent,
        "checked": len(results),
        "failed": len(failed),
        "results": results,
    }
