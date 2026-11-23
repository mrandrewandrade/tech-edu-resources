import csv
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from tej_platform.event_log import EventLogger, FIELDNAMES, read_event_rows
from tej_platform.model import ControllerResult, InputSnapshot, OutputSnapshot


class EventLoggerTests(unittest.TestCase):
    def test_write_and_append_stable_csv(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.csv"
            fixed = datetime(2027, 1, 1, 12, 0, tzinfo=timezone.utc)
            logger = EventLogger(
                path,
                data_origin="synthetic-test",
                clock=lambda: fixed,
            )
            result = ControllerResult(
                system="alarm",
                state="ARMED",
                outputs=OutputSnapshot(red=True),
                event="arming_delay_complete",
                transitioned=True,
            )
            logger.log(result, InputSnapshot(), elapsed_s=2)
            logger.log(result, InputSnapshot(trigger=True), elapsed_s=3)

            rows = read_event_rows(path)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["data_origin"], "synthetic-test")
            self.assertEqual(rows[1]["input_trigger"], "1")
            self.assertEqual(rows[0]["output_red"], "1")
            with path.open(newline="", encoding="utf-8") as handle:
                self.assertEqual(next(csv.reader(handle)), FIELDNAMES)

    def test_refuses_unrelated_csv(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.csv"
            path.write_text("wrong,header\n1,2\n", encoding="utf-8")
            logger = EventLogger(path, data_origin="test")
            result = ControllerResult("alarm", "DISARMED", OutputSnapshot())
            with self.assertRaises(ValueError):
                logger.log(result, InputSnapshot(), elapsed_s=0)

    def test_all_published_samples_use_the_platform_schema_and_synthetic_label(self) -> None:
        data_dir = Path(__file__).resolve().parents[2] / "data"
        samples = sorted(data_dir.glob("sample-*-events.csv"))
        self.assertEqual(len(samples), 3)
        for sample in samples:
            rows = read_event_rows(sample)
            self.assertGreater(len(rows), 0, sample.name)
            self.assertTrue(
                all(row["data_origin"] == "synthetic-example" for row in rows),
                sample.name,
            )


if __name__ == "__main__":
    unittest.main()
