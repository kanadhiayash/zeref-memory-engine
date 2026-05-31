---
description: Manually push approved summaries + decisions to parent project. Requires config/PARENT_SYNC.md enabled.
---

1. Read `config/PARENT_SYNC.md`.
2. If `enabled: false` → report "Parent sync not configured" and exit.
3. Invoke `parent-sync` skill (M2 in v4.1.0; until then, stub responds with implementation status).
4. Report what was pushed (or what's staged for approval if M2 not yet shipped).
