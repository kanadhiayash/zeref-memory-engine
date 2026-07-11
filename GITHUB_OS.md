<!-- privacy-audit: allow-file "Governance spec cites credential-shaped tokens in never-commit list; documents global doctrine paths as documentation." -->

# Zeref OS — Repo Doctrine (per-repo GITHUB_OS)

Per-repo customization of the global `~/Documents/Claude/00_COMMAND/GITHUB_OS.md` doctrine. Global doctrine is the source of truth; this file documents zeref-specific overrides and conventions.

## Source of truth

- **Global**: `~/Documents/Claude/00_COMMAND/GITHUB_OS.md` (Yash GitHub Operating System)
- **Knowledge-OS naming**: `~/Documents/Claude/00_COMMAND/yash_faang_architecture_brief.md` (FAANG brief §Naming convention standard)
- **Canonical spec**: `AGENTS.md` (root of this repo) — Zeref OS behavioral constitution

## Zeref-specific overrides

### Branch naming

Per global GITHUB_OS §3.2: `<type>/zeref__<short-description>`.

Examples:
- `feat/zeref__skill-router-v2`
- `fix/zeref__validator-skills-count`
- `release/v<major>.<minor>` — frozen-baseline snapshot (never receives further commits after creation)

### Tags

Per global GITHUB_OS §3.4: SemVer `v<major>.<minor>.<patch>` on `main` only.

### Commits

Conventional Commits with scope `(zeref)`. Examples:
- `chore(zeref): release v1.0.0`
- `feat(zeref): add prompt-context-engine Gate #3`
- `fix(zeref): validator dynamic skill count from registry`
- `docs(zeref): add R6 Zero Context Loss to _shared/rules.md`
- `ci(zeref): add zeref-validate workflow`

### Required gates before push

1. `python3 scripts/zeref-validate.py` — passes (Skills count matches registry; PATTERNS lint 0)
2. Zeref-scope sweep: every staged file matches allowlist (`AGENTS.md|CHANGELOG|...|scripts/|skills/|team-packs/|tests/|zeref/`); no non-zeref bleed
3. No `--force` to main; no `--no-verify`; no skipping hooks
4. R6 (Zero Context Loss) — `_shared/rules.md#R6` honored across all skill writes
5. Privacy gate — `PRIVACY.md` mode + `REDACT.md` classes enforced before any external transmission

### Model-resolver pinning

Per `_shared/model-resolver.md`: registry uses full Anthropic ids (`claude-haiku-4-5` / `claude-sonnet-4-6` / `claude-opus-4-7`). Bare aliases (`haiku`/`sonnet`/`opus`) accepted via `model_alias` field for back-compat. Cost-sensitive Opus work pins `claude-opus-4-6` (avoids +35% tokenizer inflation of 4.7).

### Memory layer discipline

Per AGENTS.md §0 reading order:
- Every ship cycle includes a `wiki-maintenance` pass before `/stop`
- `memory/{hot.md,index.md,DECISIONS.md,RISKS.md}` refreshed at every release
- `memory/patterns/PATTERNS.jsonl` records session-start + gate events + wiki-writes (validator allowlist enforced)

### Knowledge-OS artifact naming (new files only)

Per FAANG brief: `[scope]_[subject]_[type]_[state]_[owner]_[yyyy-mm-dd]_v[major.minor]`.

Applied to:
- Release log (`docs/RELEASE_LOG.md`): tabular form per row

Existing repo files (SKILL.md, AGENTS.md, CHANGELOG.md, etc.) keep their established Zeref-OS conventions.

### Classification

Per FAANG brief §Classification levels:
- `public`: README.md, CHANGELOG*.md, GitHub Releases, docs/RELEASE_LOG.md, AGENTS.md, SKILL.md, PRIVACY.md/REDACT.md/SHARING_POLICY.md
- `internal`: memory/*, agents/, scripts/, tests/, zeref/, _shared/
- `restricted`: never committed (no credentials / PII / client data)

## Repo-specific paths

- Worktree: `~/Documents/Claude/00_SKILLS/zeref-os/.claude/worktrees/<branch>/`
- Plugin manifest: `.claude-plugin/plugin.json`
- Harness stubs: `CLAUDE.md` / `GEMINI.md` / `.cursor/rules/zeref.mdc` / `.windsurfrules` / `.aider.conf.yml.example`

## Command center

Notion: https://copper-tv-288.notion.site/Zeref-Agent-OS-Command-Center-358d695d836a81af9f6adf30770217c3
