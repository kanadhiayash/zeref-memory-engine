"""Token efficiency axis for deterministic memory routing.

privacy-audit: allow-file "Scorer references tier names + example token budgets; no user data."
"""

from __future__ import annotations

import sys

from benchmarks.helpers import axis_result, print_json_result
from zeref.memory.cost_router import estimate_tokens, route_operation


def _score_markdown_guard() -> tuple[float, str]:
    result = route_operation("markdown-rewrite")
    ok = result["executor"] == "blocked"
    return (10.0 if ok else 0.0), f"markdown rewrite executor={result['executor']}"


def _score_minimalism_ladder() -> tuple[float, str]:
    duplicate = route_operation("memory-add", duplicate=True)
    append = route_operation("memory-add", text="Use atoms.")
    patch = route_operation("patch", status_change=True)
    ok = (
        duplicate["ladder_step"] == "link-existing"
        and append["ladder_step"] == "atom-append"
        and patch["ladder_step"] == "atom-patch"
    )
    return (10.0 if ok else 4.0), (
        f"duplicate={duplicate['ladder_step']}, append={append['ladder_step']}, "
        f"patch={patch['ladder_step']}"
    )


def _score_flagship_gate() -> tuple[float, str]:
    result = route_operation("memory-add", public_claim=True)
    ok = result["executor"] == "flagship"
    return (10.0 if ok else 5.0), f"public claim executor={result['executor']}"


def _score_estimator() -> tuple[float, str]:
    first = estimate_tokens("one two three")
    second = estimate_tokens("one two three")
    ok = first == second and first["estimated_tokens"] > 0
    return (10.0 if ok else 4.0), f"estimate={first['estimated_tokens']} deterministic={first == second}"


def run() -> dict:
    return axis_result("token_efficiency", {
        "markdown_guard": _score_markdown_guard(),
        "minimalism_ladder": _score_minimalism_ladder(),
        "flagship_gate": _score_flagship_gate(),
        "deterministic_estimator": _score_estimator(),
    })


if __name__ == "__main__":
    sys.exit(print_json_result(run()))
