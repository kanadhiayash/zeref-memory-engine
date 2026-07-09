"""Retrieval benchmark contract tests."""

from __future__ import annotations

from benchmarks import retrieval


def test_retrieval_benchmark_scores_all_fixtures() -> None:
    result = retrieval.run()
    assert result["axis"] == "retrieval"
    assert result["score"] == 10.0
    assert set(result["sub"]) == {
        "fixture_inventory",
        "continuity",
        "privacy_recall",
        "contradiction",
        "freshness",
        "abstention",
    }
    for sub in result["sub"].values():
        assert sub["score"] == 10.0
        assert sub["evidence"]
