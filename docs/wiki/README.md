# Zeref OS Wiki — README

This directory contains the v2.6.1 wiki for [Zeref OS](https://github.com/kanadhiayash/zeref-os).

**Start here**: [[Home]]

## Pages

| Page | Purpose |
|---|---|
| [[Home]] | Landing page · quick links · v2.6.1 4-gate chain overview |
| [[Installation]] | Per-harness install · verification · uninstall |
| [[Architecture]] | 14 skills · 6 agents · 8 commands · 6 team packs · 4-gate chain · Model-Tier Routing |
| [[Memory-Model]] | Flat layout · boundary-first reads · PATTERNS.jsonl schema (v2.6.1) |
| [[Privacy-Model]] | 3 modes · REDACT classes · R6 Zero Context Loss · attacks blocked |
| [[Team-Packs]] | 6 on-demand packs · max 4 agents · v2.6 gates integration |
| [[Pattern-Detection]] | Two-Strikes Rule · pattern-observer · skill drafting · R6 |
| [[Decision-Log]] | D1-D11 canonical + ADR-001 (4-gate) + ADR-002 (audit hardening) |
| [[Model-Debates]] | 2026 Anthropic pricing · model-resolver · cascade pattern · per-skill audit |
| [[Versioning-History]] | v1.x → v2.6.1 timeline with lessons per era |
| [[FAQ]] | v2.6.1 new questions + original FAQ |
| [[Glossary]] | All terms · R6 · 4-gate · L1-L15 · D-numbers |
| [[Inspirations]] | Naming · engineering lineage · doctrinal influences |

## Sync to GitHub Wiki

```bash
# Clone wiki separately (GitHub wikis are separate git repos)
git clone https://github.com/kanadhiayash/zeref-os.wiki.git
# Copy pages
cp docs/wiki/*.md zeref-os.wiki/
cd zeref-os.wiki
git add -A
git commit -m "wiki: sync v2.6.1 from docs/wiki/"
git push
```

The `docs/wiki/` files in the main repo are the source of truth. GitHub wiki mirrors them.

## Conventions

- File names use Title-Case + hyphens (matches GitHub wiki convention)
- `[[Page-Name]]` syntax = wiki-internal link (GitHub wiki resolves these)
- External links use full URLs
- v2.6.1 additions marked with ★ in tables where helpful
- Code blocks show actual command output where possible (validator state, etc.)

## Related

- [Main repo README](https://github.com/kanadhiayash/zeref-os)
- [AGENTS.md](https://github.com/kanadhiayash/zeref-os/blob/main/AGENTS.md)
- [CHANGELOG](https://github.com/kanadhiayash/zeref-os/blob/main/CHANGELOG.md)
- [docs/RELEASE_LOG.md](https://github.com/kanadhiayash/zeref-os/blob/main/docs/RELEASE_LOG.md)
- [docs/adr/](https://github.com/kanadhiayash/zeref-os/tree/main/docs/adr)
- [Notion Command Center](https://copper-tv-288.notion.site/Zeref-Agent-OS-Command-Center-358d695d836a81af9f6adf30770217c3)
