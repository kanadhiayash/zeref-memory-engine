"""Model-jury evaluator — cheap N-model majority + dissent.

Deterministic panel selection: cycles through available providers,
pairing each with a distinct reasoning class. Used as the simpler
baseline in the PR-11 council-value benchmark (§11.5).
"""

from __future__ import annotations

from zeref.evaluators.base import (
    EvaluationContext,
    EvaluationPlan,
    EvaluationResult,
    EvidencePacket,
    StructuredStance,
    VerificationResult,
)


class ModelJuryEvaluator:
    id = "model-jury"

    def available(self, context: EvaluationContext) -> bool:
        return len(context.available_providers) >= 2

    def plan(self, packet: EvidencePacket,
             context: EvaluationContext) -> EvaluationPlan:
        classes = ("balanced", "balanced", "deep")
        panel = []
        for i, provider in enumerate(context.available_providers[:3]):
            panel.append({
                "id": f"juror_{i+1}",
                "provider": provider,
                "reasoning_class": classes[i % len(classes)],
                "method": "independent_vote",
                "domain_weight": 1.0,
            })
        return EvaluationPlan(
            evaluator=self.id, panel=panel,
            protocol_steps=[
                "independent_vote", "majority_synthesis",
            ],
            domain=packet.domain,
        )

    def run(self, plan: EvaluationPlan, packet: EvidencePacket,
            *, responses: list[StructuredStance] | None = None) -> EvaluationResult:
        stances = list(responses or [])
        result = EvaluationResult(
            evaluator=self.id, claim=packet.claim,
            independent_outputs=stances,
        )
        if not stances:
            result.verdict = "uncertain"
            result.confidence = 0.0
            return result
        support = [s for s in stances if s.verdict == "support"]
        refute = [s for s in stances if s.verdict == "refute"]
        if len(support) > len(refute):
            result.verdict = "support"
            result.confidence = sum(s.confidence for s in support) / len(support)
        elif len(refute) > len(support):
            result.verdict = "refute"
            result.confidence = sum(s.confidence for s in refute) / len(refute)
        else:
            result.verdict = "uncertain"
            result.confidence = 0.5
        # Dissent = anyone who disagreed with the majority verdict
        result.dissent = [s for s in stances if s.verdict != result.verdict]
        result.synthesis = {
            "support_count": len(support),
            "refute_count": len(refute),
            "uncertain_count": len(stances) - len(support) - len(refute),
        }
        return result

    def verify(self, result: EvaluationResult,
               packet: EvidencePacket) -> VerificationResult:
        if not result.independent_outputs:
            return VerificationResult(ok=False,
                                       reason="no independent outputs")
        return VerificationResult(ok=True)
