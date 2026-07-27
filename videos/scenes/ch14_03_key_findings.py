"""Ch14-03: Key findings - distill the investigation to the numbers that matter.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages. The key numbers are drawn as a small stat-card dashboard built from
``RoundedRectangle`` + ``Text`` (no new mobjects).
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
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
    ACCENT_BLUE,
    ACCENT_GREEN,
    ACCENT_ORANGE,
    BG_CARD,
    ERROR_RED,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch14KeyFindingsScene(EpiBaseScene):
    """Tutorial video scene: the key-findings summary that carries the report."""

    total_steps: int = 9

    _STAT_ACCENTS = [ACCENT_BLUE, ACCENT_ORANGE, ACCENT_ORANGE, ERROR_RED, ERROR_RED, ACCENT_GREEN]

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "主要發現摘要",
            "title_sub": "把整場調查，濃縮成長官最想看的幾個數字",
            "what_heading": "主要發現摘要是什麼？",
            "what_lines": [
                "把一整場疫調濃縮成「重點數字」",
                "不是把所有分析都倒出來",
                "精挑能撐起結論的關鍵數字",
                "→ 規模、嚴重度、最可疑的暴露",
            ],
            "numbers_heading": "松柏護理之家：關鍵數字",
            "stat_values": ["280", "121", "43.2%", "19", "15.7%", "淋浴"],
            "stat_labels": ["住民數", "感染人數", "侵襲率", "死亡人數", "致死率", "主要危險因子"],
            "context_heading": "數字要有比較基準",
            "context_lines": [
                "43.2% 算高嗎？15.7% 呢？",
                "每個關鍵數字都要附上基準",
                "退伍軍人症一般致死率約 10%",
                "→ 我們 15.7% 偏高，數字才有故事",
            ],
            "conclusion_heading": "收成一句可行動的結論",
            "conclusion_lines": [
                "流行曲線 → 共同暴露源",
                "空間熱點 → 特定樓層",
                "淋浴暴露 adjusted OR 仍顯著",
                "→ 結論：淋浴供水系統為最可能感染源",
            ],
            "summary_heading": "主要發現三重點",
            "summary_lines": [
                "① 精挑關鍵數字，不是全部倒出",
                "② 每個數字都要有比較基準",
                "③ 最後收成一句可行動的結論",
                "→ 這段寫好，報告就有了靈魂",
            ],
            "extra_banner_title": "額外範例：給長官的一頁摘要",
            "extra_boss_heading": "COVID-19：一張投影片講完",
            "extra_boss_lines": [
                "當日新增、七日平均",
                "陽性率、重症佔比",
                "一句話：趨勢上升，建議加開篩檢站",
                "→ 少即是多：四個數字 + 一句建議",
            ],
            "blindspot_banner_title": "主要發現三個新手地雷",
            "outro_heading": "下一集：一鍵輸出 PPTX 簡報",
            "outro_sub": "python-pptx：記憶體 PNG → 投影片",
        },
        "en": {
            "title_main": "The Key-Findings Summary",
            "title_sub": "Distill the whole investigation to the numbers that matter",
            "what_heading": "What Is a Key-Findings Summary?",
            "what_lines": [
                'Distill the whole investigation to "the key numbers"',
                "Not a dump of every analysis you ran",
                "Hand-pick the numbers that carry the conclusion",
                "-> scale, severity, the top suspect exposure",
            ],
            "numbers_heading": "The Nursing Home: Key Numbers",
            "stat_values": ["280", "121", "43.2%", "19", "15.7%", "Shower"],
            "stat_labels": [
                "residents",
                "infected",
                "attack rate",
                "deaths",
                "case fatality",
                "top risk factor",
            ],
            "context_heading": "Numbers Need a Benchmark",
            "context_lines": [
                "Is 43.2% high? What about 15.7%?",
                "Every key number needs a comparison baseline",
                "Legionnaires' case fatality runs about 10%",
                "-> our 15.7% is high, so the number tells a story",
            ],
            "conclusion_heading": "Land on One Actionable Conclusion",
            "conclusion_lines": [
                "Epi curve -> a common source",
                "Spatial hotspot -> a specific floor",
                "Shower exposure adjusted OR still significant",
                "-> Conclusion: the shower supply is the likely source",
            ],
            "summary_heading": "Three Takeaways on Key Findings",
            "summary_lines": [
                "1. Hand-pick key numbers, not a full dump",
                "2. Every number needs a benchmark",
                "3. Land on one actionable conclusion",
                "-> write this well and the report gets a soul",
            ],
            "extra_banner_title": "Extra example: a one-slide summary for the boss",
            "extra_boss_heading": "COVID-19: one slide says it all",
            "extra_boss_lines": [
                "Daily new cases, 7-day average",
                "Positivity rate, severe-case share",
                "One line: trend rising, open more testing sites",
                "-> less is more: four numbers + one recommendation",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: export a PPTX deck in one click",
            "outro_sub": "python-pptx: in-memory PNG -> slide",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _bullets(self, heading_key: str, lines_key: str, duration: float) -> None:
        heading = self.t(heading_key)
        lines = self.t(lines_key)
        h = Text(heading, font=FONT_CJK, font_size=30, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        bl = (
            VGroup(*[Text(x, font=FONT_CJK, font_size=22, color=TEXT_PRIMARY) for x in lines])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            .next_to(h, DOWN, buff=0.55)
        )
        if bl.width > 12.5:
            bl.scale_to_fit_width(12.5)
        self.play(FadeIn(h), run_time=0.5)
        self.play(FadeIn(bl, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(h, bl)), run_time=0.5)

    def _stat_card(self, value: str, label: str, accent: str) -> VGroup:
        card = RoundedRectangle(
            corner_radius=0.15,
            width=2.9,
            height=1.7,
            fill_color=ManimColor(BG_CARD),
            fill_opacity=1,
            stroke_color=ManimColor(accent),
            stroke_width=2.5,
        )
        num = Text(value, font=FONT_CJK, font_size=34, color=accent, weight="BOLD")
        lab = Text(label, font=FONT_CJK, font_size=17, color=TEXT_SECONDARY)
        inner = VGroup(num, lab).arrange(DOWN, buff=0.18).move_to(card.get_center())
        return VGroup(card, inner)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_what_key_findings(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("what_heading", "what_lines", duration)

    def show_the_numbers(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            self.t("numbers_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)

        values = self.t("stat_values")
        labels = self.t("stat_labels")
        cards = [
            self._stat_card(value, label, self._STAT_ACCENTS[i % len(self._STAT_ACCENTS)])
            for i, (value, label) in enumerate(zip(values, labels))
        ]
        row1 = VGroup(*cards[:3]).arrange(RIGHT, buff=0.4)
        row2 = VGroup(*cards[3:]).arrange(RIGHT, buff=0.4)
        grid = VGroup(row1, row2).arrange(DOWN, buff=0.45)
        if grid.width > 12.6:
            grid.scale_to_fit_width(12.6)
        grid.move_to(DOWN * 0.2)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(grid, lag_ratio=0.15), run_time=1.6)
        self.wait(max(0.1, duration - 2.4))
        self.play(FadeOut(VGroup(heading, grid)), run_time=0.5)

    def show_context_matters(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets("context_heading", "context_lines", duration)

    def show_one_line_conclusion(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("conclusion_heading", "conclusion_lines", duration)

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_boss_slide(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("extra_boss_heading", "extra_boss_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_no_context(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'show(f"CFR {cfr:.1%}")'),
            kwargs.get("correct_code", 'show(f"CFR {cfr:.1%} vs {natl:.1%}")'),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_wrong_denominator(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "cfr = deaths / n_total"),
            kwargs.get("correct_code", "cfr = deaths / n_infected"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_cherry_pick(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "finding = crude_or"),
            kwargs.get("correct_code", "finding = adjusted_or  # ctrl confounders"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text(self.t("outro_heading"), font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).move_to(
            ORIGIN + UP * 0.5
        )
        s = Text(self.t("outro_sub"), font=FONT_CJK, font_size=20, color=TEXT_SECONDARY).next_to(
            h, DOWN, buff=0.4
        )
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
