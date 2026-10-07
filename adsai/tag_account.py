"""The Google Ads side of the tag picture: conversion actions and what they record.

Pulls the conversion-action inventory together with a 30-day conversion count
and caches it, so the cross-reference in :mod:`adsai.tag_audit` can run without
a network round trip.

Read-only.  SELECT-only GAQL; nothing here mutates the account.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path

from adsai import config

TAG_DIR = config.DATA_DIR / "tag"
TAG_DIR.mkdir(parents=True, exist_ok=True)
LATEST = TAG_DIR / "inventory-latest.json"

LABEL_RE = re.compile(r"AW-\d+/[A-Za-z0-9_-]+")

# Types whose conversions can only ever arrive from a tag on the site.  These
# are the ones the site is answerable for; GOOGLE_HOSTED (Maps local actions),
# UPLOAD_CLICKS (offline) and the GA4 imports are not.
TAG_BORNE = {"WEBPAGE", "WEBSITE_CALL", "CLICK_TO_CALL"}


@dataclass
class ConversionAction:
    id: str
    name: str
    status: str
    type: str
    category: str
    primary_for_goal: bool
    counting_type: str
    labels: list[str] = field(default_factory=list)
    conversions_30d: float = 0.0
    default_value: float | None = None
    always_use_default_value: bool | None = None

    @property
    def is_tag_borne(self) -> bool:
        return self.type in TAG_BORNE or bool(self.labels)

    def to_dict(self) -> dict:
        return asdict(self)


_INVENTORY_GAQL = """
SELECT conversion_action.id,
       conversion_action.name,
       conversion_action.status,
       conversion_action.type,
       conversion_action.category,
       conversion_action.primary_for_goal,
       conversion_action.counting_type,
       conversion_action.tag_snippets,
       conversion_action.value_settings.default_value,
       conversion_action.value_settings.always_use_default_value
FROM conversion_action
"""

# Summed from daily rows, so this is an atom sum and may be differenced.  It is
# deliberately not the rolling P30D aggregate that data/snapshots/*.json carries
# and that must never be differenced -- see references/traps.md, measurement.
_METRICS_GAQL = """
SELECT conversion_action.id, metrics.all_conversions
FROM conversion_action
WHERE segments.date DURING LAST_30_DAYS
"""


_GOALS_GAQL = """
SELECT customer_conversion_goal.category,
       customer_conversion_goal.origin,
       customer_conversion_goal.biddable
FROM customer_conversion_goal
"""

_SETTINGS_GAQL = """
SELECT customer.id,
       customer.conversion_tracking_setting.conversion_tracking_status,
       customer.conversion_tracking_setting.enhanced_conversions_for_leads_enabled
FROM customer
"""


def _rows(query: str) -> list[dict]:
    from google.protobuf.json_format import MessageToDict

    from client import get_client, get_customer_id

    client = get_client()
    service = client.get_service("GoogleAdsService")
    out: list[dict] = []
    for batch in service.search_stream(customer_id=get_customer_id(), query=query):
        for row in batch.results:
            out.append(MessageToDict(row._pb, preserving_proto_field_name=True))
    return out


def pull() -> list[ConversionAction]:
    """Fetch the live inventory and cache it."""
    counts: dict[str, float] = {}
    for row in _rows(_METRICS_GAQL):
        cid = row["conversion_action"]["id"]
        counts[cid] = counts.get(cid, 0.0) + float(
            row.get("metrics", {}).get("all_conversions", 0) or 0
        )

    actions: list[ConversionAction] = []
    for row in _rows(_INVENTORY_GAQL):
        ca = row["conversion_action"]
        snippets = ca.get("tag_snippets", []) or []
        values = ca.get("value_settings", {}) or {}
        actions.append(
            ConversionAction(
                id=ca.get("id", ""),
                name=ca.get("name", ""),
                status=ca.get("status", ""),
                # MessageToDict renders the reserved word `type` as `type_`.
                type=ca.get("type_", ca.get("type", "")),
                category=ca.get("category", ""),
                primary_for_goal=bool(ca.get("primary_for_goal", False)),
                counting_type=ca.get("counting_type", ""),
                labels=sorted(set(LABEL_RE.findall(json.dumps(snippets)))),
                conversions_30d=counts.get(ca.get("id", ""), 0.0),
                default_value=values.get("default_value"),
                always_use_default_value=values.get("always_use_default_value"),
            )
        )

    actions.sort(key=lambda a: (-a.conversions_30d, a.name))
    payload = {
        "as_of": config.now_iso(),
        "window": "P1D-sum-30",  # daily atoms summed, not a rolling aggregate
        "count": len(actions),
        "actions": [a.to_dict() for a in actions],
    }
    LATEST.write_text(json.dumps(payload, ensure_ascii=False, indent=1))
    return actions


def load(offline: bool = False) -> tuple[list[ConversionAction], str]:
    """Return the inventory and the timestamp it is as of.

    With ``offline`` the cache is used as-is; otherwise the account is pulled
    afresh and the cache is only a fallback when the API is unreachable.
    """
    if not offline:
        try:
            actions = pull()
            return actions, json.loads(LATEST.read_text())["as_of"]
        except Exception as exc:  # noqa: BLE001 - fall back, but say why
            if not LATEST.exists():
                raise
            print(f"[tag_account] live pull failed ({exc}); using cache", flush=True)
    if not LATEST.exists():
        raise FileNotFoundError(f"no cached inventory at {LATEST}; run without --offline")
    payload = json.loads(LATEST.read_text())
    return [ConversionAction(**a) for a in payload["actions"]], payload["as_of"]


def biddable_categories() -> set[str]:
    """Goal categories bidding actually optimises toward.

    A dead conversion action only costs something when its category is one of
    these -- that is what makes it a goal rather than a statistic.
    """
    out: set[str] = set()
    for row in _rows(_GOALS_GAQL):
        goal = row.get("customer_conversion_goal", {})
        if goal.get("biddable"):
            out.add(goal.get("category", ""))
    return out


def account_settings() -> dict:
    """Account-level measurement switches, for checking they are actually fed."""
    rows = _rows(_SETTINGS_GAQL)
    if not rows:
        return {}
    setting = rows[0].get("customer", {}).get("conversion_tracking_setting", {})
    return {
        "conversion_tracking_status": setting.get("conversion_tracking_status"),
        "enhanced_conversions_for_leads": bool(
            setting.get("enhanced_conversions_for_leads_enabled", False)
        ),
    }
