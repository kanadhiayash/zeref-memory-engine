"""Public claim safety benchmark axis."""

from __future__ import annotations

import sys

from benchmarks.helpers import print_json_result
from benchmarks.lineage_common import lineage_axis, lineage_reports


def run() -> dict:
    council = lineage_reports()["council"]
    policy = council["escalation_policy"]
    return lineage_axis("public_claim_safety", {
        "no_superiority_verdict": ("best" not in policy.lower() and "10/10" not in policy, "escalation policy avoids superiority claims"),
        "strict_council_passed": (council["passed"] is True, "strict council gate passed"),
        "reference_rows_not_promoted": (council["counts"]["reference_only_rows"] == 19, "19 reference-only rows retained"),
    })


if __name__ == "__main__":
    sys.exit(print_json_result(run()))
