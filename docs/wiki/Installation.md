# Installation

Zeref OS works in any harness that reads markdown. The fastest path is Claude Code; every other harness is a thin stub pointing at `AGENTS.md`.

## Claude Code (CLI)

```bash
claude plugin marketplace add kanadhiayash/zeref-os
claude plugin install zeref-os@zeref-os
```

Restart Claude Code. Skills surface as `zeref-os:<skill-name>`. Commands as `/zeref-os:<command>`.

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
```

Aider reads `AGENTS.md` natively and `.aider.conf.yml` for harness-specific behavior.

## Codex / Gemini CLI / Antigravity / Hermes / Amp / Zed / Perplexity Computer

These read `AGENTS.md` natively.

```bash
git clone https://github.com/kanadhiayash/zeref-os.git .zeref
# Point your harness at .zeref/AGENTS.md
```

Optional: copy the relevant harness stub to project root (`GEMINI.md`, `CLAUDE.md`).

## First-time setup (any harness)

```
/zeref-os:start
```
(or `/start` if your harness namespaces slash commands automatically)

This triggers the `project-setup` interview. ~5 min. Writes:

| File | Purpose |
|---|---|
| `config/PROJECT.md` | what / why / scope |
| `PRIVACY.md` | mode (default `abstract`) |
| `REDACT.md` | sensitive classes |
| `SHARING_POLICY.md` | connector allowlist (default all OFF) |
| `config/PERMISSIONS.md` | filesystem / network / shell |
| `config/PARENT_SYNC.md` | parent project rollup (default disabled) |
| `config/BUDGET.md` | token budget tier |

Re-run `/zeref-os:start` after to boot the session.

## Verify

```bash
python3 .zeref/scripts/zeref-validate.py
```

Expected:
```
Zeref OS validator — /path/to/project
Skills:           10/10
Agents:            6/6
Commands:          8/8
Team packs:        6/6
Config:            5/5
Root privacy:      3/3 (PRIVACY, REDACT, SHARING_POLICY)
v4x canon:         6/6
Harness stubs:     3/3
Memory layout:    flat
✔ Validation passed
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| `/zeref-os:start` not recognized | Restart Claude Code after install; check plugin enabled |
| "Wikis are disabled" on GitHub | Owner enables Wikis in Settings → Features |
| Validator errors on `memory/` dirs | Run `scripts/migrate-v4.2-to-v4.3.py --apply` if upgrading from pre-1.0 |
| Old `zeref@zeref` install still active | Uninstall it: `claude plugin uninstall zeref@zeref` |
| Connector requests rejected | Check `SHARING_POLICY.md` — all connectors OFF by default |

## Uninstall

```bash
claude plugin uninstall zeref-os@zeref-os
claude plugin marketplace remove zeref-os
```

Your `memory/` directory is local data — preserved unless you delete it.
