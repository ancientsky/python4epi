"""Ch02-11: 一行寫完分析 — Method Chaining 流水線

Manim scene for the tutorial video on pandas method chaining, using the
Legionella outbreak investigation as the teaching narrative.  The factory
assembly-line metaphor is used throughout to explain how data flows
through chained pandas methods without intermediate variables.
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


class Ch02MethodChainingScene(EpiBaseScene):
    """Tutorial video scene: pandas method chaining for epidemiological analysis."""

    total_steps: int = 14

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 4.0, **kwargs) -> None:
        """Title card for the method chaining lesson."""
        self.show_title_card(
            "一行寫完分析",
            "Method Chaining 流水線",
            duration=duration,
        )

    def show_problem_with_temps(self, duration: float = 8.0, **kwargs) -> None:
        """Step 1: show ugly code with many temporary variables."""
        self.show_step_indicator(1, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                'df_infected = df[df["infected"] == 1]\n'
                'grouped = df_infected.groupby("floor")\n'
                "counts = grouped.size()\n"
                'result = counts.reset_index(name="n_cases")\n'
                'final = result.sort_values("n_cases", ascending=False)'
            ),
        )

        code_panel = self.show_code(code_text, title="temp_variables.py")

        note = Text(
            "5 個拋棄式變數 — 取名取到腦袋爆炸",
            font=FONT_CJK,
            font_size=20,
            color=ACCENT_ORANGE,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_chaining_basic(self, duration: float = 7.0, **kwargs) -> None:
        """Step 2: convert temp-variable code to chained version."""
        self.show_step_indicator(2, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "result = (\n"
                "    df\n"
                '    .query("infected == 1")\n'
                '    .groupby("floor")\n'
                "    .size()\n"
                '    .reset_index(name="n_cases")\n'
                '    .sort_values("n_cases", ascending=False)\n'
                ")"
            ),
        )

        code_panel = self.show_code(code_text, title="method_chaining.py")

        note = Text(
            "0 個中間變數 — 原料進去，成品出來",
            font=FONT_CJK,
            font_size=20,
            color=ACCENT_GREEN,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_query_intro(self, duration: float = 7.0, **kwargs) -> None:
        """Step 3: introduce .query() with string-based filtering."""
        self.show_step_indicator(3, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "threshold = 70\n"
                "result = (\n"
                "    df\n"
                '    .query("infected == 1 and age >= @threshold")\n'
                ")"
            ),
        )

        code_panel = self.show_code(code_text, title="query.py")

        note = Text(
            "and / or / not + @variable — 像英文句子一樣好讀",
            font=FONT_CJK,
            font_size=20,
            color=TEXT_SECONDARY,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_assign_intro(self, duration: float = 7.0, **kwargs) -> None:
        """Step 4: introduce .assign() with lambda for computed columns."""
        self.show_step_indicator(4, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "result = (\n"
                "    df\n"
                '    .groupby("floor")\n'
                '    .agg(n=("case_id", "count"),\n'
                '         infected=("infected", "sum"))\n'
                '    .assign(attack_rate=lambda d: d["infected"] / d["n"] * 100)\n'
                ")"
            ),
        )

        code_panel = self.show_code(code_text, title="assign.py")

        note = Text(
            "lambda d = 流水線上的 DataFrame — 直接加工不跳出",
            font=FONT_CJK,
            font_size=20,
            color=ACCENT_ORANGE,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_full_pipeline(self, duration: float = 8.0, **kwargs) -> None:
        """Step 5: complete real-world analysis pipeline."""
        self.show_step_indicator(5, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "report = (\n"
                "    df\n"
                '    .query("age >= 70")\n'
                '    .groupby("floor")\n'
                '    .agg(n=("case_id", "count"),\n'
                '         infected=("infected", "sum"),\n'
                "         deaths=(\"outcome\",\n"
                '                 lambda x: (x == "dead").sum()))\n'
                "    .assign(\n"
                '        attack_rate=lambda d: d["infected"] / d["n"] * 100,\n'
                '        cfr=lambda d: d["deaths"] / d["infected"] * 100,\n'
                "    )\n"
                '    .sort_values("attack_rate", ascending=False)\n'
                ")"
            ),
        )

        code_panel = self.show_code(code_text, title="full_pipeline.py")

        note = Text(
            "filter -> group -> agg -> assign -> sort : one pipeline",
            font=FONT_MONO,
            font_size=18,
            color=ACCENT_GREEN,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Step 6: lesson summary — when to chain vs when not to."""
        self.show_step_indicator(6, self.total_steps)

        heading = Text(
            "重點整理",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(
                "1. query / groupby / agg / assign / sort_values",
                font=FONT_MONO, font_size=20, color=TEXT_PRIMARY,
            ),
            Text(
                "2. 小括號包起來就能自由換行",
                font=FONT_CJK, font_size=22, color=TEXT_PRIMARY,
            ),
            Text(
                "3. 零個中間變數 — 乾淨俐落",
                font=FONT_CJK, font_size=22, color=TEXT_PRIMARY,
            ),
            Text(
                "4. 超過 8 行就考慮拆開 — 可讀性 > 炫技",
                font=FONT_CJK, font_size=22, color=TEXT_PRIMARY,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example methods
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the ExtraExampleBanner section divider."""
        banner = ExtraExampleBanner("額外範例：結核病接觸者追蹤")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 7.0, **kwargs) -> None:
        """Step 8: TB contact tracing with method chaining."""
        self.show_step_indicator(8, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "high_risk = (\n"
                "    contacts\n"
                '    .query("tst_result == \'positive\'")\n'
                '    .groupby("exposure_setting")\n'
                "    .size()\n"
                '    .reset_index(name="n_positive")\n'
                '    .sort_values("n_positive", ascending=False)\n'
                ")"
            ),
        )

        code_panel = self.show_code(code_text, title="tb_contacts.py")

        note = Text(
            "TST 陽性接觸者依暴露場所排序 — 精準投入防疫資源",
            font=FONT_CJK,
            font_size=20,
            color=TEXT_SECONDARY,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner("Method Chaining 三大翻車現場")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_parens(self, duration: float = 5.0, **kwargs) -> None:
        """Blind spot 1: forgetting outer parentheses for multi-line chains."""
        error_code = kwargs.get("error_code", 'df.query("x > 1").groupby("a")  # no parens')
        correct_code = kwargs.get("correct_code", '(df.query("x > 1").groupby("a"))  # wrapped')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_inplace(self, duration: float = 5.0, **kwargs) -> None:
        """Blind spot 2: using inplace=True inside a chain breaks the chain."""
        error_code = kwargs.get("error_code", 'df.sort_values("a", inplace=True).head()')
        correct_code = kwargs.get("correct_code", 'df.sort_values("a").head()  # no inplace')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_query_syntax(self, duration: float = 5.0, **kwargs) -> None:
        """Blind spot 3: using & instead of 'and' inside .query() strings."""
        error_code = kwargs.get("error_code", 'df.query("age > 70 & infected == 1")')
        correct_code = kwargs.get("correct_code", 'df.query("age > 70 and infected == 1")')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card — preview next video on merge."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            "Method Chaining 流水線 — 完成！",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "下一集：merge 合併表格",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(max(0.1, duration - 1.6))
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
