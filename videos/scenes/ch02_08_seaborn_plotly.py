"""Ch02-08: seaborn + plotly + 圖表輸出投稿密技

Manim scene for the tutorial video on seaborn visualisation, plotly
interactive charts, and journal-quality figure export, using the
Legionella outbreak investigation as the teaching narrative.
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


class Ch02SeabornPlotlyScene(EpiBaseScene):
    """Tutorial video scene: seaborn, plotly, and figure export for journal submission."""

    total_steps: int = 15

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 4.0, **kwargs) -> None:
        """Title card for the seaborn + plotly lesson."""
        self.show_title_card(
            "seaborn + plotly + 圖表輸出",
            "一行出圖、互動視覺化、投稿密技",
            duration=duration,
        )

    def show_sns_histplot(self, duration: float = 6.0, **kwargs) -> None:
        """Step 1: seaborn histplot for age distribution."""
        self.show_step_indicator(1, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "import seaborn as sns\n"
                'sns.histplot(data=df, x="age", hue="infected",\n'
                '             multiple="stack", bins=10)'
            ),
        )

        code_panel = self.show_code(code_text, title="sns_histplot.py")

        note = Text(
            "hue 自動按感染狀態分色，multiple='stack' 堆疊顯示",
            font=FONT_CJK,
            font_size=20,
            color=TEXT_SECONDARY,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_sns_barplot(self, duration: float = 6.0, **kwargs) -> None:
        """Step 2: seaborn barplot with automatic CI error bars."""
        self.show_step_indicator(2, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                'sns.barplot(data=wing_stats, x="wing", y="attack_rate",\n'
                '            palette="YlOrRd")'
            ),
        )

        code_panel = self.show_code(code_text, title="sns_barplot.py")

        note = Text(
            "seaborn 自動加信賴區間誤差線",
            font=FONT_CJK,
            font_size=20,
            color=ACCENT_ORANGE,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_sns_heatmap(self, duration: float = 6.0, **kwargs) -> None:
        """Step 3: seaborn heatmap for floor x wing attack rates."""
        self.show_step_indicator(3, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                'pivot = df.pivot_table(values="infected", index="floor",\n'
                '                        columns="wing", aggfunc="mean")\n'
                'sns.heatmap(pivot, annot=True, cmap="YlOrRd", fmt=".1%")'
            ),
        )

        code_panel = self.show_code(code_text, title="sns_heatmap.py")

        note = Text(
            "annot=True 顯示數值，cmap 控制色階",
            font=FONT_CJK,
            font_size=20,
            color=TEXT_SECONDARY,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_plotly_bar(self, duration: float = 6.0, **kwargs) -> None:
        """Step 4: plotly express interactive bar chart."""
        self.show_step_indicator(4, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "import plotly.express as px\n"
                'fig = px.bar(daily_df, x="date", y="cases", color="floor",\n'
                '             title="Daily cases by floor")\n'
                "fig.show()"
            ),
        )

        code_panel = self.show_code(code_text, title="plotly_bar.py")

        note = Text(
            "hover 看數值、放大縮小、下載圖片 — 全部內建",
            font=FONT_CJK,
            font_size=20,
            color=ACCENT_GREEN,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_plotly_vs_mpl(self, duration: float = 6.0, **kwargs) -> None:
        """Step 5: imperative (matplotlib) vs declarative (plotly) comparison."""
        self.show_step_indicator(5, self.total_steps)

        heading = Text(
            "matplotlib vs plotly",
            font=FONT_MONO,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        bullets = VGroup(
            Text(
                "matplotlib  — 命令式：一步步告訴它怎麼畫",
                font=FONT_CJK, font_size=22, color=TEXT_PRIMARY,
            ),
            Text(
                "plotly      — 宣告式：告訴它你想要什麼",
                font=FONT_CJK, font_size=22, color=TEXT_PRIMARY,
            ),
            Text(
                "報告精雕 → matplotlib ／探索資料 → plotly",
                font=FONT_CJK, font_size=22, color=TEXT_SECONDARY,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(bullets, lag_ratio=0.3), run_time=1.0)
        self.wait(max(0.1, duration - 2.0))
        self.play(FadeOut(VGroup(heading, bullets)), run_time=0.5)

    def show_savefig(self, duration: float = 6.0, **kwargs) -> None:
        """Step 6: saving figures with high DPI and tight bounding box."""
        self.show_step_indicator(6, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                'fig_mpl.savefig("epi_curve.png", dpi=300, bbox_inches="tight")\n'
                'fig_mpl.savefig("epi_curve.pdf", bbox_inches="tight")'
            ),
        )

        code_panel = self.show_code(code_text, title="savefig.py")

        note = Text(
            "dpi=300 高解析 + bbox_inches='tight' 裁白邊",
            font=FONT_CJK,
            font_size=20,
            color=ACCENT_ORANGE,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_journal_spec(self, duration: float = 7.0, **kwargs) -> None:
        """Step 7: journal figure submission specifications."""
        self.show_step_indicator(7, self.total_steps)

        heading = Text(
            "期刊投稿圖表規格",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        bullets = VGroup(
            Text(
                "NEJM  : >= 1000 DPI (TIFF preferred)",
                font=FONT_MONO, font_size=20, color=TEXT_PRIMARY,
            ),
            Text(
                "Lancet: >= 300 DPI  (EPS / PDF)",
                font=FONT_MONO, font_size=20, color=TEXT_PRIMARY,
            ),
            Text(
                "Font  : Arial / Helvetica only",
                font=FONT_MONO, font_size=20, color=TEXT_PRIMARY,
            ),
            Text(
                "Color : colorblind-safe palette",
                font=FONT_MONO, font_size=20, color=TEXT_PRIMARY,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(bullets, lag_ratio=0.25), run_time=1.2)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(heading, bullets)), run_time=0.5)

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Step 8: lesson summary."""
        self.show_step_indicator(8, self.total_steps)

        heading = Text(
            "重點整理",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(
                "1. seaborn 一行搞定：histplot / barplot / heatmap",
                font=FONT_CJK, font_size=22, color=TEXT_PRIMARY,
            ),
            Text(
                "2. plotly 互動圖表：hover / zoom / download",
                font=FONT_CJK, font_size=22, color=TEXT_PRIMARY,
            ),
            Text(
                "3. savefig 三件套：PDF + dpi=300 + bbox_inches='tight'",
                font=FONT_CJK, font_size=22, color=TEXT_PRIMARY,
            ),
            Text(
                "4. 投稿注意：解析度、字體、色盲友善配色",
                font=FONT_CJK, font_size=22, color=TEXT_PRIMARY,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example methods
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the ExtraExampleBanner section divider."""
        banner = ExtraExampleBanner("額外範例：流感季節趨勢監測")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 7.0, **kwargs) -> None:
        """Step 9: influenza ILI trend with seaborn lineplot + plotly line."""
        self.show_step_indicator(9, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                'sns.lineplot(data=flu, x="epi_week", y="ili_visits",\n'
                '             hue="year", palette="coolwarm")\n'
                'fig = px.line(flu, x="epi_week", y="ili_visits",\n'
                '              color="year", title="ILI trend by year")'
            ),
        )

        code_panel = self.show_code(code_text, title="flu_trend.py")

        note = Text(
            "hue / color 按年份分色，一張圖比較多年趨勢",
            font=FONT_CJK,
            font_size=20,
            color=TEXT_SECONDARY,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner("視覺化經典踩坑 3 選")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_func_name(self, duration: float = 5.0, **kwargs) -> None:
        """Blind spot 1: wrong seaborn function name."""
        error_code = kwargs.get("error_code", 'sns.bindspots(data=df, x="age")')
        correct_code = kwargs.get("correct_code", 'sns.histplot(data=df, x="age")')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_journal_format(self, duration: float = 5.0, **kwargs) -> None:
        """Blind spot 2: missing DPI and bbox_inches for journal submission."""
        error_code = kwargs.get("error_code", 'fig.savefig("f.png")')
        correct_code = kwargs.get(
            "correct_code", 'fig.savefig("f.pdf", dpi=300, bbox_inches="tight")'
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_plotly_name(self, duration: float = 5.0, **kwargs) -> None:
        """Blind spot 3: plotly function name differs from seaborn."""
        error_code = kwargs.get("error_code", 'px.bindspots(df, x="age")')
        correct_code = kwargs.get("correct_code", 'px.histogram(df, x="age")')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card — Ch02 complete."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            "Chapter 02 完成！",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "下一章：描述性統計與二乘二表",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(max(0.1, duration - 1.6))
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
