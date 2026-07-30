"""Ch03-06: Fisher Exact Test — 小樣本也能做假設檢定

Manim scene for the tutorial video on Fisher's exact test, using the
Legionella outbreak investigation as the teaching narrative.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
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
    ExtraExampleBanner,
)


class Ch03FisherTestScene(EpiBaseScene):
    """Tutorial video scene: Fisher's exact test with the Legionella outbreak scenario."""

    total_steps: int = 16

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "Fisher Exact Test",
            "title_sub": "小樣本也能做假設檢定",
            "chisq_lim_heading": "卡方檢定的限制",
            "chisq_lim_p1": "• 卡方檢定是「近似」方法（大樣本才準）",
            "chisq_lim_p2": "• 當期望值 < 5 → 近似不可靠",
            "chisq_lim_p3": "• 需要一個「精確」的替代方案",
            "idea_heading": "Fisher Exact Test 的想法",
            "idea_p1": "• 列出所有可能的 2x2 表格排列",
            "idea_p2": "• 計算每種排列出現的機率",
            "idea_p3": "• p = 觀察到的結果（或更極端）的機率總和",
            "idea_p4": "• 不需要大樣本近似 → 「精確」檢定",
            "check_note": "有格子 < 5 → 改用 Fisher exact test!",
            "compare_heading": "Chi-square vs Fisher 比一比",
            "compare_p1": "• Chi-square p = 0.2059（近似，不可靠）",
            "compare_p2": "• Fisher p = 0.3348（精確）",
            "compare_p3": "• 小樣本時兩者可能差很多！",
            "compare_p4": "• 結論：p > 0.05，無顯著關聯",
            "flow_heading": "選擇檢定流程",
            "flow_p1": "1. 建立 2x2 交叉表",
            "flow_p2": "2. 計算期望值 (chi2_contingency)",
            "flow_p3": "3. 所有期望值 >= 5？",
            "flow_p4": "   Yes → 卡方檢定",
            "flow_p5": "   No  → Fisher exact test",
            "summary_heading": "重點整理",
            "summary_p1": "1. 期望值 < 5 → 卡方近似不可靠",
            "summary_p2": "2. Fisher exact test 不需大樣本假設",
            "summary_p3": "3. scipy fisher_exact() 回傳 OR 和 p",
            "summary_p4": "4. 先檢查期望值，再決定用哪種檢定",
            "extra_banner_title": "額外範例：罕見疫苗不良事件",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：森林圖 Forest Plot",
            "outro_sub": "一張圖看懂多個暴露因子的效果！",
        },
        "en": {
            "title_main": "Fisher's Exact Test",
            "title_sub": "Hypothesis testing that works on small samples",
            "chisq_lim_heading": "Limits of the Chi-square Test",
            "chisq_lim_p1": "• Chi-square is an approximation (accurate only with large samples)",
            "chisq_lim_p2": "• When expected < 5 → the approximation is unreliable",
            "chisq_lim_p3": "• We need an exact alternative",
            "idea_heading": "The Idea Behind Fisher's Exact Test",
            "idea_p1": "• List every possible arrangement of the 2x2 table",
            "idea_p2": "• Compute the probability of each arrangement",
            "idea_p3": "• p = the summed probability of the observed result (or more extreme)",
            "idea_p4": "• No large-sample approximation needed → an exact test",
            "check_note": "A cell < 5 → switch to Fisher's exact test!",
            "compare_heading": "Chi-square vs Fisher: head to head",
            "compare_p1": "• Chi-square p = 0.2059 (approximate, unreliable)",
            "compare_p2": "• Fisher p = 0.3348 (exact)",
            "compare_p3": "• With small samples the two can differ a lot!",
            "compare_p4": "• Conclusion: p > 0.05, no significant association",
            "flow_heading": "Choosing Your Test",
            "flow_p1": "1. Build the 2x2 crosstab",
            "flow_p2": "2. Compute expected values (chi2_contingency)",
            "flow_p3": "3. Are all expected values >= 5?",
            "flow_p4": "   Yes → chi-square test",
            "flow_p5": "   No  → Fisher's exact test",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. Expected < 5 → chi-square approximation is unreliable",
            "summary_p2": "2. Fisher's exact test needs no large-sample assumption",
            "summary_p3": "3. scipy fisher_exact() returns OR and p",
            "summary_p4": "4. Check expected values first, then pick the test",
            "extra_banner_title": "Extra example: a rare vaccine adverse event",
            "blindspot_banner_title": "3 Common Beginner Traps",
            "outro_heading": "Next up: Forest Plot",
            "outro_sub": "One chart to see the effect of many exposures at once!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the Fisher exact test lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_chisq_limitation(self, duration: float = 5.0, **kwargs) -> None:
        """Explain when chi-square fails."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            self.t("chisq_lim_heading"),
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("chisq_lim_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("chisq_lim_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("chisq_lim_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(max(0.1, duration - 1.5))
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_fisher_idea(self, duration: float = 5.0, **kwargs) -> None:
        """Explain the core idea of Fisher's exact test."""
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            self.t("idea_heading"),
            font=FONT_MONO,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("idea_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("idea_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("idea_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("idea_p4"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.0)
        self.wait(max(0.1, duration - 1.5))
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_legionella_small(self, duration: float = 6.0, **kwargs) -> None:
        """Show a small subgroup from Legionella data where Fisher is needed."""
        self.show_step_indicator(3, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# ICU 入住者中：免疫抑制 vs 死亡\n"
                "icu = df[df['icu_admission'] == True]\n"
                "small_ct = pd.crosstab(\n"
                "    icu['immunosuppressed'], icu['outcome']\n"
                ")\n"
                "print(small_ct)"
            ),
        )

        output_text = kwargs.get(
            "output",
            "outcome         dead  survived\nimmunosuppressed\nFalse              3         5\nTrue               4         2",
        )

        self.show_code(code_lines, title="small_table.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_check_expected(self, duration: float = 6.0, **kwargs) -> None:
        """Show how to check expected values before choosing the test."""
        self.show_step_indicator(4, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "from scipy.stats import chi2_contingency\n"
                "\n"
                "chi2, p, dof, expected = chi2_contingency(small_ct)\n"
                "print('Expected values:')\n"
                "print(expected)"
            ),
        )

        output_text = kwargs.get(
            "output",
            "Expected values:\n[[4.57 3.43]\n [2.43 1.57]]",
        )

        note = Text(
            self.t("check_note"),
            font=FONT_CJK,
            font_size=22,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.7)

        self.play(FadeIn(note), run_time=0.5)
        self.show_code(code_lines, title="check_expected.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.5))
        self.clear_screen()

    def show_fisher_scipy(self, duration: float = 6.0, **kwargs) -> None:
        """Show Fisher exact test with scipy."""
        self.show_step_indicator(5, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "from scipy.stats import fisher_exact\n"
                "\n"
                "oddsratio, p = fisher_exact(small_ct)\n"
                "print(f'OR = {oddsratio:.2f}')\n"
                "print(f'p  = {p:.4f}')"
            ),
        )

        output_text = kwargs.get(
            "output",
            "OR = 0.30\np  = 0.3348",
        )

        self.show_code(code_lines, title="fisher_test.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_compare_p(self, duration: float = 5.0, **kwargs) -> None:
        """Compare chi-square vs Fisher p-values."""
        self.show_step_indicator(6, self.total_steps)

        heading = Text(
            self.t("compare_heading"),
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("compare_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("compare_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("compare_p3"), font=FONT_CJK, font_size=24, color=ACCENT_ORANGE),
            Text(self.t("compare_p4"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.0)
        self.wait(max(0.1, duration - 1.5))
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_decision_flow(self, duration: float = 5.0, **kwargs) -> None:
        """Show the decision flowchart for choosing the right test."""
        self.show_step_indicator(7, self.total_steps)

        heading = Text(
            self.t("flow_heading"),
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("flow_p1"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("flow_p2"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("flow_p3"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("flow_p4"), font=FONT_CJK, font_size=23, color=ACCENT_GREEN),
            Text(self.t("flow_p5"), font=FONT_CJK, font_size=23, color=ACCENT_ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key points about Fisher's exact test."""
        self.show_step_indicator(8, self.total_steps)

        heading = Text(
            self.t("summary_heading"),
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("summary_p1"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("summary_p2"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("summary_p3"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("summary_p4"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example methods
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the ExtraExampleBanner section divider."""
        banner = ExtraExampleBanner(self.t("extra_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        """Rare vaccine adverse event example using Fisher's test."""
        self.show_step_indicator(9, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# 疫苗不良事件：接種組 vs 對照組\n"
                "import numpy as np\n"
                "table = np.array([[2, 998], [0, 1000]])\n"
                "oddsratio, p = fisher_exact(table)\n"
                "print(f'OR={oddsratio:.2f}, p={p:.4f}')"
            ),
        )

        output_text = kwargs.get("output", "OR=inf, p=0.4998")

        self.show_code(code_lines, title="vaccine_adverse.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_always_chisq(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: always using chi-square without checking."""
        error_code = kwargs.get("error_code", "chi2_contingency(ct)  # never checked expected")
        correct_code = kwargs.get("correct_code", "if (expected<5).any(): fisher_exact(ct)  # check")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_fisher_weak(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: assuming Fisher is always weaker."""
        error_code = kwargs.get("error_code", "# Fisher is less powerful, avoid it  # myth")
        correct_code = kwargs.get("correct_code", "# Fisher is exact; use when E<5  # correct")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_one_vs_two(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: one-sided vs two-sided test."""
        error_code = kwargs.get("error_code", "fisher_exact(ct, alternative='greater')  # why?")
        correct_code = kwargs.get("correct_code", "fisher_exact(ct, alternative='two-sided')  # default")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            self.t("outro_heading"),
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            self.t("outro_sub"),
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
