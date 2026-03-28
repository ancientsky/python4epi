"""Ch01b-01: 縮排——Python 的必修規矩

Manim scene for the tutorial video on Python indentation rules,
using the Legionella outbreak investigation as the teaching narrative.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Text,
    VGroup,
    Write,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_GREEN,
    ACCENT_ORANGE,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    CodePanel,
    ExtraExampleBanner,
    OutputPanel,
    StepIndicator,
)


class Ch01bIndentationScene(EpiBaseScene):
    """Tutorial video scene: Python indentation with the Legionella outbreak scenario."""

    total_steps: int = 14

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card("縮排", "Python 的必修規矩", duration=duration)

    def show_why_four_spaces(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "為什麼是 4 個空格？",
            font=FONT_CJK, font_size=32, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("1. Python 規定同一層必須對齊", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("2. 社群共識：4 個空格 (PEP 8)", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("3. 2 格能跑，但不建議（同事會翻白眼）", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("4. 不要混用 Tab 和空格", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_if_indent(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        code_text = kwargs.get("code", "cfr = 0.157\nif cfr > 0.15:\n    print('CFR > 15%, alert!')")
        code_panel = self.show_code(code_text, title="if_indent.py")
        self.wait(1.0)
        output_panel = self.show_output(kwargs.get("output", "CFR > 15%, alert!"))
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_for_indent(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        code_text = kwargs.get("code", 'wings = ["1A","1B","2A"]\nfor wing in wings:\n    print(f"checking {wing}")')
        code_panel = self.show_code(code_text, title="for_indent.py")
        self.wait(duration)
        self.clear_screen()

    def show_nested_indent(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)

        code_text = kwargs.get("code", "cases = [15, 10, 24, 25, 20, 27]\nfor count in cases:\n    if count > 20:\n        print(f'{count} - high risk!')")

        heading = Text(
            "巢狀縮排：越深越往右",
            font=FONT_CJK, font_size=26, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        code_panel = CodePanel(code_text, title="nested.py", width=8.0, height=3.0).next_to(heading, DOWN, buff=0.5)

        note = Text(
            "if 在 for 裡面 → 再縮排 4 格 = 共 8 格",
            font=FONT_CJK, font_size=20, color=TEXT_SECONDARY,
        ).next_to(code_panel, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(Create(code_panel), run_time=0.8)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(duration - 1.6)
        self.play(FadeOut(VGroup(heading, code_panel, note)), run_time=0.5)

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)

        heading = Text("重點整理", font=FONT_CJK, font_size=34, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        points = VGroup(
            Text("1. Python 用縮排決定程式區塊", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("2. 統一用 4 個空格（PEP 8）", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("3. if/for/def 冒號後要縮排", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("4. 不要混用 Tab 和空格", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        banner = ExtraExampleBanner("額外範例：登革熱分區噴藥決策")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        code_text = kwargs.get("code",
            'dengue_cases = 12\nif dengue_cases > 10:\n    action = "full spray"\n'
            'elif dengue_cases > 5:\n    action = "targeted spray"\nelse:\n    action = "education only"')
        code_panel = self.show_code(code_text, title="dengue_spray.py")
        self.wait(duration)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        banner = BlindSpotBanner("初學者常見地雷 3 選")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_no_indent(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "if cfr > 0.15:\nprint('alert')")
        correct_code = kwargs.get("correct_code", "if cfr > 0.15:\n    print('alert')")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_tab_space(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "if x > 0:\n\tprint(x)  # Tab!")
        correct_code = kwargs.get("correct_code", "if x > 0:\n    print(x)  # spaces")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_unexpected(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "x = 10\n    print(x)  # why?")
        correct_code = kwargs.get("correct_code", "x = 10\nprint(x)  # OK")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        heading = Text(
            "下一集：import — 借用別人的工具",
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)
        sub = Text("Python 有成千上萬的套件等你用！", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(heading, DOWN, buff=0.4)
        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
