"""Tests for the YouTube card markup written by videos/sync_video_embeds.py.

The card has to survive MyST's HTML-to-AST conversion, which keeps only
class/id/style/href, so the video ID must travel in the link's ``href``
(book/_static/youtube-lite.js reads it from there).
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import pytest

_PATH = Path(__file__).resolve().parent.parent / "videos" / "sync_video_embeds.py"
_SPEC = importlib.util.spec_from_file_location("sync_video_embeds", _PATH)
assert _SPEC and _SPEC.loader
sve = importlib.util.module_from_spec(_SPEC)
sys.modules["sync_video_embeds"] = sve
_SPEC.loader.exec_module(sve)


def test_render_card_carries_id_in_href_only():
    card = sve.render_card("JTt_aW9q0rU", "數值變數", "zh")
    assert card.startswith('<div class="video-card">')
    assert '<div class="video-title">教學影片：數值變數</div>' in card
    assert '<a href="https://www.youtube.com/watch?v=JTt_aW9q0rU">' in card
    # No attribute MyST would drop, and no {raw} directive (unsupported in JB2).
    assert "data-id" not in card
    assert "{raw}" not in card
    # An HTML block must not contain a blank line, or CommonMark ends it early.
    assert "\n\n" not in card


def test_render_card_english_and_unreleased():
    assert "Watch on YouTube" in sve.render_card("JTt_aW9q0rU", "Variables", "en")
    assert sve.render_card("", "Variables", "en") == ""
    with pytest.raises(ValueError, match="unknown language"):
        sve.render_card("JTt_aW9q0rU", "x", "fr")


def test_committed_cards_use_current_markup():
    """Every card in the chapters is in the markup render_card produces."""
    root = _PATH.parent.parent
    card_rx = re.compile(r"<!-- video: [A-Za-z0-9_]+ -->\n(.*?)<!-- /video -->", re.DOTALL)
    for lang, cfg in sve.LANGS.items():
        for md in sorted((root / cfg["tree"] / "chapters").glob("*.md")):
            for body in card_rx.findall(md.read_text(encoding="utf-8")):
                if not body.strip():
                    continue  # unreleased video: placeholder only
                video = re.search(r"watch\?v=([A-Za-z0-9_-]{11})", body)
                title = re.search(r'<div class="video-title">(.*?)</div>', body)
                assert video and title, f"{md}: unexpected card markup"
                expected = sve.render_card(
                    video.group(1), title.group(1)[len(cfg["prefix"]) :], lang
                )
                assert body.strip() == expected, f"{md}: card not in render_card() form"
