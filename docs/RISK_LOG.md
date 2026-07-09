# Zeref OS — Risk Log

Open and accepted risks for the project. Append-only. Every entry includes
date, owner, status, mitigation, and a reference to the decision that
created or accepted the risk.

---

## R-001 — Force-push to `main` during v1.0.0 reset

- **Opened:** 2026-06-19
- **Owner:** yk
- **Status:** accepted (one-time)
- **Severity:** high (irreversible local; recoverable from archive)
- **Description:** The v1.0.0 launch (Pivot 4) requires nuking the public
  git history of `kanadhiayash/zeref-os` and re-pushing a single squashed
  root commit. This conflicts with the standing global rule "Never
  force-push" in `~/.claude/CLAUDE.md`.
- **Mitigation:**
  1. Full original history archived to `kanadhiayash/zeref-os-archive`
     (private, read-only) **before** any force-push runs.
  2. Local archive tarball stored at `99_ARCHIVE/by-year/2026/zeref-os-pre-v1.tar.gz`.
  3. Force-push uses `--force-with-lease`, never bare `--force`.
  4. Old release tags (`v2.6.1`, `v2.6.0`, `v2.5.x`) re-created in the
     archive repo so existing installs keep resolving.
- **Trigger that ends acceptance:** the v1.0.0 launch is a one-time event.
  After v1.0.0 ships, the standing no-force-push rule resumes; future
  releases follow normal squash-merge-to-`main` plus annotated SemVer tag.

---

## R-002 — Autonomous loop bypasses APPROVE gate

- **Opened:** 2026-06-19
- **Owner:** yk
- **Status:** accepted (this run only)
- **Severity:** medium
- **Description:** The standing operational protocol requires "propose →
  APPROVE → apply". The v1.0.0 trust-repair run was authorised to execute
  fully autonomously, gated only by the public benchmark rubric.
- **Mitigation:**
  1. Hard halt: any benchmark axis scoring <8.0 stops the loop and
     surfaces the failure for human review before publish.
  2. No destructive git operation (force-push, tag push, archive
     creation) executes inside the autonomous loop. Those steps are
     emitted as exact commands in the final report for the user to run
     manually.
  3. The Opus security-audit pass (Phase 9) is independent of the
     benchmark rubric and can also halt publish.

---

## R-003 — SHA-pinning depends on Dependabot upkeep

- **Opened:** 2026-06-19
- **Owner:** yk
- **Status:** open / mitigated (initial pins **verified**)
- **Severity:** low
- **Description:** Pinning every GitHub Action to a full commit SHA
  removes the "moving major tag" supply-chain risk, but creates a
  maintenance burden: actions silently fall behind security fixes if
  pins are not refreshed.
- **Verified pins (2026-06-19, via `gh api repos/<owner>/<repo>/git/refs/tags/<tag>`):**
  - `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683` ⇔ `v4.2.2` ✅
  - `actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2b` ⇔ `v5.3.0` ✅
  - `actions/upload-artifact@b4b15b8c7c6ac21ea08fcf65892d2ee8f75cf882` ⇔ `v4.4.3` ✅
- **Mitigation:** `.github/dependabot.yml` runs weekly against the
  `github-actions` ecosystem and opens PRs for each updated SHA. Each
  Dependabot PR triggers re-verification before merge.

---

## R-004 — Benchmark rubric is self-defined

- **Opened:** 2026-06-19
- **Owner:** yk
- **Status:** open / mitigated
- **Severity:** medium
- **Description:** `benchmarks/RUBRIC.md` is authored by the same project
  it grades. Risk of grading to target.
- **Mitigation:**
  1. Rubric is public and versioned.
  2. The Opus security-audit pass in Phase 9 re-scores the `trust` axis
     independently of the rubric's own scorer.
  3. External re-scoring is invited in `CONTRIBUTING.md` — anyone may
     submit a PR proposing rubric changes.

---

## R-005 — Claude plugin install verification is environment-dependent

- **Opened:** 2026-06-19
- **Owner:** yk
- **Status:** open
- **Severity:** low
- **Description:** The autonomous loop cannot reliably invoke
  `claude plugin install` from a headless environment.
- **Mitigation:** The final report surfaces the exact manual commands
  rather than claiming a verification that did not happen.

---

## R-007 — Coverage gate measures only in-process paths

- **Opened:** 2026-06-19
- **Owner:** yk
- **Status:** open / mitigated
- **Severity:** low
- **Description:** The `tests/` suite exercises the CLI via `subprocess`
  to validate the real entry point. Python's `coverage` library does not
  see subprocess-spawned line execution by default, so the reported
  total of ~15% under-counts the actual coverage of `zeref/privacy.py`
  (well-covered in-process) and especially `zeref/cli.py` (heavily
  exercised but invisible to the in-process tracer).
- **Mitigation now:** CI gate set to `--fail-under=15` — the honest
  measured floor. Tests still run; their assertions still cover the
  behaviour. The gate prevents *regressions below* the current level.
- **Planned follow-up:** Refactor a subset of subprocess tests to call
  the CLI handlers in-process via `argparse.Namespace`, OR add
  subprocess coverage via `sitecustomize.py` + `COVERAGE_PROCESS_START`.
  Either path lets us raise the gate to 60–85% honestly. Tracked.

---

## R-006 — Never-delete-branch policy + repo size

- **Opened:** 2026-06-19
- **Owner:** yk
- **Status:** open / accepted
- **Severity:** low
- **Description:** User policy retains all branches forever, including
  merged ones. Over time this grows the ref namespace and slows some
  git operations (`git branch --all`, `git fetch --prune`).
- **Mitigation:** `branch-retention.yml` enforces the policy in CI but
  also documents that branches older than 24 months may be renamed to
  `archive/<original-name>` to keep the working ref list tractable.
  Renaming is not deletion; history is preserved.
