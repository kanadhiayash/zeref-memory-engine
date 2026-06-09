# Team Packs

On-demand multi-agent configurations per ZEREF_OS §8. Max 4 agents per pack. Outputs land in `team/` (never inline-only). Activated via `/team [type]`.

**v2.6.1 compatibility**: Team packs predate the 4-gate Auto-Activation chain but coexist cleanly. When a team pack is active, the 3 gates still fire on every major task; the pack's agents become the candidate stack `skill-router` (Gate #2) picks from.

## Pack inventory

| Pack | Roster (max 4) | Use case | Output dir |
|---|---|---|---|
| **solo** | 1 primary + memory engine | Default. Single-agent operation. | `team/solo/` |
| **build** | Planner + Implementer + Reviewer | Multi-module features. Planning + execution + QA loop. | `team/build/<feature>/` |
| **research** | Investigator + Synthesizer + Fact-checker | Tech evaluation. Sources + synthesis + verification. | `team/research/<topic>/` |
| **red** | Attacker + Security reviewer + Constraint checker + Evidence recorder (read-only) | Adversarial review. **Read-only by default.** | `team/red/<target>/` |
| **audit** | Reader + Linter + Quality gate | Pre-ship QA. Doc + spec + code audit. | `team/audit/<scope>/` |
| **ship** | Changelog drafter + Release reviewer + Deploy verifier | Release prep. CHANGELOG + scorecard + checklist. | `team/ship/<version>/` |

Each pack's roles + outputs declared in `team-packs/<name>.md`.

## Activation

```
/team               # show available packs + currently active pack
/team solo          # revert to default 1-primary + memory engine
/team build         # spawn Planner + Implementer + Reviewer
/team research      # spawn Investigator + Synthesizer + Fact-checker
/team red           # spawn read-only adversarial roster
/team audit         # spawn audit roster (used in v2.5 + v2.6.1 audit campaigns)
/team ship          # spawn ship roster (used in v2.5 Phase F + v2.6.1 Phase G)
```

### Pack-specific args

```
/team red --write              # grant write access (NOT recommended)
/team audit --scope=<path>     # scope audit to path
/team audit --diff             # audit working-tree diff vs base
/team ship --version=<semver>  # target release version
/team ship --dry               # produce artifacts without tagging
```

## Behavior

1. Read `team-packs/<name>.md`
2. If `<name>` missing, list all packs and exit
3. Verify max-agents cap (4); refuse if pack declares more
4. Spawn roster (via harness Skill tool for Claude Code)
5. Create `team/.gitkeep` if missing; ensure `team/` exists
6. Record activation in `memory/MEMORY.md` under `## Active team`
7. **v2.6 integration**: gates fire on every team-pack task per Auto-Activation chain
8. On `/done` or `/stop`: pack finalizes outputs; `memory-keeper` records decisions per pack rules

## Output contract

- Every pack writes its declared output files in `team/`
- No inline-only deliverables (orchestrator re-prompts if a role skips file output)
- Output files committed alongside code changes (rationale travels with diff)

## Safety

- **red** team is read-only by default per ZEREF_OS §8 anti-pattern: "Do NOT activate a team without user trigger or explicit recommendation."
- **ship** Deploy verifier blocks on failed checklist. User can override; override is recorded in `memory/DECISIONS.md`.
- All team writes still pass through `privacy-guardian` per `PRIVACY.md` + R3.
- **v2.6.1 R6 (Zero Context Loss)**: pack outputs that summarize or restructure source material must preserve every entity from inputs (handoff-compiler + caveman-handoff handle cross-pack handoffs).

## Pack composition vs skill-router

When `/team [type]` is active, the pack defines a candidate roster. When a new major task arrives:

1. `budget-governor` classifies weight (Gate #1)
2. `skill-router` picks lead + support + QA from the pack roster (Gate #2) — **never exceeds 5 skills** (L14 cap)
3. `fleet-activator` probes external tools the pack may need
4. `prompt-context-engine` restructures the prompt (Gate #3)
5. Pack executes per gates

Pack roster ≠ active stack. Roster is the menu; gate #2 picks the dish.

## v2.6.1 audit campaign reference (the `audit` pack in action)

The v2.6.1 audit campaign (7 phases A-G) used `/team audit` as its primary pack:
- **Reader**: walked AGENTS.md / SKILL.md / registry / CHANGELOG; extracted claims into `tests/claims-v2.6.csv`
- **Linter**: ran `python3 scripts/zeref-validate.py` + sandbox spec generation
- **Quality gate**: scored 150 sandbox rows + 8 CVSS attacks → `tests/scores-v2.6-B.csv` + `tests/security-audit-v2.6-C.md`

Force multipliers (per v2.5 hybrid stack pattern): ECC `/ecc:eval-harness`, `/ecc:security-scan`, `/ecc:agent-eval`; gstack `/qa` + `/review`; raptor (security-workspace); `/graphify` (claim graph).

## Related

- [[Architecture]] — Auto-Activation Gates context
- [[Pattern-Detection]] — `pattern-observer` may surface "user activates X pack repeatedly" → candidate skill
- `team-packs/<name>.md` — full role definitions per pack
- `references/zeref-qa-gate.md` — used by `audit` + `build` Reviewer
- `references/zeref-safety-principles.md` — used by `red` team
