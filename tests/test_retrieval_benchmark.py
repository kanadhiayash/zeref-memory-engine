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
        "external_adapter_fixtures",
    }
    assert {adapter["status"] for adapter in result["adapters"]} == {"fixture_pass"}
    for sub in result["sub"].values():
        assert sub["score"] == 10.0
        assert sub["evidence"]
