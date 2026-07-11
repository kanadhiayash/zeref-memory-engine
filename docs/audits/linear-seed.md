# linear-seed.md — Deferred Linear import

> Linear MCP (`plugin:productivity:linear`) is unauthorized in the non-interactive session that produced this audit. This file transcribes the 8 GitHub issues into a Linear-shaped seed so the user can mirror them once the connector is authorized.

## How to authorize

Interactive `claude` session → `/mcp` → authorize `plugin:productivity:linear`. Alternately, via claude.ai connector settings.

## Team + project shape

- Team: `Zeref` (create if missing)
- Project: `Repository-Wide Consistency Audit — v1.0.0 → v?`
- Milestones: `Phase 0-1: baseline` / `Phase 2-4: workstreams` / `Phase 5: synthesis` / `Remediation`

## Issue set to mirror

Each row corresponds to an existing GitHub issue on `kanadhiayash/zeref-memory-engine`. When mirroring, link the Linear issue to the GitHub URL so cross-tool navigation stays intact.

| Linear title | Linear labels | Linear priority | Linked GitHub issue | Branch |
|---|---|---|---|---|
| `[Audit] Repository-Wide Consistency Audit — umbrella tracker` | `audit`, `epic`, `consistency` | Urgent | #81 | n/a (parent) |
| `[Audit] WS-A — Documentation Archaeology` | `audit`, `documentation` | High | #84 | `audit/zeref__ws-a-doc-archaeology` |
| `[Audit] WS-B — Registry, Commands, Routing, Team Packs` | `audit`, `registry` | High | #85 | `audit/zeref__ws-b-registry-routing` |
| `[Audit] WS-C — Runtime, Memory, Write-Path Integrity [Opus 4.7]` | `audit`, `runtime`, `opus-critical` | Urgent | #82 | `audit/zeref__ws-c-runtime-writepath` |
| `[Audit] WS-D — Privacy, Permissions, Network, Security [Opus 4.7]` | `audit`, `security`, `privacy`, `opus-critical` | Urgent | #83 | `audit/zeref__ws-d-privacy-security` |
| `[Audit] WS-E — Installation & Cross-Surface Portability` | `audit`, `portability` | Medium | #86 | `audit/zeref__ws-e-install-portability` |
| `[Audit] WS-F — CI, Release, Versioning, Security Gates` | `audit`, `ci`, `release` | High | #87 | `audit/zeref__ws-f-ci-release` |
| `[Audit] WS-G — Benchmark & Evidence Reproducibility` | `audit`, `benchmarks` | Medium | #88 | `audit/zeref__ws-g-benchmarks-evidence` |

## Description template

Copy the body of each GitHub issue verbatim (available via `gh issue view --repo kanadhiayash/zeref-memory-engine <N>`), prepend a Linear header:

```
Mirrors GitHub #<N>: <URL>
Baseline commit: b82c6410bf17b1bc4d1c79227c3a55e075858ab9
Branch: audit/zeref__<slug>
```

## Do NOT

- Move audit issues between projects mid-audit — SHA-binding is what makes each finding trustworthy.
- Close GitHub issues when Linear closes; the source of truth remains the GitHub thread until remediation lands.
- Auto-sync body content bidirectionally — GitHub is canonical for this audit.
