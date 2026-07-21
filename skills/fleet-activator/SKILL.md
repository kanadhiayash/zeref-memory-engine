---
name: fleet-activator
description: Companion to skill-router. Live-probes reachability of extended-tool surfaces (ECC, claude-obsidian, Graphify, browser-harness, notebooklm) by scanning known filesystem paths and MCP availability. Reports reachable / unreachable per tool. For unreachable tools, names the gap and proposes the closest emulator. Never silently fails — every probe result is logged.
trigger:
  - invoked by skill-router when Extended-tool hint detected
  - "probe extended tools"
  - "is ECC reachable"
  - "check fleet reachability"
  - before any /ecc / /graphify / /browse invocation
model: haiku
reasoning_class: fast
max_turns: 6
---

# fleet-activator

## Mission

Provide skill-router with a reliable reachability report before any extended-tool invocation. Treat extended tools as optional — flag missing rather than fail.

## Probe targets (canonical paths)

| Tool | Probe location | Probe method | If unreachable, emulate via |
|---|---|---|---|
| **ECC** | a user-configured local path OR `~/.claude/plugins/cache/ecc/ecc/` | `test -d` on either path; if either exists → reachable | `agent-skills:*` skills (review, build, test) |
| **claude-obsidian** | `~/.claude/plugins/` plus a name match for `claude-obsidian` | directory scan | `wiki-maintenance` + `memory-keeper` (degraded — no Obsidian vault sync) |
| **Graphify** | `~/.claude/skills/graphify/SKILL.md` | `test -f` | `evidence-grader` + manual claim mapping (no graph) |
| **browser-harness** | MCP tool registry for `mcp__claude-in-chrome__*` | tool-name lookup | gstack `/browse` if present; else flag "no browser surface" |
| **notebooklm** | `~/.claude/plugins/` name match + plugin registry scan | directory + registry lookup | `/deep-research` skill (less audio-friendly) |
| **gstack** | `~/.claude/skills/` for any `gstack-*` SKILL.md OR `/browse` / `/ship` skill presence in available-skills list | skill-list scan | ECC + manual workflow |

Probe locations are environment-specific. Re-probe at each invocation — paths may move.

## Auto-Activation Rule

Invoked by `skill-router` Step 4 when any "Extended-tool hint" is present in the chosen stack. 4 steps:

1. **Receive tool list** from skill-router (e.g. `["ECC", "Graphify"]`).
2. **Probe each** per §Probe targets. Use Bash for `test -d` / `test -f`; use available-tool inspection for MCP presence.
3. **Build report**:
   ```
   [fleet-activator]
     ECC: reachable (path=~/.claude/plugins/cache/ecc/ecc/)
     Graphify: reachable (path=~/.claude/skills/graphify/SKILL.md)
     browser-harness: UNREACHABLE — emulating via gstack /browse
   ```
4. **Log probe events** to `memory/patterns/PATTERNS.jsonl` (one entry per probed tool, `event: "tool-probe"`).

If unreachable, name the gap explicitly in the report. Never proceed silently with an emulator the user did not consent to — if the emulation is materially weaker (e.g. no graph for Graphify), pause and confirm.



## Marker-file probe

Presence-only probe (`test -d` / `test -f`) is **not sufficient** — adversary can `mkdir` an empty path matching the expected location. Each tool requires a per-tool marker check:

| Tool | Marker file(s) — ALL must exist | Anti-spoof rationale |
|---|---|---|
| ECC | `<root>/CLAUDE.md` + `<root>/manifests/` OR `<root>/.claude-plugin/plugin.json` | Real ECC ships CLAUDE.md + plugin manifest; empty dir fails |
| claude-obsidian | `<root>/.claude-plugin/plugin.json` + `<root>/skills/` | Real plugin has manifest + skills tree |
| Graphify | `<root>/SKILL.md` with frontmatter `name: graphify` | Validate frontmatter not just path |
| browser-harness | MCP tool registry contains `mcp__claude-in-chrome__list_tabs` (canonical method) | Tool-name lookup, not just prefix |
| notebooklm | `<root>/.claude-plugin/plugin.json` AND audio-tool reference | Manifest verify |
| gstack | `<root>/skills/browse/SKILL.md` OR `/browse` skill present in available-skills | Skill presence check |

If marker check fails, report `UNREACHABLE-EMPTY-DIR` (distinct from `UNREACHABLE-MISSING`). Both route to emulator with explicit user-consent prompt.

Per `_shared/rules.md#R3`: marker contents never read into external output; existence + frontmatter-name only.

## Anti-patterns (hard blocks)

- **Probing unknown paths**: only probe the paths in §Probe targets. New tool? Add it to the matrix first.
- **Caching a stale probe**: re-probe every invocation. Probes are cheap (filesystem `test`); reachability changes when user installs / removes plugins mid-session.
- **Auto-installing**: never auto-install a missing tool. Report gap + emulator only.

## Safety

- Per `_shared/rules.md#R6` (Zero Context Loss): tool list received from `skill-router` is probed in full; no tool silently dropped from report even when unreachable.
- Per `_shared/rules.md#R4`: if probe result is ambiguous (path exists but executable check fails), report "PARTIAL — manual verification needed."
- Per `_shared/rules.md#R3`: never include probe-path contents in external output; path strings alone are fine.
- Probe results logged for `pattern-observer` — if a tool is repeatedly unreachable, that becomes a candidate skill-pack adjustment.
- Filesystem probes are read-only. No state mutation in this skill.
