"""Ch04-03: Time — 流行曲線

Manim scene for the tutorial video on epidemic curve construction,
using the Legionella outbreak investigation as the teaching narrative.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    UP,
    ORIGIN,
    FadeIn,
    FadeOut,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_ORANGE,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch04TimeScene(EpiBaseScene):
    """Tutorial video scene: epidemic curve (time-based descriptive epi)."""

    total_steps: int = 16

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "流行曲線",
            "title_sub": "用長條圖抓住疫情的脈搏",
            "summary_heading": "重點整理",
            "summary_p1": "1. groupby + size() 計算每日個案數",
            "summary_p2": "2. reindex() 補上沒有個案的日期（填 0）",
            "summary_p3": "3. bar chart 是流行曲線的標準畫法",
            "summary_p4": "4. DateFormatter 讓日期標籤更易讀",
            "summary_p5": "5. idxmax() 快速找到高峰日",
            "extra_banner_title": "額外範例：腸病毒每週流行曲線",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：地點比較",
            "outro_sub": "哪個翼區的侵襲率最高？用數據來說話！",
        },
        "en": {
            "title_main": "The Epidemic Curve",
            "title_sub": "Catch the outbreak's pulse with a bar chart",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. groupby + size() counts cases per day",
            "summary_p2": "2. reindex() fills in the case-free dates (with 0)",
            "summary_p3": "3. A bar chart is the standard epi-curve style",
            "summary_p4": "4. DateFormatter makes date labels easy to read",
            "summary_p5": "5. idxmax() quickly finds the peak day",
            "extra_banner_title": "Extra example: weekly enterovirus epi curve",
            "blindspot_banner_title": "3 Common Beginner Traps",
            "outro_heading": "Next up: comparing places",
            "outro_sub": "Which wing has the highest attack rate? Let the data speak!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the Time lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_groupby_size(self, duration: float = 6.0, **kwargs) -> None:
        """Show groupby + size to count cases per day."""
        self.show_step_indicator(1, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "\n"
                "df = pd.read_csv('legionella_outbreak.csv')\n"
                "df['symptom_onset_date'] = pd.to_datetime(\n"
                "    df['symptom_onset_date']\n"
                ")\n"
                "cases = df[df['case_classification'] == 'confirmed']\n"
                "daily = cases.groupby('symptom_onset_date').size()\n"
                "print(daily.head())"
            ),
        )

        output_text = kwargs.get(
            "output",
            "symptom_onset_date\n2026-01-12    2\n2026-01-13    5\n"
            "2026-01-14    7\n2026-01-15    9\n2026-01-16    11",
        )

        self.show_code(code_lines, title="groupby_size.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_reindex_fill(self, duration: float = 6.0, **kwargs) -> None:
        """Show reindex to fill missing dates with zero."""
        self.show_step_indicator(2, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "all_dates = pd.date_range(\n"
                "    daily.index.min(), daily.index.max()\n"
                ")\n"
                "daily = daily.reindex(all_dates, fill_value=0)\n"
                "print(f'Days covered: {len(daily)}')"
            ),
        )

        self.show_code(code_lines, title="reindex_fill.py")
        self.wait(duration)
        self.clear_screen()

    def show_bar_chart(self, duration: float = 6.0, **kwargs) -> None:
        """Show matplotlib bar chart for the epidemic curve."""
        self.show_step_indicator(3, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "import matplotlib.pyplot as plt\n"
                "\n"
                "fig, ax = plt.subplots(figsize=(10, 4))\n"
                "ax.bar(daily.index, daily.values, color='#D97757')\n"
                "ax.set_xlabel('Symptom Onset Date')\n"
                "ax.set_ylabel('Number of Cases')\n"
                "ax.set_title('Epidemic Curve')\n"
                "plt.tight_layout()\n"
                "plt.show()"
            ),
        )

        self.show_code(code_lines, title="epi_curve.py")
        self.wait(duration)
        self.clear_screen()

    def show_date_formatting(self, duration: float = 6.0, **kwargs) -> None:
        """Show date formatting for x-axis labels."""
        self.show_step_indicator(4, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "import matplotlib.dates as mdates\n"
                "\n"
                "ax.xaxis.set_major_locator(\n"
                "    mdates.DayLocator(interval=2)\n"
                ")\n"
                "ax.xaxis.set_major_formatter(\n"
                "    mdates.DateFormatter('%m/%d')\n"
                ")\n"
                "fig.autofmt_xdate(rotation=45)"
            ),
        )

        self.show_code(code_lines, title="date_format.py")
        self.wait(duration)
        self.clear_screen()

    def show_peak_day(self, duration: float = 6.0, **kwargs) -> None:
        """Show how to identify the peak day."""
        self.show_step_indicator(5, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "peak_date = daily.idxmax()\n"
                "peak_count = daily.max()\n"
                "print(f'Peak: {peak_date.date()} ({peak_count} cases)')"
            ),
        )

        output_text = kwargs.get(
            "output",
            "Peak: 2026-01-20 (15 cases)",
        )

        self.show_code(code_lines, title="peak_day.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key points about epidemic curves."""
        self.show_step_indicator(6, self.total_steps)

        heading = Text(
            self.t("summary_heading"),
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("summary_p1"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("summary_p2"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("summary_p3"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("summary_p4"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("summary_p5"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the ExtraExampleBanner section divider."""
        banner = ExtraExampleBanner(self.t("extra_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_extra_enterovirus(self, duration: float = 6.0, **kwargs) -> None:
        """Enterovirus weekly epidemic curve example."""
        self.show_step_indicator(8, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# Enterovirus: weekly epidemic curve\n"
                "ev = pd.read_csv('enterovirus_cases.csv')\n"
                "ev['onset'] = pd.to_datetime(ev['onset'])\n"
                "ev['epi_week'] = ev['onset'].dt.isocalendar().week\n"
                "weekly = ev.groupby('epi_week').size()\n"
                "weekly.plot.bar(color='#6A9BCC')"
            ),
        )

        self.show_code(code_lines, title="enterovirus_curve.py")
        self.wait(duration)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_gap(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: gaps in epidemic curve from missing dates."""
        error_code = kwargs.get("error_code", "cases.groupby('onset').size().plot.bar()")
        correct_code = kwargs.get("correct_code", "daily.reindex(all_dates, fill_value=0).plot.bar()")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_missing_dates(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: not converting string to datetime."""
        error_code = kwargs.get("error_code", "df.groupby('onset_date').size()  # str index")
        correct_code = kwargs.get("correct_code", "df['onset'] = pd.to_datetime(df['onset_date'])")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_wrong_date(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: using notification_date instead of onset."""
        error_code = kwargs.get("error_code", "df.groupby('notification_date').size()")
        correct_code = kwargs.get("correct_code", "df.groupby('symptom_onset_date').size()")
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
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
