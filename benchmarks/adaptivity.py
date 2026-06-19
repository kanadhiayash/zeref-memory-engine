"""
Adaptivity axis — deterministic scorer.

Sub-criteria mirror benchmarks/RUBRIC.md §Axis 2.
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _has(path: str) -> bool:
    return (REPO / path).exists()


def _score_router() -> tuple[float, str]:
    p = REPO / "skills" / "skill-router" / "SKILL.md"
    if not p.exists():
        return 0.0, "skill-router/SKILL.md missing"
    text = p.read_text(errors="ignore")
    has_ranking = "trigger" in text.lower() and "match" in text.lower()
    has_recency = "recency" in text.lower() or "last_used" in text.lower()
    score = 10.0 if (has_ranking and has_recency) else 7.0 if has_ranking else 5.0
    return score, f"router doc: ranking={has_ranking}, recency={has_recency}"


def _score_importer() -> tuple[float, str]:
    p = REPO / "skills" / "skill-importer" / "SKILL.md"
    if not p.exists():
        return 0.0, "skill-importer missing"
    text = p.read_text(errors="ignore")
    documented = "Provenance" in text or "PROVENANCE" in text
    score = 10.0 if documented else 7.0
    return score, f"skill-importer present; provenance documented={documented}"


def _score_provenance() -> tuple[float, str]:
    p = REPO / "skills" / "skill-importer" / "SKILL.md"
    if not p.exists():
        return 0.0, "no importer"
    text = p.read_text(errors="ignore")
    sha = "SHA-256" in text or "sha256" in text
    src_path = "source path" in text.lower() or "imported_from" in text
    score = 10.0 if (sha and src_path) else 7.0 if sha or src_path else 4.0
    return score, f"sha={sha}, source_path={src_path}"


def _score_review_gate() -> tuple[float, str]:
    p = REPO / "skills" / "skill-importer" / "SKILL.md"
    if not p.exists():
        return 0.0, "no importer"
    text = p.read_text(errors="ignore")
    gated = "NOT auto-activated" in text or "awaits /review-skill" in text \
            or "activation: pending-review" in text
    audit = "PATTERNS.jsonl" in text or "audit" in text.lower()
    score = 10.0 if (gated and audit) else 8.0 if gated else 5.0
    return score, f"review-gated={gated}, audit-logged={audit}"


def _score_privacy_filter() -> tuple[float, str]:
    p = REPO / "skills" / "skill-importer" / "SKILL.md"
    if not p.exists():
        return 0.0, "no importer"
    text = p.read_text(errors="ignore")
    has_filter = "privacy-guardian" in text or "Privacy filter" in text
    rejects = "abort" in text.lower() or "reject" in text.lower()
    score = 10.0 if (has_filter and rejects) else 7.0 if has_filter else 4.0
    return score, f"privacy-filter={has_filter}, rejects-on-hit={rejects}"


def run() -> dict:
    subs = {
        "router_ranking":   _score_router(),
        "importer_doc":     _score_importer(),
        "provenance":       _score_provenance(),
        "review_gate":      _score_review_gate(),
        "privacy_filter":   _score_privacy_filter(),
    }
    axis = sum(s for s, _ in subs.values()) / len(subs)
    return {
        "axis": "adaptivity",
        "score": round(axis, 2),
        "sub": {k: {"score": round(s, 2), "evidence": e} for k, (s, e) in subs.items()},
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
