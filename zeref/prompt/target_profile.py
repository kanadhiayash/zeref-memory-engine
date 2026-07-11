"""
privacy-audit: allow-file "Target-profile loader references profile field names + example targets; no user data."

Target-model profile loader.

Reads YAML frontmatter from `references/target-model-profiles/*.md` into typed
dicts. Consumers: `zeref/prompt/inject.py`, `zeref/memory/cost_router.py`,
`skills/caveman-handoff/SKILL.md` (via CLI hint), and any target-aware
wrapping code path.

Zero external deps — reuses `_parse_yaml_frontmatter` from `zeref.security.policy`.

Freshness: profiles carry `source_updated_at`; consumers can call
`is_stale(profile, max_age_days=60)` to gate on staleness.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Iterable

from zeref.security.policy import _parse_yaml_frontmatter


class ProfileMissingError(KeyError):
    """Raised when a requested target_id has no profile on disk."""


class ProfileSchemaError(ValueError):
    """Raised when a profile is present but missing required fields."""


_REQUIRED_FIELDS = (
    "target_id",
    "vendor",
    "family",
    "variant",
    "source_url",
    "source_updated_at",
    "last_verified_catalog_sha",
    "system_prompt_tokens",
    "output_style",
    "tool_use_format",
    "refusal_signature",
)


@dataclass(frozen=True)
class TargetProfile:
    """Typed view of a target profile YAML frontmatter."""

    target_id: str
    vendor: str
    family: str
    variant: str
    source_url: str
    source_updated_at: str
    last_verified_catalog_sha: str
    system_prompt_tokens: int
    tool_declaration_tokens: int
    bare_prompt_tokens: int
    output_style: str
    markdown_default: str
    emoji_default: str
    hedging_default: str
    apology_default: str
    lists_default: str
    tool_use_format: str
    tool_dispatch: str
    refusal_signature: str
    persona_lock: str
    already_knows: tuple[str, ...] = field(default_factory=tuple)
    built_in_tools: tuple[str, ...] = field(default_factory=tuple)
    input_cost_multiplier: float = 1.0
    output_cost_multiplier: float = 1.0
    cache_hit_multiplier: float = 1.0
    raw: dict = field(default_factory=dict, repr=False)


def _profiles_dir(project_root: Path | None = None) -> Path:
    from zeref.memory.core import discover_project_root
    root = project_root or discover_project_root()
    return root / "references" / "target-model-profiles"


def _coerce_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _coerce_float(value, default: float = 1.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _coerce_str(value, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _coerce_tuple(value) -> tuple[str, ...]:
    if isinstance(value, (list, tuple)):
        return tuple(str(v) for v in value)
    return ()


def _build_profile(fm: dict) -> TargetProfile:
    for req in _REQUIRED_FIELDS:
        if req not in fm:
            raise ProfileSchemaError(f"profile missing required field: {req}")
    return TargetProfile(
        target_id=_coerce_str(fm["target_id"]),
        vendor=_coerce_str(fm["vendor"]),
        family=_coerce_str(fm["family"]),
        variant=_coerce_str(fm["variant"]),
        source_url=_coerce_str(fm["source_url"]),
        source_updated_at=_coerce_str(fm["source_updated_at"]),
        last_verified_catalog_sha=_coerce_str(fm["last_verified_catalog_sha"]),
        system_prompt_tokens=_coerce_int(fm.get("system_prompt_tokens")),
        tool_declaration_tokens=_coerce_int(fm.get("tool_declaration_tokens")),
        bare_prompt_tokens=_coerce_int(fm.get("bare_prompt_tokens")),
        output_style=_coerce_str(fm["output_style"]),
        markdown_default=_coerce_str(fm.get("markdown_default", "n/a")),
        emoji_default=_coerce_str(fm.get("emoji_default", "n/a")),
        hedging_default=_coerce_str(fm.get("hedging_default", "n/a")),
        apology_default=_coerce_str(fm.get("apology_default", "n/a")),
        lists_default=_coerce_str(fm.get("lists_default", "n/a")),
        tool_use_format=_coerce_str(fm["tool_use_format"]),
        tool_dispatch=_coerce_str(fm.get("tool_dispatch", "n/a")),
        refusal_signature=_coerce_str(fm["refusal_signature"]),
        persona_lock=_coerce_str(fm.get("persona_lock", "n/a")),
        already_knows=_coerce_tuple(fm.get("already_knows", [])),
        built_in_tools=_coerce_tuple(fm.get("built_in_tools", [])),
        input_cost_multiplier=_coerce_float(fm.get("input_cost_multiplier"), 1.0),
        output_cost_multiplier=_coerce_float(fm.get("output_cost_multiplier"), 1.0),
        cache_hit_multiplier=_coerce_float(fm.get("cache_hit_multiplier"), 1.0),
        raw=dict(fm),
    )


def load_profile(target_id: str, *, project_root: Path | None = None) -> TargetProfile:
    """Return the profile for `target_id`. Raises ProfileMissingError if absent."""
    d = _profiles_dir(project_root)
    path = d / f"{target_id}.md"
    if not path.exists():
        raise ProfileMissingError(target_id)
    fm = _parse_yaml_frontmatter(path.read_text(errors="ignore"))
    return _build_profile(fm)


def list_profiles(*, project_root: Path | None = None) -> list[str]:
    d = _profiles_dir(project_root)
    if not d.exists():
        return []
    return sorted(p.stem for p in d.glob("*.md") if p.stem != "README")


def maybe_load_profile(target_id: str,
                       *,
                       project_root: Path | None = None) -> TargetProfile | None:
    """Fail-open convenience: returns None if profile absent or malformed."""
    try:
        return load_profile(target_id, project_root=project_root)
    except (ProfileMissingError, ProfileSchemaError, OSError):
        return None


def is_stale(profile: TargetProfile, *, max_age_days: int = 60,
             today: date | None = None) -> bool:
    """Return True if `source_updated_at` is more than `max_age_days` in the past."""
    if not profile.source_updated_at:
        return True
    try:
        source = date.fromisoformat(profile.source_updated_at)
    except ValueError:
        return True
    now = today or date.today()
    return (now - source).days > max_age_days


def estimate_input_tokens(profile: TargetProfile | None,
                          zeref_wrapper_tokens: int,
                          user_content_tokens: int) -> int:
    """Cost-router hint: total input tokens the target will see."""
    baseline = profile.system_prompt_tokens if profile else 0
    return baseline + zeref_wrapper_tokens + user_content_tokens


def relative_cost(profile: TargetProfile | None,
                  input_tokens: int,
                  output_tokens: int) -> float:
    """Return an abstract cost score relative to Sonnet 4.6 baseline (1.0)."""
    if profile is None:
        return float(input_tokens) + float(output_tokens)
    return (float(input_tokens) * profile.input_cost_multiplier
            + float(output_tokens) * profile.output_cost_multiplier)


def caveman_skip_categories(profile: TargetProfile | None) -> Iterable[str]:
    """Categories caveman-handoff can safely drop when this target is the recipient."""
    if profile is None:
        return ()
    return profile.already_knows
