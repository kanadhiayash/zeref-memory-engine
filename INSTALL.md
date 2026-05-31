# Install Zeref 4.3

## Claude Code (CLI)

```bash
claude plugin marketplace add kanadhiayash/zeref-os
claude plugin install zeref@zeref
```

Restart Claude Code. Skills available as `zeref:<skill-name>`. Commands available as `/zeref:<command>`.

## Codex / Gemini CLI / Antigravity / Hermes / Amp / Zed / Perplexity Computer

These harnesses read `AGENTS.md` natively (per ZEREF_OS §10).

1. Clone the repo into your project:
   ```bash
   git clone https://github.com/kanadhiayash/zeref-os.git .zeref
   ```
2. Point your harness at `.zeref/AGENTS.md` as the canonical agent spec.
3. (Optional) Symlink the relevant harness stub to your project root:
   - Gemini → `.zeref/GEMINI.md`
   - Claude → `.zeref/CLAUDE.md`

## Cursor

```bash
git clone https://github.com/kanadhiayash/zeref-os.git .zeref
mkdir -p .cursor/rules
cp .zeref/.cursor/rules/zeref.mdc .cursor/rules/
```

Cursor auto-loads `.cursor/rules/zeref.mdc` which points to `.zeref/AGENTS.md`.

## Windsurf

```bash
git clone https://github.com/kanadhiayash/zeref-os.git .zeref
cp .zeref/.windsurfrules .
```

Windsurf auto-loads `.windsurfrules` at project root.

## Aider

```bash
git clone https://github.com/kanadhiayash/zeref-os.git .zeref
cp .zeref/.aider.conf.yml.example .aider.conf.yml
# Edit .aider.conf.yml as needed
```

Aider reads `AGENTS.md` natively and `.aider.conf.yml` for harness-specific behavior.

## First-time setup (any harness)

In any new project:
```
/start
```

Triggers the `project-setup` interview. ~5 min. Writes:
- `config/PROJECT.md`
- `PRIVACY.md` (root)
- `REDACT.md` (root)
- `SHARING_POLICY.md` (root)
- `config/PERMISSIONS.md`
- `config/PARENT_SYNC.md`
- `config/BUDGET.md`

Re-run `/start` after to boot the session. Default privacy mode is **abstract**; default connectors are **all OFF**.

## Verify

```bash
python3 .zeref/scripts/zeref-validate-v4.py
```

Expect:
```
✔ Validation passed
Skills: 10/10
Agents: 6/6
Commands: 8/8
Team packs: 6/6
Privacy templates: 3/3 (PRIVACY, REDACT, SHARING_POLICY)
Memory layout: flat (v4.3)
```

## Migrate from earlier Zeref versions

```bash
# From v3 (CEO persona / fleet framing)
python3 .zeref/scripts/migrate-v3-to-v4.py --from /path/to/v3-project/wiki --to ./memory

# From v4.0 / v4.1 / v4.2 (nested memory/wiki/ layout, config/PRIVACY.md)
python3 .zeref/scripts/migrate-v4.2-to-v4.3.py            # dry-run
python3 .zeref/scripts/migrate-v4.2-to-v4.3.py --apply    # actual migration
```

The v4.2 → v4.3 script:
- Snapshots `memory/` to `memory/snapshots/pre-v4.3-<iso>/` for rollback
- Moves `memory/wiki/*` → flat `memory/`
- Renames `memory/wiki/ARCHIVE/` → `memory/archive/` (lowercase)
- Archives `memory/logs/session-events.jsonl` → `memory/archive/session-events-v4.2.jsonl`
- Creates `memory/patterns/PATTERNS.jsonl` with cutover marker
- Creates `memory/hot.md` + `memory/MEMORY.md` scaffolds
- Archives `config/PRIVACY.md` → `memory/archive/` (root `PRIVACY.md` is authored separately)
- Uses `git mv` to preserve history
- Idempotent: safe to re-run

See `MIGRATION.md` for full details.

## Uninstall

```bash
claude plugin uninstall zeref@zeref
claude plugin marketplace remove zeref
```

Your `memory/` directory is local data — preserved unless you delete it.
