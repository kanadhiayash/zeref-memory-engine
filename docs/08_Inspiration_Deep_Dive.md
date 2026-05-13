# Zeref OS — Inspiration Deep Dive

**Version:** 2.0.0 | **Updated:** May 2026

---

## Overview

Zeref OS synthesizes principles from three sources that represent the frontier of human-AI collaboration and systems thinking. This document explains what was taken from each and why.

---

## Andrej Karpathy — The Discipline Layer

**Source:** Karpathy's public writing on LLM-assisted coding, his principles for working with AI agents, and his broader philosophy on software simplicity.

### Core principles adopted

**1. Think before coding**

Karpathy advocates for explicit reasoning before execution. Zeref implements this as:
- Task classification step before skill routing
- Explicit skill stack declaration before output
- "Risks / Unknowns" section at end of every major output

The practice forces deliberate problem framing rather than reactive generation.

**2. Simplicity first**

Karpathy's preference for the minimal implementation that solves the real problem is embedded in Zeref's "minimum useful stack" rule:
- 1 lead skill, never more than 3 support skills
- No speculative features
- No abstractions added before they're needed

The discipline: "Would this output be materially worse without this skill? If no, drop it."

**3. Surgical changes only**

When modifying code or systems, touch only what needs to change. Zeref's caveman plugin operationalizes this: the Cavecrew Builder subagent "hard refuses 3+ file scope." It forces the smallest possible intervention.

**4. Surface assumptions explicitly**

Karpathy's approach to debugging — state what you know vs. what you're inferring — is formalized in Zeref's anti-hallucination layer:

```
Facts: [things directly observed]
Assumptions: [things inferred, labeled [ASSUMPTION]]
Unknowns: [things needed but not available]
```

This prevents the confident-but-wrong behavior that makes AI-generated outputs unreliable.

**5. Verifiable success criteria**

Before starting any non-trivial task, Zeref defines what "done" looks like. Not "write the auth system" but "auth system: email + Google OAuth, error messages for all failure states, no token in AsyncStorage."

### The Karpathy influence in Zeref

Every skill's "Quality Gates" section is a direct implementation of this principle. Before handoff, verify against specific, checkable criteria — not vibes.

---

## Agrici — The Systems Layer

**Source:** Agrici's approach to AI operating systems, agent orchestration, and building AI execution engines that scale beyond single-task use.

### Core principles adopted

**1. Skills as modular specialists**

Agrici's insight: a single monolithic AI prompt degrades with complexity. The solution is modular specialist roles — each scoped, defined, and triggered by specific conditions.

Zeref's 112-skill architecture is a direct implementation. Each skill is:
- Scoped to a domain (not "write" but "write LinkedIn posts for personal branding")
- Triggered by specific phrases (not catch-all)
- Bounded by explicit anti-patterns (what it never does)

**2. The routing layer**

Rather than letting AI decide ad-hoc what to do, Agrici-style systems have explicit routing logic. Zeref's 3-step routing (classify → select stack → execute) turns routing from implicit behavior into a documented, debuggable process.

**3. Memory as operating context**

Agrici's principle: AI without memory is a series of disconnected transactions. Memory transforms tools into systems.

Zeref's hot.md + wiki architecture operationalizes this:
- hot.md = working RAM (current session)
- wiki/ = persistent storage (across sessions)
- log.md = audit trail (what happened and why)

**4. Execution handoffs**

Agrici emphasizes clean handoffs between agents and sessions — compact, precise, no ambiguity. The Caveman handoff format is this principle made concrete:

```
Objective → State → Files → Decisions → Risks → Commands → Next move
```

Seven fields. No narrative. Paste into next session, resume immediately.

**5. Proof of work, not just output**

The Agrici influence on Zeref's portfolio-first orientation: every major output should be portfolio-ready, GitHub-credible, or recruiter-visible. Execution that leaves no trace doesn't compound. Execution that produces artifacts does.

---

## Graphify — The Visualization Layer

**Source:** Graphify's approach to knowledge representation, graph-based memory, and turning AI outputs into navigable knowledge structures.

### Core principles adopted

**1. Knowledge as connected structure**

Graphify's core insight: isolated documents are dead weight. Knowledge that connects to other knowledge compounds over time.

Zeref's wiki is built on this principle. Every project page links to decision logs. Decision logs link to source material. Source material links to learnings. The structure means that a question asked in month 6 can surface a decision made in month 2.

**2. The index as navigation layer**

Graphify's solution to search fatigue: before search, have an index. `wiki/index.md` is Zeref's implementation — a human-readable map of all wiki content, updated when new pages are added.

**3. Domain pages vs. session notes**

Graphify distinguishes between ephemeral session content and durable domain knowledge. Zeref implements this as hot.md (ephemeral) vs. wiki/ subdirectories (durable).

The discipline: if information will still matter in 3 months, it belongs in a domain page, not the session log.

**4. Tags and metadata for retrieval**

Graphify's retrieval design: metadata on documents enables targeted recall without full-text search. Zeref's wiki pages include frontmatter:

```markdown
---
project: journaling-app
type: decisions
date: 2026-05
status: active
---
```

This enables Dataview queries in Obsidian: "show all active project decisions from Q2."

**5. Graph traversal over linear recall**

Graphify's insight that memory is most useful when you can traverse from a concept to related concepts — not just retrieve an isolated fact.

In practice: when Zeref reads about a project, it should be able to surface: related decisions, related resources, related persona research. The wiki link structure makes this traversal possible.

---

## Synthesis: What Zeref OS Combines

| Principle | Source | Implementation in Zeref |
|-----------|--------|------------------------|
| Think before acting | Karpathy | Task classification + explicit routing before output |
| Minimum viable complexity | Karpathy | 1 lead + 0-3 support + 0-1 QA gate |
| Surgical changes | Karpathy | Cavecrew Builder hard limit, skill anti-patterns |
| Modular specialists | Agrici | 112 skills, each scoped and triggered |
| Explicit routing | Agrici | 3-step classification → stack selection → execution |
| Session memory | Agrici | hot.md read-first protocol |
| Proof of work compounding | Agrici | Portfolio-first output orientation |
| Connected knowledge | Graphify | wiki/ link structure, Obsidian backlinks |
| Domain vs. session memory | Graphify | hot.md (ephemeral) vs. wiki/ (durable) |
| Metadata for retrieval | Graphify | Frontmatter on wiki pages |

---

## What Wasn't Taken

**From Karpathy:** The academic depth. Karpathy's work goes deep into neural network internals, training dynamics, and ML research. Zeref is a practitioner tool — the philosophy without the research infrastructure.

**From Agrici:** Enterprise-scale multi-agent orchestration. Agrici's full vision involves dozens of specialized agents running in parallel with complex state management. Zeref is a single-model system with routing logic, not true multi-agent.

**From Graphify:** Full knowledge graph infrastructure. True graph memory with vector embeddings, semantic search, and automated link suggestion would require external tooling. Zeref uses a markdown-based approximation.

The goal was the best of each source that could be implemented with Claude + local files + MCP connectors — no external services, no API keys, no maintenance overhead beyond what the user already has.

---

## Further Reading

- Karpathy's writing: [karpathy.ai](https://karpathy.ai) and [@karpathy](https://twitter.com/karpathy)
- Model Context Protocol spec: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- Obsidian documentation: [obsidian.md/help](https://obsidian.md/help)

---

## Next Steps

- [09_Notion_Dashboard.md](09_Notion_Dashboard.md) — Build the command center
- [05_Memory_System.md](05_Memory_System.md) — Full memory system documentation
