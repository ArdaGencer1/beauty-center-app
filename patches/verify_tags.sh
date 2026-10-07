#!/usr/bin/env bash
# Post-deploy tag gate.
#
#   ./verify_tags.sh                      # default sample
#   ./verify_tags.sh index.html,konum.html
#
# Fails on what this deploy broke, not on the standing backlog. The site
# currently carries several long-open critical findings; a gate that refused
# every deploy until they were cleared would be switched off within a week.
# So the account/site cross-check is judged by DIFF -- a newly opened critical
# is this deploy's doing -- while the runtime check is absolute, because a page
# that throws on load was working before the deploy or it would not be listed.
#
# The regression this exists to catch took five hours to notice: script.js:902
# threw on every page load and nothing was looking.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# `run` hands the script path to python unchanged, so it must be resolved from
# the project root rather than from wherever the deploy script was invoked.
cd "$ROOT"
PAGES="${1:-}"
fail=0

echo "== tag denetimi kaydediliyor =="
# `audit` exits 1 whenever any critical stands, backlog included. That is the
# right signal for a person and the wrong one for this gate, whose question is
# only "did this deploy open something new" -- so its status is discarded here
# and the judgement is left to `diff` below.
"$ROOT/run" tag_ctx.py audit --record >/dev/null || true

echo "== bu deploy ne açtı =="
if ! "$ROOT/run" tag_ctx.py diff; then
  echo "   -> bu deploy yeni bir KRİTİK bulgu açtı"
  fail=1
fi

echo
echo "== canlı sayfa doğrulaması =="
if [ -n "$PAGES" ]; then
  "$ROOT/run" tag_ctx.py verify --pages "$PAGES" || fail=1
else
  "$ROOT/run" tag_ctx.py verify || fail=1
fi

echo
if [ "$fail" -ne 0 ]; then
  echo "TAG KAPISI: BAŞARISIZ -- deploy'u geri alın ya da düzeltin"
  exit 1
fi
echo "TAG KAPISI: TEMİZ"
