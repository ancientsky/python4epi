"""Ch12-02: Association is not causation - the counterfactual, formally.

Defines the counterfactual outcomes Y_i(1) / Y_i(0), the fundamental problem of
causal inference, and how epidemiology approximates the missing world by
comparing similar groups. Grounded in the braised-chicken (滷雞腿) food-poisoning
investigation. Extra example: ice-cream sales vs drownings (summer confounds).

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    ManimColor,
    RoundedRectangle,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_BLUE,
    ACCENT_ORANGE,
    BG_CARD,
    ERROR_RED,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch12AssociationScene(EpiBaseScene):
    """Tutorial video scene: association vs causation and the counterfactual."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "關聯 ≠ 因果",
            "title_sub": "反事實：因果推論的正式起手式",
            "avc_heading": "關聯 vs 因果，差在哪？",
            "avc_lines": [
                "關聯 association：兩個變數「一起變動」",
                "→ 相關再強、p 值再小，都只是關聯",
                "因果 causation：拿掉這個暴露，結果會不會不一樣",
                "→ 這一句，才是政策敢不敢砸錢的關鍵",
            ],
            "cf_heading": "反事實：兩個平行世界",
            "cf_world1_title": "世界 1：有暴露",
            "cf_world1_body": "Y_i(1)\n這個人有淋浴\n會發生什麼",
            "cf_world0_title": "世界 0：沒暴露",
            "cf_world0_body": "Y_i(0)\n同一人沒淋浴\n會發生什麼",
            "cf_effect": "個人因果效應 = Y_i(1) − Y_i(0)",
            "cf_note": "同一人不可能同時活兩個世界 → 因果推論的基本問題",
            "solution_heading": "流病的解法：退一步比兩群人",
            "solution_lines": [
                "不比「同一人的兩個世界」（做不到）",
                "改比「兩群條件相似的人」",
                "用暴露組去逼近未暴露組的反事實",
                "→ 這正是 Ch05 分層、Ch06 迴歸校正在做的事",
            ],
            "chicken_heading": "背景案例：滷雞腿食物中毒",
            "chicken_lines": [
                "① 先看到關聯：吃滷雞腿的學生更容易腹瀉",
                "② 小心干擾與回憶偏差：生病的人更會記得吃了什麼",
                "③ 加上實驗室證據：檢體驗出產氣莢膜梭菌",
                "→ 關聯＋生物學證據＋排除其他解釋，才敢說因果",
            ],
            "summary_heading": "關聯 ≠ 因果，三重點",
            "summary_lines": [
                "① 光有統計關聯，哪怕 p 超小，都不足以宣告因果",
                "② 因果的靈魂是反事實：拿掉會不會不一樣",
                "③ 真實疫調＝關聯＋實驗室證據＋排除其他解釋",
                "→ 想清楚要比的反事實，比算出漂亮數字更重要",
            ],
            "extra_banner_title": "額外範例：冰淇淋與溺水",
            "extra_icecream_heading": "夏天，一手牽兩條線",
            "extra_icecream_lines": [
                "冰淇淋銷量 ↑，溺水人數也 ↑，相關明顯",
                "但反事實一問：把冰淇淋收掉，溺水會變少嗎？不會",
                "真正的共同原因是「夏天」這個干擾因子",
                "→ 這是干擾，不是因果——分季節看就現形",
            ],
            "blindspot_banner_title": "關聯 ≠ 因果，三個新手地雷",
            "outro_heading": "下一集：用 DAG 把因果畫出來",
            "outro_sub": "干擾、中介、對撞——三結構，兩套相反規則",
        },
        "en": {
            "title_main": "Association != Causation",
            "title_sub": "The counterfactual: causal inference's opening move",
            "avc_heading": "Association vs causation - what's the difference?",
            "avc_lines": [
                "Association: two variables move together",
                "-> however strong, however tiny the p, still just association",
                "Causation: remove the exposure, would the outcome differ?",
                "-> this sentence is what decides whether to spend the money",
            ],
            "cf_heading": "The counterfactual: two parallel worlds",
            "cf_world1_title": "World 1: exposed",
            "cf_world1_body": "Y_i(1)\nthis person showers\nwhat happens",
            "cf_world0_title": "World 0: unexposed",
            "cf_world0_body": "Y_i(0)\nsame person, no shower\nwhat happens",
            "cf_effect": "individual causal effect = Y_i(1) - Y_i(0)",
            "cf_note": "one person can't live both worlds -> the fundamental problem",
            "solution_heading": "The epi fix: step back, compare two groups",
            "solution_lines": [
                "Don't compare one person's two worlds (impossible)",
                "Compare two groups with similar conditions instead",
                "Use the exposed group to approximate the missing counterfactual",
                "-> exactly what Ch05 stratification and Ch06 regression do",
            ],
            "chicken_heading": "Case: a braised-chicken food poisoning",
            "chicken_lines": [
                "1. Association first: kids who ate it had more diarrhea",
                "2. Watch confounding & recall bias: the sick remember better",
                "3. Add lab evidence: C. perfringens found in samples",
                "-> association + biology + ruling out alternatives = causation",
            ],
            "summary_heading": "Association != Causation, 3 Takeaways",
            "summary_lines": [
                "1. Statistical association alone, tiny p or not, isn't causation",
                "2. Causation's soul is the counterfactual: remove it, any change?",
                "3. Real investigation = association + lab evidence + alternatives out",
                "-> nailing the counterfactual beats computing a pretty number",
            ],
            "extra_banner_title": "Extra example: ice-cream and drownings",
            "extra_icecream_heading": "Summer pulls both strings at once",
            "extra_icecream_lines": [
                "Ice-cream sales up, drownings up - clear correlation",
                "But ask the counterfactual: pull ice-cream, fewer drownings? No",
                'The real common cause is "summer" - a confounder',
                "-> confounding, not causation - split by season and it shows",
            ],
            "blindspot_banner_title": "Association != Causation, 3 Blind Spots",
            "outro_heading": "Next: drawing causation with a DAG",
            "outro_sub": "Confounder, mediator, collider - 3 shapes, 2 opposite rules",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _bullets(self, heading_key: str, lines_key: str, duration: float) -> None:
        h = Text(self.t(heading_key), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.8
        )
        bl = (
            VGroup(
                *[
                    Text(x, font=FONT_CJK, font_size=22, color=TEXT_PRIMARY)
                    for x in self.t(lines_key)
                ]
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            .next_to(h, DOWN, buff=0.6)
        )
        self.play(FadeIn(h), run_time=0.5)
        self.play(FadeIn(bl, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(h, bl)), run_time=0.5)

    def _world_card(self, title_key: str, body_key: str, color: str):
        card = RoundedRectangle(
            corner_radius=0.15,
            width=4.0,
            height=2.6,
            fill_color=ManimColor(BG_CARD),
            fill_opacity=1,
            stroke_color=ManimColor(color),
            stroke_width=3,
        )
        title = Text(self.t(title_key), font=FONT_CJK, font_size=22, color=ManimColor(color), weight="BOLD")
        body = Text(self.t(body_key), font=FONT_MONO, font_size=19, color=ManimColor(TEXT_PRIMARY))
        content = VGroup(title, body).arrange(DOWN, buff=0.3)
        content.move_to(card.get_center())
        return VGroup(card, content)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_assoc_vs_causation(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("avc_heading", "avc_lines", duration)

    def show_counterfactual_def(self, duration: float = 10.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            self.t("cf_heading"), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)

        world1 = self._world_card("cf_world1_title", "cf_world1_body", ACCENT_ORANGE)
        world0 = self._world_card("cf_world0_title", "cf_world0_body", ACCENT_BLUE)
        worlds = VGroup(world1, world0).arrange(RIGHT, buff=0.7).move_to(UP * 0.4)

        effect = Text(
            self.t("cf_effect"), font=FONT_MONO, font_size=20, color=ManimColor(TEXT_PRIMARY)
        ).next_to(worlds, DOWN, buff=0.4)
        note = Text(
            self.t("cf_note"), font=FONT_CJK, font_size=18, color=ERROR_RED
        ).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(worlds, lag_ratio=0.2), run_time=1.1)
        self.play(FadeIn(effect), run_time=0.4)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(max(0.1, duration - 2.7))
        self.play(FadeOut(VGroup(heading, worlds, effect, note)), run_time=0.5)

    def show_epi_solution(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets("solution_heading", "solution_lines", duration)

    def show_chicken_case(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("chicken_heading", "chicken_lines", duration)

    def show_main_summary(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_icecream(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("extra_icecream_heading", "extra_icecream_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_p_is_cause(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "causal = (p_value < 0.05)"),
            kwargs.get("correct_code", "causal = assoc and lab and dag_ok"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_adjust(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "rr = risk_exposed / risk_unexposed"),
            kwargs.get("correct_code", "rr = mantel_haenszel(exp, out, strata)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_reverse_causation(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "x = df['measured_after_onset']"),
            kwargs.get("correct_code", "assert exposure_date < onset_date"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text(self.t("outro_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(
            ORIGIN + UP * 0.5
        )
        s = Text(self.t("outro_sub"), font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(
            h, DOWN, buff=0.4
        )
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
