"""Ch08-01: Spatial thinking - seating-chart intuition for spatial epidemiology.

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
    FadeIn,
    FadeOut,
    ManimColor,
    Square,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_ORANGE,
    BG_CARD_ALT,
    BORDER_LIGHT,
    ERROR_RED,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)

# Real coughing seats from book/chapters/08_spatial.md's classroom shuffle-test
# demo: a cluster in the back-right corner.
_REAL_COUGH_SEATS = [(3, 3), (3, 4), (4, 3), (4, 4), (2, 4), (4, 2)]
# Illustrative scattered layout used only to show "what shuffled looks like".
_SHUFFLED_COUGH_SEATS = [(0, 0), (1, 3), (2, 1), (3, 0), (0, 4), (4, 4)]


class Ch08SpatialThinkingScene(EpiBaseScene):
    """Tutorial video scene: seating-chart intuition for spatial epidemiology."""

    total_steps: int = 11

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "空間流病超白話",
            "title_sub": "教室咳嗽座位圖 + 洗牌檢定直覺",
            "seating_heading": "後排一角在咳嗽",
            "seating_lines": [
                "後排右下角一小群同學都在咳嗽",
                "傳染串？還是剛好坐得近？",
                "空間流病要回答的就是這件事",
                "→ 感覺很擠 ⟶ 統計上真的擠",
            ],
            "tobler_heading": "Tobler 第一定律",
            "tobler_lines": [
                "近的東西比較像",
                "隔壁同學的感冒、隔壁房的水管",
                "都比對街、對面樓層更相似",
                "→「在哪裡」藏著傳播的線索",
            ],
            "pattern_heading": "看星座的陷阱",
            "pattern_lines": [
                "人腦是台「找圖案的機器」",
                "隨機的星星也能連成獵戶座",
                "看著色地圖，你一定會「看到」群聚",
                "→ 光用眼睛看，還不能下結論",
            ],
            "shuffle_intuition_heading": "洗牌檢定 shuffle test",
            "shuffle_intuition_left_caption": "真實：黏成一團",
            "shuffle_intuition_right_caption": "洗牌後：散開了（示意）",
            "shuffle_intuition_note": "剪下標籤 → 隨機洗牌 → 重貼 → 重複 200 次",
            "shuffle_code_heading": "數「相鄰咳嗽對」",
            "shuffle_code_title": "shuffle_test.py",
            "shuffle_result_heading": "洗牌 200 次的結果",
            "shuffle_result_output": (
                "真實地圖：相鄰咳嗽對 = 6\n"
                "洗牌 200 次：平均 = 2.1（最多 5）\n"
                "p ≈ 0.000 → 這是真的群聚！"
            ),
            "summary_heading": "三個核心概念打包",
            "summary_lines": [
                "① Tobler 定律：近的東西比較像",
                "② 人眼會腦補，看星座不能信",
                "③ 洗牌檢定：把感覺變成證據",
                "→ 這就是 Moran's I 的靈魂",
            ],
            "extra_banner_title": "額外範例：從教室搬到台灣地圖",
            "extra_dengue_heading": "教室 → 台灣縣市",
            "extra_dengue_lines": [
                "座位 → 縣市，咳嗽 → 登革熱發生率",
                "鄰座同學 → 接壤縣市",
                "先算率、洗牌檢定、群聚≠原因",
                "→ 整套邏輯原封不動搬過去",
            ],
            "blindspot_banner_title": "空間思維三個新手地雷",
            "outro_heading": "下一集：樓層翼區侵襲率",
            "outro_sub": "groupby + pivot → 熱力圖",
        },
        "en": {
            "title_main": "Spatial Epi, Plain and Simple",
            "title_sub": "Classroom coughing seats + the shuffle-test intuition",
            "seating_heading": "Coughing in the Back Corner",
            "seating_lines": [
                "A cluster of coughing kids in the back-right corner",
                "A chain of infection - or just coincidence?",
                "This is exactly what spatial epi answers",
                '-> "feels crowded" becomes "statistically crowded"',
            ],
            "tobler_heading": "Tobler's First Law",
            "tobler_lines": [
                "Near things are more alike",
                "Your neighbor's cold, your neighbor's pipes",
                "both resemble you more than someone far away",
                '-> "where" carries clues about transmission',
            ],
            "pattern_heading": "The Constellation Trap",
            "pattern_lines": [
                "Your brain is a pattern-finding machine",
                "Random stars still get connected into Orion",
                'A colored map will always "look" clustered',
                "-> eyeballing alone is not proof",
            ],
            "shuffle_intuition_heading": "The Shuffle Test",
            "shuffle_intuition_left_caption": "Real: clumped together",
            "shuffle_intuition_right_caption": "Shuffled: spread out (illustrative)",
            "shuffle_intuition_note": "Cut labels -> shuffle -> re-paste -> repeat 200 times",
            "shuffle_code_heading": 'Count "adjacent coughing pairs"',
            "shuffle_code_title": "shuffle_test.py",
            "shuffle_result_heading": "Result after 200 shuffles",
            "shuffle_result_output": (
                "Real map: adjacent coughing pairs = 6\n"
                "200 shuffles: mean = 2.1 (max 5)\n"
                "p is about 0.000 -> this is a real cluster!"
            ),
            "summary_heading": "Three Core Ideas",
            "summary_lines": [
                "1. Tobler's law: near things are alike",
                "2. Eyes lie - constellation-style clusters aren't proof",
                "3. Shuffle test: turns a feeling into evidence",
                "-> this is the soul of Moran's I",
            ],
            "extra_banner_title": "Extra example: from classroom to Taiwan map",
            "extra_dengue_heading": "Classroom -> Taiwan counties",
            "extra_dengue_lines": [
                "Seat -> county, cough -> dengue incidence",
                "Neighboring seat -> adjacent county",
                "Rate first, shuffle test, cluster != cause",
                "-> the whole toolkit transfers unchanged",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: floor x wing attack rate",
            "outro_sub": "groupby + pivot -> heatmap",
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

    def _seating_grid(
        self,
        highlighted: list[tuple[int, int]],
        *,
        size: int = 5,
        cell: float = 0.5,
        gap: float = 0.08,
    ):
        group = VGroup()
        offset = (size - 1) / 2
        for r in range(size):
            for c in range(size):
                is_hot = (r, c) in highlighted
                sq = Square(
                    side_length=cell,
                    fill_color=ManimColor(ERROR_RED if is_hot else BG_CARD_ALT),
                    fill_opacity=1,
                    stroke_color=ManimColor(BORDER_LIGHT),
                    stroke_width=1.5,
                )
                x = (c - offset) * (cell + gap)
                y = (offset - r) * (cell + gap)
                sq.move_to(RIGHT * x + UP * y)
                group.add(sq)
        return group

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_seating_scenario(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("seating_heading", "seating_lines", duration)

    def show_toblers_law(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets("tobler_heading", "tobler_lines", duration)

    def show_pattern_trap(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets("pattern_heading", "pattern_lines", duration)

    def show_shuffle_intuition(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            self.t("shuffle_intuition_heading"), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)

        real_grid = self._seating_grid(_REAL_COUGH_SEATS).move_to(LEFT * 3 + DOWN * 0.3)
        shuffled_grid = self._seating_grid(_SHUFFLED_COUGH_SEATS).move_to(RIGHT * 3 + DOWN * 0.3)

        real_caption = Text(
            self.t("shuffle_intuition_left_caption"),
            font=FONT_CJK,
            font_size=18,
            color=TEXT_SECONDARY,
        ).next_to(real_grid, DOWN, buff=0.3)
        shuffled_caption = Text(
            self.t("shuffle_intuition_right_caption"),
            font=FONT_CJK,
            font_size=18,
            color=TEXT_SECONDARY,
        ).next_to(shuffled_grid, DOWN, buff=0.3)

        note = Text(
            self.t("shuffle_intuition_note"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(real_grid), FadeIn(real_caption), run_time=0.8)
        self.play(FadeIn(shuffled_grid), FadeIn(shuffled_caption), run_time=0.8)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(max(0.1, duration - 2.9))
        self.play(
            FadeOut(
                VGroup(heading, real_grid, shuffled_grid, real_caption, shuffled_caption, note)
            ),
            run_time=0.5,
        )

    def show_shuffle_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "import numpy as np\n"
                "\n"
                "seats = np.zeros((5, 5), dtype=int)\n"
                "for r, c in [(3, 3), (3, 4), (4, 3), (4, 4), (2, 4), (4, 2)]:\n"
                "    seats[r, c] = 1\n"
                "\n"
                "def adjacent_cough_pairs(grid):\n"
                "    pairs = 0\n"
                "    for r in range(5):\n"
                "        for c in range(5):\n"
                "            if grid[r, c] == 1:\n"
                "                if c + 1 < 5 and grid[r, c + 1] == 1: pairs += 1\n"
                "                if r + 1 < 5 and grid[r + 1, c] == 1: pairs += 1\n"
                "    return pairs"
            ),
        )
        self._code_block("shuffle_code_heading", "shuffle_code_title", code, duration)

    def show_shuffle_result(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        h = Text(
            self.t("shuffle_result_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_output(
            kwargs.get("output", self.t("shuffle_result_output")),
            position=ORIGIN,
        )
        self.wait(max(0.1, duration - 1.2))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_dengue(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        self._bullets("extra_dengue_heading", "extra_dengue_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_count_vs_rate(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "if cases_wing_a > cases_wing_b: risky = 'A'"),
            kwargs.get("correct_code", "if rate_wing_a > rate_wing_b: risky = 'A'"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_ecological_fallacy(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "if cluster_found: cause = 'shared_water_pipe'"),
            kwargs.get("correct_code", "if cluster_found: investigate_exposures(cluster)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_eyeball_only(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(11, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "cluster = looks_clustered(heatmap)"),
            kwargs.get("correct_code", "cluster = shuffle_test(heatmap, n=1000) < 0.05"),
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
