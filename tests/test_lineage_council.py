from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

from zeref.lineage.council import LENSES, run_council
from zeref.lineage.intake import REQUIRED_COLUMNS


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def _row(row_id: int, *, priority: str, adoption: str, category: str, lens: str) -> dict[str, str]:
    return {
        "id": str(row_id),
        "section": "A",
        "repo_name": f"Repo {row_id}",
        "source_link_raw": f"owner/repo-{row_id}",
        "repo_url": f"https://github.com/owner/repo-{row_id}",
        "owner": "owner",
        "source_type": "repository",
        "category": category,
        "decision_from_lineage": "test",
        "zrf_adoption": adoption,
        "priority": priority,
        "council_lens": lens,
        "why_it_matters_to_ZRF": "test",
        "guardrail": "Do not bloat core.",
        "implementation_route": "test route",
        "next_analysis_question": "What is missing?",
    }


def _valid_rows() -> list[dict[str, str]]:
    lens_pairs = [
        ("memory", "Memory Architect"),
        ("retrieval", "Retrieval Architect"),
        ("graph", "Graph Architect"),
        ("benchmarks", "Benchmark Architect"),
        ("security", "Security Gate Engineer"),
        ("agents", "Agent Routing Council"),
        ("connectors", "Connector Governance Council"),
        ("product-design", "Product Quality Council"),
        ("developer-tools", "Minimality Reviewer"),
        ("workflow", "Release Governor"),
    ]
    rows = []
    for idx in range(1, 65):
        category, lens = lens_pairs[(idx - 1) % len(lens_pairs)]
        if idx <= 10:
            rows.append(_row(idx, priority="critical", adoption="Adopt as gate principle", category=category, lens=lens))
        elif idx <= 31:
            rows.append(_row(idx, priority="high", adoption="Adapt", category=category, lens=lens))
        else:
            adoption = "Reference only" if idx <= 50 else "Monitor"
            rows.append(_row(idx, priority="medium", adoption=adoption, category=category, lens=lens))
    return rows


def test_run_council_enforces_strict_coverage(tmp_path: Path) -> None:
    path = tmp_path / "lineage.csv"
    _write_csv(path, _valid_rows())

    result = run_council(path, strict=True)

    assert result["passed"] is True
    assert result["counts"]["rows"] == 64
    assert result["counts"]["critical_rows"] == 10
    assert result["counts"]["high_rows"] == 21
    assert result["counts"]["reference_only_rows"] == 19
    assert set(result["counts"]["lenses"]) == set(LENSES)
    assert result["counts"]["verdicts"]["reference-only"] == 19


def test_lineage_council_cli_reports_json(tmp_path: Path) -> None:
    path = tmp_path / "lineage.csv"
    _write_csv(path, _valid_rows())

    result = subprocess.run(
        [sys.executable, "-m", "zeref.cli", "lineage", "council", "--strict", "--csv", str(path)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert '"passed": true' in result.stdout
    assert "5.5 High reserved" in result.stdout
