# Privacy Model (v2.6.1)

Privacy in Zeref OS is **deterministic and code-enforced** (v2.5 added the `zeref/privacy.py` runtime; v2.6.1 adds R6 zero-context-loss coverage across 9 SKILL.md Safety sections).

## Three modes (root `PRIVACY.md`)

| Mode | Default | Behavior |
|---|---|---|
| `exact` | — | Write verbatim. No abstraction. |
| `abstract` | **YES** | Strip PII / internal paths / credentials before write. Default for every fresh project. |
| `local-only` | — | Block all external transmission (parent sync, MCP connectors, handoff push). |

Set in root `PRIVACY.md` frontmatter:

```yaml
mode: abstract                  # exact | abstract | local-only
abstract_rules:
  strip_pii: true
  strip_internal_paths: true
  strip_credentials: true
  strip_numbers: false
local_only_blocks:
  - memory/sync/outbound/
  - memory/sync/parent/
connectors_default: off
external_transmission: off
```

## REDACT.md — concrete sensitive classes

`REDACT.md` defines what `privacy-abstraction` (and `zeref/privacy.py`) actually strip:

```yaml
classes:
  credentials:
    enabled: true
    patterns: [api_keys, oauth_tokens, ssh_private_keys, database_connection_strings, .env values]
  pii:
    enabled: true
    patterns: [email_addresses, phone_numbers, physical_addresses, government_ids, dates_of_birth]
  internal_paths:
    enabled: true
  client_data: ...
  financial: ...
  proprietary_code: ...
```

v2.5 L2: `email` class **default-enabled** (closed V01+V02 CRITICAL from v2.5 Phase C).
v2.5 L1: PII name regex tightened with verb-prefix lookahead (no more greedy "Hire John" matches).
v2.5 L11: `zeref write-decision` scrubs PII before disk (closed V12).

## SHARING_POLICY.md — connector allowlist

```yaml
connectors:
  github:   off
  linear:   off
  notion:   off
  jira:     off
  duckduckgo: off
  # ... all OFF by default per AGENTS.md
```

Every connector OFF until explicit enable. `sync-coordinator` reads this on `/start`; refuses to mount disabled tools.

## R6 Zero Context Loss (v2.6)

New shared rule in `_shared/rules.md#R6`. Every fact / named entity / file path / repo / URL / edge case from the raw user prompt must survive into:
- restructured briefs (`prompt-context-engine`)
- routing decisions (`skill-router`)
- handoff packages (`handoff-compiler` → `caveman-handoff`)
- parent-sync outbound staging
- memory-import-export archives
- pattern-to-skill draft synthesis

**v2.6.1 L4 sweep**: R6 referenced in **9 of 14** SKILL.md Safety sections (was 4):
- ✓ prompt-context-engine (origin)
- ✓ skill-router
- ✓ fleet-activator
- ✓ budget-governor
- ✓ caveman-handoff
- ✓ handoff-compiler (L4)
- ✓ parent-sync (L4)
- ✓ memory-import-export (L4)
- ✓ pattern-to-skill (L4)

## Privacy chain (single direction)

```
skill output
    ↓
memory-keeper (R1 single-writer)
    ↓
privacy-guardian (mode check)
    ├── exact → write verbatim
    ├── abstract → privacy-abstraction rewrites payload per REDACT.md
    └── local-only → block external transmission
    ↓
disk OR external connector (per SHARING_POLICY.md)
```

External output **always** passes through `privacy-guardian` (R3).

## Code enforcement (v2.5 runtime)

`zeref/privacy.py`:
- `scrub(text)` → returns `(scrubbed_text, ScrubReport)` with hit count + classes
- Unicode normalization (NFKC)
- Base64 nested decode + re-scan (depth limit)
- Homoglyph table for confusable detection
- Regex patterns per REDACT class (deterministic, not LLM-judged)

**v2.6.1 L12 extends to file paths**: caveman-handoff applies NFKC + lookalike-glyph scan to all path strings (Cyrillic а / Greek ο / fullwidth Latin → flag + user confirm).

## Privacy attacks blocked (per `tests/security-audit-vC.md` + `tests/security-audit-v2.6-C.md`)

| Attack class | Vector | Status |
|---|---|---|
| Homoglyph PII | `Hire Jоhn` (Cyrillic o) | CLOSED (v2.5 L1 + NFKC normalize) |
| Base64-nested credential | `<base64>` containing API key | CLOSED (recursive decode) |
| Email leak | unredacted `user@example.com` | CLOSED (v2.5 L2 default-enable) |
| PII greedy regex | "Hire John" matched as `John Smith` | CLOSED (v2.5 L1 verb-prefix lookahead) |
| Single-writer race | concurrent writes to DECISIONS.md | CLOSED (v2.5 L9 MemoryLock) |
| Mid-write crash | partial file on disk | CLOSED (v2.5 L10 atomic_write) |
| Decision-body injection | PII embedded in narrative prose | CLOSED (v2.5 L11 write-decision scrub) |
| Gate output spoof | fake `[budget-governor]` line | CLOSED (v2.6.1 L3 lint_patterns_log) |
| Prompt-injection via `<context>` | "ignore prior" embedded in brief | CLOSED (v2.6.1 L10 injection filter) |
| File-path homoglyph | Cyrillic-а in handoff payload | CLOSED (v2.6.1 L12 NFKC + confusable scan) |
| Silent cost-tier override | user types "override" | CLOSED (v2.6.1 L13 dual-key) |
| Probe spoof | empty dir at expected ECC path | CLOSED (v2.6.1 L9 marker-file probe) |

**0 CRITICAL open at v2.6.1.**

## What Zeref OS does NOT do

- Encrypt at rest (markdown is plaintext by design)
- Validate via LLM (privacy enforcement is deterministic; LLM is not a privacy enforcer per SOUL.md principle 2)
- Auto-publish to any connector (every push requires explicit user approval)
- Send telemetry (no analytics / no usage stats / no remote logging)

## Verify

```bash
python3 scripts/zeref-validate.py | grep "Root privacy"
# Root privacy:     3/3 (PRIVACY, REDACT, SHARING_POLICY)

python3 -c 'from zeref.privacy import scrub; t,r=scrub("Hire John Smith at john@example.com"); print(r.classes_hit, r.tokens_redacted)'
# {"pii", "credentials" (email)} ≥ 2 tokens
```

## Related

- [[Memory-Model]] — flat layout, single-writer chain
- [[Architecture]] — privacy-guardian + privacy-abstraction agents
- [[Glossary]] — R6, abstract mode, NFKC, homoglyph
- [`_shared/rules.md`](https://github.com/kanadhiayash/zeref-os/blob/main/_shared/rules.md) — R1-R6
- [`tests/security-audit-v2.6-C.md`](https://github.com/kanadhiayash/zeref-os/blob/main/tests/security-audit-v2.6-C.md) — full v2.6.1 audit
