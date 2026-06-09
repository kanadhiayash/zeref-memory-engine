# memory/

Local memory layer. Populated per-user-project — never bundled in this repo.

Bootstrap a fresh memory tree with:

```bash
python3 -m zeref init
```

After init, this directory holds:

- `hot.md` — last few sessions, current context (≤500 words, read first)
- `index.md` — domain index across pages
- `pages/` — durable per-domain notes
- `patterns/PATTERNS.jsonl` — append-only event log
- `wiki/` — DECISIONS, RISKS, OPEN_QUESTIONS, CONFLICTS
- `raw/`, `snapshots/`, `sync/` — local-only working state

All entries are governed by `PRIVACY.md` + `REDACT.md` at the repo root. Default privacy mode is `abstract` — `privacy-abstraction` rewrites sensitive content before any write.
