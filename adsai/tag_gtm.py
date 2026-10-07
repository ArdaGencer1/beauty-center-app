"""Read the Tag Manager containers behind the site.

The web container is what the page loads; the server-side container is where
the web one forwards GA4. Neither is on disk, so until this module can
authenticate, `tag_audit` can say a conversion arrives from somewhere it cannot
see, but not from which tag.

Read-only. Every call is a GET; nothing here creates, updates or publishes a
version, whatever permission the credential happens to carry.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from adsai import config

def _key_path() -> Path | None:
    """Where the service account key lives.

    ADSAI_GTM_KEY wins; otherwise the known locations are tried in order, so a
    key already placed for another tool is not duplicated just to be found.
    """
    import os

    override = os.getenv("ADSAI_GTM_KEY", "").strip()
    candidates = [Path(override)] if override else []
    candidates += [
        config.ROOT_DIR / ".gtm-sa.json",
        config.ROOT_DIR.parent / "all_api_google"
        / "nomadic-ocean-505508-q2-13030c4e8fb8.json",
    ]
    return next((c for c in candidates if c.exists()), None)
SCOPES = ["https://www.googleapis.com/auth/tagmanager.readonly"]
API = "https://tagmanager.googleapis.com/tagmanager/v2"


class GtmUnavailable(RuntimeError):
    """Raised when the container cannot be read, with what to do about it."""


def _session():
    try:
        from google.auth.transport.requests import AuthorizedSession
        from google.oauth2 import service_account
    except ImportError as exc:  # pragma: no cover - the libs ship with google-ads
        raise GtmUnavailable(f"google-auth eksik: {exc}") from exc

    key = _key_path()
    if key is None:
        raise GtmUnavailable(
            "service account anahtari bulunamadi (ADSAI_GTM_KEY ile yol verin)\n"
            "  1) anahtari oraya koyun, chmod 600\n"
            "  2) projede Tag Manager API etkin olsun (nomadic-ocean-505508-q2)\n"
            "  3) service account GTM hesabinda kullanici olarak ekli olsun"
        )
    creds = service_account.Credentials.from_service_account_file(
        str(key), scopes=SCOPES
    )
    return AuthorizedSession(creds)


def _get(session, path: str) -> dict:
    response = session.get(f"{API}/{path}" if not path.startswith("http") else path)
    if response.status_code == 403:
        raise GtmUnavailable(
            "403: kimlik dogrulandi ama GTM erisimi yok. Service account'un "
            "e-postasi Tag Manager hesabinda kullanici olarak ekli mi, ve "
            "projede Tag Manager API etkin mi?"
        )
    if response.status_code >= 400:
        raise GtmUnavailable(f"{response.status_code}: {response.text[:300]}")
    return response.json()


def _setting_pairs(node) -> list[tuple[str, str]]:
    """Pull (parameter, parameterValue) pairs out of a tag's settings tables.

    GTM nests these as a list of `map` entries, each holding a `parameter` key
    and a `parameterValue` key as sibling templates. Walking the structure is
    duller than a regex over the JSON and it does not miss a pair because the
    serialiser spaced it differently.
    """
    pairs: list[tuple[str, str]] = []

    def walk(n) -> None:
        if isinstance(n, dict):
            if n.get("type") == "map":
                entries = {
                    e.get("key"): e.get("value")
                    for e in n.get("map", [])
                    if isinstance(e, dict)
                }
                name, value = entries.get("parameter"), entries.get("parameterValue")
                if name and value:
                    pairs.append((name, value))
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)

    walk(node)
    return pairs


@dataclass
class Container:
    account_id: str
    container_id: str
    public_id: str
    name: str
    usage_context: list[str] = field(default_factory=list)
    path: str = ""

    def to_dict(self) -> dict:
        return {
            "public_id": self.public_id,
            "name": self.name,
            "usage_context": self.usage_context,
            "path": self.path,
        }


def containers() -> list[Container]:
    """Every container the credential can see, across every account."""
    session = _session()
    out: list[Container] = []
    for account in _get(session, "accounts").get("account", []):
        listing = _get(session, f"{account['path']}/containers")
        for c in listing.get("container", []):
            out.append(
                Container(
                    account_id=account.get("accountId", ""),
                    container_id=c.get("containerId", ""),
                    public_id=c.get("publicId", ""),
                    name=c.get("name", ""),
                    usage_context=c.get("usageContext", []),
                    path=c.get("path", ""),
                )
            )
    return out


def _live_workspace(session, container_path: str) -> str:
    workspaces = _get(session, f"{container_path}/workspaces").get("workspace", [])
    if not workspaces:
        raise GtmUnavailable(f"{container_path}: workspace yok")
    # The default workspace carries what is staged; it is the closest readable
    # thing to what a published version contains.
    for w in workspaces:
        if w.get("name", "").lower().startswith("default"):
            return w["path"]
    return workspaces[0]["path"]


def inventory(public_id: str | None = None) -> dict:
    """Tags, triggers and variables, with the Ads/GA4 ids each tag carries."""
    session = _session()
    found = [c for c in containers() if not public_id or c.public_id == public_id]
    if not found:
        raise GtmUnavailable(f"container bulunamadi: {public_id}")

    result = {"as_of": config.now_iso(), "containers": []}
    for container in found:
        workspace = _live_workspace(session, container.path)
        tags = _get(session, f"{workspace}/tags").get("tag", [])
        triggers = _get(session, f"{workspace}/triggers").get("trigger", [])
        variables = _get(session, f"{workspace}/variables").get("variable", [])

        trigger_names = {t["triggerId"]: t.get("name", "") for t in triggers}
        # Where a tag forwards GA4 to. A container can be configured perfectly
        # and point at a hostname that does not resolve, which is exactly the
        # shape of this account's dead server-side setup -- so the destination
        # is carried out of here for `tag_endpoints` to actually dial.
        server_urls: dict[str, list[str]] = {}
        paused_server_urls: dict[str, list[str]] = {}
        tag_rows = []
        for tag in tags:
            blob = json.dumps(tag)
            for key, value in _setting_pairs(tag):
                if key in ("server_container_url", "transport_url"):
                    # Several tags usually name the same destination; keep every
                    # referrer, or removing one tag looks like removing the URL.
                    # A paused tag sends nothing (GTM v35 paused the dead-host
                    # senders), so its destination is listed, not dialled.
                    (paused_server_urls if tag.get("paused") else server_urls).setdefault(
                        value, []).append(f"{tag.get('name', '')} ({key})")
            tag_rows.append({
                "name": tag.get("name", ""),
                "type": tag.get("type", ""),
                "paused": tag.get("paused", False),
                "firing_on": [trigger_names.get(t, t) for t in tag.get("firingTriggerId", [])],
                # Whatever destination ids the tag carries, however they are nested.
                # The lookbehind matters: without it the tail of a conversion
                # label ("...VG-ZCMma0_UbEITk4_0q") is reported as a destination
                # id of its own ("G-ZCMma0_UbEITk4_0q").
                "ids": sorted(set(
                    __import__("re").findall(
                        r"(?<![A-Za-z0-9_-])(?:AW|G|GT|DC)-[A-Za-z0-9_-]{6,}", blob
                    )
                )),
                "conversion_labels": sorted(set(
                    __import__("re").findall(r"AW-\d+/[A-Za-z0-9_-]+", blob)
                )),
            })

        result["containers"].append({
            **container.to_dict(),
            "server_urls": server_urls,
            "paused_server_urls": paused_server_urls,
            "tag_count": len(tags),
            "trigger_count": len(triggers),
            "variable_count": len(variables),
            "tags": tag_rows,
            "triggers": [{"name": t.get("name", ""), "type": t.get("type", "")} for t in triggers],
        })
    return result
