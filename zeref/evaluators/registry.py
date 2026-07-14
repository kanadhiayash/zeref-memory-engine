"""Evaluator registry."""

from __future__ import annotations

from zeref.evaluators.base import Evaluator
from zeref.evaluators.council_high_intelligence import (
    CouncilOfHighIntelligenceEvaluator,
)
from zeref.evaluators.model_jury import ModelJuryEvaluator


class EvaluatorNotFoundError(KeyError):
    pass


_EVALUATORS: dict[str, Evaluator] = {
    "model-jury": ModelJuryEvaluator(),
    "council-of-high-intelligence": CouncilOfHighIntelligenceEvaluator(),
}


def resolve_evaluator(name: str) -> Evaluator:
    if name not in _EVALUATORS:
        raise EvaluatorNotFoundError(
            f"no evaluator {name!r}. Known: {sorted(_EVALUATORS)}"
        )
    return _EVALUATORS[name]


def list_evaluators() -> list[dict]:
    return [{"id": ev.id} for ev in _EVALUATORS.values()]
