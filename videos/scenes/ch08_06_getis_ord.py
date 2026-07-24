"""Ch08-06: Getis-Ord Gi* hotspot analysis (p_sim + sign of Zs, binary weights)"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Circle,
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
    BG_CARD_ALT,
    BORDER_LIGHT,
    ERROR_RED,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
    VariableBox,
)


class Ch08GetisOrdScene(EpiBaseScene):
    """Tutorial video scene: Getis-Ord Gi* hotspot analysis."""

    total_steps: int = 9

    # Bilingual on-screen text — read via self.t(key). zh/en key sets match.
    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title": "Getis-Ord Gi★ 熱點分析",
            "subtitle": "紅外線熱像儀找熱點",
            "gi_vs_lisa_heading": "Gi★ 不是 LISA",
            "gi_vs_lisa_l1": "LISA：跟鄰居像不像（含離群值）",
            "gi_vs_lisa_l2": "Gi★：這一圈燙不燙（只有溫度）",
            "gi_vs_lisa_l3": "輸出 Z 分數：正 = 熱、負 = 冷",
            "gi_vs_lisa_l4": "沒有離群類別，適合畫熱區地圖",
            "binary_heading": "Gi★ 權重：一定要 binary",
            "binary_note": "transform = \"B\"，不做 row-standardize",
            "star_heading": "star=True：把自己算進這一圈",
            "star_note": "Gi 不含自己；Gi★ 含自己，空間流病常用 Gi★",
            "sig_heading": "顯著性判準（別只看 1.96！）",
            "cond_p": "p_sim",
            "cond_p_val": "< 0.05",
            "cond_z": "Zs",
            "cond_z_val": "正 / 負",
            "sig_result": "= 顯著熱點 / 顯著冷點",
            "summary_heading": "Gi★ 五重點",
            "summary_l1": "① 回答「這一圈有多燙」",
            "summary_l2": "② 權重一定用 binary（B）",
            "summary_l3": "③ star=True 含自己",
            "summary_l4": "④ 顯著性看 p_sim < 0.05",
            "summary_l5": "⑤ 冷熱看 Zs 正負號",
            "extra_banner": "額外範例：腸病毒 71 型幼兒園熱區",
            "extra_heading": "Gi★ 換個場景",
            "extra_l1": "各行政區幼兒園群聚率 → Gi★",
            "extra_l2": "熱區常落在通報快速的行政區",
            "extra_l3": "熱點是路標，不是答案",
            "extra_l4": "還要回頭查通報落差 vs 真實傳播",
            "blindspot_banner": "Gi★ 地雷 3 選",
            "outro_heading": "下一集：Choropleth + ID 對齊",
            "outro_sub": "台跟臺的字形陷阱，讓地圖悄悄空白",
        },
        "en": {
            "title": "Getis-Ord Gi* Hotspots",
            "subtitle": "A thermal camera for the map",
            "gi_vs_lisa_heading": "Gi* is not LISA",
            "gi_vs_lisa_l1": "LISA: do you resemble your neighbors (+outliers)",
            "gi_vs_lisa_l2": "Gi*: how hot is this whole window",
            "gi_vs_lisa_l3": "Output Z-score: positive = hot, negative = cold",
            "gi_vs_lisa_l4": "No outlier category — great for hotspot maps",
            "binary_heading": "Gi* weights: must be binary",
            "binary_note": "transform = \"B\", no row-standardizing",
            "star_heading": "star=True: include yourself in the window",
            "star_note": "Gi excludes self; Gi* includes self — spatial epi uses Gi*",
            "sig_heading": "Significance rule (not just 1.96!)",
            "cond_p": "p_sim",
            "cond_p_val": "< 0.05",
            "cond_z": "Zs",
            "cond_z_val": "sign",
            "sig_result": "= significant hot / cold spot",
            "summary_heading": "5 Gi* Takeaways",
            "summary_l1": "1. Answers 'how hot is this window'",
            "summary_l2": "2. Weights must be binary (B)",
            "summary_l3": "3. star=True includes yourself",
            "summary_l4": "4. Significance = p_sim < 0.05",
            "summary_l5": "5. Hot/cold = sign of Zs",
            "extra_banner": "Extra example: enterovirus daycare hotspots",
            "extra_heading": "Gi* in a different outbreak",
            "extra_l1": "Daycare cluster rate per district -> Gi*",
            "extra_l2": "Hotspots often align with fast-reporting districts",
            "extra_l3": "A hotspot is a signpost, not an answer",
            "extra_l4": "Check reporting lag vs real transmission next",
            "blindspot_banner": "3 Gi* Blind Spots",
            "outro_heading": "Next up: Choropleth + ID matching",
            "outro_sub": "The Tai/Tai character trap that silently blanks maps",
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
        panel = self.show_code(code, title="gi_star.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def _heat_grid(self) -> VGroup:
        """A 3x3 county grid with a red ring showing the Gi* 'window'."""
        colors = [
            BG_CARD_ALT, ACCENT_BLUE, BG_CARD_ALT,
            ACCENT_ORANGE, ACCENT_ORANGE, ACCENT_BLUE,
            BG_CARD_ALT, ACCENT_ORANGE, BG_CARD_ALT,
        ]
        cells = VGroup(
            *[
                RoundedRectangle(
                    corner_radius=0.06, width=0.9, height=0.9,
                    fill_color=ManimColor(c), fill_opacity=0.85,
                    stroke_color=ManimColor(BORDER_LIGHT), stroke_width=1.5,
                )
                for c in colors
            ]
        )
        cells.arrange_in_grid(rows=3, cols=3, buff=0.12)
        window = Circle(radius=1.15, color=ManimColor(ERROR_RED), stroke_width=3)
        window.move_to(cells[4].get_center())
        return VGroup(cells, window)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title"), self.t("subtitle"), duration=duration)

    def show_gi_vs_lisa(self, duration: float = 10.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)

        heading = Text(self.t("gi_vs_lisa_heading"), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE).to_edge(UP, buff=0.7)
        grid = self._heat_grid().move_to(LEFT * 3.4)
        bl = VGroup(
            *[
                Text(self.t(k), font=FONT_CJK, font_size=21, color=ManimColor(TEXT_PRIMARY))
                for k in ["gi_vs_lisa_l1", "gi_vs_lisa_l2", "gi_vs_lisa_l3", "gi_vs_lisa_l4"]
            ]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 1.8)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(grid), run_time=0.6)
        self.play(FadeIn(bl, lag_ratio=0.2), run_time=1.0)
        self.wait(max(0.1, duration - 2.5))
        self.play(FadeOut(VGroup(heading, grid, bl)), run_time=0.5)

    def show_binary_weights(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        heading = self.t("binary_heading")
        h = Text(heading, font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).to_edge(UP, buff=0.5)
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_code(kwargs.get("code", ""), title="gi_star.py", position=ORIGIN + UP * 0.3)
        note = Text(self.t("binary_note"), font=FONT_CJK, font_size=20, color=ManimColor(TEXT_SECONDARY)).next_to(
            panel, DOWN, buff=0.5
        )
        self.play(FadeIn(note), run_time=0.4)
        self.wait(max(0.1, duration - 2.3))
        self.play(FadeOut(VGroup(h, panel, note)), run_time=0.5)

    def show_star_meaning(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        h = Text(self.t("star_heading"), font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).to_edge(UP, buff=0.5)
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_code(kwargs.get("code", ""), title="gi_star.py", position=ORIGIN + UP * 0.3)
        note = Text(self.t("star_note"), font=FONT_CJK, font_size=20, color=ManimColor(TEXT_SECONDARY)).next_to(
            panel, DOWN, buff=0.5
        )
        self.play(FadeIn(note), run_time=0.4)
        self.wait(max(0.1, duration - 2.3))
        self.play(FadeOut(VGroup(h, panel, note)), run_time=0.5)

    def show_significance_rule(self, duration: float = 11.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        h = Text(self.t("sig_heading"), font=FONT_CJK, font_size=27, color=ERROR_RED).to_edge(UP, buff=0.6)

        box_p = VariableBox(self.t("cond_p"), self.t("cond_p_val"), width=2.8, height=1.1)
        and_txt = Text("AND", font=FONT_MONO, font_size=22, color=ManimColor(TEXT_SECONDARY))
        box_z = VariableBox(self.t("cond_z"), self.t("cond_z_val"), width=2.8, height=1.1)
        row = VGroup(box_p, and_txt, box_z).arrange(RIGHT, buff=0.4).next_to(h, DOWN, buff=0.6)

        result = Text(self.t("sig_result"), font=FONT_CJK, font_size=24, color=ACCENT_ORANGE).next_to(row, DOWN, buff=0.5)

        self.play(FadeIn(h), run_time=0.4)
        self.play(FadeIn(row, lag_ratio=0.2), run_time=1.0)
        self.play(FadeIn(result), run_time=0.4)

        panel = self.show_code(kwargs.get("code", ""), title="gi_star.py", position=DOWN * 2.3)
        self.wait(max(0.1, duration - 3.5))
        self.play(FadeOut(VGroup(h, row, result, panel)), run_time=0.5)

    def show_main_summary(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            "summary_heading",
            ["summary_l1", "summary_l2", "summary_l3", "summary_l4", "summary_l5"],
            duration,
        )

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner")), duration=duration)

    def show_extra_enterovirus(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
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

    def show_blindspot_zscore_threshold(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "hot = main.loc[gi.Zs > 1.96, 'COUNTYNAME']"),
            kwargs.get("correct_code", "hot = main.loc[gi.p_sim < 0.05, 'COUNTYNAME']"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_row_standardized(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "gi = G_Local(main.rate, w_row_std, star=True)"),
            kwargs.get("correct_code", "gi = G_Local(main.rate, w_binary, star=True)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_ignore_sign(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "hot = main.loc[gi.p_sim < 0.05, 'COUNTYNAME']"),
            kwargs.get("correct_code", "hot = main[(gi.p_sim<.05) & (gi.Zs>0)]"),
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
