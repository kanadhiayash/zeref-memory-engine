"""Deterministic council verdicts for the Zeref lineage program.

privacy-audit: allow-file "Council references ISO-date-shaped intake fields as schema; no user data."
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from zeref.lineage.importer import default_csv_path
from zeref.lineage.intake import (
    EXPECTED_PRIORITY_COUNTS,
    EXPECTED_REFERENCE_ONLY,
    EXPECTED_TOTAL,
    LineageRow,
    load_rows,
)


LENSES = [
    "Memory",
    "Retrieval",
    "Graph",
    "Benchmark",
    "Security Rails",
    "Agent Routing",
    "Connector Governance",
    "Product Quality",
    "Minimality",
    "Release",
]


def run_council(csv_path: str | Path | None = None, *, strict: bool = False) -> dict[str, Any]:
    """Produce deterministic lineage verdicts and strict coverage findings."""
    path = Path(csv_path) if csv_path else default_csv_path()
    rows = load_rows(path)
    verdicts = [_verdict(row) for row in rows]
    issues = _strict_issues(rows, verdicts) if strict else []
    verdict_counts = Counter(item["verdict"] for item in verdicts)
    lens_counts = Counter(item["lens"] for item in verdicts)

    return {
        "passed": not issues,
        "strict": strict,
        "csv": str(path),
        "escalation_policy": (
            "5.5 High reserved for final architecture arbitration, "
            "security-sensitive judgment, or final benchmark verdict wording."
        ),
        "expected": {
            "rows": EXPECTED_TOTAL,
            "critical": EXPECTED_PRIORITY_COUNTS["critical"],
            "high": EXPECTED_PRIORITY_COUNTS["high"],
            "reference_only": EXPECTED_REFERENCE_ONLY,
            "lenses": LENSES,
        },
        "counts": {
            "rows": len(rows),
            "verdicts": dict(sorted(verdict_counts.items())),
            "lenses": dict(sorted(lens_counts.items())),
            "critical_rows": sum(1 for row in rows if row.priority == "critical"),
            "high_rows": sum(1 for row in rows if row.priority == "high"),
            "reference_only_rows": sum(1 for row in rows if row.is_reference_only),
        },
        "verdicts": verdicts,
        "issues": issues,
    }


def _verdict(row: LineageRow) -> dict[str, Any]:
    adoption = row.zrf_adoption.lower()
    if adoption == "reference only":
        verdict = "reference-only"
    elif adoption == "reject":
        verdict = "reject"
    elif row.priority == "critical":
        verdict = "adopt" if "adopt" in adoption else "adapt"
    elif row.priority == "high":
        verdict = "monitor" if "monitor" in adoption else "adapt"
    elif "monitor" in adoption:
        verdict = "monitor"
    elif "reference" in adoption:
        verdict = "reference-only"
    else:
        verdict = "adapt"

    return {
        "row_id": row.id,
        "repo_name": row.repo_name,
        "github_repo": row.github_repo,
        "lens": _lens_for(row),
        "priority": row.priority,
        "adoption": row.zrf_adoption,
        "verdict": verdict,
        "implementation_route": row.implementation_route,
        "guardrail": row.guardrail,
        "reason": _reason(row, verdict),
    }


def _strict_issues(rows: list[LineageRow], verdicts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if len(rows) != EXPECTED_TOTAL:
        issues.append({"kind": "row_count", "message": f"expected {EXPECTED_TOTAL}, got {len(rows)}"})
    counts = Counter(row.priority for row in rows)
    for priority, expected in EXPECTED_PRIORITY_COUNTS.items():
        actual = counts.get(priority, 0)
        if actual != expected:
            issues.append({"kind": "priority_count", "message": f"expected {expected} {priority}, got {actual}"})
    reference_only = sum(1 for row in rows if row.is_reference_only)
    if reference_only != EXPECTED_REFERENCE_ONLY:
        issues.append({"kind": "reference_only_count", "message": f"expected {EXPECTED_REFERENCE_ONLY}, got {reference_only}"})

    by_id = {item["row_id"]: item for item in verdicts}
    for row in rows:
        verdict = by_id[row.id]["verdict"]
        if row.priority == "critical" and verdict not in {"adopt", "adapt"}:
            issues.append({"kind": "critical_verdict", "row_id": row.id, "message": "critical rows must adopt or adapt"})
        if row.priority == "high" and verdict not in {"adapt", "monitor"}:
            issues.append({"kind": "high_verdict", "row_id": row.id, "message": "high rows must adapt or monitor"})
        if row.is_reference_only and verdict != "reference-only":
            issues.append({"kind": "reference_verdict", "row_id": row.id, "message": "reference-only rows must stay reference-only"})

    covered_lenses = {item["lens"] for item in verdicts}
    missing = [lens for lens in LENSES if lens not in covered_lenses]
    if missing:
        issues.append({"kind": "lens_coverage", "message": "missing lenses: " + ", ".join(missing)})
    return issues


def _lens_for(row: LineageRow) -> str:
    text = f"{row.category} {row.council_lens}".lower()
    if "retrieval" in text:
        return "Retrieval"
    if "graph" in text:
        return "Graph"
    if "benchmark" in text or "eval" in text:
        return "Benchmark"
    if "security" in text or "red-team" in text or "guardrail" in text:
        return "Security Rails"
    if "agent" in text or "routing" in text or "model" in text or "llm" in text:
        return "Agent Routing"
    if "connector" in text or "mcp" in text or "ingest" in text:
        return "Connector Governance"
    if "product" in text or "design" in text or "frontend" in text:
        return "Product Quality"
    if "minimal" in text or "developer-tools" in text:
        return "Minimality"
    if "release" in text or "workflow" in text or "handoff" in text:
        return "Release"
    return "Memory"


def _reason(row: LineageRow, verdict: str) -> str:
    if verdict == "reference-only":
        return "Use as evidence, fixture, guardrail, or council input without core import."
    if verdict == "reject":
        return "Do not import code; retain only the policy lesson."
    if row.priority == "critical":
        return "Required for core identity, core gate, CI discipline, or eval lifecycle."
    if row.priority == "high":
        return "Use behind optional adapter, route, fixture, or guardrail boundary."
    return "Monitor or adapt only after a benchmark gate proves value."
