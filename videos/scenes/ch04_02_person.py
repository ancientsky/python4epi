"""Ch04-02: Person — 描述流行病學（人）

Manim scene for the tutorial video on person-based descriptive
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


class Ch04PersonScene(EpiBaseScene):
    """Tutorial video scene: person-based descriptive epidemiology."""

    total_steps: int = 15

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "描述流行病學（人）",
            "title_sub": "感染者的臉譜",
            "summary_heading": "重點整理",
            "summary_p1": "1. 先篩選確診個案再做描述統計",
            "summary_p2": "2. describe() 快速看年齡分布",
            "summary_p3": "3. pd.cut() 建立年齡組別",
            "summary_p4": "4. value_counts() 統計性別與共病",
            "summary_p5": "5. 人的描述 = 年齡 + 性別 + 共病 + 功能狀態",
            "extra_banner_title": "額外範例：登革熱年齡性別分析",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：流行曲線",
            "outro_sub": "用長條圖畫出疫情隨時間的變化！",
        },
        "en": {
            "title_main": "Descriptive Epidemiology (Person)",
            "title_sub": "A portrait of the infected",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. Filter to confirmed cases before describing them",
            "summary_p2": "2. describe() gives a quick look at the age spread",
            "summary_p3": "3. pd.cut() builds the age groups",
            "summary_p4": "4. value_counts() tallies sex and comorbidities",
            "summary_p5": "5. Person = age + sex + comorbidities + functional status",
            "extra_banner_title": "Extra example: dengue age-sex analysis",
            "blindspot_banner_title": "3 Common Beginner Traps",
            "outro_heading": "Next up: the epidemic curve",
            "outro_sub": "Draw how the outbreak changes over time with a bar chart!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the Person lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_filter_cases(self, duration: float = 6.0, **kwargs) -> None:
        """Show filtering confirmed cases."""
        self.show_step_indicator(1, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "\n"
                "df = pd.read_csv('legionella_outbreak.csv')\n"
                "cases = df[df['case_classification'] == 'confirmed']\n"
                "print(f'Confirmed: {len(cases)} / {len(df)}')"
            ),
        )

        output_text = kwargs.get("output", "Confirmed: 121 / 280")

        self.show_code(code_lines, title="filter_cases.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_age_sex(self, duration: float = 6.0, **kwargs) -> None:
        """Show age and sex distribution."""
        self.show_step_indicator(2, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "print(cases['age'].describe())\n"
                "print()\n"
                "print(cases['sex'].value_counts())"
            ),
        )

        output_text = kwargs.get(
            "output",
            "mean    72.3\nstd      9.8\nmin     55.0\nmax     95.0\n\nM    68\nF    53",
        )

        self.show_code(code_lines, title="age_sex.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_age_group(self, duration: float = 6.0, **kwargs) -> None:
        """Show age group binning and crosstab."""
        self.show_step_indicator(3, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "bins = [50, 60, 70, 80, 90, 100]\n"
                "labels = ['50-59','60-69','70-79','80-89','90+']\n"
                "cases['age_group'] = pd.cut(\n"
                "    cases['age'], bins=bins, labels=labels\n"
                ")\n"
                "print(cases['age_group'].value_counts().sort_index())"
            ),
        )

        output_text = kwargs.get(
            "output",
            "50-59     8\n60-69    25\n70-79    48\n80-89    32\n90+       8",
        )

        self.show_code(code_lines, title="age_group.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_comorbidity(self, duration: float = 6.0, **kwargs) -> None:
        """Show comorbidity prevalence among cases."""
        self.show_step_indicator(4, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "comorbidities = ['comorbidity_chf', 'comorbidity_dm',\n"
                "                 'comorbidity_cancer', 'comorbidity_copd']\n"
                "for col in comorbidities:\n"
                "    pct = cases[col].mean() * 100\n"
                "    print(f'{col}: {pct:.1f}%')"
            ),
        )

        output_text = kwargs.get(
            "output",
            "comorbidity_chf:    28.1%\ncomorbidity_dm:     33.9%\n"
            "comorbidity_cancer: 14.0%\ncomorbidity_copd:   22.3%",
        )

        self.show_code(code_lines, title="comorbidity.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key points about person description."""
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

    def show_extra_dengue(self, duration: float = 6.0, **kwargs) -> None:
        """Dengue age-sex example."""
        self.show_step_indicator(7, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# Dengue outbreak: age-sex pyramid\n"
                "dengue = pd.read_csv('dengue_cases.csv')\n"
                "dengue['age_group'] = pd.cut(\n"
                "    dengue['age'],\n"
                "    bins=[0,10,20,30,40,50,60,70,80],\n"
                ")\n"
                "print(pd.crosstab(dengue['age_group'], dengue['sex']))"
            ),
        )

        self.show_code(code_lines, title="dengue_person.py")
        self.wait(duration)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_mean_age(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: reporting mean age without median."""
        error_code = kwargs.get("error_code", "print(f'Mean age: {cases.age.mean():.1f}')")
        correct_code = kwargs.get("correct_code", "print(cases['age'].describe())")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_filter(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: describing all rows instead of confirmed cases."""
        error_code = kwargs.get("error_code", "df['age'].describe()  # all 280 rows")
        correct_code = kwargs.get("correct_code", "cases['age'].describe()  # 121 confirmed")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_sort(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: unsorted age groups."""
        error_code = kwargs.get("error_code", "cases['age_group'].value_counts()")
        correct_code = kwargs.get("correct_code", "cases['age_group'].value_counts().sort_index()")
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
