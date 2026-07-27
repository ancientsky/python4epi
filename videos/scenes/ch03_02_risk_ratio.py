"""Ch03-02: 風險比 Risk Ratio — 暴露讓風險增加了多少？

Manim scene for the tutorial video on risk ratio (relative risk), using the
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
    ACCENT_ORANGE,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch03RiskRatioScene(EpiBaseScene):
    """Tutorial video scene: risk ratio with the Legionella outbreak scenario."""

    total_steps: int = 16

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "風險比 Risk Ratio",
            "title_sub": "暴露讓風險增加了多少？",
            "formula_heading": "Risk Ratio (RR) 公式",
            "formula_p1": "• RR = 暴露組侵襲率 / 未暴露組侵襲率",
            "formula_p3": "• RR = 1 → 暴露與疾病無關聯",
            "formula_p4": "• RR > 1 → 暴露增加風險",
            "formula_p5": "• RR < 1 → 暴露降低風險（保護效果）",
            "interp_null_heading": "RR = 1：虛無值（Null Value）",
            "interp_null_p1": "• 暴露組與未暴露組的侵襲率相同",
            "interp_null_p2": "• 暴露因子與疾病之間沒有關聯",
            "interp_null_p3": "• 信賴區間若包含 1，則無統計顯著性",
            "interp_above_heading": "RR > 1：風險因子",
            "interp_above_p1": "• 我們的結果：RR = 2.28",
            "interp_above_p2": "• 使用淋浴者的感染風險是未使用者的 2.28 倍",
            "interp_above_p3": "• 淋浴使用與退伍軍人症有正向關聯",
            "interp_above_p4": "• 但 RR > 1 不等於因果關係！",
            "interp_below_heading": "RR < 1：保護因子",
            "interp_below_p1": "• 暴露反而降低了發病風險",
            "interp_below_p2": "• 例如：疫苗接種 → RR = 0.3",
            "interp_below_p3": "• 代表接種者的風險僅為未接種者的 30%",
            "interp_below_p4": "• 疫苗保護力 = (1 - RR) x 100%",
            "summary_heading": "重點整理",
            "summary_p1": "1. RR = 暴露組侵襲率 / 未暴露組侵襲率",
            "summary_p2": "2. RR = 1 無關聯, >1 風險因子, <1 保護因子",
            "summary_p3": "3. 信賴區間不含 1 才具統計顯著性",
            "summary_p4": "4. RR 適用於世代研究與橫斷面研究",
            "summary_p5": "5. epi_learning.risk_ratio() 一行搞定",
            "extra_banner_title": "額外範例：COVID-19 疫苗保護力",
            "extra_heading": "COVID-19 疫苗臨床試驗",
            "extra_p1": "• 疫苗組 20,000 人，感染 8 人",
            "extra_p2": "• 安慰劑組 20,000 人，感染 162 人",
            "extra_p3": "• 暴露 = 接種疫苗, 結果 = 確診感染",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：勝算比 Odds Ratio",
            "outro_sub": "病例對照研究的首選指標！",
        },
        "en": {
            "title_main": "Risk Ratio (RR)",
            "title_sub": "How much does exposure raise the risk?",
            "formula_heading": "Risk Ratio (RR) Formula",
            "formula_p1": "• RR = exposed attack rate / unexposed attack rate",
            "formula_p3": "• RR = 1 → no association between exposure and disease",
            "formula_p4": "• RR > 1 → exposure increases risk",
            "formula_p5": "• RR < 1 → exposure lowers risk (protective)",
            "interp_null_heading": "RR = 1: The Null Value",
            "interp_null_p1": "• Exposed and unexposed groups share the same attack rate",
            "interp_null_p2": "• No association between the exposure and the disease",
            "interp_null_p3": "• If the CI includes 1, there is no statistical significance",
            "interp_above_heading": "RR > 1: A Risk Factor",
            "interp_above_p1": "• Our result: RR = 2.28",
            "interp_above_p2": "• Shower users' infection risk is 2.28x that of non-users",
            "interp_above_p3": "• Shower use is positively associated with Legionnaires' disease",
            "interp_above_p4": "• But RR > 1 does not mean causation!",
            "interp_below_heading": "RR < 1: A Protective Factor",
            "interp_below_p1": "• Exposure actually lowers the risk of disease",
            "interp_below_p2": "• For example: vaccination → RR = 0.3",
            "interp_below_p3": "• Vaccinated people carry only 30% of the unvaccinated risk",
            "interp_below_p4": "• Vaccine efficacy = (1 - RR) x 100%",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. RR = exposed attack rate / unexposed attack rate",
            "summary_p2": "2. RR = 1 no link, >1 risk factor, <1 protective",
            "summary_p3": "3. Only a CI excluding 1 is statistically significant",
            "summary_p4": "4. RR fits cohort and cross-sectional studies",
            "summary_p5": "5. epi_learning.risk_ratio() does it in one line",
            "extra_banner_title": "Extra example: COVID-19 vaccine efficacy",
            "extra_heading": "COVID-19 vaccine clinical trial",
            "extra_p1": "• Vaccine group: 20,000 people, 8 infected",
            "extra_p2": "• Placebo group: 20,000 people, 162 infected",
            "extra_p3": "• Exposure = vaccinated, Outcome = confirmed infection",
            "blindspot_banner_title": "3 Common Beginner Traps",
            "outro_heading": "Next up: Odds Ratio",
            "outro_sub": "The go-to measure for case-control studies!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the risk ratio lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_formula(self, duration: float = 5.0, **kwargs) -> None:
        """Show the RR formula with bullet-point explanation."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            self.t("formula_heading"),
            font=FONT_MONO,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("formula_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("•    = [a / (a+b)] / [c / (c+d)]", font=FONT_MONO, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("formula_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("formula_p4"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("formula_p5"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_legionella_calc(self, duration: float = 6.0, **kwargs) -> None:
        """Calculate RR from the Legionella 2x2 table."""
        self.show_step_indicator(2, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# From 2x2 table (shower_use vs confirmed)\n"
                "a, b, c, d = 91, 69, 30, 90\n"
                "\n"
                "ar_exposed = a / (a + b)\n"
                "ar_unexposed = c / (c + d)\n"
                "rr = ar_exposed / ar_unexposed\n"
                "print(f'RR = {rr:.2f}')"
            ),
        )

        output_text = kwargs.get("output", "RR = 2.28")

        self.show_code(code_lines, title="risk_ratio.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_interpretation_null(self, duration: float = 5.0, **kwargs) -> None:
        """Explain RR = 1 as the null value."""
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            self.t("interp_null_heading"),
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("interp_null_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("interp_null_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("interp_null_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_interpretation_above(self, duration: float = 5.0, **kwargs) -> None:
        """Explain RR > 1 interpretation."""
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            self.t("interp_above_heading"),
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("interp_above_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("interp_above_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("interp_above_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("interp_above_p4"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_interpretation_below(self, duration: float = 5.0, **kwargs) -> None:
        """Explain RR < 1 interpretation."""
        self.show_step_indicator(5, self.total_steps)

        heading = Text(
            self.t("interp_below_heading"),
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("interp_below_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("interp_below_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("interp_below_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("interp_below_p4"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_python_function(self, duration: float = 6.0, **kwargs) -> None:
        """Show the epi_learning.risk_ratio helper function."""
        self.show_step_indicator(6, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "from epi_learning import risk_ratio\n"
                "\n"
                "result = risk_ratio(a=91, b=69, c=30, d=90)\n"
                "print(f'RR  = {result[\"rr\"]:.2f}')\n"
                "print(f'95% CI = ({result[\"ci_lower\"]:.2f},'\n"
                "      f' {result[\"ci_upper\"]:.2f})')"
            ),
        )

        output_text = kwargs.get(
            "output",
            "RR  = 2.28\n95% CI = (1.63, 3.18)",
        )

        self.show_code(code_lines, title="epi_rr.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key points about risk ratio."""
        self.show_step_indicator(7, self.total_steps)

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
            Text(self.t("summary_p5"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
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
        banner = ExtraExampleBanner(self.t("extra_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_extra_context(self, duration: float = 5.0, **kwargs) -> None:
        """Provide context for the COVID-19 vaccine RR example."""
        self.show_step_indicator(8, self.total_steps)

        heading = Text(
            self.t("extra_heading"),
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("extra_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("extra_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("extra_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_extra_calc(self, duration: float = 6.0, **kwargs) -> None:
        """Calculate RR and vaccine efficacy for the COVID-19 example."""
        self.show_step_indicator(9, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# COVID-19 vaccine trial\n"
                "a, b = 8, 19992      # vaccinated: ill, well\n"
                "c, d = 162, 19838    # placebo: ill, well\n"
                "\n"
                "rr = (a/(a+b)) / (c/(c+d))\n"
                "ve = (1 - rr) * 100\n"
                "print(f'RR = {rr:.3f}')\n"
                "print(f'Vaccine efficacy = {ve:.1f}%')"
            ),
        )

        output_text = kwargs.get(
            "output",
            "RR = 0.049\nVaccine efficacy = 95.1%",
        )

        self.show_code(code_lines, title="vaccine_rr.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_times(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: saying 'times more likely' vs 'times as likely'."""
        error_code = kwargs.get("error_code", "# RR=2.28 means 2.28 times MORE risk")
        correct_code = kwargs.get("correct_code", "# RR=2.28 means 2.28 times AS likely")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_causation(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: RR implies association, not causation."""
        error_code = kwargs.get("error_code", "# RR=2.28 so shower CAUSES infection")
        correct_code = kwargs.get("correct_code", "# RR=2.28 shows ASSOCIATION only")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_study_design(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: RR is not appropriate for case-control studies."""
        error_code = kwargs.get("error_code", "# case-control study: use RR?  NO!")
        correct_code = kwargs.get("correct_code", "# case-control study: use OR instead")
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
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
