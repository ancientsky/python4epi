"""Ch05-01: Confounder Concept — 干擾因子三要件

Manim scene for Chapter 05 intro video on confounding fundamentals.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages.
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

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "干擾因子三要件",
            "title_sub": "誰才算真正的共犯",
            "raincoat_heading": "雨衣的比喻",
            "raincoat_bullets": [
                "觀察：穿雨衣  ↔  感冒（看起來相關）",
                "真相：下雨天 → 穿雨衣",
                "真相：下雨天 → 感冒",
                "下雨天 = 幕後的干擾因子",
                "不控制它，你會冤枉雨衣。",
            ],
            "criteria_heading": "干擾因子三要件（缺一不可）",
            "criteria_bullets": [
                "① 與 暴露 E 相關",
                "② 與 結果 D 相關",
                "③ 不是 E → D 的中間變項",
                "三者都成立，才叫干擾因子。",
            ],
            "legionella_heading": "退伍軍人桿菌案例：驗證「功能狀態」",
            "legionella_bullets": [
                "E = 淋浴使用，D = 感染",
                "① 能走動的人才會走進淋浴 ✓",
                "② 能走動者活動範圍大、接觸水霧多 ✓",
                "③ 洗澡不會讓人變能走動（方向錯）✓",
                "→ functional_status 是干擾因子",
            ],
            "summary_heading": "重點整理：三要件缺一不可",
            "summary_bullets": [
                "① 與暴露 E 相關",
                "② 與結果 D 相關",
                "③ 非 E → D 的中間變項",
                "下一集：用 DAG 把它畫出來！",
            ],
            "extra_banner_title": "額外範例：夜市鹽酥雞 × 腹瀉",
            "night_market_heading": "夜市小吃攤的干擾因子",
            "night_market_bullets": [
                "觀察：吃鹽酥雞 ↔ 腹瀉（相關）",
                "真相：天氣熱 → 吃夜市機會多",
                "真相：天氣熱 → 食物易壞、腹瀉",
                "氣溫 = 干擾因子",
                "→ 分層或限縮溫度範圍再分析",
            ],
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：DAG 因果地圖",
            "outro_sub": "畫一張圖，干擾因子無所遁形。",
        },
        "en": {
            "title_main": "The Three Criteria for a Confounder",
            "title_sub": "Who really counts as an accomplice?",
            "raincoat_heading": "The Raincoat Analogy",
            "raincoat_bullets": [
                "Observed: raincoat  ↔  colds (looks linked)",
                "Truth: rainy day → wearing a raincoat",
                "Truth: rainy day → catching a cold",
                "Rainy day = the hidden confounder",
                "Ignore it and you'll blame the raincoat.",
            ],
            "criteria_heading": "The Three Criteria (all required)",
            "criteria_bullets": [
                "① Associated with exposure E",
                "② Associated with outcome D",
                "③ NOT a mediator on E → D",
                "All three hold → it's a confounder.",
            ],
            "legionella_heading": "Legionella case: testing 'functional status'",
            "legionella_bullets": [
                "E = shower use, D = infection",
                "① Only mobile residents reach the shower ✓",
                "② Mobile residents roam more, meet more mist ✓",
                "③ Showering doesn't make you mobile (wrong way) ✓",
                "→ functional_status is a confounder",
            ],
            "summary_heading": "Recap: all three criteria required",
            "summary_bullets": [
                "① Associated with exposure E",
                "② Associated with outcome D",
                "③ Not a mediator on E → D",
                "Next up: draw it out with a DAG!",
            ],
            "extra_banner_title": "Extra example: night-market fried chicken × diarrhea",
            "night_market_heading": "The confounder at the night-market food stall",
            "night_market_bullets": [
                "Observed: fried chicken ↔ diarrhea (linked)",
                "Truth: hot weather → more night-market trips",
                "Truth: hot weather → food spoils, diarrhea",
                "Temperature = the confounder",
                "→ Stratify or restrict the temp range, then analyze",
            ],
            "blindspot_banner_title": "3 Common Beginner Traps",
            "outro_heading": "Next up: the DAG causal map",
            "outro_sub": "Draw one map and no confounder can hide.",
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

    def show_raincoat(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            self.t("raincoat_heading"),
            self.t("raincoat_bullets"),
            duration,
        )

    def show_three_criteria(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            self.t("criteria_heading"),
            self.t("criteria_bullets"),
            duration,
        )

    def show_legionella_case(self, duration: float = 7.0, **kwargs) -> None:
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

    def show_extra_night_market(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            self.t("night_market_heading"),
            self.t("night_market_bullets"),
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

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
        h = Text(self.t("outro_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text(self.t("outro_sub"), font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
