# ZEREF_AUDIT_BASELINE.md

> Canonical baseline for the Repository-Wide Consistency Audit. Every finding, count, and verdict in the sibling audit artifacts binds to this exact commit and environment. If any of these values change during the audit, the audit stops and re-baselines per handoff §"Stop Conditions".

## Repository state

| Field | Value |
|---|---|
| Remote | `https://github.com/kanadhiayash/zeref-memory-engine.git` (`origin`, fetch = push) |
| Default branch (remote) | `main` |
| Integration branch (remote) | `dev` @ `0507555c619df504873b8b8910391fda90aa167b` |
| Audit branch | `claude/zeref-consistency-audit-ed392b` |
| Baseline HEAD | `b82c6410bf17b1bc4d1c79227c3a55e075858ab9` |
| Latest tags | `v2.6.1`, `v2.6.0` |
| Working tree | clean |
| Uncommitted changes | none |

## Environment

| Field | Value |
|---|---|
| Platform | `Darwin 25.3.0` (macOS) |
| Shell | `zsh` |
| Python | `3.14.4` (project claims support for 3.11 / 3.12 only — see finding candidate) |
| Worktree path | `<repo>/.claude/worktrees/zeref-consistency-audit-ed392b` (path abstracted per REDACT.md `internal_paths`) |

## Validation tools available at baseline

| Tool | Purpose | Notes |
|---|---|---|
| `git` | state introspection | in-scope per `config/PERMISSIONS.md` allow-list |
| `rg` | grep | evidence gathering |
| `python3` | runtime + validators | 3.14.4 exceeds documented range |
| `jq` | JSON structural checks | available |
| `pytest` | unit tests | `pytest.ini` present at repo root |
| `zeref` (CLI) | in-repo product | `[project.scripts] zeref = "zeref.cli:main"` |
| `python3 scripts/zeref-validate.py` | structural validator | to be verified in WS-B |
| `python3 scripts/check-version-consistency.py` | version drift check | to be verified in WS-F |
| `actionlint` | GitHub Actions linter | availability to be probed in WS-F |

## Derived counts at baseline (never copied from docs)

Every subsequent audit statement compares documented counts to these values. All counts derived via `find`/`git ls-files` on baseline SHA.

| Component | Count | Command used |
|---|---|---|
| Agents (`agents/*.md`) | **6** | `find agents -maxdepth 1 -type f -name '*.md' \| wc -l` |
| Skill packages (`skills/*/SKILL.md`) | **15** | `find skills -mindepth 2 -maxdepth 2 -type f -name 'SKILL.md' \| wc -l` |
| Slash-command files (`commands/*.md`) | **8** | `find commands -maxdepth 1 -type f -name '*.md' \| wc -l` |
| Team packs (`team-packs/*.md`) | **9** | `find team-packs -type f -name '*.md' \| wc -l` |
| Benchmark modules (`benchmarks/*.py`) | **28** | `find benchmarks -maxdepth 1 -type f -name '*.py' \| wc -l` |
| CI workflow files (`.github/workflows/*`) | **5** | `find .github/workflows -type f \| wc -l` |
| Tracked files (repo total) | **286** | `git ls-files \| wc -l` |

## Version surfaces at baseline (facts, not verdicts)

| Surface | Value | Source |
|---|---|---|
| `zeref/VERSION` | `1.0.0` | file contents |
| `pyproject.toml` `[project].version` | `1.0.0` | pyproject.toml:9 |
| `pyproject.toml` `[project].name` | `zeref-os` | pyproject.toml:7 |
| `.claude-plugin/plugin.json` `name` | `zeref-os` | plugin.json:2 |
| `.claude-plugin/plugin.json` `version` | `1.0.0` | plugin.json:3 |
| `.claude-plugin/marketplace.json` `name` | `zeref-os` | marketplace.json:3 |
| `zeref-registry.json` `version` | `1.0.0` | registry.json:3 |
| `SKILL.md` frontmatter `name` | `zeref-os` | SKILL.md:2 |
| `SKILL.md` frontmatter `version` | `1.0.0` | SKILL.md:3 |
| CHANGELOG top entry | `[1.0.0] — 2026-06-19` | CHANGELOG.md:8 |
| README display name | `Zeref Memory Engine (legacy: Zeref OS)` | README.md |
| Git tags on `main` | `v2.6.1`, `v2.6.0` | `git tag` |

## Identity surfaces at baseline (facts, not verdicts)

| Identity slot | Value |
|---|---|
| Repository name | `zeref-memory-engine` |
| Python package `[project].name` | `zeref-os` |
| Python import name | `zeref` |
| CLI executable | `zeref` |
| Claude plugin name | `zeref-os` |
| Claude marketplace name | `zeref-os` |
| Skill namespace | `zeref-os:*` |
| Slash-command namespace | `/zeref-os:*` |
| Documentation display name (README) | `Zeref Memory Engine` |
| Documentation display name (AGENTS.md) | `Zeref` (short) / `Zeref Memory Engine` (long) |
| Legacy alias documented | `Zeref OS` |
| Prior-audit proposed alias | `zeref-me` — **not adopted; treated as claim to test** |

## Boot-order fact set (AGENTS.md §0 / CLAUDE.md)

The documented boot reading order references files whose existence must be verified against the baseline. Presence at HEAD `b82c641`:

| Step | Path | Present at baseline |
|---|---|---|
| 0 | `SOUL.md` | **NO** — file does not exist at repo root |
| 1 | `config/PROJECT.md` | yes — but contains an absolute filesystem path in `project_root` field |
| 2 | `memory/hot.md` | no — populated by `zeref init` on user machines |
| 3 | `memory/index.md` | no — populated by `zeref init` on user machines |
| 4a | `PRIVACY.md` | yes |
| 4b | `REDACT.md` | yes |
| 4c | `SHARING_POLICY.md` | yes |
| 5 | `_shared/rules.md` | to be verified in WS-A |
| 6 | `memory/MEMORY.md` | no — populated by `zeref init` on user machines |
| 7 | `memory/patterns/PATTERNS.jsonl` | no — directory does not exist at baseline |

Interpretation is deferred to the workstream reports; the fact set above is baseline evidence only.

## Immediate seed observations (candidate findings only — pending workstream verification)

Recorded here so subsequent workstreams inherit them without re-derivation. Severity assignments in this section are provisional.

1. `SOUL.md` referenced as boot step 0 by [AGENTS.md](../../AGENTS.md) and [CLAUDE.md](../../CLAUDE.md) is not present at HEAD. Prior audit flagged this; re-verification confirms absence.
2. `config/PROJECT.md:3` contains an absolute filesystem path (`/Users/<name>/...`) in the tracked `project_root` field, contradicting `REDACT.md` `internal_paths.enabled: true`.
3. `pyproject.toml` `requires-python = ">=3.11"` with 3.11/3.12 classifiers, but the audit host runs 3.14.4. WS-F must determine whether CI covers 3.14.
4. `.claude-plugin/plugin.json.description` still describes the product as "Zeref Memory Engine (legacy: Zeref OS)" while `name` remains `zeref-os` — the compatibility-identifier contract is documented (AGENTS.md naming note) but not centrally decided.
5. Latest git tags (`v2.6.1`, `v2.6.0`) exceed every declared version surface (`1.0.0`). CHANGELOG frames `1.0.0` as a "trust-repair pivot" that carries the v2.6.x architecture forward. Reconciliation deferred to WS-F + Phase 5 council.

## Non-negotiables in effect for this audit

Inherited from user handoff verbatim. Auditors and reconcilers may not relax them:

1. Read before edit; product code untouched.
2. No reset / clean / force-push / publish / tag / release / deploy.
3. Audit artifacts land only under `docs/audits/` (plus documented extension surfaces `team-packs/` and `skills/imported/` for the fleet setup phase).
4. Facts / Assumptions / Unknowns / Risks kept separate in every finding.
5. Every count derived, never copied.
6. No harness marked "verified" unless the host actually executed the code path.
7. No credential / private path printed in full — redact in artifacts.
8. Historical files classified `active-truth | compatibility | historical | superseded | archive-candidate`.
9. Prior findings assigned `verified | partially-verified | rejected | superseded | unable-to-verify`.
10. Stop and report on any of the seven handoff stop conditions.

## Stop-condition monitors (armed at baseline)

The audit halts and reports rather than proceeding when any of these fire. Each is checked at every workstream boundary.

- Working tree not clean.
- A test would require destructive changes.
- Network-dependent verification lacks approval (approval scope for this audit: local `mktemp` venv + PyPI + GitHub read only).
- A security finding would be exposed publicly.
- A benchmark requires an unavailable private fixture.
- Repository state changes during the audit (`git rev-parse HEAD` diverges from baseline).
- Evidence cannot support a confident conclusion.

---

Baseline sealed. Every subsequent artifact under `docs/audits/` is bound to commit `b82c6410bf17b1bc4d1c79227c3a55e075858ab9`.
