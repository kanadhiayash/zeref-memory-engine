---
type: concept
title: Zeref Data Model
created: 2026-05-12
updated: 2026-05-12
status: draft
---

# Zeref Data Model

Core entities in the Zeref OS system. This model is partial — expand as Phase 3 (registry) and Phase 5 (graph) progress.

## Core Entities

| Entity | Description | Lives in |
|--------|-------------|---------|
| **Skill** | Modular execution unit — one job, one trigger phrase set, one deliverable | `skills/[name]/SKILL.md` |
| **Agent** | Orchestrator that routes or validates across multiple skills | `agents/[name].md` |
| **Command** | Thin interface that invokes a skill or memory action | `commands/[name].toml` |
| **Memory Page** | Wiki page holding durable session context | `wiki/` tree |
| **Graph Node** | Graphify-generated node linking concepts, skills, and entities | `graphify/graph.json` (planned) |

## Relationships (planned)

```
Command → invokes → Skill or Agent
Agent   → routes to → Skill(s)
Skill   → produces → Output
Output  → references → Memory Page
Memory Page → links to → Graph Node
```

## Planned Scripts (Phase 3)

| Script | Purpose |
|--------|---------|
| `generate-skill.py` | Scaffold new skill from template |
| `build-registry.py` | Build machine-readable skill registry from SKILL.md files |
| `validate-fleet.sh` | Validate name/directory alignment across all 112 skills |

## Links

- [[zeref-v2-rebuild]] — Phase 3 registry, Phase 5 graph
- [[zeref-obsidian-package]] — source files (07_Data_Model.md, 08_Development_Notes.md)
