"""Ch07-07: ARIMA and SARIMA for long-term surveillance forecasting"""

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


class Ch07ArimaSarimaScene(EpiBaseScene):
    """Tutorial video scene: ARIMA and SARIMA."""

    total_steps: int = 13

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
        panel = self.show_code(code, title="arima.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card("ARIMA / SARIMA", "時序經典武器", duration=duration)

    def show_three_letters(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            "ARIMA 三字母",
            [
                "AR = 看過去 p 天自己",
                "I = 做 d 次差分讓序列平穩",
                "MA = 看過去 q 次預測誤差",
                "ARIMA(p, d, q) 三旋鈕",
                "SARIMA 多一組 (P, D, Q, s)",
            ],
            duration,
        )

    def show_why_not_outbreak(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            "為什麼不用 outbreak 資料？",
            [
                "ARIMA 至少 30 天",
                "SARIMA 至少 2 個週期",
                "17 天硬套 → 過度配適",
                "改用合成 90 天類流感資料",
                "短序列回去用 Poisson",
            ],
            duration,
        )

    def show_synth_data(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block("合成 90 天資料（trend+seasonal+noise）", kwargs.get("code", ""), duration)

    def show_adf_test(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._code_block("ADF 平穩性檢定", kwargs.get("code", ""), duration)

    def show_arima_fit(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._code_block("ARIMA(1,1,1) 擬合 + forecast", kwargs.get("code", ""), duration)

    def show_sarima_fit(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._code_block("SARIMA(1,1,1)(1,1,1,7)", kwargs.get("code", ""), duration)

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets(
            "ARIMA/SARIMA 五步 SOP",
            [
                "① 資料 ≥ 30 天",
                "② ADF 看差分",
                "③ ARIMA(1,1,1) 起手",
                "④ 有週期 → 升級 SARIMA",
                "⑤ train/test 算 MAE",
            ],
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner("額外範例：Box-Jenkins 1970"), duration=duration)

    def show_extra_bj(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        self._bullets(
            "Box-Jenkins 經典",
            [
                "1970《Time Series Analysis》",
                "50 年金融氣象公衛愛用",
                "2009 H1N1 CDC 用 ARIMA",
                "提前 3 週預測就醫高峰",
                "幫助疫苗配送醫護排班",
            ],
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner("ARIMA 地雷 3 選"), duration=duration)

    def show_blindspot_short_data(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "ARIMA(daily_17days, order=(2,1,2)).fit()"),
            kwargs.get("correct_code", "# for <30 days, use Poisson+lag or rolling mean"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_force_sarima(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "SARIMAX(series, seasonal_order=(1,1,1,7))"),
            kwargs.get("correct_code", "# check ACF peaks first; use ARIMA if no seasonality"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_random_order(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(11, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "ARIMA(train, order=(5, 3, 5))"),
            kwargs.get("correct_code", "auto_arima(train, seasonal=False).fit()"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text("下一集：六模型大比拼", font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text("誰是王者？誰適合什麼情境？", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
