"""Portable CSV event logging shared by every controller."""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from .model import ControllerResult, InputSnapshot


FIELDNAMES = [
    "timestamp_utc",
    "elapsed_s",
    "system",
    "state",
    "event",
    "input_arm",
    "input_disarm",
    "input_trigger",
    "input_silence",
    "input_pedestrian",
    "ambient_value",
    "ambient_unit",
    "output_red",
    "output_yellow",
    "output_green",
    "output_status",
    "output_alarm",
    "output_relay",
    "output_pedestrian_walk",
    "data_origin",
]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class EventLogger:
    """Append complete, consistently structured event rows to a CSV file."""

    def __init__(
        self,
        path: str | Path,
        *,
        data_origin: str,
        clock: Callable[[], datetime] = _utc_now,
    ) -> None:
        if not data_origin.strip():
            raise ValueError("data_origin must describe measured, simulated, or synthetic data")
        self.path = Path(path)
        self.data_origin = data_origin.strip()
        self.clock = clock

    def log(
        self,
        result: ControllerResult,
        inputs: InputSnapshot,
        *,
        elapsed_s: float,
        ambient_unit: str = "",
    ) -> None:
        if elapsed_s < 0:
            raise ValueError("elapsed_s must be non-negative")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        new_file = not self.path.exists() or self.path.stat().st_size == 0
        if not new_file:
            self._check_existing_header()

        outputs = result.outputs.as_dict()
        row = {
            "timestamp_utc": self.clock().astimezone(timezone.utc).isoformat(),
            "elapsed_s": f"{elapsed_s:.3f}",
            "system": result.system,
            "state": result.state,
            "event": result.event,
            "input_arm": int(inputs.arm),
            "input_disarm": int(inputs.disarm),
            "input_trigger": int(inputs.trigger),
            "input_silence": int(inputs.silence),
            "input_pedestrian": int(inputs.pedestrian),
            "ambient_value": "" if inputs.ambient_value is None else inputs.ambient_value,
            "ambient_unit": ambient_unit,
            "output_red": int(outputs["red"]),
            "output_yellow": int(outputs["yellow"]),
            "output_green": int(outputs["green"]),
            "output_status": int(outputs["status"]),
            "output_alarm": int(outputs["alarm"]),
            "output_relay": int(outputs["relay"]),
            "output_pedestrian_walk": int(outputs["pedestrian_walk"]),
            "data_origin": self.data_origin,
        }
        with self.path.open("a", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
            if new_file:
                writer.writeheader()
            writer.writerow(row)

    def _check_existing_header(self) -> None:
        with self.path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            header = next(reader, [])
        if header != FIELDNAMES:
            raise ValueError(
                f"refusing to append: {self.path} does not use the platform CSV header"
            )


def read_event_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDNAMES:
            raise ValueError("event file has an unexpected header")
        return list(reader)
