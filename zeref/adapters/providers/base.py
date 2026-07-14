"""Provider adapter contract.

A provider adapter maps provider-neutral reasoning classes
(``zeref.core.reasoning``) to concrete model identifiers. Mapping data is
declarative JSON shipped next to this module — one file per provider:

.. code-block:: json

    {
      "schema": "zeref.provider/v1",
      "provider": "anthropic",
      "classes": {
        "frontier": {"model_id": "...", "effort": "high",
                      "restrict_to_criticality": "CRITICAL"}
      }
    }

``restrict_to_criticality`` is advisory metadata mirrored from core policy;
enforcement happens in :func:`zeref.core.reasoning.validate_request`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

from zeref.core.reasoning import ModelSpec, ReasoningPolicyError, is_reasoning_class

PROVIDER_SCHEMA = "zeref.provider/v1"


class ProviderAdapter(Protocol):
    provider: str

    def resolve(self, reasoning_class: str) -> ModelSpec: ...

    def supported_classes(self) -> tuple[str, ...]: ...


class JsonProviderAdapter:
    """Provider adapter backed by a declarative JSON mapping file."""

    def __init__(self, path: Path):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if data.get("schema") != PROVIDER_SCHEMA:
            raise ValueError(f"{path}: expected schema {PROVIDER_SCHEMA!r}, got {data.get('schema')!r}")
        self.provider: str = data["provider"]
        self._classes: dict[str, dict] = data["classes"]
        for cls in self._classes:
            if not is_reasoning_class(cls):
                raise ValueError(f"{path}: unknown reasoning class {cls!r}")

    def supported_classes(self) -> tuple[str, ...]:
        return tuple(self._classes)

    def resolve(self, reasoning_class: str) -> ModelSpec:
        entry = self._classes.get(reasoning_class)
        if entry is None:
            raise ReasoningPolicyError(
                f"provider {self.provider!r} has no mapping for reasoning class "
                f"{reasoning_class!r} (supported: {', '.join(self._classes)})"
            )
        return ModelSpec(
            provider=self.provider,
            model_id=entry["model_id"],
            reasoning_class=reasoning_class,
            effort=entry.get("effort"),
        )
