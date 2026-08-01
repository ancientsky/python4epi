"""Report anything a tutorial video would draw outside the frame.

English on-screen text runs much wider than the Chinese it was laid out for, so
a card, panel or subtitle that fits in the Chinese video can overflow the frame
in the English one — the LISA quadrant captions spilled into the neighbouring
card, and two outro subtitles ran off both edges.

Rather than render 122 videos to find that out, this walks each scene the way
the pipeline does but stubs out ``play``/``wait`` and measures every mobject
handed to them. A whole language sweeps in a few minutes.

CI does not run this: it needs the ``video`` dependency group (manim), which the
test job deliberately does not install. Run it before dispatching a video build.

Usage::

    uv run --group video python videos/check_video_layout.py           # both
    uv run --group video python videos/check_video_layout.py --lang en
"""

from __future__ import annotations

import argparse
import importlib
import os
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "videos/scripts"

#: Keys the pipeline consumes itself; the rest are passed to the method.
RESERVED = {"id", "narration", "animation", "pause_after", "total_duration", "audio_duration"}

#: Stroke width means a shape's bounding box sits a hair outside its geometry.
TOLERANCE = 0.05


def scripts_for(lang: str) -> list[pathlib.Path]:
    """Return the narration scripts belonging to *lang*."""
    everything = sorted(SCRIPTS.glob("*.yaml"))
    if lang == "en":
        return [p for p in everything if p.stem.endswith("_en")]
    return [p for p in everything if not p.stem.endswith("_en")]


def probe(scene_cls, segments: list[dict]) -> list[tuple[str, str]]:
    """Dry-run one scene and return (segment id, problem) for each overflow.

    Parameters
    ----------
    scene_cls:
        The Manim scene class named by the script's ``meta.scene_class``.
    segments:
        The script's segments, in order.

    Returns
    -------
    list[tuple[str, str]]
        Empty when every mobject the scene draws stays inside the frame.
    """
    import manim
    from manim import config

    problems: list[tuple[str, str]] = []
    drawn: list = []

    scene = scene_cls.__new__(scene_cls)
    manim.Scene.__init__(scene)
    scene.setup()
    scene.play = lambda *args, **kw: drawn.extend(
        a.mobject for a in args if getattr(a, "mobject", None) is not None
    )
    scene.wait = lambda *args, **kw: None
    scene.add = lambda *mobs, **kw: drawn.extend(mobs)
    scene.remove = lambda *mobs, **kw: None

    half_w = config.frame_width / 2 + TOLERANCE
    half_h = config.frame_height / 2 + TOLERANCE

    for segment in segments:
        drawn.clear()
        method = getattr(scene, segment["animation"], None)
        if method is None:
            problems.append((segment["id"], f"no method '{segment['animation']}'"))
            continue
        kwargs = {k: v for k, v in segment.items() if k not in RESERVED}
        try:
            method(duration=segment.get("total_duration", 4.0), **kwargs)
        except Exception as exc:  # noqa: BLE001 - report, don't abort the sweep
            problems.append((segment["id"], f"raised {type(exc).__name__}: {exc}"))
            continue

        for mob in drawn:
            if not getattr(mob, "submobjects", None) and mob.width == 0:
                continue
            left, right = mob.get_left()[0], mob.get_right()[0]
            bottom, top = mob.get_bottom()[1], mob.get_top()[1]
            if left < -half_w or right > half_w or bottom < -half_h or top > half_h:
                problems.append(
                    (
                        segment["id"],
                        f"{type(mob).__name__} spans x[{left:.2f},{right:.2f}] "
                        f"y[{bottom:.2f},{top:.2f}] outside the "
                        f"{config.frame_width:.2f}x{config.frame_height:.2f} frame",
                    )
                )
    return problems


def sweep(lang: str) -> int:
    """Check every script for *lang*; return the number of failing scripts."""
    os.environ["EPI_VIDEO_LANG"] = lang
    failures: dict[str, list[tuple[str, str]]] = {}
    scripts = scripts_for(lang)

    for path in scripts:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        meta = doc["meta"]
        try:
            module = importlib.import_module("videos." + meta["scene_module"])
            scene_cls = getattr(module, meta["scene_class"])
        except Exception as exc:  # noqa: BLE001
            failures[path.stem] = [("<import>", f"{type(exc).__name__}: {exc}")]
            continue
        found = probe(scene_cls, doc["segments"])
        if found:
            failures[path.stem] = found

    if failures:
        print(f"\n{lang}: {len(failures)} of {len(scripts)} scripts draw outside the frame",
              file=sys.stderr)
        for name, items in sorted(failures.items()):
            print(f"  {name}", file=sys.stderr)
            for segment, what in items:
                print(f"      [{segment}] {what}", file=sys.stderr)
    else:
        print(f"{lang}: {len(scripts)} scripts checked — everything stays inside the frame.")
    return len(failures)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--lang",
        choices=("zh", "en", "both"),
        default="both",
        help="Which language's scripts to sweep (default: both).",
    )
    args = parser.parse_args()

    languages = ("zh", "en") if args.lang == "both" else (args.lang,)
    if sum(sweep(lang) for lang in languages):
        sys.exit(1)


if __name__ == "__main__":
    main()
