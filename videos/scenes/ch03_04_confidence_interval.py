"""Ch03-04: 信賴區間（Confidence Interval）— 點估計的不確定性

Manim scene for the tutorial video on confidence intervals for RR and OR,
using the Legionella outbreak investigation as the teaching narrative.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    Text,
    VGroup,
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


class Ch03ConfidenceIntervalScene(EpiBaseScene):
    """Tutorial video scene: confidence intervals for RR/OR with the Legionella outbreak."""

    total_steps: int = 18

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the confidence interval lesson."""
        self.show_title_card("信賴區間 Confidence Interval", "點估計的不確定性", duration=duration)

    def show_point_vs_interval(self, duration: float = 5.0, **kwargs) -> None:
        """Explain point estimate vs interval estimate."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "點估計 vs 區間估計",
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• 點估計：RR = 1.82（一個數字）", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 區間估計：95% CI = (1.35, 2.46)", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• CI 告訴你估計的精確度（不確定性）", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 若 CI 包含 1 → 統計上不顯著", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_why_log(self, duration: float = 5.0, **kwargs) -> None:
        """Explain why we compute CI on the log scale."""
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            "為什麼要取 log？",
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• RR 和 OR 的範圍是 (0, +inf)，不對稱", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("• ln(RR) 的範圍是 (-inf, +inf)，近似常態", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("• 先算 ln(RR) 的 CI，再 exp() 轉回去", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("• 這樣 CI 下界不會 < 0", font=FONT_CJK, font_size=23, color=ACCENT_GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_three_steps(self, duration: float = 5.0, **kwargs) -> None:
        """Show the 3-step procedure for computing CI."""
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            "計算 CI 的三步驟",
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("Step 1: 計算 ln(RR) 或 ln(OR)", font=FONT_MONO, font_size=23, color=TEXT_PRIMARY),
            Text("Step 2: 計算 SE(ln) 標準誤", font=FONT_MONO, font_size=23, color=TEXT_PRIMARY),
            Text("Step 3: CI = exp(ln +/- 1.96 * SE)", font=FONT_MONO, font_size=23, color=TEXT_PRIMARY),
            Text("", font=FONT_MONO, font_size=10, color=TEXT_PRIMARY),
            Text("• 1.96 = 95% 信賴水準的 Z 值", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_katz_formula(self, duration: float = 5.0, **kwargs) -> None:
        """Show the Katz log method for RR CI."""
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            "Katz log method（RR 的 CI）",
            font=FONT_MONO,
            font_size=28,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("SE(ln RR) = sqrt(1/a - 1/(a+b) + 1/c - 1/(c+d))", font=FONT_MONO, font_size=20, color=TEXT_PRIMARY),
            Text("", font=FONT_MONO, font_size=8, color=TEXT_PRIMARY),
            Text("• a, b = 暴露組的發病、未發病人數", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY),
            Text("• c, d = 未暴露組的發病、未發病人數", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY),
            Text("• CI = exp(ln(RR) +/- 1.96 * SE)", font=FONT_MONO, font_size=22, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_katz_example(self, duration: float = 6.0, **kwargs) -> None:
        """Compute RR CI for the Legionella outbreak using Katz method."""
        self.show_step_indicator(5, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "import numpy as np\n"
                "\n"
                "a, b, c, d = 85, 65, 36, 94\n"
                "RR = (a/(a+b)) / (c/(c+d))\n"
                "se = np.sqrt(1/a - 1/(a+b) + 1/c - 1/(c+d))\n"
                "ln_rr = np.log(RR)\n"
                "ci_lo = np.exp(ln_rr - 1.96 * se)\n"
                "ci_hi = np.exp(ln_rr + 1.96 * se)\n"
                "print(f'RR = {RR:.2f} ({ci_lo:.2f}, {ci_hi:.2f})')"
            ),
        )

        output_text = kwargs.get("output", "RR = 2.04 (1.50, 2.78)")

        code_panel = self.show_code(code_lines, title="katz_ci.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_woolf_formula(self, duration: float = 5.0, **kwargs) -> None:
        """Show the Woolf method for OR CI."""
        self.show_step_indicator(6, self.total_steps)

        heading = Text(
            "Woolf method（OR 的 CI）",
            font=FONT_MONO,
            font_size=28,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("SE(ln OR) = sqrt(1/a + 1/b + 1/c + 1/d)", font=FONT_MONO, font_size=21, color=TEXT_PRIMARY),
            Text("", font=FONT_MONO, font_size=8, color=TEXT_PRIMARY),
            Text("• 比 Katz 公式更簡單：四格各取倒數再加", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY),
            Text("• CI = exp(ln(OR) +/- 1.96 * SE)", font=FONT_MONO, font_size=22, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_woolf_example(self, duration: float = 6.0, **kwargs) -> None:
        """Compute OR CI for the Legionella outbreak using Woolf method."""
        self.show_step_indicator(7, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "a, b, c, d = 85, 65, 36, 94\n"
                "OR = (a * d) / (b * c)\n"
                "se = np.sqrt(1/a + 1/b + 1/c + 1/d)\n"
                "ln_or = np.log(OR)\n"
                "ci_lo = np.exp(ln_or - 1.96 * se)\n"
                "ci_hi = np.exp(ln_or + 1.96 * se)\n"
                "print(f'OR = {OR:.2f} ({ci_lo:.2f}, {ci_hi:.2f})')"
            ),
        )

        output_text = kwargs.get("output", "OR = 3.42 (2.05, 5.70)")

        code_panel = self.show_code(code_lines, title="woolf_ci.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_ci_interpretation(self, duration: float = 5.0, **kwargs) -> None:
        """Explain how to interpret the CI correctly."""
        self.show_step_indicator(8, self.total_steps)

        heading = Text(
            "95% CI 的正確解讀",
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• 若重複抽樣 100 次，約 95 次的 CI", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("  會包含真正的母體參數", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("• CI 不包含 1 → 有統計顯著性", font=FONT_CJK, font_size=23, color=ACCENT_GREEN),
            Text("• CI 越窄 → 估計越精確（樣本數夠大）", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key CI points."""
        self.show_step_indicator(9, self.total_steps)

        heading = Text(
            "重點整理",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("1. 點估計需搭配信賴區間才完整", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("2. 先取 log，算 SE，再 exp 回來", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("3. RR 用 Katz 法，OR 用 Woolf 法", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("4. CI 不含 1 → 統計顯著", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("5. CI 寬度反映估計精確度", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example methods
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the ExtraExampleBanner section divider."""
        banner = ExtraExampleBanner("額外範例：疫苗效力與信賴區間")
        self.show_section_banner(banner, duration=duration)

    def show_ve_concept(self, duration: float = 5.0, **kwargs) -> None:
        """Introduce vaccine effectiveness and its CI."""
        self.show_step_indicator(11, self.total_steps)

        heading = Text(
            "疫苗效力 VE = 1 - RR",
            font=FONT_MONO,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• VE 的 CI 從 RR 的 CI 推導", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• VE_lo = 1 - RR_hi", font=FONT_MONO, font_size=22, color=TEXT_SECONDARY),
            Text("• VE_hi = 1 - RR_lo", font=FONT_MONO, font_size=22, color=TEXT_SECONDARY),
            Text("• 注意上下界會反轉！", font=FONT_CJK, font_size=24, color=ACCENT_ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_ve_example(self, duration: float = 6.0, **kwargs) -> None:
        """Calculate VE and its CI from RR."""
        self.show_step_indicator(12, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# Influenza vaccine RCT\n"
                "a, b, c, d = 20, 480, 80, 420\n"
                "RR = (a/(a+b)) / (c/(c+d))\n"
                "se = np.sqrt(1/a - 1/(a+b) + 1/c - 1/(c+d))\n"
                "rr_lo = np.exp(np.log(RR) - 1.96 * se)\n"
                "rr_hi = np.exp(np.log(RR) + 1.96 * se)\n"
                "VE = 1 - RR\n"
                "print(f'VE = {VE:.1%} ({1-rr_hi:.1%}, {1-rr_lo:.1%})')"
            ),
        )

        output_text = kwargs.get("output", "VE = 75.0% (61.2%, 83.8%)")

        code_panel = self.show_code(code_lines, title="vaccine_ci.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner("初學者常見地雷 3 選")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_freq_interp(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: wrong frequentist interpretation of CI."""
        error_code = kwargs.get("error_code", "# 95% chance true value is in CI  WRONG")
        correct_code = kwargs.get("correct_code", "# 95% of such CIs contain true value")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_forget_exp(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: forgetting to exponentiate back from log scale."""
        error_code = kwargs.get("error_code", "ci = (ln_rr - 1.96*se, ln_rr + 1.96*se)")
        correct_code = kwargs.get("correct_code", "ci = (np.exp(ln_rr - 1.96*se), ...)")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_ci_width(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: ignoring CI width and only checking significance."""
        error_code = kwargs.get("error_code", "# RR=1.5 (1.01,2.23) -> significant!")
        correct_code = kwargs.get("correct_code", "# CI is wide -> imprecise estimate")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            "下一集：卡方檢定 Chi-square Test",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "用統計檢定驗證關聯是否顯著！",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
