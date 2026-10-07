# Repository instructions for AI coding agents

Read `/AI_HANDOFF.md` first and use `/AI_CONTEXT.json` for machine-readable
paths, plan status, hard rules, and completion gates.

Do not bulk-open or re-analyze media. Query metadata first with:

```bash
python3 scripts/ai_media_lookup.py summary
python3 scripts/ai_media_lookup.py search QUERY --family FAMILY --limit 6
python3 scripts/ai_media_lookup.py show SLUG_OR_INSTAGRAM_ID
```

Continue the existing Artifact at
`https://claude.ai/artifact/WmsLiPPTLdnrjSrdYSXcLM`; never create a replacement.
Use `instagram.db` as the Instagram source of truth and never use `media.json`.
Do not claim a plan is complete unless every gate in `AI_CONTEXT.json` passes.
