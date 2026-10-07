# -*- coding: utf-8 -*-
"""AdsCtx store schema: unbounded storage, bounded queries.

`data/context/latest.json` is byte-capped because every session loads it, and on
2026-09-13 that cap silently emptied `recent_months` and `recent_cohorts` -- the
exact series Rulles.txt compares for a keep/revert call -- before the run died
outright for five days.  This store is the opposite shape: it keeps everything and
bounds only what a query returns.

Four invariants, each one earned from a measured failure:

1. Append-only.  Rows are never updated in place; a correction is a new row and
   the old one is marked superseded.  "What did we know on 2026-09-13?" has to
   stay answerable, because judging a past decision on today's data is unfair.
2. Every row carries provenance: `source_sha` (content hash of the artifact it
   came from) plus `run_id`.  A claim with no source does not enter the store.
3. Observations carry a `window`.  Snapshot rows are 30-day rolling aggregates
   (`date_range=2026-08-20..2026-09-18`), NOT daily values, and a rolling window
   cannot be de-aggregated.  Mixing the two silently would corrupt every
   before/after comparison, so the period is part of the key.
4. Entity ids are `^[a-z0-9_]+$` so the same ids can later be emitted as a
   graphify extraction fragment without a rename pass.

Concurrency: the legacy ledger is a monolithic JSON read-modify-write with no
lock (profit_mutate.py:47-56), so two overlapping runs can lose entries.  Here
writes go through SQLite transactions and a named lease.
"""
from __future__ import annotations

import hashlib
import re
import sqlite3
from pathlib import Path
from typing import Any

from . import config

SCHEMA_VERSION = 5

# Entity types.  Kept closed so a typo cannot silently create a parallel
# namespace that never joins to anything.
ENTITY_TYPES = frozenset({
    "account", "campaign", "ad_group", "criterion", "ad", "asset", "budget",
    "shared_set", "landing_page", "geo_target", "conversion_action", "service", "search_term",
    "script", "doc", "decision", "artifact", "run",
})

# Edge relations.  `corroborates` links our own ledger entry to Google's
# independent change_events record; `competes_with` is the self-competition the
# 2026-09-17 session found by hand (`kaş alımı` live in two campaigns at once).
EDGE_RELATIONS = frozenset({
    "contains", "lands_on", "touched_by", "justified_by", "applied_by",
    "supersedes", "reevaluates", "attributed_to", "governed_by",
    "corroborates", "refutes", "competes_with", "blocked_by",
})

_ID_SAFE = re.compile(r"[^a-z0-9]+")


def make_id(kind: str, *parts: Any) -> str:
    """Build a stable `^[a-z0-9_]+$` id.

    Deterministic from the inputs alone -- never a sequence number, never a
    chunk suffix -- so the same object reached from two different sources folds
    into one node instead of a ghost duplicate.
    """
    raw = "_".join([kind, *[str(p) for p in parts if p not in (None, "")]])
    out = _ID_SAFE.sub("_", raw.lower()).strip("_")
    if not out:
        raise ValueError(f"empty id from {kind!r} {parts!r}")
    # Long free text (a keyword, a URL) is hashed so ids stay bounded while
    # remaining deterministic.
    if len(out) > 120:
        digest = hashlib.sha256(out.encode("utf-8")).hexdigest()[:16]
        out = f"{out[:96].rstrip('_')}_{digest}"
    return out


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


DDL = """
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- One row per ingest.  `expected`/`read`/`stored`/`rejected` make a silent
-- coverage regression impossible to miss: five approval artifacts are mode
-- -r-------- and a builder running as google-ads-ai-report skips them.
CREATE TABLE IF NOT EXISTS ingest_run (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at  TEXT NOT NULL,
    finished_at TEXT,
    mode        TEXT NOT NULL,
    status      TEXT,
    expected    INTEGER DEFAULT 0,
    read        INTEGER DEFAULT 0,
    stored      INTEGER DEFAULT 0,
    rejected    INTEGER DEFAULT 0,
    skipped     TEXT,
    notes       TEXT
);

-- Content-addressed source artifacts.  Re-ingesting an unchanged file is a
-- no-op, which is what makes `ingest --rebuild` idempotent.
CREATE TABLE IF NOT EXISTS source (
    sha256    TEXT PRIMARY KEY,
    path      TEXT NOT NULL,
    kind      TEXT NOT NULL,
    bytes     INTEGER,
    mtime     TEXT,
    first_run INTEGER REFERENCES ingest_run(id),
    last_run  INTEGER REFERENCES ingest_run(id)
);
CREATE INDEX IF NOT EXISTS source_path_idx ON source(path);

CREATE TABLE IF NOT EXISTS entity (
    id         TEXT PRIMARY KEY,
    type       TEXT NOT NULL,
    ext_id     TEXT,
    name       TEXT,
    first_seen TEXT,
    last_seen  TEXT
);
CREATE INDEX IF NOT EXISTS entity_type_idx   ON entity(type);
CREATE INDEX IF NOT EXISTS entity_ext_id_idx ON entity(type, ext_id);

-- Attribute history, not current state: a status flip is a new row, so
-- "when did this keyword become PAUSED" is answerable.
CREATE TABLE IF NOT EXISTS entity_attr (
    entity_id  TEXT NOT NULL REFERENCES entity(id),
    key        TEXT NOT NULL,
    value      TEXT,
    as_of      TEXT NOT NULL,
    source_sha TEXT REFERENCES source(sha256),
    run_id     INTEGER REFERENCES ingest_run(id),
    PRIMARY KEY (entity_id, key, as_of, source_sha)
) WITHOUT ROWID;
CREATE INDEX IF NOT EXISTS entity_attr_key_idx ON entity_attr(key, as_of);

CREATE TABLE IF NOT EXISTS edge (
    src        TEXT NOT NULL,
    dst        TEXT NOT NULL,
    rel        TEXT NOT NULL,
    as_of      TEXT NOT NULL,
    attrs      TEXT,
    source_sha TEXT REFERENCES source(sha256),
    run_id     INTEGER REFERENCES ingest_run(id),
    PRIMARY KEY (src, dst, rel, as_of)
) WITHOUT ROWID;
CREATE INDEX IF NOT EXISTS edge_dst_idx ON edge(dst, rel);
CREATE INDEX IF NOT EXISTS edge_rel_idx ON edge(rel, as_of);

-- `window` is ISO-8601 duration: 'P1D' is an atom, 'P30D' a rolling aggregate.
-- Never compare across windows.
--
-- `source_sha` is part of the key, which makes this table bitemporal: one row
-- per (measured day, vintage).  Two facts force it.  First, conversions attach
-- late -- 2026-09-17's conversion count pulled today and pulled in thirty days
-- are different numbers, and with provenance outside the key INSERT OR IGNORE
-- keeps the first and silently discards every later correction.  Second,
-- `--as-of` has to answer "what was knowable on 2026-09-13", which is
-- unanswerable unless the store records when each value arrived; judging a past
-- decision against data that landed after it was made is exactly the unfairness
-- this store exists to remove.  `retrieved_at` orders the vintages.
-- Re-ingesting an unchanged source yields the same sha and stores nothing, so
-- idempotency survives.
CREATE TABLE IF NOT EXISTS observation (
    entity_id    TEXT NOT NULL,
    date         TEXT NOT NULL,
    metric       TEXT NOT NULL,
    value        REAL,
    window       TEXT NOT NULL DEFAULT 'P1D',
    source_sha   TEXT NOT NULL REFERENCES source(sha256),
    retrieved_at TEXT NOT NULL DEFAULT '',
    run_id       INTEGER REFERENCES ingest_run(id),
    PRIMARY KEY (entity_id, date, metric, window, source_sha)
) WITHOUT ROWID;
CREATE INDEX IF NOT EXISTS observation_date_idx   ON observation(date, metric);
CREATE INDEX IF NOT EXISTS observation_metric_idx ON observation(metric, window, date);
CREATE INDEX IF NOT EXISTS observation_vintage_idx ON observation(entity_id, metric, date, retrieved_at);

-- The current value of a metric is its newest vintage; every query that wants
-- "what is true now" reads this, and `--as-of` re-runs the same shape with a
-- `retrieved_at <= :as_of` filter instead.
CREATE VIEW IF NOT EXISTS observation_latest AS
SELECT o.*
FROM observation o
WHERE o.retrieved_at = (
    SELECT MAX(o2.retrieved_at) FROM observation o2
    WHERE o2.entity_id = o.entity_id AND o2.date = o.date
      AND o2.metric = o.metric AND o2.window = o.window
);

-- Ledger mutations.  `id` is NOT unique (99 rows, 95 ids -- four are retries),
-- so the key is (id, applied_at).  `object` is free text in 77 shapes across 99
-- rows and must never be parsed; touched objects arrive as `touched_by` edges
-- extracted by regex over the whole serialized entry instead.
CREATE TABLE IF NOT EXISTS change (
    id              TEXT NOT NULL,
    applied_at      TEXT NOT NULL,
    package         TEXT,
    object_text     TEXT,
    old_json        TEXT,
    new_json        TEXT,
    evidence        TEXT,
    expected_upside TEXT,
    risk            TEXT,
    rollback        TEXT,
    status          TEXT,
    error           TEXT,
    readback_json   TEXT,
    source_script   TEXT,
    script_inferred INTEGER DEFAULT 0,
    decision_id     TEXT,
    source_sha      TEXT REFERENCES source(sha256),
    run_id          INTEGER REFERENCES ingest_run(id),
    PRIMARY KEY (id, applied_at)
) WITHOUT ROWID;
CREATE INDEX IF NOT EXISTS change_applied_idx ON change(applied_at);
CREATE INDEX IF NOT EXISTS change_status_idx  ON change(status);

-- Plan -> approval -> receipt chain.  Filename is NOT the plan_id (one approval
-- file dated 20260805 carries plan_id ...20260804), so always read the field.
CREATE TABLE IF NOT EXISTS artifact (
    path           TEXT PRIMARY KEY,
    kind           TEXT NOT NULL,
    schema_version TEXT,
    plan_id        TEXT,
    plan_hash      TEXT,
    approval_id    TEXT,
    change_scope   TEXT,
    status         TEXT,
    expires_at     TEXT,
    body_json      TEXT,
    source_sha     TEXT REFERENCES source(sha256),
    run_id         INTEGER REFERENCES ingest_run(id)
);
CREATE INDEX IF NOT EXISTS artifact_plan_idx ON artifact(plan_id);
CREATE INDEX IF NOT EXISTS artifact_kind_idx ON artifact(kind);

CREATE TABLE IF NOT EXISTS decision (
    id          TEXT PRIMARY KEY,
    decided_on  TEXT,
    status      TEXT,
    title       TEXT,
    body        TEXT,
    fields_json TEXT,
    source_sha  TEXT REFERENCES source(sha256),
    run_id      INTEGER REFERENCES ingest_run(id)
);

-- Reasoning is data.  On 2026-09-18 a CPC-inflation hypothesis was refuted by
-- the session's own tool; unrecorded, the next session re-derives the same
-- wrong turn.
CREATE TABLE IF NOT EXISTS hypothesis (
    id           TEXT PRIMARY KEY,
    created_at   TEXT NOT NULL,
    statement    TEXT NOT NULL,
    evidence     TEXT,
    outcome      TEXT NOT NULL DEFAULT 'open',
    refuted_by   TEXT,
    resolved_at  TEXT,
    notes        TEXT
);
CREATE INDEX IF NOT EXISTS hypothesis_outcome_idx ON hypothesis(outcome);

-- Rulles.txt LOOP made executable: baseline, preset success/stop/rollback, a
-- maturity date, and only then a verdict.
CREATE TABLE IF NOT EXISTS experiment (
    id             TEXT PRIMARY KEY,
    created_at     TEXT NOT NULL,
    change_ids     TEXT,
    entity_ids     TEXT,
    metric         TEXT NOT NULL,
    baseline_start TEXT,
    baseline_end   TEXT,
    baseline_value REAL,
    mde            REAL,
    success_rule   TEXT,
    stop_rule      TEXT,
    rollback       TEXT,
    mature_at      TEXT,
    status         TEXT NOT NULL DEFAULT 'running',
    verdict        TEXT,
    verdict_at     TEXT,
    verdict_note   TEXT
);

-- One versioned home for numbers that today live in four unsynchronised places
-- (monitor_volume.py hardcodes BREAKEVEN_CPC=47.0/CEILING=38.0, raise_ceilings.py
-- derives lifetime_cash*0.0285, service values sit in ads-tracking.js, the
-- decision band in HANDOFF.md §3).  Append-only so a past decision can be
-- re-judged against the assumptions of its own time.
CREATE TABLE IF NOT EXISTS economics (
    key            TEXT NOT NULL,
    effective_from TEXT NOT NULL,
    value          REAL,
    unit           TEXT,
    source         TEXT,
    derivation     TEXT,
    run_id         INTEGER REFERENCES ingest_run(id),
    PRIMARY KEY (key, effective_from)
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS doc (
    path          TEXT PRIMARY KEY,
    kind          TEXT,
    title         TEXT,
    as_of         TEXT,
    bytes         INTEGER,
    superseded_by TEXT,
    body          TEXT,
    source_sha    TEXT REFERENCES source(sha256),
    run_id        INTEGER REFERENCES ingest_run(id)
);

-- The 25+ API traps that cost real money and currently live in a SUPERSEDED
-- handoff (HANDOFF-20260914.md §5), which a session following AGENTS.md never
-- opens.
CREATE TABLE IF NOT EXISTS trap (
    id          TEXT PRIMARY KEY,
    domain      TEXT NOT NULL,
    statement   TEXT NOT NULL,
    detail      TEXT,
    fix         TEXT,
    cost_note   TEXT,
    source_doc  TEXT,
    source_line TEXT
);
CREATE INDEX IF NOT EXISTS trap_domain_idx ON trap(domain);

-- The write boundary as data instead of prose spread over four documents.
CREATE TABLE IF NOT EXISTS guard_rule (
    id          TEXT PRIMARY KEY,
    object_type TEXT,
    ext_id      TEXT,
    operation   TEXT,
    verdict     TEXT NOT NULL,
    requirement TEXT,
    detail      TEXT,
    source      TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS guard_object_idx ON guard_rule(object_type, operation);

CREATE TABLE IF NOT EXISTS policy (
    id          TEXT PRIMARY KEY,
    clause      TEXT NOT NULL,
    predicate   TEXT NOT NULL,
    description TEXT,
    source      TEXT
);

-- Every number the system emits records the rows it came from, so `verify`
-- can re-derive it and an agent cannot assert what the store does not support.
CREATE TABLE IF NOT EXISTS claim (
    id          TEXT PRIMARY KEY,
    created_at  TEXT NOT NULL,
    verb        TEXT,
    statement   TEXT,
    value_json  TEXT,
    evidence    TEXT,
    -- How to recompute this claim: {module, func, kwargs}.  Without it `verify`
    -- can only confirm the cited rows exist, not that they still add up.
    recipe_json TEXT,
    run_id      INTEGER REFERENCES ingest_run(id)
);

CREATE TABLE IF NOT EXISTS lease (
    name        TEXT PRIMARY KEY,
    holder      TEXT,
    acquired_at TEXT,
    expires_at  TEXT
);

-- The metric dictionary (data/ctx/metrics.json, D-2026-09-30-01): what every
-- metric name means, its unit, the day it is keyed on (Istanbul / UTC /
-- America/Los_Angeles), who writes it and what must not be done with it.
-- `name` is exact or an fnmatch pattern ('site_btn_*'); exact wins.
CREATE TABLE IF NOT EXISTS metric (
    name        TEXT PRIMARY KEY,
    is_pattern  INTEGER NOT NULL DEFAULT 0,
    family      TEXT,
    entity_type TEXT,
    unit        TEXT,
    window      TEXT,
    day_basis   TEXT,
    source      TEXT,
    writer      TEXT,
    definition  TEXT,
    additive    INTEGER,
    censored    INTEGER,
    since       TEXT,
    status      TEXT,
    caveats     TEXT
);

-- Known data-quality periods (data/ctx/exclusions.json): a QA sweep, a dead tag
-- host, a source that has not started yet.  effect: exclude (drop the days from
-- sums) | undercount (keep, label low confidence) | no_data (missing != zero).
CREATE TABLE IF NOT EXISTS exclusion (
    id          TEXT PRIMARY KEY,
    source      TEXT NOT NULL,
    metric_like TEXT,
    entity_like TEXT,
    start_date  TEXT NOT NULL,
    end_date    TEXT,
    effect      TEXT NOT NULL,
    reason      TEXT,
    evidence    TEXT
);

-- One row per site page per day with the newest vintage of every source, rebuilt
-- by `sync --page-proof` (ctx_pages.build_page_day).  Derived: ads.db can always
-- rebuild it.  Day basis per column is in the metric dictionary (gsc_* are
-- Pacific days).
CREATE TABLE IF NOT EXISTS page_day (
    page            TEXT NOT NULL,
    date            TEXT NOT NULL,
    entity_id       TEXT NOT NULL,
    ads_cost        REAL, ads_clicks REAL, ads_impr REAL, ads_conv REAL,
    site_views_ad   REAL, site_entries_ad REAL, site_taps_ad REAL, site_taps_org REAL,
    site_eng_views  REAL, site_eng_sec REAL, site_quick_exits REAL,
    gsc_clicks      REAL, gsc_impr REAL, gsc_pos REAL,
    ga4_views       REAL, ga4_sessions REAL, ga4_entry_sessions REAL,
    ga4_entry_engaged REAL, ga4_engagement_sec REAL,
    psi             REAL, lab_lcp_ms REAL,
    score           REAL,
    provisional     INTEGER NOT NULL DEFAULT 0,
    flags           TEXT,
    built_at        TEXT,
    PRIMARY KEY (page, date)
) WITHOUT ROWID;

-- NEG-KARAR (2026-09-30).  Search terms at the finest grain Google serves them
-- (day x ad group x keyword criterion x device), and the same cell's keyword
-- totals, so a site ad session -- which carries the ad group, the criterion
-- (`t=kwd-`) and the device but never the search term -- can be joined to the
-- terms that could have produced it.  Derived: rebuilt from the pulls archived
-- under data/ctx/term_cells/ (ctx_terms.replay); the newest pull of a day wins.
CREATE TABLE IF NOT EXISTS term_cell_day (
    date         TEXT NOT NULL,
    ad_group_id  TEXT NOT NULL,
    criterion_id TEXT NOT NULL,
    device       TEXT NOT NULL,
    term         TEXT NOT NULL,
    match_type   TEXT NOT NULL,
    campaign_id  TEXT,
    impressions  REAL, clicks REAL, cost REAL, conversions REAL,
    source_sha   TEXT, retrieved_at TEXT,
    PRIMARY KEY (date, ad_group_id, criterion_id, device, term, match_type)
) WITHOUT ROWID;
CREATE INDEX IF NOT EXISTS term_cell_term_idx ON term_cell_day(term, date);

CREATE TABLE IF NOT EXISTS kw_cell_day (
    date         TEXT NOT NULL,
    ad_group_id  TEXT NOT NULL,
    criterion_id TEXT NOT NULL,
    device       TEXT NOT NULL,
    campaign_id  TEXT,
    impressions  REAL, clicks REAL, cost REAL,
    source_sha   TEXT, retrieved_at TEXT,
    PRIMARY KEY (date, ad_group_id, criterion_id, device)
) WITHOUT ROWID;

-- One row per ad session on the site (sgb_contact.log / the CRM's archive),
-- with what it did and the search terms its cell allows.  No identity of any
-- kind: the ping carries none, and nothing here may add one (tests grep it).
CREATE TABLE IF NOT EXISTS ad_session (
    session_id   TEXT PRIMARY KEY,
    date         TEXT NOT NULL,
    start_at     TEXT NOT NULL,
    end_at       TEXT,
    campaign_id  TEXT, ad_group_id TEXT, criterion_id TEXT,
    keyword      TEXT, match TEXT, device TEXT,
    pages        INTEGER, landing TEXT, page_list TEXT,
    tap          TEXT, tap_at TEXT, taps INTEGER, button TEXT,
    span_sec     REAL,
    flags        TEXT,
    term         TEXT,
    term_certain INTEGER,
    candidates   TEXT,
    cell_clicks  REAL, hidden_clicks REAL,
    built_at     TEXT
) WITHOUT ROWID;
CREATE INDEX IF NOT EXISTS ad_session_date_idx ON ad_session(date);

CREATE VIRTUAL TABLE IF NOT EXISTS search_fts USING fts5(
    ref UNINDEXED, kind UNINDEXED, title, body, tokenize='unicode61'
);
"""


def connect(path: Path | None = None, *, readonly: bool = False) -> sqlite3.Connection:
    """Open the store, creating it if needed."""
    target = Path(path or config.CTX_DB)
    target.parent.mkdir(parents=True, exist_ok=True)
    if readonly and target.exists():
        conn = sqlite3.connect(f"file:{target}?mode=ro", uri=True)
    else:
        # Wait for a writer instead of failing after sqlite's default 5 s: the reconcile ingest runs every
        # few minutes for 1-2 minutes, and every verb that records a claim used to die with "database is
        # locked" if it landed inside one (2026-10-01: `ask negatives`, twice, and the nightly export).
        conn = sqlite3.connect(target, timeout=120)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# Columns added after the first release.  `CREATE TABLE IF NOT EXISTS` cannot
# add a column to a table that already exists, so an existing store would keep
# running on the old shape and every write of the new field would fail — which
# is exactly the kind of silent divergence this store exists to prevent.
_ADDED_COLUMNS: tuple[tuple[str, str, str], ...] = (
    # Lets `verify` re-run the computation that produced a claim instead of
    # only checking that the rows it cited still exist.
    ("claim", "recipe_json", "TEXT"),
    # Marks a day whose metrics have not finished settling (impression share is
    # computed only for elapsed hours).  Consumers exclude these by default.
    ("observation", "provisional", "INTEGER NOT NULL DEFAULT 0"),
    # The preregistered status changes of a Meta experiment.  meta_roas.decide()
    # adds them to the sealed plan, so the panel's approve button is the only
    # way they reach the account.
    ("experiment", "actions_json", "TEXT"),
    # The panel shows data-quality periods to the owner in Turkish (D-2026-09-30-01).
    ("exclusion", "reason_tr", "TEXT"),
)


def _add_missing_columns(conn: sqlite3.Connection) -> list[str]:
    added = []
    for table, column, decl in _ADDED_COLUMNS:
        cols = {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}
        if column not in cols:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {decl}")
            added.append(f"{table}.{column}")
    if added:
        conn.commit()
    return added


def migrate(conn: sqlite3.Connection) -> int:
    """Create or upgrade the schema; returns the resulting version."""
    conn.executescript(DDL)
    _add_missing_columns(conn)
    row = conn.execute(
        "SELECT value FROM schema_meta WHERE key = 'schema_version'"
    ).fetchone()
    current = int(row["value"]) if row else 0
    if current != SCHEMA_VERSION:
        conn.execute(
            "INSERT INTO schema_meta(key, value) VALUES('schema_version', ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (str(SCHEMA_VERSION),),
        )
        conn.commit()
    return SCHEMA_VERSION


class LeaseHeld(RuntimeError):
    """Another writer holds the lease.  Raised rather than waited on."""


def acquire_lease(
    conn: sqlite3.Connection, name: str = "ctx_write", *, ttl_seconds: int = 1800,
    holder: str = "",
) -> str:
    """Take the single-writer lease, or fail immediately saying who holds it.

    The schema has declared this lease since day one and nothing ever took it.
    SQLite's own locking stops two writers corrupting a page, but it does not
    stop the nightly timer and a human session interleaving whole ingests --
    each reading the store, deciding what is missing, and writing on top of the
    other's conclusions.  Failing fast is deliberate: a queued second ingest
    would just repeat work against data that changed underneath it.
    """
    import os
    import socket
    from datetime import datetime, timedelta, timezone as _tz

    holder = holder or f"pid:{os.getpid()}@{socket.gethostname()}"
    now = datetime.now(_tz.utc)
    expires = (now + timedelta(seconds=ttl_seconds)).isoformat(timespec="seconds")

    row = conn.execute("SELECT holder, acquired_at, expires_at FROM lease WHERE name = ?",
                       (name,)).fetchone()
    if row and row["holder"] != holder:
        try:
            still_valid = datetime.fromisoformat(row["expires_at"]) > now
        except (TypeError, ValueError):
            still_valid = False  # an unparseable expiry is a stale lease, not a live one
        if still_valid:
            raise LeaseHeld(
                f"lease {name!r} held by {row['holder']} since {row['acquired_at']} "
                f"(expires {row['expires_at']})"
            )
    conn.execute(
        "INSERT INTO lease(name, holder, acquired_at, expires_at) VALUES(?,?,?,?) "
        "ON CONFLICT(name) DO UPDATE SET holder=excluded.holder, "
        "acquired_at=excluded.acquired_at, expires_at=excluded.expires_at",
        (name, holder, now.isoformat(timespec="seconds"), expires),
    )
    conn.commit()
    return holder


def release_lease(conn: sqlite3.Connection, name: str, holder: str) -> None:
    conn.execute("DELETE FROM lease WHERE name = ? AND holder = ?", (name, holder))
    conn.commit()


def open_store(path: Path | None = None) -> sqlite3.Connection:
    conn = connect(path)
    migrate(conn)
    return conn
