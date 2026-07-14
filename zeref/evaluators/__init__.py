"""Evaluator adapters (vNext PR 11, master plan §11.3–§11.4).

Evaluators consume an EvidencePacket and return an EvaluationResult that
carries structured stances, independent outputs, dissent, and a verdict.
The Council-of-High-Intelligence protocol is implemented as ONE evaluator
adapter — never as Zeref's canonical council. Zeref itself keeps
grading via the evidence engine (PR 10); evaluators just add review
robustness.
"""

from zeref.evaluators.base import (
    EvaluationContext,
    EvaluationPlan,
    EvaluationResult,
    Evaluator,
    EvidencePacket,
    VerificationResult,
)
from zeref.evaluators.registry import (
    EvaluatorNotFoundError,
    list_evaluators,
    resolve_evaluator,
)
from zeref.evaluators.runner import (
    EvaluatorRunFailure,
    run_evaluator,
)

__all__ = [
    "EvaluationContext", "EvaluationPlan", "EvaluationResult",
    "Evaluator", "EvidencePacket", "VerificationResult",
    "EvaluatorNotFoundError", "list_evaluators", "resolve_evaluator",
    "EvaluatorRunFailure", "run_evaluator",
]
