#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TagCtx -- what the site measures, checked against what the account expects.

Read-only.  SELECT-only GAQL against Google Ads and plain reads of the served
site; nothing here mutates either side.

    ./run tag_ctx.py audit                # the cross-reference, findings first
    ./run tag_ctx.py audit --json
    ./run tag_ctx.py inventory            # conversion actions and their labels
    ./run tag_ctx.py surface              # what each page loads, byte-safely
    ./run tag_ctx.py coverage             # page x expected-asset matrix
    ./run tag_ctx.py gtm                  # the GTM containers, tag by tag

Use ``--offline`` to work from the cached inventory instead of the API.
"""
from __future__ import annotations

import argparse
import json
import sys

from adsai import tag_account, tag_audit, tag_surface

_SEV_MARK = {"critical": "!!", "warn": " !", "info": "  "}


def _print_audit(report: dict) -> None:
    c = report["counts"]
    print(
        f"as_of {report['as_of']} | {report['pages_scanned']} sayfa, "
        f"{report['actions_scanned']} conversion action"
    )
    print(f"bulgular: {c['critical']} kritik, {c['warn']} uyarı, {c['info']} bilgi\n")
    for finding in report["findings"]:
        print(f"{_SEV_MARK[finding.severity]} [{finding.severity}] {finding.title}")
        for line in finding.evidence:
            print(f"      · {line}")
        if finding.cost:
            print(f"      maliyet: {finding.cost}")
        if finding.fix:
            print(f"      düzeltme: {finding.fix}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(prog="tag_ctx.py", description=__doc__)
    parser.add_argument(
        "verb",
        choices=("audit", "inventory", "surface", "coverage", "gtm",
                 "endpoints", "verify", "sweep", "diff", "history"),
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--record", action="store_true",
        help="audit: sonucu AdsCtx store'una yaz",
    )
    parser.add_argument("--since", default="", help="diff: bu tarihten onceki kosuyla karsilastir")
    parser.add_argument(
        "--pages", default="", help="verify: virgulle ayrilmis sayfa listesi"
    )
    parser.add_argument(
        "--consent", default="granted", choices=("granted", "denied", "unset")
    )
    parser.add_argument(
        "--probe-writes", action="store_true",
        help="endpoints: kayit tutan uclari da yokla (veri yazar)",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="use the cached conversion-action inventory instead of the API",
    )
    args = parser.parse_args()

    if args.verb in ("diff", "history"):
        from adsai import tag_store

        if args.verb == "history":
            for run in tag_store.runs():
                c = run.get("counts", {})
                print(f"  {run.get('as_of','?')}  kritik={c.get('critical',0)} "
                      f"uyari={c.get('warn',0)} bilgi={c.get('info',0)}")
            return
        delta = tag_store.diff(args.since or None)
        if delta is None:
            print("karsilastirilacak ikinci kosu yok "
                  "(once: ./run tag_ctx.py audit --record)")
            sys.exit(0)
        if args.as_json:
            print(json.dumps(delta.to_dict(), ensure_ascii=False, indent=1))
        else:
            print(f"{delta.older}  ->  {delta.newer}")
            print(f"  degismeyen: {delta.unchanged}")
            print(f"  YENI ACILAN: {len(delta.opened)}")
            for f in delta.opened:
                print(f"    !! [{f['severity']}] {f['title']}")
                for e in f.get("evidence", [])[:2]:
                    print(f"         {e}")
            print(f"  kapanan: {len(delta.closed)}")
            for fid in delta.closed:
                print(f"    ok {fid}")
        sys.exit(1 if any(f["severity"] == "critical" for f in delta.opened) else 0)

    if args.verb == "audit":
        report = tag_audit.audit(offline=args.offline)
        if args.record:
            from adsai import tag_store

            print(f"kaydedildi: {tag_store.record(report)}\n")
        if args.as_json:
            report = {**report, "findings": [f.to_dict() for f in report["findings"]]}
            print(json.dumps(report, ensure_ascii=False, indent=1))
        else:
            _print_audit(report)
        sys.exit(1 if report["counts"]["critical"] else 0)

    if args.verb == "inventory":
        actions, as_of = tag_account.load(offline=args.offline)
        if args.as_json:
            print(json.dumps(
                {"as_of": as_of, "actions": [a.to_dict() for a in actions]},
                ensure_ascii=False, indent=1,
            ))
            return
        print(f"as_of {as_of} | {len(actions)} conversion action\n")
        for a in actions:
            print(
                f"{a.status:8} {a.type:28} prim={str(a.primary_for_goal):5} "
                f"{a.conversions_30d:8.1f}  {a.name[:40]:40} {a.labels or ''}"
            )
        return

    if args.verb == "endpoints":
        from adsai import tag_endpoints

        report = tag_endpoints.survey(probe_writes=args.probe_writes)
        if args.as_json:
            print(json.dumps(
                {**report, "probes": [p.to_dict() for p in report["probes"]]},
                ensure_ascii=False, indent=1,
            ))
        else:
            print(f"{report['probed']} uc yoklandi, {report['broken']} bozuk\n")
            for probe in report["probes"]:
                mark = "!!" if probe.verdict in ("unreachable", "missing", "error") else "  "
                print(f"{mark} [{probe.verdict}] {probe.target.url}")
                print(f"      {probe.detail}")
                print(f"      kaynak: {probe.target.source}")
        sys.exit(1 if report["broken"] else 0)

    if args.verb in ("verify", "sweep"):
        from adsai import tag_runtime

        if args.verb == "sweep":
            pages = [p.name for p in tag_surface.pages()]
        elif args.pages:
            pages = [p.strip() for p in args.pages.split(",") if p.strip()]
        else:
            pages = None
        report = tag_runtime.verify(pages, consent=args.consent)
        if args.as_json:
            print(json.dumps(
                {**report, "results": [r.to_dict() for r in report["results"]]},
                ensure_ascii=False, indent=1,
            ))
        else:
            print(f"{report['checked']} sayfa, {report['failed']} basarisiz "
                  f"(consent={report['consent']})\n")
            for res in report["results"]:
                print(f"{'  ok' if res.ok else '!! HATA'}  {res.page:38} {res.detail}")
        sys.exit(1 if report["failed"] else 0)

    if args.verb == "gtm":
        from adsai import tag_gtm

        try:
            report = tag_gtm.inventory()
        except tag_gtm.GtmUnavailable as exc:
            print(f"GTM okunamadi:\n{exc}")
            sys.exit(2)
        if args.as_json:
            print(json.dumps(report, ensure_ascii=False, indent=1))
            return
        for c in report["containers"]:
            print(f"\n{c['public_id']}  {c['name']}  {c['usage_context']}")
            print(f"  {c['tag_count']} tag, {c['trigger_count']} trigger, {c['variable_count']} degisken")
            for tag in c["tags"]:
                flag = " (DURDURULMUS)" if tag["paused"] else ""
                print(f"    - {tag['name'][:44]:44} {tag['type']:22}{flag}")
                if tag["ids"]:
                    print(f"        hedefler: {tag['ids']}")
                if tag["conversion_labels"]:
                    print(f"        etiketler: {tag['conversion_labels']}")
                if tag["firing_on"]:
                    print(f"        tetik: {tag['firing_on']}")
        return

    survey = tag_surface.survey()
    if args.verb == "surface":
        payload = {
            "site_dir": survey["site_dir"],
            "pages": [p.to_dict() for p in survey["pages"]],
            "label_sites": [s.to_dict() for s in survey["label_sites"]],
            "gz_twins": [g.to_dict() for g in survey["gz_twins"]],
        }
        if args.as_json:
            print(json.dumps(payload, ensure_ascii=False, indent=1))
            return
        print(f"{survey['site_dir']}\n")
        print("etiket gönderim noktaları:")
        for site in survey["label_sites"]:
            print(f"  {site.label}  {site.file}:{site.line} -> satır {site.used_lines}")
        stale = [g for g in survey["gz_twins"] if not g.matches]
        print(f"\n.gz ikizleri: {len(survey['gz_twins'])} tane, {len(stale)} bayat")
        for g in stale:
            print(f"  {g.name}: {g.reason}")
        return

    # coverage
    rows = [p for p in survey["pages"] if p.missing_assets or p.gtag_loader_line is None]
    if args.as_json:
        print(json.dumps([p.to_dict() for p in rows], ensure_ascii=False, indent=1))
        return
    print(f"{survey['page_count']} sayfa tarandı, {len(rows)} tanesi eksik\n")
    for p in rows:
        loader = "yok" if p.gtag_loader_line is None else f"satır {p.gtag_loader_line}"
        print(f"  {p.name:42} gtag.js={loader:10} eksik={p.missing_assets}")


if __name__ == "__main__":
    main()
