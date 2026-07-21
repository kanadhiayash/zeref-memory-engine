# Zeref OS — Release Log

One row per tagged release on `main`. Source: `CHANGELOG.md`.

## Releases

| Tag | Date | Summary | Migration |
|---|---|---|---|
| `v2.0.0-alpha.2` | 2026-07-14 | Hardening: consistency + claim accuracy. Council removal completed across dependents; macOS/cloud-sync duplicate-artifact guard; claim-accuracy sweep over live public surfaces (unsupported compression-ratio and score claims removed or qualified); `scripts/zeref-validate.py` derives structure counts from the tree instead of stale constants. | None — no runtime behavior change |
| `v2.0.0-alpha.1` | 2026-07-12 | vNext Wave 1 begins: FAANG-MANGOES council removed; provider-neutral reasoning classes (fast/balanced/deep/frontier/local/private) in core; provider model ids moved to `zeref/adapters/providers/`; deprecation aliases (small→lean, medium→balanced, enterprise→assured, skill-router→capability-resolver, fleet-activator→capability-prober, skill-importer→capability-manager). | Breaking architectural pivot — see MIGRATION.md |
| `v1.1.1` | 2026-07-11 | CI green-up + branch cleanup. Fixes frontmatter break on 3 files (R13), aligns privacy-audit workflow with release-check ceiling via new `--max-hits`/`--max-files` CLI flags (R14), branch-retention filters to protected refs only (R15), Node 24 SHA bumps (R16), 7 empty audit branches deleted, `dev` synced to `main`. | None — behavior-preserving patch |
| `v1.1.0` | 2026-07-10 | Audit remediation release — closes the Repository-Wide Consistency Audit (`docs/audits/`). New `SOUL.md`, `zeref/security/policy.py` (runtime enforcement of PRIVACY/SHARING_POLICY/PERMISSIONS), Registry v1.1 (agents+commands+team_packs+gates arrays), fix `pyproject.toml` build-backend, fix `ci.yml` YAML, evidence-state HARNESS_MATRIX, SHA-bound release evidence. | `docs/audits/ZEREF_CONSISTENCY_AUDIT.md` — 40 findings, 15 P0 closed |
| `v1.0.0` | 2026-06-19 | Public v1.0.0 launch — trust-repair pivot: single version surface, reproducible `tests/`, 11 expanded privacy patterns, private vuln disclosure, SHA-pinned CI, four-axis benchmark harness. Architecture identical to v2.6.1 (carried forward). | `docs/PIVOT_LOG.md` — pre-v1 history archived to `kanadhiayash/zeref-os-archive` |

### Archived pre-v1 history

The following tags exist only in the read-only archive repo and are no
longer the canonical public surface:

| Tag (archive) | Date | Summary |
|---|---|---|
| `v2.6.1` | 2026-06-08 | Polish — code-backed gate enforcement, model-id normalization, R6 coverage sweep |
| `v2.6.0` | 2026-06-08 | Auto-Gated Execution — 4-gate chain; 4 new skills; Core Principles 13 + 14; R6 Zero Context Loss |

## Conventions

- **SemVer**: `v<major>.<minor>.<patch>` on `main` only.
- **Migration links**: `MIGRATION.md` documents breaking changes + transition steps where applicable.

## Command center

Notion: https://copper-tv-288.notion.site/Zeref-Agent-OS-Command-Center-358d695d836a81af9f6adf30770217c3
