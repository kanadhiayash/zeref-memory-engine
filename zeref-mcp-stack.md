# ZEREF RECOMMENDED MCP STACK
**Version:** 3.0.0
**These are the recommended connectors for full Zeref capability**

---

## Tier 1 — Core (Install First)

| MCP Server | Purpose | Install Command |
|------------|---------|----------------|
| filesystem | Read/write project files | `claude mcp add filesystem` |
| github | Git operations, PR creation, issue management | `claude mcp add github` |

## Tier 2 — Project Operations (Install for Team Use)

| MCP Server | Purpose | Install Command |
|------------|---------|----------------|
| notion | Create/update Notion pages and databases | `claude mcp add notion` |
| linear | Create/update Linear tickets and projects | `claude mcp add linear` |
| google-drive | Read/write Google Docs and Sheets | `claude mcp add gdrive` |

## Tier 3 — Design Intelligence (Install for Design Work)

| MCP Server | Purpose | Install Command |
|------------|---------|----------------|
| figma | Read Figma files (components, styles, tokens) | `claude mcp add figma` |

## Tier 4 — Automation (Install for Automation Layer)

| MCP Server | Purpose | Install Command |
|------------|---------|----------------|
| browser | CDP WebSocket browser control | via browser-harness repo |
| scrapling | Web scraping and evidence gathering | via Scrapling repo |

## Tier 5 — Advanced Intelligence (Install for Power Users)

| MCP Server | Purpose | Notes |
|------------|---------|-------|
| llm-council | Multi-model debate and evaluation | via llm-council repo |
| graphify | Knowledge graph retrieval | via Graphify repo |

---

## What Happens Without Each Tier

**Without Tier 1:** Zeref cannot write project files or interact with GitHub. Core functionality still works — outputs are copy-paste ready.

**Without Tier 2:** Handoff blocks are copy-paste only — not auto-created in Notion/Linear. No change to output quality.

**Without Tier 3:** Figma integration unavailable. Design skills still work — outputs are Figma-ready specs that must be applied manually.

**Without Tier 4:** No live inspection or web evidence gathering. Research skills still work using provided context.

**Without Tier 5:** No multi-model council or graph retrieval. Single-model execution with standard routing.
