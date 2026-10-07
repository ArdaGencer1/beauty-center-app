---
name: tagctx
description: "Use for every measurement or deploy question on seldagencerbeauty.com: gtag, GTM, Consent Mode, Google Ads labels, Meta CAPI, attribution, contact-ping, offline conversions, missing/double-firing tags, and the post-deploy measurement gate."
---

# TagCtx

Read `TAGCTX_RUNBOOK.md` before acting. This skill is read-only: it inspects the
served site, Google Ads inventory, GTM containers and endpoints; it does not
change the site or an advertising account.

Start on the website server:

```bash
cd /var/www/seldagencerbeauty.com/google-adsAI
test -d /var/www/seldagencerbeauty.com/public_html
./run tag_ctx.py audit
```

Required after anything touches HTML/JS, CTA, forms, Consent Mode, GTM or
tracking:

```bash
./run tag_ctx.py audit --record
./run tag_ctx.py diff
./run tag_ctx.py verify --pages index.html,CHANGED_PAGE.html
patches/verify_tags.sh index.html,CHANGED_PAGE.html
```

Rules:

1. Do not grep `ads-tracking.js`; read bytes with replacement decoding.
2. Resolve the `public_html` release symlink.
3. Compare decompressed `.gz` twins; nginx may serve them instead of plain files.
4. Do not infer tag health from the Ads account alone. Cross-check page code,
   web GTM, server GTM and runtime behavior.
5. Runtime probes must abort Google measurement requests. Never use
   `--live-hits` for a check.
6. Do not use `--probe-writes` casually; some endpoints create measurement data.
7. Account/tag/container mutations require separate explicit owner approval.
8. Do not claim completion until TagCtx diff has no newly opened critical and
   runtime verify passes.

Useful verbs:

```bash
./run tag_ctx.py inventory
./run tag_ctx.py surface
./run tag_ctx.py coverage
./run tag_ctx.py gtm
./run tag_ctx.py endpoints
./run tag_ctx.py verify
./run tag_ctx.py sweep
./run tag_ctx.py history
```

Use `--json` for machine output and `--offline` when the cached Ads inventory is
the only available account source. The static site half is trustworthy only on
the website server where `public_html` and `releases/` exist.
