"""Ch03-02: 風險比 Risk Ratio — 暴露讓風險增加了多少？

Manim scene for the tutorial video on risk ratio (relative risk), using the
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


class Ch03RiskRatioScene(EpiBaseScene):
    """Tutorial video scene: risk ratio with the Legionella outbreak scenario."""

    total_steps: int = 16

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the risk ratio lesson."""
        self.show_title_card("風險比 Risk Ratio", "暴露讓風險增加了多少？", duration=duration)

    def show_formula(self, duration: float = 5.0, **kwargs) -> None:
        """Show the RR formula with bullet-point explanation."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "Risk Ratio (RR) 公式",
            font=FONT_MONO,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• RR = 暴露組侵襲率 / 未暴露組侵襲率", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("•    = [a / (a+b)] / [c / (c+d)]", font=FONT_MONO, font_size=24, color=TEXT_PRIMARY),
            Text("• RR = 1 → 暴露與疾病無關聯", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• RR > 1 → 暴露增加風險", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• RR < 1 → 暴露降低風險（保護效果）", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
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

        code_panel = self.show_code(code_lines, title="risk_ratio.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_interpretation_null(self, duration: float = 5.0, **kwargs) -> None:
        """Explain RR = 1 as the null value."""
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            "RR = 1：虛無值（Null Value）",
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• 暴露組與未暴露組的侵襲率相同", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 暴露因子與疾病之間沒有關聯", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 信賴區間若包含 1，則無統計顯著性", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_interpretation_above(self, duration: float = 5.0, **kwargs) -> None:
        """Explain RR > 1 interpretation."""
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            "RR > 1：風險因子",
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• 我們的結果：RR = 2.28", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 使用淋浴者的感染風險是未使用者的 2.28 倍", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 淋浴使用與退伍軍人症有正向關聯", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 但 RR > 1 不等於因果關係！", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_interpretation_below(self, duration: float = 5.0, **kwargs) -> None:
        """Explain RR < 1 interpretation."""
        self.show_step_indicator(5, self.total_steps)

        heading = Text(
            "RR < 1：保護因子",
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• 暴露反而降低了發病風險", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 例如：疫苗接種 → RR = 0.3", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 代表接種者的風險僅為未接種者的 30%", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 疫苗保護力 = (1 - RR) x 100%", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
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

        code_panel = self.show_code(code_lines, title="epi_rr.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key points about risk ratio."""
        self.show_step_indicator(7, self.total_steps)

        heading = Text(
            "重點整理",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("1. RR = 暴露組侵襲率 / 未暴露組侵襲率", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("2. RR = 1 無關聯, >1 風險因子, <1 保護因子", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("3. 信賴區間不含 1 才具統計顯著性", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("4. RR 適用於世代研究與橫斷面研究", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("5. epi_learning.risk_ratio() 一行搞定", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
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
        banner = ExtraExampleBanner("額外範例：COVID-19 疫苗保護力")
        self.show_section_banner(banner, duration=duration)

    def show_extra_context(self, duration: float = 5.0, **kwargs) -> None:
        """Provide context for the COVID-19 vaccine RR example."""
        self.show_step_indicator(8, self.total_steps)

        heading = Text(
            "COVID-19 疫苗臨床試驗",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• 疫苗組 20,000 人，感染 8 人", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 安慰劑組 20,000 人，感染 162 人", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 暴露 = 接種疫苗, 結果 = 確診感染", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
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

        code_panel = self.show_code(code_lines, title="vaccine_rr.py")
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
            "下一集：勝算比 Odds Ratio",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "病例對照研究的首選指標！",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
