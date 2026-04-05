"""Ch03-01: 2x2 Table — 流行病學的基本功

Manim scene for the tutorial video on 2x2 contingency tables, using the
Legionella outbreak investigation as the teaching narrative.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    Text,
    VGroup,
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


class Ch03TwoByTwoScene(EpiBaseScene):
    """Tutorial video scene: 2x2 contingency tables with the Legionella outbreak scenario."""

    total_steps: int = 15

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the 2x2 table lesson."""
        self.show_title_card("2x2 Table", "流行病學的基本功", duration=duration)

    def show_concept_layout(self, duration: float = 5.0, **kwargs) -> None:
        """Show the conceptual layout of a 2x2 table."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "2x2 Table 的結構",
            font=FONT_MONO,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• 列（row）= 暴露狀態（有暴露 / 無暴露）", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 欄（column）= 疾病狀態（生病 / 未生病）", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 四格：a, b, c, d 各代表一組人數", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 又稱交叉表（crosstab）或列聯表", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_legionella_context(self, duration: float = 5.0, **kwargs) -> None:
        """Introduce the Legionella outbreak context for the 2x2 table."""
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            "退伍軍人症群聚：淋浴暴露 vs 感染",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• 松柏護理之家 280 位住民", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 暴露因子：是否使用淋浴設備（shower_use）", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 結果：是否感染（case_classification）", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 目標：用 2x2 表整理暴露與疾病的關係", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_crosstab_basic(self, duration: float = 6.0, **kwargs) -> None:
        """Show pd.crosstab() to build a 2x2 table."""
        self.show_step_indicator(3, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "\n"
                "df = pd.read_csv('legionella_outbreak.csv')\n"
                "table = pd.crosstab(\n"
                "    df['shower_use'],\n"
                "    df['case_classification'],\n"
                ")\n"
                "print(table)"
            ),
        )

        output_text = kwargs.get(
            "output",
            "case_classification  confirmed  non-case\n"
            "shower_use\n"
            "False                       30        90\n"
            "True                        91        69",
        )

        code_panel = self.show_code(code_lines, title="crosstab.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_extract_abcd(self, duration: float = 6.0, **kwargs) -> None:
        """Show how to extract a, b, c, d from the crosstab."""
        self.show_step_indicator(4, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# a = exposed & ill, b = exposed & well\n"
                "# c = unexposed & ill, d = unexposed & well\n"
                "a = table.loc[True, 'confirmed']    # 91\n"
                "b = table.loc[True, 'non-case']     # 69\n"
                "c = table.loc[False, 'confirmed']   # 30\n"
                "d = table.loc[False, 'non-case']    # 90\n"
                "print(f'a={a}, b={b}, c={c}, d={d}')"
            ),
        )

        output_text = kwargs.get("output", "a=91, b=69, c=30, d=90")

        code_panel = self.show_code(code_lines, title="extract_abcd.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_attack_rate(self, duration: float = 6.0, **kwargs) -> None:
        """Show attack rate calculation from 2x2 table values."""
        self.show_step_indicator(5, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# Attack rate (exposed) = a / (a + b)\n"
                "ar_exposed = a / (a + b)\n"
                "ar_unexposed = c / (c + d)\n"
                "print(f'Exposed AR:   {ar_exposed:.1%}')\n"
                "print(f'Unexposed AR: {ar_unexposed:.1%}')"
            ),
        )

        output_text = kwargs.get(
            "output",
            "Exposed AR:   56.9%\nUnexposed AR: 25.0%",
        )

        code_panel = self.show_code(code_lines, title="attack_rate.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_margins(self, duration: float = 6.0, **kwargs) -> None:
        """Show how to add margins to the crosstab."""
        self.show_step_indicator(6, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "table_m = pd.crosstab(\n"
                "    df['shower_use'],\n"
                "    df['case_classification'],\n"
                "    margins=True,\n"
                "    margins_name='Total',\n"
                ")\n"
                "print(table_m)"
            ),
        )

        output_text = kwargs.get(
            "output",
            "case_classification  confirmed  non-case  Total\n"
            "shower_use\n"
            "False                       30        90    120\n"
            "True                        91        69    160\n"
            "Total                      121       159    280",
        )

        code_panel = self.show_code(code_lines, title="margins.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key points about 2x2 tables."""
        self.show_step_indicator(7, self.total_steps)

        heading = Text(
            "重點整理",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("1. pd.crosstab() 快速建立 2x2 表", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("2. a, b, c, d 分別代表四格的人數", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("3. 侵襲率 = 生病人數 / 該組總人數", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("4. margins=True 自動加上合計列與欄", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("5. 2x2 表是計算風險比、勝算比的基礎", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
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
        banner = ExtraExampleBanner("額外範例：腸病毒群聚 2x2 表")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        """Enterovirus cluster example demonstrating 2x2 table construction."""
        self.show_step_indicator(8, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# Enterovirus cluster at a kindergarten\n"
                "# Exposure: shared toys, Outcome: HFMD\n"
                "import numpy as np\n"
                "\n"
                "data = {'shared_toys': [True]*30 + [False]*20,\n"
                "        'hfmd': [1]*18 + [0]*12 + [1]*4 + [0]*16}\n"
                "ev = pd.DataFrame(data)\n"
                "print(pd.crosstab(ev['shared_toys'], ev['hfmd']))"
            ),
        )

        output_text = kwargs.get(
            "output",
            "hfmd          0   1\nshared_toys\nFalse        16   4\nTrue         12  18",
        )

        code_panel = self.show_code(code_lines, title="enterovirus.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner("初學者常見地雷 3 選")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_row_col(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: row and column order in crosstab."""
        error_code = kwargs.get("error_code", "pd.crosstab(df['outcome'], df['exposure'])")
        correct_code = kwargs.get("correct_code", "pd.crosstab(df['exposure'], df['outcome'])")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_margins(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: forgetting margins parameter."""
        error_code = kwargs.get("error_code", "pd.crosstab(x, y)  # no totals shown")
        correct_code = kwargs.get("correct_code", "pd.crosstab(x, y, margins=True)")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_abcd(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: swapping a/b/c/d positions."""
        error_code = kwargs.get("error_code", "a = table.loc[False, 'confirmed']  # wrong!")
        correct_code = kwargs.get("correct_code", "a = table.loc[True, 'confirmed']   # exposed+ill")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            "下一集：風險比 Risk Ratio",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "有了 2x2 表，就能算出暴露的風險有多大！",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
