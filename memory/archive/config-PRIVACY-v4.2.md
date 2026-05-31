---
mode: exact   # exact | abstract | local-only
abstract_rules:
  strip_pii: true
  strip_internal_paths: true
  strip_credentials: true
  strip_numbers: false   # set true to redact $/metric values
local_only_blocks:
  - memory/sync/outbound/
  - memory/sync/parent/
---

# Privacy

Privacy is a central design concern. Every write to `memory/` passes through the privacy guardian.

## Modes

- **exact** — write full detail (default for solo, trusted-local work)
- **abstract** — `privacy-abstraction` skill rewrites before write (remove names, paths, credentials, optionally numbers)
- **local-only** — block all writes to `memory/sync/outbound/` and `memory/sync/parent/` (no upward propagation)

## Per-session overrides

Use `/reset-permissions` to clear session overrides and restore defaults from this file.

## What never gets written

Regardless of mode:
- credentials, API keys, tokens
- contents of files matched by `.gitignore`
- raw clipboard contents (unless explicitly captured to `memory/raw/`)
