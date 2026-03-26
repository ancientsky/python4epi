"""Custom Manim mobjects for Epi With Python tutorial videos.

Visual components follow the Anthropic Skilljar Academy light-theme style:
warm white background, white rounded-corner cards, dark code panels, and
Anthropic brand accent colours.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Code,
    Create,
    FadeIn,
    ManimColor,
    Paragraph,
    Rectangle,
    RoundedRectangle,
    Text,
    VGroup,
    Write,
)

# ---------------------------------------------------------------------------
# Colour palette (Anthropic Skilljar light theme)
# ---------------------------------------------------------------------------
BG_WARM = "#FAF8F3"
BG_CARD = "#FFFFFF"
BG_CARD_ALT = "#F5F3EE"
ACCENT_ORANGE = "#D97757"
ACCENT_BLUE = "#6A9BCC"
ACCENT_GREEN = "#788C5D"
TEXT_PRIMARY = "#1A1A1A"
TEXT_SECONDARY = "#6B6B6B"
ERROR_RED = "#D94452"
CODE_BG = "#2B2B2B"
CODE_TEXT = "#F8F8F2"
BORDER_LIGHT = "#E8E5DF"

# Font defaults
FONT_CJK = "Noto Sans CJK TC"
FONT_MONO = "Monospace"


# ---------------------------------------------------------------------------
# Helper: rounded card
# ---------------------------------------------------------------------------

def _card(width: float, height: float, *, fill: str = BG_CARD) -> RoundedRectangle:
    """Return a white rounded-corner card with a subtle border."""
    return RoundedRectangle(
        corner_radius=0.2,
        width=width,
        height=height,
        fill_color=ManimColor(fill),
        fill_opacity=1,
        stroke_color=ManimColor(BORDER_LIGHT),
        stroke_width=2,
    )


# ---------------------------------------------------------------------------
# VariableBox — the "labelled box" metaphor
# ---------------------------------------------------------------------------

class VariableBox(VGroup):
    """A labelled box showing ``name = value``.

    Visualises the "variable is a box with a label" metaphor central to
    the Ch01 teaching narrative.
    """

    def __init__(
        self,
        name: str = "",
        value: str = "",
        *,
        label: str = "",
        label_color: str = TEXT_SECONDARY,
        width: float = 3.0,
        height: float = 1.0,
    ) -> None:
        super().__init__()
        display_name = label or name
        card = _card(width, height)
        label_mob = Text(
            display_name,
            font=FONT_MONO,
            font_size=22,
            color=ManimColor(label_color),
        ).move_to(card.get_top() + DOWN * 0.25)
        val = Text(
            str(value),
            font=FONT_MONO,
            font_size=32,
            color=ManimColor(ACCENT_ORANGE),
            weight="BOLD",
        ).move_to(card.get_center() + DOWN * 0.1)
        self.add(card, label_mob, val)
        self.card = card
        self.label = label_mob
        self.value_mob = val


# ---------------------------------------------------------------------------
# CodePanel — dark syntax-highlighted code block
# ---------------------------------------------------------------------------

class CodePanel(VGroup):
    """Syntax-highlighted code block with dark background.

    Wraps Manim's ``Code`` mobject inside a rounded card styled to match
    the dark code-block aesthetic from the Anthropic Skilljar theme.
    """

    def __init__(
        self,
        code_string: str,
        *,
        title: str = "",
        language: str = "python",
        width: float = 6.0,
        height: float | None = None,
        font_size: int = 20,
    ) -> None:
        super().__init__()
        code_mob = Code(
            code_string,
            language=language,
            font_size=font_size,
            background="rectangle",
            background_stroke_color=ManimColor(BORDER_LIGHT),
            background_stroke_width=1,
            style="monokai",
        )
        # Override background colour
        if code_mob.background_mobject is not None:
            code_mob.background_mobject.set_fill(ManimColor(CODE_BG), opacity=1)
            code_mob.background_mobject.round_corners(0.15)

        if title:
            title_mob = Text(
                title,
                font=FONT_MONO,
                font_size=14,
                color=ManimColor(TEXT_SECONDARY),
            )
            title_mob.next_to(code_mob, UP, buff=0.15).align_to(code_mob, LEFT)
            self.add(title_mob, code_mob)
            self.title_mob = title_mob
        else:
            self.add(code_mob)
            self.title_mob = None
        self.code_mob = code_mob


# ---------------------------------------------------------------------------
# OutputPanel — terminal-style output display
# ---------------------------------------------------------------------------

class OutputPanel(VGroup):
    """Terminal-style output panel (dark or light variant)."""

    def __init__(
        self,
        text: str,
        *,
        width: float = 10.0,
        height: float = 1.2,
        dark: bool = True,
    ) -> None:
        super().__init__()
        bg = CODE_BG if dark else BG_CARD_ALT
        fg = CODE_TEXT if dark else TEXT_PRIMARY
        card = _card(width, height, fill=bg)
        prefix = Text(
            ">>> ",
            font=FONT_MONO,
            font_size=20,
            color=ManimColor(ACCENT_GREEN),
        )
        body = Text(
            text,
            font=FONT_MONO,
            font_size=20,
            color=ManimColor(fg),
        )
        line = VGroup(prefix, body).arrange(RIGHT, buff=0.05)
        line.move_to(card.get_center())
        self.add(card, line)
        self.card = card


# ---------------------------------------------------------------------------
# ArrowAssignment — animated value → box arrow
# ---------------------------------------------------------------------------

class ArrowAssignment(VGroup):
    """Curved arrow showing a value flowing into a VariableBox.

    Create with ``ArrowAssignment(start_mob, end_mob)`` and then play
    ``Create(arrow)`` to animate.
    """

    def __init__(self, start, end, *, color: str = ACCENT_ORANGE) -> None:
        from manim import CurvedArrow

        super().__init__()
        arrow = CurvedArrow(
            start.get_right(),
            end.get_left(),
            color=ManimColor(color),
            stroke_width=3,
        )
        self.add(arrow)
        self.arrow = arrow


# ---------------------------------------------------------------------------
# ErrorVsCorrect — side-by-side comparison panel
# ---------------------------------------------------------------------------

class ErrorVsCorrect(VGroup):
    """Side-by-side comparison: red error panel vs green correct panel.

    Used in the *Beginner Blind Spots* section of every video.
    """

    def __init__(
        self,
        error_code: str,
        correct_code: str,
        *,
        width: float = 5.5,
        height: float = 2.5,
    ) -> None:
        super().__init__()

        # Error side
        err_card = RoundedRectangle(
            corner_radius=0.15, width=width, height=height,
            fill_color=ManimColor("#FDF0F0"), fill_opacity=1,
            stroke_color=ManimColor(ERROR_RED), stroke_width=2,
        )
        err_label = Text(
            "NG",
            font_size=24,
            color=ManimColor(ERROR_RED),
            weight="BOLD",
        ).move_to(err_card.get_top() + DOWN * 0.3)
        err_code = Code(
            error_code, language="python", font_size=16,
            background="rectangle", style="monokai",
        )
        if err_code.background_mobject is not None:
            err_code.background_mobject.set_fill(ManimColor(CODE_BG), opacity=1)
            err_code.background_mobject.round_corners(0.1)
        err_code.move_to(err_card.get_center() + DOWN * 0.15)
        err_group = VGroup(err_card, err_label, err_code)

        # Correct side
        ok_card = RoundedRectangle(
            corner_radius=0.15, width=width, height=height,
            fill_color=ManimColor("#F0F5EC"), fill_opacity=1,
            stroke_color=ManimColor(ACCENT_GREEN), stroke_width=2,
        )
        ok_label = Text(
            "OK",
            font_size=24,
            color=ManimColor(ACCENT_GREEN),
            weight="BOLD",
        ).move_to(ok_card.get_top() + DOWN * 0.3)
        ok_code = Code(
            correct_code, language="python", font_size=16,
            background="rectangle", style="monokai",
        )
        if ok_code.background_mobject is not None:
            ok_code.background_mobject.set_fill(ManimColor(CODE_BG), opacity=1)
            ok_code.background_mobject.round_corners(0.1)
        ok_code.move_to(ok_card.get_center() + DOWN * 0.15)
        ok_group = VGroup(ok_card, ok_label, ok_code)

        self.add(err_group, ok_group)
        self.arrange(RIGHT, buff=0.5)


# ---------------------------------------------------------------------------
# Section banners
# ---------------------------------------------------------------------------

class BlindSpotBanner(VGroup):
    """Section title banner for *Beginner Blind Spots*."""

    def __init__(self, title: str = "初學者常見盲點") -> None:
        super().__init__()
        card = _card(10, 0.8, fill=BG_CARD_ALT)
        icon = Text("!", font_size=32, color=ManimColor(ERROR_RED), weight="BOLD")
        label = Text(title, font=FONT_CJK, font_size=28, color=ManimColor(TEXT_PRIMARY))
        content = VGroup(icon, label).arrange(RIGHT, buff=0.3)
        content.move_to(card.get_center())
        self.add(card, content)


class ExtraExampleBanner(VGroup):
    """Section title banner for *Extra Epi Example*."""

    def __init__(self, title: str = "換個場景試試看") -> None:
        super().__init__()
        card = _card(10, 0.8, fill=BG_CARD_ALT)
        icon = Text("+", font_size=32, color=ManimColor(ACCENT_BLUE), weight="BOLD")
        label = Text(title, font=FONT_CJK, font_size=28, color=ManimColor(TEXT_PRIMARY))
        content = VGroup(icon, label).arrange(RIGHT, buff=0.3)
        content.move_to(card.get_center())
        self.add(card, content)


class StepIndicator(VGroup):
    """Step indicator badge (e.g. ``1 / 6``) for top-right corner."""

    def __init__(self, current: int, total: int) -> None:
        super().__init__()
        card = _card(1.4, 0.5, fill=BG_CARD_ALT)
        label = Text(
            f"{current} / {total}",
            font=FONT_MONO,
            font_size=18,
            color=ManimColor(TEXT_SECONDARY),
        )
        label.move_to(card.get_center())
        self.add(card, label)
