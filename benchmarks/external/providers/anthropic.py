"""
privacy-audit: allow-file "Provider stub names the API-key env var and pricing schema as spec; no credential values, no user data."

Anthropic provider adapter stub (Phase A — no API calls).

Reads ANTHROPIC_API_KEY from the environment (never stored, never printed),
records cost per call, and supports a dry-run mode that estimates token
counts without touching the API. Live inference is Phase B and stays disabled
here so no paid call can happen from Phase A code paths.
"""

from __future__ import annotations

import os

from benchmarks.external.providers.base import Completion, Provider, Usage

DEFAULT_MODEL_ID = "claude-sonnet-4-5"

# PLACEHOLDER pricing (USD per million tokens) for dry-run cost ESTIMATES only.
# Must be re-verified against the official Anthropic pricing page before any
# Phase B live run publishes cost numbers.
PRICING_USD_PER_MTOK: dict[str, tuple[float, float]] = {
    "claude-sonnet-4-5": (3.0, 15.0),
    "claude-haiku-4-5": (1.0, 5.0),
    "claude-opus-4-1": (15.0, 75.0),
}

# Rough chars-per-token heuristic for dry-run estimates (no tokenizer, no API).
CHARS_PER_TOKEN = 4


class AnthropicProvider(Provider):
    name = "anthropic"

    def __init__(self, model_id: str = DEFAULT_MODEL_ID, dry_run: bool = True) -> None:
        self.model_id = model_id
        self.dry_run = dry_run
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.total_cost_usd = 0.0
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def estimate(self, prompt: str, expected_output_tokens: int = 256) -> Usage:
        input_tokens = max(1, len(prompt) // CHARS_PER_TOKEN)
        in_rate, out_rate = PRICING_USD_PER_MTOK.get(self.model_id, (3.0, 15.0))
        cost = (input_tokens * in_rate + expected_output_tokens * out_rate) / 1_000_000
        usage = Usage(
            input_tokens=input_tokens,
            output_tokens=expected_output_tokens,
            cost_usd=cost,
            estimated=True,
        )
        self._record(usage)
        return usage

    def complete(self, prompt: str) -> Completion:
        if self.dry_run:
            return Completion(text="", usage=self.estimate(prompt))
        raise RuntimeError(
            "Live Anthropic inference is disabled in WS5 Phase A. Phase B "
            "(budget-gated) will implement gated API calls. Use dry_run=True."
        )

    def _record(self, usage: Usage) -> None:
        self.total_cost_usd += usage.cost_usd
        self.total_input_tokens += usage.input_tokens
        self.total_output_tokens += usage.output_tokens
