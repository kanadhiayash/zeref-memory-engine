"""Benchmark adapter tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from benchmarks.adapters import ADAPTERS, adapter_summary, run_fixture_adapters
from benchmarks import retrieval


def test_adapter_fixture_statuses() -> None:
    results = run_fixture_adapters()
    assert len(results) == len(ADAPTERS)
    assert {result.status for result in results} == {"fixture_pass"}
    assert all(result.source.startswith("https://github.com/") for result in results)


def test_adapter_summary() -> None:
    score, evidence = adapter_summary(run_fixture_adapters())
    assert score == 10.0
    assert "LoCoMo=fixture_pass" in evidence
    assert "PersonaMem-v2=fixture_pass" in evidence


def test_retrieval_axis_includes_adapter_statuses() -> None:
    result = retrieval.run()
    assert result["sub"]["external_adapter_fixtures"]["score"] == 10.0
    assert len(result["adapters"]) == 5
    assert {adapter["status"] for adapter in result["adapters"]} == {"fixture_pass"}


def test_adapters_module_cli(repo_root: Path) -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "benchmarks.adapters"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0
    data = json.loads(completed.stdout)
    assert data[0]["status"] == "fixture_pass"
