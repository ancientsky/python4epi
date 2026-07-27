"""Ch04-01: SitRep Overview — 從 Line List 到疫情日報

Manim scene for the tutorial video on SitRep workflow overview,
using the Legionella outbreak investigation as the teaching narrative.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
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
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch04SitrepOverviewScene(EpiBaseScene):
    """Tutorial video scene: SitRep workflow overview."""

    total_steps: int = 16

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "SitRep 速成",
            "title_sub": "兩小時交出疫情日報",
            "five_sections_heading": "SitRep 五大區塊",
            "five_sec1": "1. 摘要指標：侵襲率、CFR、住院率",
            "five_sec2": "2. 人（Person）：年齡、性別、共病",
            "five_sec3": "3. 時（Time）：流行曲線",
            "five_sec4": "4. 地（Place）：各翼區侵襲率",
            "five_sec5": "5. 行動建議",
            "workflow_heading": "SitRep 工作流程",
            "workflow_p1": "1. 讀取 Line List (CSV)",
            "workflow_p2": "2. 清理日期欄位與欄位名稱",
            "workflow_p3": "3. 計算 KPI：侵襲率、致死率、住院率",
            "workflow_p4": "4. 繪製流行曲線、人地時分析",
            "workflow_p5": "5. 輸出報告（Word / PPT / PDF）",
            "summary_heading": "重點整理",
            "summary_p1": "1. SitRep = 疫情日報，快速掌握現況",
            "summary_p2": "2. 五大區塊：摘要、人、時、地、行動建議",
            "summary_p3": "3. 侵襲率與致死率是最重要的 KPI",
            "summary_p4": "4. 工作流程：讀取 → 清理 → 計算 → 視覺化 → 輸出",
            "summary_p5": "5. 函式化讓 SitRep 可以一鍵更新",
            "extra_banner_title": "額外範例：WHO SitRep 格式",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：描述流行病學（人）",
            "outro_sub": "感染者是誰？年齡、性別、共病分布一次看！",
        },
        "en": {
            "title_main": "SitRep Crash Course",
            "title_sub": "Ship your first situation report in two hours",
            "five_sections_heading": "The Five Sections of a SitRep",
            "five_sec1": "1. Key metrics: attack rate, CFR, hospitalization",
            "five_sec2": "2. Person: age, sex, comorbidities",
            "five_sec3": "3. Time: the epidemic curve",
            "five_sec4": "4. Place: attack rate by wing",
            "five_sec5": "5. Recommended actions",
            "workflow_heading": "The SitRep Workflow",
            "workflow_p1": "1. Read the line list (CSV)",
            "workflow_p2": "2. Clean the date fields and column names",
            "workflow_p3": "3. Compute KPIs: attack rate, CFR, hospitalization",
            "workflow_p4": "4. Draw the epi curve; analyze person, place, time",
            "workflow_p5": "5. Export the report (Word / PPT / PDF)",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. SitRep = situation report, grasp the status fast",
            "summary_p2": "2. Five sections: summary, person, time, place, actions",
            "summary_p3": "3. Attack rate and CFR are the most important KPIs",
            "summary_p4": "4. Workflow: read -> clean -> compute -> visualize -> export",
            "summary_p5": "5. Wrapping it in a function makes SitRep one-click",
            "extra_banner_title": "Extra example: the WHO SitRep format",
            "blindspot_banner_title": "3 Common Beginner Traps",
            "outro_heading": "Next up: descriptive epidemiology (Person)",
            "outro_sub": "Who got infected? Age, sex, and comorbidities at a glance!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the SitRep overview lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_five_sections(self, duration: float = 5.0, **kwargs) -> None:
        """Show the five sections of a SitRep."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            self.t("five_sections_heading"),
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("five_sec1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("five_sec2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("five_sec3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("five_sec4"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("five_sec5"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_data_prep(self, duration: float = 6.0, **kwargs) -> None:
        """Show data loading and preparation code."""
        self.show_step_indicator(2, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "\n"
                "df = pd.read_csv('legionella_outbreak.csv')\n"
                "df['symptom_onset_date'] = pd.to_datetime(\n"
                "    df['symptom_onset_date']\n"
                ")\n"
                "cases = df[df['case_classification'] == 'confirmed']"
            ),
        )

        output_text = kwargs.get(
            "output",
            "DataFrame: 280 rows x 32 columns\nConfirmed cases: 121",
        )

        self.show_code(code_lines, title="data_prep.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_kpi_metrics(self, duration: float = 6.0, **kwargs) -> None:
        """Show KPI metric calculations."""
        self.show_step_indicator(3, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "total = len(df)\n"
                "n_cases = len(cases)\n"
                "n_dead = (cases['outcome'] == 'dead').sum()\n"
                "ar = n_cases / total\n"
                "cfr = n_dead / n_cases\n"
                "print(f'AR={ar:.1%}, CFR={cfr:.1%}')"
            ),
        )

        output_text = kwargs.get(
            "output",
            "AR=43.2%, CFR=15.7%",
        )

        self.show_code(code_lines, title="kpi_metrics.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_workflow_diagram(self, duration: float = 5.0, **kwargs) -> None:
        """Show SitRep workflow as bullet points."""
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            self.t("workflow_heading"),
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("workflow_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("workflow_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("workflow_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("workflow_p4"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("workflow_p5"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_generate_sitrep(self, duration: float = 6.0, **kwargs) -> None:
        """Show generate_sitrep function skeleton."""
        self.show_step_indicator(5, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "def generate_sitrep(df):\n"
                "    cases = df[df['case_classification'] == 'confirmed']\n"
                "    ar = len(cases) / len(df)\n"
                "    cfr = (cases['outcome']=='dead').sum() / len(cases)\n"
                "    return {'AR': ar, 'CFR': cfr}"
            ),
        )

        self.show_code(code_lines, title="generate_sitrep.py")
        self.wait(duration)
        self.clear_screen()

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key points about SitRep overview."""
        self.show_step_indicator(6, self.total_steps)

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

    def show_extra_who_sitrep(self, duration: float = 6.0, **kwargs) -> None:
        """WHO SitRep example."""
        self.show_step_indicator(8, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# WHO-style SitRep structure\n"
                "sitrep = {\n"
                "    'report_date': '2026-01-20',\n"
                "    'total_cases': 121,\n"
                "    'new_cases_24h': 8,\n"
                "    'total_deaths': 19,\n"
                "    'cfr_pct': 15.7,\n"
                "}\n"
                "print(sitrep)"
            ),
        )

        self.show_code(code_lines, title="who_sitrep.py")
        self.wait(duration)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_timestamp(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: forgetting to add report timestamp."""
        error_code = kwargs.get("error_code", "sitrep = {'cases': 121}")
        correct_code = kwargs.get("correct_code", "sitrep = {'date': '2026-01-20', 'cases': 121}")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_denominator(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: reporting count without denominator."""
        error_code = kwargs.get("error_code", "print(f'Cases: {n_cases}')")
        correct_code = kwargs.get("correct_code", "print(f'AR: {n_cases}/{total} = {ar:.1%}')")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_table(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: dumping raw numbers instead of a table."""
        error_code = kwargs.get("error_code", "print(ar, cfr, hosp_rate)")
        correct_code = kwargs.get("correct_code", "pd.DataFrame([kpi], columns=['AR','CFR','Hosp'])")
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
