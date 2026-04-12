"""Ch07-01: Time series basics - asfreq, autocorrelation, stationarity"""

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


class Ch07TsBasicsScene(EpiBaseScene):
    """Tutorial video scene: time series basic concepts."""

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
        panel = self.show_code(code, title="ts.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card("時間序列基本概念", "asfreq、自相關、平穩性", duration=duration)

    def show_what_is_ts(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            "時間序列是什麼？",
            [
                "按時間排列的觀測值",
                "每日病例、每小時急診、每週通報",
                "相鄰點高度相關（關鍵特徵）",
                "→ 時間序列分析的主旋律",
            ],
            duration,
        )

    def show_asfreq_gap(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._code_block("asfreq('D', fill_value=0)", kwargs.get("code", ""), duration)

    def show_autocorrelation(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets(
            "自相關 autocorrelation",
            [
                "今天 ↔ 昨天、前天、上週",
                "傳染病天生自相關高",
                "有自相關 → lag features 有用",
                "無自相關 → 加 lag 是浪費",
            ],
            duration,
        )

    def show_stationarity(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            "平穩性 stationarity",
            [
                "均值、變異不隨時間漂移",
                "像一條河水位穩定起伏",
                "ARIMA 的前提條件",
                "不平穩 → 做差分（I 的意思）",
            ],
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            "三概念打包",
            [
                "① asfreq 補齊日期",
                "② 自相關是主旋律",
                "③ 平穩性是 ARIMA 前提",
            ],
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner("額外範例：COVID-19 每日確診"), duration=duration)

    def show_extra_covid(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            "2022 Omicron 序列特徵",
            [
                "強自相關（幾乎 1.1×）",
                "明顯趨勢（300→9 萬）",
                "週效應（週末少通報）",
                "→ SARIMA 最適合",
            ],
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner("時序基本地雷 3 選"), duration=duration)

    def show_blindspot_no_asfreq(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "daily = cases.groupby('date').size()"),
            kwargs.get("correct_code", "daily.asfreq('D', fill_value=0)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_string_date(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "df.sort_values('date')"),
            kwargs.get("correct_code", "df['date'] = pd.to_datetime(df['date'])"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_adf(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "ARIMA(series, order=(1, 0, 1)).fit()"),
            kwargs.get("correct_code", "adfuller(series); # check p-value first"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text("下一集：Rolling mean baseline", font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text("shift(1) 救命符", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
