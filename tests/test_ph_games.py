"""Static checks for the Philippines-edition teaching widgets.

``book_ph/_static/ph-games.js`` holds twelve widgets (production bible §7)
with all their strings in English, Traditional Chinese and Filipino. These
tests are fast and need no browser: they check that every planned widget is
registered and documented, that the script stays dependency- and
network-free, that its Chinese strings follow the Taiwan terminology table in
``CLAUDE.md``, and (when Node.js is installed) that it parses.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "book_ph" / "_static"
JS = STATIC / "ph-games.js"
CSS = STATIC / "ph-games.css"
GUIDE = ROOT / "book_ph" / "GAMES.md"

WIDGETS = (
    "prompt-pick",
    "bug-hunt",
    "spot-pii",
    "date-fixer",
    "epicurve-builder",
    "two-by-two",
    "threshold-watch",
    "forecast-guess",
    "map-paint",
    "lamok-patrol",
    "publish-check",
    "quiz",
)

#: Mainland / non-Taiwan renderings that CLAUDE.md says to avoid.
AVOID_ZH = ("攻擊率", "病死率", "危險比", "比值比", "置信區間", "監控", "流調", "交絡", "靈敏度", "卡方检验")


def _js() -> str:
    return JS.read_text(encoding="utf-8")


@pytest.mark.parametrize("name", WIDGETS)
def test_widget_registered_and_documented(name: str) -> None:
    """Every widget in the bible's table exists in the script and in GAMES.md."""
    src = _js()
    assert f'WIDGETS["{name}"]' in src or f"WIDGETS.{name} " in src, name
    assert f"ph-game-{name}" in GUIDE.read_text(encoding="utf-8"), name


def test_no_dependencies_or_network() -> None:
    """One self-contained file: no imports, fetches or external URLs."""
    src = _js().replace("http://www.w3.org/2000/svg", "")  # the SVG namespace is not a request
    for needle in ("fetch(", "XMLHttpRequest", "require(", "http://", "https://", "eval(", "import("):
        assert needle not in src, needle
    assert not re.search(r"^\s*import\s", src, re.MULTILINE), "no ES module imports"


def test_hydration_contract() -> None:
    """The script waits for React hydration and has a fallback when epi-site.js is absent."""
    src = _js()
    assert "epiWhenHydrated" in src
    assert 'addEventListener("load"' in src


def test_zh_strings_use_taiwan_terms() -> None:
    src = _js()
    found = [term for term in AVOID_ZH if term in src]
    assert not found, f"use the Taiwan terms from CLAUDE.md instead of {found}"


def test_css_supports_dark_and_reduced_motion() -> None:
    css = CSS.read_text(encoding="utf-8")
    assert "html.dark" in css
    assert re.search(r"prefers-reduced-motion:\s*reduce", css)


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js not installed")
def test_script_parses() -> None:
    result = subprocess.run(["node", "--check", str(JS)], capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
