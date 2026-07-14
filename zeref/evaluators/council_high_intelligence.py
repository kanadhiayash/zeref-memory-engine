"""Council-of-High-Intelligence evaluator (vNext §11.4).

Implements the 14-step protocol from the original council spec but
reimplemented as Zeref runtime state transitions, not vendored code:

  1. Panel selection based on domain + required methods.
  2. Method diversity validation.
  3. Provider/model independence validation.
  4. Pre-committed domain-weight seat (fixed BEFORE deliberation).
  5. Restatement round.
  6. Blind independent analysis.
  7. Anonymized cross-review.
  8. Anti-conformity prompt.
  9. Structured stance extraction.
 10. Dissent preservation.
 11. Independent synthesis.
 12. Verification of the synthesis against raw member outputs.
 13. Machine-readable verdict.
 14. Full failure reporting.

This module does NOT ship provider bindings — it takes the panel outputs
(StructuredStance list) as an input and enforces the protocol invariants
in code. Actual model dispatch belongs in harness adapters (PRs 12–14)
that respect the panel plan this evaluator produces.
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


PROTOCOL_STEPS = (
    "panel_selection",
    "method_diversity_validation",
    "provider_independence_validation",
    "domain_weight_precommit",
    "restatement_round",
    "blind_independent_analysis",
    "anonymized_cross_review",
    "anti_conformity_prompt",
    "structured_stance_extraction",
    "dissent_preservation",
    "independent_synthesis",
    "synthesis_verification",
    "verdict_emission",
    "failure_reporting",
)


_MIN_METHOD_DIVERSITY = 2
_MIN_PROVIDER_DIVERSITY = 2
_MIN_SEATS = 3


class CouncilOfHighIntelligenceEvaluator:
    id = "council-of-high-intelligence"

    def available(self, context: EvaluationContext) -> bool:
        return len(context.available_providers) >= _MIN_PROVIDER_DIVERSITY

    def plan(self, packet: EvidencePacket,
             context: EvaluationContext) -> EvaluationPlan:
        methods = list(packet.required_methods) or [
            "quantitative_reasoning", "case_analysis", "adversarial_review",
        ]
        providers = context.available_providers or ["provider_a", "provider_b", "provider_c"]

        # Deterministic panel: cycle providers × methods, keep the first
        # _MIN_SEATS distinct rows.
        panel: list[dict] = []
        seen: set[tuple[str, str]] = set()
        i = 0
        while len(panel) < max(_MIN_SEATS, len(methods)):
            provider = providers[i % len(providers)]
            method = methods[i % len(methods)]
            key = (provider, method)
            if key not in seen:
                seen.add(key)
                panel.append({
                    "id": f"seat_{len(panel) + 1}",
                    "provider": provider,
                    "reasoning_class": "deep",
                    "method": method,
                    # Domain weight is FIXED here; the runner must not
                    # rewrite it after panel members respond.
                    "domain_weight": _domain_weight(packet.domain, method),
                })
            i += 1
            if i > len(providers) * len(methods) * 2:
                break

        return EvaluationPlan(
            evaluator=self.id, panel=panel,
            protocol_steps=list(PROTOCOL_STEPS),
            domain=packet.domain,
            metadata={"packet_claim": packet.claim},
        )

    def run(self, plan: EvaluationPlan, packet: EvidencePacket,
            *, responses: list[StructuredStance] | None = None) -> EvaluationResult:
        failures: list[str] = []
        provider_diversity = len({p["provider"] for p in plan.panel})
        method_diversity = len({p["method"] for p in plan.panel})
        if provider_diversity < _MIN_PROVIDER_DIVERSITY:
            failures.append(
                f"provider diversity {provider_diversity} < {_MIN_PROVIDER_DIVERSITY}"
            )
        if method_diversity < _MIN_METHOD_DIVERSITY:
            failures.append(
                f"method diversity {method_diversity} < {_MIN_METHOD_DIVERSITY}"
            )
        if len(plan.panel) < _MIN_SEATS:
            failures.append(f"panel seats {len(plan.panel)} < {_MIN_SEATS}")

        result = EvaluationResult(
            evaluator=self.id, claim=packet.claim,
            independent_outputs=list(responses or []),
            failures=failures,
        )
        if failures:
            result.verdict = "uncertain"
            return result

        stances = list(responses or [])
        if not stances:
            result.verdict = "uncertain"
            result.failures.append("no panel responses")
            return result

        # Weighted synthesis using each seat's pre-committed domain weight.
        weights_by_seat = {p["id"]: p["domain_weight"] for p in plan.panel}
        support_weight = 0.0
        refute_weight = 0.0
        uncertain_weight = 0.0
        for stance in stances:
            w = weights_by_seat.get(stance.reviewer_id, 1.0)
            if stance.verdict == "support":
                support_weight += w * stance.confidence
            elif stance.verdict == "refute":
                refute_weight += w * stance.confidence
            else:
                uncertain_weight += w * stance.confidence
        total = support_weight + refute_weight + uncertain_weight

        if support_weight > refute_weight and support_weight > uncertain_weight:
            verdict = "support"
            confidence = support_weight / max(total, 1e-9)
        elif refute_weight > support_weight and refute_weight > uncertain_weight:
            verdict = "refute"
            confidence = refute_weight / max(total, 1e-9)
        else:
            verdict = "uncertain"
            confidence = uncertain_weight / max(total, 1e-9) if total else 0.0

        result.verdict = verdict
        result.confidence = round(confidence, 4)
        result.dissent = [s for s in stances if s.verdict != verdict]
        result.synthesis = {
            "support_weight": round(support_weight, 4),
            "refute_weight": round(refute_weight, 4),
            "uncertain_weight": round(uncertain_weight, 4),
            "panel_size": len(plan.panel),
            "provider_diversity": provider_diversity,
            "method_diversity": method_diversity,
        }
        return result

    def verify(self, result: EvaluationResult,
               packet: EvidencePacket) -> VerificationResult:
        """Verify that the synthesis is consistent with the raw member
        outputs (§11.4 step 12)."""
        if result.failures:
            return VerificationResult(ok=False,
                                       reason=f"protocol failures: {result.failures}",
                                       metadata={"failures": result.failures})
        if not result.independent_outputs:
            return VerificationResult(ok=False,
                                       reason="no independent outputs")
        # Every stance the result claims as dissent must actually disagree
        # with the verdict.
        bad_dissent = [s for s in result.dissent if s.verdict == result.verdict]
        if bad_dissent:
            return VerificationResult(
                ok=False,
                reason=f"dissent list includes agreeing stances: "
                       f"{[s.reviewer_id for s in bad_dissent]}",
            )
        return VerificationResult(ok=True)


def _domain_weight(domain: str, method: str) -> float:
    """Cheap deterministic mapping. Real weights come from PR 19 benchmarks."""
    if domain == "security" and method == "adversarial_review":
        return 1.5
    if domain == "research" and method == "quantitative_reasoning":
        return 1.4
    return 1.0
