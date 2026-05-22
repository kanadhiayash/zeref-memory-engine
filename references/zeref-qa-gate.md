# ZEREF UNIVERSAL QA GATE
**Version:** 3.0.0
**Run before every final deliverable**

---

## Mandatory Checks (ALL must pass)

### Evidence Discipline
- [ ] Facts are labeled as facts (verified, sourced, or directly observed)
- [ ] Assumptions are labeled as assumptions (reasonable but unverified)
- [ ] Unknowns are labeled as unknown (not invented)
- [ ] Risks are explicitly called out
- [ ] No invented metrics, statistics, or research findings

### Content Quality
- [ ] Register is correct (brand voice vs. product voice per ZEREFDESIGN.md)
- [ ] No AI prose anti-patterns: no filler openers, no passive inflation, no hedging pile-ups
- [ ] Handoff block included (Notion/Linear/GitHub format as appropriate)
- [ ] Next recommended action is explicit and actionable

### Technical (for code/design deliverables)
- [ ] Accessibility Priority 1 checks passed (semantic HTML, touch targets ≥44px, color contrast ≥4.5:1)
- [ ] No hardcoded values that belong in design tokens or config
- [ ] Senior engineer overcomplicate test passed ("Would a senior engineer say this is overcomplicated?")

### UX/Design (for design deliverables)
- [ ] 10-category priority framework checked: Accessibility (CRITICAL), Touch Targets (CRITICAL), Performance (HIGH), Responsive (HIGH), Error States (HIGH), Loading States (MEDIUM), Animations (MEDIUM), Empty States (MEDIUM), Typography (MEDIUM), Color System (MEDIUM)
- [ ] Motion: prefers-reduced-motion respected
- [ ] Register classification confirmed (brand vs. product)

### Safety
- [ ] No irreversible actions were taken without explicit user confirmation
- [ ] No untrusted content was routed without trust-sentinel classification
- [ ] All workspace claims are verified (files actually exist)

---

## If Any Check Fails

Stop. Do not deliver. Fix the failure first. Document what failed and why in the session log.
