"""Target-specific prompt injection wrappers.

privacy-audit: allow-file "Prompt-injection wrappers reference target CLI names (claude, codex, gemini) as routing constants; no user data."
"""

from __future__ import annotations

from typing import Any

from zeref.prompt.rewrite import brief_to_markdown, build_brief
from zeref.prompt.target_profile import (
    TargetProfile,
    maybe_load_profile,
    caveman_skip_categories,
)


TARGET_HEADERS = {
    "codex": "Codex Task Brief",
    "claude": "Claude Task Brief",
    "cursor": "Cursor Task Brief",
    "github": "GitHub Issue Task Brief",
    "human": "Human Handoff Brief",
}


# Map a wrapper `target=` value → a target-model profile id when the wrapper
# lands on a specific model. Multiple wrapper aliases can map to the same
# profile (e.g. "claude" wrapper may consume Opus 4.8 or Sonnet 5 profile,
# picked by explicit `profile_id=` arg or by session config). Fail-open when
# no profile is known.
_DEFAULT_PROFILE_FOR_TARGET = {
    "claude": "claude-opus-4-8",
    "codex": "codex-gpt-5-5",
    "cursor": "cursor",
    "github": None,   # not a model target
    "human": None,    # not a model target
}


def _profile_for_target(target: str, override: str | None) -> TargetProfile | None:
    if override:
        return maybe_load_profile(override)
    default = _DEFAULT_PROFILE_FOR_TARGET.get(target)
    if not default:
        return None
    return maybe_load_profile(default)


def _target_aware_note(profile: TargetProfile | None) -> str:
    """Return a compact preamble line naming what the target already knows.

    Consumers of this line drop the corresponding sections when they see it.
    Fail-open: empty string when no profile is loaded.
    """
    if profile is None:
        return ""
    skips = list(caveman_skip_categories(profile))
    if not skips:
        return ""
    return (f"_target-profile:{profile.target_id} — skip: "
            + ", ".join(skips) + "_\n\n")


def inject_prompt(raw_prompt: str,
                  *,
                  target: str = "codex",
                  profile_id: str | None = None) -> dict[str, Any]:
    """Wrap `raw_prompt` for `target`, optionally consulting a target profile.

    When `profile_id` is passed OR a default profile exists for `target`, the
    wrapper emits a compact target-aware preamble that tells downstream
    caveman-handoff/compressors which categories the target already knows.
    Fail-open — profiles missing = pre-v1.2 behavior unchanged.
    """
    if target not in TARGET_HEADERS:
        raise ValueError(f"unsupported prompt target: {target}")
    brief = build_brief(raw_prompt)
    profile = _profile_for_target(target, profile_id)
    preamble = _target_aware_note(profile)
    content = (
        f"# {TARGET_HEADERS[target]}\n\n"
        f"{preamble}"
        f"{brief_to_markdown(brief)}"
    )
    return {
        "target": target,
        "profile_id": profile.target_id if profile else None,
        "classification": brief["classification"],
        "content": content,
        "brief": brief,
    }
