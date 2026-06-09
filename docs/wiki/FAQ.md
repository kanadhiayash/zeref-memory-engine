# FAQ

### What are the Auto-Activation Gates?

Four sequential gates that fire before any execution-model call on a major task:

1. `[budget-governor]` — classifies task weight (CRITICAL / HIGH / MEDIUM / LOW), resolves model tier, enforces match.
2. `[skill-router]` — picks smallest-useful-stack (1 lead + 2-3 support + 1 QA, max 5 skills).
3. `[fleet-activator]` companion — probes extended tools (ECC, claude-obsidian, Graphify, gstack, …).
4. `[prompt-context-engine]` — classifies prompt STRUCTURED / SEMI-STRUCTURED / UNSTRUCTURED; restructures if needed.

Plus `[caveman-handoff]` at handoff. Each gate declares output inline; user can override before token spend.

See [[Architecture]] §Auto-Activation Gates.

### Why declare gates inline instead of running silently?

Two reasons: silent gates can't be redirected mid-session, and the inline declaration is a grep-able audit trail of every cost / stack / classification decision.

### What is R6 Zero Context Loss?

Shared rule R6 in `_shared/rules.md`. Every fact / entity / constraint from the raw prompt must survive into restructured briefs, routing decisions, handoff packages, parent-sync staging, and skill drafts. Verified by diff.

### Will Zeref OS work with my AI tool?

If your tool can read `AGENTS.md` (Claude Code, Codex, Cursor, Gemini, Aider, Windsurf, Hermes, Amp, Zed, Perplexity), yes. Per-harness stub in the repo handles the rest.

### Is my data sent anywhere?

No. Zeref OS is local-first. Memory lives in plain markdown in your project repo. Connectors are OFF by default in `SHARING_POLICY.md` and require explicit per-action approval to enable.

`local-only` privacy mode blocks all external transmission (parent sync, MCP connectors, handoff push).

### What does "boundary-first read" mean?

Don't load the whole wiki to find one fact. Read `memory/hot.md` (≤500 words) first; consult `memory/index.md` only if hot is insufficient; then load only the named section of the named page. Caps always-on context to ~3-4k tokens regardless of project size.

### How does Zeref OS know I'm running Claude vs GPT vs Gemini?

`budget-governor` auto-detects active model from harness env vars. Resolves to a tier (HAIKU / SONNET / OPUS or HAIKU-equivalent / SONNET-equivalent / OPUS-equivalent for non-Anthropic) and scales verbosity + per-skill caps accordingly. The model-resolver canonicalizes bare aliases to full Anthropic ids.

### What happens if I commit to a conflict?

`contradiction-resolution` skill halts the write, appends both sides to `memory/CONFLICTS.md`, and asks you to arbitrate (immediately or at `/done`). Never silently resolved. Four anti-patterns refused: recency-wins, grade-wins, silent-drop, indefinite-snooze.

### Can two sessions write to the same memory file at once?

No. `memory-keeper` is the single writer (Core Principle 5). `zeref/lock.py::MemoryLock` adds an advisory lock; the second writer aborts with a clear error.

### What is the Two-Strikes Rule?

Don't codify a rule on the first occurrence of an error. Wait for the second. First occurrence → log to `memory/MEMORY.md` as "trap noticed." Second occurrence → promote to a rule. Prevents brittle premature codification.

### How are team packs different from skill stacks?

- **Team pack** (`/team build`): on-demand multi-agent configuration. Roster of up to 4 agents.
- **Skill stack** (from `skill-router` Gate #2): the specific lead + 2-3 support + 1 QA picked for the current task.

When a team pack is active, `skill-router` picks the stack from the pack's roster.

### How do I add a new skill?

**Don't write it manually.** Let `pattern-observer` surface a candidate from repeated work, then `pattern-to-skill` drafts it, then you approve via `/review-skill`. Per Core Principle 10 (Review-First Extension).

If you must write manually: put it in `skills/<name>/SKILL.md` with proper frontmatter, add an entry to `zeref-registry.json` (with `model` + `model_alias` fields), update AGENTS.md Skills table, run `python3 scripts/zeref-validate.py`.

### How do I disable pattern detection?

`config/BUDGET.md` → set `pattern_detection: false`.

### Will the 4-gate chain slow me down?

Negligibly. Each gate is HAIKU-tier (LOW weight) and emits ≤500 tokens. Gate cost << execution cost. The user experience: each gate prints one inline `[name]` line before execution starts.

You can skip gates for trivial tasks (single-fact lookup, simple edit) by stating "execute verbatim" or "no restructure" — `prompt-context-engine` honors the skip phrase.

### What if I disagree with a gate's classification?

Override before execution. Example: `[budget-governor]` flags MISMATCH on `(CRITICAL, HAIKU)` — type the dual-key override directive:

```
OVERRIDE: CRITICAL on HAIKU — reason=spec writing, accept lower quality
```

Dual-key required for cost-tier overrides; single-key "override" rejected.

### Where do session decisions get logged?

Two places:
1. `memory/DECISIONS.md` — per-session arbitrations (single writer: `memory-keeper`).
2. `CHANGELOG.md` — shipped releases.

## Related

- [[Installation]] — per-harness setup
- [[Architecture]] — full system
- [[Glossary]] — terms used here
