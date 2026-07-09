# Installation

> Product name: **Zeref Memory Engine** (short form: **Zeref**).
> Repo / plugin identifier `zeref-os` is retained for install-URL backward
> compatibility. **Zeref is not an operating system** — it is a persistent
> memory and context layer that plugs into your existing AI harness.

Zeref v1.0.0 installs as a Claude Code plugin. Other harnesses (Cursor, Aider, Windsurf, Gemini, Codex, Llama-family) read AGENTS.md directly via per-harness stubs.

## Claude Code (primary)

### Quick install

```bash
claude plugin marketplace add kanadhiayash/zeref-os
claude plugin install zeref-os@zeref-os
```

The plugin lands at `~/.claude/plugins/cache/zeref-os/zeref-os/`.

### Verify

```bash
claude plugin list | grep zeref-os
# zeref-os@zeref-os  v1.0.0  enabled

cd ~/my-project
claude
> /zeref-os:start
```

Expected output:

```
Project: <name>
Last session: <iso> (or "never" on first run)
Active decisions: <N>
Open questions: <N>
Conflicts: <N>
Privacy mode: abstract
Model tier: Sonnet (auto-detected)
Always-on context: ~3k tokens

What do you want to work on?
```

### Run validator

```bash
cd ~/.claude/plugins/cache/zeref-os/zeref-os
python3 scripts/zeref-validate.py
```

Expected:

```
Zeref OS validator — <plugin path>
Skills:           14/14 (from zeref-registry.json)
Agents:           6/6
Commands:         8/8
Team packs:       6/6
Config:           5/5
Root privacy:     3/3 (PRIVACY, REDACT, SHARING_POLICY)
v4x canon:        6/6
Harness stubs:    3/3
Memory layout:    flat
PATTERNS lint:    0 finding(s)

✔ Validation passed
```

## Other harnesses

Each harness reads its own stub; the stub defers to `AGENTS.md`.

### Codex (native)

Codex reads `AGENTS.md` natively. Just point it at the project root.

### Cursor

Cursor reads `.cursor/rules/zeref.mdc`. The stub instructs Cursor to load `AGENTS.md`.

```bash
ls .cursor/rules/zeref.mdc
```

### Windsurf

Windsurf reads `.windsurfrules`. Same pattern.

### Aider

Aider reads `.aider.conf.yml`. An example is at `.aider.conf.yml.example` — copy + adjust.

```bash
cp .aider.conf.yml.example .aider.conf.yml
```

### Gemini CLI / Antigravity

Reads `GEMINI.md` natively. Defers to `AGENTS.md`.

### Hermes / Amp / Zed / Perplexity

AGENTS.md-native. No additional stub required.

Full table: [`references/harness-translation-map.md`](https://github.com/kanadhiayash/zeref-memory-engine/blob/main/references/harness-translation-map.md).

## Per-project setup

On first `/zeref-os:start` in a fresh project (no `config/PROJECT.md`):

1. `project-setup` skill auto-invokes
2. Interview captures: project name, parent project (optional), privacy mode (default `abstract`), model tier (auto-detect), budget warn-at threshold
3. Writes: `config/PROJECT.md`, `PRIVACY.md`, `REDACT.md`, `SHARING_POLICY.md`, `config/PERMISSIONS.md`, `config/PARENT_SYNC.md` (if parent), `config/BUDGET.md`
4. Prompts re-run `/zeref-os:start` to boot the session

If user cancels mid-interview: Zeref OS boots in **READ-ONLY mode** until the schema completes.

## Optional: install Python runtime

`zeref/` Python runtime provides CLI + structured queries:

```bash
cd ~/.claude/plugins/cache/zeref-os/zeref-os
pip install -e .
python3 -m zeref --help
```

Available commands:

```
zeref status              # print hot.md summary
zeref write-decision      # append to DECISIONS.md (with PII scrub)
zeref grade <claim>       # invoke evidence-grader logic
zeref audit               # structural validation + privacy audit
zeref init                # scaffold memory + config
zeref db-status           # report backend (sqlite/duckdb) + parquet availability
```

## Uninstall

```bash
claude plugin uninstall zeref-os@zeref-os
```

`memory/` and `config/` files in your project remain intact (per R2 non-deletion). To fully purge:

```bash
rm -rf memory/ config/PROJECT.md PRIVACY.md REDACT.md SHARING_POLICY.md
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `unknown event type 'X'` in PATTERNS lint | Custom event type added | Either add to `EVENT_SCHEMA` in `scripts/zeref-validate.py` OR rename event |
| `memory/sync/outbound/handoff-*.md` missing on cross-model handoff | `caveman-handoff` skipped | Confirm `_shared/model-resolver.md` is present + brief diff complete |
| Gate output missing from PATTERNS.jsonl | Agent skipping gates | Validator warning surfaces this advisory; check session for skipped gates |
| Cyrillic-а in path detected, blocking handoff | NFKC + homoglyph guard fired | Replace with ASCII; user confirm if intentional |

## Related

- [[Architecture]] — full system overview
- [[FAQ]] — common questions
- [`AGENTS.md`](https://github.com/kanadhiayash/zeref-memory-engine/blob/main/AGENTS.md) — canonical spec
- [`references/harness-translation-map.md`](https://github.com/kanadhiayash/zeref-memory-engine/blob/main/references/harness-translation-map.md) — per-harness install
- [Notion Command Center](https://copper-tv-288.notion.site/Zeref-Agent-OS-Command-Center-358d695d836a81af9f6adf30770217c3)
