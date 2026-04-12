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
        self.show_title_card("Adjusted RR 森林圖", "一眼看穿危險因子", duration=duration)

    def show_what_to_plot(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            "森林圖要畫什麼？",
            [
                "Y 軸：每列一個變項",
                "X 軸：RR（log scale）",
                "點 = aRR、橫線 = 95% CI",
                "中線：RR = 1 虛線參考",
                "點壓 1 = 不顯著",
            ],
            duration,
        )

    def show_why_log_x(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            "為什麼 X 軸用 log？",
            [
                "RR 是乘法效應",
                "RR = 0.5 跟 2 是同強度",
                "線性軸 → 左擠右拉、失衡",
                "log 尺度 → 左右對稱",
                "流病 forest 一律 xscale log",
            ],
            duration,
        )

    def show_code_demo(self, duration: float = 10.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block("matplotlib errorbar 骨架", kwargs.get("code", ""), duration)

    def show_interpret_plot(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            "看圖三招",
            [
                "① 壓 1 虛線的 → 不顯著",
                "② 全在右 + 不碰 1 → 危險因子",
                "③ 全在左 + 不碰 1 → 保護因子",
                "一張圖 → 優先順序一清二楚",
            ],
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            "森林圖五件事",
            [
                "Y 變項、X RR（log）",
                "點 = aRR、線 = CI",
                "RR=1 虛線",
                "點深色、CI 淺色",
                "壓 1 不顯著、遠離顯著",
            ],
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner("額外範例：Meta-analysis"), duration=duration)

    def show_extra_meta(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            "Meta-analysis 森林圖",
            [
                "每列一個研究（不是變項）",
                "最下一列：合併菱形",
                "random-effects model",
                "讀法完全一樣",
                "舉一反三 → 所有效應量都能看",
            ],
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner("Forest plot 地雷 3 選"), duration=duration)

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
        h = Text("下一集：change-in-estimate", font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text("10% 法則挑對的變項", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
