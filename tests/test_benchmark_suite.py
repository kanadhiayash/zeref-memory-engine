from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from zeref.benchmark.failure_analysis import collect_failures, write_failure_report


NEW_AXES = [
    "token_efficiency",
    "retrieval_accuracy",
    "contradiction_detection",
    "privacy_safety",
    "prompt_rewrite_quality",
    "handoff_success",
    "loop_control",
    "memory_refinement",
]


def test_new_benchmark_axes_are_standalone(repo_root: Path) -> None:
    for axis in NEW_AXES:
        result = subprocess.run(
            [sys.executable, "-m", f"benchmarks.{axis}"],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
        )
        assert result.returncode == 0, f"{axis} failed:\n{result.stdout}\n{result.stderr}"
        payload = json.loads(result.stdout)
        assert payload["axis"] == axis
        assert payload["score"] >= 9.0


def test_failure_analysis_contains_required_fields(tmp_path: Path) -> None:
    failures = collect_failures([
        {
            "axis": "example_axis",
            "score": 7.5,
            "sub": {
                "example": {"score": 5.0, "evidence": "missing fixture"},
            },
        }
    ])
    assert failures
    for key in [
        "failed_metric",
        "expected",
        "actual",
        "likely_cause",
        "needed_fix",
        "regression_test_suggestion",
    ]:
        assert key in failures[0]

    path = write_failure_report(tmp_path, failures)
    text = path.read_text(encoding="utf-8")
    assert "Expected:" in text
    assert "Actual:" in text
    assert "Likely cause:" in text
    assert "Needed fix:" in text
    assert "Regression-test suggestion:" in text
