#!/usr/bin/env python3
"""
zeref-validate.py
Zeref Skills Fleet V2 — Skill File Validator
Author: Yash Kanadhia / Zeref
Version: 2.0.0

Validates all skill .md files in the /skills/ directory.
Exit code 0 = all pass. Exit code 1 = any fail.
"""

import os
import sys
import re
import argparse
from pathlib import Path

# ─── ANSI Color Codes ───────────────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
DIM     = "\033[2m"
MAGENTA = "\033[95m"

def c(color, text):
    return f"{color}{text}{RESET}"

def banner():
    print()
    print(c(CYAN, BOLD + "╔══════════════════════════════════════════════════════════╗"))
    print(c(CYAN, BOLD + "║        ZEREF SKILLS FLEET V2 — SKILL VALIDATOR          ║"))
    print(c(CYAN, BOLD + "║                    zeref-validate.py                    ║"))
    print(c(CYAN, BOLD + "╚══════════════════════════════════════════════════════════╝"))
    print()

# ─── Constants ───────────────────────────────────────────────────────────────
VALID_LAYERS = {1, 2, 3, 4, 5, 6, 7, 8}
VALID_ROLES  = {"lead", "support", "qa-gate", "executive"}

REQUIRED_FRONTMATTER_FIELDS = [
    "id",
    "name",
    "version",
    "layer",
    "role",
    "routes_to",
    "receives_from",
]

REQUIRED_SECTIONS = [
    "Mission",
    "When To Use",
    "When NOT To Use",
    "Required Inputs",
    "Deliverables",
    "Workflow",
    "Output Format",
    "Token Discipline",
    "Handoff Protocol",
]

# ─── Frontmatter Parser ───────────────────────────────────────────────────────
def parse_frontmatter(content):
    """
    Parses YAML-style frontmatter delimited by ---
    Returns (frontmatter_dict, body_text) or (None, content) if no frontmatter.
    """
    lines = content.split("\n")
    if not lines[0].strip() == "---":
        return None, content

    end = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = i
            break

    if end is None:
        return None, content

    fm_lines = lines[1:end]
    body = "\n".join(lines[end + 1:])
    fm = {}

    for line in fm_lines:
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            # Handle list values: [a, b, c]
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                if inner:
                    fm[key] = [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
                else:
                    fm[key] = []
            else:
                fm[key] = val.strip('"').strip("'")

    return fm, body

# ─── Section Checker ─────────────────────────────────────────────────────────
def find_sections(body):
    """Return a dict of {section_name: body_text} for all ## headings found."""
    sections = {}
    current = None
    current_lines = []

    for line in body.split("\n"):
        heading = re.match(r"^##\s+(.+)", line)
        if heading:
            if current is not None:
                sections[current] = "\n".join(current_lines).strip()
            current = heading.group(1).strip()
            current_lines = []
        elif current is not None:
            current_lines.append(line)

    if current is not None:
        sections[current] = "\n".join(current_lines).strip()

    return sections

def section_present(sections, required_name):
    """Check if any key in sections contains the required_name (case-insensitive partial match)."""
    req_lower = required_name.lower()
    for key in sections:
        if req_lower in key.lower():
            return key
    return None

# ─── Skill Validator ─────────────────────────────────────────────────────────
def validate_skill(filepath, all_skill_ids):
    """
    Validates a single skill .md file.
    Returns (pass_count, warn_count, fail_count, messages)
    """
    messages = []
    passes = 0
    warns  = 0
    fails  = 0

    try:
        content = Path(filepath).read_text(encoding="utf-8")
    except Exception as e:
        return 0, 0, 1, [(RED, f"FAIL", f"Cannot read file: {e}")]

    fm, body = parse_frontmatter(content)

    # ── 1. Frontmatter presence ─────────────────────────────────────────────
    if fm is None:
        fails += 1
        messages.append((RED, "FAIL", "No YAML frontmatter found (expected --- delimiters)"))
        return passes, warns, fails, messages
    else:
        passes += 1
        messages.append((GREEN, "PASS", "Frontmatter block detected"))

    # ── 2. Required frontmatter fields ─────────────────────────────────────
    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in fm:
            fails += 1
            messages.append((RED, "FAIL", f"Missing required frontmatter field: '{field}'"))
        elif fm[field] == "" or fm[field] == [] or fm[field] is None:
            warns += 1
            messages.append((YELLOW, "WARN", f"Frontmatter field '{field}' is empty"))
        else:
            passes += 1
            messages.append((GREEN, "PASS", f"Field '{field}' = {repr(fm[field])}"))

    # ── 3. Valid layer value ────────────────────────────────────────────────
    if "layer" in fm:
        try:
            layer_val = int(fm["layer"])
            if layer_val not in VALID_LAYERS:
                fails += 1
                messages.append((RED, "FAIL", f"Invalid layer value '{fm['layer']}'. Must be one of {sorted(VALID_LAYERS)}"))
            else:
                passes += 1
                messages.append((GREEN, "PASS", f"Layer {layer_val} is valid"))
        except (ValueError, TypeError):
            # Try parsing "1/UX" style layer values
            try:
                layer_str = str(fm.get('layer', '')).split('/')[0].strip()
                layer_int = int(layer_str)
                if layer_int not in VALID_LAYERS:
                    fails += 1
                    messages.append((RED, "FAIL", f"Layer value '{fm.get('layer')}' not in {sorted(VALID_LAYERS)}"))
                else:
                    passes += 1
                    messages.append((GREEN, "PASS", f"Layer {fm.get('layer')} is valid (extended format)"))
            except (ValueError, TypeError):
                fails += 1
                messages.append((RED, "FAIL", f"Layer value '{fm.get('layer')}' is not a valid layer"))

    # ── 4. Valid role value ─────────────────────────────────────────────────
    if "role" in fm:
        role_val = str(fm["role"]).strip().lower()
        # Accept composite roles like "support/lead", "qa-gate/executive"
        role_parts = [r.strip() for r in role_val.split('/')]
        role_valid = all(r in VALID_ROLES for r in role_parts)
        if not role_valid:
            fails += 1
            messages.append((RED, "FAIL", f"Invalid role '{role_val}'. Must be one of {sorted(VALID_ROLES)}"))
        else:
            passes += 1
            messages.append((GREEN, "PASS", f"Role '{role_val}' is valid"))

    # ── 5. Required sections ────────────────────────────────────────────────
    sections = find_sections(body)

    for req_section in REQUIRED_SECTIONS:
        found_key = section_present(sections, req_section)
        if not found_key:
            fails += 1
            messages.append((RED, "FAIL", f"Missing required section: '## {req_section}'"))
        else:
            section_body = sections[found_key]
            if not section_body.strip():
                warns += 1
                messages.append((YELLOW, "WARN", f"Section '## {found_key}' is present but empty"))
            else:
                passes += 1
                messages.append((GREEN, "PASS", f"Section '## {found_key}' present and non-empty"))

    # ── 6. routes_to reference check ───────────────────────────────────────
    routes_to = fm.get("routes_to", [])
    if isinstance(routes_to, str):
        # Split comma-separated string into individual IDs
        routes_to = [r.strip() for r in routes_to.split(",") if r.strip()] if routes_to else []

    for ref_id in routes_to:
        ref_id_clean = ref_id.strip().lower()
        # Skip special values
        if ref_id_clean in ("none", "n/a", ""):
            continue
        if ref_id_clean and ref_id_clean not in all_skill_ids:
            warns += 1
            messages.append((YELLOW, "WARN", f"routes_to references '{ref_id_clean}' but no matching skill file found"))
        elif ref_id_clean:
            passes += 1
            messages.append((GREEN, "PASS", f"routes_to reference '{ref_id_clean}' resolved"))

    # ── 7. receives_from reference check ───────────────────────────────────
    receives_from = fm.get("receives_from", [])
    if isinstance(receives_from, str):
        # Split comma-separated string into individual IDs
        receives_from = [r.strip() for r in receives_from.split(",") if r.strip()] if receives_from else []

    for ref_id in receives_from:
        ref_id_clean = ref_id.strip()
        # ZEREFOS is a valid system sender, skip file check for it
        if ref_id_clean.upper() == "ZEREFOS":
            passes += 1
            messages.append((GREEN, "PASS", f"receives_from 'ZEREFOS' (system sender, no file required)"))
        elif ref_id_clean and ref_id_clean not in all_skill_ids:
            warns += 1
            messages.append((YELLOW, "WARN", f"receives_from references '{ref_id_clean}' but no matching skill file found"))
        elif ref_id_clean:
            passes += 1
            messages.append((GREEN, "PASS", f"receives_from reference '{ref_id_clean}' resolved"))

    return passes, warns, fails, messages

# ─── Skills Discovery ─────────────────────────────────────────────────────────
def discover_skills(skills_dir):
    """
    Find all .md files in the skills directory.
    Supports flat directory (skills/skill-id.md) and nested (skills/skill-id/SKILL.md).
    Returns list of Path objects.
    """
    skills_path = Path(skills_dir)
    if not skills_path.exists():
        return []

    found = []
    # Flat: skills/skill-id.md
    for f in skills_path.glob("*.md"):
        found.append(f)
    # Nested: skills/skill-id/SKILL.md or skills/skill-id/skill-id.md
    for d in skills_path.iterdir():
        if d.is_dir():
            for f in d.glob("*.md"):
                found.append(f)

    return sorted(set(found))

def build_skill_id_set(skill_files):
    """
    Build a set of known skill IDs from file paths.
    Derives ID from filename (without extension) or parent directory name.
    """
    ids = set()
    for f in skill_files:
        stem = f.stem.lower()
        parent = f.parent.name.lower()
        if stem not in ("skill", "readme"):
            ids.add(stem)
        if parent not in ("skills",):
            ids.add(parent)
    # Always include system senders (both cases)
    ids.add("zerefos")
    ids.add("ZEREFOS".lower())
    # Add "any skill" as valid receives_from token
    ids.add("any skill")
    ids.add("any")
    return ids

# ─── Main ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Zeref Skills Fleet V2 — Skill File Validator",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--skills-dir",
        default="skills",
        help="Path to the skills/ directory (default: ./skills)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show all PASS messages (default: only WARN and FAIL)",
    )
    parser.add_argument(
        "--file",
        default=None,
        help="Validate a single specific .md file instead of the whole directory",
    )
    args = parser.parse_args()

    banner()

    # ── Discover skills ─────────────────────────────────────────────────────
    if args.file:
        skill_files = [Path(args.file)]
        print(c(DIM, f"→ Validating single file: {args.file}\n"))
    else:
        skill_files = discover_skills(args.skills_dir)
        if not skill_files:
            print(c(RED, f"ERROR: No skill .md files found in '{args.skills_dir}/'"))
            print(c(DIM, "  Make sure you run this from the repo root, or pass --skills-dir"))
            sys.exit(1)
        print(c(DIM, f"→ Skills directory : {args.skills_dir}/"))
        print(c(DIM, f"→ Skill files found: {len(skill_files)}"))
        print()

    all_skill_ids = build_skill_id_set(skill_files)

    # ── Run validation ──────────────────────────────────────────────────────
    total_pass = 0
    total_warn = 0
    total_fail = 0
    skill_results = []  # (filepath, pass, warn, fail)

    for sf in skill_files:
        p, w, f, msgs = validate_skill(sf, all_skill_ids)
        total_pass += p
        total_warn += w
        total_fail += f
        skill_results.append((sf, p, w, f, msgs))

    # ── Print results ───────────────────────────────────────────────────────
    for sf, p, w, f, msgs in skill_results:
        rel = os.path.relpath(sf)
        status_color = GREEN if f == 0 and w == 0 else (YELLOW if f == 0 else RED)
        status_label = "PASS" if f == 0 and w == 0 else ("WARN" if f == 0 else "FAIL")
        print(c(BOLD, f"  {c(status_color, f'[{status_label}]')} {rel}"))
        print(c(DIM,  f"         pass={p}  warn={w}  fail={f}"))

        for (color, label, detail) in msgs:
            if label == "PASS" and not args.verbose:
                continue
            indent = "         "
            print(f"{indent}{c(color, f'  [{label}]')} {detail}")

        print()

    # ── Summary ─────────────────────────────────────────────────────────────
    total_skills = len(skill_results)
    skills_pass  = sum(1 for _, p, w, f, _ in skill_results if f == 0 and w == 0)
    skills_warn  = sum(1 for _, p, w, f, _ in skill_results if f == 0 and w > 0)
    skills_fail  = sum(1 for _, p, w, f, _ in skill_results if f > 0)

    print(c(CYAN, BOLD + "─" * 60))
    print(c(BOLD, "  VALIDATION SUMMARY"))
    print(c(CYAN, "─" * 60))
    print(f"  Skills validated : {c(WHITE, str(total_skills))}")
    print(f"  Skills PASS      : {c(GREEN, str(skills_pass))}")
    print(f"  Skills WARN      : {c(YELLOW, str(skills_warn))}")
    print(f"  Skills FAIL      : {c(RED, str(skills_fail))}")
    print()
    print(f"  Check totals     : {c(GREEN, str(total_pass))} pass  "
          f"{c(YELLOW, str(total_warn))} warn  "
          f"{c(RED, str(total_fail))} fail")
    print(c(CYAN, "─" * 60))

    if total_fail == 0 and total_warn == 0:
        print(c(GREEN, BOLD + "\n  ALL SKILLS PASSED VALIDATION ✓"))
        print(c(DIM, "  No failures. No warnings. Fleet is clean.\n"))
        sys.exit(0)
    elif total_fail == 0:
        print(c(YELLOW, BOLD + f"\n  VALIDATION PASSED WITH {total_warn} WARNING(S)"))
        print(c(DIM, "  No failures. Review warnings before release.\n"))
        sys.exit(0)
    else:
        print(c(RED, BOLD + f"\n  VALIDATION FAILED — {total_fail} CHECK(S) FAILED"))
        print(c(DIM, "  Fix all FAIL items before committing to main.\n"))
        sys.exit(1)

if __name__ == "__main__":
    main()
