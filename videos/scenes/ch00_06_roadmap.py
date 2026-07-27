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
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    ManimColor,
    RoundedRectangle,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_BLUE,
    ACCENT_GREEN,
    ACCENT_ORANGE,
    BG_CARD,
    BORDER_LIGHT,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
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

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "課程地圖",
            "title_sub": "18 章學習攻略",
            "acts_heading": "五幕劇結構",
            "act1_label": "第一幕：接獲通報",
            "act2_label": "第二幕：描述性分析",
            "act3_label": "第三幕：深入分析",
            "act4_label": "第四幕：進階建模",
            "act5_label": "第五幕：收尾與實戰",
            "mustdo_heading": "必修路線：Ch00 → Ch04",
            "mustdo_ch0": "導讀與工具",
            "mustdo_ch1": "Python 基礎",
            "mustdo_ch2": "資料處理",
            "mustdo_ch3": "描述性統計",
            "mustdo_ch4": "群聚調查",
            "choose_heading": "選修路線：依需求自由選擇",
            "elec_ch5": "分層分析",
            "elec_ch6": "邏輯斯迴歸",
            "elec_ch7": "時間序列",
            "elec_ch8": "空間流病",
            "elec_ch9": "存活分析",
            "elec_ch10": "機器學習",
            "elec_ch11": "深度學習",
            "elec_ch12": "因果推論",
            "elec_ch13": "可重現研究",
            "elec_ch14": "實戰案例",
            "choose_note": "完成 Ch00-04 後，可依興趣跳選",
            "summary_heading": "學習攻略",
            "summary_p1": "1. Ch00-04 是必修，打好基礎再往下",
            "summary_p2": "2. Ch05-14 可依角色與需求自由選修",
            "summary_p3": "3. 所有章節共用同一個退伍軍人症資料集",
            "extra_banner_title": "額外範例：不同角色的學習路線",
            "extra_heading": "依角色選擇學習路線",
            "role1_name": "感控護理師",
            "role1_desc": "Ch00-04\n重點：Ch03-04",
            "role2_name": "疫調人員",
            "role2_desc": "Ch00-04\n重點：Ch07-08",
            "role3_name": "Data Scientist",
            "role3_desc": "全修 Ch00-14\n重點：Ch10-12",
            "blindspot_banner_title": "初學者常見盲點 3 選",
            "outro_heading": "恭喜！課程地圖到手",
            "outro_sub": "下一站：Ch01 Python 基礎，開始寫程式吧！",
        },
        "en": {
            "title_main": "Course Roadmap",
            "title_sub": "An 18-Chapter Learning Guide",
            "acts_heading": "Five-Act Structure",
            "act1_label": "Act 1: Reported",
            "act2_label": "Act 2: Descriptive Analysis",
            "act3_label": "Act 3: Deeper Analysis",
            "act4_label": "Act 4: Advanced Modeling",
            "act5_label": "Act 5: Wrap-up & Practice",
            "mustdo_heading": "Required Path: Ch00 -> Ch04",
            "mustdo_ch0": "Intro & Tools",
            "mustdo_ch1": "Python Basics",
            "mustdo_ch2": "Data Wrangling",
            "mustdo_ch3": "Descriptive Stats",
            "mustdo_ch4": "Cluster Investigation",
            "choose_heading": "Elective Path: choose freely as needed",
            "elec_ch5": "Stratified Analysis",
            "elec_ch6": "Logistic Regression",
            "elec_ch7": "Time Series",
            "elec_ch8": "Spatial Epi",
            "elec_ch9": "Survival Analysis",
            "elec_ch10": "Machine Learning",
            "elec_ch11": "Deep Learning",
            "elec_ch12": "Causal Inference",
            "elec_ch13": "Reproducible Research",
            "elec_ch14": "Real-World Cases",
            "choose_note": "After finishing Ch00-04, jump around by interest",
            "summary_heading": "Learning Strategy",
            "summary_p1": "1. Ch00-04 are required - build the foundation first",
            "summary_p2": "2. Ch05-14 are electives by role and need",
            "summary_p3": "3. Every chapter shares the same Legionella dataset",
            "extra_banner_title": "Extra example: learning paths for different roles",
            "extra_heading": "Pick a Learning Path by Role",
            "role1_name": "Infection Control Nurse",
            "role1_desc": "Ch00-04\nFocus: Ch03-04",
            "role2_name": "Outbreak Investigator",
            "role2_desc": "Ch00-04\nFocus: Ch07-08",
            "role3_name": "Data Scientist",
            "role3_desc": "All Ch00-14\nFocus: Ch10-12",
            "blindspot_banner_title": "3 Common Beginner Blind Spots",
            "outro_heading": "Congrats! You've got the roadmap",
            "outro_sub": "Next stop: Ch01 Python Basics - let's start coding!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the Course Roadmap lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_five_acts(self, duration: float = 6.0, **kwargs) -> None:
        """Five-act structure visualization as a vertical column of cards."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            self.t("acts_heading"),
            font=FONT_CJK,
            font_size=32,
            color=ManimColor(TEXT_PRIMARY),
        ).to_edge(UP, buff=0.6)

        acts = [
            (self.t("act1_label"), "Ch00-02", ACCENT_ORANGE),
            (self.t("act2_label"), "Ch03-04", ACCENT_ORANGE),
            (self.t("act3_label"), "Ch05-08", ACCENT_BLUE),
            (self.t("act4_label"), "Ch09-12", ACCENT_BLUE),
            (self.t("act5_label"), "Ch13-14", ACCENT_GREEN),
        ]

        act_cards = VGroup()
        for act_label, chapters, accent in acts:
            card = _card(8.0, 0.7)
            label = Text(
                act_label,
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
            self.t("mustdo_heading"),
            font=FONT_CJK,
            font_size=30,
            color=ManimColor(ACCENT_ORANGE),
        ).to_edge(UP, buff=0.8)

        chapter_names = [
            ("Ch00", self.t("mustdo_ch0")),
            ("Ch01", self.t("mustdo_ch1")),
            ("Ch02", self.t("mustdo_ch2")),
            ("Ch03", self.t("mustdo_ch3")),
            ("Ch04", self.t("mustdo_ch4")),
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
            self.t("choose_heading"),
            font=FONT_CJK,
            font_size=30,
            color=ManimColor(ACCENT_BLUE),
        ).to_edge(UP, buff=0.8)

        electives = [
            ("Ch05", self.t("elec_ch5")),
            ("Ch06", self.t("elec_ch6")),
            ("Ch07", self.t("elec_ch7")),
            ("Ch08", self.t("elec_ch8")),
            ("Ch09", self.t("elec_ch9")),
            ("Ch10", self.t("elec_ch10")),
            ("Ch11", self.t("elec_ch11")),
            ("Ch12", self.t("elec_ch12")),
            ("Ch13", self.t("elec_ch13")),
            ("Ch14", self.t("elec_ch14")),
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
            self.t("choose_note"),
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
            self.t("summary_heading"),
            font=FONT_CJK,
            font_size=34,
            color=ManimColor(ACCENT_ORANGE),
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(
                self.t("summary_p1"),
                font=FONT_CJK, font_size=24, color=ManimColor(TEXT_PRIMARY),
            ),
            Text(
                self.t("summary_p2"),
                font=FONT_CJK, font_size=24, color=ManimColor(TEXT_PRIMARY),
            ),
            Text(
                self.t("summary_p3"),
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
        banner = ExtraExampleBanner(self.t("extra_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        """Three role cards showing recommended chapter paths."""
        self.show_step_indicator(5, self.total_steps)

        heading = Text(
            self.t("extra_heading"),
            font=FONT_CJK,
            font_size=28,
            color=ManimColor(ACCENT_BLUE),
        ).to_edge(UP, buff=0.8)

        roles = [
            (self.t("role1_name"), self.t("role1_desc"), ACCENT_ORANGE),
            (self.t("role2_name"), self.t("role2_desc"), ACCENT_BLUE),
            (self.t("role3_name"), self.t("role3_desc"), ACCENT_GREEN),
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
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_where_start(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: random chapter vs Ch00-01 first."""
        error_code = kwargs.get("error_code", "import sklearn  # Ch10 too early!")
        correct_code = kwargs.get("correct_code", "print('Hello, Epi!')  # Ch00 first")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_skip(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: skip Ch02 vs sequential for Ch00-04."""
        error_code = kwargs.get("error_code", "df.groupby(...)  # skip Ch02?")
        correct_code = kwargs.get("correct_code", "# Ch00 > Ch01 > Ch02 > Ch03")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_colab(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: Colab-only vs local install for full features."""
        error_code = kwargs.get("error_code", "# Colab only = no offline")
        correct_code = kwargs.get("correct_code", "uv sync  # local = full power")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card: congratulations, go to Ch01."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            self.t("outro_heading"),
            font=FONT_CJK,
            font_size=32,
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
