"""Provider adapter interface with mandatory cost recording."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Usage:
    """Token/cost record for one model call (or dry-run estimate)."""

    input_tokens: int
    output_tokens: int
    cost_usd: float
    estimated: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cost_usd": round(self.cost_usd, 6),
            "estimated": self.estimated,
        }


@dataclass(frozen=True)
class Completion:
    text: str
    usage: Usage


class Provider(ABC):
    """Minimal inference interface the harness drives.

    Implementations MUST record usage for every call so results JSON always
    carries a token/cost record. Phase A implementations only support
    ``estimate`` and dry-run ``complete``; live inference is Phase B.
    """

    name: str
    model_id: str

    @abstractmethod
    def estimate(self, prompt: str, expected_output_tokens: int = 256) -> Usage:
        """Estimate token counts and cost WITHOUT calling any API."""

    @abstractmethod
    def complete(self, prompt: str) -> Completion:
        """Run one completion. Phase A: dry-run only (no API calls)."""
