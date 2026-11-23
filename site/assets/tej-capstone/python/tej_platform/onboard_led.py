"""Inspect and momentarily blink a teacher-approved Linux LED device."""

from __future__ import annotations

import argparse
import re
import time
from pathlib import Path


LED_ROOT = Path("/sys/class/leds")


def available_leds(root: Path = LED_ROOT) -> list[str]:
    if not root.is_dir():
        return []
    return sorted(path.name for path in root.iterdir() if path.is_dir())


def selected_trigger(text: str) -> str | None:
    match = re.search(r"\[([^\]]+)\]", text)
    return match.group(1) if match else None


def blink_led(name: str, *, count: int, interval_s: float, root: Path = LED_ROOT) -> None:
    if count <= 0 or interval_s <= 0:
        raise ValueError("count and interval must be positive")
    if name not in available_leds(root):
        raise ValueError("choose an LED name returned by --list on this exact board")
    led = root / name
    brightness_path = led / "brightness"
    trigger_path = led / "trigger"
    original_brightness = brightness_path.read_text(encoding="utf-8").strip()
    original_trigger = (
        selected_trigger(trigger_path.read_text(encoding="utf-8"))
        if trigger_path.exists()
        else None
    )
    try:
        if trigger_path.exists():
            trigger_path.write_text("none", encoding="utf-8")
        for _ in range(count):
            brightness_path.write_text("1", encoding="utf-8")
            time.sleep(interval_s)
            brightness_path.write_text("0", encoding="utf-8")
            time.sleep(interval_s)
    finally:
        try:
            brightness_path.write_text(original_brightness, encoding="utf-8")
            if original_trigger and trigger_path.exists():
                trigger_path.write_text(original_trigger, encoding="utf-8")
        except OSError:
            print("Warning: ask the teacher to check the LED trigger and brightness state.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="list LED device names")
    parser.add_argument("--name", help="exact teacher-approved LED device name")
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument("--interval", type=float, default=0.25)
    args = parser.parse_args()

    if args.list:
        for name in available_leds():
            print(name)
        return 0
    if not args.name:
        parser.error("use --list first, then provide --name")
    try:
        blink_led(args.name, count=args.count, interval_s=args.interval)
    except PermissionError:
        print("Permission denied. Do not use sudo unless the teacher approves the exact command.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
