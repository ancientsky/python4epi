"""Ch02-07: 用 matplotlib 畫出疫調等級的流行曲線

Manim scene for the tutorial video on building publication-quality epidemic
curves with matplotlib, using the Legionella outbreak investigation as the
teaching narrative.
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


class Ch02EpiCurveScene(EpiBaseScene):
    """Tutorial video scene: matplotlib epidemic curves with the Legionella outbreak scenario."""

    total_steps: int = 14

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "matplotlib 流行曲線",
            "title_sub": "從入門到疫調等級",
            "figax_note": "fig = 紙，ax = 框，所有繪圖指令都對 ax 操作",
            "summary_heading": "流行曲線六步口訣",
            "summary_p1": "1. fig, ax = plt.subplots() 建立畫布",
            "summary_p2": "2. value_counts + sort_index 算每日病例",
            "summary_p3": "3. mdates 格式化日期軸",
            "summary_p4": "4. reindex 補零避免斷裂",
            "summary_p5": "5. CDC 風格：方塊長條 + 格線",
            "summary_p6": "6. 標題、軸標籤、tight_layout",
            "extra_banner_title": "額外範例：麻疹群聚流行曲線",
            "blindspot_banner_title": "流行曲線經典坑 3 選",
            "outro_heading": "下一集：seaborn + plotly 速成",
            "outro_sub": "統計圖表一行搞定，互動圖表一鍵放大！",
        },
        "en": {
            "title_main": "matplotlib Epidemic Curves",
            "title_sub": "From basics to investigation-grade",
            "figax_note": "fig = the paper, ax = the frame; every plotting command acts on ax",
            "summary_heading": "The Six-Step Epi-Curve Recipe",
            "summary_p1": "1. fig, ax = plt.subplots() sets up the canvas",
            "summary_p2": "2. value_counts + sort_index counts daily cases",
            "summary_p3": "3. mdates formats the date axis",
            "summary_p4": "4. reindex fills zeros to avoid gaps",
            "summary_p5": "5. CDC style: square bars + gridlines",
            "summary_p6": "6. Title, axis labels, tight_layout",
            "extra_banner_title": "Extra example: measles cluster epi curve",
            "blindspot_banner_title": "3 Classic Epi-Curve Pitfalls",
            "outro_heading": "Next up: seaborn + plotly crash course",
            "outro_sub": "Stat charts in one line, interactive charts one click to zoom!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the epidemic curve lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_fig_ax(self, duration: float = 7.0, **kwargs) -> None:
        """Step 1: introduce fig, ax = plt.subplots()."""
        self.show_step_indicator(1, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "import matplotlib.pyplot as plt\n"
                "\n"
                "fig, ax = plt.subplots(figsize=(10, 4))\n"
                "# fig = 整張紙\n"
                "# ax  = 紙上的畫框"
            ),
        )

        code_panel = self.show_code(code_text, title="fig_ax.py")

        note = Text(
            self.t("figax_note"),
            font=FONT_CJK,
            font_size=20,
            color=TEXT_SECONDARY,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_bar_basic(self, duration: float = 6.0, **kwargs) -> None:
        """Step 2: show basic bar chart for daily case counts."""
        self.show_step_indicator(2, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 每日發病人數\n"
                "daily = df['symptom_onset_date'].value_counts().sort_index()\n"
                "\n"
                "ax.bar(daily.index, daily.values,\n"
                "       width=1, edgecolor='black', linewidth=0.5)"
            ),
        )

        code_panel = self.show_code(code_text, title="bar_basic.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_date_format(self, duration: float = 6.0, **kwargs) -> None:
        """Step 3: show date axis formatting with mdates."""
        self.show_step_indicator(3, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "import matplotlib.dates as mdates\n"
                "\n"
                "ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))\n"
                "ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))\n"
                "fig.autofmt_xdate(rotation=45)"
            ),
        )

        code_panel = self.show_code(code_text, title="date_format.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_reindex_zero(self, duration: float = 6.0, **kwargs) -> None:
        """Step 4: show reindex to fill missing dates with zero."""
        self.show_step_indicator(4, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 補上沒有病例的日期（歸零）\n"
                "all_dates = pd.date_range(\n"
                "    daily.index.min(), daily.index.max()\n"
                ")\n"
                "daily = daily.reindex(all_dates, fill_value=0)"
            ),
        )

        code_panel = self.show_code(code_text, title="reindex_zero.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_cdc_style(self, duration: float = 6.0, **kwargs) -> None:
        """Step 5: apply CDC-style visual tweaks."""
        self.show_step_indicator(5, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# CDC 風格：方塊長條 + 灰色格線\n"
                "ax.bar(daily.index, daily.values,\n"
                "       width=1, color='#4472C4',\n"
                "       edgecolor='black', linewidth=0.5)\n"
                "ax.yaxis.grid(True, linestyle='--', alpha=0.5)\n"
                "ax.set_axisbelow(True)"
            ),
        )

        code_panel = self.show_code(code_text, title="cdc_style.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_title_labels(self, duration: float = 6.0, **kwargs) -> None:
        """Step 6: add title and axis labels."""
        self.show_step_indicator(6, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "ax.set_title('Legionella Outbreak Epi Curve',\n"
                "             fontsize=14, fontweight='bold')\n"
                "ax.set_xlabel('Symptom Onset Date')\n"
                "ax.set_ylabel('Number of Cases')\n"
                "fig.tight_layout()\n"
                "fig.savefig('epi_curve.png', dpi=150)"
            ),
        )

        code_panel = self.show_code(code_text, title="title_labels.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Step 7: summarise the six-step recipe for epidemic curves."""
        self.show_step_indicator(7, self.total_steps)

        heading = Text(
            self.t("summary_heading"),
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("summary_p1"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("summary_p2"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("summary_p3"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("summary_p4"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("summary_p5"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("summary_p6"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.2), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example methods
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the ExtraExampleBanner section divider."""
        banner = ExtraExampleBanner(self.t("extra_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 7.0, **kwargs) -> None:
        """Measles cluster epi curve example."""
        self.show_step_indicator(8, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 麻疹群聚流行曲線\n"
                "measles = pd.read_csv('measles_cluster.csv')\n"
                "measles['onset'] = pd.to_datetime(measles['onset'])\n"
                "\n"
                "daily = measles['onset'].value_counts().sort_index()\n"
                "fig, ax = plt.subplots(figsize=(10, 4))\n"
                "ax.bar(daily.index, daily.values, width=1,\n"
                "       color='#E07B54', edgecolor='black')\n"
                "ax.set_title('Measles Cluster Epi Curve')"
            ),
        )

        code_panel = self.show_code(code_text, title="measles_epicurve.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_save_order(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: savefig before show loses blank image."""
        error_code = kwargs.get("error_code", "plt.show(); fig.savefig('out.png')  # blank file!")
        correct_code = kwargs.get("correct_code", "fig.savefig('out.png'); plt.show()  # save first")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_bar_width(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: bar width for daily data should be 1."""
        error_code = kwargs.get("error_code", "ax.bar(dates, counts, width=0.8)  # gaps between bars")
        correct_code = kwargs.get("correct_code", "ax.bar(dates, counts, width=1)    # no gaps = CDC style")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_dpi(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: low dpi makes fuzzy images."""
        error_code = kwargs.get("error_code", "fig.savefig('curve.png')         # default 100 dpi")
        correct_code = kwargs.get("correct_code", "fig.savefig('curve.png', dpi=150) # crisp for reports")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            self.t("outro_heading"),
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            self.t("outro_sub"),
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
