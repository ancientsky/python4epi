"""Ch01b-08: Jupyter 實用密技——讓你的效率翻倍

Manim scene for the tutorial video on Jupyter Lab tips and tricks,
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


class Ch01bJupyterTipsScene(EpiBaseScene):
    """Tutorial video scene: Jupyter Lab tips and tricks."""

    total_steps: int = 14

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "Jupyter 實用密技",
            "title_sub": "讓你的效率翻倍",
            "shell_heading": "! 驚嘆號 — 在 Jupyter 裡執行終端指令",
            "shell_note": "不用另開終端機，直接在 notebook 裡執行 shell 指令",
            "install_heading": "在 Jupyter 裡安裝套件",
            "install_step1": "1. !uv add seaborn          # 安裝套件",
            "install_step2": "2. Kernel > Restart Kernel   # 重啟核心",
            "install_step3": "3. import seaborn as sns     # 匯入使用",
            "install_note": "裝完一定要 Restart Kernel！",
            "qmark_heading": "? 問號 — 查看函式說明",
            "qmark_note": "一個 ? 看說明，兩個 ?? 看原始碼",
            "tab_heading": "Tab 自動完成 — 忘記方法名稱的救星",
            "tab_step1": "1. 打 df. 然後按 Tab",
            "tab_step2": "2. 看到所有可用的方法和屬性",
            "tab_step3": "3. 選擇你要的方法，按 Enter",
            "summary_heading": "Jupyter 五大密技",
            "summary_p1": "1. ! 執行 shell 指令",
            "summary_p2": "2. !uv add 安裝套件 + Restart Kernel",
            "summary_p3": "3. ? 查說明、?? 看原始碼",
            "summary_p4": "4. Tab 自動完成方法名稱",
            "summary_p5": "5. %timeit 測量效能",
            "extra_banner_title": "額外範例：快速探索疫調資料",
            "extra_heading": "拿到新 CSV 的前 2 分鐘",
            "extra_step1": "1. !head -2 data.csv   # 看欄位名稱",
            "extra_step2": "2. !wc -l data.csv     # 看有多少筆",
            "extra_step3": "3. df = pd.read_csv('data.csv')",
            "extra_step4": "4. df.info()           # 看型別和遺漏",
            "extra_step5": "5. df.describe()       # 看數值摘要",
            "extra_note": "這就是老手的工作節奏！",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "Ch01b 全部完成！",
            "outro_sub": "你的 Python 開發者工具箱已經備齊",
            "outro_next": "下一章 Ch02：用 pandas 處理真正的疫調資料！",
        },
        "en": {
            "title_main": "Practical Jupyter Tips",
            "title_sub": "Double your efficiency",
            "shell_heading": "! bang — run terminal commands inside Jupyter",
            "shell_note": "No separate terminal needed — run shell commands right in the notebook",
            "install_heading": "Install packages inside Jupyter",
            "install_step1": "1. !uv add seaborn          # install the package",
            "install_step2": "2. Kernel > Restart Kernel   # restart the kernel",
            "install_step3": "3. import seaborn as sns     # import and use",
            "install_note": "Always Restart Kernel after installing!",
            "qmark_heading": "? question mark — view a function's docs",
            "qmark_note": "One ? shows docs, two ?? shows source code",
            "tab_heading": "Tab autocomplete — the savior when you forget a method name",
            "tab_step1": "1. Type df. then press Tab",
            "tab_step2": "2. See every available method and attribute",
            "tab_step3": "3. Pick the method you want, press Enter",
            "summary_heading": "Jupyter's Five Tricks",
            "summary_p1": "1. ! runs shell commands",
            "summary_p2": "2. !uv add installs packages + Restart Kernel",
            "summary_p3": "3. ? for docs, ?? for source code",
            "summary_p4": "4. Tab autocompletes method names",
            "summary_p5": "5. %timeit measures performance",
            "extra_banner_title": "Extra example: quickly explore outbreak data",
            "extra_heading": "The first 2 minutes with a new CSV",
            "extra_step1": "1. !head -2 data.csv   # see column names",
            "extra_step2": "2. !wc -l data.csv     # see how many rows",
            "extra_step3": "3. df = pd.read_csv('data.csv')",
            "extra_step4": "4. df.info()           # see types and missing",
            "extra_step5": "5. df.describe()       # see numeric summary",
            "extra_note": "This is the rhythm of a seasoned pro!",
            "blindspot_banner_title": "3 Common Beginner Pitfalls",
            "outro_heading": "Ch01b fully complete!",
            "outro_sub": "Your Python developer toolbox is ready",
            "outro_next": "Next chapter Ch02: use pandas on real outbreak data!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_shell_commands(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            self.t("shell_heading"),
            font=FONT_CJK, font_size=26, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        code_text = "!ls data/synthetic/\n!head -3 data/synthetic/legionella_outbreak.csv\n!wc -l data/synthetic/legionella_outbreak.csv"
        code_panel = CodePanel(code_text, title="Jupyter Cell", width=9.0, height=2.4).next_to(heading, DOWN, buff=0.5)

        note = Text(
            self.t("shell_note"),
            font=FONT_CJK, font_size=20, color=TEXT_SECONDARY,
        ).next_to(code_panel, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(Create(code_panel), run_time=0.8)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(duration - 1.6)
        self.play(FadeOut(VGroup(heading, code_panel, note)), run_time=0.5)

    def show_install_in_jupyter(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            self.t("install_heading"),
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        steps = VGroup(
            Text(self.t("install_step1"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text(self.t("install_step2"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text(self.t("install_step3"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(heading, DOWN, buff=0.6)

        note = Text(
            self.t("install_note"),
            font=FONT_CJK, font_size=22, color="#D94452",
        ).next_to(steps, DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(steps, lag_ratio=0.3), run_time=1.0)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(duration - 1.8)
        self.play(FadeOut(VGroup(heading, steps, note)), run_time=0.5)

    def show_question_mark(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            self.t("qmark_heading"),
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        code_text = "import pandas as pd\npd.read_csv?"
        code_panel = CodePanel(code_text, title="Jupyter Cell", width=7.0, height=2.0).next_to(heading, DOWN, buff=0.5)

        note = Text(
            self.t("qmark_note"),
            font=FONT_CJK, font_size=22, color=TEXT_SECONDARY,
        ).next_to(code_panel, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(Create(code_panel), run_time=0.6)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(duration - 1.4)
        self.play(FadeOut(VGroup(heading, code_panel, note)), run_time=0.5)

    def show_tab_complete(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            self.t("tab_heading"),
            font=FONT_CJK, font_size=26, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        steps = VGroup(
            Text(self.t("tab_step1"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("tab_step2"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("tab_step3"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(heading, DOWN, buff=0.6)

        note = Text(
            "df.head, df.info, df.describe, df.shape ...",
            font=FONT_MONO, font_size=18, color=ACCENT_GREEN,
        ).next_to(steps, DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(steps, lag_ratio=0.3), run_time=0.9)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, steps, note)), run_time=0.5)

    def show_timeit(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        code_text = kwargs.get("code", "import math\n%timeit math.sqrt(121)")
        output_text = kwargs.get("output", "47.3 ns per loop")
        code_panel = self.show_code(code_text, title="Jupyter Cell")
        self.wait(0.8)
        output_panel = self.show_output(output_text)
        self.wait(duration - 0.8)
        self.clear_screen()

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        heading = Text(self.t("summary_heading"), font=FONT_CJK, font_size=34, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        points = VGroup(
            Text(self.t("summary_p1"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("summary_p2"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("summary_p3"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("summary_p4"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("summary_p5"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.5)
        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.2), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        banner = ExtraExampleBanner(self.t("extra_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)

        heading = Text(
            self.t("extra_heading"),
            font=FONT_CJK, font_size=26, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        steps = VGroup(
            Text(self.t("extra_step1"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text(self.t("extra_step2"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text(self.t("extra_step3"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text(self.t("extra_step4"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text(self.t("extra_step5"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(heading, DOWN, buff=0.5)

        note = Text(
            self.t("extra_note"),
            font=FONT_CJK, font_size=20, color=ACCENT_GREEN,
        ).next_to(steps, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(steps, lag_ratio=0.2), run_time=1.2)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(duration - 2.0)
        self.play(FadeOut(VGroup(heading, steps, note)), run_time=0.5)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_no_restart(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "!uv add X\nimport X  # still fails!")
        correct_code = kwargs.get("correct_code", "!uv add X\n# Restart Kernel first!")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_bang_in_py(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "# in script.py:\n!ls  # SyntaxError!")
        correct_code = kwargs.get("correct_code", "import os\nos.system('ls')")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_cell_order(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "# run cell 5, then cell 2: bug!")
        correct_code = kwargs.get("correct_code", "# Restart + Run All: clean!")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        heading = Text(
            self.t("outro_heading"),
            font=FONT_CJK, font_size=32, color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.8)
        sub = Text(
            self.t("outro_sub"),
            font=FONT_CJK, font_size=24, color=TEXT_PRIMARY,
        ).next_to(heading, DOWN, buff=0.3)
        next_ch = Text(
            self.t("outro_next"),
            font=FONT_CJK, font_size=22, color=TEXT_SECONDARY,
        ).next_to(sub, DOWN, buff=0.3)
        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.play(FadeIn(next_ch), run_time=0.5)
        self.wait(duration - 1.6)
        self.play(FadeOut(VGroup(heading, sub, next_ch)), run_time=0.5)
