"""Ch05-02: DAG — Directed Acyclic Graph 因果地圖"""

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


class Ch05DagScene(EpiBaseScene):
    """Tutorial video scene: DAG concept."""

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
        self.show_title_card("DAG 有向無環圖", "畫一張因果地圖", duration=duration)

    def show_dag_basics(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            "DAG 三條規則",
            [
                "① 節點（Node）：代表變項",
                "② 有向箭頭：從因指向果",
                "③ 無環（Acyclic）：不能回到自己",
                "違反規則就不是 DAG。",
            ],
            duration,
        )

    def show_front_back_door(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            "前門 vs 後門路徑",
            [
                "前門：E → D（你想研究的真效應）",
                "後門：E ← C → D（干擾路徑）",
                "後門不堵，RR 會被污染",
                "堵後門 = 控制 C（分層或調整）",
            ],
            duration,
        )

    def show_legionella_dag(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets(
            "退伍軍人桿菌的 DAG",
            [
                "shower_use → infection（前門）",
                "functional_status → shower_use",
                "functional_status → infection",
                "→ 後門路徑存在，須控制 fs",
            ],
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            "重點整理",
            [
                "DAG = 節點 + 有向箭頭 + 無環",
                "前門 = 直接效應；後門 = 干擾",
                "畫 DAG 先於分析",
                "DAG 告訴你：哪些該控制、哪些不該",
            ],
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner("額外範例：吸菸 → 肺癌 + 黃手指"), duration=duration)

    def show_extra_smoking(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            "黃手指陷阱：Collider",
            [
                "smoking → lung_cancer（前門）",
                "smoking → yellow_finger（副作用）",
                "lung_cancer ← ... ← yellow_finger ?",
                "黃手指是 collider，控制它會製造假關聯",
                "→ DAG 告訴你：絕對不要控制 collider",
            ],
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner("畫 DAG 常見地雷 3 選"), duration=duration)

    def show_blindspot_time(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "dag.edge('infection', 'shower_use')"),
            kwargs.get("correct_code", "dag.edge('shower_use', 'infection')"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_unmeasured(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "dag.nodes = ['E', 'D', 'age']"),
            kwargs.get("correct_code", "dag.nodes = ['E', 'D', 'age', 'U_genetics']"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_correlation(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "if corr > 0.5: dag.add_edge(A, B)"),
            kwargs.get("correct_code", "if domain_knowledge_says_cause: dag.add_edge(A, B)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text("下一集：用 pandas 驗證三要件", font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text("把 DAG 變成數據證據。", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
