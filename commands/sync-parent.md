---
description: Manually push approved summaries + decisions to parent project. Requires config/PARENT_SYNC.md enabled. Respects PRIVACY.md mode.
---

1. Read `config/PARENT_SYNC.md`.
2. If `enabled: false` → report "Parent sync not configured" and exit.
3. Read `PRIVACY.md`. If mode = `local-only` → refuse with "local-only mode blocks parent sync".
4. Invoke `parent-sync` skill (STAGE → APPROVE → PUSH). Staged content runs through `evidence-curator` FILTER_SYNC (≥ medium) and `privacy-guardian` per current mode + `REDACT.md`.
5. Report what was pushed (target path, content list, entry counts, manifest hash).
