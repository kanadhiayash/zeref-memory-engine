"""Target-specific prompt injection wrappers."""

from __future__ import annotations

from typing import Any

from zeref.prompt.rewrite import brief_to_markdown, build_brief


TARGET_HEADERS = {
    "codex": "Codex Task Brief",
    "claude": "Claude Task Brief",
    "cursor": "Cursor Task Brief",
    "github": "GitHub Issue Task Brief",
    "human": "Human Handoff Brief",
}


def inject_prompt(raw_prompt: str, *, target: str = "codex") -> dict[str, Any]:
    if target not in TARGET_HEADERS:
        raise ValueError(f"unsupported prompt target: {target}")
    brief = build_brief(raw_prompt)
    content = f"# {TARGET_HEADERS[target]}\n\n{brief_to_markdown(brief)}"
    return {
        "target": target,
        "classification": brief["classification"],
        "content": content,
        "brief": brief,
    }
