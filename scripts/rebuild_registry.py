#!/usr/bin/env python3
"""
rebuild_registry.py — Regenerate zeref-skill-registry.json from skill frontmatter
Version: 3.0.0
Run: python3 scripts/rebuild_registry.py
"""

import json
import re
from pathlib import Path
from datetime import date

FLEET_ROOT = Path(__file__).parent.parent
SKILLS_DIR = FLEET_ROOT / "skills"
REGISTRY_PATH = FLEET_ROOT / "registry" / "zeref-skill-registry.json"

def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    fm_text = match.group(1)
    result = {}

    # skill / name / title / category / model / effort / max_turns
    for field in ["skill", "title", "category", "model", "effort", "model_preference", "risk_level"]:
        m = re.search(rf'^{field}:\s*(.+)$', fm_text, re.MULTILINE)
        if m:
            result[field] = m.group(1).strip()

    # max_turns (int)
    m = re.search(r'^max_turns:\s*(\d+)', fm_text, re.MULTILINE)
    if m:
        result["max_turns"] = int(m.group(1))

    # trigger_phrases (list)
    tp_match = re.search(r'^trigger_phrases:\n((?:  - .+\n?)+)', fm_text, re.MULTILINE)
    if tp_match:
        triggers = re.findall(r'  - (.+)', tp_match.group(1))
        result["trigger_phrases"] = [t.strip().strip('"') for t in triggers]

    # dependencies (list)
    dep_match = re.search(r'^dependencies:\n((?:  - .+\n?)+)', fm_text, re.MULTILINE)
    if dep_match:
        deps = re.findall(r'  - (.+)', dep_match.group(1))
        result["dependencies"] = [d.strip() for d in deps]

    return result

def extract_description(content: str) -> str:
    """Extract first paragraph after ## Mission heading."""
    m = re.search(r'## Mission\n+(.+?)(?:\n\n|\n##)', content, re.DOTALL)
    if m:
        text = m.group(1).strip()
        # Return first sentence only
        first = re.split(r'\. ', text)[0].strip()
        return first + "." if not first.endswith(".") else first
    # Fallback: first non-empty line after frontmatter
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('---') and not line.startswith('|'):
            return line
    return ""

def build_registry():
    skills = []
    skill_files = sorted(SKILLS_DIR.rglob("SKILL.md"))

    for skill_file in skill_files:
        content = skill_file.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(content)

        skill_id = fm.get("skill") or fm.get("name") or skill_file.parent.name
        category = fm.get("category") or skill_file.parent.name.split("-")[1] if len(skill_file.parent.name.split("-")) > 1 else "system"

        entry = {
            "id": skill_id,
            "title": fm.get("title", skill_id.replace("zeref-", "").replace("-", " ").title()),
            "category": category,
            "model": fm.get("model", "claude-sonnet-4-6"),
            "model_preference": fm.get("model_preference", "sonnet"),
            "effort": fm.get("effort", "medium"),
            "max_turns": fm.get("max_turns", 20),
            "risk_level": fm.get("risk_level", "medium"),
            "triggers": fm.get("trigger_phrases", []),
            "dependencies": fm.get("dependencies", [
                "references/zeref-qa-gate.md",
                "references/zeref-safety-principles.md"
            ]),
            "path": f"skills/{skill_file.parent.name}/SKILL.md"
        }
        skills.append(entry)

    registry = {
        "version": "3.0.0",
        "updated": str(date.today()),
        "total": len(skills),
        "skills": skills
    }

    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

    print(f"✅ Registry rebuilt: {len(skills)} skills → {REGISTRY_PATH}")

    # Stats
    missing_triggers = [s["id"] for s in skills if not s["triggers"]]
    if missing_triggers:
        print(f"⚠️  {len(missing_triggers)} skills missing trigger_phrases: {missing_triggers[:5]}")
    else:
        print("✅ All skills have trigger_phrases")

    by_category = {}
    for s in skills:
        by_category[s["category"]] = by_category.get(s["category"], 0) + 1
    print("\nSkills by category:")
    for cat, count in sorted(by_category.items()):
        print(f"  {cat}: {count}")

if __name__ == "__main__":
    build_registry()
