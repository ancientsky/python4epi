"""Ch07-05: Negative Binomial regression for overdispersion"""

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


class Ch07NegativeBinomialScene(EpiBaseScene):
    """Tutorial video scene: Negative Binomial regression."""

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
        panel = self.show_code(code, title="nb.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card("Negative Binomial", "過度離散的救星", duration=duration)

    def show_dispersion_explained(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            "過度離散白話版",
            [
                "Poisson 假設 variance = mean",
                "現實：2, 0, 15, 1, 20…",
                "variance 遠大於 mean = 過度離散",
                "原因：群聚、outbreak、通報延遲",
                "公衛資料天生會過度離散",
            ],
            duration,
        )

    def show_check_dispersion(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._code_block("dispersion = var / mean", kwargs.get("code", ""), duration)

    def show_nb_code(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block("NB GLM 程式碼", kwargs.get("code", ""), duration)

    def show_compare_mae_aic(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            "Poisson vs NB 比較",
            [
                "MAE：點估計誤差",
                "AIC：越小越好",
                "CI 寬度：NB 更誠實",
                "AIC 差 > 10 → 一定要換 NB",
            ],
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            "三步驟流程",
            [
                "① 算 dispersion = var/mean",
                "② >1.5 → NegativeBinomial",
                "③ 比 AIC 決定",
                "→ 別預設 Poisson",
            ],
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner("額外範例：登革熱每週通報"), duration=duration)

    def show_extra_dengue(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            "登革熱過度離散案例",
            [
                "10 週 0 例，突然爆 30 例",
                "variance ≈ mean × 10",
                "早年 Poisson：假警報頻繁",
                "改 NB 後假警報↓ 60%",
                "→ 過度離散的公衛意義",
            ],
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner("NB 地雷 3 選"), duration=duration)

    def show_blindspot_no_check(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "smf.glm(..., family=Poisson()).fit()"),
            kwargs.get("correct_code", "if var/mean>1.5: family=NegativeBinomial()"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_wrong_alpha(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "NegativeBinomial(alpha=0.01)"),
            kwargs.get("correct_code", "NegativeBinomial(alpha=1.0)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_zero_inflated(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "NegativeBinomial()  # 70% zeros"),
            kwargs.get("correct_code", "sm.ZeroInflatedNegativeBinomialP()"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text("下一集：Logistic threshold", font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text("是否警報二元預測", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
