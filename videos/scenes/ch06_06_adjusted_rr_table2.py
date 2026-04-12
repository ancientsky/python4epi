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
        self.show_title_card("多變項 adjusted RR", "打造論文 Table 2", duration=duration)

    def show_why_multivariate(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            "為什麼升級多變項？",
            [
                "Ch05 分層：一次只控 1 個",
                ">3 個分層 → 樣本不夠",
                "多變項迴歸：一次控 10+ 個",
                "樣本大就能跑",
            ],
            duration,
        )

    def show_full_formula(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._code_block("完整公式：10 個變項一起", kwargs.get("code", ""), duration)

    def show_table2_build(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block("Table 2 組裝程式碼", kwargs.get("code", ""), duration)

    def show_interpret_table2(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            "解讀重點",
            [
                "Intercept 跳過（無臨床意義）",
                "shower_use aRR 2.8 (1.5, 5.2), p=0.001",
                "控制其他因子後仍顯著",
                "→ 淋浴是真正的暴露源",
            ],
            duration,
        )

    def show_compare_three(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            "三個效應測量比較",
            [
                "Ch03 crude RR：無控制",
                "Ch05 MH RR：控 1 個變項",
                "Ch06 adj RR：控一打變項 ✓",
                "最可信 = 排除最多干擾",
            ],
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            "Table 2 四步驟",
            [
                "① 完整公式列出調整因子",
                "② Modified Poisson + HC0",
                "③ exp params / conf_int / pvalues",
                "④ drop Intercept、focus 暴露",
            ],
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner("額外範例：AIDS 抗病毒藥"), duration=duration)

    def show_extra_art(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets(
            "ART 抗病毒藥觀察研究",
            [
                "crude RR 0.3（效果看起來很好）",
                "病人自選（confounding by indication）",
                "控 CD4 / viral load / 年齡…",
                "adjusted RR 升到 0.55",
                "→ 仍顯著，但沒有那麼誇張",
            ],
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner("Table 2 地雷 3 選"), duration=duration)

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
        h = Text("下一集：Forest Plot", font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text("Table 變成一張森林圖", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
