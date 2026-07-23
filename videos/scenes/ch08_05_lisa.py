"""Ch08-05: Local LISA — the four quadrants (and the easy-to-misremember .q code)"""

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
    ACCENT_GREEN,
    ACCENT_ORANGE,
    ERROR_RED,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch08LisaScene(EpiBaseScene):
    """Tutorial video scene: Local Moran's I (LISA) quadrants."""

    total_steps: int = 10

    # Bilingual on-screen text — read via self.t(key). zh/en key sets match.
    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title": "局部 LISA 四象限",
            "subtitle": "熱區核心到底藏在哪？",
            "lisa_vs_global_heading": "全域 vs 局部",
            "lisa_vs_global_l1": "全域 Moran's I：整座島一個分數",
            "lisa_vs_global_l2": "局部 LISA：每個縣市一個分數 + p 值",
            "lisa_vs_global_l3": "全域 = 所有局部分數加總",
            "lisa_vs_global_l4": "LISA = Moran's I 的顯微鏡版本",
            "quadrant_heading": "LISA 四象限",
            "axis_x": "自己的率 →",
            "axis_y": "鄰居平均率 ↑",
            "q_hh_label": "震央：自己高、鄰居高",
            "q_lh_label": "颱風眼：自己低、鄰居高",
            "q_ll_label": "淨土：自己低、鄰居低",
            "q_hl_label": "火苗：自己高、鄰居低",
            "q_encoding_heading": ".q 編碼對照表（別憑直覺！）",
            "q_row_1": "1  →  HH（震央）",
            "q_row_2": "2  →  LH（颱風眼）  ⚠ 不是 3！",
            "q_row_3": "3  →  LL（淨土）",
            "q_row_4": "4  →  HL（火苗）",
            "reading_heading": "讀登革熱結果",
            "reading_l1": "臺南 / 高雄 / 嘉義 → HH 震央",
            "reading_l2": "北部縣市 → LL 淨土",
            "reading_l3": "自己不高、被 HH 包圍 → LH 颱風眼",
            "reading_l4": "颱風眼要提前佈署資源",
            "summary_heading": "LISA 四重點",
            "summary_l1": "① 局部 = 全域的顯微鏡版",
            "summary_l2": "② 兩軸：自己的率 × 鄰居平均率",
            "summary_l3": "③ .q：1=HH、2=LH、3=LL、4=HL",
            "summary_l4": "④ 先看 p_sim < 0.05 才解讀",
            "extra_banner": "額外範例：安養機構跨場域 LISA",
            "extra_heading": "把 LISA 縮小到城市尺度",
            "extra_l1": "同縣市十幾家安養機構的侵襲率",
            "extra_l2": "相鄰機構全部 HH → 共用水源嫌疑",
            "extra_l3": "孤立一家 HL → 查自己的蓮蓬頭、熱水塔",
            "extra_l4": "同一招，尺度縮放照樣好用",
            "blindspot_banner": "LISA 地雷 3 選",
            "outro_heading": "下一集：Getis-Ord Gi★ 熱點",
            "outro_sub": "紅外線熱像儀，別只看 Z > 1.96",
        },
        "en": {
            "title": "Local LISA Quadrants",
            "subtitle": "Where is the real hotspot core?",
            "lisa_vs_global_heading": "Global vs Local",
            "lisa_vs_global_l1": "Global Moran's I: one score for the island",
            "lisa_vs_global_l2": "Local LISA: one score + p-value per county",
            "lisa_vs_global_l3": "Global = sum of all local scores",
            "lisa_vs_global_l4": "LISA = the microscope version of Moran's I",
            "quadrant_heading": "The 4 LISA Quadrants",
            "axis_x": "own rate →",
            "axis_y": "neighbor avg ↑",
            "q_hh_label": "Epicenter: self high, neighbors high",
            "q_lh_label": "Eye of storm: self low, neighbors high",
            "q_ll_label": "Safe zone: self low, neighbors low",
            "q_hl_label": "Spark: self high, neighbors low",
            "q_encoding_heading": ".q code table (don't guess!)",
            "q_row_1": "1  →  HH (epicenter)",
            "q_row_2": "2  →  LH (storm eye)  ⚠ not 3!",
            "q_row_3": "3  →  LL (safe zone)",
            "q_row_4": "4  →  HL (spark)",
            "reading_heading": "Reading the dengue result",
            "reading_l1": "Tainan / Kaohsiung / Chiayi → HH epicenter",
            "reading_l2": "Northern counties → LL safe zone",
            "reading_l3": "Self low, surrounded by HH → LH storm eye",
            "reading_l4": "Storm eyes need resources deployed early",
            "summary_heading": "4 LISA Takeaways",
            "summary_l1": "1. Local = microscope version of global",
            "summary_l2": "2. Two axes: own rate x neighbor average",
            "summary_l3": "3. .q: 1=HH, 2=LH, 3=LL, 4=HL",
            "summary_l4": "4. Check p_sim < 0.05 before you interpret",
            "extra_banner": "Extra example: LISA across nursing homes",
            "extra_heading": "Zooming LISA down to city scale",
            "extra_l1": "Attack rate across a dozen nursing homes",
            "extra_l2": "Adjacent homes all HH → shared water source?",
            "extra_l3": "One isolated HL → check its own shower/heater",
            "extra_l4": "Same method, any spatial scale works",
            "blindspot_banner": "3 LISA Blind Spots",
            "outro_heading": "Next up: Getis-Ord Gi* hotspots",
            "outro_sub": "Thermal camera style — don't just use Z > 1.96",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _bullets(self, heading_key: str, line_keys: list[str], duration: float) -> None:
        h = Text(self.t(heading_key), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        bl = VGroup(
            *[Text(self.t(k), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY) for k in line_keys]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(h, DOWN, buff=0.6)
        self.play(FadeIn(h), run_time=0.5)
        self.play(FadeIn(bl, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(h, bl)), run_time=0.5)

    def _code_block(self, heading: str, code: str, duration: float) -> None:
        h = Text(heading, font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).to_edge(UP, buff=0.5)
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_code(code, title="lisa.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def _quad_card(self, label: str, sub_key: str, color: str, pos) -> VGroup:
        card = RoundedRectangle(
            corner_radius=0.12, width=3.0, height=1.5,
            fill_color=ManimColor(color), fill_opacity=0.16,
            stroke_color=ManimColor(color), stroke_width=3,
        )
        title = Text(label, font=FONT_MONO, font_size=28, color=ManimColor(color), weight="BOLD")
        sub = Text(self.t(sub_key), font=FONT_CJK, font_size=16, color=ManimColor(TEXT_PRIMARY))
        content = VGroup(title, sub).arrange(DOWN, buff=0.12)
        content.move_to(card.get_center())
        return VGroup(card, content).move_to(pos)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title"), self.t("subtitle"), duration=duration)

    def show_lisa_vs_global(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            "lisa_vs_global_heading",
            ["lisa_vs_global_l1", "lisa_vs_global_l2", "lisa_vs_global_l3", "lisa_vs_global_l4"],
            duration,
        )

    def show_quadrant_diagram(self, duration: float = 11.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)

        heading = Text(self.t("quadrant_heading"), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE).to_edge(UP, buff=0.7)

        hh = self._quad_card("HH", "q_hh_label", ACCENT_ORANGE, RIGHT * 1.9 + UP * 0.9)
        lh = self._quad_card("LH", "q_lh_label", ACCENT_BLUE, LEFT * 1.9 + UP * 0.9)
        ll = self._quad_card("LL", "q_ll_label", ACCENT_GREEN, LEFT * 1.9 + DOWN * 1.4)
        hl = self._quad_card("HL", "q_hl_label", ERROR_RED, RIGHT * 1.9 + DOWN * 1.4)

        x_label = Text(self.t("axis_x"), font=FONT_CJK, font_size=18, color=ManimColor(TEXT_SECONDARY)).next_to(
            VGroup(ll, hl), DOWN, buff=0.3
        )
        y_label = Text(self.t("axis_y"), font=FONT_CJK, font_size=18, color=ManimColor(TEXT_SECONDARY)).next_to(
            VGroup(lh, hh), UP, buff=0.2
        )

        grid = VGroup(hh, lh, ll, hl)
        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(grid, lag_ratio=0.15), run_time=1.2)
        self.play(FadeIn(x_label), FadeIn(y_label), run_time=0.4)
        self.wait(max(0.1, duration - 2.5))
        self.play(FadeOut(VGroup(heading, grid, x_label, y_label)), run_time=0.5)

    def show_q_encoding(self, duration: float = 10.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)

        heading = Text(self.t("q_encoding_heading"), font=FONT_CJK, font_size=28, color=ERROR_RED).to_edge(UP, buff=0.8)
        rows = VGroup(
            Text(self.t("q_row_1"), font=FONT_MONO, font_size=26, color=ManimColor(TEXT_PRIMARY)),
            Text(self.t("q_row_2"), font=FONT_MONO, font_size=26, color=ManimColor(ERROR_RED), weight="BOLD"),
            Text(self.t("q_row_3"), font=FONT_MONO, font_size=26, color=ManimColor(TEXT_PRIMARY)),
            Text(self.t("q_row_4"), font=FONT_MONO, font_size=26, color=ManimColor(TEXT_PRIMARY)),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.7)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(rows, lag_ratio=0.25), run_time=1.3)
        self.wait(max(0.1, duration - 2.3))
        self.play(FadeOut(VGroup(heading, rows)), run_time=0.5)

    def show_code_lisa(self, duration: float = 11.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._code_block("Moran_Local + .q 對照表", kwargs.get("code", ""), duration)

    def show_reading_result(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            "reading_heading",
            ["reading_l1", "reading_l2", "reading_l3", "reading_l4"],
            duration,
        )

    def show_main_summary(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            "summary_heading",
            ["summary_l1", "summary_l2", "summary_l3", "summary_l4"],
            duration,
        )

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner")), duration=duration)

    def show_extra_nursing_homes(self, duration: float = 10.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets(
            "extra_heading",
            ["extra_l1", "extra_l2", "extra_l3", "extra_l4"],
            duration,
        )

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner")), duration=duration)

    def show_blindspot_encoding(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "labels = {1: 'HH', 2: 'HL', 3: 'LL', 4: 'LH'}"),
            kwargs.get("correct_code", "labels = {1: 'HH', 2: 'LH', 3: 'LL', 4: 'HL'}"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_pfilter(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "main['lisa'] = [labels[q] for q in lisa.q]"),
            kwargs.get("correct_code", "main['lisa'] = [labels[q] if p<.05 else 'ns' for q,p in z]"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_islands(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "lisa = Moran_Local(gdf['rate'].values, w_all)"),
            kwargs.get("correct_code", "lisa = Moran_Local(main['rate'].values, w_mainland)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text(self.t("outro_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text(self.t("outro_sub"), font=FONT_CJK, font_size=22, color=ManimColor(TEXT_SECONDARY)).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
