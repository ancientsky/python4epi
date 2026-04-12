"""Ch06-04: statsmodels formula syntax"""

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


class Ch06FormulaSyntaxScene(EpiBaseScene):
    """Tutorial video scene: statsmodels formula syntax."""

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
        panel = self.show_code(code, title="formula.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card("公式語法完全解析", "波浪、加號、C() 三符號", duration=duration)

    def show_tilde(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            "符號 1：波浪號 ~ = 「被預測」",
            [
                "左 = Y（結果變項）",
                "右 = X（預測變項）",
                "infected ~ age",
                "= 用 age 預測 infected",
                "不是等號！",
            ],
            duration,
        )

    def show_plus(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            "符號 2：加號 + = 「同時納入」",
            [
                "不是數學加法",
                "~ age + sex + floor",
                "= 3 個變項各自算一個 β",
                "不會算 age + sex 的值",
            ],
            duration,
        )

    def show_c_symbol(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block("符號 3：C() = 「當類別變項」", kwargs.get("code", ""), duration)

    def show_full_example(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            "完整公式範例",
            [
                "infected ~ shower_use + age + C(floor)",
                "= 用 shower_use (0/1)",
                "  + age（連續）",
                "  + floor（類別，auto one-hot）",
                "  預測 infected",
            ],
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            "三符號懶人包",
            [
                "~ = 被預測",
                "+ = 同時納入",
                "C() = 當類別",
                "進階：*（交互）、-1（去截距）",
            ],
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner("額外範例：流感住院研究"), duration=duration)

    def show_extra_flu(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            "流感住院公式範例",
            [
                "hospitalized ~ vaccinated",
                "  + C(age_group) + sex",
                "age_group 是字串 → auto one-hot",
                "連續 age 要不要 C？看轉折點",
                "流病常 bin + C（更靈活）",
            ],
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner("公式語法地雷 3 選"), duration=duration)

    def show_blindspot_equals(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "smf.glm('infected = age', ...)"),
            kwargs.get("correct_code", "smf.glm('infected ~ age', ...)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_c(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "smf.glm('infected ~ floor', ...)"),
            kwargs.get("correct_code", "smf.glm('infected ~ C(floor)', ...)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_plus_math(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "smf.glm('y ~ age + age**2', ...)"),
            kwargs.get("correct_code", "smf.glm('y ~ age + I(age**2)', ...)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text("下一集：單變項 for loop", font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text("RR vs OR 一次對比完", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
