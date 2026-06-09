# Privacy Model

> Imagine writing every project note straight into a private notebook. Zeref OS is that notebook for AI sessions — and the notebook ships with locks on every drawer.

Privacy in Zeref OS is **deterministic and code-enforced**. The `zeref/privacy.py` runtime applies REDACT rules before any write; nothing relies on the model "remembering" to filter.

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
  email:
    enabled: true
    patterns: [email_addresses_standalone]
  internal_paths:
    enabled: true
  client_data: ...
  financial: ...
  proprietary_code: ...
```

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

## R6 Zero Context Loss

Shared rule in `_shared/rules.md#R6`. Every fact / named entity / file path / repo / URL / edge case from the raw user prompt must survive into:

- restructured briefs (`prompt-context-engine`)
- routing decisions (`skill-router`)
- handoff packages (`handoff-compiler` → `caveman-handoff`)
- parent-sync outbound staging
- memory-import-export archives
- pattern-to-skill draft synthesis

R6 is referenced in nine SKILL.md Safety sections across the pack.

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

## Code enforcement (`zeref/privacy.py`)

- `scrub(text)` → returns `(scrubbed_text, ScrubReport)` with hit count + classes
- Unicode normalization (NFKC)
- Base64 nested decode + re-scan (depth limit)
- Homoglyph table for confusable detection
- Regex patterns per REDACT class (deterministic, not LLM-judged)

`caveman-handoff` also applies NFKC + lookalike-glyph scan to all path strings — Cyrillic а / Greek ο / fullwidth Latin flagged and confirmed before any handoff write.

## What Zeref OS does NOT do

- Encrypt at rest (markdown is plaintext by design)
- Validate via LLM (privacy enforcement is deterministic; the LLM is not a privacy enforcer)
- Auto-publish to any connector (every push requires explicit user approval)
- Send telemetry (no analytics / no usage stats / no remote logging)

## Verify

```bash
python3 scripts/zeref-validate.py | grep "Root privacy"
# Root privacy:     3/3 (PRIVACY, REDACT, SHARING_POLICY)

python3 -c 'from zeref.privacy import scrub; t,r=scrub("Hire John Smith at john@example.com"); print(r.classes_hit, r.tokens_redacted)'
```

## Related

- [[Memory-Model]] — flat layout, single-writer chain
- [[Architecture]] — privacy-guardian + privacy-abstraction agents
- [[Glossary]] — R6, abstract mode, NFKC, homoglyph
- [`_shared/rules.md`](https://github.com/kanadhiayash/zeref-os/blob/main/_shared/rules.md) — R1-R6
