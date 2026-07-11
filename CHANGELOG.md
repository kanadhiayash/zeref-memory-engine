# Changelog — Zeref OS

All notable changes to **Zeref OS** are documented here.

Versioning: [Semantic Versioning](https://semver.org/) — `MAJOR.MINOR.PATCH`.

---

## [Unreleased — v1.2.0 canary] — Phases 13-16 (2026-07-11)

Target-model profile system. Ships the loader + inject wrapper + release-check
subcheck + benchmark axis with 2 canary profiles (Claude Opus 4.8, GPT-5.5 Instant).
Full Tier-1 batch (10 remaining profiles) pending; v1.2.0 tag holds until full
batch lands.

### Added
- `skills/imported/system-prompts-leaks/README.md` — reference-only fleet
  boundary + refresh cadence for `github.com/asgeirtj/system_prompts_leaks`
  catalog.
- `references/target-model-profiles/` — YAML profile schema + first 2 profiles
  (`claude-opus-4-8.md`, `gpt-5-5-instant.md`) + `README.md`. Derived summaries
  only; **no source text vendored**.
- `zeref/prompt/target_profile.py` — typed loader (frozen dataclass), schema
  validation, freshness gate, cost helpers, skip-list export. Zero deps.
- `zeref/release/checks.py` — new `target_profiles` subcheck (schema-valid +
  `<=60d` stale). Fail-open when profiles/ absent.
- `benchmarks/token_efficiency.py` — new `target_aware_reduction` sub-axis.
  Canary aggregate: **75% theoretical reduction (Opus 4.8=83%, GPT-5.5=67%)**;
  scores 10/10 against 15% release-gate floor.

### Changed
- `zeref/prompt/inject.py` — `inject_prompt(target, profile_id=None)`
  consults the target profile; emits `_target-profile:<id> — skip: <csv>_`
  preamble line for caveman-handoff to trust. Fail-open when no profile.
- `skills/caveman-handoff/SKILL.md` — new "Target-aware skip lists" section.
  Expected additional 15-30% reduction on Tier-1 targets.
- `_shared/model-resolver.md` — new Target-profile column; rows for
  `claude-opus-4-8` + `gpt-5-5-instant`.

### Council decisions (canary-scoped)
- Inline reconciler synth used for the "ship canary now vs wait for full
  Tier-1" call. Verdict: **canary now** — the runtime plumbing is the
  reusable primitive; remaining Tier-1 profiles are mechanical adds. Full
  12-persona batch deferred to owner opt-in.

### Not shipped in this canary
- Tier-1 profiles 3-12 (10 remaining). Extraction is mechanical against
  the schema in `references/target-model-profiles/README.md`.
- `zeref/memory/cost_router.py` deep integration — kept surgical; callers
  invoke `estimate_input_tokens` / `relative_cost` from the profile module
  directly. Deeper wiring lands with the full Tier-1 batch.
- Empirical (runtime measured) token-reduction numbers — the 75% aggregate
  is theoretical (derived from `already_knows` × 250-token synthetic
  category size vs 3000-token baseline). Real-token measurement lands in
  the Phase-16 v2 pass, after Tier-1 completes.

---

## [1.1.0] — 2026-07-10

Audit remediation release — closes the Repository-Wide Consistency Audit
(`docs/audits/ZEREF_CONSISTENCY_AUDIT.md`) at baseline commit `b82c641`.

### Added

- **`SOUL.md`** — 5 operating principles at repo root; boot step 0 per AGENTS.md §0
  is now fulfilled (ZRF-AUDIT-015).
- **`zeref/security/policy.py`** — typed loaders for PRIVACY.md, REDACT.md,
  SHARING_POLICY.md, config/PERMISSIONS.md; every LLM/network call gates through
  `require_connector` / `require_network` (ZRF-AUDIT-001, 002, 006, 007).
  Session-override lanes: `ZEREF_ALLOW_NETWORK=1`, `ZEREF_ALLOW_CONNECTOR=<csv>`.
- **`zeref-registry.json`** — Registry v1.1 adds `agents[]`, `commands[]`,
  `team_packs[]`, `gates[]` arrays; `skill-importer` registered
  (ZRF-AUDIT-016, 017).
- **`team-packs/faang-mangoes-council.md`** — 12-persona architectural decision
  panel (opt-in only).
- **`skills/imported/{gstack,ecc,mantishack,raptor,hacker-bob}/README.md`** —
  reference-only fleet import boundary docs.
- **`docs/audits/`** — full audit corpus + remediation artifacts.

### Changed

- **`pyproject.toml`** — `build-backend` corrected from
  `setuptools.backends.legacy:build` to `setuptools.build_meta`; `pip install .`
  now works (ZRF-AUDIT-009). Python 3.13 and 3.14 classifiers added.
- **`zeref/privacy.py`** — `audit()` default target = project root; `--strict`
  extends scan to `.py / .json / .yml / .yaml / .toml / .jsonl`; `_SKIP`
  narrowed to `docs/archive` + `tests/fixtures` only (ZRF-AUDIT-005).
- **`zeref/memory/core.py`** — `discover_project_root` prefers
  `config/PROJECT.md`, falls back to `AGENTS.md`; `scaffold_project` no
  longer writes absolute host paths into tracked config
  (ZRF-AUDIT-003, 010).
- **`zeref/cli.py`** — `cmd_init` skips prompts under non-TTY stdin; `cmd_grade`
  now scrubs and gates before LLM egress (ZRF-AUDIT-001, 023).
- **`zeref/lineage/importer.py`** — every `urlopen` gated through security
  policy (ZRF-AUDIT-002).
- **`zeref/release/checks.py`** — 6 → 12 subchecks; SHA-bound evidence blob
  under `docs/audits/release-evidence/` (ZRF-AUDIT-021, R9).
- **`.github/workflows/ci.yml`** — YAML block-collection repaired; SemVer tag
  guard + zeref-scope sweep now execute (ZRF-AUDIT-011).
- **`scripts/check-version-consistency.py`** — also compares against latest git
  tag; documented lineage restart via `docs/PIVOT_LOG.md` marker
  (ZRF-AUDIT-020).
- **`benchmarks/run-all.py`** — trust axis override requires
  `docs/TRUST_AUDIT.md` `Bound-commit-SHA` matching HEAD; else deterministic
  draft published (ZRF-AUDIT-013).
- **`benchmarks/lineage_common.py`** — `_fake_resolver` renamed to
  `_stub_resolver` with explicit conformance-scope note (ZRF-AUDIT-014).
- **`docs/HARNESS_MATRIX.md`** — evidence-state matrix replaces self-attested
  ✅ marks (ZRF-AUDIT-022, D7).
- **`.github/ISSUE_TEMPLATE/{bug_report,feature_request}.md`** — security
  redirect banner added (ZRF-AUDIT-026). `config.yml` URL corrected to
  `kanadhiayash/zeref-memory-engine` (ZRF-AUDIT-028).
- Multiple doc drift fixes across `QUICKSTART.md`, `MIGRATION.md`,
  `docs/HARDENING_OVERVIEW.md`, `docs/wiki/Home.md`, `AGENTS.md`,
  `commands/{start,status}.md`, `benchmarks/run-all.py` docstring, and
  `pyproject.toml` classifiers.

### Fixed

- Two absolute-path leaks: `config/PROJECT.md`, `references/shared-anti-hallucination.md`
  (ZRF-AUDIT-003, 004).
- Docstring vs code drift in `benchmarks/run-all.py` (ZRF-AUDIT-038).
- Stale wiki links + hero image URL (ZRF-AUDIT-031).
- `God Mode` → `Enterprise` tier vocabulary across AGENTS.md + commands
  (ZRF-AUDIT-036).

### Notes

- Version bump `1.0.0 → 1.1.0` per council-ratified D3 decision.
- Compatibility identifier retained per council-ratified D2:
  `zeref-os` for install URLs (`pyproject.name`, `plugin.name`,
  `marketplace.name`); `zeref:` namespace alias remains available.
- Tag lineage divergence with `v2.6.x` retained via `restart-from-2.6.1`
  marker in `docs/PIVOT_LOG.md`.

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
