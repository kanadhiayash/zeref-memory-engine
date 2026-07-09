"""Claude handoff wrapper."""

from zeref.handoff.compiler import compile_handoff


def build(root=".", objective="Continue from current Zeref memory state."):
    return compile_handoff(root, target="claude", objective=objective)
