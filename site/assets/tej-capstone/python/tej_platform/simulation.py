"""Adapters for development and tests without physical GPIO."""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable

from .model import InputSnapshot, OutputSnapshot


class ScriptedAdapter:
    """Return queued inputs and record every output for deterministic tests."""

    def __init__(self, inputs: Iterable[InputSnapshot] = ()) -> None:
        self._inputs = deque(inputs)
        self.outputs: list[OutputSnapshot] = []
        self.closed = False

    def read_inputs(self) -> InputSnapshot:
        if self.closed:
            raise RuntimeError("adapter is closed")
        return self._inputs.popleft() if self._inputs else InputSnapshot()

    def write_outputs(self, outputs: OutputSnapshot) -> None:
        if self.closed:
            raise RuntimeError("adapter is closed")
        self.outputs.append(outputs)

    def close(self) -> None:
        if not self.closed:
            self.outputs.append(OutputSnapshot())
            self.closed = True


class TerminalAdapter:
    """Turn one-line terminal commands into logical input snapshots."""

    COMMANDS = {
        "": InputSnapshot(),
        "none": InputSnapshot(),
        "arm": InputSnapshot(arm=True),
        "disarm": InputSnapshot(disarm=True),
        "trigger": InputSnapshot(trigger=True),
        "silence": InputSnapshot(silence=True),
        "walk": InputSnapshot(pedestrian=True),
    }

    def __init__(self) -> None:
        self.closed = False

    def read_inputs(self) -> InputSnapshot:
        if self.closed:
            raise RuntimeError("adapter is closed")
        command = input("command [none/arm/disarm/trigger/silence/walk/quit]: ").strip().lower()
        if command == "quit":
            raise EOFError
        try:
            return self.COMMANDS[command]
        except KeyError as exc:
            choices = ", ".join(self.COMMANDS)
            raise ValueError(f"unknown command {command!r}; choose {choices}") from exc

    def write_outputs(self, outputs: OutputSnapshot) -> None:
        if self.closed:
            raise RuntimeError("adapter is closed")
        active = [name for name, value in outputs.as_dict().items() if value]
        print("outputs:", ", ".join(active) if active else "all inactive")

    def close(self) -> None:
        if not self.closed:
            print("outputs: all inactive")
            self.closed = True
