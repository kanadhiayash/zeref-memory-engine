# FAQ

## v2.6.1 questions (new)

### What are the Auto-Activation Gates?

3 sequential gates that fire before any execution-model call on a major task:

1. `[budget-governor]` — classifies task weight (CRITICAL/HIGH/MEDIUM/LOW), resolves model tier, enforces match
2. `[skill-router]` — picks smallest-useful-stack (1 lead + 2-3 support + 1 QA, max 5 skills)
3. `[prompt-context-engine]` — classifies prompt STRUCTURED/SEMI-STRUCTURED/UNSTRUCTURED; restructures if needed

Plus `[fleet-activator]` companion (probes extended tools) and `[caveman-handoff]` at handoff. Each gate declares output inline; user can override before token spend.

See [[Architecture]] §Auto-Activation Gates.

### Why declare gates inline instead of running silently?

Two reasons:
1. **User override path** — silent gates can't be redirected mid-session
2. **Audit trail** — grep-able evidence of professional workflow design

ADR-001 covers full rationale.

### What is R6 Zero Context Loss?

Shared rule R6 in `_shared/rules.md`. Every fact / entity / constraint from the raw prompt must survive into restructured briefs, routing decisions, handoff packages, parent-sync staging, etc. Verified by diff. v2.6.1 L4 sweep extended R6 coverage to 9 of 14 SKILL.md.

### What is the L1-L15 hardening?

v2.6.1 Phase D workarounds closing Phase C audit findings:
- L1-L5 + L14-L15: validator improvements (dynamic count, event schema, stack-cap lint)
- L9-L13: skill hardening (marker probe, injection filter, cool-down, homoglyph, dual-key override)
- L4: R6 sweep coverage

Closes 2 CRITICAL + 2 HIGH + 2 MEDIUM security findings. See `tests/security-audit-v2.6-C.md` + ADR-002.

### How do I install GitHub Releases for all v2.6.1 tags?

`gh` CLI not installed locally? Use the included script:

```bash
brew install gh
gh auth login
bash scripts/zeref-publish-releases.sh --apply
```

Idempotent. Creates 11 releases (7 legacy `prerelease` + 4 post-rebrand full; v2.6.1 marked `--latest`).

### Why are there both `release/v2.6` AND `release/v2.6-legacy`?

Because the repo has two version chains:
- **Post-rebrand canonical**: v1.0.0 → v2.5.0 → v2.6.0 → v2.6.1 — full GitHub Releases
- **Pre-rebrand legacy**: v2.0.0 / v2.1.0 / v3.0.0 / v4.0.0–v4.3.0 — GitHub `prerelease` flag, branch suffix `-legacy`

The `-legacy` suffix distinguishes them in the branch list. Per FAANG §3.4 controlled-baseline pattern.

## Original FAQ

### Will Zeref OS work with my AI tool?

If your tool can read `AGENTS.md` (Claude Code, Codex, Cursor, Gemini, Aider, Windsurf, Hermes, Amp, Zed, Perplexity), yes. Per-harness stub in the repo handles the rest.

### Is my data sent anywhere?

No. Zeref OS is local-first. Memory lives in plain markdown in your project repo. Connectors are OFF by default in `SHARING_POLICY.md` and require explicit per-action approval to enable.

`local-only` privacy mode blocks all external transmission (parent sync, MCP connectors, handoff push).

### What does "boundary-first read" mean?

Don't load the whole wiki to find one fact. Read `memory/hot.md` (≤500 words) first; consult `memory/index.md` only if hot is insufficient; then load only the named section of the named page. Caps always-on context to ~3-4k tokens regardless of project size.

### How does Zeref OS know I'm running Claude vs GPT vs Gemini?

`budget-governor` auto-detects active model from harness env vars. Resolves to a tier (HAIKU / SONNET / OPUS or HAIKU-equivalent / SONNET-equivalent / OPUS-equivalent for non-Anthropic) and scales verbosity + per-skill caps accordingly. v2.6.1 model-resolver canonicalizes bare aliases to full Anthropic IDs.

### What happens if I commit to a conflict?

`contradiction-resolution` skill halts the write, appends both sides to `memory/CONFLICTS.md`, and asks you to arbitrate (immediately or at `/done`). Never silently resolved. 4 anti-patterns refused: recency-wins, grade-wins, silent-drop, indefinite-snooze.

### Can two sessions write to the same memory file at once?

No. `memory-keeper` is the single writer (Core Principle 5). v2.5 L9 added `zeref/lock.py::MemoryLock` advisory lock; second writer aborts with clear error.

### What is the Two-Strikes Rule?

Don't codify a rule on the first occurrence of an error. Wait for the second. First occurrence → log to `memory/MEMORY.md` as "trap noticed." Second occurrence → promote to a rule. Prevents brittle premature codification.

### How are team packs different from skill stacks?

- **Team pack** (`/team build`): on-demand multi-agent configuration. Roster of up to 4 agents.
- **Skill stack** (from `skill-router` Gate #2): the specific lead + 2-3 support + 1 QA picked for the current task.

When a team pack is active, `skill-router` picks the stack from the pack's roster.

### What's in `references/v4x-canon/`?

Read-only design corpus imported in v4.3: `ZEREF_OS.md` (behavioral constitution), `DECISION_LOG.md` (D1-D11), `MODEL_DEBATE.md`, `USE_CASES.md`, `RESEARCH_RESOURCES.md`, `PACKAGE_INDEX.md`. Don't edit; reference only.

### Why are pre-v2.5 versions marked `prerelease`?

Pre-rebrand (v2.0–v4.3 era). Tags were deleted in past `[Unreleased]` cleanup; restored in v2.6.1 history-reconstruction campaign for completeness. They fail current plugin loader (schema evolution). Per FAANG §3.4 controlled-baseline pattern: keep for audit + history, not for fresh install.

### How do I add a new skill?

**Don't write it manually.** Let `pattern-observer` surface a candidate from repeated work, then `pattern-to-skill` drafts it, then you approve via `/review-skill`. Per Core Principle 10 (Review-First Extension).

If you must write manually: put it in `skills/<name>/SKILL.md` with proper frontmatter, add an entry to `zeref-registry.json` (with `model` + `model_alias` fields), update AGENTS.md Skills table, run `python3 scripts/zeref-validate.py`. Cite an ADR in `docs/adr/` if it's a major addition.

### How do I disable pattern detection?

`config/BUDGET.md` → set `pattern_detection: false`.

### How do I migrate from v4.x to v1.0.0?

Already handled in the v1.0.0 release. If you're on v4.x today and want to update: `claude plugin update zeref-os@zeref-os`. No data migration needed — all memory files keep paths + content.

### How do I migrate from v2.5 to v2.6.1?

Just update the plugin. Additive only. Existing `tests/scores-v*.csv` references to Free/Standard/God Mode continue to work via `budget-governor` alias table. No data migration.

### Will the v2.6 4-gate chain slow me down?

Negligibly. Each gate is HAIKU-tier (LOW weight) and emits ≤500 tokens. Gate cost << execution cost. The user experience: each gate prints one inline `[name]` line before execution starts.

You can skip gates for trivial tasks (single-fact lookup, simple edit) by stating "execute verbatim" or "no restructure" — `prompt-context-engine` honors the skip phrase.

### What if I disagree with a gate's classification?

Override before execution. Example: `[budget-governor]` flags MISMATCH on `(CRITICAL, HAIKU)` — type the dual-key override directive:

```
OVERRIDE: CRITICAL on HAIKU — reason=spec writing, accept lower quality
```

v2.6.1 L13 enforces dual-key for cost-tier overrides; single-key "override" rejected.

### Where do session decisions get logged?

Three places:
1. `memory/DECISIONS.md` — per-session arbitrations (single writer: `memory-keeper`)
2. `docs/adr/` — per-major-release ADRs (FAANG naming)
3. `CHANGELOG.md` + `docs/RELEASE_LOG.md` — shipped releases

See [[Decision-Log]] for the full decision provenance chain.

## Related

- [[Installation]] — per-harness setup
- [[Architecture]] — full system
- [[Glossary]] — terms used here
- [[Decision-Log]] — D1-D11 + ADR-001 + ADR-002
