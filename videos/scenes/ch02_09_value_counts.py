"""Ch02-09: 頻率表速成 — value_counts + crosstab 完全攻略

Manim scene for the tutorial video on pandas value_counts and crosstab,
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
    ACCENT_GREEN,
    ACCENT_ORANGE,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch02ValueCountsScene(EpiBaseScene):
    """Tutorial video scene: pandas value_counts and crosstab with the Legionella outbreak scenario."""

    total_steps: int = 14

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "頻率表速成",
            "title_sub": "value_counts + crosstab 完全攻略",
            "why_heading": "拿到資料第一件事：看分布！",
            "why_b1": "1. 頻率表 = 快速掃描資料全貌",
            "why_b2": "2. 哪個類別最多？哪個最少？",
            "why_b3": "3. 有沒有缺失值？分布合不合理？",
            "why_b4": "4. 先看分布，再做分析！",
            "why_metaphor": "像收信先分堆，才知道哪堆最多",
            "normalize_note": "dropna=False 讓缺失值現形！",
            "crosstab_note": "margins=True 自動加行列小計",
            "cvp_b1": "crosstab：吃兩個 Series，預設計數",
            "cvp_b2": "pivot_table：吃 DataFrame，需設 aggfunc",
            "cvp_b3": "快速計數 → crosstab",
            "cvp_b4": "複雜聚合 → pivot_table",
            "cvp_metaphor": "筷子 vs 叉子，看你吃什麼菜",
            "summary_heading": "重點整理",
            "summary_p1": "1. value_counts 一行搞定單欄位頻率表",
            "summary_p2": "2. normalize=True 看比例，dropna=False 防漏",
            "summary_p3": "3. crosstab 做雙變數交叉計數",
            "summary_p4": "4. 拿到資料先跑頻率表，再做分析！",
            "extra_banner_title": "額外範例：腸病毒校園群聚",
            "blindspot_banner_title": "value_counts 三大新手坑",
            "outro_heading": "下一集：pivot_table 進階攻略",
            "outro_sub": "把分組統計玩到淋漓盡致！",
        },
        "en": {
            "title_main": "Frequency Tables, Fast",
            "title_sub": "value_counts + crosstab, the complete guide",
            "why_heading": "First thing with new data: check the distribution!",
            "why_b1": "1. Frequency table = a quick scan of the whole dataset",
            "why_b2": "2. Which category is largest? Which is smallest?",
            "why_b3": "3. Any missing values? Does the distribution make sense?",
            "why_b4": "4. Look at the distribution first, then analyze!",
            "why_metaphor": "Like sorting mail into piles to see which pile is biggest",
            "normalize_note": "dropna=False makes missing values show up!",
            "crosstab_note": "margins=True adds row and column subtotals automatically",
            "cvp_b1": "crosstab: takes two Series, counts by default",
            "cvp_b2": "pivot_table: takes a DataFrame, needs aggfunc",
            "cvp_b3": "Quick counts → crosstab",
            "cvp_b4": "Complex aggregation → pivot_table",
            "cvp_metaphor": "Chopsticks vs fork - depends what you're eating",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. value_counts builds a one-column frequency table in one line",
            "summary_p2": "2. normalize=True for proportions, dropna=False to catch gaps",
            "summary_p3": "3. crosstab for two-variable cross counts",
            "summary_p4": "4. Run a frequency table first, analyze second!",
            "extra_banner_title": "Extra example: enterovirus school cluster",
            "blindspot_banner_title": "3 Beginner Traps with value_counts",
            "outro_heading": "Next up: advanced pivot_table",
            "outro_sub": "Push grouped statistics to the limit!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the value_counts + crosstab lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_why_frequency(self, duration: float = 7.0, **kwargs) -> None:
        """Step 1: why frequency tables are the first thing in epi investigation."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            self.t("why_heading"),
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        bullets = VGroup(
            Text(self.t("why_b1"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("why_b2"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("why_b3"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("why_b4"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        metaphor = Text(
            self.t("why_metaphor"),
            font=FONT_CJK,
            font_size=18,
            color=TEXT_SECONDARY,
        ).next_to(bullets, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(bullets, lag_ratio=0.3), run_time=1.0)
        self.play(FadeIn(metaphor), run_time=0.5)
        self.wait(max(0.1, duration - 2.0))
        self.play(FadeOut(VGroup(heading, bullets, metaphor)), run_time=0.5)

    def show_value_counts_basic(self, duration: float = 6.0, **kwargs) -> None:
        """Step 2: basic value_counts usage."""
        self.show_step_indicator(2, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "\n"
                "df = pd.read_csv('legionella_outbreak.csv')\n"
                "\n"
                "# 各嚴重程度有幾人？\n"
                'df["clinical_severity"].value_counts()'
            ),
        )

        output_text = kwargs.get(
            "output",
            (
                "mild        52\n"
                "moderate    38\n"
                "severe      18\n"
                "not_ill     13\n"
                "Name: clinical_severity, dtype: int64"
            ),
        )

        self.show_code(code_text, title="value_counts_basic.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_value_counts_normalize(self, duration: float = 6.0, **kwargs) -> None:
        """Step 3: value_counts with normalize and dropna."""
        self.show_step_indicator(3, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 比例 + 顯示缺失值\n"
                'df["clinical_severity"].value_counts(\n'
                "    normalize=True, dropna=False\n"
                ")"
            ),
        )

        output_text = kwargs.get(
            "output",
            (
                "mild            0.429\n"
                "moderate        0.314\n"
                "severe          0.149\n"
                "not_ill         0.107\n"
                "NaN             0.000\n"
                "Name: clinical_severity, dtype: float64"
            ),
        )

        self.show_code(code_text, title="value_counts_normalize.py")
        self.wait(1.0)
        # max_height keeps the six-line panel clear of the code panel above it.
        self.show_output_with_note(
            output_text, self.t("normalize_note"), color=ACCENT_ORANGE, max_height=2.0
        )
        self.wait(max(0.1, duration - 1.5))
        self.clear_screen()

    def show_crosstab_intro(self, duration: float = 7.0, **kwargs) -> None:
        """Step 4: pd.crosstab for two-way frequency table."""
        self.show_step_indicator(4, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 性別 x 感染狀態 交叉表\n"
                "pd.crosstab(\n"
                '    df["sex"], df["infected"],\n'
                "    margins=True\n"
                ")"
            ),
        )

        output_text = kwargs.get(
            "output",
            (
                "infected  False  True   All\n"
                "sex\n"
                "F           82    58   140\n"
                "M           77    63   140\n"
                "All        159   121   280"
            ),
        )

        self.show_code(code_text, title="crosstab_intro.py")
        self.wait(1.0)
        self.show_output_with_note(
            output_text, self.t("crosstab_note"), color=TEXT_SECONDARY, max_height=2.0
        )
        self.wait(max(0.1, duration - 1.5))
        self.clear_screen()

    def show_crosstab_vs_pivot(self, duration: float = 6.0, **kwargs) -> None:
        """Step 5: comparison between crosstab and pivot_table."""
        self.show_step_indicator(5, self.total_steps)

        heading = Text(
            "crosstab vs pivot_table",
            font=FONT_MONO,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        bullets = VGroup(
            Text(self.t("cvp_b1"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("cvp_b2"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("cvp_b3"), font=FONT_CJK, font_size=22, color=ACCENT_GREEN),
            Text(self.t("cvp_b4"), font=FONT_CJK, font_size=22, color=ACCENT_GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        metaphor = Text(
            self.t("cvp_metaphor"),
            font=FONT_CJK,
            font_size=18,
            color=TEXT_SECONDARY,
        ).next_to(bullets, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(bullets, lag_ratio=0.25), run_time=1.0)
        self.play(FadeIn(metaphor), run_time=0.5)
        self.wait(max(0.1, duration - 2.0))
        self.play(FadeOut(VGroup(heading, bullets, metaphor)), run_time=0.5)

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Step 6: summarize key points."""
        self.show_step_indicator(6, self.total_steps)

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
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(heading, DOWN, buff=0.6)

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

    def show_extra_example(self, duration: float = 7.0, **kwargs) -> None:
        """Enterovirus school cluster example demonstrating value_counts + crosstab."""
        self.show_step_indicator(8, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 腸病毒各班病例數\n"
                'ev["class"].value_counts()\n'
                "\n"
                "# 年級 x 嚴重程度 交叉表\n"
                'pd.crosstab(ev["grade"], ev["severity"])'
            ),
        )

        self.show_code(code_text, title="enterovirus_example.py")
        self.wait(max(0.1, duration - 0.5))
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_dropna(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: forgetting dropna=False."""
        error_code = kwargs.get("error_code", 'df["col"].value_counts()')
        correct_code = kwargs.get("correct_code", 'df["col"].value_counts(dropna=False)')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_continuous(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: value_counts on continuous column."""
        error_code = kwargs.get("error_code", 'df["age"].value_counts()')
        correct_code = kwargs.get("correct_code", 'pd.cut(df["age"], bins=4).value_counts()')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_crosstab(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: confusing crosstab with pivot_table params."""
        error_code = kwargs.get("error_code", 'pd.crosstab(df, values="infected")')
        correct_code = kwargs.get("correct_code", 'pd.crosstab(df["sex"], df["infected"])')
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
