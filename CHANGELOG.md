# Changelog — Zeref OS

All notable changes to **Zeref OS** are documented here.

Versioning: [Semantic Versioning](https://semver.org/) — `MAJOR.MINOR.PATCH`.

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
