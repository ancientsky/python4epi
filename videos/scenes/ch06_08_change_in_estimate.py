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

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "CIE 變項選擇",
            "title_sub": "10% 法則科學篩選",
            "what_is_cie_heading": "CIE 概念：看 RR 變多少",
            "what_is_cie_lines": [
                "① 跑最小模型：只有暴露",
                "② 每加一個候選 → 看暴露 RR 變動",
                "③ 變動 >10% → 留（真干擾）",
                "④ 變動 <10% → 不留",
                "這叫 10% 法則",
            ],
            "why_10_heading": "為什麼選 10%？",
            "why_10_lines": [
                "流病界經驗共識",
                "<10% 通常是隨機波動",
                ">10% 實質改變效應",
                "不是神聖，但夠保守實用",
            ],
            "code_demo_heading": "CIE for loop 範例",
            "final_model_heading": "組成精簡模型",
            "final_model_lines": [
                "infected ~ shower_use + keepers",
                "只留真正會改變 RR 的變項",
                "從 15 變項 → 3~5 個",
                "CI 更窄、解讀更清晰",
                "→ 科學性變項選擇",
            ],
            "aic_heading": "AIC 輔助（點菜比喻）",
            "summary_heading": "CIE 三步驟",
            "summary_lines": [
                "① 最小模型 → 記暴露 RR",
                "② for loop 加候選、算 CIE",
                "③ >10% 留下組精簡模型",
                "→ AIC 輔助 = 完整流程",
            ],
            "extra_banner_title": "額外範例：肺結核接觸追蹤",
            "extra_tb_heading": "TB 接觸者研究",
            "extra_tb_lines": [
                "crude RR 3.5，候選 15 個",
                "CIE >10%：BCG、HIV、營養",
                "CIE <5%：年齡、性別、社經",
                "精簡 → adjusted RR 2.8",
                "→ 嚴謹分析可發 Lancet",
            ],
            "blindspot_banner_title": "CIE 地雷 3 選",
            "outro_heading": "恭喜完成 Ch06！",
            "outro_sub": "下一章 Ch07：時間序列與預測",
        },
        "en": {
            "title_main": "CIE Variable Selection",
            "title_sub": "Scientific screening with the 10% rule",
            "what_is_cie_heading": "CIE concept: watch how much RR moves",
            "what_is_cie_lines": [
                "① Run the minimal model: exposure only",
                "② Add each candidate → watch exposure RR shift",
                "③ Shift >10% → keep (true confounder)",
                "④ Shift <10% → drop",
                "This is the 10% rule",
            ],
            "why_10_heading": "Why pick 10%?",
            "why_10_lines": [
                "Epidemiology's empirical consensus",
                "<10% is usually random fluctuation",
                ">10% substantively changes the effect",
                "Not sacred, but conservative and practical",
            ],
            "code_demo_heading": "CIE for loop example",
            "final_model_heading": "Assemble the parsimonious model",
            "final_model_lines": [
                "infected ~ shower_use + keepers",
                "Keep only variables that truly change RR",
                "From 15 variables → 3~5",
                "Narrower CI, clearer interpretation",
                "→ Scientific variable selection",
            ],
            "aic_heading": "AIC as a complement (à la carte metaphor)",
            "summary_heading": "CIE Three Steps",
            "summary_lines": [
                "① Minimal model → record exposure RR",
                "② for loop adds candidates, compute CIE",
                "③ >10% keeps, assemble parsimonious model",
                "→ AIC as a complement = complete workflow",
            ],
            "extra_banner_title": "Extra example: TB contact tracing",
            "extra_tb_heading": "TB contact study",
            "extra_tb_lines": [
                "crude RR 3.5, 15 candidates",
                "CIE >10%: BCG, HIV, nutrition",
                "CIE <5%: age, sex, socioeconomic",
                "Parsimonious → adjusted RR 2.8",
                "→ Rigorous analysis worthy of the Lancet",
            ],
            "blindspot_banner_title": "3 CIE Pitfalls",
            "outro_heading": "Congrats on finishing Ch06!",
            "outro_sub": "Next chapter Ch07: time series and forecasting",
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
        panel = self.show_code(code, title="cie.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_what_is_cie(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            self.t("what_is_cie_heading"),
            self.t("what_is_cie_lines"),
            duration,
        )

    def show_why_10_percent(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            self.t("why_10_heading"),
            self.t("why_10_lines"),
            duration,
        )

    def show_code_demo(self, duration: float = 10.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block(self.t("code_demo_heading"), kwargs.get("code", ""), duration)

    def show_final_model(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            self.t("final_model_heading"),
            self.t("final_model_lines"),
            duration,
        )

    def show_aic_complement(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._code_block(self.t("aic_heading"), kwargs.get("code", ""), duration)

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            self.t("summary_heading"),
            self.t("summary_lines"),
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_tb(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets(
            self.t("extra_tb_heading"),
            self.t("extra_tb_lines"),
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

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
        h = Text(self.t("outro_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text(self.t("outro_sub"), font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
