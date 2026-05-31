---
description: Clear all session permission overrides and restore defaults from config/PERMISSIONS.md + SHARING_POLICY.md.
---

1. Invoke `sync-coordinator` RESET.
2. Clear in-memory session overrides.
3. Re-apply defaults from `config/PERMISSIONS.md` and connector allowlist from `SHARING_POLICY.md`.
4. Report:
   ```
   Session permissions reset to defaults.
   Active permissions:
     filesystem: <list>
     network: <list>
     mcp_servers: <list from SHARING_POLICY.md — enabled connectors only>
     shell_commands: <allow/deny lists>
   ```
