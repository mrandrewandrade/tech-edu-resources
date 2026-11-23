"""Run a controller through a teacher-verified libgpiod 2.x configuration."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from tej_platform.alarm import AlarmController
from tej_platform.event_log import EventLogger
from tej_platform.gpio_adapter import GPIODAdapter, GPIOUnavailable
from tej_platform.traffic_light import TrafficController


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("system", choices=("alarm", "traffic"))
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--log", type=Path, default=Path("events.csv"))
    parser.add_argument("--interval", type=float, default=0.05)
    args = parser.parse_args()
    if args.interval <= 0:
        parser.error("--interval must be positive")

    controller = AlarmController() if args.system == "alarm" else TrafficController()
    logger = EventLogger(args.log, data_origin="physical-gpio")
    started = time.monotonic()

    try:
        with GPIODAdapter.from_json(args.config) as adapter:
            print("GPIO active. Press Ctrl+C for a safe output shutdown.")
            while True:
                now_s = time.monotonic() - started
                inputs = adapter.read_inputs()
                result = controller.step(inputs, now_s)
                adapter.write_outputs(result.outputs)
                if result.transitioned or result.event:
                    logger.log(result, inputs, elapsed_s=now_s)
                time.sleep(args.interval)
    except KeyboardInterrupt:
        print("Stopping; controlled outputs were set inactive.")
        return 0
    except (GPIOUnavailable, OSError, ValueError) as exc:
        print(f"GPIO start refused: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
