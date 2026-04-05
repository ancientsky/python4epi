"""Ch03-05: 卡方檢定 — 用數字判斷「有沒有關聯」

Manim scene for the tutorial video on chi-square tests, using the
Legionella outbreak investigation as the teaching narrative.
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


class Ch03ChiSquareScene(EpiBaseScene):
    """Tutorial video scene: chi-square test basics with the Legionella outbreak scenario."""

    total_steps: int = 16

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the chi-square lesson."""
        self.show_title_card("卡方檢定", "用數字判斷「有沒有關聯」", duration=duration)

    def show_h0_concept(self, duration: float = 5.0, **kwargs) -> None:
        """Explain the null hypothesis concept for chi-square."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "虛無假設 H0",
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• H0：暴露與疾病之間沒有關聯", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• H1：暴露與疾病之間有關聯", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 卡方檢定：觀察值 vs 期望值的差距有多大？", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_expected_values(self, duration: float = 5.0, **kwargs) -> None:
        """Explain expected values under H0."""
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            "期望值 Expected Values",
            font=FONT_MONO,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• 如果 H0 為真，每個格子應該是多少？", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• E = (row total x col total) / grand total", font=FONT_MONO, font_size=22, color=TEXT_PRIMARY),
            Text("• 觀察值與期望值差越大 → 越可能有關聯", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_expected_table(self, duration: float = 6.0, **kwargs) -> None:
        """Show code computing expected values from a 2x2 table."""
        self.show_step_indicator(3, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "from scipy.stats import chi2_contingency\n"
                "\n"
                "table = pd.crosstab(df['shower_use'], df['outcome'])\n"
                "print(table)"
            ),
        )

        output_text = kwargs.get(
            "output",
            "outcome    dead  survived\nshower_use\nFalse         4       115\nTrue         15        146",
        )

        self.show_code(code_lines, title="expected_table.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_chi2_formula(self, duration: float = 5.0, **kwargs) -> None:
        """Show the chi-square formula visually."""
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            "Chi-Square Formula",
            font=FONT_MONO,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("X2 = sum( (O - E)^2 / E )", font=FONT_MONO, font_size=26, color=TEXT_PRIMARY),
            Text("• O = 觀察值（Observed）", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY),
            Text("• E = 期望值（Expected）", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY),
            Text("• 自由度 df = (rows - 1) x (cols - 1)", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_chi2_calculation(self, duration: float = 6.0, **kwargs) -> None:
        """Show scipy chi2_contingency calculation."""
        self.show_step_indicator(5, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "chi2, p, dof, expected = chi2_contingency(table)\n"
                "print(f'Chi2 = {chi2:.3f}')\n"
                "print(f'p-value = {p:.4f}')\n"
                "print(f'df = {dof}')"
            ),
        )

        output_text = kwargs.get(
            "output",
            "Chi2 = 4.217\np-value = 0.0400\ndf = 1",
        )

        self.show_code(code_lines, title="chi2_test.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_p_value(self, duration: float = 5.0, **kwargs) -> None:
        """Explain p-value interpretation."""
        self.show_step_indicator(6, self.total_steps)

        heading = Text(
            "p-value 怎麼解讀？",
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• p < 0.05 → 拒絕 H0，有統計顯著關聯", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• p >= 0.05 → 無法拒絕 H0", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• p-value 不是「效果大小」，只是「驚訝程度」", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_fisher_exact(self, duration: float = 6.0, **kwargs) -> None:
        """Mention Fisher's exact test as an alternative."""
        self.show_step_indicator(7, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "from scipy.stats import fisher_exact\n"
                "\n"
                "# 當期望值 < 5 時，改用 Fisher exact test\n"
                "oddsratio, p = fisher_exact(table)\n"
                "print(f'OR = {oddsratio:.2f}, p = {p:.4f}')"
            ),
        )

        output_text = kwargs.get("output", "OR = 2.96, p = 0.0312")

        self.show_code(code_lines, title="fisher_exact.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key points about chi-square tests."""
        self.show_step_indicator(8, self.total_steps)

        heading = Text(
            "重點整理",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("1. 卡方檢定比較觀察值 vs 期望值", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("2. scipy chi2_contingency() 一行搞定", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("3. p < 0.05 → 統計顯著關聯", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("4. 期望值 < 5 → 改用 Fisher exact test", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
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
        banner = ExtraExampleBanner("額外範例：腸病毒群聚與洗手設施")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        """Enterovirus handwashing facility example using chi-square."""
        self.show_step_indicator(9, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# 腸病毒：有洗手台 vs 無洗手台的幼兒園\n"
                "table = pd.crosstab(ev['has_sink'], ev['outbreak'])\n"
                "chi2, p, dof, exp = chi2_contingency(table)\n"
                "print(f'Chi2={chi2:.2f}, p={p:.4f}')"
            ),
        )

        self.show_code(code_lines, title="enterovirus_chi2.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner("初學者常見地雷 3 選")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_expected_five(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: ignoring expected < 5 rule."""
        error_code = kwargs.get("error_code", "chi2_contingency(small_table)  # E<5 invalid")
        correct_code = kwargs.get("correct_code", "fisher_exact(small_table)      # use Fisher if E<5")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_p_vs_effect(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: confusing p-value with effect size."""
        error_code = kwargs.get("error_code", "if p < 0.05: print('big effect')  # wrong!")
        correct_code = kwargs.get("correct_code", "print(f'OR={or_val:.2f}, p={p:.4f}')  # both")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_multiple_testing(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: multiple testing without correction."""
        error_code = kwargs.get("error_code", "for col in cols: chi2_test(col)  # no correction")
        correct_code = kwargs.get("correct_code", "multipletests(pvals, method='fdr_bh')  # adjust")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            "下一集：Fisher exact test 深入解析",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "小樣本也能做假設檢定！",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
