"""Ch07-04: Poisson regression + lag for daily count prediction"""

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


class Ch07PoissonLagScene(EpiBaseScene):
    """Tutorial video scene: Poisson regression with lag features."""

    total_steps: int = 13

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "Poisson + lag",
            "title_sub": "IRR 解讀每日病例",
            "why_poisson_heading": "為什麼用 Poisson？",
            "why_poisson_points": [
                "每日病例 = 0, 1, 2, 3…（計數）",
                "線性迴歸會預測負數",
                "Poisson log link 保證非負",
                "exp(β) = IRR（發生率比）",
                "同數學殼，不同情境",
            ],
            "code_demo_heading": "smf.glm + Poisson + lag",
            "irr_interp_heading": "IRR 解讀表格",
            "vs_rolling_heading": "vs Rolling mean 升級點",
            "vs_rolling_points": [
                "① 有信賴區間（CI）",
                "② 可解讀（IRR 白話）",
                "③ 可放其他變項",
                "代價：至少 10 天資料",
                "護理之家 17 天剛好夠",
            ],
            "main_summary_heading": "三件事",
            "main_summary_points": [
                "① cases ~ lag_1 + lag_2 + day_idx",
                "② family=Poisson()，不用 HC0",
                "③ IRR = exp(β) 解讀效應",
            ],
            "extra_banner_title": "額外範例：急診症候群監測",
            "extra_ed_heading": "急診每小時發燒通報",
            "extra_ed_points": [
                "lag_1：上一小時",
                "lag_24：昨天同一小時",
                "lag_168：上週同一小時",
                "實際 > 95% CI → 警報",
                "→ Poisson + lag 的日常應用",
            ],
            "blindspot_banner_title": "Poisson+lag 地雷 3 選",
            "outro_heading": "下一集：Negative Binomial",
            "outro_sub": "過度離散的救星",
        },
        "en": {
            "title_main": "Poisson + lag",
            "title_sub": "Read daily cases with the IRR",
            "why_poisson_heading": "Why use Poisson?",
            "why_poisson_points": [
                "Daily cases = 0, 1, 2, 3… (counts)",
                "Linear regression can predict negatives",
                "Poisson's log link guarantees non-negative",
                "exp(β) = IRR (incidence rate ratio)",
                "Same math shell, different scenario",
            ],
            "code_demo_heading": "smf.glm + Poisson + lag",
            "irr_interp_heading": "Reading the IRR table",
            "vs_rolling_heading": "Upgrades over rolling mean",
            "vs_rolling_points": [
                "① has a confidence interval (CI)",
                "② interpretable (IRR in plain words)",
                "③ can add other variables",
                "Cost: at least 10 days of data",
                "The nursing home's 17 days is just enough",
            ],
            "main_summary_heading": "Three things",
            "main_summary_points": [
                "① cases ~ lag_1 + lag_2 + day_idx",
                "② family=Poisson(), no HC0 needed",
                "③ IRR = exp(β) to read the effect",
            ],
            "extra_banner_title": "Extra example: ER syndromic surveillance",
            "extra_ed_heading": "Hourly ER fever reports",
            "extra_ed_points": [
                "lag_1: the previous hour",
                "lag_24: same hour yesterday",
                "lag_168: same hour last week",
                "Actual > 95% CI → alert",
                "→ everyday use of Poisson + lag",
            ],
            "blindspot_banner_title": "3 Poisson+lag pitfalls",
            "outro_heading": "Next up: Negative Binomial",
            "outro_sub": "The savior of overdispersion",
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
        panel = self.show_code(code, title="poisson_lag.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_why_poisson_here(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            self.t("why_poisson_heading"),
            self.t("why_poisson_points"),
            duration,
        )

    def show_code_demo(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._code_block(self.t("code_demo_heading"), kwargs.get("code", ""), duration)

    def show_irr_interpretation(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block(self.t("irr_interp_heading"), kwargs.get("code", ""), duration)

    def show_vs_rolling(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            self.t("vs_rolling_heading"),
            self.t("vs_rolling_points"),
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            self.t("main_summary_heading"),
            self.t("main_summary_points"),
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_ed(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            self.t("extra_ed_heading"),
            self.t("extra_ed_points"),
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_irr_as_rr(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "print(f'RR = {np.exp(beta):.2f}')"),
            kwargs.get("correct_code", "print(f'IRR = {np.exp(beta):.2f}')"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_dispersion(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "# fit Poisson without checking"),
            kwargs.get("correct_code", "disp = var(y)/mean(y); if disp>1.5: use NB"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_round(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "int(pred)  # floor: 4.7 -> 4"),
            kwargs.get("correct_code", "round(pred)  # standard: 4.7 -> 5"),
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
