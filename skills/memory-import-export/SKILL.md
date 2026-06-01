---
name: memory-import-export
description: Imports/exports memory across tools, repos, and formats. Migration, onboarding, backup. Explicit user request only.
trigger:
  - user says "import memory from ..."
  - user says "export memory to ..."
  - /migrate
model: claude-sonnet-4-6
max_turns: 20
---

# memory-import-export

## Mission

Move memory between projects, tools, formats, and backups without losing provenance.

## Operations

### IMPORT
Sources supported:
- v3 Zeref OS wiki (`wiki/hot.md`, `wiki/log.md`) → use `scripts/migrate-v3-to-v4.py`
- v4.2 Zeref OS (`memory/wiki/`, `memory/logs/session-events.jsonl`) → use `scripts/migrate-v4.2-to-v4.3.py`
- Plain markdown directory → parse to `memory/index.md` entries
- JSONL event log → append to `memory/patterns/PATTERNS.jsonl` (dedupe by hash)
- Notion / Linear / GitHub export → map to `memory/DECISIONS.md` / `memory/OPEN_QUESTIONS.md` / `memory/RISKS.md`

Flow:
1. Show user what will be imported (counts, sample entries)
2. Require explicit approval
3. Pass through `privacy-guardian` per `PRIVACY.md` mode
4. Write via `memory-keeper`
5. Log `{"event": "memory-imported", "payload": {"source": "...", "count": N}}`

### EXPORT
Targets supported:
- `memory.tar.gz` (full bundle of flat `memory/` layout)
- Markdown directory (flat copy of `memory/*.md` + `memory/index.md`)
- JSONL event log (filtered by date range from `memory/patterns/PATTERNS.jsonl`)
- Handoff package (calls `handoff-compiler`)

Flow:
1. User selects target format + scope
2. Pass through `privacy-guardian` (respect current `PRIVACY.md` mode + `REDACT.md` classes)
3. Write to user-specified path
4. Log `{"event": "memory-exported", "payload": {"target": "...", "format": "..."}}`

## Safety

- Both directions require explicit user approval
- Import never overwrites without conflict check
- Export respects current privacy mode and connector allowlist in `SHARING_POLICY.md`
- Per D9: never hard delete during import/export — overwrites archive predecessors to `memory/archive/`
