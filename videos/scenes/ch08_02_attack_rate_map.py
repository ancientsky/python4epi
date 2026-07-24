"""Ch08-02: Floor x wing attack rate - crosstab to heatmap.

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
    RoundedRectangle,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_ORANGE,
    BORDER_LIGHT,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)

# Illustrative (not real-data) warming palette used to shade the schematic
# floor x wing heatmap grid, coolest to hottest.
_HEAT_COLORS = ["#F5F3EE", "#F7DCC9", "#F0B79A", "#D97757", "#E2624A", "#D94452"]
# Illustrative rank (0=coolest .. 5=hottest) for each (floor, wing) cell.
_HEAT_RANKS = {
    (1, "A"): 0,
    (1, "B"): 2,
    (2, "A"): 1,
    (2, "B"): 5,
    (3, "A"): 3,
    (3, "B"): 4,
}


class Ch08AttackRateMapScene(EpiBaseScene):
    """Tutorial video scene: floor x wing attack rate crosstab and heatmap."""

    total_steps: int = 9

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "樓層 x 翼區侵襲率",
            "title_sub": "crosstab 到熱力圖",
            "setup_flags_heading": "Step 1：建立感染/死亡旗標",
            "setup_flags_title": "flags.py",
            "groupby_agg_heading": "Step 2：groupby + agg 算侵襲率",
            "groupby_agg_title": "spatial_rates.py",
            "pivot_heatmap_heading": "Step 3：pivot + heatmap",
            "pivot_heatmap_title": "heatmap.py",
            "heatmap_caption": "示意：色塊越紅侵襲率越高",
            "sorted_bar_heading": "Step 6：排序條圖找優先順序",
            "sorted_bar_title": "sorted_bar.py",
            "summary_heading": "四步口訣",
            "summary_lines": [
                "① 建旗標：infected / died",
                "② groupby().agg() 算侵襲率",
                "③ pivot() 轉矩陣 → heatmap",
                "④ 排序條圖 + 條件式上色",
            ],
            "extra_banner_title": "額外範例：工廠 COVID-19 群聚",
            "extra_covid_heading": "樓層 x 班別侵襲率",
            "extra_covid_title": "factory_covid.py",
            "blindspot_banner_title": "侵襲率地圖三個新手地雷",
            "outro_heading": "下一集：空間權重",
            "outro_sub": "Queen 接壤 vs KNN、row-standardize",
        },
        "en": {
            "title_main": "Floor x Wing Attack Rate",
            "title_sub": "From crosstab to heatmap",
            "setup_flags_heading": "Step 1: build infected/died flags",
            "setup_flags_title": "flags.py",
            "groupby_agg_heading": "Step 2: groupby + agg for attack rate",
            "groupby_agg_title": "spatial_rates.py",
            "pivot_heatmap_heading": "Step 3: pivot + heatmap",
            "pivot_heatmap_title": "heatmap.py",
            "heatmap_caption": "Illustrative: redder = higher attack rate",
            "sorted_bar_heading": "Step 6: sorted bar for priorities",
            "sorted_bar_title": "sorted_bar.py",
            "summary_heading": "The Four-Step Recipe",
            "summary_lines": [
                "1. Build flags: infected / died",
                "2. groupby().agg() for attack rate",
                "3. pivot() to a matrix -> heatmap",
                "4. sorted bar + conditional color",
            ],
            "extra_banner_title": "Extra example: a factory COVID-19 cluster",
            "extra_covid_heading": "Floor x shift attack rate",
            "extra_covid_title": "factory_covid.py",
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: spatial weights",
            "outro_sub": "Queen vs KNN, row-standardize",
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

    def _heatmap_grid(self, *, cell_w: float = 1.5, cell_h: float = 0.85, gap: float = 0.12):
        """Build a small schematic 3 (floor) x 2 (wing) heatmap grid."""
        floors = [1, 2, 3]
        wings = ["A", "B"]
        group = VGroup()
        for r, floor in enumerate(floors):
            for c, wing in enumerate(wings):
                rank = _HEAT_RANKS[(floor, wing)]
                rect = RoundedRectangle(
                    corner_radius=0.08,
                    width=cell_w,
                    height=cell_h,
                    fill_color=ManimColor(_HEAT_COLORS[rank]),
                    fill_opacity=1,
                    stroke_color=ManimColor(BORDER_LIGHT),
                    stroke_width=1.5,
                )
                label = Text(
                    f"{floor}F-{wing}", font=FONT_MONO, font_size=16, color=ManimColor(TEXT_PRIMARY)
                )
                label.move_to(rect.get_center())
                x = (c - 0.5) * (cell_w + gap)
                y = (1 - r) * (cell_h + gap)
                cell = VGroup(rect, label)
                cell.move_to(RIGHT * x + UP * y)
                group.add(cell)
        return group

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_setup_flags(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        code = kwargs.get(
            "code",
            (
                'df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)\n'
                'df["died"]     = (df["outcome"] == "dead").astype(int)'
            ),
        )
        self._code_block("setup_flags_heading", "setup_flags_title", code, duration)

    def show_groupby_agg(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        code = kwargs.get(
            "code",
            (
                'spatial = df.groupby(["floor", "wing"]).agg(\n'
                '    total    = ("case_id",  "count"),\n'
                '    infected = ("infected", "sum"),\n'
                '    died     = ("died",     "sum"),\n'
                ").reset_index()\n"
                'spatial["attack_rate"] = (spatial["infected"] / spatial["total"] * 100).round(1)\n'
                'spatial["cfr"]         = (spatial["died"] / spatial["infected"] * 100).round(1)'
            ),
        )
        self._code_block("groupby_agg_heading", "groupby_agg_title", code, duration)

    def show_pivot_heatmap(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        code = kwargs.get(
            "code",
            (
                'heatmap_ar = spatial.pivot(index="floor", columns="wing", values="attack_rate")\n'
                'sns.heatmap(heatmap_ar, annot=True, fmt=".1f", cmap="YlOrRd",\n'
                '            cbar_kws={"label": "%"})'
            ),
        )
        h = Text(
            self.t("pivot_heatmap_heading"), font=FONT_CJK, font_size=26, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.5)
        self.play(FadeIn(h), run_time=0.4)
        code_panel = self.show_code(
            code, title=self.t("pivot_heatmap_title"), position=LEFT * 3.3 + DOWN * 0.2
        )
        grid = self._heatmap_grid().move_to(RIGHT * 3.2 + DOWN * 0.2)
        caption = Text(
            self.t("heatmap_caption"), font=FONT_CJK, font_size=16, color=TEXT_SECONDARY
        ).next_to(grid, DOWN, buff=0.3)
        self.play(FadeIn(grid), FadeIn(caption), run_time=0.8)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(h, code_panel, grid, caption)), run_time=0.5)

    def show_sorted_bar(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        code = kwargs.get(
            "code",
            (
                'spatial["label"] = spatial["floor"].astype(str) + "F-" + spatial["wing"]\n'
                'spatial_sorted = spatial.sort_values("attack_rate", ascending=True)\n'
                'ax.barh(spatial_sorted["label"], spatial_sorted["attack_rate"],\n'
                '        color=["#e34a33" if ar > 50 else "#2c7fb8"\n'
                '               for ar in spatial_sorted["attack_rate"]])'
            ),
        )
        self._code_block("sorted_bar_heading", "sorted_bar_title", code, duration)

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_covid(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        code = kwargs.get(
            "code",
            (
                'spatial2 = factory_df.groupby(["floor", "shift"]).agg(\n'
                '    total    = ("worker_id", "count"),\n'
                '    infected = ("infected",  "sum"),\n'
                ").reset_index()\n"
                'spatial2["attack_rate"] = (spatial2["infected"] / spatial2["total"] * 100).round(1)\n'
                'heat2 = spatial2.pivot(index="floor", columns="shift", values="attack_rate")\n'
                'sns.heatmap(heat2, annot=True, fmt=".1f", cmap="YlOrRd")'
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

    def show_blindspot_no_flag(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "ar = grp['clinical_severity'].mean()  # wrong"),
            kwargs.get(
                "correct_code",
                "ar = grp['infected'] / grp['total'] * 100",
            ),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_reset_index(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get(
                "error_code", "g = grp.size()  # floor/wing stay as index"
            ),
            kwargs.get(
                "correct_code",
                "g = grp.size().reset_index()  # cols back",
            ),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_small_n(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "rank_by_attack_rate(spatial)"),
            kwargs.get("correct_code", "rank_by_attack_rate(spatial[spatial['total'] >= 10])"),
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
