"""Evaluator protocol + shared types."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from zeref.evidence.schema import SourceRecord


@dataclass
class EvidencePacket:
    claim: str
    sources: list[SourceRecord] = field(default_factory=list)
    domain: str = "general"
    required_methods: list[str] = field(default_factory=list)  # e.g. ["quantitative", "case-analysis"]
    metadata: dict = field(default_factory=dict)


@dataclass
class EvaluationContext:
    """Runtime info: which providers are wired, session budget, etc."""
    available_providers: list[str] = field(default_factory=list)
    session_budget_usd: float = 0.0
    session_tokens_output_max: int = 0


@dataclass
class EvaluationPlan:
    """What panel + protocol is going to run. Emitted before execution so
    the caller can budget and audit."""
    evaluator: str
    panel: list[dict]                     # [{id, provider, method, domain_weight}]
    protocol_steps: list[str]
    domain: str
    metadata: dict = field(default_factory=dict)


@dataclass
class StructuredStance:
    reviewer_id: str
    verdict: str                          # "support" / "refute" / "uncertain"
    confidence: float                     # 0..1
    reasons: list[str] = field(default_factory=list)
    counterarguments: list[str] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)


@dataclass
class EvaluationResult:
    evaluator: str
    claim: str
    independent_outputs: list[StructuredStance] = field(default_factory=list)
    dissent: list[StructuredStance] = field(default_factory=list)
    synthesis: dict = field(default_factory=dict)
    verdict: str = "uncertain"
    confidence: float = 0.0
    provider_metadata: dict = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)


@dataclass
class VerificationResult:
    ok: bool
    reason: str | None = None
    metadata: dict = field(default_factory=dict)


@runtime_checkable
class Evaluator(Protocol):
    id: str

    def available(self, context: EvaluationContext) -> bool: ...
    def plan(self, packet: EvidencePacket,
             context: EvaluationContext) -> EvaluationPlan: ...
    def run(self, plan: EvaluationPlan,
            packet: EvidencePacket,
            *,
            responses: list[StructuredStance] | None = None) -> EvaluationResult: ...
    def verify(self, result: EvaluationResult,
               packet: EvidencePacket) -> VerificationResult: ...
