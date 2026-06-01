# FAQ

## General

**Q: What is Zeref OS in one sentence?**
A persistent, harness-agnostic context and memory engine for AI work — local-first markdown files, privacy-on-by-default, no hosted service.

**Q: Is it an agent harness?**
No. Zeref OS wraps existing harnesses (Claude Code, Cursor, Codex, Gemini, etc.). It's a memory engine they plug into.

**Q: Is it open source?**
Yes — MIT licensed.

**Q: Does it require a subscription?**
No. Free install. Works with any model the user provides.

**Q: Does it transmit my data anywhere?**
No. Local files only by default. External transmission requires per-connector enablement in `SHARING_POLICY.md` (all OFF by default) and per-action user approval.

## Setup

**Q: How long does setup take?**
~5 minutes. `/zeref-os:start` runs a conversational interview that writes 7 config files. Re-run `/zeref-os:start` to boot.

**Q: Do I need to install MCP connectors?**
No. Zeref OS ships **zero** bundled MCP tools. Recommendation-only after pattern-observer detects repeated manual behavior. See [Privacy Model](Privacy-Model) → `SHARING_POLICY.md`.

**Q: What if I cancel the setup interview?**
Zeref OS boots in READ-ONLY mode until the schema is complete (per ZEREF_OS §7).

## Privacy

**Q: Default privacy mode?**
`abstract`. `privacy-abstraction` rewrites every payload, stripping credentials, PII, internal paths, and any other enabled `REDACT.md` classes.

**Q: Can I write exact data?**
Yes — set `mode: exact` in root `PRIVACY.md`. Only when project context justifies it.

**Q: How do I block all external sharing?**
Set `mode: local-only` in `PRIVACY.md`. All writes to `memory/sync/outbound/` and `memory/sync/parent/` are blocked.

**Q: What's the difference between PRIVACY.md, REDACT.md, and SHARING_POLICY.md?**
- `PRIVACY.md` = global mode (the gate)
- `REDACT.md` = concrete sensitive classes (the substance to strip)
- `SHARING_POLICY.md` = per-connector allowlist (the external surface)

See [Privacy Model](Privacy-Model).

## Memory

**Q: Where does Zeref OS store data?**
In the local project directory under `memory/`. Plain markdown files. No database, no cloud.

**Q: How does it not blow my token budget?**
Boundary-first reads. `memory/hot.md` is ≤500 words and read first. Full pages are only loaded when domain-specific context is needed. `budget-governor` scales verbosity to the active model tier.

**Q: Can I edit memory files manually?**
- `memory/MEMORY.md` — agent-written. Don't edit; agents may overwrite.
- All other `memory/*.md` — yes, edit freely. `memory-keeper` will pick up changes on next session.

**Q: What's the difference between hot.md and index.md?**
- `hot.md` = ≤500 words of current context (read first)
- `index.md` = domain index (read only if hot.md is insufficient)

## Conflicts

**Q: What happens if two decisions contradict?**
`memory-keeper` halts the write, appends both sides to `memory/CONFLICTS.md`, and surfaces to the user. User arbitrates. Never silent.

**Q: Can I snooze a conflict?**
Yes — `snooze-until-done` is a valid response. The conflict re-surfaces at the next `/zeref-os:done`. After 3 snoozes, you get a warning.

## Harnesses

**Q: Which harnesses work?**
Claude Code (native plugin), Codex, Cursor, Gemini CLI / Antigravity, Windsurf, Aider, Hermes, Amp, Zed, Perplexity Computer — any harness that reads `AGENTS.md`.

**Q: How do I switch from Claude to Cursor mid-project?**
Same project directory. Just install Cursor's stub (`cp .zeref/.cursor/rules/zeref.mdc .cursor/rules/`). Memory files don't move. Next session restores context from `hot.md` → `index.md`.

**Q: Lossless handoff between models?**
Yes — `/zeref-os:stop --handoff` compiles `STATE.json` + `SUMMARY.md` + `NEXT.md` into `memory/sync/outbound/handoff-<iso>/`. Next session in any harness reads this and resumes.

## Teams

**Q: What's a "team pack"?**
A pre-defined multi-agent configuration with role assignments. Activate via `/zeref-os:team [type]`. Max 4 agents. Outputs land in `team/`. See [Team Packs](Team-Packs).

**Q: Are team agents always running?**
No. On-demand only. After `/zeref-os:team build` completes, you're back to `solo`.

**Q: Can I run multiple teams in parallel?**
No. One team active at a time. The current team is tracked in `memory/MEMORY.md` `## Active team` section.

## Patterns + skills

**Q: How does pattern detection work?**
`pattern-observer` scans `memory/patterns/PATTERNS.jsonl` over a 48–80h rolling window. If 3+ similar events (Jaccard ≥ 0.8) cluster, a skill draft is proposed. See [Pattern Detection](Pattern-Detection).

**Q: Will it auto-create skills?**
No. Never. Drafts land in `skills/drafts/` for review via `/zeref-os:review-skill`.

**Q: What's the Two-Strikes Rule?**
Never codify a rule on the first occurrence of an error. Log it in MEMORY.md first. If a similar error occurs again within 30 days, then promote it to a rule. Prevents rule bloat. See [Glossary](Glossary).

## Versioning

**Q: Why does v1.0.0 come after v4.3?**
The plugin was renamed (`zeref` → `zeref-os`) and rebranded. The version clock reset to mark the canonical release. Full iteration history preserved in [Versioning History](Versioning-History) and `CHANGELOG-LEGACY.md`.

**Q: Did older tags work?**
Pre-v4 tags fail under the current Claude Code plugin schema (documented in `CHANGELOG-LEGACY.md`). v4.0–v4.3 tags worked but were deleted at v1.0.0 cutover per user directive: "all working versions exist in tags" — and v1.0.0 is now that single tag.

**Q: What about upgrading from a pre-1.0 install?**
See [`MIGRATION.md`](https://github.com/kanadhiayash/zeref-os/blob/main/MIGRATION.md). Mostly: just reinstall under the new name. No data migration required.

## Troubleshooting

**Q: Validator fails with "missing memory dir: memory/logs"**
You're on a pre-v1.0.0 install. Either pull the latest validator from main, or run `scripts/migrate-v4.2-to-v4.3.py --apply`.

**Q: Skills/commands not surfacing in Claude Code**
Restart Claude Code after install. Slash commands appear under `/zeref-os:`. Skills surface as `zeref-os:<name>` via the Skill tool.

**Q: Old `zeref@zeref` install still active**
Uninstall it: `claude plugin uninstall zeref@zeref`. Then install the new one: `claude plugin install zeref-os@zeref-os`.

**Q: GitHub Wiki shows 404**
Owner needs to enable Wikis in Settings → Features. Then push the wiki content from `docs/wiki/` to `<owner>/<repo>.wiki.git`.
