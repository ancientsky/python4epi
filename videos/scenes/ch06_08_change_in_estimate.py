"""Ch06-08: Change-in-estimate 10% rule for variable selection"""

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


class Ch06ChangeInEstimateScene(EpiBaseScene):
    """Tutorial video scene: change-in-estimate variable selection."""

    total_steps: int = 14

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
        panel = self.show_code(code, title="cie.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card("CIE 變項選擇", "10% 法則科學篩選", duration=duration)

    def show_what_is_cie(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            "CIE 概念：看 RR 變多少",
            [
                "① 跑最小模型：只有暴露",
                "② 每加一個候選 → 看暴露 RR 變動",
                "③ 變動 >10% → 留（真干擾）",
                "④ 變動 <10% → 不留",
                "這叫 10% 法則",
            ],
            duration,
        )

    def show_why_10_percent(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            "為什麼選 10%？",
            [
                "流病界經驗共識",
                "<10% 通常是隨機波動",
                ">10% 實質改變效應",
                "不是神聖，但夠保守實用",
            ],
            duration,
        )

    def show_code_demo(self, duration: float = 10.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block("CIE for loop 範例", kwargs.get("code", ""), duration)

    def show_final_model(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            "組成精簡模型",
            [
                "infected ~ shower_use + keepers",
                "只留真正會改變 RR 的變項",
                "從 15 變項 → 3~5 個",
                "CI 更窄、解讀更清晰",
                "→ 科學性變項選擇",
            ],
            duration,
        )

    def show_aic_complement(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._code_block("AIC 輔助（點菜比喻）", kwargs.get("code", ""), duration)

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            "CIE 三步驟",
            [
                "① 最小模型 → 記暴露 RR",
                "② for loop 加候選、算 CIE",
                "③ >10% 留下組精簡模型",
                "→ AIC 輔助 = 完整流程",
            ],
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner("額外範例：肺結核接觸追蹤"), duration=duration)

    def show_extra_tb(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets(
            "TB 接觸者研究",
            [
                "crude RR 3.5，候選 15 個",
                "CIE >10%：BCG、HIV、營養",
                "CIE <5%：年齡、性別、社經",
                "精簡 → adjusted RR 2.8",
                "→ 嚴謹分析可發 Lancet",
            ],
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner("CIE 地雷 3 選"), duration=duration)

    def show_blindspot_denom(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "cie = abs(rr_min - rr_adj) / rr_min * 100"),
            kwargs.get("correct_code", "cie = abs(rr_min - rr_adj) / rr_adj * 100"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_p_only(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "if model.pvalues[var] < 0.05: keep.append(var)"),
            kwargs.get("correct_code", "if cie_percent(var) > 10: keep.append(var)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_collider(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "candidates = all_available_vars"),
            kwargs.get("correct_code", "candidates = confounders_from_dag"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text("恭喜完成 Ch06！", font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text("下一章 Ch07：時間序列與預測", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
