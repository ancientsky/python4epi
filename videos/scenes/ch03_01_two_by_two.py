"""Ch03-01: 2x2 Table — 流行病學的基本功

Manim scene for the tutorial video on 2x2 contingency tables, using the
Legionella outbreak investigation as the teaching narrative.
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
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch03TwoByTwoScene(EpiBaseScene):
    """Tutorial video scene: 2x2 contingency tables with the Legionella outbreak scenario."""

    total_steps: int = 15

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "2x2 Table",
            "title_sub": "流行病學的基本功",
            "concept_heading": "2x2 Table 的結構",
            "concept_p1": "• 列（row）= 暴露狀態（有暴露 / 無暴露）",
            "concept_p2": "• 欄（column）= 疾病狀態（生病 / 未生病）",
            "concept_p3": "• 四格：a, b, c, d 各代表一組人數",
            "concept_p4": "• 又稱交叉表（crosstab）或列聯表",
            "legionella_heading": "退伍軍人症群聚：淋浴暴露 vs 感染",
            "legionella_p1": "• 松柏護理之家 280 位住民",
            "legionella_p2": "• 暴露因子：是否使用淋浴設備（shower_use）",
            "legionella_p3": "• 結果：是否感染（case_classification）",
            "legionella_p4": "• 目標：用 2x2 表整理暴露與疾病的關係",
            "summary_heading": "重點整理",
            "summary_p1": "1. pd.crosstab() 快速建立 2x2 表",
            "summary_p2": "2. a, b, c, d 分別代表四格的人數",
            "summary_p3": "3. 侵襲率 = 生病人數 / 該組總人數",
            "summary_p4": "4. margins=True 自動加上合計列與欄",
            "summary_p5": "5. 2x2 表是計算風險比、勝算比的基礎",
            "extra_banner_title": "額外範例：腸病毒群聚 2x2 表",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：風險比 Risk Ratio",
            "outro_sub": "有了 2x2 表，就能算出暴露的風險有多大！",
        },
        "en": {
            "title_main": "2x2 Table",
            "title_sub": "The bread and butter of epidemiology",
            "concept_heading": "Anatomy of a 2x2 Table",
            "concept_p1": "• Row = exposure status (exposed / unexposed)",
            "concept_p2": "• Column = disease status (ill / not ill)",
            "concept_p3": "• Four cells: a, b, c, d each hold one group's count",
            "concept_p4": "• Also called a crosstab or contingency table",
            "legionella_heading": "Legionella cluster: shower exposure vs infection",
            "legionella_p1": "• Pine & Cypress nursing home, 280 residents",
            "legionella_p2": "• Exposure: whether they used the showers (shower_use)",
            "legionella_p3": "• Outcome: whether they got infected (case_classification)",
            "legionella_p4": "• Goal: use a 2x2 table to map exposure vs disease",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. pd.crosstab() builds a 2x2 table fast",
            "summary_p2": "2. a, b, c, d are the four cell counts",
            "summary_p3": "3. Attack rate = cases / that group's total",
            "summary_p4": "4. margins=True adds total rows and columns automatically",
            "summary_p5": "5. The 2x2 table is the basis for risk ratio and odds ratio",
            "extra_banner_title": "Extra example: an enterovirus cluster 2x2 table",
            "blindspot_banner_title": "3 Common Beginner Traps",
            "outro_heading": "Next up: Risk Ratio",
            "outro_sub": "With a 2x2 table, you can measure how big the exposure risk is!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the 2x2 table lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_concept_layout(self, duration: float = 5.0, **kwargs) -> None:
        """Show the conceptual layout of a 2x2 table."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            self.t("concept_heading"),
            font=FONT_MONO,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("concept_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("concept_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("concept_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("concept_p4"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(max(0.1, duration - 1.5))
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_legionella_context(self, duration: float = 5.0, **kwargs) -> None:
        """Introduce the Legionella outbreak context for the 2x2 table."""
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            self.t("legionella_heading"),
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("legionella_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("legionella_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("legionella_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("legionella_p4"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(max(0.1, duration - 1.5))
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

        self.show_code(code_lines, title="crosstab.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
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

        self.show_code(code_lines, title="extract_abcd.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
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

        self.show_code(code_lines, title="attack_rate.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
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

        self.show_code(code_lines, title="margins.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key points about 2x2 tables."""
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
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example methods
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the ExtraExampleBanner section divider."""
        banner = ExtraExampleBanner(self.t("extra_banner_title"))
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

        self.show_code(code_lines, title="enterovirus.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
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
