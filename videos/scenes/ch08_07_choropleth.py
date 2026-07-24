"""Ch08-07: Per-100k choropleth — geopandas merge and Tai/Tai ID alignment"""

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
    Rectangle,
    RoundedRectangle,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_GREEN,
    ACCENT_ORANGE,
    BORDER_LIGHT,
    ERROR_RED,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch08ChoroplethScene(EpiBaseScene):
    """Tutorial video scene: per-100k choropleth, merge, and ID alignment."""

    total_steps: int = 11

    # Bilingual on-screen text — read via self.t(key). zh/en key sets match.
    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title": "每十萬人發生率 Choropleth",
            "subtitle": "merge 和 ID 對齊全攻略",
            "what_heading": "Choropleth 是什麼？",
            "what_l1": "分級著色地圖：顏色深淺 = 數值高低",
            "what_l2": "需要兩份資料：地圖 SHP + 疫情表",
            "what_l3": "靠縣市名稱 merge 在一起",
            "what_l4": "陷阱就藏在「靠名稱」這件事",
            "trap_heading": "台 ≠ 臺 陷阱",
            "trap_wrong": "台北市",
            "trap_right": "臺北市",
            "trap_result": "merge 找不到 → 地圖悄悄空白",
            "normalize_heading": "解法：正規化字典",
            "diff_heading": "merge 前先做集合差檢查",
            "rate_heading": "換算每十萬人發生率",
            "plot_heading": "merge + plot 一次上色",
            "legend_low": "低",
            "legend_high": "高",
            "summary_heading": "Choropleth 五步總結",
            "summary_l1": "① 靠縣市名稱 merge 地圖與資料",
            "summary_l2": "② 台/臺不一致是頭號陷阱",
            "summary_l3": "③ merge 前印出集合差確認",
            "summary_l4": "④ 一定換算每十萬人發生率",
            "summary_l5": "⑤ how='left' 保留所有地圖邊界",
            "extra_banner": "額外範例：登革熱鄉鎮發生率地圖",
            "extra_heading": "縮小到鄉鎮尺度",
            "extra_l1": "登革熱常畫到鄉鎮市區層級",
            "extra_l2": "同名鄉鎮更常見（中山區、大同區…）",
            "extra_l3": "merge key 要用「縣市+鄉鎮」組合",
            "extra_l4": "單用鄉鎮名稱對，會對錯地方",
            "blindspot_banner": "Choropleth 地雷 3 選",
            "outro_heading": "下一集：掃描統計與貝氏平滑",
            "outro_sub": "小縣市率忽高忽低，怎麼辦？",
        },
        "en": {
            "title": "Per-100k Choropleth",
            "subtitle": "Merge and ID alignment, start to finish",
            "what_heading": "What is a choropleth?",
            "what_l1": "Shaded map: color depth = value magnitude",
            "what_l2": "Needs two datasets: boundary SHP + case table",
            "what_l3": "Joined together by county name",
            "what_l4": "The trap hides in that 'join by name' step",
            "trap_heading": "The Tai vs Tai trap",
            "trap_wrong": "台北市 (informal)",
            "trap_right": "臺北市 (official)",
            "trap_result": "merge misses it -> map silently goes blank",
            "normalize_heading": "Fix: a normalization dict",
            "diff_heading": "Set-difference check before merging",
            "rate_heading": "Convert to rate per 100k",
            "plot_heading": "merge + plot colors it in one line",
            "legend_low": "low",
            "legend_high": "high",
            "summary_heading": "5-Step Choropleth Recipe",
            "summary_l1": "1. Join map and data by county name",
            "summary_l2": "2. Tai/Tai mismatch is the #1 trap",
            "summary_l3": "3. Print the set difference before merging",
            "summary_l4": "4. Always convert to rate per 100k",
            "summary_l5": "5. how='left' keeps every map boundary",
            "extra_banner": "Extra example: dengue township rate map",
            "extra_heading": "Zooming to township scale",
            "extra_l1": "Dengue is often mapped at township level",
            "extra_l2": "Duplicate township names are common",
            "extra_l3": "Merge key must be county + township combined",
            "extra_l4": "Township name alone will mismatch",
            "blindspot_banner": "3 Choropleth Blind Spots",
            "outro_heading": "Next up: scan statistics and Bayesian smoothing",
            "outro_sub": "What to do when small-county rates whipsaw",
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
        panel = self.show_code(code, title="choropleth.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def _legend_bar(self) -> VGroup:
        """A 5-swatch red gradient bar mimicking cmap='Reds', low -> high."""
        opacities = [0.15, 0.35, 0.55, 0.75, 0.95]
        swatches = VGroup(
            *[
                Rectangle(
                    width=0.9, height=0.6,
                    fill_color=ManimColor(ERROR_RED), fill_opacity=op,
                    stroke_color=ManimColor(BORDER_LIGHT), stroke_width=1,
                )
                for op in opacities
            ]
        ).arrange(RIGHT, buff=0.05)
        low = Text(self.t("legend_low"), font=FONT_CJK, font_size=18, color=ManimColor(TEXT_SECONDARY)).next_to(
            swatches, LEFT, buff=0.25
        )
        high = Text(self.t("legend_high"), font=FONT_CJK, font_size=18, color=ManimColor(TEXT_SECONDARY)).next_to(
            swatches, RIGHT, buff=0.25
        )
        return VGroup(low, swatches, high)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title"), self.t("subtitle"), duration=duration)

    def show_what_is_choropleth(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            "what_heading",
            ["what_l1", "what_l2", "what_l3", "what_l4"],
            duration,
        )

    def show_tai_trap(self, duration: float = 11.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)

        heading = Text(self.t("trap_heading"), font=FONT_CJK, font_size=28, color=ERROR_RED).to_edge(UP, buff=0.7)

        wrong_card = RoundedRectangle(
            corner_radius=0.12, width=3.2, height=1.1,
            fill_color=ManimColor("#FDF0F0"), fill_opacity=1,
            stroke_color=ManimColor(ERROR_RED), stroke_width=2,
        )
        wrong_txt = Text(self.t("trap_wrong"), font=FONT_CJK, font_size=26, color=ManimColor(ERROR_RED)).move_to(
            wrong_card.get_center()
        )
        wrong_group = VGroup(wrong_card, wrong_txt)

        neq = Text("≠", font=FONT_MONO, font_size=36, color=ManimColor(TEXT_SECONDARY))

        right_card = RoundedRectangle(
            corner_radius=0.12, width=3.2, height=1.1,
            fill_color=ManimColor("#F0F5EC"), fill_opacity=1,
            stroke_color=ManimColor(ACCENT_GREEN), stroke_width=2,
        )
        right_txt = Text(self.t("trap_right"), font=FONT_CJK, font_size=26, color=ManimColor(ACCENT_GREEN)).move_to(
            right_card.get_center()
        )
        right_group = VGroup(right_card, right_txt)

        row = VGroup(wrong_group, neq, right_group).arrange(RIGHT, buff=0.5).next_to(heading, DOWN, buff=0.7)

        result = Text(self.t("trap_result"), font=FONT_CJK, font_size=22, color=ManimColor(TEXT_PRIMARY)).next_to(
            row, DOWN, buff=0.6
        )

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(row, lag_ratio=0.2), run_time=1.0)
        self.play(FadeIn(result), run_time=0.5)
        self.wait(max(0.1, duration - 2.4))
        self.play(FadeOut(VGroup(heading, row, result)), run_time=0.5)

    def show_normalize_code(self, duration: float = 11.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block(self.t("normalize_heading"), kwargs.get("code", ""), duration)

    def show_id_diff_check(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._code_block(self.t("diff_heading"), kwargs.get("code", ""), duration)

    def show_rate_per_100k(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._code_block(self.t("rate_heading"), kwargs.get("code", ""), duration)

    def show_plot_choropleth(self, duration: float = 10.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)

        h = Text(self.t("plot_heading"), font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).to_edge(UP, buff=0.5)
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_code(kwargs.get("code", ""), title="choropleth.py", position=UP * 0.3)
        legend = self._legend_bar().next_to(panel, DOWN, buff=0.6)
        self.play(FadeIn(legend), run_time=0.4)
        self.wait(max(0.1, duration - 2.3))
        self.play(FadeOut(VGroup(h, panel, legend)), run_time=0.5)

    def show_main_summary(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
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

    def show_extra_dengue(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
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

    def show_blindspot_no_normalize(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "gdf.merge(df, on='county')  # raw names"),
            kwargs.get("correct_code", "gdf.merge(df, on='county_norm')  # cleaned"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_raw_count(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "gdf_merged.plot(column='cases', cmap='Reds')"),
            kwargs.get("correct_code", "gdf_merged.plot(column='rate_per_100k', cmap='Reds')"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_diff_check(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(11, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "merged = gdf.merge(df, how='left'); merged.plot()"),
            kwargs.get("correct_code", "print(shp_ids - data_ids)  # diff first"),
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
