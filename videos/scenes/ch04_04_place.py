"""Ch04-04: Place — 地點比較

Manim scene for the tutorial video on place-based descriptive
epidemiology, using the Legionella outbreak investigation.
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


class Ch04PlaceScene(EpiBaseScene):
    """Tutorial video scene: place-based descriptive epidemiology."""

    total_steps: int = 15

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "地點比較",
            "title_sub": "哪個翼區最危險？",
            "summary_heading": "重點整理",
            "summary_p1": "1. groupby + agg 同時算多個統計量",
            "summary_p2": "2. 侵襲率 = 個案數 / 該區總人數",
            "summary_p3": "3. 比較各翼區找出高風險地點",
            "summary_p4": "4. reset_index() 讓 groupby 結果變回 DataFrame",
            "summary_p5": "5. 地點分析是擬定防治策略的關鍵依據",
            "extra_banner_title": "額外範例：COVID-19 各縣市侵襲率",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：個案分類",
            "outro_sub": "確診、可能、非個案——分層統計怎麼做？",
        },
        "en": {
            "title_main": "Comparing Places",
            "title_sub": "Which wing is the most dangerous?",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. groupby + agg computes several stats at once",
            "summary_p2": "2. Attack rate = cases / total residents in that area",
            "summary_p3": "3. Compare wings to find the high-risk locations",
            "summary_p4": "4. reset_index() turns the groupby result back into a DataFrame",
            "summary_p5": "5. Place analysis is the key basis for control strategy",
            "extra_banner_title": "Extra example: COVID-19 attack rate by county",
            "blindspot_banner_title": "3 Common Beginner Traps",
            "outro_heading": "Next up: case classification",
            "outro_sub": "Confirmed, probable, non-case - how do we stratify?",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the Place lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_groupby_agg(self, duration: float = 6.0, **kwargs) -> None:
        """Show groupby + agg to compute wing-level stats."""
        self.show_step_indicator(1, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "\n"
                "df = pd.read_csv('legionella_outbreak.csv')\n"
                "wing_stats = df.groupby('wing').agg(\n"
                "    total=('case_id', 'size'),\n"
                "    cases=('case_classification',\n"
                "           lambda x: (x == 'confirmed').sum()),\n"
                ")"
            ),
        )

        self.show_code(code_lines, title="groupby_agg.py")
        self.wait(duration)
        self.clear_screen()

    def show_attack_rate_calc(self, duration: float = 6.0, **kwargs) -> None:
        """Show attack rate calculation per wing."""
        self.show_step_indicator(2, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "wing_stats['attack_rate'] = (\n"
                "    wing_stats['cases'] / wing_stats['total']\n"
                ")\n"
                "wing_stats['ar_pct'] = (\n"
                "    wing_stats['attack_rate'] * 100\n"
                ").round(1)"
            ),
        )

        self.show_code(code_lines, title="attack_rate.py")
        self.wait(duration)
        self.clear_screen()

    def show_print_table(self, duration: float = 6.0, **kwargs) -> None:
        """Show the wing comparison table."""
        self.show_step_indicator(3, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "print(wing_stats[['total','cases','ar_pct']])"
            ),
        )

        output_text = kwargs.get(
            "output",
            "      total  cases  ar_pct\nwing\n"
            "A        70     38    54.3\n"
            "B        70     32    45.7\n"
            "C        70     28    40.0\n"
            "D        70     23    32.9",
        )

        self.show_code(code_lines, title="print_table.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_reset_index(self, duration: float = 6.0, **kwargs) -> None:
        """Show reset_index for downstream usage."""
        self.show_step_indicator(4, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "wing_df = wing_stats.reset_index()\n"
                "print(wing_df.columns.tolist())\n"
                "# ['wing', 'total', 'cases', 'attack_rate', 'ar_pct']"
            ),
        )

        self.show_code(code_lines, title="reset_index.py")
        self.wait(duration)
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key points about place comparison."""
        self.show_step_indicator(5, self.total_steps)

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

    def show_extra_covid_county(self, duration: float = 6.0, **kwargs) -> None:
        """COVID-19 county-level attack rate example."""
        self.show_step_indicator(7, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# COVID-19: attack rate by county\n"
                "covid = pd.read_csv('covid_county.csv')\n"
                "county = covid.groupby('county').agg(\n"
                "    pop=('pop', 'first'),\n"
                "    cases=('confirmed', 'sum'),\n"
                ")\n"
                "county['ar_per_100k'] = (\n"
                "    county['cases'] / county['pop'] * 100_000\n"
                ").round(1)\n"
                "print(county.sort_values('ar_per_100k', ascending=False))"
            ),
        )

        self.show_code(code_lines, title="covid_county.py")
        self.wait(duration)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_reset(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: forgetting reset_index after groupby."""
        error_code = kwargs.get("error_code", "wing_stats['wing']  # KeyError!")
        correct_code = kwargs.get("correct_code", "wing_stats.reset_index()['wing']  # OK")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_size_count(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: confusing size() vs count()."""
        error_code = kwargs.get("error_code", "df.groupby('wing').count()  # all columns")
        correct_code = kwargs.get("correct_code", "df.groupby('wing').size()  # one Series")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_rate(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: reporting raw counts without rates."""
        error_code = kwargs.get("error_code", "print(f'Wing A: {38} cases')")
        correct_code = kwargs.get("correct_code", "print(f'Wing A: 38/70 = 54.3%')")
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
