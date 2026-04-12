"""Ch05-08: Case-Control Mantel-Haenszel (OR version)"""

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
        self.show_title_card("病例對照版 MH", "換個公式，邏輯一樣", duration=duration)

    def show_design_diff(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            "兩種研究設計的差異",
            [
                "世代研究：E → 追蹤 → D，算 RR",
                "病例對照：D → 回溯 → E，算 OR",
                "病例對照的侵襲率分母失真",
                "→ 只能算 OR，不能算 RR",
            ],
            duration,
        )

    def show_or_recap(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._code_block("OR 公式回顧", kwargs.get("code", ""), duration)

    def show_mh_or_formula(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets(
            "MH 合併 OR 公式",
            [
                "分子：Σᵢ  aᵢ × dᵢ / Nᵢ",
                "分母：Σᵢ  bᵢ × cᵢ / Nᵢ",
                "OR_MH = 分子 / 分母",
                "對比 RR 版：ad/N vs a(c+d)/N",
                "結構一樣，只是項目換了。",
            ],
            duration,
        )

    def show_mh_or_code(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._code_block("Python 實作", kwargs.get("code", ""), duration, output=kwargs.get("output"))

    def show_or_bias(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            "OR vs RR 的高估偏差",
            [
                "侵襲率 < 10%：OR ≈ RR 可互換",
                "侵襲率 43%（本案）：OR 明顯高估",
                "Ch06 Modified Poisson 可算 adjusted RR",
                "即使在高侵襲率情境也準確。",
            ],
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            "重點整理",
            [
                "世代研究 → MH RR",
                "病例對照 → MH OR",
                "分層邏輯完全一樣",
                "侵襲率低：OR ≈ RR；高：OR 高估",
            ],
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner("額外範例：台灣腸病毒 71 型 1998"), duration=duration)

    def show_extra_enterovirus(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._code_block("EV71 病例對照疫調", kwargs.get("code", ""), duration)

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner("病例對照分析常見地雷 3 選"), duration=duration)

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
        h = Text("恭喜完成 Ch05 分層分析！", font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text("下一章 Ch06：多變項迴歸，一次調整一打變數。", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
