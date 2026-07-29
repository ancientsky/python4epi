"""Base Manim scene with shared styling for Epi With Python tutorial videos.

All tutorial videos inherit from :class:`EpiBaseScene` to ensure consistent
visual identity aligned with the Anthropic Skilljar Academy light theme:

* Warm white background (#FAF8F3)
* White rounded-corner cards with subtle borders
* Dark code blocks for contrast
* Anthropic brand accent colours
"""

from __future__ import annotations

import json
import os
import pathlib

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    UR,
    FadeIn,
    FadeOut,
    ManimColor,
    Scene,
    Text,
    VGroup,
    config,
)

from videos.src.code_mobjects import (
    BG_WARM,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    CodePanel,
    ErrorVsCorrect,
    OutputPanel,
    StepIndicator,
    VariableBox,
)


class EpiBaseScene(Scene):
    """Base scene providing shared layout elements and animation helpers.

    Subclasses implement individual animation methods that are called by
    the pipeline with timing data derived from TTS audio durations.
    """

    # Overridden by subclass or pipeline
    total_steps: int = 1

    # Bilingual on-screen text. Subclasses set
    # ``TEXT = {"zh": {...}, "en": {...}}`` and read strings via ``self.t(key)``
    # so one scene renders in either language (picked by EPI_VIDEO_LANG).
    TEXT: dict[str, dict[str, str]] = {}

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def setup(self) -> None:  # noqa: D401
        """Set camera background and initialise state."""
        self.camera.background_color = ManimColor(BG_WARM)
        self._step = 0
        self._active_mobjects: list = []
        # "zh" (default) or "en"; the pipeline sets EPI_VIDEO_LANG per script.
        self.lang = os.environ.get("EPI_VIDEO_LANG", "zh")

    def t(self, key: str, **fmt: object) -> str:
        """Return the on-screen string for ``key`` in the active language.

        Falls back to Chinese (then to the key itself) when a language or key
        is missing, so a partially-translated scene still renders. ``**fmt``
        are applied with ``str.format`` for interpolated labels.
        """
        table = self.TEXT.get(self.lang) or self.TEXT.get("zh", {})
        text = table.get(key) or self.TEXT.get("zh", {}).get(key, key)
        return text.format(**fmt) if fmt else text

    # ------------------------------------------------------------------
    # Timing helpers
    # ------------------------------------------------------------------

    def load_timings(self) -> dict[str, float]:
        """Load per-segment timing data from the environment.

        The pipeline writes a JSON file and passes its path via the
        ``EPI_VIDEO_TIMING`` environment variable.  Each key is a segment
        ID and the value is the total duration (audio + pause) in seconds.
        """
        timing_path = os.environ.get("EPI_VIDEO_TIMING")
        if not timing_path:
            return {}
        data = json.loads(pathlib.Path(timing_path).read_text(encoding="utf-8"))
        return {seg["id"]: seg["total_duration"] for seg in data}

    # ------------------------------------------------------------------
    # Layout helpers
    # ------------------------------------------------------------------

    def show_step_indicator(self, step: int, total: int | None = None) -> StepIndicator:
        """Create and show a step indicator badge in the top-right corner."""
        self._step = step
        ind = StepIndicator(step, total if total is not None else self.total_steps)
        ind.to_corner(UR, buff=0.4)
        self.play(FadeIn(ind), run_time=0.3)
        return ind

    def show_title_card(
        self,
        title: str,
        subtitle: str = "",
        *,
        duration: float = 3.0,
    ) -> None:
        """Animate a centred title card and wait."""
        t = Text(title, font=FONT_CJK, font_size=48, color=ManimColor(TEXT_PRIMARY))
        group = VGroup(t)
        if subtitle:
            st = Text(
                subtitle,
                font=FONT_CJK,
                font_size=28,
                color=ManimColor(TEXT_SECONDARY),
            )
            group.add(st)
            group.arrange(DOWN, buff=0.4)

        self.play(FadeIn(group), run_time=min(1.0, duration * 0.3))
        self.wait(max(0.1, duration - 1.0))
        self.play(FadeOut(group), run_time=min(0.5, duration * 0.15))

    def show_section_banner(
        self,
        banner: VGroup,
        *,
        duration: float = 2.0,
    ) -> None:
        """Show and dismiss a section banner (BlindSpot / ExtraExample)."""
        self.play(FadeIn(banner), run_time=0.5)
        self.wait(max(0.1, duration - 1.0))
        self.play(FadeOut(banner), run_time=0.5)

    # ------------------------------------------------------------------
    # Code helpers
    # ------------------------------------------------------------------

    def show_code(
        self,
        code: str,
        *,
        title: str = "",
        position=LEFT * 3,
        duration: float = 2.0,
        max_width: float = 11.0,
    ) -> CodePanel:
        """Create and fade-in a code panel.

        ``max_width`` caps the panel's on-screen width; pass a smaller value
        (e.g. ``6.0``) when the panel sits beside a diagram so the code stays
        within its half and never overflows the frame or collides with it.
        """
        panel = (
            CodePanel(code, title=title, width=max_width)
            if title
            else CodePanel(code, width=max_width)
        )
        panel.move_to(position)
        self.keep_in_frame(panel)
        # Remembered so show_output can drop clear of it — the two are sized
        # from their content and can grow into each other.
        self._code_panel = panel
        self.play(FadeIn(panel), run_time=min(1.0, duration * 0.4))
        return panel

    def keep_in_frame(self, mob, *, margin: float = 0.3):
        """Nudge *mob* back inside the frame if it hangs off any edge.

        Panels are positioned by their centre, so one grows off-screen as its
        content does — a tall output panel drops past the bottom, and a code
        panel holding a long line (Chinese runs wider than the English of the
        same snippet) slides past the left edge. Returns *mob* for chaining.
        """
        floor = -config.frame_height / 2 + margin
        ceiling = config.frame_height / 2 - margin
        if mob.get_bottom()[1] < floor:
            mob.shift(UP * (floor - mob.get_bottom()[1]))
        elif mob.get_top()[1] > ceiling:
            mob.shift(DOWN * (mob.get_top()[1] - ceiling))

        left = -config.frame_width / 2 + margin
        right = config.frame_width / 2 - margin
        if mob.get_left()[0] < left:
            mob.shift(RIGHT * (left - mob.get_left()[0]))
        elif mob.get_right()[0] > right:
            mob.shift(LEFT * (mob.get_right()[0] - right))
        return mob

    def show_output(
        self,
        text: str,
        *,
        position=DOWN * 2.5,
        duration: float = 1.5,
        max_height: float | None = None,
    ) -> OutputPanel:
        """Create and fade-in an output panel, kept inside the frame."""
        panel = OutputPanel(text, max_height=max_height)
        panel.move_to(position)
        self.keep_in_frame(panel)
        self.avoid_code_panel(panel)
        self.play(FadeIn(panel), run_time=min(0.5, duration * 0.3))
        return panel

    def avoid_code_panel(self, mob, *, gap: float = 0.25):
        """Slide *mob* below the code panel already on screen, if they collide.

        Both panels size themselves from their content, so a long snippet and a
        long output can end up occupying the same band even though each one sits
        where it always has. Only moves down, and never past the frame edge.
        """
        code = getattr(self, "_code_panel", None)
        if code is None or code not in self.mobjects:
            return mob
        overlap_y = min(code.get_top()[1], mob.get_top()[1]) - max(
            code.get_bottom()[1], mob.get_bottom()[1]
        )
        overlap_x = min(code.get_right()[0], mob.get_right()[0]) - max(
            code.get_left()[0], mob.get_left()[0]
        )
        if overlap_y <= 0 or overlap_x <= 0:
            return mob
        room = mob.get_bottom()[1] - (-config.frame_height / 2 + 0.3)
        mob.shift(DOWN * min(overlap_y + gap, max(0.0, room)))
        return mob

    def show_output_with_note(
        self,
        text: str,
        note: str,
        *,
        color: str = TEXT_SECONDARY,
        position=DOWN * 2.2,
        font_size: int = 20,
        duration: float = 1.5,
        max_height: float | None = None,
    ) -> tuple[OutputPanel, Text]:
        """Output panel with a caption beneath it.

        The caption is anchored to the panel rather than to the bottom of the
        frame: a fixed `to_edge(DOWN)` caption ends up underneath the panel as
        soon as the output runs to more than a couple of lines. The pair is then
        shifted as a unit to stay on screen.
        """
        panel = self.show_output(
            text, position=position, duration=duration, max_height=max_height
        )
        caption = Text(note, font=FONT_CJK, font_size=font_size, color=ManimColor(color))
        caption.next_to(panel, DOWN, buff=0.28)
        self.keep_in_frame(VGroup(panel, caption))
        self.play(FadeIn(caption), run_time=0.5)
        return panel, caption

    def show_variable_box(
        self,
        name: str,
        value: str,
        *,
        position=RIGHT * 3,
        duration: float = 1.5,
    ) -> VariableBox:
        """Create and fade-in a variable box."""
        box = VariableBox(name, value)
        box.move_to(position)
        self.play(FadeIn(box), run_time=min(0.8, duration * 0.4))
        return box

    def show_error_vs_correct(
        self,
        error_code: str,
        correct_code: str,
        *,
        duration: float = 4.0,
    ) -> ErrorVsCorrect:
        """Show a side-by-side NG / OK comparison panel."""
        panel = ErrorVsCorrect(error_code, correct_code)
        self.play(FadeIn(panel), run_time=min(1.0, duration * 0.25))
        self.wait(max(0.1, duration - 1.5))
        return panel

    # ------------------------------------------------------------------
    # Transition helpers
    # ------------------------------------------------------------------

    def clear_screen(self, *, run_time: float = 0.5) -> None:
        """Fade out all current mobjects."""
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)

    # ------------------------------------------------------------------
    # Pipeline-driven construct
    # ------------------------------------------------------------------

    def construct_from_segments(self, segments: list[dict] | None = None) -> None:
        """Drive ``construct()`` from pipeline timing data.

        Parameters
        ----------
        segments : list[dict] | None
            Segment dicts with ``animation`` and ``total_duration`` keys.
            If *None*, loads the full segment data from the JSON file
            pointed to by the ``EPI_VIDEO_TIMING`` environment variable.
        """
        if segments is None:
            segments = self._load_segments()
        timings = self.load_timings()
        for seg in segments:
            method_name = seg["animation"]
            method = getattr(self, method_name, None)
            if method is None:
                raise AttributeError(
                    f"{type(self).__name__} has no animation method '{method_name}'"
                )
            duration = timings.get(seg["id"], seg.get("total_duration", 3.0))
            kwargs = {
                k: v
                for k, v in seg.items()
                if k not in {
                    "id", "narration", "animation", "pause_after",
                    "total_duration", "audio_duration",
                }
            }
            method(duration=duration, **kwargs)

    def _load_segments(self) -> list[dict]:
        """Load full segment data from the ``EPI_VIDEO_TIMING`` JSON file."""
        timing_path = os.environ.get("EPI_VIDEO_TIMING")
        if not timing_path:
            raise RuntimeError(
                "EPI_VIDEO_TIMING env var not set — cannot load segments. "
                "Pass segments explicitly or run via the pipeline."
            )
        return json.loads(pathlib.Path(timing_path).read_text(encoding="utf-8"))
