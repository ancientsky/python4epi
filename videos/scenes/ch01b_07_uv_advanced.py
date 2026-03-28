"""Ch01b-07: uv 進階——管理 Python 版本與套件

Manim scene for the tutorial video on advanced uv usage,
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


class Ch01bUvAdvancedScene(EpiBaseScene):
    """Tutorial video scene: advanced uv package management."""

    total_steps: int = 13

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card("uv 進階", "管理 Python 版本與套件", duration=duration)

    def show_python_versions(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "用 uv 管理多版本 Python",
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        cmds = VGroup(
            Text("uv python install 3.11   # 安裝 Python 3.11", font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text("uv python install 3.12   # 安裝 Python 3.12", font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text("uv python pin 3.12       # 鎖定此專案版本", font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text("uv run python --version  # 確認版本", font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.6)

        note = Text(
            "不同專案可以用不同版本的 Python，互不干擾",
            font=FONT_CJK, font_size=20, color=TEXT_SECONDARY,
        ).next_to(cmds, DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(cmds, lag_ratio=0.2), run_time=1.0)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(duration - 1.8)
        self.play(FadeOut(VGroup(heading, cmds, note)), run_time=0.5)

    def show_add_packages(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            "uv add — 安裝套件並記錄",
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        cmds = VGroup(
            Text('uv add pandas            # 最新版', font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text('uv add "pandas>=2.0"     # 指定版本', font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text('uv add --dev pytest      # 開發用', font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text('uv add matplotlib seaborn # 多個', font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.6)

        note = Text(
            "所有安裝紀錄存在 pyproject.toml",
            font=FONT_CJK, font_size=20, color=TEXT_SECONDARY,
        ).next_to(cmds, DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(cmds, lag_ratio=0.2), run_time=1.0)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(duration - 1.8)
        self.play(FadeOut(VGroup(heading, cmds, note)), run_time=0.5)

    def show_find_packages(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            "怎麼找到好用的套件？",
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("1. 去 pypi.org 搜尋關鍵字", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("2. 看 GitHub stars 和下載量", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("3. 確認最近有更新（活躍維護）", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("4. 流病常用：pandas, seaborn, scipy", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("5. 進階：lifelines, geopandas, plotly", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(points, lag_ratio=0.2), run_time=1.2)
        self.wait(duration - 1.6)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_uv_sync(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            "uv sync — 一鍵復原開發環境",
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        code_text = "# Clone a project\n# git clone <repo-url>\n# cd python4epi\n# uv sync\n# Done! All deps installed."
        code_panel = CodePanel(code_text, title="terminal", width=7.0, height=2.8).next_to(heading, DOWN, buff=0.5)

        note = Text(
            "有 pyproject.toml + uv.lock → 一鍵還原",
            font=FONT_CJK, font_size=20, color=TEXT_SECONDARY,
        ).next_to(code_panel, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(Create(code_panel), run_time=0.8)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(duration - 1.6)
        self.play(FadeOut(VGroup(heading, code_panel, note)), run_time=0.5)

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        heading = Text("重點整理", font=FONT_CJK, font_size=34, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        points = VGroup(
            Text("1. uv python install — 裝不同版本", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("2. uv add — 安裝並記錄套件", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("3. uv sync — 一鍵復原環境", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("4. pypi.org 找套件看星星和下載量", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)
        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        banner = ExtraExampleBanner("額外範例：建立疫苗覆蓋率分析專案")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)

        heading = Text(
            "從零建立專案的完整流程",
            font=FONT_CJK, font_size=26, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        steps = VGroup(
            Text("1. uv init vaccine_coverage     # 建立專案", font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text("2. cd vaccine_coverage", font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text("3. uv add pandas matplotlib      # 裝套件", font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text("4. uv run python analyze.py      # 執行分析", font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.6)

        note = Text(
            "同事接手？只要 uv sync 就能復現環境！",
            font=FONT_CJK, font_size=20, color=ACCENT_GREEN,
        ).next_to(steps, DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(steps, lag_ratio=0.25), run_time=1.2)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(duration - 2.0)
        self.play(FadeOut(VGroup(heading, steps, note)), run_time=0.5)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        banner = BlindSpotBanner("初學者常見地雷 3 選")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_pip_vs_uv(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "pip install pandas  # not tracked!")
        correct_code = kwargs.get("correct_code", "uv add pandas  # saved to toml")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_forget_uv_run(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "python main.py  # wrong env!")
        correct_code = kwargs.get("correct_code", "uv run python main.py  # OK")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_lock(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "# .gitignore: uv.lock  WRONG!")
        correct_code = kwargs.get("correct_code", "git add uv.lock  # reproducible!")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        heading = Text(
            "下一集：Jupyter 實用密技",
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)
        sub = Text("讓你的分析效率翻倍！", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(heading, DOWN, buff=0.4)
        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
