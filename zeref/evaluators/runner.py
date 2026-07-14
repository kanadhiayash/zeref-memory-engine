"""Runner — persists an evaluator run to PR 2's ``evaluator_runs`` table
+ appends a hash-chained ``evaluator.ran`` event."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from zeref.evaluators.base import (
    EvaluationContext,
    EvaluationPlan,
    EvaluationResult,
    EvidencePacket,
    StructuredStance,
)
from zeref.evaluators.registry import resolve_evaluator
from zeref.storage import EventEnvelope, EventLog, StateDB


class EvaluatorRunFailure(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def run_evaluator(root: Path | str,
                  *,
                  evaluator_id: str,
                  packet: EvidencePacket,
                  context: EvaluationContext,
                  responses: list[StructuredStance] | None = None) -> EvaluationResult:
    """End-to-end: plan → run → verify → persist. Returns the result;
    caller decides how to store it in memory."""
    evaluator = resolve_evaluator(evaluator_id)
    if not evaluator.available(context):
        raise EvaluatorRunFailure(
            f"evaluator {evaluator_id!r} not available under current context "
            f"(providers={context.available_providers})"
        )

    plan = evaluator.plan(packet, context)
    result = evaluator.run(plan, packet, responses=responses)
    verification = evaluator.verify(result, packet)
    if not verification.ok:
        result.failures.append(f"verification: {verification.reason}")

    root = Path(root)
    db = StateDB(root); db.migrate()
    conn = db.connect()
    try:
        conn.execute(
            """
            INSERT INTO evaluator_runs
                (id, evaluator, panel_json, provider_metadata_json,
                 independent_outputs_json, dissent_json, verdict,
                 failures, run_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "er_" + uuid.uuid4().hex[:16],
                evaluator_id,
                json.dumps(plan.panel, sort_keys=True),
                json.dumps(result.provider_metadata, sort_keys=True),
                json.dumps([_stance_to_dict(s) for s in result.independent_outputs],
                            sort_keys=True),
                json.dumps([_stance_to_dict(s) for s in result.dissent],
                            sort_keys=True),
                result.verdict,
                json.dumps(result.failures, sort_keys=True),
                _now(),
            ),
        )
        conn.commit()
        log = EventLog(root, mirror_conn=conn)
        log.append(EventEnvelope(
            event_type="evaluator.ran",
            actor="evaluator-runner",
            target=f"evaluator:{evaluator_id}",
            payload={
                "claim": packet.claim,
                "verdict": result.verdict,
                "confidence": result.confidence,
                "panel_size": len(plan.panel),
                "failures": result.failures,
            },
        ))
    finally:
        db.close()
    return result


def _stance_to_dict(s: StructuredStance) -> dict:
    return {
        "reviewer_id": s.reviewer_id,
        "verdict": s.verdict,
        "confidence": s.confidence,
        "reasons": list(s.reasons),
        "counterarguments": list(s.counterarguments),
        "citations": list(s.citations),
    }
