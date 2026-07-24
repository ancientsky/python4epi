"""Ch12-01: Causal detective - "if we ran it again, would they still get sick?"

Super-plain (超白話) intuition for causal inference: counterfactual thinking,
association != causation, and the three suspects a good detective must not
confuse (confounder / mediator / collider).

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Arrow,
    Create,
    DashedLine,
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
    ACCENT_GREEN,
    ACCENT_ORANGE,
    BG_CARD,
    BORDER_LIGHT,
    ERROR_RED,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch12CausalIntuitionScene(EpiBaseScene):
    """Tutorial video scene: the causal-detective intuition for causal inference."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "因果偵探超白話",
            "title_sub": "如果重來一次，還會生病嗎？",
            "crime_heading": "案發現場：關聯不等於真兇",
            "crime_summer": "夏天\n（藏鏡人）",
            "crime_icecream": "冰淇淋銷量\n暴露",
            "crime_drown": "溺水人數\n結果",
            "crime_link": "看起來相關，其實沒因果",
            "crime_caption": "冰淇淋和溺水一起變多，真兇卻是背後的「夏天」",
            "cf_heading": "偵探的破案咒語",
            "cf_lines": [
                "「如果重來一次，把嫌疑犯拿掉，事情還會發生嗎？」",
                "同一個人、同一情境，只差有沒有暴露",
                "比較這兩個平行世界的結果",
                "→ 這句咒語的正式名稱：反事實 counterfactual",
            ],
            "traps_heading": "三個常見辦案陷阱",
            "trap_confounder_title": "干擾 confounder",
            "trap_confounder_sub": "藏在背後的真兇\n同時牽動暴露與結果",
            "trap_mediator_title": "中介 mediator",
            "trap_mediator_sub": "案情往下傳的傳話筒\n別當犯人抓走",
            "trap_collider_title": "碰撞 collider",
            "trap_collider_sub": "只看送驗案件的假象\n絕對別校正",
            "glossary_heading": "偵探手冊 ↔ 因果推論術語",
            "glossary_lines": [
                "兩件事同時發生 → 關聯 ≠ 因果",
                "拿掉還會不會發生 → 反事實",
                "背後的真兇 → 干擾因子（該校正）",
                "往下傳的傳話筒 → 中介變項（別亂調）",
                "選樣造成的假象 → 對撞因子（絕不調）",
            ],
            "summary_heading": "整段特別篇一句話打包",
            "summary_lines": [
                "① 關聯 ≠ 因果：一起變動不代表誰造成誰",
                "② 永遠先問反事實：拿掉會不會不一樣",
                "③ 提防三陷阱：干擾、中介、對撞",
                "→ 後面的 DAG 和公式，都是這句咒語的工具",
            ],
            "extra_banner_title": "額外範例：咖啡真的「致癌」嗎？",
            "extra_coffee_heading": "咖啡 vs 胰臟癌的假關聯",
            "extra_coffee_lines": [
                "早年研究：愛喝咖啡的人胰臟癌較多",
                "但重度咖啡族也常常是老菸槍",
                "真兇其實是抽菸這個干擾因子",
                "→ 校正抽菸後，咖啡的關聯幾乎消失",
            ],
            "blindspot_banner_title": "因果偵探三個新手地雷",
            "outro_heading": "下一集：關聯 ≠ 因果，正式版",
            "outro_sub": "反事實的數學定義 + 滷雞腿疫調故事",
        },
        "en": {
            "title_main": "The Causal Detective, Plain and Simple",
            "title_sub": "If we ran it again, would they still get sick?",
            "crime_heading": "Crime scene: association is not the culprit",
            "crime_summer": "Summer\n(the hidden hand)",
            "crime_icecream": "Ice-cream sales\nexposure",
            "crime_drown": "Drownings\noutcome",
            "crime_link": "looks correlated, no causation",
            "crime_caption": 'Ice-cream and drownings rise together - but the real culprit is "summer"',
            "cf_heading": "The Detective's Magic Spell",
            "cf_lines": [
                '"If we ran it again, remove the suspect - would it still happen?"',
                "Same person, same setting, only exposure differs",
                "Compare the outcome across those two parallel worlds",
                "-> the formal name for this spell: the counterfactual",
            ],
            "traps_heading": "Three Common Case-Solving Traps",
            "trap_confounder_title": "confounder",
            "trap_confounder_sub": "the culprit hiding behind\nnudges exposure AND outcome",
            "trap_mediator_title": "mediator",
            "trap_mediator_sub": "the messenger passing it on\ndon't arrest it by mistake",
            "trap_collider_title": "collider",
            "trap_collider_sub": "an artefact of who got tested\nnever adjust for it",
            "glossary_heading": "Detective's Handbook <-> Causal Terms",
            "glossary_lines": [
                "Two things happen together -> association != causation",
                "Remove it, would it still happen -> counterfactual",
                "The hidden culprit -> confounder (do adjust)",
                "The messenger downstream -> mediator (don't over-adjust)",
                "Selection artefact -> collider (never adjust)",
            ],
            "summary_heading": "The Whole Special, In One Breath",
            "summary_lines": [
                "1. Association != causation: moving together != causing",
                "2. Always ask the counterfactual: remove it, any different?",
                "3. Beware the three traps: confounder, mediator, collider",
                "-> the DAGs and formulas ahead are just tools for this spell",
            ],
            "extra_banner_title": 'Extra example: does coffee really "cause" cancer?',
            "extra_coffee_heading": "The coffee vs pancreatic-cancer illusion",
            "extra_coffee_lines": [
                "Early studies: heavy coffee drinkers had more pancreatic cancer",
                "But heavy coffee drinkers were often heavy smokers too",
                "The real culprit was smoking - a confounder",
                "-> after adjusting for smoking, the coffee link nearly vanished",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: association != causation, the formal version",
            "outro_sub": "The math of the counterfactual + a food-poisoning investigation",
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
                    Text(x, font=FONT_CJK, font_size=23, color=TEXT_PRIMARY)
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

    def _node_card(self, text_key: str, color: str, *, width: float = 2.9, height: float = 1.3):
        card = RoundedRectangle(
            corner_radius=0.15,
            width=width,
            height=height,
            fill_color=ManimColor(BG_CARD),
            fill_opacity=1,
            stroke_color=ManimColor(color),
            stroke_width=3,
        )
        label = Text(self.t(text_key), font=FONT_CJK, font_size=20, color=ManimColor(TEXT_PRIMARY))
        label.move_to(card.get_center())
        return VGroup(card, label)

    def _trap_card(self, title_key: str, sub_key: str, color: str):
        card = RoundedRectangle(
            corner_radius=0.14,
            width=3.9,
            height=2.4,
            fill_color=ManimColor(color),
            fill_opacity=0.14,
            stroke_color=ManimColor(color),
            stroke_width=3,
        )
        title = Text(self.t(title_key), font=FONT_CJK, font_size=24, color=ManimColor(color), weight="BOLD")
        sub = Text(self.t(sub_key), font=FONT_CJK, font_size=17, color=ManimColor(TEXT_PRIMARY))
        content = VGroup(title, sub).arrange(DOWN, buff=0.25)
        content.move_to(card.get_center())
        return VGroup(card, content)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_crime_scene(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            self.t("crime_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)

        summer = self._node_card("crime_summer", ACCENT_ORANGE).move_to(UP * 1.3)
        icecream = self._node_card("crime_icecream", ACCENT_BLUE).move_to(LEFT * 3.0 + DOWN * 1.0)
        drown = self._node_card("crime_drown", ACCENT_BLUE).move_to(RIGHT * 3.0 + DOWN * 1.0)

        arrow_si = Arrow(
            summer.get_bottom(), icecream.get_top(), buff=0.1,
            color=ManimColor(ACCENT_ORANGE), stroke_width=4, max_tip_length_to_length_ratio=0.15,
        )
        arrow_sd = Arrow(
            summer.get_bottom(), drown.get_top(), buff=0.1,
            color=ManimColor(ACCENT_ORANGE), stroke_width=4, max_tip_length_to_length_ratio=0.15,
        )
        link = DashedLine(
            icecream.get_right(), drown.get_left(), buff=0.15,
            color=ManimColor(TEXT_SECONDARY), stroke_width=2,
        )
        link_label = Text(
            self.t("crime_link"), font=FONT_CJK, font_size=16, color=TEXT_SECONDARY
        ).next_to(link, UP, buff=0.15)

        caption = Text(
            self.t("crime_caption"), font=FONT_CJK, font_size=19, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(summer), run_time=0.5)
        self.play(
            Create(arrow_si), Create(arrow_sd), FadeIn(icecream), FadeIn(drown), run_time=1.0
        )
        self.play(Create(link), FadeIn(link_label), run_time=0.6)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 3.3))
        self.play(
            FadeOut(
                VGroup(
                    heading, summer, icecream, drown, arrow_si, arrow_sd, link, link_label, caption
                )
            ),
            run_time=0.5,
        )

    def show_counterfactual_spell(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets("cf_heading", "cf_lines", duration)

    def show_three_traps(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            self.t("traps_heading"), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.8)

        confounder = self._trap_card("trap_confounder_title", "trap_confounder_sub", ERROR_RED)
        mediator = self._trap_card("trap_mediator_title", "trap_mediator_sub", ACCENT_BLUE)
        collider = self._trap_card("trap_collider_title", "trap_collider_sub", ACCENT_GREEN)
        cards = VGroup(confounder, mediator, collider).arrange(RIGHT, buff=0.35).move_to(DOWN * 0.3)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(cards, lag_ratio=0.2), run_time=1.3)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(heading, cards)), run_time=0.5)

    def show_glossary(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("glossary_heading", "glossary_lines", duration)

    def show_main_summary(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_coffee(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("extra_coffee_heading", "extra_coffee_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_corr_is_cause(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "if ice_cream_up and drown_up: cause=1"),
            kwargs.get("correct_code", "check_common_cause(summer)  # confounder"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_counterfactual(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "close_case('shower is the killer')"),
            kwargs.get("correct_code", "ask('remove it, still sick?')  # cf"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_forget_confounder(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "blame(exposure)  # ignored confounders"),
            kwargs.get("correct_code", "blame(exposure, after_adjust=conf)"),
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
