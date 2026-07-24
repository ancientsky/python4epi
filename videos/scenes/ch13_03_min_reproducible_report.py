"""Ch13-03: The minimal reproducible report - three commands, clean env to report.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; command strings stay identical across
languages and are rendered with a font-safe terminal card (never ``Code()``).
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    UP,
    FadeIn,
    FadeOut,
    ManimColor,
    RoundedRectangle,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_GREEN,
    ACCENT_ORANGE,
    BORDER_LIGHT,
    CODE_BG,
    CODE_TEXT,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch13MinReportScene(EpiBaseScene):
    """Tutorial video scene: three commands from a clean environment to a report."""

    total_steps: int = 9

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "最小可重跑報告",
            "title_sub": "三行指令，從乾淨環境到報告",
            "goal_heading": "目標：零手動步驟",
            "goal_lines": [
                "從「原始資料」到「報告」之間，沒有腦中步驟",
                "別人複製 repo、跑幾行固定指令就重現",
                "不用問你「還要裝什麼、改哪裡」",
                "→ 這就是 single-command workflow",
            ],
            "commands_heading": "關鍵就這三行指令",
            "breakdown_heading": "三行的分工",
            "breakdown_lines": [
                "uv sync：依 uv.lock 重建環境，版本一致",
                "uv run pytest：驗證環境是活的、程式是對的",
                "uv run python：真正跑分析、產出報告",
                "→ 裝好、驗好、跑好，一氣呵成",
            ],
            "why_heading": "為什麼堅持單一命令",
            "why_lines": [
                "手動步驟是可重現的頭號殺手",
                "靠人腦記憶的一步，過幾個月連你都忘",
                "寫成固定指令 = 把記憶外包給程式",
                "→ 每個數字都可追溯（traceability）",
            ],
            "summary_heading": "最小可重跑報告三重點",
            "summary_lines": [
                "① 乾淨環境 + 固定指令 + 固定程式碼",
                "② 三行分工：建環境 / 驗證 / 產報告",
                "③ 零手動步驟，複製貼上就重現",
                "→ 下一集：把資料變成唯一的標準答案",
            ],
            "extra_banner_title": "額外範例：一行指令產出流感週報",
            "extra_flu_heading": "流感週報，一鍵長出來",
            "blindspot_banner_title": "單一命令三個新手地雷",
            "outro_heading": "下一集：讀資料 → 唯一的標準答案",
            "outro_sub": "Step 2：確定性摘要，一份就對",
        },
        "en": {
            "title_main": "The Minimal Reproducible Report",
            "title_sub": "Three commands, clean environment to report",
            "goal_heading": "Goal: zero manual steps",
            "goal_lines": [
                'From "raw data" to "report", no in-your-head steps',
                "Others clone the repo, run a few fixed commands",
                'No need to ask "what else to install or change"',
                "-> this is the single-command workflow",
            ],
            "commands_heading": "It's just these three commands",
            "breakdown_heading": "What each command does",
            "breakdown_lines": [
                "uv sync: rebuild env from uv.lock, same versions",
                "uv run pytest: prove env is alive, code is right",
                "uv run python: actually run analysis, make report",
                "-> install, verify, run - in one flow",
            ],
            "why_heading": "Why insist on one command",
            "why_lines": [
                "Manual steps are reproducibility's #1 killer",
                "A step held in memory is forgotten in months",
                "Fixed commands = outsource memory to code",
                "-> every number is traceable (traceability)",
            ],
            "summary_heading": "Three Takeaways",
            "summary_lines": [
                "1. Clean env + fixed commands + fixed code",
                "2. Three roles: build / verify / report",
                "3. Zero manual steps, copy-paste to reproduce",
                "-> Next: turn data into one canonical answer",
            ],
            "extra_banner_title": "Extra example: a one-command flu weekly report",
            "extra_flu_heading": "Flu weekly report, one keystroke",
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: read data -> one canonical answer",
            "outro_sub": "Step 2: a deterministic summary, right every time",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _bullets(self, heading_key: str, lines_key: str, duration: float) -> None:
        h = Text(
            self.t(heading_key), font=FONT_CJK, font_size=30, color=ManimColor(ACCENT_ORANGE)
        ).to_edge(UP, buff=0.8)
        bl = (
            VGroup(
                *[
                    Text(x, font=FONT_CJK, font_size=22, color=ManimColor(TEXT_PRIMARY))
                    for x in self.t(lines_key)
                ]
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            .next_to(h, DOWN, buff=0.6)
        )
        self.play(FadeIn(h), run_time=0.5)
        self.play(FadeIn(bl, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(h, bl)), run_time=0.5)

    def _terminal_card(self, heading_key: str, code: str, duration: float) -> None:
        """Render shell commands with ``Text(FONT_MONO)`` - never ``Code()``.

        ``Code()`` crashes in Manim v0.20.1 on shell strings, so a plain dark
        card with monospace prompt lines is used instead.
        """
        h = Text(
            self.t(heading_key), font=FONT_CJK, font_size=26, color=ManimColor(ACCENT_ORANGE)
        ).to_edge(UP, buff=0.7)
        lines = [ln for ln in code.strip("\n").split("\n") if ln.strip()]
        rows = VGroup(
            *[
                Text(f"$ {ln}", font=FONT_MONO, font_size=24, color=ManimColor(CODE_TEXT))
                for ln in lines
            ]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        card = RoundedRectangle(
            corner_radius=0.15,
            width=max(rows.width + 1.2, 7.0),
            height=rows.height + 1.0,
            fill_color=ManimColor(CODE_BG),
            fill_opacity=1,
            stroke_color=ManimColor(BORDER_LIGHT),
            stroke_width=1.5,
        ).move_to(ORIGIN + DOWN * 0.2)
        rows.move_to(card.get_center())
        self.play(FadeIn(h), run_time=0.4)
        self.play(FadeIn(card), run_time=0.4)
        self.play(FadeIn(rows, lag_ratio=0.3), run_time=1.0)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(h, card, rows)), run_time=0.5)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_the_goal(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("goal_heading", "goal_lines", duration)

    def show_three_commands(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        code = kwargs.get(
            "code",
            ("uv sync\nuv run pytest\nuv run python notebooks/run_sitrep.py"),
        )
        self._terminal_card("commands_heading", code, duration)

    def show_command_breakdown(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets("breakdown_heading", "breakdown_lines", duration)

    def show_why_single_command(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("why_heading", "why_lines", duration)

    def show_main_summary(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_flu(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        code = kwargs.get("code", "uv run python notebooks/flu_weekly.py")
        self._terminal_card("extra_flu_heading", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_bs_manual_steps(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "# remember to set PATH first"),
            kwargs.get("correct_code", "uv sync  # zero manual steps"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_bs_pip_vs_uv(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "pip install -r requirements.txt"),
            kwargs.get("correct_code", "uv sync  # uses uv.lock"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_bs_no_clean_env(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "python run_sitrep.py  # my machine"),
            kwargs.get("correct_code", "uv run pytest && uv run run_sitrep.py"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text(
            self.t("outro_heading"), font=FONT_CJK, font_size=26, color=ManimColor(ACCENT_ORANGE)
        ).move_to(ORIGIN + UP * 0.5)
        s = Text(
            self.t("outro_sub"), font=FONT_CJK, font_size=20, color=ManimColor(TEXT_SECONDARY)
        ).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
