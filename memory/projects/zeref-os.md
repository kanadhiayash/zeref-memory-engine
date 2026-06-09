# Project — Zeref OS

## One-liner

Local-first, harness-agnostic, privacy-first context + memory engine for AI coding harnesses (Claude Code, Cursor, Gemini, Aider). Canonical state in markdown; reference Python runtime for deterministic enforcement.

## Source of Truth

- **GitHub:** `zeref-os v1.0.0` (2026-05-31) — canonical release
- **Local upgrade:** `compassionate-ride-66e134` worktree (v2.0 shipped, v2.5 audit in progress)
- **Predecessor (archived):** v1.x Skills Fleet → v2.x Agent OS → v3.x → v4.x context engine

## Architecture

- **AGENTS.md** — canonical spec; all harness stubs defer
- **6 agents:** memory-keeper, privacy-guardian, sync-coordinator, evidence-curator, pattern-observer, handoff-orchestrator
- **10 skills:** wiki-maintenance, budget-governor, project-setup, contradiction-resolution, evidence-grader, handoff-compiler, memory-import-export, parent-sync, pattern-to-skill, privacy-abstraction
- **8 commands:** /start /done /stop /status /sync-parent /reset-permissions /review-skill /team
- **6 team packs:** solo build research red audit ship
- **Flat memory/ layout:** hot.md, index.md, DECISIONS.md, OPEN_QUESTIONS.md, RISKS.md, CONFLICTS.md, MEMORY.md, archive/, patterns/PATTERNS.jsonl, snapshots/, raw/, sync/

## v2.0 Additions

- `SOUL.md` (6 principles)
- `zeref-registry.json` (10 skills)
- `_shared/rules.md` (R1-R4)
- Python package `zeref/`: privacy.py, cli.py, db.py, dashboard.py, demo.py
- `pyproject.toml` (`pipx install zeref-os`)
- 40 score rows, 2 eval-harness specs

## v2.5 Audit (in progress)

- **Phase A done** — 85 claims graded, 5 contradictions K1-K5
- **Phase B-F queued** — sandbox stress, security hunt, workarounds, rubric re-score, UX polish

## Honest Score (post Phase A)

| Dim | Self-claimed v2.0 | Audit-corrected | Δ |
|---|---|---|---|
| Vision | 9 | 9 | 0 |
| Execution | 8 | 6 | -2 |
| Architecture | 9 | 7 | -2 |
| Operational Readiness | 6 | 4 | -2 |
| Engineer Credibility | 9 | 7 | -2 |

## Open Risks

- **K1** PROJECT.md never populated (self-dogfood failure)
- **K2** privacy-abstraction has 1 trigger (safety-critical, weakest spec)
- **K3** `zeref init` advertised but unimplemented
- **K4** Single-writer prose-only — no enforcement
- **K5** "Every write through privacy-guardian" — zero enforcement code

## Inspirations

ECC (Affaan) test discipline · gstack ETHOS · Karpathy paradigm shifts · AGENTS.md standard · BMAD-METHOD · GitHub Spec Kit
