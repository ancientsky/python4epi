"""Ch12-05: Attributable Risk (AR) and Population Attributable Risk (PAR/PAF).

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. AR answers the
individual-level question ("how much extra risk does the exposed group carry?")
while PAR/PAF answer the population-level question ("how many cases could the
whole population shed if this exposure were removed?"). All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages.
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
    ManimColor,
    RoundedRectangle,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_BLUE,
    ACCENT_ORANGE,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch12ARPARScene(EpiBaseScene):
    """Tutorial video scene: attributable risk AR and population AR / PAF."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "歸因風險 AR 與族群歸因風險 PAR",
            "title_sub": "把「有關」變成「能救幾個人」",
            "ar_vs_rr_heading": "AR 相減，RR 相除",
            "ar_vs_rr_lines": [
                "風險比 RR（相除）：風險變成幾倍",
                "歸因風險 AR（相減）：多背了幾個百分點",
                "RR 大但 AR 小 → 相對高、實際可預防病例卻少",
                "→ 同一份資料，兩種完全不同的問法",
            ],
            "twobytwo_heading": "食物中毒教學 2×2 表（示範數字）",
            "col_ill": "患病 Ill",
            "col_well": "未患病 Well",
            "row_exposed": "暴露\nExposed",
            "row_unexposed": "未暴露\nUnexposed",
            "twobytwo_caption": "暴露組風險 30.0%、未暴露組 6.25% → 光看就差很多",
            "ar_code_heading": "AR 是相減，RR 是相除",
            "ar_code_title": "attributable_risk.py",
            "par_paf_heading": "PAR／PAF：族群視角 + Levin 公式",
            "par_paf_title": "population_ar.py",
            "ar_output_heading": "跑出來的結果",
            "ar_output_text": (
                "AR = 0.2375 → 暴露組多背 23.7 個百分點\n"
                "RR = 4.80 → 風險變 4.8 倍\n"
                "PAR = 0.1188、PAF = 65.5%\n"
                "→ 若真為因果，理論上可少掉 65% 病例"
            ),
            "summary_heading": "AR／PAR 三重點",
            "summary_lines": [
                "① AR 相減、RR 相除，差一個符號別搞混",
                "② PAR／PAF 是族群視角，分母換成全體",
                "③ PAF 只有在因果成立時才能拿去估「救多少人」",
                "→ 關聯翻成決策數字，完成！",
            ],
            "extra_banner_title": "額外範例：抽菸對肺病的族群歸因",
            "extra_smoking_heading": "同一條 Levin 公式，換個暴露照樣用",
            "extra_smoking_title": "smoking_paf.py",
            "blindspot_banner_title": "AR／PAR 三個新手地雷",
            "outro_heading": "下一集：差異中之差異 DiD",
            "outro_sub": "正面對決「介入到底有沒有效」",
        },
        "en": {
            "title_main": "Attributable Risk AR & Population AR (PAR)",
            "title_sub": 'Turning "associated with" into "how many can we save"',
            "ar_vs_rr_heading": "AR subtracts, RR divides",
            "ar_vs_rr_lines": [
                "Risk ratio RR (divide): how many times the risk",
                "Attributable risk AR (subtract): how many extra points",
                "Big RR but small AR -> high relative risk, few preventable cases",
                "-> Same data, two completely different questions",
            ],
            "twobytwo_heading": "Food-poisoning teaching 2x2 table (demo numbers)",
            "col_ill": "Ill",
            "col_well": "Well",
            "row_exposed": "Exposed",
            "row_unexposed": "Unexposed",
            "twobytwo_caption": "Exposed risk 30.0%, unexposed 6.25% -> a clear gap",
            "ar_code_heading": "AR subtracts, RR divides",
            "ar_code_title": "attributable_risk.py",
            "par_paf_heading": "PAR / PAF: population view + Levin's formula",
            "par_paf_title": "population_ar.py",
            "ar_output_heading": "The result",
            "ar_output_text": (
                "AR = 0.2375 -> exposed carry +23.7 pts\n"
                "RR = 4.80 -> risk is 4.8x\n"
                "PAR = 0.1188, PAF = 65.5%\n"
                "-> if causal, ~65% of cases preventable"
            ),
            "summary_heading": "Three Takeaways on AR / PAR",
            "summary_lines": [
                "1. AR subtracts, RR divides - one wrong sign ruins it",
                "2. PAR / PAF are population views, denominator = everyone",
                '3. PAF only estimates "cases saved" if the link is causal',
                "-> Association turned into a decision number!",
            ],
            "extra_banner_title": "Extra example: population attribution of smoking to lung disease",
            "extra_smoking_heading": "Same Levin formula, just swap the exposure",
            "extra_smoking_title": "smoking_paf.py",
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Coming next: Difference-in-Differences (DiD)",
            "outro_sub": 'Facing "did the intervention actually work?" head on',
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _bullets(self, heading_key: str, lines_key: str, duration: float) -> None:
        heading = self.t(heading_key)
        lines = self.t(lines_key)
        h = Text(heading, font=FONT_CJK, font_size=30, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        bl = (
            VGroup(*[Text(x, font=FONT_CJK, font_size=23, color=TEXT_PRIMARY) for x in lines])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            .next_to(h, DOWN, buff=0.6)
        )
        self.play(FadeIn(h), run_time=0.5)
        self.play(FadeIn(bl, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(h, bl)), run_time=0.5)

    def _code_block(self, heading_key: str, title_key: str, code: str, duration: float) -> None:
        h = Text(self.t(heading_key), font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.5
        )
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_code(code, title=self.t(title_key), position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def _cell(self, value: str, tint: str, pos) -> VGroup:
        card = RoundedRectangle(
            corner_radius=0.12,
            width=2.4,
            height=1.4,
            fill_color=ManimColor(tint),
            fill_opacity=0.14,
            stroke_color=ManimColor(tint),
            stroke_width=3,
        )
        val = Text(value, font=FONT_MONO, font_size=34, color=ManimColor(tint), weight="BOLD")
        val.move_to(card.get_center())
        return VGroup(card, val).move_to(pos)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_ar_vs_rr(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("ar_vs_rr_heading", "ar_vs_rr_lines", duration)

    def show_two_by_two(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            self.t("twobytwo_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)

        a = self._cell("120", ACCENT_ORANGE, LEFT * 1.35 + UP * 0.8)
        b = self._cell("280", ACCENT_ORANGE, RIGHT * 1.35 + UP * 0.8)
        c = self._cell("25", ACCENT_BLUE, LEFT * 1.35 + DOWN * 0.8)
        d = self._cell("375", ACCENT_BLUE, RIGHT * 1.35 + DOWN * 0.8)
        grid = VGroup(a, b, c, d)

        col_ill = Text(
            self.t("col_ill"), font=FONT_CJK, font_size=19, color=TEXT_SECONDARY
        ).next_to(a, UP, buff=0.25)
        col_well = Text(
            self.t("col_well"), font=FONT_CJK, font_size=19, color=TEXT_SECONDARY
        ).next_to(b, UP, buff=0.25)
        row_exp = Text(
            self.t("row_exposed"), font=FONT_CJK, font_size=17, color=ManimColor(ACCENT_ORANGE)
        ).next_to(a, LEFT, buff=0.3)
        row_unexp = Text(
            self.t("row_unexposed"), font=FONT_CJK, font_size=17, color=ManimColor(ACCENT_BLUE)
        ).next_to(c, LEFT, buff=0.3)

        caption = Text(
            self.t("twobytwo_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        labels = VGroup(col_ill, col_well, row_exp, row_unexp)
        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(grid, lag_ratio=0.15), run_time=1.1)
        self.play(FadeIn(labels), run_time=0.5)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.4))
        self.play(FadeOut(VGroup(heading, grid, labels, caption)), run_time=0.5)

    def show_ar_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "a, b, c, d = 120, 280, 25, 375\n"
                "risk_exp = a / (a + b)      # 0.300\n"
                "risk_unexp = c / (c + d)    # 0.0625\n"
                "AR = risk_exp - risk_unexp  # 相減，不是相除！\n"
                "RR = risk_exp / risk_unexp  # 這才是相除"
            ),
        )
        self._code_block("ar_code_heading", "ar_code_title", code, duration)

    def show_par_paf(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "risk_total = (a + c) / (a + b + c + d)     # 0.181\n"
                "Pe = (a + b) / (a + b + c + d)             # 暴露盛行率 0.5\n"
                "PAR = risk_total - risk_unexp              # 族群歸因風險\n"
                "PAF = Pe * (RR - 1) / (1 + Pe * (RR - 1))  # Levin 公式"
            ),
        )
        self._code_block("par_paf_heading", "par_paf_title", code, duration)

    def show_ar_output(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        h = Text(
            self.t("ar_output_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_output(
            kwargs.get("output", self.t("ar_output_text")),
            position=ORIGIN,
        )
        self.wait(max(0.1, duration - 1.2))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_main_summary(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_smoking(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "Pe, RR = 0.25, 10        # 吸菸盛行率、肺病風險比\n"
                "PAF = Pe * (RR - 1) / (1 + Pe * (RR - 1))\n"
                'print(f"PAF = {PAF:.0%}")   # PAF = 69%\n'
                "# 全族群近七成肺病可歸因於吸菸"
            ),
        )
        self._code_block("extra_smoking_heading", "extra_smoking_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_subtract_not_divide(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "AR = risk_exp / risk_unexp"),
            kwargs.get("correct_code", "AR = risk_exp - risk_unexp"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_rr_alone(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "pop_impact = RR"),
            kwargs.get("correct_code", "PAF = Pe*(RR-1) / (1 + Pe*(RR-1))"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_paf_causal(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "saved = total_cases * PAF"),
            kwargs.get("correct_code", "if causal: saved = total_cases * PAF"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text(self.t("outro_heading"), font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).move_to(
            ORIGIN + UP * 0.5
        )
        s = Text(self.t("outro_sub"), font=FONT_CJK, font_size=20, color=TEXT_SECONDARY).next_to(
            h, DOWN, buff=0.4
        )
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
