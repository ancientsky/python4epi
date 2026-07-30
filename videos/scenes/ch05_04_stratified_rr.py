"""Ch05-04: Stratified RR with for loop

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages.
"""

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


class Ch05StratifiedRrScene(EpiBaseScene):
    """Tutorial video scene: stratified RR with for loop."""

    total_steps: int = 14

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "分層分析",
            "title_sub": "每一層都算一次 RR",
            "crude_rr_heading": "Step 1：粗 RR 當基準",
            "loop_template_heading": "Step 2：for loop 骨架",
            "stratum_calc_heading": "Step 3：每層 2×2 表 + RR",
            "log_ci_heading": "Step 4：log 轉換法 95% CI",
            "results_heading": "Step 5：比對各層 vs 粗 RR",
            "results_code": "# 各層 RR vs Crude RR 對照",
            "summary_heading": "重點整理：分層分析四步驟",
            "summary_bullets": [
                "① 先算粗 RR 當基準",
                "② 按干擾因子 for loop 分層",
                "③ 每層算 RR + log-based CI",
                "④ 比較各層 RR 跟粗 RR",
            ],
            "extra_banner_title": "額外範例：H1N1 按醫院層級分層",
            "h1n1_heading": "H1N1 疫苗效力分層",
            "blindspot_banner_title": "for loop 分層常見地雷 3 選",
            "outro_heading": "下一集：森林圖視覺化",
            "outro_sub": "讓長官五秒看懂分層結果。",
        },
        "en": {
            "title_main": "Stratified Analysis",
            "title_sub": "One RR per stratum",
            "crude_rr_heading": "Step 1: crude RR as the baseline",
            "loop_template_heading": "Step 2: the for-loop skeleton",
            "stratum_calc_heading": "Step 3: per-stratum 2×2 table + RR",
            "log_ci_heading": "Step 4: 95% CI via the log transform",
            "results_heading": "Step 5: compare each stratum vs crude RR",
            "results_code": "# Stratum-specific RR vs crude RR",
            "summary_heading": "Recap: stratified analysis in four steps",
            "summary_bullets": [
                "① Compute crude RR as the baseline",
                "② for-loop over the confounder's strata",
                "③ Per-stratum RR + log-based CI",
                "④ Compare each stratum RR to the crude RR",
            ],
            "extra_banner_title": "Extra example: H1N1 stratified by hospital level",
            "h1n1_heading": "H1N1 vaccine effectiveness, stratified",
            "blindspot_banner_title": "3 Common for-Loop Stratifying Traps",
            "outro_heading": "Next up: the forest plot",
            "outro_sub": "Let the boss grasp the strata in five seconds.",
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
            panel = self.show_code(code, title="stratified.py", position=LEFT * 3 + UP * 0.2)
            self.wait(0.6)
            out = self.show_output(output, position=DOWN * 2.8)
            self.wait(max(0.1, duration - 2.0))
            self.play(FadeOut(VGroup(h, panel, out)), run_time=0.5)
        else:
            panel = self.show_code(code, title="stratified.py", position=ORIGIN + DOWN * 0.3)
            self.wait(max(0.1, duration - 1.4))
            self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_crude_rr(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._code_block(self.t("crude_rr_heading"), kwargs.get("code", ""), duration, output=kwargs.get("output"))

    def show_loop_template(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._code_block(self.t("loop_template_heading"), kwargs.get("code", ""), duration)

    def show_stratum_calc(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block(self.t("stratum_calc_heading"), kwargs.get("code", ""), duration)

    def show_log_ci(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._code_block(self.t("log_ci_heading"), kwargs.get("code", ""), duration)

    def show_results_output(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._code_block(
            self.t("results_heading"),
            self.t("results_code"),
            duration,
            output=kwargs.get("output"),
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            self.t("summary_heading"),
            self.t("summary_bullets"),
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_h1n1(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._code_block(self.t("h1n1_heading"), kwargs.get("code", ""), duration)

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_shape(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "a = ct_s.loc[1,1]  # KeyError if missing"),
            kwargs.get("correct_code", "if ct_s.shape != (2,2): continue"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_too_fine(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "strata = df['age'].unique()  # 60+ levels"),
            kwargs.get("correct_code", "strata = pd.cut(df['age'], bins=[59,69,79,89,120])"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_zero_cell(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "ln_rr = np.log(0/(a+b) / c/(c+d))  # -inf"),
            kwargs.get("correct_code", "a, b, c, d = [x + 0.5 for x in (a,b,c,d)]"),
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
