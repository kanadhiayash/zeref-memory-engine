#!/usr/bin/env python3
"""
upgrade_frontmatter.py — Zeref v3.0.0 Skill Frontmatter Upgrade
Upgrades all 104 skills from thin v2 frontmatter to rich v3 frontmatter.
Run: python3 scripts/upgrade_frontmatter.py
"""

import os
import re
from pathlib import Path

FLEET_ROOT = Path(__file__).parent.parent
SKILLS_DIR = FLEET_ROOT / "skills"

# Category → model preference and effort defaults
CATEGORY_DEFAULTS = {
    "biz":    {"model": "claude-sonnet-4-6", "model_preference": "sonnet", "effort": "high", "max_turns": 25, "risk_level": "medium"},
    "cnt":    {"model": "claude-sonnet-4-6", "model_preference": "sonnet", "effort": "medium", "max_turns": 20, "risk_level": "low"},
    "dev":    {"model": "claude-sonnet-4-6", "model_preference": "sonnet", "effort": "high", "max_turns": 30, "risk_level": "high"},
    "final":  {"model": "claude-opus-4-7",   "model_preference": "opus",   "effort": "high", "max_turns": 25, "risk_level": "low"},
    "hq":     {"model": "claude-opus-4-7",   "model_preference": "opus",   "effort": "high", "max_turns": 25, "risk_level": "medium"},
    "mkt":    {"model": "claude-sonnet-4-6", "model_preference": "sonnet", "effort": "medium", "max_turns": 20, "risk_level": "low"},
    "qa":     {"model": "claude-sonnet-4-6", "model_preference": "sonnet", "effort": "medium", "max_turns": 20, "risk_level": "low"},
    "system": {"model": "claude-haiku-4-5-20251001", "model_preference": "haiku", "effort": "low", "max_turns": 10, "risk_level": "low"},
    "ux":     {"model": "claude-sonnet-4-6", "model_preference": "sonnet", "effort": "medium", "max_turns": 20, "risk_level": "low"},
}

# Override models for complex dev skills
OPUS_SKILLS = {
    "zeref-dev-technical-architect", "zeref-dev-solution-architect",
    "zeref-dev-ai-systems-engineer", "zeref-dev-agentic-workflow-engineer",
    "zeref-dev-security-engineer", "zeref-dev-database-architect",
}

# Trigger phrase map — natural language phrases that should route to each skill
TRIGGER_PHRASES = {
    # BIZ
    "zeref-biz-business-strategist":           ["business strategy", "strategic plan", "go to market", "business model"],
    "zeref-biz-business-validator":            ["validate business", "is this viable", "business case", "feasibility"],
    "zeref-biz-competitive-intelligence-analyst": ["competitor analysis", "competitive landscape", "market positioning", "benchmark competitors"],
    "zeref-biz-financial-analyst":             ["financial model", "unit economics", "revenue forecast", "P&L", "budget"],
    "zeref-biz-investor-pitch-strategist":     ["investor pitch", "fundraising deck", "pitch strategy", "raise capital"],
    "zeref-biz-kpi-analyst":                   ["KPI", "metrics", "north star", "measure success", "analytics dashboard"],
    "zeref-biz-legal-advisor":                 ["legal review", "contract", "terms of service", "compliance", "legal risk"],
    "zeref-biz-market-research-analyst":       ["market research", "market size", "TAM SAM SOM", "industry analysis"],
    "zeref-biz-monetization-strategist":       ["monetization", "pricing model", "revenue streams", "how to charge"],
    "zeref-biz-operations-strategist":         ["operations", "process design", "workflow optimization", "ops strategy"],
    "zeref-biz-opportunity-solution-analyst":  ["opportunity-solution tree", "discovery", "what should we build", "prioritize features"],
    "zeref-biz-partnership-strategist":        ["partnerships", "business development", "BD strategy", "strategic alliances"],
    "zeref-biz-product-market-fit-analyst":    ["product market fit", "PMF", "retention", "churn", "user engagement"],
    "zeref-biz-risk-analyst":                  ["risk assessment", "risk mitigation", "SWOT", "identify risks"],
    "zeref-biz-startup-operator":              ["startup", "zero to one", "early stage", "MVP launch", "founder"],
    # CNT
    "zeref-cnt-brand-voice-editor":            ["brand voice", "tone of voice", "editorial guidelines", "rewrite in brand voice"],
    "zeref-cnt-case-study-writer":             ["case study", "portfolio piece", "project writeup", "document this project"],
    "zeref-cnt-content-qa-editor":             ["proofread", "copy edit", "review this content", "check grammar"],
    "zeref-cnt-copywriter":                    ["write copy", "marketing copy", "headline", "landing page copy", "ad copy"],
    "zeref-cnt-documentation-writer":          ["write documentation", "README", "technical docs", "user guide"],
    "zeref-cnt-editorial-director":            ["editorial strategy", "content calendar", "publishing plan", "content direction"],
    "zeref-cnt-linkedin-ghostwriter":          ["LinkedIn post", "LinkedIn content", "thought leadership post", "write for LinkedIn"],
    "zeref-cnt-long-form-writer":              ["blog post", "article", "long form", "essay", "Substack"],
    "zeref-cnt-presentation-designer":         ["presentation", "slide deck", "pitch deck structure", "keynote outline"],
    "zeref-cnt-repurposing-specialist":        ["repurpose content", "turn this into", "adapt for", "content repurposing"],
    "zeref-cnt-resume-career-writer":          ["resume", "CV", "cover letter", "job application", "career document"],
    "zeref-cnt-scriptwriter":                  ["script", "video script", "podcast script", "explainer video"],
    "zeref-cnt-seo-content-writer":            ["SEO content", "keyword-optimized", "search traffic", "organic content"],
    "zeref-cnt-ux-case-study-writer":          ["UX case study", "design case study", "portfolio case study"],
    "zeref-cnt-video-content-strategist":      ["video strategy", "YouTube", "content strategy", "video marketing"],
    # DEV
    "zeref-dev-agentic-workflow-engineer":     ["agentic workflow", "AI agent", "LLM pipeline", "MCP", "multi-agent"],
    "zeref-dev-ai-systems-engineer":           ["AI system", "ML pipeline", "model integration", "AI architecture"],
    "zeref-dev-api-integration-engineer":      ["API integration", "REST API", "webhook", "third-party API", "connect services"],
    "zeref-dev-backend-engineer":              ["backend", "server-side", "Node.js", "Python backend", "API endpoint"],
    "zeref-dev-cloud-infrastructure-engineer": ["cloud infrastructure", "Firebase", "Supabase", "serverless", "deployment"],
    "zeref-dev-code-quality-reviewer":         ["code review", "review this code", "code quality", "refactor", "clean code"],
    "zeref-dev-database-architect":            ["database design", "schema", "data model", "SQL", "NoSQL", "query"],
    "zeref-dev-devops-engineer":               ["DevOps", "CI/CD", "GitHub Actions", "deployment pipeline", "Docker"],
    "zeref-dev-frontend-engineer":             ["frontend", "React", "Vue", "CSS", "UI component", "frontend code"],
    "zeref-dev-fullstack-engineer":            ["fullstack", "build this feature", "full stack", "end to end"],
    "zeref-dev-mobile-engineer":               ["mobile app", "React Native", "Expo", "iOS", "Android", "SwiftUI"],
    "zeref-dev-security-engineer":             ["security", "auth", "authentication", "vulnerability", "OWASP"],
    "zeref-dev-solution-architect":            ["solution architecture", "system design", "architecture decision", "tech stack"],
    "zeref-dev-technical-architect":           ["technical architecture", "system design", "architecture review", "tech strategy"],
    "zeref-dev-test-engineer":                 ["testing", "unit tests", "integration tests", "test strategy", "Jest", "pytest"],
    "zeref-dev-ui-quality-enforcer":           ["UI audit", "review the interface", "accessibility audit", "touch targets", "UI quality"],
    # FINAL
    "zeref-final-deliverable-packager":        ["package deliverable", "compile output", "final package", "export ready"],
    "zeref-final-executive-reviewer":          ["final review", "executive review", "approve this", "ready to ship", "QA gate"],
    "zeref-final-project-compiler":            ["compile project", "project summary", "final compilation", "wrap up"],
    "zeref-final-source-validator":            ["validate sources", "check citations", "source verification", "fact check"],
    # HQ
    "zeref-hq-chief-of-staff":                ["chief of staff", "cross-functional", "priorities", "weekly agenda"],
    "zeref-hq-chief-product-officer":         ["product direction", "CPO", "product strategy", "roadmap", "product decision"],
    "zeref-hq-chief-research-officer":        ["research strategy", "synthesize research", "research direction"],
    "zeref-hq-chief-strategy-officer":        ["strategy", "CSO", "strategic direction", "long-term strategy"],
    "zeref-hq-documentation-architect":       ["documentation architecture", "docs structure", "knowledge base design"],
    # MKT
    "zeref-mkt-analytics-specialist":         ["marketing analytics", "attribution", "campaign performance", "conversion"],
    "zeref-mkt-brand-strategist":             ["brand strategy", "brand positioning", "brand identity", "brand direction"],
    "zeref-mkt-chief-marketing-strategist":   ["marketing strategy", "CMO", "marketing plan", "growth marketing"],
    "zeref-mkt-community-strategist":         ["community building", "Discord", "community strategy", "user community"],
    "zeref-mkt-content-marketing-strategist": ["content marketing", "content strategy", "content plan", "editorial calendar"],
    "zeref-mkt-conversion-rate-optimizer":    ["CRO", "conversion rate", "optimize landing page", "A/B test copy"],
    "zeref-mkt-email-marketing-specialist":   ["email marketing", "email campaign", "newsletter", "drip sequence"],
    "zeref-mkt-growth-marketer":              ["growth hacking", "growth experiment", "user acquisition", "growth loop"],
    "zeref-mkt-gtm-strategist":               ["go to market", "GTM", "launch strategy", "product launch"],
    "zeref-mkt-performance-marketing-specialist": ["paid ads", "Google Ads", "Meta Ads", "performance marketing", "ROAS"],
    "zeref-mkt-personal-branding-strategist": ["personal brand", "thought leadership", "online presence", "personal branding"],
    "zeref-mkt-positioning-strategist":       ["positioning", "differentiation", "competitive positioning", "value prop"],
    "zeref-mkt-pr-communications-specialist": ["PR", "press release", "media relations", "communications", "public relations"],
    "zeref-mkt-seo-strategist":               ["SEO", "keyword research", "search ranking", "organic traffic", "on-page SEO"],
    "zeref-mkt-social-media-strategist":      ["social media", "Instagram", "Twitter", "TikTok", "social strategy"],
    # QA
    "zeref-qa-ab-testing-strategist":         ["A/B test", "experiment design", "hypothesis", "split test"],
    "zeref-qa-accessibility-tester":          ["accessibility test", "WCAG", "screen reader", "a11y audit"],
    "zeref-qa-edge-case-tester":              ["edge cases", "what could go wrong", "boundary testing"],
    "zeref-qa-final-quality-gatekeeper":      ["quality gate", "final QA", "approve before shipping"],
    "zeref-qa-functional-tester":             ["functional testing", "test this feature", "manual QA"],
    "zeref-qa-launch-readiness-manager":      ["launch readiness", "pre-launch checklist", "ready to launch"],
    "zeref-qa-performance-tester":            ["performance test", "load test", "lighthouse", "speed audit"],
    "zeref-qa-regression-tester":             ["regression test", "test after changes", "did this break anything"],
    "zeref-qa-security-tester":               ["security test", "penetration test", "vulnerability scan"],
    "zeref-qa-ui-consistency-auditor":        ["UI consistency", "design consistency audit", "visual QA"],
    "zeref-qa-ux-usability-tester":           ["usability test", "user test", "task analysis", "UX audit"],
    # SYSTEM
    "zeref-system-caveman-compressor":        ["compress this", "caveman", "shorten context", "handoff", "save session"],
    "zeref-system-evidence-memory-keeper":    ["save evidence", "log finding", "record this decision", "evidence map"],
    "zeref-system-live-researcher":           ["research this", "find information", "web research", "look up", "investigate"],
    "zeref-system-marketplace-packager":      ["marketplace listing", "package for marketplace", "publish plugin"],
    "zeref-system-memory-ingest":             ["save to wiki", "save session", "log this", "remember this", "update wiki"],
    "zeref-system-memory-lint":               ["clean up wiki", "lint memory", "check wiki health", "wiki audit"],
    "zeref-system-plugin-update-diagnostician": ["plugin update", "diagnose plugin", "plugin issue", "update diagnostic"],
    "zeref-system-skill-router":              ["route this task", "which skill", "what skill should"],
    "zeref-system-token-budget-controller":   ["token budget", "reduce tokens", "context length", "slim down"],
    # UX
    "zeref-ux-accessibility-specialist":      ["accessibility", "a11y", "WCAG", "screen reader", "accessible design"],
    "zeref-ux-design-qa-auditor":             ["design QA", "audit this design", "design review", "design issues"],
    "zeref-ux-design-systems-architect":      ["design system", "component library", "design tokens", "style guide"],
    "zeref-ux-developer-handoff-lead":        ["developer handoff", "design specs", "Figma handoff", "implementation notes"],
    "zeref-ux-figma-architecture-specialist": ["Figma architecture", "component structure", "Figma organization"],
    "zeref-ux-information-architect":         ["information architecture", "IA", "navigation structure", "site map"],
    "zeref-ux-interaction-designer":          ["interaction design", "micro-interactions", "animation", "motion design"],
    "zeref-ux-live-researcher":               ["live research", "user research now", "research this", "find user insights"],
    "zeref-ux-motion-designer":               ["motion design", "animation spec", "Lottie", "Framer motion", "transitions"],
    "zeref-ux-persona-strategist":            ["user personas", "persona development", "user profiles", "who are our users"],
    "zeref-ux-problem-definition-specialist": ["define the problem", "problem statement", "HMW", "user pain points"],
    "zeref-ux-product-designer":              ["product design", "design this screen", "wireframe", "UI design", "app design"],
    "zeref-ux-prototype-specialist":          ["prototype", "interactive prototype", "clickable mockup", "test prototype"],
    "zeref-ux-register-classifier":           ["what tone", "brand voice or product", "classify this design", "register check"],
    "zeref-ux-research-lead":                 ["user research", "interview plan", "research strategy", "user insights"],
    "zeref-ux-synthetic-research-analyst":    ["synthetic research", "simulate users", "synthetic personas"],
    "zeref-ux-user-flow-designer":            ["user flow", "task flow", "user journey map", "flow diagram"],
    "zeref-ux-visual-designer":               ["visual design", "colors", "typography", "brand aesthetics", "visual style"],
    "zeref-ux-writer":                        ["UX writing", "microcopy", "UI copy", "error messages", "button labels"],
}

def get_category(skill_name):
    """Extract category from skill name prefix."""
    parts = skill_name.replace("zeref-", "").split("-")
    return parts[0] if parts else "system"

def get_title(skill_name):
    """Convert skill slug to human-readable title."""
    suffix = skill_name.replace("zeref-", "")
    parts = suffix.split("-")[1:]  # drop category prefix
    return " ".join(word.capitalize() for word in parts)

def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown file."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("---", 3)
    if end == -1:
        return {}, content
    fm_text = content[3:end].strip()
    body = content[end+3:].strip()
    fm = {}
    for line in fm_text.split("\n"):
        if ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm, body

def build_new_frontmatter(skill_name, existing_fm):
    """Build the v3.0 frontmatter block."""
    category = get_category(skill_name)
    title = get_title(skill_name)
    defaults = CATEGORY_DEFAULTS.get(category, CATEGORY_DEFAULTS["system"])

    # Override to Opus for complex dev skills
    if skill_name in OPUS_SKILLS:
        model = "claude-opus-4-7"
        model_pref = "opus"
    else:
        model = defaults["model"]
        model_pref = defaults["model_preference"]

    triggers = TRIGGER_PHRASES.get(skill_name, [skill_name.split("-")[-1].replace("-", " ")])
    trigger_yaml = "\n".join(f'  - "{t}"' for t in triggers)

    desc = existing_fm.get("description", f"Zeref {title} specialist skill.")
    # Clean up multi-line description
    desc = desc.replace(">", "").replace("\n", " ").strip()
    if len(desc) > 200:
        desc = desc[:197] + "..."

    return f"""---
skill: {skill_name}
title: {title}
category: {category}
model: {model}
effort: {defaults['effort']}
max_turns: {defaults['max_turns']}
trigger_phrases:
{trigger_yaml}
model_preference: {model_pref}
risk_level: {defaults['risk_level']}
dependencies:
  - references/zeref-qa-gate.md
  - references/zeref-safety-principles.md
---"""

def upgrade_skill(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return f"  SKIP (no SKILL.md): {skill_dir.name}"

    content = skill_md.read_text(encoding="utf-8")
    skill_name = skill_dir.name

    existing_fm, body = parse_frontmatter(content)
    new_fm = build_new_frontmatter(skill_name, existing_fm)
    new_content = new_fm + "\n\n" + body
    skill_md.write_text(new_content, encoding="utf-8")
    return f"  ✅ {skill_name}"

# ─── Run ─────────────────────────────────────────────────────────────────────

skill_dirs = sorted([d for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")])
print(f"\n🔧 Upgrading frontmatter for {len(skill_dirs)} skills...\n")

results = [upgrade_skill(d) for d in skill_dirs]
for r in results:
    print(r)

passed = sum(1 for r in results if "✅" in r)
skipped = sum(1 for r in results if "SKIP" in r)
print(f"\n✅ Upgraded: {passed} | Skipped: {skipped} | Total: {len(results)}")
print("Frontmatter upgrade complete.\n")
