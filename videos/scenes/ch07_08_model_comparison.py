"""Ch07-08: Six-model comparison and selection guide"""

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


class Ch07ModelComparisonScene(EpiBaseScene):
    """Tutorial video scene: six time-series model comparison."""

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

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card("六模型大比拼", "誰適合什麼情境", duration=duration)

    def show_comparison_table(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            "六模型比較表",
            [
                "Rolling mean：5 天 / 無週期 / 無 CI",
                "Poisson + lag：10 天 / 部分 / 有 CI",
                "NB + lag：10 天 / 部分 / 有 CI",
                "Logistic：10 天 / 二元 / 機率 CI",
                "ARIMA：30 天 / 弱 / 有 CI",
                "SARIMA：60 天 / 強 / 有 CI",
            ],
            duration,
        )

    def show_decision_tree(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            "決策樹四問",
            [
                "只有 1-2 週？→ Rolling / Poisson",
                "過度離散？→ Negative Binomial",
                "是否警報？→ Logistic threshold",
                ">30 天無週期？→ ARIMA",
                "有週期？→ SARIMA",
            ],
            duration,
        )

    def show_mae_aic_rules(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets(
            "MAE / AIC 解讀規則",
            [
                "MAE 越小越好",
                "AIC 越小越好（懲罰複雜度）",
                "永遠跟 baseline 比較",
                "MAE 差 ≥ 10% 才有意義",
                "AIC 差 ≥ 10 才有意義",
            ],
            duration,
        )

    def show_complexity_vs_data(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            "複雜度 vs 資料量",
            [
                "資料少 → 用簡單模型",
                "資料多 → 可試複雜模型",
                "17 天 outbreak SARIMA 跑不動",
                "90 天合成才能示範 SARIMA",
                "不為炫技選錯工具",
            ],
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            "Ch07 畢業五口訣",
            [
                "① 短 → Rolling、Poisson+lag",
                "② 過度離散 → NB",
                "③ 是否警報 → Logistic",
                "④ 中長期 → ARIMA",
                "⑤ 有週期 → SARIMA",
            ],
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner("額外範例：COVID-19 Forecast Hub"), duration=duration)

    def show_extra_covid_forecast(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            "CDC COVID 預測比賽",
            [
                "2020 全世界團隊每週預測",
                "模型：ARIMA、LSTM、Transformer",
                "1 週預測 ARIMA/SARIMA 穩居前段",
                "4 週預測 ensemble 勝出",
                "別迷信深度學習",
            ],
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner("模型選擇地雷 3 選"), duration=duration)

    def show_blindspot_ml_hype(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "model = LSTM(hidden=128).fit(daily_17days)"),
            kwargs.get("correct_code", "model = Poisson_with_lag.fit(daily_17days)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_only_mae(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "select_model(min_mae_only=True)"),
            kwargs.get("correct_code", "select_model(mae, ci, interp, cost, cycle)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_retrain(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "# deploy once and forget"),
            kwargs.get("correct_code", "# retrain weekly, re-evaluate monthly"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text("下一章：Ch08 空間流病", font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text("Python 畫出精美疾病地圖", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
