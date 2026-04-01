"""Ch02-10: Excel 樞紐分析表 — pivot_table 完全攻略

Manim scene for the tutorial video on pandas pivot_table,
using the Legionella outbreak investigation as the teaching narrative.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Text,
    VGroup,
    Write,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_GREEN,
    ACCENT_ORANGE,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    CodePanel,
    ExtraExampleBanner,
    OutputPanel,
    StepIndicator,
)


class Ch02PivotTableScene(EpiBaseScene):
    """Tutorial video scene: pandas pivot_table with the Legionella outbreak scenario."""

    total_steps: int = 14

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the pivot_table lesson."""
        self.show_title_card("Excel 樞紐分析表", "pivot_table 完全攻略", duration=duration)

    def show_excel_analogy(self, duration: float = 7.0, **kwargs) -> None:
        """Step 1: Excel pivot table analogy — mapping fields to parameters."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "Excel \u2194 pandas 對照表",
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        mappings = VGroup(
            Text("列區域  \u2192  index", font=FONT_MONO, font_size=23, color=TEXT_PRIMARY),
            Text("欄區域  \u2192  columns", font=FONT_MONO, font_size=23, color=TEXT_PRIMARY),
            Text("值區域  \u2192  values", font=FONT_MONO, font_size=23, color=TEXT_PRIMARY),
            Text("聚合方式 \u2192  aggfunc", font=FONT_MONO, font_size=23, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        note = Text(
            "四個參數，完全對應 Excel 的四個區塊",
            font=FONT_CJK,
            font_size=20,
            color=TEXT_SECONDARY,
        ).next_to(mappings, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(mappings, lag_ratio=0.3), run_time=1.0)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(duration - 2.0)
        self.play(FadeOut(VGroup(heading, mappings, note)), run_time=0.5)

    def show_pivot_basic(self, duration: float = 6.0, **kwargs) -> None:
        """Step 2: basic pivot_table — attack rate by wing x floor."""
        self.show_step_indicator(2, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "\n"
                "df = pd.read_csv('legionella_outbreak.csv')\n"
                "\n"
                "pd.pivot_table(\n"
                "    df,\n"
                "    values='infected',\n"
                "    index='wing',\n"
                "    columns='floor',\n"
                "    aggfunc='mean',\n"
                ")"
            ),
        )

        output_text = kwargs.get(
            "output",
            (
                "floor      1      2      3\n"
                "wing\n"
                "A       0.38   0.42   0.50\n"
                "B       0.40   0.45   0.48"
            ),
        )

        code_panel = self.show_code(code_text, title="pivot_basic.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_margins(self, duration: float = 6.0, **kwargs) -> None:
        """Step 3: adding margins (subtotals) to pivot_table."""
        self.show_step_indicator(3, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "pd.pivot_table(\n"
                "    df,\n"
                "    values='infected',\n"
                "    index='wing',\n"
                "    columns='floor',\n"
                "    aggfunc='mean',\n"
                "    margins=True,\n"
                "    margins_name='合計',\n"
                ")"
            ),
        )

        code_panel = self.show_code(code_text, title="pivot_margins.py")

        note = Text(
            "margins=True 就像 Excel 的小計功能",
            font=FONT_CJK,
            font_size=20,
            color=TEXT_SECONDARY,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_multiple_aggfunc(self, duration: float = 6.0, **kwargs) -> None:
        """Step 4: multiple aggregation functions at once."""
        self.show_step_indicator(4, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "pd.pivot_table(\n"
                "    df,\n"
                "    values='infected',\n"
                "    index='wing',\n"
                "    columns='floor',\n"
                "    aggfunc=['mean', 'sum', 'count'],\n"
                ")"
            ),
        )

        code_panel = self.show_code(code_text, title="pivot_multi_agg.py")

        note = Text(
            "aggfunc 傳列表 = 一次算多種統計量",
            font=FONT_CJK,
            font_size=20,
            color=ACCENT_ORANGE,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_pivot_vs_groupby(self, duration: float = 6.0, **kwargs) -> None:
        """Step 5: when to use pivot_table vs groupby."""
        self.show_step_indicator(5, self.total_steps)

        heading = Text(
            "pivot_table vs groupby",
            font=FONT_MONO,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        bullets = VGroup(
            Text("groupby  \u2014 一維聚合，適合接續處理（流水線）", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("pivot_table \u2014 二維交叉表，適合報表展示", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("給長官看 \u2192 pivot_table", font=FONT_CJK, font_size=22, color=ACCENT_GREEN),
            Text("接著做更多運算 \u2192 groupby", font=FONT_CJK, font_size=22, color=ACCENT_GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(bullets, lag_ratio=0.25), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, bullets)), run_time=0.5)

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Step 6: summarize key points."""
        self.show_step_indicator(6, self.total_steps)

        heading = Text(
            "重點整理",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("1. index / columns / values / aggfunc 對應 Excel 四區塊", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("2. margins=True 加小計列與小計欄", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("3. aggfunc 可傳列表，一次算多種統計量", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("4. groupby 適合流水線，pivot_table 適合報表", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example methods
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the ExtraExampleBanner section divider."""
        banner = ExtraExampleBanner("額外範例：登革熱各區月份分析")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 7.0, **kwargs) -> None:
        """Dengue district x month pivot_table example."""
        self.show_step_indicator(8, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 登革熱：各行政區 x 月份 病例數\n"
                "dengue_pivot = pd.pivot_table(\n"
                "    dengue_df,\n"
                "    values='cases',\n"
                "    index='district',\n"
                "    columns='month',\n"
                "    aggfunc='sum',\n"
                "    fill_value=0,\n"
                ")\n"
                "print(dengue_pivot)"
            ),
        )

        code_panel = self.show_code(code_text, title="dengue_pivot.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner("pivot_table 三大新手坑")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_no_aggfunc(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: forgetting aggfunc defaults to mean."""
        error_code = kwargs.get("error_code", 'pivot_table(df, values="age", index="floor")')
        correct_code = kwargs.get("correct_code", 'pivot_table(df, values="age", index="floor", aggfunc="count")')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_pivot_vs_pivot_table(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: pivot (no duplicates) vs pivot_table (handles duplicates)."""
        error_code = kwargs.get("error_code", 'df.pivot(index="floor", columns="wing", values="infected")')
        correct_code = kwargs.get("correct_code", 'pd.pivot_table(df, index="floor", columns="wing", values="infected")')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_multiindex(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: accessing MultiIndex columns from multiple aggfunc."""
        error_code = kwargs.get("error_code", 'result["mean"]')
        correct_code = kwargs.get("correct_code", 'result[("mean", "infected")]')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            "下一集：method chaining",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "像串珠子一樣，把操作串成優雅的一行！",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
