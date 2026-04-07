"""Ch04-06: Generate SitRep — 函式化

Manim scene for the tutorial video on wrapping SitRep logic into
reusable functions, using the Legionella outbreak investigation.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
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
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch04GenerateSitrepScene(EpiBaseScene):
    """Tutorial video scene: wrapping SitRep into a reusable function."""

    total_steps: int = 14

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the Generate SitRep lesson."""
        self.show_title_card("函式化", "把 SitRep 包成一鍵更新", duration=duration)

    def show_function_design(self, duration: float = 6.0, **kwargs) -> None:
        """Show function signature and docstring."""
        self.show_step_indicator(1, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "def generate_sitrep(df):\n"
                '    """Generate a SitRep dict from a line list.\n'
                "\n"
                "    Parameters\n"
                "    ----------\n"
                "    df : pd.DataFrame\n"
                "        Line list with case_classification, outcome.\n"
                '    """\n'
                "    cases = df[df['case_classification']=='confirmed']"
            ),
        )

        self.show_code(code_lines, title="generate_sitrep.py")
        self.wait(duration)
        self.clear_screen()

    def show_int_casting(self, duration: float = 6.0, **kwargs) -> None:
        """Show int() casting for clean output."""
        self.show_step_indicator(2, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "    n_cases = int(len(cases))\n"
                "    n_dead = int((cases['outcome'] == 'dead').sum())\n"
                "    ar = round(n_cases / len(df) * 100, 1)\n"
                "    cfr = round(n_dead / n_cases * 100, 1)\n"
                "    return {\n"
                "        'total': len(df),\n"
                "        'cases': n_cases,\n"
                "        'deaths': n_dead,\n"
                "        'AR_pct': ar,\n"
                "        'CFR_pct': cfr,\n"
                "    }"
            ),
        )

        self.show_code(code_lines, title="int_casting.py")
        self.wait(duration)
        self.clear_screen()

    def show_guard_clause(self, duration: float = 6.0, **kwargs) -> None:
        """Show guard clause for empty DataFrame."""
        self.show_step_indicator(3, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "def generate_sitrep(df):\n"
                "    if df.empty:\n"
                "        raise ValueError('DataFrame is empty')\n"
                "    if 'case_classification' not in df.columns:\n"
                "        raise ValueError('Missing column')\n"
                "    cases = df[df['case_classification']=='confirmed']\n"
                "    ..."
            ),
        )

        self.show_code(code_lines, title="guard_clause.py")
        self.wait(duration)
        self.clear_screen()

    def show_call_function(self, duration: float = 6.0, **kwargs) -> None:
        """Show calling the function and printing results."""
        self.show_step_indicator(4, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "\n"
                "df = pd.read_csv('legionella_outbreak.csv')\n"
                "result = generate_sitrep(df)\n"
                "for k, v in result.items():\n"
                "    print(f'{k}: {v}')"
            ),
        )

        output_text = kwargs.get(
            "output",
            "total: 280\ncases: 121\ndeaths: 19\nAR_pct: 43.2\nCFR_pct: 15.7",
        )

        self.show_code(code_lines, title="call_function.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key points about function design."""
        self.show_step_indicator(5, self.total_steps)

        heading = Text(
            "重點整理",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("1. 用函式封裝 SitRep 邏輯，方便重複使用", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("2. int() 把 numpy int64 轉成 Python int", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("3. guard clause 在函式開頭檢查輸入", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("4. 回傳 dict 讓下游程式容易取用", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("5. 加 docstring 讓同事看得懂你的函式", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the ExtraExampleBanner section divider."""
        banner = ExtraExampleBanner("額外範例：疫苗覆蓋率函式")
        self.show_section_banner(banner, duration=duration)

    def show_extra_vaccine(self, duration: float = 6.0, **kwargs) -> None:
        """Vaccine coverage function example."""
        self.show_step_indicator(7, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "def vaccine_coverage(df, dose_col='doses'):\n"
                '    """Return vaccination coverage metrics."""\n'
                "    total = len(df)\n"
                "    vaccinated = (df[dose_col] >= 1).sum()\n"
                "    full = (df[dose_col] >= 2).sum()\n"
                "    return {\n"
                "        'coverage_1dose': round(vaccinated/total*100, 1),\n"
                "        'coverage_full':  round(full/total*100, 1),\n"
                "    }"
            ),
        )

        self.show_code(code_lines, title="vaccine_coverage.py")
        self.wait(duration)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner("初學者常見地雷 3 選")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_global_var(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: using global variable inside function."""
        error_code = kwargs.get("error_code", "def sitrep(): return len(df)  # global df!")
        correct_code = kwargs.get("correct_code", "def sitrep(df): return len(df)  # param df")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_return_df(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: forgetting to return the result."""
        error_code = kwargs.get("error_code", "def sitrep(df): ar = len(cases)/len(df)")
        correct_code = kwargs.get("correct_code", "def sitrep(df): ... return {'AR': ar}")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_docstring(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: no docstring in function."""
        error_code = kwargs.get("error_code", "def sitrep(df): cases = df[...]")
        correct_code = kwargs.get("correct_code", 'def sitrep(df): """Generate SitRep.""" ...')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            "下一集：專業報告輸出",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "Dashboard、Word、PPT、PDF 一次搞定！",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
