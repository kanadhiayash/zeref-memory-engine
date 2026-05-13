---
type: concept
title: Zeref UX and UI System
created: 2026-05-12
updated: 2026-05-12
status: stable
---

# Zeref UX and UI System

UX flows and UI design principles governing how Zeref surfaces execution to users across environments.

## Core UX Flows

| # | Flow | Description |
|---|------|-------------|
| 1 | Session start | Memory restoration from hot.md before any execution |
| 2 | Routing | Route to smallest useful stack — 1 lead + 0–3 support + 0–1 QA gate |
| 3 | Memory compounding | Update hot.md, log.md, and relevant project/wiki notes after major sessions |
| 4 | Cross-environment handoff | Caveman compression for long or cross-environment context transfer |
| 5 | Register-aware UX work | Brand register vs. product register distinction applied to all UX output |

## UI Design Principles

- **Brand register for public presentation** — portfolio, GitHub, marketplace outputs follow brand register
- **Accessibility is non-negotiable** — applies to any UI surface Zeref produces
- **Token-driven visual system** — when UI exists, use design tokens, not hardcoded values
- **Clarity and professional polish** — components prioritize readability and quality over cleverness

## Register Model

Two registers govern all Zeref output:

| Register | When | Characteristics |
|----------|------|-----------------|
| Brand | Public-facing (portfolio, content, pitch) | Polished, authoritative, positioned |
| Product | Working/execution (code, specs, reviews) | Precise, functional, direct |

Routing logic must apply the correct register before output. See [[zeref-routing-model]] for full routing table.

## Links

- [[zeref-routing-model]] — routing rules including register selection
- [[zeref-memory-protocol]] — session start and memory compounding flows
- [[zeref-obsidian-package]] — source files (04_UX_Flows.md, 05_UI_System.md)
