<!-- privacy-audit: allow-file "Migration doc contains example paths + install commands as documentation of the process." -->

# Migration: Zeref v3 → v4

## TL;DR

v4 is a clean philosophical reset. The 109 v3 specialist skills, CEO/fleet/council framing, Yash-specific identity, and `ZEREF.md`/`ZEREFOS.md`/`ZEREFPROJECT.md` stack are all gone. v4 is a pure context + memory engine.

v3 is frozen at git tag `v3.0.0-frozen` for archive.

## Why

v3 had become a theatrical multi-agent operating system. v4 returns to first principles:
- Local-first markdown memory
- Harness-agnostic (Claude / Codex / Gemini / any)
- Model-agnostic
- Privacy-first
- Human arbitration (no silent conflict resolution)
- Progressive activation (small default, optional power)

## What's gone

- 109 specialist skills (`zeref-biz-*`, `zeref-cnt-*`, `zeref-dev-*`, `zeref-mkt-*`, `zeref-qa-*`, `zeref-ux-*`, `zeref-hq-*`, `zeref-final-*`)
- `zeref-fleet-router`, `zeref-council-convener`, `zeref-executive-qa-agent`, `zeref-release-governor`, `zeref-context-engine` agents
- `commands/zeref-*` (14 commands)
- `ZEREF.md`, `ZEREFOS.md`, `ZEREFPROJECT.md`
- `registry/zeref-skill-registry.json`
- `output-styles/zeref-executive.md`
- All CEO / Yash-specific / Ruflo / council framing

## What's renamed

| v3 | v4 |
|---|---|
| `agents/zeref-memory-keeper.md` | `agents/memory-keeper.md` |
| `agents/zeref-trust-sentinel.md` | `agents/privacy-guardian.md` |
| `agents/zeref-evaluator.md` | `agents/evidence-curator.md` |
| `wiki/hot.md` | `memory/wiki/INDEX.md` (entries) + `memory/wiki/ARCHIVE/hot-<iso>.md` |
| `wiki/log.md` | `memory/logs/session-events.jsonl` |
| `wiki/index.md` | `memory/wiki/INDEX.md` |
| `/zeref-activate` | `/start` |
| `/zeref-save` | `/done` |
| `/zeref-orient` | (folded into `/start` boot) |
| `/zeref-recall` | (folded into `memory-keeper` READ op) |

## What's new

- `config/` (5 files): PROJECT, PRIVACY, PERMISSIONS, PARENT_SYNC, BUDGET
- `memory/` scaffold: raw, wiki, logs, snapshots, sync/{outbound,parent}
- `AGENTS.md` canonical spec (addyosmani convention)
- `GEMINI.md` harness shim
- 10 disciplined skills (down from 109)
- 6 disciplined agents (down from 8)
- 7 commands (down from 14)
- Append-only `session-events.jsonl` event log
- Snapshot system
- Parent sync mechanism (M2 in v4.1.0)
- Pattern-to-skill detection (M3 in v4.2.0)

## How to migrate your data

```bash
# 1. Back up your v3 wiki first
cp -r /path/to/v3-project/wiki ~/zeref-v3-backup-$(date +%Y%m%d)

# 2. Install Zeref Memory Engine (compat identifier retained per D2)
claude plugin install zeref-os@zeref-os

# 3. Run migration script
python3 scripts/migrate-v3-to-v4.py --from /path/to/v3-project/wiki --to ./memory

# 4. Run /start in a fresh session
# Interview will guide you through the new config/ files
```

## Backward compatibility

None. v4 is a clean break. Run `/start` and re-enter project context — it takes ~5 min and produces a much more disciplined state.

## Roadmap

- **v4.0 (M1, ships now)**: core engine
- **v4.1 (M2)**: full contradiction-resolution + parent-sync (currently stubs)
- **v4.2 (M3)**: pattern-observer + pattern-to-skill (currently stubs)
- **v4.3 (M4)**: v4.x canon import + flat memory layout + team packs + harness translation map + Two-Strikes Rule

---

# Migration: Zeref v4.2 → v4.3

## TL;DR

v4.3 aligns the file layout with the canonical v4.x spec (ZEREF_OS §12). Memory goes flat (no more `memory/wiki/`), privacy templates move to project root, and the event log gets renamed.

Use `scripts/migrate-v4.2-to-v4.3.py`. It is idempotent and uses `git mv` to preserve history.

## What's renamed (paths)

| v4.2 path | v4.3 path |
|---|---|
| `memory/wiki/INDEX.md` | `memory/index.md` |
| `memory/wiki/DECISIONS.md` | `memory/DECISIONS.md` |
| `memory/wiki/OPEN_QUESTIONS.md` | `memory/OPEN_QUESTIONS.md` |
| `memory/wiki/RISKS.md` | `memory/RISKS.md` |
| `memory/wiki/CONFLICTS.md` | `memory/CONFLICTS.md` |
| `memory/wiki/ARCHIVE/` | `memory/archive/` *(lowercase)* |
| `memory/logs/session-events.jsonl` | `memory/archive/session-events-v4.2.jsonl` + new `memory/patterns/PATTERNS.jsonl` |
| `config/PRIVACY.md` | root `PRIVACY.md` + archived original |
| `skills/_drafts/` *(never created)* | `skills/drafts/` |

## What's new

- **Root privacy templates** (per ZEREF_OS §4.1):
  - `PRIVACY.md` — modes (default `abstract`)
  - `REDACT.md` — concrete sensitive classes
  - `SHARING_POLICY.md` — per-connector allowlist (all OFF)
- **`memory/hot.md`** — last 3 sessions, ≤500 words, read FIRST per §0
- **`memory/MEMORY.md`** — agent-written session notes per §3.4
- **`memory/patterns/PATTERNS.jsonl`** — append-only tool/event log per §3.5
- **Team packs** (per §8) — `team-packs/{solo,build,research,red,audit,ship}.md` + `/team` command
- **Cross-harness stubs** (per §10) — `.cursor/rules/zeref.mdc`, `.windsurfrules`, `.aider.conf.yml.example`
- **Canon imports** — `references/v4x-canon/` (ZEREF_OS, DECISION_LOG, MODEL_DEBATE, USE_CASES, RESEARCH_RESOURCES, PACKAGE_INDEX)
- **Codified rules** — `references/two-strikes-rule.md`, `references/connector-advisory.md`, `references/harness-translation-map.md`
- **Claude overrides** — `config/claude-overrides.md`

## How to migrate

```bash
# 1. Back up first (the script also snapshots, but belt-and-suspenders)
cp -r memory ~/zeref-v4.2-backup-$(date +%Y%m%d)

# 2. Dry-run
python3 scripts/migrate-v4.2-to-v4.3.py

# 3. Apply
python3 scripts/migrate-v4.2-to-v4.3.py --apply

# 4. Verify
python3 scripts/zeref-validate.py
git status   # confirm git mv preserved history (look for "R" lines)
```

## Reading order changes (per ZEREF_OS §0)

`/start` now loads in this order:
1. `memory/hot.md` (≤500 words)
2. `memory/index.md` (if hot insufficient)
3. `PRIVACY.md` (root) before any write or tool use
4. `REDACT.md` (root) before any external output
5. `memory/MEMORY.md` first 200 lines
6. Tail of `memory/patterns/PATTERNS.jsonl`

## Backward compatibility

The migration is one-way for path nomenclature. The pre-migration snapshot lives in `memory/snapshots/pre-v4.3-<iso>/` for rollback. Original `config/PRIVACY.md` and `memory/logs/session-events.jsonl` are archived in `memory/archive/` (never hard-deleted per D9).

After migration, run `/start` to boot under the new layout. The existing wiki content carries over unchanged — only paths and reading order change.

---

# Migration: Zeref v1.x → 2.0.0-alpha.1

## TL;DR

2.0.0-alpha.1 is a breaking architectural pivot, not a minor patch — the vNext architecture reset (PR 1 of `ZEREF_VNEXT_AGENTIC_OPERATIONS_UPGRADE_PLAN.md`). The FAANG-MANGOES council is removed with no replacement in this PR. Provider model ids are no longer canonical anywhere except `zeref/adapters/providers/`. Old tier/policy/component names still work through a one-cycle alias layer, but should be migrated now — the alias layer is removed in 2.1.0.

## What's gone

- **FAANG-MANGOES council** — `team-packs/faang-mangoes-council.md`, its registry entry, and all references in `SOUL.md` / imported-skill READMEs. No alias. See `docs/adr/ADR-0003-council-removal.md` and `docs/archive/faang-mangoes-council-removal.md`.
- Anthropic-specific model names as canonical fields anywhere outside `zeref/adapters/providers/`.

## Alias table (works now, removed in 2.1.0)

| Old name | New name | Category |
|---|---|---|
| `small` | `lean` | execution-policy |
| `medium` | `balanced` | execution-policy |
| `enterprise` | `assured` | execution-policy |
| `skill-router` | `capability-resolver` | component |
| `fleet-activator` | `capability-prober` | component |
| `skill-importer` | `capability-manager` | component |
| `haiku` | `fast` | reasoning-class |
| `sonnet` | `balanced` | reasoning-class |
| `opus` | `deep` | reasoning-class |

Full detail, including the `resolve_alias()` mechanism and what is *not* aliased: `docs/DEPRECATIONS.md`.

## Registry field changes

`zeref-registry.json` skill entries: `model` / `model_alias` fields are replaced by:

- `reasoning_class` — one of `fast`, `balanced`, `deep`, `frontier`, `local`, `private`. See `docs/GLOSSARY.md`.
- `status` — one of `runtime` (executing, tested code) or `contract` (schema/spec, not yet runtime-backed). See the "Component status taxonomy" section of `docs/audits/ZEREF_COMPONENT_INVENTORY.md`.

Registry version is now `2.0.0-alpha.1`.

## Where model pins moved

Concrete provider model ids (which model backs `deep`, `frontier`, etc.) moved out of core code, the registry, and mission/skill files entirely. They now live only in `zeref/adapters/providers/<provider>.json` (e.g. `anthropic.json`, `openai.json`), resolved through `zeref.adapters.providers.resolve_model()`. If you had a script or config pinning a model id directly, point it at the provider adapter file instead — do not reintroduce a hardcoded model id elsewhere.

## How to migrate

1. Read `docs/DEPRECATIONS.md` and replace old names (`small`/`medium`/`enterprise`, `skill-router`/`fleet-activator`/`skill-importer`, `haiku`/`sonnet`/`opus`) in your own configs, scripts, and docs. The alias layer keeps them working meanwhile, but each resolution emits a one-time `DeprecationWarning`.
2. If anything referenced `team-packs/faang-mangoes-council.md` or `docs/audits/council/`, remove that reference — there is no replacement in this PR. An optional evaluator-adapter replacement is planned for a later PR (§11 of the architecture plan) and remains experimental until benchmarked.
3. If anything read `model`/`model_alias` off registry entries, switch to `reasoning_class` + `status`.
4. Re-run `python3 scripts/zeref-validate.py` to confirm registry and frontmatter consistency after migrating.

## Backward compatibility

Partial. Name aliasing works through 2.0.x and is removed in 2.1.0. Council removal and the provider-model-id relocation have no compatibility shim — they are hard breaks effective immediately in 2.0.0-alpha.1.

## Roadmap

Team-pack file renames (`team-packs/small.md` → `lean.md`, etc.) and the full `team-packs/*.md` → `missions/*.yaml` restructure are **not** part of this PR — they land with the missions PR (PR 6) per the architecture plan §5.1 and §20. The alias layer above resolves names today; it does not move files.
