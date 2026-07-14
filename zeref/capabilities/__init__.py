"""Capability registry & lifecycle (vNext §8, ADR-0004).

Every external unit of work — a skill, agent, plugin, MCP server, CLI,
repository tool, script, workflow, evaluator, or API service — enters
Zeref through this package. Nothing runs until it is ``approved`` (or a
lifecycle state past it) AND its stored digest still matches the source
on disk.

The single choke point every executor must call:

    from zeref.capabilities import assert_executable
    assert_executable(root, capability_id)   # raises CapabilityGateError
"""

from zeref.capabilities.manifest import (
    CAPABILITY_SCHEMA,
    ManifestError,
    infer_manifest,
    validate_manifest,
)
from zeref.capabilities.lifecycle import (
    LIFECYCLE_STATES,
    EXECUTABLE_STATES,
    InvalidTransition,
    can_transition,
    is_executable,
    next_state_for_digest_change,
)
from zeref.capabilities.discovery import discover
from zeref.capabilities.inspection import inspect_source
from zeref.capabilities.store import (
    CapabilityStore,
    register_discovery,
    approve,
    revoke,
)
from zeref.capabilities.gate import CapabilityGateError, assert_executable

__all__ = [
    "CAPABILITY_SCHEMA",
    "ManifestError", "infer_manifest", "validate_manifest",
    "LIFECYCLE_STATES", "EXECUTABLE_STATES", "InvalidTransition",
    "can_transition", "is_executable", "next_state_for_digest_change",
    "discover", "inspect_source",
    "CapabilityStore", "register_discovery", "approve", "revoke",
    "CapabilityGateError", "assert_executable",
]
