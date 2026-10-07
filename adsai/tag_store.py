"""Remember what the tags looked like, so a regression has something to differ from.

A finding list says what is wrong now. It cannot say what became wrong today --
and that is the question worth answering, because a defect that appeared in the
last few hours is a deploy, while one that has been open for weeks is a
backlog item.

Runs are written to the AdsCtx store as artifacts rather than to loose files,
which buys the store's as-of semantics and keeps one place to look.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

from adsai import config
from adsai.ctx_schema import open_store

KIND = "tag_audit"


def _path_for(as_of: str) -> str:
    return f"tag/audit/{as_of}.json"


def record(report: dict) -> str:
    """Persist one audit run. Returns the artifact path."""
    findings = [
        f.to_dict() if hasattr(f, "to_dict") else f
        for f in report.get("findings", [])
    ]
    body = {
        "as_of": report.get("as_of"),
        "pages_scanned": report.get("pages_scanned"),
        "actions_scanned": report.get("actions_scanned"),
        "counts": report.get("counts"),
        "finding_ids": [f["id"] for f in findings],
        "findings": findings,
    }
    path = _path_for(report.get("as_of") or config.now_iso())
    conn = open_store()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO artifact "
            "(path, kind, schema_version, status, body_json) VALUES (?,?,?,?,?)",
            (path, KIND, "tagctx-1", "recorded", json.dumps(body, ensure_ascii=False)),
        )
        conn.commit()
    finally:
        conn.close()
    return path


def runs(limit: int = 30) -> list[dict]:
    """Past audit runs, newest first."""
    conn = open_store()
    try:
        rows = conn.execute(
            "SELECT path, body_json FROM artifact WHERE kind = ? "
            "ORDER BY path DESC LIMIT ?",
            (KIND, limit),
        ).fetchall()
    finally:
        conn.close()
    out = []
    for row in rows:
        try:
            out.append({"path": row["path"], **json.loads(row["body_json"])})
        except (ValueError, TypeError):
            continue
    return out


@dataclass
class Diff:
    newer: str
    older: str
    opened: list[dict]
    closed: list[str]
    unchanged: int

    def to_dict(self) -> dict:
        return {
            "newer": self.newer,
            "older": self.older,
            "opened": self.opened,
            "closed": self.closed,
            "unchanged": self.unchanged,
        }


def diff(since: str | None = None) -> Diff | None:
    """What changed between the newest run and the one before it (or before ``since``).

    ``opened`` carries the whole finding, because a newly opened critical is the
    thing someone has to act on and it should not need a second lookup.
    """
    history = runs(limit=60)
    if len(history) < 2:
        return None
    newest = history[0]
    if since:
        older = next(
            (r for r in history[1:] if (r.get("as_of") or "") <= since),
            history[-1],
        )
    else:
        older = history[1]

    new_ids = {f["id"]: f for f in newest.get("findings", [])}
    old_ids = set(older.get("finding_ids", []))
    opened = [f for fid, f in new_ids.items() if fid not in old_ids]
    closed = sorted(old_ids - set(new_ids))
    return Diff(
        newer=newest.get("as_of", ""),
        older=older.get("as_of", ""),
        opened=opened,
        closed=closed,
        unchanged=len(set(new_ids) & old_ids),
    )
