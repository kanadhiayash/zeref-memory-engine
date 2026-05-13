---
type: source
title: Zeref Obsidian Package
created: 2026-05-12
updated: 2026-05-12
status: ingested
---

# Zeref Obsidian Package

Canonical Obsidian-ready overview of Zeref V1/V2 — the primary ingest source for Claude across environments. Covers all 16 project files (00–14 + Handover + README).

## Files

| File | Content |
|------|---------|
| `Zeref_OS_Handover.md` | Master entry point — layers, recommended vault structure, read order, routing rule |
| `00_Project_Brain.md` | Project summary — 112 skills, V1.1.2, risks, open work |
| `01_Product_Strategy.md` | Vision: free-first, graph-aware, wiki-backed execution OS |
| `02_User_Research.md` | Core user pain points — context rediscovery, generic AI, fragmented workflows |
| `03_Problem_Definition.md` | Problem: AI treats every session as disposable instead of compounding |
| `04_UX_Flows.md` | 5 core flows — session start, routing, memory compounding, handoff, register-aware UX |
| `05_UI_System.md` | Design principles — brand register, accessibility, token-driven system, professional polish |
| `06_Technical_Architecture.md` | 6 system layers — kernel, skill, memory, graph, quality, command |
| `07_Data_Model.md` | Core entities — Skill, Agent, Command, Memory Page, Graph Node |
| `08_Development_Notes.md` | Proposed scripts — generate-skill.py, build-registry.py, validate-fleet.sh |
| `09_Portfolio_Content.md` | Portfolio angle — Zeref as proof of systems-level PM/UX/technical thinking |
| `10_LinkedIn_Substack_Content.md` | Content goals — disposable AI problem, compounding memory, systems thinking proof |
| `11_QA_Audit.md` | QA status — 112 skills validated, name/directory alignment passed |
| `12_Decision_Log.md` | 3 key decisions — Obsidian+Graphify+Karpathy, free-first, smallest-stack |
| `13_Changelog.md` | Unreleased V2 — Obsidian scaffold, Graphify, skill registry all planned |
| `14_Final_Compiler.md` | Final package purpose — proof of work for portfolio/GitHub/marketplace |
| `README.txt` | Recommended Obsidian location: `ZerefOS/03Projects/zeref-skills-fleet/` |

## Key Extractions

**Recommended vault structure:**
```
ZerefOS/00System/
ZerefOS/01Raw/
ZerefOS/02Wiki/
ZerefOS/03Projects/
ZerefOS/04Graphify/
ZerefOS/05Canvases/
ZerefOS/06Reports/
ZerefOS/99Archive/
```

**Read order (enforced):**
1. hot.md
2. index.md
3. Relevant project index or GRAPHREPORT.md
4. 3–5 relevant wiki pages
5. Raw files only when needed

**Memory rules (from Handover):**
- End major sessions with durable memory updates
- Never compress: code, commands, file paths, URLs, errors, config values, warnings
- Caveman for long or cross-environment contexts

## Links

- [[zeref-v2-rebuild]] — full project page
- [[zeref-routing-model]] — routing rules
- [[zeref-memory-protocol]] — memory protocol
- [[zeref-ux-and-ui]] — UX flows and UI system
- [[zeref-data-model]] — entity model
- [[zeref-portfolio-content]] — portfolio and content strategy
