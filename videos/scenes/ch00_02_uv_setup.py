"""Ch00-02: uv 與環境設定——一行搞定 Python 套件管理

Manim scene for the tutorial video on uv package manager and virtual environments.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    UR,
    Arrow,
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
    VariableBox,
)


class Ch00UvSetupScene(EpiBaseScene):
    """Tutorial video scene: uv package manager and virtual environment setup."""

    total_steps: int = 12

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "uv 與環境設定",
            "title_sub": "一行搞定 Python 套件管理",
            "venv_heading": "虛擬環境 = 獨立工具箱",
            "venv_box_a_title": "登革熱監測",
            "venv_box_b_title": "COVID 儀表板",
            "venv_caption": "不同專案可以有不同版本的套件，互不干擾",
            "install_heading": "安裝 uv（一行指令）",
            "install_note": "Windows 使用者可用 PowerShell 安裝，詳見官方文件",
            "workflow_heading": "uv 三步驟工作流",
            "step1_title": "1. 初始化",
            "step2_title": "2. 加套件",
            "step3_title": "3. 執行",
            "summary_heading": "pip vs uv 比較",
            "summary_p1": "1. uv 自動建立虛擬環境，不需手動 python -m venv",
            "summary_p2": "2. uv 安裝速度比 pip 快 10-100 倍（Rust 寫的）",
            "summary_p3": "3. uv 用 pyproject.toml + uv.lock 鎖定版本",
            "summary_p4": "4. uv run 確保在正確的環境中執行程式",
            "extra_banner_title": "額外範例：同時開發兩個防疫專案",
            "extra_heading": "兩個專案，兩個環境，零衝突",
            "extra_caption": "uv 讓每個專案都有獨立的 .venv，版本不會打架",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：Jupyter Lab 互動式筆記本",
            "outro_sub": "uv run jupyter lab 一鍵啟動！",
        },
        "en": {
            "title_main": "uv & Environment Setup",
            "title_sub": "One line to master Python package management",
            "venv_heading": "Virtual Environment = Its Own Toolbox",
            "venv_box_a_title": "Dengue Surveillance",
            "venv_box_b_title": "COVID Dashboard",
            "venv_caption": "Different projects can use different package versions without clashing",
            "install_heading": "Install uv (one command)",
            "install_note": "Windows users can install via PowerShell - see the official docs",
            "workflow_heading": "The uv Three-Step Workflow",
            "step1_title": "1. Init",
            "step2_title": "2. Add packages",
            "step3_title": "3. Run",
            "summary_heading": "pip vs uv",
            "summary_p1": "1. uv auto-creates the virtual env - no manual python -m venv",
            "summary_p2": "2. uv installs 10-100x faster than pip (written in Rust)",
            "summary_p3": "3. uv locks versions with pyproject.toml + uv.lock",
            "summary_p4": "4. uv run makes sure code runs in the right environment",
            "extra_banner_title": "Extra example: two outbreak projects at once",
            "extra_heading": "Two projects, two environments, zero conflicts",
            "extra_caption": "uv gives each project its own .venv, so versions never fight",
            "blindspot_banner_title": "3 Common Beginner Traps",
            "outro_heading": "Next up: Jupyter Lab interactive notebooks",
            "outro_sub": "uv run jupyter lab - launch with one command!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Helper: rounded card for diagrams
    # ------------------------------------------------------------------

    def _make_card(
        self,
        title: str,
        body_lines: list[str],
        *,
        width: float = 3.2,
        height: float = 2.4,
        accent: str = ACCENT_ORANGE,
    ) -> VGroup:
        """Create a rounded card with a coloured title and body text lines."""
        card = RoundedRectangle(
            corner_radius=0.15,
            width=width,
            height=height,
            fill_color=ManimColor(BG_CARD),
            fill_opacity=1,
            stroke_color=ManimColor(BORDER_LIGHT),
            stroke_width=2,
        )
        title_mob = Text(
            title,
            font=FONT_CJK,
            font_size=22,
            color=ManimColor(accent),
            weight="BOLD",
        )
        body_mobs = VGroup(
            *[
                Text(line, font=FONT_MONO, font_size=16, color=ManimColor(TEXT_PRIMARY))
                for line in body_lines
            ]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        content = VGroup(title_mob, body_mobs).arrange(DOWN, buff=0.3)
        content.move_to(card.get_center())
        return VGroup(card, content)

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the uv setup lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_venv_metaphor(self, duration: float = 5.0, **kwargs) -> None:
        """Virtual env = toolbox metaphor with two project cards side by side."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            self.t("venv_heading"),
            font=FONT_CJK,
            font_size=32,
            color=ManimColor(TEXT_PRIMARY),
        ).to_edge(UP, buff=0.8)

        toolbox_a = self._make_card(
            self.t("venv_box_a_title"),
            ["pandas 1.5", "matplotlib 3.6", "geopandas 0.12"],
            accent=ACCENT_ORANGE,
        )
        toolbox_b = self._make_card(
            self.t("venv_box_b_title"),
            ["pandas 2.1", "plotly 5.18", "dash 2.14"],
            accent=ACCENT_BLUE,
        )
        toolboxes = VGroup(toolbox_a, toolbox_b).arrange(RIGHT, buff=1.0).move_to(ORIGIN)

        caption = Text(
            self.t("venv_caption"),
            font=FONT_CJK,
            font_size=22,
            color=ManimColor(TEXT_SECONDARY),
        ).next_to(toolboxes, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(toolboxes, lag_ratio=0.3), run_time=1.0)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(max(0.1, duration - 2.6))
        self.play(FadeOut(VGroup(heading, toolboxes, caption)), run_time=0.5)

    def show_install_uv(self, duration: float = 5.0, **kwargs) -> None:
        """Show uv installation command."""
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            self.t("install_heading"),
            font=FONT_CJK,
            font_size=30,
            color=ManimColor(TEXT_PRIMARY),
        ).to_edge(UP, buff=0.8)

        code_panel = CodePanel(
            "curl -LsSf https://astral.sh/uv/install.sh | sh",
            title="Terminal",
            width=9.0,
            height=1.6,
        ).move_to(ORIGIN + UP * 0.3)

        note = Text(
            self.t("install_note"),
            font=FONT_CJK,
            font_size=20,
            color=ManimColor(TEXT_SECONDARY),
        ).next_to(code_panel, DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(Create(code_panel), run_time=0.8)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(max(0.1, duration - 2.3))
        self.play(FadeOut(VGroup(heading, code_panel, note)), run_time=0.5)

    def show_uv_workflow(self, duration: float = 6.0, **kwargs) -> None:
        """Three-step flow: uv init -> uv add -> uv run, connected by arrows."""
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            self.t("workflow_heading"),
            font=FONT_CJK,
            font_size=30,
            color=ManimColor(TEXT_PRIMARY),
        ).to_edge(UP, buff=0.8)

        # Three step cards
        step1 = self._make_card(
            self.t("step1_title"),
            ["uv init"],
            width=3.0,
            height=1.6,
            accent=ACCENT_ORANGE,
        )
        step2 = self._make_card(
            self.t("step2_title"),
            ["uv add pandas"],
            width=3.0,
            height=1.6,
            accent=ACCENT_BLUE,
        )
        step3 = self._make_card(
            self.t("step3_title"),
            ["uv run python", "  script.py"],
            width=3.0,
            height=1.6,
            accent=ACCENT_GREEN,
        )

        steps = VGroup(step1, step2, step3).arrange(RIGHT, buff=1.5).move_to(ORIGIN)

        # Arrows between cards
        arrow1 = Arrow(
            step1.get_right(),
            step2.get_left(),
            buff=0.15,
            color=ManimColor(TEXT_SECONDARY),
            stroke_width=3,
        )
        arrow2 = Arrow(
            step2.get_right(),
            step3.get_left(),
            buff=0.15,
            color=ManimColor(TEXT_SECONDARY),
            stroke_width=3,
        )

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(step1), run_time=0.5)
        self.play(Create(arrow1), FadeIn(step2), run_time=0.6)
        self.play(Create(arrow2), FadeIn(step3), run_time=0.6)
        self.wait(max(0.1, duration - 2.7))
        self.play(
            FadeOut(VGroup(heading, steps, arrow1, arrow2)),
            run_time=0.5,
        )

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        """pip vs uv comparison summary points."""
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            self.t("summary_heading"),
            font=FONT_CJK,
            font_size=34,
            color=ManimColor(ACCENT_ORANGE),
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(
                self.t("summary_p1"),
                font=FONT_CJK, font_size=22, color=ManimColor(TEXT_PRIMARY),
            ),
            Text(
                self.t("summary_p2"),
                font=FONT_CJK, font_size=22, color=ManimColor(TEXT_PRIMARY),
            ),
            Text(
                self.t("summary_p3"),
                font=FONT_CJK, font_size=22, color=ManimColor(TEXT_PRIMARY),
            ),
            Text(
                self.t("summary_p4"),
                font=FONT_CJK, font_size=22, color=ManimColor(TEXT_PRIMARY),
            ),
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
        banner = ExtraExampleBanner(self.t("extra_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        """Two project cards with different pandas versions showing isolation."""
        self.show_step_indicator(6, self.total_steps)

        heading = Text(
            self.t("extra_heading"),
            font=FONT_CJK,
            font_size=28,
            color=ManimColor(TEXT_PRIMARY),
        ).to_edge(UP, buff=0.8)

        project_a = self._make_card(
            "dengue-monitor/",
            ["pandas==1.5.3", "numpy==1.24.0", "geopandas==0.12"],
            width=4.0,
            height=2.6,
            accent=ACCENT_ORANGE,
        )
        project_b = self._make_card(
            "covid-dashboard/",
            ["pandas==2.1.4", "numpy==1.26.0", "plotly==5.18.0"],
            width=4.0,
            height=2.6,
            accent=ACCENT_BLUE,
        )
        projects = VGroup(project_a, project_b).arrange(RIGHT, buff=1.0).move_to(ORIGIN)

        caption = Text(
            self.t("extra_caption"),
            font=FONT_CJK,
            font_size=20,
            color=ManimColor(TEXT_SECONDARY),
        ).next_to(projects, DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(projects, lag_ratio=0.3), run_time=1.0)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(max(0.1, duration - 2.5))
        self.play(FadeOut(VGroup(heading, projects, caption)), run_time=0.5)

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_not_found(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: 'command not found: uv' vs restart terminal."""
        error_code = kwargs.get("error_code", "command not found: uv")
        correct_code = kwargs.get("correct_code", "source ~/.local/bin/env")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_uv_run(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: python script.py vs uv run python script.py."""
        error_code = kwargs.get("error_code", "python script.py")
        correct_code = kwargs.get("correct_code", "uv run python script.py")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_pyproject(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: requirements.txt vs pyproject.toml."""
        error_code = kwargs.get("error_code", "pip install -r requirements.txt")
        correct_code = kwargs.get("correct_code", "uv sync  # pyproject.toml + lock")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card pointing to next lesson."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            self.t("outro_heading"),
            font=FONT_CJK,
            font_size=28,
            color=ManimColor(ACCENT_ORANGE),
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            self.t("outro_sub"),
            font=FONT_CJK,
            font_size=22,
            color=ManimColor(TEXT_SECONDARY),
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(max(0.1, duration - 1.6))
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
