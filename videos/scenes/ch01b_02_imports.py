"""Ch01b-02: import——借用別人的工具

Manim scene for the tutorial video on Python import statements,
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


class Ch01bImportsScene(EpiBaseScene):
    """Tutorial video scene: Python import statements."""

    total_steps: int = 14

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "import",
            "title_sub": "借用別人的工具",
            "import_as_heading": "import X as Y — 取個好記的綽號",
            "import_as_note": "pd, np, plt — 全世界 Python 使用者共同的約定",
            "import_order_heading": "import 的排列順序",
            "summary_heading": "重點整理",
            "summary_p1": "1. import X — 搬整個工具箱",
            "summary_p2": "2. from X import Y — 只借一個工具",
            "summary_p3": "3. import X as Y — 取綽號",
            "summary_p4": "4. import 放在檔案最上面",
            "extra_banner_title": "額外範例：用 datetime 算發病天數",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：型別與轉換",
            "outro_sub": "搞清楚數字和文字的差別！",
        },
        "en": {
            "title_main": "import",
            "title_sub": "Borrow other people's tools",
            "import_as_heading": "import X as Y — give it a memorable nickname",
            "import_as_note": "pd, np, plt — the shared convention of Python users worldwide",
            "import_order_heading": "The order of your imports",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. import X — bring the whole toolbox",
            "summary_p2": "2. from X import Y — borrow just one tool",
            "summary_p3": "3. import X as Y — give it a nickname",
            "summary_p4": "4. Put imports at the top of the file",
            "extra_banner_title": "Extra example: count onset-to-admission days with datetime",
            "blindspot_banner_title": "3 Common Beginner Pitfalls",
            "outro_heading": "Next up: types and conversion",
            "outro_sub": "Sort out the difference between numbers and text!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_import_basic(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        code_text = kwargs.get("code", "import math\nprint(math.sqrt(121))")
        code_panel = self.show_code(code_text, title="import_basic.py")
        self.wait(1.0)
        output_panel = self.show_output(kwargs.get("output", "11.0"))
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_from_import(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        code_text = kwargs.get("code", "from math import sqrt\nprint(sqrt(121))")
        code_panel = self.show_code(code_text, title="from_import.py")
        self.wait(1.0)
        output_panel = self.show_output(kwargs.get("output", "11.0"))
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_import_as(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            self.t("import_as_heading"),
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        code_text = kwargs.get("code", "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt")
        code_panel = CodePanel(code_text, title="aliases.py", width=8.0, height=2.8).next_to(heading, DOWN, buff=0.5)

        note = Text(
            self.t("import_as_note"),
            font=FONT_CJK, font_size=20, color=TEXT_SECONDARY,
        ).next_to(code_panel, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(Create(code_panel), run_time=0.8)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(duration - 1.6)
        self.play(FadeOut(VGroup(heading, code_panel, note)), run_time=0.5)

    def show_import_order(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        code_text = kwargs.get("code",
            "# 1. standard library\nimport math\nimport datetime\n"
            "# 2. third-party\nimport pandas as pd\n"
            "# 3. local\nfrom epi_learning import attack_rate")

        heading = Text(
            self.t("import_order_heading"),
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        code_panel = CodePanel(code_text, title="import_order.py", width=8.0, height=3.5).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(Create(code_panel), run_time=0.8)
        self.wait(duration - 1.2)
        self.play(FadeOut(VGroup(heading, code_panel)), run_time=0.5)

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        heading = Text(self.t("summary_heading"), font=FONT_CJK, font_size=34, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
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
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        banner = ExtraExampleBanner(self.t("extra_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        code_text = kwargs.get("code",
            "from datetime import date\nonset = date(2026, 1, 15)\n"
            "admitted = date(2026, 1, 18)\ndelay = (admitted - onset).days\n"
            'print(f"onset-to-admission: {delay} days")')
        code_panel = self.show_code(code_text, title="date_calc.py")
        self.wait(1.0)
        output_panel = self.show_output(kwargs.get("output", "onset-to-admission: 3 days"))
        self.wait(duration - 1.0)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_not_installed(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "import pandas  # ModuleNotFoundError")
        correct_code = kwargs.get("correct_code", "# uv add pandas  (install first)")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_import_middle(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "x = 10\nimport math\nprint(math.sqrt(x))")
        correct_code = kwargs.get("correct_code", "import math\nx = 10\nprint(math.sqrt(x))")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_wrong_ref(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "from math import sqrt\nprint(math.sqrt(9))  # NameError")
        correct_code = kwargs.get("correct_code", "from math import sqrt\nprint(sqrt(9))  # 3.0")
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
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
