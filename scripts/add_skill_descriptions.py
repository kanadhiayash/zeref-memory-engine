#!/usr/bin/env python3
"""
add_skill_descriptions.py — Add description field to all SKILL.md frontmatters
Version: 3.0.0
Run: python3 scripts/add_skill_descriptions.py [--dry-run]

Claude Code requires `description:` in SKILL.md frontmatter to register skills
for invocation. This script generates descriptions from title + mission + triggers.
"""

import re
import sys
from pathlib import Path

FLEET_ROOT = Path(__file__).parent.parent
SKILLS_DIR = FLEET_ROOT / "skills"
DRY_RUN = "--dry-run" in sys.argv


def extract_title(fm_text: str) -> str:
    m = re.search(r'^title:\s*(.+)$', fm_text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def extract_triggers(fm_text: str) -> list[str]:
    tp_match = re.search(r'^trigger_phrases:\n((?:\s+- .+\n?)+)', fm_text, re.MULTILINE)
    if not tp_match:
        return []
    return [t.strip().strip('"') for t in re.findall(r'- (.+)', tp_match.group(1))]


def compose_description(title: str, triggers: list[str]) -> str:
    """Build Claude Code description from title + trigger phrases.
    Trigger phrases are the authoritative 'when to invoke' signal — clean and specific.
    Mission/Use-This-Skill-When sections are boilerplate in Zeref skills."""
    if triggers:
        return f"{title}. Use for: {', '.join(triggers)}."
    return f"{title}."


def has_description(fm_text: str) -> bool:
    return bool(re.search(r'^description:', fm_text, re.MULTILINE))


def add_description_to_frontmatter(content: str, description: str) -> str:
    match = re.match(r'^(---\n)(.*?)(\n---)', content, re.DOTALL)
    if not match:
        return content
    pre, fm, post = match.group(1), match.group(2), match.group(3)
    rest = content[match.end():]

    title_match = re.search(r'^(title:.+)$', fm, re.MULTILINE)
    if title_match:
        insert_pos = title_match.end()
        new_fm = fm[:insert_pos] + f'\ndescription: "{description}"' + fm[insert_pos:]
    else:
        new_fm = fm + f'\ndescription: "{description}"'

    return pre + new_fm + post + rest


def main():
    skill_files = sorted(SKILLS_DIR.rglob("SKILL.md"))
    updated = 0
    skipped = 0
    errors = []

    for skill_file in skill_files:
        content = skill_file.read_text(encoding="utf-8", errors="replace")
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            errors.append(f"  NO FRONTMATTER: {skill_file.parent.name}")
            continue

        fm_text = match.group(1)

        if has_description(fm_text):
            skipped += 1
            continue

        title = extract_title(fm_text)
        triggers = extract_triggers(fm_text)
        description = compose_description(title, triggers)

        if DRY_RUN:
            print(f"  {skill_file.parent.name}")
            print(f"    → {description[:120]}...")
            print()
        else:
            new_content = add_description_to_frontmatter(content, description)
            skill_file.write_text(new_content, encoding="utf-8")

        updated += 1

    mode = "DRY RUN" if DRY_RUN else "UPDATED"
    print(f"{'=' * 60}")
    print(f"  {mode}: {updated} skills")
    print(f"  Skipped (already had description): {skipped}")
    if errors:
        print(f"  Errors: {len(errors)}")
        for e in errors:
            print(f"    {e}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
