"""Ch00-01: 為什麼用 Python——流行病學家的超級工具

Manim scene for the tutorial video on why epidemiologists should learn Python.
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
    ERROR_RED,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    CodePanel,
    ErrorVsCorrect,
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


class Ch00WhyPythonScene(EpiBaseScene):
    """Tutorial video scene: why epidemiologists should learn Python."""

    total_steps: int = 12

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the Why Python lesson."""
        self.show_title_card("為什麼用 Python", "流行病學家的超級工具", duration=duration)

    def show_excel_limit(self, duration: float = 6.0, **kwargs) -> None:
        """Show Excel pain points as three cards."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "Excel 的三大痛點",
            font=FONT_CJK,
            font_size=32,
            color=TEXT_PRIMARY,
        ).to_edge(UP, buff=0.8)

        cards = VGroup(
            self._make_pain_card("1", "資料量上限", "最多 104 萬行\n大型疫調容易爆掉"),
            self._make_pain_card("2", "手動重複操作", "每次分析都要\n重新點選設定"),
            self._make_pain_card("3", "無法重現", "別人無法精確\n複製你的步驟"),
        ).arrange(RIGHT, buff=0.5).move_to(ORIGIN + DOWN * 0.2)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(cards, lag_ratio=0.3), run_time=1.2)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(heading, cards)), run_time=0.5)

    def show_python_power(self, duration: float = 6.0, **kwargs) -> None:
        """Show Python advantages with a code example."""
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            "Python 一行搞定",
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        code_panel = CodePanel(
            "infected = 121\n"
            "total    = 280\n"
            "\n"
            "attack_rate = infected / total\n"
            "print(f'侵襲率: {attack_rate:.1%}')",
            title="Python",
        ).move_to(ORIGIN + UP * 0.2)

        note = Text(
            "可重現、可自動化、可分享",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(code_panel, DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(Create(code_panel), run_time=1.0)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(max(0.1, duration - 2.5))
        self.play(FadeOut(VGroup(heading, code_panel, note)), run_time=0.5)

    def show_python_vs_r(self, duration: float = 6.0, **kwargs) -> None:
        """Side-by-side comparison cards: Python vs R."""
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            "Python vs R — 選哪個？",
            font=FONT_CJK,
            font_size=32,
            color=TEXT_PRIMARY,
        ).to_edge(UP, buff=0.8)

        python_card = self._make_compare_card(
            "Python",
            ACCENT_ORANGE,
            [
                "泛用型語言",
                "ML / DL 生態系最強",
                "自動化、網頁、API 都行",
                "學一次用到處",
            ],
        ).shift(LEFT * 3.2)

        r_card = self._make_compare_card(
            "R",
            ACCENT_BLUE,
            [
                "統計學起家",
                "ggplot2 繪圖超美",
                "生物統計套件多",
                "學術論文常見",
            ],
        ).shift(RIGHT * 3.2)

        note = Text(
            "兩個都好！本課程選 Python 因為泛用性更高",
            font=FONT_CJK,
            font_size=20,
            color=TEXT_SECONDARY,
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(python_card), FadeIn(r_card), run_time=1.0)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(max(0.1, duration - 2.5))
        self.play(FadeOut(VGroup(heading, python_card, r_card, note)), run_time=0.5)

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        """Summarise three key points."""
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            "重點整理",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(
                "1. Excel 有行數上限、不可重現",
                font=FONT_CJK, font_size=24, color=TEXT_PRIMARY,
            ),
            Text(
                "2. Python 可自動化分析、處理大數據",
                font=FONT_CJK, font_size=24, color=TEXT_PRIMARY,
            ),
            Text(
                "3. 寫程式 = 寫分析紀錄，天然可重現",
                font=FONT_CJK, font_size=24, color=TEXT_PRIMARY,
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
        banner = ExtraExampleBanner("額外範例：COVID-19 大規模疫調")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        """Code showing pandas processing 100k records."""
        self.show_step_indicator(5, self.total_steps)

        code_lines = (
            "import pandas as pd\n"
            "\n"
            "# 讀取十萬筆 COVID-19 通報資料\n"
            "df = pd.read_csv('covid_100k.csv')\n"
            "print(f'共 {len(df):,} 筆資料')\n"
            "\n"
            "# 一行算出各縣市侵襲率\n"
            "rate = df.groupby('county').apply(\n"
            "    lambda g: g['confirmed'].sum() / g['population'].iloc[0]\n"
            ")"
        )

        heading = Text(
            "十萬筆資料？Python 幾秒搞定",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_BLUE,
        ).to_edge(UP, buff=0.8)

        code_panel = CodePanel(
            code_lines, title="covid_analysis.py",
        ).move_to(ORIGIN + DOWN * 0.2)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(Create(code_panel), run_time=1.2)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(heading, code_panel)), run_time=0.5)

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner("初學者常見盲點 3 選")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_math(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: myth about needing strong math vs reality."""
        error_code = kwargs.get("error_code", "import advanced_math")
        correct_code = kwargs.get("correct_code", "attack_rate = 121 / 280")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_learn_first(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: learn everything first vs learn by doing."""
        error_code = kwargs.get("error_code", "study(python, years=3)")
        correct_code = kwargs.get("correct_code", "print(121 / 280)")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_version(self, duration: float = 5.0, **kwargs) -> None:
        """ErrorVsCorrect: manual Python install vs uv."""
        error_code = kwargs.get("error_code", "pip install pandas==1.5")
        correct_code = kwargs.get("correct_code", "uv sync")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card teasing the next video."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            "下一集：安裝 uv 與建立開發環境",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "三分鐘搞定 Python 環境，馬上開始寫程式！",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(max(0.1, duration - 1.6))
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _make_pain_card(self, number: str, title: str, desc: str) -> VGroup:
        """Create a pain-point card with number badge, title, and description."""
        card = _card(3.5, 3.0)

        badge = Text(
            number, font=FONT_MONO, font_size=36,
            color=ManimColor(ERROR_RED), weight="BOLD",
        ).move_to(card.get_top() + DOWN * 0.4)

        title_mob = Text(
            title, font=FONT_CJK, font_size=24,
            color=ManimColor(TEXT_PRIMARY), weight="BOLD",
        ).next_to(badge, DOWN, buff=0.25)

        desc_mob = Text(
            desc, font=FONT_CJK, font_size=18,
            color=ManimColor(TEXT_SECONDARY),
            line_spacing=1.2,
        ).next_to(title_mob, DOWN, buff=0.3)

        return VGroup(card, badge, title_mob, desc_mob)

    def _make_compare_card(
        self, title: str, accent: str, points: list[str],
    ) -> VGroup:
        """Create a comparison card with a coloured title and bullet points."""
        card = _card(5.0, 4.0)

        title_mob = Text(
            title, font=FONT_CJK, font_size=30,
            color=ManimColor(accent), weight="BOLD",
        ).move_to(card.get_top() + DOWN * 0.45)

        bullet_group = VGroup()
        for pt in points:
            line = Text(
                f"  {pt}",
                font=FONT_CJK, font_size=20,
                color=ManimColor(TEXT_PRIMARY),
            )
            bullet_group.add(line)
        bullet_group.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        bullet_group.next_to(title_mob, DOWN, buff=0.35)

        return VGroup(card, title_mob, bullet_group)
