from __future__ import annotations

from benchmarks import (
    adapter_value,
    critical_adoption_coverage,
    foreign_code_containment,
    high_adoption_coverage,
    license_boundary,
    lineage_import_coverage,
    minimality_pressure,
    public_claim_safety,
    reference_only_guardrails,
    security_containment,
)


LINEAGE_AXES = [
    lineage_import_coverage,
    foreign_code_containment,
    critical_adoption_coverage,
    high_adoption_coverage,
    reference_only_guardrails,
    adapter_value,
    minimality_pressure,
    security_containment,
    license_boundary,
    public_claim_safety,
]


def test_lineage_benchmark_axes_pass() -> None:
    results = [axis.run() for axis in LINEAGE_AXES]

    assert [result["score"] for result in results] == [10.0] * len(LINEAGE_AXES)
    assert {result["axis"] for result in results} == {
        "lineage_import_coverage",
        "foreign_code_containment",
        "critical_adoption_coverage",
        "high_adoption_coverage",
        "reference_only_guardrails",
        "adapter_value",
        "minimality_pressure",
        "security_containment",
        "license_boundary",
        "public_claim_safety",
    }
