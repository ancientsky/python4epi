"""Check that no Chinese text survives into the English tutorial videos.

Each Manim scene renders in both languages. On-screen strings are supposed to
reach the frame one of two ways:

* ``self.t("key")`` — resolved from the scene's bilingual ``TEXT`` table, or
* ``kwargs.get("key", <zh default>)`` — supplied per segment by the script YAML.

A literal written straight into an animation method escapes both and renders in
Chinese no matter which language is building. That is how ``ch00_01`` shipped an
English video whose code panel still said ``print(f'侵襲率: ...')``.

This script simulates the English build: for every ``*_en.yaml`` it resolves the
scene class, walks each segment's animation method (following ``self._helper``
calls), and reports Chinese that would survive.

Usage::

    uv run python videos/check_video_i18n.py
"""

from __future__ import annotations

import ast
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "videos/scripts"

CJK = re.compile(r"[㐀-䶿一-鿿]")

#: Keys the pipeline consumes itself; everything else is passed to the method.
RESERVED = {"id", "narration", "animation", "pause_after", "total_duration", "audio_duration"}

#: (script stem, segment id) pairs whose Chinese is the subject matter, not a
#: translation gap. ch08_07 teaches normalising Taiwanese county names, so the
#: 台/臺 pairs have to appear verbatim in the English video too.
ALLOWED = {("ch08_07_choropleth_en", "normalize_code")}

#: Follow at most this many levels of self._helper() calls out of an animation
#: method — deep enough for the one-helper-per-scene style used here.
MAX_DEPTH = 2


def find_methods(tree: ast.Module, class_name: str) -> dict[str, ast.FunctionDef]:
    """Return the named class's methods, keyed by method name."""
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return {n.name: n for n in node.body if isinstance(n, ast.FunctionDef)}
    return {}


def scan(
    fn: ast.FunctionDef,
    provided: set[str],
    methods: dict[str, ast.FunctionDef],
    seen: set[str] | None = None,
    depth: int = 0,
) -> list[dict]:
    """Collect Chinese strings this method would render in the English build.

    Parameters
    ----------
    fn:
        The animation method to walk.
    provided:
        Keys the segment supplies, which override any ``kwargs.get`` default.
    methods:
        Every method on the scene class, so ``self._helper()`` can be followed.

    Returns
    -------
    list[dict]
        One entry per surviving string, with ``kind``, ``line`` and ``text``.
    """
    seen = seen if seen is not None else set()
    if fn.name in seen or depth > MAX_DEPTH:
        return []
    seen.add(fn.name)

    hits: list[dict] = []
    skip: set[int] = set()

    body = fn.body
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
        skip.add(id(body[0].value))

    for node in ast.walk(fn):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        # self.t("key") — the argument is a lookup key, never rendered text.
        if node.func.attr == "t":
            skip.update(id(a) for a in node.args)
        # kwargs.get("key", default) — the default only renders when the
        # segment does not supply that key.
        if (
            node.func.attr == "get"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "kwargs"
            and node.args
        ):
            key = node.args[0].value if isinstance(node.args[0], ast.Constant) else None
            for arg in node.args:
                skip.update(id(sub) for sub in ast.walk(arg))
            if len(node.args) > 1 and key not in provided:
                text = "".join(
                    c.value
                    for c in ast.walk(node.args[1])
                    if isinstance(c, ast.Constant) and isinstance(c.value, str)
                )
                if CJK.search(text):
                    hits.append({"kind": "unsupplied-default", "line": node.lineno, "text": text})

    for node in ast.walk(fn):
        if (
            isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and id(node) not in skip
            and CJK.search(node.value)
        ):
            hits.append({"kind": "hardcoded", "line": node.lineno, "text": node.value})

    for node in ast.walk(fn):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "self"
            and node.func.attr in methods
        ):
            hits += scan(methods[node.func.attr], provided, methods, seen, depth + 1)

    return hits


def main() -> None:
    scripts = sorted(SCRIPTS.glob("*_en.yaml"))
    if not scripts:
        sys.exit(f"no English scripts found under {SCRIPTS}")

    problems: list[str] = []
    for script in scripts:
        doc = yaml.safe_load(script.read_text(encoding="utf-8"))
        meta = doc["meta"]
        scene_path = ROOT / "videos" / (meta["scene_module"].replace(".", "/") + ".py")
        if not scene_path.exists():
            problems.append(f"{script.name}: scene module not found ({scene_path})")
            continue

        tree = ast.parse(scene_path.read_text(encoding="utf-8"))
        methods = find_methods(tree, meta["scene_class"])

        for segment in doc["segments"]:
            if (script.stem, segment["id"]) in ALLOWED:
                continue
            provided = set(segment) - RESERVED

            for key in sorted(provided):
                value = segment[key]
                if isinstance(value, str) and CJK.search(value):
                    problems.append(
                        f"{script.name} [{segment['id']}] {key}: Chinese left in the "
                        f"English script — {value.strip().splitlines()[0][:60]}"
                    )

            fn = methods.get(segment["animation"])
            if fn is None:
                problems.append(
                    f"{script.name} [{segment['id']}]: {meta['scene_class']} has no "
                    f"method '{segment['animation']}'"
                )
                continue

            for hit in scan(fn, provided, methods):
                rel = scene_path.relative_to(ROOT)
                problems.append(
                    f"{rel}:{hit['line']} ({hit['kind']}, used by {script.name} "
                    f"[{segment['id']}]): {hit['text'].strip().splitlines()[0][:60]}"
                )

    if problems:
        print(f"{len(problems)} string(s) would render in Chinese in the English build:\n",
              file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        print(
            "\nMove the string into the scene's TEXT table and read it with "
            "self.t(...), or let the script YAML supply it via kwargs.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"{len(scripts)} English scripts checked — no Chinese survives into the English build.")


if __name__ == "__main__":
    main()
