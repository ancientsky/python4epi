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

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "公式語法完全解析",
            "title_sub": "波浪、加號、C() 三符號",
            "tilde_heading": "符號 1：波浪號 ~ = 「被預測」",
            "tilde_lines": [
                "左 = Y（結果變項）",
                "右 = X（預測變項）",
                "infected ~ age",
                "= 用 age 預測 infected",
                "不是等號！",
            ],
            "plus_heading": "符號 2：加號 + = 「同時納入」",
            "plus_lines": [
                "不是數學加法",
                "~ age + sex + floor",
                "= 3 個變項各自算一個 β",
                "不會算 age + sex 的值",
            ],
            "c_symbol_heading": "符號 3：C() = 「當類別變項」",
            "full_example_heading": "完整公式範例",
            "full_example_lines": [
                "infected ~ shower_use + age + C(floor)",
                "= 用 shower_use (0/1)",
                "  + age（連續）",
                "  + floor（類別，auto one-hot）",
                "  預測 infected",
            ],
            "summary_heading": "三符號懶人包",
            "summary_lines": [
                "~ = 被預測",
                "+ = 同時納入",
                "C() = 當類別",
                "進階：*（交互）、-1（去截距）",
            ],
            "extra_banner_title": "額外範例：流感住院研究",
            "extra_flu_heading": "流感住院公式範例",
            "extra_flu_lines": [
                "hospitalized ~ vaccinated",
                "  + C(age_group) + sex",
                "age_group 是字串 → auto one-hot",
                "連續 age 要不要 C？看轉折點",
                "流病常 bin + C（更靈活）",
            ],
            "blindspot_banner_title": "公式語法地雷 3 選",
            "outro_heading": "下一集：單變項 for loop",
            "outro_sub": "RR vs OR 一次對比完",
        },
        "en": {
            "title_main": "Formula Syntax Fully Explained",
            "title_sub": "Three symbols: tilde, plus, C()",
            "tilde_heading": 'Symbol 1: the tilde ~ = "is predicted by"',
            "tilde_lines": [
                "Left = Y (outcome variable)",
                "Right = X (predictor variables)",
                "infected ~ age",
                "= use age to predict infected",
                "It is not an equals sign!",
            ],
            "plus_heading": 'Symbol 2: the plus + = "include together"',
            "plus_lines": [
                "It is not mathematical addition",
                "~ age + sex + floor",
                "= each of 3 variables gets its own β",
                "It does not compute age + sex",
            ],
            "c_symbol_heading": 'Symbol 3: C() = "treat as categorical"',
            "full_example_heading": "A complete formula example",
            "full_example_lines": [
                "infected ~ shower_use + age + C(floor)",
                "= use shower_use (0/1)",
                "  + age (continuous)",
                "  + floor (categorical, auto one-hot)",
                "  to predict infected",
            ],
            "summary_heading": "Three-Symbol Cheat Sheet",
            "summary_lines": [
                "~ = is predicted by",
                "+ = include together",
                "C() = treat as categorical",
                "Advanced: * (interaction), -1 (drop intercept)",
            ],
            "extra_banner_title": "Extra example: flu hospitalization study",
            "extra_flu_heading": "Flu hospitalization formula example",
            "extra_flu_lines": [
                "hospitalized ~ vaccinated",
                "  + C(age_group) + sex",
                "age_group is a string → auto one-hot",
                "Should continuous age get C? Watch for a kink",
                "Epi often bins + C (more flexible)",
            ],
            "blindspot_banner_title": "3 Formula Syntax Pitfalls",
            "outro_heading": "Next up: the univariate for loop",
            "outro_sub": "RR vs OR compared in one pass",
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
        panel = self.show_code(code, title="formula.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_tilde(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            self.t("tilde_heading"),
            self.t("tilde_lines"),
            duration,
        )

    def show_plus(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            self.t("plus_heading"),
            self.t("plus_lines"),
            duration,
        )

    def show_c_symbol(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block(self.t("c_symbol_heading"), kwargs.get("code", ""), duration)

    def show_full_example(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            self.t("full_example_heading"),
            self.t("full_example_lines"),
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            self.t("summary_heading"),
            self.t("summary_lines"),
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_flu(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            self.t("extra_flu_heading"),
            self.t("extra_flu_lines"),
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

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
        h = Text(self.t("outro_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text(self.t("outro_sub"), font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
