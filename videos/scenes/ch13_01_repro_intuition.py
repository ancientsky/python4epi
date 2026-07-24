"""Ch13-01: Reproducible research, plain and simple - it's just a good recipe.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    UP,
    FadeIn,
    FadeOut,
    Line,
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
    BG_CARD_ALT,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch13ReproIntuitionScene(EpiBaseScene):
    """Tutorial video scene: reproducible research as a good recipe."""

    total_steps: int = 9

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "可重現研究超白話",
            "title_sub": "把分析寫成一份好食譜",
            "recipe_heading": "朋友跟你要食譜",
            "recipe_lines": [
                "朋友吃到你的蛋糕，回家想做出一樣的味道",
                "你會給她什麼？一份寫得夠仔細的食譜",
                "不是「憑感覺加糖」，是「120 克糖」",
                "→ 同一份資料、同一份程式 ⟶ 同一個答案",
            ],
            "four_ingredients_heading": "備齊四樣，才能複製一顆蛋糕",
            "ing_code": "Code\n食譜（每步驟可重跑）",
            "ing_data": "Data\n食材（同一份原始資料）",
            "ing_env": "Environment\nuv.lock（廚房設定）",
            "ing_seed": "Seed\n骰子先喬好（種子）",
            "ingredients_result": "→ 任何人、任何機器，烤出同一顆蛋糕",
            "mapping_heading": "比喻 ↔ 技術名詞對照",
            "mapping_lines": [
                "食譜 → Code：每步驟寫成能重跑的程式",
                "食材 → Data：同一份原始資料，不偷改",
                "廚房設定 → Environment：uv.lock 鎖死版本",
                "骰子先喬好 → Seed：隨機也要「隨機地一致」",
                "蛋糕 → 可重現結果：不多不少複製出來",
            ],
            "definition_heading": "把重點釘死",
            "definition_lines": [
                "可重現 ≠「這次算對了沒」",
                "可重現 =「換人、換機器，還是同一個答案」",
                "→ 別人拿 code+data+env+seed 複製出同樣結果",
            ],
            "summary_heading": "可重現食譜三重點",
            "summary_lines": [
                "① 四樣材料：code / data / environment / seed",
                "② 四樣備齊，任何人都烤出同一顆蛋糕",
                "③ 重點是「可複製」，不是「這次剛好對」",
                "→ 下一集：為什麼我重跑結果不一樣？",
            ],
            "extra_banner_title": "額外範例：重現一篇 COVID-19 分析",
            "extra_covid_heading": "換場景：重現別人的論文",
            "extra_covid_lines": [
                "看到一篇 COVID-19 分析，想在自己電腦重跑",
                "作者附上 code + data + requirements + seed",
                "uv sync 裝環境、鎖種子、跑同一支腳本",
                "→ 拿到跟論文一樣的數字，才叫可重現",
            ],
            "blindspot_banner_title": "可重現研究三個新手地雷",
            "outro_heading": "下一集：為什麼我重跑結果不一樣？",
            "outro_sub": "三顆地雷 vs 三根支柱，一一對上",
        },
        "en": {
            "title_main": "Reproducible Research, Plain and Simple",
            "title_sub": "Write your analysis as a good recipe",
            "recipe_heading": "A Friend Wants Your Recipe",
            "recipe_lines": [
                "Your friend loved your cake and wants the same taste",
                "What do you give her? A detailed-enough recipe",
                'not "sugar to taste" but "120 grams of sugar"',
                "-> same data, same code -> the same answer",
            ],
            "four_ingredients_heading": "Four Things to Reproduce a Cake",
            "ing_code": "Code\nrecipe (every step re-runnable)",
            "ing_data": "Data\ningredients (same raw data)",
            "ing_env": "Environment\nuv.lock (kitchen setup)",
            "ing_seed": "Seed\nrig the dice (random seed)",
            "ingredients_result": "-> anyone, any machine bakes the same cake",
            "mapping_heading": "Metaphor <-> Technical Term",
            "mapping_lines": [
                "recipe -> Code: every step as re-runnable code",
                "ingredients -> Data: same raw data, no secret edits",
                "kitchen -> Environment: uv.lock pins versions",
                'dice -> Seed: random, but "consistently random"',
                "cake -> reproducible result: copied exactly",
            ],
            "definition_heading": "Nail Down the Point",
            "definition_lines": [
                'reproducible != "did it come out right this time"',
                'reproducible = "same answer on any machine, any person"',
                "-> others copy it from code+data+env+seed",
            ],
            "summary_heading": "Three Takeaways on the Recipe",
            "summary_lines": [
                "1. Four things: code / data / environment / seed",
                "2. All four ready -> anyone bakes the same cake",
                '3. It is about "copyable", not "right by luck"',
                "-> Next: why do I get different results?",
            ],
            "extra_banner_title": "Extra example: reproduce a COVID-19 analysis",
            "extra_covid_heading": "New scene: reproduce someone's paper",
            "extra_covid_lines": [
                "You find a COVID-19 analysis and want to re-run it",
                "The author ships code + data + requirements + seed",
                "uv sync the env, fix the seed, run the same script",
                "-> matching the paper's numbers is reproducibility",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: why do I get different results?",
            "outro_sub": "Three landmines vs three pillars, matched up",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _bullets(self, heading_key: str, lines_key: str, duration: float) -> None:
        h = Text(
            self.t(heading_key), font=FONT_CJK, font_size=30, color=ManimColor(ACCENT_ORANGE)
        ).to_edge(UP, buff=0.8)
        bl = (
            VGroup(
                *[
                    Text(x, font=FONT_CJK, font_size=23, color=ManimColor(TEXT_PRIMARY))
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

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_recipe_scenario(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("recipe_heading", "recipe_lines", duration)

    def show_four_ingredients(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        heading = Text(
            self.t("four_ingredients_heading"),
            font=FONT_CJK,
            font_size=28,
            color=ManimColor(ACCENT_ORANGE),
        ).to_edge(UP, buff=0.6)

        labels = [self.t("ing_code"), self.t("ing_data"), self.t("ing_env"), self.t("ing_seed")]
        accents = [ACCENT_ORANGE, ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE]
        cards = VGroup()
        for lab, acc in zip(labels, accents):
            card = RoundedRectangle(
                corner_radius=0.15,
                width=2.9,
                height=1.45,
                fill_color=ManimColor(BG_CARD),
                fill_opacity=1,
                stroke_color=ManimColor(acc),
                stroke_width=2,
            )
            txt = Text(
                lab, font=FONT_CJK, font_size=16, color=ManimColor(TEXT_PRIMARY)
            ).move_to(card.get_center())
            cards.add(VGroup(card, txt))
        cards.arrange(RIGHT, buff=0.22).move_to(UP * 1.0)

        arrow = Line(
            UP * 0.25, DOWN * 0.55, color=ManimColor(TEXT_SECONDARY), stroke_width=4
        ).move_to(DOWN * 0.15)
        result = RoundedRectangle(
            corner_radius=0.15,
            width=8.8,
            height=1.05,
            fill_color=ManimColor(BG_CARD_ALT),
            fill_opacity=1,
            stroke_color=ManimColor(ACCENT_GREEN),
            stroke_width=2,
        ).move_to(DOWN * 1.5)
        rtxt = Text(
            self.t("ingredients_result"),
            font=FONT_CJK,
            font_size=22,
            color=ManimColor(ACCENT_GREEN),
            weight="BOLD",
        ).move_to(result.get_center())

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(cards, lag_ratio=0.2), run_time=1.1)
        self.play(FadeIn(arrow), run_time=0.3)
        self.play(FadeIn(result), FadeIn(rtxt), run_time=0.6)
        self.wait(max(0.1, duration - 2.9))
        self.play(FadeOut(VGroup(heading, cards, arrow, result, rtxt)), run_time=0.5)

    def show_mapping(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets("mapping_heading", "mapping_lines", duration)

    def show_definition(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("definition_heading", "definition_lines", duration)

    def show_main_summary(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_covid(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("extra_covid_heading", "extra_covid_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_bs_share_only(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "share(result_png_only)"),
            kwargs.get("correct_code", "share(code, data, env, seed)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_bs_manual_edit(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "df = df.drop([3, 7])  # by hand"),
            kwargs.get("correct_code", "df = df[df.age >= 0]  # rule in code"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_bs_no_lock(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "pip install pandas"),
            kwargs.get("correct_code", "uv sync  # locked by uv.lock"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text(
            self.t("outro_heading"), font=FONT_CJK, font_size=26, color=ManimColor(ACCENT_ORANGE)
        ).move_to(ORIGIN + UP * 0.5)
        s = Text(
            self.t("outro_sub"), font=FONT_CJK, font_size=20, color=ManimColor(TEXT_SECONDARY)
        ).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
