"""
EdgeStream Detector: Ultra-lightweight motion & anomaly analyzer.
Computes frame-to-frame delta using block subsampling (< 5ms on edge CPU).
"""

import math
from typing import Any, Dict, List, Optional, Tuple


class MotionDetector:
    """Detects motion and activity across consecutive downsampled frames."""

    def __init__(self, grid_w: int = 32, grid_h: int = 24, sensitivity_threshold: float = 0.12):
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.sensitivity_threshold = sensitivity_threshold
        self.prev_frame_grid: Optional[List[int]] = None

    def downsample_buffer(self, raw_bytes: bytes, width: int, height: int) -> List[int]:
        """Downsamples raw grayscale/RGB buffer into grid_w x grid_h average luminance cells."""
        grid = [0] * (self.grid_w * self.grid_h)
        counts = [0] * (self.grid_w * self.grid_h)

        step_x = max(1, width // self.grid_w)
        step_y = max(1, height // self.grid_h)
        bytes_per_pixel = len(raw_bytes) // (width * height) if (width * height) > 0 else 1

        for gy in range(self.grid_h):
            for gx in range(self.grid_w):
                src_x = gx * step_x
                src_y = gy * step_y
                offset = (src_y * width + src_x) * bytes_per_pixel
                if offset < len(raw_bytes):
                    val = raw_bytes[offset]
                    idx = gy * self.grid_w + gx
                    grid[idx] = val

        return grid

    def process_frame(self, grid: List[int]) -> Dict[str, Any]:
        """Evaluates current grid against previous grid. Returns motion metrics."""
        if self.prev_frame_grid is None:
            self.prev_frame_grid = grid
            return {
                "motion_detected": False,
                "delta_ratio": 0.0,
                "changed_cells": 0,
                "total_cells": len(grid),
            }

        changed_cells = 0
        total_delta = 0

        for cur, prev in zip(grid, self.prev_frame_grid):
            diff = abs(cur - prev)
            total_delta += diff
            if diff > 25:  # meaningful luminance transition
                changed_cells += 1

        total_cells = len(grid)
        delta_ratio = changed_cells / total_cells if total_cells > 0 else 0.0
        motion_detected = delta_ratio >= self.sensitivity_threshold

        self.prev_frame_grid = grid

        return {
            "motion_detected": motion_detected,
            "delta_ratio": round(delta_ratio, 4),
            "changed_cells": changed_cells,
            "total_cells": total_cells,
            "avg_diff": round(total_delta / total_cells, 2) if total_cells > 0 else 0.0,
        }
