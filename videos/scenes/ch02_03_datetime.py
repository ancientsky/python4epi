"""Ch02-03: 日期時間大魔王——to_datetime 完全攻略

Manim scene for the tutorial video on pandas datetime operations,
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


class Ch02DatetimeScene(EpiBaseScene):
    """Tutorial video scene: pandas datetime operations with the Legionella outbreak scenario."""

    total_steps: int = 14

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "日期時間大魔王",
            "title_sub": "to_datetime 完全攻略",
            "summary_heading": "日期六大招",
            "summary_p1": "1. pd.to_datetime() 轉換日期型別",
            "summary_p2": "2. errors='coerce' 處理髒資料",
            "summary_p3": "3. .dt accessor 拆出年月日星期",
            "summary_p4": "4. Timedelta 算日期差",
            "summary_p5": "5. isocalendar().week 取流行病學週",
            "summary_p6": "6. strftime() 格式化輸出",
            "extra_banner_title": "額外範例：COVID-19 潛伏期計算",
            "blindspot_banner_title": "日期地雷 3 選",
            "outro_heading": "下一集：衍生變項四大招",
            "outro_sub": "cut, axis, astype, dt 一次學會！",
        },
        "en": {
            "title_main": "The Date-Time Boss Battle",
            "title_sub": "The complete to_datetime playbook",
            "summary_heading": "Six Date Power Moves",
            "summary_p1": "1. pd.to_datetime() converts to a date type",
            "summary_p2": "2. errors='coerce' handles dirty data",
            "summary_p3": "3. .dt accessor pulls out year/month/day/weekday",
            "summary_p4": "4. Timedelta computes date differences",
            "summary_p5": "5. isocalendar().week gets the epidemiological week",
            "summary_p6": "6. strftime() formats the output",
            "extra_banner_title": "Extra example: COVID-19 incubation period",
            "blindspot_banner_title": "3 Date Traps",
            "outro_heading": "Next up: four moves for derived variables",
            "outro_sub": "Learn cut, axis, astype, dt all at once!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the datetime lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_to_datetime(self, duration: float = 7.0, **kwargs) -> None:
        """Step 1: introduce pd.to_datetime()."""
        self.show_step_indicator(1, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "\n"
                "df['symptom_onset_date'] = pd.to_datetime(\n"
                "    df['symptom_onset_date']\n"
                ")\n"
                "print(df['symptom_onset_date'].dtype)"
            ),
        )
        output_text = kwargs.get("output", "datetime64[ns]")

        code_panel = self.show_code(code_text, title="to_datetime.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_errors_coerce(self, duration: float = 6.0, **kwargs) -> None:
        """Step 2: show errors='coerce' for dirty date strings."""
        self.show_step_indicator(2, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# errors='coerce' 把無法轉換的變成 NaT\n"
                "df['onset'] = pd.to_datetime(\n"
                "    df['onset'], errors='coerce'\n"
                ")\n"
                "print(df['onset'].isna().sum())"
            ),
        )

        code_panel = self.show_code(code_text, title="errors_coerce.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_dt_accessor(self, duration: float = 6.0, **kwargs) -> None:
        """Step 3: show .dt accessor for extracting date components."""
        self.show_step_indicator(3, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# .dt 存取器：取出年、月、日、星期\n"
                "df['onset_year']  = df['onset'].dt.year\n"
                "df['onset_month'] = df['onset'].dt.month\n"
                "df['onset_day']   = df['onset'].dt.day\n"
                "df['onset_dow']   = df['onset'].dt.day_name()"
            ),
        )

        code_panel = self.show_code(code_text, title="dt_accessor.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_timedelta(self, duration: float = 6.0, **kwargs) -> None:
        """Step 4: show Timedelta and date arithmetic."""
        self.show_step_indicator(4, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 計算發病到住院的天數\n"
                "df['delay'] = (\n"
                "    df['hospitalization_date']\n"
                "    - df['symptom_onset_date']\n"
                ").dt.days\n"
                "print(df['delay'].median())"
            ),
        )

        code_panel = self.show_code(code_text, title="timedelta.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_epi_week(self, duration: float = 6.0, **kwargs) -> None:
        """Step 5: show isocalendar() for epidemiological week."""
        self.show_step_indicator(5, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 取得 ISO 週數（流行病學常用）\n"
                "df['epi_week'] = (\n"
                "    df['onset'].dt.isocalendar().week\n"
                ")\n"
                "print(df['epi_week'].value_counts().sort_index())"
            ),
        )

        code_panel = self.show_code(code_text, title="epi_week.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_strftime(self, duration: float = 6.0, **kwargs) -> None:
        """Step 6: show strftime for date formatting."""
        self.show_step_indicator(6, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 格式化日期為字串\n"
                "df['onset_str'] = df['onset'].dt.strftime('%Y/%m/%d')\n"
                "print(df['onset_str'].head(3))"
            ),
        )
        output_text = kwargs.get(
            "output",
            (
                "0    2026/01/12\n"
                "1    2026/01/13\n"
                "2    2026/01/14\n"
                "Name: onset_str, dtype: object"
            ),
        )

        code_panel = self.show_code(code_text, title="strftime.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Step 7: summarise the six datetime techniques."""
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
        """COVID-19 incubation period example demonstrating datetime operations."""
        self.show_step_indicator(8, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# COVID-19 潛伏期計算\n"
                "covid['exposure'] = pd.to_datetime(covid['exposure'])\n"
                "covid['onset']    = pd.to_datetime(covid['onset'])\n"
                "\n"
                "covid['incubation'] = (\n"
                "    covid['onset'] - covid['exposure']\n"
                ").dt.days\n"
                "print(covid['incubation'].describe())"
            ),
        )

        code_panel = self.show_code(code_text, title="covid_incubation.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_string_compare(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: comparing date strings vs datetime objects."""
        error_code = kwargs.get("error_code", "df[df['onset'] > '2026-01-20']  # str compare!")
        correct_code = kwargs.get("correct_code", "df[df['onset'] > pd.Timestamp('2026-01-20')]")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_dayfirst(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: dayfirst ambiguity in date parsing."""
        error_code = kwargs.get("error_code", "pd.to_datetime('01/02/2026')  # Jan 2 or Feb 1?")
        correct_code = kwargs.get("correct_code", "pd.to_datetime('01/02/2026', dayfirst=True)")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_dt_days(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: forgetting .dt.days on timedelta."""
        error_code = kwargs.get("error_code", "df['delay'] = df['hosp'] - df['onset']  # Timedelta!")
        correct_code = kwargs.get("correct_code", "df['delay'] = (df['hosp'] - df['onset']).dt.days")
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
