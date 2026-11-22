"""Run an alarm or traffic-light controller without GPIO hardware."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from tej_platform.alarm import AlarmConfig, AlarmController
from tej_platform.event_log import EventLogger
from tej_platform.simulation import TerminalAdapter
from tej_platform.traffic_light import TrafficConfig, TrafficController


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("system", choices=("alarm", "traffic"))
    parser.add_argument("--log", type=Path, default=Path("events.csv"))
    parser.add_argument("--tick", type=float, default=1.0, help="seconds advanced per command")
    args = parser.parse_args()
    if args.tick <= 0:
        parser.error("--tick must be positive")

    controller = (
        AlarmController(AlarmConfig(arming_delay_s=3.0))
        if args.system == "alarm"
        else TrafficController(TrafficConfig(red_s=3, green_s=4, yellow_s=2, walk_s=3))
    )
    adapter = TerminalAdapter()
    logger = EventLogger(args.log, data_origin="simulated-terminal")
    started = time.monotonic()
    simulated_now = 0.0
    print("This is a software simulation. No GPIO is being controlled.")

    try:
        while True:
            try:
                inputs = adapter.read_inputs()
            except ValueError as exc:
                print(exc)
                continue
            result = controller.step(inputs, simulated_now)
            adapter.write_outputs(result.outputs)
            logger.log(result, inputs, elapsed_s=simulated_now)
            print(f"state: {result.state}; event: {result.event or 'none'}")
            simulated_now += args.tick
    except (EOFError, KeyboardInterrupt):
        print("Stopping simulation.")
    finally:
        adapter.close()
        wall_time = time.monotonic() - started
        print(f"saved {args.log} after {wall_time:.1f} s of wall time")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
