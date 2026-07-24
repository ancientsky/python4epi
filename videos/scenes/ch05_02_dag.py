"""Ch05-02: DAG — Directed Acyclic Graph 因果地圖

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


class Ch05DagScene(EpiBaseScene):
    """Tutorial video scene: DAG concept."""

    total_steps: int = 12

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "DAG 有向無環圖",
            "title_sub": "畫一張因果地圖",
            "basics_heading": "DAG 三條規則",
            "basics_bullets": [
                "① 節點（Node）：代表變項",
                "② 有向箭頭：從因指向果",
                "③ 無環（Acyclic）：不能回到自己",
                "違反規則就不是 DAG。",
            ],
            "door_heading": "前門 vs 後門路徑",
            "door_bullets": [
                "前門：E → D（你想研究的真效應）",
                "後門：E ← C → D（干擾路徑）",
                "後門不堵，RR 會被污染",
                "堵後門 = 控制 C（分層或調整）",
            ],
            "legionella_heading": "退伍軍人桿菌的 DAG",
            "legionella_bullets": [
                "shower_use → infection（前門）",
                "functional_status → shower_use",
                "functional_status → infection",
                "→ 後門路徑存在，須控制 fs",
            ],
            "summary_heading": "重點整理",
            "summary_bullets": [
                "DAG = 節點 + 有向箭頭 + 無環",
                "前門 = 直接效應；後門 = 干擾",
                "畫 DAG 先於分析",
                "DAG 告訴你：哪些該控制、哪些不該",
            ],
            "extra_banner_title": "額外範例：吸菸 → 肺癌 + 黃手指",
            "smoking_heading": "黃手指陷阱：Collider",
            "smoking_bullets": [
                "smoking → lung_cancer（前門）",
                "smoking → yellow_finger（副作用）",
                "lung_cancer ← ... ← yellow_finger ?",
                "黃手指是 collider，控制它會製造假關聯",
                "→ DAG 告訴你：絕對不要控制 collider",
            ],
            "blindspot_banner_title": "畫 DAG 常見地雷 3 選",
            "outro_heading": "下一集：用 pandas 驗證三要件",
            "outro_sub": "把 DAG 變成數據證據。",
        },
        "en": {
            "title_main": "DAG: Directed Acyclic Graph",
            "title_sub": "Drawing a causal map",
            "basics_heading": "The Three DAG Rules",
            "basics_bullets": [
                "① Node: stands for a variable",
                "② Directed arrow: cause points to effect",
                "③ Acyclic: you can't loop back to yourself",
                "Break a rule and it's not a DAG.",
            ],
            "door_heading": "Front-door vs back-door paths",
            "door_bullets": [
                "Front door: E → D (the true effect you want)",
                "Back door: E ← C → D (the confounding path)",
                "Leave the back door open and RR gets polluted",
                "Close the back door = control C (stratify or adjust)",
            ],
            "legionella_heading": "The Legionella DAG",
            "legionella_bullets": [
                "shower_use → infection (front door)",
                "functional_status → shower_use",
                "functional_status → infection",
                "→ Back-door path exists, must control fs",
            ],
            "summary_heading": "Recap",
            "summary_bullets": [
                "DAG = nodes + directed arrows + no cycles",
                "Front door = direct effect; back door = confounding",
                "Draw the DAG before you analyze",
                "The DAG tells you what to control and what NOT to",
            ],
            "extra_banner_title": "Extra example: smoking → lung cancer + yellow fingers",
            "smoking_heading": "The yellow-finger trap: a collider",
            "smoking_bullets": [
                "smoking → lung_cancer (front door)",
                "smoking → yellow_finger (side effect)",
                "lung_cancer ← ... ← yellow_finger ?",
                "Yellow finger is a collider; controlling it fakes a link",
                "→ The DAG says: NEVER control a collider",
            ],
            "blindspot_banner_title": "3 Common DAG-Drawing Traps",
            "outro_heading": "Next up: verify the three criteria with pandas",
            "outro_sub": "Turn the DAG into data-backed evidence.",
        },
    }

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
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_dag_basics(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            self.t("basics_heading"),
            self.t("basics_bullets"),
            duration,
        )

    def show_front_back_door(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            self.t("door_heading"),
            self.t("door_bullets"),
            duration,
        )

    def show_legionella_dag(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets(
            self.t("legionella_heading"),
            self.t("legionella_bullets"),
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            self.t("summary_heading"),
            self.t("summary_bullets"),
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_smoking(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            self.t("smoking_heading"),
            self.t("smoking_bullets"),
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

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
        h = Text(self.t("outro_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text(self.t("outro_sub"), font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
