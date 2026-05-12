# wiki/index.md — Zeref Master Wiki Index

> **Navigation file.** Read this after `wiki/hot.md` to find any page in the Zeref OS wiki.
> This file is the map. It does not contain logic — it points to files that do.
> Every new wiki page must be registered here within the same session it is created.
> One row per page. Keep descriptions tight (one line). Update Last Updated on every edit.

---

## How To Navigate This Wiki

1. **Start at `hot.md`** — get the current session state and last handoff.
2. **Check this index** — find the right page by section and description.
3. **Open the target page** — read it fully before acting on it.
4. **Drill into raw files only if needed** — index → page → raw file is the correct reading order.
5. **Never skip to raw files first.** The wiki layer exists to prevent token waste and context churn.

**Karpathy rule:** The wiki is the single source of truth. Raw files are evidence. Commands are thin interfaces.

---

## Projects

Pages for active and completed projects. One page per project. Contains objective, architecture, decisions, status, phases, and risks.

| Page | Description | Last Updated | Status |
|------|-------------|-------------|--------|
| `wiki/projects/zeref-v2-rebuild.md` | Full rebuild of Zeref OS from V1 skill fleet to 5-layer execution OS | 2026-05-12 | Active |
| `wiki/projects/[project-slug].md` | [One-line description of project] | [YYYY-MM-DD] | [Active / Paused / Complete] |
| `wiki/projects/[project-slug].md` | [One-line description of project] | [YYYY-MM-DD] | [Active / Paused / Complete] |

---

## Concepts

Durable, canonical documentation of Zeref rules, models, protocols, and decisions. These pages should change rarely. When they do change, log the decision in `wiki/log.md`.

| Page | Description | Last Updated | Status |
|------|-------------|-------------|--------|
| `wiki/concepts/zeref-routing-model.md` | Canonical routing model: smallest-stack, task types, registers, routing table, Caveman triggers | 2026-05-12 | Stable |
| `wiki/concepts/zeref-memory-protocol.md` | Canonical memory protocol: hot.md read-first, log rules, index maintenance, lint triggers | 2026-05-12 | Stable |
| `wiki/concepts/[concept-slug].md` | [One-line description of concept or decision] | [YYYY-MM-DD] | [Stable / Draft / Deprecated] |

---

## Sources

Curated references, guides, URLs, and repos that inform Zeref's architecture or execution. Each entry explains why it matters, not just what it is.

| Page | Description | Last Updated | Status |
|------|-------------|-------------|--------|
| `wiki/sources/zeref-reference-links.md` | Karpathy LLM Wiki, claude-obsidian, Graphify, Tenfold guides, Zeref repo — with summaries | 2026-05-12 | Current |
| `wiki/sources/[source-slug].md` | [One-line description of source or reference] | [YYYY-MM-DD] | [Current / Archived] |
| `wiki/sources/[source-slug].md` | [One-line description of source or reference] | [YYYY-MM-DD] | [Current / Archived] |

---

## Skills

The Zeref Skill Fleet lives in the skill registry. This index points to it but does not duplicate it.

| Resource | Description | Last Updated | Status |
|----------|-------------|-------------|--------|
| `skills/registry.md` | Machine-readable skill registry — trigger phrases, deliverables, support skills, QA gates | [Pending — Phase 3] | Draft |
| `skills/README.md` | Skill fleet overview, validation status, category breakdown | [YYYY-MM-DD] | Active |
| `zeref-skills-fleet/` | Local Mac source: `/Users/yashkanadhia/Documents/Claude/00SKILLS/zeref-skills-fleet` | 2026-05-12 | Live |

---

## Commands

Thin reusable command interfaces. Commands are entry points — logic lives in skills and concept pages.

| Resource | Description | Last Updated | Status |
|----------|-------------|-------------|--------|
| `commands/` | Command directory — orient, save, capture, recall, trace, lint, package, caveman | [Pending — Phase 5] | Planned |
| `commands/orient.md` | Orient command — reads hot.md, summarizes session state | [Pending] | Planned |
| `commands/caveman.md` | Caveman handoff command — compresses long context for cross-environment transfer | [Pending] | Planned |

---

## Index Maintenance Rules

- **Register every new page** in the correct section within the same session it is created.
- **One row per page.** No duplicates.
- **Update Last Updated** every time a page is substantively edited.
- **Status values:** Active · Stable · Draft · Paused · Complete · Deprecated · Planned · Archived
- **Do not add raw notes here.** This is a map, not a notebook.
- If the index grows beyond ~50 rows per section, consider splitting into sub-indexes.
