"""Codec protocol + shared types."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol, runtime_checkable


class CodecError(ValueError):
    pass


class DataShape(str, Enum):
    prose = "prose"                # long-form text, rationale, policies
    uniform_records = "uniform_records"  # list of dicts with same keys
    flat_table = "flat_table"      # 2D matrix, header row
    deep_object = "deep_object"    # nested / irregular
    typed_output = "typed_output"  # schema-driven model output


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    error: str | None = None
    metadata: dict | None = None


@runtime_checkable
class ContextCodec(Protocol):
    name: str
    supported_shapes: tuple[DataShape, ...]

    def supports(self, data: object, shape: DataShape) -> bool: ...
    def encode(self, data: object) -> str: ...
    def decode(self, payload: str) -> object: ...
    def validate(self, payload: str) -> ValidationResult: ...
    def estimate_tokens(self, payload: str,
                        tokenizer: str | None = None) -> int: ...


def infer_shape(data: object) -> DataShape:
    """Best-effort classification for the auto-selector."""
    if isinstance(data, str):
        return DataShape.prose
    if isinstance(data, list) and data and all(isinstance(x, dict) for x in data):
        keys = set(data[0].keys())
        if all(set(x.keys()) == keys for x in data):
            first = data[0]
            if all(not isinstance(v, (dict, list)) for v in first.values()):
                return DataShape.uniform_records
        return DataShape.deep_object
    if isinstance(data, list) and data and all(
        isinstance(x, list) and all(not isinstance(y, (dict, list)) for y in x)
        for x in data
    ):
        return DataShape.flat_table
    return DataShape.deep_object


def default_token_estimate(payload: str) -> int:
    """Coarse tokenizer-independent estimate (≈ 4 chars / token). Codecs
    override this when they can produce something better."""
    return max(1, (len(payload) + 3) // 4)
