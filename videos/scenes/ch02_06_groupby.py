"""Ch02-06: 分組統計秘密武器 — groupby + agg 完全攻略

Manim scene for the tutorial video on pandas groupby and aggregation,
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


class Ch02GroupbyScene(EpiBaseScene):
    """Tutorial video scene: pandas groupby and aggregation with the Legionella outbreak scenario."""

    total_steps: int = 14

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the groupby lesson."""
        self.show_title_card("分組統計秘密武器", "groupby + agg 完全攻略", duration=duration)

    def show_split_apply_combine(self, duration: float = 7.0, **kwargs) -> None:
        """Step 1: introduce the Split-Apply-Combine paradigm."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "Split \u2192 Apply \u2192 Combine",
            font=FONT_MONO,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        bullets = VGroup(
            Text("1. Split  \u2014 依照分組欄位拆成小表", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("2. Apply  \u2014 對每組做運算（sum, mean...）", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("3. Combine \u2014 把結果合回一張表", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        flow = Text(
            "df.groupby('floor')['outcome'].value_counts()",
            font=FONT_MONO,
            font_size=18,
            color=TEXT_SECONDARY,
        ).next_to(bullets, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(bullets, lag_ratio=0.3), run_time=1.0)
        self.play(FadeIn(flow), run_time=0.5)
        self.wait(duration - 2.0)
        self.play(FadeOut(VGroup(heading, bullets, flow)), run_time=0.5)

    def show_groupby_basic(self, duration: float = 6.0, **kwargs) -> None:
        """Step 2: basic groupby with size/count."""
        self.show_step_indicator(2, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "\n"
                "df = pd.read_csv('legionella_outbreak.csv')\n"
                "\n"
                "# 各樓層有多少人？\n"
                "df.groupby('floor').size()"
            ),
        )

        output_text = kwargs.get(
            "output",
            (
                "floor\n"
                "1    93\n"
                "2    94\n"
                "3    93\n"
                "dtype: int64"
            ),
        )

        code_panel = self.show_code(code_text, title="groupby_basic.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_agg_named(self, duration: float = 6.0, **kwargs) -> None:
        """Step 3: named aggregation with .agg()."""
        self.show_step_indicator(3, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 各樓層的年齡統計\n"
                "df.groupby('floor')['age'].agg(\n"
                "    mean_age='mean',\n"
                "    min_age='min',\n"
                "    max_age='max',\n"
                ")"
            ),
        )

        code_panel = self.show_code(code_text, title="agg_named.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_reset_index(self, duration: float = 5.0, **kwargs) -> None:
        """Step 4: reset_index to flatten grouped results."""
        self.show_step_indicator(4, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# groupby 結果的 index 是分組欄位\n"
                "result = df.groupby('floor').size()\n"
                "result = result.reset_index(name='count')\n"
                "print(result)"
            ),
        )

        code_panel = self.show_code(code_text, title="reset_index.py")

        note = Text(
            "reset_index() 把分組欄位從 index 變回普通欄位",
            font=FONT_CJK,
            font_size=20,
            color=TEXT_SECONDARY,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_attack_rate(self, duration: float = 7.0, **kwargs) -> None:
        """Step 5: compute attack rate per group."""
        self.show_step_indicator(5, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 各樓層侵襲率\n"
                "floor_stats = df.groupby('floor').agg(\n"
                "    n_infected=('lab_confirmed', 'sum'),\n"
                "    n_total=('case_id', 'count'),\n"
                ")\n"
                "floor_stats['attack_rate'] = (\n"
                "    floor_stats['n_infected'] / floor_stats['n_total']\n"
                ")"
            ),
        )

        code_panel = self.show_code(code_text, title="attack_rate.py")

        note = Text(
            "分母 = 該組總人數，不是全院總人數！",
            font=FONT_CJK,
            font_size=20,
            color=ACCENT_ORANGE,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_multiple_groupby(self, duration: float = 6.0, **kwargs) -> None:
        """Step 6: groupby with multiple columns."""
        self.show_step_indicator(6, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 依樓層 + 性別交叉分組\n"
                "cross = df.groupby(['floor', 'sex']).agg(\n"
                "    n=('case_id', 'count'),\n"
                "    n_dead=('outcome', lambda x: (x == 'dead').sum()),\n"
                ")\n"
                "print(cross)"
            ),
        )

        code_panel = self.show_code(code_text, title="multi_groupby.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Step 7: summarize key points."""
        self.show_step_indicator(7, self.total_steps)

        heading = Text(
            "重點整理",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("1. groupby = Split-Apply-Combine 三步驟", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("2. .agg() 可一次算多個統計量", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("3. reset_index() 把結果攤平成 DataFrame", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("4. 多欄 groupby 用 list: ['floor', 'sex']", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
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
        banner = ExtraExampleBanner("額外範例：COVID-19 各縣市統計")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 7.0, **kwargs) -> None:
        """COVID-19 county-level statistics example demonstrating groupby."""
        self.show_step_indicator(8, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# COVID-19 各縣市確診統計\n"
                "covid = pd.read_csv('covid_tw_cases.csv')\n"
                "\n"
                "county_stats = covid.groupby('county').agg(\n"
                "    confirmed=('case_id', 'count'),\n"
                "    deaths=('outcome', lambda x: (x == 'dead').sum()),\n"
                ")\n"
                "county_stats['cfr'] = (\n"
                "    county_stats['deaths'] / county_stats['confirmed']\n"
                ")\n"
                "print(county_stats.head())"
            ),
        )

        code_panel = self.show_code(code_text, title="covid_groupby.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner("groupby 經典陷阱 3 選")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_agg_vs_size(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: count() vs size() confusion."""
        error_code = kwargs.get("error_code", "df.groupby('floor').count()  # excludes NaN!")
        correct_code = kwargs.get("correct_code", "df.groupby('floor').size()   # counts all rows")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_wrong_denominator(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: wrong denominator in attack rate."""
        error_code = kwargs.get("error_code", "infected / len(df)   # wrong: uses total N")
        correct_code = kwargs.get("correct_code", "infected / group_n   # correct: group denominator")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_sum_all(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: summing all columns instead of specific ones."""
        error_code = kwargs.get("error_code", "df.groupby('floor').sum()  # sums everything!")
        correct_code = kwargs.get("correct_code", "df.groupby('floor')['age'].sum()  # specific col")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            "下一集：matplotlib 流行曲線",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "用圖表說故事，畫出疫情的時間趨勢！",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
