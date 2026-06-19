# Contributing to Zeref OS

Zeref OS is the local-first context and memory layer for AI-assisted
work. Contributions improve the harness — skills, agents, references,
scripts, benchmarks, and docs — not the underlying models.

The current public version is **v1.0.0**. See
[`docs/PIVOT_LOG.md`](docs/PIVOT_LOG.md) for pre-v1 history.

## Workflow

1. **Open or pick an issue.** Track scope in GitHub Issues. For security
   issues, **do not** open a public issue — read
   [`SECURITY.md`](SECURITY.md).
2. **Branch from `main`.** Naming: `<type>/zeref__<short-description>`.
   Types: `feat` / `fix` / `refactor` / `chore` / `docs` / `test` /
   `ci` / `revert`. Example: `feat/zeref__skill-importer-v1`.
3. **Keep branches < 3 days.** Rebase on `origin/main`. Push with
   `--force-with-lease` (never bare `--force`).
4. **Conventional Commits.** Scope `(zeref)` for global changes; use a
   tighter scope (`(skill-router)`, `(privacy)`, `(ci)`) when changes
   stay within one surface.
5. **Open a PR.** Target ~300 LOC. Use the PR template. The reviewer
   checklist covers design, functionality, complexity, tests, naming,
   comments, security.
6. **Pass CI.** Required green checks: `validate`, `pytest`,
   `privacy-audit`, `version-consistency`.
7. **Squash-merge to `main`.** Tags on `main` are SemVer
   (`v<major>.<minor>.<patch>`).

## Branch retention policy (project rule)

**We never delete branches after merge.** Old feature branches stand as
the version-of-record for the work they shipped. The
`.github/workflows/branch-retention.yml` workflow refuses delete events.

If a branch name has decayed (typos, accidental personal info), **rename
it** to `archive/<original-name>` — preserving history — instead of
deleting it.

## Adding or modifying a skill

1. Create `skills/<skill-name>/SKILL.md` with v1.0.0 frontmatter:
   ```yaml
   ---
   skill: <name>
   version: "1.0.0"
   model: claude-sonnet-4-6      # or claude-haiku-4-5 / claude-opus-4-7
   model_alias: sonnet
   risk_level: low|medium|high
   triggers:
     - <trigger phrase>
   deliverables:
     - <expected output>
   ---
   ```
2. Add an entry to `zeref-registry.json` matching the skill's metadata.
3. Run `python3 scripts/zeref-validate.py` — must pass.
4. Run `python3 -m pytest -q` — must pass.
5. PR description must say: (a) what gap this skill fills, (b) which
   existing skill (if any) was considered and why it's insufficient, (c)
   whether the skill auto-activates (and if so, the gate that triggers
   it).

### Modifying an existing skill

- Prefer additive changes. If you must rewrite a section, leave a
  one-line comment in the PR description noting the section.
- Never delete skill files. Move to `archive/skills/<name>/` instead.
- Run the validator after every edit.

## Adding a privacy pattern

1. Add the pattern to `zeref/privacy.py` under `_PROVIDER_PATTERNS`.
2. Add a positive case **and** a negative case to
   `tests/test_privacy_redaction.py`.
3. Run `pytest -q tests/test_privacy_redaction.py` — must pass.
4. If the pattern matches a credential issued by a specific vendor,
   note the vendor and the format link in the PR description.

## Updating a benchmark scorer

1. Edit the axis scorer under `benchmarks/`.
2. Mirror any scoring change in `benchmarks/RUBRIC.md` — the rubric is
   the public contract.
3. Run `python3 benchmarks/run-all.py` — every axis must remain ≥ 9.0
   and no axis below 8.0.
4. Update `docs/BENCHMARK_REPORT.md` (auto-generated; commit it).

## Safety rules

1. **Never commit secrets.** `.env*`, `*.pem`, `*.key`, service-account
   JSON, and provider tokens are gitignored. If a secret slips into a
   draft branch, rotate the secret and rebase the branch to drop the
   commit.
2. **Never bypass `--strict` privacy audit** in CI. If a legitimate
   pattern produces a false-positive, fix the regex or add a focused
   exclusion — do not lower the gate.
3. **Never claim a workspace was updated unless a file was actually
   written.** This rule applies to humans and to agents.
4. **Never add trigger phrases that could cause unsafe routing.**
   Skill triggers must be specific enough that `skill-router` doesn't
   pull the skill into unrelated tasks.
5. **`pattern-to-skill` drafts** are inert until you run
   `/review-skill <name>` — do not flip the `activation` field by hand.

## Code of conduct

Honest, evidence-disciplined contributions only. No invented metrics,
fabricated research, or hallucinated file contents. Cite sources for
non-obvious claims.

## Releases

- `chore(zeref): release v<version>` commit lands on a release branch.
- SemVer tag on `main` only.
- GitHub Release attaches the freshly-generated
  `docs/BENCHMARK_REPORT.md` and links to `CHANGELOG.md`.
