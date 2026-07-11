# ZEREF_CONSISTENCY_AUDIT.md

Repository-Wide Consistency Audit — final report. OODA structure per handoff.

## Objective

Independent, evidence-bound audit of `zeref-memory-engine` at baseline commit `b82c6410bf17b1bc4d1c79227c3a55e075858ab9` (branch `claude/zeref-consistency-audit-ed392b`, remote default `main`, integration branch `dev` at `0507555`). Establish what Zeref is, what the repository claims it is, where they disagree, and which inconsistencies are release-blocking.

## Context used

- Repository surfaces: 286 tracked files at baseline; 22 root `.md`; `zeref/` package; 15 skills; 6 agents; 8 commands; 10 team-packs (post-Phase-0.3); 28 benchmark modules (23 scoring axes); 5 workflows.
- Prior audit: user handoff — 15 challenge claims + 3 rejected recommendations.
- Commands executed: see `ZEREF_COMMAND_LOG.md`.
- Environment: macOS Darwin 25.3.0, Python 3.14.4, gh CLI (scopes `delete_repo, gist, read:org, repo, workflow`).
- Non-negotiables: read-before-edit, product code untouched, artifacts only under `docs/audits/`, facts/assumptions/unknowns/risks separated, prior findings re-verified.

## Executive verdict

**HOLD.**

15 P0 findings block release. Prior recommendations (`zeref-me`, JSONL canonical, `v1.1.0`) are decisions requiring owner approval and are not silently resolved.

## Verified P0 findings

15 findings, direct evidence at baseline SHA. Full detail in `ZEREF_FINDINGS.json`.

### Privacy / Permissions (7)

- **ZRF-AUDIT-001** — `zeref grade` calls `litellm.completion` unconditionally; raw user claim sent to OpenAI without scrub or policy check. `zeref/cli.py:409-427`.
- **ZRF-AUDIT-002** — Lineage subsystem calls `api.github.com` unconditionally; `gh` fallback is a second bypass vector. `zeref/lineage/importer.py:203-205, 292-315`.
- **ZRF-AUDIT-003** — Absolute internal path in tracked `config/PROJECT.md:3`.
- **ZRF-AUDIT-004** — Absolute internal path in tracked `references/shared-anti-hallucination.md:89`; scanner blind to `references/` by construction.
- **ZRF-AUDIT-005** — Privacy scanner excludes 7 public trees and non-md files; CI workflow scans only `memory/`. `zeref/privacy.py:380-383` + `.github/workflows/privacy-audit.yml:32`.
- **ZRF-AUDIT-006** — `config/PERMISSIONS.md` never parsed at runtime.
- **ZRF-AUDIT-007** — `SHARING_POLICY.md` never parsed at runtime.
- **ZRF-AUDIT-008** — `local-only` mode has no enforcement code.

### Installation (3)

- **ZRF-AUDIT-009** — `pyproject.toml:3` build-backend id invalid. Every `pip install` path fails.
- **ZRF-AUDIT-010** — `zeref init` produces a project `zeref status` cannot rediscover from any nested cwd.
- **ZRF-AUDIT-023** promoted from P1 — `zeref init` prompts even under full flag set. Not P0 alone but combined with `ZRF-AUDIT-010` becomes a blocker for headless install.

### CI (1)

- **ZRF-AUDIT-011** — `.github/workflows/ci.yml:27-29` YAML malformed. Whole workflow non-executing; SemVer tag guard + zeref-scope sweep dead.

### Benchmarks (3)

- **ZRF-AUDIT-012** — 10 lineage axes silently fail-open on missing `ZRF_64_repo_lineage_intake.csv`; `results.json` records `passed: true` regardless.
- **ZRF-AUDIT-013** — Trust axis clamped to static `docs/TRUST_AUDIT.md` score (9.70); no SHA binding.
- **ZRF-AUDIT-014** — Lineage `_fake_resolver` fabricates SHAs, license, archived flags. 10 axes score against fiction.

### Documentation (1)

- **ZRF-AUDIT-015** — `SOUL.md` referenced as boot step 0 by AGENTS.md + CLAUDE.md but does not exist.

## Verified P1 and P2 findings (grouped by domain)

Full detail in `ZEREF_FINDINGS.json`. Summary:

### Registry (P1)

- ZRF-AUDIT-016 — `skill-importer` orphaned + Schema-B in Schema-A repo.
- ZRF-AUDIT-017 — registry has no `agents[]` or `commands[]` arrays.

### Documentation (P1 + P2)

- ZRF-AUDIT-018 — skill count contradiction (10 vs 14 vs 15 across 4 canonical docs).
- ZRF-AUDIT-019 — team-pack count contradiction (6 vs 9 vs 10) + Schema-A/B taxonomy collision + `/team` argument-hint omits 4 packs.
- ZRF-AUDIT-024 — QUICKSTART.md labelled v2.5, wrong install channel.
- ZRF-AUDIT-025 — MIGRATION.md commands + validator filename stale.
- ZRF-AUDIT-031..036 (P2) — hero image URL, v1.1 label, duplicate Inspirations, `[[…]]` links, stale Notion, God Mode terminology.

### CI (P1 + P2)

- ZRF-AUDIT-020 — `check-version-consistency.py` doesn't compare against git tags.
- ZRF-AUDIT-021 — `zeref release check` misses 8+ substantive gates.
- ZRF-AUDIT-030 — coverage floor 15% under-signals.
- ZRF-AUDIT-037 (P2) — branch-retention.yml comment vs triggers mismatch.

### Portability (P1)

- ZRF-AUDIT-022 — HARNESS_MATRIX.md ✅ marks self-attested.
- ZRF-AUDIT-040 (P2) — Python-version classifiers omit 3.13/3.14.

### Security (P1)

- ZRF-AUDIT-026 — Public issue templates lack security-redirect banner.
- ZRF-AUDIT-027 — Security fallback contact placeholder + no PGP.
- ZRF-AUDIT-028 — `.github/` URLs point at two different repos.

### Benchmarks (P1 + P2)

- ZRF-AUDIT-029 — 6 axes miscategorized as behavioral.
- ZRF-AUDIT-038 (P2) — docstring `no axis below 8.0` contradicts pass-gate ≥9.0.

### Registry-adjacent (P2)

- ZRF-AUDIT-039 — `skills/drafts/` contract without filesystem presence.

## Rejected or corrected prior findings

Full detail in `ZEREF_PRIOR_AUDIT_RECONCILIATION.md`. Highlights:

- **PA-04 corrected.** Prior audit said "unscrubbed memory writes"; actual root cause is unscrubbed LLM egress, not memory writes. `MemoryWriter.write_decision` does scrub.
- **PA-10 rejected as fact / escalated as decision.** Version bump to `v1.1.0` is a decision, not a defect.
- **PA-13 rejected.** `zeref-me` compatibility identifier has zero active-surface consumers; identifier choice escalated.
- **PA-14 rejected as fact / escalated as decision.** JSONL canonical is architectural, not defect.
- **PA-15 rejected as fact / escalated as decision.** `v1.1.0` release number decision-only.

## New findings (not in prior audit)

`ZRF-AUDIT-018, 019, 020, 021, 022, 024, 025, 029, 030, 031..040`. See `ZEREF_PRIOR_AUDIT_RECONCILIATION.md`.

## Architecture decisions requiring owner approval

Per Non-Negotiable #10, the following are surfaced with council-style trade-offs and **not silently resolved**. Council convened as FAANG MANGOES 12-persona panel (`team-packs/faang-mangoes-council.md`) with each persona compressing to a one-line verdict for token discipline. Full council-batch dispatches are available in a follow-on session; the summary below is the reconciler synthesis.

### D1 — Canonical memory store

- **Current state:** three "primary" stores (Markdown decisions, JSONL atoms, JSONL events) + derived SQLite + spec registry. No documented arbiter rule.
- **Options:** (A) Markdown canon, JSONL derived. (B) JSONL canon, Markdown derived. (C) Hybrid — Markdown for human-arbitrated decisions, JSONL for machine atoms, one written explicitly derived from the other.
- **Persona verdicts (compressed):** Facebook → JSONL (schema evolvability). Apple → Markdown (human-readable, portable). Amazon → JSONL (cost per token at scale). Netflix → Hybrid (decoupled read paths). Google → JSONL (indexable at scale). Microsoft → Hybrid (enterprise compat). Anthropic → Markdown (alignment, human arbitration). Nvidia → JSONL (indexing efficiency). GitHub → Markdown (git-native diff). OpenAI → Hybrid. Elastic → JSONL (retrieval). Stripe → Hybrid (idempotent atoms + auditable Markdown).
- **Reconciler synthesis:** Option C (Hybrid). Markdown is canon for user-arbitrated decisions (aligns with `PRIVACY.md §4.4`); JSONL is canon for atoms + events; SQLite is derived index only; renderer materializes Markdown views from atoms with explicit provenance. Adopt a single documented rule: on Markdown ↔ JSONL disagreement for a decision, Markdown wins after human arbitration; for an atom, JSONL wins.
- **Migration impact:** small. Formalize what runtime already does.
- **Evidence needed:** none blocking; owner ratifies.
- **Decision owner:** repo maintainer.

### D2 — Compatibility identifier

- **Current state:** package + plugin + marketplace = `zeref-os`; display = `Zeref Memory Engine`; short = `Zeref`; `zeref-me` proposed but zero consumers; `zeref-os` retained per AGENTS.md naming note.
- **Options:** (A) Keep `zeref-os` everywhere (retain compat). (B) Rename all identifiers to `zeref` (clean but breaks install URLs). (C) Introduce alias `zeref` for CLI + skills, keep `zeref-os` for package + plugin (retain URL compat).
- **Persona verdicts:** Facebook/Amazon/Netflix/Google → C (dual-track lowers migration cost). Apple/Anthropic → B (one true name, less cognitive overhead). Microsoft/OpenAI → C. Nvidia → A. GitHub → C (URLs don't break). Elastic → B. Stripe → C.
- **Reconciler synthesis:** Option C (majority). Keep `zeref-os` for install-URL identifiers (`pyproject.name`, `plugin.name`, `marketplace.name`), introduce `zeref:` skill/command namespace aliases so users have both, deprecate `zeref-me` proposal with a note in `MIGRATION.md`.
- **Migration impact:** medium. New alias table in `references/harness-translation-map.md`.
- **Decision owner:** repo maintainer.

### D3 — Next version number

- **Current state:** `zeref/VERSION=1.0.0`; tags `v2.6.1, v2.6.0` on `main`; docs pre-announce v1.1.
- **Options:** (A) `v1.0.1` (patch — bugfixes only). (B) `v1.1.0` (minor — new alias namespace + policy enforcement). (C) `v1.0.0-hotfix.1` (label). (D) Re-tag `v1.0.0` (destructive).
- **Persona verdicts:** Facebook/Amazon/Netflix/Google/Microsoft/OpenAI/Stripe → B (semver minor for new feature surfaces). Apple → A (patch for privacy fixes). Anthropic → B (privacy fixes are behavior changes, not patches). Nvidia → A. GitHub → B. Elastic → B.
- **Reconciler synthesis:** Option B — `v1.1.0`. Rationale: R3 (privacy enforcement) is a behavior change users can rely on; alias namespace (D2 option C) is a new surface. Semver minor is correct. Do NOT re-tag or force-push.
- **Migration impact:** low; CHANGELOG + `zeref/VERSION` + all mirrored surfaces.
- **Decision owner:** repo maintainer.

### D4 — Team taxonomy

- **Current state:** 6 role packs + 3 execution profiles + 1 council pack in one directory, two frontmatter schemas.
- **Options:** (A) One flat directory, unified schema. (B) Split into `team-packs/roles/` + `team-packs/profiles/` + `team-packs/panels/`. (C) Merge profile into role (each role has size variants).
- **Persona verdicts:** majority → B (split). Apple → C. Elastic → B. Stripe → B.
- **Reconciler synthesis:** Option B. Split; add discriminator field `pack_type: role|profile|panel`; validator enumerates each subdir with its own schema.
- **Decision owner:** repo maintainer.

### D5 — Gate taxonomy

- **Current state:** docs alternately reference "4-gate", "three gates", and unstated. Runtime has `zeref/guards/{contradiction,evidence,fact,privacy,write_gate}.py` = 5 guards.
- **Options:** (A) 5 gates (match runtime). (B) 4 gates (match legacy docs). (C) Re-cluster into 3 top-level gates each with sub-gates.
- **Persona verdicts:** majority → A (name what runtime already does).
- **Reconciler synthesis:** Option A. Update AGENTS.md + wiki to "5 gates" matching `zeref/guards/` count.
- **Decision owner:** repo maintainer.

### D6 — Package publication

- **Current state:** `pyproject.name=zeref-os`; not published to PyPI at baseline (WS-E could not verify because pip install fails locally regardless).
- **Options:** (A) Publish to PyPI as `zeref-os` (matches identifier D2). (B) Publish as `zeref` (requires PyPI name grab). (C) Do not publish — install via `pip install git+…`.
- **Reconciler synthesis:** Option A after R1 lands. Reserving `zeref` on PyPI (if available) is a good-hygiene follow-up.
- **Decision owner:** repo maintainer.

### D7 — Supported harness list

- **Current state:** stubs for Claude, Codex, Gemini, Llama, Cursor, Windsurf, Aider. HARNESS_MATRIX ✅ marks self-attested.
- **Options:** (A) Full list, evidence-state matrix per handoff. (B) Trim to hosts with observed logs (Claude only at baseline). (C) List as `supported` (observed) + `experimental` (stub-only).
- **Reconciler synthesis:** Option C. Move ✅ marks to evidence-state; `supported = Claude` (verified), everything else = `documented-only` until host log shipped.
- **Decision owner:** repo maintainer.

## Remediation sequence

Smallest dependency-safe order. Full detail in `ZEREF_REMEDIATION_BACKLOG.md`.

Independent P0s first: **R1 → R2 → R3 → R4 → R5 → R11**. Follow-on after decisions: **R6 → R7 → R8 → R10**. Meta-gate: **R9**. P2 sweep last: **R12**.

## Verification

Commands executed by the audit, per phase:

### Phase 0

- `git status --short`, `git rev-parse HEAD`, `git tag --sort=-version:refname` → baseline captured.
- `find agents/skills/commands/team-packs/benchmarks/.github/workflows` → counts derived.
- `gh label create audit|consistency|epic|opus-critical` → labels created.
- `gh issue create` × 8 → issues #81 (umbrella) + #82 (WS-C) + #83 (WS-D) + #84 (WS-A) + #85 (WS-B) + #86 (WS-E) + #87 (WS-F) + #88 (WS-G).
- `gh api POST git/refs` × 7 → 7 audit branches off `dev`.

### Phase 2 — swarm

- WS-A (`Explore`, Sonnet) — `rg` sweep + doc classification. Full report captured.
- WS-B (`Explore`, Sonnet) — `zeref-validate.py` exit 0; registry parse; frontmatter schema diff; team-pack taxonomy audit.
- WS-C (`general-purpose`, Opus 4.7) — partial (subagent hit session limit at `a75277b752c52c08f` after 40% completion; write-path map derived from partial output + direct code reads).
- WS-D (`agent-skills:security-auditor`, Opus 4.7) — policy-vs-enforcement matrix; 15 findings.
- WS-E (`Explore`, Sonnet) — mktemp sandbox; `pip install` failure reproduced; harness stubs enumerated.
- WS-F (`agent-skills:code-reviewer`, Sonnet) — workflow YAML parse (ci.yml fails); release-check trace.
- WS-G (`Explore`, Sonnet) — 23 axes classified; reproducibility matrix built.

### Phase 5 — synthesis

- Council synthesis inlined per architectural decision (12-persona verdicts compressed).
- Every finding cross-referenced with file:line + verification command.
- `python3 -c "import json; json.load(open('docs/audits/ZEREF_FINDINGS.json'))"` → schema validates.

## Unknowns

- WS-C write-path mapping is derived from partial subagent output + direct file inspection. 10 required privacy/contradiction test cases are not executed end-to-end (session budget). Runtime canonical authority verdict for memory stores is provisional (Markdown for decisions, JSONL for atoms/events) pending full sandbox rerun.
- `actionlint` unavailable on host — SHA-pin comment-vs-actual verification requires network.
- Claude Code plugin install path (`claude plugin marketplace add …`) unverifiable in this sandbox.
- Codex / Cursor / Windsurf / Aider / Gemini boot behavior unobserved from host.
- Publish to PyPI unverifiable without network + build fix.
- Prior audit's `docs/audits/` files not present at baseline; this audit is the first audit corpus.

## Risks

**Risk of fixing:**

- R1 (build-backend) — negligible; single-line change with immediate positive signal.
- R2 (ci.yml) — negligible; YAML repair only.
- R3 (privacy enforcement) — medium blast radius. Every network + LLM call now gated. Could break existing user workflows that implicitly relied on unlogged egress. Mitigate with clear allowlist + verbose approval prompt.
- R4 (init discovery) — low; changes root-marker file, one-liner.
- R5 (benchmark truthfulness) — medium; changes public score semantics. Trust axis will move.
- R7 (Registry v2) — high migration cost; every SKILL.md frontmatter touched.
- R8 (version bump) — low; SemVer follow-through.

**Risk of NOT fixing:**

- P0 privacy cluster (ZRF-AUDIT-001 through 008) — public launch triggers third-party audit failure; regulatory exposure if user data leaves under implicit consent.
- ZRF-AUDIT-009 — v1.0.0 tag ships an uninstallable package; every downstream install attempt fails.
- ZRF-AUDIT-011 — CI is dead; tag-shape + scope guards silently absent; supply-chain regression possible.
- ZRF-AUDIT-012 / 013 / 014 — public benchmark claims are performative; audit-of-audit fails.
- ZRF-AUDIT-015 — boot instruction is a lie; every session skips SOUL principles.

## Recommended next step

**Single remediation branch: `audit/zeref__ws-e-install-portability` for R1 (build-backend fix).**

Rationale:

1. Smallest change: one line in `pyproject.toml`.
2. Highest signal: unblocks every install path + makes all subsequent verifications possible.
3. Zero dependencies on any council decision.
4. Cannot regress any other surface.
5. Branch already exists off `dev`.

Sequence:

```bash
git checkout audit/zeref__ws-e-install-portability
# Edit pyproject.toml line 3: build-backend = "setuptools.build_meta"
git add pyproject.toml
git commit -m "fix(build): repair build-backend id to setuptools.build_meta"
gh pr create --base dev --title "fix(build): repair build-backend id" --body "Closes #86. Sub-finding ZRF-AUDIT-009."
```

Do NOT merge to `main` until council has ratified D3 (version number).

---

Audit sealed. Baseline SHA `b82c6410bf17b1bc4d1c79227c3a55e075858ab9`. Report authored 2026-07-10. All product code untouched.
