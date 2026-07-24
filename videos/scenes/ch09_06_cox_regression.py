"""Ch09-06: Cox proportional-hazards regression - quantifying each factor's HR.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
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
    Dot,
    FadeIn,
    FadeOut,
    Line,
    ManimColor,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_GREEN,
    ACCENT_ORANGE,
    BORDER_LIGHT,
    ERROR_RED,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch09CoxRegressionScene(EpiBaseScene):
    """Tutorial video scene: Cox proportional-hazards regression and print_summary."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "Cox 比例風險迴歸",
            "title_sub": "一次放進所有因子，各算一個「風險比」",
            "why_heading": "為什麼還要 Cox？",
            "why_lines": [
                "Log-rank 只告訴你「有沒有差」",
                "Cox 更進一步：「差多少」",
                "還能同時放進年齡、性別、共病……",
                "→ 每個因子各算一個校正後的 HR",
            ],
            "hr_heading": "風險比 HR 是一把量尺",
            "hr_scale_low": "HR ≈ 0.5\n保護因子（死得慢）",
            "hr_scale_one": "HR = 1\n無關聯",
            "hr_scale_high": "HR ≈ 2\n危險因子（死得快）",
            "hr_caption": "HR 是「速率比」——不是機率、也不是勝算比",
            "code_heading": "三行 fit 一個 Cox 模型",
            "code_title": "cox_regression.py",
            "read_heading": "print_summary() 只要盯兩欄",
            "read_lines": [
                "exp(coef) 就是 HR ← 全場最重要",
                "p < 0.05 才算統計顯著",
                "HR 的 95% 信賴區間跨過 1 → 不顯著",
                "最下面 Concordance = c-index 排序力",
            ],
            "epv_heading": "樣本數警訊：EPV",
            "epv_lines": [
                "口訣：每個變項至少要 10 個事件",
                "本案 19 死亡 ÷ 7 變項 ≈ 2.7 << 10",
                "太多變項 → 過度配適，HR 和 CI 不可靠",
                "→ 先篩選，只留 1-2 個關鍵因子",
            ],
            "summary_heading": "Cox 迴歸三重點",
            "summary_lines": [
                "① 看 exp(coef)=HR：方向 + 強度",
                "② 看 CI 有沒有跨 1：確定性",
                "③ c-index 看排序力、EPV 看撐不撐得住",
                "→ 下一集把這張表畫成森林圖",
            ],
            "extra_banner_title": "額外範例：洗腎世代的死亡風險因子",
            "extra_dialysis_heading": "同一台 CoxPHFitter，換洗腎資料",
            "extra_dialysis_title": "cox_dialysis.py",
            "blindspot_banner_title": "Cox 迴歸三個新手地雷",
            "outro_heading": "下一集：HR 森林圖",
            "outro_sub": "把 print_summary 的數字，變成一眼看懂的圖",
        },
        "en": {
            "title_main": "Cox Proportional-Hazards Regression",
            "title_sub": 'Put every factor in at once, get a "hazard ratio" for each',
            "why_heading": "Why still use Cox?",
            "why_lines": [
                'Log-rank only tells you "is there a difference"',
                'Cox goes further: "how big is the difference"',
                "It can hold age, sex, comorbidities together...",
                "-> each factor gets its own adjusted HR",
            ],
            "hr_heading": "The Hazard Ratio HR is a Ruler",
            "hr_scale_low": "HR is about 0.5\nprotective (dies slower)",
            "hr_scale_one": "HR = 1\nno association",
            "hr_scale_high": "HR is about 2\nharmful (dies faster)",
            "hr_caption": 'HR is a "rate ratio" - not a probability, not an odds ratio',
            "code_heading": "Three lines to fit a Cox model",
            "code_title": "cox_regression.py",
            "read_heading": "print_summary(): just watch two columns",
            "read_lines": [
                "exp(coef) IS the HR <- the most important",
                "p < 0.05 for statistical significance",
                "the HR's 95% CI crossing 1 -> not significant",
                "bottom Concordance = c-index ranking power",
            ],
            "epv_heading": "Sample-size warning: EPV",
            "epv_lines": [
                "Rule: at least 10 events per variable",
                "Here 19 deaths / 7 vars ~ 2.7 << 10",
                "too many vars -> overfit, HR and CI unreliable",
                "-> screen first, keep only 1-2 key factors",
            ],
            "summary_heading": "Three Takeaways on Cox Regression",
            "summary_lines": [
                "1. Read exp(coef)=HR: direction + strength",
                "2. Check if the CI crosses 1: certainty",
                "3. c-index for ranking, EPV for sample size",
                "-> next episode turns this table into a forest plot",
            ],
            "extra_banner_title": "Extra example: mortality risk factors in a dialysis cohort",
            "extra_dialysis_heading": "Same CoxPHFitter, swap in dialysis data",
            "extra_dialysis_title": "cox_dialysis.py",
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: the HR forest plot",
            "outro_sub": "turn print_summary's numbers into an at-a-glance chart",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _bullets(self, heading_key: str, lines_key: str, duration: float) -> None:
        h = Text(
            self.t(heading_key), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.8)
        bl = (
            VGroup(
                *[
                    Text(x, font=FONT_CJK, font_size=23, color=TEXT_PRIMARY)
                    for x in self.t(lines_key)
                ]
            )
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

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_why_cox(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("why_heading", "why_lines", duration)

    def show_hr_meaning(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            self.t("hr_heading"), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.8)

        axis = Line(LEFT * 3.2, RIGHT * 3.2, color=ManimColor(BORDER_LIGHT), stroke_width=3)

        low_dot = Dot(point=LEFT * 3.2, radius=0.13, color=ManimColor(ACCENT_GREEN))
        one_dot = Dot(point=ORIGIN, radius=0.13, color=ManimColor(TEXT_SECONDARY))
        high_dot = Dot(point=RIGHT * 3.2, radius=0.13, color=ManimColor(ERROR_RED))

        low_label = Text(
            self.t("hr_scale_low"), font=FONT_CJK, font_size=16, color=TEXT_PRIMARY
        ).next_to(low_dot, DOWN, buff=0.3)
        one_label = Text(
            self.t("hr_scale_one"), font=FONT_CJK, font_size=16, color=TEXT_PRIMARY
        ).next_to(one_dot, DOWN, buff=0.3)
        high_label = Text(
            self.t("hr_scale_high"), font=FONT_CJK, font_size=16, color=TEXT_PRIMARY
        ).next_to(high_dot, DOWN, buff=0.3)

        scale = VGroup(
            axis, low_dot, one_dot, high_dot, low_label, one_label, high_label
        ).move_to(UP * 0.3)

        caption = Text(
            self.t("hr_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(scale), run_time=0.9)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(heading, scale, caption)), run_time=0.5)

    def show_cox_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "from lifelines import CoxPHFitter\n"
                "\n"
                'cox_df["is_male"] = (cox_df["sex"] == "M").astype(int)\n'
                'cox_df = cox_df.drop(columns=["sex"])\n'
                "\n"
                "cph = CoxPHFitter()\n"
                'cph.fit(cox_df, "time_to_event", "event")\n'
                "cph.print_summary()   # exp(coef)=HR, p, 95% CI"
            ),
        )
        self._code_block("code_heading", "code_title", code, duration)

    def show_read_summary(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("read_heading", "read_lines", duration)

    def show_epv_warning(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("epv_heading", "epv_lines", duration)

    def show_main_summary(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_dialysis(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "# dialysis cohort: follow months, event = death\n"
                "cox = CoxPHFitter()\n"
                'cox.fit(dialysis, "months", "death")\n'
                "cox.print_summary()   # HR for age / DM / albumin\n"
                'print("c-index =", cox.concordance_index_)'
            ),
        )
        self._code_block("extra_dialysis_heading", "extra_dialysis_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_coef_vs_hr(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'hr = cph.summary["coef"]  # this is logHR'),
            kwargs.get("correct_code", 'hr = cph.summary["exp(coef)"]  # real HR'),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_epv(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'cph.fit(df7, "time", "event")  # 19 events'),
            kwargs.get("correct_code", 'cph.fit(df[top2], "time", "event")'),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_id_column(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'cph.fit(cox_df, "time", "event")  # has id'),
            kwargs.get("correct_code", 'cox_df = cox_df.drop(columns="case_id")'),
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
