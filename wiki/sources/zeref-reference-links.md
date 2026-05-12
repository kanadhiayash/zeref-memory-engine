# zeref-reference-links.md — Curated Reference Links

> **Source page.** Update when a reference is reviewed or becomes stale.
> **Last updated:** 2026-05-12
> **Status:** Current

---

## Purpose

This page curates the external references, repos, guides, and gists that directly inform Zeref's architecture, memory model, routing logic, skill design, and execution philosophy. Each entry explains why it matters to Zeref specifically — not just what it is.

**Reading rule:** Before re-fetching any of these URLs, check this page first. If the summary covers what you need, skip the fetch. Only fetch when the summary is insufficient or the source may have changed significantly.

---

## 1. Karpathy LLM Wiki Pattern

| Field | Value |
|-------|-------|
| **Name** | Karpathy LLM Wiki / AGENTS.md pattern |
| **URL** | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f |
| **Type** | GitHub Gist |
| **Last reviewed** | 2026-05-11 |

### Why It Matters to Zeref

This is the foundational architecture for Zeref's entire memory layer. Karpathy's pattern proposes that LLM-assisted workflows should maintain a personal wiki — a set of structured, evolving pages — rather than relying on chat history or re-reading raw files each session.

**Key principles extracted and adopted by Zeref:**
- The LLM reads a structured index first, then navigates to the relevant page, then drills into raw files only when needed.
- Wiki pages are LLM-maintained: the assistant writes and updates them, not the human.
- Raw sources (files, logs, code) feed the wiki. The wiki feeds working context.
- A schema file (AGENTS.md or CLAUDE.md) governs conventions and workflows.
- This pattern turns ephemeral chat into **compounding operational memory**.

**Zeref implementation:** `wiki/hot.md` (first read), `wiki/index.md` (navigate), `wiki/projects/`, `wiki/concepts/`, `wiki/sources/` (drill). The three-tier reading order in `zeref-memory-protocol.md` directly follows this pattern.

---

## 2. claude-obsidian

| Field | Value |
|-------|-------|
| **Name** | claude-obsidian |
| **URL** | https://github.com/AgriciDaniel/claude-obsidian |
| **Type** | GitHub Repo |
| **Last reviewed** | 2026-05-11 |

### Why It Matters to Zeref

Claude-obsidian is a reference implementation of the Karpathy LLM Wiki pattern applied to Obsidian vaults. It demonstrates a working memory protocol with `hot.md`, `index.md`, and `log.md` as the core trio, plus hooks for restoring session context and maintaining continuity between environments.

**Key patterns extracted and adopted by Zeref:**
- `hot.md` as the mandatory first-read file — active session state, not a general dashboard.
- `log.md` as append-only — never edit the past, only add to the top.
- Single-writer discipline: the assistant writes wiki updates, not the human mid-session.
- Command-to-skill indirection: commands stay thin (entry points), skills and wiki pages hold durable logic.
- Memory restoration as an explicit operation, not an assumed capability.

**Zeref adoption note:** The prior Zeref Brain V1 report recommends treating claude-obsidian as a reference, not installing it as the live personal vault. The recommendation is to create a dedicated Zeref OS memory layer inside Yash's existing Obsidian vault rather than using the repo-vault directly. This wiki is that layer.

**Zeref divergence:** Zeref's wiki lives in a workspace folder (and eventually Obsidian), not inside the claude-obsidian repo structure. The patterns are adopted; the repo is not installed as-is.

---

## 3. Graphify

| Field | Value |
|-------|-------|
| **Name** | Graphify |
| **URL** | https://github.com/safishamsi/graphify |
| **Type** | GitHub Repo |
| **Last reviewed** | 2026-05-11 |

### Why It Matters to Zeref

Graphify converts folders of code, docs, papers, images, audio, and video into a structured knowledge graph. It produces three main artifacts: an interactive HTML visualization, `GRAPHREPORT.md`, and `graph.json`. For Zeref, this is the intended **Graph Layer** (Layer 4 of the 5-layer V2 architecture).

**Key patterns and features relevant to Zeref:**
- **Graph-first reading order:** Read `GRAPHREPORT.md` and `graph.json` before individual files — structural understanding without token waste.
- **Confidence labeling:** EXTRACTED / INFERRED / AMBIGUOUS — reduces hallucination risk by marking uncertainty explicitly.
- **Read-only MCP server:** Safe integration with Claude — Graphify serves structure without modification risk.
- **Multi-platform assistant skill installs:** Works with Claude, ChatGPT, and other LLM environments.
- **Cross-project global graph:** Combines multiple project graphs for system-wide structural recall.
- **Hook/watch/update flows:** Keeps graphs fresh without requiring full re-analysis every session.

**Zeref V2 roadmap for Graphify:**
- Phase 5: Run Graphify pilot on `zeref-skills-fleet/` folder first.
- Validate graph quality and GRAPHREPORT.md accuracy manually.
- Only add hooks and automation after manual validation confirms the baseline is correct.
- Eventually: global Zeref OS graph for cross-project retrieval.

**Zeref adoption note:** Graphify is a retrieval substrate, not a visualization toy. Its value to Zeref is reducing token waste by making the system read structure before raw files — the same philosophy as the Karpathy wiki pattern applied to folder-level navigation.

---

## 4. Tenfold Marketing Guides

| Field | Value |
|-------|-------|
| **Name** | Tenfold Marketing Free Resources / Claude Guides |
| **URLs** | https://guides.tenfoldmarketing.com/10k-website · https://guides.tenfoldmarketing.com/boris-cherny-10-claude-code-tips · https://guides.tenfoldmarketing.com/claude-code-usage-limits · https://guides.tenfoldmarketing.com/claude-design-skills |
| **Type** | Web Guides |
| **Last reviewed** | 2026-05-11 (partial — full text not extracted) |

### Why It Matters to Zeref

Tenfold's guides surface the principle that **many expensive AI wrappers can be replaced with direct, free or lower-cost workflows**. This directly supports Zeref's free-first policy.

**Key themes from available content:**
- Practical Claude Code usage without premium wrappers
- Free guides, automations, and skills as an alternative to paid SaaS
- MCP-style workflows using direct integrations
- Claude design skills applicable to Zeref's UI/UX skill layer

**Guides summary (partial — full extraction pending):**

| Guide | URL | Summary |
|-------|-----|---------|
| $10K Website | guides.tenfoldmarketing.com/10k-website | Building high-quality websites with Claude without paid page-builder subscriptions |
| 10 Claude Code Tips (Boris Cherny) | guides.tenfoldmarketing.com/boris-cherny-10-claude-code-tips | Expert Claude Code usage tips from a senior practitioner |
| Claude Code Usage Limits | guides.tenfoldmarketing.com/claude-code-usage-limits | Understanding and working within Claude's rate limits and context constraints |
| Claude Design Skills | guides.tenfoldmarketing.com/claude-design-skills | Claude-native design skill patterns for UX, UI, and visual work |

**Zeref note:** These guides are high-priority ingestion targets for the wiki. Their principles should become queryable memory pages rather than external URL references. Flag for full extraction in a future DOC session.

---

## 5. Zeref Skills Fleet Repo

| Field | Value |
|-------|-------|
| **Name** | Zeref Skills Fleet |
| **URL** | https://github.com/kanadhiayash/zeref-skills-fleet |
| **Type** | GitHub Repo (Yash's own) |
| **Last reviewed** | 2026-05-11 (sandbox copy inspected) |

### Why It Matters to Zeref

This is the live source of truth for the Zeref Skill Layer (Layer 2 of the V2 architecture). The repo contains the 112-skill fleet, plugin manifest, agents, commands, output styles, and themes.

**Current known state (from sandbox inspection 2026-05-11):**
- 112 skill folders validated (all contain SKILL.md, all passed `agentskills validate`)
- Plugin manifest at version 1.1.2
- 2 agents: `zeref-fleet-router.md`, `zeref-executive-qa-agent.md`
- 2 commands: `zeref-activate.md`, `zeref-package-release.md`
- 1 output style: `zeref-executive.md`
- 1 theme: `zeref-dark.json`

**Known gaps (as of V2 analysis):**
- Missing: `LICENSE`, `DISCLAIMER.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`
- Missing: machine-readable skill registry (`skills/registry.md`)
- Many skill descriptions too generic for precise routing
- Skill-level disclaimers missing for legal, financial, grant, security skills

**Next action:** Phase 1 of V2 rebuild closes the release governance gaps. Phase 3 builds the registry.

---

## 6. Zeref Command Center (Notion)

| Field | Value |
|-------|-------|
| **Name** | Zeref Skills Fleet Command Center |
| **URL** | https://copper-tv-288.notion.site/Zeref-Skills-Fleet-Command-Center-358d695d836a81af9f6adf30770217c3 |
| **Type** | Notion Page |
| **Last reviewed** | [Unknown — not confirmed live in current session] |

### Why It Matters to Zeref

This is the intended dashboard and command center for the Zeref fleet in Notion. Its current live state is unknown — it has not been read or confirmed in the current session.

**Zeref note:** Do not claim this Notion page contains any specific content until it is actually read via a connector. The URL is preserved here for reference. Confirm live state before using as a source of truth.

---

## 7. ByteByteGo System Design Reference

| Field | Value |
|-------|-------|
| **Name** | ByteByteGo — Scale from Zero to Millions of Users |
| **URL** | https://bytebytego.com/courses/system-design-interview/scale-from-zero-to-millions-of-users |
| **Type** | Course / Reference |
| **Last reviewed** | [Flagged as focused domain — not yet extracted] |

### Why It Matters to Zeref

Included as a focused domain reference for system design patterns applicable to Zeref's scaling philosophy and Yash's professional positioning as a systems scaler. Relevant for BIZ-register tasks, system architecture documentation, and technical interview preparation.

**Zeref note:** Extract relevant patterns into a dedicated concept page when preparing for technical interviews or system design work.

---

## Source Maintenance Rules

- **Review date:** Update `Last reviewed` whenever a source is fetched and confirmed current.
- **Stale threshold:** Sources not reviewed in 6+ months should be flagged for re-review.
- **Do not invent contents:** Never summarize a URL unless it was actually fetched and read in the session. Mark unread sources as `[Not yet extracted]`.
- **Add new sources** to both this page and to `wiki/index.md` (Sources section) in the same session.
