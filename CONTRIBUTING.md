# Contributing to Zeref Agent OS

## What This Is

Zeref Agent OS is a Context Engine and Agent Harness OS. Contributions improve the harness — skills, agents, references, and scripts — not the underlying models.

## How to Contribute

### Adding a New Skill

1. Create folder: `skills/zeref-[category]-[specialty]/`
2. Create `SKILL.md` with v3.0 frontmatter (see existing skills for format):
   - Required fields: `skill`, `title`, `category`, `model`, `effort`, `max_turns`, `trigger_phrases`, `model_preference`, `risk_level`, `dependencies`
3. Run `python3 scripts/zeref-validate.py` — must pass
4. Add entry to `registry/zeref-skill-registry.json`
5. Submit PR with: skill name, category, trigger phrases, why this fills a gap

### Modifying an Existing Skill

- Only append to skill files — do not rewrite existing sections
- Note the insertion point clearly in your PR description
- Run validate after modification

### Safety Rules for Contributors

1. Never delete existing skill files — archive to `archive/` instead
2. Never claim workspace was updated unless file was actually written
3. Never add trigger phrases that could cause unsafe routing
4. skill_updater.py changes require `"approved": true` — this gate is non-negotiable

### Skill Categories

| Prefix | Guild |
|--------|-------|
| `zeref-biz-` | Business strategy, competitive, GTM |
| `zeref-cnt-` | Content writing, copy, documentation |
| `zeref-dev-` | Engineering, code, architecture |
| `zeref-final-` | Final delivery, packaging, validation |
| `zeref-hq-` | Executive strategy, CPO, CTO |
| `zeref-mkt-` | Marketing, growth, brand |
| `zeref-qa-` | Testing, audits, quality |
| `zeref-system-` | Memory, compression, routing, CI |
| `zeref-ux-` | Design, research, accessibility |

## Code of Conduct

Honest, evidence-disciplined contributions only. No invented metrics, fabricated research, or hallucinated file contents in skill definitions.
