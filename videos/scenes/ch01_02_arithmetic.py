"""Ch01-02: 計算指標 — 用 Python 做流行病學運算

Manim scene for the tutorial video on arithmetic operations applied to
epi metrics (侵襲率, 致死率, 住院率), using the Legionella outbreak.
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


class Ch01ArithmeticScene(EpiBaseScene):
    """Tutorial video scene: arithmetic operators for epi metric calculation."""

    total_steps: int = 12

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "計算指標",
            "title_sub": "用 Python 算出侵襲率與致死率",
            "attack_rate_formula": "侵襲率 = 感染人數 ÷ 總住民人數",
            "cfr_formula": "致死率 = 死亡人數 ÷ 感染人數",
            "hosp_rate_formula": "住院率 = 住院人數 ÷ 感染人數",
            "summary_heading": "重點整理",
            "summary_p1": "1. / 是浮點除法，// 是整數除法（取商）",
            "summary_p2": "2. f-string：f'文字 {變數:.2%}' 格式化輸出",
            "summary_p3": "3. :.2% 自動乘以 100、加 % 號、保留兩位小數",
            "summary_p4": "4. 侵襲率、致死率、住院率都只是「除法」！",
            "extra_banner_title": "額外範例：登革熱盛行率調查",
            "blindspot_banner_title": "初學者常見地雷 3 選 1",
            "format_spec_heading": ":.2% 格式說明",
            "format_spec_p1": ": 開始格式指定符",
            "format_spec_p2": ".2 保留兩位小數",
            "format_spec_p3": "% 自動 × 100 並加上 % 號",
            "outro_heading": "下一集：用字典整理多欄位資料",
            "outro_sub": "把多個變數打包成一張「資料卡」！",
        },
        "en": {
            "title_main": "Computing Metrics",
            "title_sub": "Compute attack rate and CFR in Python",
            "attack_rate_formula": "Attack rate = infected ÷ total residents",
            "cfr_formula": "Case fatality rate = deaths ÷ infected",
            "hosp_rate_formula": "Hospitalization rate = hospitalized ÷ infected",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. / is float division, // is integer division (quotient)",
            "summary_p2": "2. f-string: f'text {var:.2%}' formats the output",
            "summary_p3": "3. :.2% auto-multiplies by 100, adds %, keeps two decimals",
            "summary_p4": "4. Attack rate, CFR, hospitalization rate are all just 'division'!",
            "extra_banner_title": "Extra example: dengue prevalence survey",
            "blindspot_banner_title": "3 Common Beginner Traps",
            "format_spec_heading": "The :.2% format, explained",
            "format_spec_p1": ": starts the format specifier",
            "format_spec_p2": ".2 keeps two decimal places",
            "format_spec_p3": "% auto ×100 and appends the % sign",
            "outro_heading": "Next up: organize multi-field data with dictionaries",
            "outro_sub": "Pack several variables into one 'data card'!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the arithmetic lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_attack_rate(self, duration: float = 7.0, **kwargs) -> None:
        """Show attack rate (侵襲率) calculation with code and output."""
        self.show_step_indicator(1, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "total_residents = 280\n"
                "infected        = 121\n"
                "\n"
                "# 侵襲率 = 感染人數 / 總暴露人數\n"
                "attack_rate = infected / total_residents\n"
                "\n"
                "print(f'侵襲率: {attack_rate:.2%}')"
            ),
        )

        output_text = kwargs.get(
            "output",
            "侵襲率: 43.21%",
        )

        formula = Text(
            self.t("attack_rate_formula"),
            font=FONT_CJK,
            font_size=24,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.7)

        self.play(FadeIn(formula), run_time=0.5)
        self.show_code(code_lines, title="attack_rate.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(duration - 1.5)
        self.clear_screen()

    def show_cfr(self, duration: float = 7.0, **kwargs) -> None:
        """Show case fatality rate (致死率) calculation."""
        self.show_step_indicator(2, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "infected = 121\n"
                "deaths   = 19\n"
                "\n"
                "# 致死率 = 死亡人數 / 確診人數\n"
                "cfr = deaths / infected\n"
                "\n"
                "print(f'致死率: {cfr:.2%}')"
            ),
        )

        output_text = kwargs.get(
            "output",
            "致死率: 15.70%",
        )

        formula = Text(
            self.t("cfr_formula"),
            font=FONT_CJK,
            font_size=24,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.7)

        self.play(FadeIn(formula), run_time=0.5)
        self.show_code(code_lines, title="cfr.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(duration - 1.5)
        self.clear_screen()

    def show_hosp_rate(self, duration: float = 7.0, **kwargs) -> None:
        """Show hospitalization rate calculation."""
        self.show_step_indicator(3, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "infected     = 121\n"
                "hospitalized = 43\n"
                "\n"
                "# 住院率 = 住院人數 / 感染人數\n"
                "hosp_rate = hospitalized / infected\n"
                "\n"
                "print(f'住院率: {hosp_rate:.2%}')"
            ),
        )

        output_text = kwargs.get(
            "output",
            "住院率: 35.54%",
        )

        formula = Text(
            self.t("hosp_rate_formula"),
            font=FONT_CJK,
            font_size=24,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.7)

        self.play(FadeIn(formula), run_time=0.5)
        self.show_code(code_lines, title="hosp_rate.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(duration - 1.5)
        self.clear_screen()

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        """Summarise arithmetic operators and f-string formatting."""
        self.show_step_indicator(4, self.total_steps)

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
        """Dengue prevalence example demonstrating the same arithmetic pattern."""
        self.show_step_indicator(5, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# 登革熱血清調查（南台灣某村）\n"
                "surveyed     = 500\n"
                "seropositive = 137\n"
                "severe_cases = 12\n"
                "\n"
                "prevalence = seropositive / surveyed\n"
                "severity   = severe_cases / seropositive\n"
                "\n"
                "print(f'盛行率: {prevalence:.2%}')\n"
                "print(f'重症比: {severity:.2%}')"
            ),
        )

        output_text = kwargs.get(
            "output",
            "盛行率: 27.40%\n重症比: 8.76%",
        )

        self.show_code(code_lines, title="dengue_prevalence.py")
        self.wait(1.2)
        self.show_output(output_text)
        self.wait(duration - 1.2)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_division(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: integer floor division // vs float division /."""
        error_code = kwargs.get(
            "error_code",
            "rate = 19 // 121   # 結果是 0！整數除法直接捨去",
        )
        correct_code = kwargs.get(
            "correct_code",
            "rate = 19 / 121    # 結果是 0.157...，才對",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_fstring(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: missing f prefix in f-string."""
        error_code = kwargs.get(
            "error_code",
            "print('侵襲率: {attack_rate:.2%}')  # 沒有 f！",
        )
        correct_code = kwargs.get(
            "correct_code",
            "print(f'侵襲率: {attack_rate:.2%}')  # 加上 f",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_format_spec(self, duration: float = 5.0, **kwargs) -> None:
        """Explain the :.2% format specifier step by step."""
        self.show_step_indicator(8, self.total_steps)

        heading = Text(
            self.t("format_spec_heading"),
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        parts = VGroup(
            Text(self.t("format_spec_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("format_spec_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("format_spec_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(heading, DOWN, buff=0.5)

        example = Text(
            "0.4321  →  43.21%",
            font=FONT_MONO,
            font_size=26,
            color=ACCENT_GREEN,
        ).next_to(parts, DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(parts, lag_ratio=0.3), run_time=1.0)
        self.play(FadeIn(example), run_time=0.5)
        self.wait(duration - 1.9)
        self.play(FadeOut(VGroup(heading, parts, example)), run_time=0.5)

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
