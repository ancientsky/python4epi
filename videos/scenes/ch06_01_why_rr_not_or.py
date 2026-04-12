"""Ch06-01: Why cohort studies should use RR not OR"""

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


class Ch06WhyRrNotOrScene(EpiBaseScene):
    """Tutorial video scene: why cohort studies should report RR not OR."""

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
            panel = self.show_code(code, title="rr_vs_or.py", position=LEFT * 3 + UP * 0.2)
            self.wait(0.6)
            out = self.show_output(output, position=DOWN * 2.8)
            self.wait(max(0.1, duration - 2.0))
            self.play(FadeOut(VGroup(h, panel, out)), run_time=0.5)
        else:
            panel = self.show_code(code, title="rr_vs_or.py", position=ORIGIN + DOWN * 0.3)
            self.wait(max(0.1, duration - 1.4))
            self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card("為什麼世代研究用 RR 不用 OR", "侵襲率 43% 的真相", duration=duration)

    def show_definition(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            "RR vs OR 定義回顧",
            [
                "RR：暴露感染率 / 未暴露感染率（機率幾倍）",
                "OR：暴露勝算 / 未暴露勝算（勝算幾倍）",
                "odds = p / (1 - p)",
                "罕見時 OR ≈ RR；常見時 OR > RR",
                "關鍵字：罕見假設",
            ],
            duration,
        )

    def show_rare_assumption(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            "罕見疾病黃金法則",
            [
                "侵襲率 < 10% → (1-p) ≈ 1 → OR ≈ RR",
                "侵襲率 1%：OR 幾乎等於 RR",
                "侵襲率 10%：開始有感差異",
                "侵襲率 43%：OR 高估 1.5~3 倍",
            ],
            duration,
        )

    def show_numerical(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block("數字範例：RR=2 vs OR=3.5", kwargs.get("code", ""), duration, output=kwargs.get("output"))

    def show_three_routes(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            "多變項分析三條路",
            [
                "分層分析：一次控制 1 個 → MH RR",
                "Modified Poisson：多變項 → adjusted RR ✓",
                "邏輯斯迴歸：多變項 → adjusted OR（高估）",
                "世代研究首選 Modified Poisson",
            ],
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            "重點整理",
            [
                "RR 答「風險幾倍」、OR 答「勝算幾倍」",
                "只有罕見疾病時兩者近似",
                "侵襲率 43%：OR 系統性高估",
                "世代研究 → Modified Poisson adjusted RR",
            ],
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner("額外範例：HRT vs 心臟病案例"), duration=duration)

    def show_extra_hrt(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            "1990s HRT 觀察研究 vs 2002 WHI",
            [
                "觀察研究：HRT OR 0.6「降低心臟病 40%」",
                "2002 WHI RCT：HRT 反而↑心臟病",
                "原因 1：盛行率高，OR ≠ RR",
                "原因 2：healthy user bias",
                "→ 選錯效應測量 = 公衛災難",
            ],
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner("常見地雷 3 選"), duration=duration)

    def show_blindspot_misinterpret(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "print(f'Risk is {or_val}x higher')"),
            kwargs.get("correct_code", "print(f'Odds is {or_val}x higher')"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_logistic_only(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "smf.logit('infected ~ ...', data=df).fit()"),
            kwargs.get("correct_code", "smf.glm(..., family=Poisson()).fit(cov_type='HC0')"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_big_or(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "print(f'Huge effect: OR={or_val}!')"),
            kwargs.get("correct_code", "print(f'OR={or_val}, check attack rate first')"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text("下一集：logit 三階梯", font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text("機率、勝算、logit 完全打開", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
