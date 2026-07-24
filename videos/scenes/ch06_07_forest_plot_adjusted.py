"""Ch06-07: Forest plot for adjusted RR"""

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


class Ch06ForestPlotAdjustedScene(EpiBaseScene):
    """Tutorial video scene: adjusted RR forest plot."""

    total_steps: int = 13

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "Adjusted RR 森林圖",
            "title_sub": "一眼看穿危險因子",
            "what_to_plot_heading": "森林圖要畫什麼？",
            "what_to_plot_lines": [
                "Y 軸：每列一個變項",
                "X 軸：RR（log scale）",
                "點 = aRR、橫線 = 95% CI",
                "中線：RR = 1 虛線參考",
                "點壓 1 = 不顯著",
            ],
            "why_log_heading": "為什麼 X 軸用 log？",
            "why_log_lines": [
                "RR 是乘法效應",
                "RR = 0.5 跟 2 是同強度",
                "線性軸 → 左擠右拉、失衡",
                "log 尺度 → 左右對稱",
                "流病 forest 一律 xscale log",
            ],
            "code_demo_heading": "matplotlib errorbar 骨架",
            "interpret_heading": "看圖三招",
            "interpret_lines": [
                "① 壓 1 虛線的 → 不顯著",
                "② 全在右 + 不碰 1 → 危險因子",
                "③ 全在左 + 不碰 1 → 保護因子",
                "一張圖 → 優先順序一清二楚",
            ],
            "summary_heading": "森林圖五件事",
            "summary_lines": [
                "Y 變項、X RR（log）",
                "點 = aRR、線 = CI",
                "RR=1 虛線",
                "點深色、CI 淺色",
                "壓 1 不顯著、遠離顯著",
            ],
            "extra_banner_title": "額外範例：Meta-analysis",
            "extra_meta_heading": "Meta-analysis 森林圖",
            "extra_meta_lines": [
                "每列一個研究（不是變項）",
                "最下一列：合併菱形",
                "random-effects model",
                "讀法完全一樣",
                "舉一反三 → 所有效應量都能看",
            ],
            "blindspot_banner_title": "Forest plot 地雷 3 選",
            "outro_heading": "下一集：change-in-estimate",
            "outro_sub": "10% 法則挑對的變項",
        },
        "en": {
            "title_main": "Adjusted RR Forest Plot",
            "title_sub": "See the risk factors at a glance",
            "what_to_plot_heading": "What does a forest plot show?",
            "what_to_plot_lines": [
                "Y axis: one variable per row",
                "X axis: RR (log scale)",
                "Dot = aRR, bar = 95% CI",
                "Center line: RR = 1 dashed reference",
                "Dot touching 1 = not significant",
            ],
            "why_log_heading": "Why a log X axis?",
            "why_log_lines": [
                "RR is a multiplicative effect",
                "RR = 0.5 and 2 are equal strength",
                "Linear axis → squished left, stretched right",
                "Log scale → left-right symmetric",
                "Epi forests always use xscale log",
            ],
            "code_demo_heading": "matplotlib errorbar skeleton",
            "interpret_heading": "Three moves to read the plot",
            "interpret_lines": [
                "① Touching the 1 line → not significant",
                "② All right + clear of 1 → risk factor",
                "③ All left + clear of 1 → protective factor",
                "One plot → priorities crystal clear",
            ],
            "summary_heading": "Five Things About Forest Plots",
            "summary_lines": [
                "Y variable, X RR (log)",
                "Dot = aRR, bar = CI",
                "RR=1 dashed line",
                "Dot dark, CI light",
                "Touch 1 not significant, far away significant",
            ],
            "extra_banner_title": "Extra example: Meta-analysis",
            "extra_meta_heading": "Meta-analysis forest plot",
            "extra_meta_lines": [
                "One study per row (not a variable)",
                "Bottom row: the pooled diamond",
                "random-effects model",
                "Read it exactly the same way",
                "Generalize → every effect size is readable",
            ],
            "blindspot_banner_title": "3 Forest Plot Pitfalls",
            "outro_heading": "Next up: change-in-estimate",
            "outro_sub": "The 10% rule picks the right variables",
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
        panel = self.show_code(code, title="forest.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_what_to_plot(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            self.t("what_to_plot_heading"),
            self.t("what_to_plot_lines"),
            duration,
        )

    def show_why_log_x(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            self.t("why_log_heading"),
            self.t("why_log_lines"),
            duration,
        )

    def show_code_demo(self, duration: float = 10.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block(self.t("code_demo_heading"), kwargs.get("code", ""), duration)

    def show_interpret_plot(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            self.t("interpret_heading"),
            self.t("interpret_lines"),
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

    def show_extra_meta(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            self.t("extra_meta_heading"),
            self.t("extra_meta_lines"),
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_no_log(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "ax.set_xscale('linear')"),
            kwargs.get("correct_code", "ax.set_xscale('log')"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_intercept(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "plot_forest(table2)"),
            kwargs.get("correct_code", "plot_forest(table2.loc[1:])"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_vline(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "# no reference line drawn"),
            kwargs.get("correct_code", "ax.axvline(1.0, ls='--', color='gray')"),
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
