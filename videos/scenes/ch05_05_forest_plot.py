"""Ch05-05: Stratified Forest Plot with matplotlib errorbar

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


class Ch05ForestPlotScene(EpiBaseScene):
    """Tutorial video scene: forest plot for stratified RR."""

    total_steps: int = 13

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "森林圖",
            "title_sub": "一眼看穿各層 RR",
            "concept_heading": "森林圖的視覺語言",
            "concept_bullets": [
                "每一層 = 一棵樹",
                "點（軀幹）= RR 點估計值",
                "水平線（樹枝）= 95% 信賴區間",
                "跨過 RR=1 參考線 = 無統計顯著",
            ],
            "errorbar_heading": "核心：plt.errorbar + xerr",
            "reference_heading": "兩條參考線：RR=1 與 粗 RR",
            "axis_heading": "最後收尾：座標軸 + 標題",
            "summary_heading": "森林圖五大元素",
            "summary_bullets": [
                "① errorbar：點 + 水平誤差棒",
                "② RR = 1 虛線參考",
                "③ 粗 RR 紅色點線參考",
                "④ y 軸標每層名稱",
                "⑤ 有資訊的標題",
            ],
            "extra_banner_title": "額外範例：Meta-analysis 森林圖",
            "meta_heading": "Meta-analysis 十層森林圖",
            "blindspot_banner_title": "畫森林圖常見地雷 3 選",
            "outro_heading": "下一集：Mantel-Haenszel 合併",
            "outro_sub": "把三層 RR 合併成一個調整後值。",
        },
        "en": {
            "title_main": "The Forest Plot",
            "title_sub": "See every stratum's RR at a glance",
            "concept_heading": "The visual language of a forest plot",
            "concept_bullets": [
                "Each stratum = one tree",
                "Dot (the trunk) = RR point estimate",
                "Horizontal line (branches) = 95% CI",
                "Crosses the RR=1 line = not significant",
            ],
            "errorbar_heading": "Core: plt.errorbar + xerr",
            "reference_heading": "Two reference lines: RR=1 and crude RR",
            "axis_heading": "Final touches: axes + title",
            "summary_heading": "The five forest-plot elements",
            "summary_bullets": [
                "① errorbar: dot + horizontal error bar",
                "② RR = 1 dashed reference",
                "③ crude RR red dotted reference",
                "④ y-axis labels each stratum",
                "⑤ an informative title",
            ],
            "extra_banner_title": "Extra example: meta-analysis forest plot",
            "meta_heading": "A ten-row meta-analysis forest plot",
            "blindspot_banner_title": "3 Common Forest-Plot Traps",
            "outro_heading": "Next up: Mantel-Haenszel pooling",
            "outro_sub": "Pool three strata into one adjusted value.",
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
        panel = self.show_code(code, title="forest_plot.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_forest_concept(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            self.t("concept_heading"),
            self.t("concept_bullets"),
            duration,
        )

    def show_errorbar_code(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._code_block(self.t("errorbar_heading"), kwargs.get("code", ""), duration)

    def show_reference_lines(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block(self.t("reference_heading"), kwargs.get("code", ""), duration)

    def show_axis_labels(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._code_block(self.t("axis_heading"), kwargs.get("code", ""), duration)

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            self.t("summary_heading"),
            self.t("summary_bullets"),
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_meta(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._code_block(self.t("meta_heading"), kwargs.get("code", ""), duration)

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_no_ref(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "ax.errorbar(rr, y, xerr=ci); plt.show()"),
            kwargs.get("correct_code", "ax.axvline(x=1, linestyle='--'); plt.show()"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_linear(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "ax.set_xscale('linear')"),
            kwargs.get("correct_code", "ax.set_xscale('log')"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_n(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "ax.set_yticklabels(['Group A', 'Group B'])"),
            kwargs.get("correct_code", "ax.set_yticklabels(['Group A (n=200)', 'Group B (n=20)'])"),
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
