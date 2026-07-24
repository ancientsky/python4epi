"""Ch01-01: 數值變數 — 先把數字存起來

Manim scene for the tutorial video on Python variables, using the
Legionella outbreak investigation as the teaching narrative.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    UR,
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
    BG_WARM,
    CODE_BG,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    CodePanel,
    ErrorVsCorrect,
    ExtraExampleBanner,
    OutputPanel,
    StepIndicator,
    VariableBox,
)


class Ch01VariablesScene(EpiBaseScene):
    """Tutorial video scene: Python variables with the Legionella outbreak scenario."""

    total_steps: int = 13

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "數值變數",
            "title_sub": "先把數字存起來",
            "scenario_heading": "松柏護理之家 — 退伍軍人症群聚",
            "stat_total_label": "總住民人數",
            "stat_infected_label": "感染人數",
            "stat_deaths_label": "死亡人數",
            "scenario_caption": "這些數字需要存下來，才能在程式裡計算！",
            "first_var_explanation": "變數就像一個貼了標籤的盒子，裡面裝著數值",
            "first_var_arrow": "← 把 280 放進盒子",
            "remaining_note": "整數、字串都可以存進變數",
            "summary_heading": "重點整理",
            "summary_p1": "1. 變數 = 貼標籤的盒子，用 = 賦值",
            "summary_p2": "2. 名稱用英文小寫 + 底線（snake_case）",
            "summary_p3": "3. 整數直接寫數字，字串加引號",
            "summary_p4": "4. print() 可以把值印出來確認",
            "extra_banner_title": "額外範例：COVID-19 學校群聚",
            "blindspot_banner_title": "初學者常見地雷 3 選 1",
            "outro_heading": "下一集：用 Python 計算侵襲率與致死率",
            "outro_sub": "把變數拿來做算術運算！",
        },
        "en": {
            "title_main": "Numeric Variables",
            "title_sub": "Store your numbers first",
            "scenario_heading": "Pine & Cypress Nursing Home — Legionnaires' cluster",
            "stat_total_label": "Total residents",
            "stat_infected_label": "Infected",
            "stat_deaths_label": "Deaths",
            "scenario_caption": "We need to store these numbers to compute with them in code!",
            "first_var_explanation": "A variable is like a labeled box that holds a value",
            "first_var_arrow": "← put 280 into the box",
            "remaining_note": "Integers and strings can both go into variables",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. Variable = a labeled box; assign with =",
            "summary_p2": "2. Name it lowercase English + underscores (snake_case)",
            "summary_p3": "3. Integers are bare numbers; strings need quotes",
            "summary_p4": "4. print() shows the value so you can check it",
            "extra_banner_title": "Extra example: COVID-19 school cluster",
            "blindspot_banner_title": "3 Common Beginner Traps",
            "outro_heading": "Next up: compute attack rate and case fatality rate in Python",
            "outro_sub": "Put your variables to work with arithmetic!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the variables lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_scenario(self, duration: float = 5.0, **kwargs) -> None:
        """Show the outbreak numbers as the motivating context."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            self.t("scenario_heading"),
            font=FONT_CJK,
            font_size=32,
            color=TEXT_PRIMARY,
        ).to_edge(UP, buff=0.8)

        numbers = VGroup(
            self._make_stat_card("280", self.t("stat_total_label"), ACCENT_ORANGE),
            self._make_stat_card("121", self.t("stat_infected_label"), "#6A9BCC"),
            self._make_stat_card("19", self.t("stat_deaths_label"), "#D94452"),
        ).arrange(RIGHT, buff=0.6).move_to(ORIGIN)

        caption = Text(
            self.t("scenario_caption"),
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(numbers, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(numbers, lag_ratio=0.3), run_time=1.0)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(duration - 2.1)
        self.play(FadeOut(VGroup(heading, numbers, caption)), run_time=0.5)

    def show_first_variable(self, duration: float = 6.0, **kwargs) -> None:
        """Animate the first variable assignment with the box metaphor."""
        self.show_step_indicator(2, self.total_steps)

        code_text = kwargs.get("code", "total_residents = 280")

        explanation = Text(
            self.t("first_var_explanation"),
            font=FONT_CJK,
            font_size=24,
            color=TEXT_PRIMARY,
        ).to_edge(UP, buff=1.0)

        code_panel = CodePanel(
            code_text,
            title="Python",
            width=6.0,
            height=1.6,
        ).shift(LEFT * 2 + UP * 0.3)

        box = VariableBox(
            label="total_residents",
            value="280",
            width=3.2,
            height=1.6,
        ).shift(RIGHT * 2.8 + UP * 0.3)

        arrow_label = Text(
            self.t("first_var_arrow"),
            font=FONT_CJK,
            font_size=20,
            color=ACCENT_ORANGE,
        ).next_to(box, DOWN, buff=0.4)

        self.play(FadeIn(explanation), run_time=0.5)
        self.play(Create(code_panel), run_time=0.8)
        self.play(FadeIn(box), run_time=0.8)
        self.play(FadeIn(arrow_label), run_time=0.5)
        self.wait(duration - 2.6)
        self.play(FadeOut(VGroup(explanation, code_panel, box, arrow_label)), run_time=0.5)

    def show_remaining_variables(self, duration: float = 6.0, **kwargs) -> None:
        """Show the remaining variable assignments for the outbreak dataset."""
        self.show_step_indicator(3, self.total_steps)

        code_lines = (
            "total_residents = 280\n"
            "infected        = 121\n"
            "deaths          = 19\n"
            "onset_start     = '2026-01-12'\n"
            "onset_end       = '2026-01-28'"
        )

        code_panel = CodePanel(
            code_lines,
            title="outbreak_vars.py",
            width=7.0,
            height=3.2,
        ).shift(LEFT * 1.2 + UP * 0.2)

        note = Text(
            self.t("remaining_note"),
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(code_panel, DOWN, buff=0.5)

        self.play(Create(code_panel), run_time=1.0)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(code_panel, note)), run_time=0.5)

    def show_print(self, duration: float = 5.0, **kwargs) -> None:
        """Show print() usage and its output."""
        self.show_step_indicator(4, self.total_steps)

        code_lines = (
            "total_residents = 280\n"
            "infected        = 121\n"
            "\n"
            "print('總住民人數:', total_residents)\n"
            "print('感染人數:',   infected)"
        )

        output_text = "總住民人數: 280\n感染人數: 121"

        code_panel = self.show_code(code_lines, title="print_demo.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        """Summarise key points about variables."""
        self.show_step_indicator(5, self.total_steps)

        heading = Text(
            self.t("summary_heading"),
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("summary_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("summary_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("summary_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("summary_p4"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

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

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        """COVID-19 school cluster example demonstrating variables."""
        self.show_step_indicator(6, self.total_steps)

        code_lines = (
            "# COVID-19 某校群聚事件\n"
            "school_students  = 1200\n"
            "covid_cases      = 87\n"
            "hospitalized     = 5\n"
            "quarantine_days  = 14\n"
            "\n"
            "print(f'確診人數: {covid_cases}')\n"
            "print(f'住院人數: {hospitalized}')"
        )

        output_text = "確診人數: 87\n住院人數: 5"

        code_panel = self.show_code(code_lines, title="covid_school.py")
        self.wait(1.2)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.2)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_string_vs_int(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: string literal '86' vs integer 86."""
        error_code = kwargs.get("error_code", 'cases = "86"   # 這是文字，不能做加法！')
        correct_code = kwargs.get("correct_code", "cases = 86     # 這才是數字，可以計算")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_case_sensitive(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: Cases (capital C) vs cases (lowercase)."""
        error_code = kwargs.get("error_code", "Cases = 121\nprint(cases)  # NameError!")
        correct_code = kwargs.get("correct_code", "cases = 121\nprint(cases)  # 121")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_reversed_assignment(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: 280 = x (SyntaxError) vs x = 280."""
        error_code = kwargs.get("error_code", "280 = total_residents  # SyntaxError!")
        correct_code = kwargs.get("correct_code", "total_residents = 280  # 正確！")
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

    def _make_stat_card(self, value: str, label: str, color: str) -> VGroup:
        """Create a simple stat card with a big number and a label."""
        val_text = Text(value, font=FONT_MONO, font_size=48, color=color)
        lbl_text = Text(label, font=FONT_CJK, font_size=20, color=TEXT_SECONDARY)
        lbl_text.next_to(val_text, DOWN, buff=0.15)
        return VGroup(val_text, lbl_text)
