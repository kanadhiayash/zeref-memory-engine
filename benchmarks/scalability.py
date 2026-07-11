"""
privacy-audit: allow-file "Axis scorer references team-pack names + example thresholds as spec; no user data."

Scalability axis — deterministic scorer.

Sub-criteria mirror benchmarks/RUBRIC.md §Axis 3.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PACKS = ["small", "medium", "enterprise"]


def _read(rel: str) -> str:
    p = REPO / rel
    return p.read_text(errors="ignore") if p.exists() else ""


def _score_packs_exist() -> tuple[float, str]:
    found = [p for p in PACKS if (REPO / "team-packs" / f"{p}.md").exists()]
    envelopes = sum(
        1 for p in found
        if "budget_target_tokens" in _read(f"team-packs/{p}.md")
    )
    score = 10.0 if (len(found) == 3 and envelopes == 3) else \
            7.0 if len(found) == 3 else \
            5.0 if len(found) >= 2 else 2.0
    return score, f"{len(found)}/3 packs present; {envelopes}/3 with token envelope"


def _score_budget_enforced() -> tuple[float, str]:
    bg = _read("skills/budget-governor/SKILL.md")
    has_soft = "warn" in bg.lower() or "target" in bg.lower()
    has_hard = "hard_cap" in bg or "hard cap" in bg.lower()
    has_override = "override" in bg.lower()
    score = 10.0 if (has_soft and has_hard and has_override) else \
            8.0 if (has_soft and has_hard) else 5.0
    return score, f"soft={has_soft}, hard={has_hard}, override={has_override}"


def _score_tier_routed() -> tuple[float, str]:
    documented = 0
    for p in PACKS:
        text = _read(f"team-packs/{p}.md")
        if "default_tier" in text:
            documented += 1
    opus_reserved = any(
        "opus_allowed: false" in _read(f"team-packs/{p}.md")
        or "opus_allowed: limited" in _read(f"team-packs/{p}.md")
        for p in PACKS
    )
    score = 10.0 if (documented == 3 and opus_reserved) else \
            8.0 if documented == 3 else \
            5.0 if documented >= 1 else 2.0
    return score, f"{documented}/3 packs set default_tier; opus_reserved={opus_reserved}"


def _score_r6_preserved() -> tuple[float, str]:
    # R6 = Zero Context Loss. Check shared rules + handoff skills mention it
    rules = _read("_shared/rules.md") + _read("_shared/model-resolver.md")
    ho = _read("skills/handoff-compiler/SKILL.md")
    ch = _read("skills/caveman-handoff/SKILL.md")
    has_rule = "R6" in rules or "Zero Context Loss" in rules
    has_handoff = ("R6" in ho or "R6" in ch
                   or "Zero Context Loss" in (ho + ch))
    score = 10.0 if (has_rule and has_handoff) else \
            7.0 if has_rule else 4.0
    return score, f"R6 in rules={has_rule}, R6 referenced in handoff skills={has_handoff}"


def _score_decision_criteria() -> tuple[float, str]:
    documented = 0
    for p in PACKS:
        text = _read(f"team-packs/{p}.md")
        # any "When to upgrade" / "When to use" / "What you give up"
        if re.search(r"(?im)^##\s*When\s*to\s*(upgrade|use)", text):
            documented += 1
    score = 10.0 if documented == 3 else 7.0 if documented == 2 else 4.0
    return score, f"{documented}/3 packs document upgrade/use criteria"


def run() -> dict:
    subs = {
        "packs_exist":        _score_packs_exist(),
        "budget_enforced":    _score_budget_enforced(),
        "tier_routed":        _score_tier_routed(),
        "r6_preserved":       _score_r6_preserved(),
        "decision_criteria":  _score_decision_criteria(),
    }
    axis = sum(s for s, _ in subs.values()) / len(subs)
    return {
        "axis": "scalability",
        "score": round(axis, 2),
        "sub": {k: {"score": round(s, 2), "evidence": e} for k, (s, e) in subs.items()},
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
