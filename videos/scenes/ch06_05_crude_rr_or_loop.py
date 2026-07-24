"""Ch06-05: Crude RR vs OR with for loop"""

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


class Ch06CrudeRrOrLoopScene(EpiBaseScene):
    """Tutorial video scene: univariate RR vs OR loop."""

    total_steps: int = 13

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "單變項 crude RR vs OR",
            "title_sub": "for loop 並排比較",
            "why_loop_heading": "為什麼要用 for loop？",
            "why_loop_lines": [
                "候選變項 10+ 個",
                "手動跑一個個打太累",
                "Python 迴圈：一次跑完",
                "統一排成 DataFrame，對齊乾淨",
            ],
            "code_demo_heading": "雙模型 loop 範例",
            "interpret_heading": "解讀對照輸出",
            "interpret_lines": [
                "shower_use：RR 3.2, OR 8.5",
                "同一筆資料、結論完全不同",
                "RR：「風險 3.2 倍」",
                "OR：「勝算 8.5 倍」",
                "→ 43% 侵襲率 OR 高估實錄",
            ],
            "ci_pvalue_heading": "CI 和 p 值一次收齊",
            "ci_pvalue_lines": [
                "CI：conf_int() → np.exp() 整組",
                "p 值：pvalues（不用 exp）",
                "完整一列：var, RR (CI), p, OR (CI)",
                "直接變成 Table 1",
            ],
            "summary_heading": "四步驟收斂",
            "summary_lines": [
                "① 列出候選變項清單",
                "② for loop 跑 Modified Poisson",
                "③ 同 loop 跑 logit 對照",
                "④ append → DataFrame → Table 1",
            ],
            "extra_banner_title": "額外範例：COVID 長者住院風險",
            "extra_covid_heading": "COVID 住院風險 loop 結果",
            "extra_covid_lines": [
                "疫苗 RR 0.40、OR 0.35（差不多）",
                "原因：住院率僅 5%，OR ≈ RR",
                "65+ RR 4.5、OR 12（差很多）",
                "原因：老人住院率高，OR 高估",
                "→ 高發生率族群必用 RR",
            ],
            "blindspot_banner_title": "for loop 地雷 3 選",
            "outro_heading": "下一集：多變項 Table 2",
            "outro_sub": "一次調整一打變數",
        },
        "en": {
            "title_main": "Univariate crude RR vs OR",
            "title_sub": "Side-by-side with a for loop",
            "why_loop_heading": "Why use a for loop?",
            "why_loop_lines": [
                "10+ candidate variables",
                "Typing them out one by one is exhausting",
                "Python loop: run them all in one pass",
                "Line up as one DataFrame, clean alignment",
            ],
            "code_demo_heading": "Two-model loop example",
            "interpret_heading": "Reading the comparison output",
            "interpret_lines": [
                "shower_use: RR 3.2, OR 8.5",
                "Same data, completely different conclusions",
                'RR: "3.2x the risk"',
                'OR: "8.5x the odds"',
                "→ OR inflation at 43% attack rate, on record",
            ],
            "ci_pvalue_heading": "CI and p-values in one go",
            "ci_pvalue_lines": [
                "CI: conf_int() → np.exp() the whole set",
                "p-values: pvalues (no exp)",
                "Full row: var, RR (CI), p, OR (CI)",
                "Becomes Table 1 directly",
            ],
            "summary_heading": "Four Steps to Wrap Up",
            "summary_lines": [
                "① List the candidate variables",
                "② for loop runs Modified Poisson",
                "③ Same loop runs logit for comparison",
                "④ append → DataFrame → Table 1",
            ],
            "extra_banner_title": "Extra example: COVID elderly hospitalization risk",
            "extra_covid_heading": "COVID hospitalization-risk loop result",
            "extra_covid_lines": [
                "Vaccine RR 0.40, OR 0.35 (about the same)",
                "Reason: hospitalization only 5%, OR ≈ RR",
                "65+ RR 4.5, OR 12 (very different)",
                "Reason: elderly hospitalization high, OR inflates",
                "→ High-incidence groups must use RR",
            ],
            "blindspot_banner_title": "3 for-loop Pitfalls",
            "outro_heading": "Next up: multivariable Table 2",
            "outro_sub": "Adjust a dozen variables at once",
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
        panel = self.show_code(code, title="crude_loop.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_why_loop(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            self.t("why_loop_heading"),
            self.t("why_loop_lines"),
            duration,
        )

    def show_code_demo(self, duration: float = 10.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._code_block(self.t("code_demo_heading"), kwargs.get("code", ""), duration)

    def show_interpret_output(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets(
            self.t("interpret_heading"),
            self.t("interpret_lines"),
            duration,
        )

    def show_ci_pvalue(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            self.t("ci_pvalue_heading"),
            self.t("ci_pvalue_lines"),
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

    def show_extra_covid(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            self.t("extra_covid_heading"),
            self.t("extra_covid_lines"),
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_only_logit(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "for var in vars: smf.logit(f'y~{var}', df).fit()"),
            kwargs.get("correct_code", "for var in vars: run_both_poisson_and_logit(var, df)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_hc0_loop(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "smf.glm(...).fit()"),
            kwargs.get("correct_code", "smf.glm(...).fit(cov_type='HC0')"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_wrong_index(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "rr = np.exp(model.params.iloc[0])"),
            kwargs.get("correct_code", "rr = np.exp(model.params.iloc[1])"),
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
