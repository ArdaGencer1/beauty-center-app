# TagCtx traps

- `ads-tracking.js` contains raw control bytes. Normal grep can report a false
  absence; `tag_surface.py` deliberately reads bytes with replacement decoding.
- `gtag(js, ...)` uses a bare identifier and throws before configuration.
  Presence of a loader does not prove configuration.
- Consent default must execute before the tag loader.
- `public_html` is a release symlink; resolve it before provenance/mtime checks.
- With `gzip_static`, stale `.gz` twins keep serving old tracking code.
- `MessageToDict` returns the conversion action field as `type_`, not `type`.
- TagCtx's 30-day conversion count is a sum of daily atoms. Do not substitute or
  difference a rolling P30D aggregate.
