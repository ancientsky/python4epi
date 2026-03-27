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

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the Git basics lesson."""
        self.show_title_card("Git 版本控制", "程式碼的時光機", duration=duration)

    def show_what_is_git(self, duration: float = 6.0, **kwargs) -> None:
        """Time-machine metaphor: timeline with snapshot cards v1→v2→v3."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "Git 就像程式碼的時光機",
            font=FONT_CJK,
            font_size=32,
            color=ManimColor(TEXT_PRIMARY),
        ).to_edge(UP, buff=0.8)

        # Timeline: three version snapshot cards
        v1 = _flow_card("v1\n初始版本", width=2.6, height=1.4, fill=BG_CARD_ALT)
        v2 = _flow_card("v2\n新增分析", width=2.6, height=1.4, fill=BG_CARD_ALT)
        v3 = _flow_card("v3\n修正錯誤", width=2.6, height=1.4, fill=BG_CARD_ALT)

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
            "每次 commit = 一張快照，隨時可以回到過去",
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
            "Git 的三個區域",
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
            "每日工作流程",
            font=FONT_CJK,
            font_size=32,
            color=ManimColor(TEXT_PRIMARY),
        ).to_edge(UP, buff=0.8)

        card_add = _flow_card('git add .', width=3.0, height=1.2, fill=BG_CARD_ALT,
                              label_color=ACCENT_ORANGE, font_size=20)
        card_commit = _flow_card('git commit\n-m "描述"', width=3.0, height=1.2,
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
            "修改 → 暫存 → 提交 → 推到遠端",
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
            "最常用的 5 個指令",
            font=FONT_CJK,
            font_size=34,
            color=ManimColor(ACCENT_ORANGE),
        ).to_edge(UP, buff=0.8)

        commands = VGroup(
            Text("git status      查看目前狀態", font=FONT_MONO, font_size=22,
                 color=ManimColor(TEXT_PRIMARY)),
            Text("git add         暫存變更", font=FONT_MONO, font_size=22,
                 color=ManimColor(TEXT_PRIMARY)),
            Text("git commit      提交快照", font=FONT_MONO, font_size=22,
                 color=ManimColor(TEXT_PRIMARY)),
            Text("git push        推到遠端", font=FONT_MONO, font_size=22,
                 color=ManimColor(TEXT_PRIMARY)),
            Text("git pull        拉取最新", font=FONT_MONO, font_size=22,
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
        banner = ExtraExampleBanner("額外範例：多人協作寫疫調報告")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 7.0, **kwargs) -> None:
        """Two branches merging: descriptive analysis + spatial analysis."""
        self.show_step_indicator(6, self.total_steps)

        heading = Text(
            "多人協作：分支與合併",
            font=FONT_CJK,
            font_size=30,
            color=ManimColor(TEXT_PRIMARY),
        ).to_edge(UP, buff=0.8)

        # Main branch
        main_card = _flow_card("main\n疫調報告", width=2.8, height=1.2, fill=BG_CARD_ALT)
        main_card.move_to(LEFT * 4 + UP * 0.2)

        # Two branches
        branch_a = _flow_card("你的分支\n描述性分析", width=3.0, height=1.2,
                              fill=BG_CARD, label_color=ACCENT_ORANGE)
        branch_b = _flow_card("同事的分支\n空間分析", width=3.0, height=1.2,
                              fill=BG_CARD, label_color=ACCENT_BLUE)
        branch_a.move_to(RIGHT * 0.5 + UP * 1.5)
        branch_b.move_to(RIGHT * 0.5 + DOWN * 1.0)

        # Merged result
        merged = _flow_card("合併後\n完整報告", width=2.8, height=1.2,
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
        banner = BlindSpotBanner("初學者常見地雷 3 選")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_git_add(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: git add . (adds .env) vs .gitignore + specific add."""
        error_code = kwargs.get(
            "error_code",
            "git add .\n# 不小心把 .env 密碼檔也加進去了！",
        )
        correct_code = kwargs.get(
            "correct_code",
            "# 先建 .gitignore 排除 .env\ngit add analysis.py data/",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_commit_msg(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: vague 'update' message vs descriptive message."""
        error_code = kwargs.get(
            "error_code",
            'git commit -m "update"',
        )
        correct_code = kwargs.get(
            "correct_code",
            'git commit -m "feat: add epi curve plot\n for chapter 02"',
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_push_rejected(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: push rejected vs git pull first."""
        error_code = kwargs.get(
            "error_code",
            "git push\n# rejected: 遠端有新的 commit！",
        )
        correct_code = kwargs.get(
            "correct_code",
            "git pull          # 先拉最新版\ngit push          # 再推上去",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card pointing to the next topic."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            "下一集：課程地圖與學習路線",
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
