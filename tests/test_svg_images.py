"""Every hand-made SVG diagram must be well-formed XML.

Browsers refuse to render an SVG that does not parse (an unescaped ``&`` in a
``<text>`` element is enough), and the book build does not notice.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

IMAGES = Path(__file__).resolve().parent.parent / "book" / "chapters" / "images"
SVGS = sorted(IMAGES.glob("*.svg"))


def test_svgs_found():
    assert len(SVGS) > 50


@pytest.mark.parametrize("svg", SVGS, ids=lambda p: p.name)
def test_svg_is_well_formed(svg: Path):
    root = ET.parse(svg).getroot()
    assert root.tag.endswith("svg")
