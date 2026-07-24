"""Ch06-02: Logit intuition - probability, odds, logit three ladders"""

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


class Ch06LogitIntuitionScene(EpiBaseScene):
    """Tutorial video scene: logit intuition three-step ladder."""

    total_steps: int = 13

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "邏輯斯迴歸三階梯",
            "title_sub": "機率、勝算、logit",
            "why_not_linear_heading": "為什麼不用普通線性迴歸？",
            "why_not_linear_lines": [
                "0/1 資料：線性會跑出 <0 或 >1 的機率",
                "解法：機率 → 勝算 → log(勝算)",
                "log(勝算) 範圍 (-∞, +∞)，可線性組合",
                "→ logistic regression 的誕生",
            ],
            "step1_heading": "第一階：機率 p",
            "step1_lines": [
                "範圍 [0, 1]（卡住的彈簧）",
                "p = 0.7 → 70% 感染",
                "是我們真正想要的數字",
                "但不能直接拿來線性迴歸",
            ],
            "step2_heading": "第二階：odds = p / (1-p)",
            "step3_heading": "第三階：logit = log(odds)",
            "beta_heading": "β 的解讀：exp(β) = OR",
            "beta_lines": [
                "β 是 log odds scale 的效應",
                "β = 1.2 → exp(1.2) = 3.32",
                "OR = 3.32：勝算是對照組 3.32 倍",
                "鐵三角：exp、beta、OR",
            ],
            "summary_heading": "三階梯總結",
            "summary_lines": [
                "機率 p：[0, 1]，被卡住",
                "odds：[0, ∞)，半開",
                "logit：(-∞, +∞)，全自由",
                "→ 線性組合 + sigmoid 還原",
            ],
            "extra_banner_title": "額外範例：COVID 疫苗住院研究",
            "extra_covid_heading": "COVID 疫苗 logistic 結果",
            "extra_covid_lines": [
                "β = -2.1 → exp(-2.1) = 0.12",
                "OR = 0.12（接種者勝算只有 12%）",
                "住院率低（~5%），OR ≈ RR",
                "可說：降低住院風險 88%",
            ],
            "blindspot_banner_title": "logit 常見地雷 3 選",
            "outro_heading": "下一集：Modified Poisson",
            "outro_sub": "借帽子算 RR 的魔法",
        },
        "en": {
            "title_main": "The Logistic Regression Three-Step Ladder",
            "title_sub": "Probability, odds, logit",
            "why_not_linear_heading": "Why not ordinary linear regression?",
            "why_not_linear_lines": [
                "0/1 data: linear predicts probabilities <0 or >1",
                "Fix: probability → odds → log(odds)",
                "log(odds) spans (-∞, +∞), linearly combinable",
                "→ the birth of logistic regression",
            ],
            "step1_heading": "Step 1: probability p",
            "step1_lines": [
                "Range [0, 1] (a jammed spring)",
                "p = 0.7 → 70% infected",
                "The number we actually want",
                "But you can't feed it straight to linear regression",
            ],
            "step2_heading": "Step 2: odds = p / (1-p)",
            "step3_heading": "Step 3: logit = log(odds)",
            "beta_heading": "Reading β: exp(β) = OR",
            "beta_lines": [
                "β is the effect on the log-odds scale",
                "β = 1.2 → exp(1.2) = 3.32",
                "OR = 3.32: odds are 3.32x the reference group",
                "The iron triangle: exp, beta, OR",
            ],
            "summary_heading": "The Three-Step Ladder Recap",
            "summary_lines": [
                "Probability p: [0, 1], jammed",
                "odds: [0, ∞), half-open",
                "logit: (-∞, +∞), fully free",
                "→ linear combination + sigmoid to restore",
            ],
            "extra_banner_title": "Extra example: COVID vaccine hospitalization study",
            "extra_covid_heading": "COVID vaccine logistic result",
            "extra_covid_lines": [
                "β = -2.1 → exp(-2.1) = 0.12",
                "OR = 0.12 (vaccinated odds only 12%)",
                "Low hospitalization rate (~5%), OR ≈ RR",
                "You can say: 88% lower hospitalization risk",
            ],
            "blindspot_banner_title": "3 Common Logit Pitfalls",
            "outro_heading": "Next up: Modified Poisson",
            "outro_sub": "The magic of borrowing a hat to compute RR",
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
            panel = self.show_code(code, title="logit.py", position=LEFT * 3 + UP * 0.2)
            self.wait(0.6)
            out = self.show_output(output, position=DOWN * 2.8)
            self.wait(max(0.1, duration - 2.0))
            self.play(FadeOut(VGroup(h, panel, out)), run_time=0.5)
        else:
            panel = self.show_code(code, title="logit.py", position=ORIGIN + DOWN * 0.3)
            self.wait(max(0.1, duration - 1.4))
            self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_why_not_linear(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            self.t("why_not_linear_heading"),
            self.t("why_not_linear_lines"),
            duration,
        )

    def show_step1_probability(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            self.t("step1_heading"),
            self.t("step1_lines"),
            duration,
        )

    def show_step2_odds(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block(self.t("step2_heading"), kwargs.get("code", ""), duration, output=kwargs.get("output"))

    def show_step3_logit(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._code_block(self.t("step3_heading"), kwargs.get("code", ""), duration, output=kwargs.get("output"))

    def show_beta_interpretation(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            self.t("beta_heading"),
            self.t("beta_lines"),
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

    def show_extra_covid(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets(
            self.t("extra_covid_heading"),
            self.t("extra_covid_lines"),
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_beta_raw(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "print(f'effect = {beta:.2f}')"),
            kwargs.get("correct_code", "print(f'OR = {np.exp(beta):.2f}')"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_logit_as_prob(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "prob = logit_value"),
            kwargs.get("correct_code", "prob = 1 / (1 + np.exp(-logit_value))"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_extreme_p(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "logit = np.log(p / (1 - p))"),
            kwargs.get("correct_code", "p = np.clip(p, 1e-6, 1 - 1e-6); logit = np.log(p/(1-p))"),
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
