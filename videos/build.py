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
        "--chapter",
        type=str,
        help="Build every video in one chapter (e.g., 'ch08')",
    )
    group.add_argument(
        "--script",
        type=pathlib.Path,
        help="Path to a specific YAML script",
    )

    parser.add_argument(
        "--lang",
        choices=["zh", "en", "both"],
        default="both",
        help="Language filter: zh (Chinese), en (English '*_en.yaml'), or both "
        "(default: both). Ignored with --script.",
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

    def _is_en(path: pathlib.Path) -> bool:
        """English scripts follow the ``*_en.yaml`` naming convention."""
        return path.stem.endswith("_en")

    if args.script:
        scripts = [args.script]
    else:
        if args.all:
            scripts = sorted(SCRIPTS_DIR.glob("ch*.yaml"))
        elif args.chapter:
            # e.g. --chapter ch08  →  every ch08_*.yaml
            scripts = sorted(SCRIPTS_DIR.glob(f"{args.chapter}_*.yaml"))
        else:  # args.concept — match the concept in either language
            scripts = sorted(
                {
                    *SCRIPTS_DIR.glob(f"*_{args.concept}.yaml"),
                    *SCRIPTS_DIR.glob(f"*_{args.concept}_en.yaml"),
                }
            )
        # Apply the language filter (zh = non-_en, en = _en, both = all).
        if args.lang == "zh":
            scripts = [s for s in scripts if not _is_en(s)]
        elif args.lang == "en":
            scripts = [s for s in scripts if _is_en(s)]

        if not scripts:
            sel = args.chapter or args.concept or "any"
            logging.error("No scripts found for '%s' (lang=%s)", sel, args.lang)
            sys.exit(1)

    succeeded: list[str] = []
    failed: list[tuple[str, str]] = []
    for script_path in scripts:
        if not script_path.exists():
            logging.error("Script not found: %s", script_path)
            failed.append((script_path.name, "script not found"))
            continue
        print(f"\n{'='*60}")
        print(f"  Building: {script_path.name}")
        print(f"{'='*60}")
        try:
            result = build_video(
                script_path,
                OUTPUT_DIR,
                quality=args.quality,
                skip_tts=args.skip_tts,
            )
        except Exception as exc:  # noqa: BLE001 — isolate one failure per video
            logging.error("FAILED %s: %s", script_path.name, exc)
            failed.append((script_path.name, str(exc)))
            continue
        print(f"  → {result}\n")
        succeeded.append(script_path.name)

    # Summary — one failing video must not silently abort the whole batch.
    print(f"\n{'='*60}")
    print(f"  Build summary: {len(succeeded)} succeeded, {len(failed)} failed")
    print(f"{'='*60}")
    for name in succeeded:
        print(f"  ✓ {name}")
    for name, reason in failed:
        print(f"  ✗ {name}  ({reason})")

    if failed:
        sys.exit(1)
    print("\nAll videos built successfully!")


if __name__ == "__main__":
    main()
