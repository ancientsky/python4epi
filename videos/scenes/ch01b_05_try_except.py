"""Ch01b-05: try/except——優雅處理意外

Manim scene for the tutorial video on Python error handling,
using the Legionella outbreak investigation as the teaching narrative.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    UP,
    Create,
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
    CodePanel,
    ExtraExampleBanner,
)


class Ch01bTryExceptScene(EpiBaseScene):
    """Tutorial video scene: try/except error handling."""

    total_steps: int = 13

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "try / except",
            "title_sub": "優雅處理意外",
            "multi_heading": "多重 except — 不同錯誤不同處理",
            "summary_heading": "重點整理",
            "summary_p1": "1. try 放可能出錯的程式碼",
            "summary_p2": "2. except 指定錯誤類型來處理",
            "summary_p3": "3. 不要 bare except（吞掉所有錯誤）",
            "summary_p4": "4. 只包住「不可控的外部資料」",
            "extra_banner_title": "額外範例：清洗疫苗接種紀錄",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：字串方法與迴圈進階",
            "outro_sub": "清理疫調資料的瑞士刀！",
        },
        "en": {
            "title_main": "try / except",
            "title_sub": "Handle surprises gracefully",
            "multi_heading": "Multiple except — different errors, different handling",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. Put risky code inside try",
            "summary_p2": "2. except names the error type to handle",
            "summary_p3": "3. No bare except (it swallows every error)",
            "summary_p4": "4. Only wrap uncontrollable external data",
            "extra_banner_title": "Extra example: cleaning vaccination records",
            "blindspot_banner_title": "3 Common Beginner Pitfalls",
            "outro_heading": "Next up: string methods and advanced loops",
            "outro_sub": "The Swiss army knife for cleaning outbreak data!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_basic_syntax(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        code_text = kwargs.get("code",
            'try:\n    result = int("N/A")\nexcept ValueError:\n    result = 0\n    print("bad value, using 0")')
        output_text = kwargs.get("output", "bad value, using 0")
        self.show_code(code_text, title="try_basic.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_real_scenario(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        code_text = kwargs.get("code",
            'raw = ["72", "85", "N/A", "68", ""]\nages = []\nskipped = 0\n'
            "for val in raw:\n    try:\n        ages.append(int(val))\n"
            "    except ValueError:\n        skipped += 1\n"
            'print(f"valid: {len(ages)}, skipped: {skipped}")')
        output_text = kwargs.get("output", "valid: 3, skipped: 2")
        self.show_code(code_text, title="clean_ages.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    def show_multiple_except(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        code_text = kwargs.get("code",
            'try:\n    f = open("report.csv")\nexcept FileNotFoundError:\n'
            '    print("file not found!")\nexcept PermissionError:\n    print("no permission!")')

        heading = Text(
            self.t("multi_heading"),
            font=FONT_CJK, font_size=26, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        code_panel = CodePanel(code_text, title="multi_except.py", width=8.0, height=3.2).next_to(heading, DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(Create(code_panel), run_time=0.8)
        self.wait(max(0.1, duration - 1.2))
        self.play(FadeOut(VGroup(heading, code_panel)), run_time=0.5)

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        heading = Text(self.t("summary_heading"), font=FONT_CJK, font_size=34, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        points = VGroup(
            Text(self.t("summary_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("summary_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("summary_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("summary_p4"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)
        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        banner = ExtraExampleBanner(self.t("extra_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        code_text = kwargs.get("code",
            'from datetime import date\nraw_dates = ["2025-03-15", "", "N/A"]\n'
            "for d in raw_dates:\n    try:\n        parsed = date.fromisoformat(d)\n"
            '        print(f"vaccinated: {parsed}")\n    except ValueError:\n'
            '        print(f"skipped: {d!r}")')
        output_text = kwargs.get("output", "vaccinated: 2025-03-15\nskipped: ''\nskipped: 'N/A'")
        self.show_code(code_text, title="vaccine_clean.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.0))
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_bare_except(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "try:\n    x = bad()\nexcept:\n    pass")
        correct_code = kwargs.get("correct_code", "try:\n    x = bad()\nexcept ValueError:\n    print('bad!')")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_too_broad(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "try:\n    # 100 lines here\nexcept: ...")
        correct_code = kwargs.get("correct_code", "# only wrap risky line\ntry:\n    val = int(x)")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_hide_bug(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "try:\n    print(infceted)\nexcept: pass")
        correct_code = kwargs.get("correct_code", "infected = 121\nprint(infected)")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        heading = Text(
            self.t("outro_heading"),
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)
        sub = Text(self.t("outro_sub"), font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(heading, DOWN, buff=0.4)
        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
