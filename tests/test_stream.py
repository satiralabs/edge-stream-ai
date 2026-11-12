"""
Tests for EdgeStream AI: Downsampling, motion delta computation, and dispatcher.
"""

import unittest
from edge_stream.detector import MotionDetector
from edge_stream.dispatcher import AlertDispatcher


class TestEdgeStream(unittest.TestCase):
    def test_motion_detection_logic(self):
        detector = MotionDetector(grid_w=4, grid_h=4, sensitivity_threshold=0.25)
        # 16 total cells
        base = [50] * 16
        res0 = detector.process_frame(base)
        self.assertFalse(res0["motion_detected"])

        # Change 1 cell (1/16 = 0.0625 < 0.25)
        minor = list(base)
        minor[0] = 120
        res1 = detector.process_frame(minor)
        self.assertFalse(res1["motion_detected"])

        # Change 5 cells (5/16 = 0.3125 >= 0.25)
        major = list(minor)
        for i in range(1, 6):
            major[i] = 200
        res2 = detector.process_frame(major)
        self.assertTrue(res2["motion_detected"])

    def test_downsample_buffer(self):
        detector = MotionDetector(grid_w=2, grid_h=2)
        raw_pixels = bytes([10, 20, 30, 40] * 4)  # 16 bytes
        grid = detector.downsample_buffer(raw_pixels, width=4, height=4)
        self.assertEqual(len(grid), 4)


if __name__ == "__main__":
    unittest.main()
