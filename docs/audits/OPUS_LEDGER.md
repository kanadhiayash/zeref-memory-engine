# OPUS_LEDGER.md

Every Opus 4.7 call across the audit + remediation. Enforces the "Opus only when critical" constraint auditably.

| ts | phase | R-id or D-id | subagent | reason | outcome |
|---|---|---|---|---|---|
| 2026-07-10 | Phase 2 WS-C | audit | `general-purpose` (Opus 4.7) | correctness-load-bearing (runtime write-path map + 10 sandbox tests) | partial — session limit hit at agent `a75277b752c52c08f`; recovered by direct main-thread reads |
| 2026-07-10 | Phase 2 WS-D | audit | `agent-skills:security-auditor` (Opus 4.7) | security-blast-radius (policy vs enforcement audit) | full — 15 candidate findings |
| 2026-07-10 | Phase 5 | reconciler | main-thread Opus 4.7 | correctness-load-bearing (evidence reconciler quality gate) | 40 findings survived |
| 2026-07-10 | Phase 5 | council synthesis | main-thread Opus 4.7 | decision-load-bearing (D1-D7 inline synthesis) | 7 decisions surfaced |
| 2026-07-11 | Phase 7 R3 | remediation | main-thread Opus 4.7 | correctness-load-bearing + security-blast-radius (privacy policy loader design) | `zeref/security/policy.py` shipped |
| 2026-07-11 | Phase 9 R9 | remediation | main-thread Opus 4.7 | trust-load-bearing (release meta-gate design) | 6 → 12 subchecks + SHA-bound evidence blobs |
| 2026-07-11 | Phase 11 | release orchestration | main-thread Opus 4.7 | irreversibility (final go/no-go on v1.1.0 changeset) | commit `cef6a77` — 12/12 subchecks PASS |

## Reason field grammar

Every row's `reason` must match one of:

- `correctness-load-bearing` — wrong output = shipped defect.
- `irreversibility` — merge-to-main / tag / publish.
- `decision-load-bearing` — architectural choice with migration cost.
- `security-blast-radius` — privacy / permissions / egress.
- `trust-load-bearing` — false PASS = shipped defect (release gate).

Anything else routes to Sonnet or Haiku. Compliance verified: every row above matches.

## Session-limit incident (Phase 2 WS-C)

Agent `a75277b752c52c08f` hit its API session limit after ~40% of its brief. Runtime write-path map + 10 sandbox test verdicts unfinished. Recovered by direct reads on:

- `zeref/cli.py`
- `zeref/memory/core.py`
- `zeref/privacy.py`
- `zeref/guards/*`
- `zeref/audit/*`

Impact on findings: none — WS-C's contribution to `ZRF-AUDIT-001..008` was validated by other workstreams + direct code inspection. R3 design lands on the completed picture.

Follow-on: WS-C sandbox tests (PII/credential/contradiction/concurrent/local-only) remain undone at v1.1.0. Recommended for v1.2.0 hardening pass.
