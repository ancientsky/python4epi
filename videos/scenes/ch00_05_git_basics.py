"""Ch00-05: Git 版本控制——程式碼的時光機

Manim scene for the tutorial video on Git version control basics.
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
)


def _flow_card(
    label: str,
    *,
    width: float = 2.8,
    height: float = 1.2,
    fill: str = BG_CARD,
    label_color: str = TEXT_PRIMARY,
    font_size: int = 22,
) -> VGroup:
    """Create a rounded-corner card with centred label text."""
    card = RoundedRectangle(
        corner_radius=0.15,
        width=width,
        height=height,
        fill_color=ManimColor(fill),
        fill_opacity=1,
        stroke_color=ManimColor(BORDER_LIGHT),
        stroke_width=2,
    )
    text = Text(label, font=FONT_CJK, font_size=font_size, color=ManimColor(label_color))
    text.move_to(card.get_center())
    return VGroup(card, text)


class Ch00GitBasicsScene(EpiBaseScene):
    """Tutorial video scene: Git version control basics."""

    total_steps: int = 12

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "Git 版本控制",
            "title_sub": "程式碼的時光機",
            "what_heading": "Git 就像程式碼的時光機",
            "what_v1": "v1\n初始版本",
            "what_v2": "v2\n新增分析",
            "what_v3": "v3\n修正錯誤",
            "what_caption": "每次 commit = 一張快照，隨時可以回到過去",
            "areas_heading": "Git 的三個區域",
            "workflow_heading": "每日工作流程",
            "workflow_commit_card": 'git commit\n-m "描述"',
            "workflow_caption": "修改 → 暫存 → 提交 → 推到遠端",
            "summary_heading": "最常用的 5 個指令",
            "summary_cmd1": "git status      查看目前狀態",
            "summary_cmd2": "git add         暫存變更",
            "summary_cmd3": "git commit      提交快照",
            "summary_cmd4": "git push        推到遠端",
            "summary_cmd5": "git pull        拉取最新",
            "extra_banner_title": "額外範例：多人協作寫疫調報告",
            "extra_heading": "多人協作：分支與合併",
            "extra_main_card": "main\n疫調報告",
            "extra_branch_a": "你的分支\n描述性分析",
            "extra_branch_b": "同事的分支\n空間分析",
            "extra_merged": "合併後\n完整報告",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：課程地圖與學習路線",
        },
        "en": {
            "title_main": "Git Version Control",
            "title_sub": "A time machine for your code",
            "what_heading": "Git Is Like a Time Machine for Code",
            "what_v1": "v1\nInitial version",
            "what_v2": "v2\nAdd analysis",
            "what_v3": "v3\nFix bugs",
            "what_caption": "Each commit = a snapshot; jump back in time anytime",
            "areas_heading": "Git's Three Areas",
            "workflow_heading": "Daily Workflow",
            "workflow_commit_card": 'git commit\n-m "message"',
            "workflow_caption": "edit -> stage -> commit -> push to remote",
            "summary_heading": "The 5 Most-Used Commands",
            "summary_cmd1": "git status      check current state",
            "summary_cmd2": "git add         stage changes",
            "summary_cmd3": "git commit      save a snapshot",
            "summary_cmd4": "git push        push to remote",
            "summary_cmd5": "git pull        fetch the latest",
            "extra_banner_title": "Extra example: co-authoring an outbreak report",
            "extra_heading": "Collaboration: branches and merging",
            "extra_main_card": "main\noutbreak report",
            "extra_branch_a": "your branch\ndescriptive analysis",
            "extra_branch_b": "colleague's branch\nspatial analysis",
            "extra_merged": "after merge\ncomplete report",
            "blindspot_banner_title": "3 Common Beginner Traps",
            "outro_heading": "Next up: course roadmap and learning path",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the Git basics lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_what_is_git(self, duration: float = 6.0, **kwargs) -> None:
        """Time-machine metaphor: timeline with snapshot cards v1→v2→v3."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            self.t("what_heading"),
            font=FONT_CJK,
            font_size=32,
            color=ManimColor(TEXT_PRIMARY),
        ).to_edge(UP, buff=0.8)

        # Timeline: three version snapshot cards
        v1 = _flow_card(self.t("what_v1"), width=2.6, height=1.4, fill=BG_CARD_ALT)
        v2 = _flow_card(self.t("what_v2"), width=2.6, height=1.4, fill=BG_CARD_ALT)
        v3 = _flow_card(self.t("what_v3"), width=2.6, height=1.4, fill=BG_CARD_ALT)

        versions = VGroup(v1, v2, v3).arrange(RIGHT, buff=1.8).move_to(ORIGIN)

        arrow_1 = Arrow(
            v1.get_right(), v2.get_left(),
            color=ManimColor(ACCENT_ORANGE), stroke_width=3, buff=0.1,
        )
        arrow_2 = Arrow(
            v2.get_right(), v3.get_left(),
            color=ManimColor(ACCENT_ORANGE), stroke_width=3, buff=0.1,
        )

        caption = Text(
            self.t("what_caption"),
            font=FONT_CJK,
            font_size=22,
            color=ManimColor(TEXT_SECONDARY),
        ).next_to(versions, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(v1), run_time=0.5)
        self.play(Create(arrow_1), FadeIn(v2), run_time=0.6)
        self.play(Create(arrow_2), FadeIn(v3), run_time=0.6)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.6))
        self.play(
            FadeOut(VGroup(heading, v1, v2, v3, arrow_1, arrow_2, caption)),
            run_time=0.5,
        )

    def show_three_areas(self, duration: float = 6.0, **kwargs) -> None:
        """Flow diagram: Working Directory → Staging Area → Repository."""
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            self.t("areas_heading"),
            font=FONT_CJK,
            font_size=32,
            color=ManimColor(TEXT_PRIMARY),
        ).to_edge(UP, buff=0.8)

        wd = _flow_card("Working\nDirectory", fill=BG_CARD, width=3.0, height=1.6)
        sa = _flow_card("Staging\nArea", fill=BG_CARD_ALT, width=3.0, height=1.6)
        repo = _flow_card("Repository", fill=ACCENT_GREEN, width=3.0, height=1.6,
                          label_color="#FFFFFF")

        areas = VGroup(wd, sa, repo).arrange(RIGHT, buff=1.6).move_to(ORIGIN + UP * 0.2)

        arrow_add = Arrow(
            wd.get_right(), sa.get_left(),
            color=ManimColor(ACCENT_ORANGE), stroke_width=3, buff=0.1,
        )
        label_add = Text(
            "git add", font=FONT_MONO, font_size=18, color=ManimColor(ACCENT_ORANGE),
        ).next_to(arrow_add, UP, buff=0.15)

        arrow_commit = Arrow(
            sa.get_right(), repo.get_left(),
            color=ManimColor(ACCENT_ORANGE), stroke_width=3, buff=0.1,
        )
        label_commit = Text(
            "git commit", font=FONT_MONO, font_size=18, color=ManimColor(ACCENT_ORANGE),
        ).next_to(arrow_commit, UP, buff=0.15)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(wd), run_time=0.4)
        self.play(Create(arrow_add), FadeIn(label_add), FadeIn(sa), run_time=0.7)
        self.play(Create(arrow_commit), FadeIn(label_commit), FadeIn(repo), run_time=0.7)
        self.wait(max(0.1, duration - 2.7))
        self.play(
            FadeOut(VGroup(heading, wd, sa, repo, arrow_add, label_add,
                           arrow_commit, label_commit)),
            run_time=0.5,
        )

    def show_daily_workflow(self, duration: float = 6.0, **kwargs) -> None:
        """Three command cards: git add → git commit → git push."""
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            self.t("workflow_heading"),
            font=FONT_CJK,
            font_size=32,
            color=ManimColor(TEXT_PRIMARY),
        ).to_edge(UP, buff=0.8)

        card_add = _flow_card('git add .', width=3.0, height=1.2, fill=BG_CARD_ALT,
                              label_color=ACCENT_ORANGE, font_size=20)
        card_commit = _flow_card(self.t("workflow_commit_card"), width=3.0, height=1.2,
                                 fill=BG_CARD_ALT, label_color=ACCENT_ORANGE, font_size=20)
        card_push = _flow_card('git push', width=3.0, height=1.2, fill=BG_CARD_ALT,
                               label_color=ACCENT_ORANGE, font_size=20)

        cards = VGroup(card_add, card_commit, card_push).arrange(RIGHT, buff=1.6).move_to(ORIGIN)

        arrow_1 = Arrow(
            card_add.get_right(), card_commit.get_left(),
            color=ManimColor(ACCENT_BLUE), stroke_width=3, buff=0.1,
        )
        arrow_2 = Arrow(
            card_commit.get_right(), card_push.get_left(),
            color=ManimColor(ACCENT_BLUE), stroke_width=3, buff=0.1,
        )

        caption = Text(
            self.t("workflow_caption"),
            font=FONT_CJK,
            font_size=22,
            color=ManimColor(TEXT_SECONDARY),
        ).next_to(cards, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(card_add), run_time=0.4)
        self.play(Create(arrow_1), FadeIn(card_commit), run_time=0.5)
        self.play(Create(arrow_2), FadeIn(card_push), run_time=0.5)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.7))
        self.play(
            FadeOut(VGroup(heading, card_add, card_commit, card_push,
                           arrow_1, arrow_2, caption)),
            run_time=0.5,
        )

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise the 5 most-used Git commands."""
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            self.t("summary_heading"),
            font=FONT_CJK,
            font_size=34,
            color=ManimColor(ACCENT_ORANGE),
        ).to_edge(UP, buff=0.8)

        commands = VGroup(
            Text(self.t("summary_cmd1"), font=FONT_MONO, font_size=22,
                 color=ManimColor(TEXT_PRIMARY)),
            Text(self.t("summary_cmd2"), font=FONT_MONO, font_size=22,
                 color=ManimColor(TEXT_PRIMARY)),
            Text(self.t("summary_cmd3"), font=FONT_MONO, font_size=22,
                 color=ManimColor(TEXT_PRIMARY)),
            Text(self.t("summary_cmd4"), font=FONT_MONO, font_size=22,
                 color=ManimColor(TEXT_PRIMARY)),
            Text(self.t("summary_cmd5"), font=FONT_MONO, font_size=22,
                 color=ManimColor(TEXT_PRIMARY)),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(commands, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(heading, commands)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example methods
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the ExtraExampleBanner section divider."""
        banner = ExtraExampleBanner(self.t("extra_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 7.0, **kwargs) -> None:
        """Two branches merging: descriptive analysis + spatial analysis."""
        self.show_step_indicator(6, self.total_steps)

        heading = Text(
            self.t("extra_heading"),
            font=FONT_CJK,
            font_size=30,
            color=ManimColor(TEXT_PRIMARY),
        ).to_edge(UP, buff=0.8)

        # Main branch
        main_card = _flow_card(self.t("extra_main_card"), width=2.8, height=1.2, fill=BG_CARD_ALT)
        main_card.move_to(LEFT * 4 + UP * 0.2)

        # Two branches
        branch_a = _flow_card(self.t("extra_branch_a"), width=3.0, height=1.2,
                              fill=BG_CARD, label_color=ACCENT_ORANGE)
        branch_b = _flow_card(self.t("extra_branch_b"), width=3.0, height=1.2,
                              fill=BG_CARD, label_color=ACCENT_BLUE)
        branch_a.move_to(RIGHT * 0.5 + UP * 1.5)
        branch_b.move_to(RIGHT * 0.5 + DOWN * 1.0)

        # Merged result
        merged = _flow_card(self.t("extra_merged"), width=2.8, height=1.2,
                            fill=ACCENT_GREEN, label_color="#FFFFFF")
        merged.move_to(RIGHT * 4.5 + UP * 0.2)

        arrow_ma = Arrow(main_card.get_right(), branch_a.get_left(),
                         color=ManimColor(ACCENT_ORANGE), stroke_width=3, buff=0.1)
        arrow_mb = Arrow(main_card.get_right(), branch_b.get_left(),
                         color=ManimColor(ACCENT_BLUE), stroke_width=3, buff=0.1)
        arrow_am = Arrow(branch_a.get_right(), merged.get_left(),
                         color=ManimColor(ACCENT_ORANGE), stroke_width=3, buff=0.1)
        arrow_bm = Arrow(branch_b.get_right(), merged.get_left(),
                         color=ManimColor(ACCENT_BLUE), stroke_width=3, buff=0.1)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(main_card), run_time=0.4)
        self.play(
            Create(arrow_ma), FadeIn(branch_a),
            Create(arrow_mb), FadeIn(branch_b),
            run_time=0.8,
        )
        self.play(
            Create(arrow_am), Create(arrow_bm), FadeIn(merged),
            run_time=0.8,
        )
        self.wait(max(0.1, duration - 2.9))
        self.play(
            FadeOut(VGroup(heading, main_card, branch_a, branch_b, merged,
                           arrow_ma, arrow_mb, arrow_am, arrow_bm)),
            run_time=0.5,
        )

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_git_add(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: git add . (adds .env) vs .gitignore + specific add."""
        error_code = kwargs.get("error_code", "git add .  # includes .env!")
        correct_code = kwargs.get("correct_code", "git add analysis.py data/")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_commit_msg(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: vague 'update' message vs descriptive message."""
        error_code = kwargs.get("error_code", 'git commit -m "update"')
        correct_code = kwargs.get("correct_code", 'git commit -m "feat: add epi curve"')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_push_rejected(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: push rejected vs git pull first."""
        error_code = kwargs.get("error_code", "git push  # rejected!")
        correct_code = kwargs.get("correct_code", "git pull && git push")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card pointing to the next topic."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            self.t("outro_heading"),
            font=FONT_CJK,
            font_size=28,
            color=ManimColor(ACCENT_ORANGE),
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "Next: Course roadmap",
            font=FONT_MONO,
            font_size=22,
            color=ManimColor(TEXT_SECONDARY),
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(max(0.1, duration - 1.6))
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
