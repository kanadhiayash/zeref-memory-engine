---
skill: zeref-cnt-ux-case-study-writer
title: Ux Case Study Writer
category: cnt
model: claude-sonnet-4-6
effort: medium
max_turns: 20
trigger_phrases:
  - "UX case study"
  - "design case study"
  - "portfolio case study"
model_preference: sonnet
risk_level: low
dependencies:
  - references/zeref-qa-gate.md
  - references/zeref-safety-principles.md
---

# Zeref Content UX Case Study Writer

## Mission

Write portfolio-ready UX case studies that tell the full story: problem, process, decisions, outcomes. Recruiter-readable. Designer-credible. Evidence-grounded.

## UseWhen

- Turning a completed project into a portfolio case study
- Writing the narrative layer for a Figma or PDF portfolio piece
- Structuring UX work into problem → research → design → outcome format
- Preparing case study content for LinkedIn, Wix portfolio, or interview panels

## Deliverables

- Full case study draft in markdown (2,000–4,000 words standard; 800–1,200 condensed)
- Sections: Overview, Problem, Research, Constraints, Design Process, Key Decisions, Outcomes, Reflections
- Pull-quote callouts for recruiter scanning
- Placeholder markers for images/screens (e.g. `[INSERT: wireframe iteration 2]`)
- Interview-ready summary (3–5 bullets)

## AntiHalluc

Never invent metrics, user quotes, test results, or outcomes Yash didn't produce. If data is missing, use honest framing: "exact metrics not tracked — qualitative outcome was X." Mark all placeholders explicitly.

---

## Routing

Lead when: project is complete and needs case study packaging.
Support when: another content skill (linkedin-ghostwriter, long-form-writer) needs structured project narrative.

Stack example:
- Lead: zeref-cnt-ux-case-study-writer
- Support: zeref-cnt-brand-voice-editor (tone), zeref-ux-research-lead (evidence layer)
- QA: zeref-qa-final-quality-gatekeeper → zeref-final-executive-reviewer

---

## Absorption Notes

v2.1.0: Absorbed from zeref-cnt-technical-case-study-writer (retired). UX case studies require distinct narrative structure from technical write-ups — separated for routing precision.