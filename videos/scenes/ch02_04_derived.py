"""Ch02-04: 衍生變項四大招——cut, axis, astype, dt

Manim scene for the tutorial video on creating derived variables in pandas,
using the Legionella outbreak investigation as the teaching narrative.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    UP,
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


class Ch02DerivedScene(EpiBaseScene):
    """Tutorial video scene: creating derived variables with the Legionella outbreak scenario."""

    total_steps: int = 15

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "衍生變項四大招",
            "title_sub": "cut, axis, astype, dt",
            "assign_note": "assign() 回傳新 DataFrame，適合 method chaining",
            "summary_heading": "四大招回顧",
            "summary_p1": "1. pd.cut() 連續變項分組",
            "summary_p2": "2. .sum(axis=1) 橫向加總共病數",
            "summary_p3": "3. .astype() 型別轉換",
            "summary_p4": "4. .dt accessor 拆解日期衍生欄位",
            "extra_banner_title": "額外範例：登革熱嚴重度與就醫延遲",
            "blindspot_banner_title": "衍生變項經典坑 3 選",
            "outro_heading": "下一集：遺漏值偵探社",
            "outro_sub": "NaN, NaT, None 一次搞懂！",
        },
        "en": {
            "title_main": "Four Moves for Derived Variables",
            "title_sub": "cut, axis, astype, dt",
            "assign_note": "assign() returns a new DataFrame, perfect for method chaining",
            "summary_heading": "The Four Moves, Recapped",
            "summary_p1": "1. pd.cut() bins continuous variables",
            "summary_p2": "2. .sum(axis=1) totals comorbidities row-wise",
            "summary_p3": "3. .astype() converts data types",
            "summary_p4": "4. .dt accessor derives fields from dates",
            "extra_banner_title": "Extra example: dengue severity and care delay",
            "blindspot_banner_title": "3 Classic Derived-Variable Traps",
            "outro_heading": "Next up: the Missing-Value Detective Agency",
            "outro_sub": "Master NaN, NaT, None all at once!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the derived variables lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_pd_cut(self, duration: float = 7.0, **kwargs) -> None:
        """Step 1: show pd.cut() for binning continuous variables."""
        self.show_step_indicator(1, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "\n"
                "# 將年齡分組\n"
                "df['age_group'] = pd.cut(\n"
                "    df['age'],\n"
                "    bins=[0, 65, 75, 85, 120],\n"
                "    labels=['<65', '65-74', '75-84', '85+']\n"
                ")\n"
                "print(df['age_group'].value_counts())"
            ),
        )

        self.show_code(code_text, title="pd_cut.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_sum_axis(self, duration: float = 6.0, **kwargs) -> None:
        """Step 2: show .sum(axis=1) for row-wise summation."""
        self.show_step_indicator(2, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 計算每人的共病數（橫向加總）\n"
                "comorbidity_cols = [\n"
                "    'comorbidity_chf', 'comorbidity_dm',\n"
                "    'comorbidity_cancer', 'comorbidity_copd'\n"
                "]\n"
                "df['n_comorbidities'] = df[comorbidity_cols].sum(axis=1)\n"
                "print(df['n_comorbidities'].describe())"
            ),
        )

        self.show_code(code_text, title="sum_axis.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_astype(self, duration: float = 6.0, **kwargs) -> None:
        """Step 3: show .astype() for type conversion."""
        self.show_step_indicator(3, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 把 0/1 整數欄位轉成布林\n"
                "df['is_icu'] = df['icu_admission'].astype(bool)\n"
                "print(df['is_icu'].dtype)\n"
                "print(df['is_icu'].sum())"
            ),
        )
        output_text = kwargs.get("output", "bool\n14")

        self.show_code(code_text, title="astype.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_dt_days(self, duration: float = 6.0, **kwargs) -> None:
        """Step 4: show .dt.days for extracting integer days from timedelta."""
        self.show_step_indicator(4, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 計算住院延遲天數\n"
                "df['hosp_delay'] = (\n"
                "    df['hospitalization_date']\n"
                "    - df['symptom_onset_date']\n"
                ").dt.days\n"
                "print(df['hosp_delay'].median())"
            ),
        )

        self.show_code(code_text, title="dt_days.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_isocalendar(self, duration: float = 6.0, **kwargs) -> None:
        """Step 5: show .dt.isocalendar() for epidemiological week."""
        self.show_step_indicator(5, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 取得 ISO 週數作為衍生變項\n"
                "df['epi_week'] = (\n"
                "    df['symptom_onset_date']\n"
                "    .dt.isocalendar().week\n"
                "    .astype(int)\n"
                ")\n"
                "print(df['epi_week'].value_counts().sort_index())"
            ),
        )

        self.show_code(code_text, title="isocalendar.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_assign(self, duration: float = 6.0, **kwargs) -> None:
        """Step 6: show .assign() for chaining derived columns."""
        self.show_step_indicator(6, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# assign() 一次新增多個衍生欄位\n"
                "df = df.assign(\n"
                "    is_severe = df['clinical_severity'] == 'severe',\n"
                "    is_dead   = df['outcome'] == 'dead',\n"
                ")"
            ),
        )

        self.show_code(code_text, title="assign.py")

        note = Text(
            self.t("assign_note"),
            font=FONT_CJK,
            font_size=20,
            color=TEXT_SECONDARY,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Step 7: summarise the four techniques."""
        self.show_step_indicator(7, self.total_steps)

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
        banner = ExtraExampleBanner(self.t("extra_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 7.0, **kwargs) -> None:
        """Dengue severity and delay example demonstrating derived variables."""
        self.show_step_indicator(8, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 登革熱：嚴重度分組 + 就醫延遲\n"
                "dengue['severity'] = pd.cut(\n"
                "    dengue['platelet_min'],\n"
                "    bins=[0, 50, 100, 500],\n"
                "    labels=['severe', 'warning', 'mild']\n"
                ")\n"
                "dengue['visit_delay'] = (\n"
                "    dengue['visit_date'] - dengue['onset']\n"
                ").dt.days"
            ),
        )

        self.show_code(code_text, title="dengue_derived.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_axis(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: axis=0 vs axis=1 in sum()."""
        error_code = kwargs.get("error_code", "df[cols].sum()         # axis=0: sums each column")
        correct_code = kwargs.get("correct_code", "df[cols].sum(axis=1)   # axis=1: sums each row")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_bins(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: wrong number of labels for pd.cut()."""
        error_code = kwargs.get("error_code", "pd.cut(x, bins=[0,65,85], labels=['A','B','C'])")
        correct_code = kwargs.get("correct_code", "pd.cut(x, bins=[0,65,85], labels=['A','B'])")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_astype(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: astype on column with NaN."""
        error_code = kwargs.get("error_code", "df['x'].astype(int)    # NaN -> ValueError!")
        correct_code = kwargs.get("correct_code", "df['x'].astype('Int64')  # nullable integer OK")
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
