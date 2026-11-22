"""Deterministic traffic-light and pedestrian-request state machine."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .model import ControllerResult, InputSnapshot, OutputSnapshot


class TrafficState(str, Enum):
    RED = "RED"
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    WALK = "WALK"


@dataclass(frozen=True)
class TrafficConfig:
    red_s: float = 3.0
    green_s: float = 5.0
    yellow_s: float = 2.0
    walk_s: float = 4.0

    def __post_init__(self) -> None:
        values = (self.red_s, self.green_s, self.yellow_s, self.walk_s)
        if any(value <= 0 for value in values):
            raise ValueError("all traffic-light durations must be positive")


class TrafficController:
    """Cycle lights and insert a protected WALK phase after yellow."""

    def __init__(self, config: TrafficConfig | None = None) -> None:
        self.config = config or TrafficConfig()
        self.state = TrafficState.RED
        self._state_entered_at: float | None = None
        self._pedestrian_waiting = False

    def reset(self, now_s: float = 0.0) -> ControllerResult:
        self.state = TrafficState.RED
        self._state_entered_at = now_s
        self._pedestrian_waiting = False
        return self._result(event="reset", transitioned=True)

    def step(self, inputs: InputSnapshot, now_s: float) -> ControllerResult:
        if now_s < 0:
            raise ValueError("now_s must be non-negative")
        if self._state_entered_at is None:
            self._state_entered_at = now_s

        if inputs.pedestrian and self.state is not TrafficState.WALK:
            self._pedestrian_waiting = True

        elapsed = now_s - self._state_entered_at
        previous = self.state
        event = "pedestrian_request_latched" if inputs.pedestrian else ""

        if self.state is TrafficState.RED and elapsed >= self.config.red_s:
            self._enter(TrafficState.GREEN, now_s)
            event = "red_complete"
        elif self.state is TrafficState.GREEN and elapsed >= self.config.green_s:
            self._enter(TrafficState.YELLOW, now_s)
            event = "green_complete"
        elif self.state is TrafficState.YELLOW and elapsed >= self.config.yellow_s:
            next_state = TrafficState.WALK if self._pedestrian_waiting else TrafficState.RED
            self._enter(next_state, now_s)
            event = "walk_started" if next_state is TrafficState.WALK else "yellow_complete"
        elif self.state is TrafficState.WALK and elapsed >= self.config.walk_s:
            self._pedestrian_waiting = False
            self._enter(TrafficState.RED, now_s)
            event = "walk_complete"

        return self._result(event=event, transitioned=self.state is not previous)

    @property
    def pedestrian_waiting(self) -> bool:
        return self._pedestrian_waiting

    def _enter(self, state: TrafficState, now_s: float) -> None:
        self.state = state
        self._state_entered_at = now_s

    def _result(self, *, event: str, transitioned: bool) -> ControllerResult:
        outputs = {
            TrafficState.RED: OutputSnapshot(red=True),
            TrafficState.GREEN: OutputSnapshot(green=True),
            TrafficState.YELLOW: OutputSnapshot(yellow=True),
            TrafficState.WALK: OutputSnapshot(red=True, pedestrian_walk=True),
        }[self.state]
        return ControllerResult(
            system="traffic_light",
            state=self.state.value,
            outputs=outputs,
            event=event,
            transitioned=transitioned,
        )
