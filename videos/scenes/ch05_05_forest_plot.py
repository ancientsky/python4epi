"""Ch05-05: Stratified Forest Plot with matplotlib errorbar"""

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
        self.show_title_card("森林圖", "一眼看穿各層 RR", duration=duration)

    def show_forest_concept(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            "森林圖的視覺語言",
            [
                "每一層 = 一棵樹",
                "點（軀幹）= RR 點估計值",
                "水平線（樹枝）= 95% 信賴區間",
                "跨過 RR=1 參考線 = 無統計顯著",
            ],
            duration,
        )

    def show_errorbar_code(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._code_block("核心：plt.errorbar + xerr", kwargs.get("code", ""), duration)

    def show_reference_lines(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block("兩條參考線：RR=1 與 粗 RR", kwargs.get("code", ""), duration)

    def show_axis_labels(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._code_block("最後收尾：座標軸 + 標題", kwargs.get("code", ""), duration)

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            "森林圖五大元素",
            [
                "① errorbar：點 + 水平誤差棒",
                "② RR = 1 虛線參考",
                "③ 粗 RR 紅色點線參考",
                "④ y 軸標每層名稱",
                "⑤ 有資訊的標題",
            ],
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner("額外範例：Meta-analysis 森林圖"), duration=duration)

    def show_extra_meta(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._code_block("Meta-analysis 十層森林圖", kwargs.get("code", ""), duration)

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner("畫森林圖常見地雷 3 選"), duration=duration)

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
        h = Text("下一集：Mantel-Haenszel 合併", font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text("把三層 RR 合併成一個調整後值。", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
