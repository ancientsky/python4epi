"""Ch03-03: 勝算比（Odds Ratio）— 暴露與疾病的關聯強度

Manim scene for the tutorial video on odds ratios, using the
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


class Ch03OddsRatioScene(EpiBaseScene):
    """Tutorial video scene: odds ratio basics with the Legionella outbreak scenario."""

    total_steps: int = 16

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the odds ratio lesson."""
        self.show_title_card("勝算比（Odds Ratio）", "暴露與疾病的關聯強度", duration=duration)

    def show_odds_vs_risk(self, duration: float = 6.0, **kwargs) -> None:
        """Explain the difference between odds and risk (probability)."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "Odds vs Risk（勝算 vs 風險）",
            font=FONT_MONO,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• Risk（風險）= 事件數 / 總人數", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• Odds（勝算）= 事件數 / 非事件數", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• Risk = p, Odds = p / (1 - p)", font=FONT_MONO, font_size=22, color=TEXT_SECONDARY),
            Text("• 當疾病罕見時，Odds 近似 Risk", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_or_formula(self, duration: float = 6.0, **kwargs) -> None:
        """Show the OR formula using a 2x2 table."""
        self.show_step_indicator(2, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "#        Disease+  Disease-\n"
                "# Exp+      a         b\n"
                "# Exp-      c         d\n"
                "#\n"
                "# OR = (a * d) / (b * c)\n"
                "# OR = odds_exposed / odds_unexposed"
            ),
        )

        code_panel = self.show_code(code_lines, title="or_formula.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_legionella_calc(self, duration: float = 7.0, **kwargs) -> None:
        """Calculate OR for shower use in the Legionella outbreak."""
        self.show_step_indicator(3, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "\n"
                "df = pd.read_csv('legionella_outbreak.csv')\n"
                "ct = pd.crosstab(df['shower_use'], df['outcome'])\n"
                "a, b = ct.loc[True, 'dead'], ct.loc[True, 'survived']\n"
                "c, d = ct.loc[False, 'dead'], ct.loc[False, 'survived']\n"
                "OR = (a * d) / (b * c)\n"
                "print(f'OR = {OR:.2f}')"
            ),
        )

        output_text = kwargs.get("output", "OR = 2.45")

        code_panel = self.show_code(code_lines, title="legionella_or.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_or_interpretation(self, duration: float = 6.0, **kwargs) -> None:
        """Explain how to interpret OR values."""
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            "如何解讀 OR？",
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• OR = 1 → 暴露與疾病無關聯", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• OR > 1 → 暴露可能增加疾病風險", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• OR < 1 → 暴露可能降低疾病風險", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• OR = 2.45 → 使用淋浴者的勝算是未使用者的 2.45 倍", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_rare_disease(self, duration: float = 5.0, **kwargs) -> None:
        """Explain the rare disease assumption: OR approximates RR."""
        self.show_step_indicator(5, self.total_steps)

        heading = Text(
            "罕見疾病假設（Rare Disease Assumption）",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• 當盛行率 < 10%，OR 近似 RR", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 退伍軍人症 CFR 15.7% → OR 不等於 RR", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 病例對照研究中只能算 OR，不能算 RR", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_when_to_use(self, duration: float = 5.0, **kwargs) -> None:
        """When to use OR vs RR."""
        self.show_step_indicator(6, self.total_steps)

        heading = Text(
            "OR vs RR：何時用哪個？",
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• 世代研究（cohort）→ 用 RR（風險比）", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 病例對照研究（case-control）→ 用 OR", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 邏輯斯迴歸（logistic regression）→ 輸出 OR", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 橫斷面研究 → 可用 PR（盛行率比）或 OR", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key points about OR."""
        self.show_step_indicator(7, self.total_steps)

        heading = Text(
            "重點整理",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("1. Odds = p / (1-p)，不是機率本身", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("2. OR = (a*d) / (b*c)，來自 2x2 表", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("3. OR > 1 暴露增加風險，OR < 1 降低風險", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("4. 罕見疾病時 OR 近似 RR", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("5. 病例對照研究只能算 OR", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
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
        """Explain the extra example context."""
        self.show_step_indicator(8, self.total_steps)

        heading = Text(
            "COVID-19 病例對照研究",
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• 研究設計：病例對照（case-control）", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 病例組：確診 COVID-19 住院者", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 對照組：同期未確診住院者", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 暴露：是否接種疫苗", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_extra_calc(self, duration: float = 6.0, **kwargs) -> None:
        """Calculate OR for COVID-19 vaccine example."""
        self.show_step_indicator(9, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# COVID-19 case-control vaccine study\n"
                "a, b = 50, 200   # cases: vacc+, vacc-\n"
                "c, d = 150, 100  # controls: vacc+, vacc-\n"
                "OR = (a * d) / (b * c)\n"
                "VE = 1 - OR\n"
                "print(f'OR = {OR:.2f}')\n"
                "print(f'VE = {VE:.1%}')"
            ),
        )

        output_text = kwargs.get("output", "OR = 0.17\nVE = 83.3%")

        code_panel = self.show_code(code_lines, title="covid_or.py")
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

    def show_blindspot_odds_prob(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: confusing odds with probability."""
        error_code = kwargs.get("error_code", "OR=2.45 means 2.45x probability  # WRONG")
        correct_code = kwargs.get("correct_code", "OR=2.45 means 2.45x the ODDS    # correct")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_common_disease(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: treating OR as RR when disease is common."""
        error_code = kwargs.get("error_code", "CFR=15% -> OR ~ RR             # WRONG")
        correct_code = kwargs.get("correct_code", "CFR=15% -> OR overestimates RR  # correct")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_logistic(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: forgetting to exponentiate logistic regression coefficients."""
        error_code = kwargs.get("error_code", "coef = 0.89  # this is log(OR), not OR!")
        correct_code = kwargs.get("correct_code", "OR = np.exp(0.89)  # OR = 2.44")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            "下一集：信賴區間（Confidence Interval）",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "點估計不夠，還要知道估計的不確定性！",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
