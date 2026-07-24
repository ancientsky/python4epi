"""Ch14-02: Report structure - the 8-paragraph outbreak report mapped to chapter skills.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages. The eight-section skeleton is drawn as a document mockup from
``RoundedRectangle`` + ``Text`` (no new mobjects).
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
    ACCENT_ORANGE,
    BG_CARD,
    BORDER_LIGHT,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch14ReportStructureScene(EpiBaseScene):
    """Tutorial video scene: the 8-paragraph report structure and chapter mapping."""

    total_steps: int = 9

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "報告的八個段落",
            "title_sub": "標準疫調格式 ↔ 每段對應一章技能",
            "why_heading": "為什麼要固定架構？",
            "why_lines": [
                "疫調報告是給人「照著做」的公文",
                "八段落格式 → 每次排版都一致",
                "讀者知道第幾段找什麼",
                "→ 自己也不會漏掉「行動建議」",
            ],
            "eight_heading": "報告骨架：八個段落",
            "eight_rows": [
                "① 背景與通報　　　　Ch00 · Ch04",
                "② 方法與 line list　　Ch02",
                "③ 描述性流行病學　　Ch02–04",
                "④ 分析性流行病學　　Ch03 · 05 · 06",
                "⑤ 時間與空間分析　　Ch07 · Ch08",
                "⑥ 進階分析　　　　　Ch09–11",
                "⑦ 因果研判與建議　　Ch12",
                "⑧ 結論與行動建議　　總整理",
            ],
            "map_heading": "段落 ↔ 章節技能",
            "map_lines": [
                "背景通報 → 個案定義（Ch00, 04）",
                "方法 → line list 清理（Ch02）",
                "描述性 → 人時地分布（Ch02–04）",
                "分析性 → 2×2、分層、adjusted OR（Ch03,05,06）",
                "時間空間 → 時序分解、熱點（Ch07, 08）",
            ],
            "consistency_heading": "固定格式的好處",
            "consistency_lines": [
                "可重現：這次跟下次長得一樣",
                "好比較：跨案件一段對一段",
                "不漏段：關鍵段落不會被忘掉",
                "→ Ch13 的延伸：同一張菜單，誰做都一樣",
            ],
            "summary_heading": "報告架構三重點",
            "summary_lines": [
                "① 標準報告有八個固定段落",
                "② 每段對應前面某一章的技能",
                "③ 固定格式 → 可重現、好比較、不漏段",
                "→ 骨架搭好，接著把數字填進去",
            ],
            "extra_banner_title": "額外範例：食因性群聚報告",
            "extra_foodborne_heading": "尾牙食物中毒，塞進八段落",
            "extra_foodborne_lines": [
                "背景 → 宴會後多人腹瀉通報",
                "描述 → 發病時間曲線",
                "分析 → 食物別侵襲率 2×2，揪出哪道菜",
                "因果 → 指向那盤生魚片",
            ],
            "blindspot_banner_title": "報告架構三個新手地雷",
            "outro_heading": "下一集：主要發現摘要",
            "outro_sub": "把整場調查，濃縮成長官最想看的幾個數字",
        },
        "en": {
            "title_main": "The Eight Report Sections",
            "title_sub": "Standard format <-> each section maps to a chapter",
            "why_heading": "Why a Fixed Structure?",
            "why_lines": [
                'A report is an official document people "follow"',
                "Eight-section format -> consistent layout every time",
                "Readers know which section holds what",
                '-> and you never drop the "action items"',
            ],
            "eight_heading": "The Skeleton: Eight Sections",
            "eight_rows": [
                "1  Background & notification    Ch00 · Ch04",
                "2  Methods & line list          Ch02",
                "3  Descriptive epidemiology     Ch02-04",
                "4  Analytic epidemiology        Ch03 · 05 · 06",
                "5  Time & space analysis        Ch07 · Ch08",
                "6  Advanced analysis            Ch09-11",
                "7  Causal assessment & advice   Ch12",
                "8  Conclusion & action items    Summary",
            ],
            "map_heading": "Section <-> Chapter Skill",
            "map_lines": [
                "Background -> case definition (Ch00, 04)",
                "Methods -> line-list cleaning (Ch02)",
                "Descriptive -> person-place-time (Ch02-04)",
                "Analytic -> 2x2, strata, adjusted OR (Ch03,05,06)",
                "Time & space -> decomposition, hotspots (Ch07, 08)",
            ],
            "consistency_heading": "Why a Fixed Format Wins",
            "consistency_lines": [
                "Reproducible: this one looks like the next",
                "Comparable: match section-by-section across cases",
                "Complete: key sections never get forgotten",
                "-> Ch13 extended: same menu, same result",
            ],
            "summary_heading": "Three Takeaways on Structure",
            "summary_lines": [
                "1. A standard report has eight fixed sections",
                "2. Each section maps to an earlier chapter's skill",
                "3. Fixed format -> reproducible, comparable, complete",
                "-> skeleton set, now fill in the numbers",
            ],
            "extra_banner_title": "Extra example: a foodborne-outbreak report",
            "extra_foodborne_heading": "Banquet food poisoning into eight sections",
            "extra_foodborne_lines": [
                "Background -> diarrhea reports after the banquet",
                "Descriptive -> onset-time curve",
                "Analytic -> food-specific attack rate 2x2, find the dish",
                "Causal -> points to the plate of sashimi",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: the key-findings summary",
            "outro_sub": "Distill the whole investigation to the numbers the boss wants",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helper
    # ------------------------------------------------------------------

    def _bullets(self, heading_key: str, lines_key: str, duration: float) -> None:
        heading = self.t(heading_key)
        lines = self.t(lines_key)
        h = Text(heading, font=FONT_CJK, font_size=30, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        bl = (
            VGroup(*[Text(x, font=FONT_CJK, font_size=22, color=TEXT_PRIMARY) for x in lines])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.38)
            .next_to(h, DOWN, buff=0.55)
        )
        if bl.width > 12.5:
            bl.scale_to_fit_width(12.5)
        self.play(FadeIn(h), run_time=0.5)
        self.play(FadeIn(bl, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(h, bl)), run_time=0.5)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_why_structure(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("why_heading", "why_lines", duration)

    def show_eight_paragraphs(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            self.t("eight_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.5)

        rows = self.t("eight_rows")
        page = RoundedRectangle(
            corner_radius=0.15,
            width=9.6,
            height=5.2,
            fill_color=ManimColor(BG_CARD),
            fill_opacity=1,
            stroke_color=ManimColor(BORDER_LIGHT),
            stroke_width=2,
        )
        lines = VGroup(
            *[Text(r, font=FONT_CJK, font_size=18, color=TEXT_PRIMARY) for r in rows]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        if lines.width > 8.9:
            lines.scale_to_fit_width(8.9)
        lines.move_to(page.get_center())
        doc = VGroup(page, lines).next_to(heading, DOWN, buff=0.35)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(page), run_time=0.5)
        self.play(FadeIn(lines, lag_ratio=0.15), run_time=1.6)
        self.wait(max(0.1, duration - 2.9))
        self.play(FadeOut(VGroup(heading, doc)), run_time=0.5)

    def show_section_chapter_map(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets("map_heading", "map_lines", duration)

    def show_consistency(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("consistency_heading", "consistency_lines", duration)

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

    def show_extra_foodborne(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("extra_foodborne_heading", "extra_foodborne_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_no_structure(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "write(sections_in_random_order)"),
            kwargs.get("correct_code", "write(SITREP_8_SECTIONS)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_action_section(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "sections = [bg, methods, results]"),
            kwargs.get("correct_code", "sections += [conclusion, actions]"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_mix_desc_analytic(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "mix(descriptive, analytic)"),
            kwargs.get("correct_code", "describe_first(); then_analyze()"),
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
