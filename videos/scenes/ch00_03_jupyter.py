"""Ch00-03: Jupyter Lab 入門——邊寫邊看結果的神器

Manim scene for the tutorial video on Jupyter Lab basics.
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
    CODE_TEXT,
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


class Ch00JupyterScene(EpiBaseScene):
    """Tutorial video scene: Jupyter Lab basics for epidemiologists."""

    total_steps: int = 12

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the Jupyter Lab lesson."""
        self.show_title_card("Jupyter Lab 入門", "邊寫邊看結果的神器", duration=duration)

    def show_launch(self, duration: float = 5.0, **kwargs) -> None:
        """Show terminal launching Jupyter Lab."""
        self.show_step_indicator(1, self.total_steps)

        code_panel = CodePanel(
            "uv run jupyter lab",
            title="Terminal",
            width=7.0,
        ).shift(UP * 1.0)

        output_panel = OutputPanel(
            "Jupyter Server is running at http://localhost:8888/lab",
            width=10.0,
            height=1.0,
        ).shift(DOWN * 1.0)

        self.play(FadeIn(code_panel), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(output_panel), run_time=0.8)
        self.wait(max(0.1, duration - 2.6))
        self.play(FadeOut(VGroup(code_panel, output_panel)), run_time=0.5)

    def show_cells(self, duration: float = 6.0, **kwargs) -> None:
        """Show two cell types side by side: Code cell vs Markdown cell."""
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            "Notebook 有兩種 Cell",
            font=FONT_CJK,
            font_size=30,
            color=ManimColor(TEXT_PRIMARY),
        ).to_edge(UP, buff=0.8)

        # Code cell (dark bg)
        code_card = RoundedRectangle(
            corner_radius=0.15, width=5.0, height=3.0,
            fill_color=ManimColor(CODE_BG), fill_opacity=1,
            stroke_color=ManimColor(BORDER_LIGHT), stroke_width=2,
        )
        code_label = Text(
            "Code Cell", font=FONT_MONO, font_size=18,
            color=ManimColor(ACCENT_GREEN),
        ).move_to(code_card.get_top() + DOWN * 0.3)
        code_body = Text(
            "infected = 121\nprint(infected)",
            font=FONT_MONO, font_size=18,
            color=ManimColor(CODE_TEXT),
        ).move_to(code_card.get_center() + DOWN * 0.1)
        code_group = VGroup(code_card, code_label, code_body)

        # Markdown cell (light bg)
        md_card = RoundedRectangle(
            corner_radius=0.15, width=5.0, height=3.0,
            fill_color=ManimColor(BG_CARD), fill_opacity=1,
            stroke_color=ManimColor(BORDER_LIGHT), stroke_width=2,
        )
        md_label = Text(
            "Markdown Cell", font=FONT_MONO, font_size=18,
            color=ManimColor(ACCENT_BLUE),
        ).move_to(md_card.get_top() + DOWN * 0.3)
        md_body = Text(
            "# 疫情調查報告\n本次群聚共 121 例感染",
            font=FONT_CJK, font_size=18,
            color=ManimColor(TEXT_PRIMARY),
        ).move_to(md_card.get_center() + DOWN * 0.1)
        md_group = VGroup(md_card, md_label, md_body)

        cells = VGroup(code_group, md_group).arrange(RIGHT, buff=0.8).move_to(ORIGIN + DOWN * 0.3)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(cells, lag_ratio=0.3), run_time=1.0)
        self.wait(max(0.1, duration - 2.5))
        self.play(FadeOut(VGroup(heading, cells)), run_time=0.5)

    def show_run_cell(self, duration: float = 5.0, **kwargs) -> None:
        """Show Shift+Enter shortcut and cell execution."""
        self.show_step_indicator(3, self.total_steps)

        shortcut = Text(
            "Shift + Enter",
            font=FONT_MONO,
            font_size=36,
            color=ManimColor(ACCENT_ORANGE),
        ).to_edge(UP, buff=1.0)

        hint = Text(
            "= 執行目前 Cell 並跳到下一格",
            font=FONT_CJK,
            font_size=22,
            color=ManimColor(TEXT_SECONDARY),
        ).next_to(shortcut, DOWN, buff=0.3)

        # Simulated executed cell
        cell_card = RoundedRectangle(
            corner_radius=0.15, width=8.0, height=2.4,
            fill_color=ManimColor(CODE_BG), fill_opacity=1,
            stroke_color=ManimColor(ACCENT_BLUE), stroke_width=2,
        )
        in_label = Text(
            "[1]:", font=FONT_MONO, font_size=18,
            color=ManimColor(ACCENT_BLUE),
        ).move_to(cell_card.get_left() + RIGHT * 0.6 + UP * 0.3)
        cell_code = Text(
            "total_residents = 280\nprint(total_residents)",
            font=FONT_MONO, font_size=18,
            color=ManimColor(CODE_TEXT),
        ).next_to(in_label, RIGHT, buff=0.4).align_to(in_label, UP)

        output_card = RoundedRectangle(
            corner_radius=0.15, width=8.0, height=0.8,
            fill_color=ManimColor(BG_CARD_ALT), fill_opacity=1,
            stroke_color=ManimColor(BORDER_LIGHT), stroke_width=1,
        ).next_to(cell_card, DOWN, buff=0.1)
        output_text = Text(
            "280", font=FONT_MONO, font_size=18,
            color=ManimColor(TEXT_PRIMARY),
        ).move_to(output_card.get_center())

        cell_group = VGroup(cell_card, in_label, cell_code, output_card, output_text)
        cell_group.move_to(ORIGIN + DOWN * 0.8)

        self.play(FadeIn(shortcut), run_time=0.5)
        self.play(FadeIn(hint), run_time=0.4)
        self.play(FadeIn(cell_group), run_time=0.8)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(shortcut, hint, cell_group)), run_time=0.5)

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        """Summarise 4 key points about Jupyter Lab."""
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            "重點整理",
            font=FONT_CJK,
            font_size=34,
            color=ManimColor(ACCENT_ORANGE),
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("1. uv run jupyter lab 啟動環境", font=FONT_CJK, font_size=24,
                 color=ManimColor(TEXT_PRIMARY)),
            Text("2. Code Cell 寫程式，Markdown Cell 寫說明", font=FONT_CJK, font_size=24,
                 color=ManimColor(TEXT_PRIMARY)),
            Text("3. Shift+Enter 執行 Cell", font=FONT_CJK, font_size=24,
                 color=ManimColor(TEXT_PRIMARY)),
            Text("4. Ctrl+S 隨時存檔", font=FONT_CJK, font_size=24,
                 color=ManimColor(TEXT_PRIMARY)),
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
        banner = ExtraExampleBanner("額外範例：用 Jupyter 寫疫情週報")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        """Mock notebook layout: Markdown heading + Code cell + Output placeholder."""
        self.show_step_indicator(5, self.total_steps)

        # Markdown cell (report heading)
        md_card = RoundedRectangle(
            corner_radius=0.12, width=9.0, height=1.0,
            fill_color=ManimColor(BG_CARD), fill_opacity=1,
            stroke_color=ManimColor(BORDER_LIGHT), stroke_width=2,
        )
        md_text = Text(
            "# 2026 年第 4 週疫情週報",
            font=FONT_CJK, font_size=20,
            color=ManimColor(TEXT_PRIMARY),
        ).move_to(md_card.get_center())
        md_group = VGroup(md_card, md_text)

        # Code cell (chart code)
        code_card = RoundedRectangle(
            corner_radius=0.12, width=9.0, height=1.6,
            fill_color=ManimColor(CODE_BG), fill_opacity=1,
            stroke_color=ManimColor(BORDER_LIGHT), stroke_width=2,
        )
        code_text = Text(
            "import matplotlib.pyplot as plt\nplt.bar(['Week3','Week4'], [45, 76])\nplt.title('New Cases')",
            font=FONT_MONO, font_size=16,
            color=ManimColor(CODE_TEXT),
        ).move_to(code_card.get_center())
        code_group = VGroup(code_card, code_text)

        # Output placeholder (chart area)
        out_card = RoundedRectangle(
            corner_radius=0.12, width=9.0, height=1.4,
            fill_color=ManimColor(BG_CARD_ALT), fill_opacity=1,
            stroke_color=ManimColor(BORDER_LIGHT), stroke_width=1,
        )
        out_text = Text(
            "[bar chart output]",
            font=FONT_MONO, font_size=18,
            color=ManimColor(TEXT_SECONDARY),
        ).move_to(out_card.get_center())
        out_group = VGroup(out_card, out_text)

        notebook = VGroup(md_group, code_group, out_group).arrange(DOWN, buff=0.15).move_to(ORIGIN)

        self.play(FadeIn(notebook, lag_ratio=0.3), run_time=1.2)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(notebook), run_time=0.5)

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner("初學者常見地雷 3 選 1")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_order(self, duration: float = 5.0, **kwargs) -> None:
        """Running cells out of order vs Restart & Run All."""
        error_code = kwargs.get(
            "error_code",
            "# Cell [3] 先跑\nprint(result)\n# NameError: 'result' not defined",
        )
        correct_code = kwargs.get(
            "correct_code",
            "# Kernel → Restart & Run All\n# 從頭到尾按順序執行",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_kernel(self, duration: float = 5.0, **kwargs) -> None:
        """Import fails after pip install vs restart kernel first."""
        error_code = kwargs.get(
            "error_code",
            "!pip install pandas\nimport pandas  # ModuleNotFoundError",
        )
        correct_code = kwargs.get(
            "correct_code",
            "!pip install pandas\n# Restart Kernel 後再\nimport pandas  # OK",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_stuck(self, duration: float = 5.0, **kwargs) -> None:
        """[*] spinning forever vs press stop button."""
        error_code = kwargs.get(
            "error_code",
            "# In [*]:  一直轉圈...\nwhile True:\n    pass",
        )
        correct_code = kwargs.get(
            "correct_code",
            '# 按工具列的 ■ 停止按鈕\n# 或 Kernel → Interrupt',
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            "下一集：Hello Epi — 第一支流行病學程式",
            font=FONT_CJK,
            font_size=28,
            color=ManimColor(ACCENT_ORANGE),
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "用 Python 算出侵襲率！",
            font=FONT_CJK,
            font_size=22,
            color=ManimColor(TEXT_SECONDARY),
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(max(0.1, duration - 1.6))
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
