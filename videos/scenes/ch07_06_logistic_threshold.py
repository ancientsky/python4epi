"""Ch07-06: Logistic regression for binary threshold alert"""

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


class Ch07LogisticThresholdScene(EpiBaseScene):
    """Tutorial video scene: Logistic threshold alert."""

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
        panel = self.show_code(code, title="logit.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card("Logistic threshold 警報", "是否高峰日二元預測", duration=duration)

    def show_continuous_vs_binary(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            "連續 vs 二元",
            [
                "連續：明天 7.3 人（長官聽不懂）",
                "二元：超過門檻機率 72%",
                "長官要的是「要不要啟動」",
                "Logistic 輸出機率 → yes/no",
                "警報系統真正要的輸出",
            ],
            duration,
        )

    def show_define_threshold(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._code_block("定義高峰日：quantile 0.75", kwargs.get("code", ""), duration)

    def show_logit_code(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block("smf.logit + lag 特徵", kwargs.get("code", ""), duration)

    def show_evaluate_accuracy(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            "Accuracy 的陷阱",
            [
                "accuracy = 預測對的比例",
                "高峰日只 25%、全猜 0 → 75%",
                "真正關鍵：sensitivity、ROC",
                "初學 accuracy 打底",
                "進階再上 AUC",
            ],
            duration,
        )

    def show_action_threshold(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            "行動門檻不是 0.5",
            [
                "0.5 是數學預設",
                "公衛：寧可多演練",
                "實務門檻 0.2 - 0.3",
                "假警報↑ 但漏警率↓",
                "高 sensitivity 換 specificity",
            ],
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            "Logistic 警報三件事",
            [
                "① quantile 0.75 定門檻",
                "② logit ~ lag_1 + lag_2",
                "③ 行動門檻 0.2-0.5 視風險",
                "→ 比預測幾人更貼近決策",
            ],
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner("額外範例：流感季前警報系統"), duration=duration)

    def show_extra_flu_alert(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets(
            "CDC 流感警報",
            [
                "過去 5 年同週 baseline",
                "高於 baseline + 2 SD → 警報",
                "現代版加氣溫、學校、lag",
                "機率門檻 0.3",
                "2018 南韓提前 2 週偵測",
            ],
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner("Logistic 警報地雷 3 選"), duration=duration)

    def show_blindspot_only_accuracy(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "print(f'accuracy = {acc:.2f}')"),
            kwargs.get("correct_code", "print(f'sensitivity = {tp/(tp+fn):.2f}')"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_default_threshold(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "pred = (prob > 0.5).astype(int)"),
            kwargs.get("correct_code", "pred = (prob > 0.3).astype(int)  # public health"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_leaky_threshold(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "threshold = ts_model['cases'].quantile(0.75)"),
            kwargs.get("correct_code", "threshold = train_cases.quantile(0.75)  # train only"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text("下一集：ARIMA / SARIMA", font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text("長期監測經典武器", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
