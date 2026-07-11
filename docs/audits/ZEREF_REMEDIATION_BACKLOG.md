# ZEREF_REMEDIATION_BACKLOG.md

Baseline: `b82c6410bf17b1bc4d1c79227c3a55e075858ab9`. Ordered smallest-dependency-safe sequence. **Only the first remediation branch is recommended for immediate action** — subsequent items depend on the council decisions in `ZEREF_CONSISTENCY_AUDIT.md` §Architecture-decisions.

## Priority ladder

P0 (release blockers) → P1 (contract drift) → P2 (maintenance).

## R1 — Fix broken pip install (RECOMMENDED FIRST BRANCH)

- **ID:** R1
- **Priority:** P0
- **Finding:** `ZRF-AUDIT-009`
- **Objective:** Repair `pyproject.toml` build-backend so `pip install .`, `pip install -e .`, and `pip install <git-url>` succeed.
- **Files affected:** `pyproject.toml`
- **Dependencies:** none
- **Implementation outline:** change `pyproject.toml:3` from `build-backend = "setuptools.backends.legacy:build"` to `build-backend = "setuptools.build_meta"`.
- **Regression tests:** `mktemp -d && python3 -m venv .v && . .v/bin/activate && pip install .` exit 0; `which zeref` non-empty; `zeref --help` runs.
- **Verification commands:**
  ```bash
  cd $(mktemp -d) && python3 -m venv .v && . .v/bin/activate
  pip install <repo> && which zeref && zeref --version
  ```
- **Rollback:** revert `pyproject.toml` line 3.
- **Definition of done:** clean-room install passes in CI (new step in `.github/workflows/test.yml`) on Python 3.11, 3.12, 3.13.
- **Branch:** `audit/zeref__ws-e-install-portability` (already exists).

## R2 — Fix ci.yml YAML block-collection

- **ID:** R2
- **Priority:** P0
- **Finding:** `ZRF-AUDIT-011`
- **Objective:** Restore CI workflow so SemVer tag guard + zeref-scope sweep run.
- **Files affected:** `.github/workflows/ci.yml`
- **Dependencies:** none
- **Implementation outline:** indent `with:` block one level deeper (col 9) under `- uses:` at lines 27-29.
- **Regression tests:** `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"` exit 0; `actionlint .github/workflows/*.yml` clean.
- **Verification commands:** as above.
- **Rollback:** revert ci.yml.
- **Definition of done:** ci.yml runs on a PR to `dev`; log shows SemVer + scope-sweep steps executed.
- **Branch:** `audit/zeref__ws-f-ci-release` (already exists).

## R3 — Privacy scanner scope + policy enforcement

- **ID:** R3
- **Priority:** P0
- **Finding:** `ZRF-AUDIT-003`, `ZRF-AUDIT-004`, `ZRF-AUDIT-005`, `ZRF-AUDIT-006`, `ZRF-AUDIT-007`, `ZRF-AUDIT-008`
- **Objective:** Make privacy/permissions/sharing-policy actually enforce.
- **Files affected:** `zeref/privacy.py`, `zeref/cli.py`, new `zeref/security/policy.py` (loader), `config/PROJECT.md` (redact leak), `references/shared-anti-hallucination.md` (redact leak), `.github/workflows/privacy-audit.yml` (scan repo root not just memory/).
- **Dependencies:** none (do NOT wait on council)
- **Implementation outline:**
  1. New `zeref/security/policy.py`: loaders for PRIVACY.md, REDACT.md, SHARING_POLICY.md, config/PERMISSIONS.md. Returns typed struct.
  2. `zeref.privacy.audit()`: default target = project root; extend rglob to `.md .py .json .jsonl .yml .yaml .toml`; narrow `_SKIP` to `{docs/archive, tests/fixtures}`.
  3. `zeref.cli.cmd_grade`: refuse to send unless SHARING_POLICY connector enabled + per-call approval; scrub claim before send.
  4. `zeref.lineage.importer`: every `urlopen` / `gh api` call routed through policy gate.
  5. `MemoryWriter`: if mode=local-only, refuse writes to `memory/sync/outbound/` and `memory/sync/parent/` with clear error.
  6. Redact the two path leaks in tracked files.
- **Regression tests:** new `tests/test_policy_enforcement.py` — LLM egress denied when policy off; lineage GH call denied when github.enabled=false; local-only refuses sync writes.
- **Verification commands:**
  ```bash
  python3 -m zeref audit-privacy --strict
  python3 -m pytest tests/test_policy_enforcement.py
  rg -n '/Users/|/home/' config/ references/
  ```
- **Rollback:** revert new policy module + config; leaks remain redacted (safety-first).
- **Definition of done:** all P0 privacy findings closed; privacy-audit workflow scans root; two path leaks gone; policy loader has ≥85% coverage.
- **Branch:** `audit/zeref__ws-d-privacy-security` (already exists).

## R4 — Fix `zeref init` project discovery + non-interactive mode

- **ID:** R4
- **Priority:** P0
- **Finding:** `ZRF-AUDIT-010`, `ZRF-AUDIT-023`
- **Objective:** `zeref init` produces a project the CLI can rediscover from any nested cwd, headlessly.
- **Files affected:** `zeref/memory/core.py`, `zeref/cli.py`
- **Dependencies:** none
- **Implementation outline:**
  1. Change `discover_project_root` to look for `config/PROJECT.md` (already scaffolded) instead of `AGENTS.md`. OR: scaffold `AGENTS.md` in `scaffold_project` if choosing to keep AGENTS.md as marker.
  2. `cmd_init`: skip parent-project prompt when non-TTY OR when all mandatory flags supplied; require `--parent` explicit when TTY.
- **Regression tests:** new `tests/test_init_discovery.py` — init in tempdir, chdir to nested subdir, `zeref status` succeeds; init from piped stdin exits 0.
- **Verification commands:**
  ```bash
  cd $(mktemp -d) && zeref init --name X --privacy abstract --tier standard --parent ''
  cd nested/a/b && zeref status  # must not print 'PROJECT.md missing'
  ```
- **Rollback:** revert cli + core changes.
- **Definition of done:** nested-cwd status works; scripted install works.
- **Branch:** `audit/zeref__ws-e-install-portability` (shared with R1).

## R5 — Benchmark truthfulness + trust freshness

- **ID:** R5
- **Priority:** P0
- **Finding:** `ZRF-AUDIT-012`, `ZRF-AUDIT-013`, `ZRF-AUDIT-014`
- **Objective:** Benchmarks either measure or explicitly skip; trust score binds to SHA.
- **Files affected:** `benchmarks/run-all.py`, `benchmarks/lineage_common.py`, `docs/TRUST_AUDIT.md`, `zeref/lineage/importer.py`
- **Dependencies:** none (independent of council decisions)
- **Implementation outline:**
  1. `docs/TRUST_AUDIT.md`: add `Bound-commit-SHA: <sha>` field; `_apply_verified_overrides` (`run-all.py:81`) refuses override unless SHA matches HEAD.
  2. `run-all.py`: when input CSV absent, write `results.json` with `axis.status = "skipped"` NOT "passed"; final `passed = all(axes) except skipped ignored` with explicit `skipped_axes` list.
  3. `_fake_resolver` (`lineage_common.py:41`): rename to `_stub_resolver`; rename affected axes to `lineage-schema-conformance-<subaxis>` OR ship a real snapshot CSV.
  4. Add `RUBRIC.md` binding each axis to its measurement class.
- **Regression tests:** `python3 benchmarks/run-all.py` on a clone with no CSV emits `skipped_axes` list, exit 0. With CSV bundled, exit ≤ current pass.
- **Verification commands:**
  ```bash
  python3 benchmarks/run-all.py
  jq '.axes[] | select(.status == "skipped")' benchmarks/results.json
  ```
- **Rollback:** revert changes; delete `docs/TRUST_AUDIT.md` SHA field.
- **Definition of done:** no axis reports "passed" on missing input; trust score never inherited across code changes.
- **Branch:** `audit/zeref__ws-g-benchmarks-evidence` (already exists).

## R6 — SOUL.md decision (blocked on council)

- **ID:** R6
- **Priority:** P0
- **Finding:** `ZRF-AUDIT-015`
- **Objective:** Decide: create SOUL.md, or strike the reference.
- **Files affected:** `SOUL.md` (new) OR `AGENTS.md:21` + `CLAUDE.md/CODEX.md/GEMINI.md/LLAMA.md` (edit).
- **Dependencies:** council decision on canonical boot sequence.
- **Implementation outline:** two branches. If create: author the 5 operating principles (§0), commit. If strike: remove reference from all 5 files.
- **Regression tests:** if create, add `scripts/zeref-validate.py` assertion that SOUL.md exists.
- **Verification commands:** `ls SOUL.md`; `rg -n 'SOUL.md' *.md`.
- **Rollback:** delete the created file OR restore the reference.
- **Definition of done:** boot step 0 is either fulfilled or removed cleanly.
- **Branch:** `audit/zeref__ws-a-doc-archaeology` (already exists).

## R7 — Registry v2 (blocked on council)

- **ID:** R7
- **Priority:** P1
- **Finding:** `ZRF-AUDIT-016`, `ZRF-AUDIT-017`, `ZRF-AUDIT-018`, `ZRF-AUDIT-019`, `ZRF-AUDIT-039`
- **Objective:** One schema per surface; agents + commands + skills + team-packs all registered; counts derived from registry.
- **Files affected:** `zeref-registry.json`, `scripts/zeref-validate.py`, `AGENTS.md`, `INSTALL.md`, `skills/skill-router/SKILL.md`, `commands/team.md`, `team-packs/*` (split), all SKILL.md frontmatter.
- **Dependencies:** council decision on team-pack taxonomy + skill-schema.
- **Implementation outline:** design Registry v2 after council decision; migrate SKILL.md frontmatter; extend validator; update AGENTS.md counts to disk-derived.
- **Regression tests:** validator enforces disk-count == registry-count for every surface.
- **Definition of done:** every filesystem surface registered; every count in docs matches registry.
- **Branch:** `audit/zeref__ws-b-registry-routing` (already exists).

## R8 — Version + tag alignment (blocked on council)

- **ID:** R8
- **Priority:** P1
- **Finding:** `ZRF-AUDIT-020`
- **Objective:** `check-version-consistency.py` compares against `git tag`; documented lineage-restart if any.
- **Files affected:** `scripts/check-version-consistency.py`, `docs/PIVOT_LOG.md`, `docs/RELEASE_LOG.md`.
- **Dependencies:** council decision on next version number.
- **Definition of done:** VERSION vs tag divergence produces CI error unless PIVOT_LOG explicitly records the intentional break.
- **Branch:** `audit/zeref__ws-f-ci-release` (shared with R2).

## R9 — Release-check comprehensive gate

- **ID:** R9
- **Priority:** P1
- **Finding:** `ZRF-AUDIT-021`
- **Objective:** `zeref release check` reruns tests, validator, version-consistency, package build, plugin manifest lint, doc links, privacy audit, tag alignment, benchmark freshness.
- **Files affected:** `zeref/release/checks.py`.
- **Dependencies:** R1, R2, R3, R5 (each sub-check must be reliable first).
- **Definition of done:** stored PASS files carry current HEAD SHA + timestamp; consumers can't be fooled by stale results.
- **Branch:** `audit/zeref__ws-f-ci-release`.

## R10 — Portability evidence matrix

- **ID:** R10
- **Priority:** P1
- **Finding:** `ZRF-AUDIT-022`
- **Objective:** Replace `docs/HARNESS_MATRIX.md ✅` marks with evidence-state matrix.
- **Files affected:** `docs/HARNESS_MATRIX.md`, `scripts/harness-probe.py`, `benchmarks/portability.py`.
- **Dependencies:** council decision on supported-harness list.
- **Definition of done:** every row cites a host log or is labeled `documented-only` / `blocked`.
- **Branch:** `audit/zeref__ws-e-install-portability`.

## R11 — Security surface hardening

- **ID:** R11
- **Priority:** P1
- **Finding:** `ZRF-AUDIT-026`, `ZRF-AUDIT-027`, `ZRF-AUDIT-028`
- **Objective:** Public issue templates redirect security; fallback contact verified; URLs normalized.
- **Files affected:** `.github/ISSUE_TEMPLATE/{bug_report.md,feature_request.md,config.yml}`, `SECURITY_CONTACTS.md`.
- **Dependencies:** none.
- **Definition of done:** clicking any public template shows security-redirect banner; contact email verified; PGP fingerprint published; all `.github/` URLs point at `kanadhiayash/zeref-memory-engine`.
- **Branch:** `audit/zeref__ws-d-privacy-security`.

## R12 — Doc-drift sweep (P2 cluster)

- **ID:** R12
- **Priority:** P2
- **Findings:** `ZRF-AUDIT-024`, `ZRF-AUDIT-025`, `ZRF-AUDIT-031` through `ZRF-AUDIT-040`.
- **Objective:** Batch-rewrite the P2 doc-drift set after P0/P1 decisions land.
- **Dependencies:** R7 (registry) + R8 (version) — most P2 rewrites depend on canonical counts + version.
- **Branch:** `audit/zeref__ws-a-doc-archaeology`.

## Dependency-safe execution sequence

Independent (parallelizable) first:

1. **R1** (build-backend) — 1-line change; ships install fix.
2. **R2** (ci.yml) — 1-line change; ships CI recovery.
3. **R3** (privacy enforcement) — largest P0; touch 2 dozen files, adds tests.
4. **R4** (init discovery) — depends on R1 for end-to-end verify.
5. **R5** (benchmark truthfulness) — independent.
6. **R11** (security surface) — independent.

Blocked on council (do NOT start pre-decision):

7. **R6** (SOUL.md) — needs boot-sequence decision.
8. **R7** (Registry v2) — needs team-pack taxonomy + skill schema decision.
9. **R8** (version alignment) — needs next-version decision.
10. **R10** (portability matrix) — needs supported-harness decision.

Follow-on:

11. **R9** (release-check gate) — depends on R1/R2/R3/R5.
12. **R12** (P2 doc sweep) — depends on R7/R8.

## Recommended first branch

**R1 — build-backend fix.** Smallest change (one line), highest signal (unblocks every install path), zero dependencies, cannot regress anything else. All other P0 remediations become easier to verify once the package installs.

Landing sequence for R1:

```
git checkout audit/zeref__ws-e-install-portability
# edit pyproject.toml line 3
git add pyproject.toml
git commit -m "fix(build): repair build-backend id to setuptools.build_meta"
gh pr create --base dev --title "fix(build): repair build-backend id"
```

Do NOT merge to `main` until council has decided next-version (R8).
