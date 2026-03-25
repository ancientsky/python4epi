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
)

from videos.src.code_mobjects import (
    ACCENT_BLUE,
    ACCENT_GREEN,
    ACCENT_ORANGE,
    BG_CARD,
    BG_CARD_ALT,
    BG_WARM,
    BORDER_LIGHT,
    CODE_BG,
    ERROR_RED,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    CodePanel,
    ErrorVsCorrect,
    ExtraExampleBanner,
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

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def setup(self) -> None:  # noqa: D401
        """Set camera background and initialise state."""
        self.camera.background_color = ManimColor(BG_WARM)
        self._step = 0
        self._active_mobjects: list = []

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

    def show_step_indicator(self, step: int) -> StepIndicator:
        """Create and show a step indicator badge in the top-right corner."""
        self._step = step
        ind = StepIndicator(step, self.total_steps)
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
        position=LEFT * 3,
        duration: float = 2.0,
    ) -> CodePanel:
        """Create and fade-in a code panel."""
        panel = CodePanel(code)
        panel.move_to(position)
        self.play(FadeIn(panel), run_time=min(1.0, duration * 0.4))
        return panel

    def show_output(
        self,
        text: str,
        *,
        position=DOWN * 2.5,
        duration: float = 1.5,
    ) -> OutputPanel:
        """Create and fade-in an output panel."""
        panel = OutputPanel(text)
        panel.move_to(position)
        self.play(FadeIn(panel), run_time=min(0.5, duration * 0.3))
        return panel

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

    def construct_from_segments(self, segments: list[dict]) -> None:
        """Drive ``construct()`` from pipeline timing data.

        Each segment dict must have ``animation`` (method name on this
        scene) and ``total_duration`` (seconds).  Additional keys are
        forwarded as keyword arguments to the animation method.
        """
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
                if k not in {"id", "narration", "animation", "pause_after", "total_duration"}
            }
            method(duration=duration, **kwargs)
