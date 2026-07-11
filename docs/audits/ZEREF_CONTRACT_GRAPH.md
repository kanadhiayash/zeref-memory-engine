# ZEREF_CONTRACT_GRAPH.md

Baseline: `b82c6410bf17b1bc4d1c79227c3a55e075858ab9`. Every domain records claimed authority, competing authority, runtime authority, current conflict. Winners **not** chosen here — see reconciliation + council.

## 16 authority domains

| Domain | Claimed authority | Competing authority | Runtime authority | Current conflict |
|---|---|---|---|---|
| Product identity | `README.md` "Zeref Memory Engine" | every other root `.md`, all wiki, `SKILL.md` frontmatter still "Zeref OS" | package name `zeref-os` (pyproject.toml:7) | display name migrated; identifier legacy retained; no single source names both |
| Product version | `zeref/VERSION = 1.0.0` | git tags `v2.6.1, v2.6.0`; `docs/HARDENING_OVERVIEW.md:1 v1.1`; `QUICKSTART.md:1 v2.5` | `zeref/__init__.py` reads VERSION file | tags exceed VERSION; version-consistency check doesn't compare against tags (WSF-4) |
| Component registry | `zeref-registry.json` | filesystem; `AGENTS.md` counts (differ) | none — registry unused at runtime | 14 registered / 15 on disk (skill-importer orphan); no agents/commands arrays |
| Boot sequence | `AGENTS.md §0` | `CLAUDE.md`; harness stubs; `SOUL.md` missing | no runtime enforcement; guides read by human/model | SOUL.md referenced but absent (WSA-1) |
| Memory authority | `AGENTS.md` "Markdown canonical" (§4.4 via PRIVACY.md) | JSONL atoms + events; SQLite state; generated Markdown views | mixed: `MemoryWriter.write_decision` writes Markdown + JSONL event (`memory/core.py:227-260`); `atom_store` writes JSONL; SQLite in `state.db` | three stores; no single "on disagreement, X wins" rule |
| Write path | `agents/memory-keeper.md` "single writer" | direct CLI writes; `zeref/guards/write_gate.py` | `zeref/lock.py` enforces file lock on `write_decision` (`cli.py:79`); other CLI writes may bypass | not every CLI write funnels through write_gate (WSC-partial finding) |
| Privacy policy | `PRIVACY.md` mode `abstract`; `REDACT.md` classes | none | `zeref/privacy.py:310-368 scrub()` works; `zeref/privacy.py:383 audit()` covers `.md` only in `memory/` | WSD-3 (LLM egress), WSD-4 (lineage GH), WSD-5 (local-only unenforced), WSD-6/7 (PERMISSIONS + SHARING_POLICY unparsed) |
| Permission policy | `config/PERMISSIONS.md network: denied` | none | **file never read** (WSD-6) | documentary-only |
| Network policy | `PRIVACY.md external_transmission: off` + PERMISSIONS `network: denied` | none | `zeref/cli.py:409-427` calls `litellm.completion` unconditionally; `zeref/lineage/importer.py:203-205, 292-310` calls `urllib.request.urlopen("https://api.github.com/...")` unconditionally | policy fully documentary; runtime egress in ≥2 vectors |
| Model routing | `zeref-registry.json` per-skill `model` field; `references/*.md`; council pack Phase-0.3 | `zeref/memory/cost_router.py` (`token_efficiency` benchmark) | `zeref route` CLI uses cost_router policy (name collision with markdown skill-router) | two distinct concepts share the "router" name |
| Harness portability | `docs/HARNESS_MATRIX.md` ✅ marks | `benchmarks/portability.py` (file-presence check) | none host-observed | ✅ marks self-attested (WSE-6, WSE-8); benchmark 10.0/10.0 file-presence only |
| Installation | `INSTALL.md`; `.claude-plugin/plugin.json`; `pyproject.toml` | `MIGRATION.md:65` legacy cmd; `docs/wiki/Installation.md` | `pip install .` **fails** at build-backend (WSE-1); `python3 -m zeref` works via PYTHONPATH only | package uninstallable at HEAD |
| Release readiness | `zeref release check` + `scripts/check-version-consistency.py` | `docs/RELEASE_GATES.md`; `docs/RELEASE_PROCESS.md`; benchmark run-all | `zeref/release/checks.py` 6 checks; freshness-blind (WSF-3); no test/lint/build rerun (WSF-2) | release gate green with broken install |
| Benchmark verdict | `benchmarks/run-all.py` (23 axes, pass ≥ 9.0) | `docs/TRUST_AUDIT.md` static score | override in `run-all.py:81-117` reads TRUST_AUDIT.md and clamps trust axis to `9.70` regardless of code | old audit auto-applied to new code (WSG-2); 10 lineage axes need missing CSV (WSG-1); fake resolver (WSG-3) |
| Security reporting | `SECURITY.md:11-13` GitHub PVR canonical + `SECURITY_CONTACTS.md` fallback | `.github/ISSUE_TEMPLATE/bug_report.md, feature_request.md` (public forms) | PVR link works; email fallback self-flagged as placeholder | public issue templates lack security-redirect banner (WSD-8); email unverified (WSD-9) |
| Historical documentation | `docs/PIVOT_LOG.md, docs/RELEASE_LOG.md, docs/archive/` | duplicates in active wiki (`docs/archive/INSPIRATIONS.md` vs `docs/wiki/Inspirations.md`) | none | duplicate content, unreconciled (WSA-10) |
| CI + gate authority | `.github/workflows/*.yml` | `zeref release check`; `zeref-validate.py` | `.github/workflows/ci.yml` **YAML-malformed at line 27-29** (WSF-1); other 4 workflows parse | ci.yml non-executing; SemVer tag guard + scope sweep dead |

## Memory-authority subgraph (write-path canon)

Ten claimed memory stores. Runtime touch enumerated:

| Store | Path pattern | Written by | Read by | Runtime canonical? |
|---|---|---|---|---|
| Markdown memory | `memory/DECISIONS.md`, `memory/hot.md`, etc | `MemoryWriter.write_decision` (`zeref/memory/core.py:227`), `zeref/memory/render.py` | `zeref/memory/recall.py`, humans | **primary** for decisions |
| JSONL atoms | `memory/l1_atoms/*.jsonl` | `zeref/memory/atom_store.py` | `zeref/memory/search.py`, `recall.py` | primary for atoms |
| JSONL events | `memory/l1_atoms/contradictions.jsonl` etc | `_wiki_write_event` (`memory/core.py:277`) | audit logger, indexer | primary for events |
| SQLite state | `memory/l1_atoms/state.db` | `zeref/memory_state.py` | `db-status`, indexer | derived index |
| Generated Markdown views | `memory/views/*.md` | `zeref/memory/render.py` | humans | **derived** — regenerable |
| Snapshots | `memory/snapshots/` | `_write_memory_files` scaffolding | manual | derived |
| PATTERNS.jsonl | `memory/patterns/PATTERNS.jsonl` | `zeref/audit/logger.py` | pattern-observer, validator | primary for events |
| Registry JSON | `zeref-registry.json` | manual edits | none at runtime | **spec-only** |
| AGENTS.md | root | manual | humans, models | spec-only |
| Python runtime | `zeref/*.py` | dev | itself | executable truth |

**Conflict recorded, not resolved:** three "primary" stores (Markdown, JSONL atoms, JSONL events) + one derived (SQLite state) + one spec (registry). No single documented rule resolves disagreement across the three primaries. Council decision required — see architectural decisions section of `ZEREF_CONSISTENCY_AUDIT.md`.

## Router subgraph (name collision recorded)

- `skills/skill-router/SKILL.md` = Markdown routing prompt (Sonnet/Haiku instructions).
- `zeref/cli.py cmd_route` → `zeref.routing.policy` = task-vs-tier cost router.
- Same repo, same word, different concept. Runtime backing exists for only the cost router.

## Boot-sequence subgraph

`AGENTS.md §0` reading order: SOUL → PROJECT → hot → index → PRIVACY → REDACT → MEMORY.md head → PATTERNS.jsonl tail. Runtime enforcement: **none** — the harness executes the reads (model behavior), no Python code fails if a step is skipped. `SOUL.md` absence produces no error signal.
