"""Ch08-03: Spatial weights - defining neighbors (Queen vs KNN), row-standardize.

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
    DashedLine,
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
    ACCENT_GREEN,
    ACCENT_ORANGE,
    ERROR_RED,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)

# Schematic "counties on a map" layout for the Queen-adjacency / KNN graphs.
# Purely illustrative positions, not real geography.
_MAIN_NODES = {
    "A": UP * 1.3 + LEFT * 1.0,
    "B": UP * 1.3 + RIGHT * 1.0,
    "C": RIGHT * 1.9 + DOWN * 0.6,
    "D": DOWN * 1.6,
    "E": LEFT * 1.9 + DOWN * 0.6,
}
_QUEEN_EDGES = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "A")]
_ISLAND_POINT = RIGHT * 3.8 + UP * 0.2
_KNN_EDGES = [("ISL", "B"), ("ISL", "C")]


class Ch08SpatialWeightsScene(EpiBaseScene):
    """Tutorial video scene: spatial weights (Queen adjacency vs KNN)."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "空間權重",
            "title_sub": "定義鄰居：Queen 接壤 vs KNN",
            "why_heading": "為什麼要正式定義鄰居？",
            "why_lines": [
                "「近」到底是多近？電腦不會自己猜",
                "先建一張「誰是誰的鄰居」點名表",
                "正式名字：空間權重矩陣 W",
                "→ 這是 Moran's I 的原料",
            ],
            "queen_def_heading": "Queen 接壤",
            "queen_def_caption": "邊界碰到（含一個角）就是鄰居",
            "queen_code_heading": "一行程式建出鄰居點名表",
            "queen_code_title": "queen_weights.py",
            "islands_knn_heading": "離島問題 → 改用 KNN",
            "island_label": "離島（0 鄰居）",
            "knn_caption": "KNN：不管接壤，抓最近的 k 個當鄰居",
            "row_std_heading": "row-standardize：公平投票",
            "row_std_title": "row_standardize.py",
            "summary_heading": "空間權重三重點",
            "summary_lines": [
                "① Queen 接壤：邊界碰到（含角）＝鄰居",
                "② 離島 0 鄰居 → KNN 或聚焦本島",
                "③ row-standardize：鄰居權重加總 = 1",
                "→ W 準備好了，下一集餵給 Moran's I",
            ],
            "extra_banner_title": "額外範例：COVID-19 防疫熱區怎麼分鄰居",
            "extra_covid_heading": "行政區的 Queen 鄰接",
            "extra_covid_title": "covid_zones.py",
            "blindspot_banner_title": "空間權重三個新手地雷",
            "outro_heading": "下一集：全域 Moran's I",
            "outro_sub": "用一個數字回答「有沒有群聚」",
        },
        "en": {
            "title_main": "Spatial Weights",
            "title_sub": "Defining neighbors: Queen adjacency vs KNN",
            "why_heading": 'Why formally define "neighbor"?',
            "why_lines": [
                'How "near" is near? Software won\'t guess for you',
                'Build a roster of "who neighbors whom" first',
                "Formal name: the spatial weights matrix W",
                "-> this is the raw material for Moran's I",
            ],
            "queen_def_heading": "Queen Adjacency",
            "queen_def_caption": "Touching borders (even just a corner) = neighbors",
            "queen_code_heading": "One line builds the whole neighbor roster",
            "queen_code_title": "queen_weights.py",
            "islands_knn_heading": "The Island Problem -> Switch to KNN",
            "island_label": "Offshore island (0 neighbors)",
            "knn_caption": "KNN: forget borders, grab the k nearest as neighbors",
            "row_std_heading": "Row-Standardize: Fair Voting",
            "row_std_title": "row_standardize.py",
            "summary_heading": "Three Takeaways on Spatial Weights",
            "summary_lines": [
                "1. Queen adjacency: touching border (incl. corner) = neighbor",
                "2. Islands with 0 neighbors -> KNN or focus on the mainland",
                "3. row-standardize: neighbor weights sum to 1",
                "-> W is ready, next episode feeds it into Moran's I",
            ],
            "extra_banner_title": "Extra example: COVID-19 alert-zone neighbors",
            "extra_covid_heading": "Queen adjacency for city districts",
            "extra_covid_title": "covid_zones.py",
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: global Moran's I",
            "outro_sub": 'One number answers "is there a real cluster?"',
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

    def _graph(self, nodes: dict, solid_edges: list[tuple[str, str]]) -> VGroup:
        lines = VGroup(
            *[
                Line(nodes[a], nodes[b], color=ManimColor(ACCENT_GREEN), stroke_width=3)
                for a, b in solid_edges
            ]
        )
        dots = VGroup(
            *[Dot(point=p, radius=0.14, color=ManimColor(ACCENT_BLUE)) for p in nodes.values()]
        )
        return VGroup(lines, dots)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_why_neighbors(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("why_heading", "why_lines", duration)

    def show_queen_definition(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        heading = Text(
            self.t("queen_def_heading"), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)
        graph = self._graph(_MAIN_NODES, _QUEEN_EDGES)
        caption = Text(
            self.t("queen_def_caption"), font=FONT_CJK, font_size=20, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(graph), run_time=0.9)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 1.9))
        self.play(FadeOut(VGroup(heading, graph, caption)), run_time=0.5)

    def show_queen_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "from libpysal.weights import Queen, KNN\n"
                "\n"
                "w_all = Queen.from_dataframe(gdf, use_index=False)\n"
                "print(w_all.islands)   # 0-neighbor counties"
            ),
        )
        self._code_block("queen_code_heading", "queen_code_title", code, duration)

    def show_islands_knn(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        heading = Text(
            self.t("islands_knn_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)
        queen_graph = self._graph(_MAIN_NODES, _QUEEN_EDGES)
        island_dot = Dot(point=_ISLAND_POINT, radius=0.14, color=ManimColor(ERROR_RED))
        island_label = Text(
            self.t("island_label"), font=FONT_CJK, font_size=16, color=TEXT_SECONDARY
        ).next_to(island_dot, UP, buff=0.2)
        knn_lines = VGroup(
            *[
                DashedLine(
                    _ISLAND_POINT,
                    _MAIN_NODES[b],
                    color=ManimColor(ACCENT_ORANGE),
                    stroke_width=3,
                )
                for _, b in _KNN_EDGES
            ]
        )
        knn_caption = Text(
            self.t("knn_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(queen_graph), FadeIn(island_dot), FadeIn(island_label), run_time=0.8)
        self.play(FadeIn(knn_lines), FadeIn(knn_caption), run_time=0.8)
        self.wait(max(0.1, duration - 2.5))
        self.play(
            FadeOut(VGroup(heading, queen_graph, island_dot, island_label, knn_lines, knn_caption)),
            run_time=0.5,
        )

    def show_row_standardize(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        code = kwargs.get(
            "code",
            (
                'main = gdf[~gdf["is_inset"]].reset_index(drop=True)\n'
                "w = Queen.from_dataframe(main, use_index=False)\n"
                'w.transform = "r"   # row-standardized'
            ),
        )
        self._code_block("row_std_heading", "row_std_title", code, duration)

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

    def show_extra_covid_zones(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "w_district = Queen.from_dataframe(district_gdf, use_index=False)\n"
                'w_district.transform = "r"\n'
                'alert_neighbors = w_district.neighbors["信義區"]'
            ),
        )
        self._code_block("extra_covid_heading", "extra_covid_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_ignore_islands(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "w = Queen.from_dataframe(gdf)"),
            kwargs.get("correct_code", "w = Queen.from_dataframe(gdf); print(w.islands)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_row_standardize(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "w = Queen.from_dataframe(gdf)  # binary weights only"),
            kwargs.get("correct_code", "w.transform = 'r'  # row-standardize for fair voting"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_random_k(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "w = KNN.from_dataframe(gdf, k=1)"),
            kwargs.get("correct_code", "w = KNN.from_dataframe(gdf, k=5)  # try a few k values"),
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
