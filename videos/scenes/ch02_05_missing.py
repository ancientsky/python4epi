"""Ch02-05: 遺漏值偵探社 — NaN, NaT, None 一次搞懂

Manim scene for the tutorial video on handling missing values in pandas,
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
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_GREEN,
    ACCENT_ORANGE,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    CodePanel,
    ExtraExampleBanner,
)


class Ch02MissingScene(EpiBaseScene):
    """Tutorial video scene: handling missing values in pandas."""

    total_steps: int = 13

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "遺漏值偵探社",
            "title_sub": "NaN, NaT, None 一次搞懂",
            "three_heading": "遺漏值三兄弟",
            "three_p1": "NaN  — 數字欄位的遺漏值（float）",
            "three_p2": "NaT  — 日期欄位的遺漏值（datetime）",
            "three_p3": "None — Python 通用的空值",
            "struct_heading": "兩種遺漏值，處理方式大不同",
            "struct_ok": "結構性遺漏 (OK)：death_date 存活者本來就沒有",
            "struct_ng": "資料錯誤 (NG)：symptom_onset_date 不該漏填",
            "struct_note": "先判斷「為什麼遺漏」，再決定「怎麼處理」",
            "fill_note": "fillna 適合可推估的欄位；dropna 適合關鍵欄位缺失時",
            "summary_heading": "重點整理",
            "summary_p1": "1. NaN/NaT/None 都是遺漏值，isnull() 一網打盡",
            "summary_p2": "2. 先用 isnull().sum() 掌握全貌",
            "summary_p3": "3. 區分結構性遺漏 vs 資料錯誤再處理",
            "summary_p4": "4. fillna 填補 / dropna 刪除，依情境選擇",
            "extra_banner_title": "額外範例：疫苗接種紀錄",
            "blindspot_banner_title": "遺漏值經典地雷 3 選",
            "outro_heading": "下一集：groupby 分組統計",
            "outro_sub": "把資料分組，算出每組的侵襲率與致死率！",
        },
        "en": {
            "title_main": "The Missing-Value Detective Agency",
            "title_sub": "NaN, NaT, None demystified at once",
            "three_heading": "The Three Missing-Value Brothers",
            "three_p1": "NaN  — missing value in numeric columns (float)",
            "three_p2": "NaT  — missing value in date columns (datetime)",
            "three_p3": "None — Python's all-purpose null",
            "struct_heading": "Two Kinds of Missing, Very Different Fixes",
            "struct_ok": "Structural missing (OK): survivors simply have no death_date",
            "struct_ng": "Data error (NG): symptom_onset_date should never be blank",
            "struct_note": "First ask 'why is it missing', then decide 'how to handle it'",
            "fill_note": "fillna fits estimable columns; dropna fits missing key columns",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. NaN/NaT/None are all missing; isnull() catches them all",
            "summary_p2": "2. Use isnull().sum() first to see the full picture",
            "summary_p3": "3. Tell structural missing from data errors before acting",
            "summary_p4": "4. fillna to fill / dropna to drop, pick by context",
            "extra_banner_title": "Extra example: vaccination records",
            "blindspot_banner_title": "3 Classic Missing-Value Traps",
            "outro_heading": "Next up: groupby aggregation",
            "outro_sub": "Group the data and compute each group's attack rate and CFR!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the missing values lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_nan_nat_none(self, duration: float = 7.0, **kwargs) -> None:
        """Step 1: introduce the three types of missing values."""
        self.show_step_indicator(1, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "import numpy as np\n"
                "\n"
                "print(type(np.nan))   # float\n"
                "print(type(pd.NaT))   # NaTType\n"
                "print(type(None))     # NoneType"
            ),
        )

        heading = Text(
            self.t("three_heading"),
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        bullets = VGroup(
            Text(self.t("three_p1"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("three_p2"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("three_p3"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(RIGHT * 2.0 + DOWN * 0.2)

        code_panel = CodePanel(
            code_text,
            title="missing_types.py",
            width=6.0,
            height=3.2,
        ).shift(LEFT * 2.0 + DOWN * 0.2)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(Create(code_panel), run_time=0.8)
        self.play(FadeIn(bullets, lag_ratio=0.2), run_time=0.8)
        self.wait(max(0.1, duration - 2.1))
        self.play(FadeOut(VGroup(heading, code_panel, bullets)), run_time=0.5)

    def show_isnull_sum(self, duration: float = 6.0, **kwargs) -> None:
        """Step 2: show isnull().sum() to count missing values."""
        self.show_step_indicator(2, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 統計每欄的遺漏值數量\n"
                "df.isnull().sum()"
            ),
        )
        output_text = kwargs.get(
            "output",
            (
                "age                  0\n"
                "symptom_onset_date   3\n"
                "death_date         261\n"
                "hospitalization_date  5\n"
                "dtype: int64"
            ),
        )

        self.show_code(code_text, title="check_missing.py")
        self.wait(0.8)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 0.8))
        self.clear_screen()

    def show_structural_vs_error(self, duration: float = 6.0, **kwargs) -> None:
        """Step 3: distinguish structural vs error missing data."""
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            self.t("struct_heading"),
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        ok_text = Text(
            self.t("struct_ok"),
            font=FONT_CJK,
            font_size=22,
            color=ACCENT_GREEN,
        )
        ng_text = Text(
            self.t("struct_ng"),
            font=FONT_CJK,
            font_size=22,
            color="#D94452",
        )

        bullets = VGroup(ok_text, ng_text).arrange(
            DOWN, aligned_edge=LEFT, buff=0.5,
        ).next_to(heading, DOWN, buff=0.8)

        note = Text(
            self.t("struct_note"),
            font=FONT_CJK,
            font_size=20,
            color=TEXT_SECONDARY,
        ).next_to(bullets, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(bullets, lag_ratio=0.3), run_time=0.8)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(max(0.1, duration - 1.8))
        self.play(FadeOut(VGroup(heading, bullets, note)), run_time=0.5)

    def show_loc_filter(self, duration: float = 6.0, **kwargs) -> None:
        """Step 4: filter rows with missing values using .loc."""
        self.show_step_indicator(4, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 找出缺少發病日的個案\n"
                "missing_onset = df.loc[\n"
                "    df['symptom_onset_date'].isnull()\n"
                "]\n"
                "print(f'缺少發病日: {len(missing_onset)} 筆')"
            ),
        )
        output_text = kwargs.get("output", "缺少發病日: 3 筆")

        self.show_code(code_text, title="filter_missing.py")
        self.wait(0.8)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 0.8))
        self.clear_screen()

    def show_fillna_dropna(self, duration: float = 6.0, **kwargs) -> None:
        """Step 5: show fillna and dropna usage."""
        self.show_step_indicator(5, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 填補：用中位數填補年齡遺漏值\n"
                "df['age'].fillna(df['age'].median(), inplace=True)\n"
                "\n"
                "# 刪除：只刪除發病日遺漏的列\n"
                "df_clean = df.dropna(subset=['symptom_onset_date'])"
            ),
        )

        self.show_code(code_text, title="fill_or_drop.py")

        note = Text(
            self.t("fill_note"),
            font=FONT_CJK,
            font_size=20,
            color=TEXT_SECONDARY,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(note), run_time=0.5)
        self.wait(max(0.1, duration - 0.5))
        self.clear_screen()

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
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
        """Vaccine records example demonstrating missing value handling."""
        self.show_step_indicator(7, self.total_steps)

        code_text = kwargs.get(
            "code",
            (
                "# 疫苗接種紀錄常見遺漏值\n"
                "vax = pd.DataFrame({\n"
                "    'patient_id': ['P01', 'P02', 'P03'],\n"
                "    'dose_1_date': ['2025-03-01', None, '2025-04-10'],\n"
                "    'dose_2_date': [None, None, '2025-05-08'],\n"
                "})\n"
                "\n"
                "print(vax.isnull().sum())"
            ),
        )
        output_text = kwargs.get(
            "output",
            (
                "patient_id     0\n"
                "dose_1_date    1\n"
                "dose_2_date    2\n"
                "dtype: int64"
            ),
        )

        self.show_code(code_text, title="vaccine_missing.py")
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

    def show_blindspot_nan_compare(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: == None vs isnull()."""
        error_code = kwargs.get("error_code", "df[df['age'] == None]  # always empty!")
        correct_code = kwargs.get("correct_code", "df[df['age'].isnull()]  # correct way")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_dropna_aggressive(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: dropna() all vs dropna(subset=...)."""
        error_code = kwargs.get("error_code", "df.dropna()  # drops too many rows!")
        correct_code = kwargs.get("correct_code", "df.dropna(subset=['onset_date'])  # targeted")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_fillna_zero(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: fillna(0) vs fillna(median)."""
        error_code = kwargs.get("error_code", "df['age'].fillna(0)  # 0 skews the mean!")
        correct_code = kwargs.get("correct_code", "df['age'].fillna(df['age'].median())  # better")
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
