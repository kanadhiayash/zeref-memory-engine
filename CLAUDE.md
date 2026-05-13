# Zeref OS: LLM Wiki

Mode: D + B Hybrid (Second Brain + Fleet Module System)
Purpose: Persistent memory, skill fleet documentation, career + project tracking for Yash Kanadhia
Owner: Yash Kanadhia
Created: 2026-05-12

---

## Structure

```
zeref-agent-os/          ← repo root (also the Obsidian vault root)
├── .raw/                # Source docs — never modify
├── wiki/
│   ├── brain/           # MASTER HUB — start here (00_master.md)
│   │   ├── 00_master.md        # Entry point
│   │   ├── 01_zeref_os.md      # OS kernel docs
│   │   ├── 02_fleet_map.md     # All 112 skills
│   │   ├── 03_architecture.md  # System design
│   │   ├── 04_memory_protocol.md
│   │   ├── 05_commands.md      # All 9 commands
│   │   └── 06_agents.md        # Fleet router + QA agent
│   ├── fleet/           # 9 domain pages — all 112 skills documented
│   ├── index.md         # Master catalog of all pages
│   ├── log.md           # Append-only operation log
│   ├── hot.md           # Hot cache: recent context ~500 words
│   ├── overview.md      # Executive summary of the whole wiki
│   ├── career/          # Job search, positioning, portfolio, proof of work
│   ├── projects/        # Active builds and initiatives
│   ├── learning/        # Skills, tools, frameworks being developed
│   ├── decisions/       # Key decisions with rationale and date
│   ├── memory/          # Persistent facts, rules, constraints, context
│   ├── sources/         # Ingested source summaries
│   └── meta/            # Dashboards, lint reports, conventions
├── _templates/          # Note templates per type
└── skills/              # The actual skill SKILL.md files (source of truth)
```

---

## Conventions

- All notes use YAML frontmatter: `type`, `status`, `created`, `updated`, `tags` (minimum)
- Wikilinks use `[[Note Name]]` format — filenames are unique, no paths needed
- `.raw/` contains source documents — never modify them
- `wiki/index.md` is master catalog — update on every ingest
- `wiki/log.md` is append-only — new entries go at TOP
- `wiki/hot.md` is overwritten each session — keep under 500 words
- Skills live in `skills/` — wiki pages in `wiki/fleet/` reference them, never duplicate them

---

## Domain Tags

| Tag | Domain |
|-----|--------|
| `#fleet` | Skills, agents, routing, plugin architecture |
| `#career` | Positioning, job search, portfolio, proof of work |
| `#project` | Active builds and initiatives |
| `#learning` | Skills, tools, frameworks being developed |
| `#decision` | Key decisions with rationale |
| `#memory` | Persistent facts, rules, constraints |

---

## Operations

- **Ingest**: drop source in `.raw/`, say "ingest [filename]" → `wiki-ingest`
- **Query**: ask any question → `wiki-query` (reads hot.md first, then index, then drills)
- **Lint**: say "lint the wiki" → `wiki-lint`
- **Save**: say "save this" → `save`
- **Research**: say "research [topic]" → `autoresearch`
- **Upgrade fleet**: edit `skills/[skill]/SKILL.md` directly — then update `wiki/fleet/[skill].md`

---

## Wiki Knowledge Base (for cross-project referencing)

Add this to any other project's CLAUDE.md:

```markdown
## Zeref OS Wiki
Path: ~/Documents/Claude/99_ZEREF/zeref-skills-fleet 2

When you need context not in this project:
1. Read wiki/hot.md first (recent context, ~500 words)
2. Read wiki/brain/00_master.md to orient
3. If not enough, read wiki/index.md (full catalog)
4. If domain-specific, read wiki/fleet/[domain]-skills.md
5. Only then read individual wiki pages
```
