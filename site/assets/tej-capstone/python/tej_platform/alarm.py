"""Deterministic alarm state machine with no GPIO dependency."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .model import ControllerResult, InputSnapshot, OutputSnapshot


class AlarmState(str, Enum):
    DISARMED = "DISARMED"
    ARMING = "ARMING"
    ARMED = "ARMED"
    ALARM = "ALARM"
    SILENCED = "SILENCED"


@dataclass(frozen=True)
class AlarmConfig:
    arming_delay_s: float = 5.0
    blink_period_s: float = 0.5

    def __post_init__(self) -> None:
        if self.arming_delay_s < 0:
            raise ValueError("arming_delay_s must be non-negative")
        if self.blink_period_s <= 0:
            raise ValueError("blink_period_s must be positive")


class AlarmController:
    """Advance the alarm from explicit inputs and a monotonic time value."""

    def __init__(self, config: AlarmConfig | None = None) -> None:
        self.config = config or AlarmConfig()
        self.state = AlarmState.DISARMED
        self._state_entered_at: float | None = None

    def reset(self, now_s: float = 0.0) -> ControllerResult:
        self.state = AlarmState.DISARMED
        self._state_entered_at = now_s
        return self._result(event="reset", transitioned=True, now_s=now_s)

    def step(self, inputs: InputSnapshot, now_s: float) -> ControllerResult:
        if now_s < 0:
            raise ValueError("now_s must be non-negative")
        if self._state_entered_at is None:
            self._state_entered_at = now_s

        previous = self.state
        event = ""

        # A disarm request is the safe-state command from every active state.
        if inputs.disarm and self.state is not AlarmState.DISARMED:
            self._enter(AlarmState.DISARMED, now_s)
            event = "disarm_requested"
        elif self.state is AlarmState.DISARMED and inputs.arm:
            self._enter(AlarmState.ARMING, now_s)
            event = "arm_requested"
        elif self.state is AlarmState.ARMING:
            elapsed = now_s - self._state_entered_at
            if elapsed >= self.config.arming_delay_s:
                self._enter(AlarmState.ARMED, now_s)
                event = "arming_delay_complete"
        elif self.state is AlarmState.ARMED and inputs.trigger:
            self._enter(AlarmState.ALARM, now_s)
            event = "trigger_active"
        elif self.state is AlarmState.ALARM and inputs.silence:
            self._enter(AlarmState.SILENCED, now_s)
            event = "silence_requested"
        elif self.state is AlarmState.SILENCED and inputs.arm:
            self._enter(AlarmState.ARMED, now_s)
            event = "rearmed"

        return self._result(
            event=event,
            transitioned=self.state is not previous,
            now_s=now_s,
        )

    def _enter(self, state: AlarmState, now_s: float) -> None:
        self.state = state
        self._state_entered_at = now_s

    def _blink_on(self, now_s: float) -> bool:
        assert self._state_entered_at is not None
        phase = int((now_s - self._state_entered_at) / self.config.blink_period_s)
        return phase % 2 == 0

    def _outputs(self, now_s: float) -> OutputSnapshot:
        if self.state is AlarmState.DISARMED:
            return OutputSnapshot(green=True, status=True)
        if self.state is AlarmState.ARMING:
            return OutputSnapshot(yellow=self._blink_on(now_s), status=True)
        if self.state is AlarmState.ARMED:
            return OutputSnapshot(red=True, status=True)
        if self.state is AlarmState.ALARM:
            active = self._blink_on(now_s)
            return OutputSnapshot(red=active, alarm=True, relay=True, status=True)
        return OutputSnapshot(red=True, status=True)

    def _result(
        self,
        *,
        event: str,
        transitioned: bool,
        now_s: float,
    ) -> ControllerResult:
        return ControllerResult(
            system="alarm",
            state=self.state.value,
            outputs=self._outputs(now_s),
            event=event,
            transitioned=transitioned,
        )
