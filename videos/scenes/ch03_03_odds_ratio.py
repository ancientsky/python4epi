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

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "勝算比（Odds Ratio）",
            "title_sub": "暴露與疾病的關聯強度",
            "odds_risk_heading": "Odds vs Risk（勝算 vs 風險）",
            "odds_risk_p1": "• Risk（風險）= 事件數 / 總人數",
            "odds_risk_p2": "• Odds（勝算）= 事件數 / 非事件數",
            "odds_risk_p4": "• 當疾病罕見時，Odds 近似 Risk",
            "or_interp_heading": "如何解讀 OR？",
            "or_interp_p1": "• OR = 1 → 暴露與疾病無關聯",
            "or_interp_p2": "• OR > 1 → 暴露可能增加疾病風險",
            "or_interp_p3": "• OR < 1 → 暴露可能降低疾病風險",
            "or_interp_p4": "• OR = 2.45 → 使用淋浴者的勝算是未使用者的 2.45 倍",
            "rare_heading": "罕見疾病假設（Rare Disease Assumption）",
            "rare_p1": "• 當盛行率 < 10%，OR 近似 RR",
            "rare_p2": "• 退伍軍人症 CFR 15.7% → OR 不等於 RR",
            "rare_p3": "• 病例對照研究中只能算 OR，不能算 RR",
            "when_heading": "OR vs RR：何時用哪個？",
            "when_p1": "• 世代研究（cohort）→ 用 RR（風險比）",
            "when_p2": "• 病例對照研究（case-control）→ 用 OR",
            "when_p3": "• 邏輯斯迴歸（logistic regression）→ 輸出 OR",
            "when_p4": "• 橫斷面研究 → 可用 PR（盛行率比）或 OR",
            "summary_heading": "重點整理",
            "summary_p1": "1. Odds = p / (1-p)，不是機率本身",
            "summary_p2": "2. OR = (a*d) / (b*c)，來自 2x2 表",
            "summary_p3": "3. OR > 1 暴露增加風險，OR < 1 降低風險",
            "summary_p4": "4. 罕見疾病時 OR 近似 RR",
            "summary_p5": "5. 病例對照研究只能算 OR",
            "extra_banner_title": "額外範例：COVID-19 疫苗保護力",
            "extra_heading": "COVID-19 病例對照研究",
            "extra_p1": "• 研究設計：病例對照（case-control）",
            "extra_p2": "• 病例組：確診 COVID-19 住院者",
            "extra_p3": "• 對照組：同期未確診住院者",
            "extra_p4": "• 暴露：是否接種疫苗",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：信賴區間（Confidence Interval）",
            "outro_sub": "點估計不夠，還要知道估計的不確定性！",
        },
        "en": {
            "title_main": "Odds Ratio (OR)",
            "title_sub": "The strength of the exposure–disease association",
            "odds_risk_heading": "Odds vs Risk",
            "odds_risk_p1": "• Risk = events / total people",
            "odds_risk_p2": "• Odds = events / non-events",
            "odds_risk_p4": "• When disease is rare, odds ≈ risk",
            "or_interp_heading": "How do we read OR?",
            "or_interp_p1": "• OR = 1 → no association between exposure and disease",
            "or_interp_p2": "• OR > 1 → exposure may increase disease risk",
            "or_interp_p3": "• OR < 1 → exposure may lower disease risk",
            "or_interp_p4": "• OR = 2.45 → shower users' odds are 2.45x those of non-users",
            "rare_heading": "The Rare Disease Assumption",
            "rare_p1": "• When prevalence < 10%, OR ≈ RR",
            "rare_p2": "• Legionnaires' CFR 15.7% → OR ≠ RR",
            "rare_p3": "• In case-control studies you can only compute OR, not RR",
            "when_heading": "OR vs RR: which one, when?",
            "when_p1": "• Cohort study → use RR (risk ratio)",
            "when_p2": "• Case-control study → use OR",
            "when_p3": "• Logistic regression → outputs OR",
            "when_p4": "• Cross-sectional study → use PR (prevalence ratio) or OR",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. Odds = p / (1-p), not the probability itself",
            "summary_p2": "2. OR = (a*d) / (b*c), straight from the 2x2 table",
            "summary_p3": "3. OR > 1 exposure raises risk, OR < 1 lowers it",
            "summary_p4": "4. When disease is rare, OR ≈ RR",
            "summary_p5": "5. Case-control studies can only compute OR",
            "extra_banner_title": "Extra example: COVID-19 vaccine efficacy",
            "extra_heading": "COVID-19 case-control study",
            "extra_p1": "• Study design: case-control",
            "extra_p2": "• Cases: hospitalized confirmed COVID-19 patients",
            "extra_p3": "• Controls: same-period hospitalized patients without COVID-19",
            "extra_p4": "• Exposure: whether they were vaccinated",
            "blindspot_banner_title": "3 Common Beginner Traps",
            "outro_heading": "Next up: Confidence Interval",
            "outro_sub": "A point estimate isn't enough — you need its uncertainty too!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the odds ratio lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_odds_vs_risk(self, duration: float = 6.0, **kwargs) -> None:
        """Explain the difference between odds and risk (probability)."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            self.t("odds_risk_heading"),
            font=FONT_MONO,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("odds_risk_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("odds_risk_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• Risk = p, Odds = p / (1 - p)", font=FONT_MONO, font_size=22, color=TEXT_SECONDARY),
            Text(self.t("odds_risk_p4"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
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
            self.t("or_interp_heading"),
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("or_interp_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("or_interp_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("or_interp_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("or_interp_p4"), font=FONT_CJK, font_size=22, color=TEXT_SECONDARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_rare_disease(self, duration: float = 5.0, **kwargs) -> None:
        """Explain the rare disease assumption: OR approximates RR."""
        self.show_step_indicator(5, self.total_steps)

        heading = Text(
            self.t("rare_heading"),
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("rare_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("rare_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("rare_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_when_to_use(self, duration: float = 5.0, **kwargs) -> None:
        """When to use OR vs RR."""
        self.show_step_indicator(6, self.total_steps)

        heading = Text(
            self.t("when_heading"),
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("when_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("when_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("when_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("when_p4"), font=FONT_CJK, font_size=22, color=TEXT_SECONDARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key points about OR."""
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
        """Explain the extra example context."""
        self.show_step_indicator(8, self.total_steps)

        heading = Text(
            self.t("extra_heading"),
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("extra_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("extra_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("extra_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("extra_p4"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
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
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
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
