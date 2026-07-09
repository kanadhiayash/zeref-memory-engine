"""Structured memory substrate for Zeref.

This package contains the v2 atom schema and append-only JSONL store. The
legacy markdown files remain human-readable views; atoms are the machine-facing
source for new memory work.
"""

from zeref.memory.atom_store import AtomStore
from zeref.memory.schemas import (
    AtomValidationError,
    create_atom,
    make_atom_id,
    validate_atom,
)

__all__ = [
    "AtomStore",
    "AtomValidationError",
    "create_atom",
    "make_atom_id",
    "validate_atom",
]
