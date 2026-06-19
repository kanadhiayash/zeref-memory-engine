# Changelog — Zeref OS

All notable changes to **Zeref OS** are documented here.

Versioning: [Semantic Versioning](https://semver.org/) — `MAJOR.MINOR.PATCH`.

---

## [1.0.0] — 2026-06-19

Public launch. Trust-repair pivot — single source of truth for the active
version, operationally verified guarantees on every public surface. The
v2.6.x architecture (4-gate Auto-Activation, 14 skills, 6 agents,
R6 Zero Context Loss, three privacy modes, flat memory layout) is carried
forward unchanged. Pre-v1 history is archived to
`kanadhiayash/zeref-os-archive` — see [`docs/PIVOT_LOG.md`](docs/PIVOT_LOG.md).

### Added

- **`zeref/VERSION`** — single source of truth for the active version.
  `zeref/__init__.py`, `zeref/cli.py`, `pyproject.toml`,
  `zeref-registry.json`, `.claude-plugin/plugin.json`, README badge, wiki
  installation copy, and `docs/RELEASE_LOG.md` all align with this file.
- **`scripts/check-version-consistency.py`** — fails CI on any drift
  between version surfaces.
- **`tests/`** — reproducible pytest suite covering version consistency,
  privacy redaction (positive + negative cases for every supported
  pattern), CLI contract, init scaffold, write-decision round-trip,
  db-status surface, and the structural validator. Coverage target on
  `zeref/` is ≥85%; CI publishes the coverage report.
- **11 expanded privacy patterns** in `zeref/privacy.py`:
  - `sk-proj-…` (OpenAI project keys)
  - bare `sk-…` provider-shaped tokens
  - `github_pat_…`, `ghp_…` (GitHub PATs)
  - `xoxb-…` (Slack bot tokens)
  - `AIza…` (Google API keys)
  - `AKIA…` (AWS access key IDs)
  - PEM private-key blocks (`-----BEGIN … PRIVATE KEY-----`)
  - natural-language `API key <token>`, `secret key <token>`,
    `access token <token>`
- **`zeref audit-privacy --strict`** — exits non-zero on any unredacted
  hit, suitable for CI gates.
- **`SECURITY.md` rewrite** — vulnerabilities now route through GitHub
  Private Vulnerability Reporting plus a PGP-encrypted fallback contact;
  no public-issue disclosure path. See also new
  `SECURITY_CONTACTS.md`.
- **CI hardening** — every GitHub Action pinned to its full commit SHA
  with a human-readable tag comment; `.github/dependabot.yml` refreshes
  pins weekly. New workflows: `test.yml` (pytest matrix),
  `privacy-audit.yml` (strict scrub on PR), `version-consistency.yml`,
  `branch-retention.yml`.
- **Portability layer** — `scripts/harness-probe.py` detects the host
  harness and validates required-tool surface; new
  `docs/HARNESS_MATRIX.md` documents the install + smoke-test result
  per harness.
- **Adaptivity layer** — `skills/skill-importer/` pulls a skill from the
  user's broader skill directory into the project with provenance
  metadata; `skill-router` ranks candidates by trigger match + recency.
- **Scalability layer** — `team-packs/small.md`, `medium.md`,
  `enterprise.md` encode token / credit envelopes per team size;
  `budget-governor` enforces the envelope.
- **`benchmarks/`** — four-axis harness (portability, adaptivity,
  scalability, trust) with public rubric in `benchmarks/RUBRIC.md`;
  `benchmarks/run-all.py` produces `docs/BENCHMARK_REPORT.md` and
  machine-readable `benchmarks/results.json`.
- **`docs/PIVOT_LOG.md`** — full pre-v1 design lineage (Pivot 1 → 4).
- **`docs/RISK_LOG.md`** — accepted risks for the v1.0.0 launch.

### Changed

- All version surfaces aligned on `1.0.0` (was: `pyproject.toml` 2.0.0,
  `__init__.py` 2.0.0, plugin manifest 1.0.0, README 2.6.1,
  registry 2.6.1-phaseD).
- `zeref-registry.json` `version` and `generated` fields refreshed.
- `README.md` reframed for public launch; install matrix unchanged.
- `docs/RELEASE_LOG.md` rewritten with v1.0.0 as the first public release;
  pre-v1 tags listed as archived.

### Architecture (carried forward unchanged from v2.6.1)

- 6 background agents.
- 14 disciplined skills with strict triggers.
- 4-gate Auto-Activation chain (budget → router → fleet → prompt).
- R6 Zero Context Loss invariant.
- 6 on-demand team packs (now extended with size variants).
- Three privacy modes (default `abstract`).
- Flat per-project markdown memory layout.

### Removed

- Public-issue route for security disclosures (now private only).
- Moving-major-tag GitHub Action references (now SHA-pinned).
- Stale `2.0.0` / `2.6.1-phaseD` strings in version surfaces.

### Migration from v2.6.1

No data migration required. `memory/`, `PRIVACY.md`, `REDACT.md`,
`SHARING_POLICY.md`, `config/` keep their paths. Reinstall the plugin to
pick up v1.0.0:

```bash
claude plugin uninstall zeref-os@zeref-os
claude plugin marketplace add kanadhiayash/zeref-os
claude plugin install zeref-os@zeref-os
claude plugin list | grep "zeref-os.*1.0.0"
```

If you need to stay on v2.6.1, install from the archive repo
`kanadhiayash/zeref-os-archive` (branch `legacy/v2.6.1`).

---

## Pre-v1.0.0 history (archived)

The entries below describe the v2.6.x line that preceded the v1.0.0
public launch. The corresponding git history lives in
`kanadhiayash/zeref-os-archive`.

---

## [2.6.1] — 2026-06-08

Polish release on top of v2.6.0. Hardens the four Auto-Activation Gates with
code-backed enforcement, normalizes model identifiers across the pack, and
extends R6 (Zero Context Loss) coverage.

### Added

- **Model resolver** (`_shared/model-resolver.md`) — canonical Anthropic id
  mapping (`claude-haiku-4-5-20251001`, `claude-sonnet-4-6`, `claude-opus-4-7`)
  + aliases. Single source of truth for tier → model id.
- **Event-schema validator** — eleven known event types with required and
  optional payload keys; rejects unknown events at validate time.
- **Marker-file probe** in `fleet-activator` — per-tool marker file required
  before any external tool is declared reachable.
- **Prompt injection filter** in `prompt-context-engine` — pattern-scans for
  override markers; wraps suspicious content in `<context type="untrusted-input">`.
- **Irreversibility cool-down** in `prompt-context-engine` — 60s window;
  auto-approve allows only read-only / dry-run / draft-to-temp until 90s.
- **NFKC + homoglyph guard** in `caveman-handoff` — normalizes path strings,
  flags non-ASCII and Cyrillic / Greek / fullwidth lookalikes.
- **Dual-key override** in `budget-governor` — single-key override insufficient;
  requires `OVERRIDE: …` plus an `<override-acknowledged>` block. Repeat
  overrides become reclassification candidates.
- **Stack-cap lint** in `skill-router` — validator rejects routes with more
  than five skills active simultaneously.
- **R6 sweep** — Zero Context Loss extended from four to nine SKILL.md files.

### Changed

- `scripts/zeref-validate.py` — skill count read dynamically from registry
  (no hardcode). PATTERNS.jsonl lint reports unknown event types.
- `zeref-registry.json` — model identifiers normalized to full Anthropic ids.

### Removed

- Hardcoded skill counts in the validator.

### Documentation

- `_shared/rules.md` R6 doctrine clarified.
- Wiki Architecture page updated with v2.6 4-gate diagram.

---

## [2.6.0] — 2026-06-08

Major feature release introducing the **4-gate Auto-Activation chain**. Every
major task now self-classifies cost, stack, prompt, and handoff before any
token spend.

### Added

- **skill-router** — declares `[skill-router] domain=<D> lead=<L> support=[…] qa=<Q>`
  inline before every major action. Stack cap five.
- **fleet-activator** — probes external tool reachability and declares
  `[fleet-activator] <tool>: reachable|UNREACHABLE-…` per tool.
- **prompt-context-engine** — classifies prompt as STRUCTURED, AMBIGUOUS, or
  HOSTILE; restructures when needed; declares `[prompt-context-engine] …`.
- **caveman-handoff** — model-tier-aware handoff compression with
  byte-equal-on-decompress invariant.
- **budget-governor** rewrite — gate-style `[budget-governor] weight=… tier=… est=…`
  declaration before any spend, with override grammar.
- **Core Principle 13** — Auto-Activation Gates.
- **Core Principle 14** — R6 Zero Context Loss.

### Changed

- Skills count 10 → 14.
- Every major task surfaces a gate declaration to the user before spend.

### Migration

Additive. No breaking changes from v2.5.x. See `MIGRATION.md`.

---

## Earlier history

Earlier releases (v2.5 and the pre-rebrand line) are not maintained on this
branch. The v2.6 pack is the canonical surface.

---

## Command center

Notion: https://copper-tv-288.notion.site/Zeref-Agent-OS-Command-Center-358d695d836a81af9f6adf30770217c3
