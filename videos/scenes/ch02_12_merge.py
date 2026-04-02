"""Ch02-12: 合併資料表 — merge 就是你的 VLOOKUP

Manim scene for the tutorial video on pandas merge (joining DataFrames),
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
    ACCENT_BLUE,
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


class Ch02MergeScene(EpiBaseScene):
    """Tutorial video scene: pandas merge with the Legionella outbreak scenario."""

    total_steps: int = 14

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the merge lesson."""
        self.show_title_card("合併資料表", "merge 就是你的 VLOOKUP", duration=duration)

    def show_why_merge(self, duration: float = 7.0, **kwargs) -> None:
        """Step 1: why merge is essential in epidemiology."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "疫調資料散落各處",
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        tables = VGroup(
            self._make_table_card("個案名冊", "case_id, age, sex...", ACCENT_ORANGE),
            self._make_table_card("實驗室報告", "case_id, ct_value...", ACCENT_BLUE),
            self._make_table_card("住院紀錄", "patient_id, icu...", ACCENT_GREEN),
        ).arrange(RIGHT, buff=0.5).next_to(heading, DOWN, buff=0.6)

        arrow_text = Text(
            "merge() → 一行搞定合併",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(tables, DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(tables, lag_ratio=0.3), run_time=1.0)
        self.play(FadeIn(arrow_text), run_time=0.5)
        self.wait(duration - 2.0)
        self.play(FadeOut(VGroup(heading, tables, arrow_text)), run_time=0.5)

    def show_merge_basic(self, duration: float = 7.0, **kwargs) -> None:
        """Step 2: basic merge with on and how='left'."""
        self.show_step_indicator(2, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "merged = pd.merge(\n"
                "    cases_df, lab_df,\n"
                '    on="case_id", how="left"\n'
                ")"
            ),
        )

        output_text = kwargs.get(
            "output",
            "cases: 280 rows -> merged: 280 rows (lab matched: 241)",
        )

        code_panel = self.show_code(code_text, title="merge_basic.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_how_parameter(self, duration: float = 8.0, **kwargs) -> None:
        """Step 3: the four join types."""
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            "how 參數：四種合併方式",
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        rows = VGroup(
            self._make_join_row("left", "保留左表所有列", "VLOOKUP（疫調首選）"),
            self._make_join_row("inner", "只保留兩邊都有", "pandas 預設，小心！"),
            self._make_join_row("outer", "兩邊全部保留", "完整合併"),
            self._make_join_row("right", "保留右表所有列", "比較少用"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(rows, lag_ratio=0.2), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, rows)), run_time=0.5)

    def show_merge_different_keys(self, duration: float = 6.0, **kwargs) -> None:
        """Step 4: left_on / right_on for different column names."""
        self.show_step_indicator(4, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "merged = pd.merge(\n"
                "    cases_df, lab_df,\n"
                '    left_on="case_id",\n'
                '    right_on="patient_id",\n'
                '    how="left"\n'
                ")"
            ),
        )

        code_panel = self.show_code(code_text, title="different_keys.py")

        note = Text(
            "欄位名不同？left_on + right_on 解決！",
            font=FONT_CJK,
            font_size=20,
            color=TEXT_SECONDARY,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_validate(self, duration: float = 6.0, **kwargs) -> None:
        """Step 5: validate parameter to catch unexpected many-to-many."""
        self.show_step_indicator(5, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "merged = pd.merge(\n"
                "    cases_df, lab_df,\n"
                '    on="case_id", how="left",\n'
                '    validate="one_to_one"\n'
                ")"
            ),
        )

        code_panel = self.show_code(code_text, title="validate.py")

        note = Text(
            "validate 幫你抓蟲：預期的關係 vs 實際的資料",
            font=FONT_CJK,
            font_size=20,
            color=ACCENT_ORANGE,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Step 6: summarize key points."""
        self.show_step_indicator(6, self.total_steps)

        heading = Text(
            "重點整理",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text('1. merge = Python 版 VLOOKUP，更強更不易出錯', font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text('2. how="left" 是疫調首選，不遺漏任何個案', font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("3. 欄位名不同就用 left_on + right_on", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("4. 用 validate 檢查預期的對應關係", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
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
        banner = ExtraExampleBanner("額外範例：疫苗接種紀錄連結")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 7.0, **kwargs) -> None:
        """Vaccine records linkage example demonstrating merge."""
        self.show_step_indicator(8, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "merged = pd.merge(\n"
                "    cases_df, vaccine_df,\n"
                '    on="case_id", how="left"\n'
                ")\n"
                'merged["vaccinated"] = merged["vaccine_date"].notna()'
            ),
        )

        code_panel = self.show_code(code_text, title="vaccine_merge.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner("merge 三大翻車現場")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_duplicate_keys(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: many-to-many row explosion."""
        error_code = kwargs.get("error_code", 'pd.merge(df1, df2, on="name")  # duplicates!')
        correct_code = kwargs.get("correct_code", 'pd.merge(df1, df2, on="name", validate="1:m")')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_inner_default(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: inner join by default loses rows."""
        error_code = kwargs.get("error_code", 'pd.merge(cases, labs, on="id")  # inner join')
        correct_code = kwargs.get("correct_code", 'pd.merge(cases, labs, on="id", how="left")')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_suffix_collision(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: suffix collision on same-name columns."""
        error_code = kwargs.get("error_code", 'result["date"]  # KeyError: date_x / date_y')
        correct_code = kwargs.get("correct_code", 'pd.merge(a, b, on="id", suffixes=("_case","_lab"))')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            "下一集：文字清理三板斧",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "str + drop_duplicates + rename，把髒資料變乾淨！",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _make_table_card(self, title: str, columns: str, color: str) -> VGroup:
        """Create a small card representing a data table."""
        t = Text(title, font=FONT_CJK, font_size=22, color=color)
        c = Text(columns, font=FONT_MONO, font_size=14, color=TEXT_SECONDARY)
        c.next_to(t, DOWN, buff=0.15)
        return VGroup(t, c)

    def _make_join_row(self, how: str, desc: str, note: str) -> VGroup:
        """Create a row for the join type comparison."""
        label = Text(f'"{how}"', font=FONT_MONO, font_size=20, color=ACCENT_ORANGE)
        description = Text(f" — {desc}", font=FONT_CJK, font_size=20, color=TEXT_PRIMARY)
        annotation = Text(f"  ({note})", font=FONT_CJK, font_size=16, color=TEXT_SECONDARY)
        description.next_to(label, RIGHT, buff=0.1)
        annotation.next_to(description, RIGHT, buff=0.1)
        return VGroup(label, description, annotation)
