"""Ch08-04: Global Moran's I - the "birds of a feather" index, with permutation p-value.

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
    Dot,
    FadeIn,
    FadeOut,
    Line,
    ManimColor,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_BLUE,
    ACCENT_ORANGE,
    BORDER_LIGHT,
    ERROR_RED,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch08MoransIScene(EpiBaseScene):
    """Tutorial video scene: global Moran's I with permutation p-value."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "全域 Moran's I",
            "title_sub": "整張地圖的「物以類聚」指數",
            "why_switch_heading": "為什麼換場景？",
            "why_switch_lines": [
                "護理之家只有一棟樓，6 組樣本太小",
                "縣市級空間統計 → 換上登革熱 x 全台縣市",
                "上一集做好的權重 w，直接沿用",
                "→ 這是台灣空間流病最經典的應用",
            ],
            "moran_intuition_heading": "Moran's I 量表",
            "moran_scale_neg1": "I ≈ −1\n高低相間（少見）",
            "moran_scale_zero": "I ≈ 0\n隨機散布",
            "moran_scale_pos1": "I ≈ +1\n高聚高、低聚低",
            "moran_intuition_caption": "跟第一集的洗牌檢定同一個靈魂，只是換了公式",
            "moran_code_heading": "esda.moran.Moran 一行算出來",
            "moran_code_title": "morans_i.py",
            "moran_output_heading": "跑出來的結果",
            "moran_output_text": (
                "Moran's I = 0.503, p = 0.0010\n"
                "→ 全台登革熱發生率有顯著空間群聚\n"
                "台南／高雄／嘉義：熱區核心\n"
                "北部：低發生率安全區"
            ),
            "pvalue_caution_heading": "光看 I 還不夠",
            "pvalue_caution_lines": [
                "I = 0.5 看起來像群聚",
                "但要靠洗牌 p_sim 證明不是巧合",
                "只有全域顯著，才值得往下做局部分析",
                "→ 局部熱區核心（LISA）留到下半部",
            ],
            "summary_heading": "全域 Moran's I 三重點",
            "summary_lines": [
                "① 正負號：+1 物以類聚、0 隨機、−1 高低相間",
                "② p_sim 才是「不是巧合」的判準",
                "③ 全域顯著才值得做局部分析",
                "→ 空間流病第一部完結！",
            ],
            "extra_banner_title": "額外範例：結核病的空間群聚",
            "extra_tb_heading": "換一種疾病，同一套程式",
            "extra_tb_title": "morans_i_tb.py",
            "blindspot_banner_title": "Moran's I 三個新手地雷",
            "outro_heading": "下半部預告：LISA 與 Getis-Ord Gi*",
            "outro_sub": "找出熱區核心、畫出給長官看的熱點圖",
        },
        "en": {
            "title_main": "Global Moran's I",
            "title_sub": 'A single "birds of a feather" index for the whole map',
            "why_switch_heading": "Why switch scenarios?",
            "why_switch_lines": [
                "The nursing home is one building - only 6 cells, too small",
                "County-level stats -> switch to dengue x all Taiwan counties",
                "The weights w built last episode carry over directly",
                "-> Taiwan's classic spatial epi application",
            ],
            "moran_intuition_heading": "The Moran's I Scale",
            "moran_scale_neg1": "I is about -1\ncheckerboard (rare)",
            "moran_scale_zero": "I is about 0\nrandom scatter",
            "moran_scale_pos1": "I is about +1\nhigh-with-high, low-with-low",
            "moran_intuition_caption": "Same soul as episode 1's shuffle test, just a fancier formula",
            "moran_code_heading": "esda.moran.Moran computes it in one line",
            "moran_code_title": "morans_i.py",
            "moran_output_heading": "The result",
            "moran_output_text": (
                "Moran's I = 0.503, p = 0.0010\n"
                "-> significant spatial clustering in dengue incidence\n"
                "Tainan / Kaohsiung / Chiayi: hotspot core\n"
                "North: a low-incidence safe zone"
            ),
            "pvalue_caution_heading": "I alone is not enough",
            "pvalue_caution_lines": [
                "I = 0.5 looks like clustering",
                "but the permutation p_sim must confirm it isn't chance",
                "only a significant global I is worth drilling into",
                "-> local hotspot cores (LISA) come in the second half",
            ],
            "summary_heading": "Three Takeaways on Global Moran's I",
            "summary_lines": [
                "1. Sign: +1 clustered, 0 random, -1 checkerboard",
                '2. p_sim is what proves "not chance"',
                "3. Only a significant global I justifies local analysis",
                "-> Part 1 of spatial epi complete!",
            ],
            "extra_banner_title": "Extra example: spatial clustering of TB",
            "extra_tb_heading": "Swap the disease, keep the same code",
            "extra_tb_title": "morans_i_tb.py",
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Coming next: LISA and Getis-Ord Gi*",
            "outro_sub": "Find the hotspot core and draw the map for your boss",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _bullets(self, heading_key: str, lines_key: str, duration: float) -> None:
        heading = self.t(heading_key)
        lines = self.t(lines_key)
        h = Text(heading, font=FONT_CJK, font_size=30, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        bl = (
            VGroup(*[Text(x, font=FONT_CJK, font_size=23, color=TEXT_PRIMARY) for x in lines])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            .next_to(h, DOWN, buff=0.6)
        )
        self.play(FadeIn(h), run_time=0.5)
        self.play(FadeIn(bl, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(h, bl)), run_time=0.5)

    def _code_block(self, heading_key: str, title_key: str, code: str, duration: float) -> None:
        h = Text(self.t(heading_key), font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.5
        )
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_code(code, title=self.t(title_key), position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_why_switch(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("why_switch_heading", "why_switch_lines", duration)

    def show_moran_intuition(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            self.t("moran_intuition_heading"), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.8)

        axis = Line(LEFT * 3.2, RIGHT * 3.2, color=ManimColor(BORDER_LIGHT), stroke_width=3)

        neg1_dot = Dot(point=LEFT * 3.2, radius=0.13, color=ManimColor(ACCENT_BLUE))
        zero_dot = Dot(point=ORIGIN, radius=0.13, color=ManimColor(TEXT_SECONDARY))
        pos1_dot = Dot(point=RIGHT * 3.2, radius=0.13, color=ManimColor(ERROR_RED))

        neg1_label = Text(
            self.t("moran_scale_neg1"), font=FONT_CJK, font_size=16, color=TEXT_PRIMARY
        ).next_to(neg1_dot, DOWN, buff=0.3)
        zero_label = Text(
            self.t("moran_scale_zero"), font=FONT_CJK, font_size=16, color=TEXT_PRIMARY
        ).next_to(zero_dot, DOWN, buff=0.3)
        pos1_label = Text(
            self.t("moran_scale_pos1"), font=FONT_CJK, font_size=16, color=TEXT_PRIMARY
        ).next_to(pos1_dot, DOWN, buff=0.3)

        scale = VGroup(
            axis, neg1_dot, zero_dot, pos1_dot, neg1_label, zero_label, pos1_label
        ).move_to(UP * 0.3)

        caption = Text(
            self.t("moran_intuition_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(scale), run_time=0.9)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(heading, scale, caption)), run_time=0.5)

    def show_moran_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "from esda.moran import Moran\n"
                "\n"
                'moran = Moran(main["rate"].values, w, permutations=999)\n'
                'print(f"Moran\'s I = {moran.I:.3f}, p = {moran.p_sim:.4f}")'
            ),
        )
        self._code_block("moran_code_heading", "moran_code_title", code, duration)

    def show_moran_output(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        h = Text(
            self.t("moran_output_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_output(
            kwargs.get("output", self.t("moran_output_text")),
            position=ORIGIN,
        )
        self.wait(max(0.1, duration - 1.2))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_pvalue_caution(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("pvalue_caution_heading", "pvalue_caution_lines", duration)

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_tb(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        code = kwargs.get(
            "code",
            (
                'moran_tb = Moran(main["tb_rate"].values, w, permutations=999)\n'
                'print(f"TB Moran\'s I = {moran_tb.I:.3f}, p = {moran_tb.p_sim:.4f}")\n'
                "# illustrative: significant positive I -> TB clusters spatially too"
            ),
        )
        self._code_block("extra_tb_heading", "extra_tb_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_i_without_p(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "if moran.I > 0.3: cluster = True"),
            kwargs.get("correct_code", "cluster = moran.I > 0.3 and moran.p_sim < 0.05"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_weight_sensitivity(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "w = Queen.from_dataframe(gdf)  # only tested once"),
            kwargs.get("correct_code", "w2 = KNN.from_dataframe(gdf, k=5)  # recheck"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_small_pop_raw_rate(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "moran = Moran(raw_rate, w)"),
            kwargs.get(
                "correct_code", "moran = Moran(main_rate, w)  # drop islands"
            ),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text(self.t("outro_heading"), font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).move_to(
            ORIGIN + UP * 0.5
        )
        s = Text(self.t("outro_sub"), font=FONT_CJK, font_size=20, color=TEXT_SECONDARY).next_to(
            h, DOWN, buff=0.4
        )
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
