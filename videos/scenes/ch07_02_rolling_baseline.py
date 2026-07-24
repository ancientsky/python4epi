"""Ch07-02: Rolling mean baseline and shift(1) data leakage"""

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


class Ch07RollingBaselineScene(EpiBaseScene):
    """Tutorial video scene: rolling mean baseline."""

    total_steps: int = 13

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "Rolling mean baseline",
            "title_sub": "shift(1) 救命符",
            "rolling_concept_heading": "rolling 概念",
            "rolling_concept_points": [
                "window 天數的移動平均",
                "daily.rolling(7).mean()",
                "每日對應前 7 天平均",
                "笨但有效的 baseline",
            ],
            "why_shift_heading": "shift(1) 避免 data leakage",
            "window_selection_heading": "for loop 選最佳 window",
            "pros_cons_heading": "優缺點",
            "pros_cons_points": [
                "優：簡單 / 第一天可用 / 無假設",
                "缺：不預測轉折",
                "缺：沒有信賴區間",
                "缺：不能放其他變項",
                "→ baseline 起點很夠",
            ],
            "main_summary_heading": "三件事記起來",
            "main_summary_points": [
                "① rolling(w).mean() = 過去 w 天平均",
                "② shift(1) 不是選配，是必配",
                "③ window 用 MAE for loop 挑",
            ],
            "extra_banner_title": "額外範例：Google Flu Trends 教訓",
            "extra_gft_heading": "Google Flu Trends 2013 慘案",
            "extra_gft_points": [
                "預測流感峰值高估 2 倍",
                "原因：訓練時吃到未來資料",
                "Science 期刊檢討 data leakage",
                "→ shift(1) 在 Google 也是大事",
            ],
            "blindspot_banner_title": "Rolling 地雷 3 選",
            "outro_heading": "下一集：Lag features",
            "outro_sub": "把時序變成迴歸表格",
        },
        "en": {
            "title_main": "Rolling mean baseline",
            "title_sub": "shift(1), your lifesaver",
            "rolling_concept_heading": "The rolling idea",
            "rolling_concept_points": [
                "A moving average over a window of days",
                "daily.rolling(7).mean()",
                "Each day maps to the prior 7-day average",
                "A dumb but effective baseline",
            ],
            "why_shift_heading": "shift(1) avoids data leakage",
            "window_selection_heading": "for loop to pick the best window",
            "pros_cons_heading": "Pros and cons",
            "pros_cons_points": [
                "Pro: simple / usable day one / no assumptions",
                "Con: won't predict turning points",
                "Con: no confidence interval",
                "Con: can't add other variables",
                "→ plenty good as a baseline starting point",
            ],
            "main_summary_heading": "Three things to remember",
            "main_summary_points": [
                "① rolling(w).mean() = past w-day average",
                "② shift(1) isn't optional, it's mandatory",
                "③ pick window with a MAE for loop",
            ],
            "extra_banner_title": "Extra example: the Google Flu Trends lesson",
            "extra_gft_heading": "The Google Flu Trends 2013 disaster",
            "extra_gft_points": [
                "Overshot the flu peak by 2×",
                "Cause: future data leaked into training",
                "Science journal flagged the data leakage",
                "→ shift(1) is a big deal even at Google",
            ],
            "blindspot_banner_title": "3 rolling-mean pitfalls",
            "outro_heading": "Next up: Lag features",
            "outro_sub": "Turn a time series into a regression table",
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
        panel = self.show_code(code, title="rolling.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_rolling_concept(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            self.t("rolling_concept_heading"),
            self.t("rolling_concept_points"),
            duration,
        )

    def show_why_shift(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._code_block(self.t("why_shift_heading"), kwargs.get("code", ""), duration)

    def show_window_selection(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block(self.t("window_selection_heading"), kwargs.get("code", ""), duration)

    def show_pros_cons(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            self.t("pros_cons_heading"),
            self.t("pros_cons_points"),
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

    def show_extra_gft(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            self.t("extra_gft_heading"),
            self.t("extra_gft_points"),
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_no_shift(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "pred = daily.rolling(7).mean()"),
            kwargs.get("correct_code", "pred = daily.rolling(7).mean().shift(1)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_baseline(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "print(f'my model MAE = {mae:.2f}')"),
            kwargs.get("correct_code", "print(f'my MAE vs baseline {mae_roll:.2f}')"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_min_periods(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "daily.rolling(7, min_periods=1).mean()"),
            kwargs.get("correct_code", "daily.rolling(7).mean().shift(1).dropna()"),
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
