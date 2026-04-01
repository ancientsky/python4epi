"""Ch02-13: 文字清理三板斧 — str + drop_duplicates + rename

Manim scene for the tutorial video on pandas string operations and data cleanup,
using the Legionella outbreak investigation as the teaching narrative.
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


class Ch02StrCleanupScene(EpiBaseScene):
    """Tutorial video scene: str operations, drop_duplicates, rename with the Legionella outbreak scenario."""

    total_steps: int = 15

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the string cleanup lesson."""
        self.show_title_card("文字清理三板斧", "str + drop_duplicates + rename", duration=duration)

    def show_dirty_data_reality(self, duration: float = 7.0, **kwargs) -> None:
        """Step 1: show messy real-world data."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "現實世界的資料長這樣…",
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        messy_examples = VGroup(
            Text('wing: " A", "a", "A"  → 三種寫法！', font=FONT_MONO, font_size=20, color=TEXT_PRIMARY),
            Text('hospital: "NTU", "ntu", "Ntu Hospital"', font=FONT_MONO, font_size=20, color=TEXT_PRIMARY),
            Text("case_id: A001 (x3) → 重複通報", font=FONT_MONO, font_size=20, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(heading, DOWN, buff=0.6)

        warning = Text(
            "不先清理 → groupby 分錯組 → 分析結果報廢",
            font=FONT_CJK,
            font_size=22,
            color=ACCENT_ORANGE,
        ).next_to(messy_examples, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(messy_examples, lag_ratio=0.3), run_time=1.0)
        self.play(FadeIn(warning), run_time=0.5)
        self.wait(duration - 2.0)
        self.play(FadeOut(VGroup(heading, messy_examples, warning)), run_time=0.5)

    def show_str_basic(self, duration: float = 6.0, **kwargs) -> None:
        """Step 2: str.upper, str.lower, str.strip."""
        self.show_step_indicator(2, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                '# 統一大小寫 + 去除前後空白\n'
                'df["wing"] = df["wing"].str.strip().str.upper()\n'
                'print(df["wing"].value_counts())'
            ),
        )

        output_text = kwargs.get(
            "output",
            (
                "A    142\n"
                "B    138"
            ),
        )

        code_panel = self.show_code(code_text, title="str_basic.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_str_contains(self, duration: float = 6.0, **kwargs) -> None:
        """Step 3: str.contains for text search."""
        self.show_step_indicator(3, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                '# 搜尋重症個案\n'
                'severe = df["clinical_severity"].str.contains(\n'
                '    "severe", na=False\n'
                ')\n'
                'print(df[severe].shape[0], "severe cases")'
            ),
        )

        output_text = kwargs.get("output", "23 severe cases")

        code_panel = self.show_code(code_text, title="str_contains.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_str_replace(self, duration: float = 6.0, **kwargs) -> None:
        """Step 4: str.replace for batch text substitution."""
        self.show_step_indicator(4, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                '# 統一醫院名稱\n'
                'df["hospital"] = (\n'
                '    df["hospital"]\n'
                '    .str.replace("NTU Hospital", "NTUH")\n'
                '    .str.replace("ntu hospital", "NTUH")\n'
                ")"
            ),
        )

        code_panel = self.show_code(code_text, title="str_replace.py")

        note = Text(
            "str.replace 可以串接：一行解決多種寫法",
            font=FONT_CJK,
            font_size=20,
            color=TEXT_SECONDARY,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_drop_duplicates(self, duration: float = 6.0, **kwargs) -> None:
        """Step 5: drop_duplicates to remove repeat notifications."""
        self.show_step_indicator(5, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                '# 去除重複通報\n'
                "df = df.drop_duplicates(\n"
                '    subset="case_id", keep="first"\n'
                ")\n"
                'print(f"Unique cases: {len(df)}")'
            ),
        )

        output_text = kwargs.get("output", "Unique cases: 280")

        code_panel = self.show_code(code_text, title="drop_duplicates.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_rename_nlargest(self, duration: float = 6.0, **kwargs) -> None:
        """Step 6: rename columns and nlargest for top N."""
        self.show_step_indicator(6, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                '# 改欄位名 + 找前三名\n'
                'df = df.rename(columns={"wing": "Wing"})\n'
                'top3 = df.nlargest(3, "attack_rate")\n'
                'print(top3[["floor", "attack_rate"]])'
            ),
        )

        output_text = kwargs.get(
            "output",
            (
                "floor  attack_rate\n"
                "    3       0.55\n"
                "    2       0.44\n"
                "    1       0.39"
            ),
        )

        code_panel = self.show_code(code_text, title="rename_nlargest.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Step 7: summarize the three tools."""
        self.show_step_indicator(7, self.total_steps)

        heading = Text(
            "三板斧總整理",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("1. str：strip / upper / lower / contains / replace", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("2. drop_duplicates：去重，subset 指定 key 欄位", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("3. rename + nlargest：改名 + 快速排名", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("先洗再分析，養成好習慣！", font=FONT_CJK, font_size=22, color=ACCENT_ORANGE),
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
        banner = ExtraExampleBanner("額外範例：流感監測資料清理")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 7.0, **kwargs) -> None:
        """Flu surveillance data cleanup example."""
        self.show_step_indicator(9, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                '# 流感監測：統一醫院名稱\n'
                'flu["hospital"] = (\n'
                '    flu["hospital"]\n'
                "    .str.strip()\n"
                '    .str.replace("NTU Hospital", "NTUH")\n'
                '    .str.replace("ntu hospital", "NTUH")\n'
                ")\n"
                'print(flu["hospital"].value_counts())'
            ),
        )

        code_panel = self.show_code(code_text, title="flu_cleanup.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner("資料清理三大翻車現場")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_na_false(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: forgetting na=False in str.contains."""
        error_code = kwargs.get("error_code", 'df["col"].str.contains("text")  # NaN crash')
        correct_code = kwargs.get("correct_code", 'df["col"].str.contains("text", na=False)')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_case_sensitive(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: case sensitivity in value_counts."""
        error_code = kwargs.get("error_code", 'df["sex"].value_counts()  # Male, male, MALE')
        correct_code = kwargs.get("correct_code", 'df["sex"].str.lower().value_counts()')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_inplace(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: inplace=True breaks chaining."""
        error_code = kwargs.get("error_code", "df.drop_duplicates(inplace=True)  # no chain")
        correct_code = kwargs.get("correct_code", "df = df.drop_duplicates()  # explicit assign")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card — Ch02 complete!"""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            "Ch02 完成！",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "下一章 Ch03：2×2 表、RR、OR、卡方檢定",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
