---
defaults:
  filesystem:
    - read: project-root
    - write: memory/
  network:
    - denied
  mcp_servers: []
  shell_commands:
    - allow: [git status, git diff, git log, ls, cat]
    - deny: [rm -rf, git push --force, git reset --hard]
session_overrides:
  # ephemeral; cleared by /reset-permissions or /stop
  # example: { mcp_servers: [github, linear] }
---

# Permissions

Project defaults with per-session overrides. The `sync-coordinator` agent enforces these.

## Defaults

Apply on every `/start` unless overridden.

## Session overrides

Granted at `/start` interview or mid-session by explicit user prompt. Cleared by `/reset-permissions` or end of session via `/stop`.

## Irreversible actions

Always require explicit user confirmation regardless of permissions:
- destructive git operations (force push, hard reset, branch delete)
- file deletion outside `memory/snapshots/`
- network requests to non-allowlisted hosts
- publishing / sending / posting to any external surface
