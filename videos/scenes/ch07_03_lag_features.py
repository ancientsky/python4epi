"""Ch07-03: Lag features - turn time series into regression table"""

from __future__ import annotations

from manim import DOWN, LEFT, UP, ORIGIN, FadeIn, FadeOut, Text, VGroup

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_ORANGE,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch07LagFeaturesScene(EpiBaseScene):
    """Tutorial video scene: lag features."""

    total_steps: int = 13

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "Lag features 魔法",
            "title_sub": "時序變迴歸表格",
            "problem_heading": "迴歸要什麼？",
            "problem_points": [
                "每列要獨立樣本",
                "時序每列跟前後相關",
                "解法：搬昨天的值進今天這列",
                "→ 這就是 lag features",
            ],
            "shift_concept_heading": "shift 的作用：整欄下推",
            "shift_concept_points": [
                "原始：5, 8, 12, 15, 10",
                "shift(1)：NaN, 5, 8, 12, 15",
                "shift(2) = 前天",
                "shift(7) = 上週同一天",
                "一個 shift，串起時間",
            ],
            "build_lag_table_heading": "造 lag_1、lag_2 + dropna",
            "how_many_lags_heading": "要加幾個 lag？",
            "how_many_lags_points": [
                "太少：捕捉不到週期",
                "太多：共線性 + 過度配適",
                "短序列（<30 天）：lag_1、lag_2",
                "長序列（>60 天）：加 lag_7",
                "ACF 圖可輔助選擇",
            ],
            "main_summary_heading": "四步驟總結",
            "main_summary_points": [
                "① reset_index 攤平日期",
                "② day_idx 當趨勢",
                "③ shift(1)、shift(2) 造 lag",
                "④ dropna 清前幾列",
            ],
            "extra_banner_title": "額外範例：SARS 2003 和平醫院",
            "extra_sars_heading": "SARS 2003 時序分析",
            "extra_sars_points": [
                "每日通報 + lag_1 ~ lag_7",
                "lag_1 和 lag_7 係數最大",
                "「上週同一天」最有預測力",
                "→ 啟發「星期幾」變項",
                "shift(7) 救了監測效率",
            ],
            "blindspot_banner_title": "Lag 地雷 3 選",
            "outro_heading": "下一集：Poisson + lag",
            "outro_sub": "IRR 解讀每日病例",
        },
        "en": {
            "title_main": "Lag feature magic",
            "title_sub": "Turn a time series into a regression table",
            "problem_heading": "What does regression need?",
            "problem_points": [
                "Each row should be an independent sample",
                "In a series each row correlates with its neighbors",
                "Fix: move yesterday's value into today's row",
                "→ that's exactly lag features",
            ],
            "shift_concept_heading": "What shift does: push the whole column down",
            "shift_concept_points": [
                "Original: 5, 8, 12, 15, 10",
                "shift(1): NaN, 5, 8, 12, 15",
                "shift(2) = day before yesterday",
                "shift(7) = same day last week",
                "One shift stitches time together",
            ],
            "build_lag_table_heading": "Build lag_1, lag_2 + dropna",
            "how_many_lags_heading": "How many lags to add?",
            "how_many_lags_points": [
                "Too few: can't capture cycles",
                "Too many: collinearity + overfitting",
                "Short series (<30 days): lag_1, lag_2",
                "Long series (>60 days): add lag_7",
                "An ACF plot helps you choose",
            ],
            "main_summary_heading": "Four-step summary",
            "main_summary_points": [
                "① reset_index to flatten the date",
                "② day_idx as the trend",
                "③ shift(1), shift(2) to build lags",
                "④ dropna to clean the first rows",
            ],
            "extra_banner_title": "Extra example: SARS 2003, Heping Hospital",
            "extra_sars_heading": "SARS 2003 time-series analysis",
            "extra_sars_points": [
                "Daily reports + lag_1 ~ lag_7",
                "lag_1 and lag_7 had the biggest coefficients",
                "\"Same day last week\" was most predictive",
                "→ inspired a \"day of week\" variable",
                "shift(7) rescued surveillance efficiency",
            ],
            "blindspot_banner_title": "3 lag-feature pitfalls",
            "outro_heading": "Next up: Poisson + lag",
            "outro_sub": "Read daily cases with the IRR",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    def _bullets(self, heading: str, lines: list[str], duration: float) -> None:
        h = Text(heading, font=FONT_CJK, font_size=30, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        bl = VGroup(
            *[Text(x, font=FONT_CJK, font_size=23, color=TEXT_PRIMARY) for x in lines]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(h, DOWN, buff=0.6)
        self.play(FadeIn(h), run_time=0.5)
        self.play(FadeIn(bl, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(h, bl)), run_time=0.5)

    def _code_block(self, heading: str, code: str, duration: float) -> None:
        h = Text(heading, font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).to_edge(UP, buff=0.5)
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_code(code, title="lag.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_problem(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            self.t("problem_heading"),
            self.t("problem_points"),
            duration,
        )

    def show_shift_concept(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            self.t("shift_concept_heading"),
            self.t("shift_concept_points"),
            duration,
        )

    def show_build_lag_table(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block(self.t("build_lag_table_heading"), kwargs.get("code", ""), duration)

    def show_how_many_lags(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            self.t("how_many_lags_heading"),
            self.t("how_many_lags_points"),
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            self.t("main_summary_heading"),
            self.t("main_summary_points"),
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_sars(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            self.t("extra_sars_heading"),
            self.t("extra_sars_points"),
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_shift_neg(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "ts['lag_1'] = ts['cases'].shift(-1)"),
            kwargs.get("correct_code", "ts['lag_1'] = ts['cases'].shift(1)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_dropna(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "ts_model = ts"),
            kwargs.get("correct_code", "ts_model = ts.dropna().reset_index(drop=True)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_too_many_lags(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "for k in range(1, 15): ts[f'lag_{k}'] = ..."),
            kwargs.get("correct_code", "ts['lag_1'] = ...; ts['lag_2'] = ..."),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text(self.t("outro_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text(self.t("outro_sub"), font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
