"""Adapter value benchmark axis."""

from __future__ import annotations

import sys

from benchmarks.helpers import print_json_result
from benchmarks.lineage_common import intake_skip, lineage_axis, lineage_reports


def run() -> dict:
    skipped = intake_skip("adapter_value")
    if skipped:
        return skipped
    high = lineage_reports()["high"]
    forms = high["forms"]
    return lineage_axis("adapter_value", {
        "optional_adapters_present": (forms.get("optional-adapter", 0) == 4, "4 optional adapter targets gated"),
        "fixtures_present": (forms.get("benchmark-fixture", 0) == 4, "4 benchmark fixture adaptations"),
        "connector_policy_present": (forms.get("connector-governance", 0) == 1, "connector boundary represented"),
    })


if __name__ == "__main__":
    sys.exit(print_json_result(run()))
