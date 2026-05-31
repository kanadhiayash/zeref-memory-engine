# Summary

<!-- 1–3 sentences. What problem does this PR solve? -->

## Type

- [ ] `feat`  — new capability
- [ ] `fix`   — bug fix
- [ ] `docs`  — documentation only
- [ ] `chore` — tooling, deps, repo housekeeping
- [ ] `refactor` — code structure, no behavior change
- [ ] `breaking` — incompatible change (requires major version bump)

## Changes

- <!-- bullet list of what changed -->
-

## Architectural fit

Confirm this PR respects Zeref's core principles:
- [ ] Local-first (no hosted dependency added)
- [ ] Harness-agnostic (works in Claude / Codex / Gemini)
- [ ] Privacy-first (writes pass through privacy-guardian)
- [ ] Single-writer wiki (only memory-keeper writes to memory/wiki/)
- [ ] Append-only event log preserved
- [ ] Boundary-first reads (no full-page scans introduced)
- [ ] Human arbitration preserved (no silent conflict resolution)

## Test plan

- [ ] `python3 scripts/zeref-validate-v4.py` passes
- [ ] `claude plugin validate .` passes
- [ ] Manually exercised affected skills/agents/commands
- [ ] Sandbox-tested at HEAD

## Breaking changes

<!-- if Type includes `breaking`, describe migration path here. otherwise: "none". -->

## Related issues

Closes #
