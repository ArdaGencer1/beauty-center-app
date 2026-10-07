"""adsai — Selda Gençer Beauty Google Ads growth system.

A small, extensible toolkit that:
  1. reads Google Ads performance (campaigns, search terms, daily metrics),
  2. reads real new-customer appointments from the beauty panel,
  3. ties spend to actual customers, stores a daily snapshot,
  4. checks the Rulles.txt goals (more verified attended-and-paid customers,
     higher contribution economics, lower paid CAC and waste), and
  5. writes a detailed action log + human journal so every run builds on the
     previous one.

Entry point: ../daily_report.py  (run with ./run daily_report.py)
"""

__version__ = "1.0.0"
