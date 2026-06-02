#!/usr/bin/env python
"""Run the full LFM Speech Dataset Studio pipeline.

This script is a repository entry point. The complete Kaggle one-cell implementation
is kept in the notebook. For local development, call individual scripts or port the
notebook cells into these script stages.
"""

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-fast", action="store_true")
    parser.add_argument("--out-root", default="outputs")
    args = parser.parse_args()

    out_root = Path(args.out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    print("LFM Speech Dataset Studio")
    print(f"run_fast={args.run_fast}")
    print(f"out_root={out_root}")
    print()
    print("Recommended execution order:")
    print("1. scripts/01_prepare_banspeech.py")
    print("2. scripts/02_audit_lfm_audio_runner.py")
    print("3. scripts/03_run_bangla_asr.py")
    print("4. scripts/04_liquid_repair_potential.py")
    print("5. scripts/05_route_and_abstain.py")
    print("6. scripts/06_make_action_cards.py")
    print("7. scripts/07_make_artifacts.py")
    print()
    print("For Kaggle, use notebooks/LFM_Speech_Dataset_Studio_v5_1_demo.ipynb.")


if __name__ == "__main__":
    main()
