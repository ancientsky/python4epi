"""Manim scene for Ch01-05: 條件判斷 (Conditionals)."""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    UR,
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
    BG_WARM,
    CODE_BG,
    CODE_TEXT,
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


class Ch01ConditionalsScene(EpiBaseScene):
    """Tutorial video scene: Python conditionals for epi logic."""

    total_steps: int = 3

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Part 1 – Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(
            "條件判斷",
            "讓程式依情況做不同的事",
            duration=duration,
        )

    def show_if_elif_else(self, duration: float = 6.0, **kwargs) -> None:
        code = kwargs.get(
            "code",
            (
                "# 根據侵襲率判斷疫情等級\n"
                "attack_rate = 43.2  # 松柏護理之家，單位：%\n"
                "\n"
                "if attack_rate >= 50:\n"
                "    level = \"嚴重\"\n"
                "elif attack_rate >= 30:\n"
                "    level = \"中等\"\n"
                "else:\n"
                "    level = \"輕微\"\n"
                "\n"
                "print(f\"疫情等級：{level}\")"
            ),
        )
        step = self.show_step_indicator(1)
        panel = self.show_code(code, duration=duration * 0.6)
        output = self.show_output("疫情等級：中等", duration=duration * 0.25)
        self.wait(max(0.1, duration * 0.1))
        self.play(FadeOut(panel), FadeOut(output), FadeOut(step), run_time=0.5)

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        step = self.show_step_indicator(2)
        points = VGroup(
            Text("if / elif / else 依序檢查條件", font=FONT_CJK, font_size=28, color=TEXT_PRIMARY),
            Text("條件為 True 則執行該區塊，其餘跳過", font=FONT_CJK, font_size=28, color=TEXT_PRIMARY),
            Text("比較運算子：==  !=  >  <  >=  <=", font=FONT_MONO, font_size=26, color=ACCENT_ORANGE),
            Text("縮排（4 格空白）決定程式區塊範圍", font=FONT_CJK, font_size=28, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        points.move_to([0, 0, 0])
        self.play(FadeIn(points), run_time=0.6)
        self.wait(max(0.5, duration - 0.6))
        self.play(FadeOut(points), FadeOut(step), run_time=0.5)

    # ------------------------------------------------------------------
    # Part 2 – Extra epi example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner())
        self.wait(max(0.1, duration - 0.5))

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        code = kwargs.get(
            "code",
            (
                "# 疫苗覆蓋率門檻判斷（以麻疹為例）\n"
                "coverage_pct = 85.0  # 某地區覆蓋率 %\n"
                "\n"
                "if coverage_pct >= 95:\n"
                "    status = \"達到群體免疫門檻 ✅\"\n"
                "elif coverage_pct >= 80:\n"
                "    status = \"尚可，但仍有缺口 ⚠️\"\n"
                "else:\n"
                "    status = \"風險偏高，需加強接種 ❌\"\n"
                "\n"
                "print(f\"覆蓋率 {coverage_pct}%：{status}\")"
            ),
        )
        panel = self.show_code(code, duration=duration * 0.6)
        output = self.show_output("覆蓋率 85.0%：尚可，但仍有缺口 ⚠️", duration=duration * 0.25)
        self.wait(max(0.1, duration * 0.1))
        self.play(FadeOut(panel), FadeOut(output), run_time=0.5)

    # ------------------------------------------------------------------
    # Part 3 – Beginner blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner())
        self.wait(max(0.1, duration - 0.5))

    def show_blindspot_single_equal(self, duration: float = 4.0, **kwargs) -> None:
        error_code = kwargs.get(
            "error_code",
            "if attack_rate = 43.2:   # ❌ SyntaxError\n    print(\"相等\")",
        )
        correct_code = kwargs.get(
            "correct_code",
            "if attack_rate == 43.2:  # ✅ == 才是比較\n    print(\"相等\")",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_missing_colon(self, duration: float = 4.0, **kwargs) -> None:
        error_code = kwargs.get(
            "error_code",
            "if attack_rate >= 50   # ❌ SyntaxError: expected ':'\n    level = \"嚴重\"",
        )
        correct_code = kwargs.get(
            "correct_code",
            "if attack_rate >= 50:  # ✅ 冒號不能少\n    level = \"嚴重\"",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_indentation(self, duration: float = 4.0, **kwargs) -> None:
        error_code = kwargs.get(
            "error_code",
            "if attack_rate >= 30:\n"
            "level = \"中等\"  # ❌ IndentationError\n"
            "                # 沒有縮排！",
        )
        correct_code = kwargs.get(
            "correct_code",
            "if attack_rate >= 30:\n"
            "    level = \"中等\"  # ✅ 4 格縮排\n"
            "                   # 區塊才正確",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(
            "小結",
            "條件判斷讓程式有「判斷力」，記得冒號和縮排！",
            duration=duration,
        )
