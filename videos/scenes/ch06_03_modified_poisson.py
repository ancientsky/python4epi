"""Ch06-03: Modified Poisson regression for adjusted RR"""

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


class Ch06ModifiedPoissonScene(EpiBaseScene):
    """Tutorial video scene: Modified Poisson regression."""

    total_steps: int = 13

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "Modified Poisson 借帽子",
            "title_sub": "Zou 2004 的神奇魔法",
            "why_not_other_heading": "其他方法為什麼不夠好？",
            "why_not_other_lines": [
                "log-binomial：理論對、實務不收斂",
                "Cox：需要時間變項",
                "logistic：OR 在高侵襲率下高估",
                "→ Zou 2004：Poisson + HC0 借帽子",
            ],
            "poisson_original_heading": "Poisson 原本的用途",
            "poisson_original_lines": [
                "計數資料：一天來幾個病人",
                "假設 E(Y) = Var(Y)",
                "exp(β) = incidence rate ratio",
                "對 0/1 感染資料，exp(β) ≈ RR",
            ],
            "borrow_hat_heading": "「借帽子 + 修正貼紙」比喻",
            "borrow_hat_lines": [
                "直接借：SE 被吹脹、CI 太寬",
                "修正：用 robust sandwich SE (HC0)",
                "覆蓋 Poisson 原 SE → Modified",
                "像頭圍不合，墊衛生紙填滿",
            ],
            "code_demo_heading": "smf.glm + Poisson + HC0",
            "exp_ci_heading": "輸出解讀三招",
            "exp_ci_lines": [
                "np.exp(params) → adjusted RR",
                "np.exp(conf_int()) → 95% CI",
                "pvalues → p 值（不用 exp）",
                "三招一組 = 完整 Table 2",
            ],
            "summary_heading": "三件事記起來",
            "summary_lines": [
                "世代研究首選 Modified Poisson",
                "family=Poisson() + cov_type='HC0'",
                "結果 np.exp 還原才是 RR",
                "一行公式取代 logistic",
            ],
            "extra_banner_title": "額外範例：台南 2015 登革熱",
            "extra_dengue_heading": "登革熱高侵襲率情境",
            "extra_dengue_lines": [
                "某里侵襲率達 20%",
                "logistic：OR 3.5（高估）",
                "Modified Poisson：adjusted RR 2.3",
                "差 50% → 決策完全不同",
                "→ 高侵襲率必用 Modified Poisson",
            ],
            "blindspot_banner_title": "Modified Poisson 地雷 3 選",
            "outro_heading": "下一集：公式語法",
            "outro_sub": "~、+、C() 完全解析",
        },
        "en": {
            "title_main": "Modified Poisson: Borrowing a Hat",
            "title_sub": "The clever magic of Zou 2004",
            "why_not_other_heading": "Why aren't the other methods good enough?",
            "why_not_other_lines": [
                "log-binomial: theory right, often won't converge",
                "Cox: needs a time variable",
                "logistic: OR inflates at high attack rates",
                "→ Zou 2004: Poisson + HC0, borrow a hat",
            ],
            "poisson_original_heading": "Poisson's original purpose",
            "poisson_original_lines": [
                "Count data: how many patients arrive in a day",
                "Assumes E(Y) = Var(Y)",
                "exp(β) = incidence rate ratio",
                "For 0/1 infection data, exp(β) ≈ RR",
            ],
            "borrow_hat_heading": 'The "borrow a hat + patch sticker" metaphor',
            "borrow_hat_lines": [
                "Borrow directly: SE inflated, CI too wide",
                "Fix: use a robust sandwich SE (HC0)",
                "Override Poisson's SE → Modified",
                "Like a hat that won't fit, stuff tissue to fill it",
            ],
            "code_demo_heading": "smf.glm + Poisson + HC0",
            "exp_ci_heading": "Three moves to read the output",
            "exp_ci_lines": [
                "np.exp(params) → adjusted RR",
                "np.exp(conf_int()) → 95% CI",
                "pvalues → p-values (no exp)",
                "All three together = a complete Table 2",
            ],
            "summary_heading": "Three Things to Remember",
            "summary_lines": [
                "Cohort study's top pick: Modified Poisson",
                "family=Poisson() + cov_type='HC0'",
                "exp the result to restore the RR",
                "One formula line replaces logistic",
            ],
            "extra_banner_title": "Extra example: Tainan 2015 dengue",
            "extra_dengue_heading": "Dengue high-attack-rate scenario",
            "extra_dengue_lines": [
                "One village hit a 20% attack rate",
                "logistic: OR 3.5 (inflated)",
                "Modified Poisson: adjusted RR 2.3",
                "50% apart → totally different decisions",
                "→ High attack rate demands Modified Poisson",
            ],
            "blindspot_banner_title": "3 Modified Poisson Pitfalls",
            "outro_heading": "Next up: formula syntax",
            "outro_sub": "~, +, C() fully explained",
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
        panel = self.show_code(code, title="mod_poisson.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_why_not_other(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            self.t("why_not_other_heading"),
            self.t("why_not_other_lines"),
            duration,
        )

    def show_poisson_original(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            self.t("poisson_original_heading"),
            self.t("poisson_original_lines"),
            duration,
        )

    def show_borrow_hat(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets(
            self.t("borrow_hat_heading"),
            self.t("borrow_hat_lines"),
            duration,
        )

    def show_code_demo(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._code_block(self.t("code_demo_heading"), kwargs.get("code", ""), duration)

    def show_exp_and_ci(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            self.t("exp_ci_heading"),
            self.t("exp_ci_lines"),
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            self.t("summary_heading"),
            self.t("summary_lines"),
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_dengue(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets(
            self.t("extra_dengue_heading"),
            self.t("extra_dengue_lines"),
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_no_hc0(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "model.fit()"),
            kwargs.get("correct_code", "model.fit(cov_type='HC0')"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_exp(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "rr = model.params"),
            kwargs.get("correct_code", "rr = np.exp(model.params)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_wrong_family(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "family=sm.families.Binomial()"),
            kwargs.get("correct_code", "family=sm.families.Poisson()"),
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
