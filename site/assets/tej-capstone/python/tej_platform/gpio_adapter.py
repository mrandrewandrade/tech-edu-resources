"""Isolated libgpiod 2.x adapter.

This module intentionally contains no BeagleBone header-to-line mapping. A
teacher must verify each exact board, image, pinmux, gpiochip, and line with the
provided worksheet and ``gpioinfo`` before creating the JSON configuration.
"""

from __future__ import annotations

import json
import warnings
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any

from .model import InputSnapshot, OutputSnapshot


class GPIOUnavailable(RuntimeError):
    """Raised when the configured Linux GPIO interface is unavailable."""


@dataclass(frozen=True)
class LineSpec:
    chip: str
    line: int | str
    active_low: bool = False
    bias: str = "as-is"

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "LineSpec":
        required = {"chip", "line"}
        missing = required - value.keys()
        if missing:
            raise ValueError(f"line specification is missing: {', '.join(sorted(missing))}")
        chip = str(value["chip"])
        line = value["line"]
        if "REPLACE" in chip.upper() or (
            isinstance(line, str) and "REPLACE" in line.upper()
        ):
            raise ValueError("replace all GPIO placeholders with teacher-verified values")
        if not (isinstance(line, int) or isinstance(line, str)):
            raise TypeError("GPIO line must be an integer offset or kernel line name")
        bias = str(value.get("bias", "as-is")).lower()
        if bias not in {"as-is", "disabled", "pull-up", "pull-down"}:
            raise ValueError(f"unsupported GPIO bias: {bias}")
        return cls(
            chip=chip,
            line=line,
            active_low=bool(value.get("active_low", False)),
            bias=bias,
        )


class GPIODAdapter:
    """Map verified GPIO lines to the platform's logical I/O contract."""

    INPUT_NAMES = {field.name for field in fields(InputSnapshot)} - {"ambient_value"}
    OUTPUT_NAMES = {field.name for field in fields(OutputSnapshot)}

    def __init__(
        self,
        inputs: dict[str, LineSpec],
        outputs: dict[str, LineSpec],
    ) -> None:
        unknown_inputs = set(inputs) - self.INPUT_NAMES
        unknown_outputs = set(outputs) - self.OUTPUT_NAMES
        if unknown_inputs or unknown_outputs:
            raise ValueError(
                f"unknown logical lines; inputs={sorted(unknown_inputs)}, "
                f"outputs={sorted(unknown_outputs)}"
            )
        self._gpiod = self._load_gpiod_v2()
        self._input_requests: dict[str, tuple[Any, int | str]] = {}
        self._output_requests: dict[str, tuple[Any, int | str]] = {}
        self._closed = False
        self.cleanup_errors: list[str] = []

        try:
            for name, spec in inputs.items():
                request = self._request_input(spec, consumer=f"tej-input-{name}")
                self._input_requests[name] = (request, spec.line)
            for name, spec in outputs.items():
                request = self._request_output(spec, consumer=f"tej-output-{name}")
                self._output_requests[name] = (request, spec.line)
        except Exception:
            self.close()
            raise

    @classmethod
    def from_json(cls, path: str | Path) -> "GPIODAdapter":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        inputs = {
            name: LineSpec.from_dict(spec) for name, spec in data.get("inputs", {}).items()
        }
        outputs = {
            name: LineSpec.from_dict(spec) for name, spec in data.get("outputs", {}).items()
        }
        if not inputs and not outputs:
            raise ValueError("GPIO configuration contains no inputs or outputs")
        return cls(inputs=inputs, outputs=outputs)

    @staticmethod
    def _load_gpiod_v2() -> Any:
        try:
            import gpiod  # type: ignore
        except ImportError as exc:
            raise GPIOUnavailable(
                "Python gpiod is not installed; stop and ask the teacher to verify the image"
            ) from exc
        if not hasattr(gpiod, "request_lines") or not hasattr(gpiod, "LineSettings"):
            raise GPIOUnavailable(
                "this adapter requires libgpiod Python API 2.x; do not guess an older API mapping"
            )
        return gpiod

    def _bias(self, name: str) -> Any:
        bias = self._gpiod.line.Bias
        return {
            "as-is": bias.AS_IS,
            "disabled": bias.DISABLED,
            "pull-up": bias.PULL_UP,
            "pull-down": bias.PULL_DOWN,
        }[name]

    def _request_input(self, spec: LineSpec, *, consumer: str) -> Any:
        settings = self._gpiod.LineSettings(
            direction=self._gpiod.line.Direction.INPUT,
            bias=self._bias(spec.bias),
            active_low=spec.active_low,
        )
        return self._gpiod.request_lines(
            spec.chip,
            consumer=consumer,
            config={spec.line: settings},
        )

    def _request_output(self, spec: LineSpec, *, consumer: str) -> Any:
        settings = self._gpiod.LineSettings(
            direction=self._gpiod.line.Direction.OUTPUT,
            active_low=spec.active_low,
            output_value=self._gpiod.line.Value.INACTIVE,
        )
        return self._gpiod.request_lines(
            spec.chip,
            consumer=consumer,
            config={spec.line: settings},
        )

    def read_inputs(self) -> InputSnapshot:
        self._require_open()
        values: dict[str, bool] = {}
        for name, (request, line) in self._input_requests.items():
            values[name] = request.get_value(line) == self._gpiod.line.Value.ACTIVE
        return InputSnapshot(**values)

    def write_outputs(self, outputs: OutputSnapshot) -> None:
        self._require_open()
        values = outputs.as_dict()
        for name, (request, line) in self._output_requests.items():
            level = (
                self._gpiod.line.Value.ACTIVE
                if values[name]
                else self._gpiod.line.Value.INACTIVE
            )
            request.set_value(line, level)

    def close(self) -> None:
        if self._closed:
            return
        for request, line in self._output_requests.values():
            try:
                request.set_value(line, self._gpiod.line.Value.INACTIVE)
            except Exception as exc:
                self.cleanup_errors.append(f"could not deactivate output line {line!r}: {exc}")
        for request, _line in [
            *self._output_requests.values(),
            *self._input_requests.values(),
        ]:
            try:
                request.release()
            except Exception as exc:
                self.cleanup_errors.append(f"could not release GPIO request: {exc}")
        self._closed = True
        if self.cleanup_errors:
            warnings.warn(
                "GPIO cleanup needs teacher inspection: " + "; ".join(self.cleanup_errors),
                RuntimeWarning,
                stacklevel=2,
            )

    def _require_open(self) -> None:
        if self._closed:
            raise RuntimeError("GPIO adapter is closed")

    def __enter__(self) -> "GPIODAdapter":
        return self

    def __exit__(self, *_args: Any) -> None:
        self.close()
