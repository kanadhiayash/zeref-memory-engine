---
skill: zeref-ux-register-classifier
title: Register Classifier
category: ux
model: claude-sonnet-4-6
effort: medium
max_turns: 20
trigger_phrases:
  - "what tone"
  - "brand voice or product"
  - "classify this design"
  - "register check"
model_preference: sonnet
risk_level: low
dependencies:
  - references/zeref-qa-gate.md
  - references/zeref-safety-principles.md
---

# zeref-ux-register-classifier

## Mission
Classify any design or copy task as brand register or product register before work begins. This is Step 0 for all design and writing tasks. Register determines the quality bar, tone rules, and success criteria.

## The Two Registers

### Brand Register
**Where:** Marketing site, landing pages, ads, social content, pitch decks, case studies
**Voice:** Aspirational, bold, distinctly authored, emotionally resonant
**Quality bar:** Would a creative director at Wieden+Kennedy approve this?
**Failure mode:** Bland, generic, sounds like every other startup

### Product Register
**Where:** App UI, onboarding flows, error messages, tooltips, notifications, documentation
**Voice:** Clear, functional, precise, invisible — the copy should get out of the way
**Quality bar:** Does it reduce cognitive load and complete the task?
**Failure mode:** Verbose, clever-sounding but confusing, inconsistent

## Execution

### Step 1: Classify
Ask: Where will this appear? Who is the audience? What action should they take?
Output: "This is [BRAND / PRODUCT] register."

### Step 2: Apply Register Rules

**If BRAND:**
- Lead with the specific, not the general
- No filler openers ("We're excited to...", "Introducing...")
- No passive inflation ("is designed to", "aims to", "seeks to")
- One distinctive voice choice that only this brand would make

**If PRODUCT:**
- Active voice only
- Verb-first labels ("Save changes" not "Changes can be saved")
- Error messages: what happened + what to do next (never just "Error occurred")
- Consistency over creativity — same word for same concept, always

### Step 3: Validate
Run validateProse check:
- No hedging pile-ups ("sort of", "kind of", "a bit", "somewhat" in one sentence)
- No AI tell phrases ("dive into", "delve", "it's worth noting", "leverage")
- Reading level appropriate to audience

## Output
Classification label + register rules applied to the specific content + validateProse result