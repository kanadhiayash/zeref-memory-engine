# Zeref OS — Pivot Log (pre-v1.0.0 history)

This file captures the design pivots and version lineage that preceded the
public **v1.0.0** launch of Zeref OS. The git history corresponding to these
versions is preserved in the read-only archive repo
[`kanadhiayash/zeref-os-archive`](https://github.com/kanadhiayash/zeref-os-archive).

Versioning policy going forward: every public release of `zeref-os` follows
[Semantic Versioning](https://semver.org/) starting at `v1.0.0`. Pre-v1
versions listed here are historical; they are **not** installable from the
public registry and their concepts are summarised below for archaeology only.

---

## Pivot 1 — Initial concept (pre-v2.0)

**Frame:** "AI assistants forget everything between sessions. Build a
per-project markdown wiki the AI reads first."

**Shipped:**
- Minimum-viable memory layout (`memory/hot.md`, `memory/MEMORY.md`).
- One agent: a single writer (later renamed `memory-keeper`).
- One privacy posture: PII never leaves disk.

**Limits found:**
- No conflict-resolution path → contradictions accumulated silently.
- No evidence grading → stale claims read as truth.
- No cross-harness portability.

---

## Pivot 2 — v2.0–v2.5 — Multi-skill fleet

**Frame:** Single writer is not enough. Need a fleet of disciplined skills
plus on-demand team packs for different work shapes.

**Shipped:**
- 6 background agents (`memory-keeper`, `privacy-guardian`,
  `sync-coordinator`, `evidence-curator`, `pattern-observer`,
  `handoff-orchestrator`).
- 10 on-trigger skills (project-setup, wiki-maintenance,
  contradiction-resolution, evidence-grader, etc.).
- 6 team packs (solo / build / research / red / audit / ship).
- Three privacy modes: `exact` / `abstract` / `local-only`.
- Reference Python runtime (`zeref/cli.py`) for `status`,
  `write-decision`, `audit-privacy`, `audit`.

**Limits found:**
- Token spend not gated → expensive skills fired on trivial prompts.
- Skill routing implicit → too many skills active at once.
- Cross-harness handoff lossy → context evaporated on model switch.

---

## Pivot 3 — v2.6.x — 4-gate Auto-Activation chain

**Frame:** Every major task must self-classify cost, stack, prompt, and
handoff *before* any token spend.

**Shipped:**
- 14 disciplined skills (4 new: `skill-router`, `fleet-activator`,
  `prompt-context-engine`, `caveman-handoff`).
- 4-gate Auto-Activation: `budget-governor` → `skill-router` →
  `fleet-activator` → `prompt-context-engine`.
- R6 Zero Context Loss invariant — every entity in a prompt survives
  restructure, routing, and handoff.
- Model-tier routing: Haiku 4.5 / Sonnet 4.6 / Opus 4.7 with canonical id
  mapping in `_shared/model-resolver.md`.
- `zeref-validate.py` skill-count read dynamically from registry;
  `PATTERNS.jsonl` event-schema validator with 11 known event types.
- Prompt-injection filter; irreversibility cool-down; NFKC + homoglyph
  guard; dual-key budget override.

**Audit verdict (Jun 2026):** Strong architecture, but version surfaces
had drifted across files (`pyproject.toml` 2.0.0, `__init__.py` 2.0.0,
plugin manifest 1.0.0, README 2.6.1, registry 2.6.1-phaseD). Privacy
scrubber missed provider-shaped tokens (`sk-proj-*`, bare `sk-*`,
natural-language `API key sk-...`). No reproducible `tests/` directory.
`SECURITY.md` routed vuln reports to public issues. CI used moving
`@v4`/`@v5` action tags. Verdict: trust repair required before any
feature expansion.

---

## Pivot 4 — v1.0.0 (public launch)

**Decision (2026-06-19):** Reset the version line. Treat the current repo
as the public **v1.0.0** baseline. Pre-v1 history archived to
`kanadhiayash/zeref-os-archive` (read-only). The v1.0.0 release packages
the v2.6.x architecture (4-gate chain, 14 skills, 6 agents, R6 invariant)
under a single coherent version surface, with operationally verified
trust guarantees:

- single source of truth for the active version (`zeref/VERSION`);
- machine-checked version consistency across every surface
  (`scripts/check-version-consistency.py`);
- public, reproducible `tests/` directory with ≥85% coverage on `zeref/`;
- expanded privacy scrubber covering 11 additional credential patterns;
- `SECURITY.md` routed through GitHub Private Vulnerability Reporting
  (no public-issue disclosure path);
- CI workflows pinned to full commit SHAs with `dependabot.yml` upkeep;
- four-axis benchmark harness (`portability`, `adaptivity`,
  `scalability`, `trust`) with a published `RUBRIC.md`;
- harness-portability matrix evidence in `docs/HARNESS_MATRIX.md`;
- small / medium / enterprise team packs with explicit token envelopes.

**What carries forward unchanged:** the 6 background agents, 14 skills,
6 team packs, 8 commands, R6 invariant, 4-gate chain, three privacy
modes, flat memory layout. The v2.6.x architecture is the v1.0.0
architecture. The reset is a version-surface reset, not an architecture
reset.

**What this is *not*:** a rewrite. No skills were renamed. No agents
were removed. No memory-layout fields were dropped. Anyone with a
working v2.6.1 install can stay on v2.6.1 indefinitely from the archive
repo — the public registry simply starts numbering at `v1.0.0`.

---

## Reference

- Full v2.6.x release notes: archived in
  `kanadhiayash/zeref-os-archive` (branch `legacy/v2.6.1`).
- v2.6.1 → v1.0.0 surface diff: see `CHANGELOG.md`.
- Trust-repair overrides applied during this pivot: see `docs/RISK_LOG.md`.
