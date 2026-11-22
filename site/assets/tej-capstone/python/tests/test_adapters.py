import tempfile
import unittest
from pathlib import Path

from tej_platform.gpio_adapter import LineSpec
from tej_platform.model import InputSnapshot, OutputSnapshot
from tej_platform.onboard_led import available_leds, blink_led, selected_trigger
from tej_platform.simulation import ScriptedAdapter


class AdapterTests(unittest.TestCase):
    def test_scripted_adapter_uses_safe_close(self) -> None:
        adapter = ScriptedAdapter([InputSnapshot(trigger=True)])
        self.assertTrue(adapter.read_inputs().trigger)
        self.assertEqual(adapter.read_inputs(), InputSnapshot())
        adapter.write_outputs(OutputSnapshot(relay=True))
        adapter.close()
        self.assertEqual(adapter.outputs[-1], OutputSnapshot())
        with self.assertRaises(RuntimeError):
            adapter.read_inputs()

    def test_gpio_placeholders_are_rejected_before_import(self) -> None:
        with self.assertRaises(ValueError):
            LineSpec.from_dict(
                {"chip": "/dev/gpiochipREPLACE", "line": "REPLACE_WITH_LINE"}
            )
        spec = LineSpec.from_dict(
            {"chip": "/dev/gpiochip0", "line": 7, "active_low": True, "bias": "pull-up"}
        )
        self.assertEqual(spec.line, 7)
        self.assertTrue(spec.active_low)

    def test_onboard_led_requires_discovered_name_and_restores_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            led = root / "test-led"
            led.mkdir()
            (led / "brightness").write_text("1", encoding="utf-8")
            (led / "trigger").write_text("none timer [heartbeat]", encoding="utf-8")
            self.assertEqual(available_leds(root), ["test-led"])
            self.assertEqual(selected_trigger("none timer [heartbeat]"), "heartbeat")
            blink_led("test-led", count=1, interval_s=0.001, root=root)
            self.assertEqual((led / "brightness").read_text(encoding="utf-8"), "1")
            self.assertEqual((led / "trigger").read_text(encoding="utf-8"), "heartbeat")
            with self.assertRaises(ValueError):
                blink_led("guessed-name", count=1, interval_s=0.001, root=root)


if __name__ == "__main__":
    unittest.main()
