"""Ch05-01: Confounder Concept — 干擾因子三要件

Manim scene for Chapter 05 intro video on confounding fundamentals.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    ORIGIN,
    FadeIn,
    FadeOut,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_ORANGE,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch05ConfounderConceptScene(EpiBaseScene):
    """Tutorial video scene: introduction to confounders."""

    total_steps: int = 12

    def construct(self) -> None:
        self.construct_from_segments()

    def _bullets(self, heading: str, lines: list[str], duration: float) -> None:
        h = Text(heading, font=FONT_CJK, font_size=32, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        bl = VGroup(
            *[Text(x, font=FONT_CJK, font_size=24, color=TEXT_PRIMARY) for x in lines]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(h, DOWN, buff=0.6)
        self.play(FadeIn(h), run_time=0.5)
        self.play(FadeIn(bl, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(h, bl)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card("干擾因子三要件", "誰才算真正的共犯", duration=duration)

    def show_raincoat(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            "雨衣的比喻",
            [
                "觀察：穿雨衣  ↔  感冒（看起來相關）",
                "真相：下雨天 → 穿雨衣",
                "真相：下雨天 → 感冒",
                "下雨天 = 幕後的干擾因子",
                "不控制它，你會冤枉雨衣。",
            ],
            duration,
        )

    def show_three_criteria(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            "干擾因子三要件（缺一不可）",
            [
                "① 與 暴露 E 相關",
                "② 與 結果 D 相關",
                "③ 不是 E → D 的中間變項",
                "三者都成立，才叫干擾因子。",
            ],
            duration,
        )

    def show_legionella_case(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets(
            "退伍軍人桿菌案例：驗證「功能狀態」",
            [
                "E = 淋浴使用，D = 感染",
                "① 能走動的人才會走進淋浴 ✓",
                "② 能走動者活動範圍大、接觸水霧多 ✓",
                "③ 洗澡不會讓人變能走動（方向錯）✓",
                "→ functional_status 是干擾因子",
            ],
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            "重點整理：三要件缺一不可",
            [
                "① 與暴露 E 相關",
                "② 與結果 D 相關",
                "③ 非 E → D 的中間變項",
                "下一集：用 DAG 把它畫出來！",
            ],
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner("額外範例：夜市鹽酥雞 × 腹瀉"), duration=duration)

    def show_extra_night_market(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            "夜市小吃攤的干擾因子",
            [
                "觀察：吃鹽酥雞 ↔ 腹瀉（相關）",
                "真相：天氣熱 → 吃夜市機會多",
                "真相：天氣熱 → 食物易壞、腹瀉",
                "氣溫 = 干擾因子",
                "→ 分層或限縮溫度範圍再分析",
            ],
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner("初學者常見地雷 3 選"), duration=duration)

    def show_blindspot_correlation(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "if corr(C, E) > 0.3: confounders.append(C)"),
            kwargs.get("correct_code", "if passes_three_criteria(C, E, D): confounders.append(C)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_mediator(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "model.adjust_for(['smoking', 'lung_function'])"),
            kwargs.get("correct_code", "model.adjust_for(['age', 'sex'])  # NOT mediators"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_one_criterion(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "if chi2(C, exposure).pvalue < 0.05: confound = True"),
            kwargs.get("correct_code", "check_all_three_criteria(C, exposure, outcome)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text("下一集：DAG 因果地圖", font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text("畫一張圖，干擾因子無所遁形。", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
