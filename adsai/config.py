"""Central configuration, paths, and tunable thresholds for the adsai system.

Everything that a future run might want to tweak lives here so the rest of the
code stays declarative. Thresholds encode the goals from Rulles.txt.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

# --- Paths -----------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent  # .../google-adsAI
DATA_DIR = ROOT_DIR / "data"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
CONTEXT_DIR = DATA_DIR / "context"
HEALTH_DIR = DATA_DIR / "health"
LOGS_DIR = ROOT_DIR / "logs"
STATE_FILE = DATA_DIR / "state.json"
CONTEXT_FILE = CONTEXT_DIR / "latest.json"
HEALTH_FILE = HEALTH_DIR / "latest.json"
ACTIONS_LOG = LOGS_DIR / "actions.jsonl"
RUN_LOG = LOGS_DIR / "run.log"
JOURNAL_MD = ROOT_DIR / "JOURNAL.md"

for _d in (DATA_DIR, SNAPSHOTS_DIR, CONTEXT_DIR, HEALTH_DIR, LOGS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

load_dotenv(ROOT_DIR / ".env")

# --- Locale ----------------------------------------------------------------
TIMEZONE = ZoneInfo("Europe/Istanbul")
CURRENCY = "TRY"


def today() -> str:
    """Business 'today' in Istanbul time (YYYY-MM-DD)."""
    return datetime.now(TIMEZONE).date().isoformat()


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone(TIMEZONE).isoformat(timespec="seconds")


def days_ago(n: int) -> str:
    return (datetime.now(TIMEZONE).date() - timedelta(days=n)).isoformat()


# --- Tunable thresholds (encode Rulles.txt goals) --------------------------
# Rule: "Make the click expense minimum." Flag campaigns whose average CPC is
# above this (TRY) for review.
CPC_REVIEW_THRESHOLD = float(os.getenv("ADSAI_CPC_REVIEW_THRESHOLD", "20"))

# Rule: "Don't advertise to people who won't buy." A search term that spent at
# least this much (TRY) with zero conversions is a waste candidate -> negative
# keyword suggestion.
WASTE_TERM_MIN_COST = float(os.getenv("ADSAI_WASTE_TERM_MIN_COST", "150"))

# A search term with at least this many clicks and zero conversions is also a
# waste candidate even if cheap.
WASTE_TERM_MIN_CLICKS = int(os.getenv("ADSAI_WASTE_TERM_MIN_CLICKS", "15"))

# Operational volume diagnostic. Only completed rolling windows are compared;
# it is not itself a win unless paid/quality economics also improve.
ROLLING_WINDOW_DAYS = int(os.getenv("ADSAI_ROLLING_WINDOW_DAYS", "7"))

# Explicit non-client intent only. Price/discount words are deliberately absent:
# price searches can produce paid customers and must never be blanket-blocked.
WRONG_INTENT_SIGNAL_WORDS = [
    "kurs", "eğitim", "egitim", "sertifika", "iş ilanı", "is ilani", "eleman",
    "nasıl yapılır", "nasil yapilir", "evde yapımı", "evde yapimi",
]

# Default lookback for the dashboard.
DEFAULT_LOOKBACK_DAYS = int(os.getenv("ADSAI_LOOKBACK_DAYS", "30"))

# Financial/lifecycle reporting uses exact calendar months independently from
# the shorter campaign-diagnostics window.
LIFECYCLE_MONTHS = int(os.getenv("ADSAI_LIFECYCLE_MONTHS", "12"))
LTV_HORIZONS = (30, 60, 90, 180, 365)
ACTIVE_CUSTOMER_DAYS = int(os.getenv("ADSAI_ACTIVE_CUSTOMER_DAYS", "90"))
LAPSE_GRACE_DAYS = int(os.getenv("ADSAI_LAPSE_GRACE_DAYS", "30"))
MIN_SOURCE_COVERAGE = float(os.getenv("ADSAI_MIN_SOURCE_COVERAGE", "0.90"))
FINANCIAL_FRESHNESS_MAX_DAYS = int(
    os.getenv("ADSAI_FINANCIAL_FRESHNESS_MAX_DAYS", "7")
)
CONTEXT_MAX_BYTES = int(os.getenv("ADSAI_CONTEXT_MAX_BYTES", "8000"))
CONTEXT_MAX_MONTHS = int(os.getenv("ADSAI_CONTEXT_MAX_MONTHS", "6"))
CONTEXT_MAX_COHORTS = int(os.getenv("ADSAI_CONTEXT_MAX_COHORTS", "6"))
CONTEXT_MAX_ANOMALIES = int(os.getenv("ADSAI_CONTEXT_MAX_ANOMALIES", "5"))

GOOGLE_ADS_SOURCE_KEY = "google_ads"
