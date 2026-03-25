"""Replace YouTube placeholder IDs in chapter markdown files.

Usage::

    uv run python videos/update_youtube_ids.py \\
        --chapter book/chapters/01_fundamentals.md \\
        --ids "01_VARIABLES=dQw4w9WgXcQ,02_ARITHMETIC=abc123,..."

Or with a YAML mapping file::

    uv run python videos/update_youtube_ids.py \\
        --chapter book/chapters/01_fundamentals.md \\
        --from-yaml videos/youtube_ids.yaml
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

import yaml


def update_ids(chapter_path: pathlib.Path, id_map: dict[str, str]) -> int:
    """Replace YOUTUBE_ID_* placeholders with real IDs.

    Returns the number of replacements made.
    """
    text = chapter_path.read_text(encoding="utf-8")
    count = 0
    for placeholder, real_id in id_map.items():
        token = f"YOUTUBE_ID_{placeholder}"
        if token in text:
            text = text.replace(token, real_id)
            count += 1
            print(f"  {token} → {real_id}")
    chapter_path.write_text(text, encoding="utf-8")
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Update YouTube video IDs in chapter markdown")
    parser.add_argument("--chapter", type=pathlib.Path, required=True, help="Chapter .md file")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--ids",
        type=str,
        help='Comma-separated key=value pairs, e.g. "01_VARIABLES=dQw4,02_ARITHMETIC=abc1"',
    )
    group.add_argument(
        "--from-yaml",
        type=pathlib.Path,
        help="YAML file mapping placeholder suffixes to YouTube IDs",
    )

    args = parser.parse_args()

    if args.from_yaml:
        id_map = yaml.safe_load(args.from_yaml.read_text(encoding="utf-8"))
    else:
        id_map = dict(pair.split("=", 1) for pair in args.ids.split(","))

    if not args.chapter.exists():
        print(f"Error: {args.chapter} not found", file=sys.stderr)
        sys.exit(1)

    count = update_ids(args.chapter, id_map)
    print(f"\nUpdated {count} placeholder(s) in {args.chapter}")


if __name__ == "__main__":
    main()
