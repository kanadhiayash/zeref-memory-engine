"""vNext PR 11 gate tests — Council-of-High-Intelligence evaluator adapter."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from zeref.evaluators import (
    EvaluationContext,
    EvidencePacket,
    Evaluator,
    EvaluatorRunFailure,
    list_evaluators,
    resolve_evaluator,
    run_evaluator,
)
from zeref.evaluators.base import StructuredStance
from zeref.evaluators.council_high_intelligence import (
    PROTOCOL_STEPS,
    CouncilOfHighIntelligenceEvaluator,
)
from zeref.evaluators.model_jury import ModelJuryEvaluator
from zeref.evidence.schema import SourceRecord
from zeref.storage import EventLog, StateDB


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

def test_both_evaluators_registered() -> None:
    names = {row["id"] for row in list_evaluators()}
    assert names == {"model-jury", "council-of-high-intelligence"}
    for name in names:
        assert resolve_evaluator(name) is not None


def test_unknown_evaluator_raises() -> None:
    with pytest.raises(KeyError):
        resolve_evaluator("nope")


# ---------------------------------------------------------------------------
# Protocol properties
# ---------------------------------------------------------------------------

def test_council_declares_full_protocol() -> None:
    ctx = EvaluationContext(available_providers=["a", "b", "c"])
    packet = EvidencePacket(claim="x", domain="research")
    plan = CouncilOfHighIntelligenceEvaluator().plan(packet, ctx)
    assert plan.protocol_steps == list(PROTOCOL_STEPS)
    assert len(plan.protocol_steps) == 14


def test_council_requires_minimum_providers() -> None:
    ctx = EvaluationContext(available_providers=["only-one"])
    assert not CouncilOfHighIntelligenceEvaluator().available(ctx)


def test_council_panel_has_diverse_providers_and_methods() -> None:
    ctx = EvaluationContext(available_providers=["a", "b", "c"])
    packet = EvidencePacket(claim="x", domain="research",
                            required_methods=["quantitative_reasoning",
                                              "case_analysis"])
    plan = CouncilOfHighIntelligenceEvaluator().plan(packet, ctx)
    assert len({p["provider"] for p in plan.panel}) >= 2
    assert len({p["method"] for p in plan.panel}) >= 2


def test_council_domain_weight_precommitted() -> None:
    """Every seat has a numeric domain_weight FIXED at plan time —
    the runner may not rewrite it after responses arrive."""
    ctx = EvaluationContext(available_providers=["a", "b", "c"])
    packet = EvidencePacket(claim="claim", domain="security",
                            required_methods=["adversarial_review",
                                              "case_analysis"])
    plan = CouncilOfHighIntelligenceEvaluator().plan(packet, ctx)
    for seat in plan.panel:
        assert isinstance(seat["domain_weight"], (int, float))
        assert seat["domain_weight"] > 0.0
    # Security × adversarial_review should get the boosted weight (1.5).
    adv = [s for s in plan.panel if s["method"] == "adversarial_review"]
    assert adv and adv[0]["domain_weight"] == 1.5


# ---------------------------------------------------------------------------
# Run + verify
# ---------------------------------------------------------------------------

def _panel_stances(plan, *, verdicts) -> list[StructuredStance]:
    stances: list[StructuredStance] = []
    for seat, verdict in zip(plan.panel, verdicts):
        stances.append(StructuredStance(
            reviewer_id=seat["id"], verdict=verdict, confidence=0.8,
            reasons=[f"seat {seat['id']} reasoning"],
        ))
    return stances


def test_council_run_synthesizes_verdict_and_preserves_dissent() -> None:
    ctx = EvaluationContext(available_providers=["a", "b", "c"])
    packet = EvidencePacket(claim="claim", domain="research",
                            required_methods=["quantitative_reasoning",
                                              "case_analysis",
                                              "adversarial_review"])
    ev = CouncilOfHighIntelligenceEvaluator()
    plan = ev.plan(packet, ctx)
    stances = _panel_stances(plan, verdicts=["support", "support", "refute"])
    result = ev.run(plan, packet, responses=stances)
    assert result.verdict == "support"
    assert result.confidence > 0.0
    assert len(result.dissent) == 1
    assert result.dissent[0].verdict == "refute"
    # verification checks dissent list integrity
    ver = ev.verify(result, packet)
    assert ver.ok, ver.reason


def test_council_flags_protocol_failure_when_diversity_too_low() -> None:
    ctx = EvaluationContext(available_providers=["only-a", "only-b"])
    packet = EvidencePacket(claim="claim", domain="general",
                            required_methods=["one_method"])
    ev = CouncilOfHighIntelligenceEvaluator()
    plan = ev.plan(packet, ctx)
    # Force a low-diversity panel by truncating.
    plan.panel = plan.panel[:1]
    stances = _panel_stances(plan, verdicts=["support"])
    result = ev.run(plan, packet, responses=stances)
    assert result.failures
    ver = ev.verify(result, packet)
    assert not ver.ok


def test_council_verify_rejects_stale_dissent_list() -> None:
    ctx = EvaluationContext(available_providers=["a", "b", "c"])
    packet = EvidencePacket(claim="claim", domain="research",
                            required_methods=["quantitative_reasoning",
                                              "case_analysis",
                                              "adversarial_review"])
    ev = CouncilOfHighIntelligenceEvaluator()
    plan = ev.plan(packet, ctx)
    stances = _panel_stances(plan, verdicts=["support", "support", "refute"])
    result = ev.run(plan, packet, responses=stances)
    # Corrupt the dissent list — verifier must catch it.
    result.dissent.append(result.independent_outputs[0])  # a supporter
    ver = ev.verify(result, packet)
    assert not ver.ok
    assert "dissent list" in (ver.reason or "").lower()


# ---------------------------------------------------------------------------
# Model-jury baseline
# ---------------------------------------------------------------------------

def test_model_jury_needs_two_providers() -> None:
    assert not ModelJuryEvaluator().available(
        EvaluationContext(available_providers=["one"])
    )
    assert ModelJuryEvaluator().available(
        EvaluationContext(available_providers=["a", "b"])
    )


def test_model_jury_majority_verdict() -> None:
    ctx = EvaluationContext(available_providers=["a", "b", "c"])
    packet = EvidencePacket(claim="claim")
    ev = ModelJuryEvaluator()
    plan = ev.plan(packet, ctx)
    stances = _panel_stances(plan, verdicts=["support", "support", "refute"])
    result = ev.run(plan, packet, responses=stances)
    assert result.verdict == "support"
    assert result.synthesis["support_count"] == 2
    assert result.synthesis["refute_count"] == 1


# ---------------------------------------------------------------------------
# Runner — persistence + hash-chained event
# ---------------------------------------------------------------------------

def test_run_evaluator_persists_row_and_emits_event(tmp_path: Path) -> None:
    ctx = EvaluationContext(available_providers=["a", "b", "c"])
    packet = EvidencePacket(claim="claim", domain="research",
                            required_methods=["quantitative_reasoning",
                                              "case_analysis",
                                              "adversarial_review"])
    ev = CouncilOfHighIntelligenceEvaluator()
    plan = ev.plan(packet, ctx)
    stances = _panel_stances(plan, verdicts=["support", "support", "refute"])
    result = run_evaluator(
        tmp_path, evaluator_id="council-of-high-intelligence",
        packet=packet, context=ctx, responses=stances,
    )
    assert result.verdict == "support"

    db = StateDB(tmp_path); db.migrate()
    conn = db.connect()
    row = conn.execute(
        "SELECT verdict, failures FROM evaluator_runs "
        "WHERE evaluator=?",
        ("council-of-high-intelligence",),
    ).fetchone()
    db.close()
    assert row is not None
    assert row[0] == "support"
    assert json.loads(row[1]) == []

    log = EventLog(tmp_path)
    types = {e["event_type"] for e in log.iter_events()}
    assert "evaluator.ran" in types
    log.verify_chain()


def test_runner_raises_when_evaluator_unavailable(tmp_path: Path) -> None:
    with pytest.raises(EvaluatorRunFailure):
        run_evaluator(
            tmp_path, evaluator_id="council-of-high-intelligence",
            packet=EvidencePacket(claim="claim"),
            context=EvaluationContext(available_providers=["only-one"]),
        )
