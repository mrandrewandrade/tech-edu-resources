"""Small adapter contract used by every physical-computing project."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .model import InputSnapshot, OutputSnapshot


@runtime_checkable
class IOAdapter(Protocol):
    """Translate between logical project values and one I/O implementation."""

    def read_inputs(self) -> InputSnapshot:
        """Return one logical input snapshot without changing outputs."""

    def write_outputs(self, outputs: OutputSnapshot) -> None:
        """Apply one complete logical output snapshot."""

    def close(self) -> None:
        """Place controlled outputs in their safe inactive state and release I/O."""
