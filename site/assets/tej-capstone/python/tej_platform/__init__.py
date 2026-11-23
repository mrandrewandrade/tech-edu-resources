"""Reusable, hardware-independent TEJ physical-computing platform."""

from .alarm import AlarmConfig, AlarmController, AlarmState
from .interfaces import IOAdapter
from .model import ControllerResult, InputSnapshot, OutputSnapshot
from .traffic_light import TrafficConfig, TrafficController, TrafficState

__all__ = [
    "AlarmConfig",
    "AlarmController",
    "AlarmState",
    "ControllerResult",
    "IOAdapter",
    "InputSnapshot",
    "OutputSnapshot",
    "TrafficConfig",
    "TrafficController",
    "TrafficState",
]
