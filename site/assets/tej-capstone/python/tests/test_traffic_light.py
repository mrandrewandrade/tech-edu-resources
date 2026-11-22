import unittest

from tej_platform.model import InputSnapshot
from tej_platform.traffic_light import TrafficConfig, TrafficController


class TrafficControllerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = TrafficController(
            TrafficConfig(red_s=3, green_s=5, yellow_s=2, walk_s=4)
        )

    def test_normal_cycle_without_pedestrian(self) -> None:
        self.assertEqual(self.controller.step(InputSnapshot(), 0).state, "RED")
        self.assertEqual(self.controller.step(InputSnapshot(), 3).state, "GREEN")
        self.assertEqual(self.controller.step(InputSnapshot(), 8).state, "YELLOW")
        result = self.controller.step(InputSnapshot(), 10)
        self.assertEqual(result.state, "RED")
        self.assertFalse(result.outputs.pedestrian_walk)

    def test_pedestrian_request_is_latched_until_walk(self) -> None:
        self.controller.step(InputSnapshot(), 0)
        result = self.controller.step(InputSnapshot(pedestrian=True), 1)
        self.assertTrue(self.controller.pedestrian_waiting)
        self.assertEqual(result.event, "pedestrian_request_latched")
        self.controller.step(InputSnapshot(), 3)
        self.controller.step(InputSnapshot(), 8)
        result = self.controller.step(InputSnapshot(), 10)
        self.assertEqual(result.state, "WALK")
        self.assertTrue(result.outputs.red)
        self.assertTrue(result.outputs.pedestrian_walk)
        result = self.controller.step(InputSnapshot(), 14)
        self.assertEqual(result.state, "RED")
        self.assertFalse(self.controller.pedestrian_waiting)

    def test_invalid_duration_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            TrafficConfig(red_s=0)


if __name__ == "__main__":
    unittest.main()
