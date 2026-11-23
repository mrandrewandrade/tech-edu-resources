"""Shared values exchanged between controllers and hardware adapters."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class InputSnapshot:
    """Logical inputs for all supported projects.

    Adapters leave unused inputs False and may leave ``ambient_value`` unset.
    Values are logical: an active-low physical button is still ``True`` when
    pressed after the adapter has interpreted the electrical level.
    """

    arm: bool = False
    disarm: bool = False
    trigger: bool = False
    silence: bool = False
    pedestrian: bool = False
    ambient_value: float | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class OutputSnapshot:
    """Logical outputs shared by alarm, traffic-light, and extension projects."""

    red: bool = False
    yellow: bool = False
    green: bool = False
    status: bool = False
    alarm: bool = False
    relay: bool = False
    pedestrian_walk: bool = False

    def as_dict(self) -> dict[str, bool]:
        return asdict(self)


@dataclass(frozen=True)
class ControllerResult:
    """One deterministic controller result for logging and adapters."""

    system: str
    state: str
    outputs: OutputSnapshot
    event: str = ""
    transitioned: bool = False
