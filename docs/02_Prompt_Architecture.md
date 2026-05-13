# Zeref OS — Prompt Architecture

**Version:** 2.0.0 | **Updated:** May 2026

---

## Overview

Zeref OS uses a **5-layer instruction hierarchy**. Each layer has a defined scope, authority level, and override behavior. Understanding this architecture is essential for debugging unexpected behavior and for building custom skill extensions.

```
Layer 5 (Highest Authority)  →  Safety, Privacy, Security
Layer 4                       →  User's explicit request (this conversation)
Layer 3                       →  Project Instructions / CLAUDE.md (Zeref OS)
Layer 2                       →  Global Instructions (ZerefClaude.md)
Layer 1 (Lowest Authority)    →  Skill Files (domain specialists)
```

When layers conflict, higher authority wins. Conflicts are surfaced explicitly — Zeref never silently resolves them.

---

## Layer 5 — Safety & Security (Non-Negotiable)

**What it covers:**
- Irreversible destructive operations (never execute without explicit confirmation)
- Privacy (never expose credentials, personal data, or internal paths to output)
- Security (never generate exploits, malicious code, or deceptive content)
- Tool honesty (never claim a tool was called when it wasn't)

**Override behavior:** Cannot be overridden by any lower layer. Safety rules persist even if user explicitly requests otherwise.

**Example:**
```
User: "Delete everything in the wiki folder"
Zeref: [Pauses] "This will permanently delete all files in wiki/. Cannot be undone. Confirm?"
```

---

## Layer 4 — User's Explicit Request

**What it covers:**
The actual task stated in the current conversation turn.

**Override behavior:** Overrides Layers 1–3 for task-specific behavior. Cannot override Layer 5.

**Example:**
```
User: "Respond without using any skill routing headers"
→ Zeref suppresses routing display for this session, even though Layer 3 enables it by default
```

---

## Layer 3 — Project Instructions (ZEREFOS.md / CLAUDE.md)

**What it covers:**
- Core identity (Zeref as CEO-level execution partner)
- Routing rules (smallest useful stack)
- Output formats (Small Task Mode vs. Major Task Mode)
- Memory protocol (read hot.md, write to wiki)
- Evidence discipline (never invent, always verify)
- Workspace update rules

**Override behavior:** Overrides Layer 2 defaults. Applied to every response unless Layer 4 explicitly suspends it.

**Where it lives:**
- Claude Project: Project Instructions field
- Claude Code: `CLAUDE.md` at repo root or `~/.claude/CLAUDE.md`
- Cowork: System instructions

**Key rules enforced at this layer:**

```
1. Read hot.md before every major task
2. Use smallest useful skill stack (1 lead + 0-3 support + 0-1 QA)
3. Never invent: workspace updates, connector access, file contents, metrics
4. Produce copy-paste-ready outputs
5. End major tasks with workspace update recommendations
6. Suggest memory file for any significant output
```

---

## Layer 2 — Global Instructions (ZerefClaude.md)

**What it covers:**
- User identity (Yash Kanadhia, Toronto, early-career UX/Product Designer)
- Long-term goals (systems scaler, professional positioning)
- Default behavior (structured, concise, actionable)
- Tone preferences (no generic advice, no over-explanation)
- Core transformation chain (Chaos → Systems → Execution → Proof → Opportunity → Leverage)

**Override behavior:** Provides defaults. Overridden by Layers 3–4 for specific behaviors.

**Where it lives:**
- `_templates/ZerefClaude.md` in repo
- Pasted into Claude's global instructions or system prompt
- In Cowork: user preferences section

---

## Layer 1 — Skill Files

**What it covers:**
- Domain-specific behavior for each of 112 specialists
- Output formats for that skill's deliverables
- Quality gates specific to that domain
- Triggers that activate the skill

**Override behavior:** Lowest authority. Skills adapt to Layers 2–4 constraints. A skill can never override routing rules, memory protocol, or safety rules.

**Skill file location:** `skills/` directory, organized by layer prefix:

```
skills/
  zeref-hq-*/          ← Executive layer (8 skills)
  zeref-ux-*/          ← UX/Design layer (16 skills)
  zeref-dev-*/         ← Development layer (17 skills)
  zeref-biz-*/         ← Business layer (14 skills)
  zeref-mkt-*/         ← Marketing layer (16 skills)
  zeref-cnt-*/         ← Content layer (16 skills)
  zeref-qa-*/          ← QA layer (15 skills)
  zeref-final-*/       ← Final delivery layer (4 skills)
  zeref-system-*/      ← System infrastructure (6 skills)
```

---

## How Routing Works

When a task arrives, Zeref runs a 3-step routing decision:

### Step 1 — Task Classification
Classify the task type:

| Task Type | Lead Layer |
|-----------|-----------|
| Strategy, positioning, market | `biz` |
| UX flows, design systems, research | `ux` |
| Code, architecture, debugging | `dev` |
| Writing, content, ghostwriting | `cnt` |
| GTM, growth, campaigns | `mkt` |
| Testing, auditing, QA | `qa` |
| Cross-functional strategy | `hq` |
| Final packaging, delivery | `final` |

### Step 2 — Select Minimum Stack
```
Lead skill: 1 (always)
Support skills: 0–3 (only if they materially improve output)
QA gate: 0–1 (only for portfolio-facing, recruiter-facing, or shipping-critical output)
```

**Decision rule for support skills:**
> "Would the output be materially worse without this skill? If yes, include it. If no, exclude it."

**Decision rule for QA gate:**
> "Would a quality defect in this output damage professional positioning or cause rework? If yes, gate it."

### Step 3 — Execute with Explicit Routing
Output format for major tasks:

```
Lead: zeref-ux-product-designer
Support: zeref-biz-business-strategist, zeref-dev-frontend-engineer
QA: zeref-qa-final-quality-gatekeeper
---
[Output here]
---
Quality check: [what was verified]
Risks: [what was not verified]
Next move: [recommended next step]
```

---

## Instruction Conflict Resolution

When layers conflict, Zeref follows this protocol:

1. **Identify the conflict** — State which layers are in tension
2. **Apply hierarchy** — Higher layer wins
3. **Surface the conflict** — Tell the user what was overridden and why
4. **Proceed** — Don't stall, don't silently pick one

**Example:**
```
Skill file says: "Always include a full competitive analysis"
User says: "Keep this response under 200 words"
→ Layer 4 (user request) overrides Layer 1 (skill default)
→ Zeref: "Keeping to 200 words as requested — competitive analysis abbreviated"
```

---

## Memory Protocol Integration

The prompt architecture integrates with the memory system:

```
Session Start:
  → Read wiki/hot.md
  → Load active project context
  → Check pending decisions

During Session:
  → Apply Layer 3 routing rules
  → Use Layer 1 skills as needed
  → Track decisions and outputs

Session End:
  → Update wiki/hot.md with current state
  → Append to wiki/log.md
  → Suggest which memory files need updating
```

See [05_Memory_System.md](05_Memory_System.md) for full protocol.

---

## Debugging Unexpected Behavior

If Zeref behaves unexpectedly, check layers in order:

| Symptom | Likely Layer | Check |
|---------|-------------|-------|
| Wrong skill being used | Layer 3 | Check routing rules in ZEREFOS.md |
| Ignoring skill output format | Layer 4 | User request may be overriding skill defaults |
| Not reading hot.md | Layer 3 | Confirm memory protocol in project instructions |
| Using wrong tone | Layer 2 | Check ZerefClaude.md global instructions |
| Refusing valid task | Layer 5 | Safety rule triggered — check if task triggers irreversible action check |
| Skill not activating | Layer 1 | Check skill trigger phrases in skill file |

**Validation command:**
```bash
python zeref-validate.py --verbose
```

---

## Extending the Architecture

### Adding a new layer
Not recommended — the 5-layer system covers all cases. If you need project-specific behavior, add it to Layer 3 (CLAUDE.md) with a comment explaining the override.

### Adding skills within a layer
See [03_Skills_Fleet_Guide.md#custom-skills](03_Skills_Fleet_Guide.md#custom-skills).

### Overriding a skill's default behavior for a project
Add override rules to your project CLAUDE.md:

```markdown
## Skill Overrides
- zeref-cnt-copywriter: Always write in first person
- zeref-qa-lead: Skip functional testing for prototype deliverables
```

---

## Next Steps

- [03_Skills_Fleet_Guide.md](03_Skills_Fleet_Guide.md) — All 112 skills mapped
- [05_Memory_System.md](05_Memory_System.md) — How memory integrates with prompt layers
