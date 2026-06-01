# Team Packs

On-demand multi-agent configurations. Max 4 agents per pack. Outputs always land in `team/` (never inline-only).

Activate via `/zeref-os:team [type]`.

## When to use which

| Team | Use it when |
|---|---|
| **solo** | Default. Single-file edits, debugging, conversational work, quick lookups. |
| **build** | Multi-module features, new product surfaces, cross-cutting refactors. |
| **research** | Architecture choices, tech evaluation, comparative analysis, migrations. |
| **red** | Pre-launch security review, adversarial stress test, post-incident retrospective, compliance audit prep. |
| **audit** | Pre-ship QA pass, accessibility audit, code review for external PR, periodic health check. |
| **ship** | Tagging a release, pushing to staging/prod, hotfix, plugin marketplace update. |

## solo

| Role | Notes |
|---|---|
| primary | Whatever model the user invoked |
| memory engine | `memory-keeper` + `privacy-guardian` + `pattern-observer` (background) |

No team files. Standard flow into `memory/`.

## build

| Role | Output |
|---|---|
| Planner | `team/build-plan.md` — module boundaries, contracts, sequencing |
| Implementer | `team/build-progress.md` (append per module) |
| Reviewer | `team/build-review.md` — runs QA gate per hand-off |

**Hand-off protocol:** Planner publishes → User approves → Implementer builds → Reviewer audits → on pass: `memory-keeper` records decision → loop.

## research

| Role | Output |
|---|---|
| Investigator | `team/research-raw.md` — cited sources |
| Synthesizer | `team/research-synthesis.md` — trade-offs + recommendation |
| Fact-checker | `team/research-verification.md` — adversarial verify |

**Rule:** Synthesizer must not make claims absent from `research-raw.md`. Fact-checker scores each major claim `confirmed` / `refuted` / `uncertain`. Final decision recorded in `memory/DECISIONS.md` only after Fact-checker pass.

## red (read-only by default)

| Role | Output |
|---|---|
| Attacker | `team/red-team-attacks.md` (attack catalog — gitignored if sensitive) |
| Security reviewer | flagged findings |
| Constraint checker | invariant verification |
| Evidence recorder | `team/red-team-report.md` (one entry per finding) |

**Rules of engagement:**
- Read-only by default. Override with `--write` (not recommended).
- Per-attack approval for any execution.
- Severity classification mandatory: `critical` / `high` / `medium` / `low` / `informational`.
- Reproducer required for every `critical` or `high` finding.
- No live destructive actions.

## audit

| Role | Output |
|---|---|
| Reader | `team/audit-survey.md` — map of what exists / what changed |
| Linter | `team/audit-lint.md` — style, types, a11y, dead code |
| Quality gate | `team/audit-verdict.md` — pass/fail per item with rationale |

**Args:** `--scope=<path>`, `--diff`.

**Rule:** Quality gate decides ship / no-ship. User override recorded in `memory/DECISIONS.md` with rationale.

## ship

| Role | Output |
|---|---|
| Changelog drafter | `team/ship-changelog.md` (draft for CHANGELOG.md) |
| Release reviewer | `team/ship-review.md` — version bumps, breaking-change call-outs |
| Deploy verifier | `team/ship-verify.md` — smoke tests, health checks, rollback plan |

**Args:** `--version=<semver>`, `--dry`.

**Rules:** Deploy verifier blocks on failed checklist. Breaking changes must be flagged with migration notes. Semver: patch (fix), minor (additive), major (breaking).

## Universal team rules (per ZEREF_OS §8)

1. Team outputs ALWAYS land in files. Never inline-only.
2. Red team is read-only by default.
3. Max 4 agents per pack.
4. All team writes pass through `privacy-guardian`.
5. Recorded activation in `memory/MEMORY.md` under `## Active team`.

## Anti-patterns

- Activating a team without user trigger or explicit recommendation
- Letting a team exceed 4 agents
- Allowing red team write access without `--write` flag
- Skipping the file output (everything must land on disk)
