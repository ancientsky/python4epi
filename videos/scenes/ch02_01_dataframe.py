"""Ch02-01: DataFrame 是什麼？ — 從 CSV 到表格的第一步

Manim scene for the tutorial video on pandas DataFrames, using the
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


class Ch02DataFrameScene(EpiBaseScene):
    """Tutorial video scene: pandas DataFrame basics with the Legionella outbreak scenario."""

    total_steps: int = 14

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "DataFrame 是什麼？",
            "title_sub": "從 CSV 到表格的第一步",
            "analogy_p1": "• 每一列（row）= 一筆資料（一位個案）",
            "analogy_p2": "• 每一欄（column）= 一個欄位（年齡、性別…）",
            "analogy_p3": "• 每欄只能有一種資料型別（數字 or 文字）",
            "series_note": "單一欄位 = Series（一維），整張表 = DataFrame（二維）",
            "summary_heading": "重點整理",
            "summary_p1": "1. pd.read_csv() 讀取 CSV 成 DataFrame",
            "summary_p2": "2. .shape 看維度，.head() 看前幾列",
            "summary_p3": "3. df['col'] 取一欄 → Series",
            "summary_p4": "4. iloc 用位置，loc 用標籤",
            "summary_p5": "5. df[布林條件] 篩選符合條件的列",
            "extra_banner_title": "額外範例：登革熱監測資料",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：info 和 describe 驗貨神器",
            "outro_sub": "讀完資料第一步：先做品質檢查！",
        },
        "en": {
            "title_main": "What Is a DataFrame?",
            "title_sub": "Your first step from CSV to table",
            "analogy_p1": "• Each row = one record (one case)",
            "analogy_p2": "• Each column = one field (age, sex...)",
            "analogy_p3": "• Each column holds one data type (numbers OR text)",
            "series_note": "One column = Series (1D), the whole table = DataFrame (2D)",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. pd.read_csv() loads a CSV into a DataFrame",
            "summary_p2": "2. .shape shows dimensions, .head() peeks at the top rows",
            "summary_p3": "3. df['col'] grabs one column → Series",
            "summary_p4": "4. iloc selects by position, loc selects by label",
            "summary_p5": "5. df[boolean condition] filters the matching rows",
            "extra_banner_title": "Extra example: dengue surveillance data",
            "blindspot_banner_title": "3 Common Beginner Traps",
            "outro_heading": "Next up: info and describe, your QC power tools",
            "outro_sub": "First step after loading data: run a quality check!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the DataFrame lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_excel_analogy(self, duration: float = 5.0, **kwargs) -> None:
        """Show the DataFrame vs Excel analogy with bullet points."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "DataFrame vs Excel",
            font=FONT_MONO,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("analogy_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("analogy_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("analogy_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_read_csv(self, duration: float = 6.0, **kwargs) -> None:
        """Show pd.read_csv() code and its output."""
        self.show_step_indicator(2, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "\n"
                "df = pd.read_csv('legionella_outbreak.csv')\n"
                "print(type(df))"
            ),
        )

        output_text = kwargs.get("output", "<class 'pandas.core.frame.DataFrame'>")

        code_panel = self.show_code(code_lines, title="read_csv.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_shape_head(self, duration: float = 6.0, **kwargs) -> None:
        """Show .shape and .head() usage."""
        self.show_step_indicator(3, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "print(df.shape)    # (列數, 欄數)\n"
                "print(df.head(3))  # 前 3 列"
            ),
        )

        output_text = kwargs.get(
            "output",
            "(280, 32)\n   case_id  age sex  floor  ...\n0    C001   82   M      3  ...\n1    C002   75   F      2  ...\n2    C003   68   M      1  ...",
        )

        code_panel = self.show_code(code_lines, title="shape_head.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_columns(self, duration: float = 6.0, **kwargs) -> None:
        """Show column access and Series concept."""
        self.show_step_indicator(4, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# 取出單一欄位 → 回傳 Series\n"
                "ages = df['age']\n"
                "print(type(ages))\n"
                "print(ages.head())"
            ),
        )

        output_text = kwargs.get(
            "output",
            "<class 'pandas.core.series.Series'>\n0    82\n1    75\n2    68\n3    91\n4    70\nName: age, dtype: int64",
        )

        note = Text(
            self.t("series_note"),
            font=FONT_CJK,
            font_size=20,
            color=TEXT_SECONDARY,
        ).to_edge(UP, buff=0.7)

        self.play(FadeIn(note), run_time=0.5)
        code_panel = self.show_code(code_lines, title="columns.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.5)
        self.clear_screen()

    def show_iloc_loc(self, duration: float = 6.0, **kwargs) -> None:
        """Show iloc vs loc for row/column selection."""
        self.show_step_indicator(5, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# iloc: 用位置索引（整數）\n"
                "print(df.iloc[0, 1])     # 第 0 列, 第 1 欄\n"
                "\n"
                "# loc: 用標籤索引\n"
                "print(df.loc[0, 'age'])  # 第 0 列, 'age' 欄"
            ),
        )

        output_text = kwargs.get("output", "82\n82")

        note = Text(
            "iloc = integer location, loc = label location",
            font=FONT_MONO,
            font_size=22,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.7)

        self.play(FadeIn(note), run_time=0.5)
        code_panel = self.show_code(code_lines, title="iloc_vs_loc.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.5)
        self.clear_screen()

    def show_boolean_filter(self, duration: float = 6.0, **kwargs) -> None:
        """Show boolean filtering on the DataFrame."""
        self.show_step_indicator(6, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# 篩選死亡個案\n"
                "dead = df[df['outcome'] == 'dead']\n"
                "print(len(dead))  # 死亡人數\n"
                "print(dead['age'].mean())  # 平均年齡"
            ),
        )

        output_text = kwargs.get("output", "19\n81.4")

        code_panel = self.show_code(code_lines, title="boolean_filter.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key points about DataFrames."""
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
            Text(self.t("summary_p5"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40).next_to(heading, DOWN, buff=0.6)

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

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        """Dengue surveillance example demonstrating DataFrame operations."""
        self.show_step_indicator(8, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# 登革熱每週通報資料\n"
                "dengue = pd.read_csv('dengue_weekly.csv')\n"
                "print(dengue.shape)\n"
                "\n"
                "# 篩選台南市的病例\n"
                "tainan = dengue[dengue['county'] == 'Tainan']\n"
                "print(f'台南市病例數: {len(tainan)}')"
            ),
        )

        code_panel = self.show_code(code_lines, title="dengue_df.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_case(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: column name case sensitivity."""
        error_code = kwargs.get("error_code", "df['Age']   # KeyError: column is 'age'")
        correct_code = kwargs.get("correct_code", "df['age']   # column names are case-sensitive")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_slice(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: slice vs head for preview."""
        error_code = kwargs.get("error_code", "print(df)       # prints ALL 280 rows!")
        correct_code = kwargs.get("correct_code", "print(df.head())  # only first 5 rows")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_double_brackets(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: single vs double brackets for column selection."""
        error_code = kwargs.get("error_code", "df['age','sex']   # KeyError: use [[]]")
        correct_code = kwargs.get("correct_code", "df[['age','sex']]  # double brackets = DataFrame")
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
