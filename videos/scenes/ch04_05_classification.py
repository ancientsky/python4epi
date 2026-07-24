"""Ch04-05: Classification — 個案分類

Manim scene for the tutorial video on case classification and
stratified statistics, using the Legionella outbreak investigation.
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


class Ch04ClassificationScene(EpiBaseScene):
    """Tutorial video scene: case classification and stratified statistics."""

    total_steps: int = 14

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "個案分類",
            "title_sub": "確診、可能和非個案的分層統計",
            "summary_heading": "重點整理",
            "summary_p1": "1. value_counts() 快速看各分類人數",
            "summary_p2": "2. groupby + agg 可同時算多個指標",
            "summary_p3": "3. lambda 讓你在 agg 裡自訂計算邏輯",
            "summary_p4": "4. 致死率的分母是確診個案數，不是全體",
            "summary_p5": "5. 個案分類是分層分析的重要基礎",
            "extra_banner_title": "額外範例：結核病個案分類統計",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：函式化",
            "outro_sub": "把 SitRep 包成函式，一鍵更新！",
        },
        "en": {
            "title_main": "Case Classification",
            "title_sub": "Stratified stats for confirmed, probable, and non-cases",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. value_counts() shows counts per classification fast",
            "summary_p2": "2. groupby + agg computes several metrics at once",
            "summary_p3": "3. lambda lets you customize the logic inside agg",
            "summary_p4": "4. CFR's denominator is confirmed cases, not everyone",
            "summary_p5": "5. Case classification is the backbone of stratified analysis",
            "extra_banner_title": "Extra example: TB case-classification stats",
            "blindspot_banner_title": "3 Common Beginner Traps",
            "outro_heading": "Next up: wrapping it in a function",
            "outro_sub": "Package the SitRep into a function for one-click updates!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the Classification lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_groupby_classification(self, duration: float = 6.0, **kwargs) -> None:
        """Show groupby on case_classification."""
        self.show_step_indicator(1, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "\n"
                "df = pd.read_csv('legionella_outbreak.csv')\n"
                "class_counts = df['case_classification'].value_counts()\n"
                "print(class_counts)"
            ),
        )

        self.show_code(code_lines, title="classification.py")
        self.wait(duration)
        self.clear_screen()

    def show_hosp_rate(self, duration: float = 6.0, **kwargs) -> None:
        """Show hospitalization rate by classification."""
        self.show_step_indicator(2, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "hosp = df.groupby('case_classification').agg(\n"
                "    total=('case_id', 'size'),\n"
                "    hospitalized=('hospitalized', 'sum'),\n"
                ")\n"
                "hosp['hosp_rate'] = (\n"
                "    hosp['hospitalized'] / hosp['total'] * 100\n"
                ").round(1)\n"
                "print(hosp)"
            ),
        )

        output_text = kwargs.get(
            "output",
            "                    total  hospitalized  hosp_rate\n"
            "case_classification\n"
            "confirmed             121            98       81.0\n"
            "non-case              159             0        0.0",
        )

        self.show_code(code_lines, title="hosp_rate.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_lambda_trick(self, duration: float = 6.0, **kwargs) -> None:
        """Show lambda in agg for custom calculations."""
        self.show_step_indicator(3, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "stats = df.groupby('case_classification').agg(\n"
                "    n=('case_id', 'size'),\n"
                "    deaths=('outcome',\n"
                "            lambda x: (x == 'dead').sum()),\n"
                "    icu=('icu_admission', 'sum'),\n"
                ")\n"
                "stats['cfr'] = (\n"
                "    stats['deaths'] / stats['n'] * 100\n"
                ").round(1)"
            ),
        )

        self.show_code(code_lines, title="lambda_agg.py")
        self.wait(duration)
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key points about case classification."""
        self.show_step_indicator(4, self.total_steps)

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
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the ExtraExampleBanner section divider."""
        banner = ExtraExampleBanner(self.t("extra_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_extra_tb(self, duration: float = 6.0, **kwargs) -> None:
        """TB case classification example."""
        self.show_step_indicator(6, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# TB: classification by lab confirmation\n"
                "tb = pd.read_csv('tb_cases.csv')\n"
                "tb_class = tb.groupby('classification').agg(\n"
                "    n=('case_id', 'size'),\n"
                "    treated=('treatment_started', 'sum'),\n"
                ")\n"
                "tb_class['tx_rate'] = (\n"
                "    tb_class['treated'] / tb_class['n'] * 100\n"
                ").round(1)\n"
                "print(tb_class)"
            ),
        )

        self.show_code(code_lines, title="tb_classification.py")
        self.wait(duration)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_definition(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: mixing up case definitions."""
        error_code = kwargs.get("error_code", "cases = df[df['lab_confirmed'] == True]")
        correct_code = kwargs.get("correct_code", "cases = df[df['case_classification']=='confirmed']")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_lambda(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: lambda returning wrong type."""
        error_code = kwargs.get("error_code", "agg(deaths=('outcome', lambda x: x=='dead'))")
        correct_code = kwargs.get("correct_code", "agg(deaths=('outcome', lambda x: (x=='dead').sum()))")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_cfr_denominator(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: CFR denominator should be cases, not total."""
        error_code = kwargs.get("error_code", "cfr = deaths / len(df)  # wrong denominator")
        correct_code = kwargs.get("correct_code", "cfr = deaths / len(cases)  # confirmed only")
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
