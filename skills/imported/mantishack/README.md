---
pack: mantishack
mode: reference-only
classification: restricted
source_path: "~/security-workspace/mantishack/"
license: unknown-verify-with-owner
outbound_write: forbidden
foreign_code_containment: pass
imported_at: 2026-07-10
imported_by: audit(zeref-consistency-audit)
scope: offensive-security-research
---

# mantishack — reference-only import (restricted)

## Origin

mantishack is a user-local offensive-security research harness under `~/security-workspace/mantishack/`. Access is scoped to authorized security research, CTF work, and defensive validation only.

## Classification: restricted

Per user's global `CLAUDE.md`: "All security work follows the same GitHub_OS rules (branch from `main`, no direct push, conventional commits, secrets out of code, classification embedded in filenames when restricted)."

Restricted means:

- No mantishack artifact, output, or configuration is written to Zeref memory in `exact` privacy mode. `abstract` mode required.
- No mantishack output crosses into the tracked repo tree.
- Any mantishack invocation is logged to a **local-only** journal, never `memory/sync/outbound/`.

## Boundary

No source vendored. mantishack is invoked out-of-band via `cd ~/security-workspace/mantishack && claude`. This directory exists only to document the boundary and register the pack for council membership.

## Audit-scope use in this session

**None.** WS-D (privacy/security) is a passive policy-vs-enforcement audit; it does not exercise offensive tooling. mantishack is registered because the user asked for the full enterprise fleet stood up, not because the audit needs it.

## Forbidden

- Executing mantishack from within this repo's worktree.
- Passing Zeref memory into mantishack.
- Committing mantishack output into `zeref-memory-engine`.
- Any offensive test against third-party infrastructure without prior written authorization.

## Council pack membership

Registered in [team-packs/faang-mangoes-council.md](../../../team-packs/faang-mangoes-council.md) as an on-demand red-team consultant for the security-policy decisions surfaced in Phase 5. Not activated by default.
