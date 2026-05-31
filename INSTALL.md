# Install Zeref 4.0

## Claude Code (CLI)

```bash
claude plugin marketplace add kanadhiayash/zeref-os
claude plugin install zeref@zeref
```

Restart Claude Code. Skills available as `zeref:<skill-name>`. Commands available as `/zeref:<command>`.

## Codex / Gemini CLI / other harnesses

1. Clone the repo into your project:
   ```bash
   git clone https://github.com/kanadhiayash/zeref-os.git .zeref
   ```
2. Point your harness at `.zeref/AGENTS.md` as the canonical agent spec.
3. (Optional) Symlink `.zeref/CLAUDE.md` or `.zeref/GEMINI.md` to your project root for harness auto-load.

## First-time setup

In any new project:
```
/start
```

Triggers the `project-setup` interview. ~5 min. Writes 5 config files. Re-run `/start` after to boot the session.

## Verify

```bash
python3 .zeref/scripts/zeref-validate-v4.py
```

Expect:
```
✔ Validation passed
Skills: 10/10
Agents: 6/6
Commands: 7/7
Config: 5/5
```

## Migrate from v3

```bash
python3 .zeref/scripts/migrate-v3-to-v4.py --from /path/to/old/wiki --to ./memory
```

See `MIGRATION.md` for what changes.

## Uninstall

```bash
claude plugin uninstall zeref@zeref
claude plugin marketplace remove zeref
```

Your `memory/` directory is local data — preserved unless you delete it.
