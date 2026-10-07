"""Tag health as `doctor.py` checks.

Folding into doctor rather than standing up a sixth timer buys the existing
schedule (03:15 and 18:15 UTC), the `data/health/latest.json` publish, the
PASS/WARN/FAIL rollup and the exit code, all of it already wired.

Contract matches `adsai.ctx_doctor.ctx_checks`: a list of
``(name, status, detail)`` with status in ``PASS | WARN | FAIL`` and no
dependency on doctor's own types.

**Sandbox note.** The report unit runs as `google-ads-ai-report` under
``ProtectSystem=strict`` and ``ProtectHome=true``. A check that reads the
served site or nginx succeeds when a person runs it as root and raises
``PermissionError`` in production. Every check here therefore degrades to WARN
on a permission error instead of reporting the site as broken -- an unreadable
file is an unknown, not a failure.
"""
from __future__ import annotations

PASS, WARN, FAIL = "PASS", "WARN", "FAIL"


def _unreadable(name: str, exc: Exception) -> tuple[str, str, str]:
    return (name, WARN, f"okunamadi ({type(exc).__name__}); sandbox kisiti olabilir")


def tag_checks(deep: bool = False) -> list[tuple[str, str, str]]:
    """Static checks always; endpoint and account checks only with ``deep``."""
    checks: list[tuple[str, str, str]] = []

    try:
        from adsai import tag_surface

        survey = tag_surface.survey()
        pages = survey["pages"]

        # GTM loads the Google tag on pages that carry no gtag.js of their own,
        # so only a page with neither is unmeasured.
        untagged = [
            p.name for p in pages
            if p.gtag_loader_line is None
            and not p.gtm_ids
            and p.gtm_loader_line is None
        ]
        checks.append((
            "tag_page_coverage",
            FAIL if untagged else PASS,
            f"{len(pages)} sayfa; tag'siz={untagged or 'yok'}",
        ))

        broken = [p.name for p in pages if p.unquoted_gtag]
        checks.append((
            "tag_gtag_syntax",
            FAIL if broken else PASS,
            f"tirnaksiz gtag cagrisi olan sayfalar={broken or 'yok'}",
        ))

        # Consent ordering is not checked here: doctor's own site_consent_order
        # already covers it, and two names for one defect is noise.

        stale = [g.name for g in survey["gz_twins"] if not g.matches]
        checks.append((
            "tag_gz_twins",
            FAIL if stale else PASS,
            f"{len(survey['gz_twins'])} ikiz; bayat={stale or 'yok'}",
        ))
    except PermissionError as exc:
        checks.append(_unreadable("tag_site_surface", exc))
    except Exception as exc:  # noqa: BLE001
        checks.append(("tag_site_surface", WARN, f"{type(exc).__name__}: {exc}"))

    if not deep:
        return checks

    try:
        from adsai import tag_endpoints

        report = tag_endpoints.survey()
        broken_eps = [
            f"{p.target.url} ({p.verdict})"
            for p in report["probes"]
            if p.verdict in ("unreachable", "missing", "error")
        ]
        checks.append((
            "tag_endpoints",
            FAIL if broken_eps else PASS,
            f"{report['probed']} uc; bozuk={broken_eps or 'yok'}",
        ))
    except Exception as exc:  # noqa: BLE001
        checks.append(("tag_endpoints", WARN, f"{type(exc).__name__}: {exc}"))

    try:
        from adsai import tag_audit

        report = tag_audit.audit()
        counts = report["counts"]
        critical = [f.title for f in report["findings"] if f.severity == "critical"]
        checks.append((
            "tag_account_cross",
            FAIL if counts["critical"] else (WARN if counts["warn"] else PASS),
            f"kritik={counts['critical']} uyari={counts['warn']}; "
            f"{'; '.join(critical[:3]) if critical else 'temiz'}",
        ))
    except Exception as exc:  # noqa: BLE001
        checks.append(("tag_account_cross", WARN, f"{type(exc).__name__}: {exc}"))

    return checks
