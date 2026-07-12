"""Runtime supervisor (vNext PR 8, master plan §10).

Given a persisted CompiledTeamPlan (PR 7 wrote it to
team_runs / team_assignments / execution_steps), the Supervisor drives
the RUN state machine:

    CREATED → COMPILED → AUTHORIZED → RUNNING → VERIFYING → COMPLETED

Failure branches: PAUSED_PERMISSION / PAUSED_BUDGET / RETRYING /
DEGRADED / FAILED / CANCELLED.

Every side-effect action passes through:
  1. zeref.policy.evaluate    — precedence + autonomy
  2. zeref.capabilities.assert_executable — lifecycle + digest gate
  3. adapter.invoke           — the concrete adapter (PR 5)

Every state transition + step outcome writes a hash-chained event
through zeref.storage.EventLog (PR 2).
"""

from zeref.runtime.state_machine import (
    INVALID_RUN_TRANSITION,
    INVALID_STEP_TRANSITION,
    RUN_STATES,
    STEP_STATES,
    can_run_transition,
    can_step_transition,
)
from zeref.runtime.budget import BudgetError, BudgetTracker
from zeref.runtime.supervisor import (
    Supervisor,
    SupervisorError,
    resume,
)

__all__ = [
    "INVALID_RUN_TRANSITION", "INVALID_STEP_TRANSITION",
    "RUN_STATES", "STEP_STATES",
    "can_run_transition", "can_step_transition",
    "BudgetError", "BudgetTracker",
    "Supervisor", "SupervisorError", "resume",
]
