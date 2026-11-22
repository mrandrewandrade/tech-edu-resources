import unittest

from tej_platform.alarm import AlarmConfig, AlarmController, AlarmState
from tej_platform.model import InputSnapshot


class AlarmControllerTests(unittest.TestCase):
    def test_complete_alarm_sequence(self) -> None:
        controller = AlarmController(AlarmConfig(arming_delay_s=2, blink_period_s=0.5))

        result = controller.step(InputSnapshot(arm=True), 0)
        self.assertEqual(result.state, AlarmState.ARMING.value)
        self.assertTrue(result.transitioned)
        self.assertEqual(result.event, "arm_requested")

        self.assertEqual(controller.step(InputSnapshot(), 1.9).state, "ARMING")
        result = controller.step(InputSnapshot(), 2.0)
        self.assertEqual(result.state, "ARMED")
        self.assertTrue(result.outputs.red)

        result = controller.step(InputSnapshot(trigger=True), 2.1)
        self.assertEqual(result.state, "ALARM")
        self.assertTrue(result.outputs.alarm)
        self.assertTrue(result.outputs.relay)

        result = controller.step(InputSnapshot(silence=True), 2.2)
        self.assertEqual(result.state, "SILENCED")
        self.assertFalse(result.outputs.alarm)
        self.assertFalse(result.outputs.relay)

        result = controller.step(InputSnapshot(disarm=True), 2.3)
        self.assertEqual(result.state, "DISARMED")
        self.assertTrue(result.outputs.green)

    def test_disarm_is_safe_from_alarm(self) -> None:
        controller = AlarmController(AlarmConfig(arming_delay_s=0))
        controller.step(InputSnapshot(arm=True), 0)
        controller.step(InputSnapshot(), 0)
        controller.step(InputSnapshot(trigger=True), 0)
        result = controller.step(InputSnapshot(disarm=True), 1)
        self.assertEqual(result.state, "DISARMED")
        self.assertFalse(result.outputs.relay)
        self.assertFalse(result.outputs.alarm)

    def test_invalid_configuration_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            AlarmConfig(arming_delay_s=-1)
        with self.assertRaises(ValueError):
            AlarmConfig(blink_period_s=0)


if __name__ == "__main__":
    unittest.main()
