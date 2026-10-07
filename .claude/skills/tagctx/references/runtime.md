# Runtime probing

```bash
cd /var/www/seldagencerbeauty.com/google-adsAI/tagtools
export PLAYWRIGHT_BROWSERS_PATH="$PWD/browsers"
node tag_probe.mjs --url https://seldagencerbeauty.com/ --consent granted --scenario whatsapp
```

The probe records matching Google measurement requests and aborts them, so a
test does not become a real conversion. Do not pass `--live-hits` during normal
verification.

Scenarios are `load`, `whatsapp` and `phone`; consent states are `granted`,
`denied` and `unset`. `hit_counts` reports the destinations seen. Check
`same_endpoint_repeats` before calling two transports a double conversion, and
check browser/page errors before interpreting a missing hit.
