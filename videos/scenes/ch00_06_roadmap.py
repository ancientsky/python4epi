"""Ch00-06: 課程地圖——18 章學習攻略

Manim scene for the tutorial video on course roadmap and learning strategy.
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
    ERROR_RED,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    CodePanel,
    ErrorVsCorrect,
    ExtraExampleBanner,
    StepIndicator,
)


def _card(width: float, height: float, *, fill: str = BG_CARD) -> RoundedRectangle:
    """Return a rounded-corner card with a subtle border."""
    return RoundedRectangle(
        corner_radius=0.2,
        width=width,
        height=height,
        fill_color=ManimColor(fill),
        fill_opacity=1,
        stroke_color=ManimColor(BORDER_LIGHT),
        stroke_width=2,
    )


class Ch00RoadmapScene(EpiBaseScene):
    """Tutorial video scene: course roadmap and 18-chapter learning strategy."""

    total_steps: int = 12

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the Course Roadmap lesson."""
        self.show_title_card("課程地圖", "18 章學習攻略", duration=duration)

    def show_five_acts(self, duration: float = 6.0, **kwargs) -> None:
        """Five-act structure visualization as a vertical column of cards."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "五幕劇結構",
            font=FONT_CJK,
            font_size=32,
            color=ManimColor(TEXT_PRIMARY),
        ).to_edge(UP, buff=0.6)

        acts = [
            ("第一幕", "接獲通報", "Ch00-02", ACCENT_ORANGE),
            ("第二幕", "描述性分析", "Ch03-04", ACCENT_ORANGE),
            ("第三幕", "深入分析", "Ch05-08", ACCENT_BLUE),
            ("第四幕", "進階建模", "Ch09-12", ACCENT_BLUE),
            ("第五幕", "收尾與實戰", "Ch13-14", ACCENT_GREEN),
        ]

        act_cards = VGroup()
        for act_num, act_name, chapters, accent in acts:
            card = _card(8.0, 0.7)
            label = Text(
                f"{act_num}：{act_name}",
                font=FONT_CJK,
                font_size=22,
                color=ManimColor(accent),
                weight="BOLD",
            ).move_to(card.get_center() + LEFT * 1.5)
            ch_label = Text(
                chapters,
                font=FONT_MONO,
                font_size=18,
                color=ManimColor(TEXT_SECONDARY),
            ).move_to(card.get_center() + RIGHT * 2.5)
            act_cards.add(VGroup(card, label, ch_label))

        act_cards.arrange(DOWN, buff=0.15).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(act_cards, lag_ratio=0.2), run_time=1.5)
        self.wait(max(0.1, duration - 2.5))
        self.play(FadeOut(VGroup(heading, act_cards)), run_time=0.5)

    def show_must_do(self, duration: float = 6.0, **kwargs) -> None:
        """Required path: highlight Ch00-04 as sequential with arrow connections."""
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            "必修路線：Ch00 → Ch04",
            font=FONT_CJK,
            font_size=30,
            color=ManimColor(ACCENT_ORANGE),
        ).to_edge(UP, buff=0.8)

        chapter_names = [
            ("Ch00", "導讀與工具"),
            ("Ch01", "Python 基礎"),
            ("Ch02", "資料處理"),
            ("Ch03", "描述性統計"),
            ("Ch04", "群聚調查"),
        ]

        boxes = VGroup()
        for ch_id, ch_name in chapter_names:
            card = _card(2.0, 1.0)
            ch_text = Text(
                ch_id,
                font=FONT_MONO,
                font_size=20,
                color=ManimColor(ACCENT_ORANGE),
                weight="BOLD",
            ).move_to(card.get_center() + UP * 0.15)
            name_text = Text(
                ch_name,
                font=FONT_CJK,
                font_size=14,
                color=ManimColor(TEXT_SECONDARY),
            ).move_to(card.get_center() + DOWN * 0.2)
            boxes.add(VGroup(card, ch_text, name_text))

        boxes.arrange(RIGHT, buff=0.6).move_to(ORIGIN + DOWN * 0.2)

        # Create arrows between consecutive boxes
        arrows = VGroup()
        for i in range(len(boxes) - 1):
            arrow = Arrow(
                boxes[i].get_right(),
                boxes[i + 1].get_left(),
                buff=0.1,
                color=ManimColor(ACCENT_ORANGE),
                stroke_width=3,
            )
            arrows.add(arrow)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(boxes, lag_ratio=0.15), run_time=1.0)
        self.play(Create(arrows, lag_ratio=0.3), run_time=1.0)
        self.wait(max(0.1, duration - 3.0))
        self.play(FadeOut(VGroup(heading, boxes, arrows)), run_time=0.5)

    def show_choose_path(self, duration: float = 6.0, **kwargs) -> None:
        """Elective path: show Ch05-14 as a flexible grid, blue accent."""
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            "選修路線：依需求自由選擇",
            font=FONT_CJK,
            font_size=30,
            color=ManimColor(ACCENT_BLUE),
        ).to_edge(UP, buff=0.8)

        electives = [
            ("Ch05", "分層分析"),
            ("Ch06", "邏輯斯迴歸"),
            ("Ch07", "時間序列"),
            ("Ch08", "空間流病"),
            ("Ch09", "存活分析"),
            ("Ch10", "機器學習"),
            ("Ch11", "深度學習"),
            ("Ch12", "因果推論"),
            ("Ch13", "可重現研究"),
            ("Ch14", "實戰案例"),
        ]

        grid = VGroup()
        for ch_id, ch_name in electives:
            card = _card(2.2, 0.8)
            ch_text = Text(
                ch_id,
                font=FONT_MONO,
                font_size=16,
                color=ManimColor(ACCENT_BLUE),
                weight="BOLD",
            ).move_to(card.get_center() + UP * 0.1)
            name_text = Text(
                ch_name,
                font=FONT_CJK,
                font_size=13,
                color=ManimColor(TEXT_SECONDARY),
            ).move_to(card.get_center() + DOWN * 0.15)
            grid.add(VGroup(card, ch_text, name_text))

        # Arrange as 2 rows of 5
        row1 = VGroup(*grid[:5]).arrange(RIGHT, buff=0.3)
        row2 = VGroup(*grid[5:]).arrange(RIGHT, buff=0.3)
        full_grid = VGroup(row1, row2).arrange(DOWN, buff=0.25).move_to(ORIGIN + DOWN * 0.2)

        note = Text(
            "完成 Ch00-04 後，可依興趣跳選",
            font=FONT_CJK,
            font_size=20,
            color=ManimColor(TEXT_SECONDARY),
        ).to_edge(DOWN, buff=0.7)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(full_grid, lag_ratio=0.08), run_time=1.2)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(max(0.1, duration - 2.6))
        self.play(FadeOut(VGroup(heading, full_grid, note)), run_time=0.5)

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        """Summarise three learning tips."""
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            "學習攻略",
            font=FONT_CJK,
            font_size=34,
            color=ManimColor(ACCENT_ORANGE),
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(
                "1. Ch00-04 是必修，打好基礎再往下",
                font=FONT_CJK, font_size=24, color=ManimColor(TEXT_PRIMARY),
            ),
            Text(
                "2. Ch05-14 可依角色與需求自由選修",
                font=FONT_CJK, font_size=24, color=ManimColor(TEXT_PRIMARY),
            ),
            Text(
                "3. 所有章節共用同一個退伍軍人症資料集",
                font=FONT_CJK, font_size=24, color=ManimColor(TEXT_PRIMARY),
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
        banner = ExtraExampleBanner("額外範例：不同角色的學習路線")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        """Three role cards showing recommended chapter paths."""
        self.show_step_indicator(5, self.total_steps)

        heading = Text(
            "依角色選擇學習路線",
            font=FONT_CJK,
            font_size=28,
            color=ManimColor(ACCENT_BLUE),
        ).to_edge(UP, buff=0.8)

        roles = [
            ("感控護理師", "Ch00-04\n重點：Ch03-04", ACCENT_ORANGE),
            ("疫調人員", "Ch00-04\n重點：Ch07-08", ACCENT_BLUE),
            ("Data Scientist", "全修 Ch00-14\n重點：Ch10-12", ACCENT_GREEN),
        ]

        role_cards = VGroup()
        for role_name, desc, accent in roles:
            card = _card(3.5, 2.8)
            title_mob = Text(
                role_name,
                font=FONT_CJK,
                font_size=24,
                color=ManimColor(accent),
                weight="BOLD",
            ).move_to(card.get_top() + DOWN * 0.45)
            desc_mob = Text(
                desc,
                font=FONT_CJK,
                font_size=18,
                color=ManimColor(TEXT_SECONDARY),
                line_spacing=1.3,
            ).move_to(card.get_center() + DOWN * 0.2)
            role_cards.add(VGroup(card, title_mob, desc_mob))

        role_cards.arrange(RIGHT, buff=0.4).move_to(ORIGIN + DOWN * 0.2)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(role_cards, lag_ratio=0.3), run_time=1.2)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(heading, role_cards)), run_time=0.5)

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner("初學者常見盲點 3 選")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_where_start(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: random chapter vs Ch00-01 first."""
        error_code = kwargs.get(
            "error_code",
            "# 隨便挑一章開始\n"
            "# 直接跳到 Ch10 機器學習\n"
            "import sklearn  # 基礎還沒學！",
        )
        correct_code = kwargs.get(
            "correct_code",
            "# 從 Ch00-01 開始\n"
            "# 先學工具與 Python 基礎\n"
            "print('Hello, Epi!')  # 穩扎穩打",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_skip(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: skip Ch02 vs sequential for Ch00-04."""
        error_code = kwargs.get(
            "error_code",
            "# 跳過 Ch02 資料處理\n"
            "# 直接做 Ch03 描述性統計\n"
            "df.groupby(...)  # 看不懂！",
        )
        correct_code = kwargs.get(
            "correct_code",
            "# Ch00 → Ch01 → Ch02 → Ch03\n"
            "# 按順序學完必修五章\n"
            "# Ch02 教的 pandas 是基礎",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_colab(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: Colab-only vs local install for full features."""
        error_code = kwargs.get(
            "error_code",
            "# 只用 Colab 不裝本機環境\n"
            "# 網路斷線就無法練習\n"
            "# 大型資料跑不動",
        )
        correct_code = kwargs.get(
            "correct_code",
            "# 本機安裝 uv + Python\n"
            "# uv sync\n"
            "# 離線也能練習，效能更好",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card: congratulations, go to Ch01."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            "恭喜！課程地圖到手",
            font=FONT_CJK,
            font_size=32,
            color=ManimColor(ACCENT_ORANGE),
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "下一站：Ch01 Python 基礎，開始寫程式吧！",
            font=FONT_CJK,
            font_size=22,
            color=ManimColor(TEXT_SECONDARY),
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(max(0.1, duration - 1.6))
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
