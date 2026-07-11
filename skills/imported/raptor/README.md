---
pack: raptor
mode: reference-only
classification: restricted
source_path: "~/security-workspace/raptor/"
license: unknown-verify-with-owner
outbound_write: forbidden
foreign_code_containment: pass
imported_at: 2026-07-10
imported_by: audit(zeref-consistency-audit)
scope: autonomous-security-research
---

# raptor — reference-only import (restricted)

## Origin

raptor is a user-local autonomous security research harness under `~/security-workspace/raptor/`. Scope is authorized security research and vulnerability triage.

## Classification: restricted

Same rules as [mantishack](../mantishack/README.md):

- Zeref memory writes touching raptor artifacts require `abstract` privacy mode.
- No raptor output crosses into tracked repo tree.
- All invocations logged to local-only journals.

## Boundary

No source vendored. raptor is invoked out-of-band via `cd ~/security-workspace/raptor && claude`. This directory documents the boundary only.

## Audit-scope use in this session

**None.** raptor is registered for enterprise-fleet completeness; the consistency audit does not exercise autonomous security tooling.

## Forbidden

- Executing raptor from within this repo's worktree.
- Passing Zeref memory into raptor.
- Committing raptor output into `zeref-memory-engine`.
- Autonomous scans against third-party infrastructure without prior written authorization.

## Council pack membership

Registered in [team-packs/faang-mangoes-council.md](../../../team-packs/faang-mangoes-council.md) as an on-demand red-team consultant. Not activated by default.
