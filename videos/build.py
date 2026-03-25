"""CLI entry point for building tutorial videos.

Usage::

    uv run python videos/build.py --all
    uv run python videos/build.py --concept variables
    uv run python videos/build.py --script videos/scripts/ch01_01_variables.yaml
    uv run python videos/build.py --all --quality l   # low-quality preview
"""

from __future__ import annotations

import argparse
import logging
import pathlib
import sys

# Ensure the project root is importable
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from videos.src.pipeline import build_video  # noqa: E402

SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent / "scripts"
OUTPUT_DIR = pathlib.Path(__file__).resolve().parent / "output"


def main() -> None:
    """Parse arguments and build videos."""
    parser = argparse.ArgumentParser(
        description="Build Epi With Python tutorial videos (Manim + TTS + FFMPEG)",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--all",
        action="store_true",
        help="Build all videos found in scripts/",
    )
    group.add_argument(
        "--concept",
        type=str,
        help="Build one concept video (e.g., 'variables')",
    )
    group.add_argument(
        "--script",
        type=pathlib.Path,
        help="Path to a specific YAML script",
    )

    parser.add_argument(
        "--quality",
        choices=["l", "m", "h"],
        default="h",
        help="Manim render quality: l=480p, m=720p, h=1080p (default: h)",
    )
    parser.add_argument(
        "--skip-tts",
        action="store_true",
        help="Reuse cached TTS audio (skip generation)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)-8s %(message)s",
    )

    if args.all:
        scripts = sorted(SCRIPTS_DIR.glob("ch*.yaml"))
        if not scripts:
            logging.error("No scripts found in %s", SCRIPTS_DIR)
            sys.exit(1)
    elif args.concept:
        # Match any chapter with this concept name
        matches = sorted(SCRIPTS_DIR.glob(f"*_{args.concept}.yaml"))
        if not matches:
            logging.error("No script found for concept '%s'", args.concept)
            sys.exit(1)
        scripts = matches
    else:
        scripts = [args.script]

    for script_path in scripts:
        if not script_path.exists():
            logging.error("Script not found: %s", script_path)
            sys.exit(1)
        print(f"\n{'='*60}")
        print(f"  Building: {script_path.name}")
        print(f"{'='*60}")
        result = build_video(
            script_path,
            OUTPUT_DIR,
            quality=args.quality,
            skip_tts=args.skip_tts,
        )
        print(f"  → {result}\n")

    print("All videos built successfully!")


if __name__ == "__main__":
    main()
