"""Plot a TEJ platform CSV event log with matplotlib."""

from __future__ import annotations

import argparse
from pathlib import Path

from tej_platform.event_log import read_event_rows


def _as_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def plot_events(csv_path: Path, output_path: Path) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError(
            "matplotlib is not installed; ask the teacher before installing packages"
        ) from exc

    rows = read_event_rows(csv_path)
    if not rows:
        raise ValueError("event log contains no data rows")
    times = [float(row["elapsed_s"]) for row in rows]
    state_names = list(dict.fromkeys(row["state"] for row in rows))
    state_index = {name: index for index, name in enumerate(state_names)}
    states = [state_index[row["state"]] for row in rows]

    figure, axes = plt.subplots(3, 1, sharex=True, figsize=(10, 7), constrained_layout=True)
    axes[0].step(times, states, where="post")
    axes[0].set_yticks(range(len(state_names)), labels=state_names)
    axes[0].set_ylabel("state")
    axes[0].grid(alpha=0.3)

    for column, label in (
        ("output_red", "red"),
        ("output_yellow", "yellow"),
        ("output_green", "green"),
        ("output_alarm", "alarm"),
        ("output_relay", "relay"),
    ):
        axes[1].step(times, [int(row[column]) for row in rows], where="post", label=label)
    axes[1].set_ylabel("logical output")
    axes[1].set_yticks([0, 1])
    axes[1].legend(ncol=5, loc="upper center")
    axes[1].grid(alpha=0.3)

    ambient = [_as_float(row["ambient_value"]) for row in rows]
    valid_ambient = [(time_s, value) for time_s, value in zip(times, ambient) if value is not None]
    if valid_ambient:
        axes[2].plot(
            [item[0] for item in valid_ambient],
            [item[1] for item in valid_ambient],
            marker="o",
        )
        unit = next((row["ambient_unit"] for row in rows if row["ambient_unit"]), "value")
        axes[2].set_ylabel(f"ambient ({unit})")
    else:
        axes[2].text(0.5, 0.5, "No ambient values recorded", ha="center", va="center")
        axes[2].set_ylabel("ambient")
    axes[2].set_xlabel("elapsed time (s)")
    axes[2].grid(alpha=0.3)
    figure.suptitle(f"{rows[0]['system']} event log — {rows[0]['data_origin']} data")
    figure.savefig(output_path, dpi=160)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output", type=Path, default=Path("event-plot.png"))
    args = parser.parse_args()
    try:
        plot_events(args.csv, args.output)
    except (RuntimeError, ValueError) as exc:
        print(exc)
        return 2
    print(f"saved {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
