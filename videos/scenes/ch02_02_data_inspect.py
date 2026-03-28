"""Ch02-02: 一分鐘看懂你的資料 — info() 與 describe()

Manim scene for the tutorial video on DataFrame inspection methods,
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


class Ch02DataInspectScene(EpiBaseScene):
    """Tutorial video scene: DataFrame inspection with info() and describe()."""

    total_steps: int = 13

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the data inspection lesson."""
        self.show_title_card("一分鐘看懂你的資料", "info() 與 describe()", duration=duration)

    def show_info(self, duration: float = 6.0, **kwargs) -> None:
        """Show df.info() code and sample output."""
        self.show_step_indicator(1, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "\n"
                "df = pd.read_csv('legionella_outbreak.csv')\n"
                "df.info()"
            ),
        )

        output_text = kwargs.get(
            "output",
            (
                "<class 'pandas.core.frame.DataFrame'>\n"
                "RangeIndex: 280 entries, 0 to 279\n"
                "Data columns (total 32 columns)\n"
                " #  Column    Non-Null Count  Dtype\n"
                " 0  case_id   280 non-null     object\n"
                " 1  age       280 non-null     int64\n"
                " 2  sex       280 non-null     object\n"
                "..."
            ),
        )

        code_panel = self.show_code(code_lines, title="info_demo.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_dtypes(self, duration: float = 5.0, **kwargs) -> None:
        """Show common dtypes with bullet points."""
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            "常見資料型別（dtype）",
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• int64    — 整數（如 age, floor）", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• float64  — 浮點數（如 temperature）", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• object   — 文字 / 混合型（如 sex, outcome）", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• datetime64 — 日期時間（需要轉換才會出現）", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_describe(self, duration: float = 6.0, **kwargs) -> None:
        """Show df.describe() code and output."""
        self.show_step_indicator(3, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# 數值欄位的摘要統計\n"
                "df.describe()"
            ),
        )

        output_text = kwargs.get(
            "output",
            (
                "         age       floor\n"
                "count  280.0      280.0\n"
                "mean    76.3        2.0\n"
                "std      9.8        0.8\n"
                "min     60.0        1.0\n"
                "25%     69.0        1.0\n"
                "50%     76.0        2.0\n"
                "75%     84.0        3.0\n"
                "max     95.0        3.0"
            ),
        )

        code_panel = self.show_code(code_lines, title="describe_demo.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_describe_interpret(self, duration: float = 5.0, **kwargs) -> None:
        """Show how to interpret describe() output."""
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            "describe() 怎麼看？",
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• count — 有多少筆非空值（檢查遺漏）", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("• mean / std — 平均值與標準差（看分布）", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("• min, 25%, 50%, 75%, max — 五數摘要", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("• min vs max 差太大？可能有離群值", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_value_counts(self, duration: float = 6.0, **kwargs) -> None:
        """Show value_counts() for categorical columns."""
        self.show_step_indicator(5, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# 類別欄位的次數分布\n"
                "print(df['outcome'].value_counts())\n"
                "print()\n"
                "print(df['clinical_severity'].value_counts())"
            ),
        )

        output_text = kwargs.get(
            "output",
            (
                "survived    261\n"
                "dead         19\n"
                "Name: outcome, dtype: int64\n"
                "\n"
                "not_ill       159\n"
                "mild           48\n"
                "moderate       38\n"
                "severe         35\n"
                "Name: clinical_severity, dtype: int64"
            ),
        )

        code_panel = self.show_code(code_lines, title="value_counts.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise the data quality quick-screen approach."""
        self.show_step_indicator(6, self.total_steps)

        heading = Text(
            "資料品質快篩三招",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("1. df.info()  — 看型別、看缺值", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("2. df.describe() — 看分布、抓離群值", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("3. df['col'].value_counts() — 看類別分布", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example methods
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the ExtraExampleBanner section divider."""
        banner = ExtraExampleBanner("額外範例：結核病接觸者追蹤")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        """TB contact tracing example demonstrating inspection methods."""
        self.show_step_indicator(7, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# 結核病接觸者追蹤資料\n"
                "tb = pd.read_csv('tb_contacts.csv')\n"
                "print(tb.shape)\n"
                "print(tb.info())\n"
                "\n"
                "# 檢查 TST 結果分布\n"
                "print(tb['tst_result'].value_counts())"
            ),
        )

        code_panel = self.show_code(code_lines, title="tb_inspect.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner("初學者常見地雷 3 選")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_no_parens(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: forgetting parentheses on info/describe."""
        error_code = kwargs.get("error_code", "df.info    # no output, just shows method")
        correct_code = kwargs.get("correct_code", "df.info()  # call it with parentheses!")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_object(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: assuming object dtype means string."""
        error_code = kwargs.get("error_code", "# dtype=object, assume it is numeric")
        correct_code = kwargs.get("correct_code", "# dtype=object usually means string/mixed")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_include_all(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: describe() skips non-numeric by default."""
        error_code = kwargs.get("error_code", "df.describe()  # only shows numeric cols")
        correct_code = kwargs.get("correct_code", "df.describe(include='all')  # all dtypes")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            "下一集：日期時間大魔王",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "把 object 轉成 datetime64，時間計算不再卡關！",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
