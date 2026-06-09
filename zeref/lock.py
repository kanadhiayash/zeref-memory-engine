"""
zeref.lock — Advisory single-writer lock + atomic write helpers (v2.5 L9 + L10).

Closes Phase C V06/V11 (single-writer race) and Phase B Recovery gap.

Two primitives:

1. MemoryLock — context manager. Creates memory/.lock atomically via O_EXCL.
   Second writer aborts with LockError containing holder PID + timestamp.

2. atomic_write(path, content) — write to <path>.tmp, fsync, rename.
   On crash mid-write, the original file is preserved intact.

Usage:
    from zeref.lock import MemoryLock, atomic_write, LockError
    with MemoryLock(Path("memory")):
        atomic_write(Path("memory/DECISIONS.md"), new_content)
"""

from __future__ import annotations

import os
import time
from pathlib import Path


class LockError(RuntimeError):
    """Raised when memory/.lock is already held by another writer."""


class MemoryLock:
    """Advisory POSIX lock for the memory/ tree using O_CREAT|O_EXCL."""

    def __init__(self, memory_dir: Path, timeout_seconds: int = 0):
        self.lockfile = memory_dir / ".lock"
        self.timeout = timeout_seconds
        self._fd: int | None = None

    def acquire(self) -> None:
        deadline = time.monotonic() + max(0, self.timeout)
        first = True
        while True:
            try:
                self._fd = os.open(
                    str(self.lockfile),
                    os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                    0o600,
                )
                holder = f"pid={os.getpid()}\nacquired={time.time()}\n"
                os.write(self._fd, holder.encode())
                return
            except FileExistsError:
                if first and self.timeout == 0:
                    raise LockError(
                        f"memory/.lock held by {self._read_holder()}. Another writer is active."
                    )
                first = False
                if time.monotonic() >= deadline:
                    raise LockError(
                        f"timed out waiting for memory/.lock (held by {self._read_holder()})"
                    )
                time.sleep(0.05)

    def release(self) -> None:
        if self._fd is not None:
            try:
                os.close(self._fd)
            except OSError:
                pass
            self._fd = None
        try:
            self.lockfile.unlink()
        except FileNotFoundError:
            pass

    def _read_holder(self) -> str:
        try:
            return self.lockfile.read_text(errors="ignore").strip().replace("\n", " ")
        except Exception:
            return "<unknown>"

    def __enter__(self) -> "MemoryLock":
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.release()


def atomic_write(path: Path, content: str) -> None:
    """Write content to path atomically: tmp -> fsync -> replace."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.parent.mkdir(parents=True, exist_ok=True)

    fd = os.open(str(tmp), os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o644)
    try:
        os.write(fd, content.encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(tmp, path)


def atomic_append(path: Path, content: str) -> None:
    """Append-only variant — read current, append, atomic_write back."""
    existing = path.read_text() if path.exists() else ""
    atomic_write(path, existing + content)
