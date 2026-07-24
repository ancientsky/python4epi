"""Ch05-08: Case-Control Mantel-Haenszel (OR version)

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages.
"""

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


class Ch05CaseControlMhScene(EpiBaseScene):
    """Tutorial video scene: case-control MH weighted OR."""

    total_steps: int = 13

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "病例對照版 MH",
            "title_sub": "換個公式，邏輯一樣",
            "design_heading": "兩種研究設計的差異",
            "design_bullets": [
                "世代研究：E → 追蹤 → D，算 RR",
                "病例對照：D → 回溯 → E，算 OR",
                "病例對照的侵襲率分母失真",
                "→ 只能算 OR，不能算 RR",
            ],
            "or_recap_heading": "OR 公式回顧",
            "formula_heading": "MH 合併 OR 公式",
            "formula_bullets": [
                "分子：Σᵢ  aᵢ × dᵢ / Nᵢ",
                "分母：Σᵢ  bᵢ × cᵢ / Nᵢ",
                "OR_MH = 分子 / 分母",
                "對比 RR 版：ad/N vs a(c+d)/N",
                "結構一樣，只是項目換了。",
            ],
            "code_heading": "Python 實作",
            "or_bias_heading": "OR vs RR 的高估偏差",
            "or_bias_bullets": [
                "侵襲率 < 10%：OR ≈ RR 可互換",
                "侵襲率 43%（本案）：OR 明顯高估",
                "Ch06 Modified Poisson 可算 adjusted RR",
                "即使在高侵襲率情境也準確。",
            ],
            "summary_heading": "重點整理",
            "summary_bullets": [
                "世代研究 → MH RR",
                "病例對照 → MH OR",
                "分層邏輯完全一樣",
                "侵襲率低：OR ≈ RR；高：OR 高估",
            ],
            "extra_banner_title": "額外範例：台灣腸病毒 71 型 1998",
            "enterovirus_heading": "EV71 病例對照疫調",
            "blindspot_banner_title": "病例對照分析常見地雷 3 選",
            "outro_heading": "恭喜完成 Ch05 分層分析！",
            "outro_sub": "下一章 Ch06：多變項迴歸，一次調整一打變數。",
        },
        "en": {
            "title_main": "Case-Control Mantel-Haenszel",
            "title_sub": "Swap the formula, keep the logic",
            "design_heading": "The difference between the two study designs",
            "design_bullets": [
                "Cohort: E → follow-up → D, compute RR",
                "Case-control: D → traceback → E, compute OR",
                "Case-control distorts the attack-rate denominator",
                "→ Can only compute OR, not RR",
            ],
            "or_recap_heading": "The OR formula, revisited",
            "formula_heading": "The MH pooled-OR formula",
            "formula_bullets": [
                "Numerator: Σᵢ  aᵢ × dᵢ / Nᵢ",
                "Denominator: Σᵢ  bᵢ × cᵢ / Nᵢ",
                "OR_MH = numerator / denominator",
                "Compare RR version: ad/N vs a(c+d)/N",
                "Same structure, just different terms.",
            ],
            "code_heading": "Python implementation",
            "or_bias_heading": "OR-over-RR overestimation bias",
            "or_bias_bullets": [
                "Attack rate < 10%: OR ≈ RR, interchangeable",
                "Attack rate 43% (this case): OR clearly overestimates",
                "Ch06's Modified Poisson gives an adjusted RR",
                "Accurate even at high attack rates.",
            ],
            "summary_heading": "Recap",
            "summary_bullets": [
                "Cohort → MH RR",
                "Case-control → MH OR",
                "The stratifying logic is identical",
                "Low attack rate: OR ≈ RR; high: OR overestimates",
            ],
            "extra_banner_title": "Extra example: Taiwan's 1998 enterovirus 71 outbreak",
            "enterovirus_heading": "The EV71 case-control investigation",
            "blindspot_banner_title": "3 Common Case-Control Traps",
            "outro_heading": "Congrats on finishing Ch05: stratified analysis!",
            "outro_sub": "Next chapter, Ch06: multivariable regression — adjust a dozen variables at once.",
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

    def _code_block(self, heading: str, code: str, duration: float, output: str | None = None) -> None:
        h = Text(heading, font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).to_edge(UP, buff=0.5)
        self.play(FadeIn(h), run_time=0.4)
        if output:
            panel = self.show_code(code, title="mh_or.py", position=LEFT * 3 + UP * 0.2)
            self.wait(0.6)
            out = self.show_output(output, position=DOWN * 2.8)
            self.wait(max(0.1, duration - 2.0))
            self.play(FadeOut(VGroup(h, panel, out)), run_time=0.5)
        else:
            panel = self.show_code(code, title="mh_or.py", position=ORIGIN + DOWN * 0.3)
            self.wait(max(0.1, duration - 1.4))
            self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_design_diff(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            self.t("design_heading"),
            self.t("design_bullets"),
            duration,
        )

    def show_or_recap(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._code_block(self.t("or_recap_heading"), kwargs.get("code", ""), duration)

    def show_mh_or_formula(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets(
            self.t("formula_heading"),
            self.t("formula_bullets"),
            duration,
        )

    def show_mh_or_code(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._code_block(self.t("code_heading"), kwargs.get("code", ""), duration, output=kwargs.get("output"))

    def show_or_bias(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            self.t("or_bias_heading"),
            self.t("or_bias_bullets"),
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            self.t("summary_heading"),
            self.t("summary_bullets"),
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_enterovirus(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._code_block(self.t("enterovirus_heading"), kwargs.get("code", ""), duration)

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_wrong_metric(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "rr = (a/(a+b)) / (c/(c+d))  # case-control!"),
            kwargs.get("correct_code", "or_val = (a * d) / (b * c)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_rare_disease(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "print(f'OR approx RR = {or_val:.2f}')"),
            kwargs.get("correct_code", "print(f'OR = {or_val:.2f} (attack rate 43%)')"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_control_select(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "controls = hospital_other_ward_patients"),
            kwargs.get("correct_code", "controls = same_source_population_healthy"),
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
