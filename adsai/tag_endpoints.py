"""Are the places measurement is sent to actually there?

Two of this account's live defects were of exactly one shape: a destination
that is configured correctly everywhere, and does not exist. The GA4 server
container points at a hostname with no DNS record; the Meta CAPI relay posts to
a path nginx answers 404. Both fail silently, because the senders swallow their
own errors.

Targets are derived from the code, never from a hard-coded list -- the lesson
`monitor_volume.py` paid for. If someone adds a fourth endpoint tomorrow, this
finds it without being told.

Read-only, with one nuance: some endpoints RECORD what is sent to them.
Probing `/api/public/contact-ping` would write a line into the contact log and
corrupt `contact_report.py`; `.../withdraw` revokes a consent. Those are
resolved and reported, never sent to, unless `probe_writes` is set.
"""
from __future__ import annotations

import json
import re
import socket
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

from adsai import config, tag_surface

SITE_ORIGIN = "https://seldagencerbeauty.com"

# Endpoints that record what reaches them. Probing these is a write.
WRITING_PATHS = (
    "/api/public/contact-ping",
    "/api/public/google-ads-attribution/capture",
    "/api/public/google-ads-attribution/withdraw",
    "/api/public/google-ads-attribution/whatsapp-click",
    "/api/public/website-leads",
)

_API_PATH_RE = re.compile(r"""['"](/api/[A-Za-z0-9/_-]+)['"]""")
_ABS_URL_RE = re.compile(r"""['"](https?://[A-Za-z0-9.-]+(?:/[^'"\s]*)?)['"]""")


@dataclass
class Target:
    url: str
    source: str
    writes: bool = False
    method: str = "POST"

    @property
    def host(self) -> str:
        return urlparse(self.url).netloc


@dataclass
class Probe:
    target: Target
    resolved: bool
    status: int | None
    verdict: str          # ok | unreachable | missing | gated | error | not_probed
    detail: str

    def to_dict(self) -> dict:
        return {
            "url": self.target.url,
            "source": self.target.source,
            "verdict": self.verdict,
            "status": self.status,
            "resolved": self.resolved,
            "detail": self.detail,
        }


def _read(path: Path) -> str:
    """Bytes in, text out. These files carry raw control bytes -- see traps.md."""
    return path.read_bytes().decode("utf-8", errors="replace")


def discover(site_dir: Path | None = None, include_gtm: bool = True) -> list[Target]:
    """Every measurement destination the code names."""
    root = site_dir or tag_surface.SITE_DIR
    seen: dict[str, Target] = {}

    def add(url: str, source: str, method: str = "POST") -> None:
        if url.startswith("/"):
            url = SITE_ORIGIN + url
        path = urlparse(url).path
        writes = any(path.startswith(w) for w in WRITING_PATHS)
        seen.setdefault(url, Target(url, source, writes=writes, method=method))

    for js in tag_surface.scripts(root):
        text = _read(js)
        for match in _API_PATH_RE.finditer(text):
            line = text[: match.start()].count("\n") + 1
            add(match.group(1), f"{js.name}:{line}")

    if include_gtm:
        try:
            from adsai import tag_gtm

            for container in tag_gtm.inventory()["containers"]:
                for url, referrers in container.get("server_urls", {}).items():
                    add(url, f"GTM {container['public_id']}: {', '.join(referrers)}", "GET")
        except Exception as exc:  # noqa: BLE001 - GTM is optional here
            seen.setdefault(
                "gtm://unavailable",
                Target("gtm://unavailable", f"GTM okunamadi: {exc}"),
            )

    return sorted(
        (t for t in seen.values() if not t.url.startswith("gtm://")),
        key=lambda t: t.url,
    )


def _resolve(host: str) -> bool:
    try:
        socket.getaddrinfo(host, None)
        return True
    except socket.gaierror:
        return False


def probe(target: Target, probe_writes: bool = False, timeout: int = 10) -> Probe:
    host = target.host
    if not _resolve(host):
        return Probe(
            target, False, None, "unreachable",
            f"DNS kaydi yok: {host}",
        )

    if target.writes and not probe_writes:
        return Probe(
            target, True, None, "not_probed",
            "kayit tutan uc; yoklamak veri yazar (--probe-writes ile acilir)",
        )

    request = urllib.request.Request(
        target.url,
        data=b"{}" if target.method == "POST" else None,
        method=target.method,
        headers={"Content-Type": "application/json", "User-Agent": "tagctx/1"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status
    except urllib.error.HTTPError as exc:
        status = exc.code
    except Exception as exc:  # noqa: BLE001
        return Probe(target, True, None, "error", f"{type(exc).__name__}: {exc}")

    if status in (404, 410):
        verdict, detail = "missing", f"HTTP {status}: uc mevcut degil"
    elif status >= 500:
        verdict, detail = "error", f"HTTP {status}: sunucu hatasi"
    elif status in (401, 403, 400, 422):
        # An empty body is meant to be refused; this says the route exists.
        verdict, detail = "gated", f"HTTP {status}: uc var, bos govdeyi reddetti"
    else:
        verdict, detail = "ok", f"HTTP {status}"
    return Probe(target, True, status, verdict, detail)


def survey(probe_writes: bool = False, include_gtm: bool = True) -> dict:
    probes = [probe(t, probe_writes=probe_writes) for t in discover(include_gtm=include_gtm)]
    broken = [p for p in probes if p.verdict in ("unreachable", "missing", "error")]
    return {
        "as_of": config.now_iso(),
        "probed": len(probes),
        "broken": len(broken),
        "probes": probes,
    }
