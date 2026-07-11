"""Deterministic cost routing and artifact budget checks.

privacy-audit: allow-file "Cost router references model tier names + example token budgets; no user data."
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


DEFAULT_POLICY = {
    "default_executor": "deterministic",
    "default_model_tier": "cheap",
    "deterministic_first": True,
    "max_context_tokens_for_memory_write": 1200,
    "max_output_tokens_for_memory_write": 300,
    "full_markdown_rewrite_requires": "approval_or_render",
    "flagship_requires": [
        "contradiction_resolution",
        "privacy_boundary",
        "public_claim",
        "architecture_migration",
        "benchmark_verdict",
        "irreversible_delete",
    ],
    "forbidden_by_default": [
        "load_all_memory_files",
        "rewrite_entire_memory_folder",
        "summarize_without_source_pointers",
        "silent_conflict_resolution",
    ],
    "artifact_budgets": {
        "hot.md": 700,
        "session_digest": 300,
        "project_digest": 500,
        "handoff_pack": 900,
        "decision_record": 180,
        "memory_atom": 80,
        "contradiction_case": 300,
        "evidence_packet": 400,
    },
}

LADDER = [
    "no-write",
    "link-existing",
    "metadata-update",
    "atom-append",
    "atom-patch",
    "view-render",
    "markdown-rewrite",
    "flagship-review",
]


def load_policy(root: Path | str = Path(".")) -> dict[str, Any]:
    path = Path(root) / "config" / "COST_POLICY.json"
    if not path.exists():
        return DEFAULT_POLICY
    return {**DEFAULT_POLICY, **json.loads(path.read_text(encoding="utf-8"))}


def estimate_tokens(text: str) -> dict[str, Any]:
    tokens = max(1, (len(re.findall(r"\S+", text)) * 4 + 2) // 3) if text else 0
    return {
        "estimated_tokens": tokens,
        "estimated_chars": len(text),
        "method": "deterministic_words_x_1_33",
    }


def route_operation(
    operation: str,
    *,
    text: str = "",
    approval: bool = False,
    render_mode: bool = False,
    duplicate: bool = False,
    status_change: bool = False,
    public_claim: bool = False,
    contradiction: bool = False,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    policy = policy or DEFAULT_POLICY
    estimate = estimate_tokens(text)
    op = operation.replace("_", "-")

    if operation in policy["forbidden_by_default"]:
        return _decision("blocked", "flagship-review", estimate, "operation forbidden by default")
    if op in {"markdown-rewrite", "full-markdown-rewrite"} and not (approval or render_mode):
        return _decision("blocked", "markdown-rewrite", estimate, "markdown rewrite requires approval or render mode")
    if public_claim:
        return _decision("flagship", "flagship-review", estimate, "public claim requires high-judgment review")
    if contradiction:
        return _decision("flagship", "flagship-review", estimate, "contradiction requires arbitration")
    if duplicate:
        return _decision("deterministic", "link-existing", estimate, "duplicate memory should link existing atom")
    if status_change or op in {"patch", "metadata-update", "atom-patch"}:
        return _decision("deterministic", "atom-patch", estimate, "status or metadata change")
    if op in {"memory-add", "atom-append", "add"}:
        return _decision("deterministic", "atom-append", estimate, "new simple memory atom")
    if op in {"render", "view-render"}:
        return _decision("deterministic", "view-render", estimate, "rendered view generation")
    if estimate["estimated_tokens"] == 0:
        return _decision("deterministic", "no-write", estimate, "empty input")
    if estimate["estimated_tokens"] > policy["max_context_tokens_for_memory_write"]:
        return _decision("mid", "flagship-review", estimate, "input exceeds memory write budget")
    return _decision("deterministic", "no-write", estimate, "no durable write needed")


def audit_budgets(root: Path | str = Path("."), *, strict: bool = False) -> dict[str, Any]:
    root_path = Path(root)
    policy = load_policy(root_path)
    budgets = policy["artifact_budgets"]
    checks = []
    mapping = {
        "hot.md": root_path / "memory" / "hot.md",
    }
    for name, budget in budgets.items():
        path = mapping.get(name)
        if path is None or not path.exists():
            continue
        tokens = estimate_tokens(path.read_text(encoding="utf-8"))["estimated_tokens"]
        checks.append({
            "artifact": name,
            "path": str(path),
            "budget": budget,
            "estimated_tokens": tokens,
            "ok": tokens <= budget,
        })
    passed = all(check["ok"] for check in checks)
    return {"passed": passed, "strict": strict, "checks": checks}


def report(root: Path | str = Path(".")) -> dict[str, Any]:
    policy = load_policy(root)
    return {
        "default_executor": policy["default_executor"],
        "default_model_tier": policy["default_model_tier"],
        "deterministic_first": policy["deterministic_first"],
        "ladder": LADDER,
        "artifact_budgets": policy["artifact_budgets"],
    }


def _decision(executor: str, ladder_step: str, estimate: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "executor": executor,
        "ladder_step": ladder_step,
        "estimate": estimate,
        "reason": reason,
    }
