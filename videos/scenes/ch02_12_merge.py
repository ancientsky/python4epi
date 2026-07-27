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
    ExtraExampleBanner,
)


class Ch02MergeScene(EpiBaseScene):
    """Tutorial video scene: pandas merge with the Legionella outbreak scenario."""

    total_steps: int = 14

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "合併資料表",
            "title_sub": "merge 就是你的 VLOOKUP",
            "why_heading": "疫調資料散落各處",
            "tbl1": "個案名冊",
            "tbl2": "實驗室報告",
            "tbl3": "住院紀錄",
            "why_arrow": "merge() → 一行搞定合併",
            "how_heading": "how 參數：四種合併方式",
            "join_left_desc": "保留左表所有列",
            "join_left_note": "VLOOKUP（疫調首選）",
            "join_inner_desc": "只保留兩邊都有",
            "join_inner_note": "pandas 預設，小心！",
            "join_outer_desc": "兩邊全部保留",
            "join_outer_note": "完整合併",
            "join_right_desc": "保留右表所有列",
            "join_right_note": "比較少用",
            "diff_keys_note": "欄位名不同？left_on + right_on 解決！",
            "validate_note": "validate 幫你抓蟲：預期的關係 vs 實際的資料",
            "summary_heading": "重點整理",
            "summary_p1": "1. merge = Python 版 VLOOKUP，更強更不易出錯",
            "summary_p2": '2. how="left" 是疫調首選，不遺漏任何個案',
            "summary_p3": "3. 欄位名不同就用 left_on + right_on",
            "summary_p4": "4. 用 validate 檢查預期的對應關係",
            "extra_banner_title": "額外範例：疫苗接種紀錄連結",
            "blindspot_banner_title": "merge 三大翻車現場",
            "outro_heading": "下一集：文字清理三板斧",
            "outro_sub": "str + drop_duplicates + rename，把髒資料變乾淨！",
        },
        "en": {
            "title_main": "Joining Data Tables",
            "title_sub": "merge is your VLOOKUP",
            "why_heading": "Investigation data is scattered everywhere",
            "tbl1": "Case roster",
            "tbl2": "Lab reports",
            "tbl3": "Hospital records",
            "why_arrow": "merge() → joins them in one line",
            "how_heading": "The how parameter: four ways to join",
            "join_left_desc": "keeps every row of the left table",
            "join_left_note": "VLOOKUP (top pick for investigations)",
            "join_inner_desc": "keeps only rows in both",
            "join_inner_note": "pandas default, watch out!",
            "join_outer_desc": "keeps all rows from both",
            "join_outer_note": "full merge",
            "join_right_desc": "keeps every row of the right table",
            "join_right_note": "less common",
            "diff_keys_note": "Different column names? left_on + right_on solves it!",
            "validate_note": "validate catches bugs: expected relationship vs actual data",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. merge = Python's VLOOKUP, stronger and less error-prone",
            "summary_p2": '2. how="left" is the go-to for investigations, drops no case',
            "summary_p3": "3. Different column names? Use left_on + right_on",
            "summary_p4": "4. Use validate to check the expected relationship",
            "extra_banner_title": "Extra example: linking vaccination records",
            "blindspot_banner_title": "3 merge Wipeouts",
            "outro_heading": "Next up: three moves for text cleanup",
            "outro_sub": "str + drop_duplicates + rename to turn dirty data clean!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the merge lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_why_merge(self, duration: float = 7.0, **kwargs) -> None:
        """Step 1: why merge is essential in epidemiology."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            self.t("why_heading"),
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        tables = VGroup(
            self._make_table_card(self.t("tbl1"), "case_id, age, sex...", ACCENT_ORANGE),
            self._make_table_card(self.t("tbl2"), "case_id, ct_value...", ACCENT_BLUE),
            self._make_table_card(self.t("tbl3"), "patient_id, icu...", ACCENT_GREEN),
        ).arrange(RIGHT, buff=0.5).next_to(heading, DOWN, buff=0.6)

        arrow_text = Text(
            self.t("why_arrow"),
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

        self.show_code(code_text, title="merge_basic.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_how_parameter(self, duration: float = 8.0, **kwargs) -> None:
        """Step 3: the four join types."""
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            self.t("how_heading"),
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        rows = VGroup(
            self._make_join_row("left", self.t("join_left_desc"), self.t("join_left_note")),
            self._make_join_row("inner", self.t("join_inner_desc"), self.t("join_inner_note")),
            self._make_join_row("outer", self.t("join_outer_desc"), self.t("join_outer_note")),
            self._make_join_row("right", self.t("join_right_desc"), self.t("join_right_note")),
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

        self.show_code(code_text, title="different_keys.py")

        note = Text(
            self.t("diff_keys_note"),
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

        self.show_code(code_text, title="validate.py")

        note = Text(
            self.t("validate_note"),
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
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example methods
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the ExtraExampleBanner section divider."""
        banner = ExtraExampleBanner(self.t("extra_banner_title"))
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

        self.show_code(code_text, title="vaccine_merge.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
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
