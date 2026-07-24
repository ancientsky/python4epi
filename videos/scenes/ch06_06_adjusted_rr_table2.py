"""Ch06-06: Multivariate adjusted RR and Table 2"""

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


class Ch06AdjustedRrTable2Scene(EpiBaseScene):
    """Tutorial video scene: multivariate adjusted RR & Table 2."""

    total_steps: int = 13

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "多變項 adjusted RR",
            "title_sub": "打造論文 Table 2",
            "why_multi_heading": "為什麼升級多變項？",
            "why_multi_lines": [
                "Ch05 分層：一次只控 1 個",
                ">3 個分層 → 樣本不夠",
                "多變項迴歸：一次控 10+ 個",
                "樣本大就能跑",
            ],
            "full_formula_heading": "完整公式：10 個變項一起",
            "table2_build_heading": "Table 2 組裝程式碼",
            "interpret_heading": "解讀重點",
            "interpret_lines": [
                "Intercept 跳過（無臨床意義）",
                "shower_use aRR 2.8 (1.5, 5.2), p=0.001",
                "控制其他因子後仍顯著",
                "→ 淋浴是真正的暴露源",
            ],
            "compare_three_heading": "三個效應測量比較",
            "compare_three_lines": [
                "Ch03 crude RR：無控制",
                "Ch05 MH RR：控 1 個變項",
                "Ch06 adj RR：控一打變項 ✓",
                "最可信 = 排除最多干擾",
            ],
            "summary_heading": "Table 2 四步驟",
            "summary_lines": [
                "① 完整公式列出調整因子",
                "② Modified Poisson + HC0",
                "③ exp params / conf_int / pvalues",
                "④ drop Intercept、focus 暴露",
            ],
            "extra_banner_title": "額外範例：AIDS 抗病毒藥",
            "extra_art_heading": "ART 抗病毒藥觀察研究",
            "extra_art_lines": [
                "crude RR 0.3（效果看起來很好）",
                "病人自選（confounding by indication）",
                "控 CD4 / viral load / 年齡…",
                "adjusted RR 升到 0.55",
                "→ 仍顯著，但沒有那麼誇張",
            ],
            "blindspot_banner_title": "Table 2 地雷 3 選",
            "outro_heading": "下一集：Forest Plot",
            "outro_sub": "Table 變成一張森林圖",
        },
        "en": {
            "title_main": "Multivariable adjusted RR",
            "title_sub": "Building a publication-ready Table 2",
            "why_multi_heading": "Why upgrade to multivariable?",
            "why_multi_lines": [
                "Ch05 stratification: control only 1 at a time",
                ">3 strata → not enough sample",
                "Multivariable regression: control 10+ at once",
                "Runs fine with a big enough sample",
            ],
            "full_formula_heading": "Full formula: 10 variables together",
            "table2_build_heading": "Table 2 assembly code",
            "interpret_heading": "Key points for interpretation",
            "interpret_lines": [
                "Skip Intercept (no clinical meaning)",
                "shower_use aRR 2.8 (1.5, 5.2), p=0.001",
                "Still significant after adjusting for others",
                "→ Showering is the true exposure source",
            ],
            "compare_three_heading": "Comparing three effect measures",
            "compare_three_lines": [
                "Ch03 crude RR: no control",
                "Ch05 MH RR: control 1 variable",
                "Ch06 adj RR: control a dozen variables ✓",
                "Most credible = removes the most confounding",
            ],
            "summary_heading": "Table 2 Four Steps",
            "summary_lines": [
                "① Full formula listing adjustment factors",
                "② Modified Poisson + HC0",
                "③ exp params / conf_int / pvalues",
                "④ drop Intercept, focus on the exposure",
            ],
            "extra_banner_title": "Extra example: AIDS antiretroviral drugs",
            "extra_art_heading": "ART antiretroviral observational study",
            "extra_art_lines": [
                "crude RR 0.3 (looks very effective)",
                "Patient self-selection (confounding by indication)",
                "Control CD4 / viral load / age...",
                "adjusted RR rises to 0.55",
                "→ Still significant, but not as extreme",
            ],
            "blindspot_banner_title": "3 Table 2 Pitfalls",
            "outro_heading": "Next up: the Forest Plot",
            "outro_sub": "Turn the table into a forest plot",
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
        panel = self.show_code(code, title="table2.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_why_multivariate(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            self.t("why_multi_heading"),
            self.t("why_multi_lines"),
            duration,
        )

    def show_full_formula(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._code_block(self.t("full_formula_heading"), kwargs.get("code", ""), duration)

    def show_table2_build(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block(self.t("table2_build_heading"), kwargs.get("code", ""), duration)

    def show_interpret_table2(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            self.t("interpret_heading"),
            self.t("interpret_lines"),
            duration,
        )

    def show_compare_three(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            self.t("compare_three_heading"),
            self.t("compare_three_lines"),
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

    def show_extra_art(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets(
            self.t("extra_art_heading"),
            self.t("extra_art_lines"),
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_keep_intercept(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "table2.to_csv('table2.csv')"),
            kwargs.get("correct_code", "table2.loc[1:].to_csv('table2.csv')"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_overfit(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "formula = 'y ~ ' + ' + '.join(30_variables)"),
            kwargs.get("correct_code", "formula = 'y ~ ' + ' + '.join(selected_by_cie)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_wrong_ref(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "C(floor)"),
            kwargs.get("correct_code", "C(floor, Treatment(reference=3))"),
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
