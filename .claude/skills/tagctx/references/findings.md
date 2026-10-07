# Current finding policy

Do not trust a copied historical finding list as current state. Run:

```bash
./run tag_ctx.py audit --json
./run tag_ctx.py verify --json
```

The packaged regression baseline is `tagctx-baseline.json`. At the 2026-10-07
baseline, runtime was 5/5 clean while the static/account audit had two known
criticals. `audit --record` followed by `diff` distinguishes a new deploy
regression from that existing backlog.
