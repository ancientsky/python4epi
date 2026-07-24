"""Ch08-08: Concept extension — Kulldorff scan statistic + Bayesian smoothing (BYM)"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Circle,
    Create,
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
    BG_CARD_ALT,
    BORDER_LIGHT,
    ERROR_RED,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    ArrowAssignment,
    BlindSpotBanner,
    ExtraExampleBanner,
    VariableBox,
)


class Ch08ScanSmoothingScene(EpiBaseScene):
    """Tutorial video scene: Kulldorff scan statistic + Bayesian smoothing."""

    total_steps: int = 9

    # Bilingual on-screen text — read via self.t(key). zh/en key sets match.
    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title": "掃描統計與貝氏平滑",
            "subtitle": "概念延伸：SaTScan + BYM",
            "small_pop_heading": "小人口率為什麼會暴衝？",
            "pop_label": "連江縣",
            "rate_before": "0 例",
            "rate_after": "7.7 /10萬",
            "small_pop_note": "多 1 例，率就暴衝——分母只有 1.3 萬人",
            "bayes_heading": "貝氏平滑：向鄰居借資訊",
            "bar_before": "平滑前（原始率）",
            "bar_after": "平滑後（借資訊）",
            "scan_heading": "Kulldorff 掃描統計：移動圓圈找群聚",
            "scan_found": "圈內顯著多 → 回報最可能群聚",
            "sig_heading": "顯著性怎麼判？不能查卡方表",
            "mc_sim_label": "999 次模擬統計量",
            "mc_real_label": "真實資料統計量",
            "summary_heading": "掃描 + 平滑四重點",
            "summary_l1": "① 小人口率暴衝，別直接畫圖/排名",
            "summary_l2": "② 貝氏平滑：向鄰居 + 全域借穩定",
            "summary_l3": "③ 掃描統計：移動圓圈，不受邊界限制",
            "summary_l4": "④ 顯著性看蒙地卡羅模擬 p，不是卡方 p",
            "extra_banner": "額外範例：結核病跨鄉鎮群聚掃描",
            "extra_heading": "掃描統計換個病",
            "extra_l1": "結核病傳播常沿通勤路線擴散",
            "extra_l2": "不會乖乖停在行政區邊界",
            "extra_l3": "掃描統計抓到跨鄉鎮不規則熱區",
            "extra_l4": "單一行政區地圖看不出這個型態",
            "blindspot_banner": "掃描與平滑地雷 3 選",
            "outro_heading": "下一章：存活分析",
            "outro_sub": "發病後，誰活得比較久？",
        },
        "en": {
            "title": "Scan Statistics + Bayesian Smoothing",
            "subtitle": "Concept extension: SaTScan + BYM",
            "small_pop_heading": "Why do small-population rates spike?",
            "pop_label": "Lienchiang Cty",
            "rate_before": "0 cases",
            "rate_after": "7.7/100k",
            "small_pop_note": "1 more case sends the rate soaring — denominator is only 13k",
            "bayes_heading": "Bayesian smoothing: borrow from neighbors",
            "bar_before": "before smoothing (raw rate)",
            "bar_after": "after smoothing (borrowed info)",
            "scan_heading": "Kulldorff scan: a moving circle hunts clusters",
            "scan_found": "significantly more inside -> report likely cluster",
            "sig_heading": "How to judge significance? Not a chi-square table",
            "mc_sim_label": "999 simulated statistics",
            "mc_real_label": "real-data statistic",
            "summary_heading": "4 Scan + Smoothing Takeaways",
            "summary_l1": "1. Small-pop rates spike — don't map/rank raw",
            "summary_l2": "2. Bayesian smoothing borrows neighbor + global info",
            "summary_l3": "3. Scan statistic: moving circle, no boundary limits",
            "summary_l4": "4. Significance = Monte Carlo p, not chi-square p",
            "extra_banner": "Extra example: TB cross-township cluster scan",
            "extra_heading": "Scan statistics, a different disease",
            "extra_l1": "TB spread often follows commuting routes",
            "extra_l2": "It doesn't stop neatly at admin boundaries",
            "extra_l3": "The scan catches an irregular cross-township hotspot",
            "extra_l4": "A single-district map would miss this pattern",
            "blindspot_banner": "3 Scan + Smoothing Blind Spots",
            "outro_heading": "Next chapter: survival analysis",
            "outro_sub": "After onset, who survives longer?",
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
        panel = self.show_code(code, title="scan_smooth.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def _bar_pair(self) -> VGroup:
        """Raw (spiky) rate bars vs smoothed (even) rate bars, side by side."""

        def _bars(heights: list[float], color: str) -> VGroup:
            return VGroup(
                *[
                    Rectangle(
                        width=0.4, height=max(0.2, h),
                        fill_color=ManimColor(color), fill_opacity=0.85,
                        stroke_color=ManimColor(BORDER_LIGHT), stroke_width=1,
                    )
                    for h in heights
                ]
            ).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)

        before = _bars([0.3, 2.4, 0.4, 1.9, 0.25], ERROR_RED)
        after = _bars([0.9, 1.3, 1.0, 1.4, 1.1], ACCENT_GREEN)

        before_label = Text(self.t("bar_before"), font=FONT_CJK, font_size=18, color=ManimColor(TEXT_SECONDARY)).next_to(
            before, DOWN, buff=0.25
        )
        after_label = Text(self.t("bar_after"), font=FONT_CJK, font_size=18, color=ManimColor(TEXT_SECONDARY)).next_to(
            after, DOWN, buff=0.25
        )

        before_group = VGroup(before, before_label)
        after_group = VGroup(after, after_label)
        return VGroup(before_group, after_group).arrange(RIGHT, buff=1.1)

    def _cluster_grid(self) -> VGroup:
        """A 4x4 township grid with a 2x2 orange cluster block."""
        colors = [BG_CARD_ALT] * 16
        for i in (5, 6, 9, 10):
            colors[i] = ACCENT_ORANGE
        cells = VGroup(
            *[
                RoundedRectangle(
                    corner_radius=0.05, width=0.75, height=0.75,
                    fill_color=ManimColor(c), fill_opacity=0.85,
                    stroke_color=ManimColor(BORDER_LIGHT), stroke_width=1.2,
                )
                for c in colors
            ]
        )
        cells.arrange_in_grid(rows=4, cols=4, buff=0.1)
        return cells

    def _mc_bars(self) -> VGroup:
        """999 grey simulated-statistic bars vs one tall red real-data bar."""
        heights = [0.3, 0.5, 0.4, 0.6, 0.35, 0.55, 0.45, 0.5, 0.6, 0.4, 0.5, 0.45]
        sim_bars = VGroup(
            *[
                Rectangle(
                    width=0.16, height=h,
                    fill_color=ManimColor(BORDER_LIGHT), fill_opacity=0.95,
                    stroke_width=0,
                )
                for h in heights
            ]
        ).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
        real_bar = Rectangle(
            width=0.22, height=1.5,
            fill_color=ManimColor(ERROR_RED), fill_opacity=0.95,
            stroke_width=0,
        )
        row = VGroup(sim_bars, real_bar).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)

        sim_label = Text(self.t("mc_sim_label"), font=FONT_CJK, font_size=16, color=ManimColor(TEXT_SECONDARY)).next_to(
            sim_bars, DOWN, buff=0.25
        )
        real_label = Text(self.t("mc_real_label"), font=FONT_CJK, font_size=16, color=ManimColor(ERROR_RED)).next_to(
            real_bar, DOWN, buff=0.25
        )
        return VGroup(row, sim_label, real_label)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title"), self.t("subtitle"), duration=duration)

    def show_small_pop_problem(self, duration: float = 10.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)

        heading = Text(self.t("small_pop_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.7
        )
        box_before = VariableBox(self.t("pop_label"), self.t("rate_before"), width=3.0, height=1.2).move_to(LEFT * 3)
        box_after = VariableBox(self.t("pop_label"), self.t("rate_after"), width=3.0, height=1.2).move_to(RIGHT * 3)
        arrow = ArrowAssignment(box_before, box_after)
        note = Text(self.t("small_pop_note"), font=FONT_CJK, font_size=20, color=ManimColor(TEXT_PRIMARY)).next_to(
            VGroup(box_before, box_after), DOWN, buff=0.8
        )

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(box_before), run_time=0.5)
        self.play(Create(arrow), FadeIn(box_after), run_time=0.6)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(max(0.1, duration - 2.5))
        self.play(FadeOut(VGroup(heading, box_before, box_after, arrow, note)), run_time=0.5)

    def show_bayesian_smoothing(self, duration: float = 11.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)

        h = Text(self.t("bayes_heading"), font=FONT_CJK, font_size=27, color=ACCENT_ORANGE).to_edge(UP, buff=0.6)
        bars = self._bar_pair().next_to(h, DOWN, buff=0.7)
        self.play(FadeIn(h), run_time=0.4)
        self.play(FadeIn(bars, lag_ratio=0.1), run_time=0.9)

        panel = self.show_code(kwargs.get("code", ""), title="smoothing.py", position=DOWN * 2.6)
        self.wait(max(0.1, duration - 2.8))
        self.play(FadeOut(VGroup(h, bars, panel)), run_time=0.5)

    def show_kulldorff_scan(self, duration: float = 11.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)

        heading = Text(self.t("scan_heading"), font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).to_edge(UP, buff=0.7)
        grid = self._cluster_grid().move_to(ORIGIN + DOWN * 0.1)
        circle = Circle(radius=0.5, color=ManimColor(ERROR_RED), stroke_width=3)
        circle.move_to(grid[0].get_center())

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(grid), run_time=0.5)
        self.play(Create(circle), run_time=0.4)

        waypoints = [grid[2].get_center(), grid[8].get_center()]
        for pos in waypoints:
            self.play(circle.animate.move_to(pos), run_time=0.5)

        cluster_center = VGroup(grid[5], grid[6], grid[9], grid[10]).get_center()
        self.play(
            circle.animate.move_to(cluster_center).scale(1.6).set_color(ManimColor(ACCENT_ORANGE)),
            run_time=0.8,
        )

        found = Text(self.t("scan_found"), font=FONT_CJK, font_size=20, color=ManimColor(TEXT_PRIMARY)).next_to(
            grid, DOWN, buff=0.5
        )
        self.play(FadeIn(found), run_time=0.4)
        self.wait(max(0.1, duration - 4.1))
        self.play(FadeOut(VGroup(heading, grid, circle, found)), run_time=0.5)

    def show_scan_significance(self, duration: float = 12.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)

        h = Text(self.t("sig_heading"), font=FONT_CJK, font_size=26, color=ERROR_RED).to_edge(UP, buff=0.6)
        mc = self._mc_bars().next_to(h, DOWN, buff=0.8)
        self.play(FadeIn(h), run_time=0.4)
        self.play(FadeIn(mc, lag_ratio=0.05), run_time=1.0)
        self.wait(max(0.1, duration - 1.9))
        self.play(FadeOut(VGroup(h, mc)), run_time=0.5)

    def show_main_summary(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
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

    def show_extra_tb_scan(self, duration: float = 9.0, **kwargs) -> None:
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

    def show_blindspot_raw_small_pop(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "top3 = df.nlargest(3, 'raw_rate')  # noisy"),
            kwargs.get("correct_code", "top3 = df.nlargest(3, 'smooth_rate')  # stable"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_naive_pvalue(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "p = chi2.sf(llr_stat, df=1)"),
            kwargs.get("correct_code", "p = monte_carlo_pvalue(llr_stat, n_sim=999)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_admin_boundary_only(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "cluster = df.groupby('county')['cases'].sum().idxmax()"),
            kwargs.get("correct_code", "cluster = kulldorff_scan(df, max_radius_km=50)"),
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
