"""
EdgeStream AI CLI: Command-line streaming motion detector & edge event trigger.
"""

import argparse
import json
import sys
import time
from .detector import MotionDetector
from .dispatcher import AlertDispatcher


def cmd_simulate(args):
    detector = MotionDetector(grid_w=16, grid_h=12, sensitivity_threshold=args.threshold)
    dispatcher = AlertDispatcher(args.webhook)

    print(f"Starting EdgeStream simulation (grid: 16x12, threshold: {args.threshold})...")
    # Base frame (all zero)
    f0 = [100] * (16 * 12)
    detector.process_frame(f0)

    # Simulate minor noise (1 cell)
    f1 = list(f0)
    f1[5] = 130
    res1 = detector.process_frame(f1)
    print(f"[Frame 1 - Noise] Motion: {res1['motion_detected']} (Delta: {res1['delta_ratio']})")

    # Simulate significant movement (30 cells)
    f2 = list(f0)
    for i in range(30):
        f2[i] = 200
    res2 = detector.process_frame(f2)
    print(f"[Frame 2 - Movement] Motion: {res2['motion_detected']} (Delta: {res2['delta_ratio']})")

    if res2["motion_detected"]:
        dispatcher.dispatch({"event": "motion_alarm", "metrics": res2})
        print("  -> Trigger dispatched successfully.")


def main():
    parser = argparse.ArgumentParser(
        prog="edge-stream-ai",
        description="EdgeStream AI: Lightweight Edge Vision & Motion Trigger",
    )
    subparsers = parser.add_subparsers(dest="command")

    p_sim = subparsers.add_parser("simulate", help="Run simulated motion detection benchmark")
    p_sim.add_argument("--threshold", type=float, default=0.10)
    p_sim.add_argument("--webhook", help="Optional webhook URL for alert delivery")
    p_sim.set_defaults(func=cmd_simulate)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
