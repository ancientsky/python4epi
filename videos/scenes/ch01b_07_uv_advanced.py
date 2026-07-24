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

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "uv 進階",
            "title_sub": "管理 Python 版本與套件",
            "versions_heading": "用 uv 管理多版本 Python",
            "versions_cmd1": "uv python install 3.11   # 安裝 Python 3.11",
            "versions_cmd2": "uv python install 3.12   # 安裝 Python 3.12",
            "versions_cmd3": "uv python pin 3.12       # 鎖定此專案版本",
            "versions_cmd4": "uv run python --version  # 確認版本",
            "versions_note": "不同專案可以用不同版本的 Python，互不干擾",
            "add_heading": "uv add — 安裝套件並記錄",
            "add_cmd1": "uv add pandas            # 最新版",
            "add_cmd2": 'uv add "pandas>=2.0"     # 指定版本',
            "add_cmd3": "uv add --dev pytest      # 開發用",
            "add_cmd4": "uv add matplotlib seaborn # 多個",
            "add_note": "所有安裝紀錄存在 pyproject.toml",
            "find_heading": "怎麼找到好用的套件？",
            "find_p1": "1. 去 pypi.org 搜尋關鍵字",
            "find_p2": "2. 看 GitHub stars 和下載量",
            "find_p3": "3. 確認最近有更新（活躍維護）",
            "find_p4": "4. 流病常用：pandas, seaborn, scipy",
            "find_p5": "5. 進階：lifelines, geopandas, plotly",
            "sync_heading": "uv sync — 一鍵復原開發環境",
            "sync_note": "有 pyproject.toml + uv.lock → 一鍵還原",
            "summary_heading": "重點整理",
            "summary_p1": "1. uv python install — 裝不同版本",
            "summary_p2": "2. uv add — 安裝並記錄套件",
            "summary_p3": "3. uv sync — 一鍵復原環境",
            "summary_p4": "4. pypi.org 找套件看星星和下載量",
            "extra_banner_title": "額外範例：建立疫苗覆蓋率分析專案",
            "extra_heading": "從零建立專案的完整流程",
            "extra_step1": "1. uv init vaccine_coverage     # 建立專案",
            "extra_step2": "2. cd vaccine_coverage",
            "extra_step3": "3. uv add pandas matplotlib      # 裝套件",
            "extra_step4": "4. uv run python analyze.py      # 執行分析",
            "extra_note": "同事接手？只要 uv sync 就能復現環境！",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：Jupyter 實用密技",
            "outro_sub": "讓你的分析效率翻倍！",
        },
        "en": {
            "title_main": "Advanced uv",
            "title_sub": "Manage Python versions and packages",
            "versions_heading": "Manage multiple Python versions with uv",
            "versions_cmd1": "uv python install 3.11   # install Python 3.11",
            "versions_cmd2": "uv python install 3.12   # install Python 3.12",
            "versions_cmd3": "uv python pin 3.12       # pin this project's version",
            "versions_cmd4": "uv run python --version  # check the version",
            "versions_note": "Different projects can use different Python versions, no interference",
            "add_heading": "uv add — install packages and record them",
            "add_cmd1": "uv add pandas            # latest version",
            "add_cmd2": 'uv add "pandas>=2.0"     # pin a version',
            "add_cmd3": "uv add --dev pytest      # dev-only",
            "add_cmd4": "uv add matplotlib seaborn # multiple at once",
            "add_note": "Every install is recorded in pyproject.toml",
            "find_heading": "How do you find good packages?",
            "find_p1": "1. Search keywords on pypi.org",
            "find_p2": "2. Check GitHub stars and download counts",
            "find_p3": "3. Confirm recent updates (actively maintained)",
            "find_p4": "4. Epi favorites: pandas, seaborn, scipy",
            "find_p5": "5. Advanced: lifelines, geopandas, plotly",
            "sync_heading": "uv sync — restore the dev environment in one command",
            "sync_note": "With pyproject.toml + uv.lock → one-command restore",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. uv python install — install different versions",
            "summary_p2": "2. uv add — install and record packages",
            "summary_p3": "3. uv sync — restore the environment in one command",
            "summary_p4": "4. Find packages on pypi.org by stars and downloads",
            "extra_banner_title": "Extra example: build a vaccine-coverage analysis project",
            "extra_heading": "The full flow of building a project from scratch",
            "extra_step1": "1. uv init vaccine_coverage     # create the project",
            "extra_step2": "2. cd vaccine_coverage",
            "extra_step3": "3. uv add pandas matplotlib      # install packages",
            "extra_step4": "4. uv run python analyze.py      # run the analysis",
            "extra_note": "A colleague takes over? Just uv sync to reproduce it all!",
            "blindspot_banner_title": "3 Common Beginner Pitfalls",
            "outro_heading": "Next up: practical Jupyter tips",
            "outro_sub": "Double your analysis efficiency!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_python_versions(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            self.t("versions_heading"),
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        cmds = VGroup(
            Text(self.t("versions_cmd1"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text(self.t("versions_cmd2"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text(self.t("versions_cmd3"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text(self.t("versions_cmd4"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.6)

        note = Text(
            self.t("versions_note"),
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
            self.t("add_heading"),
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        cmds = VGroup(
            Text(self.t("add_cmd1"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text(self.t("add_cmd2"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text(self.t("add_cmd3"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text(self.t("add_cmd4"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.6)

        note = Text(
            self.t("add_note"),
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
            self.t("find_heading"),
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("find_p1"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("find_p2"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("find_p3"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("find_p4"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("find_p5"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(points, lag_ratio=0.2), run_time=1.2)
        self.wait(duration - 1.6)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_uv_sync(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            self.t("sync_heading"),
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        code_text = "# Clone a project\n# git clone <repo-url>\n# cd python4epi\n# uv sync\n# Done! All deps installed."
        code_panel = CodePanel(code_text, title="terminal", width=7.0, height=2.8).next_to(heading, DOWN, buff=0.5)

        note = Text(
            self.t("sync_note"),
            font=FONT_CJK, font_size=20, color=TEXT_SECONDARY,
        ).next_to(code_panel, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(Create(code_panel), run_time=0.8)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(duration - 1.6)
        self.play(FadeOut(VGroup(heading, code_panel, note)), run_time=0.5)

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

        heading = Text(
            self.t("extra_heading"),
            font=FONT_CJK, font_size=26, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        steps = VGroup(
            Text(self.t("extra_step1"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text(self.t("extra_step2"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text(self.t("extra_step3"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
            Text(self.t("extra_step4"), font=FONT_MONO, font_size=18, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.6)

        note = Text(
            self.t("extra_note"),
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
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
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
            self.t("outro_heading"),
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)
        sub = Text(self.t("outro_sub"), font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(heading, DOWN, buff=0.4)
        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
