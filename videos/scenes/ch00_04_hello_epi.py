"""Ch00-04: 第一支程式 Hello Epi——十分鐘跑完你的第一個流病分析

Manim scene for the tutorial video on running your first epidemiology analysis.
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
    ManimColor,
    RoundedRectangle,
    Text,
    VGroup,
    Write,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_BLUE,
    ACCENT_GREEN,
    ACCENT_ORANGE,
    BG_CARD,
    BG_CARD_ALT,
    BORDER_LIGHT,
    CODE_BG,
    ERROR_RED,
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
)


class Ch00HelloEpiScene(EpiBaseScene):
    """Tutorial video scene: first epidemiology program with the Legionella outbreak."""

    total_steps: int = 13

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the Hello Epi lesson."""
        self.show_title_card(
            "第一支程式 Hello Epi",
            "十分鐘跑完你的第一個流病分析",
            duration=duration,
        )

    def show_clone_repo(self, duration: float = 6.0, **kwargs) -> None:
        """Show terminal commands for cloning the repo and installing deps."""
        self.show_step_indicator(1, self.total_steps)

        code_lines = (
            "# 1. 複製教材到本機\n"
            "git clone https://github.com/your-org/python4epi.git\n"
            "\n"
            "# 2. 進入專案資料夾\n"
            "cd python4epi\n"
            "\n"
            "# 3. 安裝所有相依套件\n"
            "uv sync"
        )

        code_panel = CodePanel(
            code_lines,
            title="Terminal",
            width=8.0,
            height=3.6,
        ).move_to(ORIGIN)

        self.play(Create(code_panel), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(code_panel), run_time=0.5)

    def show_open_notebook(self, duration: float = 5.0, **kwargs) -> None:
        """Show how to launch Jupyter Lab and navigate to a notebook."""
        self.show_step_indicator(2, self.total_steps)

        code_panel = CodePanel(
            "uv run jupyter lab",
            title="Terminal",
            width=6.0,
            height=1.6,
        ).shift(UP * 1.5)

        # Simulated file browser card
        browser_card = RoundedRectangle(
            corner_radius=0.2,
            width=7.0,
            height=2.4,
            fill_color=ManimColor(BG_CARD),
            fill_opacity=1,
            stroke_color=ManimColor(BORDER_LIGHT),
            stroke_width=2,
        ).shift(DOWN * 1.0)

        browser_title = Text(
            "Jupyter Lab — 檔案瀏覽器",
            font=FONT_CJK,
            font_size=18,
            color=ManimColor(TEXT_SECONDARY),
        ).move_to(browser_card.get_top() + DOWN * 0.3)

        files = VGroup(
            Text("notebooks/", font=FONT_MONO, font_size=18, color=ManimColor(ACCENT_BLUE)),
            Text("  00_hello_epi.ipynb", font=FONT_MONO, font_size=18, color=ManimColor(ACCENT_ORANGE)),
            Text("data/synthetic/", font=FONT_MONO, font_size=18, color=ManimColor(ACCENT_BLUE)),
            Text("  legionella_outbreak.csv", font=FONT_MONO, font_size=18, color=ManimColor(TEXT_PRIMARY)),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(browser_card.get_center() + DOWN * 0.1)

        browser_group = VGroup(browser_card, browser_title, files)

        self.play(Create(code_panel), run_time=0.8)
        self.play(FadeIn(browser_group), run_time=0.8)
        self.wait(max(0.1, duration - 2.1))
        self.play(FadeOut(VGroup(code_panel, browser_group)), run_time=0.5)

    def show_run_analysis(self, duration: float = 6.0, **kwargs) -> None:
        """Show the core analysis code reading CSV and computing metrics."""
        self.show_step_indicator(3, self.total_steps)

        code_lines = (
            "import pandas as pd\n"
            "\n"
            "df = pd.read_csv('data/synthetic/legionella_outbreak.csv')\n"
            "\n"
            "total = len(df)\n"
            "infected = df['case_classification'].eq('confirmed').sum()\n"
            "deaths = df['outcome'].eq('dead').sum()\n"
            "\n"
            "attack_rate = infected / total * 100\n"
            "cfr = deaths / infected * 100\n"
            "\n"
            "print(f'侵襲率: {attack_rate:.1f}%')\n"
            "print(f'致死率: {cfr:.1f}%')"
        )

        code_panel = CodePanel(
            code_lines,
            title="hello_epi.py",
            width=8.5,
            height=5.0,
            font_size=18,
        ).move_to(ORIGIN)

        self.play(Create(code_panel), run_time=1.5)
        self.wait(max(0.1, duration - 2.0))
        self.play(FadeOut(code_panel), run_time=0.5)

    def show_see_result(self, duration: float = 5.0, **kwargs) -> None:
        """Show the analysis results as big number stat cards."""
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            "分析結果",
            font=FONT_CJK,
            font_size=34,
            color=ManimColor(ACCENT_ORANGE),
        ).to_edge(UP, buff=0.8)

        cards = VGroup(
            self._make_stat_card("43.2%", "侵襲率 (Attack Rate)", ACCENT_ORANGE),
            self._make_stat_card("15.7%", "致死率 (CFR)", ERROR_RED),
        ).arrange(RIGHT, buff=1.2).move_to(ORIGIN)

        caption = Text(
            "280 位住民中 121 人感染、19 人死亡",
            font=FONT_CJK,
            font_size=22,
            color=ManimColor(TEXT_SECONDARY),
        ).next_to(cards, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(cards, lag_ratio=0.3), run_time=1.0)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(max(0.1, duration - 2.5))
        self.play(FadeOut(VGroup(heading, cards, caption)), run_time=0.5)

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        """Summarise the four steps you just completed."""
        self.show_step_indicator(5, self.total_steps)

        heading = Text(
            "你剛剛完成了什麼？",
            font=FONT_CJK,
            font_size=34,
            color=ManimColor(ACCENT_ORANGE),
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("1. git clone 把教材複製到本機", font=FONT_CJK, font_size=24, color=ManimColor(TEXT_PRIMARY)),
            Text("2. uv sync 安裝所有相依套件", font=FONT_CJK, font_size=24, color=ManimColor(TEXT_PRIMARY)),
            Text("3. 用 pandas 讀取 CSV 資料", font=FONT_CJK, font_size=24, color=ManimColor(TEXT_PRIMARY)),
            Text("4. 計算侵襲率與致死率", font=FONT_CJK, font_size=24, color=ManimColor(TEXT_PRIMARY)),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example methods
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the ExtraExampleBanner section divider."""
        banner = ExtraExampleBanner("額外範例：用同樣流程分析腸病毒資料")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        """Enterovirus example using the same analysis pattern."""
        self.show_step_indicator(6, self.total_steps)

        code_lines = (
            "# 腸病毒幼兒園群聚事件\n"
            "import pandas as pd\n"
            "\n"
            "df = pd.read_csv('enterovirus_kindergarten.csv')\n"
            "\n"
            "total = len(df)          # 120 位幼童\n"
            "infected = df['confirmed'].sum()  # 34 人確診\n"
            "severe = df['severe'].sum()       # 2 人重症\n"
            "\n"
            "attack_rate = infected / total * 100\n"
            "print(f'侵襲率: {attack_rate:.1f}%')  # 28.3%"
        )

        output_text = "侵襲率: 28.3%"

        code_panel = self.show_code(
            code_lines,
            title="enterovirus_analysis.py",
            position=ORIGIN + UP * 0.5,
            duration=1.5,
        )
        self.wait(0.5)
        output_panel = self.show_output(output_text, position=DOWN * 2.5)
        self.wait(max(0.1, duration - 2.0))
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner("初學者常見地雷 3 選 1")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_git_clone(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: git not installed vs download ZIP alternative."""
        error_code = kwargs.get("error_code", "git clone ... # not recognized")
        correct_code = kwargs.get("correct_code", "# GitHub > Code > Download ZIP")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_uv_sync(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: panic at slow install vs normal first-time behaviour."""
        error_code = kwargs.get("error_code", "uv sync  # Ctrl+C too early!")
        correct_code = kwargs.get("correct_code", "uv sync  # wait 1-2 min first time")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_warnings(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: Warning (yellow, safe) vs Error (red, must fix)."""
        error_code = kwargs.get("error_code", "FutureWarning: ...  # panic!")
        correct_code = kwargs.get("correct_code", "# Warning = OK, Error = fix it")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card pointing to the next video."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            "下一集：Git 基礎版本控制",
            font=FONT_CJK,
            font_size=28,
            color=ManimColor(ACCENT_ORANGE),
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "學會追蹤你的分析程式碼！",
            font=FONT_CJK,
            font_size=22,
            color=ManimColor(TEXT_SECONDARY),
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(max(0.1, duration - 1.6))
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _make_stat_card(self, value: str, label: str, color: str) -> VGroup:
        """Create a simple stat card with a big number and a label."""
        val_text = Text(value, font=FONT_MONO, font_size=48, color=ManimColor(color))
        lbl_text = Text(label, font=FONT_CJK, font_size=20, color=ManimColor(TEXT_SECONDARY))
        lbl_text.next_to(val_text, DOWN, buff=0.15)
        return VGroup(val_text, lbl_text)
