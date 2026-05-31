---
harness: claude-code
# Claude-specific behavior overrides that diverge from AGENTS.md defaults.
# Keep this file short. Anything universal belongs in AGENTS.md.
overrides:
  skill_invocation: native        # use Claude Code's Skill tool with `zeref:<name>`
  command_namespace: /zeref       # slash commands resolve under /zeref:<command>
  subagent_model_pref:
    memory-keeper: haiku
    project-setup: sonnet
    pattern-to-skill: opus        # only for draft generation
  hook_ordering: native           # rely on Claude Code SessionStart/UserPromptSubmit hooks
---

# Claude Overrides

> Per ZEREF_OS §12 file structure. Claude-Code-specific quirks live here so AGENTS.md stays harness-agnostic.

## Model selection

- **memory-keeper** writes use Haiku for cost/speed (high-frequency, low-reasoning).
- **project-setup** uses Sonnet for the interview (conversational, moderate reasoning).
- **pattern-to-skill** draft generation uses Opus (creative synthesis from event log).

## Skill / command surface

- All Zeref skills surface as `zeref:<skill-name>` via Claude Code's Skill tool.
- All Zeref commands surface as `/zeref:<command>` in the slash command namespace.
- The `.claude-plugin/plugin.json` manifest binds these.

## Hooks

Zeref relies on Claude Code's native SessionStart and UserPromptSubmit hooks (not custom watchers) to trigger:
- `/start` boot sequence on session start
- `privacy-guardian` pre-write checks
- `pattern-observer` background scan on every prompt submit

## What does NOT belong here

- Universal protocol (memory model, privacy modes, team packs) → `AGENTS.md`
- Per-project config → `config/PROJECT.md`
- Budget tier → `config/BUDGET.md`
- Connector enablement → `SHARING_POLICY.md`
