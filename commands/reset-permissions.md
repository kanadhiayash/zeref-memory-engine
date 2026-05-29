---
description: Clear all session permission overrides and restore defaults from config/PERMISSIONS.md.
---

1. Invoke `sync-coordinator` RESET.
2. Clear in-memory session overrides.
3. Re-apply defaults from `config/PERMISSIONS.md`.
4. Report:
   ```
   Session permissions reset to defaults.
   Active permissions:
     filesystem: <list>
     network: <list>
     mcp_servers: <list>
     shell_commands: <allow/deny lists>
   ```
